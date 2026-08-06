"""Verification of owner-provided storage observations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence


class StorageIntegrity(str, Enum):
    VERIFIED = "verified"
    FAILED = "failed"
    UNKNOWN = "unknown"


class StorageState(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BLOCKED = "blocked"


_STATE_RANK = {StorageState.HEALTHY: 0, StorageState.DEGRADED: 1, StorageState.BLOCKED: 2}


@dataclass(frozen=True, slots=True)
class StorageObservation:
    storage_id: str
    owner_ref: str
    expected_owner_ref: str
    observed_at: datetime
    total_bytes: int
    free_bytes: int
    protected_floor_bytes: int
    recovery_reserve_bytes: int
    mount_available: bool
    expected_writable: bool
    read_only: bool
    integrity: StorageIntegrity
    backup_ready: bool
    release_set_ref: str

    def __post_init__(self) -> None:
        if not self.storage_id or not self.owner_ref or not self.expected_owner_ref or not self.release_set_ref:
            raise ValueError("storage identity, owner and release set are required")
        _require_aware(self.observed_at, "observed_at")
        values = (self.total_bytes, self.free_bytes, self.protected_floor_bytes, self.recovery_reserve_bytes)
        if any(value < 0 for value in values):
            raise ValueError("storage byte values cannot be negative")
        if self.free_bytes > self.total_bytes:
            raise ValueError("free_bytes cannot exceed total_bytes")


@dataclass(frozen=True, slots=True)
class StorageDomainResult:
    storage_id: str
    owner_ref: str
    state: StorageState
    reason_codes: tuple[str, ...]
    observed_at: str
    release_set_ref: str
    free_bytes: int
    protected_floor_bytes: int
    recovery_reserve_bytes: int


@dataclass(frozen=True, slots=True)
class StorageVerificationReport:
    generated_at: str
    state: StorageState
    domains: tuple[StorageDomainResult, ...]
    reason_codes: tuple[str, ...]
    authoritative: bool = False


def verify_storage(
    observations: Sequence[StorageObservation],
    *,
    now: datetime,
    max_age_seconds: int,
    minimum_recovery_reserve_bytes: int,
) -> StorageVerificationReport:
    """Verify bounded observations without acquiring direct storage authority."""

    _require_aware(now, "now")
    if max_age_seconds <= 0 or minimum_recovery_reserve_bytes < 0:
        raise ValueError("verification bounds are invalid")
    ids: set[str] = set()
    results: list[StorageDomainResult] = []
    global_reasons: set[str] = set()
    for item in sorted(observations, key=lambda value: value.storage_id):
        if item.storage_id in ids:
            raise ValueError(f"duplicate storage observation: {item.storage_id}")
        ids.add(item.storage_id)
        reasons: set[str] = set()
        state = StorageState.HEALTHY
        age = (now - item.observed_at).total_seconds()
        if age < 0 or age > max_age_seconds:
            reasons.add("observation_stale")
            state = StorageState.BLOCKED
        if item.owner_ref != item.expected_owner_ref:
            reasons.add("owner_mismatch")
            state = StorageState.BLOCKED
        if not item.mount_available:
            reasons.add("mount_unavailable")
            state = StorageState.BLOCKED
        if item.integrity is StorageIntegrity.FAILED:
            reasons.add("integrity_failed")
            state = StorageState.BLOCKED
        elif item.integrity is StorageIntegrity.UNKNOWN:
            reasons.add("integrity_unknown")
            state = StorageState.BLOCKED
        if item.free_bytes < item.protected_floor_bytes:
            reasons.add("protected_floor_breached")
            state = StorageState.BLOCKED
        if item.recovery_reserve_bytes < minimum_recovery_reserve_bytes:
            reasons.add("recovery_reserve_insufficient")
            state = StorageState.BLOCKED
        if item.expected_writable and item.read_only and state is not StorageState.BLOCKED:
            reasons.add("unexpected_read_only")
            state = StorageState.DEGRADED
        if not item.backup_ready and state is StorageState.HEALTHY:
            reasons.add("backup_not_ready")
            state = StorageState.DEGRADED
        global_reasons.update(reasons)
        results.append(
            StorageDomainResult(
                storage_id=item.storage_id,
                owner_ref=item.owner_ref,
                state=state,
                reason_codes=tuple(sorted(reasons)),
                observed_at=item.observed_at.astimezone(timezone.utc).isoformat(),
                release_set_ref=item.release_set_ref,
                free_bytes=item.free_bytes,
                protected_floor_bytes=item.protected_floor_bytes,
                recovery_reserve_bytes=item.recovery_reserve_bytes,
            )
        )
    overall = max((item.state for item in results), key=lambda state: _STATE_RANK[state], default=StorageState.BLOCKED)
    if not results:
        global_reasons.add("storage_observation_missing")
    return StorageVerificationReport(
        generated_at=now.astimezone(timezone.utc).isoformat(),
        state=overall,
        domains=tuple(results),
        reason_codes=tuple(sorted(global_reasons)),
    )


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
