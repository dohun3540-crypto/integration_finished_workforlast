# Team 3 — Data Quality Audit (2026-11-03)

## Additional contract verification
The additional read-only metric checks verified source text against one uniquely keyed approved Gold citation for every field. Missing or duplicate approval evidence and source-text substitutions now BLOCK official scoring. Native case-id mismatch blocks the same way. Optional null dates no longer inflate date-normalization accuracy. XLSX explicit `null` and blank cells are no longer silently treated as identical. Test results: **854 integrated PASS / 88 Team3 PASS, 60/60 PDF PASS and Ruff PASS** at code HEAD `ff3319f0e46384fd25b427d44a27958acede275e` (runs 41602141542 / 41602141445). These are **synthetic safety tests**, not proof that human review was completed.


## Provenance and scope
- Original read-only: `dohun3540-crypto/leadtime-guardian-agent` @ `a925103077173b37d1cefcd6a9576ae644dc2040`, PR #13.
- Integrated baseline: `dohun3540-crypto/integration_finished_workforlast` @ `e948a4a6d3aba6aacd68495bec422b1e845075a0`.
- Isolated implementation: `feat/team3-gold-data-quality-20261103` / Draft PR #3. Original project, main and old PR #2 were not modified.
- Inspection method: Git tree path list plus Git Blob SHA comparison, followed by targeted content and archived machine-audit review. This is not a new blind human inspection of 60 PDF images.

## File-level reconciliation
| Target | Original blob | Integrated baseline blob | Decision |
|---|---|---|---|
| qa/inventory.py | ee66c440… | 6bdb6f6d… | Preserve integrated strict numeric and path protections |
| qa/review_records.py | 842b886f… | 842b886f… | Identical; preserve |
| qa/xlsx_snapshot.py | acb98567… | acb98567… | Identical; preserve |
| C001 candidate.v1.json | 721cb76a… | 721cb76a… | Identical; preserve AI_CANDIDATE |
| C001 PDF_EVIDENCE_MATRIX.csv | d5183054… | d5183054… | Identical; do not replace |
| C001 REVIEW_GUIDE.md | 69b630e6… | 69b630e6… | Identical |
| qa/templates/* | a7983afd… / 55dc54a5… | identical | Preserve |
| tests/qa/test_inventory.py | f635bec4… | 970b792b… | Preserve integrated newer regression |
| other member3 tests/qa/* | source SHA | identical | Preserve |
| .github/workflows/member3-data-check.yml | bfa8df0c… | missing | Adapted to integrated PR/dispatch trigger rather than copying outdated branch-only workflow |
| qa/reports/*; docs/member3_migration_20261102/* | Source only | Missing | Historical handoff remains in original read-only repo; key facts reconciled in this report package |

No wholesale copy, cherry-pick, original PDF edit, DRAFT edit, Team 1 QA edit, or Team 2 Safety V6 edit.

## Checks and limits
- **PASS (CI source integrity):** 60 manifest-referenced PDF sources, SHA-256, page count, strict PDF parse, approved archive path checks. Duplicate source hashes: none. CI evidence: integrated run 41599191412, Team 3 run 41599191486.
- **PASS (archived semantic fixture validation):** previous `semantic-pdf.json` cross-checks DRAFT against synthetic template labels. Not a claim of independent Gold.
- **PASS (software regression):** see REGRESSION_REPORT.md for the exact verified head and counts.
- **BLOCKED:** Latest user review `PDF_EVIDENCE_MATRIX.xlsx` is absent from the checked repository tree and current supplied files. Original XLSX bytes, SHA-256, sheet state, cell type, reviewer identity, modifications and approvals cannot be checked.
- **NOT_MEASURED:** Live Studio extraction vs approved frozen Human Gold. Previous C001 archived native replay is not current live run; generator DRAFT is not observed prediction.

## Specific data risks and controls
- Identifiers: `"001"` is not numeric `1`; `PO999` must not be substituted by `PO1`.
- Null / missing / empty / zero / false: strict JSON and typed cell comparator avoid silent coercions. Missing XLSX cells cannot authenticate absence.
- Dates: Korean source text preserved alongside ISO machine candidate; malformed dates cannot be guessed or silently rounded.
- Monetary fields: `"1000.00"` decimal string is distinct from numeric 1000 and currency `KRW` remains separate. Shipping 500 is once per quote.
- Receipts: C008 R1=40, R2=60; delivery notice targets only R2. No merging receipts into a single receipt.
- Review records: schema / duplicate / time / decision checks are software validation only. No synthetic reviewer, timestamp, ACCEPT or TEAM_APPROVED is entered in production candidates.
- Evidence: each candidate has per-document filename, SHA, page and date/original evidence where archived audit provides it. Field-by-field human visual verification remains open.

## Newly implemented, safely isolated
- `qa/review_bridge.py`: original XLSX-byte snapshot + strict CSV candidate cell comparison; no mutation or Gold promotion.
- `qa/gold_metrics.py`: source-bound Studio native prediction versus explicitly frozen, human/team-approved Gold contract; official metrics never created for an AI candidate.
- `qa/gold_candidates/SYN-C008|SYN-C013|SYN-C017/candidate.machine.v1.json`: separate unapproved machine-evidence candidates.
- New review/evaluation/case-specific tests and adapted Team 3 CI.


Integration-contract compatibility fix: exact matching of `C001` to `SYN-C001` is supported through narrowly scoped leading-prefix normalization. Distinct case numbers are never interchangeable; the independent QA and Studio adapter code were not modified.
