"""Immutable governance decision values and invariants."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import math
import re
from typing import Iterable, Mapping, TypeAlias


class DomainValidationError(ValueError):
    """Raised when a governance domain value violates a declared invariant."""


class DecisionClass(StrEnum):
    """Decision classes owned by Governance Policy Runtime."""

    AUTHORIZATION = "authorization"
    DISCLOSURE = "disclosure"
    CONSENT = "consent"
    PRIVILEGE = "privilege"
    EXCEPTION = "exception"


class DecisionResult(StrEnum):
    """Observable policy-evaluation results from the component contract."""

    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


class ObligationType(StrEnum):
    """Registered obligation categories returned to enforcing callers."""

    DATA_MINIMIZATION = "data_minimization"
    DESTINATION_RESTRICTION = "destination_restriction"
    SECONDARY_APPROVAL = "secondary_approval"
    DURATION_LIMIT = "duration_limit"
    PRIVILEGED_EXECUTION_PATH = "privileged_execution_path"
    AUDIT_EVIDENCE = "audit_evidence"
    SUBJECT_NOTIFICATION = "subject_notification"
    COMPENSATING_CONTROL = "compensating_control"
    FOLLOW_UP_REVIEW = "follow_up_review"
    RETENTION_LIMIT = "retention_limit"
    RECEIPT_LINKAGE = "receipt_linkage"
    RE_EVALUATION_BEFORE_EXECUTION = "re_evaluation_before_execution"


class DiagnosticSeverity(StrEnum):
    """Stable diagnostic severities for policy evaluation."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


JsonScalar: TypeAlias = None | bool | int | float | str


@dataclass(frozen=True, slots=True)
class FrozenObject:
    """Deterministically ordered immutable representation of a JSON object."""

    items: tuple[tuple[str, "FrozenJson"], ...]


FrozenJson: TypeAlias = JsonScalar | tuple["FrozenJson", ...] | FrozenObject

_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
_SIMPLE_ID = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_REASON_CODE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")
_REQUEST_ID = re.compile(r"^POLREQ-[A-Z0-9-]{8,}$")
_CORRELATION_ID = re.compile(r"^CORR-[A-Z0-9-]{8,}$")
_OBLIGATION_ID = re.compile(r"^obligation\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise DomainValidationError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise DomainValidationError(f"{field_name} must not be empty")
    if any(ord(character) < 32 for character in normalized):
        raise DomainValidationError(f"{field_name} must not contain control characters")
    return normalized


def _matching_text(value: str, field_name: str, pattern: re.Pattern[str]) -> str:
    normalized = _required_text(value, field_name)
    if pattern.fullmatch(normalized) is None:
        raise DomainValidationError(f"{field_name} has an invalid format")
    return normalized


def _semantic_version(value: str, field_name: str) -> str:
    return _matching_text(value, field_name, _SEMVER)


def _aware_datetime(value: datetime, field_name: str) -> datetime:
    if not isinstance(value, datetime):
        raise DomainValidationError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise DomainValidationError(f"{field_name} must include a timezone")
    return value


def _unique_texts(
    values: Iterable[str],
    field_name: str,
    *,
    required: bool = False,
    pattern: re.Pattern[str] | None = None,
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise DomainValidationError(f"{field_name} must be an iterable of strings")
    normalized = tuple(
        _matching_text(value, field_name, pattern)
        if pattern is not None
        else _required_text(value, field_name)
        for value in values
    )
    if required and not normalized:
        raise DomainValidationError(f"{field_name} must contain at least one value")
    if len(set(normalized)) != len(normalized):
        raise DomainValidationError(f"{field_name} must not contain duplicates")
    return tuple(sorted(normalized))


def _freeze_json(value: object, field_name: str = "value") -> FrozenJson:
    if isinstance(value, FrozenObject):
        return value
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DomainValidationError(f"{field_name} must not contain non-finite numbers")
        return value
    if isinstance(value, datetime):
        return _aware_datetime(value, field_name).isoformat()
    if isinstance(value, Mapping):
        frozen_items: list[tuple[str, FrozenJson]] = []
        for key, nested in value.items():
            normalized_key = _required_text(key, f"{field_name} key")
            frozen_items.append((normalized_key, _freeze_json(nested, field_name)))
        keys = [key for key, _ in frozen_items]
        if len(set(keys)) != len(keys):
            raise DomainValidationError(f"{field_name} must not contain duplicate keys")
        return FrozenObject(tuple(sorted(frozen_items, key=lambda item: item[0])))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if isinstance(value, (set, frozenset)):
        frozen = tuple(_freeze_json(item, field_name) for item in value)
        return tuple(sorted(frozen, key=repr))
    raise DomainValidationError(f"{field_name} must be JSON-compatible")


def _thaw_json(value: FrozenJson) -> object:
    if isinstance(value, FrozenObject):
        return {key: _thaw_json(nested) for key, nested in value.items}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class PolicyObligation:
    """A bounded condition the enforcing caller must satisfy."""

    obligation_id: str
    obligation_type: ObligationType
    enforcement_owner: str
    description: str
    parameters: FrozenJson = FrozenObject(())
    evidence_requirement_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "obligation_id",
            _matching_text(self.obligation_id, "obligation_id", _OBLIGATION_ID),
        )
        try:
            obligation_type = ObligationType(self.obligation_type)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("obligation_type is not registered") from exc
        object.__setattr__(self, "obligation_type", obligation_type)
        object.__setattr__(
            self,
            "enforcement_owner",
            _required_text(self.enforcement_owner, "enforcement_owner"),
        )
        object.__setattr__(
            self,
            "description",
            _required_text(self.description, "description"),
        )
        object.__setattr__(
            self,
            "parameters",
            _freeze_json(self.parameters, "parameters"),
        )
        object.__setattr__(
            self,
            "evidence_requirement_refs",
            _unique_texts(
                self.evidence_requirement_refs,
                "evidence_requirement_refs",
            ),
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "obligation_id": self.obligation_id,
            "obligation_type": self.obligation_type.value,
            "enforcement_owner": self.enforcement_owner,
            "description": self.description,
            "parameters": _thaw_json(self.parameters),
            "evidence_requirement_refs": list(self.evidence_requirement_refs),
        }


@dataclass(frozen=True, slots=True)
class DecisionDiagnostic:
    """Machine-readable reason or failure diagnostic for a decision."""

    code: str
    severity: DiagnosticSeverity
    message: str
    reference_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _matching_text(self.code, "code", _REASON_CODE))
        try:
            severity = DiagnosticSeverity(self.severity)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("severity is not registered") from exc
        object.__setattr__(self, "severity", severity)
        object.__setattr__(self, "message", _required_text(self.message, "message"))
        object.__setattr__(
            self,
            "reference_ids",
            _unique_texts(self.reference_ids, "reference_ids"),
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
            "reference_ids": list(self.reference_ids),
        }


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    """Authoritative result of one bounded policy evaluation.

    This value is evaluation evidence only. It is not an execution credential and
    does not mutate the caller's state.
    """

    request_id: str
    correlation_id: str
    decision_class: DecisionClass
    result: DecisionResult
    policy_set_ref: str
    authority_version: str
    evaluated_at: datetime
    evaluator_identity: str
    evaluator_version: str
    rule_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]
    obligations: tuple[PolicyObligation, ...] = ()
    diagnostics: tuple[DecisionDiagnostic, ...] = ()
    review_requirement_ids: tuple[str, ...] = ()
    verified_context_refs: tuple[str, ...] = ()
    exception_ids: tuple[str, ...] = ()

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
        try:
            result = DecisionResult(self.result)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("result is not a registered decision result") from exc
        object.__setattr__(self, "result", result)
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
        object.__setattr__(
            self,
            "evaluated_at",
            _aware_datetime(self.evaluated_at, "evaluated_at"),
        )
        object.__setattr__(
            self,
            "evaluator_identity",
            _required_text(self.evaluator_identity, "evaluator_identity"),
        )
        object.__setattr__(
            self,
            "evaluator_version",
            _semantic_version(self.evaluator_version, "evaluator_version"),
        )
        object.__setattr__(
            self,
            "rule_ids",
            _unique_texts(self.rule_ids, "rule_ids", required=True),
        )
        object.__setattr__(
            self,
            "reason_codes",
            _unique_texts(
                self.reason_codes,
                "reason_codes",
                required=True,
                pattern=_REASON_CODE,
            ),
        )

        obligations = tuple(self.obligations)
        if not all(isinstance(item, PolicyObligation) for item in obligations):
            raise DomainValidationError("obligations must contain PolicyObligation values")
        obligation_ids = [item.obligation_id for item in obligations]
        if len(set(obligation_ids)) != len(obligation_ids):
            raise DomainValidationError("obligations must not contain duplicate identifiers")
        object.__setattr__(
            self,
            "obligations",
            tuple(sorted(obligations, key=lambda item: item.obligation_id)),
        )

        diagnostics = tuple(self.diagnostics)
        if not all(isinstance(item, DecisionDiagnostic) for item in diagnostics):
            raise DomainValidationError("diagnostics must contain DecisionDiagnostic values")
        diagnostic_codes = [item.code for item in diagnostics]
        if len(set(diagnostic_codes)) != len(diagnostic_codes):
            raise DomainValidationError("diagnostics must not contain duplicate codes")
        object.__setattr__(
            self,
            "diagnostics",
            tuple(sorted(diagnostics, key=lambda item: item.code)),
        )
        object.__setattr__(
            self,
            "review_requirement_ids",
            _unique_texts(self.review_requirement_ids, "review_requirement_ids"),
        )
        object.__setattr__(
            self,
            "verified_context_refs",
            _unique_texts(self.verified_context_refs, "verified_context_refs"),
        )
        object.__setattr__(
            self,
            "exception_ids",
            _unique_texts(self.exception_ids, "exception_ids"),
        )

        if result is DecisionResult.ALLOW and self.review_requirement_ids:
            raise DomainValidationError("allow must not retain unresolved review requirements")
        if result is DecisionResult.BLOCKED:
            has_failure_diagnostic = any(
                item.severity in {DiagnosticSeverity.ERROR, DiagnosticSeverity.CRITICAL}
                for item in diagnostics
            )
            if not has_failure_diagnostic and not self.review_requirement_ids:
                raise DomainValidationError(
                    "blocked requires an error diagnostic or review requirement"
                )

    @property
    def permits_execution(self) -> bool:
        """Return whether policy permits the exact declared request.

        The caller must still validate correlation, scope, authority version and all
        obligations before executing anything.
        """

        return self.result is DecisionResult.ALLOW

    def as_dict(self) -> dict[str, object]:
        return {
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "decision_class": self.decision_class.value,
            "result": self.result.value,
            "policy_set_ref": self.policy_set_ref,
            "authority_version": self.authority_version,
            "evaluated_at": self.evaluated_at.isoformat(),
            "evaluator_identity": self.evaluator_identity,
            "evaluator_version": self.evaluator_version,
            "rule_ids": list(self.rule_ids),
            "reason_codes": list(self.reason_codes),
            "obligations": [item.as_dict() for item in self.obligations],
            "diagnostics": [item.as_dict() for item in self.diagnostics],
            "review_requirement_ids": list(self.review_requirement_ids),
            "verified_context_refs": list(self.verified_context_refs),
            "exception_ids": list(self.exception_ids),
        }
