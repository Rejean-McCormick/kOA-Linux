from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from koa_operations.backup.plan import BackupPlanError, create_plan, load_plan, write_plan
from koa_operations.backup.run import BackupExecutionError, run_backup
from koa_operations.backup.verify import BackupVerificationError, verify_backup
from koa_operations.config import json_digest, load_mapping, write_json_atomic
from koa_operations.evidence import EvidenceJournal


FIXED_TIME = "2026-08-06T16:00:00Z"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _config(tmp_path: Path, *, backup_set_id: str = "backup-0001") -> dict[str, object]:
    source = tmp_path / "owner-export.bin"
    source.write_bytes(b"owner controlled checkpoint\n")
    primary = tmp_path / "primary"
    independent = tmp_path / "independent"
    members = [
        {
            "backup_id": "identity-primary",
            "source_storage_id": "identity-store",
            "target_storage_id": "backup-primary",
            "owner_id": "identity-and-trust",
            "method": "logical_export",
            "consistency": "application_consistent",
            "restore_after": [],
            "offline_copy_required": False,
            "data_class": "identity-subject-records",
            "source_kind": "owner_export",
            "source_path": str(source),
            "relative_path": "identity/export.bin",
            "checkpoint_ref": "checkpoint:identity:42",
            "checkpoint_state": "committed",
            "owner_evidence_ref": "evidence:identity:42",
            "classification": "restricted",
            "audience_refs": ["audience:recovery-operators"],
            "provenance_ref": "provenance:identity:42",
            "expected_sha256": _sha(source.read_bytes()),
            "required": True,
            "protected_key_material": False,
        },
        {
            "backup_id": "identity-independent",
            "source_storage_id": "identity-store",
            "target_storage_id": "backup-independent",
            "owner_id": "identity-and-trust",
            "method": "logical_export",
            "consistency": "application_consistent",
            "restore_after": ["identity-primary"],
            "offline_copy_required": True,
            "data_class": "identity-subject-records",
            "source_kind": "owner_export",
            "source_path": str(source),
            "relative_path": "identity/export.bin",
            "checkpoint_ref": "checkpoint:identity:42",
            "checkpoint_state": "committed",
            "owner_evidence_ref": "evidence:identity:42",
            "classification": "restricted",
            "audience_refs": ["audience:recovery-operators"],
            "provenance_ref": "provenance:identity:42",
            "expected_sha256": _sha(source.read_bytes()),
            "required": True,
            "protected_key_material": False,
        },
    ]
    assembly_items = [
        {
            key: member[key]
            for key in (
                "backup_id",
                "source_storage_id",
                "target_storage_id",
                "owner_id",
                "method",
                "consistency",
                "restore_after",
                "offline_copy_required",
            )
        }
        for member in members
    ]
    return {
        "canonical_schema_ref": "docs/contracts/artifact-contracts/backup-set.schema.json",
        "backup_set_id": backup_set_id,
        "operation_id": "operation-backup-0001",
        "correlation_id": "correlation-backup-0001",
        "created_at": FIXED_TIME,
        "tenant_id": "tenant-a",
        "environment_id": "production-a",
        "profile_id": "sovereign-linux-node",
        "authority_scope_ref": "authority:tenant-a:production-a",
        "policy_decision_ref": "decision:backup-approved:0001",
        "release_context": {
            "source_release_set_ref": "release-set:stable:42",
            "authority_release_ref": "authority-release:42",
            "manifest_ref": "release-manifest:42",
            "manifest_sha256": "1" * 64,
            "lock_ref": "release-lock:42",
            "lock_sha256": "2" * 64,
            "verification_evidence_ref": "evidence:release:42",
        },
        "objectives": {
            "rpo_seconds": 3600,
            "rto_seconds": 7200,
            "retention_days": 30,
            "restore_test_interval_days": 7,
        },
        "limits": {
            "max_members": 10,
            "max_total_bytes": 1024 * 1024,
            "max_duration_seconds": 60,
            "max_concurrency": 1,
            "max_retries": 3,
        },
        "encryption": {
            "required": True,
            "envelope_profile_ref": "encryption-profile:restricted",
            "data_key_identity_ref": "key:backup-data:42",
            "recipient_key_identity_ref": "key:backup-recipient:42",
            "key_custody_ref": "custody:backup:42",
        },
        "offline_copy_required": True,
        "targets": [
            {
                "target_id": "backup-primary",
                "root_path": str(primary),
                "independent": False,
                "offline": False,
                "immutable": True,
                "protected": True,
                "encryption_context_ref": "encryption-context:primary",
                "retention_policy_ref": "retention:30-days",
            },
            {
                "target_id": "backup-independent",
                "root_path": str(independent),
                "independent": True,
                "offline": True,
                "immutable": True,
                "protected": True,
                "encryption_context_ref": "encryption-context:offline",
                "retention_policy_ref": "retention:30-days",
            },
        ],
        "members": members,
        "assembly_backup_plan": {
            "items": assembly_items,
            "restore_order": ["identity-primary", "identity-independent"],
        },
    }


def _schema(tmp_path: Path) -> Path:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://koa.example/contracts/artifact-contracts/backup-set.schema.json",
        "type": "object",
        "required": [
            "format",
            "$schema",
            "backup_set_id",
            "lifecycle_state",
            "members",
            "targets",
            "plan_digest",
        ],
        "properties": {
            "format": {"const": "koa.operations.backup-manifest.v1"},
            "$schema": {"const": "docs/contracts/artifact-contracts/backup-set.schema.json"},
            "backup_set_id": {"type": "string"},
            "lifecycle_state": {"const": "assembled"},
            "members": {"type": "array", "minItems": 1},
            "targets": {"type": "array", "minItems": 1},
            "plan_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
    }
    path = tmp_path / "backup-set.schema.json"
    path.write_text(json.dumps(schema), encoding="utf-8")
    return path


def _run(tmp_path: Path):
    config = _config(tmp_path)
    plan = create_plan(config)
    journal = EvidenceJournal(tmp_path / "evidence", clock=lambda: FIXED_TIME)
    result = run_backup(plan, evidence_journal=journal, clock=lambda: FIXED_TIME)
    return plan, journal, result


def test_plan_is_deterministic_and_preserves_assembly_ownership(tmp_path: Path) -> None:
    config = _config(tmp_path)
    first = create_plan(config)
    second = create_plan(config)
    assert first.digest == second.digest
    assert first.restore_order == ("identity-primary", "identity-independent")
    assert first.members["identity-primary"].owner_id == "identity-and-trust"
    path = tmp_path / "plan.json"
    write_plan(path, first)
    loaded = load_plan(path)
    assert loaded.digest == first.digest


def test_plan_rejects_cycle_owner_change_and_private_keys(tmp_path: Path) -> None:
    config = _config(tmp_path)
    config["members"][0]["restore_after"] = ["identity-independent"]  # type: ignore[index]
    config["assembly_backup_plan"]["items"][0]["restore_after"] = ["identity-independent"]  # type: ignore[index]
    with pytest.raises(BackupPlanError, match="cycle"):
        create_plan(config)
    config = _config(tmp_path)
    config["members"][0]["owner_id"] = "backup-coordinator"  # type: ignore[index]
    with pytest.raises(BackupPlanError, match="changes assembly field owner_id"):
        create_plan(config)
    config = _config(tmp_path)
    config["members"][0]["protected_key_material"] = True  # type: ignore[index]
    with pytest.raises(BackupPlanError, match="private-key"):
        create_plan(config)


def test_run_and_verify_all_targets_with_canonical_schema(tmp_path: Path) -> None:
    plan, journal, result = _run(tmp_path)
    assert result["execution_state"] == "completed"
    assert result["committed_targets"] == ["backup-independent", "backup-primary"]
    report = verify_backup(
        plan,
        result,
        evidence_journal=journal,
        canonical_schema_path=_schema(tmp_path),
        clock=lambda: FIXED_TIME,
    )
    assert report["verification_state"] == "verified"
    assert report["restore_eligible"] is True
    assert report["restore_tested"] is False
    assert len(journal.verify("correlation-backup-0001")) == 2


def test_verify_without_canonical_schema_is_blocked_not_success(tmp_path: Path) -> None:
    plan, journal, result = _run(tmp_path)
    with pytest.raises(BackupVerificationError) as captured:
        verify_backup(plan, result, evidence_journal=journal, clock=lambda: FIXED_TIME)
    assert captured.value.report["verification_state"] == "blocked"
    assert captured.value.report["restore_eligible"] is False
    assert "backup_set_schema_unavailable" in captured.value.report["blocking_reasons"]


def test_corruption_fails_verification_and_writes_evidence(tmp_path: Path) -> None:
    plan, journal, result = _run(tmp_path)
    target = Path(plan.targets["backup-primary"].root_path)
    payload = target / "backup-sets" / "backup-0001" / "members" / "identity" / "export.bin"
    payload.write_bytes(b"corrupt")
    with pytest.raises(BackupVerificationError) as captured:
        verify_backup(
            plan,
            result,
            evidence_journal=journal,
            canonical_schema_path=_schema(tmp_path),
            clock=lambda: FIXED_TIME,
        )
    assert captured.value.report["verification_state"] == "failed"
    assert any("member_integrity_failed" in item for item in captured.value.report["errors"])
    assert len(journal.verify("correlation-backup-0001")) == 2


def test_failed_run_preserves_previous_backup_and_reports_failure(tmp_path: Path) -> None:
    config = _config(tmp_path)
    previous = Path(config["targets"][0]["root_path"]) / "backup-sets" / "previous-verified"  # type: ignore[index]
    previous.mkdir(parents=True)
    marker = previous / "marker"
    marker.write_text("verified", encoding="utf-8")
    config["members"][0]["expected_sha256"] = "0" * 64  # type: ignore[index]
    plan = create_plan(config)
    journal = EvidenceJournal(tmp_path / "evidence", clock=lambda: FIXED_TIME)
    with pytest.raises(BackupExecutionError) as captured:
        run_backup(plan, evidence_journal=journal, clock=lambda: FIXED_TIME)
    assert captured.value.result["execution_state"] == "failed"
    assert captured.value.result["previous_verified_backup_preserved"] is True
    assert marker.read_text(encoding="utf-8") == "verified"


def test_existing_set_is_never_overwritten(tmp_path: Path) -> None:
    config = _config(tmp_path)
    existing = Path(config["targets"][0]["root_path"]) / "backup-sets" / "backup-0001"  # type: ignore[index]
    existing.mkdir(parents=True)
    marker = existing / "marker"
    marker.write_text("old", encoding="utf-8")
    plan = create_plan(config)
    journal = EvidenceJournal(tmp_path / "evidence", clock=lambda: FIXED_TIME)
    with pytest.raises(BackupExecutionError, match="refusing to replace"):
        run_backup(plan, evidence_journal=journal, clock=lambda: FIXED_TIME)
    assert marker.read_text(encoding="utf-8") == "old"


def test_cli_exposes_blocked_verification_with_nonzero_exit(tmp_path: Path) -> None:
    config_path = tmp_path / "config.json"
    write_json_atomic(config_path, _config(tmp_path))
    plan_path = tmp_path / "plan.json"
    run_path = tmp_path / "run.json"
    verify_path = tmp_path / "verify.json"
    evidence = tmp_path / "cli-evidence"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parents[1] / "src")
    base = [sys.executable, "-m", "koa_operations"]
    planned = subprocess.run(base + ["backup", "plan", "--config", str(config_path), "--output", str(plan_path), "--evidence-dir", str(evidence)], env=env, capture_output=True, text=True)
    assert planned.returncode == 0, planned.stderr
    executed = subprocess.run(base + ["backup", "run", "--plan", str(plan_path), "--output", str(run_path), "--evidence-dir", str(evidence)], env=env, capture_output=True, text=True)
    assert executed.returncode == 0, executed.stderr
    verified = subprocess.run(base + ["backup", "verify", "--plan", str(plan_path), "--run-result", str(run_path), "--output", str(verify_path), "--evidence-dir", str(evidence)], env=env, capture_output=True, text=True)
    assert verified.returncode == 5
    report = load_mapping(verify_path)
    assert report["verification_state"] == "blocked"
    assert report["restore_eligible"] is False


def test_evidence_chain_detects_tampering(tmp_path: Path) -> None:
    journal = EvidenceJournal(tmp_path / "evidence", clock=lambda: FIXED_TIME)
    journal.record(operation_id="operation-a", correlation_id="correlation-a", phase="backup_plan", outcome="succeeded", subject_ref="backup-set:a", details={"a": 1})
    journal.record(operation_id="operation-a", correlation_id="correlation-a", phase="backup_run", outcome="succeeded", subject_ref="backup-set:a", details={"b": 2})
    records = sorted((tmp_path / "evidence" / "correlation-a").glob("*.json"))
    altered = json.loads(records[0].read_text(encoding="utf-8"))
    altered["phase"] = "tampered"
    records[0].write_text(json.dumps(altered), encoding="utf-8")
    from koa_operations.evidence import EvidenceError
    with pytest.raises(EvidenceError, match="broken evidence chain"):
        journal.verify("correlation-a")
