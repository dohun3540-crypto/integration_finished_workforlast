# Independent QA scorecard — verified 2026-10-31 KST

## Successful integrated CI
- Repository: `dohun3540-crypto/leadtime-guardian-agent.copy`.
- Branch: `feat/qa-source-restore-20261031`.
- Restored upstream snapshot: original PR #11 at `f196c694917f2d9e5f4ec228c752bd3f2a4eb882`.
- Upstream blob integrity: **156/156 exact SHA matches** (including binary/PDF/archive), verified in GitHub Git trees. Existing QA files were retained separately.
- Integrated commit: `482251a4adfc3417d13bc677b0101e5d4933f3df`.
- Full Python CI: **134 passed in 8.77s**, `ruff check .`: **All checks passed**.
- Full CI: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178077099
- Independent QA CI: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41178077095
- Integrated review: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/2 (Draft).

## Scope of those 134 checks
- Source repository's existing 80 local unit/integration contract tests.
- New 54 independent QA unit and adversarial tests.
- Coverage includes strict missing-field rejection, malformed/duplicate JSON, fake-vs-real evidence labels, quantity/deadline/currency validation, order conservation, stock double allocation, capacity sharing, duplicate shipping and review-state safeguards.
- No new Studio network job was run by the QA branch; SDK mock tests **are not** live API or Studio runs.

## Still not verified — blocking live evidence/claims
- New real Studio execution for SYN-C013, SYN-C017 and broader C002–C020.
- Source PDF text human-reviewed against any claimed Gold labels: still DRAFT.
- Extraction accuracy / end-to-end latency / actual API cost: **N/A**.
- Business-calendar optimization, real ERP, actual purchase/email functionality: out of MVP scope.
- The source contains the 57 C002–C020 PDF bytes in an archive; extraction/verification into a local worktree may be needed before real Studio runs.
- Full application demo in a live Studio session remains pending team handoff.
- No original repository edits, no merge into main, no force push, no external actions.

## Safe integration next
1. Team 2 supplies updated Adapter/engine outputs without modifying this QA's contract-owner files.
2. Team 3 supplies manually source-reviewed Gold, separate from the actual predictions.
3. Validate latest Git snapshot, re-run all 134+ tests, Ruff and error cases. Then use QA gate with real normalized integrated inputs.
4. Verify real Studio run metadata and PDF evidence; distinguish live, replay, SDK mock and local fixture.
5. Update this scorecard only using test logs, job IDs and evidence.
