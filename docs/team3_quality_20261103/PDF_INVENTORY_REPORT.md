# Original PDF Inventory and Integrity

## Verified machine execution
- Latest evidence before this documentation package: Integrated Python QA [run 41599191412](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41599191412), Team 3 [run 41599191486](https://github.com/dohun3540-crypto/integration_finished_workforlast/actions/runs/41599191486), head `9995c0620c62f1299fea633ffe34f4a521c6bf10`.
- Command actually executed by both workflows: `python -m qa.inventory --root . --out <new-artifact-directory>`.
- **PASS: 60/60** (20 cases × 3 documents). FAIL 0, BLOCKED 0, duplicate hashes 0.
- Archive `data/cases/SYN-C002-C020_DRAFT_PDFs.tar.xz` SHA-256: `a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc`.
- Original input byte changes: none. Archive is read without extraction to disk. PDF parsing uses `pypdf`, checks manifest hash and page count. The other integrity script and semantic fixture audit also passed in integrated CI.
- Human visual PDF verification: **NOT_VERIFIED**. Official Gold: **BLOCKED**. Studio extraction accuracy: **NOT_MEASURED**.

## Priority original file pointers
| Case | Purchase Order | Delivery Notice | Supplier Quotation | Pages |
|---|---|---|---|---|
| C001 | 9246b693… | 7a5f7b8f… | 35c9dedd… | 1 each |
| C008 | dd8e8b66… | ec6f04c0… | 7b93b501… | 1 each |
| C013 | 8616adc3… | f4d7446b… | 590a11d6… | 1 each |
| C017 | 22d5f85e… | 17f06614… | aad4125f… | 1 each |

Full SHA-256 values, filename, document IDs, page numbers and dates are present in each `data/cases/SYN-C###/manifest.json`, the C001 candidate, and new per-case candidates. For all 60 original rows use the downloadable CI `inventory/INVENTORY_REPORT.json`, `DATA_INVENTORY.csv`, `SOURCE_TEXT_MACHINE.jsonl`. These artifacts are archived evidence, not manually approved labels.

## Re-run
```bash
python -m pip install -r requirements-validation.txt
python -m qa.inventory --root . --out /tmp/team3-new-inventory
python scripts/qa_semantic_pdf_audit.py
```
The output directory must not already exist and should not be placed under original `data/`.
