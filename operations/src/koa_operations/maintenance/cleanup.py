"""Bounded cleanup planning through owner-authorized operations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from hashlib import sha256
from typing import Callable, Sequence
import json


class CleanupCategory(str, Enum):
    REPRODUCIBLE_CACHE = "reproducible_cache"
    DERIVATIVE = "derivative"
    STAGING = "staging"
    TEMPORARY_DIAGNOSTIC = "temporary_diagnostic"
    AUTHORITATIVE_DATA = "authoritative_data"
    ORIGINAL = "original"
    ACTIVE_RELEASE_METADATA = "active_release_metadata"
    MANIFEST = "manifest"
    RECEIPT = "receipt"
    EVIDENCE = "evidence"
    RECOVERY_MATERIAL = "recovery_material"
    BACKUP = "backup"


_REMOVABLE = {
    CleanupCategory.REPRODUCIBLE_CACHE,
    CleanupCategory.DERIVATIVE,
    CleanupCategory.STAGING,
    CleanupCategory.TEMPORARY_DIAGNOSTIC,
}
_PROTECTED = set(CleanupCategory) - _REMOVABLE


@dataclass(frozen=True, slots=True)
class CleanupCandidate:
    object_ref: str
    owner_ref: str
    category: CleanupCategory
    size_bytes: int
    created_at: datetime
    owner_authorized: bool
    reproducible: bool
    active: bool = False
    legal_hold: bool = False
    retention_expired: bool = True

    def __post_init__(self) -> None:
        if not self.object_ref or not self.owner_ref:
            raise ValueError("object and owner references are required")
        if self.size_bytes < 0:
            raise ValueError("size_bytes cannot be negative")
        _require_aware(self.created_at, "created_at")


@dataclass(frozen=True, slots=True)
class CleanupPolicy:
    policy_id: str
    allowed_categories: tuple[CleanupCategory, ...]
    max_items: int
    max_bytes: int
    min_age: timedelta
    valid_until: datetime
    resource_admission_ref: str

    def __post_init__(self) -> None:
        if not self.policy_id or not self.resource_admission_ref:
            raise ValueError("policy and resource admission references are required")
        if not self.allowed_categories or not set(self.allowed_categories).issubset(_REMOVABLE):
            raise ValueError("cleanup policy can allow only removable categories")
        if not 1 <= self.max_items <= 10_000 or not 1 <= self.max_bytes <= 10 * 1024**4:
            raise ValueError("cleanup bounds are invalid")
        if self.min_age.total_seconds() < 0:
            raise ValueError("min_age cannot be negative")
        _require_aware(self.valid_until, "valid_until")


@dataclass(frozen=True, slots=True)
class RejectedCleanupCandidate:
    object_ref: str
    reason_code: str


@dataclass(frozen=True, slots=True)
class CleanupPlan:
    plan_id: str
    policy_id: str
    created_at: str
    valid_until: str
    resource_admission_ref: str
    selected: tuple[CleanupCandidate, ...]
    rejected: tuple[RejectedCleanupCandidate, ...]
    selected_bytes: int
    max_items: int
    max_bytes: int


@dataclass(frozen=True, slots=True)
class CleanupItemResult:
    object_ref: str
    owner_ref: str
    outcome: str
    reason_code: str


@dataclass(frozen=True, slots=True)
class CleanupExecutionResult:
    plan_id: str
    completed_at: str
    items: tuple[CleanupItemResult, ...]
    removed_items: int
    removed_bytes: int
    terminal_state: str


def plan_cleanup(candidates: Sequence[CleanupCandidate], policy: CleanupPolicy, *, now: datetime) -> CleanupPlan:
    _require_aware(now, "now")
    if now > policy.valid_until:
        raise ValueError("cleanup policy has expired")
    selected: list[CleanupCandidate] = []
    rejected: list[RejectedCleanupCandidate] = []
    selected_bytes = 0

    for candidate in sorted(candidates, key=lambda item: (item.created_at, item.object_ref)):
        reason = _rejection_reason(candidate, policy, now)
        if reason:
            rejected.append(RejectedCleanupCandidate(candidate.object_ref, reason))
            continue
        if len(selected) >= policy.max_items:
            rejected.append(RejectedCleanupCandidate(candidate.object_ref, "item_limit_reached"))
            continue
        if selected_bytes + candidate.size_bytes > policy.max_bytes:
            rejected.append(RejectedCleanupCandidate(candidate.object_ref, "byte_limit_reached"))
            continue
        selected.append(candidate)
        selected_bytes += candidate.size_bytes

    seed = {
        "policy_id": policy.policy_id,
        "created_at": now.astimezone(timezone.utc).isoformat(),
        "selected": [item.object_ref for item in selected],
        "selected_bytes": selected_bytes,
    }
    plan_id = "cleanup:" + sha256(json.dumps(seed, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return CleanupPlan(
        plan_id=plan_id,
        policy_id=policy.policy_id,
        created_at=now.astimezone(timezone.utc).isoformat(),
        valid_until=policy.valid_until.astimezone(timezone.utc).isoformat(),
        resource_admission_ref=policy.resource_admission_ref,
        selected=tuple(selected),
        rejected=tuple(rejected),
        selected_bytes=selected_bytes,
        max_items=policy.max_items,
        max_bytes=policy.max_bytes,
    )


def execute_cleanup(
    plan: CleanupPlan,
    *,
    delete_through_owner: Callable[[CleanupCandidate], bool],
    now: datetime,
) -> CleanupExecutionResult:
    """Execute only the immutable plan through the owner's declared operation."""

    _require_aware(now, "now")
    if now > datetime.fromisoformat(plan.valid_until):
        raise ValueError("cleanup plan has expired")
    if len(plan.selected) > plan.max_items or plan.selected_bytes > plan.max_bytes:
        raise ValueError("cleanup plan violates its own bounds")

    results: list[CleanupItemResult] = []
    removed_bytes = 0
    for candidate in plan.selected:
        if candidate.category in _PROTECTED:
            raise ValueError("protected category appeared in executable cleanup plan")
        try:
            removed = bool(delete_through_owner(candidate))
        except Exception:
            results.append(CleanupItemResult(candidate.object_ref, candidate.owner_ref, "failed", "owner_operation_failed"))
            break
        if not removed:
            results.append(CleanupItemResult(candidate.object_ref, candidate.owner_ref, "failed", "owner_operation_rejected"))
            break
        results.append(CleanupItemResult(candidate.object_ref, candidate.owner_ref, "removed", "owner_operation_confirmed"))
        removed_bytes += candidate.size_bytes

    complete = len(results) == len(plan.selected) and all(item.outcome == "removed" for item in results)
    return CleanupExecutionResult(
        plan_id=plan.plan_id,
        completed_at=now.astimezone(timezone.utc).isoformat(),
        items=tuple(results),
        removed_items=sum(item.outcome == "removed" for item in results),
        removed_bytes=removed_bytes,
        terminal_state="completed" if complete else "incomplete",
    )


def _rejection_reason(candidate: CleanupCandidate, policy: CleanupPolicy, now: datetime) -> str | None:
    if candidate.category in _PROTECTED:
        return "protected_category"
    if candidate.category not in policy.allowed_categories:
        return "category_not_allowed"
    if not candidate.owner_authorized:
        return "owner_authority_missing"
    if candidate.active:
        return "object_active"
    if candidate.legal_hold:
        return "legal_hold"
    if not candidate.retention_expired:
        return "retention_not_expired"
    if candidate.category in {CleanupCategory.REPRODUCIBLE_CACHE, CleanupCategory.DERIVATIVE} and not candidate.reproducible:
        return "reproducibility_not_proven"
    if now - candidate.created_at < policy.min_age:
        return "minimum_age_not_met"
    return None


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
