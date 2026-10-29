"""Citation check: does each cited article exist, and does any quoted wording match the official text?

This is a small open version of the check, covering the laws in `laws/index.json`.
A citation it cannot check is labelled "not checked"; it is never passed quietly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .arabic import compare_quote, normalize, to_ascii_digits

LAW_INDEX = Path(__file__).resolve().parent.parent / "laws" / "index.json"

QUOTE_CLOSE = 0.70  # word similarity at or above this: the quote is the same passage, with some words changed

FEDERAL_KINDS = {"federal_decree_law", "federal_law"}
# Normalised names (see arabic.normalize); an emirate is recognised when its name appears in the field,
# so "إمارة دبي" and "Emirate of Dubai" both read as Dubai.
EMIRATES = {
    "abu dhabi": "Abu Dhabi", "ابوظبي": "Abu Dhabi", "ابو ظبي": "Abu Dhabi",
    "dubai": "Dubai", "دبي": "Dubai",
    "sharjah": "Sharjah", "الشارقه": "Sharjah",
    "ajman": "Ajman", "عجمان": "Ajman",
    "umm al quwain": "Umm Al Quwain", "ام القيوين": "Umm Al Quwain",
    "ras al khaimah": "Ras Al Khaimah", "راس الخيمه": "Ras Al Khaimah",
    "fujairah": "Fujairah", "الفجيره": "Fujairah",
}

_ARTICLE_WORD = r"(?:المادتين|المادتان|المواد|المادة|مادة|articles?|art\.?)"
_ARTICLE_START = re.compile(_ARTICLE_WORD + r"\s*(?:رقم|no\.?|number)?\s*", re.IGNORECASE)
_CLAUSE_START = re.compile(r"(?:البند|بند|الفقرة|فقرة|clause|para(?:graph)?)\s*(?:رقم)?\s*", re.IGNORECASE)
_FIELD_START = re.compile(r"^\s*")
_NUMBER = re.compile(r"\(?\s*(\d+)\s*\)?(\s*(?:مكرر|bis))?", re.IGNORECASE)
_SEP = re.compile(r"\s*(و|,|،|and|&|-|–|—|إلى|الى|حتى|to|through)\s*(?:" + _ARTICLE_WORD + r")?\s*(?:رقم|no\.?)?\s*",
                  re.IGNORECASE)
_RANGE_SEPS = {"-", "–", "—", "إلى", "الى", "حتى", "to", "through"}
_MAX_RANGE = 30
_LAW_REF = re.compile(r"رقم\s*\(?\s*(\d+)\s*\)?\s*لسنة\s*\(?\s*(\d{4})|no\.?\s*\(?\s*(\d+)\s*\)?\s*of\s*(\d{4})",
                      re.IGNORECASE)


def _emirate(name: str) -> str:
    text = normalize(name or "")
    for key, emirate in EMIRATES.items():
        if key in text:
            return emirate
    return ""


def _scope(kind: str, emirate: str) -> tuple[str, str] | None:
    """('federal', '') or ('local', <emirate>); None when the citation can't be placed."""
    if kind in FEDERAL_KINDS:
        return ("federal", "")
    if kind == "local_law":
        found = _emirate(emirate)
        return ("local", found) if found else None
    return None


class LawIndex:
    def __init__(self, path: Path = LAW_INDEX):
        data = json.loads(path.read_text(encoding="utf-8"))
        self.laws: list[dict[str, Any]] = data["laws"]

    def find(self, number: str, year: Any, kind: str = "", emirate: str = "") -> tuple[dict[str, Any] | None, str]:
        """The law this citation names, or (None, why it can't be checked)."""
        scope = _scope(kind, emirate)
        if scope is None:
            return None, "local_without_emirate" if kind == "local_law" else "unsupported_kind"
        number = to_ascii_digits(str(number or "")).strip().lstrip("0")
        try:
            year = int(to_ascii_digits(str(year)))
        except ValueError:
            return None, "not_in_index"
        matches = [
            law for law in self.laws
            if law["number"] == number and law["year"] == year
            and (("federal", "") if law["kind"] in FEDERAL_KINDS else ("local", law["emirate"])) == scope
        ]
        return (matches[0], "") if len(matches) == 1 else (None, "not_in_index")


def _numbers_after(start: re.Pattern[str], text: str) -> list[str]:
    """Numbers that follow `start`, with lists ('43 و 145'), ranges ('73-76', 'من 73 إلى 76') and 'مكرر'."""
    t = to_ascii_digits(text or "")
    found: list[str] = []
    pos = 0
    # re clamps a start position past the end back to the end, so stop explicitly there.
    while pos <= len(t) and (m := start.search(t, pos)) is not None:
        first = _NUMBER.match(t, m.end())
        if first is None:
            pos = max(m.end(), pos + 1)
            continue
        items = [(int(first.group(1)), bool(first.group(2)))]
        p = first.end()
        while (sep := _SEP.match(t, p)) is not None and (nxt := _NUMBER.match(t, sep.end())) is not None:
            number, last = int(nxt.group(1)), items[-1][0]
            if sep.group(1).lower() in _RANGE_SEPS and last < number <= last + _MAX_RANGE:
                items += [(k, False) for k in range(last + 1, number)]
            items.append((number, bool(nxt.group(2))))
            p = nxt.end()
        for number, bis in items:
            key = f"{number} bis" if bis else str(number)
            if key not in found:
                found.append(key)
        pos = max(p, pos + 1)
    return found


def article_numbers(text: str) -> list[str]:
    """Articles a citation names after an article word:
    'البند (1) من المادة رقم (145)' -> ['145']; 'المادتين (43) و(145)' -> ['43', '145'];
    'المواد (73-76)' -> ['73', '74', '75', '76']; 'المادة (12) مكرراً' -> ['12 bis']."""
    return _numbers_after(_ARTICLE_START, text)


def clause_numbers(text: str) -> list[str]:
    return _numbers_after(_CLAUSE_START, text)


def field_numbers(article: str) -> list[str]:
    """Articles in an extracted article field: '47', '(٤٧)', '43 و 145', '73-76', 'المادة 47', '25/1/أ' -> 25."""
    text = to_ascii_digits(article or "")
    numbers = article_numbers(text)
    if numbers:
        return numbers
    if _CLAUSE_START.search(text):
        return []  # a clause, not an article
    return _numbers_after(_FIELD_START, text)


def article_key(article: str) -> str:
    """The one article a field names, or '' (none, or several)."""
    numbers = field_numbers(article)
    return numbers[0] if len(numbers) == 1 else ""


def _law_count(text: str) -> int:
    refs = {(m.group(1) or m.group(3), m.group(2) or m.group(4)) for m in _LAW_REF.finditer(to_ascii_digits(text or ""))}
    return len(refs)


def resolve_articles(citation: dict[str, Any]) -> list[str]:
    """Every article this citation entry should be checked against.

    The citation as written on the page comes first: in 'البند (1) من المادة (145)' the article is
    145 even when the extracted field says 1 (a clause number). When the field names another
    article, both are checked. When the words name more than one law, only the field is used,
    because the words' other articles may belong to the other law.
    """
    text = citation.get("text_ar", "")
    field = field_numbers(citation.get("article", ""))
    if _law_count(text) > 1:
        return field
    written = article_numbers(text)
    clauses = set(clause_numbers(text))
    bases = {w.split()[0] for w in written}
    out = list(written)
    for n in field:
        if n in out or n.split()[0] in bases:
            continue  # already there (or the same article written as 'مكرر')
        if n in clauses:
            continue  # a clause number put in the article field
        out.append(n)
    return out


def split_multi_article(citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One entry per article to check (field 'article_checked'), without duplicates."""
    result: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    for c in citations:
        articles = resolve_articles(c) or [""]
        for article in articles:
            entry = {**c, "article_checked": article}
            key = (c.get("text_ar"), str(c.get("law_number")), str(c.get("law_year")), c.get("law_kind"),
                   _emirate(c.get("emirate", "")), article, c.get("page"))
            if key in seen:
                continue
            seen.add(key)
            result.append(entry)
    return result


NOT_CHECKED = {
    "not_in_index": ("Not checked: this law is not in the Case Reader's law index. Check it by hand.",
                     "لم يتم التحقق: هذا القانون غير موجود في فهرس القوانين لدى قارئ القضايا. يرجى التحقق يدوياً."),
    "unsupported_kind": ("Not checked: the Case Reader checks laws and decree-laws only. Check this citation by hand.",
                         "لم يتم التحقق: يتحقق قارئ القضايا من القوانين والمراسيم بقوانين فقط. يرجى التحقق يدوياً."),
    "local_without_emirate": ("Not checked: the citation does not say which emirate's law it is. Check it by hand.",
                              "لم يتم التحقق: لا يبيّن الاستشهاد الإمارة التي صدر عنها القانون. يرجى التحقق يدوياً."),
    "no_article": ("Not checked: no single article number could be read. Check it by hand.",
                   "لم يتم التحقق: تعذرت قراءة رقم مادة واحد. يرجى التحقق يدوياً."),
}


def check_citation(citation: dict[str, Any], index: LawIndex) -> dict[str, Any]:
    law, why = index.find(citation.get("law_number", ""), citation.get("law_year", 0),
                          citation.get("law_kind", ""), citation.get("emirate", ""))
    if law is None:
        en, ar = NOT_CHECKED[why]
        return {"status": "not_checked", "reason": why, "article": citation.get("article_checked", ""),
                "label_en": en, "label_ar": ar}

    base = {"law_id": law["id"], "law_title_en": law["title_en"], "law_title_ar": law["title_ar"],
            "article_count": law["article_count"],
            "source_url_en": law["source"]["url_en"], "source_url_ar": law["source"]["url_ar"]}
    if law.get("status", {}).get("state") == "repealed":
        # The article may exist and still be the wrong law for the facts: say so every time.
        base["law_status"] = law["status"]
    if "article_checked" in citation:
        key = citation["article_checked"]
    else:
        articles = resolve_articles(citation)
        key = articles[0] if len(articles) == 1 else ""
    if not key:
        en, ar = NOT_CHECKED["no_article"]
        return {**base, "status": "not_checked", "reason": "no_article", "article": "", "label_en": en, "label_ar": ar}
    base["article"] = key
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
        result["quote"] = _check_quote(quote, official)
    return result


def _check_quote(quote: str, official: dict[str, str] | None) -> dict[str, Any]:
    if not official:
        return {"status": "not_checked",
                "label_en": "The file quotes this article; the quote was not compared, because this index has no text for it.",
                "label_ar": "تتضمن الوثيقة اقتباساً من هذه المادة، ولم تتم مقارنته لعدم توفر نصها في هذا الفهرس."}
    ratio, differences = compare_quote(quote, official["ar"])
    if ratio == 1.0:
        return {"status": "matches", "similarity": 1.0, "differences": [],
                "label_en": "The quoted wording matches the official text word for word.",
                "label_ar": "النص المقتبس مطابق للنص الرسمي حرفياً."}
    if ratio < QUOTE_CLOSE:
        return {"status": "does_not_match", "similarity": round(ratio, 3), "differences": differences,
                "label_en": "The quoted wording does not match the official text.",
                "label_ar": "النص المقتبس لا يطابق النص الرسمي."}
    changed = "; ".join(f"«{d['in_file'] or '—'}» instead of «{d['official'] or '—'}»" for d in differences[:4])
    changed_ar = "؛ ".join(f"«{d['in_file'] or '—'}» بدلاً من «{d['official'] or '—'}»" for d in differences[:4])
    slight = all(d["kind"] == "reading" for d in differences)
    # One changed word can reverse the law ("debtor" for "creditor"), so every difference is reported
    # in full; a letter-level one may also be a misreading of the scan, and the label says so.
    note_en = " It may be a misreading of the scan, or a changed word: check the page." if slight else ""
    note_ar = " قد يكون ذلك خطأً في قراءة المستند الممسوح أو كلمة معدّلة: يرجى مراجعة الصفحة." if slight else ""
    return {"status": "differs", "slight": slight, "similarity": round(ratio, 3), "differences": differences,
            "label_en": f"The quoted wording differs from the official text: {changed}.{note_en}",
            "label_ar": f"النص المقتبس يختلف عن النص الرسمي: {changed_ar}.{note_ar}"}
