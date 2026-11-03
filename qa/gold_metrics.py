"""Read-only evaluator. Neither DRAFT nor AI candidates are official Gold."""
import argparse
import json
import re
from pathlib import Path

from qa.inventory import strict_json

MISSING = object()
DATE_KEYS = {"original_delivery", "revised_delivery", "arrival_date", "eta", "due_date"}


def typed_equal(a, b):
    if b is MISSING or type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(typed_equal(v, b[k]) for k, v in a.items())
    if isinstance(a, list):
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def index_documents(documents):
    if not isinstance(documents, list):
        raise TypeError("expected list")
    result = {}
    for doc in documents:
        if not isinstance(doc, dict):
            raise TypeError("expected object")
        name = doc.get("document_id")
        if not isinstance(name, str) or not name or name in result:
            raise ValueError("missing or duplicate document_id")
        result[name] = doc
    return result


def flatten(value, prefix=""):
    if isinstance(value, dict):
        for key, item in value.items():
            if not prefix and key == "document_id":
                continue
            yield from flatten(item, (prefix + "." if prefix else "") + key)
    elif isinstance(value, list):
        for n, item in enumerate(value):
            yield from flatten(item, f"{prefix}[{n}]")
    else:
        yield prefix, value


def lookup(value, path):
    node = value
    for step in re.findall(r"[^.\[\]]+|\[\d+\]", path):
        if step.startswith("["):
            n = int(step[1:-1])
            if not isinstance(node, list) or n >= len(node):
                return MISSING
            node = node[n]
        elif not isinstance(node, dict) or step not in node:
            return MISSING
        else:
            node = node[step]
    return node


def is_approved(gold):
    flags = ("human_reviewed", "team_approved", "eligible_for_official_metrics",
             "gold_frozen")
    review = gold.get("approval_provenance")
    return (gold.get("label_status") == "HUMAN_GOLD_FROZEN"
            and all(gold.get(k) is True for k in flags)
            and re.fullmatch(r"[0-9a-f]{64}", str(gold.get("gold_sha256", ""))) is not None
            and isinstance(review, dict)
            and all(review.get(k) for k in ("reviewer", "reviewed_at", "approval_record_sha256")))


def bound_native(gold, binding):
    if not isinstance(binding, dict) or binding.get("execution_kind") != "STUDIO_NATIVE":
        return False
    if not all(isinstance(binding.get(k), str) and binding[k]
               for k in ("job_id", "config_id", "workflow_version")):
        return False
    try:
        expected = index_documents(gold["sources"])
        observed = index_documents(binding["file_bindings"])
    except (KeyError, ValueError, TypeError):
        return False
    if expected.keys() != observed.keys():
        return False
    return all(isinstance(observed[k].get("file_id"), str) and observed[k]["file_id"]
               and expected[k].get("sha256") == observed[k].get("sha256")
               and expected[k].get("filename") == observed[k].get("filename")
               for k in expected)


def metric(n, d):
    return {"status": "MEASURED" if d else "NOT_MEASURED",
            "numerator": n, "denominator": d, "rate": n / d if d else None}


def evaluate(prediction, gold, native=None):
    """Official denominator requires frozen reviewed Gold AND bound native execution."""
    result = {"case_id": gold.get("case_id"), "status": "BLOCKED",
              "accuracy_status": "NOT_MEASURED", "official_metrics_eligible": False,
              "release_authorized": False, "metrics": {}, "field_results": [], "reason": ""}
    if not is_approved(gold):
        result["reason"] = "HUMAN_GOLD_NOT_APPROVED"
        return result
    if not bound_native(gold, native):
        result["reason"] = "NATIVE_JOB_CONFIG_FILE_BINDINGS_REQUIRED"
        return result
    if not isinstance(prediction, dict) or not isinstance(prediction.get("documents"), list):
        result["reason"] = "NATIVE_PREDICTION_REQUIRED"
        return result
    try:
        gold_docs = index_documents(gold["field_gold_candidate"])
        pred_docs = index_documents(prediction["documents"])
        sources = index_documents(gold["sources"])
    except (KeyError, ValueError, TypeError):
        result["reason"] = "INVALID_DOCUMENT_SET"
        return result
    if gold_docs.keys() != sources.keys():
        result["reason"] = "GOLD_SOURCE_MISMATCH"
        return result
    scores = {k: [0, 0] for k in ("classification", "fields", "null_preservation",
                                  "date_normalization", "receipt_identity",
                                  "quotation_fields", "evidence_linkage", "item_receipt_identity",
                                  "sentinel_preservation", "date_source_preservation")}
    evidence = prediction.get("evidence", [])
    evidence = evidence if isinstance(evidence, list) else []
    failed = []
    missing = []
    for did, expected in gold_docs.items():
        actual = pred_docs.get(did, {})
        scores["classification"][1] += 1
        scores["classification"][0] += int(typed_equal(
            expected.get("document_type", MISSING), actual.get("document_type", MISSING)))
        for path, want in flatten(expected):
            got = lookup(actual, path)
            ok = typed_equal(want, got)
            scores["fields"][1] += 1
            scores["fields"][0] += int(ok)
            if not ok:
                failed.append({"document_id": did, "field_path": path,
                               "reason": "MISSING" if got is MISSING else "TYPE_OR_VALUE"})
            if got is MISSING:
                missing.append({"document_id": did, "field_path": path})
            column = path.rsplit(".", 1)[-1]
            for category, selected in (
                ("null_preservation", want is None),
                ("date_normalization", column in DATE_KEYS),
                ("receipt_identity", column == "receipt_id"),
                ("quotation_fields", path.startswith("quote.")),
                ("item_receipt_identity", path.startswith("items[") and
                 column in {"product_id", "receipt_id"}),
                ("sentinel_preservation", want is None or
                 (type(want) is str and want == "") or
                 (type(want) is int and want == 0) or
                 (type(want) is bool and want is False)),
            ):
                if selected:
                    scores[category][1] += 1
                    scores[category][0] += int(ok)
            source = sources[did]
            # Each normalized output slot is counted once. Evidence must cite origin.
            scores["evidence_linkage"][1] += 1
            if any(isinstance(e, dict) and e.get("document_id") == did
                   and e.get("field_path") == path
                   and e.get("source_file_sha256") == source.get("sha256")
                   and e.get("page") == source.get("source_page")
                   and (bool(e.get("source_original_text")) or
                        (want is None and e.get("absence_confirmed") is True
                         and bool(e.get("review_record_sha256")))) for e in evidence):
                scores["evidence_linkage"][0] += 1
    # Preserve original language dates separately from their normalized ISO values.
    for did, source in sources.items():
        for entry in source.get("date_evidence", []):
            scores["date_source_preservation"][1] += 1
            if any(isinstance(e, dict) and e.get("document_id") == did
                   and e.get("field_path") == entry.get("field")
                   and e.get("source_original_text") == entry.get("source_text")
                   and e.get("source_file_sha256") == source.get("sha256")
                   and e.get("page") == source.get("source_page") for e in evidence):
                scores["date_source_preservation"][0] += 1
    po = {d.get("po_id") for d in gold_docs.values() if isinstance(d.get("po_id"), str)}
    conflict = len(po) > 1
    detected = typed_equal(conflict, prediction.get("po_conflict_detected", MISSING))
    blocked = not conflict or prediction.get("business_status") == "BLOCKED"
    scores["po_conflict_detection"] = [int(detected), 1]
    scores["po_conflict_business_block"] = [int(blocked), int(conflict)]
    # Incidence is a missing-field rate (lower is better), not detection accuracy.\n    scores["missing_field_incidence"] = [len(missing), scores["fields"][1]]\n    result["metrics"] = {key: metric(*score) for key, score in scores.items()}
    result["field_results"] = failed
    result["missing_fields"] = missing
    result["extra_document_ids"] = sorted(pred_docs.keys() - gold_docs.keys())
    result["accuracy_status"] = "MEASURED"
    result["official_metrics_eligible"] = True
    result["status"] = ("PASS" if not failed and not result["extra_document_ids"]
                        and detected and blocked
                        and scores["evidence_linkage"][0] == scores["evidence_linkage"][1]
                        and scores["date_source_preservation"][0] ==
                        scores["date_source_preservation"][1]
                        else "FAIL")
    result["reason"] = "VALIDATED" if result["status"] == "PASS" else "MISMATCH"
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gold", type=Path, required=True)
    p.add_argument("--prediction", type=Path)
    p.add_argument("--binding", type=Path)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if args.out.exists() or args.out in {args.gold, args.prediction, args.binding}:
        raise FileExistsError("output must be new")
    def read(path):
        return strict_json(path.read_text(encoding="utf-8")) if path else None
    result = evaluate(read(args.prediction), read(args.gold), read(args.binding))
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
