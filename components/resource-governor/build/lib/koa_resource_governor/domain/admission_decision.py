"""Deterministic Resource Governor admission outcomes."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Iterable

from .resource_envelope import ResourceLimit


class AdmissionOutcome(str, Enum):
    """Canonical outcomes of ``RG-IF-003``."""

    ADMITTED = "admitted"
    QUEUED = "queued"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    BLOCKED = "blocked"


def _required(name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _optional(name: str, value: str | None) -> str | None:
    if value is None:
        return None
    return _required(name, value)


def _instant(name: str, value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _refs(name: str, values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({_required(name, value) for value in values}))


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    """Immutable resource decision for a previously identified request."""

    decision_id: str
    request_id: str
    outcome: AdmissionOutcome
    resolved_envelope_refs: tuple[str, ...]
    decision_reason: str
    reason_codes: tuple[str, ...]
    decided_at: datetime
    effective_limits: tuple[ResourceLimit, ...] = ()
    queue_item_ref: str | None = None
    retry_after: timedelta | None = None
    receipt_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        outcome = AdmissionOutcome(self.outcome)
        envelope_refs = _refs("resolved_envelope_ref", self.resolved_envelope_refs)
        if not envelope_refs:
            raise ValueError("resolved_envelope_refs must contain at least one reference")
        reason_codes = _refs("reason_code", self.reason_codes)
        if not reason_codes:
            raise ValueError("reason_codes must contain at least one deterministic code")

        limits = tuple(self.effective_limits)
        if not all(isinstance(item, ResourceLimit) for item in limits):
            raise ValueError("effective_limits entries must be ResourceLimit values")
        dimensions = [item.dimension for item in limits]
        if len(set(dimensions)) != len(dimensions):
            raise ValueError("effective_limits cannot contain duplicate dimensions")
        limits = tuple(sorted(limits, key=lambda item: item.dimension.value))

        queue_item_ref = _optional("queue_item_ref", self.queue_item_ref)
        if self.retry_after is not None:
            if not isinstance(self.retry_after, timedelta) or self.retry_after <= timedelta(0):
                raise ValueError("retry_after must be a positive timedelta")

        if outcome is AdmissionOutcome.ADMITTED:
            if not limits:
                raise ValueError("an admitted decision requires effective_limits")
            if queue_item_ref is not None or self.retry_after is not None:
                raise ValueError("an admitted decision cannot own queue or retry metadata")
        elif outcome is AdmissionOutcome.QUEUED:
            if queue_item_ref is None:
                raise ValueError("a queued decision requires queue_item_ref")
            if limits:
                raise ValueError("a queued decision cannot claim effective resource allocation")
        else:
            if queue_item_ref is not None:
                raise ValueError(f"a {outcome.value} decision cannot own a queue item")
            if limits:
                raise ValueError(f"a {outcome.value} decision cannot claim effective limits")

        object.__setattr__(self, "decision_id", _required("decision_id", self.decision_id))
        object.__setattr__(self, "request_id", _required("request_id", self.request_id))
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "resolved_envelope_refs", envelope_refs)
        object.__setattr__(
            self, "decision_reason", _required("decision_reason", self.decision_reason)
        )
        object.__setattr__(self, "reason_codes", reason_codes)
        object.__setattr__(self, "decided_at", _instant("decided_at", self.decided_at))
        object.__setattr__(self, "effective_limits", limits)
        object.__setattr__(self, "queue_item_ref", queue_item_ref)
        object.__setattr__(self, "receipt_refs", _refs("receipt_ref", self.receipt_refs))
        object.__setattr__(self, "evidence_refs", _refs("evidence_ref", self.evidence_refs))

    @property
    def is_executable(self) -> bool:
        """Only admitted resource work can proceed to execution binding."""

        return self.outcome is AdmissionOutcome.ADMITTED

    @property
    def retains_queue_ownership(self) -> bool:
        """Only a queued outcome creates Resource Governor queue ownership."""

        return self.outcome is AdmissionOutcome.QUEUED

    @property
    def grants_business_authority(self) -> bool:
        """A resource admission decision is never business authorization."""

        return False
