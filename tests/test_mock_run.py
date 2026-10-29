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

    # The two invalid citations in the test files are always caught by the citation check.
    assert sum(c["citations"]["invalid_caught"] for c in scores.values()) == 2
    # The mock's deliberate mistakes are all seen by the scorer.
    assert all(c["parties"]["correct"] == c["parties"]["total"] - 1 for c in scores.values())
    assert scores["case-01"]["claims"]["correct"] == scores["case-01"]["claims"]["total"] - 1
    assert scores["case-03"]["dates"]["correct"] == scores["case-03"]["dates"]["total"] - 1
    assert all(c["marks"]["correct"] == c["marks"]["total"] - 1 for c in scores.values())
    # The mock's false find over printed text is turned down by the reader, not kept as a mark.
    summary = json.loads((out / "case-01" / "summary.json").read_text(encoding="utf-8"))
    assert len(summary["rejected_marks"]) == 1
