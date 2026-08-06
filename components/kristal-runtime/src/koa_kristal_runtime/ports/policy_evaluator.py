"""Governance Policy Runtime client port."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Protocol

PolicyOutcome = Literal["allow", "deny", "blocked"]


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    outcome: PolicyOutcome
    decision_id: str
    policy_ref: str
    receipt_ref: str
    obligations: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    reason_code: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "obligations", MappingProxyType(dict(self.obligations)))


class PolicyEvaluator(Protocol):
    def evaluate(
        self,
        action: str,
        actor_context: Mapping[str, Any],
        resource: Mapping[str, Any],
        context: Mapping[str, Any],
    ) -> PolicyDecision:
        raise NotImplementedError
