"""Public transport models for the Identity and Trust component.

The module deliberately contains no storage, policy, authorization, or key-material
logic.  It mirrors the observable command and query surface owned by the canonical
component contract and provides strict boundary validation for a transport adapter.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

COMPONENT_ID = "identity_and_trust"
CONTRACT_VERSION = "1.0.0"
API_VERSION = "v1"


class OperationKind(StrEnum):
    COMMAND = "command"
    QUERY = "query"


class IdentityResult(StrEnum):
    ESTABLISHED = "established"
    NOT_ESTABLISHED = "not_established"
    INDETERMINATE = "indeterminate"


class TrustResult(StrEnum):
    TRUSTED = "trusted"
    UNTRUSTED = "untrusted"
    INDETERMINATE = "indeterminate"


EXPECTED_FAILURE_CODES = frozenset(
    {
        "identity_not_established",
        "identity_result_indeterminate",
        "credential_expired",
        "credential_revoked",
        "trust_scope_mismatch",
        "trust_root_unavailable",
        "revocation_state_stale",
        "signature_invalid",
        "algorithm_or_version_unsupported",
        "private_key_provider_unavailable",
        "offline_trust_update_invalid",
        "identity_store_restore_partial",
        "receipt_path_unavailable",
        "cross_component_identity_write_attempt",
        "authentication_authorization_boundary_violation",
        "trust_root_scope_undefined",
        "private_material_disclosure_detected",
        "component_conformance_evidence_incomplete",
    }
)

TRANSPORT_FAILURE_CODES = frozenset(
    {
        "request_contract_violation",
        "response_contract_violation",
        "operation_not_declared",
        "method_not_allowed",
        "missing_correlation_context",
        "missing_idempotency_key",
    }
)

# These keys may never cross an ordinary public response boundary.  The check is
# recursive and case-insensitive; references such as ``key_or_material_reference``
# remain permitted because they do not contain the protected material itself.
_PROTECTED_RESPONSE_KEYS = frozenset(
    {
        "private_key",
        "private_key_material",
        "secret",
        "secret_material",
        "password",
        "password_verifier",
        "authentication_factor_values",
        "credential_secret",
        "raw_credential",
        "recovery_code",
        "protected_evidence_payload",
    }
)


class ApiBoundaryError(ValueError):
    """A stable, non-secret boundary error suitable for a public error envelope."""

    def __init__(self, code: str, message: str, *, field: str | None = None) -> None:
        allowed = EXPECTED_FAILURE_CODES | TRANSPORT_FAILURE_CODES
        if code not in allowed:
            raise ValueError(f"undeclared API boundary code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message
        self.field = field


@dataclass(frozen=True, slots=True)
class OperationSpec:
    operation_id: str
    kind: OperationKind
    request_fields: tuple[str, ...]
    response_fields: tuple[str, ...]
    idempotency: str | None = None
    critical_transition: bool = False
    selective_disclosure: bool = False

    @property
    def path(self) -> str:
        collection = "commands" if self.kind is OperationKind.COMMAND else "queries"
        return f"/{API_VERSION}/{collection}/{self.operation_id}"

    @property
    def requires_idempotency_key(self) -> bool:
        return self.idempotency == "idempotency_key_required"


_OPERATION_SPECS = (
    OperationSpec(
        "authenticate_subject",
        OperationKind.COMMAND,
        ("request_id", "subject_hint", "authentication_context", "presented_factors", "tenant_ref", "environment", "profile_ref"),
        ("request_id", "identity_result", "identity_ref", "assurance_context", "expires_at", "reason_code", "receipt_ref"),
        idempotency="request_scoped",
    ),
    OperationSpec(
        "authenticate_service",
        OperationKind.COMMAND,
        ("request_id", "presented_credential", "expected_subject_type", "tenant_ref", "environment", "intended_use"),
        ("request_id", "identity_result", "identity_ref", "validated_scope", "expires_at", "reason_code", "receipt_ref"),
        idempotency="request_scoped",
    ),
    OperationSpec(
        "validate_credential",
        OperationKind.COMMAND,
        ("request_id", "credential", "intended_use", "tenant_ref", "environment"),
        ("request_id", "trust_result", "identity_ref", "validated_scope", "reason_code", "verification_ref"),
        idempotency="deterministic_for_fixed_inputs_and_trust_state",
    ),
    OperationSpec(
        "verify_signature",
        OperationKind.COMMAND,
        ("request_id", "signed_object_ref", "signature", "intended_use", "tenant_ref", "environment", "release_channel", "artifact_class"),
        ("request_id", "trust_result", "signer_identity_ref", "trust_root_ref", "validated_scope", "reason_code", "verification_ref"),
        idempotency="deterministic_for_fixed_inputs_and_trust_state",
    ),
    OperationSpec(
        "issue_credential",
        OperationKind.COMMAND,
        ("request_id", "subject_identity_ref", "credential_type", "scope", "validity", "issuer_authority_ref", "evidence_refs"),
        ("request_id", "credential_ref", "status", "issued_at", "expires_at", "receipt_ref"),
        idempotency="idempotency_key_required",
        critical_transition=True,
    ),
    OperationSpec(
        "register_trust_root",
        OperationKind.COMMAND,
        ("request_id", "trust_root_material_ref", "root_type", "scope", "owner_ref", "validity", "authority_ref", "evidence_refs"),
        ("request_id", "trust_root_ref", "status", "activated_at", "reason_code", "receipt_ref"),
        idempotency="idempotency_key_required",
        critical_transition=True,
    ),
    OperationSpec(
        "revoke_trust_object",
        OperationKind.COMMAND,
        ("request_id", "target_ref", "target_type", "scope", "reason_code", "authority_ref", "effective_at"),
        ("request_id", "target_ref", "resulting_status", "effective_at", "receipt_ref"),
        idempotency="idempotency_key_required",
        critical_transition=True,
    ),
    OperationSpec(
        "apply_offline_trust_update",
        OperationKind.COMMAND,
        ("request_id", "package_ref", "expected_scope", "current_sequence", "profile_ref"),
        ("request_id", "verification_result", "previous_sequence", "active_sequence", "applied_changes", "receipt_ref"),
        idempotency="package_identity_and_sequence",
        critical_transition=True,
    ),
    OperationSpec(
        "resolve_identity",
        OperationKind.QUERY,
        ("identity_ref", "requester_context", "view"),
        ("identity_ref", "subject_type", "status", "public_attributes", "expires_at"),
        selective_disclosure=True,
    ),
    OperationSpec(
        "resolve_trust_context",
        OperationKind.QUERY,
        ("tenant_ref", "environment", "release_channel", "artifact_class", "integration", "component", "purpose"),
        ("trust_context_ref", "active_root_refs", "revocation_state_ref", "valid_until"),
        selective_disclosure=True,
    ),
    OperationSpec(
        "get_component_status",
        OperationKind.QUERY,
        ("view",),
        ("health", "readiness", "active_trust_contexts", "revocation_freshness", "rotation_status", "offline_update_status", "degraded_capabilities"),
        selective_disclosure=True,
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
                "algorithm_or_version_unsupported",
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


def validate_request(spec: OperationSpec, payload: Mapping[str, Any], context: RequestContext) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ApiBoundaryError("request_contract_violation", "request payload must be an object")
    _validate_exact_fields(spec.request_fields, payload, boundary="request")
    if spec.requires_idempotency_key and context.idempotency_key is None:
        raise ApiBoundaryError(
            "missing_idempotency_key",
            "this critical transition requires an idempotency key",
            field="idempotency_key",
        )
    _require_non_empty_strings(payload, ("request_id", "identity_ref", "view"))
    return dict(payload)


def validate_response(spec: OperationSpec, payload: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ApiBoundaryError("response_contract_violation", "service response must be an object")
    _validate_exact_fields(spec.response_fields, payload, boundary="response")
    protected_path = find_protected_material(payload)
    if protected_path is not None:
        raise ApiBoundaryError(
            "private_material_disclosure_detected",
            "protected material cannot cross the ordinary API response boundary",
            field=protected_path,
        )
    if "identity_result" in payload:
        try:
            IdentityResult(str(payload["identity_result"]))
        except ValueError as exc:
            raise ApiBoundaryError(
                "response_contract_violation", "invalid identity result", field="identity_result"
            ) from exc
    if "trust_result" in payload:
        try:
            TrustResult(str(payload["trust_result"]))
        except ValueError as exc:
            raise ApiBoundaryError(
                "response_contract_violation", "invalid trust result", field="trust_result"
            ) from exc
    return dict(payload)


def find_protected_material(value: Any, path: str = "payload") -> str | None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            key_text = str(key).lower()
            child_path = f"{path}.{key}"
            if key_text in _PROTECTED_RESPONSE_KEYS:
                return child_path
            found = find_protected_material(nested, child_path)
            if found is not None:
                return found
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            found = find_protected_material(nested, f"{path}[{index}]")
            if found is not None:
                return found
    return None


def _validate_exact_fields(expected: tuple[str, ...], payload: Mapping[str, Any], *, boundary: str) -> None:
    expected_set = set(expected)
    actual_set = set(payload)
    missing = sorted(expected_set - actual_set)
    unknown = sorted(actual_set - expected_set)
    if missing or unknown:
        details = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if unknown:
            details.append("unknown=" + ",".join(unknown))
        raise ApiBoundaryError(
            f"{boundary}_contract_violation",
            f"{boundary} fields do not match the declared contract ({'; '.join(details)})",
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
