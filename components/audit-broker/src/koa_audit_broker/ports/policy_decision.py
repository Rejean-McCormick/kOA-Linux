"""Governance Policy Runtime port for selective audit operations."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Mapping, Protocol, TypeAlias, runtime_checkable

from .identity_context import IdentityReference

SelectorValue: TypeAlias = str | tuple[str, ...]
Selectors: TypeAlias = Mapping[str, SelectorValue]


class PolicyOutcome(StrEnum):
    """Closed policy outcomes consumed by Audit Broker."""

    ALLOWED = "allowed"
    PARTIALLY_ALLOWED = "partially_allowed"
    DENIED = "denied"
    EXPIRED = "expired"
    UNAVAILABLE = "unavailable"


class FieldAction(StrEnum):
    """Authorized transformation for one disclosed field."""

    INCLUDE = "include"
    REDACT = "redact"
    PSEUDONYMIZE = "pseudonymize"


@dataclass(frozen=True, slots=True)
class DisclosureAuthorizationRequest:
    request_id: str
    requester_identity: IdentityReference
    requester_identity_ref: str
    purpose: str
    requested_scope: tuple[str, ...]
    selectors: Selectors
    requested_fields: tuple[str, ...]
    desired_output_class: str
    expires_at: datetime
    requested_limit: int


@dataclass(frozen=True, slots=True)
class RetentionAuthorizationRequest:
    request_id: str
    requester_identity: IdentityReference
    requester_identity_ref: str
    purpose: str
    selectors: Selectors
    action: str
    policy_or_hold_ref: str
    effective_at: datetime


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Scope-bound decision; Audit Broker may only narrow it."""

    decision_ref: str
    outcome: PolicyOutcome
    purpose: str
    effective_scope: tuple[str, ...] = ()
    effective_selectors: Selectors = field(default_factory=dict)
    field_actions: Mapping[str, FieldAction] = field(default_factory=dict)
    maximum_records: int = 0
    valid_until: datetime | None = None
    consent_ref: str | None = None
    rights_refs: tuple[str, ...] = ()
    exception_refs: tuple[str, ...] = ()
    obligations: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()
    redaction_profile: str | None = None

    @property
    def permits_work(self) -> bool:
        return self.outcome in {PolicyOutcome.ALLOWED, PolicyOutcome.PARTIALLY_ALLOWED}


@runtime_checkable
class PolicyDecisionPort(Protocol):
    """Requests decisions from Governance Policy Runtime."""

    @abstractmethod
    def authorize_disclosure(
        self, request: DisclosureAuthorizationRequest, *, at: datetime
    ) -> PolicyDecision:
        """Authorize a bounded audit query or evidence package."""
        raise NotImplementedError("a PolicyDecision adapter is required")

    @abstractmethod
    def authorize_retention(
        self, request: RetentionAuthorizationRequest, *, at: datetime
    ) -> PolicyDecision:
        """Authorize a bounded retention or hold transition."""
        raise NotImplementedError("a PolicyDecision adapter is required")
