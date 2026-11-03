"""Reproductions of numeric crashes and correlated cost-rounding false PASS."""
import json
from copy import deepcopy
from decimal import localcontext
from pathlib import Path

import pytest

from leadtime_guardian.engine import analyze_portfolio
from leadtime_guardian.qa.portfolio import audit_portfolio

ROOT = Path(__file__).resolve().parents[1]


def case():
    return json.loads((ROOT / "data/sample/portfolio_case.json").read_bytes())


@pytest.mark.parametrize("price", ["1e999999", "0.12345678901234567890123456789"])
def test_unrepresentable_cost_blocks_without_mutation(price):
    payload = case()
    payload["quotes"][0]["unit_price"] = price
    before = deepcopy(payload)
    result = analyze_portfolio(payload)
    assert result["execution_status"] == "BLOCKED"
    assert result["needs_review"] is True
    assert result["estimated_quote_cost_krw"] is None
    assert result["supplier_options"] == []
    assert result["evidence_document_ids"] == []
    assert result["review_flags"]
    assert payload == before


@pytest.mark.parametrize("price,reported", [
    ("1e999999", "1e999999"),
    ("0.12345678901234567890123456789", "507.4074073407407407340740741"),
])
def test_independent_qa_never_passes_unverifiable_cost(price, reported):
    payload = case()
    result = analyze_portfolio(payload)
    payload["quotes"][0]["unit_price"] = price
    result["supplier_options"][0]["unit_price"] = price
    result["estimated_quote_cost_krw"] = reported
    report = audit_portfolio(payload, result)
    assert report["qa_status"] == "FAIL"
    assert any(x["issue_code"] == "UNVERIFIABLE_COST_ARITHMETIC" for x in report["issues"])


def test_cost_uses_fixed_precision_without_mutating_callers_decimal_context():
    payload = case()
    payload["quotes"][0]["unit_price"] = "1000.01"
    with localcontext() as context:
        context.prec = 4
        result = analyze_portfolio(payload)
        assert result["estimated_quote_cost_krw"] == "60500.60"
        assert audit_portfolio(payload, result)["qa_status"] == "PASS"
        assert context.prec == 4
