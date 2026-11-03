# Team 3 Regression Report — Evidence Boundaries

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
