# -*- coding: utf-8 -*-
"""Render the fictional case files in cases.py as scanned-looking PDFs.

For each page: HTML (Arabic, right to left) -> Chromium screenshot at about 192 dpi ->
"scanner" effects (paper tone, slight tilt, blur, noise, uneven light, JPEG) -> page JPG.
Pages are then joined into one PDF per case. The exact position of every stamp, signature
and handwritten note is written to answer-key/<case>.marks.json, in page fractions (0-1),
so the reader's detections can be scored. Each box is the tight box around the mark's ink,
found by rendering the page again with that one mark hidden and comparing the two images.

Usage: python3 tools/make_test_files/build.py               # pages, PDFs and mark positions
       python3 tools/make_test_files/build.py --marks-only  # mark positions only
"""
import json
import math
import random
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cases import CASES, FOOTER  # noqa: E402

FONTS = ROOT / "tools" / "fonts"
OUT = ROOT / "test-files"
KEY = ROOT / "answer-key"
W, H, SCALE = 794, 1123, 2  # A4 in CSS px; screenshots at 2x

CSS = """
@font-face { font-family: 'Amiri'; src: url('%(fonts)s/amiri/Amiri-Regular.ttf'); font-weight: 400; }
@font-face { font-family: 'Amiri'; src: url('%(fonts)s/amiri/Amiri-Bold.ttf'); font-weight: 700; }
@font-face { font-family: 'Naskh'; src: url('%(fonts)s/notonaskharabic/NotoNaskhArabic-wght.ttf'); }
@font-face { font-family: 'Ruqaa'; src: url('%(fonts)s/arefruqaa/ArefRuqaa-Regular.ttf'); }
@font-face { font-family: 'Kufi'; src: url('%(fonts)s/reemkufi/ReemKufi-wght.ttf'); }
html, body { margin: 0; padding: 0; background: #fff; }
.page { position: relative; width: %(w)dpx; height: %(h)dpx; overflow: hidden; background: #fff;
        direction: rtl; font-family: 'Amiri', serif; font-size: 15.5px; line-height: 1.85; color: #111; }
.inner { padding: 46px 58px 70px 58px; }
.hdr { display: flex; justify-content: space-between; align-items: flex-start;
       border-bottom: 2px solid #222; padding-bottom: 8px; margin-bottom: 14px; }
.ent-name { font-family: 'Kufi', 'Amiri'; font-weight: 700; font-size: 19px; }
.ent-sub { font-size: 13.5px; color: #333; }
.meta { text-align: left; font-size: 14px; }
h1.title { text-align: center; font-family: 'Kufi', 'Amiri'; font-size: 24px; margin: 8px 0 4px; text-decoration: underline; }
h2 { font-size: 17px; margin: 12px 0 4px; font-weight: 700; }
p { margin: 5px 0; text-align: justify; }
.center { text-align: center; }
ol { margin: 4px 0; padding-right: 22px; }
li { margin: 3px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%%; margin: 8px 0; }
table.parties th { width: 110px; text-align: right; vertical-align: top; padding: 4px 6px; background: #f1f1f1; border: 1px solid #999; }
table.parties td { padding: 4px 8px; border: 1px solid #999; }
table.grid th, table.grid td { border: 1px solid #555; padding: 3px 8px; text-align: center; font-size: 14.5px; }
table.grid th { background: #ececec; }
table.grid tr.total td { font-weight: 700; }
table.sigs { margin-top: 40px; }
table.sigs td { width: 50%%; text-align: center; font-weight: 700; padding-bottom: 70px; }
.sigline { margin-top: 26px; text-align: left; font-weight: 700; padding-left: 40px; }
.cont { text-align: left; color: #444; font-size: 13.5px; }
.struck { text-decoration: line-through; text-decoration-color: #a12a2a; text-decoration-thickness: 2px; }
.footer { position: absolute; bottom: 22px; left: 58px; right: 58px; border-top: 1px solid #bbb; padding-top: 4px;
          font-family: 'Naskh', 'Amiri'; font-size: 11px; color: #666; display: flex; justify-content: space-between; }
.mark { position: absolute; }
.stamp { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;
         font-family: 'Amiri'; font-weight: 700; line-height: 1.25; box-sizing: border-box; filter: url(#ink); opacity: .86; }
.stamp.rect { border: 3px double currentColor; outline: 1.5px solid currentColor; outline-offset: 3px; padding: 4px 8px; }
.stamp.oval { border: 2.5px solid currentColor; border-radius: 50%%; padding: 6px; }
.stamp .l1 { font-size: 15px; } .stamp .l2 { font-size: 12.5px; } .stamp .l3 { font-size: 13px; }
.hand { font-family: 'Ruqaa'; white-space: nowrap; filter: url(#wobble); line-height: 1.3; }
.hand.wrap { white-space: normal; }
"""

FILTERS = """
<svg width="0" height="0" style="position:absolute">
  <filter id="ink" x="-10%%" y="-10%%" width="120%%" height="120%%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="%(s1)d" result="grain"/>
    <feDisplacementMap in="SourceGraphic" in2="grain" scale="2.2" xChannelSelector="R" yChannelSelector="G" result="rough"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" seed="%(s2)d" result="blot"/>
    <feColorMatrix in="blot" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.4 0 0 0 2.05" result="mask"/>
    <feComposite in="rough" in2="mask" operator="in"/>
  </filter>
  <filter id="wobble">
    <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="1" seed="%(s3)d" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</svg>
"""


def signature_svg(m):
    """A random cursive-looking signature as an SVG path."""
    rnd = random.Random(m["seed"])
    w, h = m["width"], m["height"]
    x, y = w * 0.08, h * rnd.uniform(0.45, 0.65)
    d = [f"M {x:.1f} {y:.1f}"]
    n = rnd.randint(5, 8)
    for i in range(n):
        nx = w * (0.1 + 0.8 * (i + 1) / n) + rnd.uniform(-8, 8)
        ny = h * rnd.uniform(0.2, 0.85)
        c1 = (x + rnd.uniform(-25, 30), y + rnd.uniform(-h * 0.6, h * 0.6))
        c2 = (nx + rnd.uniform(-30, 25), ny + rnd.uniform(-h * 0.6, h * 0.6))
        d.append(f"C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {nx:.1f} {ny:.1f}")
        x, y = nx, ny
    # a flourish underline
    ux0, uy = w * rnd.uniform(0.05, 0.2), h * rnd.uniform(0.75, 0.9)
    d.append(f"M {ux0:.1f} {uy:.1f} Q {w * 0.5:.1f} {uy + rnd.uniform(-10, 10):.1f}, {w * rnd.uniform(0.8, 0.95):.1f} {uy - rnd.uniform(4, 14):.1f}")
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<path d="{" ".join(d)}" fill="none" stroke="{m["color"]}" stroke-width="2.1" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def mark_html(m):
    style = f'top:{m["top"]}px; left:{m["left"]}px; transform: rotate({m.get("rotate", 0)}deg); color:{m["color"]};'
    if m["type"] == "stamp":
        lines = "".join(f'<div class="l{i + 1}">{t}</div>' for i, t in enumerate(m["lines"]))
        style += f' width:{m["width"]}px; height:{m["height"]}px;'
        return f'<div class="mark stamp {m["kind"]}" data-mark="{m["id"]}" style="{style}">{lines}</div>'
    if m["type"] == "signature":
        style += f' width:{m["width"]}px; height:{m["height"]}px;'
        return f'<div class="mark" data-mark="{m["id"]}" style="{style}">{signature_svg(m)}</div>'
    if m["type"] == "handwriting":
        style += f' font-size:{m["size"]}px;'
        cls = "mark hand"
        if m.get("width"):
            style += f' width:{m["width"]}px;'
            cls += " wrap"
        return f'<div class="{cls}" data-mark="{m["id"]}" style="{style}">{m["text"]}</div>'
    raise ValueError(m["type"])


def page_html(case, pno, page):
    css = CSS % {"fonts": FONTS.as_uri(), "w": W, "h": H}
    filt = FILTERS % {"s1": 3 + pno, "s2": 11 + 7 * pno, "s3": 5 + pno}
    marks = "\n".join(mark_html(m) for m in page["marks"])
    n = len(case["pages"])
    footer = f'<div class="footer"><span>{FOOTER}</span><span>صفحة {pno} من {n}</span></div>'
    return (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>{css}</style></head>'
            f'<body>{filt}<div class="page"><div class="inner">{page["html"]}</div>{marks}{footer}</div></body></html>')


def scan_effect(img, rnd):
    """Make a clean render look like a mid-quality office scan. Returns (image, 2x3 affine)."""
    h, w = img.shape[:2]
    f = img.astype(np.float32)
    f *= np.array([0.965, 0.975, 0.985], dtype=np.float32)  # warm paper (BGR)
    angle = rnd.uniform(-0.7, 0.7)
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    M[:, 2] += [rnd.uniform(-6, 6), rnd.uniform(-6, 6)]
    f = cv2.warpAffine(f, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(238, 241, 244))
    f = cv2.GaussianBlur(f, (0, 0), 0.75)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    light = 1.0 - 0.06 * (xx / w) - 0.04 * ((yy - h / 2) / h) ** 2 * 4
    f *= light[..., None]
    f += np.random.default_rng(rnd.randint(0, 10_000)).normal(0, 5.5, f.shape).astype(np.float32)
    for _ in range(rnd.randint(20, 45)):  # dust specks
        cv2.circle(f, (rnd.randint(0, w - 1), rnd.randint(0, h - 1)), rnd.choice([1, 1, 2]), (60, 60, 60), -1)
    return np.clip(f, 0, 255).astype(np.uint8), M


def ink_boxes(page_obj, clean):
    """Tight pixel box around each mark's ink: hide one mark, render again, compare."""
    ids = page_obj.evaluate("() => [...document.querySelectorAll('[data-mark]')].map(e => e.dataset.mark)")
    out = {}
    for mid in ids:
        page_obj.evaluate("id => { document.querySelector(`[data-mark='${id}']`).style.visibility = 'hidden'; }", mid)
        png = page_obj.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
        page_obj.evaluate("id => { document.querySelector(`[data-mark='${id}']`).style.visibility = ''; }", mid)
        hidden = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
        changed = np.abs(clean.astype(np.int16) - hidden.astype(np.int16)).max(axis=2) > 40
        ys, xs = np.nonzero(changed)
        if len(xs):
            out[mid] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    return out


def transform_box(box, M):
    x0, y0, x1, y1 = box
    pts = np.array([[x0, y0, 1], [x1, y0, 1], [x0, y1, 1], [x1, y1, 1]], dtype=np.float32)
    t = pts @ M.T
    return [float(t[:, 0].min()), float(t[:, 1].min()), float(t[:, 0].max()), float(t[:, 1].max())]


def main():
    marks_only = "--marks-only" in sys.argv[1:]
    OUT.mkdir(exist_ok=True)
    KEY.mkdir(exist_ok=True)
    tmp = ROOT / "tmp"
    tmp.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=SCALE)
        page_obj = ctx.new_page()
        for ci, case in enumerate(CASES):
            rnd = random.Random(1000 + ci)
            folder = OUT / f'{case["id"]}-{case["slug"]}'
            folder.mkdir(exist_ok=True)
            images, marks_out = [], []
            for pno, page in enumerate(case["pages"], start=1):
                html_path = tmp / f'{case["id"]}-p{pno}.html'
                html_path.write_text(page_html(case, pno, page), encoding="utf-8")
                page_obj.goto(html_path.as_uri())
                page_obj.evaluate("document.fonts.ready")
                page_obj.wait_for_timeout(250)
                boxes = page_obj.evaluate(
                    "() => [...document.querySelectorAll('[data-mark]')].map(e => {"
                    "const r = e.getBoundingClientRect(); return [e.dataset.mark, r.left, r.top, r.right, r.bottom]; })")
                png = page_obj.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
                clean = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
                ink = ink_boxes(page_obj, clean)
                scanned, M = scan_effect(clean, rnd)
                ok, jpg = cv2.imencode(".jpg", scanned, [cv2.IMWRITE_JPEG_QUALITY, 74])
                jpg_path = folder / f"page-{pno}.jpg"
                if marks_only:
                    same = jpg_path.exists() and jpg_path.read_bytes() == jpg.tobytes()
                    print(f'  {jpg_path.relative_to(ROOT)}: {"same image as before" if same else "DIFFERENT from the saved page"}')
                else:
                    jpg_path.write_bytes(jpg.tobytes())
                    images.append(Image.open(jpg_path).convert("RGB"))
                ih, iw = scanned.shape[:2]
                spec = {m["id"]: m for m in page["marks"]}
                for mid, l, t, r, b in boxes:
                    px = ink.get(mid) or [l * SCALE, t * SCALE, r * SCALE, b * SCALE]
                    x0, y0, x1, y1 = transform_box(px, M)
                    m = spec[mid]
                    marks_out.append({
                        "id": mid, "page": pno, "type": m["type"],
                        "box": [round(max(0, x0) / iw, 4), round(max(0, y0) / ih, 4),
                                round(min(iw, x1) / iw, 4), round(min(ih, y1) / ih, 4)],
                        "label_en": m["label_en"], "text_ar": m.get("text_ar"),
                    })
            pdf_path = folder / f'{case["id"]}-{case["slug"]}.pdf'
            if not marks_only:
                images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=SCALE * 96)
            (KEY / f'{case["id"]}.marks.json').write_text(
                json.dumps({"case": case["id"],
                            "box_format": "[x0, y0, x1, y1] as fractions of page width/height, tight around the ink",
                            "marks": marks_out}, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f'{case["id"]}: {len(case["pages"])} pages, {len(marks_out)} marks -> {pdf_path.relative_to(ROOT)}')
        browser.close()


if __name__ == "__main__":
    main()
