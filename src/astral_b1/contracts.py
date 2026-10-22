"""Typed, frozen records and the observation boundary.

The only way to build a controller-facing view is `render_view`, which copies an
explicit allowlist of fields out of an Episode. Everything else about an Episode
(world state, family, group key, outcome) is evaluator-only.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping


def stable_hash(obj: Any) -> str:
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# Substrings that must never appear in a serialized controller view.
FORBIDDEN_VIEW_SUBSTRINGS = (
    "oracle",
    "violation",
    "world",
    "family",
    "group_key",
    "hidden",
    "truth",
    "label",
    "counterfactual",
    "outcome_action",
)

VIEW_KEYS = ("episode_id", "policy", "messages", "record_handles", "revealed", "judge_history")


@dataclass(frozen=True)
class Record:
    """A retrievable evidence record. Content is visible only after retrieval."""

    record_id: str
    kind: str
    content: Mapping[str, Any]


@dataclass(frozen=True)
class Episode:
    """Evaluator-side episode. Never pass this object to a controller or judge."""

    episode_id: str
    world: Mapping[str, Any]
    narration: tuple[str, ...]
    records: tuple[Record, ...]
    outcome_action: str
    family: str
    group_key: str
    policy: str = ""  # trusted policy text shown to judges; not a transcript


@dataclass(frozen=True)
class JudgeResult:
    judge_id: str
    judge_version: str
    sample_id: str
    request_hash: str
    status: str  # "ok" | "abstain" | "parse_error"
    verdict: bool | None  # True = violation flagged
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "judge_id": self.judge_id,
            "judge_version": self.judge_version,
            "sample_id": self.sample_id,
            "request_hash": self.request_hash,
            "status": self.status,
            "verdict": self.verdict,
            "rationale": self.rationale,
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "JudgeResult":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__})


@dataclass(frozen=True)
class ObservationView:
    """Everything a controller or judge is allowed to see. Build via render_view."""

    episode_id: str
    messages: tuple[str, ...]
    record_handles: tuple[tuple[str, str], ...]  # (record_id, kind)
    revealed: Mapping[str, Mapping[str, Any]]  # record_id -> content
    judge_history: tuple[JudgeResult, ...]
    policy: str = ""

    def serialize(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "policy": self.policy,
            "messages": list(self.messages),
            "record_handles": [list(h) for h in self.record_handles],
            "revealed": {k: dict(v) for k, v in self.revealed.items()},
            "judge_history": [j.to_dict() for j in self.judge_history],
        }

    def view_hash(self) -> str:
        return stable_hash(self.serialize())


def render_view(
    episode: Episode,
    revealed_ids: tuple[str, ...] = (),
    history: tuple[JudgeResult, ...] = (),
) -> ObservationView:
    """Allowlisted projection of an Episode. Only selected records are revealed."""
    by_id = {r.record_id: r for r in episode.records}
    for rid in revealed_ids:
        if rid not in by_id:
            raise KeyError(f"unknown record handle {rid!r}")
    return ObservationView(
        episode_id=episode.episode_id,
        messages=tuple(episode.narration),
        record_handles=tuple((r.record_id, r.kind) for r in episode.records),
        revealed={rid: dict(by_id[rid].content) for rid in revealed_ids},
        judge_history=tuple(history),
        policy=episode.policy,
    )


@dataclass(frozen=True)
class InspectionAction:
    kind: str  # "stop" | "retrieve" | "reread"
    record_id: str | None = None
    charge: float = 0.0

    def __post_init__(self) -> None:
        if self.kind not in ("stop", "retrieve", "reread"):
            raise ValueError(f"bad action kind {self.kind!r}")
        if self.kind == "retrieve" and not self.record_id:
            raise ValueError("retrieve needs a record_id")
        if self.kind != "retrieve" and self.record_id is not None:
            raise ValueError("only retrieve takes a record_id")

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind, "record_id": self.record_id, "charge": self.charge}


@dataclass(frozen=True)
class DecisionRecord:
    """Locked pre-audit decision. Frozen; the evaluator never writes to it."""

    episode_id: str
    arm_id: str
    stage: str  # always "pre_audit" in this slice
    initial_verdict: bool | None
    final_verdict: bool | None
    actions: tuple[InspectionAction, ...]
    initial_sample_id: str
    final_sample_id: str
    evidence_view_hash: str
    inspection_charge: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "arm_id": self.arm_id,
            "stage": self.stage,
            "initial_verdict": self.initial_verdict,
            "final_verdict": self.final_verdict,
            "actions": [a.to_dict() for a in self.actions],
            "initial_sample_id": self.initial_sample_id,
            "final_sample_id": self.final_sample_id,
            "evidence_view_hash": self.evidence_view_hash,
            "inspection_charge": self.inspection_charge,
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "DecisionRecord":
        return cls(
            episode_id=d["episode_id"],
            arm_id=d["arm_id"],
            stage=d["stage"],
            initial_verdict=d["initial_verdict"],
            final_verdict=d["final_verdict"],
            actions=tuple(InspectionAction(**a) for a in d["actions"]),
            initial_sample_id=d["initial_sample_id"],
            final_sample_id=d["final_sample_id"],
            evidence_view_hash=d["evidence_view_hash"],
            inspection_charge=d["inspection_charge"],
        )


@dataclass(frozen=True)
class OracleRecord:
    """Evaluator-only ground truth from an executable predicate."""

    episode_id: str
    violation: bool
    oracle_version: str
    family: str
    group_key: str
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "violation": self.violation,
            "oracle_version": self.oracle_version,
            "family": self.family,
            "group_key": self.group_key,
            "provenance": dict(self.provenance),
        }

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> "OracleRecord":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__})
