# Remaining Tasks and Handoffs — Release BLOCKED

## Immediate code status
Integrated QA origin three-file exact Blob import: DONE. First integrated 815 PASS: DONE. Added and tested 37-targeted suite, CLI smoke, C001 archived offline bridge, 60 PDFs and full tracked-file checks in exact code SHA 12aae80750cdb84b40e8d8b7a501d2dc34a7d307: DONE, https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575684831.
Protected seven integrated safety/QA/data module Git Blobs are unchanged. Work remains on feat/final-team1-e2e-preflight-20261103, Draft PR #1 only. CI for this subsequently committed report-only SHA must be independently checked, with exact run linked in PR conversation. Do not merge automatically.

## Blockers before final submission (external evidence)
1. **Team1 / Studio operator**: demonstrate ONE genuine B0-C001 integrated Case Job containing purchase order + delivery notice + quote (not three PDF jobs). Export actual B0 saved config, Config ID/version, operational Job ID, 3 provider File IDs, SHA256 original bytes and all Stage Run IDs/raw/Normalize output. Record execution timestamp and paid-run approval separately. Do not turn a snapshot or archived split jobs into Live evidence.
2. **Team1 / Studio operator**: obtain a genuinely comparable E1-C001 Job on identical source PDF bytes with own saved config and documented execution conditions. Preserve independent QA job IDs if separate. Run B0/E1 same-case matching, evidence completeness and safety gates before computing ANY quality/accuracy change.
3. **Team2 (윤현준)**: supply read-only Safety V6 final actual Native and prediction JSON, source git SHA, execution_provenance, trusted input case, Job/Step/Config binding and adapter-to-Python reproducible command. Confirm quantity/date/amount/receipt and Counterfactual/Partial Delivery outputs against originals. Existing synthetic C008/C013 tests cannot stand in for Live execution.
4. **Team3 (김민주)**: visually review the actual PDF page/table cells for 20 case inventory as required, record reviewer/time/decision, supply real reviewed XLSX/CSV and frozen independently approved Gold. Current AI_CANDIDATE must remain ineligible for official accuracy metrics; no synthetic reviewer signatures.
5. **Team1 / QA**: collect original Independent QA Raw Input and Report, QA Job/Agent/Config IDs, PDF receipt and byte SHA. Construct complete local release-evidence manifest with all listed source paths and SHA declarations. Run scripts/team1_e2e_preflight.py --manifest PATH --json-report NEW_UNUSED_PATH; exit 2 (BLOCKED) is expected absent live proof; a local check must never authenticate its own receipts.
6. **Team1 / Integration**: run same commands at final post-evidence SHA: requirements-validation installation; targeted + full pytest; Ruff; archived C001; inventory; file audit; offline QA CLI; real input preflight; Cross-Agent; B0/E1 comparison. Capture GitHub Actions run SHA/conclusion and archive artifact. Before any main merge, obtain human release decision; no auto-merge or paid execution.

## Additional case proof before release
- C013: run real PO-ID conflict and assert fail-closed; ensure no cross-case merging.
- C008: run real R1/R2 partial deliveries, prove receipt-level allocation and shortage.
- C017: run real Korean-date PDF → normalized ISO date contract, with exact source citation and QA comparison.
- Case-by-case original PDF evidence and null/number/duplicate-key adversarial checks must remain non-bypassable.

## Nonblocking development improvements
- Improve versioned docs for CLI examples, with explicit separate archived/synthetic/live labels.
- Store authenticated stage manifests and reproducible evidence under a controlled evidence directory, not as fabricated fixtures.
- Keep this integrated branch open for safe future additions. Avoid destructive bulk merge from personal copy / yuseok_integration, weakening assertions, replacing stricter strict_json, resetting history or rewriting original PDF/Native artifacts.

## Final requested decisions
SOURCE_INTEGRATION PASS; FULL_REGRESSION PASS; PYTHON_V6 PASS (local); INDEPENDENT_QA PASS (local); CROSS_AGENT PASS (local); FILE_INTEGRITY PARTIAL (mechanical PASS, semantic source and reviewed XLSX pending); DATA_GOLD PENDING; OFFLINE_E2E PASS for archived C001; STUDIO_LIVE_E2E NOT_VERIFIED; GITHUB_CI SUCCESS at verified code SHA; FINAL_RELEASE BLOCKED.
