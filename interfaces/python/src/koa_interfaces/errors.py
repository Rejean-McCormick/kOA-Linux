"""Error bindings for common kOA transport interfaces."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, NoReturn

ERROR_ENVELOPE_SCHEMA_PATH = "interfaces/transport/error-envelope.schema.json"
_ERROR_ENVELOPE_VERSION = "1.0.0"
_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,254}$")
_ERROR_CODE_RE = re.compile(r"^[a-z][a-z0-9_]{2,127}$")
_REASON_CODE_RE = re.compile(r"^[A-Z0-9][A-Z0-9_.-]{1,127}$")
_SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
_MEDIA_TYPE_RE = re.compile(
    r"^[A-Za-z0-9!#$&^_.+-]+/[A-Za-z0-9!#$&^_.+-]+"
    r"(?:\s*;\s*[A-Za-z0-9!#$&^_.+-]+=[^;]+)*$"
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class InterfaceValidationError(ValueError):
    """Raised when a binding cannot represent the supplied interface value."""


class TransportError(RuntimeError):
    """Raised when the local transport cannot complete a request."""


class ProtocolError(RuntimeError):
    """Raised when a peer violates the declared transport contract."""


class ErrorCategory(StrEnum):
    """Canonical ``error_class`` values from the error-envelope schema.

    Historical member names remain aliases so callers compiled against the
    earlier binding can migrate without reintroducing the obsolete JSON shape.
    """

    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    POLICY = "policy"
    COMPATIBILITY = "compatibility"
    CONFLICT = "conflict"
    NOT_FOUND = "not_found"
    RATE_LIMIT = "rate_limit"
    RESOURCE = "resource"
    TIMEOUT = "timeout"
    DEPENDENCY = "dependency"
    TRANSPORT = "transport"
    INTERNAL = "internal"
    INDETERMINATE_OUTCOME = "indeterminate_outcome"

    # Compatibility aliases for the pre-schema-aligned Python API.
    INVALID_REQUEST = "validation"
    AUTHENTICATION_REQUIRED = "authentication"
    AUTHORIZATION_DENIED = "authorization"
    INCOMPATIBLE = "compatibility"
    DEPENDENCY_UNAVAILABLE = "dependency"
    RESOURCE_EXHAUSTED = "resource"
    CANCELLED = "internal"
    INDETERMINATE = "indeterminate_outcome"


class ErrorDisposition(StrEnum):
    """Compatibility view derived from the canonical ``retry`` object."""

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


def _freeze_json(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            normalized[_require_text(key, f"{field_name} key")] = _freeze_json(
                item, f"{field_name}.{key}"
            )
        return MappingProxyType(normalized)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, field_name) for item in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise InterfaceValidationError(f"{field_name} contains a non-JSON value")


def _thaw_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw_json(item) for item in value]
    return value


def _freeze_mapping(value: Mapping[str, Any] | None, field_name: str) -> Mapping[str, Any]:
    """Preserve the shallow-freeze behavior used by the older shared bindings."""

    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise InterfaceValidationError(f"{field_name} must be an object")
    normalized: dict[str, Any] = {}
    for key, item in value.items():
        normalized[_require_text(key, f"{field_name} key")] = item
    return MappingProxyType(normalized)


def _freeze_json_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InterfaceValidationError(f"{field_name} must be an object")
    frozen = _freeze_json(value, field_name)
    assert isinstance(frozen, Mapping)
    return frozen


def _optional_mapping(value: Any, field_name: str) -> Mapping[str, Any] | None:
    if value is None:
        return None
    return _freeze_json_mapping(value, field_name)


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


def _closed_object(
    value: Any,
    field_name: str,
    *,
    required: set[str],
    allowed: set[str],
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InterfaceValidationError(f"{field_name} must be an object")
    unexpected = sorted(set(value) - allowed)
    if unexpected:
        raise InterfaceValidationError(
            f"{field_name} has unexpected fields: {', '.join(unexpected)}"
        )
    missing = sorted(required - set(value))
    if missing:
        raise InterfaceValidationError(f"{field_name} missing fields: {', '.join(missing)}")
    return value


def _identifier(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _IDENTIFIER_RE.fullmatch(text):
        raise InterfaceValidationError(f"{field_name} must be a kOA identifier")
    return text


def _semantic_version(value: Any, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not _SEMVER_RE.fullmatch(text):
        raise InterfaceValidationError(f"{field_name} must be a semantic version")
    return text


def _validate_interface(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "interface",
        required={"interface_id", "interface_version"},
        allowed={"interface_id", "interface_version", "contract_ref"},
    )
    _identifier(obj["interface_id"], "interface.interface_id")
    _semantic_version(obj["interface_version"], "interface.interface_version")
    if "contract_ref" in obj:
        _require_text(obj["contract_ref"], "interface.contract_ref")


def _validate_producer(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "producer",
        required={"component_id"},
        allowed={"component_id", "instance_id", "profile_id"},
    )
    for key in obj:
        _identifier(obj[key], f"producer.{key}")


def _validate_receiver(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "intended_receiver",
        required={"kind", "identifier"},
        allowed={"kind", "identifier"},
    )
    if obj["kind"] not in {"component", "capability", "subscription", "topic"}:
        raise InterfaceValidationError("intended_receiver.kind is invalid")
    _identifier(obj["identifier"], "intended_receiver.identifier")


def _validate_correlation(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "correlation",
        required={"correlation_id"},
        allowed={"correlation_id", "causation_id", "request_id", "trace_id"},
    )
    for key in obj:
        _identifier(obj[key], f"correlation.{key}")


def _validate_outcome(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "outcome",
        required={"state", "finality", "authoritative_effect"},
        allowed={"state", "finality", "authoritative_effect", "status_ref"},
    )
    if obj["state"] not in {
        "rejected",
        "blocked",
        "failed",
        "expired",
        "cancelled",
        "indeterminate",
    }:
        raise InterfaceValidationError("outcome.state is invalid")
    if obj["finality"] not in {"final", "non_final", "indeterminate"}:
        raise InterfaceValidationError("outcome.finality is invalid")
    if obj["authoritative_effect"] not in {
        "none",
        "unchanged",
        "unknown_requires_resolution",
    }:
        raise InterfaceValidationError("outcome.authoritative_effect is invalid")
    if "status_ref" in obj:
        _require_text(obj["status_ref"], "outcome.status_ref")
    if obj["state"] == "indeterminate":
        if obj["finality"] != "indeterminate":
            raise InterfaceValidationError("indeterminate outcome requires indeterminate finality")
        if obj["authoritative_effect"] != "unknown_requires_resolution":
            raise InterfaceValidationError(
                "indeterminate outcome requires unknown_requires_resolution"
            )
        if "status_ref" not in obj:
            raise InterfaceValidationError("indeterminate outcome requires status_ref")


def _validate_retry(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "retry",
        required={"allowed", "strategy"},
        allowed={
            "allowed",
            "strategy",
            "after_seconds",
            "maximum_attempts",
            "idempotency_required",
        },
    )
    if not isinstance(obj["allowed"], bool):
        raise InterfaceValidationError("retry.allowed must be a boolean")
    if obj["strategy"] not in {
        "none",
        "immediate",
        "bounded_backoff",
        "status_resolution",
        "manual_intervention",
    }:
        raise InterfaceValidationError("retry.strategy is invalid")
    for key, minimum in (("after_seconds", 0), ("maximum_attempts", 1)):
        if key in obj and (
            isinstance(obj[key], bool) or not isinstance(obj[key], int) or obj[key] < minimum
        ):
            raise InterfaceValidationError(f"retry.{key} must be an integer >= {minimum}")
    if "idempotency_required" in obj and not isinstance(obj["idempotency_required"], bool):
        raise InterfaceValidationError("retry.idempotency_required must be a boolean")
    if obj["allowed"] is False:
        if obj["strategy"] != "none":
            raise InterfaceValidationError("retry strategy must be none when retry is not allowed")
        if "after_seconds" in obj or "maximum_attempts" in obj:
            raise InterfaceValidationError("disabled retry cannot define timing or attempt limits")
    if obj["strategy"] == "bounded_backoff" and not {
        "after_seconds",
        "maximum_attempts",
    }.issubset(obj):
        raise InterfaceValidationError(
            "bounded_backoff retry requires after_seconds and maximum_attempts"
        )
    if obj["strategy"] == "status_resolution" and obj.get("idempotency_required") is not True:
        raise InterfaceValidationError(
            "status_resolution retry requires idempotency_required=true"
        )


def _validate_disclosure(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "disclosure",
        required={"class", "payload_minimized", "contains_secrets"},
        allowed={"class", "payload_minimized", "contains_secrets"},
    )
    if obj["class"] not in {
        "public_summary",
        "tenant_visible",
        "operator_restricted",
        "security_restricted",
        "evidence_restricted",
    }:
        raise InterfaceValidationError("disclosure.class is invalid")
    if obj["payload_minimized"] is not True:
        raise InterfaceValidationError("disclosure.payload_minimized must be true")
    if obj["contains_secrets"] is not False:
        raise InterfaceValidationError("disclosure.contains_secrets must be false")


def _validate_authority(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "authority",
        required={
            "transport_grants_authority",
            "error_grants_authority",
            "transfers_ownership",
        },
        allowed={
            "transport_grants_authority",
            "error_grants_authority",
            "transfers_ownership",
        },
    )
    if any(obj[key] is not False for key in obj):
        raise InterfaceValidationError("error envelope authority fields must all be false")


def _validate_payload_representation(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "payload_representation",
        required={"media_type", "schema_ref", "schema_version"},
        allowed={"media_type", "schema_ref", "schema_version", "encoding", "content_digest"},
    )
    media_type = _require_text(obj["media_type"], "payload_representation.media_type")
    if not _MEDIA_TYPE_RE.fullmatch(media_type):
        raise InterfaceValidationError("payload_representation.media_type is invalid")
    _require_text(obj["schema_ref"], "payload_representation.schema_ref")
    _semantic_version(obj["schema_version"], "payload_representation.schema_version")
    if "encoding" in obj and obj["encoding"] not in {"identity", "base64", "uri_reference"}:
        raise InterfaceValidationError("payload_representation.encoding is invalid")
    if "content_digest" in obj:
        digest = _closed_object(
            obj["content_digest"],
            "payload_representation.content_digest",
            required={"algorithm", "value"},
            allowed={"algorithm", "value"},
        )
        if digest["algorithm"] != "sha256":
            raise InterfaceValidationError("content digest algorithm must be sha256")
        text = _require_text(digest["value"], "payload_representation.content_digest.value")
        if not _SHA256_RE.fullmatch(text):
            raise InterfaceValidationError("content digest value must be lowercase sha256 hex")


def _validate_release_context(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "release_context",
        required=set(),
        allowed={"release_set_id", "sender_release", "receiver_release"},
    )
    if not obj:
        raise InterfaceValidationError("release_context must not be empty")
    if "release_set_id" in obj:
        _identifier(obj["release_set_id"], "release_context.release_set_id")
    for key in ("sender_release", "receiver_release"):
        if key in obj:
            _semantic_version(obj[key], f"release_context.{key}")


def _validate_details(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "details",
        required=set(),
        allowed={"field_violations", "dependency_ref", "expected_version", "received_version"},
    )
    if not obj:
        raise InterfaceValidationError("details must not be empty")
    if "dependency_ref" in obj:
        _identifier(obj["dependency_ref"], "details.dependency_ref")
    for key in ("expected_version", "received_version"):
        if key in obj:
            _semantic_version(obj[key], f"details.{key}")
    if "field_violations" in obj:
        violations = obj["field_violations"]
        if not isinstance(violations, (list, tuple)) or not violations:
            raise InterfaceValidationError("details.field_violations must be a non-empty array")
        for index, item in enumerate(violations):
            violation = _closed_object(
                item,
                f"details.field_violations[{index}]",
                required={"path", "code"},
                allowed={"path", "code", "message"},
            )
            _require_text(violation["path"], f"details.field_violations[{index}].path")
            code = _require_text(violation["code"], f"details.field_violations[{index}].code")
            if not _ERROR_CODE_RE.fullmatch(code):
                raise InterfaceValidationError("field violation code is invalid")
            if "message" in violation:
                _require_text(
                    violation["message"], f"details.field_violations[{index}].message"
                )


def _validate_evidence(value: Mapping[str, Any]) -> None:
    obj = _closed_object(
        value,
        "evidence",
        required=set(),
        allowed={"receipt_refs", "evidence_refs"},
    )
    if not obj:
        raise InterfaceValidationError("evidence must not be empty")
    for key in ("receipt_refs", "evidence_refs"):
        if key not in obj:
            continue
        items = obj[key]
        if isinstance(items, str) or not isinstance(items, (list, tuple)):
            raise InterfaceValidationError(f"evidence.{key} must be an array")
        if len(items) != len(set(items)):
            raise InterfaceValidationError(f"evidence.{key} must not contain duplicates")
        for item in items:
            if key == "receipt_refs":
                _identifier(item, "evidence.receipt_refs")
            else:
                _require_text(item, "evidence.evidence_refs")


@dataclass(frozen=True, slots=True)
class ErrorEnvelope:
    """Schema-aligned machine-readable failure across a component boundary."""

    error_id: str
    error_code: str
    error_class: ErrorCategory
    message: str
    interface: Mapping[str, Any]
    producer: Mapping[str, Any]
    intended_receiver: Mapping[str, Any]
    correlation: Mapping[str, Any]
    occurred_at: datetime
    outcome: Mapping[str, Any]
    retry: Mapping[str, Any]
    disclosure: Mapping[str, Any]
    authority: Mapping[str, Any]
    reason_codes: tuple[str, ...] = ()
    payload_representation: Mapping[str, Any] | None = None
    release_context: Mapping[str, Any] | None = None
    details: Mapping[str, Any] | None = None
    evidence: Mapping[str, Any] | None = None
    schema_version: str = _ERROR_ENVELOPE_VERSION

    SCHEMA_PATH: ClassVar[str] = ERROR_ENVELOPE_SCHEMA_PATH
    ENVELOPE_TYPE: ClassVar[str] = "error"

    def __post_init__(self) -> None:
        object.__setattr__(self, "error_id", _identifier(self.error_id, "error_id"))
        error_code = _require_text(self.error_code, "error_code")
        if not _ERROR_CODE_RE.fullmatch(error_code):
            raise InterfaceValidationError("error_code does not match the canonical pattern")
        object.__setattr__(self, "error_code", error_code)
        object.__setattr__(
            self, "error_class", _enum_value(ErrorCategory, self.error_class, "error_class")
        )
        object.__setattr__(self, "message", _require_text(self.message, "message"))
        if len(self.message) > 1024:
            raise InterfaceValidationError("message must be at most 1024 characters")
        object.__setattr__(self, "schema_version", _semantic_version(self.schema_version, "schema_version"))
        if self.schema_version != _ERROR_ENVELOPE_VERSION:
            raise InterfaceValidationError("schema_version must be 1.0.0")

        for field_name in (
            "interface",
            "producer",
            "intended_receiver",
            "correlation",
            "outcome",
            "retry",
            "disclosure",
            "authority",
        ):
            object.__setattr__(self, field_name, _freeze_json_mapping(getattr(self, field_name), field_name))

        object.__setattr__(self, "occurred_at", _parse_timestamp(self.occurred_at, "occurred_at"))
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        for reason in self.reason_codes:
            if not _REASON_CODE_RE.fullmatch(reason):
                raise InterfaceValidationError(
                    "reason_codes entries must match the canonical uppercase pattern"
                )

        for field_name in (
            "payload_representation",
            "release_context",
            "details",
            "evidence",
        ):
            object.__setattr__(
                self, field_name, _optional_mapping(getattr(self, field_name), field_name)
            )

        _validate_interface(self.interface)
        _validate_producer(self.producer)
        _validate_receiver(self.intended_receiver)
        _validate_correlation(self.correlation)
        _validate_outcome(self.outcome)
        _validate_retry(self.retry)
        _validate_disclosure(self.disclosure)
        _validate_authority(self.authority)
        if self.payload_representation is not None:
            _validate_payload_representation(self.payload_representation)
        if self.release_context is not None:
            _validate_release_context(self.release_context)
        if self.details is not None:
            _validate_details(self.details)
        if self.evidence is not None:
            _validate_evidence(self.evidence)

    # Compatibility views: these names are API conveniences only and are never
    # serialized into the canonical envelope.
    @property
    def code(self) -> str:
        return self.error_code

    @property
    def category(self) -> ErrorCategory:
        return self.error_class

    @property
    def observed_at(self) -> datetime:
        return self.occurred_at

    @property
    def correlation_id(self) -> str:
        return str(self.correlation["correlation_id"])

    @property
    def retryable(self) -> bool:
        return bool(self.retry["allowed"])

    @property
    def disposition(self) -> ErrorDisposition:
        strategy = str(self.retry["strategy"])
        if not self.retryable or strategy == "none":
            return ErrorDisposition.TERMINAL
        if strategy in {"immediate", "bounded_backoff"}:
            return ErrorDisposition.RETRY_SAME_REQUEST
        if strategy == "status_resolution":
            return ErrorDisposition.RECONCILE_BEFORE_RETRY
        return ErrorDisposition.OPERATOR_ACTION_REQUIRED

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "envelope_type": self.ENVELOPE_TYPE,
            "error_id": self.error_id,
            "error_code": self.error_code,
            "error_class": self.error_class.value,
            "message": self.message,
            "interface": _thaw_json(self.interface),
            "producer": _thaw_json(self.producer),
            "intended_receiver": _thaw_json(self.intended_receiver),
            "correlation": _thaw_json(self.correlation),
            "occurred_at": _format_timestamp(self.occurred_at),
            "outcome": _thaw_json(self.outcome),
            "retry": _thaw_json(self.retry),
            "disclosure": _thaw_json(self.disclosure),
            "authority": _thaw_json(self.authority),
        }
        if self.reason_codes:
            result["reason_codes"] = list(self.reason_codes)
        for field_name in (
            "payload_representation",
            "release_context",
            "details",
            "evidence",
        ):
            value = getattr(self, field_name)
            if value is not None:
                result[field_name] = _thaw_json(value)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ErrorEnvelope:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("error envelope must be an object")
        allowed = {
            "schema_version",
            "envelope_type",
            "error_id",
            "error_code",
            "error_class",
            "message",
            "reason_codes",
            "interface",
            "producer",
            "intended_receiver",
            "correlation",
            "occurred_at",
            "payload_representation",
            "release_context",
            "outcome",
            "retry",
            "details",
            "disclosure",
            "evidence",
            "authority",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version",
            "envelope_type",
            "error_id",
            "error_code",
            "error_class",
            "message",
            "interface",
            "producer",
            "intended_receiver",
            "correlation",
            "occurred_at",
            "outcome",
            "retry",
            "disclosure",
            "authority",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        if data["envelope_type"] != cls.ENVELOPE_TYPE:
            raise InterfaceValidationError("envelope_type must be error")
        return cls(
            schema_version=data["schema_version"],
            error_id=data["error_id"],
            error_code=data["error_code"],
            error_class=data["error_class"],
            message=data["message"],
            interface=data["interface"],
            producer=data["producer"],
            intended_receiver=data["intended_receiver"],
            correlation=data["correlation"],
            occurred_at=data["occurred_at"],
            outcome=data["outcome"],
            retry=data["retry"],
            disclosure=data["disclosure"],
            authority=data["authority"],
            reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
            payload_representation=data.get("payload_representation"),
            release_context=data.get("release_context"),
            details=data.get("details"),
            evidence=data.get("evidence"),
        )


class RemoteError(RuntimeError):
    """Raised when a peer returns a valid kOA error envelope."""

    def __init__(self, status: int, envelope: ErrorEnvelope) -> None:
        self.status = status
        self.envelope = envelope
        super().__init__(f"remote error {status} {envelope.error_code}: {envelope.message}")
