"""Draw a run's marks on the test pages, next to the answer key, for a quick visual check.

    python tools/overlay.py runs/<run-name>

Writes runs/<run-name>/overlays/<case>-p<N>.jpg:
  thin lines   every box SAM 3.1 returned (before clean-up), with its confidence;
  thick lines  the marks the reader kept, with their ids;
  grey dashes  the answer key.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parent.parent
COLOURS = {"stamp": (0, 170, 255), "signature": (150, 80, 255), "handwriting": (240, 150, 0)}


def _rect(draw: ImageDraw.ImageDraw, box: list[float], size: tuple[int, int], colour, width: int) -> tuple[int, int]:
    w, h = size
    x0, y0, x1, y1 = box[0] * w, box[1] * h, box[2] * w, box[3] * h
    draw.rectangle([x0, y0, x1, y1], outline=colour, width=width)
    return int(x0), int(y0)


def _dashed(draw: ImageDraw.ImageDraw, box: list[float], size: tuple[int, int]) -> None:
    w, h = size
    x0, y0, x1, y1 = box[0] * w, box[1] * h, box[2] * w, box[3] * h
    step = 10
    for x in range(int(x0), int(x1), step * 2):
        draw.line([x, y0, min(x + step, x1), y0], fill=(120, 120, 120), width=2)
        draw.line([x, y1, min(x + step, x1), y1], fill=(120, 120, 120), width=2)
    for y in range(int(y0), int(y1), step * 2):
        draw.line([x0, y, x0, min(y + step, y1)], fill=(120, 120, 120), width=2)
        draw.line([x1, y, x1, min(y + step, y1)], fill=(120, 120, 120), width=2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run")
    args = parser.parse_args(argv)
    run = Path(args.run)
    out = run / "overlays"
    out.mkdir(exist_ok=True)
    written = 0
    for case_dir in sorted(d for d in run.iterdir() if d.is_dir() and d.name.startswith("case-")):
        folder = next((REPO / "test-files").glob(f"{case_dir.name}-*"), None)
        if folder is None:
            continue
        raw = json.loads((case_dir / "marks.found.json").read_text(encoding="utf-8")) if (case_dir / "marks.found.json").exists() else []
        summary = json.loads((case_dir / "summary.json").read_text(encoding="utf-8")) if (case_dir / "summary.json").exists() else {"marks": [], "rejected_marks": []}
        key_file = REPO / "answer-key" / f"{case_dir.name}.marks.json"
        key = json.loads(key_file.read_text(encoding="utf-8"))["marks"] if key_file.exists() else []
        for page_file in sorted(folder.glob("page-*.jpg")):
            page = int(page_file.stem.split("-")[1])
            img = Image.open(page_file).convert("RGB")
            draw = ImageDraw.Draw(img)
            for k in (k for k in key if k["page"] == page):
                _dashed(draw, k["box"], img.size)
            for f in (f for f in raw if f.get("page") == page and "box" in f):
                x, y = _rect(draw, f["box"], img.size, COLOURS.get(f["type"], (255, 0, 0)), 1)
                if f.get("confidence") is not None:
                    draw.text((x + 3, y + 3), f"{f['confidence']:.2f}", fill=COLOURS.get(f["type"], (255, 0, 0)))
            for m in (m for m in summary["marks"] if m["page"] == page and m.get("box")):
                x, y = _rect(draw, m["box"], img.size, COLOURS.get(m["type"], (255, 0, 0)), 4)
                draw.text((x + 3, y - 14), f"{m['mark_id']} {m['type']}", fill=COLOURS.get(m["type"], (255, 0, 0)))
            for m in (m for m in summary.get("rejected_marks", []) if m["page"] == page and m.get("box")):
                x, y = _rect(draw, m["box"], img.size, (220, 0, 0), 2)
                draw.text((x + 3, y - 14), f"{m['mark_id']} rejected", fill=(220, 0, 0))
            scale = 900 / img.width
            img.resize((900, round(img.height * scale))).save(out / f"{case_dir.name}-p{page}.jpg", quality=85)
            written += 1
    print(f"Wrote {written} overlays to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
