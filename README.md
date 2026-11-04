# LAVERTY Case Reader

Built for the **Meta Global AI Developer Hackathon** (theme: Build for Your World), 26 Oct – 4 Nov 2026.

LAVERTY is the legal brain of the Gulf: Arabic–English legal AI for lawyers, starting with the UAE. Court papers in the UAE often reach lawyers as scanned Arabic documents full of stamps, signatures and handwritten notes, and reading them takes hours before any legal work starts.

The **Case Reader** is a new LAVERTY feature built during this hackathon on Meta's models. It takes a scanned Arabic case file and returns a structured case summary in Arabic and English:

- the parties, dates, claims, deadlines and key facts, each linked to the page it came from;
- the stamps, signatures and handwritten notes, marked for the lawyer so they are never misread as printed text;
- every law the file cites, checked against the official UAE law text.

## Results on Meta's models

Run 6 (4 Nov 2026): all 13 test files, 33 pages, read with `muse-spark-1.3` (reasoning effort high) and `sam-3.1`, scored by `tools/score.py` against the hand-checked answer key. The full run, with every miss listed, is on the [`results` branch](https://github.com/infinity-ai-labs/laverty-case-reader/tree/results/runs/run-6-1).

| What was checked | Result |
|---|---|
| Citations of articles that don't exist, caught | **6 of 6** |
| Quote with one changed word, caught | **1 of 1** |
| Citation verdicts right (valid, invalid or not checked) | **80 of 80** |
| Claim amounts | **35 of 35** |
| Parties, with the right role | 65 of 67 |
| Dates | 125 of 131 |
| Deadlines | 19 of 24 |
| Stamps, signatures and handwritten notes in the right place (box overlap ≥ 0.5) | 98 of 109 |
| Dates that exist only in handwriting, marked as handwriting | 8 of 10 |

What the runs taught us:
- **SAM 3.1 phrasings.** "stamp", "blue stamp" and "purple stamp" found 12 of 13 stamps on the first four files, and "signature" found 10 of 11, with no false boxes. "rubber stamp", "official seal" and every phrasing tried for handwriting ("handwritten text", "handwriting", "writing", "note", ...) returned nothing.
- **Handwriting is placed by Muse Spark, with a close-up second look.** Muse Spark reads the handwritten notes SAM 3.1 does not find and gives their position on the page. That first position is rough, so each note gets a close-up: the area around it is cut out and Muse Spark places the note again inside it. In run 6 this raised the handwritten notes placed right (overlap ≥ 0.5) from 5 to 12 of 22, and all marks from 91 (run 5) to 98 of 109.
- **Quotes are checked wherever they sit.** Muse Spark sometimes leaves a quoted article inside the citation text; the check now finds it there. One false alarm remains where Muse Spark misread a long quote (case 10): the summary says the wording differs and asks the lawyer to check the page, so nothing passes quietly.

## How it works

1. **Pages.** The PDF is rendered page by page.
2. **Marks, with SAM 3.1.** On every page, SAM 3.1 is asked for "rubber stamp", "signature" and "handwritten text", and returns a box for each one it finds. Weak, oversized and duplicate boxes are dropped, and the rest are numbered M1, M2, ... in reading order.
3. **Reading, with Muse Spark 1.3.** Muse Spark reads all the pages together, plus a close-up of every mark, and fills in a fixed JSON schema: court, parties, dates, deadlines, claims, key facts, citations, and what each stamp, signature and handwritten note says. Every item carries its page. An item known only from a stamp or a handwritten note says so and points to the mark, and a handwritten correction of printed text is flagged with both values.
4. **Citation check.** Every cited article is checked against the official law text: is it the right law (federal, or the right emirate's), does the article exist, and does any quoted wording match word for word? The article is read from the citation as written on the page, and a citation naming two articles is checked twice. A citation that cannot be checked is labelled "not checked"; it is never passed quietly. In the LAVERTY app this step is LAVERTY's citation check against its UAE law library. This repository includes a small open version covering the 11 laws cited in the test files (`laws/`).
5. **Output.** `summary.json` for software and `summary.md` for people, starting with the points a lawyer should check first.

The reader extracts and the check verifies: Muse Spark never decides whether an article exists.

## Run it

```bash
pip install -r requirements.txt
export MODEL_API_KEY="<your Meta Model API key>"

python -m case_reader check-key
python -m case_reader read test-files/case-02-commercial/case-02-commercial.pdf --out runs/my-run/case-02
python -m case_reader read-all --out runs/my-run      # all 13 test files
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
| `test-files/` | 13 made-up scanned Arabic case files, 33 pages in all, each one PDF with stamps, signatures and handwritten notes |
| `answer-key/` | The hand-checked answers used to score the reader, and the position of every stamp, signature and handwritten note, measured tight around the ink |
| `tools/score.py` | Scores a run against the answer key |
| `tools/overlay.py` | Draws a run's marks on the pages beside the answer key |
| `tools/make_test_files/` | The generator that made the test files (`cases.py` for cases 01–03, `extra/` for 04–13) |
| `tools/fonts/` | Open-licence Arabic fonts used by the generator (SIL Open Font License) |
| `tests/` | Offline tests |

## The test files are fictional

Every person, company, case number, ID number, address and event in `test-files/` is invented, and every page says so in its footer. The stamps say "نموذج تدريبي" (training sample).

| Case | What it is | Pages |
|---|---|---|
| 01 | Labour claim: unpaid wages, gratuity, unlawful dismissal (Dubai) | 3 |
| 02 | Commercial claim: unpaid supply invoices and a returned cheque | 3 |
| 03 | Tenancy claim: eviction for unpaid rent (Dubai) | 2 |
| 04 | Labour claim before the Abu Dhabi labour court, with the Ministry's referral memo | 2 |
| 05 | Three returned cheques, with the judge's handwritten attachment decision | 3 |
| 06 | Dubai tenancy: a rent increase at renewal, with the landlord's notice | 2 |
| 07 | Traffic accident compensation under the 2025 Civil Transactions Law | 3 |
| 08 | Partners' dispute in an LLC: removing the manager | 3 |
| 09 | Consumer claim: a new car with a repeated gearbox defect | 2 |
| 10 | Application to ratify and enforce an arbitral award | 3 |
| 11 | Payment order, with a signed acknowledgment of debt | 2 |
| 12 | Trademark counterfeiting | 2 |
| 13 | Construction contract under the 1985 Civil Transactions Law | 3 |

The laws cited are real UAE laws, and every valid citation was checked against the official text. The files plant problems on purpose, so the reader and the citation check have something to catch:

- **Articles that don't exist:** Labour Relations Law Art. 145 (case 01; the law has 74 articles), Commercial Transactions Law Art. 712 (case 02; 684), Civil Procedure Law Art. 350 (case 05; 338), Commercial Companies Law Art. 380, cited clause first (case 08; 366), Consumer Protection Law Art. 45 (case 09; 38) and Trademarks Law Art. 47 bis (case 12; there is none).
- **A quote with one word changed:** case 07 quotes Civil Transactions Law (2025) Art. 255 with "محتملة" (probable) where the official text says "طبيعية" (natural).
- **A law outside the index:** Dubai Decree No. 43 of 2013 (case 06) must come back "not checked", never "valid".
- **A repealed law that still governs:** case 13's contract predates 1 June 2026, so the 1985 Civil Transactions Law applies even though it has been repealed.
- **Handwriting that changes or adds facts:** amounts corrected by hand (cases 02, 11, 13), and dates, case numbers or file numbers that appear only in handwriting (most cases).
- **Citation forms:** article ranges (cases 05 and 13), clause-first citations (cases 01, 04, 08), "المادة رقم" (case 04), two laws in one sentence (case 10), and deadlines that must be worked out from the text.

## Rebuild the test files

```bash
pip install playwright opencv-python pillow numpy
python3 -m playwright install chromium
python3 tools/make_test_files/build.py
```

## Licence

Apache License 2.0: see `LICENSE` and `NOTICE`. Copyright 2026 Infinity AI Technology Labs, Inc. The licence covers this repository only (the Case Reader built during the hackathon); LAVERTY's app code and law library are not part of it. Fonts: SIL Open Font License, see `tools/fonts/*/OFL.txt`. Law texts: official UAE and Dubai legislation, see `laws/README.md`.
