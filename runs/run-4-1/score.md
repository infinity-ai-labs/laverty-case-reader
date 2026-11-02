# Score for run-4-1

| | case-01 | case-02 | case-03 | case-04 | case-05 | case-06 | case-07 | case-08 | case-09 | case-10 | case-11 | case-12 | case-13 | All |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Parties | 6/6 | 2/5 | 2/2 | 5/5 | 5/6 | 3/3 | 5/6 | 7/8 | 3/4 | 7/7 | 4/4 | 2/4 | 3/7 | 54/67 (81%) |
| Dates | 9/9 | 13/13 | 9/9 | 9/9 | 13/13 | 6/6 | 13/14 | 10/10 | 8/8 | 8/8 | 8/8 | 10/10 | 11/14 | 127/131 (97%) |
| Deadlines | 2/2 | 2/2 | 2/2 | 1/2 | 1/1 | 2/3 | 0/0 | 1/2 | 1/1 | 1/1 | 2/2 | 1/2 | 2/4 | 18/24 (75%) |
| Claim amounts | 6/6 | 1/1 | 1/1 | 5/5 | 1/1 | 2/2 | 5/5 | 1/1 | 4/4 | 4/4 | 1/1 | 1/1 | 3/3 | 35/35 (100%) |
| Citations (right verdict) | 7/7 | 4/4 | 4/4 | 7/7 | 8/8 | 7/7 | 5/5 | 9/9 | 6/6 | 8/8 | 2/2 | 7/7 | 5/6 | 79/80 (99%) |
| Stamps, signatures, handwriting (IoU ≥ 0.5) | 5/8 | 7/11 | 6/8 | 5/5 | 6/7 | 6/7 | 7/8 | 10/11 | 6/7 | 9/10 | 5/6 | 7/8 | 9/13 | 88/109 (81%) |
| Invalid citations caught | 1/1 | 1/1 | 0/0 | 0/0 | 1/1 | 0/0 | 0/0 | 1/1 | 1/1 | 0/0 | 0/0 | 1/1 | 0/0 | 6/6 |
| Changed quotes caught | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 1/1 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 0/0 | 1/1 |
| Handwritten-only dates marked as handwriting | 0/0 | 2/2 | 1/1 | 1/1 | 0/0 | 1/1 | 0/0 | 0/0 | 1/1 | 1/1 | 0/0 | 1/1 | 2/2 | 10/10 |
| Extra marks found (not in the key) | 3 | 4 | 2 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 4 | |

## Misses

**case-01**: 
- page 1 handwriting: Registry clerk's handwritten case number
- page 3 stamp: Hearings desk stamp (training sample)
- page 3 handwriting: Lawyer's handwritten follow-up note

**case-02**: 
- Tariq Maher Al Suwaidi (claimant_representative): not found
- Al Saqr Al Thahabi Contracting Establishment (defendant): not found
- Rashid Hamad Al Falasi (defendant_representative): not found
- page 1 handwriting: Handwritten note: notice served on the debtor
- page 2 signature: Signature of the claimant's lawyer
- page 2 handwriting: Registry clerk's handwritten hearing date
- page 3 handwriting: Handwritten correction of the balance to 386,500, with initials

**case-03**: 
- page 1 handwriting: Centre clerk's handwritten hearing date
- page 2 handwriting: Tenant staff's handwritten receipt note

**case-04**: 
- deadline 2026-09-14 (page 1, Pay the worker's wages and all dues within 14 days of the end of the contract on 31 Aug 2026 (Labour Law Article 53); passed without payment): not found

**case-05**: 
- Al Kuthban National Bank PJSC (other): not found
- page 3 signature: Summary judge's signature

**case-06**: 
- deadline 2026-10-02 (page 1, Last day to notify the tenant of any change to the lease terms, including the rent: at least 90 days before the lease ends on 31 Dec 2026 (Article 14). The tenant received the notice on 12 Oct 2026, 80 days before expiry, so the notice was late): not found
- page 2 handwriting: Tenant staff's handwritten receipt note, with the date the notice was received

**case-07**: 
- Dr Nader Salim Al Khoury (other): found, but role given as expert
- date 2026-06-29 (page 1, Claimant discharged from hospital): found on page [3]
- page 3 handwriting: Doctor's handwritten permanent disability percentage

**case-08**: 
- Al Rukn Al Mateen Auditing (other): not found
- deadline 2026-03-31 (page 3, Prepare the 2025 balance sheet, profit and loss account and annual report within three months of the end of the financial year (Article 87); missed, as the draft reached the auditor only on 11 May 2026): not found
- page 2 signature: Claimant's signature

**case-09**: 
- Wael Fahmy Abdelqader (other): found, but role given as expert
- page 2 handwriting: Technician's handwritten note of the second repair, with its date

**case-10**: 
- quote of article 52 (page 3): quote check said differs
- page 3 handwriting: Execution clerk's handwritten note: execution file number and date

**case-11**: 
- page 2 handwriting: Handwritten correction of the debt amount to 293,450, with initials

**case-12**: 
- Ghaymat Al Rayhan Perfumes Trading Est. (defendant): not found
- Faisal Mansour Al Jabri (defendant_representative): not found
- deadline 2026-10-26 (page 1, File the claim on the merits within 20 days of the precautionary order of 6 Oct 2026 (Trademarks Law Art. 47(7)), or the order may be cancelled at the defendant's request; met, the claim was registered on 22 Oct 2026): not found
- page 2 handwriting: Shop cashier's handwritten receipt number

**case-13**: 
- Al Mirsam Engineering Consultants (other): not found
- Karim Fouad Al Halabi (other): found, but role given as expert
- Nadia Samir Awad (other): found, but role given as expert
- Anas Tariq Al Khatib (other): found, but role given as claimant_representative
- date 2026-06-01 (page 1, New Civil Transactions Law (Federal Decree-Law No. 25 of 2025) in force; the 1985 law repealed): not found
- date 2026-09-21 (page 1, Completion certificate issued by the consultant): found on page [2]
- date 2026-09-24 (page 1, Final payment certificate no. 8 issued): found on page [3]
- deadline 2026-10-08 (page 1, Pay the final payment, AED 167,850, within 14 days of the final payment certificate of 24 Sep 2026 (contract clause 9); unpaid): found on page [3]
- deadline 2026-10-21 (page 1, Release the retention, AED 152,650, within 30 days of the completion certificate of 21 Sep 2026 (contract clause 9); unpaid): found on page [3]
- البند (1) من المادة (4) منه (page 1): not found
- page 1 handwriting: Registry clerk's handwritten hearing date
- page 2 handwriting: Actual completion date, handwritten by the supervising engineer (not printed anywhere)
- page 2 handwriting: Handwritten snag list (three items, to be completed within 14 days)
- page 3 handwriting: Handwritten correction of the retention to 152,650, initialled by the supervising engineer

## SAM 3.1 phrasings

| Type | Phrase | Boxes | Hits |
|---|---|---|---|
| signature | signature | 38 | 38/42 |
| stamp | blue stamp | 31 | 31/45 |
| stamp | purple stamp | 24 | 24/45 |
| stamp | stamp | 39 | 39/45 |
