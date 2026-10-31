# LeadTime Guardian — Independent QA verified scorecard

**Verification date:** 2026-10-31 KST  
**Repository:** `dohun3540-crypto/leadtime-guardian-agent.copy`  
**QA integration branch:** `feat/qa-source-restore-20261031`  
**Draft review:** https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/2

## Verified GitHub Actions checkpoint

The following checks passed on **`62cc55377bc1094d1b59c8251d873d38632d4011`**, before this documentation update.

| Measurement | Outcome | Execution evidence |
| --- | --- | --- |
| Full Python regression | **203 passed in 8.57 s**, Ruff passed | [Python CI #41178897177](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178897177) |
| Independent QA regression | **123 passed in 0.52 s**, Ruff passed | [Independent QA #41178897173](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178897173) |
| Source archive content | **156 / 156 upstream Git blob SHA matches** | Original PR #11: `f196c694917f2d9e5f4ec228c752bd3f2a4eb882` |
| Archived C001 file integrity | **3 / 3 PDF SHA-256 checks** | Independent QA CI archive-check step |
| Original C001 offline replay | **PASS** in automated test | `tests/test_qa_replay.py` |
| Native, current Studio live execution | **NOT_RUN** in this QA session | Requires separate Studio access |
| Human-reviewed ground truth | **NOT_VERIFIED** | Draft Gold is not human-approved |

**Interpretation:** The 203 tests comprise the restored project's original 80 tests plus 123 independent QA contract, replay, archival, adversarial, and CLI tests. This is not 203 Studio executions and not an extraction-accuracy score.

## Latest code hardening

- Corrected a **false FAIL**: the deterministic engine supports nonnegative integer KRW monetary fields; independent input QA now supports integer or decimal-string money while rejecting boolean, float, negative and non-finite values.
- Prevented **false PASS**: missing supplier ID/risk, unknown product, empty customer-order collection, and revised inbound ETA at or before the snapshot date.
- Prevented malformed lists/objects used as order, receipt and quote IDs from crashing the independent validator. They now produce structured QA failures.
- Added detection of altered delivery product IDs and invented supplier-risk output fields.
- Tested the real CLI with subprocesses: normal PASS yields exit code 0; malformed JSON, suspicious outputs, unhashable IDs and absent files yield exit code 1 with JSON error details.
- Preserved the original engine, Studio Adapter, Native Studio config, original PDFs and Gold untouched.

## Source semantics and evidence provenance

| Evidence source | Label / what it proves | Limits |
| --- | --- | --- |
| C001 archived Studio Web job from 2026-10-30 | `REAL_STUDIO_RUN` **historical archived record** | This session did not run Studio again |
| C001 offline deterministic pipeline replay | `ARCHIVED_REPLAY` | Same recorded predictions, not a new inference |
| SDK / fake-client tests | `SDK_HTTP_MOCK` or `FAKE_CLIENT_TEST` | Cannot prove real cloud availability |
| Local engine QA and synthetic tests | `LOCAL_ENGINE_ONLY` | Cannot prove PDF extraction |
| Unreviewed case answer files | `DRAFT_GOLD` | Do not publish accuracy based on these |
| Manually source-verified answer files | `HUMAN_VERIFIED_GOLD` | No new case has this evidenced here |

## Blocking items before live-release claims

1. Actual Studio runs for C013/C017 and the remaining extension cases: **NOT_RUN** in this QA session.
2. Independent manual validation of PDFs against Gold labels: **BLOCKED** awaiting team 3.
3. Final Studio → Adapter integration with team 2's latest ongoing work: **BLOCKED** until their branch is ready.
4. True PDF extraction precision/recall, current latency, operational API costs: **N/A**.
5. End-to-end live demonstration and external procurement/email: **NOT_RUN**. External purchase/send remains outside scope.

**Do not merge this Draft PR into main until the shared integration gate has been reviewed.** Original repository and PR #11 remain read-only throughout this QA work.
