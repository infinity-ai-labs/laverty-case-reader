"""Citation check: does each cited article exist, and does any quoted wording match the official text?

This is a small open version of the check, covering the laws in `laws/index.json`.
A citation it cannot check is labelled "not checked"; it is never passed quietly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .arabic import compare_quote, to_ascii_digits

LAW_INDEX = Path(__file__).resolve().parent.parent / "laws" / "index.json"

QUOTE_CLOSE = 0.70  # word similarity at or above this, but not exact: the quote differs in places


class LawIndex:
    def __init__(self, path: Path = LAW_INDEX):
        data = json.loads(path.read_text(encoding="utf-8"))
        self.laws: list[dict[str, Any]] = data["laws"]

    def find(self, number: str, year: int, kind: str = "", emirate: str = "") -> dict[str, Any] | None:
        number = to_ascii_digits(str(number or "")).strip().lstrip("0")
        try:
            year = int(to_ascii_digits(str(year)))
        except ValueError:
            return None
        matches = [law for law in self.laws if law["number"] == number and law["year"] == year]
        if len(matches) > 1:
            local = kind == "local_law" or bool(emirate)
            narrowed = [law for law in matches if (law["kind"] == "local_law") == local]
            matches = narrowed or matches
        return matches[0] if matches else None


def article_key(article: str) -> str:
    """'المادة (٤٧)' -> '47'; '25/1/أ' -> '25'; '12 مكرر' -> '12 bis'."""
    text = to_ascii_digits(article or "")
    match = re.search(r"\d+", text)
    if not match:
        return ""
    key = str(int(match.group(0)))
    if re.search(r"مكرر|bis", text, re.IGNORECASE):
        key += " bis"
    return key


def check_citation(citation: dict[str, Any], index: LawIndex) -> dict[str, Any]:
    law = index.find(citation.get("law_number", ""), citation.get("law_year", 0),
                     citation.get("law_kind", ""), citation.get("emirate", ""))
    if law is None:
        return {
            "status": "not_checked",
            "label_en": "Not checked: this law is not in the Case Reader's law index. Check it by hand.",
            "label_ar": "لم يتم التحقق: هذا القانون غير موجود في فهرس القوانين لدى قارئ القضايا. يرجى التحقق يدوياً.",
        }
    key = article_key(citation.get("article", ""))
    base = {"law_id": law["id"], "law_title_en": law["title_en"], "law_title_ar": law["title_ar"],
            "article": key, "article_count": law["article_count"],
            "source_url_en": law["source"]["url_en"], "source_url_ar": law["source"]["url_ar"]}
    if not key:
        return {**base, "status": "not_checked",
                "label_en": "Not checked: the article number could not be read. Check it by hand.",
                "label_ar": "لم يتم التحقق: تعذرت قراءة رقم المادة. يرجى التحقق يدوياً."}
    if key not in law["articles"]:
        return {**base, "status": "invalid",
                "label_en": (f"Article {key} does not exist in {law['short_en']}: "
                             f"the official text has {law['article_count']} articles."),
                "label_ar": (f"المادة ({key}) غير موجودة في {law['short_ar']}، "
                             f"إذ يتكون النص الرسمي من {law['article_count']} مادة.")}

    result = {**base, "status": "valid",
              "label_en": f"Article {key} of {law['short_en']} exists in the official text.",
              "label_ar": f"المادة ({key}) من {law['short_ar']} موجودة في النص الرسمي."}
    official = law["texts"].get(key)
    if official:
        result["official_text_ar"] = official["ar"]
        result["official_text_en"] = official["en"]
    quote = (citation.get("quoted_text_ar") or "").strip()
    if quote:
        if not official:
            result["quote"] = {"status": "not_checked",
                               "label_en": "The file quotes this article; the quote was not compared.",
                               "label_ar": "تتضمن الوثيقة اقتباساً من هذه المادة لم تتم مقارنته."}
        else:
            ratio, differences = compare_quote(quote, official["ar"])
            if ratio == 1.0:
                q = {"status": "matches", "label_en": "The quoted wording matches the official text word for word.",
                     "label_ar": "النص المقتبس مطابق للنص الرسمي حرفياً."}
            elif ratio >= QUOTE_CLOSE:
                changed = "; ".join(f"«{d['in_file'] or '—'}» instead of «{d['official'] or '—'}»" for d in differences[:4])
                changed_ar = "؛ ".join(f"«{d['in_file'] or '—'}» بدلاً من «{d['official'] or '—'}»" for d in differences[:4])
                q = {"status": "differs",
                     "label_en": f"The quoted wording differs from the official text: {changed}.",
                     "label_ar": f"النص المقتبس يختلف عن النص الرسمي: {changed_ar}."}
            else:
                q = {"status": "does_not_match", "label_en": "The quoted wording does not match the official text.",
                     "label_ar": "النص المقتبس لا يطابق النص الرسمي."}
            result["quote"] = {**q, "similarity": round(ratio, 3), "differences": differences}
    return result
