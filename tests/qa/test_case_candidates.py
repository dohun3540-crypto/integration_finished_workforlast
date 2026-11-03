"""Archived synthetic PDF evidence candidate tests; not Human Gold or Studio scores."""
import json
from pathlib import Path

import pytest

from qa.gold_metrics import evaluate

ROOT = Path(__file__).resolve().parents[2]


def load(case, basename):
    return json.loads((ROOT / f"data/cases/SYN-C{case:03d}" / basename).read_text())


def candidate(case):
    name = ROOT / f"qa/gold_candidates/SYN-C{case:03d}/candidate.machine.v1.json"
    return json.loads(name.read_text())


@pytest.mark.parametrize("case", [8, 13, 17])
def test_source_sha_and_human_approval_absence(case):
    gold = candidate(case)
    manifest = load(case, "manifest.json")
    src = {item["document_id"]: item for item in gold["sources"]}
    assert len(src) == 3
    for doc in manifest["documents"]:
        assert src[doc["document_id"]]["sha256"] == doc["sha256"]
        assert src[doc["document_id"]]["source_page"] == 1
    assert gold["label_status"] == "AI_CANDIDATE"
    assert gold["human_reviewed"] is False
    assert gold["team_approved"] is False
    assert gold["gold_frozen"] is False
    assert gold["eligible_for_official_metrics"] is False
    assert evaluate(None, gold)["accuracy_status"] == "NOT_MEASURED"
    assert evaluate(None, gold)["metrics"] == {}


def test_c008_receipts_and_partial_notice():
    docs = {x["document_type"]: x for x in candidate(8)["field_gold_candidate"]}
    po = {x["receipt_id"]: x["quantity"] for x in docs["purchase_order"]["items"]}
    notice = {x["receipt_id"]: x["quantity"] for x in docs["delivery_notice"]["items"]}
    assert po == {"R1": 40, "R2": 60}
    assert notice == {"R2": 60}
    assert docs["delivery_notice"]["revised_delivery"] == "2026-11-08"


def test_c013_po999_is_original_conflict_not_a_correction():
    docs = {x["document_type"]: x for x in candidate(13)["field_gold_candidate"]}
    assert docs["purchase_order"]["po_id"] == "PO1"
    assert docs["delivery_notice"]["po_id"] == "PO999"
    assert docs["quotation"]["po_id"] == "PO1"


def test_c017_korean_dates_preserved_with_iso_candidates():
    gold = candidate(17)
    dates = [date for src in gold["sources"] for date in src["date_evidence"]]
    assert any(x["source_text"] == "2026년 11월 3일"
               and x["normalized"] == "2026-11-03" for x in dates)
    assert any(x["source_text"] == "2026년 11월 8일"
               and x["normalized"] == "2026-11-08" for x in dates)
    assert any(x["source_text"] == "2026년 11월 4일"
               and x["normalized"] == "2026-11-04" for x in dates)
