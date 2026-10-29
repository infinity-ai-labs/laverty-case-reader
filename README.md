# LAVERTY Case Reader

Built for the **Meta Global AI Developer Hackathon** (theme: Build for Your World), 26 Oct – 4 Nov 2026.

LAVERTY is the legal brain of the Gulf: Arabic–English legal AI for lawyers, starting with the UAE. Court papers in the UAE often reach lawyers as scanned Arabic documents full of stamps, signatures and handwritten notes, and reading them takes hours before any legal work starts.

The **Case Reader** is a new LAVERTY feature built during this hackathon on Meta's models. It takes a scanned Arabic case file and returns a structured case summary in Arabic and English:

- the parties, dates, claims, deadlines and key facts, each linked to the page it came from;
- the stamps, signatures and handwritten notes, marked for the lawyer so they are never misread as printed text;
- every law the file cites, checked against the official UAE law text.

> Status: the reader is built and tested offline. The first runs with Meta's models come next; their scores will appear here.

## How it works

1. **Pages.** The PDF is rendered page by page.
2. **Marks, with SAM 3.1.** On every page, SAM 3.1 is asked for "rubber stamp", "signature" and "handwritten text", and returns a box for each one it finds. Weak, oversized and duplicate boxes are dropped, and the rest are numbered M1, M2, ... in reading order.
3. **Reading, with Muse Spark 1.3.** Muse Spark reads all the pages together, plus a close-up of every mark, and fills in a fixed JSON schema: court, parties, dates, deadlines, claims, key facts, citations, and what each stamp, signature and handwritten note says. Every item carries its page. An item known only from a stamp or a handwritten note says so and points to the mark, and a handwritten correction of printed text is flagged with both values.
4. **Citation check.** Every cited article is checked against the official law text: is it the right law (federal, or the right emirate's), does the article exist, and does any quoted wording match word for word? The article is read from the citation as written on the page, and a citation naming two articles is checked twice. A citation that cannot be checked is labelled "not checked"; it is never passed quietly. In the LAVERTY app this step is LAVERTY's citation check against its UAE law library. This repository includes a small open version covering the three laws cited in the test files (`laws/`).
5. **Output.** `summary.json` for software and `summary.md` for people, starting with the points a lawyer should check first.

The reader extracts and the check verifies: Muse Spark never decides whether an article exists.

## Run it

```bash
pip install -r requirements.txt
export MODEL_API_KEY="<your Meta Model API key>"

python -m case_reader check-key
python -m case_reader read test-files/case-02-commercial/case-02-commercial.pdf --out runs/my-run/case-02
python -m case_reader read-all --out runs/my-run      # all three test files
python tools/score.py runs/my-run                     # score against the answer key
```

Options: `--effort` sets Muse Spark's reasoning effort (default `high`); `--sweep` tries several SAM 3.1 phrasings for each mark type; `--min-confidence` sets the SAM 3.1 confidence cut-off.

**On GitHub:** Actions → "Run the Case Reader" → Run workflow. It needs the repository secret `META_API_KEY`, and saves each run, with its score, on the `results` branch.

**Without a key:** `python -m case_reader read-all --mock --out runs/mock` runs the whole pipeline offline from the answer key, with a few deliberate mistakes, to test the code and the scorer. Mock output is labelled as such and is not a model result. `python -m pytest` runs the tests.

## What is in this repository

Everything here was made during the hackathon.

| Folder | What it holds |
|---|---|
| `case_reader/` | The Case Reader: SAM 3.1 marks, Muse Spark reading, citation check, summary |
| `laws/` | The law index used by the open citation check |
| `test-files/` | Three made-up scanned Arabic case files (labour, commercial, tenancy), 8 pages in all, with stamps, signatures and handwritten notes |
| `answer-key/` | The hand-checked answers used to score the reader, and the position of every stamp, signature and handwritten note, measured tight around the ink |
| `tools/score.py` | Scores a run against the answer key |
| `tools/make_test_files/` | The generator that made the test files |
| `tools/fonts/` | Open-licence Arabic fonts used by the generator (SIL Open Font License) |
| `tests/` | Offline tests |

## The test files are fictional

Every person, company, case number, ID number, address and event in `test-files/` is invented, and every page says so in its footer. The stamps say "نموذج تدريبي" (training sample).

The laws cited are real UAE laws. Every valid citation was checked against the official text. Two citations are wrong on purpose so the citation check has something to catch:

- Article 145 of Federal Decree-Law No. 33 of 2021 (Labour Relations), a law with 74 articles;
- Article 712 of Federal Decree-Law No. 50 of 2022 (Commercial Transactions), a law with 684 articles.

## Rebuild the test files

```bash
pip install playwright opencv-python pillow numpy
python3 -m playwright install chromium
python3 tools/make_test_files/build.py
```

## Licence

Code: no licence chosen yet [FOUNDER TO CONFIRM]; until one is added, all rights are reserved by Infinity AI Technology Labs, Inc. Fonts: SIL Open Font License, see `tools/fonts/*/OFL.txt`. Law texts: official UAE and Dubai legislation, see `laws/README.md`.
