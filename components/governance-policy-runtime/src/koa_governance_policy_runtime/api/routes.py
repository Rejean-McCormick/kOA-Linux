"""Transport-neutral dispatch boundary for Governance Policy Runtime."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol, runtime_checkable

from .models import (
    API_VERSION,
    ApiError,
    ApiRequest,
    ApiResponse,
    DecisionReceipt,
    DecisionReceiptQuery,
    GovernancePolicyHealthResponse,
    HealthAndReadinessRequest,
    ModelValidationError,
    PolicyBundleStageRequest,
    PolicyBundleStageResponse,
    PolicyEvaluationRequest,
    PolicyEvaluationResponse,
    PolicySetActivationRequest,
    PolicySetActivationResponse,
    PolicySetRollbackRequest,
    PolicySetRollbackResponse,
    PolicySetStatusRequest,
    PolicySetStatusResponse,
)

EVALUATE_DECISION = "evaluate_decision"
GET_POLICY_SET_STATUS = "get_policy_set_status"
STAGE_POLICY_BUNDLE = "stage_policy_bundle"
ACTIVATE_POLICY_SET = "activate_policy_set"
ROLLBACK_POLICY_SET = "rollback_policy_set"
GET_DECISION_RECEIPT = "get_decision_receipt"
HEALTH_AND_READINESS = "health_and_readiness"


@dataclass(frozen=True, slots=True)
class RouteDefinition:
    interface_id: str
    contract_interface_id: str
    interaction: str
    critical: bool
    request_type: str
    response_type: str


ROUTE_DEFINITIONS: Mapping[str, RouteDefinition] = MappingProxyType(
    {
        EVALUATE_DECISION: RouteDefinition(EVALUATE_DECISION, "IFACE-GOV-POL-001", "request_response", True, "policy_evaluation_request", "policy_evaluation_response"),
        GET_POLICY_SET_STATUS: RouteDefinition(GET_POLICY_SET_STATUS, "IFACE-GOV-POL-002", "query", False, "policy_set_status_request", "policy_set_status_response"),
        STAGE_POLICY_BUNDLE: RouteDefinition(STAGE_POLICY_BUNDLE, "IFACE-GOV-POL-003", "command", True, "policy_bundle_stage_request", "policy_bundle_stage_response"),
        ACTIVATE_POLICY_SET: RouteDefinition(ACTIVATE_POLICY_SET, "IFACE-GOV-POL-004", "command", True, "policy_set_activation_request", "policy_set_activation_response"),
        ROLLBACK_POLICY_SET: RouteDefinition(ROLLBACK_POLICY_SET, "IFACE-GOV-POL-005", "command", True, "policy_set_rollback_request", "policy_set_rollback_response"),
        GET_DECISION_RECEIPT: RouteDefinition(GET_DECISION_RECEIPT, "IFACE-GOV-POL-006", "query", False, "decision_receipt_query", "decision_receipt_response"),
        HEALTH_AND_READINESS: RouteDefinition(HEALTH_AND_READINESS, "IFACE-GOV-POL-007", "query", True, "health_request", "governance_policy_health_response"),
    }
)
INTERFACE_VERSIONS: Mapping[str, str] = MappingProxyType({name: API_VERSION for name in ROUTE_DEFINITIONS})


@runtime_checkable
class GovernancePolicyRuntimeService(Protocol):
    """Public application boundary supplied by preceding bundles."""

    def evaluate_decision(self, request: PolicyEvaluationRequest) -> PolicyEvaluationResponse: ...
    def get_policy_set_status(self, request: PolicySetStatusRequest) -> PolicySetStatusResponse: ...
    def stage_policy_bundle(self, request: PolicyBundleStageRequest) -> PolicyBundleStageResponse: ...
    def activate_policy_set(self, request: PolicySetActivationRequest) -> PolicySetActivationResponse: ...
    def rollback_policy_set(self, request: PolicySetRollbackRequest) -> PolicySetRollbackResponse: ...
    def get_decision_receipt(self, request: DecisionReceiptQuery) -> DecisionReceipt: ...
    def health_and_readiness(self, request: HealthAndReadinessRequest) -> GovernancePolicyHealthResponse: ...


class GovernancePolicyRuntimeServiceError(RuntimeError):
    """Known fail-closed service error safe to map to a public code."""

    failure_code = "GOV_CONTEXT_INVALID"
    public_message = "the policy operation was blocked"
    details: Mapping[str, str] = MappingProxyType({})

    def __init__(self, *, details: Mapping[str, str] | None = None) -> None:
        super().__init__(self.public_message)
        if details:
            self.details = MappingProxyType(dict(details))


class RequiredPolicyUnavailable(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_POLICY_MISSING"
    public_message = "required policy authority is unavailable"


class PolicyStale(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_POLICY_STALE"
    public_message = "the active policy authority is stale"


class PolicyIncompatible(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_POLICY_INCOMPATIBLE"
    public_message = "the policy set is incompatible"


class IdentityUnverified(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_IDENTITY_UNVERIFIED"
    public_message = "required identity could not be verified"


class ReceiptUnavailable(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_RECEIPT_FAILURE"
    public_message = "required decision evidence could not be created"


class AuditUnavailable(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_AUDIT_UNAVAILABLE"
    public_message = "required audit evidence intake is unavailable"


class AtomicActivationFailed(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_ACTIVATION_FAILED"
    public_message = "policy-set activation was blocked"


class ObligationUnsatisfied(GovernancePolicyRuntimeServiceError):
    failure_code = "GOV_OBLIGATION_UNSATISFIED"
    public_message = "a required obligation cannot be satisfied"


Parser = Callable[[Mapping[str, Any], ApiRequest], object]
Handler = Callable[[object], object]


class GovernancePolicyRuntimeApi:
    """Closed dispatcher that delegates all authority to a public service port."""

    def __init__(self, service: GovernancePolicyRuntimeService) -> None:
        self._service = service

    def dispatch(self, raw_request: ApiRequest | Mapping[str, Any]) -> ApiResponse:
        request: ApiRequest | None = raw_request if isinstance(raw_request, ApiRequest) else None
        try:
            request = request or ApiRequest.from_mapping(raw_request)
            route = ROUTE_DEFINITIONS.get(request.interface_id)
            if route is None:
                return ApiResponse.rejected(request, ApiError("unregistered_interface", "interface is not registered"))
            parsed = self._parse(request)
            result = self._invoke(request.interface_id, parsed)
            return ApiResponse.success(request, result)
        except ModelValidationError as exc:
            if request is None:
                request = _safe_request(raw_request)
            return ApiResponse.rejected(request, ApiError(exc.code, exc.message, field=exc.field_name))
        except GovernancePolicyRuntimeServiceError as exc:
            assert request is not None
            return ApiResponse.rejected(request, ApiError(exc.failure_code, exc.public_message, details=exc.details))
        except Exception:
            assert request is not None
            return ApiResponse.failed(request, ApiError("internal_failure", "the policy operation failed"))

    def _parse(self, request: ApiRequest) -> object:
        parsers: Mapping[str, Parser] = {
            EVALUATE_DECISION: PolicyEvaluationRequest.from_payload,
            GET_POLICY_SET_STATUS: PolicySetStatusRequest.from_payload,
            STAGE_POLICY_BUNDLE: PolicyBundleStageRequest.from_payload,
            ACTIVATE_POLICY_SET: PolicySetActivationRequest.from_payload,
            ROLLBACK_POLICY_SET: PolicySetRollbackRequest.from_payload,
            GET_DECISION_RECEIPT: DecisionReceiptQuery.from_payload,
            HEALTH_AND_READINESS: HealthAndReadinessRequest.from_payload,
        }
        return parsers[request.interface_id](request.payload, request)

    def _invoke(self, interface_id: str, request: object) -> object:
        handlers: Mapping[str, Handler] = {
            EVALUATE_DECISION: self._service.evaluate_decision,
            GET_POLICY_SET_STATUS: self._service.get_policy_set_status,
            STAGE_POLICY_BUNDLE: self._service.stage_policy_bundle,
            ACTIVATE_POLICY_SET: self._service.activate_policy_set,
            ROLLBACK_POLICY_SET: self._service.rollback_policy_set,
            GET_DECISION_RECEIPT: self._service.get_decision_receipt,
            HEALTH_AND_READINESS: self._service.health_and_readiness,
        }
        return handlers[interface_id](request)


def create_api(service: GovernancePolicyRuntimeService) -> GovernancePolicyRuntimeApi:
    return GovernancePolicyRuntimeApi(service)


def _safe_request(raw: object) -> ApiRequest:
    if isinstance(raw, Mapping):
        interface_id = raw.get("interface_id")
        request_id = raw.get("request_id")
        correlation_id = raw.get("correlation_id")
        version = raw.get("version")
        if all(isinstance(item, str) for item in (interface_id, request_id, correlation_id, version)):
            try:
                return ApiRequest(interface_id, request_id, correlation_id, {}, version)
            except ModelValidationError:
                return ApiRequest("invalid_request", "POLREQ-INVALID-0001", "CORR-INVALID-0001", {}, API_VERSION)
    return ApiRequest("invalid_request", "POLREQ-INVALID-0001", "CORR-INVALID-0001", {}, API_VERSION)
