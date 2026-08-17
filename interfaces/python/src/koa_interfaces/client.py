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
    """Canonical idempotency context projected from idempotency.schema.json."""

    idempotency_key: str
    operation: str
    owner_component_id: str
    scope: Mapping[str, Any]
    canonical_request: Mapping[str, Any]
    duplicate_handling: Mapping[str, Any]
    validity: Mapping[str, Any]
    authority: Mapping[str, Any]
    schema_version: str = "1.0.0"
    request_id: str | None = None
    correlation_id: str | None = None
    expected_state: Mapping[str, Any] | None = None
    anti_replay: Mapping[str, Any] | None = None

    SCHEMA_PATH: ClassVar[str] = IDEMPOTENCY_SCHEMA_PATH

    def __post_init__(self) -> None:
        for field_name in (
            "idempotency_key",
            "operation",
            "owner_component_id",
            "schema_version",
        ):
            object.__setattr__(
                self, field_name, _require_text(getattr(self, field_name), field_name)
            )
        if self.schema_version != "1.0.0":
            raise InterfaceValidationError("schema_version must be 1.0.0")

        object.__setattr__(self, "request_id", _optional_text(self.request_id, "request_id"))
        object.__setattr__(
            self, "correlation_id", _optional_text(self.correlation_id, "correlation_id")
        )

        scope = _closed_event_mapping(
            self.scope,
            field_name="scope",
            required={"kind"},
            allowed={"kind", "target_ref", "workflow_id", "step_id"},
        )
        scope_kind = scope["kind"]
        if scope_kind not in {"owner_operation", "owner_operation_target", "workflow_step"}:
            raise InterfaceValidationError("scope.kind is not supported")
        if scope_kind == "owner_operation_target":
            if "target_ref" not in scope:
                raise InterfaceValidationError("scope.target_ref is required for owner_operation_target")
            _require_text(scope["target_ref"], "scope.target_ref")
        if scope_kind == "workflow_step":
            for key in ("workflow_id", "step_id"):
                if key not in scope:
                    raise InterfaceValidationError(f"scope.{key} is required for workflow_step")
                _require_text(scope[key], f"scope.{key}")
        for key in ("target_ref", "workflow_id", "step_id"):
            if key in scope:
                _require_text(scope[key], f"scope.{key}")
        object.__setattr__(self, "scope", scope)

        canonical_request = _closed_event_mapping(
            self.canonical_request,
            field_name="canonical_request",
            required={"algorithm", "digest", "media_type"},
            allowed={"algorithm", "digest", "media_type", "schema_ref", "schema_version"},
        )
        if canonical_request["algorithm"] != "sha256":
            raise InterfaceValidationError("canonical_request.algorithm must be sha256")
        digest = _require_text(canonical_request["digest"], "canonical_request.digest")
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise InterfaceValidationError(
                "canonical_request.digest must be lowercase sha256 hex"
            )
        _require_text(canonical_request["media_type"], "canonical_request.media_type")
        has_schema_ref = "schema_ref" in canonical_request
        has_schema_version = "schema_version" in canonical_request
        if has_schema_ref != has_schema_version:
            raise InterfaceValidationError(
                "canonical_request.schema_ref and schema_version must be provided together"
            )
        if has_schema_ref:
            _require_text(canonical_request["schema_ref"], "canonical_request.schema_ref")
            _require_text(
                canonical_request["schema_version"], "canonical_request.schema_version"
            )
        object.__setattr__(self, "canonical_request", canonical_request)

        duplicate_handling = _closed_event_mapping(
            self.duplicate_handling,
            field_name="duplicate_handling",
            required={"action", "result_consistency"},
            allowed={"action", "result_consistency", "terminal_result_ref_required"},
        )
        action = duplicate_handling["action"]
        consistency = duplicate_handling["result_consistency"]
        if action not in {
            "return_prior_result",
            "resume_existing_operation",
            "reject_duplicate",
            "reconcile_before_retry",
        }:
            raise InterfaceValidationError("duplicate_handling.action is not supported")
        if consistency not in {"exact_prior_result", "current_status", "reconciled_result"}:
            raise InterfaceValidationError(
                "duplicate_handling.result_consistency is not supported"
            )
        expected_consistency = {
            "return_prior_result": "exact_prior_result",
            "resume_existing_operation": "current_status",
            "reconcile_before_retry": "reconciled_result",
        }.get(action)
        if expected_consistency is not None and consistency != expected_consistency:
            raise InterfaceValidationError(
                f"duplicate_handling.result_consistency must be {expected_consistency} "
                f"for {action}"
            )
        if action == "return_prior_result":
            if duplicate_handling.get("terminal_result_ref_required") is not True:
                raise InterfaceValidationError(
                    "duplicate_handling.terminal_result_ref_required must be true "
                    "for return_prior_result"
                )
        elif "terminal_result_ref_required" in duplicate_handling and not isinstance(
            duplicate_handling["terminal_result_ref_required"], bool
        ):
            raise InterfaceValidationError(
                "duplicate_handling.terminal_result_ref_required must be a boolean"
            )
        object.__setattr__(self, "duplicate_handling", duplicate_handling)

        validity_source = dict(self.validity) if isinstance(self.validity, Mapping) else self.validity
        validity = _closed_event_mapping(
            validity_source,
            field_name="validity",
            required={"created_at"},
            allowed={"created_at", "expires_at", "retain_terminal_result_seconds"},
        )
        _parse_timestamp(validity["created_at"], "validity.created_at")
        if "expires_at" in validity:
            _parse_timestamp(validity["expires_at"], "validity.expires_at")
        if "retain_terminal_result_seconds" in validity:
            retain_seconds = validity["retain_terminal_result_seconds"]
            if (
                isinstance(retain_seconds, bool)
                or not isinstance(retain_seconds, int)
                or retain_seconds < 0
            ):
                raise InterfaceValidationError(
                    "validity.retain_terminal_result_seconds must be a non-negative integer"
                )
        object.__setattr__(self, "validity", validity)

        authority = _closed_event_mapping(
            self.authority,
            field_name="authority",
            required={
                "receiving_owner_enforces",
                "transport_grants_authority",
                "duplicate_effects_permitted",
            },
            allowed={
                "receiving_owner_enforces",
                "transport_grants_authority",
                "duplicate_effects_permitted",
            },
        )
        if authority["receiving_owner_enforces"] is not True:
            raise InterfaceValidationError("authority.receiving_owner_enforces must be true")
        if authority["transport_grants_authority"] is not False:
            raise InterfaceValidationError("authority.transport_grants_authority must be false")
        if authority["duplicate_effects_permitted"] is not False:
            raise InterfaceValidationError("authority.duplicate_effects_permitted must be false")
        object.__setattr__(self, "authority", authority)

        if self.expected_state is not None:
            expected_state = _closed_event_mapping(
                self.expected_state,
                field_name="expected_state",
                required={"kind", "value"},
                allowed={"kind", "value"},
            )
            if expected_state["kind"] not in {"version", "etag", "digest", "state_id"}:
                raise InterfaceValidationError("expected_state.kind is not supported")
            _require_text(expected_state["value"], "expected_state.value")
            object.__setattr__(self, "expected_state", expected_state)

        if self.anti_replay is not None:
            anti_replay = _closed_event_mapping(
                self.anti_replay,
                field_name="anti_replay",
                required=set(),
                allowed={"nonce", "sequence", "challenge_ref"},
            )
            if not anti_replay:
                raise InterfaceValidationError("anti_replay must not be empty")
            for key in ("nonce", "challenge_ref"):
                if key in anti_replay:
                    _require_text(anti_replay[key], f"anti_replay.{key}")
            if "sequence" in anti_replay:
                sequence = anti_replay["sequence"]
                if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
                    raise InterfaceValidationError(
                        "anti_replay.sequence must be a non-negative integer"
                    )
            object.__setattr__(self, "anti_replay", anti_replay)

    @property
    def required(self) -> bool:
        """Compatibility view: a canonical Idempotency object is always required/present."""
        return True

    @property
    def key(self) -> str:
        """Compatibility alias used by the HTTP Idempotency-Key header."""
        return self.idempotency_key

    @property
    def duplicate_outcome(self) -> DuplicateOutcome | None:
        mapping = {
            "return_prior_result": DuplicateOutcome.RETURN_PRIOR_RESULT,
            "reject_duplicate": DuplicateOutcome.REJECT,
        }
        return mapping.get(self.duplicate_handling["action"])

    @property
    def retention_rule(self) -> str | None:
        seconds = self.validity.get("retain_terminal_result_seconds")
        if isinstance(seconds, int):
            return f"retain terminal result for {seconds} seconds"
        return None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "idempotency_key": self.idempotency_key,
            "operation": self.operation,
            "owner_component_id": self.owner_component_id,
            "scope": _plain_json_value(self.scope),
            "canonical_request": _plain_json_value(self.canonical_request),
            "duplicate_handling": _plain_json_value(self.duplicate_handling),
            "validity": _plain_json_value(self.validity),
            "authority": _plain_json_value(self.authority),
        }
        if self.request_id is not None:
            result["request_id"] = self.request_id
        if self.correlation_id is not None:
            result["correlation_id"] = self.correlation_id
        if self.expected_state is not None:
            result["expected_state"] = _plain_json_value(self.expected_state)
        if self.anti_replay is not None:
            result["anti_replay"] = _plain_json_value(self.anti_replay)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Idempotency:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("idempotency must be an object")
        allowed = {
            "schema_version",
            "idempotency_key",
            "request_id",
            "correlation_id",
            "operation",
            "owner_component_id",
            "scope",
            "canonical_request",
            "expected_state",
            "duplicate_handling",
            "validity",
            "anti_replay",
            "authority",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version",
            "idempotency_key",
            "operation",
            "owner_component_id",
            "scope",
            "canonical_request",
            "duplicate_handling",
            "validity",
            "authority",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(
                "idempotency missing fields: " + ", ".join(missing)
            )
        return cls(
            schema_version=data["schema_version"],
            idempotency_key=data["idempotency_key"],
            request_id=data.get("request_id"),
            correlation_id=data.get("correlation_id"),
            operation=data["operation"],
            owner_component_id=data["owner_component_id"],
            scope=data["scope"],
            canonical_request=data["canonical_request"],
            expected_state=data.get("expected_state"),
            duplicate_handling=data["duplicate_handling"],
            validity=data["validity"],
            anti_replay=data.get("anti_replay"),
            authority=data["authority"],
        )


@dataclass(frozen=True, slots=True)
class VersionNegotiation:
    """Canonical version-negotiation message projected from the transport schema."""

    message_type: str
    negotiation_id: str
    interface_id: str
    sender: Mapping[str, Any]
    intended_receiver: Mapping[str, Any]
    correlation_id: str
    authority: Mapping[str, Any]
    schema_version: str = "1.0.0"
    offered_versions: tuple[str, ...] | None = None
    preferred_version: str | None = None
    selected_version: str | None = None
    compatibility_mode: str | None = None
    rejection: Mapping[str, Any] | None = None
    release_context: Mapping[str, Any] | None = None

    SCHEMA_PATH: ClassVar[str] = VERSION_NEGOTIATION_SCHEMA_PATH
    AUTOMATIC_SCHEMA_GUESSING: ClassVar[bool] = False

    def __post_init__(self) -> None:
        for field_name in (
            "message_type",
            "negotiation_id",
            "interface_id",
            "correlation_id",
            "schema_version",
        ):
            object.__setattr__(
                self, field_name, _require_text(getattr(self, field_name), field_name)
            )
        if self.schema_version != "1.0.0":
            raise InterfaceValidationError("schema_version must be 1.0.0")
        if self.message_type not in {
            "version_offer",
            "version_selection",
            "version_rejection",
        }:
            raise InterfaceValidationError("message_type is not supported")

        sender = _closed_event_mapping(
            self.sender,
            field_name="sender",
            required={"component_id"},
            allowed={"component_id", "instance_id", "profile_id"},
        )
        for key, value in sender.items():
            _require_text(value, f"sender.{key}")
        object.__setattr__(self, "sender", sender)

        receiver = _closed_event_mapping(
            self.intended_receiver,
            field_name="intended_receiver",
            required={"kind", "identifier"},
            allowed={"kind", "identifier"},
        )
        receiver_kind = _require_text(receiver["kind"], "intended_receiver.kind")
        if receiver_kind not in {"component", "capability", "subscription", "topic"}:
            raise InterfaceValidationError("intended_receiver.kind is not supported")
        _require_text(receiver["identifier"], "intended_receiver.identifier")
        object.__setattr__(self, "intended_receiver", receiver)

        if self.offered_versions is not None:
            offered_versions = _string_tuple(self.offered_versions, "offered_versions")
            if not offered_versions:
                raise InterfaceValidationError("offered_versions must not be empty")
            object.__setattr__(self, "offered_versions", offered_versions)

        for field_name in ("preferred_version", "selected_version", "compatibility_mode"):
            object.__setattr__(
                self, field_name, _optional_text(getattr(self, field_name), field_name)
            )
        if self.compatibility_mode is not None and self.compatibility_mode not in {
            "exact",
            "backward_compatible",
            "coordinated_transition_required",
        }:
            raise InterfaceValidationError("compatibility_mode is not supported")

        if self.rejection is not None:
            rejection = _closed_event_mapping(
                self.rejection,
                field_name="rejection",
                required={"reason_code", "existing_valid_state_preserved"},
                allowed={"reason_code", "message", "existing_valid_state_preserved"},
            )
            reason_code = _require_text(rejection["reason_code"], "rejection.reason_code")
            if reason_code not in {
                "no_common_version",
                "interface_unknown",
                "contract_inactive",
                "contract_invalid",
                "release_incompatible",
                "coordinated_transition_required",
            }:
                raise InterfaceValidationError("rejection.reason_code is not supported")
            if "message" in rejection:
                _require_text(rejection["message"], "rejection.message")
            if rejection["existing_valid_state_preserved"] is not True:
                raise InterfaceValidationError(
                    "rejection.existing_valid_state_preserved must be true"
                )
            object.__setattr__(self, "rejection", rejection)

        if self.release_context is not None:
            release_context = _closed_event_mapping(
                self.release_context,
                field_name="release_context",
                required=set(),
                allowed={"release_set_id", "sender_release", "receiver_release"},
            )
            if not release_context:
                raise InterfaceValidationError("release_context must not be empty")
            for key, value in release_context.items():
                _require_text(value, f"release_context.{key}")
            object.__setattr__(self, "release_context", release_context)

        authority = _closed_event_mapping(
            self.authority,
            field_name="authority",
            required={
                "transport_grants_authority",
                "selection_changes_domain_authority",
                "receiving_contract_remains_authoritative",
            },
            allowed={
                "transport_grants_authority",
                "selection_changes_domain_authority",
                "receiving_contract_remains_authoritative",
            },
        )
        if authority["transport_grants_authority"] is not False:
            raise InterfaceValidationError("authority.transport_grants_authority must be false")
        if authority["selection_changes_domain_authority"] is not False:
            raise InterfaceValidationError(
                "authority.selection_changes_domain_authority must be false"
            )
        if authority["receiving_contract_remains_authoritative"] is not True:
            raise InterfaceValidationError(
                "authority.receiving_contract_remains_authoritative must be true"
            )
        object.__setattr__(self, "authority", authority)

        if self.message_type == "version_offer":
            if self.offered_versions is None or self.preferred_version is None:
                raise InterfaceValidationError(
                    "version_offer requires offered_versions and preferred_version"
                )
            if self.selected_version is not None or self.rejection is not None:
                raise InterfaceValidationError(
                    "version_offer must omit selected_version and rejection"
                )
        elif self.message_type == "version_selection":
            if (
                self.offered_versions is None
                or self.selected_version is None
                or self.compatibility_mode is None
            ):
                raise InterfaceValidationError(
                    "version_selection requires offered_versions, selected_version "
                    "and compatibility_mode"
                )
            if self.rejection is not None:
                raise InterfaceValidationError("version_selection must omit rejection")
        else:
            if self.rejection is None:
                raise InterfaceValidationError("version_rejection requires rejection")
            if self.selected_version is not None:
                raise InterfaceValidationError("version_rejection must omit selected_version")

        if (
            self.preferred_version is not None
            and self.offered_versions is not None
            and self.preferred_version not in self.offered_versions
        ):
            raise InterfaceValidationError("preferred_version must be present in offered_versions")
        if (
            self.selected_version is not None
            and self.offered_versions is not None
            and self.selected_version not in self.offered_versions
        ):
            raise InterfaceValidationError("selected_version must be present in offered_versions")

    @property
    def supported_versions(self) -> tuple[str, ...]:
        """Compatibility view of the explicitly offered versions."""
        return self.offered_versions or ()

    def select(self, peer_supported_versions: Sequence[str]) -> str:
        """Choose only from an explicit offer; callers must emit a selection message separately."""
        if self.message_type != "version_offer" or self.offered_versions is None:
            raise InterfaceValidationError("selection requires a version_offer message")
        peer = _string_tuple(tuple(peer_supported_versions), "peer_supported_versions")
        if self.preferred_version is not None and self.preferred_version in peer:
            return self.preferred_version
        for candidate in self.offered_versions:
            if candidate in peer:
                return candidate
        raise InterfaceValidationError("no mutually supported interface version")

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "message_type": self.message_type,
            "negotiation_id": self.negotiation_id,
            "interface_id": self.interface_id,
            "sender": _plain_json_value(self.sender),
            "intended_receiver": _plain_json_value(self.intended_receiver),
            "correlation_id": self.correlation_id,
            "automatic_schema_guessing": self.AUTOMATIC_SCHEMA_GUESSING,
            "authority": _plain_json_value(self.authority),
        }
        if self.offered_versions is not None:
            result["offered_versions"] = list(self.offered_versions)
        if self.preferred_version is not None:
            result["preferred_version"] = self.preferred_version
        if self.selected_version is not None:
            result["selected_version"] = self.selected_version
        if self.compatibility_mode is not None:
            result["compatibility_mode"] = self.compatibility_mode
        if self.rejection is not None:
            result["rejection"] = _plain_json_value(self.rejection)
        if self.release_context is not None:
            result["release_context"] = _plain_json_value(self.release_context)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> VersionNegotiation:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("version negotiation must be an object")
        allowed = {
            "schema_version",
            "message_type",
            "negotiation_id",
            "interface_id",
            "sender",
            "intended_receiver",
            "correlation_id",
            "offered_versions",
            "preferred_version",
            "selected_version",
            "compatibility_mode",
            "rejection",
            "release_context",
            "automatic_schema_guessing",
            "authority",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version",
            "message_type",
            "negotiation_id",
            "interface_id",
            "sender",
            "intended_receiver",
            "correlation_id",
            "automatic_schema_guessing",
            "authority",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(
                "version negotiation missing fields: " + ", ".join(missing)
            )
        if data["automatic_schema_guessing"] is not False:
            raise InterfaceValidationError("automatic_schema_guessing must be false")
        return cls(
            schema_version=data["schema_version"],
            message_type=data["message_type"],
            negotiation_id=data["negotiation_id"],
            interface_id=data["interface_id"],
            sender=data["sender"],
            intended_receiver=data["intended_receiver"],
            correlation_id=data["correlation_id"],
            offered_versions=(
                _string_tuple(data["offered_versions"], "offered_versions")
                if "offered_versions" in data
                else None
            ),
            preferred_version=data.get("preferred_version"),
            selected_version=data.get("selected_version"),
            compatibility_mode=data.get("compatibility_mode"),
            rejection=data.get("rejection"),
            release_context=data.get("release_context"),
            authority=data["authority"],
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


def _freeze_json_value(value: Any, field_name: str) -> Any:
    if isinstance(value, Mapping):
        frozen: dict[str, Any] = {}
        for key, child in value.items():
            if not isinstance(key, str):
                raise InterfaceValidationError(f"{field_name} object keys must be strings")
            frozen[key] = _freeze_json_value(child, field_name)
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json_value(child, field_name) for child in value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise InterfaceValidationError(f"{field_name} must contain JSON-compatible values")


def _plain_json_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain_json_value(child) for key, child in value.items()}
    if isinstance(value, tuple):
        return [_plain_json_value(child) for child in value]
    if isinstance(value, list):
        return [_plain_json_value(child) for child in value]
    return value


def _closed_event_mapping(
    value: Mapping[str, Any],
    *,
    field_name: str,
    required: set[str],
    allowed: set[str],
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InterfaceValidationError(f"{field_name} must be an object")
    _unexpected_fields(value, allowed)
    missing = sorted(required - set(value))
    if missing:
        raise InterfaceValidationError(
            f"{field_name} missing fields: {', '.join(missing)}"
        )
    return _freeze_json_value(value, field_name)


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Canonical domain-event envelope projected from event-envelope.schema.json."""

    message_id: str
    event_id: str
    event_type: str
    event_version: str
    interface: Mapping[str, Any]
    publisher: Mapping[str, Any]
    intended_receivers: tuple[Mapping[str, Any], ...]
    correlation: Correlation
    occurred_at: datetime
    committed_at: datetime
    payload_representation: Mapping[str, Any]
    payload: Any
    ordering: Mapping[str, Any]
    replay: Mapping[str, Any]
    disclosure: Mapping[str, Any]
    authority: Mapping[str, Any]
    schema_version: str = "1.0.0"
    expires_at: datetime | None = None
    compatibility: Mapping[str, Any] | None = None
    evidence: Mapping[str, Any] | None = None

    SCHEMA_PATH: ClassVar[str] = EVENT_ENVELOPE_SCHEMA_PATH
    ENVELOPE_TYPE: ClassVar[str] = "domain_event"

    def __post_init__(self) -> None:
        for field_name in (
            "message_id",
            "event_id",
            "event_type",
            "event_version",
            "schema_version",
        ):
            object.__setattr__(
                self, field_name, _require_text(getattr(self, field_name), field_name)
            )
        if self.schema_version != "1.0.0":
            raise InterfaceValidationError("schema_version must be 1.0.0")

        interface = _closed_event_mapping(
            self.interface,
            field_name="interface",
            required={"interface_id", "interface_version"},
            allowed={"interface_id", "interface_version", "contract_ref"},
        )
        for key in ("interface_id", "interface_version"):
            _require_text(interface[key], f"interface.{key}")
        if "contract_ref" in interface:
            _require_text(interface["contract_ref"], "interface.contract_ref")
        object.__setattr__(self, "interface", interface)

        publisher = _closed_event_mapping(
            self.publisher,
            field_name="publisher",
            required={"component_id"},
            allowed={"component_id", "instance_id", "profile_id"},
        )
        for key, value in publisher.items():
            _require_text(value, f"publisher.{key}")
        object.__setattr__(self, "publisher", publisher)

        if not isinstance(self.intended_receivers, (list, tuple)) or not self.intended_receivers:
            raise InterfaceValidationError("intended_receivers must contain at least one receiver")
        receivers: list[Mapping[str, Any]] = []
        seen_receivers: set[tuple[str, str]] = set()
        for index, receiver in enumerate(self.intended_receivers):
            frozen = _closed_event_mapping(
                receiver,
                field_name=f"intended_receivers[{index}]",
                required={"kind", "identifier"},
                allowed={"kind", "identifier"},
            )
            kind = _require_text(frozen["kind"], f"intended_receivers[{index}].kind")
            identifier = _require_text(
                frozen["identifier"], f"intended_receivers[{index}].identifier"
            )
            if kind not in {"component", "capability", "subscription", "topic"}:
                raise InterfaceValidationError(
                    f"intended_receivers[{index}].kind is not supported"
                )
            identity = (kind, identifier)
            if identity in seen_receivers:
                raise InterfaceValidationError("intended_receivers must be unique")
            seen_receivers.add(identity)
            receivers.append(frozen)
        object.__setattr__(self, "intended_receivers", tuple(receivers))

        if not isinstance(self.correlation, Correlation):
            raise InterfaceValidationError("correlation must be a Correlation")
        object.__setattr__(self, "occurred_at", _parse_timestamp(self.occurred_at, "occurred_at"))
        object.__setattr__(
            self, "committed_at", _parse_timestamp(self.committed_at, "committed_at")
        )
        if self.committed_at < self.occurred_at:
            raise InterfaceValidationError("committed_at cannot precede occurred_at")
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _parse_timestamp(self.expires_at, "expires_at"))
            if self.expires_at <= self.committed_at:
                raise InterfaceValidationError("expires_at must be later than committed_at")

        representation = _closed_event_mapping(
            self.payload_representation,
            field_name="payload_representation",
            required={"media_type", "schema_ref", "schema_version"},
            allowed={"media_type", "schema_ref", "schema_version", "encoding", "content_digest"},
        )
        for key in ("media_type", "schema_ref", "schema_version"):
            _require_text(representation[key], f"payload_representation.{key}")
        if "encoding" in representation and representation["encoding"] not in {
            "identity",
            "base64",
            "uri_reference",
        }:
            raise InterfaceValidationError("payload_representation.encoding is not supported")
        if "content_digest" in representation:
            digest = _closed_event_mapping(
                representation["content_digest"],
                field_name="payload_representation.content_digest",
                required={"algorithm", "value"},
                allowed={"algorithm", "value"},
            )
            if digest["algorithm"] != "sha256":
                raise InterfaceValidationError(
                    "payload_representation.content_digest.algorithm must be sha256"
                )
            value = _require_text(
                digest["value"], "payload_representation.content_digest.value"
            )
            if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
                raise InterfaceValidationError(
                    "payload_representation.content_digest.value must be lowercase sha256 hex"
                )
        object.__setattr__(self, "payload_representation", representation)
        object.__setattr__(self, "payload", _freeze_json_value(self.payload, "payload"))

        ordering = _closed_event_mapping(
            self.ordering,
            field_name="ordering",
            required={"scope", "sequence"},
            allowed={"scope", "sequence", "partition_key"},
        )
        _require_text(ordering["scope"], "ordering.scope")
        sequence = ordering["sequence"]
        if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
            raise InterfaceValidationError("ordering.sequence must be a non-negative integer")
        if "partition_key" in ordering:
            _require_text(ordering["partition_key"], "ordering.partition_key")
        object.__setattr__(self, "ordering", ordering)

        replay = _closed_event_mapping(
            self.replay,
            field_name="replay",
            required={"mode", "duplicate_handling"},
            allowed={
                "mode",
                "duplicate_handling",
                "original_message_id",
                "replayed_at",
                "replay_reason",
            },
        )
        mode = replay["mode"]
        if mode not in {"original", "replay"}:
            raise InterfaceValidationError("replay.mode is not supported")
        if replay["duplicate_handling"] not in {
            "ignore_if_applied",
            "return_current_state",
            "rebuild_projection",
            "reject_duplicate",
        }:
            raise InterfaceValidationError("replay.duplicate_handling is not supported")
        replay_fields = {"original_message_id", "replayed_at", "replay_reason"}
        if mode == "original" and replay_fields.intersection(replay):
            raise InterfaceValidationError("original replay mode must omit replay-only fields")
        if mode == "replay":
            missing = {"original_message_id", "replayed_at"} - set(replay)
            if missing:
                raise InterfaceValidationError(
                    "replay mode missing fields: " + ", ".join(sorted(missing))
                )
            _require_text(replay["original_message_id"], "replay.original_message_id")
            _parse_timestamp(replay["replayed_at"], "replay.replayed_at")
        object.__setattr__(self, "replay", replay)

        disclosure = _closed_event_mapping(
            self.disclosure,
            field_name="disclosure",
            required={"class", "payload_minimized"},
            allowed={"class", "payload_minimized", "redaction_applied"},
        )
        if disclosure["class"] not in {
            "public_summary",
            "tenant_visible",
            "operator_restricted",
            "security_restricted",
            "evidence_restricted",
        }:
            raise InterfaceValidationError("disclosure.class is not supported")
        if disclosure["payload_minimized"] is not True:
            raise InterfaceValidationError("disclosure.payload_minimized must be true")
        if "redaction_applied" in disclosure and not isinstance(
            disclosure["redaction_applied"], bool
        ):
            raise InterfaceValidationError("disclosure.redaction_applied must be a boolean")
        object.__setattr__(self, "disclosure", disclosure)

        authority = _closed_event_mapping(
            self.authority,
            field_name="authority",
            required={
                "effect",
                "publisher_owns_fact",
                "grants_mutation_authority",
                "transfers_ownership",
            },
            allowed={
                "effect",
                "publisher_owns_fact",
                "grants_mutation_authority",
                "transfers_ownership",
            },
        )
        expected_authority = {
            "effect": "committed_fact_evidence",
            "publisher_owns_fact": True,
            "grants_mutation_authority": False,
            "transfers_ownership": False,
        }
        if dict(authority) != expected_authority:
            raise InterfaceValidationError("authority must preserve committed-fact ownership semantics")
        object.__setattr__(self, "authority", authority)

        if self.compatibility is not None:
            compatibility = _closed_event_mapping(
                self.compatibility,
                field_name="compatibility",
                required=set(),
                allowed={"minimum_consumer_version", "release_context"},
            )
            if not compatibility:
                raise InterfaceValidationError("compatibility must not be empty")
            object.__setattr__(self, "compatibility", compatibility)
        if self.evidence is not None:
            evidence = _closed_event_mapping(
                self.evidence,
                field_name="evidence",
                required=set(),
                allowed={"receipt_refs", "evidence_refs"},
            )
            if not evidence:
                raise InterfaceValidationError("evidence must not be empty")
            object.__setattr__(self, "evidence", evidence)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "schema_version": self.schema_version,
            "envelope_type": self.ENVELOPE_TYPE,
            "message_id": self.message_id,
            "event_id": self.event_id,
            "event_type": self.event_type,
            "event_version": self.event_version,
            "interface": _plain_json_value(self.interface),
            "publisher": _plain_json_value(self.publisher),
            "intended_receivers": _plain_json_value(self.intended_receivers),
            "correlation": self.correlation.to_dict(),
            "occurred_at": _format_timestamp(self.occurred_at),
            "committed_at": _format_timestamp(self.committed_at),
            "payload_representation": _plain_json_value(self.payload_representation),
            "payload": _plain_json_value(self.payload),
            "ordering": _plain_json_value(self.ordering),
            "replay": _plain_json_value(self.replay),
            "disclosure": _plain_json_value(self.disclosure),
            "authority": _plain_json_value(self.authority),
        }
        if self.expires_at is not None:
            result["expires_at"] = _format_timestamp(self.expires_at)
        if self.compatibility is not None:
            result["compatibility"] = _plain_json_value(self.compatibility)
        if self.evidence is not None:
            result["evidence"] = _plain_json_value(self.evidence)
        return result

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> EventEnvelope:
        if not isinstance(data, Mapping):
            raise InterfaceValidationError("event envelope must be an object")
        allowed = {
            "schema_version",
            "envelope_type",
            "message_id",
            "event_id",
            "event_type",
            "event_version",
            "interface",
            "publisher",
            "intended_receivers",
            "correlation",
            "occurred_at",
            "committed_at",
            "expires_at",
            "payload_representation",
            "payload",
            "ordering",
            "replay",
            "compatibility",
            "disclosure",
            "evidence",
            "authority",
        }
        _unexpected_fields(data, allowed)
        required = {
            "schema_version",
            "envelope_type",
            "message_id",
            "event_id",
            "event_type",
            "event_version",
            "interface",
            "publisher",
            "intended_receivers",
            "correlation",
            "occurred_at",
            "committed_at",
            "payload_representation",
            "payload",
            "ordering",
            "replay",
            "disclosure",
            "authority",
        }
        missing = sorted(required - set(data))
        if missing:
            raise InterfaceValidationError(f"missing fields: {', '.join(missing)}")
        if data["envelope_type"] != cls.ENVELOPE_TYPE:
            raise InterfaceValidationError("envelope_type must be domain_event")
        receivers = data["intended_receivers"]
        if not isinstance(receivers, (list, tuple)):
            raise InterfaceValidationError("intended_receivers must be an array")
        return cls(
            schema_version=data["schema_version"],
            message_id=data["message_id"],
            event_id=data["event_id"],
            event_type=data["event_type"],
            event_version=data["event_version"],
            interface=data["interface"],
            publisher=data["publisher"],
            intended_receivers=tuple(receivers),
            correlation=Correlation.from_dict(data["correlation"]),
            occurred_at=data["occurred_at"],
            committed_at=data["committed_at"],
            expires_at=data.get("expires_at"),
            payload_representation=data["payload_representation"],
            payload=data["payload"],
            ordering=data["ordering"],
            replay=data["replay"],
            compatibility=data.get("compatibility"),
            disclosure=data["disclosure"],
            evidence=data.get("evidence"),
            authority=data["authority"],
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
