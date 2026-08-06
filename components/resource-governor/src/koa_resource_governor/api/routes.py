"""Framework-neutral HTTP-over-local-socket routing for Resource Governor."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol, runtime_checkable

from .models import (
    ApiBoundaryError,
    ApiResponse,
    CONTRACT_VERSION,
    EXPECTED_FAILURE_CODES,
    OPERATIONS_BY_PATH,
    RequestContext,
    operation_for_path,
    validate_request,
    validate_response,
)

CONTRACT_VERSION_HEADER = "x-koa-contract-version"
CORRELATION_HEADER = "x-koa-correlation-id"
CAUSATION_HEADER = "x-koa-causation-id"
IDEMPOTENCY_HEADER = "x-koa-idempotency-key"


class ComponentFailure(RuntimeError):
    """Declared Resource Governor failure preserving fail-closed behavior."""

    def __init__(self, reason_code: str, message: str, *, http_status: int = 503) -> None:
        if reason_code not in EXPECTED_FAILURE_CODES:
            raise ValueError(f"undeclared component failure code: {reason_code}")
        if not 400 <= http_status <= 599:
            raise ValueError("component failure HTTP status must be an error status")
        super().__init__(message)
        self.reason_code = reason_code
        self.public_message = message
        self.http_status = http_status


@runtime_checkable
class ResourceGovernorService(Protocol):
    """Public application port consumed by the transport boundary.

    Implementations belong to the application/bootstrap bundles.  This API never
    imports adapters, the Audit Broker implementation, a workload store, or a
    privileged host-control implementation.
    """

    def execute(
        self,
        operation_id: str,
        payload: Mapping[str, Any],
        context: RequestContext,
    ) -> Mapping[str, Any]: ...


@dataclass(frozen=True, slots=True)
class RouteDefinition:
    method: str
    path: str
    operation_id: str


@dataclass(frozen=True, slots=True)
class HttpResult:
    status_code: int
    body: Mapping[str, Any]
    headers: Mapping[str, str]


ROUTES = tuple(
    RouteDefinition(method="POST", path=path, operation_id=spec.operation_id)
    for path, spec in OPERATIONS_BY_PATH.items()
)


class ResourceGovernorRouter:
    """Strict dispatcher for a Unix-socket or equivalent local HTTP adapter."""

    def __init__(self, service: ResourceGovernorService) -> None:
        if not isinstance(service, ResourceGovernorService):
            raise TypeError("service must implement ResourceGovernorService")
        self._service = service

    def dispatch(
        self,
        method: str,
        path: str,
        body: Mapping[str, Any],
        headers: Mapping[str, str],
    ) -> HttpResult:
        normalized_headers = {str(key).lower(): str(value) for key, value in headers.items()}
        correlation_id = normalized_headers.get(CORRELATION_HEADER)
        operation_id: str | None = None
        try:
            spec = operation_for_path(path)
            operation_id = spec.operation_id
            if method.upper() != "POST":
                raise ApiBoundaryError("method_not_allowed", "declared operations accept POST only")
            context = self._build_context(normalized_headers)
            request_payload = validate_request(spec, body, context)
            raw_response = self._service.execute(spec.operation_id, request_payload, context)
            response_payload = validate_response(spec, raw_response)
            response = ApiResponse(
                operation_id=spec.operation_id,
                correlation_id=context.correlation_id,
                outcome="completed",
                payload=response_payload,
            )
            return self._result(200, response, context.correlation_id)
        except ComponentFailure as exc:
            response = ApiResponse(
                operation_id=operation_id,
                correlation_id=correlation_id,
                outcome="blocked" if exc.http_status in {409, 423, 429} else "failed",
                reason_code=exc.reason_code,
                message=exc.public_message,
            )
            return self._result(exc.http_status, response, correlation_id)
        except ApiBoundaryError as exc:
            response = ApiResponse(
                operation_id=operation_id,
                correlation_id=correlation_id,
                outcome="rejected",
                reason_code=exc.code,
                message=exc.message,
            )
            return self._result(_status_for_boundary_error(exc.code), response, correlation_id)
        except Exception:
            # Never reveal adapter, process, filesystem, policy, queue, or workload details.
            response = ApiResponse(
                operation_id=operation_id,
                correlation_id=correlation_id,
                outcome="failed",
                reason_code="component_runtime_unavailable",
                message="resource governance processing is unavailable",
            )
            return self._result(503, response, correlation_id)

    @staticmethod
    def _build_context(headers: Mapping[str, str]) -> RequestContext:
        return RequestContext(
            correlation_id=headers.get(CORRELATION_HEADER, ""),
            contract_version=headers.get(CONTRACT_VERSION_HEADER, ""),
            idempotency_key=headers.get(IDEMPOTENCY_HEADER),
            causation_id=headers.get(CAUSATION_HEADER),
        )

    @staticmethod
    def _result(status: int, response: ApiResponse, correlation_id: str | None) -> HttpResult:
        response_headers = {
            "content-type": "application/json",
            CONTRACT_VERSION_HEADER: CONTRACT_VERSION,
        }
        if correlation_id:
            response_headers[CORRELATION_HEADER] = correlation_id
        return HttpResult(status_code=status, body=response.to_dict(), headers=response_headers)


def build_router(service: ResourceGovernorService) -> ResourceGovernorRouter:
    return ResourceGovernorRouter(service)


def _status_for_boundary_error(code: str) -> int:
    if code == "operation_not_declared":
        return 404
    if code == "method_not_allowed":
        return 405
    if code == "response_contract_violation":
        return 502
    return 400
