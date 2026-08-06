"""Transport-neutral route registry and dispatcher for the Audit Broker API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Final, Protocol, TypeAlias

from .models import (
    API_VERSION,
    ApiOutcome,
    ApiRequest,
    ApiResponse,
    AuditDisclosureRequest,
    AuditHealth,
    AuditHealthQuery,
    AuditRecordMetadata,
    AuditRecordMetadataQuery,
    AuditRequestStatus,
    AuditRequestStatusQuery,
    AuditEventSubmission,
    DisclosureResult,
    InvalidateAuditRecordRequest,
    InvalidationResult,
    ModelValidationError,
    PublicModel,
    RetentionActionRequest,
    RetentionResult,
    SubmissionResult,
)

SUBMIT_AUDIT_EVENT: Final = "submit_audit_event"
REQUEST_AUDIT_DISCLOSURE: Final = "request_audit_disclosure"
APPLY_RETENTION_ACTION: Final = "apply_retention_action"
INVALIDATE_AUDIT_RECORD: Final = "invalidate_audit_record"
GET_AUDIT_RECORD_METADATA: Final = "get_audit_record_metadata"
GET_AUDIT_REQUEST_STATUS: Final = "get_audit_request_status"
GET_AUDIT_HEALTH: Final = "get_audit_health"

INTERFACE_VERSIONS: Final[dict[str, str]] = {
    SUBMIT_AUDIT_EVENT: API_VERSION,
    REQUEST_AUDIT_DISCLOSURE: API_VERSION,
    APPLY_RETENTION_ACTION: API_VERSION,
    INVALIDATE_AUDIT_RECORD: API_VERSION,
    GET_AUDIT_RECORD_METADATA: API_VERSION,
    GET_AUDIT_REQUEST_STATUS: API_VERSION,
    GET_AUDIT_HEALTH: API_VERSION,
}


@dataclass(frozen=True, slots=True)
class RouteDefinition:
    interface_id: str
    version: str
    interaction: str
    mutation: bool
    authenticated: bool
    policy_decision_required: bool
    idempotency_required: bool
    default_result: str | None = None


ROUTE_DEFINITIONS: Final[tuple[RouteDefinition, ...]] = (
    RouteDefinition(
        interface_id=SUBMIT_AUDIT_EVENT,
        version=API_VERSION,
        interaction="command",
        mutation=True,
        authenticated=True,
        policy_decision_required=False,
        idempotency_required=True,
    ),
    RouteDefinition(
        interface_id=REQUEST_AUDIT_DISCLOSURE,
        version=API_VERSION,
        interaction="command",
        mutation=True,
        authenticated=True,
        policy_decision_required=True,
        idempotency_required=False,
    ),
    RouteDefinition(
        interface_id=APPLY_RETENTION_ACTION,
        version=API_VERSION,
        interaction="command",
        mutation=True,
        authenticated=True,
        policy_decision_required=True,
        idempotency_required=False,
    ),
    RouteDefinition(
        interface_id=INVALIDATE_AUDIT_RECORD,
        version=API_VERSION,
        interaction="command",
        mutation=True,
        authenticated=True,
        policy_decision_required=False,
        idempotency_required=False,
    ),
    RouteDefinition(
        interface_id=GET_AUDIT_RECORD_METADATA,
        version=API_VERSION,
        interaction="query",
        mutation=False,
        authenticated=True,
        policy_decision_required=False,
        idempotency_required=False,
        default_result="metadata_only",
    ),
    RouteDefinition(
        interface_id=GET_AUDIT_REQUEST_STATUS,
        version=API_VERSION,
        interaction="query",
        mutation=False,
        authenticated=True,
        policy_decision_required=False,
        idempotency_required=False,
        default_result="status_without_protected_content",
    ),
    RouteDefinition(
        interface_id=GET_AUDIT_HEALTH,
        version=API_VERSION,
        interaction="query",
        mutation=False,
        authenticated=True,
        policy_decision_required=False,
        idempotency_required=False,
        default_result="bounded_health_and_readiness",
    ),
)


class AuditBrokerService(Protocol):
    """Public application boundary consumed by the transport adapter."""

    submit_audit_event: Callable[[AuditEventSubmission], SubmissionResult]
    request_audit_disclosure: Callable[[AuditDisclosureRequest], DisclosureResult]
    apply_retention_action: Callable[[RetentionActionRequest], RetentionResult]
    invalidate_audit_record: Callable[[InvalidateAuditRecordRequest], InvalidationResult]
    get_audit_record_metadata: Callable[[AuditRecordMetadataQuery], AuditRecordMetadata]
    get_audit_request_status: Callable[[AuditRequestStatusQuery], AuditRequestStatus]
    get_audit_health: Callable[[AuditHealthQuery], AuditHealth]


class AuditBrokerServiceError(RuntimeError):
    """Sanitized application failure that can cross the API boundary."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        response_outcome: str = "failed",
    ) -> None:
        super().__init__(message)
        self.code = code
        self.public_message = message
        self.retryable = retryable
        self.response_outcome = response_outcome


class RequiredAuthorityUnavailable(AuditBrokerServiceError):
    def __init__(self, authority: str) -> None:
        super().__init__(
            "required_authority_unavailable",
            "A required authority is unavailable; the operation remains blocked.",
            retryable=True,
            response_outcome="rejected",
        )
        self.authority = authority


class AuditIntegrityFailure(AuditBrokerServiceError):
    def __init__(self) -> None:
        super().__init__(
            "integrity_failure",
            "Integrity verification failed; affected material remains quarantined.",
            retryable=False,
            response_outcome="quarantined",
        )


Handler: TypeAlias = Callable[[object], PublicModel]


class AuditBrokerApi:
    """Closed dispatcher for the component contract's seven public interfaces."""

    def __init__(self, service: AuditBrokerService) -> None:
        self._service = service
        self._handlers: dict[str, Handler] = {
            SUBMIT_AUDIT_EVENT: self._submit_audit_event,
            REQUEST_AUDIT_DISCLOSURE: self._request_audit_disclosure,
            APPLY_RETENTION_ACTION: self._apply_retention_action,
            INVALIDATE_AUDIT_RECORD: self._invalidate_audit_record,
            GET_AUDIT_RECORD_METADATA: self._get_audit_record_metadata,
            GET_AUDIT_REQUEST_STATUS: self._get_audit_request_status,
            GET_AUDIT_HEALTH: self._get_audit_health,
        }

    def dispatch(self, request: ApiRequest | object) -> ApiResponse:
        """Validate and execute one API operation without leaking protected payloads."""

        if not isinstance(request, ApiRequest):
            try:
                request = ApiRequest.from_mapping(request)
            except ModelValidationError as exc:
                synthetic = ApiRequest(
                    interface_id="invalid_request",
                    version=API_VERSION,
                    request_id="unresolved",
                    correlation_id="unresolved",
                    payload={},
                )
                return ApiResponse.failure(
                    synthetic,
                    outcome=ApiOutcome.REJECTED,
                    code=exc.code,
                    message=exc.message,
                    details={"field": exc.field_name},
                )

        expected_version = INTERFACE_VERSIONS.get(request.interface_id)
        if expected_version is None:
            return ApiResponse.failure(
                request,
                outcome=ApiOutcome.REJECTED,
                code="unregistered_interface",
                message="The requested Audit Broker interface is not registered.",
            )
        if request.version != expected_version:
            return ApiResponse.failure(
                request,
                outcome=ApiOutcome.REJECTED,
                code="unsupported_interface_version",
                message="The requested Audit Broker interface version is not supported.",
                details={"supported_version": expected_version},
            )

        try:
            result = self._handlers[request.interface_id](request.payload)
        except ModelValidationError as exc:
            return ApiResponse.failure(
                request,
                outcome=ApiOutcome.REJECTED,
                code=exc.code,
                message=exc.message,
                details={"field": exc.field_name},
            )
        except AuditBrokerServiceError as exc:
            api_outcome = (
                ApiOutcome.REJECTED
                if exc.response_outcome in {"rejected", "quarantined"}
                else ApiOutcome.FAILED
            )
            return ApiResponse.failure(
                request,
                outcome=api_outcome,
                code=exc.code,
                message=exc.public_message,
                retryable=exc.retryable,
                details={"service_outcome": exc.response_outcome},
            )
        except Exception:
            return ApiResponse.failure(
                request,
                outcome=ApiOutcome.FAILED,
                code="internal_failure",
                message=(
                    "The Audit Broker operation failed without a confirmed "
                    "authoritative result."
                ),
                retryable=False,
            )

        return ApiResponse.success(request, result)

    def _submit_audit_event(self, payload: object) -> SubmissionResult:
        return self._service.submit_audit_event(AuditEventSubmission.from_mapping(payload))

    def _request_audit_disclosure(self, payload: object) -> DisclosureResult:
        return self._service.request_audit_disclosure(
            AuditDisclosureRequest.from_mapping(payload)
        )

    def _apply_retention_action(self, payload: object) -> RetentionResult:
        return self._service.apply_retention_action(RetentionActionRequest.from_mapping(payload))

    def _invalidate_audit_record(self, payload: object) -> InvalidationResult:
        return self._service.invalidate_audit_record(
            InvalidateAuditRecordRequest.from_mapping(payload)
        )

    def _get_audit_record_metadata(self, payload: object) -> AuditRecordMetadata:
        return self._service.get_audit_record_metadata(
            AuditRecordMetadataQuery.from_mapping(payload)
        )

    def _get_audit_request_status(self, payload: object) -> AuditRequestStatus:
        return self._service.get_audit_request_status(
            AuditRequestStatusQuery.from_mapping(payload)
        )

    def _get_audit_health(self, payload: object) -> AuditHealth:
        return self._service.get_audit_health(AuditHealthQuery.from_mapping(payload))


def create_api(service: AuditBrokerService) -> AuditBrokerApi:
    """Create the transport-neutral public API around an application service."""

    return AuditBrokerApi(service)
