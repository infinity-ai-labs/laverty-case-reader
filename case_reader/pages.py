"""Page images: render a PDF, load scans, make data URLs and close-up crops."""

from __future__ import annotations

import base64
import io
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


@dataclass
class Page:
    number: int  # from 1
    path: Path
    width: int
    height: int


def _page_number(path: Path) -> int:
    match = re.search(r"(\d+)", path.stem)
    return int(match.group(1)) if match else 0


def render_pdf(pdf_path: Path, out_dir: Path, target_width: int = 1600) -> list[Path]:
    """Render every PDF page to a JPEG about `target_width` pixels wide."""
    import pypdfium2 as pdfium

    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(str(pdf_path))
    paths: list[Path] = []
    try:
        for index in range(len(pdf)):
            page = pdf[index]
            width_pt, _ = page.get_size()
            bitmap = page.render(scale=target_width / width_pt)
            image = bitmap.to_pil().convert("RGB")
            path = out_dir / f"page-{index + 1}.jpg"
            image.save(path, quality=92)
            paths.append(path)
    finally:
        pdf.close()
    return paths


def load_pages(source: Path, out_dir: Path) -> list[Page]:
    """Load a case file (a PDF, a folder of page images, or one image) into out_dir/pages."""
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        found = sorted((p for p in source.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES), key=_page_number)
        paths = []
        for i, src in enumerate(found, 1):
            dst = pages_dir / f"page-{i}{src.suffix.lower()}"
            shutil.copyfile(src, dst)
            paths.append(dst)
    elif source.suffix.lower() == ".pdf":
        paths = render_pdf(source, pages_dir)
    elif source.suffix.lower() in IMAGE_SUFFIXES:
        dst = pages_dir / f"page-1{source.suffix.lower()}"
        shutil.copyfile(source, dst)
        paths = [dst]
    else:
        raise ValueError(f"Not a PDF, image or folder of images: {source}")
    if not paths:
        raise ValueError(f"No pages found in {source}")
    pages = []
    for i, path in enumerate(paths, 1):
        with Image.open(path) as im:
            pages.append(Page(number=i, path=path, width=im.width, height=im.height))
    return pages


def image_data_url(image: Image.Image | Path, *, max_side: int | None = None, quality: int = 90) -> str:
    """A base64 JPEG data URL, optionally scaled down so the longer side is at most max_side."""
    if isinstance(image, Path):
        with Image.open(image) as im:
            img = im.convert("RGB")
    else:
        img = image.convert("RGB")
    if max_side and max(img.size) > max_side:
        scale = max_side / max(img.size)
        img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def crop_box(image_path: Path, box: list[float], *, pad: float = 0.35, min_side_px: int = 200) -> Image.Image:
    """Crop a box ([x0, y0, x1, y1] as page fractions) with some margin around it."""
    with Image.open(image_path) as im:
        img = im.convert("RGB")
    w, h = img.size
    x0, y0, x1, y1 = box[0] * w, box[1] * h, box[2] * w, box[3] * h
    bw, bh = max(1.0, x1 - x0), max(1.0, y1 - y0)
    px = max(bw * pad, (min_side_px - bw) / 2, 12)
    py = max(bh * pad, (min_side_px - bh) / 2, 12)
    left, top = max(0, int(x0 - px)), max(0, int(y0 - py))
    right, bottom = min(w, int(x1 + px)), min(h, int(y1 + py))
    return img.crop((left, top, right, bottom))
