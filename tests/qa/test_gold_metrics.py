"""Local synthetic test data MUST NOT be reported as actual human approval."""
from copy import deepcopy

from qa.gold_metrics import MISSING, evaluate, flatten, lookup, typed_equal


def add_test_evidence(gold, doc, source):
    """SYNTHETIC fixtures; never represent an actual Human Gold approval."""
    for path, value in flatten(doc):
        row = {"document_id": doc["document_id"], "field_path": path,
               "source_file_sha256": source["sha256"], "page": source["source_page"],
               "decision": "ACCEPT", "review_record_sha256": "d" * 64}
        if value is None:
            row["absence_confirmed"] = True
        else:
            row["source_original_text"] = str(value)
        gold["approved_field_evidence"].append(row)


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
    gold["approved_field_evidence"] = []
    add_test_evidence(gold, gold["field_gold_candidate"][0], gold["sources"][0])
    binding = {"execution_kind": "STUDIO_NATIVE", "case_id": "SYN-TEST",
               "job_id": "synthetic-job",
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
    add_test_evidence(gold, notice, gold["sources"][-1])
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
    evidence = deepcopy(gold["approved_field_evidence"])
    pred["evidence"] = evidence
    assert evaluate(pred, gold, binding)["status"] == "PASS"
    for record in evidence:
        if record.get("absence_confirmed"):
            record.pop("review_record_sha256")
    assert evaluate(pred, gold, binding)["status"] == "FAIL"



def test_unreviewed_gold_citations_cannot_create_official_metrics():
    gold, binding, pred = sample()
    gold["approved_field_evidence"].pop()
    report = evaluate(pred, gold, binding)
    assert report["status"] == "BLOCKED"
    assert report["accuracy_status"] == "NOT_MEASURED"
    assert report["metrics"] == {}


def test_duplicate_or_invalid_approved_evidence_blocks_evaluation():
    gold, binding, pred = sample()
    gold["approved_field_evidence"].append(deepcopy(gold["approved_field_evidence"][0]))
    assert evaluate(pred, gold, binding)["accuracy_status"] == "NOT_MEASURED"
    gold["approved_field_evidence"].pop()
    gold["approved_field_evidence"][0]["review_record_sha256"] = "NOT_A_SHA"
    assert evaluate(pred, gold, binding)["status"] == "BLOCKED"


def test_wrong_original_evidence_text_does_not_count_as_source_linkage():
    gold, binding, pred = sample()
    pred["evidence"] = deepcopy(gold["approved_field_evidence"])
    assert evaluate(pred, gold, binding)["status"] == "PASS"
    pred["evidence"][0]["source_original_text"] = "UNRELATED TEXT"
    result = evaluate(pred, gold, binding)
    assert result["status"] == "FAIL"
    assert result["metrics"]["evidence_linkage"]["numerator"] < (
        result["metrics"]["evidence_linkage"]["denominator"])


def test_native_case_binding_mismatch_cannot_score():
    gold, binding, pred = sample()
    binding["case_id"] = "SYN-C999"
    assert evaluate(pred, gold, binding)["reason"] == (
        "NATIVE_JOB_CONFIG_FILE_BINDINGS_REQUIRED")
    binding["case_id"] = "SYN-TEST"
    pred["case_id"] = "SYN-C999"
    assert evaluate(pred, gold, binding)["reason"] == "NATIVE_PREDICTION_CASE_MISMATCH"


def test_optional_null_dates_do_not_inflate_date_accuracy_denominator():
    gold, binding, pred = sample()
    gold["field_gold_candidate"][0]["revised_delivery"] = None
    pred["documents"][0]["revised_delivery"] = None
    add_test_evidence(gold, {"document_id": "PO-DOC", "revised_delivery": None},
                      gold["sources"][0])
    report = evaluate(pred, gold, binding)
    assert report["metrics"]["date_normalization"]["denominator"] == 1
