"""Integrity and deterministic rendition value objects."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
import re

_HEX_DIGEST = re.compile(r"^[0-9a-f]+$")


def _required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _optional_text(value: str | None, field_name: str) -> str | None:
    return None if value is None else _required_text(value, field_name)


def _utc_datetime(value: datetime | None, field_name: str) -> datetime | None:
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


class DigestAlgorithm(StrEnum):
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"

    @property
    def hexadecimal_length(self) -> int:
        return {
            DigestAlgorithm.SHA256: 64,
            DigestAlgorithm.SHA384: 96,
            DigestAlgorithm.SHA512: 128,
        }[self]


@dataclass(frozen=True, slots=True)
class Integrity:
    """Integrity identity of bytes, optionally accompanied by local verification."""

    algorithm: DigestAlgorithm
    digest: str
    verified_at: datetime | None = None
    verified_by: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.algorithm, DigestAlgorithm):
            try:
                object.__setattr__(self, "algorithm", DigestAlgorithm(self.algorithm))
            except (TypeError, ValueError) as exc:
                raise ValueError("unsupported digest algorithm") from exc
        if not isinstance(self.digest, str):
            raise TypeError("digest must be a string")
        digest = self.digest.strip()
        if not _HEX_DIGEST.fullmatch(digest):
            raise ValueError("digest must contain lowercase hexadecimal characters only")
        if len(digest) != self.algorithm.hexadecimal_length:
            raise ValueError(
                f"{self.algorithm.value} digest must contain "
                f"{self.algorithm.hexadecimal_length} hexadecimal characters"
            )
        object.__setattr__(self, "digest", digest)
        object.__setattr__(
            self,
            "verified_at",
            _utc_datetime(self.verified_at, "verified_at"),
        )
        object.__setattr__(
            self,
            "verified_by",
            _optional_text(self.verified_by, "verified_by"),
        )
        if self.verified_by is not None and self.verified_at is None:
            raise ValueError("verified_by requires verified_at")

    @property
    def is_verified(self) -> bool:
        return self.verified_at is not None

    def to_dict(self, *, include_verification: bool = True) -> dict[str, object]:
        result: dict[str, object] = {
            "algorithm": self.algorithm.value,
            "digest": self.digest,
        }
        if include_verification and self.verified_at is not None:
            result["verified_at"] = _timestamp(self.verified_at)
        if include_verification and self.verified_by is not None:
            result["verified_by"] = self.verified_by
        return result


@dataclass(frozen=True, slots=True)
class Rendition:
    """An accepted deterministic derivative of a specific media version."""

    rendition_id: str
    kind: str
    version_id: str
    integrity: Integrity
    media_type: str | None = None
    storage_ref: str | None = None
    transformation_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "rendition_id", _required_text(self.rendition_id, "rendition_id"))
        object.__setattr__(self, "kind", _required_text(self.kind, "kind"))
        object.__setattr__(self, "version_id", _required_text(self.version_id, "version_id"))
        if not isinstance(self.integrity, Integrity):
            raise TypeError("integrity must be an Integrity instance")
        object.__setattr__(self, "media_type", _optional_text(self.media_type, "media_type"))
        object.__setattr__(self, "storage_ref", _optional_text(self.storage_ref, "storage_ref"))
        object.__setattr__(
            self,
            "transformation_ref",
            _optional_text(self.transformation_ref, "transformation_ref"),
        )
        if self.storage_ref is not None and not self.integrity.is_verified:
            raise ValueError("a stored rendition requires verified integrity")

    def to_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "rendition_id": self.rendition_id,
            "kind": self.kind,
            "version_id": self.version_id,
            "integrity": self.integrity.to_dict(include_verification=False),
        }
        if self.media_type is not None:
            result["media_type"] = self.media_type
        if self.storage_ref is not None:
            result["storage_ref"] = self.storage_ref
        if self.transformation_ref is not None:
            result["transformation_ref"] = self.transformation_ref
        return result
