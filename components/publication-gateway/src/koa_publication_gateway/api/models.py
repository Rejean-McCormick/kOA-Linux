"""Transport-neutral public models for Publication Gateway.

The boundary validates observable request shape and fail-closed invariants. It
never selects source content, grants authority, writes another component's
state, performs destination transport, or treats a send attempt as publication.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field, fields, is_dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, Sequence

COMPONENT_ID = "publication_gateway"
API_VERSION = "1.0.0"
PUBLICATION_REQUEST_SCHEMA = "../artifact-contracts/publication-request.schema.json"
PUBLICATION_RECEIPT_SCHEMA = "publication-receipt.schema.json"

JSONScalar = str | int | float | bool | None
JSONValue = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]

_SECRET_KEYS = frozenset(
    {
        "access_token",
        "api_key",
        "authorization_header",
        "credential",
        "credentials",
        "password",
        "private_key",
        "raw_secret",
        "secret",
        "secret_key",
        "token",
    }
)

PUBLICATION_REQUEST_REQUIRED_FIELDS = frozenset(
    {
        "$schema",
        "schema_version",
        "artifact_class",
        "request_id",
        "status",
        "language",
        "created_at",
        "updated_at",
        "request_context",
        "source",
        "selection",
        "publication_intent",
        "destination",
        "classification",
        "policy_context",
        "transformation_plan",
        "approval_plan",
        "gateway",
        "delivery",
        "receipts",
        "security",
        "offline_behavior",
        "lifecycle",
        "validation",
    }
)

ARTIFACT_REQUEST_STATUSES = frozenset(
    {
        "requested", "validating", "policy_pending", "approval_pending",
        "transformation_pending", "ready", "deferred", "submitted",
        "published", "rejected", "cancelled", "withdrawal_pending",
        "withdrawn", "superseded", "failed", "conflicted", "expired",
        "recovery_required",
    }
)

REVALIDATION_DIMENSIONS = frozenset(
    {
        "source_version",
        "requester_identity",
        "delegation",
        "trust",
        "revocation",
        "consent",
        "cultural_authority",
        "governance_policy",
        "exception",
        "destination",
        "audience",
        "representation",
        "credentials",
        "time_validity",
        "conflict_state",
    }
)


class ModelValidationError(ValueError):
    """Deterministic validation failure safe to expose without submitted data."""

    def __init__(self, field_name: str, code: str, message: str) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.code = code
        self.message = message


class ApiOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    REJECTED = "rejected"
    FAILED = "failed"


class PublicationDecisionOutcome(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"


class PublicationState(str, Enum):
    RECEIVED = "received"
    VALIDATING = "validating"
    AWAITING_AUTHORITY = "awaiting_authority"
    AWAITING_REVIEW = "awaiting_review"
    DENIED = "denied"
    BLOCKED = "blocked"
    APPROVED = "approved"
    STAGING = "staging"
    READY = "ready"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    PARTIALLY_DELIVERED = "partially_delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVOKED = "revoked"
    REMEDIATING = "remediating"
    CLOSED = "closed"


class ExecutionResult(str, Enum):
    PUBLISHED = "published"
    PARTIALLY_DELIVERED = "partially_delivered"
    FAILED = "failed"
    CANCELLED = "cancelled"
    NOT_SUBMITTED = "not_submitted"
    QUEUED = "queued"


class PublicationRecordState(str, Enum):
    NOT_PUBLISHED = "not_published"
    ACTIVE = "active"
    EXPIRED = "expired"
    WITHDRAWAL_PENDING = "withdrawal_pending"
    WITHDRAWN = "withdrawn"
    REMEDIATION_PENDING = "remediation_pending"
    REMEDIATED = "remediated"
    EXTERNAL_LIMITATION = "external_limitation"


class WithdrawalAction(str, Enum):
    CANCEL_PENDING = "cancel_pending"
    STOP_FUTURE_RELEASE = "stop_future_release"
    INITIATE_SUPPORTED_DOWNSTREAM_NOTICE = "initiate_supported_downstream_notice"


class HealthState(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    UNAVAILABLE = "unavailable"


class RetryOutcome(str, Enum):
    ACCEPTED = "accepted"
    EXISTING_STATUS_RETURNED = "existing_status_returned"
    BLOCKED = "blocked"


def _string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ModelValidationError(field_name, "invalid_string", f"{field_name} must be a non-empty string")
    return value


def _boolean(value: object, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ModelValidationError(field_name, "invalid_boolean", f"{field_name} must be a boolean")
    return value


def _mapping(value: object, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ModelValidationError(field_name, "invalid_mapping", f"{field_name} must be an object")
    result: dict[str, Any] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ModelValidationError(field_name, "invalid_mapping_key", f"{field_name} keys must be strings")
        result[key] = item
    return result


def _strings(value: object, field_name: str, *, nonempty: bool = False) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ModelValidationError(field_name, "invalid_sequence", f"{field_name} must be an array of strings")
    result = tuple(_string(item, field_name) for item in value)
    if nonempty and not result:
        raise ModelValidationError(field_name, "empty_sequence", f"{field_name} must not be empty")
    if len(set(result)) != len(result):
        raise ModelValidationError(field_name, "duplicate_value", f"{field_name} must not contain duplicates")
    return result


def _enum(enum_type: type[Enum], value: object, field_name: str) -> Any:
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ModelValidationError(field_name, "unsupported_value", f"{field_name} contains an unsupported value") from exc


def _reject_secrets(value: object, field_name: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in _SECRET_KEYS:
                raise ModelValidationError(field_name, "secret_material_prohibited", "secret material must be passed by reference")
            _reject_secrets(item, field_name)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for item in value:
            _reject_secrets(item, field_name)


def _freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({str(k): _freeze(v) for k, v in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(_freeze(item) for item in value)
    return value


def _json(value: object) -> JSONValue:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {item.name: _json(getattr(value, item.name)) for item in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _json(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported response value: {type(value).__name__}")


def _require_keys(value: Mapping[str, Any], required: frozenset[str], field_name: str) -> None:
    missing = sorted(required.difference(value))
    if missing:
        raise ModelValidationError(field_name, "missing_required_fields", f"{field_name} is missing required fields: {', '.join(missing)}")


def _validate_publication_artifact(artifact: Mapping[str, Any]) -> None:
    _require_keys(artifact, PUBLICATION_REQUEST_REQUIRED_FIELDS, "publication_request")
    if artifact["$schema"] != PUBLICATION_REQUEST_SCHEMA:
        raise ModelValidationError("publication_request.$schema", "schema_mismatch", "publication request schema reference is not supported")
    if artifact["schema_version"] != API_VERSION or artifact["artifact_class"] != "publication_request" or artifact["language"] != "en":
        raise ModelValidationError("publication_request", "contract_identity_mismatch", "publication request contract identity is invalid")
    _string(artifact["request_id"], "publication_request.request_id")
    if artifact["status"] not in ARTIFACT_REQUEST_STATUSES:
        raise ModelValidationError("publication_request.status", "unsupported_value", "publication request status is unsupported")

    context = _mapping(artifact["request_context"], "publication_request.request_context")
    _require_keys(context, frozenset({"idempotency_id", "correlation_id", "requesting_subject_ref", "authority_scope_ref"}), "publication_request.request_context")
    _string(context["idempotency_id"], "publication_request.request_context.idempotency_id")
    _string(context["correlation_id"], "publication_request.request_context.correlation_id")

    source = _mapping(artifact["source"], "publication_request.source")
    _require_keys(source, frozenset({"source_component_ref", "source_object_ref", "source_version_ref", "source_owner_ref", "source_authority_preserved", "direct_source_store_write_allowed"}), "publication_request.source")
    if source["source_authority_preserved"] is not True or source["direct_source_store_write_allowed"] is not False:
        raise ModelValidationError("publication_request.source", "source_authority_violation", "source authority must remain with the source owner")

    selection = _mapping(artifact["selection"], "publication_request.selection")
    if selection.get("minimum_necessary_reviewed") is not True or selection.get("unrelated_source_data_included") is not False:
        raise ModelValidationError("publication_request.selection", "minimum_necessary_violation", "selection must be bounded and minimum necessary")
    selected = selection.get("selected_elements")
    if not isinstance(selected, Sequence) or isinstance(selected, (str, bytes)) or not selected:
        raise ModelValidationError("publication_request.selection.selected_elements", "empty_selection", "at least one explicit element is required")

    destination = _mapping(artifact["destination"], "publication_request.destination")
    _require_keys(destination, frozenset({"destination_id", "destination_ref", "integration_ref", "destination_bound", "direct_authoritative_write_allowed"}), "publication_request.destination")
    if destination["destination_bound"] is not True or destination["direct_authoritative_write_allowed"] is not False:
        raise ModelValidationError("publication_request.destination", "destination_boundary_violation", "destination must be explicit and accessed through its declared interface")

    classification = _mapping(artifact["classification"], "publication_request.classification")
    if classification.get("classification_known") is not True or classification.get("secret_key_material_in_output") is not False:
        raise ModelValidationError("publication_request.classification", "classification_blocked", "classification must be known and secret material excluded")

    policy = _mapping(artifact["policy_context"], "publication_request.policy_context")
    if policy.get("resource_state_used_as_authority") is not False:
        raise ModelValidationError("publication_request.policy_context", "authority_violation", "resource state cannot authorize publication")

    _reject_secrets(artifact, "publication_request")


@dataclass(frozen=True, slots=True)
class ApiRequest:
    interface_id: str
    request_id: str
    correlation_id: str
    payload: Mapping[str, Any]
    version: str = API_VERSION

    def __post_init__(self) -> None:
        object.__setattr__(self, "interface_id", _string(self.interface_id, "interface_id"))
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "correlation_id", _string(self.correlation_id, "correlation_id"))
        if self.version != API_VERSION:
            raise ModelValidationError("version", "unsupported_version", "the requested interface version is unsupported")
        payload = _mapping(self.payload, "payload")
        _reject_secrets(payload)
        object.__setattr__(self, "payload", _freeze(payload))

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ApiRequest":
        mapping = _mapping(value, "request")
        return cls(
            mapping.get("interface_id"),
            mapping.get("request_id"),
            mapping.get("correlation_id"),
            mapping.get("payload", {}),
            mapping.get("version", API_VERSION),
        )


@dataclass(frozen=True, slots=True)
class ApiError:
    code: str
    message: str
    field: str | None = None
    details: Mapping[str, str] = dataclass_field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "code", _string(self.code, "error.code"))
        object.__setattr__(self, "message", _string(self.message, "error.message"))
        if self.field is not None:
            object.__setattr__(self, "field", _string(self.field, "error.field"))
        details = _mapping(self.details, "error.details")
        if any(not isinstance(value, str) for value in details.values()):
            raise ModelValidationError("error.details", "invalid_details", "error details must contain strings")
        object.__setattr__(self, "details", MappingProxyType(dict(details)))


@dataclass(frozen=True, slots=True)
class ApiResponse:
    interface_id: str
    request_id: str
    correlation_id: str
    status: ApiOutcome
    result: Mapping[str, JSONValue] | None = None
    error: ApiError | None = None
    version: str = API_VERSION

    def __post_init__(self) -> None:
        if self.status is ApiOutcome.SUCCEEDED and (self.result is None or self.error is not None):
            raise ModelValidationError("response", "invalid_success", "successful responses require only a result")
        if self.status is not ApiOutcome.SUCCEEDED and (self.error is None or self.result is not None):
            raise ModelValidationError("response", "invalid_failure", "non-success responses require only an error")

    @classmethod
    def success(cls, request: ApiRequest, result: object) -> "ApiResponse":
        serialized = _json(result)
        if not isinstance(serialized, dict):
            raise ModelValidationError("service_result", "invalid_service_result", "service result must be a registered public model")
        return cls(request.interface_id, request.request_id, request.correlation_id, ApiOutcome.SUCCEEDED, serialized)

    @classmethod
    def rejected(cls, request: ApiRequest, error: ApiError) -> "ApiResponse":
        return cls(request.interface_id, request.request_id, request.correlation_id, ApiOutcome.REJECTED, error=error)

    @classmethod
    def failed(cls, request: ApiRequest, error: ApiError) -> "ApiResponse":
        return cls(request.interface_id, request.request_id, request.correlation_id, ApiOutcome.FAILED, error=error)

    def to_mapping(self) -> dict[str, JSONValue]:
        value: dict[str, JSONValue] = {
            "interface_id": self.interface_id,
            "request_id": self.request_id,
            "correlation_id": self.correlation_id,
            "version": self.version,
            "status": self.status.value,
        }
        if self.result is not None:
            value["result"] = dict(self.result)
        if self.error is not None:
            value["error"] = _json(self.error)
        return value


@dataclass(frozen=True, slots=True)
class PublicationRequestCommand:
    publication_request: Mapping[str, Any]
    execute_when_approved: bool = True

    def __post_init__(self) -> None:
        artifact = _mapping(self.publication_request, "publication_request")
        _validate_publication_artifact(artifact)
        object.__setattr__(self, "publication_request", _freeze(artifact))
        object.__setattr__(self, "execute_when_approved", _boolean(self.execute_when_approved, "execute_when_approved"))

    @property
    def artifact_request_id(self) -> str:
        return str(self.publication_request["request_id"])

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], _: ApiRequest) -> "PublicationRequestCommand":
        return cls(payload.get("publication_request"), payload.get("execute_when_approved", True))


@dataclass(frozen=True, slots=True)
class RevocationOrWithdrawalNotice:
    publication_request_id: str
    action: WithdrawalAction
    authority_ref: str
    affected_scope_ref: str
    reason_code: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "publication_request_id", _string(self.publication_request_id, "publication_request_id"))
        object.__setattr__(self, "action", _enum(WithdrawalAction, self.action, "action"))
        object.__setattr__(self, "authority_ref", _string(self.authority_ref, "authority_ref"))
        object.__setattr__(self, "affected_scope_ref", _string(self.affected_scope_ref, "affected_scope_ref"))
        object.__setattr__(self, "reason_code", _string(self.reason_code, "reason_code"))

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], _: ApiRequest) -> "RevocationOrWithdrawalNotice":
        return cls(payload.get("publication_request_id"), payload.get("action"), payload.get("authority_ref"), payload.get("affected_scope_ref"), payload.get("reason_code"))


@dataclass(frozen=True, slots=True)
class PublicationStatusQuery:
    publication_request_id: str
    authorized_scope_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "publication_request_id", _string(self.publication_request_id, "publication_request_id"))
        object.__setattr__(self, "authorized_scope_ref", _string(self.authorized_scope_ref, "authorized_scope_ref"))

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], _: ApiRequest) -> "PublicationStatusQuery":
        return cls(payload.get("publication_request_id"), payload.get("authorized_scope_ref"))


@dataclass(frozen=True, slots=True)
class HealthQuery:
    authorized_scope_ref: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "authorized_scope_ref", _string(self.authorized_scope_ref, "authorized_scope_ref"))

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], _: ApiRequest) -> "HealthQuery":
        return cls(payload.get("authorized_scope_ref"))


@dataclass(frozen=True, slots=True)
class QueueInspectionQuery:
    authorized_scope_ref: str
    limit: int = 50

    def __post_init__(self) -> None:
        object.__setattr__(self, "authorized_scope_ref", _string(self.authorized_scope_ref, "authorized_scope_ref"))
        if not isinstance(self.limit, int) or isinstance(self.limit, bool) or not 1 <= self.limit <= 100:
            raise ModelValidationError("limit", "invalid_limit", "limit must be between 1 and 100")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], _: ApiRequest) -> "QueueInspectionQuery":
        return cls(payload.get("authorized_scope_ref"), payload.get("limit", 50))


@dataclass(frozen=True, slots=True)
class ControlledRetryRequest:
    publication_request_id: str
    prior_attempt_ref: str
    authority_ref: str
    idempotency_key: str
    revalidation_dimensions: tuple[str, ...]
    duplicate_effect_prevention_ref: str
    scope_unchanged: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "publication_request_id", _string(self.publication_request_id, "publication_request_id"))
        object.__setattr__(self, "prior_attempt_ref", _string(self.prior_attempt_ref, "prior_attempt_ref"))
        object.__setattr__(self, "authority_ref", _string(self.authority_ref, "authority_ref"))
        object.__setattr__(self, "idempotency_key", _string(self.idempotency_key, "idempotency_key"))
        dimensions = _strings(self.revalidation_dimensions, "revalidation_dimensions", nonempty=True)
        if frozenset(dimensions) != REVALIDATION_DIMENSIONS:
            raise ModelValidationError("revalidation_dimensions", "incomplete_revalidation", "controlled retry must revalidate every mutable authority and compatibility dimension")
        object.__setattr__(self, "revalidation_dimensions", dimensions)
        object.__setattr__(self, "duplicate_effect_prevention_ref", _string(self.duplicate_effect_prevention_ref, "duplicate_effect_prevention_ref"))
        if _boolean(self.scope_unchanged, "scope_unchanged") is not True:
            raise ModelValidationError("scope_unchanged", "scope_broadened", "a retry must not broaden publication scope")

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], _: ApiRequest) -> "ControlledRetryRequest":
        return cls(
            payload.get("publication_request_id"),
            payload.get("prior_attempt_ref"),
            payload.get("authority_ref"),
            payload.get("idempotency_key"),
            payload.get("revalidation_dimensions", ()),
            payload.get("duplicate_effect_prevention_ref"),
            payload.get("scope_unchanged"),
        )


@dataclass(frozen=True, slots=True)
class PublicationDecision:
    decision_id: str
    outcome: PublicationDecisionOutcome
    request_id: str
    authority_refs: tuple[str, ...]
    obligation_refs: tuple[str, ...]
    executable: bool
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision_id", _string(self.decision_id, "decision_id"))
        object.__setattr__(self, "outcome", _enum(PublicationDecisionOutcome, self.outcome, "outcome"))
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "authority_refs", _strings(self.authority_refs, "authority_refs", nonempty=True))
        obligations = _strings(self.obligation_refs, "obligation_refs", nonempty=self.outcome is PublicationDecisionOutcome.ALLOW)
        object.__setattr__(self, "obligation_refs", obligations)
        object.__setattr__(self, "reason_codes", _strings(self.reason_codes, "reason_codes"))
        executable = _boolean(self.executable, "executable")
        if executable and self.outcome is not PublicationDecisionOutcome.ALLOW:
            raise ModelValidationError("executable", "non_allow_execution", "only an allow decision can be executable")
        if self.outcome is PublicationDecisionOutcome.REVIEW_REQUIRED and executable:
            raise ModelValidationError("executable", "review_prevents_execution", "review-required decisions cannot execute")


@dataclass(frozen=True, slots=True)
class PublicationReceipt:
    receipt_id: str
    request_id: str
    source_version_ref: str
    destination_ref: str
    audience_ref: str
    decision_ref: str
    execution_result: ExecutionResult
    publication_state: PublicationRecordState
    correlation_id: str
    evidence_refs: tuple[str, ...]
    destination_acknowledgement_ref: str | None = None
    remediation_ref: str | None = None
    record_status: str = "issued"
    artifact_class: str = "publication_receipt"
    immutable: bool = True

    def __post_init__(self) -> None:
        for name in ("receipt_id", "request_id", "source_version_ref", "destination_ref", "audience_ref", "decision_ref", "correlation_id"):
            object.__setattr__(self, name, _string(getattr(self, name), name))
        object.__setattr__(self, "execution_result", _enum(ExecutionResult, self.execution_result, "execution_result"))
        object.__setattr__(self, "publication_state", _enum(PublicationRecordState, self.publication_state, "publication_state"))
        object.__setattr__(self, "evidence_refs", _strings(self.evidence_refs, "evidence_refs", nonempty=True))
        if self.artifact_class != "publication_receipt" or self.record_status not in {"issued", "superseded"} or self.immutable is not True:
            raise ModelValidationError("receipt", "invalid_receipt_identity", "publication receipt identity or immutability is invalid")
        if self.execution_result is ExecutionResult.PUBLISHED:
            if not self.destination_acknowledgement_ref or self.publication_state is not PublicationRecordState.ACTIVE:
                raise ModelValidationError("receipt", "unacknowledged_publication", "published result requires destination acknowledgement and active state")
        if self.execution_result is ExecutionResult.PARTIALLY_DELIVERED:
            if not self.remediation_ref or self.publication_state not in {PublicationRecordState.REMEDIATION_PENDING, PublicationRecordState.EXTERNAL_LIMITATION}:
                raise ModelValidationError("receipt", "partial_delivery_unclosed", "partial delivery requires explicit remediation state")
        if self.execution_result is ExecutionResult.FAILED and self.publication_state is not PublicationRecordState.NOT_PUBLISHED:
            raise ModelValidationError("receipt", "failed_publication_state", "failed delivery cannot claim a published state")


@dataclass(frozen=True, slots=True)
class PublicationRequestResult:
    request_id: str
    state: PublicationState
    decision: PublicationDecision
    receipt: PublicationReceipt | None
    duplicate_request: bool = False
    queued: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "state", _enum(PublicationState, self.state, "state"))
        if self.decision.request_id != self.request_id:
            raise ModelValidationError("decision.request_id", "correlation_mismatch", "decision does not belong to the request")
        if self.state is PublicationState.PUBLISHED:
            if self.decision.outcome is not PublicationDecisionOutcome.ALLOW or self.receipt is None or self.receipt.execution_result is not ExecutionResult.PUBLISHED:
                raise ModelValidationError("state", "false_publication_success", "published state requires allow decision and acknowledged receipt")
        if self.state is PublicationState.PARTIALLY_DELIVERED:
            if self.receipt is None or self.receipt.execution_result is not ExecutionResult.PARTIALLY_DELIVERED:
                raise ModelValidationError("state", "hidden_partial_delivery", "partial delivery must be explicit in the receipt")
        if self.decision.outcome is not PublicationDecisionOutcome.ALLOW and self.state in {PublicationState.STAGING, PublicationState.READY, PublicationState.PUBLISHING, PublicationState.PUBLISHED}:
            raise ModelValidationError("state", "non_allow_progression", "non-allow decisions cannot progress to execution")


@dataclass(frozen=True, slots=True)
class WithdrawalResult:
    request_id: str
    action: WithdrawalAction
    state: PublicationState
    historical_receipt_preserved: bool
    downstream_limitation: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "action", _enum(WithdrawalAction, self.action, "action"))
        object.__setattr__(self, "state", _enum(PublicationState, self.state, "state"))
        if _boolean(self.historical_receipt_preserved, "historical_receipt_preserved") is not True:
            raise ModelValidationError("historical_receipt_preserved", "history_rewrite_prohibited", "withdrawal must preserve historical receipt evidence")
        if self.downstream_limitation is not None:
            object.__setattr__(self, "downstream_limitation", _string(self.downstream_limitation, "downstream_limitation"))


@dataclass(frozen=True, slots=True)
class PublicationStatus:
    request_id: str
    state: PublicationState
    decision_outcome: PublicationDecisionOutcome
    receipt_ref: str | None
    remediation_required: bool
    restricted_metadata_only: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "state", _enum(PublicationState, self.state, "state"))
        object.__setattr__(self, "decision_outcome", _enum(PublicationDecisionOutcome, self.decision_outcome, "decision_outcome"))
        if self.receipt_ref is not None:
            object.__setattr__(self, "receipt_ref", _string(self.receipt_ref, "receipt_ref"))
        if self.restricted_metadata_only is not True:
            raise ModelValidationError("restricted_metadata_only", "source_content_disclosure", "status responses must contain restricted metadata only")


@dataclass(frozen=True, slots=True)
class HealthResult:
    state: HealthState
    process_alive: bool
    accepting_requests: bool
    required_authorities_available: bool
    queue_depth: int
    source_content_included: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", _enum(HealthState, self.state, "state"))
        for name in ("process_alive", "accepting_requests", "required_authorities_available"):
            object.__setattr__(self, name, _boolean(getattr(self, name), name))
        if not isinstance(self.queue_depth, int) or isinstance(self.queue_depth, bool) or self.queue_depth < 0:
            raise ModelValidationError("queue_depth", "invalid_queue_depth", "queue depth must be a non-negative integer")
        if self.source_content_included is not False:
            raise ModelValidationError("source_content_included", "health_content_leak", "health must not contain source content")
        if self.state is HealthState.HEALTHY and (not self.process_alive or not self.accepting_requests or not self.required_authorities_available):
            raise ModelValidationError("state", "false_healthy_state", "healthy state requires live, ready, authoritative operation")


@dataclass(frozen=True, slots=True)
class QueueEntry:
    request_id: str
    state: PublicationState
    destination_ref: str
    expires_at: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "state", _enum(PublicationState, self.state, "state"))
        object.__setattr__(self, "destination_ref", _string(self.destination_ref, "destination_ref"))
        object.__setattr__(self, "expires_at", _string(self.expires_at, "expires_at"))


@dataclass(frozen=True, slots=True)
class QueueInspectionResult:
    entries: tuple[QueueEntry, ...]
    restricted_metadata_only: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.entries, Sequence) or isinstance(self.entries, (str, bytes)):
            raise ModelValidationError("entries", "invalid_entries", "entries must be an array")
        entries = tuple(self.entries)
        if any(not isinstance(item, QueueEntry) for item in entries):
            raise ModelValidationError("entries", "invalid_entry", "queue entries must use the public queue model")
        object.__setattr__(self, "entries", entries)
        if self.restricted_metadata_only is not True:
            raise ModelValidationError("restricted_metadata_only", "queue_content_leak", "queue inspection must contain restricted metadata only")


@dataclass(frozen=True, slots=True)
class ControlledRetryResult:
    request_id: str
    outcome: RetryOutcome
    state: PublicationState
    revalidation_complete: bool
    duplicate_effect_prevented: bool
    receipt_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _string(self.request_id, "request_id"))
        object.__setattr__(self, "outcome", _enum(RetryOutcome, self.outcome, "outcome"))
        object.__setattr__(self, "state", _enum(PublicationState, self.state, "state"))
        if _boolean(self.revalidation_complete, "revalidation_complete") is not True:
            raise ModelValidationError("revalidation_complete", "retry_without_revalidation", "retry cannot proceed without complete revalidation")
        if _boolean(self.duplicate_effect_prevented, "duplicate_effect_prevented") is not True:
            raise ModelValidationError("duplicate_effect_prevented", "duplicate_publication_risk", "retry must prevent duplicate destination effects")
        if self.receipt_ref is not None:
            object.__setattr__(self, "receipt_ref", _string(self.receipt_ref, "receipt_ref"))
