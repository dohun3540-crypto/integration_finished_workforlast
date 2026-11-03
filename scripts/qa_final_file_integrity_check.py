"""Read-only audit of tracked JSON, CSV, XLSX, PDF inventory and protected blobs.

This is mechanical file integrity only; it never authenticates Studio jobs or Gold.
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from leadtime_guardian.strict_json import loads_strict
from qa.inventory import collect

KINDS = {"purchase_order", "delivery_notice", "quotation"}
PROTECTED_BLOBS = {
    "src/leadtime_guardian/qa/audit.py": "8de0aaaf7b1911d361bd85c9b970d978a126daac",
    "src/leadtime_guardian/strict_json.py": "afa56a5f201af250eeb28a20580bd0188fe5cb51",
    "src/leadtime_guardian/qa/input_delivery.py": "f838759de7f188b1330a3c93a466f8cfab344e2a",
    "qa/inventory.py": "6bdb6f6d710066e491451bdc21c6233a5965a19d",
    "src/leadtime_guardian/qa/release_inventory.py": "69bc2b0bc5d8bdb683836ded89b94429e5a745a9",
    "src/leadtime_guardian/qa/studio_contract.py": "08b23233ce12575c1c18f654e3ae296b8efa3e7c",
    "src/leadtime_guardian/qa/experiment_compare.py": "379d3c77e93152087a57fc48acb0a837462c13f0",
}
EXPECTED_ARCHIVE_SHA256 = "a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc"


def main() -> int:
    names = [
        raw.decode("utf-8")
        for raw in subprocess.check_output(
            ["git", "ls-files", "-z"], cwd=ROOT
        ).split(b"\0") if raw
    ]
    issues = []
    counts = {"json": 0, "csv": 0, "xlsx": 0, "pdf_direct": 0}
    manifests = []
    for name in names:
        path = ROOT / name
        try:
            if path.suffix == ".json":
                obj = loads_strict(path.read_bytes())
                counts["json"] += 1
                if name.startswith("data/cases/") and name.endswith("/manifest.json"):
                    manifests.append(name)
                    docs = obj.get("documents") if isinstance(obj, dict) else None
                    if (not isinstance(docs, list) or len(docs) != 3
                            or {x.get("document_type") for x in docs
                                if isinstance(x, dict)} != KINDS):
                        issues.append(f"MANIFEST_DOCUMENT_TYPES:{name}")
            elif path.suffix == ".csv":
                with path.open("r", encoding="utf-8-sig", newline="") as stream:
                    rows = list(csv.reader(stream, strict=True))
                counts["csv"] += 1
                if not rows or not rows[0] or len(set(rows[0])) != len(rows[0]):
                    issues.append(f"CSV_HEADER_INVALID:{name}")
                elif any(len(row) != len(rows[0]) for row in rows[1:]):
                    issues.append(f"CSV_WIDTH_MISMATCH:{name}")
            elif path.suffix == ".xlsx":
                from openpyxl import load_workbook

                workbook = load_workbook(path, read_only=True, data_only=False)
                try:
                    if not workbook.sheetnames:
                        issues.append(f"XLSX_NO_SHEETS:{name}")
                finally:
                    workbook.close()
                counts["xlsx"] += 1
            elif path.suffix == ".pdf":
                if not path.is_file():
                    issues.append(f"PDF_NOT_PRESENT:{name}")
                counts["pdf_direct"] += 1
        except (OSError, ValueError, TypeError, KeyError, csv.Error, UnicodeError) as exc:
            issues.append(f"FILE_PARSE_INVALID:{name}:{type(exc).__name__}")

    protected = {}
    for name, expected in PROTECTED_BLOBS.items():
        try:
            actual = subprocess.check_output(
                ["git", "hash-object", name], cwd=ROOT, text=True
            ).strip()
        except subprocess.CalledProcessError:
            actual = None
        protected[name] = {"expected": expected, "actual": actual, "match": actual == expected}
        if actual != expected:
            issues.append(f"PROTECTED_BLOB_MISMATCH:{name}")

    gold_name = "qa/gold_candidates/SYN-C001/candidate.v1.json"
    candidate = loads_strict((ROOT / gold_name).read_bytes())
    candidate_pending = (
        candidate.get("label_status") == "AI_CANDIDATE"
        and candidate.get("human_reviewed") is False
        and candidate.get("team_approved") is False
        and candidate.get("eligible_for_official_metrics") is False
        and candidate.get("gold_frozen") is False
    )
    if not candidate_pending:
        issues.append("GOLD_MUST_REMAIN_UNAPPROVED")

    pdf_rows, _, duplicate_hashes, archive_sha256 = collect(ROOT)
    pdf_counts = {
        status: sum(row["status"] == status for row in pdf_rows)
        for status in ("PASS", "FAIL", "BLOCKED")
    }
    if (len(pdf_rows) != 60 or pdf_counts["PASS"] != 60 or duplicate_hashes
            or archive_sha256 != EXPECTED_ARCHIVE_SHA256):
        issues.append("PDF_ARCHIVE_MANIFEST_INTEGRITY_FAILED")
    if len(manifests) != 20 or counts["pdf_direct"] != 3:
        issues.append("TRACKED_CASE_MANIFEST_OR_DIRECT_PDF_COUNT_MISMATCH")

    result = {
        "status": "PASS" if not issues else "FAIL",
        "scope": "TRACKED_BYTES_AND_MACHINE_PARSE_ONLY",
        "tracked_files": len(names),
        "file_counts": counts,
        "case_manifests": len(manifests),
        "pdf_inventory": {
            "total": len(pdf_rows),
            "counts": pdf_counts,
            "duplicate_hashes": duplicate_hashes,
            "archive_sha256": archive_sha256,
            "archive_pdf_count": len(pdf_rows) - counts["pdf_direct"],
        },
        "protected_blobs": protected,
        "candidate": {"status": "AI_CANDIDATE" if candidate_pending else "INVALID"},
        "reviewed_xlsx": "NOT_PROVIDED" if counts["xlsx"] == 0 else "PRESENT_NOT_APPROVED",
        "human_visual_pdf_review": "NEEDS_HUMAN_REVIEW",
        "studio_live_authentication": "NOT_VERIFIED",
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
