"""Gateway tests with fake transports. No network, no credentials."""

import json
from pathlib import Path

import pytest

from astral_b1.contracts import render_view
from astral_b1.environment import generate
from astral_b1.gateway import (
    AttemptLog,
    IdentityMismatch,
    JudgeSpec,
    OpenRouterJudge,
    ResponseCache,
    build_request,
    parse_verdict,
)
from astral_b1.runner import replay, run_live

SPEC = JudgeSpec(model="anthropic/claude-sonnet-5.5", provider="anthropic")


def ok_payload(text, model=SPEC.model, provider="Anthropic"):
    return 200, {"id": "gen-1", "model": model, "provider": provider,
                 "choices": [{"message": {"content": text}, "finish_reason": "stop"}],
                 "usage": {"prompt_tokens": 10, "completion_tokens": 5, "cost": 0.0001}}


def make_judge(tmp_path: Path, transport):
    return OpenRouterJudge(SPEC, ResponseCache(tmp_path / "cache"), AttemptLog(tmp_path / "attempts.jsonl"),
                           transport=transport, sleep=lambda s: None)


@pytest.fixture
def view():
    (ep,), _ = generate(7, 1)
    return render_view(ep)


def test_request_pins_route_and_forbids_fallback(view):
    body = build_request(SPEC, view)
    assert body["provider"] == {"only": ["anthropic"], "allow_fallbacks": False, "require_parameters": True}
    assert body["model"] == SPEC.model
    assert "temperature" not in body


def test_prompt_excludes_prior_judge_results():
    from astral_b1.contracts import JudgeResult
    (ep,), _ = generate(7, 1)
    prior = JudgeResult("x", "1", "s", "h", "ok", True, "SENTINEL_PRIOR_RATIONALE")
    v = render_view(ep, (), (prior,))
    text = json.dumps(build_request(SPEC, v))
    for bad in ("SENTINEL_PRIOR_RATIONALE", "judge_history", "oracle", "family"):
        assert bad not in text


def test_parse_verdict_cases():
    assert parse_verdict('{"violation": true, "reason": "x"}') == ("ok", True, "x")
    assert parse_verdict('prefix {"violation": false, "reason": "y"} suffix')[:2] == ("ok", False)
    assert parse_verdict('{"violation": null, "reason": "unsure"}')[0] == "abstain"
    assert parse_verdict("no json here")[0] == "parse_error"
    assert parse_verdict('{"verdict": true}')[0] == "parse_error"
    assert parse_verdict('{"violation": "yes"}')[0] == "parse_error"


def test_cache_hit_makes_no_network_call(tmp_path, view):
    calls = []

    def transport(body):
        calls.append(body)
        return ok_payload('{"violation": true, "reason": "r"}')

    j = make_judge(tmp_path, transport)
    a = j(view, "arm:ep:s0")
    b = j(view, "arm:ep:s0")
    assert a == b and len(calls) == 1 and j.cache_hits == 1


def test_independent_samples_do_not_collapse(tmp_path, view):
    n = {"i": 0}

    def transport(body):
        n["i"] += 1
        return ok_payload(json.dumps({"violation": n["i"] % 2 == 0, "reason": str(n["i"])}))

    j = make_judge(tmp_path, transport)
    a = j(view, "arm:ep:s0")
    b = j(view, "arm:ep:s1")
    assert a.request_hash == b.request_hash
    assert a.sample_id != b.sample_id and a.verdict != b.verdict and n["i"] == 2


def test_retry_on_429_then_success_is_logged(tmp_path, view):
    seq = [(429, {"error": {"message": "rate limited"}}), ok_payload('{"violation": false, "reason": "ok"}')]
    j = make_judge(tmp_path, lambda body: seq.pop(0))
    r = j(view, "arm:ep:s0")
    assert r.status == "ok" and j.network_calls == 2
    rows = [json.loads(l) for l in (tmp_path / "attempts.jsonl").read_text().splitlines()]
    assert [x["http_status"] for x in rows] == [429, 200]


def test_non_retryable_error_is_recorded_not_retried(tmp_path, view):
    j = make_judge(tmp_path, lambda body: (400, {"error": {"message": "bad request"}}))
    r = j(view, "arm:ep:s0")
    assert r.status == "request_failed" and j.network_calls == 1
    assert "400" in r.rationale


def test_exhausted_retries_recorded(tmp_path, view):
    j = make_judge(tmp_path, lambda body: (503, {"error": {"message": "down"}}))
    r = j(view, "arm:ep:s0")
    assert r.status == "request_failed" and j.network_calls == 3


def test_parse_error_is_a_result_not_a_retry(tmp_path, view):
    j = make_judge(tmp_path, lambda body: ok_payload("I think it is fine."))
    r = j(view, "arm:ep:s0")
    assert r.status == "parse_error" and j.network_calls == 1


def test_content_filter_is_recorded_as_refusal(tmp_path, view):
    payload = ok_payload("")
    payload[1]["choices"][0]["finish_reason"] = "content_filter"
    j = make_judge(tmp_path, lambda body: payload)
    r = j(view, "arm:ep:s0")
    assert r.status == "refusal" and r.verdict is None and j.network_calls == 1


def test_identity_mismatch_fails_loudly(tmp_path, view):
    j = make_judge(tmp_path, lambda body: ok_payload('{"violation": true}', model="anthropic/claude-sonnet-5"))
    with pytest.raises(IdentityMismatch):
        j(view, "arm:ep:s0")
    j2 = make_judge(tmp_path / "b", lambda body: ok_payload('{"violation": true}', provider="Amazon Bedrock"))
    with pytest.raises(IdentityMismatch):
        j2(view, "arm:ep:s0")


def test_live_run_resumes_from_cache_and_replays(tmp_path):
    calls = {"n": 0}

    def transport(body):
        calls["n"] += 1
        flag = "not_approved" in json.dumps(body) or "without" in json.dumps(body)
        return ok_payload(json.dumps({"violation": flag, "reason": "fixture"}))

    out = tmp_path / "live"
    report = run_live(out, [SPEC], tmp_path / "cache", seed=0, n_episodes=6, workers=2, transport=transport)
    first = calls["n"]
    assert first > 0 and set(report["arms"]) == {f"{c}+claude-sonnet-5.5" for c in
                                                 ("stop", "retrieve_registry", "retrieve_request", "status_aware", "random")}
    # Crash/resume: a second run over the same cache makes zero network calls and matches.
    out2 = tmp_path / "live2"
    report2 = run_live(out2, [SPEC], tmp_path / "cache", seed=0, n_episodes=6, workers=2, transport=transport)
    assert calls["n"] == first and report2 == report
    assert replay(out) and replay(out2)
    m = json.loads((out2 / "manifest.json").read_text())
    assert m["stage"] == "development_live"
    assert m["config"]["gateway"]["claude-sonnet-5.5"]["network_calls"] == 0
