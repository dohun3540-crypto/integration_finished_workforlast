# Selective integration diff

Source PR29 modifies six Team1 QA/CLI files and adds one Team1 regression file. Five source checkpoint documents stay in the immutable original PR29, not copied as claims of current runtime evidence.

- `experiment_compare.py` and `release_inventory.py`: shared baseline blob exactly matched PR29 base; use PR29 tested content.
- `stage_trace.py`: shared file is older; PR29 is a strict superset of nested/root metadata checks and C013 intake. Use PR29 Team1-owned file.
- `cross_agent.py`: add exact current agent/config/version allow-list and typed validation; preserve shared repo's `expected_github_repository` guard.
- `handoff_builder.py`: add current QA config validator; preserve shared `github_repository` parameter and owner/repo validation.
- `qa_combined_e2e_check.py`: port C013 three-document guard and native report case alias mapping; retain shared `github_repository` param and CLI.
- `tests/test_qa_native_closure.py`: 17 regression cases imported from PR29; previous source CI passed them, new shared environment pending.

Team2 calculation engine, Studio Adapter, Team3 frozen Gold, original PDFs, common PR3 and main untouched. A green PR does not mean a complete Studio Live E2E or approved release.

- `scripts/qa_final_file_integrity_check.py` (integration-only maintenance): bind the exact two intentionally changed PR29 Team1 Git Blobs in the existing strict SHA allowlist; all other protected hash requirements, PDF/Gold parsers and release prohibitions unchanged. CI artifact on attempt #41652592519 proved these were the only two integrity issues.
