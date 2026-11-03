# Read-only Ground Truth Evaluation Contract

Implementation: `qa/gold_metrics.py` and `qa/review_bridge.py`. Both avoid updates to the studio adapter, QA safety, original PDFs, existing DRAFT and workflow configs.

## Hard gate
`evaluate(prediction, gold, native_binding)` only emits measured official metrics if ALL are supplied:
1. Gold metadata `label_status=HUMAN_GOLD_FROZEN`, `human_reviewed=true`, `team_approved=true`, `gold_frozen=true`, `eligible_for_official_metrics=true`, 64-hex Gold digest, plus nonempty reviewer/time/approval-record hash. Human authority and hashes still require independently verified records; metadata alone does not authenticate a person.
2. Native run `execution_kind=STUDIO_NATIVE`, nonempty `job_id`, `config_id`, `workflow_version`, and per-document `file_bindings` with `file_id`, exact filename and original source SHA equal to Gold sources. The calling team must independently verify those identities in Studio.
3. Prediction `documents` with unique `document_id` and Gold `sources` matching each approved document ID.

If not met: `status=BLOCKED, accuracy_status=NOT_MEASURED, metrics={}`. Archived C001 Replay, synthetic DRAFT, AI candidates and detached XLSX cannot yield official accuracy.

## Numerators / denominators
| Indicator (JSON metrics key) | Numerator | Denominator | Meaning |
|---|---|---|---|
| classification | Documents with exact document_type | Approved Gold documents | Classification accuracy |
| fields | Exact type-and-value matches per normalized leaf field | All Gold normalized leaf field slots, document_type included | Field accuracy |
| missing_field_incidence | Expected leaf slots missing from prediction | All expected leaf field slots | Missing incidence, lower is better, NOT accuracy |
| null_preservation | Explicit output null for Gold-null slot | Gold-null slots | Distinguishes null from absent/0 |
| date_normalization | Exact typed ISO output matches for date-named slots | Date-named slots in Gold | Raw original date retention must be checked separately using source evidence |
| receipt_identity | Exact `receipt_id` value matches | Gold receipt_id slots (null included if present) | Identity, not quantity correctness |
| quotation_fields | Exact leaf match under `quote.*` | Gold quotation leaf slots | Quote identifiers, supplier, capacity, cost and currency |
| evidence_linkage | Leaf output slots with matching doc/SHA/page/path and nonempty original text | All Gold leaf slots | Source binding per output slot; null absence needs separately attested source evidence |
| po_conflict_detection | 1 if predicted boolean equals Gold cross-document PO conflict | 1 per case | Collision classification |
| po_conflict_business_block | 1 if contradictory PO IDs and business status BLOCKED | 1 only for conflict cases | Safety gate; no conflict => NOT_MEASURED |

Each metric returns `status`, `numerator`, `denominator`, and `rate`; zero denominator produces `NOT_MEASURED` with rate null, never divide by zero. Missing fields also return precise coordinates in `missing_fields`; errors and extra document IDs are separate. `case status=PASS` requires all checked fields, source evidence, PO conflict detection and business block conditions to pass, but release authorization is always false.

**Duplicate-source policy:** field accuracy and evidence linkage are per *normalized output slot* (`document_id + field_path`), not per independent physical observation. Reused quotation supplier/product/capacity in multiple slots is counted once **per output slot**, so these rates are not the number of distinct ground-truth facts; do not call them independent-observation accuracy. A later analysis may group aliases by shared source cell for an independent factual metric.

**Value policy:** strict Python/JSON type comparison: `null`, missing, `false`, `0`, `0.0`, `""`, `"1000.00"`, `1000` are distinct. No rounding, date guessing, exchange-rate conversion or implicit string→number conversion. List positions use `items[0].receipt_id` paths; the approved Gold must define receipt matching policy when order changes.

## Example
```bash
python -m qa.gold_metrics \
 --gold review/approved/SYN-C001.gold.frozen.json \
 --prediction review/native/latest-studio-result.json \
 --binding review/native/studio-source-bindings.json \
 --out /tmp/team3-official-evaluation.json
```
Input paths are examples, not claims that those files exist. A file labelled Human Gold must be independently verified before this command. **Actual measured extraction accuracy: NOT_MEASURED** as of this audit.
