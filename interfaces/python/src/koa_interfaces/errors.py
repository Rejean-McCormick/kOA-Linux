"""Error bindings for common kOA transport interfaces."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping, NoReturn

ERROR_ENVELOPE_SCHEMA_PATH = "interfaces/transport/error-envelope.schema.json"


class InterfaceValidationError(ValueError):
    """Raised when a binding cannot represent the supplied interface value."""


class TransportError(RuntimeError):
    """Raised when the local transport cannot complete a request."""


class ProtocolError(RuntimeError):
    """Raised when a peer violates the declared transport contract."""


class ErrorCategory(StrEnum):
    INVALID_REQUEST = "invalid_request"
    AUTHENTICATION_REQUIRED = "authentication_required"
    AUTHORIZATION_DENIED = "authorization_denied"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    INCOMPATIBLE = "incompatible"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    INTERNAL = "internal"
    INDETERMINATE = "indeterminate"


class ErrorDisposition(StrEnum):
    TERMINAL = "terminal"
    RETRY_SAME_REQUEST = "retry_same_request"
    RECONCILE_BEFORE_RETRY = "reconcile_before_retry"
    OPERATOR_ACTION_REQUIRED = "operator_action_required"


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InterfaceValidationError(f"{field_name} must be a non-empty string")
    return value


def _optional_text(value: Any, field_name: str) -> str | None:
    if value is None:
        return None
    return _require_text(value, field_name)


def _parse_timestamp(value: Any, field_name: str) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise InterfaceValidationError(f"{field_name} must be an RFC 3339 timestamp") from exc
    else:
        raise InterfaceValidationError(f"{field_name} must be an RFC 3339 timestamp")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InterfaceValidationError(f"{field_name} must include a UTC offset")
    return parsed.astimezone(timezone.utc)


def _format_timestamp(value: datetime) -> str:
    parsed = _parse_timestamp(value, "timestamp")
    return parsed.isoformat().replace("+00:00", "Z")


def _freeze_mapping(value: Mapping[str, Any] | None, field_name: str) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise InterfaceValidationError(f"{field_name} must be an object")
    normalized: dict[str, Any] = {}
    for key, item in value.items():
        normalized[_require_text(key, f"{field_name} key")] = item
    return MappingProxyType(normalized)


def _string_tuple(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise InterfaceValidationError(f"{field_name} must be an array of strings")
    result = tuple(_require_text(item, field_name) for item in value)
    if len(result) != len(set(result)):
        raise InterfaceValidationError(f"{field_name} must not contain duplicates")
    return result


def _enum_value(enum_type: type[StrEnum], value: Any, field_name: str) -> StrEnum:
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        allowed = ", ".join(member.value for member in enum_type)
        raise InterfaceValidationError(f"{field_name} must be one of: {allowed}") from exc


def _unexpected_fields(data: Mapping[str, Any], allowed: set[str]) -> NoReturn | None:
    unexpected = sorted(set(data) - allowed)
    if unexpected:
        raise InterfaceValidationError(f"unexpected fields: {', '.join(unexpected)}")
    return None


@dataclass(frozen=True, slots=True)
class ErrorEnvelope:
    """Stable machine-readable failure returned across a component boundary."""

    error_id: str
    code: str
    category: ErrorCategory
    message: str
    disposition: ErrorDisposition
    observed_at: datetime
    correlation_id: str
    reason_codes: tuple[str, ...] = ()
    details: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    SCHEMA_PATH = ERROR_ENVELOPE_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "error_id", _require_text(self.error_id, "error_id"))
        object.__setattr__(self, "code", _require_text(self.code, "code"))
        object.__setattr__(self, "category", _enum_value(ErrorCategory, self.category, "category"))
        object.__setattr__(self, "message", _require_text(self.message, "message"))
        object.__setattr__(
            self,
            "disposition",
            _enum_value(ErrorDisposition, self.disposition, "disposition"),
        )
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(
            self, "correlation_id", _require_text(self.correlation_id, "correlation_id")
        )
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        object.__setattr__(self, "details", _freeze_mapping(self.details, "details"))

    @property
    def retryable(self) -> bool:
        return self.disposition in {
            ErrorDisposition.RETRY_SAME_REQUEST,
            ErrorDisposition.RECONCILE_BEFORE_RETRY,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "error_id": self.error_id,
            "code": self.code,
            "category": self.category.value,
            "message": self.message,
            "disposition": self.disposition.value,
            "observed_at": _format_timestamp(self.observed_at),
            "correlation_id": self.correlation_id,
            "reason_codes": list(self.reason_codes),
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ErrorEnvelope:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("error envelope must be an object")
        allowed = {
            "error_id",
            "code",
            "category",
            "message",
            "disposition",
            "observed_at",
            "correlation_id",
            "reason_codes",
            "details",
        }
        _unexpected_fields(data, allowed)
        required = allowed - {"reason_codes", "details"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            error_id=data["error_id"],
            code=data["code"],
            category=data["category"],
            message=data["message"],
            disposition=data["disposition"],
            observed_at=data["observed_at"],
            correlation_id=data["correlation_id"],
            reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
            details=_freeze_mapping(data.get("details"), "details"),
        )


class RemoteError(RuntimeError):
    """Raised when a peer returns a valid kOA error envelope."""

    def __init__(self, status: int, envelope: ErrorEnvelope) -> None:
        self.status = status
        self.envelope = envelope
        super().__init__(f"remote error {status} {envelope.code}: {envelope.message}")
