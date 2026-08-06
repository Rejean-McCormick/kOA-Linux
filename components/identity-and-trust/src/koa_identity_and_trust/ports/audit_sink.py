"""Audit and receipt-delivery boundary for Identity and Trust."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping, Protocol, Sequence, runtime_checkable


_SENSITIVE_NAMES = frozenset(
    {
        "secret",
        "password",
        "private_key",
        "private-key",
        "token",
        "factor",
        "presented_proof",
        "signature",
        "credential_material",
    }
)


def _frozen_details(details: Mapping[str, str]) -> Mapping[str, str]:
    normalized: dict[str, str] = {}
    for key, value in details.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("audit detail keys must be non-empty strings")
        lowered = key.strip().lower()
        if lowered in _SENSITIVE_NAMES or any(name in lowered for name in _SENSITIVE_NAMES):
            raise ValueError(f"audit detail {key!r} may expose protected material")
        if not isinstance(value, str):
            raise TypeError("audit detail values must be strings")
        normalized[key.strip()] = value
    return MappingProxyType(dict(sorted(normalized.items())))


@dataclass(frozen=True, slots=True)
class AuditEvent:
    """A redacted, attributable event delivered to the audit boundary."""

    event_id: str
    operation_id: str
    request_id: str
    event_type: str
    outcome: str
    occurred_at: datetime
    subject_refs: tuple[str, ...] = ()
    reason_code: str | None = None
    receipt_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()
    details: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for field_name in ("event_id", "operation_id", "request_id", "event_type", "outcome"):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        if self.occurred_at.tzinfo is None or self.occurred_at.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware")
        object.__setattr__(self, "subject_refs", tuple(self.subject_refs))
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))
        object.__setattr__(self, "details", _frozen_details(self.details))


@runtime_checkable
class AuditSink(Protocol):
    """Deliver redacted audit evidence through the declared component boundary."""

    def ensure_available(self, *, critical: bool) -> None:
        """Fail before evaluation or transition when the required path is unavailable."""
        raise NotImplementedError

    def publish(self, event: AuditEvent) -> None:
        """Durably accept one redacted event or raise an explicit dependency failure."""
        raise NotImplementedError
