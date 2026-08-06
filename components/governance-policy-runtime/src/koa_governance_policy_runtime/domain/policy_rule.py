"""Deterministic policy-rule expressions and decisions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
import re
from typing import Final

from .decision import (
    DecisionResult,
    DomainValidationError,
    FrozenJson,
    _aware_datetime,
    _freeze_json,
    _matching_text,
    _required_text,
    _semantic_version,
    _thaw_json,
    _unique_texts,
    _REASON_CODE,
    _SIMPLE_ID,
)
from .evaluation_context import EvaluationContext


class RuleOutcome(StrEnum):
    """Outcomes declared by policy-bundle rules."""

    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_REVIEW = "require_review"

    @property
    def runtime_result(self) -> DecisionResult:
        if self is RuleOutcome.ALLOW:
            return DecisionResult.ALLOW
        if self is RuleOutcome.DENY:
            return DecisionResult.DENY
        return DecisionResult.BLOCKED


class CompareOperator(StrEnum):
    EQ = "eq"
    NE = "ne"
    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"


_UNSET: Final = object()
_FACT_ID = re.compile(r"^fact\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_POLICY_RULE_ID = re.compile(r"^policy-rule\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_OBLIGATION_ID = re.compile(r"^obligation\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_REVIEW_ID = re.compile(r"^review\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")


@dataclass(frozen=True, slots=True)
class Operand:
    """A fact reference or literal operand, never both."""

    fact_ref: str | None = None
    literal: object = _UNSET

    def __post_init__(self) -> None:
        has_fact = self.fact_ref is not None
        has_literal = self.literal is not _UNSET
        if has_fact == has_literal:
            raise DomainValidationError("operand must define exactly one of fact_ref or literal")
        if has_fact:
            object.__setattr__(
                self,
                "fact_ref",
                _matching_text(self.fact_ref or "", "fact_ref", _FACT_ID),
            )
        else:
            object.__setattr__(self, "literal", _freeze_json(self.literal, "literal"))

    def resolve(self, context: EvaluationContext, *, at: datetime | None = None) -> FrozenJson:
        if self.fact_ref is not None:
            return context.value(self.fact_ref, at=at)
        return self.literal  # type: ignore[return-value]

    def as_dict(self) -> dict[str, object]:
        if self.fact_ref is not None:
            return {"fact_ref": self.fact_ref}
        return {"literal": _thaw_json(self.literal)}  # type: ignore[arg-type]


class Expression(ABC):
    """Base protocol for side-effect-free policy expressions."""

    @abstractmethod
    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def as_dict(self) -> dict[str, object]:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class AllExpression(Expression):
    expressions: tuple[Expression, ...]

    def __post_init__(self) -> None:
        expressions = tuple(self.expressions)
        if not expressions or not all(isinstance(item, Expression) for item in expressions):
            raise DomainValidationError("all expression requires one or more expressions")
        object.__setattr__(self, "expressions", expressions)

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        return all(item.evaluate(context, at=at) for item in self.expressions)

    def as_dict(self) -> dict[str, object]:
        return {"all": [item.as_dict() for item in self.expressions]}


@dataclass(frozen=True, slots=True)
class AnyExpression(Expression):
    expressions: tuple[Expression, ...]

    def __post_init__(self) -> None:
        expressions = tuple(self.expressions)
        if not expressions or not all(isinstance(item, Expression) for item in expressions):
            raise DomainValidationError("any expression requires one or more expressions")
        object.__setattr__(self, "expressions", expressions)

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        return any(item.evaluate(context, at=at) for item in self.expressions)

    def as_dict(self) -> dict[str, object]:
        return {"any": [item.as_dict() for item in self.expressions]}


@dataclass(frozen=True, slots=True)
class NotExpression(Expression):
    expression: Expression

    def __post_init__(self) -> None:
        if not isinstance(self.expression, Expression):
            raise DomainValidationError("not expression requires one expression")

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        return not self.expression.evaluate(context, at=at)

    def as_dict(self) -> dict[str, object]:
        return {"not": self.expression.as_dict()}


@dataclass(frozen=True, slots=True)
class ExistsExpression(Expression):
    fact_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "fact_ref",
            _matching_text(self.fact_ref, "fact_ref", _FACT_ID),
        )

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        try:
            context.fact(self.fact_ref, at=at)
        except DomainValidationError:
            return False
        return True

    def as_dict(self) -> dict[str, object]:
        return {"exists": self.fact_ref}


@dataclass(frozen=True, slots=True)
class CompareExpression(Expression):
    left: Operand
    operator: CompareOperator
    right: Operand

    def __post_init__(self) -> None:
        if not isinstance(self.left, Operand) or not isinstance(self.right, Operand):
            raise DomainValidationError("compare operands must be Operand values")
        try:
            operator = CompareOperator(self.operator)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("compare operator is not registered") from exc
        object.__setattr__(self, "operator", operator)

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        left = self.left.resolve(context, at=at)
        right = self.right.resolve(context, at=at)
        try:
            if self.operator is CompareOperator.EQ:
                return left == right
            if self.operator is CompareOperator.NE:
                return left != right
            if self.operator is CompareOperator.LT:
                return left < right  # type: ignore[operator]
            if self.operator is CompareOperator.LTE:
                return left <= right  # type: ignore[operator]
            if self.operator is CompareOperator.GT:
                return left > right  # type: ignore[operator]
            return left >= right  # type: ignore[operator]
        except TypeError as exc:
            raise DomainValidationError("compare operands are not order-compatible") from exc

    def as_dict(self) -> dict[str, object]:
        return {
            "compare": {
                "left": self.left.as_dict(),
                "operator": self.operator.value,
                "right": self.right.as_dict(),
            }
        }


@dataclass(frozen=True, slots=True)
class ContainsExpression(Expression):
    set_operand: Operand
    value_operand: Operand

    def __post_init__(self) -> None:
        if not isinstance(self.set_operand, Operand) or not isinstance(
            self.value_operand, Operand
        ):
            raise DomainValidationError("contains operands must be Operand values")

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        collection = self.set_operand.resolve(context, at=at)
        value = self.value_operand.resolve(context, at=at)
        if not isinstance(collection, tuple):
            raise DomainValidationError("contains set operand must resolve to a collection")
        return value in collection

    def as_dict(self) -> dict[str, object]:
        return {
            "contains": {
                "set": self.set_operand.as_dict(),
                "value": self.value_operand.as_dict(),
            }
        }


@dataclass(frozen=True, slots=True)
class MatchesExpression(Expression):
    value_operand: Operand
    pattern: str

    def __post_init__(self) -> None:
        if not isinstance(self.value_operand, Operand):
            raise DomainValidationError("matches value must be an Operand")
        pattern = _required_text(self.pattern, "pattern")
        if len(pattern) > 500:
            raise DomainValidationError("pattern must not exceed 500 characters")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise DomainValidationError("pattern is not a valid regular expression") from exc
        object.__setattr__(self, "pattern", pattern)

    def evaluate(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        value = self.value_operand.resolve(context, at=at)
        if not isinstance(value, str):
            raise DomainValidationError("matches operand must resolve to a string")
        return re.search(self.pattern, value) is not None

    def as_dict(self) -> dict[str, object]:
        return {
            "matches": {
                "value": self.value_operand.as_dict(),
                "pattern": self.pattern,
            }
        }


@dataclass(frozen=True, slots=True)
class RuleDecision:
    """Deterministic decision produced when a policy rule matches."""

    outcome: RuleOutcome
    reason_codes: tuple[str, ...]
    obligation_ids: tuple[str, ...] = ()
    review_requirement_id: str | None = None
    decision_validity_seconds: int | None = None

    def __post_init__(self) -> None:
        try:
            outcome = RuleOutcome(self.outcome)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("outcome is not registered") from exc
        object.__setattr__(self, "outcome", outcome)
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
        object.__setattr__(
            self,
            "obligation_ids",
            _unique_texts(
                self.obligation_ids,
                "obligation_ids",
                pattern=_OBLIGATION_ID,
            ),
        )
        if self.review_requirement_id is not None:
            object.__setattr__(
                self,
                "review_requirement_id",
                _matching_text(
                    self.review_requirement_id,
                    "review_requirement_id",
                    _REVIEW_ID,
                ),
            )
        if outcome is RuleOutcome.REQUIRE_REVIEW and self.review_requirement_id is None:
            raise DomainValidationError(
                "require_review requires review_requirement_id"
            )
        if outcome is not RuleOutcome.REQUIRE_REVIEW and self.review_requirement_id is not None:
            raise DomainValidationError(
                "review_requirement_id is only valid for require_review"
            )
        if self.decision_validity_seconds is not None:
            if (
                not isinstance(self.decision_validity_seconds, int)
                or isinstance(self.decision_validity_seconds, bool)
                or self.decision_validity_seconds < 0
            ):
                raise DomainValidationError(
                    "decision_validity_seconds must be a non-negative integer"
                )

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "outcome": self.outcome.value,
            "reason_codes": list(self.reason_codes),
            "obligation_ids": list(self.obligation_ids),
        }
        if self.review_requirement_id is not None:
            result["review_requirement_id"] = self.review_requirement_id
        if self.decision_validity_seconds is not None:
            result["decision_validity_seconds"] = self.decision_validity_seconds
        return result


@dataclass(frozen=True, slots=True)
class PolicyRule:
    """One immutable, side-effect-free policy rule."""

    rule_id: str
    version: str
    title: str
    description: str
    priority: int
    when: Expression
    decision: RuleDecision
    enabled: bool = True
    effective_from: datetime | None = None
    expires_at: datetime | None = None
    supersedes_rule_refs: tuple[str, ...] = ()
    evidence_requirement_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "rule_id",
            _matching_text(self.rule_id, "rule_id", _POLICY_RULE_ID),
        )
        object.__setattr__(self, "version", _semantic_version(self.version, "version"))
        object.__setattr__(self, "title", _required_text(self.title, "title"))
        object.__setattr__(
            self,
            "description",
            _required_text(self.description, "description"),
        )
        if (
            not isinstance(self.priority, int)
            or isinstance(self.priority, bool)
            or self.priority < 0
        ):
            raise DomainValidationError("priority must be a non-negative integer")
        if not isinstance(self.when, Expression):
            raise DomainValidationError("when must be an Expression")
        if not isinstance(self.decision, RuleDecision):
            raise DomainValidationError("decision must be a RuleDecision")
        if not isinstance(self.enabled, bool):
            raise DomainValidationError("enabled must be a boolean")
        effective_from = None
        if self.effective_from is not None:
            effective_from = _aware_datetime(self.effective_from, "effective_from")
            object.__setattr__(self, "effective_from", effective_from)
        if self.expires_at is not None:
            expires_at = _aware_datetime(self.expires_at, "expires_at")
            if effective_from is not None and expires_at <= effective_from:
                raise DomainValidationError("expires_at must be later than effective_from")
            object.__setattr__(self, "expires_at", expires_at)
        object.__setattr__(
            self,
            "supersedes_rule_refs",
            _unique_texts(
                self.supersedes_rule_refs,
                "supersedes_rule_refs",
                pattern=_POLICY_RULE_ID,
            ),
        )
        if self.rule_id in self.supersedes_rule_refs:
            raise DomainValidationError("a rule must not supersede itself")
        object.__setattr__(
            self,
            "evidence_requirement_refs",
            _unique_texts(
                self.evidence_requirement_refs,
                "evidence_requirement_refs",
            ),
        )
        object.__setattr__(
            self,
            "tags",
            _unique_texts(self.tags, "tags", pattern=_SIMPLE_ID),
        )

    def is_effective_at(self, instant: datetime) -> bool:
        instant = _aware_datetime(instant, "instant")
        if not self.enabled:
            return False
        if self.effective_from is not None and instant < self.effective_from:
            return False
        return self.expires_at is None or instant < self.expires_at

    def matches(self, context: EvaluationContext, *, at: datetime | None = None) -> bool:
        instant = context.requested_at if at is None else _aware_datetime(at, "at")
        return self.is_effective_at(instant) and self.when.evaluate(context, at=instant)

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "rule_id": self.rule_id,
            "version": self.version,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "when": self.when.as_dict(),
            "decision": self.decision.as_dict(),
            "enabled": self.enabled,
            "supersedes_rule_refs": list(self.supersedes_rule_refs),
            "evidence_requirement_refs": list(self.evidence_requirement_refs),
            "tags": list(self.tags),
        }
        if self.effective_from is not None:
            result["effective_from"] = self.effective_from.isoformat()
        if self.expires_at is not None:
            result["expires_at"] = self.expires_at.isoformat()
        return result
