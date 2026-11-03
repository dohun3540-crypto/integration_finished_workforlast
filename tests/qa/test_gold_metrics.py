"""Local synthetic test data MUST NOT be reported as actual human approval."""
from copy import deepcopy

from qa.gold_metrics import MISSING, evaluate, flatten, lookup, typed_equal


def sample():
    gold = {
        "case_id": "SYN-TEST", "label_status": "HUMAN_GOLD_FROZEN",
        "human_reviewed": True, "team_approved": True, "gold_frozen": True,
        "eligible_for_official_metrics": True, "gold_sha256": "a" * 64,
        "approval_provenance": {"reviewer": "TEST_ONLY",
                                "reviewed_at": "2026-11-02T11:00:00+09:00",
                                "approval_record_sha256": "b" * 64},
        "sources": [{"document_id": "PO-DOC", "filename": "po.pdf",
                     "sha256": "c" * 64, "source_page": 1}],
        "field_gold_candidate": [
            {"document_id": "PO-DOC", "document_type": "purchase_order", "po_id": "PO1",
             "supplier_id": None, "original_delivery": "2026-11-03",
             "items": [{"product_id": "A", "receipt_id": "R1", "quantity": 0}],
             "quote": {"unit_price": "1000.00", "shipping_cost": "500"}}]}
    binding = {"execution_kind": "STUDIO_NATIVE", "job_id": "synthetic-job",
               "config_id": "synthetic-config", "workflow_version": "synthetic",
               "file_bindings": [{"document_id": "PO-DOC", "filename": "po.pdf",
                                  "sha256": "c" * 64, "file_id": "synthetic-file"}]}
    pred = {"documents": deepcopy(gold["field_gold_candidate"]),
            "po_conflict_detected": False}
    return gold, binding, pred


def test_strict_types_and_paths():
    assert not typed_equal(None, 0)
    assert not typed_equal(0, False)
    assert not typed_equal(0, 0.0)
    assert not typed_equal("1000.00", 1000)
    assert typed_equal(None, None)
    assert lookup({"items": [{"receipt_id": "R1"}]}, "items[0].receipt_id") == "R1"
    assert lookup({}, "items[0].receipt_id") is MISSING
    assert dict(flatten({"document_id": "D", "items": [{"quantity": 0}]})) == {
        "items[0].quantity": 0}


def test_unapproved_candidate_has_no_official_metrics():
    gold, binding, pred = sample()
    gold["label_status"] = "AI_CANDIDATE"
    gold["human_reviewed"] = False
    report = evaluate(pred, gold, binding)
    assert report["status"] == "BLOCKED"
    assert report["accuracy_status"] == "NOT_MEASURED"
    assert report["metrics"] == {}


def test_unverified_native_job_is_blocked():
    gold, binding, pred = sample()
    assert evaluate(pred, gold)["accuracy_status"] == "NOT_MEASURED"
    binding["execution_kind"] = "ARCHIVED_REPLAY"
    assert evaluate(pred, gold, binding)["accuracy_status"] == "NOT_MEASURED"


def test_sha_mismatch_refuses_official_denominator():
    gold, binding, pred = sample()
    binding["file_bindings"][0]["sha256"] = "d" * 64
    assert evaluate(pred, gold, binding)["metrics"] == {}


def test_valid_synthetic_contract_measures_but_never_releases():
    gold, binding, pred = sample()
    report = evaluate(pred, gold, binding)
    assert report["metrics"]["fields"]["numerator"] == report["metrics"]["fields"][
        "denominator"]
    assert report["accuracy_status"] == "MEASURED"
    assert report["release_authorized"] is False
    assert report["status"] == "FAIL"  # no evidence supplied, not PASS


def test_missing_null_vs_zero_boolean_and_quote_price():
    gold, binding, pred = sample()
    del pred["documents"][0]["supplier_id"]
    pred["documents"][0]["items"][0]["quantity"] = False
    pred["documents"][0]["quote"]["unit_price"] = 1000
    report = evaluate(pred, gold, binding)
    assert {e["field_path"] for e in report["field_results"]} == {
        "supplier_id", "items[0].quantity", "quote.unit_price"}
    assert report["metrics"]["null_preservation"]["numerator"] == 0


def test_po_conflict_detection_and_block_independent():
    gold, binding, pred = sample()
    notice = deepcopy(gold["field_gold_candidate"][0])
    notice["document_id"] = "NOTICE-DOC"
    notice["document_type"] = "delivery_notice"
    notice["po_id"] = "PO999"
    gold["field_gold_candidate"].append(notice)
    pred["documents"].append(deepcopy(notice))
    gold["sources"].append({"document_id": "NOTICE-DOC", "filename": "notice.pdf",
                             "sha256": "d" * 64, "source_page": 1})
    binding["file_bindings"].append({"document_id": "NOTICE-DOC",
                                     "filename": "notice.pdf", "sha256": "d" * 64,
                                     "file_id": "synthetic-notice"})
    pred["po_conflict_detected"] = True
    pred["business_status"] = "COMPLETED"
    report = evaluate(pred, gold, binding)
    assert report["metrics"]["po_conflict_detection"]["numerator"] == 1
    assert report["metrics"]["po_conflict_business_block"]["numerator"] == 0
    pred["business_status"] = "BLOCKED"
    assert evaluate(pred, gold, binding)["metrics"]["po_conflict_business_block"][
        "numerator"] == 1


def test_absence_evidence_requires_explicit_attestation():
    gold, binding, pred = sample()
    document = gold["field_gold_candidate"][0]
    evidence = []
    for path, value in flatten(document):
        record = {"document_id": "PO-DOC", "field_path": path,
                  "source_file_sha256": "c" * 64, "page": 1}
        if value is None:
            record.update(absence_confirmed=True, review_record_sha256="d" * 64)
        else:
            record["source_original_text"] = str(value)
        evidence.append(record)
    pred["evidence"] = evidence
    assert evaluate(pred, gold, binding)["status"] == "PASS"
    for record in evidence:
        if record.get("absence_confirmed"):
            record.pop("review_record_sha256")
    assert evaluate(pred, gold, binding)["status"] == "FAIL"
