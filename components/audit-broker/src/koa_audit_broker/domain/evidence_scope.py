"""Purpose-bound evidence scopes that cannot silently broaden authority."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable

from .audit_event import DomainValidationError


class AuditClass(StrEnum):
    """Primary selective-audit classes."""

    PUBLIC_TRANSPARENCY_RECEIPTS = "public_transparency_receipts"
    TENANT_OPERATIONAL_AUDIT = "tenant_operational_audit"
    RESTRICTED_EVIDENCE_AUDIT = "restricted_evidence_audit"
    PERSONAL_PRIVACY_RECORDS = "personal_privacy_records"
    SECURITY_AND_NODE_AUDIT = "security_and_node_audit"


class ScopeExpansionError(DomainValidationError):
    """Raised when an effective evidence scope broadens its governing scope."""


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainValidationError(f"{field_name} must be a non-empty string")
    return value.strip()


def _optional_text(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    return _required_text(value, field_name)


def _frozen_references(
    values: Iterable[str],
    field_name: str,
    *,
    required: bool = False,
) -> frozenset[str]:
    if isinstance(values, (str, bytes)):
        raise DomainValidationError(f"{field_name} must be an iterable of strings")
    normalized = frozenset(_required_text(value, field_name) for value in values)
    if required and not normalized:
        raise DomainValidationError(f"{field_name} must not be empty")
    return normalized


def _aware_datetime(value: datetime | None, field_name: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


@dataclass(frozen=True, slots=True)
class EvidenceScope:
    """Closed, purpose-bound scope for an audit query or disclosure.

    Empty sets are never interpreted as wildcards. At least one subject or record
    selector and at least one allowed field are required, preventing unbounded queries.
    """

    purpose: str
    audit_class: AuditClass
    field_allowlist: frozenset[str]
    subject_references: frozenset[str] = frozenset()
    record_references: frozenset[str] = frozenset()
    audience_references: frozenset[str] = frozenset()
    destination_reference: str | None = None
    valid_from: datetime | None = None
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "purpose", _required_text(self.purpose, "purpose"))
        try:
            audit_class = AuditClass(self.audit_class)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("audit_class is not a declared selective-audit class") from exc
        object.__setattr__(self, "audit_class", audit_class)

        fields = _frozen_references(
            self.field_allowlist,
            "field_allowlist",
            required=True,
        )
        subjects = _frozen_references(self.subject_references, "subject_references")
        records = _frozen_references(self.record_references, "record_references")
        if not subjects and not records:
            raise DomainValidationError(
                "an evidence scope requires at least one subject or record selector"
            )
        object.__setattr__(self, "field_allowlist", fields)
        object.__setattr__(self, "subject_references", subjects)
        object.__setattr__(self, "record_references", records)
        object.__setattr__(
            self,
            "audience_references",
            _frozen_references(self.audience_references, "audience_references"),
        )
        object.__setattr__(
            self,
            "destination_reference",
            _optional_text(self.destination_reference, "destination_reference"),
        )

        valid_from = _aware_datetime(self.valid_from, "valid_from")
        expires_at = _aware_datetime(self.expires_at, "expires_at")
        if expires_at is None:
            raise DomainValidationError("expires_at is required for a bounded evidence scope")
        if valid_from is not None and valid_from >= expires_at:
            raise DomainValidationError("valid_from must be earlier than expires_at")
        object.__setattr__(self, "valid_from", valid_from)
        object.__setattr__(self, "expires_at", expires_at)

    def is_within(self, governing_scope: EvidenceScope) -> bool:
        """Return whether this scope is a non-broadening projection of another scope."""

        if self.purpose != governing_scope.purpose:
            return False
        if self.audit_class is not governing_scope.audit_class:
            return False
        if not self.field_allowlist <= governing_scope.field_allowlist:
            return False
        if not self.subject_references <= governing_scope.subject_references:
            return False
        if not self.record_references <= governing_scope.record_references:
            return False
        if not self.audience_references <= governing_scope.audience_references:
            return False
        if self.destination_reference != governing_scope.destination_reference:
            return False

        if governing_scope.valid_from is not None:
            if self.valid_from is None or self.valid_from < governing_scope.valid_from:
                return False
        if self.expires_at > governing_scope.expires_at:
            return False
        return True

    def require_within(self, governing_scope: EvidenceScope) -> None:
        """Fail closed if this scope would broaden the governing scope."""

        if not self.is_within(governing_scope):
            raise ScopeExpansionError(
                "effective evidence scope must not broaden purpose, class, selectors, "
                "fields, audience, destination, or validity"
            )

    def as_dict(self) -> dict[str, object]:
        """Return a deterministic serialization-ready representation."""

        return {
            "purpose": self.purpose,
            "audit_class": self.audit_class.value,
            "field_allowlist": sorted(self.field_allowlist),
            "subject_references": sorted(self.subject_references),
            "record_references": sorted(self.record_references),
            "audience_references": sorted(self.audience_references),
            "destination_reference": self.destination_reference,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "expires_at": self.expires_at.isoformat(),
        }
