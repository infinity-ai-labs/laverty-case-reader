"""Helpers to read the answer key (shared by the scorer and the offline mock)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ANSWER_KEY_DIR = Path(__file__).resolve().parent.parent / "answer-key"


def load_answer_key(case_id: str, key_dir: Path = ANSWER_KEY_DIR) -> tuple[dict[str, Any], dict[str, Any]] | None:
    case_file = key_dir / f"{case_id}.json"
    marks_file = key_dir / f"{case_id}.marks.json"
    if not case_file.exists():
        return None
    marks = json.loads(marks_file.read_text(encoding="utf-8")) if marks_file.exists() else {"marks": []}
    return json.loads(case_file.read_text(encoding="utf-8")), marks


def role_code(role: str) -> str:
    """Map an answer-key role ("claimant's lawyer", "landlord (claimant)") to a reader role code."""
    r = role.lower()
    side = ""
    positions = {s: r.find(s) for s in ("claimant", "defendant") if s in r}
    if positions:
        side = min(positions, key=positions.get)
    if "lawyer" in r and side:
        return f"{side}_lawyer"
    if "judge" in r:
        return "judge"
    if "clerk" in r:
        return "clerk"
    if "notary" in r:
        return "notary"
    if side and re.search(rf"{side}'s\s+\w", r):
        return f"{side}_representative"
    return side or "other"


def parse_law(text: str) -> dict[str, Any]:
    """'Federal Decree-Law No. 33 of 2021 ...' -> kind, emirate, number, year."""
    match = re.search(r"No\.\s*\(?(\d+)\)?\s+of\s+(\d{4})", text)
    number, year = (match.group(1), int(match.group(2))) if match else ("", 0)
    lowered = text.lower()
    if lowered.startswith("federal decree-law"):
        kind, emirate = "federal_decree_law", ""
    elif lowered.startswith("federal law"):
        kind, emirate = "federal_law", ""
    else:
        emirate = text.split()[0] if text else ""
        kind = "local_law"
    return {"kind": kind, "emirate": emirate, "number": number, "year": year}
