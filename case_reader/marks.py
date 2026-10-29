"""Find stamps, signatures and handwritten notes on each page with SAM 3.1.

SAM 3.1 takes a short noun phrase (a "concept") and an image, and returns every
instance it finds as special-token text, one record per object:

    <0f>0<|box;x1=181;y1=365;x2=556;y2=486;w=1516;h=1600;c=0.91|><|mask;x=0;y=0;data=...|>,1<|box;...|>...

Box corners are inclusive pixel positions in an image of size w x h; `c` is the
confidence when it was asked for. Only the boxes are used here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pages import Page, image_data_url

MARK_TYPES = ("stamp", "signature", "handwriting")

# One phrase per mark type for normal runs.
DEFAULT_CONCEPTS: dict[str, list[str]] = {
    "stamp": ["rubber stamp"],
    "signature": ["signature"],
    "handwriting": ["handwritten text"],
}

# Several phrasings per type, to find the best ones on the test files.
SWEEP_CONCEPTS: dict[str, list[str]] = {
    "stamp": ["rubber stamp", "ink stamp", "official seal", "stamp"],
    "signature": ["signature", "handwritten signature"],
    "handwriting": ["handwritten text", "handwritten note", "handwriting"],
}

_HEADER = re.compile(r"^<(\d+)f(?:;[^>]*)?>")
_RECORD = re.compile(r",?(\d+)((?:<\|[A-Za-z][A-Za-z0-9_.-]*(?:;[^|]*)?\|>)+)")
_TOKEN = re.compile(r"<\|([A-Za-z][A-Za-z0-9_.-]*)(?:;([^|]*))?\|>")


@dataclass
class SamBox:
    object_id: int
    x1: int  # inclusive pixel corners
    y1: int
    x2: int
    y2: int
    width: int  # size of the image the box refers to
    height: int
    confidence: float | None

    def fraction(self) -> list[float]:
        """[x0, y0, x1, y1] as fractions of the page width and height."""
        return [
            round(self.x1 / self.width, 5),
            round(self.y1 / self.height, 5),
            round((self.x2 + 1) / self.width, 5),
            round((self.y2 + 1) / self.height, 5),
        ]


def _fields(body: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (body or "").split(";"):
        if "=" in part:
            key, value = part.split("=", 1)
            out[key.strip()] = value.strip()
    return out


def _confidence(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    return number if 0.0 <= number <= 1.0 else None


def parse_sam_output(text: str) -> tuple[list[SamBox], list[str]]:
    """Parse SAM 3.1 output text into boxes; also return a list of problems found."""
    boxes: list[SamBox] = []
    problems: list[str] = []
    for line_number, raw in enumerate((text or "").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        header = _HEADER.match(line)
        body = line[header.end():] if header else line
        for record in _RECORD.finditer(body):
            object_id = int(record.group(1))
            tokens = {name: _fields(fields) for name, fields in _TOKEN.findall(record.group(2))}
            box = tokens.get("box")
            if box is None:
                problems.append(f"line {line_number}, object {object_id}: no box")
                continue
            try:
                x1, y1, x2, y2, w, h = (int(box[key]) for key in ("x1", "y1", "x2", "y2", "w", "h"))
            except (KeyError, ValueError):
                problems.append(f"line {line_number}, object {object_id}: unreadable box {box}")
                continue
            if not (w > 0 and h > 0 and 0 <= x1 <= x2 < w and 0 <= y1 <= y2 < h):
                problems.append(f"line {line_number}, object {object_id}: box outside the image {box}")
                continue
            confidence = _confidence(box.get("c"))
            if confidence is None:
                confidence = _confidence(tokens.get("mask", {}).get("c"))
            boxes.append(SamBox(object_id, x1, y1, x2, y2, w, h, confidence))
    return boxes, problems


def iou(a: list[float], b: list[float]) -> float:
    """Intersection over union of two [x0, y0, x1, y1] boxes."""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def area(box: list[float]) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def find_marks_on_page(client: Any, page: Page, concepts: dict[str, list[str]],
                       raw_dir: Path | None = None) -> list[dict[str, Any]]:
    """Run SAM 3.1 once per concept on one page; return every box it found."""
    image_url = image_data_url(page.path)
    found: list[dict[str, Any]] = []
    for mark_type, phrases in concepts.items():
        for phrase in phrases:
            text = client.segment(phrase, image_url, label=f"sam:p{page.number}:{_slug(phrase)}")
            if raw_dir is not None:
                raw_dir.mkdir(parents=True, exist_ok=True)
                (raw_dir / f"page-{page.number}.{mark_type}.{_slug(phrase)}.txt").write_text(text or "", encoding="utf-8")
            boxes, problems = parse_sam_output(text)
            for b in boxes:
                found.append({
                    "page": page.number,
                    "type": mark_type,
                    "found_as": phrase,
                    "box": b.fraction(),
                    "confidence": b.confidence,
                })
            for problem in problems:
                found.append({"page": page.number, "type": mark_type, "found_as": phrase, "problem": problem})
    return found


def clean_marks(found: list[dict[str, Any]], *, min_confidence: float = 0.3, min_area: float = 0.0002,
                max_area: float = 0.35, same_type_iou: float = 0.5, cross_type_iou: float = 0.6) -> list[dict[str, Any]]:
    """Drop weak, tiny, huge and duplicate boxes; number the rest M1, M2, ... in reading order."""
    candidates = [
        f for f in found
        if "box" in f
        and min_area <= area(f["box"]) <= max_area
        and (f.get("confidence") is None or f["confidence"] >= min_confidence)
    ]
    candidates.sort(key=lambda f: -(f.get("confidence") if f.get("confidence") is not None else 0.5))

    kept: list[dict[str, Any]] = []
    for f in candidates:
        duplicate = False
        for k in kept:
            if k["page"] != f["page"]:
                continue
            overlap = iou(k["box"], f["box"])
            if k["type"] == f["type"] and overlap >= same_type_iou:
                duplicate = True
            elif {k["type"], f["type"]} == {"signature", "handwriting"} and overlap >= same_type_iou:
                # A signature is handwriting too; keep the more specific label.
                if f["type"] == "signature":
                    k.update(type="signature", found_as=f["found_as"])
                duplicate = True
            elif overlap >= cross_type_iou:
                duplicate = True
            if duplicate:
                break
        if not duplicate:
            kept.append(dict(f))

    # Reading order: page, then top to bottom, then right to left (Arabic pages).
    kept.sort(key=lambda f: (f["page"], round(f["box"][1], 2), -f["box"][2]))
    for i, f in enumerate(kept, 1):
        f["mark_id"] = f"M{i}"
    return kept
