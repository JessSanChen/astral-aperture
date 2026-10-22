"""Offline pilot analysis over a collected response bank.

Three questions, in order:
  1. Headroom: do single-step inspections change judge errors, and in which direction?
  2. Predictability: can allowed information predict which inspection helps?
  3. Transfer: does a controller trained on four families work on the fifth?

Boundary: a policy sees (view, initial judge result, candidate action names) and
returns one action. The bank is consulted only by the evaluator after the choice.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable

from .bank import INITIAL, REREAD, RETRIEVE_ALL, read_bank
from .contracts import Episode, JudgeResult, ObservationView, OracleRecord, render_view
from .families import FAMILIES, generate_pilot

HEDGE_WORDS = ("appears", "as far as i can tell", "seems", "presumably")
RATIONALE_DOUBT = ("narration", "unverified", "cannot verify", "claims", "self-reported",
                   "not retrieved", "no records", "taken at face value")
STOP = "stop"


def _err(verdict: bool | None, truth: bool) -> int:
    return 0 if verdict == truth else 1


# ---------------------------------------------------------------- features (allowed info only)

def line_for_kind(view: ObservationView, kind: str) -> str | None:
    tokens = [t for t in kind.split("_") if t]
    for m in view.messages:
        low = m.lower()
        if "check:" in low and all(t in low for t in tokens):
            return m
    return None


def episode_features(view: ObservationView, j0: JudgeResult) -> dict[str, float]:
    checks = [m for m in view.messages if "check:" in m.lower()]
    text = " ".join(view.messages).lower()
    rat = (j0.rationale or "").lower()
    n_hedged = sum(any(h in m.lower() for h in HEDGE_WORDS) for m in checks)
    n_ref = sum("(see " in m for m in checks)
    return {
        "n_checks": len(checks),
        "handles_minus_checks": len(view.record_handles) - len(checks),
        "n_hedged": n_hedged,
        "n_unreferenced": len(checks) - n_ref,
        "admits": float("proceeding anyway" in text),
        "rejected": float("request rejected" in text),
        "j0_violation": float(j0.verdict is True),
        "j0_unresolved": float(j0.verdict is None),
        "rationale_doubt": float(sum(w in rat for w in RATIONALE_DOUBT)),
    }


def action_features(view: ObservationView, j0: JudgeResult, action: str) -> dict[str, float]:
    f = episode_features(view, j0)
    f.update({"is_reread": float(action == REREAD), "is_all": float(action == RETRIEVE_ALL),
              "is_single": float(action.startswith("retrieve:")),
              "line_hedged": 0.0, "line_unreferenced": 0.0, "line_missing": 0.0, "kind_in_rationale": 0.0})
    if action.startswith("retrieve:"):
        kind = action.split(":", 1)[1]
        line = line_for_kind(view, kind)
        if line is None:
            f["line_missing"] = 1.0
        else:
            f["line_hedged"] = float(any(h in line.lower() for h in HEDGE_WORDS))
            f["line_unreferenced"] = float("(see " not in line)
        rat = (j0.rationale or "").lower()
        f["kind_in_rationale"] = float(any(t in rat for t in kind.split("_") if len(t) > 3))
    return f


CUE_FEATURES = ("n_hedged", "n_unreferenced", "line_hedged", "line_unreferenced", "line_missing", "handles_minus_checks")


# ---------------------------------------------------------------- tiny logistic regression

class Logit:
    def __init__(self, names: list[str], l2: float = 0.05, lr: float = 0.1, epochs: int = 500):
        self.names = names
        self.l2, self.lr, self.epochs = l2, lr, epochs
        self.mu = {n: 0.0 for n in names}
        self.sd = {n: 1.0 for n in names}
        self.w = {n: 0.0 for n in names}
        self.b = 0.0

    def _vec(self, x: dict) -> dict:
        return {n: (x.get(n, 0.0) - self.mu[n]) / self.sd[n] for n in self.names}

    def fit(self, X: list[dict], y: list[int]) -> "Logit":
        n = len(X)
        for k in self.names:
            vals = [x.get(k, 0.0) for x in X]
            self.mu[k] = sum(vals) / n
            var = sum((v - self.mu[k]) ** 2 for v in vals) / n
            self.sd[k] = math.sqrt(var) if var > 1e-12 else 1.0
        Z = [self._vec(x) for x in X]
        for _ in range(self.epochs):
            gw = {k: 0.0 for k in self.names}
            gb = 0.0
            for z, t in zip(Z, y):
                p = self._p(z)
                d = p - t
                for k in self.names:
                    gw[k] += d * z[k]
                gb += d
            for k in self.names:
                self.w[k] -= self.lr * (gw[k] / n + self.l2 * self.w[k])
            self.b -= self.lr * gb / n
        return self

    def _p(self, z: dict) -> float:
        s = self.b + sum(self.w[k] * z[k] for k in self.names)
        s = max(-30.0, min(30.0, s))
        return 1.0 / (1.0 + math.exp(-s))

    def predict(self, x: dict) -> float:
        return self._p(self._vec(x))


def auc(scores: list[float], labels: list[int]) -> float | None:
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return None
    wins = 0.0
    for p in pos:
        for q in neg:
            wins += 1.0 if p > q else 0.5 if p == q else 0.0
    return wins / (len(pos) * len(neg))


# ---------------------------------------------------------------- bank access (evaluator side)

class Bank:
    def __init__(self, rows: list[dict]):
        self.by: dict[tuple[str, str, str], dict] = {(r["judge_id"], r["episode_id"], r["action"]): r for r in rows}
        self.judges = sorted({r["judge_id"] for r in rows})

    def result(self, judge: str, ep: str, action: str) -> dict:
        return self.by[(judge, ep, action)]

    def j0(self, judge: str, ep: str) -> JudgeResult:
        return JudgeResult.from_dict({k: self.by[(judge, ep, INITIAL)][k] for k in JudgeResult.__dataclass_fields__})


def candidate_actions(view: ObservationView) -> list[str]:
    return [REREAD, RETRIEVE_ALL] + [f"retrieve:{kind}" for _, kind in view.record_handles]


def burden(action: str, view: ObservationView) -> float:
    """Records retrieved; a reread costs one extra judge call, counted as 0.5."""
    if action == STOP:
        return 0.0
    if action == REREAD:
        return 0.5
    if action == RETRIEVE_ALL:
        return float(len(view.record_handles))
    return 1.0


Policy = Callable[[ObservationView, JudgeResult, list[str]], str]


# ---------------------------------------------------------------- policies

def p_stop(view, j0, cands):
    return STOP


def p_reread(view, j0, cands):
    return REREAD


def p_all(view, j0, cands):
    return RETRIEVE_ALL


def make_random(seed: int) -> Policy:
    def p(view, j0, cands):
        rng = random.Random(f"{seed}:{view.episode_id}")
        return rng.choice([c for c in cands if c.startswith("retrieve:")])
    return p


def p_hedge_heuristic(view, j0, cands):
    """Untrained cue policy: retrieve the record whose check line is hedged, else unreferenced, else stop."""
    singles = [c for c in cands if c.startswith("retrieve:")]
    for pred in (lambda l: any(h in l.lower() for h in HEDGE_WORDS), lambda l: "(see " not in l):
        for c in singles:
            line = line_for_kind(view, c.split(":", 1)[1])
            if line is not None and pred(line):
                return c
    return STOP


def p_inspect_if_clear(view, j0, cands):
    """Risk-style baseline: the judge's misses are on 'looks clean' episodes, so inspect those fully."""
    return RETRIEVE_ALL if j0.verdict is not True else STOP


def make_learned(model: Logit, tau: float) -> Policy:
    def p(view, j0, cands):
        scored = [(model.predict(action_features(view, j0, c)), c) for c in cands]
        best_p, best = max(scored, key=lambda t: (t[0], -burden(t[1], view)))
        return best if best_p >= tau else STOP
    return p


# ---------------------------------------------------------------- evaluation

def evaluate(policy: Policy, judge: str, episodes: list[Episode], oracles: dict[str, OracleRecord],
             bank: Bank) -> dict:
    n = miss = fa = err0 = err1 = unresolved = 0
    load = 0.0
    change = Counter()
    pos = neg = 0
    for ep in episodes:
        view = render_view(ep)
        j0 = bank.j0(judge, ep.episode_id)
        action = policy(view, j0, candidate_actions(view))
        if action == STOP:
            final = j0.verdict
        else:
            final = bank.result(judge, ep.episode_id, action)["verdict"]
        truth = oracles[ep.episode_id].violation
        e0, e1 = _err(j0.verdict, truth), _err(final, truth)
        n += 1
        err0 += e0
        err1 += e1
        change[e0 - e1] += 1
        pos += truth
        neg += not truth
        miss += truth and final is not True
        fa += (not truth) and final is True
        unresolved += final is None
        load += burden(action, view)
    return {"n": n, "initial_errors": err0, "final_errors": err1, "corrected": change[1], "corrupted": change[-1],
            "missed_positives": miss, "n_positives": pos, "false_alarms": fa, "n_negatives": neg,
            "unresolved": unresolved, "mean_burden": load / n if n else None}


def oracle_best(judge: str, episodes: list[Episode], oracles: dict[str, OracleRecord], bank: Bank) -> dict:
    """Evaluator-only upper bound: the cheapest single action with the best outcome per episode."""
    def p(view, j0, cands):
        truth = oracles[view.episode_id].violation
        best = (_err(j0.verdict, truth), 0.0, STOP)
        for c in cands:
            e = _err(bank.result(judge, view.episode_id, c)["verdict"], truth)
            best = min(best, (e, burden(c, view), c))
        return best[2]
    return evaluate(p, judge, episodes, oracles, bank)


def headroom(judge: str, episodes: list[Episode], oracles: dict[str, OracleRecord], bank: Bank) -> dict:
    per_action = defaultdict(Counter)
    init_err = 0
    fixable_single = fixable_all = 0
    reread_disagree = 0
    by_mode = defaultdict(Counter)
    by_flag = defaultdict(Counter)
    for ep in episodes:
        truth = oracles[ep.episode_id].violation
        prov = oracles[ep.episode_id].provenance
        j0 = bank.j0(judge, ep.episode_id)
        e0 = _err(j0.verdict, truth)
        init_err += e0
        by_mode[prov["mode"]]["n"] += 1
        by_mode[prov["mode"]]["initial_error"] += e0
        for flag in ("boundary", "distractor_misleading"):
            if prov.get(flag):
                by_flag[flag]["n"] += 1
                by_flag[flag]["initial_error"] += e0
                by_flag[flag]["retrieve_all_error"] += _err(bank.result(judge, ep.episode_id, RETRIEVE_ALL)["verdict"], truth)
        singles_fix = False
        for action in [REREAD, RETRIEVE_ALL] + [f"retrieve:{r.kind}" for r in ep.records]:
            e1 = _err(bank.result(judge, ep.episode_id, action)["verdict"], truth)
            key = action if not action.startswith("retrieve:") or action == RETRIEVE_ALL else "retrieve:<single>"
            per_action[key][{1: "corrected", 0: "no_change", -1: "corrupted"}[e0 - e1]] += 1
            if action.startswith("retrieve:") and e0 == 1 and e1 == 0:
                singles_fix = True
            if action == REREAD and bank.result(judge, ep.episode_id, action)["verdict"] != j0.verdict:
                reread_disagree += 1
        fixable_single += e0 == 1 and singles_fix
        fixable_all += e0 == 1 and _err(bank.result(judge, ep.episode_id, RETRIEVE_ALL)["verdict"], truth) == 0
    n = len(episodes)
    return {"n": n, "initial_errors": init_err, "fixable_by_some_single_retrieval": fixable_single,
            "fixable_by_retrieve_all": fixable_all, "reread_disagreements": reread_disagree,
            "per_action": {k: dict(v) for k, v in per_action.items()},
            "initial_error_by_mode": {k: dict(v) for k, v in by_mode.items()},
            "errors_by_flag": {k: dict(v) for k, v in by_flag.items()}}


def _rows_for(judge: str, episodes: list[Episode], oracles: dict[str, OracleRecord], bank: Bank
              ) -> tuple[list[dict], list[int]]:
    X, y = [], []
    for ep in episodes:
        view = render_view(ep)
        j0 = bank.j0(judge, ep.episode_id)
        truth = oracles[ep.episode_id].violation
        e0 = _err(j0.verdict, truth)
        for c in candidate_actions(view):
            e1 = _err(bank.result(judge, ep.episode_id, c)["verdict"], truth)
            X.append(action_features(view, j0, c))
            y.append(int(e0 - e1 == 1))
    return X, y


def run_pilot(run_dir: Path, taus: tuple[float, ...] = (0.2, 0.3, 0.4, 0.5, 0.6)) -> dict:
    meta = json.loads((run_dir / "manifest.json").read_text())
    cfg = meta["config"]
    episodes, oracle_list = generate_pilot(cfg["seed"], cfg["per_family"])
    oracles = {o.episode_id: o for o in oracle_list}
    stored = {o["episode_id"]: o["violation"] for o in
              (json.loads(l) for l in (run_dir / "evaluator" / "oracle.jsonl").read_text().splitlines() if l.strip())}
    assert all(stored[e.episode_id] == oracles[e.episode_id].violation for e in episodes), "oracle mismatch with stored run"
    bank = Bank(read_bank(run_dir / "bank.jsonl"))
    families = sorted({e.family for e in episodes})
    feature_names = sorted(action_features(render_view(episodes[0]), bank.j0(bank.judges[0], episodes[0].episode_id), REREAD))
    ablated_names = [n for n in feature_names if n not in CUE_FEATURES]

    out: dict = {"judges": {}, "note": "Development pilot on fictional workflows. Exploratory; no confidence intervals."}
    for judge in bank.judges:
        J: dict = {"headroom": headroom(judge, episodes, oracles, bank), "held_out": {}, "pooled_held_out": {}}
        pooled: dict[str, list[dict]] = defaultdict(list)
        auc_full, auc_ablated, auc_labels = [], [], []
        for held in families:
            train = [e for e in episodes if e.family != held]
            test = [e for e in episodes if e.family == held]
            Xtr, ytr = _rows_for(judge, train, oracles, bank)
            model = Logit(feature_names).fit(Xtr, ytr)
            ablated = Logit(ablated_names).fit(Xtr, ytr)
            Xte, yte = _rows_for(judge, test, oracles, bank)
            auc_full += [model.predict(x) for x in Xte]
            auc_ablated += [ablated.predict(x) for x in Xte]
            auc_labels += yte
            policies: dict[str, Policy] = {
                "stop": p_stop, "reread": p_reread, "retrieve_all": p_all, "random_single": make_random(cfg["seed"]),
                "hedge_heuristic": p_hedge_heuristic, "inspect_if_clear": p_inspect_if_clear,
            }
            for tau in taus:
                policies[f"learned_tau{tau}"] = make_learned(model, tau)
            fold = {name: evaluate(p, judge, test, oracles, bank) for name, p in policies.items()}
            fold["oracle_best_evaluator_only"] = oracle_best(judge, test, oracles, bank)
            fold["_positive_rate_train"] = sum(ytr) / len(ytr)
            fold["_top_weights"] = sorted(model.w.items(), key=lambda kv: -abs(kv[1]))[:6]
            J["held_out"][held] = fold
            for name, r in fold.items():
                if not name.startswith("_"):
                    pooled[name].append(r)
        for name, rs in pooled.items():
            agg = {k: sum(r[k] for r in rs) for k in ("n", "initial_errors", "final_errors", "corrected", "corrupted",
                                                       "missed_positives", "n_positives", "false_alarms", "n_negatives", "unresolved")}
            agg["mean_burden"] = sum(r["mean_burden"] * r["n"] for r in rs) / agg["n"]
            J["pooled_held_out"][name] = agg
        J["predictability"] = {
            "auc_gain_full_features_held_out": auc(auc_full, auc_labels),
            "auc_gain_without_cue_features_held_out": auc(auc_ablated, auc_labels),
            "n_action_rows": len(auc_labels), "positive_rows": sum(auc_labels),
        }
        out["judges"][judge] = J
    (run_dir / "pilot_report.json").write_text(json.dumps(out, indent=2, sort_keys=True))
    (run_dir / "pilot_report.md").write_text(render_pilot_markdown(out, meta))
    return out


def render_pilot_markdown(out: dict, meta: dict) -> str:
    L = [f"# Pilot report ({meta['stage']})", "", f"Run `{meta['run_id']}`. {out['note']}", ""]
    for judge, J in out["judges"].items():
        h = J["headroom"]
        L += [f"## Judge {judge}", "",
              f"Initial errors {h['initial_errors']}/{h['n']}. Fixable by some single retrieval: "
              f"{h['fixable_by_some_single_retrieval']}; by retrieve_all: {h['fixable_by_retrieve_all']}. "
              f"Reread disagreed with initial on {h['reread_disagreements']}/{h['n']}.", "",
              "Per action (all episodes): " + json.dumps(h["per_action"], sort_keys=True), "",
              "Initial error by hidden mode: " + json.dumps(h["initial_error_by_mode"], sort_keys=True), "",
              "Errors on flagged episodes: " + json.dumps(h["errors_by_flag"], sort_keys=True), "",
              f"Predictability (held-out AUC for 'this action corrects the verdict'): full features "
              f"{_fmt(J['predictability']['auc_gain_full_features_held_out'])}, without cue features "
              f"{_fmt(J['predictability']['auc_gain_without_cue_features_held_out'])}.", "",
              "### Pooled over held-out families (each family held out once)", "",
              "| Policy | final err | init err | +1 | -1 | missed pos | false alarm | unresolved | mean burden |",
              "|---|---|---|---|---|---|---|---|---|"]
        for name, r in J["pooled_held_out"].items():
            L.append(f"| {name} | {r['final_errors']}/{r['n']} | {r['initial_errors']}/{r['n']} | {r['corrected']} | {r['corrupted']} "
                     f"| {r['missed_positives']}/{r['n_positives']} | {r['false_alarms']}/{r['n_negatives']} "
                     f"| {r['unresolved']} | {r['mean_burden']:.2f} |")
        L += ["", "### Per held-out family: final errors", "",
              "| Family | " + " | ".join(J["pooled_held_out"]) + " |",
              "|---|" + "---|" * len(J["pooled_held_out"])]
        for fam, fold in J["held_out"].items():
            L.append(f"| {fam} | " + " | ".join(f"{fold[p]['final_errors']}/{fold[p]['n']}" for p in J["pooled_held_out"]) + " |")
        L.append("")
    return "\n".join(L)


def _fmt(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.3f}"
