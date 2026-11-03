"""The field audit must not pass on matching numbers elsewhere on a page."""
import json
from pathlib import Path

import pytest

from qa.inventory import collect
from scripts.qa_semantic_pdf_audit import compare_page, normalized_date

ROOT = Path(__file__).resolve().parents[1]


def test_labelled_price_mismatch_cannot_hide_in_an_unrelated_note():
    _, pages, _, _ = collect(ROOT)
    page = next(p for p in pages if p["case_id"] == "SYN-C001"
                and p["document_id"] == "QUOTE-DOC")
    draft = json.loads((ROOT / "data/cases/SYN-C001/extraction_gold.DRAFT.json").read_bytes())
    quote = draft["documents"][2]
    assert compare_page(page["text"], "SYN-C001", quote)["status"] == "PASS"
    changed = page["text"].replace("1000.00 KRW / EA", "999.00 KRW / EA") + "\n1000.00\n"
    result = compare_page(changed, "SYN-C001", quote)
    assert result["status"] == "FAIL"
    assert result["mismatches"][0]["field"] == "quote.unit_price"


def test_missing_quantity_is_not_zero_or_a_verified_complete_case():
    _, pages, _, _ = collect(ROOT)
    page = next(p for p in pages if p["case_id"] == "SYN-C015"
                and p["document_id"] == "C015-NOTICE")
    draft = json.loads((ROOT / "data/cases/SYN-C015/extraction_gold.DRAFT.json").read_bytes())
    notice = draft["documents"][1]
    assert compare_page(page["text"], "SYN-C015", notice)["status"] == "PASS"
    notice["items"][0]["quantity"] = 0
    assert compare_page(page["text"], "SYN-C015", notice)["status"] == "FAIL"


@pytest.mark.parametrize("text", ["2026년 2월 30일", "2026-02-30", "20261108"])
def test_invalid_or_noncanonical_dates_are_never_normalized(text):
    assert normalized_date("2026년 11월 8일") == "2026-11-08"
    with pytest.raises(ValueError):
        normalized_date(text)
