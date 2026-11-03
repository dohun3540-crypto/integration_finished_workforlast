"""Read-only field comparison for the two archived synthetic PDF templates.

This is machine text consistency, never Human Gold or measured Studio accuracy.
Unknown layouts and unreadable text require review rather than inferred values.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from leadtime_guardian.strict_json import loads_strict
from leadtime_guardian.studio_integration import analyze_studio_documents
from qa.inventory import collect

TITLES = {"purchase_order": "PURCHASE ORDER / 발주서",
          "delivery_notice": "DELIVERY NOTICE / 납기 변경 통보서",
          "quotation": "SUPPLIER QUOTE / 대체 공급업체 견적서"}


def normalized_date(raw):
    match = re.fullmatch(r"([0-9]{4})년 ([0-9]{1,2})월 ([0-9]{1,2})일", raw)
    if match:
        return date(*map(int, match.groups())).isoformat()
    parsed = date.fromisoformat(raw)
    if parsed.isoformat() != raw:
        raise ValueError("noncanonical date")
    return raw


def compare_page(text, case_id, document):
    """Compare labelled fields and exact table cells, never substring matches."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    mismatches, checked, dates = [], [], []

    def check(field, actual, expected):
        checked.append(field)
        if type(actual) is not type(expected) or actual != expected:
            mismatches.append({"field": field, "observed": actual, "expected": expected})

    def value(label):
        positions = [i for i, line in enumerate(lines) if line.split(" / ")[0] == label]
        if len(positions) != 1 or positions[0] + 1 >= len(lines):
            raise ValueError("missing or ambiguous label: " + label)
        return lines[positions[0] + 1]

    def scalar(field, label, expected, *, is_date=False, suffix=""):
        raw = value(label)
        actual = None if raw.startswith("NOT PROVIDED") else raw
        if actual is not None and suffix:
            if not actual.endswith(suffix):
                raise ValueError("unsupported monetary cell: " + label)
            actual = actual[:-len(suffix)]
        if actual is not None and is_date:
            actual = normalized_date(actual)
            dates.append({"field": field, "source_text": raw, "normalized": actual})
        check(field, actual, expected)

    try:
        kind = document["document_type"]
        check("document_type", [line for line in lines if line in TITLES.values()],
              [TITLES[kind]])
        scalar("case_id", "Case ID", case_id)
        scalar("document_id", "Document ID", document["document_id"])
        scalar("po_id", "Related PO" if kind == "quotation" else "PO ID", document["po_id"])
        if kind == "quotation":
            quote = document["quote"]
            for field, label in (("quote_id", "Quote ID"), ("supplier_id", "Supplier ID"),
                                 ("currency", "Currency")):
                scalar("quote." + field, label, quote[field])
            scalar("quote.arrival_date", "Arrival date", quote["arrival_date"], is_date=True)
            scalar("quote.unit_price", "Unit price", quote["unit_price"], suffix=" KRW / EA")
            scalar("quote.shipping_cost", "Shipping cost", quote["shipping_cost"],
                   suffix=" KRW (once per quote)")
            header, fields = ["Product", "Capacity", "Unit"], ["product_id", "quantity", "unit"]
        else:
            scalar("original_delivery", "Original delivery", document["original_delivery"],
                   is_date=True)
            if kind == "delivery_notice":
                scalar("revised_delivery", "Revised delivery", document["revised_delivery"],
                       is_date=True)
            header = ["Product", "Receipt", "Quantity", "Unit"]
            fields = ["product_id", "receipt_id", "quantity", "unit"]
        # C001 uses bilingual column labels and Affected quantity.
        simple = [line.split(" / ")[0].replace("Affected quantity", "Quantity") for line in lines]
        starts = [i for i in range(len(simple)) if simple[i:i + len(header)] == header]
        if len(starts) != 1:
            raise ValueError("unknown table header")
        start = starts[0] + len(header)
        expected_cells = ["NOT PROVIDED" if item.get(field) is None else str(item[field])
                          for item in document["items"] for field in fields]
        check("items", lines[start:start + len(expected_cells)], expected_cells)
        # Verify row count as well; appended rows cannot hide beyond matched cells.
        tail = lines[start + len(expected_cells):]
        if not tail or not tail[0].startswith(("This purchase order", "Original inbound",
                                               "Only the", "Replacement offer")):
            raise ValueError("unexpected extra table cells or missing note")
        if document.get("warnings"):
            for warning in document["warnings"]:
                mentioned_dates = re.findall(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", warning)
                if not mentioned_dates or any(d not in text for d in mentioned_dates):
                    raise ValueError("warning date evidence not present")
        return {"status": "FAIL" if mismatches else "PASS", "checked_fields": checked,
                "mismatches": mismatches, "date_evidence": dates}
    except (ValueError, TypeError, KeyError, IndexError) as exc:
        return {"status": "NEEDS_HUMAN_REVIEW", "checked_fields": checked,
                "mismatches": mismatches, "reason": str(exc), "date_evidence": dates}


def audit(root):
    root = Path(root)
    inventory, pages, duplicates, archive_sha = collect(root)
    schema = loads_strict((root / "configs/schemas/document_extraction.schema.json").read_bytes())
    documents, cases = [], []
    for number in range(1, 21):
        cid = f"SYN-C{number:03}"
        folder = root / "data/cases" / cid
        draft = loads_strict((folder / "extraction_gold.DRAFT.json").read_bytes())["documents"]
        base = loads_strict((folder / "trusted_base_case.json").read_bytes())
        manifests = [row for row in inventory if row["case_id"] == cid]
        current = []
        for doc in draft:
            evidence = [p for p in pages if p["case_id"] == cid
                        and p["document_id"] == doc["document_id"]]
            result = (compare_page(evidence[0]["text"], cid, doc) if len(evidence) == 1
                      else {"status": "NEEDS_HUMAN_REVIEW", "reason": "single text page required"})
            result.update(case_id=cid, document_id=doc["document_id"],
                          document_type=doc["document_type"],
                          source_filename=evidence[0]["source_filename"] if evidence else None,
                          sha256=evidence[0]["source_file_sha256"] if evidence else None,
                          source_page=1 if evidence else None)
            current.append(result)
        documents.extend(current)
        calculation = analyze_studio_documents(base, draft, schema)
        incomplete = any(
            not d.get("revised_delivery") and d["document_type"] == "delivery_notice"
            or any(item.get("quantity") is None or
                   d["document_type"] != "quotation" and item.get("receipt_id") is None
                   for item in d["items"]) for d in draft
        )
        warnings = calculation["review_flags"]
        valid_numbers = all(type(item["quantity"]) is int and item["quantity"] >= 0
                            for d in draft for item in d["items"]
                            if item.get("quantity") is not None)
        valid_money = all(Decimal(str(d["quote"][field])).is_finite()
                          and Decimal(str(d["quote"][field])) >= 0
                          for d in draft if isinstance(d.get("quote"), dict)
                          for field in ("unit_price", "shipping_cost"))
        dimensions = {
            "Completeness": "FAIL" if incomplete else "PASS",
            "Validity": "FAIL" if not valid_numbers or not valid_money else
                        "NOT_VERIFIED" if incomplete else "PASS",
            "Consistency": "PASS" if calculation["status"] == "OK" else "FAIL",
            "Accuracy": "FAIL" if any(d["status"] == "FAIL" for d in current) else
                        "PASS" if all(d["status"] == "PASS" for d in current)
                        else "NEEDS_HUMAN_REVIEW",
            "Uniqueness": "PASS" if len({d["document_id"] for d in draft}) == len(draft)
                          and not duplicates else "FAIL",
            "Timeliness": "PASS" if all(d["status"] == "PASS" for d in current)
                          else "NOT_VERIFIED",
            "Traceability": "PASS" if all(d["sha256"] and d["source_page"] for d in current)
                            else "BLOCKED",
            "Integrity": "PASS" if all(r["status"] == "PASS" for r in manifests) else "FAIL",
        }
        cases.append({"case_id": cid, "dimensions": dimensions,
                      "calculation_status": calculation["execution_status"],
                      "review_flags": warnings,
                      "changed_shortage": calculation["changed_shortage_quantity"],
                      "quote_cost_krw": calculation["estimated_quote_cost_krw"],
                      "human_review": "NEEDS_HUMAN_REVIEW",
                      "cloud_file_ids": "NOT_VERIFIED"})
    return {"status": "PASS" if len(documents) == 60 and
            all(d["status"] == "PASS" for d in documents) else "NEEDS_HUMAN_REVIEW",
            "scope": "MACHINE_TEMPLATE_TEXT_VS_DRAFT_ONLY",
            "archive_sha256": archive_sha, "documents": documents, "cases": cases,
            "human_gold": "MISSING_REQUIRED_EVIDENCE", "reviewed_xlsx": "MISSING_REQUIRED_EVIDENCE",
            "official_metrics_eligible": False, "accuracy_status": "NOT_MEASURED",
            "release_authorized": False,
            "dimension_scope": {
                "Accuracy": "Exact labelled PDF text/table cells versus unapproved generator draft",
                "Timeliness": "PDF dates parse/normalize; no wall-clock or real supplier freshness claim",
                "Traceability": "Local page and original SHA only; cloud receipt not authenticated",
            }}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = audit(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
