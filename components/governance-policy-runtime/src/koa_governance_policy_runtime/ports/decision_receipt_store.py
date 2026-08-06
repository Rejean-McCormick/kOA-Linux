"""Authoritative decision-receipt persistence boundary."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class DecisionResult(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


_ALLOWED_OBLIGATION_TYPES = frozenset(
    {
        "data_minimization",
        "destination_restriction",
        "secondary_approval",
        "duration_limit",
        "privileged_execution_path",
        "audit_evidence",
        "subject_notification",
        "compensating_control",
        "follow_up_review",
        "retention_limit",
        "receipt_linkage",
        "re_evaluation_before_execution",
    }
)


@dataclass(frozen=True, slots=True)
class DecisionObligation:
    obligation_type: str
    parameters: Mapping[str, Any]
    required: bool = True

    def __post_init__(self) -> None:
        if self.obligation_type not in _ALLOWED_OBLIGATION_TYPES:
            raise ValueError(f"unsupported obligation type: {self.obligation_type}")


@dataclass(frozen=True, slots=True)
class DecisionReceipt:
    receipt_id: str
    request_id: str
    request_fingerprint: str
    correlation_id: str
    requester_ref: str
    action_ref: str
    target_ref: str
    scope: tuple[str, ...]
    decision_class: str
    result: DecisionResult
    obligations: tuple[DecisionObligation, ...]
    diagnostics: tuple[str, ...]
    policy_set_ref: str
    authority_version: str
    verified_context_refs: tuple[str, ...]
    exception_ids: tuple[str, ...]
    evaluated_at: datetime
    evaluator_identity: str
    evaluator_version: str
    audit_evidence_ref: str | None = None


@runtime_checkable
class DecisionReceiptStore(Protocol):
    """Store immutable receipts and idempotency evidence."""

    @abstractmethod
    def find_by_request_id(self, request_id: str) -> tuple[DecisionReceipt, ...]:
        """Return every receipt retained for a request identity."""
        raise NotImplementedError("a DecisionReceiptStore adapter is required")

    @abstractmethod
    def save(self, receipt: DecisionReceipt) -> None:
        """Durably persist an immutable receipt."""
        raise NotImplementedError("a DecisionReceiptStore adapter is required")
