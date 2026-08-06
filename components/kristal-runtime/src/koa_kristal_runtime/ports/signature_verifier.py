"""Trust and integrity verification port for Kristal artifacts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class SignatureVerification:
    identity_valid: bool
    digest_valid: bool
    provenance_valid: bool
    trust_required: bool
    trusted: bool
    signatures_valid: bool
    verifier_ref: str
    reason_code: str | None = None


class SignatureVerifier(Protocol):
    def verify(
        self,
        artifact: Mapping[str, Any],
        signatures: Sequence[Mapping[str, Any]],
    ) -> SignatureVerification:
        raise NotImplementedError
