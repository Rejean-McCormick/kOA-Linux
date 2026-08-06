from __future__ import annotations

from datetime import datetime, timedelta, timezone
import pytest

from koa_operations.maintenance import (
    CleanupCandidate,
    CleanupCategory,
    CleanupPolicy,
    ReceiptRotationPolicy,
    ReceiptSegment,
    StorageIntegrity,
    StorageObservation,
    StorageState,
    execute_cleanup,
    execute_receipt_rotation,
    plan_cleanup,
    plan_receipt_rotation,
    verify_storage,
)

NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)
DIGEST = "a" * 64


def cleanup_policy(max_items=2, max_bytes=1000):
    return CleanupPolicy(
        policy_id="cleanup.v1",
        allowed_categories=(CleanupCategory.REPRODUCIBLE_CACHE, CleanupCategory.DERIVATIVE),
        max_items=max_items,
        max_bytes=max_bytes,
        min_age=timedelta(hours=1),
        valid_until=NOW + timedelta(hours=1),
        resource_admission_ref="resource-admission:cleanup-001",
    )


def candidate(ref, category=CleanupCategory.REPRODUCIBLE_CACHE, size=100, **overrides):
    values = {
        "object_ref": ref,
        "owner_ref": "component:media",
        "category": category,
        "size_bytes": size,
        "created_at": NOW - timedelta(days=2),
        "owner_authorized": True,
        "reproducible": True,
    }
    values.update(overrides)
    return CleanupCandidate(**values)


def test_cleanup_protects_authoritative_receipts_evidence_and_recovery_material():
    items = [
        candidate("cache:1"),
        candidate("data:1", CleanupCategory.AUTHORITATIVE_DATA),
        candidate("receipt:1", CleanupCategory.RECEIPT),
        candidate("evidence:1", CleanupCategory.EVIDENCE),
        candidate("recovery:1", CleanupCategory.RECOVERY_MATERIAL),
    ]
    plan = plan_cleanup(items, cleanup_policy(), now=NOW)
    assert [item.object_ref for item in plan.selected] == ["cache:1"]
    rejected = dict((item.object_ref, item.reason_code) for item in plan.rejected)
    assert rejected["data:1"] == "protected_category"
    assert rejected["receipt:1"] == "protected_category"
    assert rejected["evidence:1"] == "protected_category"
    assert rejected["recovery:1"] == "protected_category"


def test_cleanup_is_owner_authorized_reproducible_and_bounded():
    items = [
        candidate("cache:1", size=400),
        candidate("cache:2", size=400),
        candidate("cache:3", size=400),
        candidate("cache:no-owner", owner_authorized=False),
        candidate("cache:not-reproducible", reproducible=False),
        candidate("cache:active", active=True),
    ]
    plan = plan_cleanup(items, cleanup_policy(max_items=2, max_bytes=800), now=NOW)
    assert len(plan.selected) == 2
    assert plan.selected_bytes == 800
    reasons = {item.reason_code for item in plan.rejected}
    assert {"item_limit_reached", "owner_authority_missing", "reproducibility_not_proven", "object_active"} <= reasons


def test_cleanup_executes_only_selected_owner_operations_and_stops_on_failure():
    plan = plan_cleanup([candidate("cache:1"), candidate("cache:2")], cleanup_policy(), now=NOW)
    called = []

    def owner_delete(item):
        called.append(item.object_ref)
        return item.object_ref != "cache:2"

    result = execute_cleanup(plan, delete_through_owner=owner_delete, now=NOW)
    assert called == ["cache:1", "cache:2"]
    assert result.terminal_state == "incomplete"
    assert result.removed_items == 1


def test_expired_cleanup_plan_is_rejected():
    plan = plan_cleanup([candidate("cache:1")], cleanup_policy(), now=NOW)
    with pytest.raises(ValueError, match="expired"):
        execute_cleanup(plan, delete_through_owner=lambda item: True, now=NOW + timedelta(hours=2))


def segment(ref, **overrides):
    values = {
        "segment_id": ref,
        "owner_ref": "component:audit-broker",
        "opened_at": NOW - timedelta(days=10),
        "closed_at": NOW - timedelta(days=9),
        "receipt_count": 100,
        "size_bytes": 200,
        "sha256": DIGEST,
        "active": False,
        "legal_hold": False,
        "archived": False,
        "retention_until": NOW - timedelta(days=1),
    }
    values.update(overrides)
    return ReceiptSegment(**values)


def rotation_policy():
    return ReceiptRotationPolicy(
        policy_id="receipt-rotation.v1",
        archive_owner_ref="archive:audit-broker",
        max_segments=2,
        max_bytes=500,
        min_closed_age=timedelta(days=1),
        valid_until=NOW + timedelta(hours=1),
        resource_admission_ref="resource-admission:rotation-001",
    )


def test_receipt_rotation_never_selects_active_or_held_segments():
    plan = plan_receipt_rotation(
        [
            segment("segment:ok"),
            segment("segment:active", active=True, closed_at=None),
            segment("segment:hold", legal_hold=True),
            segment("segment:retained", retention_until=NOW + timedelta(days=1)),
        ],
        rotation_policy(),
        now=NOW,
    )
    assert [item.segment_id for item in plan.selected] == ["segment:ok", "segment:retained"]
    assert plan.destructive_deletion_allowed is False
    assert {reason for _, reason in plan.rejected} == {"segment_active", "legal_hold"}


def test_receipt_rotation_archives_through_owner_and_preserves_sources():
    plan = plan_receipt_rotation([segment("segment:1"), segment("segment:2")], rotation_policy(), now=NOW)
    calls = []

    def archive(item, owner):
        calls.append((item.segment_id, owner))
        return True

    result = execute_receipt_rotation(plan, seal_and_archive_through_owner=archive, now=NOW)
    assert result.terminal_state == "completed"
    assert result.source_segments_preserved is True
    assert calls == [("segment:1", "archive:audit-broker"), ("segment:2", "archive:audit-broker")]


def observation(storage_id="storage:main", **overrides):
    values = {
        "storage_id": storage_id,
        "owner_ref": "component:media",
        "expected_owner_ref": "component:media",
        "observed_at": NOW,
        "total_bytes": 10_000,
        "free_bytes": 4_000,
        "protected_floor_bytes": 2_000,
        "recovery_reserve_bytes": 1_000,
        "mount_available": True,
        "expected_writable": True,
        "read_only": False,
        "integrity": StorageIntegrity.VERIFIED,
        "backup_ready": True,
        "release_set_ref": "release-set:abc",
    }
    values.update(overrides)
    return StorageObservation(**values)


def test_storage_verification_distinguishes_healthy_degraded_and_blocked():
    healthy = verify_storage((observation(),), now=NOW, max_age_seconds=60, minimum_recovery_reserve_bytes=500)
    assert healthy.state is StorageState.HEALTHY
    assert healthy.authoritative is False

    degraded = verify_storage(
        (observation(backup_ready=False),), now=NOW, max_age_seconds=60, minimum_recovery_reserve_bytes=500
    )
    assert degraded.state is StorageState.DEGRADED
    assert "backup_not_ready" in degraded.reason_codes

    blocked = verify_storage(
        (observation(free_bytes=100, integrity=StorageIntegrity.UNKNOWN),),
        now=NOW,
        max_age_seconds=60,
        minimum_recovery_reserve_bytes=500,
    )
    assert blocked.state is StorageState.BLOCKED
    assert {"protected_floor_breached", "integrity_unknown"} <= set(blocked.reason_codes)


def test_storage_owner_mismatch_and_stale_observation_fail_closed():
    report = verify_storage(
        (observation(owner_ref="component:wrong", observed_at=NOW - timedelta(minutes=5)),),
        now=NOW,
        max_age_seconds=60,
        minimum_recovery_reserve_bytes=500,
    )
    assert report.state is StorageState.BLOCKED
    assert {"owner_mismatch", "observation_stale"} <= set(report.reason_codes)


def test_no_storage_observation_is_blocked():
    report = verify_storage((), now=NOW, max_age_seconds=60, minimum_recovery_reserve_bytes=500)
    assert report.state is StorageState.BLOCKED
    assert report.reason_codes == ("storage_observation_missing",)
