"""Strict public transport models for the kOA Mediatheque.

The module projects the canonical component contract without owning storage,
policy, identity, resource admission, publication transport, or UCKK state.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

COMPONENT_ID = "koa_mediatheque"
CONTRACT_VERSION = "1.0.0"
API_VERSION = "v1"
SHARED_FRAME_ID = "koa-uckk-shared-mediatheque-frame"


class OperationKind(StrEnum):
    COMMAND = "command"
    QUERY = "query"


class ApiBoundaryError(ValueError):
    """Stable fail-closed error suitable for a public error envelope."""

    _ALLOWED_CODES = frozenset(
        {
            "request_contract_violation",
            "response_contract_violation",
            "operation_not_declared",
            "method_not_allowed",
            "missing_correlation_context",
            "missing_identity_context",
            "missing_authorization_context",
            "missing_disclosure_context",
            "missing_idempotency_key",
            "invalid_shared_frame",
            "restricted_content_disclosure",
            "service_unavailable",
        }
    )

    def __init__(self, code: str, message: str) -> None:
        if code not in self._ALLOWED_CODES:
            raise ValueError(f"undeclared API boundary code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class OperationSpec:
    operation_id: str
    interface_id: str
    kind: OperationKind
    request_fields: tuple[str, ...]
    response_fields: tuple[str, ...]
    authentication_required: bool = True
    authorization_required: bool = True
    idempotency_required: bool = False
    selective_disclosure: bool = False
    quarantine_required: bool = False

    @property
    def path(self) -> str:
        collection = "commands" if self.kind is OperationKind.COMMAND else "queries"
        return f"/{API_VERSION}/{collection}/{self.operation_id}"


_COMMAND_RESULT = ("request_id", "outcome", "receipt_ref")
_RECORD_RESULT = ("request_id", "outcome", "record_id", "version_id", "receipt_ref")
_IMPORT_RESULT = ("request_id", "outcome", "import_id", "quarantine_ref", "receipt_ref")
_PACKAGE_RESULT = ("request_id", "outcome", "package_id", "receipt_ref")

_OPERATION_SPECS = (
    OperationSpec("create_record", "media_record_command", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "media_record"), _RECORD_RESULT,
                  idempotency_required=True),
    OperationSpec("add_version", "media_record_command", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "content", "integrity", "provenance"), _RECORD_RESULT,
                  idempotency_required=True),
    OperationSpec("update_metadata", "media_record_command", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "metadata_patch"), _RECORD_RESULT,
                  idempotency_required=True),
    OperationSpec("classify", "media_record_command", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "classification"), _RECORD_RESULT,
                  idempotency_required=True),
    OperationSpec("apply_rights", "media_record_command", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "rights"), _RECORD_RESULT,
                  idempotency_required=True),
    OperationSpec("transition_lifecycle", "media_record_command", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "record_state", "version_state"), _RECORD_RESULT,
                  idempotency_required=True),
    OperationSpec("stage_import", "media_import", OperationKind.COMMAND,
                  ("request_id", "source_ref", "shared_frame", "content_ref"), _IMPORT_RESULT,
                  quarantine_required=True),
    OperationSpec("verify_import", "media_import", OperationKind.COMMAND,
                  ("request_id", "import_id", "evidence_refs"),
                  ("request_id", "outcome", "import_id", "verification_state", "receipt_ref"),
                  quarantine_required=True),
    OperationSpec("accept_import", "media_import", OperationKind.COMMAND,
                  ("request_id", "import_id", "record_id", "version_id"), _RECORD_RESULT,
                  quarantine_required=True),
    OperationSpec("reject_import", "media_import", OperationKind.COMMAND,
                  ("request_id", "import_id", "reason_code"), _COMMAND_RESULT,
                  quarantine_required=True),
    OperationSpec("publication_result", "publication_result", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "publication_receipt"),
                  ("request_id", "outcome", "receipt_ref", "local_source_authority"),
                  idempotency_required=True),
    OperationSpec("stage_uckk_package", "uckk_learning_package_acceptance", OperationKind.COMMAND,
                  ("request_id", "package_id", "source_ref", "package_ref", "shared_frame"), _PACKAGE_RESULT,
                  idempotency_required=True, quarantine_required=True),
    OperationSpec("validate_uckk_package", "uckk_learning_package_acceptance", OperationKind.COMMAND,
                  ("request_id", "package_id", "evidence_refs"),
                  ("request_id", "outcome", "package_id", "validation_state", "receipt_ref"),
                  idempotency_required=True, quarantine_required=True),
    OperationSpec("accept_uckk_package", "uckk_learning_package_acceptance", OperationKind.COMMAND,
                  ("request_id", "package_id", "record_id", "version_id"), _RECORD_RESULT,
                  idempotency_required=True, quarantine_required=True),
    OperationSpec("reject_uckk_package", "uckk_learning_package_acceptance", OperationKind.COMMAND,
                  ("request_id", "package_id", "reason_code"), _PACKAGE_RESULT,
                  idempotency_required=True, quarantine_required=True),
    OperationSpec("record_update_candidate", "uckk_learning_package_acceptance", OperationKind.COMMAND,
                  ("request_id", "package_id", "record_id", "source_version_ref"), _PACKAGE_RESULT,
                  idempotency_required=True, quarantine_required=True),
    OperationSpec("media_record_query", "media_record_query", OperationKind.QUERY,
                  ("record_id", "version_id", "view"), ("record",),
                  idempotency_required=False, selective_disclosure=True),
    OperationSpec("publication_candidate", "publication_candidate", OperationKind.COMMAND,
                  ("request_id", "record_id", "version_id", "destination_ref", "authorization_ref"),
                  ("request_id", "outcome", "package_ref", "authorization_required", "receipt_ref"),
                  idempotency_required=True),
    OperationSpec("backup_export", "backup_export", OperationKind.COMMAND,
                  ("request_id", "checkpoint_ref", "disclosure_policy_ref"),
                  ("request_id", "outcome", "backup_ref", "manifest_ref", "verification_state", "receipt_ref"),
                  idempotency_required=True),
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
    identity_ref: str | None
    authorization_ref: str | None
    disclosure_policy_ref: str | None
    idempotency_key: str | None
    contract_version: str


@dataclass(frozen=True, slots=True)
class ApiRequest:
    method: str
    path: str
    headers: Mapping[str, str]
    body: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class ApiResponse:
    status: int
    headers: Mapping[str, str]
    body: Mapping[str, Any]


_PROTECTED_RESPONSE_KEYS = frozenset(
    {
        "content_bytes",
        "raw_content",
        "media_payload",
        "secret",
        "password",
        "credential",
        "private_key",
        "private_key_material",
        "access_token",
        "refresh_token",
    }
)


def normalize_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {str(key).lower(): str(value).strip() for key, value in headers.items()}


def request_context(spec: OperationSpec, headers: Mapping[str, str]) -> RequestContext:
    normalized = normalize_headers(headers)
    version = normalized.get("x-koa-contract-version", "")
    if version != CONTRACT_VERSION:
        raise ApiBoundaryError("request_contract_violation", "unsupported contract version")
    correlation = normalized.get("x-koa-correlation-id", "")
    if not correlation:
        raise ApiBoundaryError("missing_correlation_context", "correlation context is required")
    identity = normalized.get("x-koa-identity-ref")
    authorization = normalized.get("x-koa-authorization-ref")
    disclosure = normalized.get("x-koa-disclosure-policy-ref")
    idempotency = normalized.get("x-koa-idempotency-key")
    if spec.authentication_required and not identity:
        raise ApiBoundaryError("missing_identity_context", "identity context is required")
    if spec.authorization_required and not authorization:
        raise ApiBoundaryError("missing_authorization_context", "authorization context is required")
    if spec.selective_disclosure and not disclosure:
        raise ApiBoundaryError("missing_disclosure_context", "disclosure context is required")
    if spec.idempotency_required and not idempotency:
        raise ApiBoundaryError("missing_idempotency_key", "idempotency key is required")
    return RequestContext(correlation, identity, authorization, disclosure, idempotency, version)


def validate_request(spec: OperationSpec, body: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(body, Mapping):
        raise ApiBoundaryError("request_contract_violation", "request body must be an object")
    missing = [field for field in spec.request_fields if field not in body]
    if missing:
        raise ApiBoundaryError("request_contract_violation", "required request fields are missing")
    unknown = sorted(set(body) - set(spec.request_fields))
    if unknown:
        raise ApiBoundaryError("request_contract_violation", "undeclared request fields are prohibited")
    payload = {field: body[field] for field in spec.request_fields}
    if "shared_frame" in payload:
        frame = payload["shared_frame"]
        if not isinstance(frame, Mapping) or frame.get("frame_id") != SHARED_FRAME_ID:
            raise ApiBoundaryError("invalid_shared_frame", "shared Mediatheque frame is invalid")
    return payload


def _scan_protected(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if str(key).lower() in _PROTECTED_RESPONSE_KEYS:
                raise ApiBoundaryError("restricted_content_disclosure", "restricted content was blocked")
            _scan_protected(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            _scan_protected(nested)


def validate_response(spec: OperationSpec, body: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(body, Mapping):
        raise ApiBoundaryError("response_contract_violation", "service response must be an object")
    missing = [field for field in spec.response_fields if field not in body]
    if missing:
        raise ApiBoundaryError("response_contract_violation", "service response is incomplete")
    unknown = sorted(set(body) - set(spec.response_fields))
    if unknown:
        raise ApiBoundaryError("response_contract_violation", "service response contains undeclared fields")
    result = {field: body[field] for field in spec.response_fields}
    _scan_protected(result)
    if spec.operation_id == "publication_result" and result["local_source_authority"] != "retained":
        raise ApiBoundaryError("response_contract_violation", "local source authority must be retained")
    if spec.operation_id == "publication_candidate" and result["authorization_required"] is not True:
        raise ApiBoundaryError("response_contract_violation", "publication authorization cannot be bypassed")
    return result
