"""Score a Case Reader run against the answer key.

    python tools/score.py runs/<run-name>

Writes score.json and score.md into the run folder and prints the table.
How each item counts is described in answer-key/README.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from case_reader.answer_key import ANSWER_KEY_DIR, load_answer_key, parse_law, role_code  # noqa: E402
from case_reader.arabic import similarity, to_ascii_digits  # noqa: E402
from case_reader.citations import article_key  # noqa: E402
from case_reader.marks import iou  # noqa: E402

NAME_MATCH = 0.85
IOU_MATCH = 0.5


def _ratio(correct: int, total: int) -> str:
    return f"{correct}/{total}"


# People in the file who are not parties (a doctor, an auditor, an arbitrator): the key calls them "other";
# naming them "expert" or "witness" is just as right.
NON_PARTY_ROLES = {"other", "expert", "witness"}


def score_parties(found: list[dict], key: list[dict]) -> dict[str, Any]:
    used: set[int] = set()
    correct, misses = 0, []
    for kp in key:
        want_role = role_code(kp["role"])
        best, best_sim, best_role_ok = None, 0.0, False
        for i, p in enumerate(found):
            if i in used:
                continue
            sim = similarity(kp["name_ar"], p["name_ar"]) if p.get("name_ar") else similarity(kp["name_en"], p["name_en"])
            role_ok = p.get("role") == want_role or (want_role == "other" and p.get("role") in NON_PARTY_ROLES)
            if sim >= NAME_MATCH and (sim, role_ok) > (best_sim, best_role_ok):
                best, best_sim, best_role_ok = i, sim, role_ok
        if best is not None:
            used.add(best)
        if best is not None and best_role_ok:
            correct += 1
        else:
            reason = "not found" if best is None else f"found, but role given as {found[best].get('role')}"
            misses.append(f"{kp['name_en']} ({want_role}): {reason}")
    return {"correct": correct, "total": len(key), "found": len(found), "misses": misses}


def score_dated(found: list[dict], key: list[dict], label: str, elsewhere: list[dict] | None = None) -> dict[str, Any]:
    """Same calendar date on the same page, matched one to one."""
    unused = [(f["date"], f["page"]) for f in found]
    correct, misses = 0, []
    for k in key:
        if (k["date"], k["page"]) in unused:
            unused.remove((k["date"], k["page"]))
            correct += 1
            continue
        pages = sorted({f["page"] for f in found if f["date"] == k["date"]})
        if pages:
            where = f"found on page {pages}"
        elif elsewhere and any(e["date"] == k["date"] for e in elsewhere):
            where = "listed only under deadlines"
        else:
            where = "not found"
        misses.append(f"{label} {k['date']} (page {k['page']}, {k['what_en']}): {where}")
    return {"correct": correct, "total": len(key), "found": len(found), "misses": misses}


def score_claims(found: list[dict], key: list[dict]) -> dict[str, Any]:
    amounts = [c["amount_aed"] for c in found if c.get("has_amount")]
    want = [c for c in key if c["amount_aed"] is not None]
    correct, misses = 0, []
    remaining = list(amounts)
    for k in want:
        hit = next((a for a in remaining if abs(a - k["amount_aed"]) < 0.5), None)
        if hit is None:
            misses.append(f"AED {k['amount_aed']:,} ({k['item_en']}): not found")
        else:
            remaining.remove(hit)
            correct += 1
    return {"correct": correct, "total": len(want), "found": len(amounts), "misses": misses}


def _checked_article(c: dict) -> str:
    """The article the check looked at (after reading the citation as written), else the raw field."""
    return c.get("article_checked") or (c.get("check") or {}).get("article") or article_key(c.get("article", ""))


def score_citations(found: list[dict], key: list[dict]) -> dict[str, Any]:
    def law_of(c: dict) -> tuple[str, int]:
        return to_ascii_digits(str(c.get("law_number", ""))).lstrip("0"), int(c.get("law_year") or 0)

    used: set[int] = set()
    correct, caught, invalid_total, misses = 0, 0, 0, []
    quotes_right, quotes_total, misquotes_caught, misquotes_total = 0, 0, 0, 0
    for k in key:
        law = parse_law(k["law"])
        want = ((law["number"], law["year"]), k["article"])
        candidates = [i for i, c in enumerate(found)
                      if i not in used and (law_of(c), _checked_article(c)) == want]
        same_page = [i for i in candidates if found[i].get("page") == k["page"]]
        pick = (same_page or candidates or [None])[0]
        expected = "not_checked" if k.get("not_in_index") else ("valid" if k["valid"] else "invalid")
        if expected == "invalid":
            invalid_total += 1
        has_quote = "quote_ar" in k or "quote_matches_official_text" in k
        if has_quote:
            quotes_total += 1
            misquotes_total += k.get("quote_matches_official_text") is False
        if pick is None:
            misses.append(f"{k['text_ar']} (page {k['page']}): not found")
            continue
        used.add(pick)
        check = found[pick]["check"]
        if check["status"] == expected:
            correct += 1
            caught += expected == "invalid"
        else:
            misses.append(f"{k['text_ar']} (page {k['page']}): check said {check['status']}, expected {expected}")
        if has_quote:
            quote = (check.get("quote") or {}).get("status")
            if k.get("quote_matches_official_text") is False:
                if quote in ("differs", "does_not_match"):
                    quotes_right += 1
                    misquotes_caught += 1
                else:
                    misses.append(f"misquote of article {k['article']} (page {k['page']}): quote check said {quote}")
            elif quote == "matches":
                quotes_right += 1
            else:
                misses.append(f"quote of article {k['article']} (page {k['page']}): quote check said {quote}")
    return {"correct": correct, "total": len(key), "found": len(found), "misses": misses,
            "invalid_caught": caught, "invalid_total": invalid_total,
            "quotes_right": quotes_right, "quotes_total": quotes_total,
            "misquotes_caught": misquotes_caught, "misquotes_total": misquotes_total}


def match_marks(found: list[dict], key: list[dict], *, same_type: bool = True) -> list[tuple[int, int, float]]:
    pairs = []
    for i, f in enumerate(found):
        for j, k in enumerate(key):
            if f["page"] != k["page"] or (same_type and f["type"] != k["type"]):
                continue
            overlap = iou(f["box"], k["box"])
            if overlap >= IOU_MATCH:
                pairs.append((overlap, i, j))
    pairs.sort(reverse=True)
    used_f, used_k, matches = set(), set(), []
    for overlap, i, j in pairs:
        if i in used_f or j in used_k:
            continue
        used_f.add(i)
        used_k.add(j)
        matches.append((i, j, overlap))
    return matches


def score_marks(found: list[dict], key: list[dict]) -> dict[str, Any]:
    found = [m for m in found if m.get("box")]
    matches = match_marks(found, key)
    any_type = match_marks(found, key, same_type=False)
    matched_keys = {j for _, j, _ in matches}
    misses = [f"page {k['page']} {k['type']}: {k['label_en']}" for j, k in enumerate(key) if j not in matched_keys]
    return {"correct": len(matches), "total": len(key), "found": len(found), "misses": misses,
            "right_place_any_type": len(any_type),
            "mean_iou": round(sum(o for _, _, o in matches) / len(matches), 3) if matches else 0.0}


def score_handwriting_dates(found_dates: list[dict], key_dates: list[dict]) -> dict[str, Any]:
    """Dates the key marks as handwriting-only: did the reader say they come from handwriting?"""
    want = [d for d in key_dates if d.get("source") == "handwriting"]
    by_date = defaultdict(set)
    for d in found_dates:
        by_date[d["date"]].add(d["source"])
    correct = sum(1 for d in want if "handwriting" in by_date.get(d["date"], set()))
    return {"correct": correct, "total": len(want)}


def score_phrases(found_raw: list[dict], key_marks: list[dict], min_confidence: float) -> list[dict[str, Any]]:
    """Per SAM phrase: how many of the key's marks of that type its boxes hit (before clean-up)."""
    rows = []
    by_phrase = defaultdict(list)
    for f in found_raw:
        if "box" in f and (f.get("confidence") is None or f["confidence"] >= min_confidence):
            by_phrase[(f["type"], f["found_as"])].append(f)
    phrases = {(f["type"], f["found_as"]) for f in found_raw if "found_as" in f}
    for mark_type, phrase in sorted(phrases):
        boxes = by_phrase.get((mark_type, phrase), [])
        key = [k for k in key_marks if k["type"] == mark_type]
        matches = match_marks(boxes, key)
        rows.append({"type": mark_type, "phrase": phrase, "boxes": len(boxes), "hits": len(matches), "of": len(key)})
    return rows


def unread_case(case_id: str, key: dict[str, Any], marks_key: dict[str, Any], mock: bool) -> dict[str, Any]:
    """A case the run could not read scores zero on everything the key holds."""
    def zero(total: int, **extra: Any) -> dict[str, Any]:
        return {"correct": 0, "total": total, "found": 0, "misses": ["the case could not be read"], **extra}
    return {
        "case": case_id, "mock": mock, "unread": True,
        "parties": zero(len(key["parties"])), "dates": zero(len(key["dates"])),
        "deadlines": zero(len(key["deadlines"])),
        "claims": zero(sum(1 for c in key["claims"] if c["amount_aed"] is not None)),
        "citations": zero(len(key["citations"]), invalid_caught=0,
                          invalid_total=sum(1 for c in key["citations"] if not c["valid"] and not c.get("not_in_index")),
                          quotes_right=0, quotes_total=sum(1 for c in key["citations"] if "quote_ar" in c or "quote_matches_official_text" in c),
                          misquotes_caught=0, misquotes_total=sum(1 for c in key["citations"] if c.get("quote_matches_official_text") is False)),
        "marks": zero(len(marks_key["marks"]), right_place_any_type=0, mean_iou=0.0),
        "handwriting_dates": {"correct": 0, "total": sum(1 for d in key["dates"] if d.get("source") == "handwriting")},
        "phrases": [],
    }


def score_case(case_dir: Path, key_dir: Path, mock: bool = False) -> dict[str, Any] | None:
    case_id = case_dir.name
    loaded = load_answer_key(case_id, key_dir)
    if loaded is None:
        return None
    key, marks_key = loaded
    summary_file = case_dir / "summary.json"
    if not summary_file.exists():
        return unread_case(case_id, key, marks_key, mock)
    s = json.loads(summary_file.read_text(encoding="utf-8"))
    found_raw_file = case_dir / "marks.found.json"
    found_raw = json.loads(found_raw_file.read_text(encoding="utf-8")) if found_raw_file.exists() else []
    return {
        "case": case_id,
        "mock": s.get("mock", False),
        "parties": score_parties(s["parties"], key["parties"]),
        "dates": score_dated(s["dates"], key["dates"], "date", elsewhere=s["deadlines"]),
        "deadlines": score_dated(s["deadlines"], key["deadlines"], "deadline"),
        "claims": score_claims(s["claims"], key["claims"]),
        "citations": score_citations(s["citations"], key["citations"]),
        "marks": score_marks(s["marks"], marks_key["marks"]),
        "handwriting_dates": score_handwriting_dates(s["dates"] + s["deadlines"], key["dates"]),
        "phrases": score_phrases(found_raw, marks_key["marks"], s["run"].get("min_confidence", 0.0)),
    }


CATEGORIES = [("parties", "Parties"), ("dates", "Dates"), ("deadlines", "Deadlines"), ("claims", "Claim amounts"),
              ("citations", "Citations (right verdict)"), ("marks", "Stamps, signatures, handwriting (IoU ≥ 0.5)")]


def to_markdown(cases: list[dict[str, Any]], run_name: str) -> str:
    lines = []
    if any(c["mock"] for c in cases):
        lines.append("> **Mock run.** These numbers test the scoring code only; they are not model results.\n")
    lines.append(f"# Score for {run_name}\n")
    header = "| | " + " | ".join(c["case"] for c in cases) + " | All |"
    lines += [header, "|---" * (len(cases) + 2) + "|"]
    for key, label in CATEGORIES:
        cells = [_ratio(c[key]["correct"], c[key]["total"]) for c in cases]
        total_c = sum(c[key]["correct"] for c in cases)
        total_t = sum(c[key]["total"] for c in cases)
        pct = f" ({100 * total_c / total_t:.0f}%)" if total_t else ""
        lines.append(f"| {label} | " + " | ".join(cells) + f" | {_ratio(total_c, total_t)}{pct} |")
    caught = sum(c["citations"]["invalid_caught"] for c in cases)
    invalid = sum(c["citations"]["invalid_total"] for c in cases)
    lines.append(f"| Invalid citations caught | " + " | ".join(
        _ratio(c["citations"]["invalid_caught"], c["citations"]["invalid_total"]) for c in cases) + f" | {_ratio(caught, invalid)} |")
    mq_c = sum(c["citations"].get("misquotes_caught", 0) for c in cases)
    mq_t = sum(c["citations"].get("misquotes_total", 0) for c in cases)
    if mq_t:
        lines.append(f"| Changed quotes caught | " + " | ".join(
            _ratio(c["citations"].get("misquotes_caught", 0), c["citations"].get("misquotes_total", 0)) for c in cases)
            + f" | {_ratio(mq_c, mq_t)} |")
    hw_c = sum(c["handwriting_dates"]["correct"] for c in cases)
    hw_t = sum(c["handwriting_dates"]["total"] for c in cases)
    lines.append(f"| Handwritten-only dates marked as handwriting | " + " | ".join(
        _ratio(c["handwriting_dates"]["correct"], c["handwriting_dates"]["total"]) for c in cases) + f" | {_ratio(hw_c, hw_t)} |")
    lines.append(f"| Extra marks found (not in the key) | " + " | ".join(
        str(c["marks"]["found"] - c["marks"]["correct"]) for c in cases) + " | |")

    unread = [c["case"] for c in cases if c.get("unread")]
    if unread:
        lines.append(f"\n**Not read:** {', '.join(unread)}; these cases score zero above.")
    lines.append("\n## Misses\n")
    for c in cases:
        misses = [m for key, _ in CATEGORIES for m in c[key]["misses"]]
        lines.append(f"**{c['case']}**: " + ("none" if not misses else ""))
        lines += [f"- {m}" for m in misses]
        lines.append("")

    lines.append("## SAM 3.1 phrasings\n\n| Type | Phrase | Boxes | Hits |\n|---|---|---|---|")
    totals = defaultdict(lambda: [0, 0, 0])
    for c in cases:
        for row in c["phrases"]:
            t = totals[(row["type"], row["phrase"])]
            t[0] += row["boxes"]
            t[1] += row["hits"]
            t[2] += row["of"]
    for (mark_type, phrase), (boxes, hits, of) in sorted(totals.items()):
        lines.append(f"| {mark_type} | {phrase} | {boxes} | {hits}/{of} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", help="run folder, e.g. runs/2026-11-01-a")
    parser.add_argument("--answer-key", default=str(ANSWER_KEY_DIR))
    args = parser.parse_args(argv)
    run = Path(args.run)
    key_dir = Path(args.answer_key)
    run_info = json.loads((run / "run.json").read_text(encoding="utf-8")) if (run / "run.json").exists() else {}
    case_ids = {d.name for d in run.iterdir() if d.is_dir()} | {c["case"] for c in run_info.get("cases", [])}
    cases = [r for case_id in sorted(case_ids)
             if (r := score_case(run / case_id, key_dir, mock=bool(run_info.get("mock"))))]
    if not cases:
        print(f"No scored cases in {run}", file=sys.stderr)
        return 1
    (run / "score.json").write_text(json.dumps(cases, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    markdown = to_markdown(cases, run.name)
    (run / "score.md").write_text(markdown, encoding="utf-8")
    print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())
