# Final Regression and CI Evidence

## Observed chronology (never aggregate overlapping suites)
| Revision | Evidence | Result |
| --- | --- | --- |
| Baseline main 67b93291c1f32acaf43e45815d2d1119480b652a | https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41574688500 | Full 778 passed, 0 failed/skipped; Ruff PASS; C001 archive and 60 PDF PASS |
| Exact-import 491ca36bc13b21ca6d1ac80d5628357e0f6d5414 | https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575183121 | Full 815 passed, 0 failed/skipped; Ruff PASS; C001 archive and inventory PASS |
| Validation automation 12aae80750cdb84b40e8d8b7a501d2dc34a7d307 | https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575684831 | Targeted 37 passed; full 815 passed, 0 failed/skipped; Ruff PASS; CLI smoke, actual offline replay, C001 archive, PDF inventory and tracked-file audit all SUCCESS |

Test count difference: 815 - 778 = 37 newly collected tests in the imported QA test file. The targeted 37 are INCLUDED in 815, not 37 additional to the full-suite total. No assertions or tests were deleted/weakened/skipped. No product failure was observed in the two integrated CI runs; therefore no speculative product bug fix was made.

## Actual executed commands (Ubuntu / Python 3.11, GitHub Actions)
- python -m pip install -r requirements-validation.txt
- python -m ruff check .
- python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
- python scripts/team1_e2e_preflight.py --help
- python -m qa.integration --help
- python -m pytest -q --junitxml=validation-logs/pytest.xml
- python scripts/qa_archive_check.py --root .
- python scripts/qa_gate_check.py --root .
- python -m qa.integration --native data/results/studio_runs/C001_20261030_v4/instruct_original.json --trusted-base data/cases/SYN-C001/trusted_base_case.json --candidate qa/gold_candidates/SYN-C001/candidate.v1.json --case-id C001 --job-id job_gPmEYKzuJdBA6BmKhVnujs --github-sha ece3a7dcc254b5c7a14c72792750170346419eb8
- python -m qa.inventory --root . --out validation-logs/inventory
- python scripts/qa_final_file_integrity_check.py

Offline integrated replay is EXPECTED to exit 2, not 0, because live/human release evidence is absent. CI explicitly verifies exit=2, result.status=BLOCKED, result.combined.python_safety_status=PASS_LOCAL and release_or_merge_authorized=false. A false release PASS would make the CI step FAIL. Native C001 bytes are historical V4 archive, not a newly executed V6 Studio run.

## Cases and failure controls
- C001 archived Native: metadata/content parsing, three document types, calculation 0→60 shortage, 60 units alternative, estimated quote KRW 60,500, local independent QA. Offline command executed in CI; no new Studio job.
- C013 synthetic: inconsistent PO1 vs PO999 must block merged computation; no null-to-valid coercion.
- C008 synthetic: receipt R1 40 / R2 60, change only R2, changed shortage 40, quote KRW 40,500.
- C017 synthetic: ISO revised date accepted; raw Korean date injected directly into engine blocked until valid normalization.
- Adversarial/identity: duplicate PDF or File ID; Case mismatch; metadata/document case relabel; wrong receipt Case; invalid JSON/double keys/nonfinite exponents; invalid config/job/step identity; role swaps; B0 vs E1 unequal PDF bytes; incomplete/no Gold or QA evidence.
- Validation is via the existing combined V6/QA/Cross-Agent/Team3 tests plus the imported 37 targeted preflight tests. It does not prove a full real multi-stage Studio job.

## Artifacts and environment
Latest code-head CI: https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575684831 (integrated-validation-4c279c0dbe85b88bf9f019c65dc443c65465efb2).
Retained files include validation-logs/ruff.txt, team1-e2e-regression.txt, pytest.txt, pytest.xml, archive.json, gate.json, offline-c001.json, inventory/INVENTORY_REPORT.json, final-file-audit.json, Python version, installed dependencies and checkout-sha.txt. The artifact name reflects the PR test merge SHA; its TREE is verified identical to the code HEAD TREE b41a5f34ba8d99349f5cef75b543558694b6a369.
No full local clone test was claimed: current container cannot resolve github.com for this private repository. Actual tests ran in GitHub Actions.
