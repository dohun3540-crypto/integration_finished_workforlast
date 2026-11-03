# Team1 E2E regression — pre-CI boundary

Inherited evidence: PR29 independent QA CI run 41650045135 SUCCESS, prior local tests reported 787 full / 538 QA, isolated integration 845 / 577. Common PR3 CI 41604857978 SUCCESS with earlier 861 full tests and 37 Team1 targeted E2E according to PR description. Those runs refer to DIFFERENT commits: do not combine them into a new pass count. New shared branch runs PENDING until exact-head CI is checked.

Imported regressions: nested and root provenance conflicts, typed config version, C013 three-document preflight, current QA config strict binding, explicit C001/SYN-C001 and C013/SYN-C013 aliases, and parsed native QA verdict. C013 NEEDS_REVIEW must cause cross-agent FAIL by policy; it is not a passing purchase decision. Source PDF 60/60 was previously confirmed by CI but has not yet been revalidated for this new head.

## Integration CI first attempt — confirmed diagnosis

Exact integrated PR #4 commit `712eeb0077a8197cb8841051458fb7eed11ce443`: [CI #41652592519](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41652592519) concluded **FAILURE**, despite **878 pytest PASS**, Team1 target **37 PASS**, Ruff PASS, PDF source inventory **60/60 PASS**, and archived C001 gate/replay PASS. Downloaded `final-file-audit.json` contained EXACTLY two issues: `PROTECTED_BLOB_MISMATCH` for `qa/release_inventory.py` and `qa/experiment_compare.py`, because old hard-pinned hashes did not match the now-verified PR29 updated Git Blobs. Other five protected blob assertions matched exactly. Updated only the two pinned expected hashes, retaining all validators and all tests; next exact-head CI PENDING.
