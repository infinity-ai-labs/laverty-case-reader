"""Read one case file end to end: pages -> marks (SAM 3.1) -> summary (Muse Spark) -> citation check."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from . import __version__
from .assemble import assemble, to_markdown
from .marks import DEFAULT_CONCEPTS, clean_marks, find_marks_on_page
from .meta_api import SAM_MODEL
from .pages import Page, load_pages
from .reader import MAX_PAGES, READER_MODEL, read_case
from .refine import refine_reader_marks


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def read_file(
    source: Path,
    out_dir: Path,
    *,
    case_id: str,
    make_client: Callable[[list[Page]], Any],
    concepts: dict[str, list[str]] | None = None,
    reader_model: str = READER_MODEL,
    reasoning_effort: str | None = "high",
    min_confidence: float = 0.3,
    refine: bool = True,
    mock: bool = False,
    log: Callable[[str], None] = print,
) -> dict[str, Any]:
    concepts = concepts or DEFAULT_CONCEPTS
    out_dir.mkdir(parents=True, exist_ok=True)
    started_at, started = _now(), time.time()

    pages = load_pages(source, out_dir)
    log(f"{case_id}: {len(pages)} pages")
    if len(pages) > MAX_PAGES:  # before any paid call
        raise ValueError(f"The file has {len(pages)} pages; the Case Reader reads up to {MAX_PAGES} at a time.")
    client = make_client(pages)

    found: list[dict[str, Any]] = []
    for page in pages:
        found += find_marks_on_page(client, page, concepts, raw_dir=out_dir / "sam")
    _write_json(out_dir / "marks.found.json", found)
    marks = clean_marks(found, min_confidence=min_confidence)
    log(f"{case_id}: SAM 3.1 found {sum(1 for f in found if 'box' in f)} boxes, kept {len(marks)} marks")

    reader, mode = read_case(client, pages, marks, out_dir=out_dir, model=reader_model,
                             reasoning_effort=reasoning_effort)
    log(f"{case_id}: Muse Spark answered ({mode}): {len(reader['parties'])} parties, "
        f"{len(reader['dates'])} dates, {len(reader['citations'])} citations")
    if refine:
        placed = refine_reader_marks(client, pages, reader, model=reader_model, log=log)
        log(f"{case_id}: Muse Spark close-ups placed {placed} of "
            f"{sum(1 for m in reader['marks'] if str(m.get('mark_id', '')).startswith('X'))} marks again")
    _write_json(out_dir / "reader.json", reader)

    run = {
        "started": started_at,
        "finished": _now(),
        "seconds": round(time.time() - started, 1),
        "reader_model": reader_model,
        "marks_model": SAM_MODEL,
        "reasoning_effort": reasoning_effort,
        "concepts": concepts,
        "min_confidence": min_confidence,
        "reader_output_mode": mode,
        "close_ups": refine,
        "mock": mock,
        "case_reader_version": __version__,
    }
    summary = assemble(case_id=case_id, source=source, out_dir=out_dir, pages=pages,
                       found_marks=marks, reader=reader, run=run)
    _write_json(out_dir / "summary.json", summary)
    (out_dir / "summary.md").write_text(to_markdown(summary), encoding="utf-8")
    checks = [c["check"]["status"] for c in summary["citations"]]
    log(f"{case_id}: citations valid {checks.count('valid')}, invalid {checks.count('invalid')}, "
        f"not checked {checks.count('not_checked')}; {len(summary['flags'])} points flagged")
    return summary
