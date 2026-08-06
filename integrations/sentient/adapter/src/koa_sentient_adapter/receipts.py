"""Durable, minimized receipts for SenTient workbench transitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Any, Mapping


class ReceiptType(str, Enum):
    WORKBENCH_STATE = "workbench_state"
    CANDIDATE_PRODUCED = "candidate_produced"
    IMPORT_REQUESTED = "import_requested"
    OWNER_ACCEPTANCE = "owner_acceptance"
    OWNER_REJECTION = "owner_rejection"
    WORKBENCH_REMOVAL = "workbench_removal"


class ReceiptOutcome(str, Enum):
    RECORDED = "recorded"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    QUARANTINED = "quarantined"


_FORBIDDEN_KEYS = (
    "password",
    "secret",
    "token",
    "credential",
    "private_key",
    "raw_key",
    "authorization",
    "prompt_text",
    "raw_prompt",
    "content_bytes",
    "private_proof",
)


@dataclass(frozen=True, slots=True)
class WorkbenchReceipt:
    receipt_id: str
    receipt_type: ReceiptType
    outcome: ReceiptOutcome
    request_id: str
    correlation_id: str
    subject_ref: str
    actor_ref: str
    reason_code: str
    recorded_at: datetime
    job_id: str | None = None
    candidate_refs: tuple[str, ...] = ()
    authority_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    details: tuple[tuple[str, str | int | float | bool | None], ...] = ()
    disclosure_class: str = "restricted"
    authoritative: bool = False

    def __post_init__(self) -> None:
        for field in (
            "receipt_id",
            "request_id",
            "correlation_id",
            "subject_ref",
            "actor_ref",
            "reason_code",
            "disclosure_class",
        ):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        if self.job_id is not None:
            object.__setattr__(self, "job_id", _required_text(self.job_id, "job_id"))
        object.__setattr__(self, "recorded_at", _utc(self.recorded_at, "recorded_at"))
        for field in ("candidate_refs", "authority_refs", "evidence_refs"):
            object.__setattr__(self, field, _sorted_unique(getattr(self, field), field))
        object.__setattr__(self, "details", _safe_details(dict(self.details)))
        if self.authoritative:
            raise ValueError("a SenTient receipt is evidence and cannot be authoritative")
        if self.receipt_type in {ReceiptType.OWNER_ACCEPTANCE, ReceiptType.OWNER_REJECTION} and not self.authority_refs:
            raise ValueError("owner acceptance or rejection receipt requires authority_refs")
        if self.receipt_type is ReceiptType.CANDIDATE_PRODUCED and not self.candidate_refs:
            raise ValueError("candidate_produced receipt requires candidate_refs")

    @classmethod
    def create(
        cls,
        *,
        receipt_type: ReceiptType,
        outcome: ReceiptOutcome,
        request_id: str,
        correlation_id: str,
        subject_ref: str,
        actor_ref: str,
        reason_code: str,
        recorded_at: datetime,
        job_id: str | None = None,
        candidate_refs: tuple[str, ...] = (),
        authority_refs: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        details: Mapping[str, Any] | None = None,
    ) -> "WorkbenchReceipt":
        at = _utc(recorded_at, "recorded_at")
        seed = "|".join(
            (
                receipt_type.value,
                outcome.value,
                request_id,
                correlation_id,
                subject_ref,
                job_id or "",
                _iso(at),
            )
        )
        return cls(
            receipt_id=f"sentient-receipt-{sha256(seed.encode('utf-8')).hexdigest()[:32]}",
            receipt_type=receipt_type,
            outcome=outcome,
            request_id=request_id,
            correlation_id=correlation_id,
            subject_ref=subject_ref,
            actor_ref=actor_ref,
            reason_code=reason_code,
            recorded_at=at,
            job_id=job_id,
            candidate_refs=candidate_refs,
            authority_refs=authority_refs,
            evidence_refs=evidence_refs,
            details=tuple((details or {}).items()),
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": "1.0.0",
            "artifact_class": "decision_receipt",
            "receipt_id": self.receipt_id,
            "receipt_type": self.receipt_type.value,
            "outcome": self.outcome.value,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "subject_ref": self.subject_ref,
            "actor_ref": self.actor_ref,
            "job_id": self.job_id,
            "candidate_refs": list(self.candidate_refs),
            "authority_refs": list(self.authority_refs),
            "evidence_refs": list(self.evidence_refs),
            "reason_code": self.reason_code,
            "recorded_at": _iso(self.recorded_at),
            "details": dict(self.details),
            "disclosure_class": self.disclosure_class,
            "producer_component_id": "sentient_adapter",
            "authority_effect": "evidence_only",
            "authoritative": False,
        }


def _safe_details(values: Mapping[str, Any]) -> tuple[tuple[str, str | int | float | bool | None], ...]:
    result: list[tuple[str, str | int | float | bool | None]] = []
    for key in sorted(values):
        normalized = _required_text(key, "detail key").lower()
        if any(part in normalized for part in _FORBIDDEN_KEYS):
            raise ValueError(f"receipt detail {key!r} is prohibited")
        value = values[key]
        if value is not None and not isinstance(value, (str, int, float, bool)):
            raise TypeError("receipt detail values must be bounded scalars")
        if isinstance(value, str) and len(value) > 512:
            raise ValueError("receipt detail string exceeds 512 characters")
        result.append((key, value))
    return tuple(result)


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _sorted_unique(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(item, field) for item in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return tuple(sorted(cleaned))


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
