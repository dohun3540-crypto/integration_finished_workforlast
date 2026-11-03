# LeadTime Guardian — Final Team1 Integration Report
Date: 2026-11-03 KST. Destination is dohun3540-crypto/integration_finished_workforlast, Draft PR #1. All findings describe the checked revision and evidence scope, never a Studio Live claim.

## Source baseline and change control
- Destination main, independently fetched before any write: 67b93291c1f32acaf43e45815d2d1119480b652a (matched requested SHA exactly). Branch created: feat/final-team1-e2e-preflight-20261103. No main updates.
- Baseline exact-SHA destination GitHub Actions: https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41574688500 — 778 passed, Ruff PASS, PDF 60/60 PASS, archived C001/local gate completed. The same SHA is the read-only yuseok_integration PR #2 validated baseline (source run #41465445285).
- QA origin: read-only leadtime-guardian-agent.copy PR #22 HEAD 81569b0ddcc384388ee0e2575ba3cc38cb1bf895, verified using that exact Git tree and file contents. Its separate CI is not evidence for our merged code.
- First imported commit: 491ca36bc13b21ca6d1ac80d5628357e0f6d5414, new code tree 04c9b83ba263dd8b18da89fe7e0b6ee406fa80ac.
- Follow-up reproducible validation commit: 12aae80750cdb84b40e8d8b7a501d2dc34a7d307, Git tree b41a5f34ba8d99349f5cef75b543558694b6a369.

## Exact imported Git blobs
| File | Original QA blob SHA | Destination blob |
| --- | --- | --- |
| src/leadtime_guardian/qa/e2e_bundle_preflight.py | 9fa51ce0d41467fb7618fd9dbf00075c61c38d3c | SAME |
| scripts/team1_e2e_preflight.py | 7968fffbe93be4e67175baa09786dccbe751cdde | SAME |
| tests/test_qa_parallel_e2e_bundle.py | 429bc6f45bdfc63dbaee11d7aed9c30c0df9d94a | SAME |

Each original UTF-8 file was fetched from the specific PR22 head, recreated as a Git blob in the destination, and its returned blob SHA checked for equality BEFORE insertion in the new branch tree. The target previously contained none of these three paths. No hand reconstruction, bulk copying, path collision, replacement, or upstream write occurred.

## Existing implementation preserved
Protected Git blobs verified from baseline and subsequently by the new CI full-file audit:
- qa/audit.py (src/leadtime_guardian/qa/audit.py): 8de0aaaf7b1911d361bd85c9b970d978a126daac
- strict_json.py: afa56a5f201af250eeb28a20580bd0188fe5cb51
- qa/input_delivery.py: f838759de7f188b1330a3c93a466f8cfab344e2a
- qa/inventory.py: 6bdb6f6d710066e491451bdc21c6233a5965a19d
- qa/release_inventory.py: fb8982edb23078cb98a333ac4f9c581ad219ef47
- qa/studio_contract.py: 08b23233ce12575c1c18f654e3ae296b8efa3e7c
- qa/experiment_compare.py: 0c0bbf2c38456019d891625e7486e379e1f96ecf

No replacement of Python Safety V6 engine, Studio adapter, Agents API, Cross-Agent modules, Team3 data, manifests, PDFs, archived Native export, saved Studio config or Gold candidate. Duplicate JSON keys, non-finite/underflow numbers, signed-zero/type mismatches and Case/Job/Config/Step provenance guards remain covered by the integrated regressions. The only existing file subsequently extended was .github/workflows/ci.yml, with additional read-only validation stages.

## Validation automation added
- scripts/qa_final_file_integrity_check.py: repeatable read-only scan of tracked JSON (strict decoding), CSV structures, any tracked XLSX, 20 case manifests, original 60 PDF inventory/archive, protected 7 blob hashes and C001 candidate nonapproval. Writes JSON to standard output. No source mutations.
- CI adds the targeted 37-case test; both CLI --help imports; a real archived C001 via python -m qa.integration (expected BLOCKED and exit=2 with Python V6 PASS_LOCAL); and read-only tracked data audit, in addition to existing Ruff, full pytest, C001 archive and 60-PDF inventory. CI artifact retains logs.
- Exact code SHA 12aae807... run https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575684831: completed SUCCESS, 37 targeted PASS; 815 full PASS; Ruff PASS; archive, offline replay, inventory, full file audit steps SUCCESS.
- For PR checks, the temporary merge commit 4c279c0dbe85b88bf9f019c65dc443c65465efb2 had Git tree b41a5f34ba8d99349f5cef75b543558694b6a369 identical to code HEAD, so its test checkout content was identical at this checkpoint. The final report-only commit must be checked again at its own SHA; earlier CI cannot be reused as evidence for any later code modifications.

## Integration scope and restrictions
Confirmed: Python V6 ↔ archived Studio V4 content/metadata ↔ independent reference QA in local code; Case conflict, partial receipts, null/date/strict input and B0/E1 eligibility are regression-tested. The new Team1 preflight joins SHA-verified local source artifacts only and ALWAYS denies release authorization without authenticated provider/reviewer proof. No complete, newly authenticated operational+QA+Gold E2E bundle was provided, so no actual Live chain nor measured B0/E1 improvement has been claimed.

Historical documents under docs/team1_parallel_readiness_20261103/ and docs/team1_final_hardening_20261103/ were reviewed as prior design/hardening provenance; docs/team1_final_release_audit_20261104/ is the latest QA-side handoff. They are NOT bulk transplanted, to avoid confusing historical standalone QA CI with this integrated code and duplicating superseded reports. Original source documents remain unchanged on read-only PR #22.

## Release
Code integration and regression: PASS for above local/CI scopes. Final provider authentication, confirmed single-case B0/E1 runs, reviewed Gold and actual deployment/release authorization: BLOCKED. See RELEASE_GATE.json and REMAINING_TASKS.md.
