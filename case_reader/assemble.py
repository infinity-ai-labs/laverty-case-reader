"""Put the reader's answer, the marks and the citation check together into one case summary."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .citations import LawIndex, check_citation
from .pages import Page

SOURCE_WORDS = {"stamp": ("a stamp", "ختم"), "handwriting": ("a handwritten note", "ملاحظة بخط اليد")}


def _merge_marks(found: list[dict[str, Any]], reviews: list[dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    review_by_id = {r["mark_id"]: r for r in reviews if r.get("mark_id")}
    marks, rejected = [], []
    for m in found:
        review = review_by_id.pop(m["mark_id"], None)
        entry = {
            "mark_id": m["mark_id"], "page": m["page"], "box": m["box"],
            "type": m["type"], "found_as": m.get("found_as"), "confidence": m.get("confidence"),
            "text_ar": "", "meaning_en": "", "meaning_ar": "", "changes_printed_text": False,
            "reviewed": review is not None,
        }
        if review:
            entry.update(text_ar=review["text_ar"], meaning_en=review["meaning_en"], meaning_ar=review["meaning_ar"],
                         changes_printed_text=review["changes_printed_text"])
            if review["type"] == "not_a_mark":
                rejected.append(entry)
                continue
            entry["type"] = review["type"]
        marks.append(entry)
    # Marks the reader saw that the image model did not find (no position known).
    for review in review_by_id.values():
        if review["type"] == "not_a_mark":
            continue
        marks.append({
            "mark_id": review["mark_id"], "page": review["page"], "box": None, "type": review["type"],
            "found_as": "reader", "confidence": None, "text_ar": review["text_ar"],
            "meaning_en": review["meaning_en"], "meaning_ar": review["meaning_ar"],
            "changes_printed_text": review["changes_printed_text"], "reviewed": True,
        })
    return marks, rejected


def _auto_flags(summary: dict[str, Any]) -> list[dict[str, Any]]:
    flags: list[dict[str, Any]] = []

    def add(en: str, ar: str, page: int, severity: str) -> None:
        flags.append({"flag_en": en, "flag_ar": ar, "page": page, "severity": severity, "by": "check"})

    for c in summary["citations"]:
        check = c["check"]
        if check["status"] == "invalid":
            add(f"Citation on page {c['page']}: {check['label_en']}", check["label_ar"], c["page"], "high")
        elif check["status"] == "not_checked":
            add(f"Citation on page {c['page']} ({c['text_ar']}): {check['label_en']}", check["label_ar"],
                c["page"], "medium")
        quote = check.get("quote")
        if quote and quote["status"] in ("differs", "does_not_match"):
            add(f"Quote of article {check['article']} on page {c['page']}: {quote['label_en']}", quote["label_ar"],
                c["page"], "high" if quote["status"] == "does_not_match" else "medium")

    for kind in ("dates", "deadlines"):
        for d in summary[kind]:
            words = SOURCE_WORDS.get(d["source"])
            if words:
                add(f"{d['date']} ({d['what_en']}) appears only in {words[0]} on page {d['page']}.",
                    f"التاريخ {d['date']} ({d['what_ar'] or d['what_en']}) وارد فقط في {words[1]} في الصفحة {d['page']}.",
                    d["page"], "medium")

    for m in summary["marks"]:
        if m["changes_printed_text"]:
            add(f"Handwritten change to the printed text on page {m['page']} ({m['mark_id']}): {m['meaning_en']}",
                f"تعديل بخط اليد على النص المطبوع في الصفحة {m['page']} ({m['mark_id']}): "
                f"{m['meaning_ar'] or m['text_ar']}",
                m["page"], "high")
    return flags


def assemble(*, case_id: str, source: Path, out_dir: Path, pages: list[Page], found_marks: list[dict[str, Any]],
             reader: dict[str, Any], run: dict[str, Any], law_index: LawIndex | None = None) -> dict[str, Any]:
    law_index = law_index or LawIndex()
    page_info = {p["page"]: p for p in reader["pages"]}
    marks, rejected = _merge_marks(found_marks, reader["marks"])
    summary: dict[str, Any] = {
        "case": case_id,
        "source_file": source.name,
        "mock": bool(run.get("mock")),
        "run": run,
        "title_en": reader["case_title_en"],
        "title_ar": reader["case_title_ar"],
        "case_type": reader["case_type"],
        "summary_en": reader["summary_en"],
        "summary_ar": reader["summary_ar"],
        "pages": [
            {
                "page": p.number,
                "image": os.path.relpath(p.path, out_dir),
                "width": p.width,
                "height": p.height,
                "document_en": page_info.get(p.number, {}).get("document_en", ""),
                "document_ar": page_info.get(p.number, {}).get("document_ar", ""),
            }
            for p in pages
        ],
        "court": reader["court"],
        "parties": reader["parties"],
        "dates": sorted(reader["dates"], key=lambda d: (d["date"], d["page"])),
        "deadlines": sorted(reader["deadlines"], key=lambda d: (d["date"], d["page"])),
        "claims": reader["claims"],
        "key_facts": reader["key_facts"],
        "citations": [{**c, "check": check_citation(c, law_index)} for c in reader["citations"]],
        "marks": marks,
        "rejected_marks": rejected,
    }
    reader_flags = [{**f, "by": "reader"} for f in reader["flags"]]
    summary["flags"] = _auto_flags(summary) + reader_flags
    return summary


# -- Markdown ------------------------------------------------------------------

def _amount(c: dict[str, Any]) -> str:
    return f"AED {c['amount_aed']:,.0f}" if c["has_amount"] else ""


def _cell(text: Any) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def to_markdown(s: dict[str, Any]) -> str:
    out: list[str] = []
    if s["mock"]:
        out.append("> **Mock run.** Made without calling the models, to test the pipeline. Not a real result.\n")
    out.append(f"# {s['title_en']}\n")
    out.append(f"{s['summary_en']}\n")
    out.append(f"Source file: `{s['source_file']}` · {len(s['pages'])} pages · read with "
               f"{s['run'].get('reader_model')} and {s['run'].get('marks_model')}\n")

    high = [f for f in s["flags"] if f["severity"] == "high"]
    if high:
        out.append("## Check these first\n")
        out += [f"- **Page {f['page']}:** {f['flag_en']}" for f in high]
        out.append("")

    out.append("## Pages\n\n| Page | Document |\n|---|---|")
    out += [f"| {p['page']} | {_cell(p['document_en'])} |" for p in s["pages"]]
    court = s["court"]
    out.append(f"\n## Court\n\n{court['name_en']}" + (f", case no. {court['case_number']}" if court["case_number"] else "")
               + (f" (case number from {SOURCE_WORDS[court['case_number_source']][0]})"
                  if court["case_number_source"] in SOURCE_WORDS else "") + "\n")

    out.append("## Parties\n\n| Role | Name | Arabic | Pages |\n|---|---|---|---|")
    out += [f"| {_cell(p['role_en'])} | {_cell(p['name_en'])} | {_cell(p['name_ar'])} | "
            f"{', '.join(map(str, p['pages']))} |" for p in s["parties"]]

    out.append("\n## Deadlines\n\n| Date | Who | What | Page |\n|---|---|---|---|")
    for d in s["deadlines"]:
        what = d["what_en"]
        if d["computed"]:
            what += f" (worked out: {d['basis_en']})" if d["basis_en"] else " (worked out from the file)"
        if d["source"] in SOURCE_WORDS:
            what += f" — from {SOURCE_WORDS[d['source']][0]}"
        out.append(f"| {d['date']}{(' ' + d['time']) if d['time'] else ''} | {_cell(d['who_en'])} | {_cell(what)} | {d['page']} |")

    out.append("\n## Dates\n\n| Date | What | Page | From |\n|---|---|---|---|")
    out += [f"| {d['date']} | {_cell(d['what_en'])} | {d['page']} | {d['source']} |" for d in s["dates"]]

    out.append("\n## Claims\n\n| Claim | Amount | Page |\n|---|---|---|")
    out += [f"| {_cell(c['item_en'])} | {_amount(c)} | {c['page']} |" for c in s["claims"]]

    out.append("\n## Key facts\n")
    out += [f"- {f['fact_en']} (page {f['page']}{', ' + f['source'] if f['source'] != 'printed' else ''})"
            for f in s["key_facts"]]

    out.append("\n## Citations\n\n| Page | As cited | Check |\n|---|---|---|")
    icon = {"valid": "✅", "invalid": "❌", "not_checked": "⚠️"}
    for c in s["citations"]:
        check = c["check"]
        text = check["label_en"]
        if check.get("quote"):
            text += " " + check["quote"]["label_en"]
        out.append(f"| {c['page']} | {_cell(c['text_ar'])} | {icon[check['status']]} {_cell(text)} |")

    out.append("\n## Stamps, signatures and handwriting\n\n| Mark | Page | Type | Says | Meaning |\n|---|---|---|---|---|")
    out += [f"| {m['mark_id']} | {m['page']} | {m['type']} | {_cell(m['text_ar'])} | {_cell(m['meaning_en'])} |"
            for m in s["marks"]]

    others = [f for f in s["flags"] if f["severity"] != "high"]
    if others:
        out.append("\n## Other points to check\n")
        out += [f"- Page {f['page']}: {f['flag_en']}" for f in others]

    out.append(f"\n---\n\n<div dir=\"rtl\">\n\n# {s['title_ar'] or s['title_en']}\n\n{s['summary_ar']}\n")
    out.append("## الأطراف\n")
    out += [f"- {(p['role_ar'] + ': ') if p['role_ar'] else ''}{p['name_ar'] or p['name_en']}" for p in s["parties"]]
    out.append("\n## المواعيد\n")
    out += [f"- {d['date']}{(' ' + d['time']) if d['time'] else ''}: {d['what_ar'] or d['what_en']} (الصفحة {d['page']})"
            for d in s["deadlines"]]
    out.append("\n## الطلبات\n")
    out += [f"- {c['item_ar'] or c['item_en']}" + (f": {c['amount_aed']:,.0f} درهم" if c["has_amount"] else "")
            for c in s["claims"]]
    out.append("\n## التحقق من الاستشهادات\n")
    out += [f"- {c['text_ar']}: {c['check']['label_ar']}" for c in s["citations"]]
    out.append("\n## نقاط تستوجب الانتباه\n")
    out += [f"- الصفحة {f['page']}: {f['flag_ar'] or f['flag_en']}" for f in s["flags"]]
    out.append("\n</div>\n")
    return "\n".join(out)
