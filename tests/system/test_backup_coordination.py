from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "operations/src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from koa_operations.backup.plan import create_plan  # noqa: E402
from koa_operations.backup.run import BackupExecutionError, run_backup  # noqa: E402
from koa_operations.backup.verify import verify_backup  # noqa: E402
from koa_operations.evidence import EvidenceJournal  # noqa: E402

FIXED_TIME = "2026-08-06T16:00:00Z"


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _config(tmp_path: Path) -> dict[str, object]:
    source = tmp_path / "owner-export.bin"
    source.write_bytes(b"owner-controlled checkpoint\n")
    members = []
    for backup_id, target_id, offline, after in (
        ("identity-primary", "primary", False, []),
        ("identity-offline", "offline", True, ["identity-primary"]),
    ):
        members.append({
            "backup_id": backup_id,
            "source_storage_id": "identity-store",
            "target_storage_id": target_id,
            "owner_id": "identity-and-trust",
            "method": "logical_export",
            "consistency": "application_consistent",
            "restore_after": after,
            "offline_copy_required": offline,
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
        })
    assembly_items = [{key: member[key] for key in (
        "backup_id", "source_storage_id", "target_storage_id", "owner_id",
        "method", "consistency", "restore_after", "offline_copy_required",
    )} for member in members]
    return {
        "canonical_schema_ref": "docs/contracts/artifact-contracts/backup-set.schema.json",
        "backup_set_id": "backup-system-001",
        "operation_id": "operation:backup:system:001",
        "correlation_id": "correlation:backup:system:001",
        "created_at": FIXED_TIME,
        "tenant_id": "tenant-a",
        "environment_id": "production-a",
        "profile_id": "sovereign-linux-node",
        "authority_scope_ref": "authority:tenant-a:production-a",
        "policy_decision_ref": "decision:backup-approved:001",
        "release_context": {
            "source_release_set_ref": "release-set:active",
            "authority_release_ref": "authority-release:42",
            "manifest_ref": "release-manifest:42",
            "manifest_sha256": "1" * 64,
            "lock_ref": "release-lock:42",
            "lock_sha256": "2" * 64,
            "verification_evidence_ref": "evidence:release:42",
        },
        "objectives": {"rpo_seconds": 3600, "rto_seconds": 7200, "retention_days": 30, "restore_test_interval_days": 7},
        "limits": {"max_members": 10, "max_total_bytes": 1048576, "max_duration_seconds": 60, "max_concurrency": 1, "max_retries": 3},
        "encryption": {
            "required": True,
            "envelope_profile_ref": "encryption-profile:restricted",
            "data_key_identity_ref": "key:backup-data:42",
            "recipient_key_identity_ref": "key:backup-recipient:42",
            "key_custody_ref": "custody:backup:42",
        },
        "offline_copy_required": True,
        "targets": [
            {"target_id": "primary", "root_path": str(tmp_path / "primary"), "independent": False, "offline": False, "immutable": True, "protected": True, "encryption_context_ref": "encryption:primary", "retention_policy_ref": "retention:30-days"},
            {"target_id": "offline", "root_path": str(tmp_path / "offline"), "independent": True, "offline": True, "immutable": True, "protected": True, "encryption_context_ref": "encryption:offline", "retention_policy_ref": "retention:30-days"},
        ],
        "members": members,
        "assembly_backup_plan": {"items": assembly_items, "restore_order": ["identity-primary", "identity-offline"]},
    }


def _schema(tmp_path: Path) -> Path:
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["format", "$schema", "backup_set_id", "lifecycle_state", "members", "targets", "plan_digest"],
        "properties": {
            "format": {"const": "koa.operations.backup-manifest.v1"},
            "$schema": {"const": "docs/contracts/artifact-contracts/backup-set.schema.json"},
            "lifecycle_state": {"const": "assembled"},
            "members": {"type": "array", "minItems": 1},
            "targets": {"type": "array", "minItems": 2},
            "plan_digest": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
    }
    path = tmp_path / "backup-set.schema.json"
    path.write_text(json.dumps(schema), encoding="utf-8")
    return path


def test_backup_coordinates_primary_and_independent_offline_copy(tmp_path: Path) -> None:
    plan = create_plan(_config(tmp_path))
    journal = EvidenceJournal(tmp_path / "evidence", clock=lambda: FIXED_TIME)
    result = run_backup(plan, evidence_journal=journal, clock=lambda: FIXED_TIME)
    report = verify_backup(
        plan,
        result,
        evidence_journal=journal,
        canonical_schema_path=_schema(tmp_path),
        clock=lambda: FIXED_TIME,
    )
    assert plan.restore_order == ("identity-primary", "identity-offline")
    assert result["execution_state"] == "completed"
    assert result["committed_targets"] == ["offline", "primary"]
    assert report["verification_state"] == "verified"
    assert report["restore_eligible"] is True
    assert len(journal.verify("correlation:backup:system:001")) == 2


def test_failed_backup_preserves_previous_verified_material(tmp_path: Path) -> None:
    config = _config(tmp_path)
    previous = Path(config["targets"][0]["root_path"]) / "backup-sets/previous-verified"  # type: ignore[index]
    previous.mkdir(parents=True)
    marker = previous / "marker"
    marker.write_text("verified", encoding="utf-8")
    config["members"][0]["expected_sha256"] = "0" * 64  # type: ignore[index]
    plan = create_plan(config)
    journal = EvidenceJournal(tmp_path / "evidence", clock=lambda: FIXED_TIME)
    with pytest.raises(BackupExecutionError) as captured:
        run_backup(plan, evidence_journal=journal, clock=lambda: FIXED_TIME)
    assert captured.value.result["previous_verified_backup_preserved"] is True
    assert marker.read_text(encoding="utf-8") == "verified"
