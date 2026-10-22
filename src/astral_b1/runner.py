"""Smoke run, live development run, and offline replay.

Layout of an output directory:
  observations.jsonl   controller-facing views at decision time (allowlisted)
  judge_calls.jsonl    every judge call, including failures
  decisions.jsonl      locked pre-audit decisions
  gateway_attempts.jsonl   live runs only: every HTTP attempt and cache hit
  evaluator/oracle.jsonl   evaluator-only labels (never read by controllers)
  manifest.json, report.json, report.md
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Mapping

from . import __version__
from .contracts import (
    DecisionRecord,
    Episode,
    JudgeResult,
    ObservationView,
    OracleRecord,
    render_view,
    stable_hash,
)
from .controllers import Controller, default_controllers
from .environment import ORACLE_VERSION, generate
from .evaluator import render_markdown, score
from .gateway import SYSTEM_PROMPT, AttemptLog, JudgeSpec, OpenRouterJudge, ResponseCache
from .judges import JUDGES

Judge = Callable[[ObservationView, str], JudgeResult]


def run_episode(
    episode: Episode, controller: Controller, judge: Judge, arm_id: str
) -> tuple[DecisionRecord, list[JudgeResult], ObservationView]:
    """One bounded inspection step. The controller only ever sees views."""
    calls: list[JudgeResult] = []
    sample = lambda k: f"{arm_id}:{episode.episode_id}:{k}"  # noqa: E731

    view0 = render_view(episode)
    j0 = judge(view0, sample("s0"))
    calls.append(j0)
    view1 = render_view(episode, (), (j0,))
    action = controller.decide(view1)

    if action.kind == "stop":
        final_view, jf = view1, j0
    elif action.kind == "retrieve":
        final_view = render_view(episode, (action.record_id,), (j0,))
        jf = judge(final_view, sample("s1"))
        calls.append(jf)
    else:  # reread: same evidence, new sample identity
        final_view = view1
        jf = judge(view1, sample("s1"))
        calls.append(jf)

    decision = DecisionRecord(
        episode_id=episode.episode_id,
        arm_id=arm_id,
        stage="pre_audit",
        initial_verdict=j0.verdict,
        final_verdict=jf.verdict,
        actions=(action,),
        initial_sample_id=j0.sample_id,
        final_sample_id=jf.sample_id,
        evidence_view_hash=final_view.view_hash(),
        inspection_charge=action.charge,
    )
    return decision, calls, view1


def _run_arms(
    episodes: list[Episode],
    controllers: list[Controller],
    judges: Mapping[str, Judge],
    workers: int,
) -> tuple[list[DecisionRecord], list[JudgeResult], list[dict]]:
    jobs = [
        (ep, ctrl, judge, f"{ctrl.controller_id}+{judge_id}")
        for judge_id, judge in judges.items()
        for ctrl in controllers
        for ep in episodes
    ]
    if workers <= 1:
        results = [run_episode(*j) for j in jobs]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = list(pool.map(lambda j: run_episode(*j), jobs))
    decisions, calls, views = [], [], []
    for (ep, ctrl, judge, arm_id), (d, c, v) in zip(jobs, results):
        decisions.append(d)
        calls.extend(c)
        views.append({"arm_id": arm_id, **v.serialize()})
    return decisions, calls, views


def _finish(output: Path, seed: int, n_episodes: int, stage: str, config: dict,
            episodes, oracles, decisions, calls, views) -> dict:
    _write_jsonl(output / "observations.jsonl", views)
    _write_jsonl(output / "judge_calls.jsonl", [c.to_dict() for c in calls])
    _write_jsonl(output / "decisions.jsonl", [d.to_dict() for d in decisions])
    _write_jsonl(output / "evaluator" / "oracle.jsonl", [o.to_dict() for o in oracles])
    oracle_map = {o.episode_id: o for o in oracles}
    report = score(decisions, oracle_map, calls)
    manifest = _manifest(output, seed, n_episodes, stage, config, len(decisions), len(calls))
    (output / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    (output / "report.md").write_text(render_markdown(report, manifest))
    return report


def run_smoke(output: Path, seed: int = 0, n_episodes: int = 36) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    (output / "evaluator").mkdir(exist_ok=True)
    episodes, oracles = generate(seed, n_episodes)
    controllers = default_controllers(seed)
    decisions, calls, views = _run_arms(episodes, controllers, JUDGES, workers=1)
    config = {"seed": seed, "n_episodes": n_episodes, "judges": sorted(JUDGES), "oracle_version": ORACLE_VERSION}
    return _finish(output, seed, n_episodes, "plumbing", config, episodes, oracles, decisions, calls, views)


def run_live(output: Path, specs: list[JudgeSpec], cache_dir: Path, seed: int = 0,
             n_episodes: int = 36, workers: int = 6, transport=None) -> dict:
    """Development run with real fixed judges. Requires explicit authorization."""
    output.mkdir(parents=True, exist_ok=True)
    (output / "evaluator").mkdir(exist_ok=True)
    log = AttemptLog(output / "gateway_attempts.jsonl")
    judges: dict[str, OpenRouterJudge] = {}
    for spec in specs:
        cache = ResponseCache(cache_dir / "dev" / spec.judge_id)
        judges[spec.judge_id] = OpenRouterJudge(spec, cache, log, transport=transport)
    episodes, oracles = generate(seed, n_episodes)
    controllers = default_controllers(seed)
    decisions, calls, views = _run_arms(episodes, controllers, judges, workers=workers)
    config = {
        "seed": seed, "n_episodes": n_episodes, "oracle_version": ORACLE_VERSION,
        "judges": {jid: j.spec.to_dict() for jid, j in judges.items()},
        "system_prompt_sha256": stable_hash(SYSTEM_PROMPT),
        "gateway": {jid: {"network_calls": j.network_calls, "cache_hits": j.cache_hits} for jid, j in judges.items()},
    }
    return _finish(output, seed, n_episodes, "development_live", config, episodes, oracles, decisions, calls, views)


def run_collect(output: Path, specs: list[JudgeSpec], cache_dir: Path, seed: int = 1,
                per_family: int = 36, workers: int = 8, transport=None) -> dict:
    """Collect the one-step inspection bank for the pilot environment with real judges."""
    from .bank import collect, write_bank
    from .families import ORACLE_VERSION as PILOT_ORACLE, generate_pilot

    output.mkdir(parents=True, exist_ok=True)
    (output / "evaluator").mkdir(exist_ok=True)
    log = AttemptLog(output / "gateway_attempts.jsonl")
    judges: dict[str, OpenRouterJudge] = {}
    for spec in specs:
        cache = ResponseCache(cache_dir / "pilot" / spec.judge_id)
        judges[spec.judge_id] = OpenRouterJudge(spec, cache, log, transport=transport)
    episodes, oracles = generate_pilot(seed, per_family)
    rows = collect(episodes, judges, workers=workers)
    write_bank(output / "bank.jsonl", rows)
    _write_jsonl(output / "evaluator" / "oracle.jsonl", [o.to_dict() for o in oracles])
    config = {
        "seed": seed, "per_family": per_family, "oracle_version": PILOT_ORACLE,
        "judges": {jid: j.spec.to_dict() for jid, j in judges.items()},
        "system_prompt_sha256": stable_hash(SYSTEM_PROMPT),
        "gateway": {jid: {"network_calls": j.network_calls, "cache_hits": j.cache_hits} for jid, j in judges.items()},
    }
    manifest = _manifest(output, seed, len(episodes), "pilot_collection", config, 0, len(rows))
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))
    status = {}
    for r in rows:
        status.setdefault(r["judge_id"], {}).setdefault(r["status"], 0)
        status[r["judge_id"]][r["status"]] += 1
    return {"rows": len(rows), "status": status}


def replay(run_dir: Path) -> bool:
    """Rebuild the report from frozen records and compare to the stored one."""
    decisions = [DecisionRecord.from_dict(d) for d in _read_jsonl(run_dir / "decisions.jsonl")]
    calls = [JudgeResult.from_dict(c) for c in _read_jsonl(run_dir / "judge_calls.jsonl")]
    oracles = {o["episode_id"]: OracleRecord.from_dict(o) for o in _read_jsonl(run_dir / "evaluator" / "oracle.jsonl")}
    rebuilt = score(decisions, oracles, calls)
    stored = json.loads((run_dir / "report.json").read_text())
    return rebuilt == stored


def _manifest(output: Path, seed: int, n: int, stage: str, config: dict, n_decisions: int, n_calls: int) -> dict:
    commit, dirty = _git_state()
    artifacts = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(output.glob("*.jsonl"))
    }
    return {
        "schema_version": "0.1",
        "run_id": f"{stage}-{seed}-{stable_hash(config)[:8]}",
        "stage": stage,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "code": {"package_version": __version__, "git_commit": commit, "dirty": dirty, "python": sys.version.split()[0]},
        "config": config,
        "config_sha256": stable_hash(config),
        "counts": {"episodes": n, "decisions": n_decisions, "judge_calls": n_calls},
        "artifacts_sha256": artifacts,
        "note": "Evaluator metadata is never controller input.",
    }


def _git_state() -> tuple[str | None, bool | None]:
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], text=True, stderr=subprocess.DEVNULL).strip())
        return commit, dirty
    except (OSError, subprocess.CalledProcessError):
        return None, None


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
