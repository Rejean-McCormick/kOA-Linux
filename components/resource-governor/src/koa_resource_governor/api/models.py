"""Strict public transport models for Resource Governor.

The API projects the canonical ``RG-IF-*`` interfaces without owning policy,
identity, workload business data, or host-wide privilege.  It validates only
transport and resource-governance semantics; application and adapter behavior
is supplied through the public service port in :mod:`routes`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

COMPONENT_ID = "resource_governor"
CONTRACT_VERSION = "1.0.0"
API_VERSION = "v1"


class OperationKind(StrEnum):
    COMMAND = "command"
    QUERY = "query"


class AdmissionOutcome(StrEnum):
    ADMITTED = "admitted"
    QUEUED = "queued"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    BLOCKED = "blocked"


class QueueItemState(StrEnum):
    ACCEPTED = "accepted"
    WAITING = "waiting"
    ELIGIBLE = "eligible"
    DEQUEUED = "dequeued"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    REJECTED = "rejected"
    COMPLETED = "completed"


class WorkloadEventType(StrEnum):
    STARTED = "started"
    CHECKPOINTED = "checkpointed"
    SUSPENDED = "suspended"
    RESUMED = "resumed"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TERMINATED = "terminated"


class ResourceControlCommand(StrEnum):
    APPLY_LIMITS = "apply_limits"
    UPDATE_LIMITS = "update_limits"
    THROTTLE = "throttle"
    SUSPEND = "suspend"
    RESUME = "resume"
    TERMINATE = "terminate"
    RELEASE = "release"


class DegradationState(StrEnum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    RESTORING = "restoring"


EXPECTED_FAILURE_CODES = frozenset(
    {
        "active_envelope_unresolved",
        "envelope_incompatible",
        "authority_unresolved",
        "enforcement_adapter_unavailable",
        "execution_identity_unresolved",
        "resource_observation_unavailable",
        "capacity_pressure",
        "queue_capacity_exhausted",
        "durable_queue_unavailable",
        "policy_runtime_unavailable",
        "receipt_path_unavailable",
        "hard_integrity_pressure",
        "component_runtime_unavailable",
        "reconciliation_incomplete",
        "current_controls_unverified",
        "unsupported_resource_dimension",
        "control_operation_not_permitted",
        "business_authority_boundary_violation",
        "cross_component_data_write_attempt",
    }
)

BOUNDARY_FAILURE_CODES = frozenset(
    {
        "request_contract_violation",
        "response_contract_violation",
        "operation_not_declared",
        "method_not_allowed",
        "missing_correlation_context",
        "missing_idempotency_key",
        "contract_version_unsupported",
        "workload_payload_prohibited",
    }
)

# Resource observations and requests may carry resource metadata, but never the
# owning workload's business content or credentials.  The check is recursive.
_PROHIBITED_WORKLOAD_KEYS = frozenset(
    {
        "business_payload",
        "workload_payload",
        "domain_data",
        "document_content",
        "media_content",
        "message_content",
        "prompt_content",
        "raw_command_arguments",
        "credential",
        "credentials",
        "password",
        "private_key",
        "secret",
        "token",
    }
)

_PROHIBITED_RESPONSE_KEYS = _PROHIBITED_WORKLOAD_KEYS | frozenset(
    {"authorization_result", "consent_result", "disclosure_result", "privilege_result"}
)


class ApiBoundaryError(ValueError):
    """Stable non-secret error emitted by the public boundary."""

    def __init__(self, code: str, message: str, *, field: str | None = None) -> None:
        if code not in EXPECTED_FAILURE_CODES | BOUNDARY_FAILURE_CODES:
            raise ValueError(f"undeclared API boundary code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message
        self.field = field


@dataclass(frozen=True, slots=True)
class OperationSpec:
    operation_id: str
    kind: OperationKind
    interface_ids: tuple[str, ...]
    required_request_fields: tuple[str, ...]
    response_fields: tuple[str, ...]
    optional_request_fields: tuple[str, ...] = ()
    idempotency: str | None = None
    critical_transition: bool = False

    @property
    def path(self) -> str:
        collection = "commands" if self.kind is OperationKind.COMMAND else "queries"
        return f"/{API_VERSION}/{collection}/{self.operation_id}"

    @property
    def requires_idempotency_key(self) -> bool:
        return self.idempotency == "idempotency_key_required"


_OPERATION_SPECS = (
    OperationSpec(
        "activate_resource_envelope",
        OperationKind.COMMAND,
        ("RG-IF-001", "RG-IF-010"),
        (
            "request_id",
            "envelope_ref",
            "target_scope",
            "requested_activation_time",
            "requesting_actor_ref",
        ),
        (
            "request_id",
            "activation_state",
            "active_envelope_ref",
            "previous_envelope_ref",
            "activated_at",
            "receipt_ref",
        ),
        idempotency="idempotency_key_required",
        critical_transition=True,
    ),
    OperationSpec(
        "admit_workload",
        OperationKind.COMMAND,
        ("RG-IF-002", "RG-IF-003"),
        (
            "request_id",
            "workload_owner_ref",
            "workload_class",
            "target_scope",
            "resource_request",
            "criticality",
            "priority",
            "requested_at",
        ),
        (
            "decision_id",
            "request_id",
            "outcome",
            "resolved_envelope_refs",
            "decision_reason",
            "decided_at",
        ),
        optional_request_fields=(
            "deadline",
            "expiry",
            "queue_policy_ref",
            "policy_decision_ref",
            "exception_refs",
        ),
        idempotency="request_scoped",
    ),
    OperationSpec(
        "record_usage_observation",
        OperationKind.COMMAND,
        ("RG-IF-005",),
        (
            "observation_id",
            "target_execution_ref",
            "resource_measurements",
            "observed_at",
            "measurement_source",
        ),
        ("observation_id", "accepted", "recorded_at"),
        idempotency="observation_identity",
    ),
    OperationSpec(
        "record_workload_lifecycle_event",
        OperationKind.COMMAND,
        ("RG-IF-006",),
        ("event_id", "target_execution_ref", "event_type", "occurred_at"),
        ("event_id", "target_execution_ref", "recorded_state", "recorded_at"),
        idempotency="event_identity",
    ),
    OperationSpec(
        "get_admission_decision",
        OperationKind.QUERY,
        ("RG-IF-003",),
        ("request_id",),
        (
            "decision_id",
            "request_id",
            "outcome",
            "resolved_envelope_refs",
            "decision_reason",
            "decided_at",
        ),
    ),
    OperationSpec(
        "get_execution_binding",
        OperationKind.QUERY,
        ("RG-IF-004",),
        ("request_id",),
        (
            "binding_id",
            "request_id",
            "target_execution_ref",
            "applied_limits",
            "lease_or_reservation",
            "effective_at",
        ),
    ),
    OperationSpec(
        "get_resource_control_command",
        OperationKind.QUERY,
        ("RG-IF-007",),
        ("command_id",),
        (
            "command_id",
            "target_execution_ref",
            "command",
            "reason",
            "expected_result",
            "issued_at",
        ),
    ),
    OperationSpec(
        "get_resource_pressure_event",
        OperationKind.QUERY,
        ("RG-IF-008",),
        ("event_id",),
        (
            "event_id",
            "scope",
            "pressure_class",
            "severity",
            "affected_capabilities",
            "active_degradation_actions",
            "occurred_at",
        ),
    ),
    OperationSpec(
        "get_queue_item_state",
        OperationKind.QUERY,
        ("RG-IF-009",),
        ("queue_item_id",),
        (
            "queue_item_id",
            "workload_request_id",
            "state",
            "position_or_priority",
            "updated_at",
        ),
    ),
    OperationSpec(
        "get_component_status",
        OperationKind.QUERY,
        (),
        ("view",),
        (
            "health",
            "readiness",
            "active_envelopes",
            "allocation_state",
            "queue_state",
            "resource_pressure_state",
            "degraded_capabilities",
            "reconciliation_state",
        ),
    ),
)

OPERATIONS: Mapping[str, OperationSpec] = MappingProxyType(
    {spec.operation_id: spec for spec in _OPERATION_SPECS}
)
OPERATIONS_BY_PATH: Mapping[str, OperationSpec] = MappingProxyType(
    {spec.path: spec for spec in _OPERATION_SPECS}
)


@dataclass(frozen=True, slots=True)
class RequestContext:
    correlation_id: str
    contract_version: str
    idempotency_key: str | None = None
    causation_id: str | None = None

    def __post_init__(self) -> None:
        if not self.correlation_id.strip():
            raise ApiBoundaryError(
                "missing_correlation_context", "a non-empty correlation identifier is required"
            )
        if self.contract_version != CONTRACT_VERSION:
            raise ApiBoundaryError(
                "contract_version_unsupported",
                f"unsupported component contract version: {self.contract_version}",
                field="contract_version",
            )
        if self.idempotency_key is not None and not self.idempotency_key.strip():
            raise ApiBoundaryError(
                "request_contract_violation", "idempotency key cannot be empty", field="idempotency_key"
            )


@dataclass(frozen=True, slots=True)
class ApiResponse:
    operation_id: str | None
    correlation_id: str | None
    outcome: str
    payload: Mapping[str, Any] | None = None
    reason_code: str | None = None
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "component_id": COMPONENT_ID,
            "contract_version": CONTRACT_VERSION,
            "operation_id": self.operation_id,
            "correlation_id": self.correlation_id,
            "outcome": self.outcome,
        }
        if self.payload is not None:
            result["payload"] = dict(self.payload)
        if self.reason_code is not None:
            result["reason_code"] = self.reason_code
        if self.message is not None:
            result["message"] = self.message
        return result


def operation_for_path(path: str) -> OperationSpec:
    try:
        return OPERATIONS_BY_PATH[path]
    except KeyError as exc:
        raise ApiBoundaryError("operation_not_declared", "the requested operation is not declared") from exc


def validate_request(
    spec: OperationSpec, payload: Mapping[str, Any], context: RequestContext
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ApiBoundaryError("request_contract_violation", "request payload must be an object")
    _validate_fields(
        spec.required_request_fields,
        spec.optional_request_fields,
        payload,
        boundary="request",
    )
    if spec.requires_idempotency_key and context.idempotency_key is None:
        raise ApiBoundaryError(
            "missing_idempotency_key",
            "this critical transition requires an idempotency key",
            field="idempotency_key",
        )
    prohibited_path = find_prohibited_workload_content(payload)
    if prohibited_path is not None:
        raise ApiBoundaryError(
            "workload_payload_prohibited",
            "workload business content and credentials are outside resource authority",
            field=prohibited_path,
        )
    _require_non_empty_strings(
        payload,
        (
            "request_id",
            "envelope_ref",
            "requesting_actor_ref",
            "workload_owner_ref",
            "workload_class",
            "criticality",
            "observation_id",
            "target_execution_ref",
            "measurement_source",
            "event_id",
            "event_type",
            "command_id",
            "queue_item_id",
            "view",
        ),
    )
    _require_mapping(payload, "target_scope")
    _require_mapping(payload, "resource_request")
    _require_mapping(payload, "resource_measurements")
    if "exception_refs" in payload and not isinstance(payload["exception_refs"], list):
        raise ApiBoundaryError(
            "request_contract_violation", "exception_refs must be an array", field="exception_refs"
        )
    if "event_type" in payload:
        _validate_enum(WorkloadEventType, payload["event_type"], "event_type", "request")
    return dict(payload)


def validate_response(spec: OperationSpec, payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ApiBoundaryError("response_contract_violation", "service response must be an object")
    # Check authority-sensitive content before reporting structural differences so
    # neither a value nor the sensitive field name is reflected to the caller.
    protected_path = find_prohibited_response_content(payload)
    if protected_path is not None:
        raise ApiBoundaryError(
            "response_contract_violation",
            "response crosses a resource or policy authority boundary",
        )
    _validate_fields(spec.response_fields, (), payload, boundary="response")
    if "outcome" in payload:
        _validate_enum(AdmissionOutcome, payload["outcome"], "outcome", "response")
    if "state" in payload:
        _validate_enum(QueueItemState, payload["state"], "state", "response")
    if "command" in payload:
        _validate_enum(ResourceControlCommand, payload["command"], "command", "response")
    if "recorded_state" in payload:
        _validate_enum(WorkloadEventType, payload["recorded_state"], "recorded_state", "response")
    if "resource_pressure_state" in payload:
        _validate_enum(
            DegradationState,
            payload["resource_pressure_state"],
            "resource_pressure_state",
            "response",
        )
    if "resolved_envelope_refs" in payload:
        _require_string_list(payload, "resolved_envelope_refs", boundary="response")
    for name in ("affected_capabilities", "active_degradation_actions", "degraded_capabilities"):
        if name in payload:
            _require_string_list(payload, name, boundary="response")
    for name in (
        "target_scope",
        "resource_request",
        "resource_measurements",
        "applied_limits",
        "lease_or_reservation",
        "health",
        "readiness",
        "allocation_state",
        "queue_state",
        "reconciliation_state",
    ):
        _require_mapping(payload, name, boundary="response")
    if "accepted" in payload and not isinstance(payload["accepted"], bool):
        raise ApiBoundaryError(
            "response_contract_violation", "accepted must be a boolean", field="accepted"
        )
    return dict(payload)


def find_prohibited_workload_content(value: Any, path: str = "request") -> str | None:
    return _find_prohibited_key(value, _PROHIBITED_WORKLOAD_KEYS, path)


def find_prohibited_response_content(value: Any, path: str = "response") -> str | None:
    return _find_prohibited_key(value, _PROHIBITED_RESPONSE_KEYS, path)


def _find_prohibited_key(value: Any, prohibited: frozenset[str], path: str) -> str | None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}"
            if key_text in prohibited:
                return child_path
            found = _find_prohibited_key(nested, prohibited, child_path)
            if found is not None:
                return found
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            found = _find_prohibited_key(nested, prohibited, f"{path}[{index}]")
            if found is not None:
                return found
    return None


def _validate_fields(
    required: tuple[str, ...],
    optional: tuple[str, ...],
    payload: Mapping[str, Any],
    *,
    boundary: str,
) -> None:
    required_set = set(required)
    allowed_set = required_set | set(optional)
    actual_set = set(payload)
    missing = sorted(required_set - actual_set)
    unknown = sorted(actual_set - allowed_set)
    if missing or unknown:
        details = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unknown:
            details.append("unknown=" + ",".join(unknown))
        raise ApiBoundaryError(
            f"{boundary}_contract_violation",
            f"{boundary} fields do not match the declared interface ({'; '.join(details)})",
        )


def _require_non_empty_strings(payload: Mapping[str, Any], names: tuple[str, ...]) -> None:
    for name in names:
        if name not in payload:
            continue
        value = payload[name]
        if not isinstance(value, str) or not value.strip():
            raise ApiBoundaryError(
                "request_contract_violation", f"{name} must be a non-empty string", field=name
            )


def _require_mapping(
    payload: Mapping[str, Any], name: str, *, boundary: str = "request"
) -> None:
    if name not in payload:
        return
    if not isinstance(payload[name], Mapping):
        raise ApiBoundaryError(
            f"{boundary}_contract_violation", f"{name} must be an object", field=name
        )


def _require_string_list(payload: Mapping[str, Any], name: str, *, boundary: str) -> None:
    value = payload[name]
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ApiBoundaryError(
            f"{boundary}_contract_violation",
            f"{name} must be an array of non-empty strings",
            field=name,
        )


def _validate_enum(enum_type: type[StrEnum], value: Any, name: str, boundary: str) -> None:
    try:
        enum_type(str(value))
    except ValueError as exc:
        raise ApiBoundaryError(
            f"{boundary}_contract_violation", f"invalid {name}", field=name
        ) from exc
