# Team 3 Regression Report — Evidence Boundaries

## Final 2026-11-03 verified executable checkpoint

**Team 3 implementation SHA: `f6fdd1f3d263f86a985e21100d99fbd9986e914e`**

- [Integrated CI run 41602469455](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41602469455): 855 full pytest **PASS**, 37 Team 1 E2E **PASS**, repository Ruff **PASS**, 60/60 PDF SHA/page checks **PASS**, source integrity and archived replay gates successful.
- [Team 3 CI run 41602469577](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41602469577): 89 dedicated pytest **PASS**, QA Ruff **PASS**, PDF 60/60 machine check **PASS**, C001 unapproved-Gold `NOT_MEASURED` guard **PASS**.
- Compared to original integrated baseline 828 passed, additions are retained without edits to Team 1 QA, Team 2 Safety V6, original source PDFs or DRAFT Gold.
- Important remaining evidence: **actual reviewed XLSX bytes unavailable, independent human approval unverified, frozen Gold unavailable, latest Studio Native Job/Config/File data unavailable**. Official accuracy `NOT_MEASURED`, release `BLOCKED`.
- This report is added as a **documentation-only commit after** the above verified source-code HEAD; the documentation commit's CI must be checked separately.


## 2026-11-03 Additional Grounded Regression — Source-matching fix

Verified exact **new code HEAD `ff3319f0e46384fd25b427d44a27958acede275e`**:
- [Integrated Python QA run 41602141542](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41602141542): **854 passed, 0 failures**, Team 1 E2E **37 passed**, full-repo Ruff **PASS**, all 60 PDF source-manifest SHA/page/parser checks **PASS**, archived replay and existing integration/file audits **PASS**.
- [Team 3 run 41602141445](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41602141445): Team 3 **88 passed**, QA Ruff **PASS**, 60/60 PDF **PASS**, unapproved C001 `NOT_MEASURED` negative gate **PASS**.
- Added six synthetic regression tests for frozen source-evidence completeness/uniqueness, incorrect raw evidence, wrong Studio case binding, null-date denominator, and explicit null XLSX tokens; no actual user review was claimed.
- Previous 828 baseline tests were left intact, and original team 1 / team 2 implementation paths were unchanged. A green automated CI is not independent source visual review, human approval, live Studio evaluation or release authorization.

**Post-run reporting commit:** This section and the RELEASE_DATA_GATE metadata are documentation-only changes following that exact validated code head; its own GitHub Actions result must be checked separately. Human Gold **BLOCKED** and official extraction accuracy **NOT_MEASURED** remain unchanged.


## Final source-code validation (subsequent to the checkpoint below)
- Verified **code head** `207d0b8eb2eb6f1d6ef1921876cf008d7d4dd6af` using [Integrated CI run 41600256028](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41600256028): **848 pytest PASS**, Team 1 targeted E2E **37 PASS**, repository Ruff **PASS**, source PDF **60/60 PASS**, archived C001 expected blocked replay, file integrity and semantic fixture audit steps passed.
- [Team 3 run 41600255920](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41600255920): **82 pytest PASS**, QA Ruff **PASS**, 60/60 source PDF PASS, unapproved C001 official metric NOT_MEASURED negative test PASS.
- A development attempt on `cb1d45f7…` failed 3 newly added evaluator tests (845 passed) because a literal escaped newline commented out a metrics assignment. Fixed in the subsequent verified code head above; do not conceal or misattribute this failed CI. A previous TRY004 Ruff issue was also corrected.
- A documentation-only commit containing this section follows the **verified code head**; GitHub CI for that packaging commit must be checked separately.


## Completed GitHub Actions runs
Code head containing all three machine candidates and case tests:
`9995c0620c62f1299fea633ffe34f4a521c6bf10`.

| Check | Actual result | Evidence |
|---|---|---|
| Entire integrated pytest | **847 PASS**, 0 fail, 0 skip | [Integrated Python QA run 41599191412](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41599191412) |
| Team1 targeted E2E | **37 PASS** | same integrated run |
| Team3 dedicated pytest | **81 PASS** | [Team 3 run 41599191486](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41599191486) |
| Repository Ruff | **PASS** | integrated run |
| QA Ruff | **PASS** | dedicated run |
| Original PDF SHA/page/archive/strict parse | **60/60 PASS**, no duplicate hash | both runs |
| `scripts/qa_final_file_integrity_check.py` | **PASS** (workflow step) | integrated run |
| `scripts/qa_semantic_pdf_audit.py` | **PASS** (workflow step) | integrated run |
| Archived C001 replay | **PASS_LOCAL**, external Release BLOCKED expected | integrated run |
| C008/C013/C017 receipt/PO/date candidate regression | **PASS** | included in 847/81 tests |
| Unapproved C001 Gold official accuracy | **NOT_MEASURED** expected, safety-test PASS | dedicated run |
| Latest actual user XLSX | **BLOCKED / NOT_RUN** | original not available |
| New Live Studio extraction accuracy | **NOT_MEASURED** | missing verified native and approved Gold |

Baseline from pre-change integration audit: **828 PASS**. In code head above, total tests increased to 847; previous 828 were not deleted (file inventory and test changes are additive, with existing integration-specific `qa/inventory.py` preserved). Test count increase is not by itself a quality metric.

Earlier during development, the first integrated CI failed on 2 Ruff TRY004 warnings in `qa/gold_metrics.py`. This was fixed in later isolated commits; above runs are the **successful re-validation**. The dedicated run already passed earlier, but earlier integration failure is not erased from the history.

## After the above tested head
Commit(s) adding missing-field incidence and this report package are not included in run 41599191412. **Do not interpret this run as checking a later commit**. The current PR head's own CI must be checked separately. Archived 2026-11-02 Team3 original CI 130 PASS/7 SKIP and earlier 2026-11-03 integrated 828 PASS are historical baselines only.

## Reproduction commands
```bash
python -m pip install -r requirements-validation.txt
python -m pytest tests/qa -q
python -m pytest -q
python -m ruff check .
python -m qa.inventory --root . --out /tmp/member3-inventory-new
python scripts/qa_final_file_integrity_check.py
python scripts/qa_semantic_pdf_audit.py
```
No full local repository checkout was available in the chat container. These checks were executed on the linked GitHub Actions runner with exact run IDs above.
