"""Rights evaluation boundary owned outside the Mediatheque application."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from .audit_sink import require_utc

_ALLOWED_OUTCOMES = frozenset({"allowed", "denied", "indeterminate"})
_ALLOWED_ACTIONS = frozenset({"ingest", "update_metadata", "derive_rendition", "prepare_export", "delete"})


@dataclass(frozen=True, slots=True)
class RightsRequest:
    action: str
    actor_id: str
    purpose: str
    record_id: str | None = None
    version_id: str | None = None
    audience: str | None = None
    destination: str | None = None
    context: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.action not in _ALLOWED_ACTIONS:
            raise ValueError(f"unsupported rights action: {self.action}")
        for name in ("actor_id", "purpose"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must not be empty")
        frozen: dict[str, str] = {}
        for key, value in self.context.items():
            if not isinstance(key, str) or not key.strip() or not isinstance(value, str):
                raise ValueError("rights context must contain non-empty string keys and string values")
            frozen[key] = value
        object.__setattr__(self, "context", MappingProxyType(dict(sorted(frozen.items()))))


@dataclass(frozen=True, slots=True)
class RightsDecision:
    decision_id: str
    outcome: str
    reason_code: str
    evaluated_at: datetime
    evidence_refs: tuple[str, ...]
    allowed_metadata_fields: tuple[str, ...] = ()
    max_content_bytes: int | None = None
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.decision_id.strip() or not self.reason_code.strip():
            raise ValueError("decision_id and reason_code must not be empty")
        if self.outcome not in _ALLOWED_OUTCOMES:
            raise ValueError(f"unsupported rights outcome: {self.outcome}")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("rights decisions require evidence references")
        if self.max_content_bytes is not None and self.max_content_bytes < 0:
            raise ValueError("max_content_bytes must be non-negative")
        object.__setattr__(self, "evaluated_at", require_utc(self.evaluated_at))
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", require_utc(self.expires_at))
        object.__setattr__(self, "evidence_refs", tuple(dict.fromkeys(self.evidence_refs)))
        object.__setattr__(self, "allowed_metadata_fields", tuple(dict.fromkeys(self.allowed_metadata_fields)))


@runtime_checkable
class RightsEvaluator(Protocol):
    def evaluate(self, request: RightsRequest) -> RightsDecision:
        """Return an explicit decision. Transport failure must map to indeterminate."""
