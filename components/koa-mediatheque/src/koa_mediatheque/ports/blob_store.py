"""Managed-content storage port."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

_ALLOWED_ALGORITHMS = frozenset({"sha256", "sha384", "sha512"})


@dataclass(frozen=True, slots=True)
class BlobDescriptor:
    blob_ref: str
    media_type: str
    size_bytes: int

    def __post_init__(self) -> None:
        if not self.blob_ref.strip():
            raise ValueError("blob_ref must not be empty")
        if not self.media_type.strip():
            raise ValueError("media_type must not be empty")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")


@dataclass(frozen=True, slots=True)
class StagedBlob:
    staging_ref: str
    media_type: str
    size_bytes: int

    def __post_init__(self) -> None:
        if not self.staging_ref.strip():
            raise ValueError("staging_ref must not be empty")
        if not self.media_type.strip():
            raise ValueError("media_type must not be empty")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")


@runtime_checkable
class BlobStore(Protocol):
    """Own managed bytes while exposing only opaque references."""

    def stage(self, content: bytes, media_type: str, *, staging_key: str) -> StagedBlob:
        """Stage bytes without making them active."""

    def calculate_digest(self, blob_ref: str, algorithm: str) -> str:
        """Calculate a lowercase hexadecimal digest over staged or managed bytes."""

    def commit(self, staging_ref: str, *, blob_key: str) -> BlobDescriptor:
        """Atomically promote staged bytes into managed storage."""

    def discard_staged(self, staging_ref: str) -> None:
        """Remove uncommitted staged bytes."""

    def describe(self, blob_ref: str) -> BlobDescriptor:
        """Describe managed bytes without reading content."""

    def delete(self, blob_ref: str) -> None:
        """Delete a blob only after the authoritative store declares it unreferenced."""


def require_digest(algorithm: str, digest: str) -> tuple[str, str]:
    algorithm = algorithm.lower()
    digest = digest.lower()
    if algorithm not in _ALLOWED_ALGORITHMS:
        raise ValueError(f"unsupported digest algorithm: {algorithm}")
    expected = {"sha256": 64, "sha384": 96, "sha512": 128}[algorithm]
    if len(digest) != expected or any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError(f"invalid {algorithm} digest")
    return algorithm, digest
