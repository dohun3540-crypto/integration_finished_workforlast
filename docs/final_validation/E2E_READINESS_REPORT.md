# E2E Integration and Operational Readiness

## What was executed, not just reviewed
Exact integrated code/checkpoint: 12aae80750cdb84b40e8d8b7a501d2dc34a7d307.
Evidence: https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41575684831.
The CI executed python -m qa.integration with preserved C001 2026-10-30 archived instruct_original.json, trusted_base_case.json, AI_CANDIDATE candidate.v1.json, case C001 and archived job_gPmEYKzuJdBA6BmKhVnujs. The tool returned release BLOCKED exit code 2 by design while the combined Python Safety V6 status was PASS_LOCAL. Shell asserts these exact facts; unexpected success/FAIL makes CI fail. The existing C001 archive replay and independent QA regression also pass.

The new Team1 e2e_bundle_preflight can read/hash/validate a manifest and correlate original PDF receipt roles, operational/QA Native source bindings, provenance and B0/E1. All 37 synthetic positive/adversarial tests PASS. Its missing live stage manifest/receipt/human Gold evidence is NOT silently invented. A complete provider-authenticated bundle was NOT provided or run.

## Chain status
| Stage | Verification | Limitation |
| --- | --- | --- |
| PDF source + 60 manifest inventory | PASS mechanical SHA/page/role in CI | Human visual source review NOT_RUN |
| Parse/Classify/Extract | Archived V4 C001 and synthetic contracts PASS_LOCAL | New real Studio Stage Raw/Step IDs missing |
| Merge/Normalize | Archived content/metadata parsed, three C001 document types tested | New single operational Job vs split PDF Jobs not authenticated |
| Studio Adapter + Python V6 | Archived C001 read-only CLI PASS_LOCAL; full regression PASS | Not a freshly executed Studio V6 job |
| Evidence-Grounded safety + partial allocations | C013/C008/C017 synthetic fail-closed tests PASS | No latest operational Native provenance |
| Independent QA + Cross-Agent | CI regression PASS for local contract and mismatched evidence | QA provider Job/Report/Native raw and signed provenance still absent |
| B0/E1 comparison gate | Same-source, Case ID, duplicates, normalized metadata tests PASS synthetic | Genuine B0 and E1 matched single-case Jobs NOT_VERIFIED |
| Release | BLOCKED exit=2 intentionally | Human Gold and Studio Live verification required |

## Named cases
- C001 (ARCHIVED_LOCAL): purchase order, revised notice and quote; original shortage 0, changed shortage 60; 60 replacement units, KRW 60,500 quote cost; 3-document archived Native contract; release BLOCKED because QA provider evidence and Gold absent. Previously split 3 independent PDF Jobs must NEVER be treated as a single B0 job.
- C013 (SYNTHETIC_TEST): PO1 vs PO999 is a source PO conflict; preserve original ids, block computation rather than guess merge.
- C008 (SYNTHETIC_TEST): R1=40 and R2=60, only R2 delivery changed; changed shortage 40, alternative quote KRW 40,500; enforce receipt isolation.
- C017 (SYNTHETIC_TEST): normalized ISO dates accepted; unnormalized Korean date string fails closed. No evidence that the live Extract/Normalize transforms raw Korean source correctly.
- B0/E1: no matched authenticated single-case saved config, 3 original PDF SHA receipts, Job+Step identities and IndependentQA verdict pair; measured performance NOT_MEASURED.

## Operational controls / Release gate
Read-only local tools perform NO Studio upload, paid execution, approvals, emails or orders. Python computed recommendation must be reviewed by a person. Original archive replay PASS is NOT independent Studio Live E2E. Original PDF mechanical PASS is NOT accurate extraction or human Gold. Workflow currently allows code development and further non-destructive commits to the Draft PR, not merge/release.

Expected next input bundle: saved B0 and E1 config export+Config IDs, genuine single operational Case Job each, three original PDF bytes/SHA+provider File IDs, Extract/Merge/Normalize Stage Run IDs/raw Native, Team2 calculation bytes with Git commit SHA and provenance, independent QA Job Input/Report/raw, human-reviewed Excel/Gold with review signatures and source page citations. Then execute the read-only preflight CLI, Cross-Agent and comparison and re-evaluate all gates.
