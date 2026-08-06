"""Bounded execution of owner-produced backup members."""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
import time
from pathlib import Path
from typing import Callable, Mapping

from ..config import ConfigurationError, ensure_directory, json_digest, reject_symlink_chain, write_json_atomic
from ..evidence import EvidenceJournal, utc_now
from .plan import BackupPlan, MemberSpec


class BackupExecutionError(RuntimeError):
    """Raised with an explicit result when a backup cannot complete."""

    def __init__(self, message: str, result: Mapping[str, object]) -> None:
        super().__init__(message)
        self.result = dict(result)


def _open_regular_no_follow(path: Path) -> tuple[int, os.stat_result]:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError as exc:
        raise BackupExecutionError(
            f"cannot open owner-produced backup member {path}: {exc}",
            {"execution_state": "failed", "reason_code": "source_open_failed"},
        ) from exc
    metadata = os.fstat(fd)
    if not stat.S_ISREG(metadata.st_mode):
        os.close(fd)
        raise BackupExecutionError(
            f"backup member must be a regular file: {path}",
            {"execution_state": "failed", "reason_code": "source_not_regular"},
        )
    return fd, metadata


def _copy_member(
    member: MemberSpec,
    destination: Path,
    *,
    deadline: float,
    total_budget: list[int],
    max_total_bytes: int,
) -> dict[str, object]:
    if member.source_kind in {"immutable_reference", "regenerable"}:
        return {
            "backup_id": member.backup_id,
            "owner_id": member.owner_id,
            "data_class": member.data_class,
            "target_id": member.target_storage_id,
            "member_kind": member.source_kind,
            "relative_path": member.relative_path,
            "source_ref": member.source_ref,
            "sha256": member.expected_sha256,
            "size_bytes": 0,
            "checkpoint_ref": member.checkpoint_ref,
            "owner_evidence_ref": member.owner_evidence_ref,
            "classification": member.classification,
            "audience_refs": list(member.audience_refs),
            "provenance_ref": member.provenance_ref,
            "restore_after": list(member.restore_after),
            "required": member.required,
        }
    source = Path(member.source_path or "")
    reject_symlink_chain(source.parent)
    if source.is_symlink():
        raise BackupExecutionError(
            f"symlink backup member is forbidden: {source}",
            {"execution_state": "failed", "reason_code": "source_symlink"},
        )
    fd, metadata = _open_regular_no_follow(source)
    try:
        if total_budget[0] + metadata.st_size > max_total_bytes:
            raise BackupExecutionError(
                "backup size exceeds the declared plan limit",
                {"execution_state": "failed", "reason_code": "size_limit_exceeded"},
            )
        ensure_directory(destination.parent)
        if destination.exists() or destination.is_symlink():
            raise BackupExecutionError(
                f"duplicate or pre-existing staged member: {destination}",
                {"execution_state": "failed", "reason_code": "staging_collision"},
            )
        output_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        output_fd = os.open(destination, output_flags, 0o600)
        digest = hashlib.sha256()
        copied = 0
        try:
            while True:
                if time.monotonic() > deadline:
                    raise BackupExecutionError(
                        "backup execution exceeded max_duration_seconds",
                        {"execution_state": "failed", "reason_code": "deadline_exceeded"},
                    )
                chunk = os.read(fd, 1024 * 1024)
                if not chunk:
                    break
                view = memoryview(chunk)
                while view:
                    written = os.write(output_fd, view)
                    if written <= 0:
                        raise BackupExecutionError(
                            "backup target stopped accepting data",
                            {"execution_state": "failed", "reason_code": "target_write_failed"},
                        )
                    view = view[written:]
                digest.update(chunk)
                copied += len(chunk)
            os.fsync(output_fd)
        finally:
            os.close(output_fd)
        final_metadata = os.fstat(fd)
        if (
            copied != metadata.st_size
            or final_metadata.st_size != metadata.st_size
            or final_metadata.st_mtime_ns != metadata.st_mtime_ns
            or final_metadata.st_ino != metadata.st_ino
        ):
            destination.unlink(missing_ok=True)
            raise BackupExecutionError(
                f"source changed while being copied: {source}",
                {"execution_state": "failed", "reason_code": "source_changed"},
            )
        actual = digest.hexdigest()
        if member.expected_sha256 is not None and actual != member.expected_sha256:
            destination.unlink(missing_ok=True)
            raise BackupExecutionError(
                f"source digest mismatch for {member.backup_id}",
                {"execution_state": "failed", "reason_code": "source_digest_mismatch"},
            )
        total_budget[0] += copied
        return {
            "backup_id": member.backup_id,
            "owner_id": member.owner_id,
            "data_class": member.data_class,
            "target_id": member.target_storage_id,
            "member_kind": member.source_kind,
            "relative_path": member.relative_path,
            "source_ref": None,
            "sha256": actual,
            "size_bytes": copied,
            "checkpoint_ref": member.checkpoint_ref,
            "owner_evidence_ref": member.owner_evidence_ref,
            "classification": member.classification,
            "audience_refs": list(member.audience_refs),
            "provenance_ref": member.provenance_ref,
            "restore_after": list(member.restore_after),
            "required": member.required,
        }
    finally:
        os.close(fd)


def run_backup(
    plan: BackupPlan,
    *,
    evidence_journal: EvidenceJournal,
    clock: Callable[[], str] = utc_now,
) -> dict[str, object]:
    started_at = clock()
    deadline = time.monotonic() + int(plan.payload["limits"]["max_duration_seconds"])  # type: ignore[index]
    backup_set_id = str(plan.payload["backup_set_id"])
    operation_id = str(plan.payload["operation_id"])
    correlation_id = str(plan.payload["correlation_id"])
    staging: dict[str, Path] = {}
    finals: dict[str, Path] = {}
    committed: list[str] = []
    inventory: list[dict[str, object]] = []
    total_budget = [0]
    try:
        for target in plan.targets.values():
            root = Path(target.root_path)
            ensure_directory(root)
            reject_symlink_chain(root)
            staging_root = root / ".koa-backup-staging" / f"{backup_set_id}-{operation_id}"
            final_root = root / "backup-sets" / backup_set_id
            if final_root.exists() or final_root.is_symlink():
                raise BackupExecutionError(
                    f"refusing to replace existing backup set at {target.target_id}",
                    {"execution_state": "failed", "reason_code": "backup_set_exists"},
                )
            if staging_root.exists():
                raise BackupExecutionError(
                    f"staging path already exists at {target.target_id}",
                    {"execution_state": "failed", "reason_code": "staging_exists"},
                )
            ensure_directory(staging_root / "members")
            staging[target.target_id] = staging_root
            finals[target.target_id] = final_root
        for backup_id in plan.restore_order:
            member = plan.members[backup_id]
            destination = staging[member.target_storage_id] / "members" / member.relative_path
            inventory.append(
                _copy_member(
                    member,
                    destination,
                    deadline=deadline,
                    total_budget=total_budget,
                    max_total_bytes=int(plan.payload["limits"]["max_total_bytes"]),  # type: ignore[index]
                )
            )
        finished_at = clock()
        manifest: dict[str, object] = {
            "format": "koa.operations.backup-manifest.v1",
            "$schema": plan.payload["canonical_schema_ref"],
            "backup_set_id": backup_set_id,
            "operation_id": operation_id,
            "correlation_id": correlation_id,
            "lifecycle_state": "assembled",
            "created_at": plan.payload["created_at"],
            "started_at": started_at,
            "finished_at": finished_at,
            "tenant_id": plan.payload["tenant_id"],
            "environment_id": plan.payload["environment_id"],
            "profile_id": plan.payload["profile_id"],
            "authority_scope_ref": plan.payload["authority_scope_ref"],
            "policy_decision_ref": plan.payload["policy_decision_ref"],
            "release_context": plan.payload["release_context"],
            "objectives": plan.payload["objectives"],
            "encryption": plan.payload["encryption"],
            "plan_digest": plan.digest,
            "assembly_plan_digest": plan.payload["assembly_plan_digest"],
            "restore_order": list(plan.restore_order),
            "members": sorted(inventory, key=lambda item: str(item["backup_id"])),
            "targets": [
                {
                    "target_id": target.target_id,
                    "independent": target.independent,
                    "offline": target.offline,
                    "immutable": target.immutable,
                    "protected": target.protected,
                    "encryption_context_ref": target.encryption_context_ref,
                    "retention_policy_ref": target.retention_policy_ref,
                }
                for target in plan.targets.values()
            ],
            "total_size_bytes": total_budget[0],
            "restore_test_required": True,
            "restore_tested": False,
        }
        manifest_digest = json_digest(manifest)
        for target_id, stage in staging.items():
            write_json_atomic(stage / "backup-manifest.json", manifest)
            acknowledgement = {
                "format": "koa.operations.backup-target-ack.v1",
                "backup_set_id": backup_set_id,
                "target_id": target_id,
                "manifest_sha256": manifest_digest,
                "acknowledged_at": finished_at,
                "durable": True,
            }
            write_json_atomic(stage / "target-ack.json", acknowledgement)
        for target_id in sorted(staging):
            final = finals[target_id]
            ensure_directory(final.parent)
            os.replace(staging[target_id], final)
            committed.append(target_id)
        result: dict[str, object] = {
            "format": "koa.operations.backup-run-result.v1",
            "execution_state": "completed",
            "backup_set_id": backup_set_id,
            "operation_id": operation_id,
            "correlation_id": correlation_id,
            "started_at": started_at,
            "finished_at": finished_at,
            "plan_digest": plan.digest,
            "manifest_sha256": manifest_digest,
            "committed_targets": committed,
            "failed_targets": [],
            "total_size_bytes": total_budget[0],
        }
        evidence_journal.record(
            operation_id=operation_id,
            correlation_id=correlation_id,
            phase="backup_run",
            outcome="succeeded",
            subject_ref=f"backup-set:{backup_set_id}",
            details=result,
        )
        return result
    except (BackupExecutionError, ConfigurationError, OSError) as exc:
        reason = exc.result.get("reason_code") if isinstance(exc, BackupExecutionError) else "execution_error"
        for target_id, stage in staging.items():
            if target_id not in committed and stage.exists():
                shutil.rmtree(stage, ignore_errors=True)
        failed_targets = sorted(set(plan.targets) - set(committed))
        result = {
            "format": "koa.operations.backup-run-result.v1",
            "execution_state": "failed",
            "reason_code": reason,
            "message": str(exc),
            "backup_set_id": backup_set_id,
            "operation_id": operation_id,
            "correlation_id": correlation_id,
            "started_at": started_at,
            "finished_at": clock(),
            "plan_digest": plan.digest,
            "committed_targets": committed,
            "failed_targets": failed_targets,
            "previous_verified_backup_preserved": True,
        }
        evidence_journal.record(
            operation_id=operation_id,
            correlation_id=correlation_id,
            phase="backup_run",
            outcome="failed",
            subject_ref=f"backup-set:{backup_set_id}",
            details=result,
        )
        raise BackupExecutionError(str(exc), result) from exc
