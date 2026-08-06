"""Framework-neutral local router for the kOA Mediatheque public API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .models import (
    API_VERSION,
    CONTRACT_VERSION,
    ApiBoundaryError,
    ApiRequest,
    ApiResponse,
    OperationKind,
    OperationSpec,
    OPERATIONS_BY_PATH,
    RequestContext,
    request_context,
    validate_request,
    validate_response,
)


class MediathequeService(Protocol):
    """Public application port implemented by the application bundle."""

    def execute(
        self,
        operation_id: str,
        payload: Mapping[str, Any],
        context: RequestContext,
    ) -> Mapping[str, Any]:
        raise NotImplementedError("public service port")


@dataclass(frozen=True, slots=True)
class Route:
    method: str
    path: str
    operation_id: str


ROUTES = tuple(
    Route("POST" if spec.kind is OperationKind.COMMAND else "GET", spec.path, spec.operation_id)
    for spec in OPERATIONS_BY_PATH.values()
)


class Router:
    def __init__(self, service: MediathequeService) -> None:
        self._service = service

    def dispatch(self, request: ApiRequest) -> ApiResponse:
        correlation = request.headers.get("x-koa-correlation-id") or request.headers.get("X-KOA-Correlation-ID") or "unavailable"
        try:
            spec = self._resolve(request.method, request.path)
            context = request_context(spec, request.headers)
            payload = validate_request(spec, request.body)
            raw = self._service.execute(spec.operation_id, payload, context)
            body = validate_response(spec, raw)
            return ApiResponse(
                200,
                {
                    "content-type": "application/json",
                    "x-koa-contract-version": CONTRACT_VERSION,
                    "x-koa-correlation-id": context.correlation_id,
                },
                body,
            )
        except ApiBoundaryError as error:
            return self._error_response(error, correlation)
        except Exception:
            return self._error_response(
                ApiBoundaryError("service_unavailable", "Mediatheque operation failed closed"),
                correlation,
            )

    @staticmethod
    def _resolve(method: str, path: str) -> OperationSpec:
        spec = OPERATIONS_BY_PATH.get(path)
        if spec is None:
            raise ApiBoundaryError("operation_not_declared", "operation is not declared")
        expected = "POST" if spec.kind is OperationKind.COMMAND else "GET"
        if method.upper() != expected:
            raise ApiBoundaryError("method_not_allowed", "method is not allowed")
        return spec

    @staticmethod
    def _error_response(error: ApiBoundaryError, correlation_id: str) -> ApiResponse:
        status = {
            "operation_not_declared": 404,
            "method_not_allowed": 405,
            "service_unavailable": 503,
            "restricted_content_disclosure": 502,
            "response_contract_violation": 502,
        }.get(error.code, 400)
        return ApiResponse(
            status,
            {
                "content-type": "application/json",
                "x-koa-contract-version": CONTRACT_VERSION,
                "x-koa-correlation-id": correlation_id,
            },
            {
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "component": "koa_mediatheque",
                    "api_version": API_VERSION,
                }
            },
        )


def build_router(service: MediathequeService) -> Router:
    return Router(service)
