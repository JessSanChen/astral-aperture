"""Baseline controllers. Each sees an ObservationView and nothing else."""

from __future__ import annotations

import random

from .contracts import InspectionAction, ObservationView

RETRIEVE_CHARGE = 1.0
REREAD_CHARGE = 0.5


def _handle(view: ObservationView, kind: str) -> str | None:
    for rid, k in view.record_handles:
        if k == kind:
            return rid
    return None


class Controller:
    controller_id = "base"

    def decide(self, view: ObservationView) -> InspectionAction:
        raise NotImplementedError


class StopController(Controller):
    controller_id = "stop"

    def decide(self, view):
        return InspectionAction("stop")


class RetrieveRegistryController(Controller):
    controller_id = "retrieve_registry"

    def decide(self, view):
        rid = _handle(view, "vendor_registry")
        return InspectionAction("retrieve", rid, RETRIEVE_CHARGE) if rid else InspectionAction("stop")


class RetrieveRequestController(Controller):
    controller_id = "retrieve_request"

    def decide(self, view):
        rid = _handle(view, "request_document")
        return InspectionAction("retrieve", rid, RETRIEVE_CHARGE) if rid else InspectionAction("stop")


class StatusAwareController(Controller):
    """Reread on parse failure, retrieve the registry on abstention, else stop."""

    controller_id = "status_aware"

    def decide(self, view):
        last = view.judge_history[-1] if view.judge_history else None
        if last is None:
            return InspectionAction("stop")
        if last.status == "parse_error":
            return InspectionAction("reread", charge=REREAD_CHARGE)
        if last.status == "abstain":
            rid = _handle(view, "vendor_registry")
            if rid:
                return InspectionAction("retrieve", rid, RETRIEVE_CHARGE)
        return InspectionAction("stop")


class RandomController(Controller):
    """Random action, seeded per episode so results do not depend on call order."""

    controller_id = "random"

    def __init__(self, seed: int = 0):
        self.seed = seed

    def decide(self, view):
        rng = random.Random(f"{self.seed}:{view.episode_id}")
        choice = rng.choice(("stop", "retrieve", "reread"))
        if choice == "retrieve" and view.record_handles:
            rid = rng.choice([rid for rid, _ in view.record_handles])
            return InspectionAction("retrieve", rid, RETRIEVE_CHARGE)
        if choice == "reread":
            return InspectionAction("reread", charge=REREAD_CHARGE)
        return InspectionAction("stop")


def default_controllers(seed: int) -> list[Controller]:
    return [
        StopController(),
        RetrieveRegistryController(),
        RetrieveRequestController(),
        StatusAwareController(),
        RandomController(seed),
    ]
