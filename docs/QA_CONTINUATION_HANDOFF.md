# QA continuation handoff — 2026-10-31 KST

## Canonical remote

- Work **only** in `dohun3540-crypto/leadtime-guardian-agent.copy`.
- Branch `feat/qa-source-restore-20261031`.
- Draft PR #2: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/2
- Independent early Draft PR #1 contains older QA-only work; do **not** mistake it for current integration PR.
- Read-only upstream PR #11: https://github.com/dohun3540-crypto/leadtime-guardian-agent/pull/11
- Upstream source checkpoint: `f196c694917f2d9e5f4ec228c752bd3f2a4eb882`.
- Last fully observed code-test SHA before documentation-only changes: `62cc55377bc1094d1b59c8251d873d38632d4011`.
- **Resolve the current head on the remote every session**. The text above is a provenance checkpoint, not a static claim that the live branch HEAD will never change.
- 156 original source blob hashes matched byte-for-byte when checked. No upstream engine, Studio Adapter, native config, source PDF or Gold was changed in this QA work.

## Latest measured tests and evidence

| Environment | Verified observation |
| --- | --- |
| Full Python pytest at code checkpoint | 203 passed, Ruff PASS |
| Independent QA pytest at code checkpoint | 123 passed, Ruff PASS |
| Full CI URL | https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178897177 |
| QA CI URL | https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178897173 |
| Archived C001 | 3 PDF SHA-256 verified, metadata consistency PASS, adapter replay PASS |
| New live Studio job initiated in this QA session | **No** |
| Human validated Gold and extraction accuracy | **No / N/A** |

## What this continuation implemented

- `src/leadtime_guardian/qa/audit.py`: input-contract alignment with engine: integer/decimal-string KRW, required supplier fields, unknown SKU rejection, nonempty orders, ETA strictly after snapshot date, safe malformed sections.
- `src/leadtime_guardian/qa/portfolio.py`: fail-closed list/dict IDs in order/receipt/quote references; correct source SKU type validation, delivery product matching and supplier risk provenance.
- `tests/test_qa_independent.py`: normal/invalid money formats and supplier/PO/SKU/ETA edge cases.
- `tests/test_qa_hardening.py`: adversarial engine-output mutations and formerly crashing unhashable IDs.
- `tests/test_qa_cli.py`: actual CLI subprocess exit-code tests for valid, invalid, malformed and missing files.
- `docs/QA_SCORECARD.md`, `docs/INTEGRATION_GATE.md`: updated test evidence and merge limitations.
- Original upstream code, existing test fixtures and original Studio archive deliberately untouched.

## Next safe work units

1. Fetch PR #2 head and *its own* most recent successful CI conclusions; confirm they reference the same SHA. Do not call old CI runs proof for a newer code change.
2. Confirm both original and QA tests still pass if new team 2 adapter updates arrive. Preserve their changes in a new PR or independent integration branch.
3. Import only team-3 independently reviewed labels and confirm source PDF hashes; do not replace predictions with Gold or infer correctness from file names.
4. Run C013/C017 and extension cases against real Studio **only** through permitted Studio access; record Agent ID, Config ID, Job ID and whether it is actually new inference.
5. Perform regression, scorecard refresh and a reviewed merge gate. Keep Draft until verified; do not push to upstream or merge main without separate approval.

## Fail-closed labels

- `PASS`: specific test actually executed and passed.
- `FAIL`: reproduced condition violated contract.
- `BLOCKED`: dependency, source or permission absent.
- `NOT_RUN`: no test executed.
- `NOT_VERIFIED`: claim cannot be supported (not a measured success).

Never claim 100% extraction accuracy from local QA passes, and never treat archived C001 replay as a new Studio run.
