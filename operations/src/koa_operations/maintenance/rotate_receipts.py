"""Bounded sealing and archival of immutable receipt segments."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Callable, Sequence
import json
import re

_DIGEST = re.compile(r"^[a-f0-9]{64}$")


@dataclass(frozen=True, slots=True)
class ReceiptSegment:
    segment_id: str
    owner_ref: str
    opened_at: datetime
    closed_at: datetime | None
    receipt_count: int
    size_bytes: int
    sha256: str
    active: bool
    legal_hold: bool
    archived: bool
    retention_until: datetime

    def __post_init__(self) -> None:
        if not self.segment_id or not self.owner_ref:
            raise ValueError("segment and owner references are required")
        _require_aware(self.opened_at, "opened_at")
        _require_aware(self.retention_until, "retention_until")
        if self.closed_at is not None:
            _require_aware(self.closed_at, "closed_at")
            if self.closed_at < self.opened_at:
                raise ValueError("closed_at cannot precede opened_at")
        if self.receipt_count < 0 or self.size_bytes < 0:
            raise ValueError("receipt counts and sizes cannot be negative")
        if not _DIGEST.fullmatch(self.sha256):
            raise ValueError("segment sha256 must be explicit")


@dataclass(frozen=True, slots=True)
class ReceiptRotationPolicy:
    policy_id: str
    archive_owner_ref: str
    max_segments: int
    max_bytes: int
    min_closed_age: timedelta
    valid_until: datetime
    resource_admission_ref: str

    def __post_init__(self) -> None:
        if not self.policy_id or not self.archive_owner_ref or not self.resource_admission_ref:
            raise ValueError("policy, archive owner and resource admission are required")
        if not 1 <= self.max_segments <= 10_000 or not 1 <= self.max_bytes <= 10 * 1024**4:
            raise ValueError("rotation bounds are invalid")
        if self.min_closed_age.total_seconds() < 0:
            raise ValueError("min_closed_age cannot be negative")
        _require_aware(self.valid_until, "valid_until")


@dataclass(frozen=True, slots=True)
class ReceiptRotationPlan:
    plan_id: str
    policy_id: str
    archive_owner_ref: str
    selected: tuple[ReceiptSegment, ...]
    rejected: tuple[tuple[str, str], ...]
    selected_bytes: int
    valid_until: str
    resource_admission_ref: str
    destructive_deletion_allowed: bool = False


@dataclass(frozen=True, slots=True)
class ReceiptRotationResult:
    plan_id: str
    completed_at: str
    archived_segment_ids: tuple[str, ...]
    failed_segment_id: str | None
    archived_bytes: int
    terminal_state: str
    source_segments_preserved: bool = True


def plan_receipt_rotation(
    segments: Sequence[ReceiptSegment],
    policy: ReceiptRotationPolicy,
    *,
    now: datetime,
) -> ReceiptRotationPlan:
    """Select closed immutable segments for archival; never plan deletion."""

    _require_aware(now, "now")
    if now > policy.valid_until:
        raise ValueError("receipt rotation policy has expired")
    selected: list[ReceiptSegment] = []
    rejected: list[tuple[str, str]] = []
    selected_bytes = 0
    for segment in sorted(segments, key=lambda item: (item.closed_at or item.opened_at, item.segment_id)):
        reason = _rotation_rejection(segment, policy, now)
        if reason:
            rejected.append((segment.segment_id, reason))
            continue
        if len(selected) >= policy.max_segments:
            rejected.append((segment.segment_id, "segment_limit_reached"))
            continue
        if selected_bytes + segment.size_bytes > policy.max_bytes:
            rejected.append((segment.segment_id, "byte_limit_reached"))
            continue
        selected.append(segment)
        selected_bytes += segment.size_bytes
    seed = {
        "policy_id": policy.policy_id,
        "selected": [(item.segment_id, item.sha256) for item in selected],
        "selected_bytes": selected_bytes,
        "now": now.astimezone(timezone.utc).isoformat(),
    }
    return ReceiptRotationPlan(
        plan_id="receipt-rotation:" + sha256(json.dumps(seed, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        policy_id=policy.policy_id,
        archive_owner_ref=policy.archive_owner_ref,
        selected=tuple(selected),
        rejected=tuple(rejected),
        selected_bytes=selected_bytes,
        valid_until=policy.valid_until.astimezone(timezone.utc).isoformat(),
        resource_admission_ref=policy.resource_admission_ref,
    )


def execute_receipt_rotation(
    plan: ReceiptRotationPlan,
    *,
    seal_and_archive_through_owner: Callable[[ReceiptSegment, str], bool],
    now: datetime,
) -> ReceiptRotationResult:
    _require_aware(now, "now")
    if now > datetime.fromisoformat(plan.valid_until):
        raise ValueError("receipt rotation plan has expired")
    if plan.destructive_deletion_allowed:
        raise ValueError("receipt rotation cannot authorize destructive deletion")

    archived: list[str] = []
    archived_bytes = 0
    failed: str | None = None
    for segment in plan.selected:
        if segment.active or segment.closed_at is None or segment.legal_hold:
            raise ValueError("unsafe receipt segment appeared in executable plan")
        try:
            accepted = bool(seal_and_archive_through_owner(segment, plan.archive_owner_ref))
        except Exception:
            accepted = False
        if not accepted:
            failed = segment.segment_id
            break
        archived.append(segment.segment_id)
        archived_bytes += segment.size_bytes
    return ReceiptRotationResult(
        plan_id=plan.plan_id,
        completed_at=now.astimezone(timezone.utc).isoformat(),
        archived_segment_ids=tuple(archived),
        failed_segment_id=failed,
        archived_bytes=archived_bytes,
        terminal_state="completed" if failed is None and len(archived) == len(plan.selected) else "incomplete",
    )


def _rotation_rejection(segment: ReceiptSegment, policy: ReceiptRotationPolicy, now: datetime) -> str | None:
    if segment.active or segment.closed_at is None:
        return "segment_active"
    if segment.legal_hold:
        return "legal_hold"
    if segment.archived:
        return "already_archived"
    if now - segment.closed_at < policy.min_closed_age:
        return "minimum_age_not_met"
    return None


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
