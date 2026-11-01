"""Read-only strict original Stage evidence intake. No provider API requests."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from leadtime_guardian.qa.audit import load_json_strict
from leadtime_guardian.qa.stage_trace import STAGES, audit_stage_evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest_path = args.manifest.resolve(strict=True)
        manifest = load_json_strict(manifest_path.read_bytes())
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be a JSON object")
        metadata = manifest.get("stages", {})
        if not isinstance(metadata, dict):
            raise ValueError("stages must be object")
        artifacts = {}
        for name in STAGES:
            item = metadata.get(name)
            if not isinstance(item, dict) or item.get("path") is None:
                continue
            relative = item["path"]
            if (not isinstance(relative, str) or not relative
                    or Path(relative).is_absolute()):
                raise ValueError("path must be nonempty manifest-relative")
            path = (manifest_path.parent / relative).resolve(strict=True)
            if not path.is_relative_to(manifest_path.parent):
                raise ValueError("path escapes manifest directory")
            artifacts[name] = path.read_bytes()
        result = audit_stage_evidence(manifest, artifacts)
    except (OSError, TypeError, ValueError, UnicodeDecodeError):
        result = {
            "status": "FAIL", "release_or_merge_authorized": False,
            "studio_live_execution_authenticated": False,
            "issues": [{"issue_code": "MANIFEST_OR_STAGE_FILE_UNREADABLE",
                        "stage": "cli", "severity": "ERROR"}],
        }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 1 if result["status"] == "FAIL" else 2


if __name__ == "__main__":
    raise SystemExit(main())
