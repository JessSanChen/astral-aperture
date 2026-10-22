"""Tests that protect the observation boundary and decision lock."""

import dataclasses
import json

import pytest

from astral_b1.contracts import (
    FORBIDDEN_VIEW_SUBSTRINGS,
    VIEW_KEYS,
    InspectionAction,
    ObservationView,
    render_view,
)
from astral_b1.controllers import Controller, StopController
from astral_b1.environment import generate
from astral_b1.judges import JUDGES
from astral_b1.runner import run_episode


def test_oracle_perturbation_does_not_change_view():
    (ep,), _ = generate(1, 1)
    flipped_world = dict(ep.world, decision="rejected", vendor_approved=not ep.world["vendor_approved"])
    twin = dataclasses.replace(ep, world=flipped_world, family="other", group_key="other", outcome_action="rejected")
    assert render_view(ep).serialize() == render_view(twin).serialize()
    assert render_view(ep).view_hash() == render_view(twin).view_hash()


def test_view_serialization_is_allowlisted():
    eps, _ = generate(2, 6)
    for ep in eps:
        view = render_view(ep, (ep.records[1].record_id,), ())
        ser = view.serialize()
        assert tuple(ser) == VIEW_KEYS
        text = json.dumps(ser).lower()
        for bad in FORBIDDEN_VIEW_SUBSTRINGS:
            assert bad not in text, bad


def test_unknown_record_handle_rejected():
    (ep,), _ = generate(3, 1)
    with pytest.raises(KeyError):
        render_view(ep, ("not-a-record",))


def test_unselected_branch_isolation():
    (ep,), _ = generate(4, 1)
    view = render_view(ep, (ep.records[0].record_id,))
    assert set(view.revealed) == {ep.records[0].record_id}
    assert render_view(ep).revealed == {}


def test_controller_receives_only_views():
    seen = []

    class Spy(Controller):
        controller_id = "spy"

        def decide(self, view):
            seen.append(view)
            return InspectionAction("stop")

    eps, _ = generate(5, 3)
    for ep in eps:
        run_episode(ep, Spy(), JUDGES["narration"], "spy+narration")
    assert seen and all(isinstance(v, ObservationView) for v in seen)
    assert all(not hasattr(v, "world") and v.revealed == {} for v in seen)


def test_decision_record_is_locked():
    (ep,), _ = generate(6, 1)
    d, _, _ = run_episode(ep, StopController(), JUDGES["record"], "stop+record")
    with pytest.raises(dataclasses.FrozenInstanceError):
        d.final_verdict = True  # type: ignore[misc]
    assert d.stage == "pre_audit"


def test_action_validation():
    with pytest.raises(ValueError):
        InspectionAction("retrieve")
    with pytest.raises(ValueError):
        InspectionAction("stop", record_id="x")
    with pytest.raises(ValueError):
        InspectionAction("peek")
