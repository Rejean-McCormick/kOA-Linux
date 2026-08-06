"""Verified and bounded context used for governance evaluation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re
from typing import Iterable

from .decision import (
    DecisionClass,
    DomainValidationError,
    FrozenJson,
    _aware_datetime,
    _freeze_json,
    _matching_text,
    _required_text,
    _semantic_version,
    _thaw_json,
    _unique_texts,
    _CORRELATION_ID,
    _REQUEST_ID,
    _SIMPLE_ID,
)


_FACT_ID = re.compile(r"^fact\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")


class ContextClassification(StrEnum):
    """Supported classification labels for verified context values."""

    PUBLIC = "public"
    INTERNAL = "internal"
    PRIVATE = "private"
    RESTRICTED = "restricted"
    HIGHLY_RESTRICTED = "highly_restricted"


class MissingContextFact(DomainValidationError):
    """Raised when a rule asks for an unavailable or stale context fact."""


_REQUIRED_CONTEXT: dict[DecisionClass, frozenset[str]] = {
    DecisionClass.AUTHORIZATION: frozenset(
        {
            "fact.verified_requester",
            "fact.registered_action",
            "fact.target",
            "fact.scope",
            "fact.component_authority",
            "fact.profile_applicability",
        }
    ),
    DecisionClass.DISCLOSURE: frozenset(
        {
            "fact.source_owner",
            "fact.data_or_representation",
            "fact.destination",
            "fact.audience",
            "fact.purpose",
            "fact.applicable_consent",
            "fact.retention_or_use_constraints",
        }
    ),
    DecisionClass.CONSENT: frozenset(
        {
            "fact.subject",
            "fact.purpose",
            "fact.data_scope",
            "fact.recipient_or_use_domain",
            "fact.duration_or_closure_condition",
            "fact.revocation_state",
            "fact.evidence_obligations",
        }
    ),
    DecisionClass.PRIVILEGE: frozenset(
        {
            "fact.verified_requester",
            "fact.target_node_or_resource",
            "fact.exact_privileged_operation",
            "fact.profile",
            "fact.assurance_context",
            "fact.duration",
            "fact.evidence_requirements",
        }
    ),
    DecisionClass.EXCEPTION: frozenset(
        {
            "fact.exception_id",
            "fact.affected_requirement_or_lock",
            "fact.subject",
            "fact.scope",
            "fact.activation_condition",
            "fact.expiration_or_closure_condition",
            "fact.compensating_controls",
            "fact.evidence_obligations",
        }
    ),
}


@dataclass(frozen=True, slots=True)
class VerifiedContextFact:
    """One minimized fact with explicit authority, verification and freshness."""

    name: str
    value: FrozenJson
    source_authority_ref: str
    evidence_ref: str
    verified_at: datetime
    classification: ContextClassification = ContextClassification.INTERNAL
    valid_until: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _matching_text(self.name, "name", _FACT_ID))
        object.__setattr__(self, "value", _freeze_json(self.value, f"fact {self.name}"))
        object.__setattr__(
            self,
            "source_authority_ref",
            _required_text(self.source_authority_ref, "source_authority_ref"),
        )
        object.__setattr__(
            self,
            "evidence_ref",
            _required_text(self.evidence_ref, "evidence_ref"),
        )
        verified_at = _aware_datetime(self.verified_at, "verified_at")
        object.__setattr__(self, "verified_at", verified_at)
        try:
            classification = ContextClassification(self.classification)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("classification is not registered") from exc
        object.__setattr__(self, "classification", classification)
        if self.valid_until is not None:
            valid_until = _aware_datetime(self.valid_until, "valid_until")
            if valid_until <= verified_at:
                raise DomainValidationError("valid_until must be later than verified_at")
            object.__setattr__(self, "valid_until", valid_until)

    def is_valid_at(self, instant: datetime) -> bool:
        instant = _aware_datetime(instant, "instant")
        return self.verified_at <= instant and (
            self.valid_until is None or instant < self.valid_until
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "value": _thaw_json(self.value),
            "source_authority_ref": self.source_authority_ref,
            "evidence_ref": self.evidence_ref,
            "verified_at": self.verified_at.isoformat(),
            "classification": self.classification.value,
            "valid_until": self.valid_until.isoformat() if self.valid_until else None,
        }


@dataclass(frozen=True, slots=True)
class EvaluationContext:
    """Complete bounded context for one policy request.

    Facts must be declared by the active policy contract, include the mandatory
    fields for the selected decision class, and be valid at request time.
    """

    request_id: str
    correlation_id: str
    decision_class: DecisionClass
    requester_ref: str
    action_ref: str
    target_ref: str
    scope_refs: tuple[str, ...]
    policy_set_ref: str
    authority_version: str
    requested_at: datetime
    allowed_fact_names: frozenset[str]
    facts: tuple[VerifiedContextFact, ...]
    exception_ids: tuple[str, ...] = ()
    prior_receipt_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_id",
            _matching_text(self.request_id, "request_id", _REQUEST_ID),
        )
        object.__setattr__(
            self,
            "correlation_id",
            _matching_text(self.correlation_id, "correlation_id", _CORRELATION_ID),
        )
        try:
            decision_class = DecisionClass(self.decision_class)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("decision_class is not registered") from exc
        object.__setattr__(self, "decision_class", decision_class)
        object.__setattr__(
            self,
            "requester_ref",
            _required_text(self.requester_ref, "requester_ref"),
        )
        object.__setattr__(self, "action_ref", _required_text(self.action_ref, "action_ref"))
        object.__setattr__(self, "target_ref", _required_text(self.target_ref, "target_ref"))
        object.__setattr__(
            self,
            "scope_refs",
            _unique_texts(self.scope_refs, "scope_refs", required=True),
        )
        object.__setattr__(
            self,
            "policy_set_ref",
            _required_text(self.policy_set_ref, "policy_set_ref"),
        )
        object.__setattr__(
            self,
            "authority_version",
            _semantic_version(self.authority_version, "authority_version"),
        )
        requested_at = _aware_datetime(self.requested_at, "requested_at")
        object.__setattr__(self, "requested_at", requested_at)

        allowed_names = frozenset(
            _matching_text(name, "allowed_fact_names", _FACT_ID)
            for name in self.allowed_fact_names
        )
        required_names = _REQUIRED_CONTEXT[decision_class]
        missing_declarations = required_names - allowed_names
        if missing_declarations:
            raise DomainValidationError(
                "allowed_fact_names omits required context: "
                + ", ".join(sorted(missing_declarations))
            )
        object.__setattr__(self, "allowed_fact_names", allowed_names)

        facts = tuple(self.facts)
        if not all(isinstance(fact, VerifiedContextFact) for fact in facts):
            raise DomainValidationError("facts must contain VerifiedContextFact values")
        fact_names = [fact.name for fact in facts]
        if len(set(fact_names)) != len(fact_names):
            raise DomainValidationError("facts must not contain duplicate names")
        undeclared = set(fact_names) - allowed_names
        if undeclared:
            raise DomainValidationError(
                "evaluation context contains undeclared facts: "
                + ", ".join(sorted(undeclared))
            )
        missing_required = required_names - set(fact_names)
        if missing_required:
            raise DomainValidationError(
                "evaluation context is missing required facts: "
                + ", ".join(sorted(missing_required))
            )
        stale = [fact.name for fact in facts if not fact.is_valid_at(requested_at)]
        if stale:
            raise DomainValidationError(
                "evaluation context contains stale or not-yet-valid facts: "
                + ", ".join(sorted(stale))
            )
        object.__setattr__(self, "facts", tuple(sorted(facts, key=lambda fact: fact.name)))
        object.__setattr__(
            self,
            "exception_ids",
            _unique_texts(self.exception_ids, "exception_ids"),
        )
        object.__setattr__(
            self,
            "prior_receipt_refs",
            _unique_texts(self.prior_receipt_refs, "prior_receipt_refs"),
        )

    @classmethod
    def required_fact_names(cls, decision_class: DecisionClass) -> frozenset[str]:
        try:
            normalized = DecisionClass(decision_class)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("decision_class is not registered") from exc
        return _REQUIRED_CONTEXT[normalized]

    def fact(self, name: str, *, at: datetime | None = None) -> VerifiedContextFact:
        normalized_name = _matching_text(name, "name", _FACT_ID)
        instant = self.requested_at if at is None else _aware_datetime(at, "at")
        for fact in self.facts:
            if fact.name == normalized_name:
                if not fact.is_valid_at(instant):
                    raise MissingContextFact(f"context fact {normalized_name} is stale")
                return fact
        raise MissingContextFact(f"context fact {normalized_name} is missing")

    def value(self, name: str, *, at: datetime | None = None) -> FrozenJson:
        return self.fact(name, at=at).value

    @property
    def verified_context_refs(self) -> tuple[str, ...]:
        return tuple(sorted({fact.evidence_ref for fact in self.facts}))

    def as_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "decision_class": self.decision_class.value,
            "requester_ref": self.requester_ref,
            "action_ref": self.action_ref,
            "target_ref": self.target_ref,
            "scope_refs": list(self.scope_refs),
            "policy_set_ref": self.policy_set_ref,
            "authority_version": self.authority_version,
            "requested_at": self.requested_at.isoformat(),
            "allowed_fact_names": sorted(self.allowed_fact_names),
            "facts": [fact.as_dict() for fact in self.facts],
            "exception_ids": list(self.exception_ids),
            "prior_receipt_refs": list(self.prior_receipt_refs),
        }
