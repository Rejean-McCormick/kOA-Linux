"""Verification of inventory, integrity, target acknowledgements, and contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Mapping

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

from ..config import ConfigurationError, file_digest, json_digest, load_mapping, reject_symlink_chain
from ..evidence import EvidenceJournal, utc_now
from .plan import BackupPlan


class BackupVerificationError(RuntimeError):
    """Raised when verification fails or remains explicitly blocked."""

    def __init__(self, message: str, report: Mapping[str, object]) -> None:
        super().__init__(message)
        self.report = dict(report)


def _load_schema(schema_path: str | Path | None) -> tuple[dict[str, object] | None, str | None]:
    if schema_path is None:
        return None, "backup_set_schema_unavailable"
    path = Path(schema_path)
    if path.name != "backup-set.schema.json":
        return None, "wrong_backup_set_schema"
    try:
        schema = load_mapping(path, max_bytes=8 * 1024 * 1024)
        Draft202012Validator.check_schema(schema)
    except (ConfigurationError, SchemaError) as exc:
        return None, f"invalid_backup_set_schema:{exc}"
    return schema, None


def verify_backup(
    plan: BackupPlan,
    run_result: Mapping[str, object],
    *,
    evidence_journal: EvidenceJournal,
    canonical_schema_path: str | Path | None = None,
    clock: Callable[[], str] = utc_now,
) -> dict[str, object]:
    backup_set_id = str(plan.payload["backup_set_id"])
    operation_id = str(plan.payload["operation_id"])
    correlation_id = str(plan.payload["correlation_id"])
    errors: list[str] = []
    blocked: list[str] = []
    checks: list[str] = []
    if run_result.get("execution_state") != "completed":
        errors.append("backup_run_not_completed")
    if run_result.get("plan_digest") != plan.digest:
        errors.append("plan_digest_mismatch")
    committed = tuple(sorted(run_result.get("committed_targets", [])))
    if committed != tuple(sorted(plan.targets)):
        errors.append("required_targets_not_committed")
    manifests: list[dict[str, object]] = []
    for target_id, target in plan.targets.items():
        set_root = Path(target.root_path) / "backup-sets" / backup_set_id
        try:
            reject_symlink_chain(set_root)
            manifest_path = set_root / "backup-manifest.json"
            ack_path = set_root / "target-ack.json"
            manifest = load_mapping(manifest_path, max_bytes=16 * 1024 * 1024)
            acknowledgement = load_mapping(ack_path)
        except ConfigurationError as exc:
            errors.append(f"target_read_failed:{target_id}:{exc}")
            continue
        manifest_digest = json_digest(manifest)
        if acknowledgement.get("manifest_sha256") != manifest_digest:
            errors.append(f"target_ack_manifest_mismatch:{target_id}")
        if acknowledgement.get("target_id") != target_id or acknowledgement.get("durable") is not True:
            errors.append(f"target_ack_invalid:{target_id}")
        if run_result.get("manifest_sha256") != manifest_digest:
            errors.append(f"run_manifest_mismatch:{target_id}")
        manifests.append(manifest)
    if manifests:
        first_digest = json_digest(manifests[0])
        if any(json_digest(item) != first_digest for item in manifests[1:]):
            errors.append("target_manifests_diverge")
        manifest = manifests[0]
        if manifest.get("plan_digest") != plan.digest:
            errors.append("manifest_plan_digest_mismatch")
        if manifest.get("lifecycle_state") != "assembled":
            errors.append("manifest_not_assembled")
        inventory = manifest.get("members")
        if not isinstance(inventory, list):
            errors.append("manifest_inventory_invalid")
            inventory = []
        inventory_by_id = {
            item.get("backup_id"): item
            for item in inventory
            if isinstance(item, dict) and isinstance(item.get("backup_id"), str)
        }
        if set(inventory_by_id) != set(plan.members):
            errors.append("inventory_incomplete")
        for backup_id, member in plan.members.items():
            item = inventory_by_id.get(backup_id)
            if not isinstance(item, dict):
                continue
            if item.get("owner_id") != member.owner_id or item.get("checkpoint_ref") != member.checkpoint_ref:
                errors.append(f"member_identity_mismatch:{backup_id}")
            if item.get("owner_evidence_ref") != member.owner_evidence_ref:
                errors.append(f"owner_evidence_mismatch:{backup_id}")
            if member.source_kind in {"owner_snapshot", "owner_export"}:
                target = plan.targets[member.target_storage_id]
                payload_path = Path(target.root_path) / "backup-sets" / backup_set_id / "members" / member.relative_path
                try:
                    reject_symlink_chain(payload_path)
                    if payload_path.is_symlink() or not payload_path.is_file():
                        raise ConfigurationError("payload is not a regular file")
                    digest, size = file_digest(payload_path)
                except ConfigurationError as exc:
                    errors.append(f"member_read_failed:{backup_id}:{exc}")
                    continue
                if digest != item.get("sha256") or size != item.get("size_bytes"):
                    errors.append(f"member_integrity_failed:{backup_id}")
        checks.extend(["inventory", "identity", "integrity", "checkpoints", "ownership", "target_acknowledgements"])
        schema, schema_error = _load_schema(canonical_schema_path)
        if schema_error:
            blocked.append(schema_error)
        elif schema is not None:
            validation_errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda error: list(error.path))
            if validation_errors:
                errors.extend(f"canonical_schema:{error.json_path}:{error.message}" for error in validation_errors)
            else:
                checks.append("canonical_backup_set_schema")
    else:
        errors.append("no_manifest_available")
    if errors:
        state = "failed"
        restore_eligible = False
        outcome = "failed"
    elif blocked:
        state = "blocked"
        restore_eligible = False
        outcome = "blocked"
    else:
        state = "verified"
        restore_eligible = True
        outcome = "succeeded"
    report: dict[str, object] = {
        "format": "koa.operations.backup-verification.v1",
        "verification_state": state,
        "restore_eligible": restore_eligible,
        "restore_tested": False,
        "restore_test_required": True,
        "backup_set_id": backup_set_id,
        "operation_id": operation_id,
        "correlation_id": correlation_id,
        "verified_at": clock(),
        "plan_digest": plan.digest,
        "manifest_sha256": run_result.get("manifest_sha256"),
        "checks": sorted(set(checks)),
        "errors": errors,
        "blocking_reasons": blocked,
    }
    evidence_journal.record(
        operation_id=operation_id,
        correlation_id=correlation_id,
        phase="backup_verify",
        outcome=outcome,
        subject_ref=f"backup-set:{backup_set_id}",
        details=report,
    )
    if state != "verified":
        raise BackupVerificationError(f"backup verification {state}", report)
    return report
