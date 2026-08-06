from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from koa_assembly.plans import (  # noqa: E402
    BackupItem,
    BackupPlan,
    DependencyCycleError,
    PlanValidationError,
    StorageBoundary,
    StoragePlan,
)


def _storage_plan() -> StoragePlan:
    return StoragePlan(
        [
            StorageBoundary(
                "identity-db",
                "identity-and-trust",
                "authoritative",
                "/var/lib/koa/identity/db",
                writer_owner_ids=("identity-and-trust",),
                encrypted=True,
                backup_policy_id="identity-daily",
            ),
            StorageBoundary(
                "identity-backup",
                "identity-and-trust",
                "backup",
                "/var/backups/koa/identity",
                source_storage_id="identity-db",
                encrypted=True,
            ),
            StorageBoundary(
                "audit-log",
                "audit-broker",
                "audit_or_evidence",
                "/var/lib/koa/audit/evidence",
                writer_owner_ids=("audit-broker",),
                encrypted=True,
                backup_policy_id="audit-daily",
            ),
            StorageBoundary(
                "audit-backup",
                "audit-broker",
                "backup",
                "/var/backups/koa/audit",
                source_storage_id="audit-log",
                encrypted=True,
            ),
            StorageBoundary(
                "identity-cache",
                "identity-and-trust",
                "cache",
                "/var/cache/koa/identity",
                source_storage_id="identity-db",
                persistent=False,
            ),
        ]
    )


def test_storage_plan_preserves_authority_and_backup_restore_order() -> None:
    storage = _storage_plan()
    assert [item.storage_id for item in storage.authoritative_for("identity-and-trust")] == [
        "identity-db"
    ]
    backup = BackupPlan(
        storage,
        [
            BackupItem(
                "identity-backup-job",
                "identity-db",
                "identity-backup",
                "identity-and-trust",
                "snapshot",
                "application_consistent",
                offline_copy_required=True,
            ),
            BackupItem(
                "audit-backup-job",
                "audit-log",
                "audit-backup",
                "audit-broker",
                "logical_export",
                "application_consistent",
                restore_after=("identity-backup-job",),
            ),
        ],
    )
    assert backup.restore_order == ("identity-backup-job", "audit-backup-job")


def test_storage_plan_rejects_authority_transfer_and_overlapping_writes() -> None:
    with pytest.raises(PlanValidationError, match="changes owner"):
        StoragePlan(
            [
                StorageBoundary(
                    "source",
                    "owner-a",
                    "authoritative",
                    "/var/lib/koa/source",
                    writer_owner_ids=("owner-a",),
                ),
                StorageBoundary(
                    "replica",
                    "owner-b",
                    "replica",
                    "/var/lib/koa/replica",
                    source_storage_id="source",
                ),
            ]
        )

    with pytest.raises(PlanValidationError, match="overlapping writable storage"):
        StoragePlan(
            [
                StorageBoundary(
                    "one",
                    "owner-a",
                    "authoritative",
                    "/var/lib/koa/shared",
                    writer_owner_ids=("owner-a",),
                ),
                StorageBoundary(
                    "two",
                    "owner-b",
                    "authoritative",
                    "/var/lib/koa/shared/nested",
                    writer_owner_ids=("owner-b",),
                ),
            ]
        )


def test_storage_plan_rejects_non_owner_authoritative_writer() -> None:
    with pytest.raises(PlanValidationError, match="exactly its owner as writer"):
        StorageBoundary(
            "identity-db",
            "identity-and-trust",
            "authoritative",
            "/var/lib/koa/identity",
            writer_owner_ids=("identity-and-trust", "audit-broker"),
        )


def test_backup_plan_requires_coverage_and_acyclic_restore() -> None:
    storage = _storage_plan()
    with pytest.raises(PlanValidationError, match="missing backup coverage"):
        BackupPlan(
            storage,
            [
                BackupItem(
                    "identity-only",
                    "identity-db",
                    "identity-backup",
                    "identity-and-trust",
                    "snapshot",
                    "application_consistent",
                )
            ],
        )

    with pytest.raises(DependencyCycleError):
        BackupPlan(
            storage,
            [
                BackupItem(
                    "identity-job",
                    "identity-db",
                    "identity-backup",
                    "identity-and-trust",
                    "snapshot",
                    "application_consistent",
                    restore_after=("audit-job",),
                ),
                BackupItem(
                    "audit-job",
                    "audit-log",
                    "audit-backup",
                    "audit-broker",
                    "logical_export",
                    "application_consistent",
                    restore_after=("identity-job",),
                ),
            ],
        )
