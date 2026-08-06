"""Closed, transport-neutral dispatch boundary for Kristal Runtime."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol, runtime_checkable

from .models import (
    API_VERSION,
    ApiError,
    ApiRequest,
    ApiResponse,
    KristalIdentityResolutionRequest,
    KristalIdentityResolutionResponse,
    ModelValidationError,
    RuntimePackActivationRequest,
    RuntimePackRollbackRequest,
    RuntimePackTransitionResult,
    RuntimePackValidationRequest,
    RuntimePackVerificationResult,
    RuntimeStatusRequest,
    RuntimeStatusResponse,
)

KRISTAL_IDENTITY_RESOLUTION = "kristal_identity_resolution"
RUNTIME_PACK_VALIDATION = "runtime_pack_validation"
RUNTIME_PACK_ACTIVATION = "runtime_pack_activation"
RUNTIME_PACK_ROLLBACK = "runtime_pack_rollback"
RUNTIME_STATUS_QUERY = "runtime_status_query"


@dataclass(frozen=True, slots=True)
class RouteDefinition:
    interface_id: str
    interaction: str
    authoritative_effect: str
    request_type: str
    response_type: str


ROUTE_DEFINITIONS: Mapping[str, RouteDefinition] = MappingProxyType(
    {
        KRISTAL_IDENTITY_RESOLUTION: RouteDefinition(
            KRISTAL_IDENTITY_RESOLUTION,
            "query",
            "none",
            "kristal_identity_resolution_request",
            "kristal_identity_resolution_response",
        ),
        RUNTIME_PACK_VALIDATION: RouteDefinition(
            RUNTIME_PACK_VALIDATION,
            "command",
            "runtime_pack_verification_record",
            "runtime_pack_validation_request",
            "runtime_pack_verification_result",
        ),
        RUNTIME_PACK_ACTIVATION: RouteDefinition(
            RUNTIME_PACK_ACTIVATION,
            "command",
            "active_runtime_pack_record",
            "runtime_pack_activation_request",
            "runtime_pack_transition_result",
        ),
        RUNTIME_PACK_ROLLBACK: RouteDefinition(
            RUNTIME_PACK_ROLLBACK,
            "command",
            "active_runtime_pack_record",
            "runtime_pack_rollback_request",
            "runtime_pack_transition_result",
        ),
        RUNTIME_STATUS_QUERY: RouteDefinition(
            RUNTIME_STATUS_QUERY,
            "query",
            "none",
            "runtime_status_request",
            "runtime_status_response",
        ),
    }
)
INTERFACE_VERSIONS: Mapping[str, str] = MappingProxyType({name: API_VERSION for name in ROUTE_DEFINITIONS})


@runtime_checkable
class KristalRuntimeService(Protocol):
    """Public application boundary supplied by preceding Kristal bundles."""

    def resolve_kristal_identity(self, request: KristalIdentityResolutionRequest) -> KristalIdentityResolutionResponse: ...
    def validate_runtime_pack(self, request: RuntimePackValidationRequest) -> RuntimePackVerificationResult: ...
    def activate_runtime_pack(self, request: RuntimePackActivationRequest) -> RuntimePackTransitionResult: ...
    def rollback_runtime_pack(self, request: RuntimePackRollbackRequest) -> RuntimePackTransitionResult: ...
    def query_runtime_status(self, request: RuntimeStatusRequest) -> RuntimeStatusResponse: ...


class KristalRuntimeServiceError(RuntimeError):
    """Known fail-closed service error safe to expose at the API boundary."""

    failure_code = "kristal_operation_blocked"
    public_message = "the Kristal Runtime operation was blocked"
    details: Mapping[str, str] = MappingProxyType({})

    def __init__(self, *, details: Mapping[str, str] | None = None) -> None:
        super().__init__(self.public_message)
        if details:
            self.details = MappingProxyType(dict(details))


class CanonicalContentUnavailable(KristalRuntimeServiceError):
    failure_code = "canonical_content_unavailable"
    public_message = "canonical epistemic content is unavailable"


class ContentDigestInvalid(KristalRuntimeServiceError):
    failure_code = "content_digest_invalid"
    public_message = "content integrity validation failed"


class ArtifactInvalid(KristalRuntimeServiceError):
    failure_code = "artifact_invalid"
    public_message = "the Runtime Pack is invalid"


class ArtifactUntrusted(KristalRuntimeServiceError):
    failure_code = "artifact_untrusted"
    public_message = "required artifact trust could not be established"


class ArtifactIncompatible(KristalRuntimeServiceError):
    failure_code = "artifact_incompatible"
    public_message = "the Runtime Pack is incompatible"


class ReleaseChannelInvalid(KristalRuntimeServiceError):
    failure_code = "release_channel_invalid"
    public_message = "the Runtime Pack is not in the knowledge release channel"


class DowngradeOrSubstitutionDenied(KristalRuntimeServiceError):
    failure_code = "downgrade_or_substitution_denied"
    public_message = "the requested Runtime Pack replacement is not authorized"


class VerificationMissing(KristalRuntimeServiceError):
    failure_code = "verification_missing"
    public_message = "a verified Runtime Pack record is required"


class AuthorizationUnavailable(KristalRuntimeServiceError):
    failure_code = "authorization_unavailable"
    public_message = "required governance authorization is unavailable"


class ResourceGrantUnavailable(KristalRuntimeServiceError):
    failure_code = "resource_grant_unavailable"
    public_message = "required resource admission is unavailable"


class AtomicActivationFailed(KristalRuntimeServiceError):
    failure_code = "activation_failed"
    public_message = "the Runtime Pack was not activated"


class RollbackTargetUnavailable(KristalRuntimeServiceError):
    failure_code = "rollback_target_unavailable"
    public_message = "the declared last valid Runtime Pack is unavailable"


class RollbackBlocked(KristalRuntimeServiceError):
    failure_code = "rollback_blocked"
    public_message = "Runtime Pack rollback is blocked"


class ForwardRepairRequired(KristalRuntimeServiceError):
    failure_code = "forward_repair_required"
    public_message = "forward repair is required"


class RuntimeStateUnavailable(KristalRuntimeServiceError):
    failure_code = "runtime_state_unavailable"
    public_message = "Kristal Runtime state is unavailable"


class StatusScopeDenied(KristalRuntimeServiceError):
    failure_code = "status_scope_denied"
    public_message = "the requested status scope is not authorized"


class EvidenceUnavailable(KristalRuntimeServiceError):
    failure_code = "evidence_unavailable"
    public_message = "required transition evidence is unavailable"


Parser = Callable[[Mapping[str, Any], ApiRequest], object]
Handler = Callable[[object], object]


class KristalRuntimeApi:
    """Closed dispatcher delegating all authority to a public service protocol."""

    def __init__(self, service: KristalRuntimeService) -> None:
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
        except KristalRuntimeServiceError as exc:
            assert request is not None
            return ApiResponse.rejected(request, ApiError(exc.failure_code, exc.public_message, details=exc.details))
        except Exception:
            request = request or _safe_request(raw_request)
            return ApiResponse.failed(request, ApiError("internal_failure", "the Kristal Runtime operation failed"))

    def _parse(self, request: ApiRequest) -> object:
        parsers: Mapping[str, Parser] = {
            KRISTAL_IDENTITY_RESOLUTION: KristalIdentityResolutionRequest.from_payload,
            RUNTIME_PACK_VALIDATION: RuntimePackValidationRequest.from_payload,
            RUNTIME_PACK_ACTIVATION: RuntimePackActivationRequest.from_payload,
            RUNTIME_PACK_ROLLBACK: RuntimePackRollbackRequest.from_payload,
            RUNTIME_STATUS_QUERY: RuntimeStatusRequest.from_payload,
        }
        return parsers[request.interface_id](request.payload, request)

    def _invoke(self, interface_id: str, request: object) -> object:
        handlers: Mapping[str, tuple[Handler, type[object]]] = {
            KRISTAL_IDENTITY_RESOLUTION: (self._service.resolve_kristal_identity, KristalIdentityResolutionResponse),
            RUNTIME_PACK_VALIDATION: (self._service.validate_runtime_pack, RuntimePackVerificationResult),
            RUNTIME_PACK_ACTIVATION: (self._service.activate_runtime_pack, RuntimePackTransitionResult),
            RUNTIME_PACK_ROLLBACK: (self._service.rollback_runtime_pack, RuntimePackTransitionResult),
            RUNTIME_STATUS_QUERY: (self._service.query_runtime_status, RuntimeStatusResponse),
        }
        handler, expected_type = handlers[interface_id]
        result = handler(request)
        if not isinstance(result, expected_type):
            raise ModelValidationError("result", "invalid_service_result", "service returned the wrong public result type")
        return result


def create_api(service: KristalRuntimeService) -> KristalRuntimeApi:
    return KristalRuntimeApi(service)


def _safe_request(raw: object) -> ApiRequest:
    if isinstance(raw, Mapping):
        values = [raw.get(name) for name in ("interface_id", "request_id", "correlation_id", "version")]
        if all(isinstance(value, str) for value in values):
            try:
                return ApiRequest(values[0], values[1], values[2], {}, values[3])
            except ModelValidationError:
                return ApiRequest(
                    "invalid_request",
                    "request.invalid",
                    "correlation.invalid",
                    {},
                    API_VERSION,
                )
    return ApiRequest("invalid_request", "request.invalid", "correlation.invalid", {}, API_VERSION)
