# LeadTime Guardian — Independent QA Integration Gate

**Updated 2026-10-31 KST.** This document applies to the restored QA *copy* branch, not to the live production Studio workflow.

## Ownership and safeguards

- **Team 2:** Python calculation engine, Studio document Adapter, NormalizeDocuments and Studio ↔ Python integration. Read-only in this QA branch.
- **Team 3:** source PDF corpus, expected/Gold data, manual ground-truth reviews. Read-only here; DRAFT must not become HUMAN_VERIFIED automatically.
- **Independent QA:** `src/leadtime_guardian/qa/`, `tests/test_qa_*.py`, QA scripts, QA workflow and QA documentation.
- No writes to original repository or PR #11. No force push or main merge. No live ordering or email sending.

## Actual CI status

| Gate | Observed status |
| --- | --- |
| Upstream checkpoint file restore | **PASS**: 156/156 upstream Git blobs identical, including PDF/ZIP |
| Full repository pytest | **PASS**: 203/203 at tested commit `62cc55377bc1094d1b59c8251d873d38632d4011` |
| Whole-project Ruff | **PASS** at same commit |
| Independent QA pytest | **PASS**: 123/123 at same commit |
| QA Ruff and archived C001 evidence check | **PASS** at same commit |
| Offline C001 Adapter replay and output comparison | **PASS**, not live inference |
| New live C013/C017 | **NOT_RUN** in this QA session |
| Independent source-PDF human Gold verification | **BLOCKED** until team 3 delivers |
| Team 2 latest branch against this QA gate | **BLOCKED**, needs their updated integration snapshot |
| Measured end-to-end extraction accuracy | **NOT_VERIFIED** |

Full CI evidence: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178897177  
QA CI evidence: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178897173

## Reproduction

From the integrated repository with the declared dependencies installed:

```bash
python -m pip install -r requirements-agents.txt
python -m pytest -q
python -m ruff check .
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
python scripts/qa_archive_check.py --root .
```

CLI for a *trusted, integrated* case with its corresponding analysis output:

```bash
python scripts/qa_audit.py --case integrated_case.json --output analysis.json
```

The original `data/cases/SYN-C001/trusted_base_case.json` is **pre-Studio** (no extracted revised ETA/quotes). It is **not** the proper comparison input for the archived C001 completed output. Never claim end-to-end PASS by pairing mismatched stages. Archived `tests/test_qa_replay.py` reconstructs the correct integrated input from immutable saved predictions.

## Merge decision and required evidence

1. Check that team 2 and team 3 supplied separately reviewable artifacts; do not overwrite their files.
2. Re-run original full Python and QA tests against the *combined* updated tree, with Ruff.
3. Evaluate false PASS, false FAIL, malformed-ID, delayed-arrival, double-allocation, Decimal/KRW and blocked-state tests.
4. For Studio findings, record actual Agent ID, Config ID, Job ID, source file hashes and execution evidence. Distinguish archived replay, fake-client, SDK HTTP mock and new Studio execution.
5. Require independently human-verified PDF labels before scoring extraction accuracy. Missing evidence is NOT_VERIFIED, not 100% accuracy.
6. Keep PR #2 Draft and do not merge until checked and authorized separately.

## Historical restoration note

Original PR #11 source snapshot `f196c694917f2d9e5f4ec228c752bd3f2a4eb882` **has already been fully restored and hash-checked** on `feat/qa-source-restore-20261031`. The historical helper `scripts/qa_restore_source.sh` was not used for this Git-object restoration and **must not** be rerun on the integrated branch. All previous notes saying the source files remain un-restored are superseded.

## Continuation

Read `docs/QA_CONTINUATION_HANDOFF.md` and `docs/QA_SCORECARD.md` for exact tested SHA and unresolved work. This independent QA gate does not modify engine/source schemas.
