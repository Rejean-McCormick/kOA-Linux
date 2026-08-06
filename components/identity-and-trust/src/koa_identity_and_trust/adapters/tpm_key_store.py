"""TPM key-store adapter over an injected profile-approved backend."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable


class TPMKeyStoreUnavailable(RuntimeError):
    """Raised when a required hardware-backed provider is unavailable."""


@runtime_checkable
class TPMBackend(Protocol):
    """Minimal public boundary required from a TPM implementation."""

    def is_available(self) -> bool: ...

    def create_key(self, key_id: str, attributes: Mapping[str, object]) -> str: ...

    def sign(self, handle: str, payload: bytes, algorithm: str) -> bytes: ...

    def public_material(self, handle: str) -> bytes: ...

    def destroy_key(self, handle: str) -> None: ...


class TPMKeyStore:
    """Keep only opaque TPM handles and fail closed when hardware is unavailable."""

    def __init__(self, backend: TPMBackend) -> None:
        self._backend = backend

    def available(self) -> bool:
        try:
            return bool(self._backend.is_available())
        except Exception:
            return False

    def _require_available(self) -> None:
        if not self.available():
            raise TPMKeyStoreUnavailable("private_key_provider_unavailable")

    def create(
        self,
        key_id: str,
        *,
        purpose: str,
        algorithm: str,
        scope: Mapping[str, object],
    ) -> str:
        if not key_id or not purpose or not algorithm or not scope:
            raise ValueError("key_id, purpose, algorithm and a non-empty scope are required")
        self._require_available()
        handle = self._backend.create_key(
            key_id,
            {"purpose": purpose, "algorithm": algorithm, "scope": dict(scope)},
        )
        if not handle:
            raise TPMKeyStoreUnavailable("TPM backend returned no opaque key handle")
        return f"tpm-key://{handle}"

    def sign(self, reference: str, payload: bytes, *, algorithm: str) -> bytes:
        if not payload:
            raise ValueError("payload must not be empty")
        self._require_available()
        handle = self._handle(reference)
        return self._backend.sign(handle, payload, algorithm)

    def public_material(self, reference: str) -> bytes:
        self._require_available()
        return self._backend.public_material(self._handle(reference))

    def destroy(self, reference: str) -> None:
        self._require_available()
        self._backend.destroy_key(self._handle(reference))

    @staticmethod
    def _handle(reference: str) -> str:
        prefix = "tpm-key://"
        if not reference.startswith(prefix) or len(reference) == len(prefix):
            raise ValueError("invalid TPM key reference")
        return reference[len(prefix) :]
