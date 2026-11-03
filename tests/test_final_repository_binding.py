"""Repository/SHA provenance must stay scoped to the caller's actual source."""
import json
import subprocess
import sys
from pathlib import Path

from leadtime_guardian.qa.cross_agent import audit_cross_agent_handoff
from leadtime_guardian.qa.handoff_builder import build_studio_raw_handoff
from scripts.qa_combined_e2e_check import audit_combined_bytes

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "dohun3540-crypto/integration_finished_workforlast"
SHA = "026c949bc82fd747d03ffbc60cd72d04c50ac9c1"
AGENT = "agt_HdtUJPQPXir9rGKgPWSyZG"
CONFIG = "cfg_X2xXakDtmDTHh2RoqVysvL"


def artifacts():
    native = (ROOT / "data/results/studio_runs/C001_20261030_v4/instruct_original.json").read_bytes()
    report = json.dumps({
        "case_id": "C001", "qa_status": "NOT_VERIFIED",
        "checked_document_ids": ["PO-DOC", "NOTICE-DOC", "QUOTE-DOC"],
        "issues": [], "evidence_status": "PARTIAL", "recommended_action": "Verify source",
        "workflow_version": "v1", "execution_provenance": None,
        "field_checks": [{"status": "SOURCE_NOT_VERIFIED", "field": "po_id"}],
    }).encode()
    return native, report


def test_explicit_repository_and_sha_survive_handoff_and_are_independently_bound():
    native, report = artifacts()
    manifest = build_studio_raw_handoff(
        native, report, case_id="C001", agent_id=AGENT, config_id=CONFIG,
        config_version=1, github_sha=SHA, github_repository=REPOSITORY,
        execution_kind="ARCHIVED_REPLAY",
    )
    assert manifest["github"]["repository"] == REPOSITORY
    assert manifest["github"]["head_sha"] == SHA
    options = {"native_bytes": native, "report_bytes": report, "expected_agent_id": AGENT,
               "expected_config_id": CONFIG, "expected_github_sha": SHA}
    result = audit_cross_agent_handoff(manifest, expected_github_repository=REPOSITORY,
                                       **options)
    assert result["qa_status"] == "BLOCKED"
    assert result["release_or_merge_authorized"] is False
    wrong = audit_cross_agent_handoff(manifest, **options)
    assert wrong["qa_status"] == "FAIL"
    assert any(x["issue_code"] == "GITHUB_REPOSITORY_MISMATCH" for x in wrong["issues"])


def test_combined_path_records_and_passes_the_explicit_source_repository():
    native, report = artifacts()
    result = audit_combined_bytes(
        native, (ROOT / "data/cases/SYN-C001/trusted_base_case.json").read_bytes(),
        (ROOT / "configs/schemas/document_extraction.schema.json").read_bytes(),
        operational_job_id="job_gPmEYKzuJdBA6BmKhVnujs", case_id="C001",
        github_sha=SHA, github_repository=REPOSITORY, qa_native_bytes=native,
        qa_report_bytes=report, qa_agent_id=AGENT, qa_config_id=CONFIG,
        qa_config_version=1, execution_kind="ARCHIVED_REPLAY",
    )
    assert result["github"] == {"repository": REPOSITORY, "head_sha": SHA,
                                "authenticated": False}
    assert result["cross_agent_status"] == "BLOCKED"
    assert result["python_safety_status"] == "PASS_LOCAL"
    assert result["release_or_merge_authorized"] is False


def test_repository_binding_is_exposed_through_builder_validator_and_gate_clis(tmp_path):
    native, report = artifacts()
    np, rp, mp = [tmp_path / name for name in ("native.json", "report.json", "manifest.json")]
    np.write_bytes(native)
    rp.write_bytes(report)
    proc = subprocess.run([
        sys.executable, "scripts/qa_prepare_studio_raw_handoff.py", "--native", str(np),
        "--qa-report", str(rp), "--case-id", "C001", "--agent-id", AGENT,
        "--config-id", CONFIG, "--config-version", "1", "--github-sha", SHA,
        "--github-repository", REPOSITORY, "--execution-kind", "ARCHIVED_REPLAY",
        "--manifest-output", str(mp),
    ], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    assert proc.returncode == 2, proc.stderr
    assert json.loads(mp.read_text())["github"]["repository"] == REPOSITORY
    proc = subprocess.run([
        sys.executable, "scripts/qa_cross_agent_check.py", "--manifest", str(mp),
        "--native", str(np), "--qa-report", str(rp), "--expected-agent-id", AGENT,
        "--expected-config-id", CONFIG, "--expected-github-sha", SHA,
        "--expected-github-repository", REPOSITORY,
    ], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["qa_status"] == "BLOCKED"
    proc = subprocess.run([
        sys.executable, "scripts/qa_gate_check.py", "--root", str(ROOT),
        "--studio-handoff", str(mp), "--studio-native", str(np),
        "--studio-qa-report", str(rp), "--expected-agent-id", AGENT,
        "--expected-config-id", CONFIG, "--expected-github-sha", SHA,
        "--expected-github-repository", REPOSITORY,
    ], cwd=ROOT, capture_output=True, text=True, timeout=30, check=False)
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["local_checks_passed"] is True
