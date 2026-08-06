"""Governance Policy Runtime boundary for publication decisions."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class PolicyOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True, slots=True)
class PolicyObligation:
    obligation_type: str
    parameters: Mapping[str, Any]
    required: bool = True


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    decision_id: str
    outcome: PolicyOutcome
    issued_at: datetime
    expires_at: datetime
    policy_set_ref: str
    obligations: tuple[PolicyObligation, ...] = ()
    reason_codes: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()


@runtime_checkable
class PolicyRuntime(Protocol):
    """Evaluate minimum publication context without receiving source payloads."""

    @abstractmethod
    def evaluate(
        self,
        context: Mapping[str, Any],
        *,
        evaluated_at: datetime,
    ) -> PolicyDecision:
        """Return one closed publication decision and enforceable obligations."""
        raise NotImplementedError("a PolicyRuntime adapter is required")
