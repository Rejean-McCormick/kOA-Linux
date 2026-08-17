"""Application-layer primitives for deterministic resource governance."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
import json
from typing import Mapping, Sequence

from ..domain import PriorityClass, ResourceEnvelope, ResourceLimit


class ResourceGovernorApplicationError(RuntimeError):
    """Base class for explicit application failures."""

    reason_code = "resource_governor_application_error"

    def __init__(self, message: str, *, reason_code: str | None = None) -> None:
        super().__init__(message)
        if reason_code is not None:
            self.reason_code = reason_code


class InvalidRequest(ResourceGovernorApplicationError, ValueError):
    reason_code = "invalid_request"


class DependencyUnavailable(ResourceGovernorApplicationError):
    reason_code = "dependency_unavailable"


class Conflict(ResourceGovernorApplicationError):
    reason_code = "state_conflict"


class ReconciliationRequired(ResourceGovernorApplicationError):
    reason_code = "reconciliation_required"


def require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidRequest(f"{field} must be a non-empty string")
    normalized = value.strip()
    if any(ord(character) < 32 for character in normalized):
        raise InvalidRequest(f"{field} contains control characters")
    return normalized


def require_utc(value: datetime, field: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InvalidRequest(f"{field} must be a timezone-aware datetime")
    return value.astimezone(UTC)


def stable_ref(kind: str, *parts: str) -> str:
    material = "\x1f".join(require_text(part, "reference part") for part in parts)
    return f"{require_text(kind, 'kind')}-{sha256(material.encode()).hexdigest()[:32]}"


def timestamp(value: datetime) -> str:
    return require_utc(value, "timestamp").isoformat().replace("+00:00", "Z")


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


@dataclass(frozen=True, slots=True)
class ResolvedEnvelope:
    envelope_refs: tuple[str, ...]
    limits: tuple[ResourceLimit, ...]
    max_concurrency: int
    queue_capacity: int
    retry_limit: int
    priority: int
    priority_class: PriorityClass


def resolve_envelope_chain(
    envelopes: Sequence[ResourceEnvelope],
    *,
    target_scope: str,
    at: datetime,
) -> ResolvedEnvelope:
    """Validate an enclosing-to-specific envelope chain and merge restrictions."""

    instant = require_utc(at, "at")
    chain = tuple(envelopes)
    if not chain:
        raise DependencyUnavailable("no active resource envelope resolved", reason_code="active_envelope_unresolved")
    merged: dict[object, ResourceLimit] = {}
    for index, envelope in enumerate(chain):
        if not isinstance(envelope, ResourceEnvelope):
            raise InvalidRequest("envelope chain contains a non-ResourceEnvelope value")
        if not envelope.is_effective_at(instant):
            raise DependencyUnavailable(
                f"resource envelope is not effective: {envelope.envelope_id}",
                reason_code="active_envelope_not_effective",
            )
        accepted_targets = {
            envelope.target_id,
            envelope.target_scope,
            f"{envelope.target_scope}:{envelope.target_id}",
        }
        if target_scope not in accepted_targets:
            raise InvalidRequest(
                f"resource envelope {envelope.envelope_id} does not target {target_scope}"
            )
        if index:
            envelope.assert_within(chain[index - 1])
        for limit in envelope.limits:
            merged[limit.dimension] = limit
    most_specific = chain[-1]
    return ResolvedEnvelope(
        envelope_refs=tuple(envelope.envelope_id for envelope in chain),
        limits=tuple(sorted(merged.values(), key=lambda item: item.dimension.value)),
        max_concurrency=min(envelope.max_concurrency for envelope in chain),
        queue_capacity=min(envelope.queue_capacity for envelope in chain),
        retry_limit=min(envelope.retry_limit for envelope in chain),
        priority=most_specific.priority,
        priority_class=most_specific.priority_class,
    )


def limit_values(limits: Sequence[ResourceLimit]) -> dict[str, str]:
    result: dict[str, str] = {}
    for limit in sorted(limits, key=lambda item: item.dimension.value):
        prefix = limit.dimension.value
        result[f"{prefix}_reservation"] = str(Decimal(limit.reservation))
        if limit.soft_limit is not None:
            result[f"{prefix}_soft_limit"] = str(Decimal(limit.soft_limit))
        result[f"{prefix}_hard_limit"] = str(Decimal(limit.hard_limit))
        result[f"{prefix}_unit"] = limit.unit
    return result


def audit_record(
    *,
    event_type: str,
    correlation_id: str,
    occurred_at: datetime,
    payload: Mapping[str, object],
) -> dict[str, object]:
    return {
        "event_type": require_text(event_type, "event_type"),
        "correlation_id": require_text(correlation_id, "correlation_id"),
        "occurred_at": timestamp(occurred_at),
        "payload": dict(payload),
    }


from .admit_workload import (  # noqa: E402
    AdmissionContext,
    AdmitWorkload,
    AdmitWorkloadCommand,
)
from .apply_envelope import (  # noqa: E402
    ApplyEnvelope,
    ApplyEnvelopeCommand,
    ApplyEnvelopeResult,
)
from .degrade_workload import (  # noqa: E402
    DegradeWorkload,
    DegradeWorkloadCommand,
    DegradeWorkloadResult,
)
from .reconcile_usage import (  # noqa: E402
    ReconcileUsage,
    ReconcileUsageCommand,
    UsageReconciliation,
)
from .restore_workload import (  # noqa: E402
    RestoreWorkload,
    RestoreWorkloadCommand,
    RestoreWorkloadResult,
)

__all__ = (
    "AdmissionContext",
    "AdmitWorkload",
    "AdmitWorkloadCommand",
    "ApplyEnvelope",
    "ApplyEnvelopeCommand",
    "ApplyEnvelopeResult",
    "Conflict",
    "DegradeWorkload",
    "DegradeWorkloadCommand",
    "DegradeWorkloadResult",
    "DependencyUnavailable",
    "InvalidRequest",
    "ReconcileUsage",
    "ReconcileUsageCommand",
    "ReconciliationRequired",
    "ResourceGovernorApplicationError",
    "RestoreWorkload",
    "RestoreWorkloadCommand",
    "RestoreWorkloadResult",
    "UsageReconciliation",
)
