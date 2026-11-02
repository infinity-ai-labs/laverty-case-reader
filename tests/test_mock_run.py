"""End to end without the API: the offline mock runs the whole pipeline, then the scorer checks it."""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_mock_run_and_score(tmp_path):
    out = tmp_path / "mock-run"
    subprocess.run([sys.executable, "-m", "case_reader", "read-all", "--mock", "--out", str(out)],
                   cwd=REPO, check=True, capture_output=True)
    for case in ("case-01", "case-02", "case-03"):
        summary = json.loads((out / case / "summary.json").read_text(encoding="utf-8"))
        assert summary["mock"] is True
        assert (out / case / "summary.md").read_text(encoding="utf-8").startswith("> **Mock run.**")

    subprocess.run([sys.executable, "tools/score.py", str(out)], cwd=REPO, check=True, capture_output=True)
    scores = {c["case"]: c for c in json.loads((out / "score.json").read_text(encoding="utf-8"))}

    # Every planted citation problem is caught: articles that don't exist, a changed quote,
    # and a law outside the index left "not checked".
    keys = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((REPO / "answer-key").glob("case-??.json"))]
    planted_invalid = sum(1 for k in keys for c in k["citations"] if not c["valid"] and not c.get("not_in_index"))
    planted_misquotes = sum(1 for k in keys for c in k["citations"] if c.get("quote_matches_official_text") is False)
    assert planted_invalid >= 2 and sum(c["citations"]["invalid_caught"] for c in scores.values()) == planted_invalid
    assert sum(c["citations"]["misquotes_caught"] for c in scores.values()) == planted_misquotes
    assert all(c["citations"]["correct"] == c["citations"]["total"] for c in scores.values())
    # The mock's deliberate mistakes in the first three cases are all seen by the scorer.
    first = [scores[c] for c in ("case-01", "case-02", "case-03")]
    assert all(c["parties"]["correct"] == c["parties"]["total"] - 1 for c in first)
    assert scores["case-01"]["claims"]["correct"] == scores["case-01"]["claims"]["total"] - 1
    assert all(c["dates"]["correct"] == c["dates"]["total"] - 1 for c in first)
    assert all(c["marks"]["correct"] == c["marks"]["total"] - 1 for c in first)
    # The mock's false find over printed text is turned down by the reader, not kept as a mark.
    summary = json.loads((out / "case-01" / "summary.json").read_text(encoding="utf-8"))
    assert len(summary["rejected_marks"]) == 1


def test_a_case_that_was_not_read_scores_zero(tmp_path):
    out = tmp_path / "mock-run"
    subprocess.run([sys.executable, "-m", "case_reader", "read-all", "--mock", "--out", str(out), "--cases", "case-01, case-03"],
                   cwd=REPO, check=True, capture_output=True)
    (out / "case-03" / "summary.json").unlink()
    subprocess.run([sys.executable, "tools/score.py", str(out)], cwd=REPO, check=True, capture_output=True)
    scores = {c["case"]: c for c in json.loads((out / "score.json").read_text(encoding="utf-8"))}
    assert set(scores) == {"case-01", "case-03"}
    assert scores["case-03"]["unread"] and scores["case-03"]["dates"]["correct"] == 0
    assert scores["case-03"]["dates"]["total"] > 0


def test_unknown_case_ids_are_refused(tmp_path):
    done = subprocess.run([sys.executable, "-m", "case_reader", "read-all", "--mock", "--out", str(tmp_path / "x"),
                           "--cases", "case-99"], cwd=REPO, capture_output=True)
    assert done.returncode == 2
