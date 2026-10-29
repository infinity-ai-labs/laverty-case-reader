"""The live Case Reader on Modal: the demo page, plus "read your own file".

Deploy (from the repository root):

    modal deploy deploy/modal_app.py

It needs a Modal secret named `meta-model-api` that holds MODEL_API_KEY.
Uploads are read with Muse Spark and SAM 3.1 and then thrown away; nothing is
kept. Daily limits keep the cost of the public demo bounded.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import modal

ROOT = Path(__file__).resolve().parent.parent
APP_DIR = "/root/app"
MAX_BYTES = 10 * 1024 * 1024
MAX_PAGES = 6
DAILY_LIMIT = int(os.environ.get("CASE_READER_DAILY_LIMIT", "60"))
PER_VISITOR_DAILY_LIMIT = int(os.environ.get("CASE_READER_PER_VISITOR_LIMIT", "5"))

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install_from_requirements(str(ROOT / "requirements.txt"))
    .pip_install("fastapi[standard]>=0.115", "python-multipart>=0.0.9")
    .env({"PYTHONPATH": APP_DIR})
    .add_local_dir(ROOT / "case_reader", f"{APP_DIR}/case_reader")
    .add_local_dir(ROOT / "laws", f"{APP_DIR}/laws")
    .add_local_dir(ROOT / "demo", f"{APP_DIR}/demo")
    .add_local_dir(ROOT / "test-files", f"{APP_DIR}/test-files")
)

app = modal.App("laverty-case-reader", image=image)
meta_secret = modal.Secret.from_name("meta-model-api")
usage = modal.Dict.from_name("laverty-case-reader-usage", create_if_missing=True)
progress = modal.Dict.from_name("laverty-case-reader-progress", create_if_missing=True)


@app.function(secrets=[meta_secret], timeout=900, max_containers=3)
def read_upload(kind: str, data: bytes) -> dict:
    """Read one uploaded file end to end and return its case summary (page images inline)."""
    import tempfile

    from case_reader.meta_api import MetaClient
    from case_reader.pages import image_data_url
    from case_reader.pipeline import read_file

    job = modal.current_function_call_id()

    def log(message: str) -> None:
        try:
            progress[job] = message
        except Exception:
            pass

    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / f"your-file.{kind}"
        source.write_bytes(data)
        out = Path(tmp) / "out"
        client = MetaClient()
        summary = read_file(source, out, case_id="your-file", make_client=lambda pages: client, log=log)
        for page in summary["pages"]:
            page["src"] = image_data_url(out / page["image"], max_side=1400, quality=82)
        return summary


def _kind(data: bytes) -> str | None:
    if data.startswith(b"%PDF"):
        return "pdf"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    return None


def _take(key: str, limit: int) -> bool:
    used = usage.get(key, 0)
    if used >= limit:
        return False
    usage[key] = used + 1
    return True


@app.function(max_containers=2)
@modal.concurrent(max_inputs=40)
@modal.asgi_app()
def web():
    from fastapi import FastAPI, File, HTTPException, Request, UploadFile
    from fastapi.responses import RedirectResponse, Response
    from fastapi.staticfiles import StaticFiles

    api = FastAPI(title="LAVERTY Case Reader", docs_url=None, redoc_url=None, openapi_url=None)

    @api.get("/")
    def home():
        return RedirectResponse("/demo/")

    @api.get("/demo/config.js")
    def config():
        return Response("window.CASE_READER_API = '/api';\n", media_type="application/javascript")

    @api.post("/api/read")
    async def start(request: Request, file: UploadFile = File(...)):
        data = await file.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise HTTPException(413, "The file is larger than 10 MB.")
        kind = _kind(data)
        if kind is None:
            raise HTTPException(415, "Upload a PDF, JPG or PNG file.")
        if kind == "pdf":
            import pypdfium2 as pdfium

            try:
                pdf = pdfium.PdfDocument(data)
                pages = len(pdf)
                pdf.close()
            except Exception:
                raise HTTPException(422, "This PDF could not be opened.") from None
            if pages > MAX_PAGES:
                raise HTTPException(422, f"The file has {pages} pages; the live demo reads up to {MAX_PAGES}.")
        day = datetime.now(timezone.utc).date().isoformat()
        # The right-most X-Forwarded-For entry is the one Modal's proxy added; earlier ones come from the client.
        forwarded = request.headers.get("x-forwarded-for", "")
        visitor = forwarded.split(",")[-1].strip() if forwarded else (request.client.host if request.client else "?")
        if not _take(f"visitor:{visitor}:{day}", PER_VISITOR_DAILY_LIMIT):
            raise HTTPException(429, f"You have read {PER_VISITOR_DAILY_LIMIT} files today. Try again tomorrow.")
        if not _take(f"day:{day}", DAILY_LIMIT):
            raise HTTPException(429, "Today's live reads are used up. Try again tomorrow, or open the three test files.")
        call = read_upload.spawn(kind, data)
        return {"job": call.object_id}

    @api.get("/api/jobs/{job}")
    def job_status(job: str):
        if not re.fullmatch(r"fc-[A-Za-z0-9]+", job):
            raise HTTPException(404, "No such job.")
        call = modal.FunctionCall.from_id(job)
        try:
            summary = call.get(timeout=0)
        except (TimeoutError, modal.exception.TimeoutError):
            return {"status": "running", "step": progress.get(job, "")}
        except Exception:
            return {"status": "failed", "error": "The file could not be read. Try another file."}
        return {"status": "done", "summary": summary}

    api.mount("/test-files", StaticFiles(directory=f"{APP_DIR}/test-files"), name="test-files")
    api.mount("/demo", StaticFiles(directory=f"{APP_DIR}/demo", html=True), name="demo")
    return api
