"""Muse Spark reads the pages and the close-ups of the marks, and fills in the case summary."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from .arabic import to_ascii_digits
from .meta_api import MetaAPIError, chat_output_text
from .pages import Page, crop_box, image_data_url
from .schema import CASE_SCHEMA, conform

READER_MODEL = "muse-spark-1.3"
MAX_IMAGES = 48  # the API takes up to 50 images per request

SYSTEM_PROMPT = """\
You are the Case Reader inside LAVERTY, an Arabic-English legal assistant for lawyers in the UAE.
You receive the scanned pages of one court case file, then close-ups of the stamps, signatures and \
handwritten notes found on those pages, each with a mark id such as M3. Return one JSON object that \
follows the schema exactly.

Rules:
1. Use only what the pages show. Never invent a party, date, amount, case number or law. When something \
is unclear, say so in flags.
2. Every item carries the page it comes from. Pages are numbered from 1 in the order given.
3. Dates are Gregorian, written YYYY-MM-DD. Read Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩) carefully.
4. Amounts are numbers in AED without commas. Set has_amount to false (and amount_aed to 0) when the \
file states no amount.
5. Printed text and marks: when an item is known only from a stamp or a handwritten note, set source to \
"stamp" or "handwriting" and list the mark ids it comes from. When a handwritten note corrects printed \
text, use the corrected value, set changes_printed_text on that mark, and add a flag naming both values.
6. Deadlines: what must be done, by whom and by when. When the file sets a deadline relative to another \
date (for example "within 15 days of receipt"), compute the date, set computed to true and explain the \
basis in basis_en.
7. Citations: copy each citation exactly as written in Arabic (text_ar). Give the law's kind, number and \
year and the article, also when the text says "the same law" (resolve it to the law named before). When \
the file quotes the article's words, copy the quote into quoted_text_ar; otherwise leave it empty. Do \
not judge whether an article exists: a separate citation check does that against the official law text.
8. Marks: return one entry for every mark id you received. Confirm its type, or use "not_a_mark" when \
the close-up shows printed text or noise. Transcribe its Arabic text and say in plain English what it \
records. Report any stamp, signature or handwriting you see that has no mark id, with ids X1, X2, ...
9. Parties: use the role codes, and put the role as the file words it in role_en and role_ar.
10. Write English in plain words for a busy lawyer, and Arabic in formal legal Arabic.
"""


def _pct(box: list[float]) -> str:
    return "x {:.0f}-{:.0f}%, y {:.0f}-{:.0f}% of the page".format(box[0] * 100, box[2] * 100, box[1] * 100, box[3] * 100)


def build_messages(pages: list[Page], marks: list[dict[str, Any]], *, include_schema_text: bool = False) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [
        {"type": "text", "text": f"Case file with {len(pages)} page(s). The pages follow in order."}
    ]
    for page in pages:
        content.append({"type": "text", "text": f"Page {page.number}:"})
        content.append({"type": "image_url", "image_url": {"url": image_data_url(page.path)}})

    by_page = {p.number: p for p in pages}
    room = max(0, MAX_IMAGES - len(pages))
    if marks:
        content.append({"type": "text", "text": (
            "Close-ups of the marks an image model found on the pages. The image model can be wrong: "
            "check each one against the page.")})
        ranked = sorted(marks, key=lambda m: -(m.get("confidence") if m.get("confidence") is not None else 0.5))
        with_image = {m["mark_id"] for m in ranked[:room]}
        for m in marks:
            line = f"Mark {m['mark_id']}: page {m['page']}, found as {m['type']}, at {_pct(m['box'])}."
            if m["mark_id"] in with_image and m["page"] in by_page:
                content.append({"type": "text", "text": line})
                crop = crop_box(by_page[m["page"]].path, m["box"])
                content.append({"type": "image_url", "image_url": {"url": image_data_url(crop)}})
            else:
                content.append({"type": "text", "text": line + " (no close-up; look at the page)"})
    else:
        content.append({"type": "text", "text": (
            "The image model found no stamps, signatures or handwriting. Report any you see, "
            "with ids X1, X2, ...")})

    closing = "Return the JSON object now."
    if include_schema_text:
        closing = ("Return only one JSON object, with no other text, that matches this JSON Schema:\n"
                   + json.dumps(CASE_SCHEMA, ensure_ascii=False))
    content.append({"type": "text", "text": closing})
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": content}]


_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$")
_DMY = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})$")


def normalize_date(text: str) -> str:
    """'٠٦/١٠/٢٠٢٦' or '6/10/2026' (day first, as in the UAE) -> '2026-10-06'; anything else unchanged."""
    s = to_ascii_digits((text or "").strip())
    m = _ISO.match(s)
    if m:
        y, mo, d = m.groups()
    else:
        m = _DMY.match(s)
        if not m:
            return s
        d, mo, y = m.groups()
    try:
        return date(int(y), int(mo), int(d)).isoformat()
    except ValueError:
        return s


def _fix_dates(summary: dict[str, Any]) -> dict[str, Any]:
    for kind in ("dates", "deadlines"):
        for item in summary[kind]:
            item["date"] = normalize_date(item["date"])
    return summary


def parse_json_text(text: str) -> dict[str, Any] | None:
    """Read a JSON object from model text, tolerating code fences or words around it."""
    if not text:
        return None
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    for candidate in (cleaned, cleaned[cleaned.find("{"): cleaned.rfind("}") + 1]):
        try:
            value = json.loads(candidate)
        except (ValueError, TypeError):
            continue
        if isinstance(value, dict):
            return value
    return None


def read_case(client: Any, pages: list[Page], marks: list[dict[str, Any]], *, out_dir: Path,
              model: str = READER_MODEL, reasoning_effort: str | None = "high",
              max_completion_tokens: int = 32000) -> tuple[dict[str, Any], str]:
    """Ask Muse Spark for the case summary. Returns (summary, how the JSON was obtained)."""
    attempts: list[tuple[str, dict[str, Any] | None]] = [
        ("json_schema", {"type": "json_schema", "json_schema": {"name": "case_summary", "schema": CASE_SCHEMA}}),
        ("json_object", {"type": "json_object"}),
        ("plain", None),
    ]
    last_error: Exception | None = None
    for mode, response_format in attempts:
        messages = build_messages(pages, marks, include_schema_text=(mode != "json_schema"))
        try:
            data = client.chat(model, messages, response_format=response_format,
                               reasoning_effort=reasoning_effort,
                               max_completion_tokens=max_completion_tokens, label=f"reader:{mode}")
        except MetaAPIError as exc:
            last_error = exc
            if exc.status == 400:
                (out_dir / f"reader.{mode}.error.txt").write_text(str(exc), encoding="utf-8")
                continue  # this output mode was refused; try the next one
            raise
        (out_dir / f"reader.{mode}.response.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        parsed = parse_json_text(chat_output_text(data))
        if parsed is not None:
            return _fix_dates(conform(parsed, CASE_SCHEMA)), mode
        last_error = ValueError(f"no JSON object in the {mode} answer")
    raise RuntimeError(f"Muse Spark did not return a usable answer: {last_error}")
