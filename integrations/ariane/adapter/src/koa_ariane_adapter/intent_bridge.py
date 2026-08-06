"""Validation boundary for structured candidate intents.

Candidate intents are input only. They never carry authority, confirmation, or
permission to invoke a driver.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Mapping

from .client import JsonValue


class IntentSource(str, Enum):
    LOCAL_STRUCTURED_CONTROL = "local_structured_control"
    EXTERNAL_VOICE = "external_voice"


_PROHIBITED_CANDIDATE_FIELDS = {
    "authority_refs",
    "policy_decision_ref",
    "confirmation",
    "confirmed",
    "execute",
    "driver_operation",
    "credential",
    "token",
    "password",
    "secret",
}


@dataclass(frozen=True, slots=True)
class CandidateIntent:
    candidate_id: str
    source: IntentSource
    application_id: str
    goal_id: str
    created_at: datetime
    parameters: tuple[tuple[str, JsonValue], ...] = ()
    locale: str | None = None

    def __post_init__(self) -> None:
        for field in ("candidate_id", "application_id", "goal_id"):
            object.__setattr__(self, field, _required_text(getattr(self, field), field))
        object.__setattr__(self, "created_at", _utc(self.created_at, "created_at"))
        if self.locale is not None:
            object.__setattr__(self, "locale", _required_text(self.locale, "locale"))
        object.__setattr__(self, "parameters", _parameters(self.parameters))

    def ensure_fresh(self, *, now: datetime, max_age: timedelta) -> None:
        now = _utc(now, "now")
        if max_age <= timedelta(0) or max_age > timedelta(minutes=10):
            raise ValueError("max_age must be greater than zero and no more than ten minutes")
        if self.created_at > now:
            raise IntentRejected("ARIANE_INTENT_NOT_YET_VALID")
        if now - self.created_at > max_age:
            raise IntentRejected("ARIANE_INTENT_STALE")

    def to_dict(self) -> dict[str, JsonValue]:
        return {
            "candidate_id": self.candidate_id,
            "source": self.source.value,
            "application_id": self.application_id,
            "goal_id": self.goal_id,
            "created_at": self.created_at.isoformat().replace("+00:00", "Z"),
            "parameters": {key: value for key, value in self.parameters},
            "locale": self.locale,
        }

    @classmethod
    def from_mapping(
        cls,
        payload: Mapping[str, Any],
        *,
        expected_source: IntentSource | None = None,
    ) -> "CandidateIntent":
        unexpected = set(payload) & _PROHIBITED_CANDIDATE_FIELDS
        if unexpected:
            raise IntentRejected("ARIANE_INTENT_FORBIDDEN_AUTHORITY_FIELD")
        source = IntentSource(_required_text(payload.get("source"), "source"))
        if expected_source is not None and source is not expected_source:
            raise IntentRejected("ARIANE_INTENT_SOURCE_MISMATCH")
        parameters = payload.get("parameters", {})
        if not isinstance(parameters, Mapping):
            raise IntentRejected("ARIANE_INTENT_PARAMETERS_INVALID")
        created_at = _parse_timestamp(payload.get("created_at"), "created_at")
        return cls(
            candidate_id=_required_text(payload.get("candidate_id"), "candidate_id"),
            source=source,
            application_id=_required_text(payload.get("application_id"), "application_id"),
            goal_id=_required_text(payload.get("goal_id"), "goal_id"),
            created_at=created_at,
            parameters=tuple(parameters.items()),
            locale=_optional_text(payload.get("locale"), "locale"),
        )


@dataclass(frozen=True, slots=True)
class ValidatedIntent:
    """A schema-checked candidate that is still non-authoritative."""

    candidate: CandidateIntent
    validated_at: datetime
    validation_reason_code: str = "ARIANE_INTENT_VALID"

    def __post_init__(self) -> None:
        object.__setattr__(self, "validated_at", _utc(self.validated_at, "validated_at"))
        object.__setattr__(
            self,
            "validation_reason_code",
            _required_text(self.validation_reason_code, "validation_reason_code"),
        )

    @property
    def grants_authority(self) -> bool:
        return False

    @property
    def confirms_sensitive_action(self) -> bool:
        return False

    @property
    def can_invoke_driver(self) -> bool:
        return False


@dataclass(frozen=True, slots=True)
class IntentBridge:
    max_candidate_age: timedelta = timedelta(minutes=2)

    def __post_init__(self) -> None:
        if self.max_candidate_age <= timedelta(0) or self.max_candidate_age > timedelta(minutes=10):
            raise ValueError("max_candidate_age must be greater than zero and no more than ten minutes")

    def validate(
        self,
        candidate: CandidateIntent,
        *,
        now: datetime,
        supported_applications: tuple[str, ...],
        supported_goals: tuple[str, ...],
    ) -> ValidatedIntent:
        candidate.ensure_fresh(now=now, max_age=self.max_candidate_age)
        applications = _unique_refs(supported_applications, "supported_applications")
        goals = _unique_refs(supported_goals, "supported_goals")
        if candidate.application_id not in applications:
            raise IntentRejected("ARIANE_INTENT_APPLICATION_UNSUPPORTED")
        if candidate.goal_id not in goals:
            raise IntentRejected("ARIANE_INTENT_GOAL_UNSUPPORTED")
        return ValidatedIntent(candidate=candidate, validated_at=now)


class IntentRejected(ValueError):
    def __init__(self, reason_code: str) -> None:
        self.reason_code = _required_text(reason_code, "reason_code")
        super().__init__(f"Ariane candidate intent rejected: {self.reason_code}")


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_text(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _required_text(value, field)


def _utc(value: datetime, field: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc)


def _parse_timestamp(value: object, field: str) -> datetime:
    text = _required_text(value, field)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IntentRejected("ARIANE_INTENT_TIMESTAMP_INVALID") from exc
    return _utc(parsed, field)


def _unique_refs(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    cleaned = tuple(_required_text(value, field) for value in values)
    if len(set(cleaned)) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicates")
    return cleaned


def _parameters(values: tuple[tuple[str, JsonValue], ...]) -> tuple[tuple[str, JsonValue], ...]:
    result: list[tuple[str, JsonValue]] = []
    seen: set[str] = set()
    for key, value in values:
        clean_key = _required_text(key, "parameter key")
        lowered = clean_key.lower()
        if lowered in _PROHIBITED_CANDIDATE_FIELDS or any(
            fragment in lowered for fragment in ("password", "secret", "token", "credential")
        ):
            raise IntentRejected("ARIANE_INTENT_FORBIDDEN_PARAMETER")
        if clean_key in seen:
            raise ValueError("parameters must not contain duplicates")
        _validate_json(value)
        seen.add(clean_key)
        result.append((clean_key, value))
    return tuple(sorted(result, key=lambda item: item[0]))


def _validate_json(value: JsonValue) -> None:
    if value is None or isinstance(value, (str, bool, int, float)):
        if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
            raise IntentRejected("ARIANE_INTENT_PARAMETER_NOT_FINITE")
        return
    if isinstance(value, list):
        for item in value:
            _validate_json(item)
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            _required_text(key, "parameter key")
            _validate_json(item)
        return
    raise IntentRejected("ARIANE_INTENT_PARAMETER_NOT_JSON")
