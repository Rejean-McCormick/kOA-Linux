"""Selective, machine-readable Ariane navigation receipts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping


class ReceiptClass(str, Enum):
    TRANSITION = "transition_receipt"
    VERIFICATION = "verification_receipt"
    RECOVERY = "recovery_receipt"


class NavigationEvidenceType(str, Enum):
    NAVIGATION_SESSION = "navigation_session"
    CONFIRMATION = "confirmation"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    FAILURE = "failure"
    CANCELLATION = "cancellation"
    RECOVERY = "recovery"


class ReceiptOutcome(str, Enum):
    PREPARED = "prepared"
    COMMITTED = "committed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RECOVERED = "forward_repaired"
    CLOSED = "closed"
    BLOCKED = "denied"


_FORBIDDEN_DETAIL_KEYS = {
    "password",
    "secret",
    "token",
    "credential",
    "authorization_header",
    "raw_screen",
    "screenshot",
    "audio_bytes",
    "raw_audio",
}


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _refs(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(value, field) for value in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


def _safe_details(value: Mapping[str, Any]) -> tuple[tuple[str, str | int | float | bool | None], ...]:
    result: list[tuple[str, str | int | float | bool | None]] = []
    for key in sorted(value):
        normalized = _required_text(key, "detail key").lower()
        if normalized in _FORBIDDEN_DETAIL_KEYS or any(part in normalized for part in ("password", "secret", "token", "credential")):
            raise ValueError(f"receipt detail {key!r} is prohibited")
        item = value[key]
        if item is not None and not isinstance(item, (str, int, float, bool)):
            raise TypeError("receipt details must contain only bounded scalar values")
        if isinstance(item, str) and len(item) > 512:
            raise ValueError("receipt string details must not exceed 512 characters")
        result.append((key, item))
    return tuple(result)


@dataclass(frozen=True, slots=True)
class NavigationReceipt:
    receipt_id: str
    receipt_class: ReceiptClass
    evidence_type: NavigationEvidenceType
    outcome: ReceiptOutcome
    request_id: str
    correlation_id: str
    subject_ref: str
    actor_ref: str
    application_ref: str
    reason_code: str
    recorded_at: datetime
    target_refs: tuple[str, ...] = ()
    authority_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    disclosure_class: str = "restricted_operational"
    details: tuple[tuple[str, str | int | float | bool | None], ...] = ()

    def __post_init__(self) -> None:
        for field in (
            "receipt_id",
            "request_id",
            "correlation_id",
            "subject_ref",
            "actor_ref",
            "application_ref",
            "reason_code",
            "disclosure_class",
        ):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "recorded_at", _utc(self.recorded_at, "recorded_at"))
        object.__setattr__(self, "target_refs", _refs(self.target_refs, "target_refs"))
        object.__setattr__(self, "authority_refs", _refs(self.authority_refs, "authority_refs"))
        object.__setattr__(self, "evidence_refs", _refs(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "details", _safe_details(dict(self.details)))
        if self.outcome is ReceiptOutcome.COMMITTED and self.evidence_type not in {
            NavigationEvidenceType.EXECUTION,
            NavigationEvidenceType.VERIFICATION,
        }:
            raise ValueError("committed outcome is valid only for execution or verification evidence")

    @classmethod
    def create(
        cls,
        *,
        receipt_class: ReceiptClass,
        evidence_type: NavigationEvidenceType,
        outcome: ReceiptOutcome,
        request_id: str,
        correlation_id: str,
        subject_ref: str,
        actor_ref: str,
        application_ref: str,
        reason_code: str,
        recorded_at: datetime,
        target_refs: tuple[str, ...] = (),
        authority_refs: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        details: Mapping[str, Any] | None = None,
    ) -> "NavigationReceipt":
        seed = "|".join(
            [
                request_id,
                correlation_id,
                evidence_type.value,
                outcome.value,
                application_ref,
                recorded_at.astimezone(timezone.utc).isoformat(),
            ]
        )
        receipt_id = f"ariane-receipt-{sha256(seed.encode('utf-8')).hexdigest()[:32]}"
        return cls(
            receipt_id=receipt_id,
            receipt_class=receipt_class,
            evidence_type=evidence_type,
            outcome=outcome,
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=subject_ref,
            actor_ref=actor_ref,
            application_ref=application_ref,
            reason_code=reason_code,
            recorded_at=recorded_at,
            target_refs=target_refs,
            authority_refs=authority_refs,
            evidence_refs=evidence_refs,
            details=tuple((details or {}).items()),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "receipt_id": self.receipt_id,
            "receipt_schema_version": "1.0.0",
            "receipt_class": self.receipt_class.value,
            "transition_type": self.evidence_type.value,
            "producer_component_id": "ariane-adapter",
            "subject_ref": self.subject_ref,
            "actor_ref": self.actor_ref,
            "target_refs": list(self.target_refs),
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "authority_refs": list(self.authority_refs),
            "outcome": self.outcome.value,
            "reason_code": self.reason_code,
            "recorded_at": self.recorded_at.isoformat().replace("+00:00", "Z"),
            "evidence_refs": list(self.evidence_refs),
            "disclosure_class": self.disclosure_class,
            "details": dict(self.details),
        }
