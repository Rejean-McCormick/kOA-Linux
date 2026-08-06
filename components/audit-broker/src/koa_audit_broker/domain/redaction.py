"""Declarative, policy-bound disclosure transformation profiles."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable

from .audit_event import DomainValidationError
from .evidence_scope import EvidenceScope


class DisclosureTechnique(StrEnum):
    """Declared techniques used to minimize audit disclosure output."""

    FIELD_PROJECTION = "field_projection"
    REDACTION = "redaction"
    PSEUDONYMIZATION = "pseudonymization"
    AGGREGATION = "aggregation"
    PRIVATE_PROOF = "private_proof"


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainValidationError(f"{field_name} must be a non-empty string")
    return value.strip()


def _references(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise DomainValidationError(f"{field_name} must be an iterable of references")
    normalized = tuple(sorted({_required_text(value, field_name) for value in values}))
    return normalized


def _aware_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


@dataclass(frozen=True, slots=True)
class RedactionRule:
    """One deterministic instruction bound to a single authorized source field."""

    source_field: str
    technique: DisclosureTechnique
    reason_code: str
    parameter_references: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "source_field",
            _required_text(self.source_field, "source_field"),
        )
        try:
            technique = DisclosureTechnique(self.technique)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("technique is not a declared disclosure technique") from exc
        object.__setattr__(self, "technique", technique)
        object.__setattr__(
            self,
            "reason_code",
            _required_text(self.reason_code, "reason_code"),
        )
        object.__setattr__(
            self,
            "parameter_references",
            _references(self.parameter_references, "parameter_references"),
        )


@dataclass(frozen=True, slots=True)
class RedactionProfile:
    """Immutable transformation plan constrained by a policy decision and scope.

    The profile contains references to transformation parameters, never secret values or
    protected source payloads. Execution belongs to the application layer; the domain
    object validates that the plan cannot select undeclared fields or outlive authority.
    """

    profile_id: str
    policy_decision_ref: str
    purpose: str
    field_allowlist: frozenset[str]
    rules: tuple[RedactionRule, ...]
    valid_until: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "profile_id", _required_text(self.profile_id, "profile_id"))
        object.__setattr__(
            self,
            "policy_decision_ref",
            _required_text(self.policy_decision_ref, "policy_decision_ref"),
        )
        object.__setattr__(self, "purpose", _required_text(self.purpose, "purpose"))

        if isinstance(self.field_allowlist, (str, bytes)):
            raise DomainValidationError("field_allowlist must be an iterable of field names")
        fields = frozenset(
            _required_text(field_name, "field_allowlist")
            for field_name in self.field_allowlist
        )
        if not fields:
            raise DomainValidationError("field_allowlist must not be empty")
        object.__setattr__(self, "field_allowlist", fields)

        rules = tuple(self.rules)
        if not all(isinstance(rule, RedactionRule) for rule in rules):
            raise DomainValidationError("rules must contain only RedactionRule values")
        keys = [(rule.source_field, rule.technique.value) for rule in rules]
        if len(keys) != len(set(keys)):
            raise DomainValidationError("duplicate redaction rules are not allowed")
        outside = sorted({rule.source_field for rule in rules} - fields)
        if outside:
            raise DomainValidationError(
                "redaction rules reference fields outside field_allowlist: "
                + ", ".join(outside)
            )
        object.__setattr__(self, "rules", tuple(sorted(rules, key=lambda rule: (rule.source_field, rule.technique.value))))
        object.__setattr__(
            self,
            "valid_until",
            _aware_datetime(self.valid_until, "valid_until"),
        )

    def validate_against(self, scope: EvidenceScope) -> None:
        """Fail closed if the profile exceeds its authorized evidence scope."""

        if self.purpose != scope.purpose:
            raise DomainValidationError("redaction profile purpose must match evidence scope")
        if not self.field_allowlist <= scope.field_allowlist:
            raise DomainValidationError(
                "redaction profile field_allowlist must not broaden evidence scope"
            )
        if self.valid_until > scope.expires_at:
            raise DomainValidationError(
                "redaction profile validity must not outlive evidence scope"
            )

    def rules_for(self, field_name: str) -> tuple[RedactionRule, ...]:
        """Return deterministic instructions for an authorized field."""

        normalized = _required_text(field_name, "field_name")
        if normalized not in self.field_allowlist:
            raise DomainValidationError("field is outside the redaction profile allowlist")
        return tuple(rule for rule in self.rules if rule.source_field == normalized)

    def as_dict(self) -> dict[str, object]:
        """Return a deterministic serialization-ready representation."""

        return {
            "profile_id": self.profile_id,
            "policy_decision_ref": self.policy_decision_ref,
            "purpose": self.purpose,
            "field_allowlist": sorted(self.field_allowlist),
            "rules": [
                {
                    "source_field": rule.source_field,
                    "technique": rule.technique.value,
                    "reason_code": rule.reason_code,
                    "parameter_references": list(rule.parameter_references),
                }
                for rule in self.rules
            ],
            "valid_until": self.valid_until.isoformat(),
        }
