"""Terminal, correlation-safe receipts for the SemantiK Architect adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
from types import MappingProxyType
from typing import Callable, Mapping, Sequence

Clock = Callable[[], datetime]


class Decision(StrEnum):
    """Authority decision attached to an integration transition."""

    AUTHORIZED = "authorized"
    DENIED = "denied"
    INDETERMINATE = "indeterminate"
    NOT_APPLICABLE = "not_applicable"


class ExecutionState(StrEnum):
    """Execution state kept separate from authority and commit state."""

    NOT_STARTED = "not_started"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CommitState(StrEnum):
    """Commit state for transitions that can alter accepted kOA state."""

    NOT_APPLICABLE = "not_applicable"
    NOT_COMMITTED = "not_committed"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FORWARD_REPAIRED = "forward_repaired"


class ReceiptOutcome(StrEnum):
    """Closed terminal outcomes exposed by this adapter."""

    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    BLOCKED = "blocked"


_FORBIDDEN_DETAIL_TOKENS = frozenset(
    {
        "authorization",
        "cookie",
        "credential",
        "password",
        "private_key",
        "secret",
        "token",
    }
)


def utc_now() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


def _clean_ref(value: str, field_name: str) -> str:
    candidate = value.strip()
    if not candidate or len(candidate) > 256 or any(ch.isspace() for ch in candidate):
        raise ValueError(f"{field_name} must be a non-empty stable reference")
    return candidate


def _clean_reason(value: str) -> str:
    candidate = value.strip()
    if not candidate or len(candidate) > 96:
        raise ValueError("reason_code must be a non-empty bounded value")
    if not candidate.replace("_", "").isalnum() or candidate.lower() != candidate:
        raise ValueError("reason_code must use lower snake case")
    return candidate


def _sanitize_details(details: Mapping[str, str] | None) -> Mapping[str, str]:
    if not details:
        return MappingProxyType({})
    cleaned: dict[str, str] = {}
    for raw_key, raw_value in details.items():
        key = str(raw_key).strip().lower()
        if not key or any(token in key for token in _FORBIDDEN_DETAIL_TOKENS):
            continue
        value = str(raw_value).strip()
        if not value or len(value) > 256:
            continue
        if any(token in value.lower() for token in _FORBIDDEN_DETAIL_TOKENS):
            continue
        cleaned[key] = value
    return MappingProxyType(dict(sorted(cleaned.items())))


@dataclass(frozen=True, slots=True)
class IntegrationReceipt:
    """Immutable terminal receipt for an adapter-visible transition."""

    receipt_id: str
    receipt_type: str
    request_id: str
    correlation_id: str
    subject_ref: str
    decision: Decision
    execution_state: ExecutionState
    commit_state: CommitState
    outcome: ReceiptOutcome
    reason_code: str
    recorded_at: datetime
    evidence_refs: tuple[str, ...] = ()
    details: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        for name, enum_type in (
            ("decision", Decision),
            ("execution_state", ExecutionState),
            ("commit_state", CommitState),
            ("outcome", ReceiptOutcome),
        ):
            value = getattr(self, name)
            if not isinstance(value, enum_type):
                raise TypeError(f"{name} must be a {enum_type.__name__}")
        for name in ("receipt_id", "receipt_type", "request_id", "correlation_id", "subject_ref"):
            object.__setattr__(self, name, _clean_ref(getattr(self, name), name))
        object.__setattr__(self, "reason_code", _clean_reason(self.reason_code))
        if self.recorded_at.tzinfo is None:
            raise ValueError("recorded_at must be timezone-aware")
        refs = tuple(_clean_ref(ref, "evidence_ref") for ref in self.evidence_refs)
        if len(set(refs)) != len(refs):
            raise ValueError("evidence_refs must be unique")
        object.__setattr__(self, "evidence_refs", refs)
        object.__setattr__(self, "details", _sanitize_details(self.details))
        self._validate_terminal_semantics()

    def _validate_terminal_semantics(self) -> None:
        allowed = {
            ReceiptOutcome.SUCCEEDED: {ExecutionState.SUCCEEDED},
            ReceiptOutcome.FAILED: {ExecutionState.FAILED},
            ReceiptOutcome.CANCELLED: {ExecutionState.CANCELLED},
            ReceiptOutcome.REJECTED: {ExecutionState.NOT_STARTED},
            ReceiptOutcome.BLOCKED: {ExecutionState.NOT_STARTED},
        }
        if self.execution_state not in allowed[self.outcome]:
            raise ValueError("receipt outcome and execution_state are inconsistent")
        if self.outcome is ReceiptOutcome.SUCCEEDED and self.decision is Decision.DENIED:
            raise ValueError("a denied decision cannot have a successful outcome")
        if self.commit_state is CommitState.COMMITTED and self.outcome is not ReceiptOutcome.SUCCEEDED:
            raise ValueError("only a successful outcome can be committed")

    def to_mapping(self) -> Mapping[str, object]:
        """Return a deterministic JSON-compatible projection."""

        return MappingProxyType(
            {
                "receipt_id": self.receipt_id,
                "receipt_type": self.receipt_type,
                "request_id": self.request_id,
                "correlation_id": self.correlation_id,
                "subject_ref": self.subject_ref,
                "decision": self.decision.value,
                "execution_state": self.execution_state.value,
                "commit_state": self.commit_state.value,
                "outcome": self.outcome.value,
                "reason_code": self.reason_code,
                "recorded_at": self.recorded_at.isoformat(),
                "evidence_refs": list(self.evidence_refs),
                "details": dict(self.details),
            }
        )


def make_receipt(
    *,
    receipt_type: str,
    request_id: str,
    correlation_id: str,
    subject_ref: str,
    decision: Decision,
    execution_state: ExecutionState,
    commit_state: CommitState,
    outcome: ReceiptOutcome,
    reason_code: str,
    evidence_refs: Sequence[str] = (),
    details: Mapping[str, str] | None = None,
    clock: Clock = utc_now,
) -> IntegrationReceipt:
    """Create a deterministic-identity terminal receipt."""

    identity_material = "\x1f".join(
        (
            receipt_type,
            request_id,
            correlation_id,
            subject_ref,
            outcome.value,
            reason_code,
        )
    )
    receipt_id = f"semantik-receipt:sha256:{sha256(identity_material.encode('utf-8')).hexdigest()}"
    return IntegrationReceipt(
        receipt_id=receipt_id,
        receipt_type=receipt_type,
        request_id=request_id,
        correlation_id=correlation_id,
        subject_ref=subject_ref,
        decision=decision,
        execution_state=execution_state,
        commit_state=commit_state,
        outcome=outcome,
        reason_code=reason_code,
        recorded_at=clock(),
        evidence_refs=tuple(evidence_refs),
        details=_sanitize_details(details),
    )
