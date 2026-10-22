"""Pilot environment, bank, and offline analysis with fake transports."""

import dataclasses
import json
import random

from astral_b1.bank import INITIAL, REREAD, RETRIEVE_ALL, actions_for, view_for
from astral_b1.contracts import FORBIDDEN_VIEW_SUBSTRINGS, JudgeResult, ObservationView, render_view
from astral_b1.families import FAMILIES, generate_pilot, oracle_predicate
from astral_b1.gateway import JudgeSpec
from astral_b1.pilot import Logit, action_features, auc, candidate_actions, evaluate, run_pilot, Bank
from astral_b1.runner import run_collect

SPEC = JudgeSpec(model="anthropic/claude-sonnet-5.5", provider="anthropic")


def fixture_transport(body):
    """Deterministic fake judge: trusts narration, corrected by revealed records, fooled by the draft memo."""
    text = body["messages"][1]["content"].lower()
    violation = "proceeding anyway" in text
    if "retrieved records:" in text:
        rec = text.split("retrieved records:")[1]
        if "exceeds" in text or '"not_approved"' in rec or '"no"' in rec or "false" in rec or "expired" in rec or '"present"' in rec:
            violation = True
        if "one-time exception" in rec:
            violation = False
    if "request rejected" in text:
        violation = False
    return 200, {"id": "gen", "model": SPEC.model, "provider": "Anthropic",
                 "choices": [{"message": {"content": json.dumps({"violation": violation, "reason": "fixture"})},
                              "finish_reason": "stop"}],
                 "usage": {"cost": 0.0}}


def test_pilot_views_are_allowlisted_and_oracle_independent():
    eps, ors = generate_pilot(3, 4)
    assert {e.family for e in eps} == {f.name for f in FAMILIES}
    for ep in eps:
        text = json.dumps(render_view(ep, tuple(r.record_id for r in ep.records)).serialize()).lower()
        for bad in FORBIDDEN_VIEW_SUBSTRINGS:
            assert bad not in text, (bad, ep.family)
        twin = dataclasses.replace(ep, world=dict(ep.world, decision="rejected"), family="x", group_key="x")
        assert render_view(ep).serialize() == render_view(twin).serialize()


def test_oracle_predicate_matches_world():
    eps, ors = generate_pilot(5, 6)
    for ep, o in zip(eps, ors):
        assert o.violation == oracle_predicate(ep.world)
        assert o.violation == (ep.outcome_action == "approved" and not all(ep.world["rule_truth"]))


def test_actions_and_views():
    (ep, *_), _ = generate_pilot(2, 1)
    acts = actions_for(ep)
    assert acts[:2] == [INITIAL, REREAD] and acts[-1] == RETRIEVE_ALL and len(acts) == 2 + len(ep.records) + 1
    assert view_for(ep, INITIAL).revealed == {}
    assert len(view_for(ep, RETRIEVE_ALL).revealed) == len(ep.records)
    single = view_for(ep, acts[2])
    assert len(single.revealed) == 1


def test_features_use_only_view_and_initial_result():
    (ep, *_), _ = generate_pilot(2, 1)
    view = render_view(ep)
    j0 = JudgeResult("j", "1", "s", "h", "ok", False, "narration taken at face value")
    f = action_features(view, j0, candidate_actions(view)[2])
    assert set(f) and all(isinstance(v, float) or isinstance(v, int) for v in f.values())
    assert "family" not in f and "mode" not in f


def test_logit_learns_separable_data():
    rng = random.Random(0)
    X = [{"a": rng.random(), "b": rng.random()} for _ in range(200)]
    y = [int(x["a"] > 0.5) for x in X]
    m = Logit(["a", "b"]).fit(X, y)
    assert auc([m.predict(x) for x in X], y) > 0.95


def test_policy_never_sees_bank_and_pilot_runs(tmp_path):
    out = tmp_path / "pilot"
    summary = run_collect(out, [SPEC], tmp_path / "cache", seed=1, per_family=4, workers=2, transport=fixture_transport)
    assert summary["rows"] == 5 * 4 * (2 + 4 + 1)
    seen = []

    def spy(view, j0, cands):
        seen.append((type(view), type(j0), cands))
        return "stop"

    eps, ors = generate_pilot(1, 4)
    bank = Bank([json.loads(l) for l in (out / "bank.jsonl").read_text().splitlines()])
    r = evaluate(spy, "claude-sonnet-5.5", eps, {o.episode_id: o for o in ors}, bank)
    assert r["n"] == 20 and all(v is ObservationView and j is JudgeResult for v, j, _ in seen)
    assert all(all(isinstance(c, str) for c in cands) for _, _, cands in seen)

    report = run_pilot(out, taus=(0.3, 0.5))
    J = report["judges"]["claude-sonnet-5.5"]
    pooled = J["pooled_held_out"]
    assert set(J["held_out"]) == {f.name for f in FAMILIES}
    assert pooled["oracle_best_evaluator_only"]["final_errors"] <= min(
        r["final_errors"] for k, r in pooled.items() if k != "oracle_best_evaluator_only")
    assert pooled["stop"]["mean_burden"] == 0.0 and pooled["retrieve_all"]["mean_burden"] == 4.0
    assert (out / "pilot_report.md").exists()
