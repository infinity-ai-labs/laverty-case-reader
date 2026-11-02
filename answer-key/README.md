# Answer key

One pair of files per test case (13 cases):

- `case-0N.json`: what a careful lawyer would extract from the file, checked by hand. Each item carries the page it comes from.
- `case-0N.marks.json`: where every stamp, signature and handwritten note sits, as `[x0, y0, x1, y1]` fractions of the page width and height. The generator measures each box tight around the mark's ink, by rendering the page again with that one mark hidden and comparing the two images.

## Fields in `case-0N.json`

| Field | Meaning |
|---|---|
| `pages` | What each page is (statement of claim, hearing minutes, notice, statement of account) |
| `court` | Court or centre, case number, where it appears |
| `parties` | Everyone with a role in the case, in Arabic and English |
| `dates` | Every date that matters, as `YYYY-MM-DD`; `source` says when it comes from a stamp or handwriting |
| `deadlines` | What must happen by when, and who must do it; `computed: true` means the date is worked out from the text (for example "15 days from receipt") |
| `claims` | What is claimed, with amounts in AED where the file states one |
| `key_facts` | The facts a lawyer needs first |
| `citations` | Each law and article cited, and whether it exists (`valid`) in the official text |
| `reader_should_flag` | Points the reader must bring to the lawyer's attention |

## How the reader is scored

| Item | Counted as correct when |
|---|---|
| Party | Name matches (Arabic letters normalised) and the role is right |
| Date | Same calendar date, on the right page, in the reader's list of dates (each found date counts once) |
| Deadline | Same calendar date, on the right page, in the reader's list of deadlines |
| Claim | Same amount |
| Citation | Same law and article, and the verdict is right: valid, invalid, or "not checked" for a law outside the index. A quoted article must also get the right wording check (matches, or a changed quote caught) |
| Case not read | A case the run could not read scores zero on every item |
| Stamp, signature or handwriting | Same type, and the boxes overlap by at least half (IoU ≥ 0.5) |

The planted problems must be flagged, never passed quietly: the six citations of articles that don't exist (`"valid": false`), the changed quote in case 07 (`"quote_matches_official_text": false`), and the Dubai decree outside the index in case 06 (`"not_in_index": true`, which the check must report as "not checked").
