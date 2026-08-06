"""Typed transport bindings and a bounded HTTP-over-Unix client."""

from __future__ import annotations

import http.client
import json
import socket
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, Sequence
from urllib.parse import urlencode

from .errors import (
    ErrorEnvelope,
    InterfaceValidationError,
    ProtocolError,
    RemoteError,
    TransportError,
    _enum_value,
    _format_timestamp,
    _freeze_mapping,
    _optional_text,
    _parse_timestamp,
    _require_text,
    _string_tuple,
    _unexpected_fields,
)
from .health import HealthStatus, Readiness, ReadinessClass
from .receipts import Correlation

SCHEMA_PATHS: Mapping[str, str] = MappingProxyType(
    {
        "event_envelope": "interfaces/transport/event-envelope.schema.json",
        "error_envelope": "interfaces/transport/error-envelope.schema.json",
        "idempotency": "interfaces/transport/idempotency.schema.json",
        "version_negotiation": "interfaces/transport/version-negotiation.schema.json",
        "health_status": "interfaces/health/health-status.schema.json",
        "readiness": "interfaces/health/readiness.schema.json",
        "receipt_envelope": "interfaces/receipts/receipt-envelope.schema.json",
        "correlation": "interfaces/receipts/correlation.schema.json",
        "job_request": "interfaces/jobs/job-request.schema.json",
        "job_status": "interfaces/jobs/job-status.schema.json",
        "identity_context": "interfaces/identity/identity-context.schema.json",
        "capability_snapshot": "interfaces/capabilities/capability-snapshot.schema.json",
    }
)

EVENT_ENVELOPE_SCHEMA_PATH = SCHEMA_PATHS["event_envelope"]
IDEMPOTENCY_SCHEMA_PATH = SCHEMA_PATHS["idempotency"]
VERSION_NEGOTIATION_SCHEMA_PATH = SCHEMA_PATHS["version_negotiation"]
JOB_REQUEST_SCHEMA_PATH = SCHEMA_PATHS["job_request"]
JOB_STATUS_SCHEMA_PATH = SCHEMA_PATHS["job_status"]
IDENTITY_CONTEXT_SCHEMA_PATH = SCHEMA_PATHS["identity_context"]


class DeliveryGuarantee(StrEnum):
    AT_MOST_ONCE = "at_most_once"
    AT_LEAST_ONCE = "at_least_once"
    EFFECTIVELY_ONCE = "effectively_once"
    BEST_EFFORT = "best_effort"


class Ordering(StrEnum):
    NONE = "none"
    PER_KEY = "per_key"
    GLOBAL = "global"


class DuplicateOutcome(StrEnum):
    RETURN_PRIOR_RESULT = "return_prior_result"
    REJECT = "reject"
    IGNORE = "ignore"
    MERGE_BY_CONTRACT = "merge_by_contract"


class JobState(StrEnum):
    NOT_STARTED = "not_started"
    ACCEPTED = "accepted"
    QUEUED = "queued"
    RUNNING = "running"
    AWAITING_DEPENDENCY = "awaiting_dependency"
    AWAITING_AUTHORITY = "awaiting_authority"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"
    CONFLICTED = "conflicted"
    EXPIRED = "expired"


class IdentityType(StrEnum):
    HUMAN = "human"
    TENANT = "tenant"
    ORGANIZATION = "organization"
    ROLE = "role"
    NODE = "node"
    WORKLOAD = "workload"
    SERVICE = "service"
    PUBLISHER = "publisher"
    SIGNER = "signer"
    ARTIFACT = "artifact"
    EXTERNAL_INTEGRATION = "external_integration"


@dataclass(frozen=True, slots=True)
class SchemaBinding:
    """Resolved identity for one dependency-owned JSON schema."""

    logical_name: str
    repository_path: str
    canonical_id: str
    title: str | None = None


@dataclass(frozen=True, slots=True)
class SchemaCatalog:
    """Read-only catalog that resolves the actual ``$id`` from dependency schemas."""

    bindings: Mapping[str, SchemaBinding]

    def __post_init__(self) -> None:
        object.__setattr__(self, "bindings", MappingProxyType(dict(self.bindings)))
        missing = sorted(set(SCHEMA_PATHS) - set(self.bindings))
        unexpected = sorted(set(self.bindings) - set(SCHEMA_PATHS))
        if missing or unexpected:
            details = []
            if missing:
                details.append(f"missing: {', '.join(missing)}")
            if unexpected:
                details.append(f"unexpected: {', '.join(unexpected)}")
            raise InterfaceValidationError("schema catalog mismatch (" + "; ".join(details) + ")")

    @classmethod
    def from_repository(cls, repository_root: str | Path) -> SchemaCatalog:
        root = Path(repository_root)
        resolved: dict[str, SchemaBinding] = {}
        for logical_name, relative in SCHEMA_PATHS.items():
            schema_path = root / relative
            try:
                raw = json.loads(schema_path.read_text(encoding="utf-8"))
            except FileNotFoundError as exc:
                raise InterfaceValidationError(f"missing dependency schema: {relative}") from exc
            except json.JSONDecodeError as exc:
                raise InterfaceValidationError(f"invalid JSON schema: {relative}: {exc}") from exc
            if not isinstance(raw, dict):
                raise InterfaceValidationError(f"schema root must be an object: {relative}")
            schema_type = raw.get("type")
            if schema_type not in {None, "object"}:
                raise InterfaceValidationError(
                    f"common envelope schema must describe an object: {relative}"
                )
            canonical_id = raw.get("$id", relative)
            if not isinstance(canonical_id, str) or not canonical_id.strip():
                raise InterfaceValidationError(f"schema $id must be a non-empty string: {relative}")
            title = raw.get("title")
            if title is not None and not isinstance(title, str):
                raise InterfaceValidationError(f"schema title must be a string: {relative}")
            resolved[logical_name] = SchemaBinding(
                logical_name=logical_name,
                repository_path=relative,
                canonical_id=canonical_id,
                title=title,
            )
        return cls(resolved)

    def canonical_id(self, logical_name: str) -> str:
        try:
            return self.bindings[logical_name].canonical_id
        except KeyError as exc:
            raise InterfaceValidationError(f"unknown schema binding: {logical_name}") from exc


@dataclass(frozen=True, slots=True)
class Idempotency:
    required: bool
    key: str | None = None
    duplicate_outcome: DuplicateOutcome | None = None
    retention_rule: str | None = None

    SCHEMA_PATH: ClassVar[str] = IDEMPOTENCY_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "key", _optional_text(self.key, "key"))
        object.__setattr__(
            self, "retention_rule", _optional_text(self.retention_rule, "retention_rule")
        )
        if self.duplicate_outcome is not None:
            object.__setattr__(
                self,
                "duplicate_outcome",
                _enum_value(DuplicateOutcome, self.duplicate_outcome, "duplicate_outcome"),
            )
        if self.required and (
            self.key is None or self.duplicate_outcome is None or self.retention_rule is None
        ):
            raise InterfaceValidationError(
                "required idempotency needs key, duplicate_outcome and retention_rule"
            )
        if not self.required and any(
            value is not None for value in (self.key, self.duplicate_outcome, self.retention_rule)
        ):
            raise InterfaceValidationError(
                "optional idempotency must omit key, duplicate_outcome and retention_rule"
            )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"required": self.required}
        if self.required:
            result.update(
                {
                    "key": self.key,
                    "duplicate_outcome": self.duplicate_outcome.value,
                    "retention_rule": self.retention_rule,
                }
            )
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Idempotency:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("idempotency must be an object")
        _unexpected_fields(data, {"required", "key", "duplicate_outcome", "retention_rule"})
        if "required" not in data or not isinstance(data["required"], bool):
            raise InterfaceValidationError("required must be a boolean")
        return cls(
            required=data["required"],
            key=data.get("key"),
            duplicate_outcome=data.get("duplicate_outcome"),
            retention_rule=data.get("retention_rule"),
        )


@dataclass(frozen=True, slots=True)
class VersionNegotiation:
    supported_versions: tuple[str, ...]
    selected_version: str | None = None
    minimum_compatible_version: str | None = None

    SCHEMA_PATH: ClassVar[str] = VERSION_NEGOTIATION_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "supported_versions",
            _string_tuple(self.supported_versions, "supported_versions"),
        )
        if not self.supported_versions:
            raise InterfaceValidationError("supported_versions must not be empty")
        object.__setattr__(
            self, "selected_version", _optional_text(self.selected_version, "selected_version")
        )
        object.__setattr__(
            self,
            "minimum_compatible_version",
            _optional_text(self.minimum_compatible_version, "minimum_compatible_version"),
        )
        if self.selected_version is not None and self.selected_version not in self.supported_versions:
            raise InterfaceValidationError("selected_version must be in supported_versions")

    def select(self, peer_supported_versions: Sequence[str]) -> str:
        peer = _string_tuple(tuple(peer_supported_versions), "peer_supported_versions")
        for candidate in self.supported_versions:
            if candidate in peer:
                return candidate
        raise InterfaceValidationError("no mutually supported interface version")

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"supported_versions": list(self.supported_versions)}
        if self.selected_version is not None:
            result["selected_version"] = self.selected_version
        if self.minimum_compatible_version is not None:
            result["minimum_compatible_version"] = self.minimum_compatible_version
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> VersionNegotiation:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("version negotiation must be an object")
        allowed = {"supported_versions", "selected_version", "minimum_compatible_version"}
        _unexpected_fields(data, allowed)
        if "supported_versions" not in data:
            raise InterfaceValidationError("missing fields: supported_versions")
        return cls(
            supported_versions=_string_tuple(data["supported_versions"], "supported_versions"),
            selected_version=data.get("selected_version"),
            minimum_compatible_version=data.get("minimum_compatible_version"),
        )


@dataclass(frozen=True, slots=True)
class IdentityContext:
    actor_ref: str
    subject_ref: str
    identity_type: IdentityType
    authenticated: bool
    assurance_level: str
    authority_refs: tuple[str, ...] = ()
    delegation_refs: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))

    SCHEMA_PATH: ClassVar[str] = IDENTITY_CONTEXT_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "actor_ref", _require_text(self.actor_ref, "actor_ref"))
        object.__setattr__(self, "subject_ref", _require_text(self.subject_ref, "subject_ref"))
        object.__setattr__(
            self,
            "identity_type",
            _enum_value(IdentityType, self.identity_type, "identity_type"),
        )
        object.__setattr__(
            self, "assurance_level", _require_text(self.assurance_level, "assurance_level")
        )
        object.__setattr__(
            self, "authority_refs", _string_tuple(self.authority_refs, "authority_refs")
        )
        object.__setattr__(
            self, "delegation_refs", _string_tuple(self.delegation_refs, "delegation_refs")
        )
        object.__setattr__(self, "attributes", _freeze_mapping(self.attributes, "attributes"))
        if not self.authenticated and self.authority_refs:
            raise InterfaceValidationError(
                "unauthenticated identity context cannot assert authority_refs"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "actor_ref": self.actor_ref,
            "subject_ref": self.subject_ref,
            "identity_type": self.identity_type.value,
            "authenticated": self.authenticated,
            "assurance_level": self.assurance_level,
            "authority_refs": list(self.authority_refs),
            "delegation_refs": list(self.delegation_refs),
            "attributes": dict(self.attributes),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> IdentityContext:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("identity context must be an object")
        allowed = {
            "actor_ref", "subject_ref", "identity_type", "authenticated", "assurance_level",
            "authority_refs", "delegation_refs", "attributes",
        }
        _unexpected_fields(data, allowed)
        required = {"actor_ref", "subject_ref", "identity_type", "authenticated", "assurance_level"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        if not isinstance(data["authenticated"], bool):
            raise InterfaceValidationError("authenticated must be a boolean")
        return cls(
            actor_ref=data["actor_ref"],
            subject_ref=data["subject_ref"],
            identity_type=data["identity_type"],
            authenticated=data["authenticated"],
            assurance_level=data["assurance_level"],
            authority_refs=_string_tuple(data.get("authority_refs"), "authority_refs"),
            delegation_refs=_string_tuple(data.get("delegation_refs"), "delegation_refs"),
            attributes=_freeze_mapping(data.get("attributes"), "attributes"),
        )


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event_id: str
    event_type: str
    interface_version: str
    sender: str
    intended_receiver: str
    payload_schema: str
    payload: Mapping[str, Any]
    created_at: datetime
    correlation: Correlation
    delivery_guarantee: DeliveryGuarantee
    ordering: Ordering = Ordering.NONE
    ordering_key: str | None = None
    idempotency: Idempotency = field(default_factory=lambda: Idempotency(required=False))
    expires_at: datetime | None = None
    release_context: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    evidence_refs: tuple[str, ...] = ()

    SCHEMA_PATH: ClassVar[str] = EVENT_ENVELOPE_SCHEMA_PATH

    def __post_init__(self) -> None:
        for field_name in (
            "event_id",
            "event_type",
            "interface_version",
            "sender",
            "intended_receiver",
            "payload_schema",
        ):
            object.__setattr__(self, field_name, _require_text(getattr(self, field_name), field_name))
        object.__setattr__(self, "payload", _freeze_mapping(self.payload, "payload"))
        object.__setattr__(self, "created_at", _parse_timestamp(self.created_at, "created_at"))
        if not isinstance(self.correlation, Correlation):
            raise InterfaceValidationError("correlation must be a Correlation")
        object.__setattr__(
            self,
            "delivery_guarantee",
            _enum_value(DeliveryGuarantee, self.delivery_guarantee, "delivery_guarantee"),
        )
        object.__setattr__(self, "ordering", _enum_value(Ordering, self.ordering, "ordering"))
        object.__setattr__(self, "ordering_key", _optional_text(self.ordering_key, "ordering_key"))
        if not isinstance(self.idempotency, Idempotency):
            raise InterfaceValidationError("idempotency must be an Idempotency")
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _parse_timestamp(self.expires_at, "expires_at"))
            if self.expires_at <= self.created_at:
                raise InterfaceValidationError("expires_at must be later than created_at")
        object.__setattr__(
            self, "release_context", _freeze_mapping(self.release_context, "release_context")
        )
        object.__setattr__(
            self, "evidence_refs", _string_tuple(self.evidence_refs, "evidence_refs")
        )
        if self.ordering is Ordering.PER_KEY and self.ordering_key is None:
            raise InterfaceValidationError("ordering_key is required for per_key ordering")
        if self.ordering is not Ordering.PER_KEY and self.ordering_key is not None:
            raise InterfaceValidationError("ordering_key is only valid for per_key ordering")

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "interface_version": self.interface_version,
            "sender": self.sender,
            "intended_receiver": self.intended_receiver,
            "payload_schema": self.payload_schema,
            "payload": dict(self.payload),
            "created_at": _format_timestamp(self.created_at),
            "correlation": self.correlation.to_dict(),
            "delivery_guarantee": self.delivery_guarantee.value,
            "ordering": self.ordering.value,
            "idempotency": self.idempotency.to_dict(),
            "release_context": dict(self.release_context),
            "evidence_refs": list(self.evidence_refs),
        }
        if self.ordering_key is not None:
            result["ordering_key"] = self.ordering_key
        if self.expires_at is not None:
            result["expires_at"] = _format_timestamp(self.expires_at)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> EventEnvelope:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("event envelope must be an object")
        allowed = {
            "event_id", "event_type", "interface_version", "sender", "intended_receiver",
            "payload_schema", "payload", "created_at", "correlation", "delivery_guarantee",
            "ordering", "ordering_key", "idempotency", "expires_at", "release_context",
            "evidence_refs",
        }
        _unexpected_fields(data, allowed)
        required = {
            "event_id", "event_type", "interface_version", "sender", "intended_receiver",
            "payload_schema", "payload", "created_at", "correlation", "delivery_guarantee",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        return cls(
            event_id=data["event_id"],
            event_type=data["event_type"],
            interface_version=data["interface_version"],
            sender=data["sender"],
            intended_receiver=data["intended_receiver"],
            payload_schema=data["payload_schema"],
            payload=_freeze_mapping(data["payload"], "payload"),
            created_at=data["created_at"],
            correlation=Correlation.from_dict(data["correlation"]),
            delivery_guarantee=data["delivery_guarantee"],
            ordering=data.get("ordering", Ordering.NONE),
            ordering_key=data.get("ordering_key"),
            idempotency=Idempotency.from_dict(data.get("idempotency", {"required": False})),
            expires_at=data.get("expires_at"),
            release_context=_freeze_mapping(data.get("release_context"), "release_context"),
            evidence_refs=_string_tuple(data.get("evidence_refs"), "evidence_refs"),
        )


@dataclass(frozen=True, slots=True)
class JobRequest:
    job_id: str
    job_type: str
    interface_version: str
    sender: str
    intended_receiver: str
    payload_schema: str
    payload: Mapping[str, Any]
    created_at: datetime
    correlation: Correlation
    idempotency: Idempotency
    deadline: datetime | None = None
    result_channel: str | None = None
    identity_context: IdentityContext | None = None

    SCHEMA_PATH: ClassVar[str] = JOB_REQUEST_SCHEMA_PATH

    def __post_init__(self) -> None:
        for field_name in (
            "job_id", "job_type", "interface_version", "sender", "intended_receiver",
            "payload_schema",
        ):
            object.__setattr__(self, field_name, _require_text(getattr(self, field_name), field_name))
        object.__setattr__(self, "payload", _freeze_mapping(self.payload, "payload"))
        object.__setattr__(self, "created_at", _parse_timestamp(self.created_at, "created_at"))
        if not isinstance(self.correlation, Correlation):
            raise InterfaceValidationError("correlation must be a Correlation")
        if not isinstance(self.idempotency, Idempotency):
            raise InterfaceValidationError("idempotency must be an Idempotency")
        if not self.idempotency.required:
            raise InterfaceValidationError("job requests require an idempotency strategy")
        if self.deadline is not None:
            object.__setattr__(self, "deadline", _parse_timestamp(self.deadline, "deadline"))
            if self.deadline <= self.created_at:
                raise InterfaceValidationError("deadline must be later than created_at")
        object.__setattr__(
            self, "result_channel", _optional_text(self.result_channel, "result_channel")
        )
        if self.identity_context is not None and not isinstance(
            self.identity_context, IdentityContext
        ):
            raise InterfaceValidationError("identity_context must be an IdentityContext")

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "interface_version": self.interface_version,
            "sender": self.sender,
            "intended_receiver": self.intended_receiver,
            "payload_schema": self.payload_schema,
            "payload": dict(self.payload),
            "created_at": _format_timestamp(self.created_at),
            "correlation": self.correlation.to_dict(),
            "idempotency": self.idempotency.to_dict(),
        }
        if self.deadline is not None:
            result["deadline"] = _format_timestamp(self.deadline)
        if self.result_channel is not None:
            result["result_channel"] = self.result_channel
        if self.identity_context is not None:
            result["identity_context"] = self.identity_context.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> JobRequest:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("job request must be an object")
        allowed = {
            "job_id", "job_type", "interface_version", "sender", "intended_receiver",
            "payload_schema", "payload", "created_at", "correlation", "idempotency",
            "deadline", "result_channel", "identity_context",
        }
        _unexpected_fields(data, allowed)
        required = allowed - {"deadline", "result_channel", "identity_context"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        identity = data.get("identity_context")
        return cls(
            job_id=data["job_id"],
            job_type=data["job_type"],
            interface_version=data["interface_version"],
            sender=data["sender"],
            intended_receiver=data["intended_receiver"],
            payload_schema=data["payload_schema"],
            payload=_freeze_mapping(data["payload"], "payload"),
            created_at=data["created_at"],
            correlation=Correlation.from_dict(data["correlation"]),
            idempotency=Idempotency.from_dict(data["idempotency"]),
            deadline=data.get("deadline"),
            result_channel=data.get("result_channel"),
            identity_context=IdentityContext.from_dict(identity) if identity is not None else None,
        )


@dataclass(frozen=True, slots=True)
class JobStatus:
    job_id: str
    state: JobState
    observed_at: datetime
    correlation_id: str
    progress: int | None = None
    result: Mapping[str, Any] | None = None
    error: ErrorEnvelope | None = None
    reason_codes: tuple[str, ...] = ()

    SCHEMA_PATH: ClassVar[str] = JOB_STATUS_SCHEMA_PATH

    def __post_init__(self) -> None:
        object.__setattr__(self, "job_id", _require_text(self.job_id, "job_id"))
        object.__setattr__(self, "state", _enum_value(JobState, self.state, "state"))
        object.__setattr__(self, "observed_at", _parse_timestamp(self.observed_at, "observed_at"))
        object.__setattr__(
            self, "correlation_id", _require_text(self.correlation_id, "correlation_id")
        )
        if self.progress is not None and (
            not isinstance(self.progress, int) or not 0 <= self.progress <= 100
        ):
            raise InterfaceValidationError("progress must be an integer from 0 to 100")
        if self.result is not None:
            object.__setattr__(self, "result", _freeze_mapping(self.result, "result"))
        if self.error is not None and not isinstance(self.error, ErrorEnvelope):
            raise InterfaceValidationError("error must be an ErrorEnvelope")
        object.__setattr__(self, "reason_codes", _string_tuple(self.reason_codes, "reason_codes"))
        if self.state is JobState.COMPLETED and self.error is not None:
            raise InterfaceValidationError("completed job cannot contain an error")
        if self.state is JobState.FAILED and self.error is None:
            raise InterfaceValidationError("failed job must contain an error")
        if self.state is JobState.COMPLETED and self.progress not in {None, 100}:
            raise InterfaceValidationError("completed job progress must be 100 when present")

    @property
    def terminal(self) -> bool:
        return self.state in {
            JobState.COMPLETED,
            JobState.CANCELLED,
            JobState.FAILED,
            JobState.CONFLICTED,
            JobState.EXPIRED,
        }

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "job_id": self.job_id,
            "state": self.state.value,
            "observed_at": _format_timestamp(self.observed_at),
            "correlation_id": self.correlation_id,
            "reason_codes": list(self.reason_codes),
        }
        if self.progress is not None:
            result["progress"] = self.progress
        if self.result is not None:
            result["result"] = dict(self.result)
        if self.error is not None:
            result["error"] = self.error.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> JobStatus:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("job status must be an object")
        allowed = {
            "job_id", "state", "observed_at", "correlation_id", "progress", "result",
            "error", "reason_codes",
        }
        _unexpected_fields(data, allowed)
        required = {"job_id", "state", "observed_at", "correlation_id"}
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        error = data.get("error")
        return cls(
            job_id=data["job_id"],
            state=data["state"],
            observed_at=data["observed_at"],
            correlation_id=data["correlation_id"],
            progress=data.get("progress"),
            result=_freeze_mapping(data["result"], "result") if "result" in data else None,
            error=ErrorEnvelope.from_dict(error) if error is not None else None,
            reason_codes=_string_tuple(data.get("reason_codes"), "reason_codes"),
        )


class _UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: str, timeout: float) -> None:
        super().__init__("localhost", timeout=timeout)
        self._socket_path = socket_path

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
            sock.connect(self._socket_path)
        except OSError:
            sock.close()
            raise
        self.sock = sock


class UnixHttpClient:
    """Minimal JSON client for HTTP over a local Unix-domain socket.

    The client performs no implicit retry and does not infer authorization from
    successful transport. Callers own retry and reconciliation decisions.
    """

    def __init__(
        self,
        socket_path: str | Path,
        *,
        sender: str,
        timeout_seconds: float = 5.0,
        max_response_bytes: int = 1_048_576,
        interface_version: str = "1.0.0",
    ) -> None:
        self.socket_path = str(socket_path)
        self.sender = _require_text(sender, "sender")
        self.interface_version = _require_text(interface_version, "interface_version")
        if timeout_seconds <= 0:
            raise InterfaceValidationError("timeout_seconds must be positive")
        if max_response_bytes <= 0:
            raise InterfaceValidationError("max_response_bytes must be positive")
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes

    @staticmethod
    def _validate_path(path: str) -> str:
        normalized = _require_text(path, "path")
        if not normalized.startswith("/") or normalized.startswith("//"):
            raise InterfaceValidationError("path must be an absolute origin-form path")
        pure = PurePosixPath(normalized.split("?", 1)[0])
        if ".." in pure.parts:
            raise InterfaceValidationError("path traversal is not permitted")
        return normalized

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Mapping[str, Any] | None = None,
        correlation: Correlation | None = None,
        idempotency_key: str | None = None,
        headers: Mapping[str, str] | None = None,
        expected_status: Sequence[int] = (200,),
    ) -> Mapping[str, Any] | None:
        verb = _require_text(method, "method").upper()
        request_path = self._validate_path(path)
        expected = tuple(expected_status)
        if not expected or any(not isinstance(status, int) for status in expected):
            raise InterfaceValidationError("expected_status must contain HTTP status integers")
        request_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "koa-interfaces/0.1.0",
            "X-kOA-Sender": self.sender,
            "X-kOA-Interface-Version": self.interface_version,
        }
        if correlation is not None:
            request_headers["X-Correlation-ID"] = correlation.correlation_id
            if correlation.request_id is not None:
                request_headers["X-Request-ID"] = correlation.request_id
            if correlation.causation_id is not None:
                request_headers["X-Causation-ID"] = correlation.causation_id
        if idempotency_key is not None:
            request_headers["Idempotency-Key"] = _require_text(
                idempotency_key, "idempotency_key"
            )
        if headers is not None:
            for key, value in headers.items():
                normalized_key = _require_text(key, "header name")
                normalized_value = _require_text(value, f"header {normalized_key}")
                if "\r" in normalized_key or "\n" in normalized_key:
                    raise InterfaceValidationError("header names cannot contain newlines")
                if "\r" in normalized_value or "\n" in normalized_value:
                    raise InterfaceValidationError("header values cannot contain newlines")
                request_headers[normalized_key] = normalized_value
        payload = None
        if body is not None:
            try:
                payload = json.dumps(
                    dict(_freeze_mapping(body, "body")),
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                ).encode("utf-8")
            except (TypeError, ValueError) as exc:
                raise InterfaceValidationError("body must contain JSON-compatible values") from exc
            request_headers["Content-Length"] = str(len(payload))
        connection = _UnixHTTPConnection(self.socket_path, self.timeout_seconds)
        try:
            connection.request(verb, request_path, body=payload, headers=request_headers)
            response = connection.getresponse()
            raw = response.read(self.max_response_bytes + 1)
        except (OSError, TimeoutError, http.client.HTTPException) as exc:
            raise TransportError(f"HTTP-over-Unix request failed: {exc}") from exc
        finally:
            connection.close()
        if len(raw) > self.max_response_bytes:
            raise ProtocolError("response exceeds max_response_bytes")
        parsed: Mapping[str, Any] | None
        if raw:
            content_type = response.getheader("Content-Type", "")
            if "application/json" not in content_type.lower():
                raise ProtocolError("non-empty response must use application/json")
            try:
                value = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise ProtocolError("response body is not valid UTF-8 JSON") from exc
            if not isinstance(value, dict):
                raise ProtocolError("response JSON root must be an object")
            parsed = MappingProxyType(value)
        else:
            parsed = None
        if response.status not in expected:
            if parsed is None:
                raise ProtocolError(f"HTTP {response.status} response omitted error envelope")
            try:
                envelope = ErrorEnvelope.from_dict(parsed)
            except InterfaceValidationError as exc:
                raise ProtocolError(
                    f"HTTP {response.status} response contains an invalid error envelope"
                ) from exc
            raise RemoteError(response.status, envelope)
        return parsed

    def health(self) -> HealthStatus:
        payload = self.request("GET", "/health", expected_status=(200,))
        if payload is None:
            raise ProtocolError("health response cannot be empty")
        return HealthStatus.from_dict(payload)

    def readiness(self, readiness_class: ReadinessClass | None = None) -> Readiness:
        path = "/readiness"
        if readiness_class is not None:
            selected = _enum_value(ReadinessClass, readiness_class, "readiness_class")
            path += "?" + urlencode({"class": selected.value})
        payload = self.request("GET", path, expected_status=(200,))
        if payload is None:
            raise ProtocolError("readiness response cannot be empty")
        return Readiness.from_dict(payload)

    def submit_job(self, request: JobRequest) -> JobStatus:
        if not isinstance(request, JobRequest):
            raise InterfaceValidationError("request must be a JobRequest")
        payload = self.request(
            "POST",
            "/jobs",
            body=request.to_dict(),
            correlation=request.correlation,
            idempotency_key=request.idempotency.key,
            expected_status=(200, 202),
        )
        if payload is None:
            raise ProtocolError("job submission response cannot be empty")
        return JobStatus.from_dict(payload)

    def job_status(self, job_id: str, *, correlation: Correlation | None = None) -> JobStatus:
        normalized = _require_text(job_id, "job_id")
        if "/" in normalized:
            raise InterfaceValidationError("job_id cannot contain a path separator")
        payload = self.request(
            "GET",
            f"/jobs/{normalized}",
            correlation=correlation,
            expected_status=(200,),
        )
        if payload is None:
            raise ProtocolError("job status response cannot be empty")
        return JobStatus.from_dict(payload)
