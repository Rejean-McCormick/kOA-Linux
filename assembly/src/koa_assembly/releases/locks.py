"""Reproducible Release Set locks derived from validated manifests."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from ..model import canonical_json_bytes
from .manifest import CANONICAL_CHANNEL_NAMESPACES, ReleaseManifest
from .release_set import ReleaseSet


class ReleaseLockError(ValueError):
    """Raised when a lock is malformed or does not reproduce its Release Set."""


@dataclass(frozen=True, slots=True)
class LockedArtifact:
    artifact_ref: str
    artifact_class: str
    version: str
    channel_id: str
    sha256: str
    size_bytes: int

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "LockedArtifact":
        _require_keys(
            value,
            {"artifact_ref", "artifact_class", "version", "channel_id", "sha256", "size_bytes"},
            "locked artifact",
        )
        size = value.get("size_bytes")
        if not isinstance(size, int) or isinstance(size, bool):
            raise ReleaseLockError("locked artifact size_bytes must be an integer")
        return cls(
            artifact_ref=_string(value, "artifact_ref"),
            artifact_class=_string(value, "artifact_class"),
            version=_string(value, "version"),
            channel_id=_string(value, "channel_id"),
            sha256=_string(value, "sha256"),
            size_bytes=size,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_ref": self.artifact_ref,
            "artifact_class": self.artifact_class,
            "version": self.version,
            "channel_id": self.channel_id,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
        }


@dataclass(frozen=True, slots=True)
class LockedChannel:
    channel_id: str
    release_id: str
    version: str
    manifest_ref: str
    manifest_sha256: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "LockedChannel":
        _require_keys(
            value,
            {"channel_id", "release_id", "version", "manifest_ref", "manifest_sha256"},
            "locked channel",
        )
        return cls(
            channel_id=_string(value, "channel_id"),
            release_id=_string(value, "release_id"),
            version=_string(value, "version"),
            manifest_ref=_string(value, "manifest_ref"),
            manifest_sha256=_string(value, "manifest_sha256"),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "channel_id": self.channel_id,
            "release_id": self.release_id,
            "version": self.version,
            "manifest_ref": self.manifest_ref,
            "manifest_sha256": self.manifest_sha256,
        }


@dataclass(frozen=True, slots=True)
class ReleaseLock:
    release_set_id: str
    release_set_version: str
    release_set_sha256: str
    channels: tuple[LockedChannel, ...]
    artifacts: tuple[LockedArtifact, ...]

    def __post_init__(self) -> None:
        channels = tuple(sorted(self.channels, key=lambda item: item.channel_id))
        artifacts = tuple(sorted(self.artifacts, key=lambda item: item.artifact_ref))
        if {item.channel_id for item in channels} != set(CANONICAL_CHANNEL_NAMESPACES):
            raise ReleaseLockError("lock requires exactly the four canonical channels")
        if len({item.manifest_ref for item in channels}) != len(channels):
            raise ReleaseLockError("lock manifest_ref values must be unique")
        if len({item.artifact_ref for item in artifacts}) != len(artifacts):
            raise ReleaseLockError("lock artifact_ref values must be unique")
        _digest(self.release_set_sha256, "release_set_sha256")
        for channel in channels:
            _digest(channel.manifest_sha256, f"{channel.channel_id}.manifest_sha256")
        for artifact in artifacts:
            _digest(artifact.sha256, f"{artifact.artifact_ref}.sha256")
            if artifact.channel_id not in CANONICAL_CHANNEL_NAMESPACES:
                raise ReleaseLockError(f"unknown artifact channel: {artifact.channel_id}")
            if isinstance(artifact.size_bytes, bool) or artifact.size_bytes < 0:
                raise ReleaseLockError("artifact size_bytes must be non-negative")
        object.__setattr__(self, "channels", channels)
        object.__setattr__(self, "artifacts", artifacts)

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ReleaseLock":
        _require_keys(
            value,
            {"format", "format_version", "release_set", "channels", "artifacts"},
            "release lock",
        )
        if value.get("format") != "koa.release-lock":
            raise ReleaseLockError("unsupported release lock format")
        if value.get("format_version") != "1.0.0":
            raise ReleaseLockError("unsupported release lock format_version")
        release_set = value.get("release_set")
        if not isinstance(release_set, Mapping):
            raise ReleaseLockError("release_set must be an object")
        _require_keys(
            release_set,
            {"release_set_id", "version", "sha256"},
            "release lock release_set",
        )
        channels = value.get("channels")
        artifacts = value.get("artifacts")
        if not isinstance(channels, list) or not isinstance(artifacts, list):
            raise ReleaseLockError("channels and artifacts must be arrays")
        return cls(
            release_set_id=_string(release_set, "release_set_id"),
            release_set_version=_string(release_set, "version"),
            release_set_sha256=_string(release_set, "sha256"),
            channels=tuple(
                LockedChannel.from_mapping(item)
                if isinstance(item, Mapping)
                else _raise_lock("locked channel entries must be objects")
                for item in channels
            ),
            artifacts=tuple(
                LockedArtifact.from_mapping(item)
                if isinstance(item, Mapping)
                else _raise_lock("locked artifact entries must be objects")
                for item in artifacts
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "koa.release-lock",
            "format_version": "1.0.0",
            "release_set": {
                "release_set_id": self.release_set_id,
                "version": self.release_set_version,
                "sha256": self.release_set_sha256,
            },
            "channels": [item.to_dict() for item in self.channels],
            "artifacts": [item.to_dict() for item in self.artifacts],
        }

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_dict())

    @property
    def digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()


def load_release_lock(path: str | Path) -> ReleaseLock:
    """Load a strict release lock and reject duplicate JSON keys."""

    source = Path(path).expanduser().resolve(strict=True)
    try:
        value = json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ReleaseLockError(f"invalid release lock JSON: {exc}") from exc
    if not isinstance(value, Mapping):
        raise ReleaseLockError("release lock JSON must contain an object")
    return ReleaseLock.from_mapping(value)


def build_release_lock(
    release_set: ReleaseSet, manifests: Iterable[ReleaseManifest]
) -> ReleaseLock:
    """Derive a lock from validated input; no environment value enters the result."""

    by_channel = _manifest_map(manifests)
    document = release_set.to_dict()
    channels = document.get("channels")
    if not isinstance(channels, Mapping):
        raise ReleaseLockError("release set channels are unavailable")
    locked_channels: list[LockedChannel] = []
    locked_artifacts: list[LockedArtifact] = []
    for channel_id in CANONICAL_CHANNEL_NAMESPACES:
        manifest = by_channel[channel_id]
        release = channels.get(channel_id)
        if not isinstance(release, Mapping):
            raise ReleaseLockError(f"release set channel is missing: {channel_id}")
        expected = manifest.to_channel_release()
        if dict(release) != expected:
            raise ReleaseLockError(
                f"manifest {manifest.manifest_ref} does not match Release Set channel {channel_id}"
            )
        locked_channels.append(
            LockedChannel(
                channel_id=channel_id,
                release_id=manifest.release_id,
                version=manifest.version,
                manifest_ref=manifest.manifest_ref,
                manifest_sha256=manifest.digest,
            )
        )
        locked_artifacts.extend(
            LockedArtifact(
                artifact_ref=item.artifact_ref,
                artifact_class=item.artifact_class,
                version=item.version,
                channel_id=item.channel_id,
                sha256=item.sha256,
                size_bytes=item.size_bytes,
            )
            for item in manifest.artifacts
        )
    return ReleaseLock(
        release_set_id=release_set.release_set_id,
        release_set_version=release_set.version,
        release_set_sha256=release_set.digest,
        channels=tuple(locked_channels),
        artifacts=tuple(locked_artifacts),
    )


def verify_release_lock(
    lock: ReleaseLock, release_set: ReleaseSet, manifests: Iterable[ReleaseManifest]
) -> None:
    """Fail closed unless reconstruction produces the exact same canonical lock."""

    expected = build_release_lock(release_set, manifests)
    if lock.canonical_bytes() != expected.canonical_bytes():
        raise ReleaseLockError("release lock does not reproduce from Release Set manifests")


def _manifest_map(manifests: Iterable[ReleaseManifest]) -> Mapping[str, ReleaseManifest]:
    values = tuple(manifests)
    by_channel = {item.channel_id: item for item in values}
    if len(values) != len(by_channel):
        raise ReleaseLockError("duplicate channel manifests are prohibited")
    if set(by_channel) != set(CANONICAL_CHANNEL_NAMESPACES):
        raise ReleaseLockError("exactly four canonical channel manifests are required")
    return MappingProxyType(by_channel)


def _string(value: Mapping[str, Any], field_name: str) -> str:
    item = value.get(field_name)
    if not isinstance(item, str) or not item:
        raise ReleaseLockError(f"{field_name} must be a non-empty string")
    return item


def _require_keys(value: Mapping[str, Any], required: set[str], label: str) -> None:
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required)
    if missing:
        raise ReleaseLockError(f"{label} is missing fields: {missing}")
    if unknown:
        raise ReleaseLockError(f"{label} contains unsupported fields: {unknown}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _raise_lock(message: str) -> Any:
    raise ReleaseLockError(message)


def _digest(value: str, field_name: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ReleaseLockError(f"{field_name} must be a lowercase SHA-256 digest")
