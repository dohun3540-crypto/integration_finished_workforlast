# C001 Human Gold — Readiness, not approval

## Actual state
```json
{
  "label_status": "AI_CANDIDATE",
  "human_reviewed": false,
  "team_approved": false,
  "eligible_for_official_metrics": false,
  "gold_frozen": false,
  "gold_sha256": null
}
```
C001 `qa/gold_candidates/SYN-C001/candidate.v1.json` and `PDF_EVIDENCE_MATRIX.csv` were preserved unchanged and have the same Blob SHA as Team 3 original. The review guide describes 40 candidate field rows, including 3 document-classification entries and 8 null/absent candidates, and warns about duplicate use of the same quotation source cells.

Original PDF paths:
- `data/cases/SYN-C001/SYN-C001_purchase_order.pdf`
- `data/cases/SYN-C001/SYN-C001_delivery_notice.pdf`
- `data/cases/SYN-C001/SYN-C001_quotation.pdf`

The archived machine PDF text and SHA agree with stored candidate evidence for the fields checked, but this remains source-template vs DRAFT corroboration, not a new human/visual inspection. The release gate remains **BLOCKED**.

## Review XLSX availability
Latest user-edited `PDF_EVIDENCE_MATRIX.xlsx`: **NOT_VERIFIED / MISSING_REQUIRED_EVIDENCE** in current checkout/currently accessible source files. The 2026-11-02 migration handoff explicitly records an earlier attachment that could not be reopened, its actual bytes and SHA absent. The CSV is **not** a substitute for XLSX original bytes.

`qa/review_bridge.py` now supports type-sensitive comparisons against original XLSX bytes via `qa.xlsx_snapshot.snapshot`:
- Cell coordinates, Excel type, Python type, number format and source SHA retained without rewriting workbook.
- Baseline/unknown/duplicate/missing field keys and original candidate values checked.
- `null` vs `0`, `"001"` vs `1`, money string vs number, blank vs field absence, dates and formulas differentiated.
- Reviewer/time/ACCEPT/TEAM_APPROVED are *claims* requiring separate independent review. An XLSX that passes mechanical matching does not promote Gold.
- Corrections or ambiguous decisions require a separately versioned candidate with history; never overwrite the AI baseline.

## Human tasks before promotion
1. Supply original latest XLSX (unmodified byte-for-byte) and choose worksheet explicitly where needed. Record file SHA, workbook metadata, editable vs frozen history and exact reviewed rows.
2. Visually inspect all 3 PDFs and all 40 evidence rows, including null/absence, date contexts and duplicate quote source values.
3. Validate reviewer's actual authority, timestamps, approvals, corrections, conflicts and second review for high-risk cells.
4. Freeze approved *scope only* in a new immutable Gold version, with approval record SHA, effective field list and provenance. Never alter `candidate.v1.json`.
5. Supply a separate actual Studio Native result matching the same original 3 PDFs to calculate official metrics.

## CLI after original XLSX becomes available
```bash
python -m qa.review_bridge \
 --xlsx review/latest/PDF_EVIDENCE_MATRIX.xlsx \
 --csv qa/gold_candidates/SYN-C001/PDF_EVIDENCE_MATRIX.csv \
 --sheet '실제_검수_시트명' \
 --out /tmp/team3-review-comparison.json
```
Exit code 0 means baseline structural comparison PASS only; exit 2 means BLOCKED. It never asserts human approval.
