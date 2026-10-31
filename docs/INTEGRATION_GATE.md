# Independent QA integration gate — isolated copy branch

## Scope
This module is deliberately read-only. It does not patch the engine, Studio adapter, original Studio configuration, source PDFs or draft gold. It is **not** a replacement for end-to-end Studio validation.

Run locally:
```sh
python scripts/qa_audit.py --case data/cases/SYN-C001/trusted_base_case.json
python -m pytest -q tests/test_qa_independent.py
python -m ruff check src/leadtime_guardian/qa scripts/qa_audit.py tests/test_qa_independent.py
```

Caution: the trusted base case uses additional project-specific fields; this independent QA checks only selected universal field invariants. Validation against actual repository fixtures remains necessary before gate approval.

## Merge gate
| Gate | Status until verified |
| --- | --- |
| Source branch and binary assets fully restored | BLOCKED |
| Existing pytest regressions | NOT_RUN |
| Existing Ruff checks | NOT_RUN |
| Independent QA regression | NOT_RUN until executed |
| Schema compatibility | NOT_RUN |
| Actual Studio C001 live provenance | NOT_RUN, archived evidence available in source PR |
| Human gold review | BLOCKED |
| Actual C013 and C017 runs | BLOCKED |

No claim of measured Studio extraction accuracy without human-reviewed ground truth. Never merge this work into source repository without explicit review. External actions are prohibited.

## Provenance
Source intended snapshot: source PR #11, `f196c694917f2d9e5f4ec228c752bd3f2a4eb882`. This copy's base was initially README-only, and a complete source tree migration is separately required.
