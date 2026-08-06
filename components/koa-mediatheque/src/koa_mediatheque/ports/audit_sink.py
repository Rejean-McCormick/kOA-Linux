"""Redacted audit and receipt boundaries for kOA Mediatheque."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable



@runtime_checkable
class Clock(Protocol):
    """Provide timezone-aware timestamps for deterministic application decisions."""

    def now(self) -> datetime:
        """Return the current timezone-aware time."""


def require_utc(value: datetime) -> datetime:
    """Validate and normalize a timestamp to UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return value.astimezone(timezone.utc)


_ALLOWED_OUTCOMES = frozenset({"succeeded", "denied", "indeterminate", "failed", "queued", "deferred"})


def _freeze_text_map(value: Mapping[str, str]) -> Mapping[str, str]:
    frozen: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("audit detail keys must be non-empty strings")
        if not isinstance(item, str):
            raise TypeError("audit detail values must be strings")
        frozen[key] = item
    return MappingProxyType(dict(sorted(frozen.items())))


@dataclass(frozen=True, slots=True)
class AuditEvent:
    event_id: str
    event_type: str
    actor_id: str
    subject_refs: tuple[str, ...]
    outcome: str
    occurred_at: datetime
    evidence_refs: tuple[str, ...] = ()
    details: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("event_id", "event_type", "actor_id"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.outcome not in _ALLOWED_OUTCOMES:
            raise ValueError(f"unsupported audit outcome: {self.outcome}")
        if not self.subject_refs or any(not value.strip() for value in self.subject_refs):
            raise ValueError("subject_refs must contain non-empty references")
        object.__setattr__(self, "occurred_at", require_utc(self.occurred_at))
        object.__setattr__(self, "subject_refs", tuple(dict.fromkeys(self.subject_refs)))
        object.__setattr__(self, "evidence_refs", tuple(dict.fromkeys(self.evidence_refs)))
        object.__setattr__(self, "details", _freeze_text_map(self.details))


@dataclass(frozen=True, slots=True)
class EvidenceReceipt:
    receipt_id: str
    receipt_type: str
    idempotency_key: str
    subject_refs: tuple[str, ...]
    outcome: str
    issued_at: datetime
    evidence_refs: tuple[str, ...] = ()
    details: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("receipt_id", "receipt_type", "idempotency_key"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        if self.outcome not in _ALLOWED_OUTCOMES:
            raise ValueError(f"unsupported receipt outcome: {self.outcome}")
        if not self.subject_refs or any(not value.strip() for value in self.subject_refs):
            raise ValueError("subject_refs must contain non-empty references")
        object.__setattr__(self, "issued_at", require_utc(self.issued_at))
        object.__setattr__(self, "subject_refs", tuple(dict.fromkeys(self.subject_refs)))
        object.__setattr__(self, "evidence_refs", tuple(dict.fromkeys(self.evidence_refs)))
        object.__setattr__(self, "details", _freeze_text_map(self.details))


@runtime_checkable
class AuditSink(Protocol):
    """Append-only sink. Media bytes and restricted metadata are prohibited."""

    def emit(self, event: AuditEvent) -> None:
        """Persist a redacted audit event or fail explicitly."""

    def record_receipt(self, receipt: EvidenceReceipt) -> None:
        """Persist immutable evidence or fail explicitly."""
