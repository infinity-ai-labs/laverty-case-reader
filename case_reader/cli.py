"""Command line: python -m case_reader {read, read-all, check-key}."""

from __future__ import annotations

import argparse
import json
import re
import sys
import traceback
from pathlib import Path

from .marks import DEFAULT_CONCEPTS, SWEEP_CONCEPTS
from .reader import READER_MODEL

REPO = Path(__file__).resolve().parent.parent


def _client_factory(args: argparse.Namespace, case_id: str, usage_log: Path):
    if args.mock:
        from .answer_key import load_answer_key
        from .mock import MockClient

        key = load_answer_key(case_id)
        if key is None:
            raise SystemExit(f"--mock needs an answer key for {case_id}")
        return lambda pages: MockClient(key[0], key[1], pages)

    from .meta_api import MetaClient

    client = MetaClient(usage_log=usage_log)
    return lambda pages: client


def _case_id(path: Path) -> str:
    match = re.match(r"(case-\d+)", path.stem if path.is_file() else path.name)
    return match.group(1) if match else path.stem


def _read_one(args: argparse.Namespace, source: Path, out_dir: Path, case_id: str, usage_log: Path) -> dict:
    from .pipeline import read_file

    return read_file(
        source, out_dir, case_id=case_id,
        make_client=_client_factory(args, case_id, usage_log),
        concepts=SWEEP_CONCEPTS if args.sweep else DEFAULT_CONCEPTS,
        reader_model=args.model, reasoning_effort=args.effort or None,
        min_confidence=args.min_confidence, mock=args.mock,
    )


def cmd_read(args: argparse.Namespace) -> int:
    source = Path(args.file)
    case_id = args.case_id or _case_id(source)
    out = Path(args.out)
    _read_one(args, source, out, case_id, out / "usage.jsonl")
    print(f"Done: {out / 'summary.md'}")
    return 0


def cmd_read_all(args: argparse.Namespace) -> int:
    tests = Path(args.tests)
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    case_dirs = sorted(p for p in tests.iterdir() if p.is_dir())
    wanted = [c.strip() for c in args.cases.split(",") if c.strip()]
    unknown = sorted(set(wanted) - {_case_id(d) for d in case_dirs})
    if unknown:
        print(f"No test file for: {', '.join(unknown)}", file=sys.stderr)
        return 2
    chosen = [d for d in case_dirs if not wanted or _case_id(d) in wanted]
    run = {"mock": args.mock, "model": args.model, "effort": args.effort, "sweep": args.sweep,
           "cases": [{"case": _case_id(d), "status": "not started"} for d in chosen]}
    run_file = out_root / "run.json"

    def save_run() -> None:
        run_file.write_text(json.dumps(run, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    save_run()  # written first, so a run that is stopped part-way still lists every case it was asked to read
    for i, case_dir in enumerate(chosen):
        pdfs = sorted(case_dir.glob("*.pdf"))
        source = pdfs[0] if pdfs else case_dir
        case_id = _case_id(case_dir)
        try:
            _read_one(args, source, out_root / case_id, case_id, out_root / "usage.jsonl")
            run["cases"][i] = {"case": case_id, "status": "done"}
        except Exception as exc:  # keep going with the other cases
            traceback.print_exc()
            run["cases"][i] = {"case": case_id, "status": "failed", "error": f"{type(exc).__name__}: {exc}"[:500]}
        save_run()
    results = run["cases"]
    failed = [r for r in results if r["status"] != "done"]
    print(f"Read {len(results) - len(failed)} of {len(results)} case files into {out_root}")
    return 1 if failed else 0


def cmd_check_key(args: argparse.Namespace) -> int:
    from .meta_api import MetaAPIError, MetaClient, MissingKeyError

    try:
        models = MetaClient().check_access()
    except MissingKeyError as exc:
        print(exc, file=sys.stderr)
        return 2
    except MetaAPIError as exc:
        if exc.status in (401, 403):
            print(f"The key did not work: {exc}", file=sys.stderr)
            return 1
        print(f"Could not list the models ({exc}); carrying on.", file=sys.stderr)
        return 0
    print(f"The key works. {len(models)} models available.")
    for needed in (args.model, "sam-3.1"):
        print(f"  {needed}: {'available' if needed in models else 'NOT in the list'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="case_reader", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--out", required=True, help="folder for the results")
        p.add_argument("--model", default=READER_MODEL, help="Muse Spark model id (default %(default)s)")
        p.add_argument("--effort", default="high", help="reasoning effort: minimal, low, medium, high, xhigh")
        p.add_argument("--min-confidence", type=float, default=0.3, help="drop SAM boxes below this confidence")
        p.add_argument("--sweep", action="store_true", help="try several SAM phrasings per mark type")
        p.add_argument("--mock", action="store_true", help="offline test run from the answer key (no API calls)")

    p_read = sub.add_parser("read", help="read one case file (PDF, image, or folder of page images)")
    p_read.add_argument("file")
    p_read.add_argument("--case-id")
    common(p_read)
    p_read.set_defaults(func=cmd_read)

    p_all = sub.add_parser("read-all", help="read every case file in the test-files folder")
    p_all.add_argument("--tests", default=str(REPO / "test-files"))
    p_all.add_argument("--cases", default="", help="comma-separated case ids, e.g. case-01,case-03")
    common(p_all)
    p_all.set_defaults(func=cmd_read_all)

    p_key = sub.add_parser("check-key", help="check that the Meta Model API key works")
    p_key.add_argument("--model", default=READER_MODEL)
    p_key.set_defaults(func=cmd_check_key)

    args = parser.parse_args(argv)
    return args.func(args)
