# Team 3 → Team 1 Gu Dohun: Read-only Data Contract

## Files ready for immediate use
- `qa/inventory.py` — original PDF integrity reader, `collect(root)` for rows/pages/hash duplication diagnostics (preserve newer integrated implementation).
- `qa/gold_candidates/SYN-C001/candidate.v1.json` + `PDF_EVIDENCE_MATRIX.csv` + `REVIEW_GUIDE.md` — human approval pending, do not use as official Gold.
- `qa/gold_candidates/SYN-C008/candidate.machine.v1.json`, `SYN-C013/...`, `SYN-C017/...` — machine evidence candidates, not Human Gold.
- `qa/review_bridge.py` — `inspect_xlsx_review(original_xlsx_bytes, baseline_csv_bytes, sheet)`; returns cell-level discrepancy and original-byte hashes, never approves.
- `qa/gold_metrics.py` — `evaluate(studio_prediction, approved_gold, studio_native_bindings)`; returns `NOT_MEASURED` unless all gates are supplied. Does not touch team1 QA or Python V6.
- `tests/qa/test_gold_metrics.py`, `test_review_bridge.py`, `test_case_candidates.py` — synthetic guard tests and case regression.
- `.github/workflows/member3-data-check.yml` — team3-only tests, Ruff, all 60 PDF machine checks, explicit not-measured negative test.
- `docs/team3_quality_20261103/` — this eight-file audit, reproducibility and release gate.

## Minimum case data per record
```json
{
  "case_id": "SYN-C013",
  "document_id": "C013-NOTICE",
  "filename": "SYN-C013_delivery_notice.pdf",
  "sha256": "f4d7446b540c7dd2a50cf566ba47982cc4fcc8ce1230743d8175239eac9d2bfb",
  "page": 1,
  "original_field": "PO999",
  "normalized_candidate": "PO999",
  "label_status": "AI_CANDIDATE",
  "studio_job_id": null,
  "studio_config_id": null,
  "studio_file_id": null
}
```
Machine archived evidence and original SHA are available; field-level human approvals are not.

## Required from other people/systems
- From Team 3 / real reviewer: *actual latest* `PDF_EVIDENCE_MATRIX.xlsx` bytes (not an OCR reconstruction), sheet, original SHA, original PDF visual evidence for 40 C001 rows, reviewers/time/decisions/corrections and team-authorized signoff; new frozen Gold file + its own digest and approval record digest. For C008/C013/C017, equivalent source review matrices and explicit checked scope.
- From Team 1 Studio: authentic latest Native result JSON (not `extraction_gold.DRAFT.json`), `job_id`, `config_id`, `workflow_version`, `file_bindings[]` for each doc (`document_id`, `file_id`, `filename`, `sha256`), source `evidence[]` with `document_id`, `field_path`, `source_file_sha256`, `page`, `source_original_text`; documented conflict signal `po_conflict_detected` and `business_status`.
- From Team 2 (existing implementation only): no code change requested. Supply any independently verified Safety V6 status and contract output for release notes; never claim a Studio extraction score from engine-only results.

## Safe handoff sequence
1. Verify inventory CI and candidate/source SHA first.
2. Evaluate original XLSX bytes using `qa.review_bridge`; investigate all issues and verify actual humans outside this module.
3. Freeze only genuinely approved evidence in a distinct version, without touching archived DRAFT.
4. Match exact Studio run/job/config/files and document IDs. Reject a 3-independent-job run when a single combined-case job is required.
5. Run `qa.gold_metrics`; separate extraction metrics from PO conflict detection and business block. Check Team 1's QA source gates independently.
6. Keep Release Gate **BLOCKED** until human evidence and authentic Studio results are verified.

All paths with `review/approved/` or `review/native/` in examples are required future inputs, not existing project files.



## New required Gold/source fields in Team 3 evaluator

To prevent incorrect Evidence credit and cross-case mixing, provide
`approved_field_evidence[]` **after actual human review**. Every normalized
field leaf requires one uniquely keyed reviewed source citation (including
`document_type` and null fields), matching its source document SHA and page.
Non-null entries require exact `source_original_text`; null entries require
`absence_confirmed=true` plus `review_record_sha256`.
The native-source-binding JSON also requires a matching `case_id`.
No source text, signed approval or timestamps are fabricated by this code.


Team 1 can pass `case_id="C001"` (Studio/QA convention) for Gold `"SYN-C001"`; the evaluator accepts only this documented prefix alias, not arbitrary filename/Job ID mixing. All document IDs, filenames, file hashes and source citations must still match.


## Verified final source code checkpoint
Implementation `f6fdd1f3d263f86a985e21100d99fbd9986e914e`: integration run 41602469455 **855 PASS**, Team 3 run 41602469577 **89 PASS**, Ruff PASS, 60/60 PDF PASS. Human Gold approval and real latest Studio Native linking are still BLOCKED. Reports are packaged in a later documentation-only commit; use PR CI to verify the packaged HEAD.
