"""Public, transport-neutral models for the Audit Broker component API.

The models in this module intentionally contain no persistence, policy, identity,
or transport implementation. They validate the closed public interface declared
by ``audit-broker.component.json`` and preserve the receiving component's right
to accept or reject every operation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, Sequence, TypeVar

COMPONENT_ID = "audit_broker"
API_VERSION = "1.0.0"

JSONScalar = str | int | float | bool | None
JSONValue = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]


class ModelValidationError(ValueError):
    """A deterministic validation failure safe to expose without payload data."""

    def __init__(self, field_name: str, code: str, message: str) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.code = code
        self.message = message

    def as_error(self) -> dict[str, str]:
        return {
            "code": self.code,
            "field": self.field_name,
            "message": self.message,
        }


class AuditEventClass(str, Enum):
    POLICY_DECISION_EVENT = "policy_decision_event"
    PRIVILEGED_OPERATION_EVENT = "privileged_operation_event"
    ARTIFACT_ACTIVATION_EVENT = "artifact_activation_event"
    PUBLICATION_EVENT = "publication_event"
    INTEGRATION_IMPORT_EVENT = "integration_import_event"
    TEST_OR_EVIDENCE_EVENT = "test_or_evidence_event"
    SECURITY_OR_INCIDENT_EVENT = "security_or_incident_event"
    AUDIT_ACCESS_OR_DISCLOSURE_EVENT = "audit_access_or_disclosure_event"


class AuditEvidenceClass(str, Enum):
    PUBLIC_TRANSPARENCY_RECEIPTS = "public_transparency_receipts"
    TENANT_OPERATIONAL_AUDIT = "tenant_operational_audit"
    RESTRICTED_EVIDENCE_AUDIT = "restricted_evidence_audit"
    PERSONAL_PRIVACY_RECORDS = "personal_privacy_records"
    SECURITY_AND_NODE_AUDIT = "security_and_node_audit"


class SubmissionOutcome(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    QUARANTINED = "quarantined"


class DisclosureOutcome(str, Enum):
    ALLOWED = "allowed"
    PARTIALLY_ALLOWED = "partially_allowed"
    DENIED = "denied"
    EXPIRED = "expired"
    FAILED = "failed"


class RetentionOutcome(str, Enum):
    APPLIED = "applied"
    PARTIALLY_APPLIED = "partially_applied"
    DENIED = "denied"
    FAILED = "failed"


class InvalidationOutcome(str, Enum):
    INVALIDATED = "invalidated"
    DENIED = "denied"
    NOT_FOUND = "not_found"
    FAILED = "failed"


class ApiOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    REJECTED = "rejected"
    FAILED = "failed"


REGISTERED_EVENT_MINIMUM_FIELDS: Mapping[AuditEventClass, frozenset[str]] = MappingProxyType(
    {
        AuditEventClass.POLICY_DECISION_EVENT: frozenset(
            {
                "decision_ref",
                "decision_outcome",
                "scope",
                "purpose",
                "actor_or_subject_refs",
                "occurred_at",
            }
        ),
        AuditEventClass.PRIVILEGED_OPERATION_EVENT: frozenset(
            {
                "operation_class",
                "authorization_ref",
                "target_ref",
                "outcome",
                "receipt_ref",
                "occurred_at",
            }
        ),
        AuditEventClass.ARTIFACT_ACTIVATION_EVENT: frozenset(
            {
                "artifact_class_id",
                "artifact_id",
                "previous_artifact_id",
                "release_set_ref",
                "outcome",
                "receipt_ref",
                "occurred_at",
            }
        ),
        AuditEventClass.PUBLICATION_EVENT: frozenset(
            {
                "publication_request_ref",
                "source_domain_ref",
                "destination_scope",
                "policy_decision_ref",
                "outcome",
                "publication_receipt_ref",
                "occurred_at",
            }
        ),
        AuditEventClass.INTEGRATION_IMPORT_EVENT: frozenset(
            {
                "integration_id",
                "owning_component_id",
                "candidate_artifact_ref",
                "acceptance_outcome",
                "provenance_ref",
                "occurred_at",
            }
        ),
        AuditEventClass.TEST_OR_EVIDENCE_EVENT: frozenset(
            {
                "test_id",
                "evidence_id",
                "subject_ref",
                "outcome",
                "validity_state",
                "occurred_at",
            }
        ),
        AuditEventClass.SECURITY_OR_INCIDENT_EVENT: frozenset(
            {
                "event_type",
                "source_component_id",
                "severity",
                "subject_refs",
                "outcome_or_state",
                "occurred_at",
            }
        ),
        AuditEventClass.AUDIT_ACCESS_OR_DISCLOSURE_EVENT: frozenset(
            {
                "request_id",
                "requester_identity",
                "purpose",
                "policy_decision_ref",
                "effective_scope",
                "outcome",
                "receipt_ref",
                "occurred_at",
            }
        ),
    }
)

PROHIBITED_SECRET_FIELD_NAMES = frozenset(
    {
        "access_token",
        "api_key",
        "credential",
        "credentials",
        "password",
        "private_key",
        "secret",
        "secret_key",
        "token",
    }
)


T = TypeVar("T")


def _enum(enum_type: type[T], value: object, field_name: str) -> T:
    try:
        return enum_type(value)  # type: ignore[call-arg]
    except (TypeError, ValueError) as exc:
        allowed = ", ".join(str(member.value) for member in enum_type)  # type: ignore[attr-defined]
        raise ModelValidationError(
            field_name,
            "unsupported_value",
            f"{field_name} must be one of: {allowed}",
        ) from exc


def _non_empty_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ModelValidationError(
            field_name,
            "required_non_empty_string",
            f"{field_name} must be a non-empty string",
        )
    return value.strip()


def _mapping(value: object, field_name: str) -> dict[str, JSONValue]:
    if not isinstance(value, Mapping):
        raise ModelValidationError(
            field_name,
            "required_object",
            f"{field_name} must be an object",
        )
    converted: dict[str, JSONValue] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not key:
            raise ModelValidationError(
                field_name,
                "invalid_object_key",
                f"{field_name} keys must be non-empty strings",
            )
        converted[key] = _json_value(item, f"{field_name}.{key}")
    return converted


def _json_value(value: object, field_name: str) -> JSONValue:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return _mapping(value, field_name)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_json_value(item, field_name) for item in value]
    raise ModelValidationError(
        field_name,
        "not_json_serializable",
        f"{field_name} must contain JSON-compatible values",
    )


def _string_tuple(value: object, field_name: str, *, allow_empty: bool = False) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ModelValidationError(
            field_name,
            "required_string_array",
            f"{field_name} must be an array of strings",
        )
    result = tuple(_non_empty_text(item, field_name) for item in value)
    if not allow_empty and not result:
        raise ModelValidationError(
            field_name,
            "empty_array",
            f"{field_name} must contain at least one item",
        )
    if len(set(result)) != len(result):
        raise ModelValidationError(
            field_name,
            "duplicate_items",
            f"{field_name} must not contain duplicate items",
        )
    return result


def _timestamp(value: object, field_name: str) -> str:
    text = _non_empty_text(value, field_name)
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ModelValidationError(
            field_name,
            "invalid_timestamp",
            f"{field_name} must be an RFC 3339 timestamp",
        ) from exc
    if parsed.tzinfo is None:
        raise ModelValidationError(
            field_name,
            "timezone_required",
            f"{field_name} must include a timezone",
        )
    return text


def _closed_payload(
    payload: object,
    required: frozenset[str],
    optional: frozenset[str] = frozenset(),
) -> dict[str, object]:
    if not isinstance(payload, Mapping):
        raise ModelValidationError("payload", "required_object", "payload must be an object")
    keys = set(payload)
    missing = sorted(required - keys)
    if missing:
        raise ModelValidationError(
            missing[0],
            "missing_field",
            "missing required field(s): " + ", ".join(missing),
        )
    unexpected = sorted(keys - required - optional)
    if unexpected:
        raise ModelValidationError(
            unexpected[0],
            "unexpected_field",
            "unexpected field(s): " + ", ".join(unexpected),
        )
    return dict(payload)


def _reject_secret_fields(value: JSONValue, field_name: str = "event_payload") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in PROHIBITED_SECRET_FIELD_NAMES:
                raise ModelValidationError(
                    field_name,
                    "secret_field_prohibited",
                    "audit payloads must not contain credential or secret fields",
                )
            _reject_secret_fields(item, field_name)
    elif isinstance(value, list):
        for item in value:
            _reject_secret_fields(item, field_name)


def _public_value(value: Any) -> JSONValue:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {key: _public_value(item) for key, item in asdict(value).items()}
    if isinstance(value, Mapping):
        return {str(key): _public_value(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_public_value(item) for item in value]
    if isinstance(value, list):
        return [_public_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"unsupported public value type: {type(value).__name__}")


@dataclass(frozen=True, slots=True)
class PublicModel:
    """Base class with deterministic JSON-compatible serialization."""

    def to_dict(self) -> dict[str, JSONValue]:
        return {
            model_field.name: _public_value(getattr(self, model_field.name))
            for model_field in fields(self)
        }


@dataclass(frozen=True, slots=True)
class AuditEventSubmission(PublicModel):
    event_class_id: AuditEventClass
    producer_identity: dict[str, JSONValue]
    event_payload: dict[str, JSONValue]
    classification: str
    purpose: str
    retention_class: str
    correlation_id: str
    idempotency_key: str

    REQUIRED: ClassVar[frozenset[str]] = frozenset(
        {
            "event_class_id",
            "producer_identity",
            "event_payload",
            "classification",
            "purpose",
            "retention_class",
            "correlation_id",
            "idempotency_key",
        }
    )

    @classmethod
    def from_mapping(cls, payload: object) -> "AuditEventSubmission":
        data = _closed_payload(payload, cls.REQUIRED)
        event_class_id = _enum(AuditEventClass, data["event_class_id"], "event_class_id")
        event_payload = _mapping(data["event_payload"], "event_payload")
        minimum = REGISTERED_EVENT_MINIMUM_FIELDS[event_class_id]
        missing = sorted(minimum - set(event_payload))
        if missing:
            raise ModelValidationError(
                f"event_payload.{missing[0]}",
                "missing_event_field",
                "event_payload is missing declared minimum field(s): " + ", ".join(missing),
            )
        _reject_secret_fields(event_payload)
        return cls(
            event_class_id=event_class_id,
            producer_identity=_mapping(data["producer_identity"], "producer_identity"),
            event_payload=event_payload,
            classification=_non_empty_text(data["classification"], "classification"),
            purpose=_non_empty_text(data["purpose"], "purpose"),
            retention_class=_non_empty_text(data["retention_class"], "retention_class"),
            correlation_id=_non_empty_text(data["correlation_id"], "correlation_id"),
            idempotency_key=_non_empty_text(data["idempotency_key"], "idempotency_key"),
        )


@dataclass(frozen=True, slots=True)
class AuditDisclosureRequest(PublicModel):
    request_id: str
    requester_identity: dict[str, JSONValue]
    purpose: str
    requested_scope: dict[str, JSONValue]
    subject_or_record_selectors: tuple[str, ...]
    desired_output_class: AuditEvidenceClass
    expiry: str
    policy_decision_ref: str

    REQUIRED: ClassVar[frozenset[str]] = frozenset(
        {
            "request_id",
            "requester_identity",
            "purpose",
            "requested_scope",
            "subject_or_record_selectors",
            "desired_output_class",
            "expiry",
            "policy_decision_ref",
        }
    )

    @classmethod
    def from_mapping(cls, payload: object) -> "AuditDisclosureRequest":
        data = _closed_payload(payload, cls.REQUIRED)
        return cls(
            request_id=_non_empty_text(data["request_id"], "request_id"),
            requester_identity=_mapping(data["requester_identity"], "requester_identity"),
            purpose=_non_empty_text(data["purpose"], "purpose"),
            requested_scope=_mapping(data["requested_scope"], "requested_scope"),
            subject_or_record_selectors=_string_tuple(
                data["subject_or_record_selectors"],
                "subject_or_record_selectors",
            ),
            desired_output_class=_enum(
                AuditEvidenceClass,
                data["desired_output_class"],
                "desired_output_class",
            ),
            expiry=_timestamp(data["expiry"], "expiry"),
            policy_decision_ref=_non_empty_text(
                data["policy_decision_ref"],
                "policy_decision_ref",
            ),
        )


@dataclass(frozen=True, slots=True)
class RetentionActionRequest(PublicModel):
    record_selectors: tuple[str, ...]
    action: str
    policy_or_hold_ref: str
    effective_at: str

    REQUIRED: ClassVar[frozenset[str]] = frozenset(
        {"record_selectors", "action", "policy_or_hold_ref", "effective_at"}
    )

    @classmethod
    def from_mapping(cls, payload: object) -> "RetentionActionRequest":
        data = _closed_payload(payload, cls.REQUIRED)
        return cls(
            record_selectors=_string_tuple(data["record_selectors"], "record_selectors"),
            action=_non_empty_text(data["action"], "action"),
            policy_or_hold_ref=_non_empty_text(
                data["policy_or_hold_ref"],
                "policy_or_hold_ref",
            ),
            effective_at=_timestamp(data["effective_at"], "effective_at"),
        )


@dataclass(frozen=True, slots=True)
class InvalidateAuditRecordRequest(PublicModel):
    record_ref: str
    source_correction_or_retraction_ref: str
    reason: str
    effective_at: str

    REQUIRED: ClassVar[frozenset[str]] = frozenset(
        {
            "record_ref",
            "source_correction_or_retraction_ref",
            "reason",
            "effective_at",
        }
    )

    @classmethod
    def from_mapping(cls, payload: object) -> "InvalidateAuditRecordRequest":
        data = _closed_payload(payload, cls.REQUIRED)
        return cls(
            record_ref=_non_empty_text(data["record_ref"], "record_ref"),
            source_correction_or_retraction_ref=_non_empty_text(
                data["source_correction_or_retraction_ref"],
                "source_correction_or_retraction_ref",
            ),
            reason=_non_empty_text(data["reason"], "reason"),
            effective_at=_timestamp(data["effective_at"], "effective_at"),
        )


@dataclass(frozen=True, slots=True)
class AuditRecordMetadataQuery(PublicModel):
    record_ref: str
    requester_identity: dict[str, JSONValue]
    purpose: str

    REQUIRED: ClassVar[frozenset[str]] = frozenset(
        {"record_ref", "requester_identity", "purpose"}
    )

    @classmethod
    def from_mapping(cls, payload: object) -> "AuditRecordMetadataQuery":
        data = _closed_payload(payload, cls.REQUIRED)
        return cls(
            record_ref=_non_empty_text(data["record_ref"], "record_ref"),
            requester_identity=_mapping(data["requester_identity"], "requester_identity"),
            purpose=_non_empty_text(data["purpose"], "purpose"),
        )


@dataclass(frozen=True, slots=True)
class AuditRequestStatusQuery(PublicModel):
    request_id: str
    requester_identity: dict[str, JSONValue]

    REQUIRED: ClassVar[frozenset[str]] = frozenset({"request_id", "requester_identity"})

    @classmethod
    def from_mapping(cls, payload: object) -> "AuditRequestStatusQuery":
        data = _closed_payload(payload, cls.REQUIRED)
        return cls(
            request_id=_non_empty_text(data["request_id"], "request_id"),
            requester_identity=_mapping(data["requester_identity"], "requester_identity"),
        )


@dataclass(frozen=True, slots=True)
class AuditHealthQuery(PublicModel):
    requester_identity: dict[str, JSONValue]

    REQUIRED: ClassVar[frozenset[str]] = frozenset({"requester_identity"})

    @classmethod
    def from_mapping(cls, payload: object) -> "AuditHealthQuery":
        data = _closed_payload(payload, cls.REQUIRED)
        return cls(requester_identity=_mapping(data["requester_identity"], "requester_identity"))


@dataclass(frozen=True, slots=True)
class AuditReceipt(PublicModel):
    receipt_id: str
    request_id: str
    outcome: str
    occurred_at: str
    reason_codes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _non_empty_text(self.receipt_id, "receipt_id")
        _non_empty_text(self.request_id, "request_id")
        _non_empty_text(self.outcome, "outcome")
        _timestamp(self.occurred_at, "occurred_at")
        _string_tuple(self.reason_codes, "reason_codes", allow_empty=True)


@dataclass(frozen=True, slots=True)
class SubmissionResult(PublicModel):
    outcome: SubmissionOutcome
    receipt: AuditReceipt
    audit_record_id: str | None = None
    record_state: str | None = None

    def __post_init__(self) -> None:
        if self.outcome is SubmissionOutcome.ACCEPTED and not self.audit_record_id:
            raise ModelValidationError(
                "audit_record_id",
                "accepted_record_id_required",
                "accepted submissions require audit_record_id",
            )
        if self.outcome is not SubmissionOutcome.ACCEPTED and self.audit_record_id is not None:
            raise ModelValidationError(
                "audit_record_id",
                "rejected_record_id_prohibited",
                "non-accepted submissions must not expose an authoritative record id",
            )


@dataclass(frozen=True, slots=True)
class DisclosureResult(PublicModel):
    outcome: DisclosureOutcome
    receipt: AuditReceipt
    effective_scope: dict[str, JSONValue]
    disclosure_package: dict[str, JSONValue] | None = None

    def __post_init__(self) -> None:
        if self.outcome in {DisclosureOutcome.ALLOWED, DisclosureOutcome.PARTIALLY_ALLOWED}:
            if self.disclosure_package is None:
                raise ModelValidationError(
                    "disclosure_package",
                    "package_required",
                    "allowed disclosure results require a bounded package",
                )
        elif self.disclosure_package is not None:
            raise ModelValidationError(
                "disclosure_package",
                "package_prohibited",
                "denied, expired, or failed disclosures must not include a package",
            )


@dataclass(frozen=True, slots=True)
class RetentionResult(PublicModel):
    outcome: RetentionOutcome
    receipt: AuditReceipt
    affected_record_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class InvalidationResult(PublicModel):
    outcome: InvalidationOutcome
    receipt: AuditReceipt
    invalidation_record_ref: str | None = None

    def __post_init__(self) -> None:
        if self.outcome is InvalidationOutcome.INVALIDATED and not self.invalidation_record_ref:
            raise ModelValidationError(
                "invalidation_record_ref",
                "lineage_ref_required",
                "invalidated results require an append-only lineage reference",
            )
        if self.outcome is not InvalidationOutcome.INVALIDATED and self.invalidation_record_ref:
            raise ModelValidationError(
                "invalidation_record_ref",
                "lineage_ref_prohibited",
                "non-invalidated results must not claim an invalidation record",
            )


@dataclass(frozen=True, slots=True)
class AuditRecordMetadata(PublicModel):
    record_ref: str
    event_class_id: AuditEventClass
    producer_component_id: str
    occurred_at: str
    classification: str
    retention_class: str
    state: str
    correlation_id: str
    source_receipt_or_evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AuditRequestStatus(PublicModel):
    request_id: str
    state: str
    terminal: bool
    outcome: str | None
    receipt_ref: str | None
    updated_at: str


@dataclass(frozen=True, slots=True)
class AuditHealth(PublicModel):
    component_state: str
    ready: bool
    ingestion_queue_depth: int
    query_queue_depth: int
    disclosure_queue_depth: int
    storage_capacity_state: str
    retention_job_state: str
    policy_path_state: str
    identity_path_state: str
    integrity_alarm_state: str
    last_successful_backup_or_recovery_point: str | None

    PROTECTED_FIELD_NAMES: ClassVar[frozenset[str]] = frozenset(
        {
            "audit_record",
            "audit_records",
            "event_payload",
            "private_proof",
            "protected_content",
            "subject_references",
        }
    )

    def __post_init__(self) -> None:
        for name in (
            "ingestion_queue_depth",
            "query_queue_depth",
            "disclosure_queue_depth",
        ):
            if getattr(self, name) < 0:
                raise ModelValidationError(
                    name,
                    "negative_queue_depth",
                    f"{name} cannot be negative",
                )


@dataclass(frozen=True, slots=True)
class ApiError(PublicModel):
    code: str
    message: str
    retryable: bool = False
    details: dict[str, JSONValue] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ApiRequest(PublicModel):
    interface_id: str
    version: str
    request_id: str
    correlation_id: str
    payload: dict[str, JSONValue]

    @classmethod
    def from_mapping(cls, value: object) -> "ApiRequest":
        data = _closed_payload(
            value,
            frozenset({"interface_id", "version", "request_id", "correlation_id", "payload"}),
        )
        return cls(
            interface_id=_non_empty_text(data["interface_id"], "interface_id"),
            version=_non_empty_text(data["version"], "version"),
            request_id=_non_empty_text(data["request_id"], "request_id"),
            correlation_id=_non_empty_text(data["correlation_id"], "correlation_id"),
            payload=_mapping(data["payload"], "payload"),
        )


@dataclass(frozen=True, slots=True)
class ApiResponse(PublicModel):
    component_id: str
    interface_id: str
    version: str
    request_id: str
    correlation_id: str
    outcome: ApiOutcome
    terminal: bool
    result: dict[str, JSONValue] | None = None
    error: ApiError | None = None

    def __post_init__(self) -> None:
        if self.outcome is ApiOutcome.SUCCEEDED:
            if self.result is None or self.error is not None:
                raise ModelValidationError(
                    "result",
                    "invalid_success_envelope",
                    "successful responses require a result and prohibit an error",
                )
        elif self.error is None or self.result is not None:
            raise ModelValidationError(
                "error",
                "invalid_failure_envelope",
                "rejected or failed responses require an error and prohibit a result",
            )

    @classmethod
    def success(cls, request: ApiRequest, model: PublicModel) -> "ApiResponse":
        return cls(
            component_id=COMPONENT_ID,
            interface_id=request.interface_id,
            version=request.version,
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            outcome=ApiOutcome.SUCCEEDED,
            terminal=True,
            result=model.to_dict(),
        )

    @classmethod
    def failure(
        cls,
        request: ApiRequest,
        *,
        outcome: ApiOutcome,
        code: str,
        message: str,
        retryable: bool = False,
        details: Mapping[str, JSONValue] | None = None,
    ) -> "ApiResponse":
        if outcome is ApiOutcome.SUCCEEDED:
            raise ValueError("failure response cannot use succeeded outcome")
        return cls(
            component_id=COMPONENT_ID,
            interface_id=request.interface_id,
            version=request.version,
            request_id=request.request_id,
            correlation_id=request.correlation_id,
            outcome=outcome,
            terminal=True,
            error=ApiError(
                code=code,
                message=message,
                retryable=retryable,
                details=dict(details or {}),
            ),
        )
