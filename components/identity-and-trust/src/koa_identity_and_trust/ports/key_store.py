"""Protected key-material port.

Only opaque handles and public verification outcomes cross this boundary.  Raw
private keys, passwords, recovery secrets, and unrestricted credentials never do.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Mapping, Protocol, runtime_checkable

from .identity_store import TrustScope

TrustResult = Literal["trusted", "untrusted", "indeterminate"]


@dataclass(frozen=True, slots=True)
class KeyMaterialRef:
    """Opaque reference to staged or active protected material."""

    material_ref: str
    public_material_ref: str
    provider: str
    algorithm: str
    version: str
    state: Literal["staged", "active", "retired", "revoked"]

    def __post_init__(self) -> None:
        for name in ("material_ref", "public_material_ref", "provider", "algorithm", "version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class ProofVerification:
    """Non-authorizing verification result returned by a protected provider."""

    result: TrustResult
    algorithm: str | None
    reason_code: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.result not in {"trusted", "untrusted", "indeterminate"}:
            raise ValueError("unsupported trust result")
        if not self.reason_code:
            raise ValueError("reason_code must not be empty")
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))


@runtime_checkable
class KeyStore(Protocol):
    """Manage protected material through bounded lifecycle operations."""

    def stage_credential_material(
        self,
        *,
        material_id: str,
        subject_identity_id: str,
        credential_type: str,
        scope: TrustScope,
        not_before: datetime,
        expires_at: datetime,
    ) -> KeyMaterialRef:
        """Create protected material in a non-active state and return opaque references."""
        raise NotImplementedError

    def verify_staged_credential_material(
        self,
        material: KeyMaterialRef,
        *,
        subject_identity_id: str,
        credential_type: str,
        scope: TrustScope,
    ) -> ProofVerification:
        """Verify a staged credential before authoritative activation."""
        raise NotImplementedError

    def verify_credential(
        self,
        *,
        material_ref: str,
        presented_proof: bytes,
        intended_use: str,
        context: Mapping[str, str],
        verification_time: datetime,
    ) -> ProofVerification:
        """Verify proof without returning or logging protected material."""
        raise NotImplementedError

    def stage_trust_root(
        self,
        *,
        material_id: str,
        public_material_ref: str,
        root_type: str,
        scope: TrustScope,
        owner_ref: str,
        valid_from: datetime,
        expires_at: datetime,
    ) -> KeyMaterialRef:
        """Stage an exactly scoped public trust root."""
        raise NotImplementedError

    def verify_staged_trust_root(
        self,
        material: KeyMaterialRef,
        *,
        root_type: str,
        scope: TrustScope,
        owner_ref: str,
        verification_time: datetime,
    ) -> ProofVerification:
        """Verify staged root ownership, scope, algorithm, and usability."""
        raise NotImplementedError

    def activate_material(self, material_ref: str, *, activated_at: datetime) -> None:
        """Activate already verified staged material."""
        raise NotImplementedError

    def retire_material(self, material_ref: str, *, retired_at: datetime) -> None:
        """Retire predecessor material without exposing it."""
        raise NotImplementedError

    def revoke_material(self, material_ref: str, *, revoked_at: datetime, reason_code: str) -> None:
        """Prevent new protected use of the referenced material."""
        raise NotImplementedError

    def discard_staged_material(self, material_ref: str) -> None:
        """Remove material that never became authoritative after a failed transition."""
        raise NotImplementedError
