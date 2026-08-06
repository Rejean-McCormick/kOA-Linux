"""Authoritative persistence port for Identity and Trust application services."""

from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Literal, Mapping, Protocol, Sequence, runtime_checkable

IdentityState = Literal["pending", "active", "suspended", "revoked", "expired", "retired"]
CredentialState = Literal["pending", "active", "suspended", "revoked", "expired", "retired"]
TrustRootState = Literal["staged", "active", "suspended", "revoked", "superseded", "retired"]
SessionState = Literal["active", "revoked", "expired", "retired"]
IdentityResult = Literal["established", "not_established", "indeterminate"]
TrustResult = Literal["trusted", "untrusted", "indeterminate"]

_SCOPE_FIELDS = (
    "tenant",
    "environment",
    "release_channel",
    "artifact_class",
    "integration",
    "component",
    "purpose",
)


def _tuple(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(values)


def _mapping(values: Mapping[str, str]) -> Mapping[str, str]:
    return MappingProxyType(dict(sorted(values.items())))


@dataclass(frozen=True, slots=True)
class TrustScope:
    """Exact trust scope; absent dimensions are explicit rather than wildcard fallbacks."""

    tenant: str | None
    environment: str | None
    release_channel: str | None = None
    artifact_class: str | None = None
    integration: str | None = None
    component: str | None = None
    purpose: str | None = None

    def __post_init__(self) -> None:
        if all(getattr(self, field) is None for field in _SCOPE_FIELDS):
            raise ValueError("an unscoped global trust root is prohibited")
        for field_name in _SCOPE_FIELDS:
            value = getattr(self, field_name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"scope field {field_name} must be a non-empty string or None")

    def exact_match(self, other: "TrustScope") -> bool:
        """Return true only when every scope dimension is identical."""

        return all(getattr(self, field) == getattr(other, field) for field in _SCOPE_FIELDS)

    def as_mapping(self) -> Mapping[str, str]:
        """Return present dimensions in stable order."""

        return MappingProxyType(
            {field: value for field in _SCOPE_FIELDS if (value := getattr(self, field)) is not None}
        )


@dataclass(frozen=True, slots=True)
class IdentityRecord:
    identity_id: str
    subject_type: str
    display_name: str
    owner_ref: str
    tenant_ref: str | None
    environment: str
    status: IdentityState
    created_at: datetime
    activated_at: datetime | None
    expires_at: datetime | None
    revoked_at: datetime | None = None
    retired_at: datetime | None = None
    credential_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "credential_refs", _tuple(self.credential_refs))
        object.__setattr__(self, "evidence_refs", _tuple(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class CredentialRecord:
    credential_id: str
    subject_identity_id: str
    credential_type: str
    issuer_ref: str
    scope: TrustScope
    issued_at: datetime
    not_before: datetime
    expires_at: datetime
    status: CredentialState
    key_or_material_reference: str
    revocation_reference: str
    version: str = "1"
    intended_uses: tuple[str, ...] = ()
    revoked_at: datetime | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "intended_uses", _tuple(self.intended_uses))
        object.__setattr__(self, "evidence_refs", _tuple(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class TrustRootRecord:
    trust_root_id: str
    root_type: str
    public_material_ref: str
    protected_material_ref: str
    scope: TrustScope
    owner_ref: str
    status: TrustRootState
    activated_at: datetime | None
    expires_at: datetime
    revoked_at: datetime | None = None
    supersedes_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_refs", _tuple(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class SessionRecord:
    session_id: str
    identity_id: str
    credential_id: str
    tenant_ref: str | None
    environment: str
    assurance_context: Mapping[str, str]
    issued_at: datetime
    expires_at: datetime
    status: SessionState = "active"
    revoked_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "assurance_context", _mapping(self.assurance_context))


@dataclass(frozen=True, slots=True)
class VerificationRecord:
    verification_id: str
    request_id: str
    credential_or_artifact_ref: str
    result: TrustResult
    resolved_identity_ref: str | None
    resolved_trust_root_ref: str | None
    validated_scope: TrustScope | None
    algorithm: str | None
    verified_at: datetime
    reason_code: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_refs", _tuple(self.evidence_refs))


@dataclass(frozen=True, slots=True)
class TransitionReceiptRecord:
    receipt_ref: str
    receipt_class: Literal[
        "decision_receipt",
        "verification_receipt",
        "transition_receipt",
        "evidence_access_receipt",
        "recovery_receipt",
    ]
    transition: str
    request_id: str
    operation_id: str
    subject_refs: tuple[str, ...]
    outcome: str
    reason_code: str
    occurred_at: datetime
    authority_ref: str | None = None
    evidence_refs: tuple[str, ...] = ()
    details: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "subject_refs", _tuple(self.subject_refs))
        object.__setattr__(self, "evidence_refs", _tuple(self.evidence_refs))
        object.__setattr__(self, "details", _mapping(self.details))


@dataclass(frozen=True, slots=True)
class IdempotencyRecord:
    operation_id: str
    idempotency_key: str
    request_fingerprint: str
    response: Mapping[str, str]
    created_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "response", _mapping(self.response))


@runtime_checkable
class IdentityStore(Protocol):
    """Persist only Identity and Trust authoritative records."""

    def transaction(self) -> AbstractContextManager[None]:
        """Return an atomic transaction covering all writes in one use case."""
        raise NotImplementedError

    def get_identity(self, identity_id: str) -> IdentityRecord | None:
        raise NotImplementedError

    def find_identity(
        self,
        *,
        owner_ref: str,
        tenant_ref: str | None,
        environment: str,
        subject_type: str,
    ) -> IdentityRecord | None:
        raise NotImplementedError

    def put_identity(self, record: IdentityRecord) -> None:
        raise NotImplementedError

    def get_credential(self, credential_id: str) -> CredentialRecord | None:
        raise NotImplementedError

    def put_credential(self, record: CredentialRecord) -> None:
        raise NotImplementedError

    def get_trust_root(self, trust_root_id: str) -> TrustRootRecord | None:
        raise NotImplementedError

    def list_trust_roots(self, scope: TrustScope) -> Sequence[TrustRootRecord]:
        raise NotImplementedError

    def put_trust_root(self, record: TrustRootRecord) -> None:
        raise NotImplementedError

    def get_session(self, session_id: str) -> SessionRecord | None:
        raise NotImplementedError

    def put_session(self, record: SessionRecord) -> None:
        raise NotImplementedError

    def invalidate_sessions_for_credential(self, credential_id: str, *, effective_at: datetime) -> int:
        raise NotImplementedError

    def append_verification(self, record: VerificationRecord) -> None:
        raise NotImplementedError

    def append_receipt(self, record: TransitionReceiptRecord) -> None:
        raise NotImplementedError

    def get_idempotency(self, operation_id: str, idempotency_key: str) -> IdempotencyRecord | None:
        raise NotImplementedError

    def put_idempotency(self, record: IdempotencyRecord) -> None:
        raise NotImplementedError
