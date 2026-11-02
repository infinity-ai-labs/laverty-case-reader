# Score for run-2-1

| | case-01 | case-05 | case-07 | case-11 | All |
|---|---|---|---|---|---|
| Parties | 6/6 | 6/6 | 5/6 | 4/4 | 21/22 (95%) |
| Dates | 9/9 | 13/13 | 13/14 | 8/8 | 43/44 (98%) |
| Deadlines | 2/2 | 1/1 | 0/0 | 2/2 | 5/5 (100%) |
| Claim amounts | 5/6 | 1/1 | 5/5 | 1/1 | 12/13 (92%) |
| Citations (right verdict) | 7/7 | 8/8 | 5/5 | 2/2 | 22/22 (100%) |
| Stamps, signatures, handwriting (IoU ≥ 0.5) | 5/8 | 3/7 | 6/8 | 5/6 | 19/29 (66%) |
| Invalid citations caught | 1/1 | 1/1 | 0/0 | 0/0 | 2/2 |
| Changed quotes caught | 0/0 | 0/0 | 0/1 | 0/0 | 0/1 |
| Handwritten-only dates marked as handwriting | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 |
| Extra marks found (not in the key) | 0 | 0 | 0 | 0 | |

## Misses

**case-01**: 
- AED 196,460 (Total): not found
- page 1 handwriting: Registry clerk's handwritten case number
- page 3 stamp: Hearings desk stamp (training sample)
- page 3 handwriting: Lawyer's handwritten follow-up note

**case-05**: 
- page 1 stamp: Court registry date stamp (training sample)
- page 3 handwriting: Judge's handwritten decision: attachment ordered; main claim to be filed within 8 days
- page 3 signature: Summary judge's signature
- page 3 stamp: Court stamp (training sample)

**case-07**: 
- Dr Nader Salim Al Khoury (other): found, but role given as expert
- date 2026-06-29 (page 1, Claimant discharged from hospital): found on page [3]
- misquote of article 255 (page 1): quote check said None
- page 2 stamp: Traffic accidents section stamp (training sample)
- page 3 handwriting: Doctor's handwritten permanent disability percentage

**case-11**: 
- page 2 handwriting: Handwritten correction of the debt amount to 293,450, with initials

## SAM 3.1 phrasings

| Type | Phrase | Boxes | Hits |
|---|---|---|---|
| signature | handwritten signature | 8 | 8/11 |
| signature | signature | 10 | 10/11 |
| stamp | stamp | 9 | 9/13 |
