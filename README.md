# LAVERTY Case Reader

Built for the **Meta Global AI Developer Hackathon** (theme: Build for Your World), 26 Oct – 4 Nov 2026.

LAVERTY is the legal brain of the Gulf: Arabic–English legal AI for lawyers, starting with the UAE. Court papers in the UAE often reach lawyers as scanned Arabic documents full of stamps, signatures and handwritten notes, and reading them takes hours before any legal work starts.

The **Case Reader** is a new LAVERTY feature built during this hackathon on Meta's models. It takes a scanned Arabic case file and returns a structured case summary in Arabic and English:

- the parties, dates, claims, deadlines and key facts, each linked to the page it came from;
- the stamps, signatures and handwritten notes, marked for the lawyer so they are never misread as printed text;
- every law the file cites, sent to LAVERTY's citation check against official UAE law.

> Status: the test set and answer key are ready; the reader itself is being built now.

## What is in this repository

Everything here was made during the hackathon.

| Folder | What it holds |
|---|---|
| `test-files/` | Three made-up scanned Arabic case files (labour, commercial, tenancy), 8 pages in all, with stamps, signatures and handwritten notes |
| `answer-key/` | The hand-checked answers used to score the reader, and the exact position of every stamp, signature and handwritten note |
| `tools/make_test_files/` | The generator that made the test files |
| `tools/fonts/` | Open-licence Arabic fonts used by the generator (SIL Open Font License) |

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

Code: no licence chosen yet [FOUNDER TO CONFIRM]; until one is added, all rights are reserved by Infinity AI Technology Labs, Inc. Fonts: SIL Open Font License, see `tools/fonts/*/OFL.txt`.
