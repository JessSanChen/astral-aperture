"""End-to-end smoke run, accounting, replay, and CLI."""

import json
import socket
import subprocess
import sys

import pytest

from astral_b1.runner import replay, run_smoke


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    out = tmp_path_factory.mktemp("smoke")
    report = run_smoke(out, seed=0, n_episodes=36)
    return out, report


def test_error_change_bookkeeping_covers_all_three_cases(run):
    _, report = run
    arms = report["arms"]
    # Retrieving the registry under the narration judge corrects hallucinated
    # vendors and is corrupted by the misleading note family.
    r = arms["retrieve_registry+narration"]
    assert r["corrected"] > 0 and r["corrupted"] > 0 and r["no_change"] > 0
    for arm in arms.values():
        assert arm["corrected"] + arm["no_change"] + arm["corrupted"] == arm["n_episodes"]


def test_failures_and_abstentions_are_counted(run):
    _, report = run
    arms = report["arms"]
    assert arms["stop+narration"]["judge_call_status"].get("parse_error", 0) > 0
    assert arms["stop+record"]["judge_call_status"].get("abstain", 0) > 0
    assert arms["stop+record"]["unresolved_final"] > 0
    for arm in arms.values():
        assert arm["missed_positive_rate"]["denominator"] == arm["n_positives"]
        assert arm["n_positives"] + arm["n_negatives"] == arm["n_episodes"]


def test_status_aware_reduces_unresolved(run):
    _, report = run
    arms = report["arms"]
    assert arms["status_aware+record"]["unresolved_final"] < arms["stop+record"]["unresolved_final"]
    assert arms["status_aware+narration"]["unresolved_final"] <= arms["stop+narration"]["unresolved_final"]


def test_rereads_have_distinct_sample_ids(run):
    out, _ = run
    calls = [json.loads(l) for l in (out / "judge_calls.jsonl").read_text().splitlines()]
    assert len({c["sample_id"] for c in calls}) == len(calls)


def test_manifest_and_artifacts(run):
    out, _ = run
    m = json.loads((out / "manifest.json").read_text())
    assert m["stage"] == "plumbing"
    assert m["counts"]["decisions"] == 36 * 10
    assert set(m["artifacts_sha256"]) == {"decisions.jsonl", "judge_calls.jsonl", "observations.jsonl"}
    assert (out / "evaluator" / "oracle.jsonl").exists()


def test_observations_never_contain_oracle_fields(run):
    out, _ = run
    text = (out / "observations.jsonl").read_text().lower()
    for bad in ("violation", "family", "group_key", "oracle"):
        assert bad not in text


def test_replay_matches_with_network_disabled(run, monkeypatch):
    out, _ = run

    def no_network(*a, **k):
        raise RuntimeError("network disabled")

    monkeypatch.setattr(socket, "socket", no_network)
    assert replay(out)


def test_cli(tmp_path):
    out = tmp_path / "cli"
    r = subprocess.run([sys.executable, "-m", "astral_b1", "smoke", "--output", str(out), "--episodes", "12"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "Report (plumbing)" in r.stdout
    r2 = subprocess.run([sys.executable, "-m", "astral_b1", "replay", "--input", str(out)], capture_output=True, text=True)
    assert r2.returncode == 0 and "identical" in r2.stdout
