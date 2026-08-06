"""Signature and provenance verification boundary for policy bundles."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable


class SignatureStatus(StrEnum):
    VERIFIED = "verified"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class SignatureVerification:
    status: SignatureStatus
    signer_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()

    @property
    def accepted(self) -> bool:
        return self.status is SignatureStatus.VERIFIED


@runtime_checkable
class SignatureVerifier(Protocol):
    """Verify artifact integrity, signatures, signer scope, and provenance."""

    @abstractmethod
    def verify_policy_bundle(
        self,
        bundle: Mapping[str, Any],
        *,
        at: datetime,
    ) -> SignatureVerification:
        """Return a closed verification outcome without mutating trust state."""
        raise NotImplementedError("a SignatureVerifier adapter is required")
