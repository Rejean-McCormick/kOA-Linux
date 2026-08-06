"""Closed transport-neutral dispatcher for Publication Gateway."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol, runtime_checkable

from .models import (
    API_VERSION,
    ApiError,
    ApiRequest,
    ApiResponse,
    ControlledRetryRequest,
    ControlledRetryResult,
    HealthQuery,
    HealthResult,
    ModelValidationError,
    PublicationRequestCommand,
    PublicationRequestResult,
    PublicationStatus,
    PublicationStatusQuery,
    QueueInspectionQuery,
    QueueInspectionResult,
    RevocationOrWithdrawalNotice,
    WithdrawalResult,
)

PUBLICATION_REQUEST = "publication_request"
REVOCATION_OR_WITHDRAWAL_NOTICE = "revocation_or_withdrawal_notice"
PUBLICATION_STATUS_QUERY = "publication_status_query"
HEALTH = "health"
QUEUE_INSPECTION = "queue_inspection"
CONTROLLED_RETRY = "controlled_retry"


@dataclass(frozen=True, slots=True)
class RouteDefinition:
    interface_id: str
    interaction: str
    authentication_required: bool
    selective_disclosure_required: bool
    request_model: str
    result_model: str


ROUTE_DEFINITIONS: Mapping[str, RouteDefinition] = MappingProxyType(
    {
        PUBLICATION_REQUEST: RouteDefinition(PUBLICATION_REQUEST, "command", True, False, "PublicationRequestCommand", "PublicationRequestResult"),
        REVOCATION_OR_WITHDRAWAL_NOTICE: RouteDefinition(REVOCATION_OR_WITHDRAWAL_NOTICE, "command", True, False, "RevocationOrWithdrawalNotice", "WithdrawalResult"),
        PUBLICATION_STATUS_QUERY: RouteDefinition(PUBLICATION_STATUS_QUERY, "query", True, True, "PublicationStatusQuery", "PublicationStatus"),
        HEALTH: RouteDefinition(HEALTH, "query", True, True, "HealthQuery", "HealthResult"),
        QUEUE_INSPECTION: RouteDefinition(QUEUE_INSPECTION, "query", True, True, "QueueInspectionQuery", "QueueInspectionResult"),
        CONTROLLED_RETRY: RouteDefinition(CONTROLLED_RETRY, "command", True, False, "ControlledRetryRequest", "ControlledRetryResult"),
    }
)
INTERFACE_VERSIONS: Mapping[str, str] = MappingProxyType({name: API_VERSION for name in ROUTE_DEFINITIONS})


@runtime_checkable
class PublicationGatewayService(Protocol):
    """Public application boundary supplied by the preceding bundles."""

    def publication_request(self, request: PublicationRequestCommand) -> PublicationRequestResult: ...
    def revocation_or_withdrawal_notice(self, request: RevocationOrWithdrawalNotice) -> WithdrawalResult: ...
    def publication_status_query(self, request: PublicationStatusQuery) -> PublicationStatus: ...
    def health(self, request: HealthQuery) -> HealthResult: ...
    def queue_inspection(self, request: QueueInspectionQuery) -> QueueInspectionResult: ...
    def controlled_retry(self, request: ControlledRetryRequest) -> ControlledRetryResult: ...


class PublicationGatewayServiceError(RuntimeError):
    failure_code = "publication_blocked"
    public_message = "the publication operation was blocked"
    details: Mapping[str, str] = MappingProxyType({})

    def __init__(self, *, details: Mapping[str, str] | None = None) -> None:
        super().__init__(self.public_message)
        if details:
            self.details = MappingProxyType(dict(details))


class IdentityUnavailable(PublicationGatewayServiceError):
    failure_code = "identity_unavailable"
    public_message = "required identity or trust authority is unavailable"


class PolicyUnavailable(PublicationGatewayServiceError):
    failure_code = "policy_unavailable"
    public_message = "required governance authority is unavailable"


class ConsentUnavailable(PublicationGatewayServiceError):
    failure_code = "consent_unavailable"
    public_message = "required consent authority is unavailable"


class CulturalAuthorityDisputed(PublicationGatewayServiceError):
    failure_code = "cultural_authority_disputed"
    public_message = "competent human review is required"


class DestinationUnavailable(PublicationGatewayServiceError):
    failure_code = "destination_unavailable"
    public_message = "the declared destination is unavailable"


class DestinationIncompatible(PublicationGatewayServiceError):
    failure_code = "destination_incompatible"
    public_message = "the declared destination contract is incompatible"


class ResourceUnavailable(PublicationGatewayServiceError):
    failure_code = "resource_unavailable"
    public_message = "bounded publication resources are unavailable"


class AuditUnavailable(PublicationGatewayServiceError):
    failure_code = "audit_unavailable"
    public_message = "required audit evidence intake is unavailable"


class ReceiptPersistenceFailed(PublicationGatewayServiceError):
    failure_code = "receipt_persistence_failed"
    public_message = "publication success cannot be reported because receipt evidence is unavailable"


class RevalidationFailed(PublicationGatewayServiceError):
    failure_code = "revalidation_failed"
    public_message = "the publication request failed required revalidation"


class StatusScopeDenied(PublicationGatewayServiceError):
    failure_code = "status_scope_denied"
    public_message = "the requested publication status scope is not authorized"


class QueueScopeDenied(PublicationGatewayServiceError):
    failure_code = "queue_scope_denied"
    public_message = "the requested queue scope is not authorized"


Parser = Callable[[Mapping[str, Any], ApiRequest], object]
Handler = Callable[[object], object]


class PublicationGatewayApi:
    """Closed dispatcher that delegates authority and side effects to a public port."""

    def __init__(self, service: PublicationGatewayService) -> None:
        self._service = service

    def dispatch(self, raw_request: ApiRequest | Mapping[str, Any]) -> ApiResponse:
        request: ApiRequest | None = raw_request if isinstance(raw_request, ApiRequest) else None
        try:
            request = request or ApiRequest.from_mapping(raw_request)
            if request.interface_id not in ROUTE_DEFINITIONS:
                return ApiResponse.rejected(request, ApiError("unregistered_interface", "interface is not registered"))
            parsed = self._parse(request)
            result = self._invoke(request.interface_id, parsed)
            return ApiResponse.success(request, result)
        except ModelValidationError as exc:
            request = request or _safe_request(raw_request)
            return ApiResponse.rejected(request, ApiError(exc.code, exc.message, field=exc.field_name))
        except PublicationGatewayServiceError as exc:
            assert request is not None
            return ApiResponse.rejected(request, ApiError(exc.failure_code, exc.public_message, details=exc.details))
        except Exception:
            assert request is not None
            return ApiResponse.failed(request, ApiError("internal_failure", "the publication operation failed"))

    def _parse(self, request: ApiRequest) -> object:
        parsers: Mapping[str, Parser] = {
            PUBLICATION_REQUEST: PublicationRequestCommand.from_payload,
            REVOCATION_OR_WITHDRAWAL_NOTICE: RevocationOrWithdrawalNotice.from_payload,
            PUBLICATION_STATUS_QUERY: PublicationStatusQuery.from_payload,
            HEALTH: HealthQuery.from_payload,
            QUEUE_INSPECTION: QueueInspectionQuery.from_payload,
            CONTROLLED_RETRY: ControlledRetryRequest.from_payload,
        }
        return parsers[request.interface_id](request.payload, request)

    def _invoke(self, interface_id: str, request: object) -> object:
        handlers: Mapping[str, Handler] = {
            PUBLICATION_REQUEST: self._service.publication_request,
            REVOCATION_OR_WITHDRAWAL_NOTICE: self._service.revocation_or_withdrawal_notice,
            PUBLICATION_STATUS_QUERY: self._service.publication_status_query,
            HEALTH: self._service.health,
            QUEUE_INSPECTION: self._service.queue_inspection,
            CONTROLLED_RETRY: self._service.controlled_retry,
        }
        result_types: Mapping[str, type[object]] = {
            PUBLICATION_REQUEST: PublicationRequestResult,
            REVOCATION_OR_WITHDRAWAL_NOTICE: WithdrawalResult,
            PUBLICATION_STATUS_QUERY: PublicationStatus,
            HEALTH: HealthResult,
            QUEUE_INSPECTION: QueueInspectionResult,
            CONTROLLED_RETRY: ControlledRetryResult,
        }
        result = handlers[interface_id](request)
        if not isinstance(result, result_types[interface_id]):
            raise ModelValidationError(
                "service_result",
                "invalid_service_result",
                "service result must be a registered public model",
            )
        return result


def create_api(service: PublicationGatewayService) -> PublicationGatewayApi:
    return PublicationGatewayApi(service)


def _safe_request(raw: object) -> ApiRequest:
    if isinstance(raw, Mapping):
        try:
            return ApiRequest(
                str(raw.get("interface_id") or "invalid_request"),
                str(raw.get("request_id") or "invalid-request"),
                str(raw.get("correlation_id") or "invalid-correlation"),
                {},
                API_VERSION,
            )
        except ModelValidationError:
            return ApiRequest("invalid_request", "invalid-request", "invalid-correlation", {}, API_VERSION)
    return ApiRequest("invalid_request", "invalid-request", "invalid-correlation", {}, API_VERSION)
