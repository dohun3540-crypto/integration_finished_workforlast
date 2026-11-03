# File Integrity Audit — Machine Scope Versus Human Source Scope

## Source and command
Initial main source SHA: 67b93291c1f32acaf43e45815d2d1119480b652a; integrated code SHA audited: 12aae80750cdb84b40e8d8b7a501d2dc34a7d307. CI https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575684831. The read-only scripts are python -m qa.inventory --root . --out validation-logs/inventory and python scripts/qa_final_file_integrity_check.py > validation-logs/final-file-audit.json. Both steps completed successfully. Original files are neither regenerated nor edited.

## PDF (60 original synthetic cases)
- Git tree: 3 individual C001 PDFs plus 1 retained XZ-TAR PDF archive for C002–C020 (57 PDFs), NOT 60 individually tracked .pdf paths. This is the original intentional archive layout, not a missing 57-file regression.
- Individual C001 blobs: purchase_order e25b56ec55fa94a7ce6f24545e5d35c800931a03; delivery_notice 1e9e33b967b5f9b184feda7db8c0bc508771e8df; quotation c06cb7f37facde545422f37bb348c004605b8960.
- C002–C020 archive Git Blob: fb4e5b88587468a971dbe2d368d39f3106d9a34a; recorded archive SHA-256: a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc.
- Actual GitHub CI inventory: 60 PASS / 0 FAIL / 0 BLOCKED, no duplicate SHA; 20 manifests and all three document roles per Case. Existing inventory checks declared file hashes, PDF page parse, archive path/size constraints; this is mechanical only. Individual Git Blob SHA is NOT the same algorithmic value as PDF SHA-256.
- Human visual/semantic PDF content comparison: NEEDS_HUMAN_REVIEW. OCR accuracy, true source field meaning, label approval and Studio extraction accuracy were not proven.

## JSON / Config / Native
- Baseline tracked tree contained 114 .json paths, 4 .csv paths and 0 .xlsx paths (before final validation reports). A new gate JSON in this directory may change count at the final docs commit.
- The new audit scans ALL tracked .json files using leadtime_guardian.strict_json.loads_strict, rejecting duplicate keys, malformed Unicode, numeric overflow/non-finite/silent underflow and invalid JSON. It checks the 20 case manifests for three document roles.
- Existing full regression protects strict numeric type, signed zero, null vs zero and provenance/Job/Step/Cfg identity. Schema and Native actual-provider binding are separate from JSON syntax validity.
- Existing saved config source configs/studio_native/config_v4.export.json and data/results/studio_runs/C001_20261030_v4/extractions_native.zip remain Git-blob-identical; archived operational Native is V4 and is not certified as a new Studio Live V6 output.
- Agent ID / Config ID / Job ID / Step Run ID of a new verified live run: NOT_VERIFIED. Source-config static inspection is not authenticated saved configuration evidence.

## CSV / XLSX / Candidate Gold
- The four tracked CSV files include data/cases/case_types.csv, qa/gold_candidates/SYN-C001/PDF_EVIDENCE_MATRIX.csv, qa/templates/CASE_COVERAGE_MATRIX.csv, and qa/templates/HUMAN_REVIEW_LOG.csv. Read-only CI parses CSV structure/headers/width. Suite also includes Team3 review and XLSX parsing tests.
- Tracked reviewed XLSX source: NONE; cannot claim parse success for an absent human-reviewed workbook. XLSX loader executes only if an XLSX file is present; current result is NOT_PROVIDED.
- C001 candidate blob: 721cb76a6a3b9fd07e8ea393ab7dabef43682397. The CI audit explicitly requires label_status=AI_CANDIDATE; human_reviewed=false; team_approved=false; eligible_for_official_metrics=false; gold_frozen=false. APPROVED is prohibited without actual reviewer evidence.

## Python / CI / Docs / protected source
- Original seven protected blobs: audit.py 8de0aaaf..., strict_json.py afa56a5f..., input_delivery.py f838759d..., qa/inventory.py 6bdb6f6d..., release_inventory.py fb8982ed..., studio_contract.py 08b23233..., experiment_compare.py 0c0bbf2c.... New audit executes git hash-object for every protected path and checks its exact 40-character baseline SHA; step PASS on code SHA 12aae807....
- Ruff, complete pytest and CLI --help imports PASS in the same PR CI. Requirements are installed using requirements-validation.txt -> requirements-agents.txt + qa/requirements.txt. No original data/config source changes, and the original Team2 operating engine was not replaced.
- CI generated artifacts are retained for 14 days. Independent claim of all external Studio files being present is NOT_VERIFIED. Archive and candidate remain unapproved.
- Overall REPOSITORY_MACHINE_INTEGRITY: PASS for the tested code revision. COMPLETE_RELEASE_FILE_AND_HUMAN_EVIDENCE: PARTIAL; explicitly pending source visual review, reviewed XLSX/Gold and provider-authenticated raw evidence.
