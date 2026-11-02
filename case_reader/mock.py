"""Offline stand-in for the Meta Model API, built from the answer key.

It lets the whole pipeline run without a key, to test the plumbing. It makes a
few deliberate mistakes so the scorer has something to catch. Its output is
always labelled as a mock run and is never a model result.
"""

from __future__ import annotations

import json
import random
import re
from datetime import date, timedelta
from typing import Any

from .answer_key import parse_law, role_code
from .citations import LawIndex
from .marks import SWEEP_CONCEPTS, iou
from .pages import Page, image_data_url

_MARK_LINE = re.compile(r"Mark (M\d+): page (\d+), found as (\w+), at x (\d+)-(\d+)%, y (\d+)-(\d+)%")


def _concept_type(concept: str) -> str:
    for mark_type, phrases in SWEEP_CONCEPTS.items():
        if concept in phrases:
            return mark_type
    return "handwriting"


def _source(text: str | None) -> str:
    text = text or ""
    if "printed" in text or not text:
        return "printed"
    if "stamp" in text:
        return "stamp"
    return "handwriting"


class MockClient:
    def __init__(self, case_key: dict[str, Any], marks_key: dict[str, Any], pages: list[Page]):
        self.key = case_key
        self.marks = marks_key["marks"]
        self.page_by_url = {image_data_url(p.path): p for p in pages}
        self.calls = 0

    # SAM 3.1 stand-in --------------------------------------------------------

    def segment(self, concept: str, image_url: str, *, include_confidence: bool = True, label: str = "sam") -> str:
        self.calls += 1
        page = self.page_by_url.get(image_url)
        if page is None:
            return ""
        mark_type = _concept_type(concept)
        rng = random.Random(f"{self.key['case']}:{page.number}:{concept}")
        records = []
        wanted = [m for m in self.marks if m["page"] == page.number and m["type"] == mark_type]
        if page.number == 1 and mark_type == "handwriting" and wanted:
            wanted = wanted[1:]  # deliberate miss
        boxes = [m["box"] for m in wanted]
        if page.number == 1 and mark_type == "handwriting":
            boxes.append([0.55, 0.30, 0.85, 0.33])  # deliberate false find over printed text
        for i, box in enumerate(boxes):
            j = [v + rng.uniform(-0.006, 0.006) for v in box]
            x1 = max(0, int(j[0] * page.width))
            y1 = max(0, int(j[1] * page.height))
            x2 = min(page.width - 1, int(j[2] * page.width) - 1)
            y2 = min(page.height - 1, int(j[3] * page.height) - 1)
            c = 0.41 if box == [0.55, 0.30, 0.85, 0.33] else round(rng.uniform(0.8, 0.97), 2)
            records.append(f"{i}<|box;x1={x1};y1={y1};x2={x2};y2={y2};w={page.width};h={page.height};c={c}|>"
                           f"<|mask;x=0;y=0;data=1,1,!A;c={c}|>")
        return ("<0f>" + ",".join(records)) if records else ""

    # Muse Spark stand-in -----------------------------------------------------

    def chat(self, model: str, messages: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
        self.calls += 1
        texts = [part.get("text", "") for part in messages[-1]["content"] if part.get("type") == "text"]
        seen_marks = [m.groups() for t in texts for m in [_MARK_LINE.search(t)] if m]
        answer = self._reader_answer(seen_marks)
        return {"choices": [{"message": {"role": "assistant", "content": json.dumps(answer, ensure_ascii=False)}}],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "mock": True}

    def _reader_answer(self, seen_marks: list[tuple[str, ...]]) -> dict[str, Any]:
        k = self.key
        law_index = LawIndex()
        parties = [{"role": role_code(p["role"]), "role_en": p["role"], "role_ar": "",
                    "name_ar": p["name_ar"], "name_en": p["name_en"], "details_en": p.get("details_en", ""),
                    "pages": p["pages"]} for p in k["parties"]]
        parties[-1]["role"] = "other"  # deliberate wrong role
        dates = [{"date": d["date"], "what_en": d["what_en"], "what_ar": "", "page": d["page"],
                  "source": _source(d.get("source")), "mark_ids": []} for d in k["dates"]]
        last = date.fromisoformat(dates[-1]["date"]) + timedelta(days=1)
        dates[-1]["date"] = last.isoformat()  # deliberate wrong date
        claims = [{"item_en": c["item_en"], "item_ar": "", "has_amount": c["amount_aed"] is not None,
                   "amount_aed": c["amount_aed"] or 0, "page": c["page"]} for c in k["claims"]]
        if len(claims) > 2 and claims[1]["has_amount"]:
            claims.pop(1)  # deliberate miss
        citations = []
        for c in k["citations"]:
            law = parse_law(c["law"])
            quote = c.get("quote_ar", "")
            if not quote and c.get("quote_matches_official_text"):
                found, _ = law_index.find(law["number"], law["year"], law["kind"], law["emirate"])
                quote = (found or {}).get("texts", {}).get(c["article"], {}).get("ar", "")
            citations.append({"text_ar": c["text_ar"], "law_kind": law["kind"], "emirate": law["emirate"],
                              "law_number": law["number"], "law_year": law["year"], "law_title_en": c["law"],
                              "article": c["article"], "clause": "", "quoted_text_ar": quote, "page": c["page"]})
        marks = []
        for mark_id, page, mark_type, x0, x1, y0, y1 in seen_marks:
            box = [int(x0) / 100, int(y0) / 100, int(x1) / 100, int(y1) / 100]
            best = max((m for m in self.marks if m["page"] == int(page)),
                       key=lambda m: iou(m["box"], box), default=None)
            if best is None or iou(best["box"], box) < 0.3:
                marks.append({"mark_id": mark_id, "page": int(page), "type": "not_a_mark", "text_ar": "",
                              "meaning_en": "Printed text, not a mark.", "meaning_ar": "", "changes_printed_text": False})
            else:
                marks.append({"mark_id": mark_id, "page": int(page), "type": best["type"],
                              "text_ar": best.get("text_ar") or "", "meaning_en": best["label_en"], "meaning_ar": "",
                              "changes_printed_text": "corrected" in best["label_en"].lower()})
        court = k["court"]
        return {
            "case_title_en": k["title_en"], "case_title_ar": "", "case_type": "other",
            "summary_en": "Mock summary built from the answer key.", "summary_ar": "",
            "pages": [{"page": p["page"], "document_en": p["document_en"], "document_ar": p["document_ar"]}
                      for p in k["pages"]],
            "court": {"name_en": court["name_en"], "name_ar": court["name_ar"],
                      "case_number": court.get("case_number", ""), "case_number_source": "printed",
                      "pages": court["pages"]},
            "parties": parties, "dates": dates,
            "deadlines": [{"date": d["date"], "time": "", "who_en": d["who"], "what_en": d["what_en"], "what_ar": "",
                           "page": d["page"], "computed": bool(d.get("computed")), "basis_en": "",
                           "source": "printed", "mark_ids": []} for d in k["deadlines"]],
            "claims": claims,
            "key_facts": [{"fact_en": f["fact_en"], "fact_ar": "", "page": f["page"],
                           "source": _source(f.get("source")), "mark_ids": []} for f in k["key_facts"]],
            "citations": citations, "marks": marks,
            "flags": [{"flag_en": f, "flag_ar": "", "page": 1, "severity": "medium"} for f in k["reader_should_flag"]],
        }
