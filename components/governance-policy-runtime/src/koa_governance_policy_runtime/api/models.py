"""Transport-neutral public models for Governance Policy Runtime.

This module owns validation of the observable component boundary only.  It does
not load bundles, evaluate policy, persist receipts, verify identity, publish
content, execute privileged operations, or mutate a caller's business state.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field, fields as dataclass_fields, is_dataclass
from enum import Enum
import re
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, Sequence

COMPONENT_ID = "governance_policy_runtime"
API_VERSION = "1.0.0"

JSONScalar = str | int | float | bool | None
JSONValue = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]

_REQUEST_ID = re.compile(r"^POLREQ-[A-Z0-9-]{8,}$")
_CORRELATION_ID = re.compile(r"^CORR-[A-Z0-9-]{8,}$")
_SECRET_KEYS = frozenset(
    {
        "api_key",
        "access_token",
        "auth_token",
        "credential",
        "credentials",
        "password",
        "private_key",
        "raw_root_credential",
        "secret",
        "secret_key",
    }
)


class ModelValidationError(ValueError):
    """Deterministic validation failure that contains no submitted value."""

    def __init__(self, field_name: str, code: str, message: str) -> None:
        super().__init__(message)
        self.field_name = field_name
        self.code = code
        self.message = message

    def as_error(self) -> dict[str, str]:
        return {"code": self.code, "field": self.field_name, "message": self.message}


class DecisionClass(str, Enum):
    AUTHORIZATION = "authorization"
    DISCLOSURE = "disclosure"
    CONSENT = "consent"
    PRIVILEGE = "privilege"
    EXCEPTION = "exception"


class DecisionResult(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    BLOCKED = "blocked"


class ObligationType(str, Enum):
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


class ApiOutcome(str, Enum):
    SUCCEEDED = "succeeded"
    REJECTED = "rejected"
    FAILED = "failed"


class ServiceState(str, Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    MAINTENANCE = "maintenance"
    STOPPED = "stopped"


class PolicySetState(str, Enum):
    ABSENT = "absent"
    STAGED = "staged"
    VALIDATING = "validating"
    VALIDATED = "validated"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    ACTIVATION_FAILED = "activation_failed"
    ROLLBACK_REQUIRED = "rollback_required"
    FORWARD_REPAIR_REQUIRED = "forward_repair_required"


class FailureCode(str, Enum):
    POLICY_MISSING = "GOV_POLICY_MISSING"
    POLICY_STALE = "GOV_POLICY_STALE"
    POLICY_INCOMPATIBLE = "GOV_POLICY_INCOMPATIBLE"
    IDENTITY_UNVERIFIED = "GOV_IDENTITY_UNVERIFIED"
    CONTEXT_INVALID = "GOV_CONTEXT_INVALID"
    EXCEPTION_INVALID = "GOV_EXCEPTION_INVALID"
    OBLIGATION_UNSATISFIED = "GOV_OBLIGATION_UNSATISFIED"
    RECEIPT_FAILURE = "GOV_RECEIPT_FAILURE"
    AUDIT_UNAVAILABLE = "GOV_AUDIT_UNAVAILABLE"
    ACTIVATION_FAILED = "GOV_ACTIVATION_FAILED"
    EXTERNAL_AI_UNAVAILABLE = "GOV_EXTERNAL_AI_UNAVAILABLE"


DECISION_CONTEXT_FIELDS: Mapping[DecisionClass, frozenset[str]] = MappingProxyType(
    {
        DecisionClass.AUTHORIZATION: frozenset(
            {
                "verified_requester",
                "registered_action",
                "target",
                "scope",
                "component_authority",
                "profile_applicability",
            }
        ),
        DecisionClass.DISCLOSURE: frozenset(
            {
                "source_owner",
                "data_or_representation",
                "destination",
                "audience",
                "purpose",
                "applicable_consent",
                "retention_or_use_constraints",
            }
        ),
        DecisionClass.CONSENT: frozenset(
            {
                "subject",
                "purpose",
                "data_scope",
                "recipient_or_use_domain",
                "duration_or_closure_condition",
                "revocation_state",
                "evidence_obligations",
            }
        ),
        DecisionClass.PRIVILEGE: frozenset(
            {
                "verified_requester",
                "target_node_or_resource",
                "exact_privileged_operation",
                "profile",
                "assurance_context",
                "duration",
                "evidence_requirements",
            }
        ),
        DecisionClass.EXCEPTION: frozenset(
            {
                "exception_id",
                "affected_requirement_or_lock",
                "subject",
                "scope",
                "activation_condition",
                "expiration_or_closure_condition",
                "compensating_controls",
                "evidence_obligations",
            }
        ),
    }
)


def _require_string(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ModelValidationError(field_name, "invalid_string", f"{field_name} must be a non-empty string")
    return value


def _require_request_id(value: object, field_name: str = "request_id") -> str:
    text = _require_string(value, field_name)
    if not _REQUEST_ID.fullmatch(text):
        raise ModelValidationError(field_name, "invalid_request_id", f"{field_name} does not match the registered format")
    return text


def _require_correlation_id(value: object, field_name: str = "correlation_id") -> str:
    text = _require_string(value, field_name)
    if not _CORRELATION_ID.fullmatch(text):
        raise ModelValidationError(field_name, "invalid_correlation_id", f"{field_name} does not match the registered format")
    return text


def _require_mapping(value: object, field_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ModelValidationError(field_name, "invalid_mapping", f"{field_name} must be an object")
    result: dict[str, Any] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ModelValidationError(field_name, "invalid_mapping_key", f"{field_name} keys must be strings")
        result[key] = item
    return result


def _require_string_sequence(value: object, field_name: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise ModelValidationError(field_name, "invalid_sequence", f"{field_name} must be an array of strings")
    result = tuple(_require_string(item, field_name) for item in value)
    if not allow_empty and not result:
        raise ModelValidationError(field_name, "empty_sequence", f"{field_name} must not be empty")
    if len(set(result)) != len(result):
        raise ModelValidationError(field_name, "duplicate_value", f"{field_name} must not contain duplicates")
    return result


def _reject_unknown_fields(data: Mapping[str, Any], allowed: frozenset[str], field_name: str = "payload") -> None:
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ModelValidationError(field_name, "unknown_field", f"{field_name} contains undeclared fields")


def _find_secret_key(value: object, path: str = "payload") -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key).lower()
            if key_text in _SECRET_KEYS or key_text.endswith("_password") or key_text.endswith("_secret"):
                return f"{path}.{key}"
            found = _find_secret_key(item, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for index, item in enumerate(value):
            found = _find_secret_key(item, f"{path}[{index}]")
            if found:
                return found
    return None


def _reject_secrets(value: object, field_name: str = "payload") -> None:
    if _find_secret_key(value, field_name):
        raise ModelValidationError(field_name, "secret_field_prohibited", f"{field_name} contains a prohibited secret field")


def _enum_value(enum_type: type[Enum], value: object, field_name: str):
    try:
        return enum_type(value)
    except (TypeError, ValueError) as exc:
        raise ModelValidationError(field_name, "invalid_enum", f"{field_name} contains an unregistered value") from exc


def _to_json(value: Any) -> JSONValue:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {item.name: _to_json(getattr(value, item.name)) for item in dataclass_fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _to_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_to_json(item) for item in value]
    if isinstance(value, list):
        return [_to_json(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"unsupported public JSON value: {type(value).__name__}")


@dataclass(frozen=True, slots=True)
class ApiError:
    code: str
    message: str
    field: str | None = None
    details: Mapping[str, JSONValue] = dataclass_field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_string(self.code, "code")
        _require_string(self.message, "message")
        object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(frozen=True, slots=True)
class ApiRequest:
    interface_id: str
    request_id: str
    correlation_id: str
    payload: Mapping[str, Any]
    version: str = API_VERSION

    _FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"interface_id", "request_id", "correlation_id", "payload", "version"}
    )

    def __post_init__(self) -> None:
        _require_string(self.interface_id, "interface_id")
        _require_request_id(self.request_id)
        _require_correlation_id(self.correlation_id)
        if self.version != API_VERSION:
            raise ModelValidationError("version", "unsupported_version", "version is not supported")
        payload = _require_mapping(self.payload, "payload")
        _reject_secrets(payload)
        object.__setattr__(self, "payload", MappingProxyType(payload))

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ApiRequest":
        data = _require_mapping(value, "request")
        _reject_unknown_fields(data, cls._FIELDS, "request")
        missing = sorted(cls._FIELDS - set(data))
        if missing:
            raise ModelValidationError("request", "missing_field", "request is missing required fields")
        return cls(
            interface_id=data["interface_id"],
            request_id=data["request_id"],
            correlation_id=data["correlation_id"],
            payload=data["payload"],
            version=data["version"],
        )


@dataclass(frozen=True, slots=True)
class PolicyObligation:
    obligation_type: ObligationType
    parameters: Mapping[str, JSONValue] = dataclass_field(default_factory=dict)
    required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "obligation_type", _enum_value(ObligationType, self.obligation_type, "obligation_type"))
        parameters = _require_mapping(self.parameters, "parameters")
        _reject_secrets(parameters, "parameters")
        object.__setattr__(self, "parameters", MappingProxyType(parameters))


@dataclass(frozen=True, slots=True)
class DecisionReceipt:
    receipt_id: str
    request_id: str
    correlation_id: str
    requester_ref: str
    action_ref: str
    target_ref: str
    scope: Mapping[str, JSONValue]
    decision_class: DecisionClass
    result: DecisionResult
    obligations: tuple[PolicyObligation, ...]
    policy_set_ref: str
    authority_version: str
    verified_context_refs: tuple[str, ...]
    exception_ids: tuple[str, ...]
    evaluated_at: str
    evaluator_identity: str
    evaluator_version: str

    def __post_init__(self) -> None:
        _require_string(self.receipt_id, "receipt_id")
        _require_request_id(self.request_id)
        _require_correlation_id(self.correlation_id)
        for name in ("requester_ref", "action_ref", "target_ref", "policy_set_ref", "authority_version", "evaluated_at", "evaluator_identity", "evaluator_version"):
            _require_string(getattr(self, name), name)
        object.__setattr__(self, "scope", MappingProxyType(_require_mapping(self.scope, "scope")))
        object.__setattr__(self, "decision_class", _enum_value(DecisionClass, self.decision_class, "decision_class"))
        object.__setattr__(self, "result", _enum_value(DecisionResult, self.result, "result"))
        object.__setattr__(self, "obligations", tuple(self.obligations))
        object.__setattr__(self, "verified_context_refs", _require_string_sequence(self.verified_context_refs, "verified_context_refs"))
        object.__setattr__(self, "exception_ids", _require_string_sequence(self.exception_ids, "exception_ids"))
        serialized = _to_json(self)
        _reject_secrets(serialized, "receipt")
        prohibited = {"execution_payload", "credential", "private_key"}
        if prohibited.intersection(serialized):
            raise ModelValidationError("receipt", "execution_evidence_prohibited", "receipt must not contain execution evidence")


@dataclass(frozen=True, slots=True)
class PolicyEvaluationRequest:
    request_id: str
    correlation_id: str
    decision_class: DecisionClass
    requester: Mapping[str, JSONValue]
    action: str
    target: str
    scope: Mapping[str, JSONValue]
    policy_set_ref: str
    authority_version: str
    evaluation_context: Mapping[str, JSONValue]
    exception_ids: tuple[str, ...] = ()
    prior_receipt_refs: tuple[str, ...] = ()
    requested_at: str | None = None

    _FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "request_id", "correlation_id", "decision_class", "requester", "action",
            "target", "scope", "policy_set_ref", "authority_version", "evaluation_context",
            "exception_ids", "prior_receipt_refs", "requested_at",
        }
    )

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "PolicyEvaluationRequest":
        data = _require_mapping(payload, "payload")
        _reject_unknown_fields(data, cls._FIELDS)
        required = cls._FIELDS - {"exception_ids", "prior_receipt_refs", "requested_at"}
        if required - set(data):
            raise ModelValidationError("payload", "missing_field", "policy evaluation request is missing required fields")
        request_id = _require_request_id(data["request_id"])
        correlation_id = _require_correlation_id(data["correlation_id"])
        if request_id != envelope.request_id or correlation_id != envelope.correlation_id:
            raise ModelValidationError("correlation_id", "correlation_mismatch", "payload and envelope identifiers must match")
        decision_class = _enum_value(DecisionClass, data["decision_class"], "decision_class")
        context = _require_mapping(data["evaluation_context"], "evaluation_context")
        expected = DECISION_CONTEXT_FIELDS[decision_class]
        if set(context) != set(expected):
            raise ModelValidationError("evaluation_context", "unbounded_context", "evaluation_context must contain exactly the registered decision context")
        _reject_secrets(context, "evaluation_context")
        requested_at = data.get("requested_at")
        if requested_at is not None:
            requested_at = _require_string(requested_at, "requested_at")
        return cls(
            request_id=request_id,
            correlation_id=correlation_id,
            decision_class=decision_class,
            requester=MappingProxyType(_require_mapping(data["requester"], "requester")),
            action=_require_string(data["action"], "action"),
            target=_require_string(data["target"], "target"),
            scope=MappingProxyType(_require_mapping(data["scope"], "scope")),
            policy_set_ref=_require_string(data["policy_set_ref"], "policy_set_ref"),
            authority_version=_require_string(data["authority_version"], "authority_version"),
            evaluation_context=MappingProxyType(context),
            exception_ids=_require_string_sequence(data.get("exception_ids", ()), "exception_ids"),
            prior_receipt_refs=_require_string_sequence(data.get("prior_receipt_refs", ()), "prior_receipt_refs"),
            requested_at=requested_at,
        )


@dataclass(frozen=True, slots=True)
class PolicyEvaluationResponse:
    request_id: str
    correlation_id: str
    decision_class: DecisionClass
    result: DecisionResult
    policy_set_ref: str
    authority_version: str
    evaluated_at: str
    evaluator_identity: str
    obligations: tuple[PolicyObligation, ...]
    diagnostics: tuple[str, ...]
    receipt: DecisionReceipt

    def __post_init__(self) -> None:
        _require_request_id(self.request_id)
        _require_correlation_id(self.correlation_id)
        object.__setattr__(self, "decision_class", _enum_value(DecisionClass, self.decision_class, "decision_class"))
        object.__setattr__(self, "result", _enum_value(DecisionResult, self.result, "result"))
        for name in ("policy_set_ref", "authority_version", "evaluated_at", "evaluator_identity"):
            _require_string(getattr(self, name), name)
        object.__setattr__(self, "obligations", tuple(self.obligations))
        object.__setattr__(self, "diagnostics", _require_string_sequence(self.diagnostics, "diagnostics"))
        if self.receipt.request_id != self.request_id or self.receipt.correlation_id != self.correlation_id:
            raise ModelValidationError("receipt", "receipt_correlation_mismatch", "receipt must match the evaluated request")
        if self.receipt.decision_class is not self.decision_class or self.receipt.result is not self.result:
            raise ModelValidationError("receipt", "receipt_semantic_mismatch", "receipt must match the decision semantics")
        if self.result is DecisionResult.ALLOW and not all(obligation.required for obligation in self.obligations):
            raise ModelValidationError("obligations", "optional_obligation_prohibited", "allow obligations returned by the authority must be required")


@dataclass(frozen=True, slots=True)
class PolicyBundleStageRequest:
    request_id: str
    correlation_id: str
    bundle_ref: str
    target_profiles: tuple[str, ...]
    target_components: tuple[str, ...]
    expected_current_policy_set: str
    proposed_policy_set: str
    release_set_ref: str

    _FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"request_id", "correlation_id", "bundle_ref", "target_profiles", "target_components", "expected_current_policy_set", "proposed_policy_set", "release_set_ref"}
    )

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "PolicyBundleStageRequest":
        data = _closed_payload(payload, cls._FIELDS, envelope)
        return cls(
            request_id=envelope.request_id,
            correlation_id=envelope.correlation_id,
            bundle_ref=_require_string(data["bundle_ref"], "bundle_ref"),
            target_profiles=_require_string_sequence(data["target_profiles"], "target_profiles", allow_empty=False),
            target_components=_require_string_sequence(data["target_components"], "target_components", allow_empty=False),
            expected_current_policy_set=_require_string(data["expected_current_policy_set"], "expected_current_policy_set"),
            proposed_policy_set=_require_string(data["proposed_policy_set"], "proposed_policy_set"),
            release_set_ref=_require_string(data["release_set_ref"], "release_set_ref"),
        )


@dataclass(frozen=True, slots=True)
class PolicyBundleStageResponse:
    bundle_ref: str
    candidate_policy_set_ref: str
    validation_plan_ref: str
    state: PolicySetState = PolicySetState.STAGED
    active: bool = False

    def __post_init__(self) -> None:
        for name in ("bundle_ref", "candidate_policy_set_ref", "validation_plan_ref"):
            _require_string(getattr(self, name), name)
        object.__setattr__(self, "state", _enum_value(PolicySetState, self.state, "state"))
        if self.state is not PolicySetState.STAGED or self.active:
            raise ModelValidationError("state", "partial_activation_prohibited", "staging must not activate policy authority")


@dataclass(frozen=True, slots=True)
class PolicySetActivationRequest:
    request_id: str
    correlation_id: str
    staged_policy_set_ref: str
    expected_current_policy_set: str
    release_set_ref: str
    activation_authority_ref: str

    _FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"request_id", "correlation_id", "staged_policy_set_ref", "expected_current_policy_set", "release_set_ref", "activation_authority_ref"}
    )

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "PolicySetActivationRequest":
        data = _closed_payload(payload, cls._FIELDS, envelope)
        return cls(
            request_id=envelope.request_id,
            correlation_id=envelope.correlation_id,
            staged_policy_set_ref=_require_string(data["staged_policy_set_ref"], "staged_policy_set_ref"),
            expected_current_policy_set=_require_string(data["expected_current_policy_set"], "expected_current_policy_set"),
            release_set_ref=_require_string(data["release_set_ref"], "release_set_ref"),
            activation_authority_ref=_require_string(data["activation_authority_ref"], "activation_authority_ref"),
        )


@dataclass(frozen=True, slots=True)
class PolicySetActivationResponse:
    previous_policy_set_ref: str
    active_policy_set_ref: str
    release_set_ref: str
    activation_receipt_ref: str
    state: PolicySetState = PolicySetState.ACTIVE
    atomic: bool = True

    def __post_init__(self) -> None:
        for name in ("previous_policy_set_ref", "active_policy_set_ref", "release_set_ref", "activation_receipt_ref"):
            _require_string(getattr(self, name), name)
        object.__setattr__(self, "state", _enum_value(PolicySetState, self.state, "state"))
        if self.state is not PolicySetState.ACTIVE or not self.atomic:
            raise ModelValidationError("atomic", "partial_activation_prohibited", "policy activation must be atomic")
        if self.previous_policy_set_ref == self.active_policy_set_ref:
            raise ModelValidationError("active_policy_set_ref", "activation_no_change", "active and previous policy sets must differ")


@dataclass(frozen=True, slots=True)
class PolicySetRollbackRequest:
    request_id: str
    correlation_id: str
    failed_policy_set_ref: str
    expected_active_policy_set: str
    previous_valid_policy_set_ref: str
    rollback_authority_ref: str

    _FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"request_id", "correlation_id", "failed_policy_set_ref", "expected_active_policy_set", "previous_valid_policy_set_ref", "rollback_authority_ref"}
    )

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "PolicySetRollbackRequest":
        data = _closed_payload(payload, cls._FIELDS, envelope)
        return cls(
            request_id=envelope.request_id,
            correlation_id=envelope.correlation_id,
            failed_policy_set_ref=_require_string(data["failed_policy_set_ref"], "failed_policy_set_ref"),
            expected_active_policy_set=_require_string(data["expected_active_policy_set"], "expected_active_policy_set"),
            previous_valid_policy_set_ref=_require_string(data["previous_valid_policy_set_ref"], "previous_valid_policy_set_ref"),
            rollback_authority_ref=_require_string(data["rollback_authority_ref"], "rollback_authority_ref"),
        )


@dataclass(frozen=True, slots=True)
class PolicySetRollbackResponse:
    outcome: str
    failed_policy_set_ref: str
    restored_policy_set_ref: str | None = None
    rollback_receipt_ref: str | None = None
    repair_plan_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.outcome not in {"rolled_back", "forward_repair_required"}:
            raise ModelValidationError("outcome", "invalid_enum", "rollback outcome is not registered")
        _require_string(self.failed_policy_set_ref, "failed_policy_set_ref")
        object.__setattr__(self, "evidence_refs", _require_string_sequence(self.evidence_refs, "evidence_refs"))
        if self.outcome == "rolled_back":
            if not self.restored_policy_set_ref or not self.rollback_receipt_ref or self.repair_plan_ref:
                raise ModelValidationError("outcome", "invalid_rollback_result", "successful rollback requires restored state and receipt only")
        else:
            if not self.repair_plan_ref or self.restored_policy_set_ref or self.rollback_receipt_ref:
                raise ModelValidationError("outcome", "invalid_forward_repair_result", "unsafe rollback must require forward repair without claiming restoration")


@dataclass(frozen=True, slots=True)
class PolicySetStatusRequest:
    requester_identity: Mapping[str, JSONValue]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "PolicySetStatusRequest":
        data = _query_payload(payload, frozenset({"requester_identity"}))
        return cls(requester_identity=MappingProxyType(_require_mapping(data["requester_identity"], "requester_identity")))


@dataclass(frozen=True, slots=True)
class PolicySetStatusResponse:
    active_policy_set_ref: str | None
    staged_policy_set_refs: tuple[str, ...]
    previous_valid_policy_set_ref: str | None
    compatibility_state: str
    activation_state: PolicySetState
    authority_version: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "staged_policy_set_refs", _require_string_sequence(self.staged_policy_set_refs, "staged_policy_set_refs"))
        object.__setattr__(self, "activation_state", _enum_value(PolicySetState, self.activation_state, "activation_state"))
        _require_string(self.compatibility_state, "compatibility_state")
        for name in ("active_policy_set_ref", "previous_valid_policy_set_ref", "authority_version"):
            value = getattr(self, name)
            if value is not None:
                _require_string(value, name)


@dataclass(frozen=True, slots=True)
class DecisionReceiptQuery:
    receipt_id: str | None
    decision_correlation_id: str | None
    requester_identity: Mapping[str, JSONValue]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "DecisionReceiptQuery":
        data = _query_payload(payload, frozenset({"receipt_id", "decision_correlation_id", "requester_identity"}), required=frozenset({"requester_identity"}))
        receipt_id = data.get("receipt_id")
        correlation_id = data.get("decision_correlation_id")
        if (receipt_id is None) == (correlation_id is None):
            raise ModelValidationError("payload", "query_selector_invalid", "exactly one receipt selector is required")
        return cls(
            receipt_id=None if receipt_id is None else _require_string(receipt_id, "receipt_id"),
            decision_correlation_id=None if correlation_id is None else _require_correlation_id(correlation_id, "decision_correlation_id"),
            requester_identity=MappingProxyType(_require_mapping(data["requester_identity"], "requester_identity")),
        )


@dataclass(frozen=True, slots=True)
class HealthAndReadinessRequest:
    requester_identity: Mapping[str, JSONValue]

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any], envelope: ApiRequest) -> "HealthAndReadinessRequest":
        data = _query_payload(payload, frozenset({"requester_identity"}))
        return cls(requester_identity=MappingProxyType(_require_mapping(data["requester_identity"], "requester_identity")))


@dataclass(frozen=True, slots=True)
class GovernancePolicyHealthResponse:
    service_state: ServiceState
    process_healthy: bool
    ready: bool
    health_checks: Mapping[str, bool]
    readiness_checks: Mapping[str, bool]
    active_policy_set_ref: str | None
    authority_version: str | None
    compatible: bool
    blocked_decision_classes: tuple[DecisionClass, ...] = ()
    diagnostic_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_state", _enum_value(ServiceState, self.service_state, "service_state"))
        health = _boolean_check_map(self.health_checks, "health_checks")
        readiness = _boolean_check_map(self.readiness_checks, "readiness_checks")
        object.__setattr__(self, "health_checks", MappingProxyType(health))
        object.__setattr__(self, "readiness_checks", MappingProxyType(readiness))
        object.__setattr__(self, "blocked_decision_classes", tuple(_enum_value(DecisionClass, item, "blocked_decision_classes") for item in self.blocked_decision_classes))
        object.__setattr__(self, "diagnostic_refs", _require_string_sequence(self.diagnostic_refs, "diagnostic_refs"))
        if self.process_healthy != all(health.values()):
            raise ModelValidationError("process_healthy", "health_inconsistent", "process health must equal all health checks")
        if self.ready != all(readiness.values()):
            raise ModelValidationError("ready", "readiness_inconsistent", "readiness must equal all readiness checks")
        if self.ready and (not self.process_healthy or not self.compatible or not self.active_policy_set_ref):
            raise ModelValidationError("ready", "readiness_inconsistent", "ready requires health, compatibility, and active authority")
        for name in ("active_policy_set_ref", "authority_version"):
            value = getattr(self, name)
            if value is not None:
                _require_string(value, name)


@dataclass(frozen=True, slots=True)
class ApiResponse:
    request_id: str
    correlation_id: str
    interface_id: str
    outcome: ApiOutcome
    result: JSONValue | None = None
    error: ApiError | None = None
    version: str = API_VERSION
    terminal: bool = True

    def __post_init__(self) -> None:
        _require_string(self.interface_id, "interface_id")
        object.__setattr__(self, "outcome", _enum_value(ApiOutcome, self.outcome, "outcome"))
        if self.version != API_VERSION:
            raise ModelValidationError("version", "unsupported_version", "response version is not supported")
        if not self.terminal:
            raise ModelValidationError("terminal", "non_terminal_response", "public responses must be terminal")
        if self.outcome is ApiOutcome.SUCCEEDED:
            if self.result is None or self.error is not None:
                raise ModelValidationError("outcome", "response_shape_invalid", "success requires result and no error")
        elif self.result is not None or self.error is None:
            raise ModelValidationError("outcome", "response_shape_invalid", "failure requires error and no result")

    @classmethod
    def success(cls, request: ApiRequest, result: object) -> "ApiResponse":
        return cls(request.request_id, request.correlation_id, request.interface_id, ApiOutcome.SUCCEEDED, result=_to_json(result))

    @classmethod
    def rejected(cls, request: ApiRequest, error: ApiError) -> "ApiResponse":
        return cls(request.request_id, request.correlation_id, request.interface_id, ApiOutcome.REJECTED, error=error)

    @classmethod
    def failed(cls, request: ApiRequest, error: ApiError) -> "ApiResponse":
        return cls(request.request_id, request.correlation_id, request.interface_id, ApiOutcome.FAILED, error=error)

    def to_dict(self) -> dict[str, JSONValue]:
        return _to_json(self)  # type: ignore[return-value]


def _closed_payload(payload: Mapping[str, Any], fields_: frozenset[str], envelope: ApiRequest) -> dict[str, Any]:
    data = _require_mapping(payload, "payload")
    _reject_unknown_fields(data, fields_)
    if fields_ - set(data):
        raise ModelValidationError("payload", "missing_field", "request is missing required fields")
    if _require_request_id(data["request_id"]) != envelope.request_id or _require_correlation_id(data["correlation_id"]) != envelope.correlation_id:
        raise ModelValidationError("correlation_id", "correlation_mismatch", "payload and envelope identifiers must match")
    return data


def _query_payload(payload: Mapping[str, Any], allowed: frozenset[str], *, required: frozenset[str] | None = None) -> dict[str, Any]:
    data = _require_mapping(payload, "payload")
    _reject_unknown_fields(data, allowed)
    required_fields = allowed if required is None else required
    if required_fields - set(data):
        raise ModelValidationError("payload", "missing_field", "query is missing required fields")
    return data


def _boolean_check_map(value: Mapping[str, bool], field_name: str) -> dict[str, bool]:
    data = _require_mapping(value, field_name)
    if not data or not all(isinstance(item, bool) for item in data.values()):
        raise ModelValidationError(field_name, "invalid_check_map", f"{field_name} must contain boolean checks")
    return {key: bool(item) for key, item in data.items()}
