"""Second look: place the marks SAM 3.1 did not find more precisely.

SAM 3.1 finds stamps and signatures, but no phrasing made it find handwriting. Muse Spark reads
every handwritten note and gives its position on the whole page, but roughly (run 5: median box
overlap 0.24 with the answer key). Here each such mark gets a close-up: the area around Muse
Spark's position is cut out and sent back to Muse Spark, which places the note again inside the
close-up, where a percent is a few pixels instead of a few lines.
"""

from __future__ import annotations

from typing import Any, Callable

from PIL import Image

from .meta_api import MetaAPIError, chat_output_text
from .pages import Page, image_data_url
from .reader import parse_json_text

TYPE_WORDS = {"handwriting": "handwritten note", "stamp": "stamp", "signature": "signature"}

PLACE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "found": {"type": "boolean"},
        "x_from_pct": {"type": "number"}, "x_to_pct": {"type": "number"},
        "y_from_pct": {"type": "number"}, "y_to_pct": {"type": "number"},
    },
    "required": ["found", "x_from_pct", "x_to_pct", "y_from_pct", "y_to_pct"],
}

PROMPT = """\
This image is a close-up cut from page {page} of a scanned Arabic court file. It contains a {what} \
that reads: «{text}». Find that {what} in this image and give the tightest box around its ink, as \
percentages of THIS image: x_from_pct and x_to_pct (0 at the left edge, 100 at the right) and \
y_from_pct and y_to_pct (0 at the top, 100 at the bottom). Include all of its ink and no printed text. \
If it is not in this image, set found to false. Return only the JSON object."""


def _box(mark: dict[str, Any]) -> list[float] | None:
    try:
        x1, x2, y1, y2 = (float(mark.get(k) or 0) for k in ("x_from_pct", "x_to_pct", "y_from_pct", "y_to_pct"))
    except (TypeError, ValueError):
        return None
    if not (0 <= x1 < x2 <= 100 and 0 <= y1 < y2 <= 100):
        return None
    return [x1 / 100, y1 / 100, x2 / 100, y2 / 100]


def close_up_region(box: list[float], *, grow: float = 0.6, min_w: float = 0.30, min_h: float = 0.10) -> list[float]:
    """The page area to cut out around a rough box: the box grown on every side, at least min_w x min_h."""
    x1, y1, x2, y2 = box
    w, h = x2 - x1, y2 - y1
    cw, ch = max(w * (1 + 2 * grow), min_w), max(h * (1 + 2 * grow), min_h)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    left, top = min(max(0.0, cx - cw / 2), max(0.0, 1 - cw)), min(max(0.0, cy - ch / 2), max(0.0, 1 - ch))
    return [round(left, 4), round(top, 4), round(min(1.0, left + cw), 4), round(min(1.0, top + ch), 4)]


def to_page(region: list[float], answer: dict[str, Any]) -> list[float] | None:
    """Map a box given in percent of the close-up back to page fractions, or None if it is not usable."""
    try:
        x1, x2, y1, y2 = (float(answer[k]) for k in ("x_from_pct", "x_to_pct", "y_from_pct", "y_to_pct"))
    except (KeyError, TypeError, ValueError):
        return None
    if not answer.get("found") or not (0 <= x1 < x2 <= 100 and 0 <= y1 < y2 <= 100):
        return None
    if (x2 - x1) * (y2 - y1) < 4:  # a dot, not a note
        return None
    rx1, ry1, rx2, ry2 = region
    rw, rh = rx2 - rx1, ry2 - ry1
    return [round(rx1 + rw * x1 / 100, 4), round(ry1 + rh * y1 / 100, 4),
            round(rx1 + rw * x2 / 100, 4), round(ry1 + rh * y2 / 100, 4)]


def refine_reader_marks(client: Any, pages: list[Page], reader: dict[str, Any], *, model: str,
                        reasoning_effort: str | None = "medium",
                        log: Callable[[str], None] = print) -> int:
    """Give every mark the reader placed itself (ids X1, X2, ...) a close-up second look.

    Updates the marks' x/y percentages in place and records the first position under 'rough_box'.
    Returns how many marks were placed again. Any failure keeps the first position.
    """
    by_number = {p.number: p for p in pages}
    placed = 0
    for mark in reader.get("marks", []):
        if not str(mark.get("mark_id", "")).startswith("X"):
            continue
        rough, page = _box(mark), by_number.get(mark.get("page"))
        if rough is None or page is None:
            continue
        region = close_up_region(rough)
        with Image.open(page.path) as im:
            img = im.convert("RGB")
        w, h = img.size
        crop = img.crop((int(region[0] * w), int(region[1] * h), int(region[2] * w), int(region[3] * h)))
        what = TYPE_WORDS.get(mark.get("type"), "mark")
        text = (mark.get("text_ar") or mark.get("meaning_en") or "").strip()[:200]
        messages = [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": image_data_url(crop, max_side=1600)}},
            {"type": "text", "text": PROMPT.format(page=page.number, what=what, text=text)},
        ]}]
        try:
            data = client.chat(model, messages,
                               response_format={"type": "json_schema",
                                                "json_schema": {"name": "mark_position", "schema": PLACE_SCHEMA}},
                               reasoning_effort=reasoning_effort, max_completion_tokens=4000,
                               label=f"refine:{mark['mark_id']}")
        except MetaAPIError as exc:
            if exc.status in (401, 403):
                raise
            log(f"  close-up of {mark['mark_id']} failed ({exc}); keeping the first position")
            continue
        answer = parse_json_text(chat_output_text(data)) or {}
        box = to_page(region, answer) if isinstance(answer, dict) else None
        if box is None:
            continue
        mark["rough_box"] = rough
        mark["x_from_pct"], mark["y_from_pct"] = round(box[0] * 100, 2), round(box[1] * 100, 2)
        mark["x_to_pct"], mark["y_to_pct"] = round(box[2] * 100, 2), round(box[3] * 100, 2)
        mark["placed_by"] = "close-up"
        placed += 1
    return placed
