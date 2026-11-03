"""Turn a Case Reader run into the demo page's data.

    python tools/build_demo.py runs/<run-name>                 # writes demo/data/
    python tools/build_demo.py runs/<run-name> --standalone demo/standalone.html

The standalone file has the data and the page images inside it, so it opens
without a web server.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parent.parent
SHORT = {
    "labour": ("Labour claim", "دعوى عمالية"),
    "commercial": ("Commercial claim", "دعوى تجارية"),
    "tenancy": ("Tenancy claim", "دعوى إيجارية"),
    "labour-abudhabi": ("Labour claim, Abu Dhabi", "دعوى عمالية، أبوظبي"),
    "cheques": ("Returned cheques", "شيكات مرتجعة"),
    "rent-increase": ("Rent increase", "زيادة الإيجار"),
    "traffic-compensation": ("Traffic accident", "تعويض حادث مروري"),
    "llc-partners": ("Partners' dispute", "نزاع بين الشركاء"),
    "consumer-car": ("Faulty car", "حماية المستهلك"),
    "arbitral-award": ("Arbitral award", "تنفيذ حكم تحكيم"),
    "payment-order": ("Payment order", "أمر أداء"),
    "trademark": ("Trademark", "علامة تجارية"),
    "construction": ("Construction contract", "عقد مقاولة"),
}


def _test_dir(case_id: str) -> Path:
    matches = sorted((REPO / "test-files").glob(f"{case_id}-*"))
    if not matches:
        raise SystemExit(f"No test-files folder for {case_id}")
    return matches[0]


def _data_url(path: Path, width: int = 1000) -> str:
    with Image.open(path) as im:
        img = im.convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=80)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def build(run: Path) -> tuple[list[dict], dict[str, dict]]:
    cases, data = [], {}
    for summary_file in sorted(run.glob("case-*/summary.json")):
        s = json.loads(summary_file.read_text(encoding="utf-8"))
        case_id = s["case"]
        folder = _test_dir(case_id)
        kind = folder.name.split("-", 2)[-1]  # case-04-labour-abudhabi -> labour-abudhabi
        short_en, short_ar = SHORT.get(kind, (case_id, case_id))
        for p in s["pages"]:
            p["src"] = f"../test-files/{folder.name}/page-{p['page']}.jpg"
        cases.append({"case": case_id, "short_en": short_en, "short_ar": short_ar})
        data[case_id] = s
    if not cases:
        raise SystemExit(f"No case summaries in {run}")
    return cases, data


def score_totals(run: Path, data: dict) -> dict | None:
    """Headline numbers for the demo page from the run's score.json (written by tools/score.py), or None."""
    f = run / "score.json"
    if not f.exists():
        return None
    cases = json.loads(f.read_text(encoding="utf-8"))
    if any(c.get("mock") for c in cases):
        return None  # never show mock numbers as results
    total = lambda cat, a, b: [sum(c[cat][a] for c in cases), sum(c[cat][b] for c in cases)]
    return {
        "run": run.name, "files": len(cases), "pages": sum(len(s["pages"]) for s in data.values()),
        "fake": total("citations", "invalid_caught", "invalid_total"),
        "quote": total("citations", "misquotes_caught", "misquotes_total"),
        "verdicts": total("citations", "correct", "total"),
        "dates": total("dates", "correct", "total"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run")
    parser.add_argument("--out", default=str(REPO / "demo" / "data"))
    parser.add_argument("--standalone", help="also write one self-contained HTML file here")
    args = parser.parse_args(argv)

    cases, data = build(Path(args.run))
    score = score_totals(Path(args.run), data)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    index = {"cases": cases, **({"score": score} if score else {})}
    (out / "cases.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for case_id, s in data.items():
        (out / f"{case_id}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {len(cases)} cases to {out}")

    if args.standalone:
        for s in data.values():
            for p in s["pages"]:
                p["src"] = _data_url(REPO / "demo" / p["src"])
        payload = json.dumps({"cases": cases, "data": data, "score": score}, ensure_ascii=False).replace("</", "<\\/")
        html = (REPO / "demo" / "index.html").read_text(encoding="utf-8")
        html = html.replace("<script>\n\"use strict\";", f"<script>window.CASE_DATA = {payload};</script>\n<script>\n\"use strict\";", 1)
        Path(args.standalone).write_text(html, encoding="utf-8")
        print(f"Wrote {args.standalone} ({Path(args.standalone).stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
