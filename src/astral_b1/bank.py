"""Collect a bounded one-step inspection-response bank with fixed judges.

For every episode and judge the collector evaluates: the initial view, a reread of
the initial view with a new sample id, one view per single retrievable record, and a
view with all records retrieved. The collector sees the whole tree. A replayed
controller must only ever be shown the initial view plus the branch it chose; that
restriction is enforced in `pilot.py`, not here.
"""

from __future__ import annotations

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Mapping

from .contracts import Episode, JudgeResult, ObservationView, render_view

Judge = Callable[[ObservationView, str], JudgeResult]

INITIAL, REREAD, RETRIEVE_ALL = "initial", "reread", "retrieve_all"


def retrieve_action(kind: str) -> str:
    return f"retrieve:{kind}"


def actions_for(episode: Episode) -> list[str]:
    return [INITIAL, REREAD] + [retrieve_action(r.kind) for r in episode.records] + [RETRIEVE_ALL]


def view_for(episode: Episode, action: str) -> ObservationView:
    if action in (INITIAL, REREAD):
        return render_view(episode)
    if action == RETRIEVE_ALL:
        return render_view(episode, tuple(r.record_id for r in episode.records))
    kind = action.split(":", 1)[1]
    rid = next(r.record_id for r in episode.records if r.kind == kind)
    return render_view(episode, (rid,))


def _collect_one(judge_id: str, judge: Judge, ep: Episode) -> list[dict]:
    rows = []
    for action in actions_for(ep):
        view = view_for(ep, action)
        res = judge(view, f"bank:{judge_id}:{ep.episode_id}:{action}")
        rows.append({"judge_id": judge_id, "episode_id": ep.episode_id, "action": action,
                     "view_hash": view.view_hash(), **res.to_dict()})
    return rows


def collect(episodes: list[Episode], judges: Mapping[str, Judge], workers: int = 8) -> list[dict]:
    jobs = [(jid, j, ep) for jid, j in judges.items() for ep in episodes]
    if workers <= 1:
        out = [_collect_one(*j) for j in jobs]
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            out = list(pool.map(lambda j: _collect_one(*j), jobs))
    return [r for rows in out for r in rows]


def write_bank(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def read_bank(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
