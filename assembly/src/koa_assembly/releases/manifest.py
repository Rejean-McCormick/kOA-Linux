"""Deterministic channel release manifests used by Release Set assembly."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import re
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from ..model import canonical_json_bytes


CANONICAL_CHANNEL_NAMESPACES: Mapping[str, str] = MappingProxyType(
    {
        "system": "koa.system",
        "services": "koa.services",
        "governance": "koa.governance",
        "knowledge": "koa.knowledge",
    }
)

_STABLE_ID = re.compile(r"^[a-z0-9]+(?:[._:-][a-z0-9]+)*$")
_SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
_HEX_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REF = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|[A-Za-z0-9_.-]+/|[A-Za-z0-9_.-]+$).+$")
_BUNDLE_ID = re.compile(r"^B-[0-9]{4}$")
_PROFILE_ID = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_TOOL_ID = re.compile(r"^[a-z0-9]+(?:[._:-][a-z0-9]+)*$")


class ManifestValidationError(ValueError):
    """Raised when a channel manifest is incomplete or non-canonical."""


@dataclass(frozen=True, slots=True)
class RecoveryDeclaration:
    """Channel-owned recovery behavior copied into the Release Set."""

    mode: str
    procedure_ref: str
    previous_compatible_release_ref: str | None = None
    forward_repair_artifact_ref: str | None = None
    rollback_boundary_ref: str | None = None

    def __post_init__(self) -> None:
        if self.mode not in {"rollback", "forward_repair", "rollback_or_forward_repair"}:
            raise ManifestValidationError(f"unsupported recovery mode: {self.mode}")
        _require_ref(self.procedure_ref, "procedure_ref")
        for field_name in (
            "previous_compatible_release_ref",
            "forward_repair_artifact_ref",
            "rollback_boundary_ref",
        ):
            value = getattr(self, field_name)
            if value is not None:
                _require_ref(value, field_name)
        if self.mode == "forward_repair" and self.forward_repair_artifact_ref is None:
            raise ManifestValidationError(
                "forward_repair requires forward_repair_artifact_ref"
            )

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "RecoveryDeclaration":
        allowed = {
            "mode",
            "procedure_ref",
            "previous_compatible_release_ref",
            "forward_repair_artifact_ref",
            "rollback_boundary_ref",
        }
        _reject_unknown(value, allowed, "recovery")
        return cls(
            mode=_required_string(value, "mode"),
            procedure_ref=_required_string(value, "procedure_ref"),
            previous_compatible_release_ref=_optional_string(
                value, "previous_compatible_release_ref"
            ),
            forward_repair_artifact_ref=_optional_string(
                value, "forward_repair_artifact_ref"
            ),
            rollback_boundary_ref=_optional_string(value, "rollback_boundary_ref"),
        )

    def to_dict(self) -> dict[str, str]:
        result = {"mode": self.mode, "procedure_ref": self.procedure_ref}
        for field_name in (
            "previous_compatible_release_ref",
            "forward_repair_artifact_ref",
            "rollback_boundary_ref",
        ):
            value = getattr(self, field_name)
            if value is not None:
                result[field_name] = value
        return result


@dataclass(frozen=True, slots=True)
class ArtifactManifestEntry:
    """One immutable artifact selected by a channel owner."""

    artifact_ref: str
    artifact_class: str
    version: str
    channel_id: str
    sha256: str
    size_bytes: int
    provenance_ref: str
    sbom_ref: str | None = None

    def __post_init__(self) -> None:
        _require_ref(self.artifact_ref, "artifact_ref")
        _require_stable_id(self.artifact_class, "artifact_class")
        _require_semver(self.version, "version")
        if self.channel_id not in CANONICAL_CHANNEL_NAMESPACES:
            raise ManifestValidationError(f"unknown release channel: {self.channel_id}")
        digest = self.sha256.lower()
        if not _HEX_SHA256.fullmatch(digest):
            raise ManifestValidationError("sha256 must be 64 lowercase hexadecimal characters")
        object.__setattr__(self, "sha256", digest)
        if (
            not isinstance(self.size_bytes, int)
            or isinstance(self.size_bytes, bool)
            or self.size_bytes < 0
        ):
            raise ManifestValidationError("size_bytes must be a non-negative integer")
        _require_ref(self.provenance_ref, "provenance_ref")
        if self.sbom_ref is not None:
            _require_ref(self.sbom_ref, "sbom_ref")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ArtifactManifestEntry":
        allowed = {
            "artifact_ref",
            "artifact_class",
            "version",
            "channel_id",
            "sha256",
            "size_bytes",
            "provenance_ref",
            "sbom_ref",
        }
        _reject_unknown(value, allowed, "artifact")
        size = value.get("size_bytes")
        if not isinstance(size, int) or isinstance(size, bool):
            raise ManifestValidationError("artifact.size_bytes must be an integer")
        return cls(
            artifact_ref=_required_string(value, "artifact_ref"),
            artifact_class=_required_string(value, "artifact_class"),
            version=_required_string(value, "version"),
            channel_id=_required_string(value, "channel_id"),
            sha256=_required_string(value, "sha256"),
            size_bytes=size,
            provenance_ref=_required_string(value, "provenance_ref"),
            sbom_ref=_optional_string(value, "sbom_ref"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "artifact_ref": self.artifact_ref,
            "artifact_class": self.artifact_class,
            "version": self.version,
            "channel_id": self.channel_id,
            "sha256": self.sha256,
            "size_bytes": self.size_bytes,
            "provenance_ref": self.provenance_ref,
        }
        if self.sbom_ref is not None:
            result["sbom_ref"] = self.sbom_ref
        return result


@dataclass(frozen=True, slots=True)
class ReleaseManifest:
    """Validated immutable manifest for exactly one canonical release channel."""

    channel_id: str
    release_namespace: str
    release_id: str
    version: str
    manifest_ref: str
    source_release_ref: str
    artifacts: tuple[ArtifactManifestEntry, ...]
    provenance_ref: str
    validation_evidence_refs: tuple[str, ...]
    recovery: RecoveryDeclaration
    interface_versions: tuple[tuple[str, str], ...] = ()
    schema_versions: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        expected_namespace = CANONICAL_CHANNEL_NAMESPACES.get(self.channel_id)
        if expected_namespace is None:
            raise ManifestValidationError(f"unknown release channel: {self.channel_id}")
        if self.release_namespace != expected_namespace:
            raise ManifestValidationError(
                f"channel {self.channel_id} requires namespace {expected_namespace}"
            )
        _require_stable_id(self.release_id, "release_id")
        _require_semver(self.version, "version")
        _require_ref(self.manifest_ref, "manifest_ref")
        _require_ref(self.source_release_ref, "source_release_ref")
        _require_ref(self.provenance_ref, "provenance_ref")
        if not self.artifacts:
            raise ManifestValidationError("a channel release requires at least one artifact")
        artifacts = tuple(sorted(self.artifacts, key=lambda item: item.artifact_ref))
        artifact_refs = [item.artifact_ref for item in artifacts]
        if len(artifact_refs) != len(set(artifact_refs)):
            raise ManifestValidationError("artifact_ref values must be unique in a manifest")
        if any(item.channel_id != self.channel_id for item in artifacts):
            raise ManifestValidationError(
                "every artifact entry must declare the manifest channel_id"
            )
        object.__setattr__(self, "artifacts", artifacts)
        object.__setattr__(
            self,
            "validation_evidence_refs",
            _unique_refs(self.validation_evidence_refs, "validation_evidence_refs"),
        )
        object.__setattr__(
            self,
            "interface_versions",
            _version_pairs(self.interface_versions, "interface_versions"),
        )
        object.__setattr__(
            self,
            "schema_versions",
            _version_pairs(self.schema_versions, "schema_versions"),
        )

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ReleaseManifest":
        allowed = {
            "format",
            "format_version",
            "channel_id",
            "release_namespace",
            "release_id",
            "version",
            "manifest_ref",
            "source_release_ref",
            "artifacts",
            "provenance_ref",
            "validation_evidence_refs",
            "recovery",
            "interface_versions",
            "schema_versions",
        }
        _reject_unknown(value, allowed, "release manifest")
        if value.get("format", "koa.release-manifest") != "koa.release-manifest":
            raise ManifestValidationError("unsupported release manifest format")
        if value.get("format_version", "1.0.0") != "1.0.0":
            raise ManifestValidationError("unsupported release manifest format_version")
        raw_artifacts = value.get("artifacts")
        if not isinstance(raw_artifacts, list):
            raise ManifestValidationError("release manifest artifacts must be an array")
        evidence = _string_sequence(value.get("validation_evidence_refs"), "validation_evidence_refs")
        recovery = value.get("recovery")
        if not isinstance(recovery, Mapping):
            raise ManifestValidationError("release manifest recovery must be an object")
        return cls(
            channel_id=_required_string(value, "channel_id"),
            release_namespace=_required_string(value, "release_namespace"),
            release_id=_required_string(value, "release_id"),
            version=_required_string(value, "version"),
            manifest_ref=_required_string(value, "manifest_ref"),
            source_release_ref=_required_string(value, "source_release_ref"),
            artifacts=tuple(
                ArtifactManifestEntry.from_mapping(item)
                if isinstance(item, Mapping)
                else _raise_manifest("artifact entries must be objects")
                for item in raw_artifacts
            ),
            provenance_ref=_required_string(value, "provenance_ref"),
            validation_evidence_refs=evidence,
            recovery=RecoveryDeclaration.from_mapping(recovery),
            interface_versions=_mapping_pairs(value.get("interface_versions", {}), "interface_versions"),
            schema_versions=_mapping_pairs(value.get("schema_versions", {}), "schema_versions"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "format": "koa.release-manifest",
            "format_version": "1.0.0",
            "channel_id": self.channel_id,
            "release_namespace": self.release_namespace,
            "release_id": self.release_id,
            "version": self.version,
            "manifest_ref": self.manifest_ref,
            "source_release_ref": self.source_release_ref,
            "artifacts": [item.to_dict() for item in self.artifacts],
            "provenance_ref": self.provenance_ref,
            "validation_evidence_refs": list(self.validation_evidence_refs),
            "recovery": self.recovery.to_dict(),
        }
        if self.interface_versions:
            result["interface_versions"] = dict(self.interface_versions)
        if self.schema_versions:
            result["schema_versions"] = dict(self.schema_versions)
        return result

    def to_channel_release(self) -> dict[str, Any]:
        """Project this manifest into the Release Set channelRelease schema."""

        result: dict[str, Any] = {
            "channel_id": self.channel_id,
            "release_namespace": self.release_namespace,
            "release_id": self.release_id,
            "version": self.version,
            "release_manifest_ref": self.manifest_ref,
            "artifact_refs": [item.artifact_ref for item in self.artifacts],
            "provenance_ref": self.provenance_ref,
            "validation_evidence_refs": list(self.validation_evidence_refs),
            "recovery": self.recovery.to_dict(),
        }
        if self.interface_versions:
            result["interface_versions"] = dict(self.interface_versions)
        if self.schema_versions:
            result["schema_versions"] = dict(self.schema_versions)
        return result

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_dict())

    @property
    def digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()



@dataclass(frozen=True, slots=True)
class AssemblyBundleManifest:
    """Closed deterministic manifest for one generated assembly-plan bundle."""

    bundle_id: str
    profile_id: str
    profile_contract_ref: str
    overlay_refs: tuple[str, ...]
    resolved_plan: Mapping[str, Any]
    input_digests: tuple[tuple[str, str], ...]
    tool_versions: tuple[tuple[str, str], ...]
    projection_refs: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not _BUNDLE_ID.fullmatch(self.bundle_id):
            raise ManifestValidationError("bundle_id must match B-<four digits>")
        if not _PROFILE_ID.fullmatch(self.profile_id):
            raise ManifestValidationError("profile_id must be a stable lowercase identifier")
        _require_repository_ref(self.profile_contract_ref, "profile_contract_ref")
        overlays = tuple(sorted(set(self.overlay_refs)))
        if len(overlays) != len(self.overlay_refs):
            raise ManifestValidationError("overlay_refs values must be unique")
        for ref in overlays:
            _require_repository_ref(ref, "overlay_refs")
        object.__setattr__(self, "overlay_refs", overlays)

        plan = deepcopy(dict(self.resolved_plan))
        if plan.get("profile_id") != self.profile_id:
            raise ManifestValidationError("resolved_plan.profile_id must match profile_id")
        object.__setattr__(self, "resolved_plan", MappingProxyType(plan))

        digests = _digest_pairs(self.input_digests)
        required_sources = {self.profile_contract_ref, *overlays}
        missing_sources = sorted(required_sources - {path for path, _ in digests})
        if missing_sources:
            raise ManifestValidationError(
                "profile and overlay authorities require input digests: "
                + ", ".join(missing_sources)
            )
        object.__setattr__(self, "input_digests", digests)

        tools = tuple(sorted(self.tool_versions))
        if not tools:
            raise ManifestValidationError("tool_versions must not be empty")
        if len({key for key, _ in tools}) != len(tools):
            raise ManifestValidationError("tool_versions keys must be unique")
        for key, version in tools:
            if not isinstance(key, str) or not _TOOL_ID.fullmatch(key):
                raise ManifestValidationError(f"invalid tool version key: {key!r}")
            if not isinstance(version, str) or not version.strip() or "\n" in version:
                raise ManifestValidationError(
                    f"tool_versions.{key} must be a non-empty single-line string"
                )
        object.__setattr__(self, "tool_versions", tools)

        projections = tuple(sorted(self.projection_refs))
        if not projections:
            raise ManifestValidationError("projection_refs must not be empty")
        if len({key for key, _ in projections}) != len(projections):
            raise ManifestValidationError("projection_refs keys must be unique")
        for key, ref in projections:
            if not isinstance(key, str) or not _TOOL_ID.fullmatch(key):
                raise ManifestValidationError(f"invalid projection key: {key!r}")
            _require_generated_ref(ref, f"projection_refs.{key}")
        object.__setattr__(self, "projection_refs", projections)

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "koa.assembly-bundle",
            "format_version": "1.0.0",
            "bundle_id": self.bundle_id,
            "profile": {
                "profile_id": self.profile_id,
                "contract_ref": self.profile_contract_ref,
                "overlays": list(self.overlay_refs),
            },
            "resolved_plan": deepcopy(dict(self.resolved_plan)),
            "input_digests": dict(self.input_digests),
            "tool_versions": dict(self.tool_versions),
            "projection_refs": dict(self.projection_refs),
        }

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_dict())

    @property
    def digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()


def _digest_pairs(values: Iterable[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    pairs = tuple(sorted(values))
    if not pairs:
        raise ManifestValidationError("input_digests must not be empty")
    if len({path for path, _ in pairs}) != len(pairs):
        raise ManifestValidationError("input_digests paths must be unique")
    normalized: list[tuple[str, str]] = []
    for path, digest in pairs:
        _require_repository_ref(path, "input_digests path")
        if not isinstance(digest, str):
            raise ManifestValidationError(f"input digest for {path!r} must be a string")
        value = digest.lower().removeprefix("sha256:")
        if not _HEX_SHA256.fullmatch(value):
            raise ManifestValidationError(f"input digest for {path!r} must be sha256")
        normalized.append((path, f"sha256:{value}"))
    return tuple(normalized)


def _require_repository_ref(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value or value.startswith("/"):
        raise ManifestValidationError(f"{field_name} must be a repository-relative reference")
    path = PurePosixPath(value.split("#", 1)[0])
    if not path.parts or ".." in path.parts:
        raise ManifestValidationError(f"{field_name} must not escape the repository")


def _require_generated_ref(value: str, field_name: str) -> None:
    _require_repository_ref(value, field_name)
    path = PurePosixPath(value.split("#", 1)[0])
    if not path.parts or path.parts[0] != "generated":
        raise ManifestValidationError(f"{field_name} must be under generated/")

def build_release_manifest(
    *,
    channel_id: str,
    release_id: str,
    version: str,
    manifest_ref: str,
    source_release_ref: str,
    artifacts: Iterable[ArtifactManifestEntry],
    provenance_ref: str,
    validation_evidence_refs: Iterable[str],
    recovery: RecoveryDeclaration,
    interface_versions: Mapping[str, str] | None = None,
    schema_versions: Mapping[str, str] | None = None,
) -> ReleaseManifest:
    """Build one canonical manifest without timestamps or environment defaults."""

    namespace = CANONICAL_CHANNEL_NAMESPACES.get(channel_id)
    if namespace is None:
        raise ManifestValidationError(f"unknown release channel: {channel_id}")
    return ReleaseManifest(
        channel_id=channel_id,
        release_namespace=namespace,
        release_id=release_id,
        version=version,
        manifest_ref=manifest_ref,
        source_release_ref=source_release_ref,
        artifacts=tuple(artifacts),
        provenance_ref=provenance_ref,
        validation_evidence_refs=tuple(validation_evidence_refs),
        recovery=recovery,
        interface_versions=tuple((interface_versions or {}).items()),
        schema_versions=tuple((schema_versions or {}).items()),
    )


def _required_string(value: Mapping[str, Any], field_name: str) -> str:
    raw = value.get(field_name)
    if not isinstance(raw, str) or not raw.strip():
        raise ManifestValidationError(f"{field_name} must be a non-empty string")
    return raw.strip()


def _optional_string(value: Mapping[str, Any], field_name: str) -> str | None:
    raw = value.get(field_name)
    if raw is None:
        return None
    if not isinstance(raw, str) or not raw.strip():
        raise ManifestValidationError(f"{field_name} must be a non-empty string when present")
    return raw.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise ManifestValidationError(f"{field_name} must be a non-empty array")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ManifestValidationError(f"{field_name} must contain non-empty strings")
    return tuple(item.strip() for item in value)


def _mapping_pairs(value: Any, field_name: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, Mapping):
        raise ManifestValidationError(f"{field_name} must be an object")
    pairs: list[tuple[str, str]] = []
    for key, item in value.items():
        if not isinstance(key, str) or not key.strip() or not _STABLE_ID.fullmatch(key):
            raise ManifestValidationError(f"{field_name} contains an invalid key: {key!r}")
        if not isinstance(item, str) or not item.strip():
            raise ManifestValidationError(f"{field_name}.{key} must be a non-empty string")
        pairs.append((key, item.strip()))
    return tuple(pairs)


def _version_pairs(
    value: Iterable[tuple[str, str]], field_name: str
) -> tuple[tuple[str, str], ...]:
    pairs = tuple(sorted(value))
    if len({key for key, _ in pairs}) != len(pairs):
        raise ManifestValidationError(f"{field_name} keys must be unique")
    for key, item in pairs:
        _require_stable_id(key, f"{field_name} key")
        if not isinstance(item, str) or not item.strip():
            raise ManifestValidationError(f"{field_name}.{key} must be a non-empty string")
    return pairs


def _unique_refs(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    items = tuple(sorted(values))
    if not items:
        raise ManifestValidationError(f"{field_name} must not be empty")
    if len(items) != len(set(items)):
        raise ManifestValidationError(f"{field_name} values must be unique")
    for item in items:
        _require_ref(item, field_name)
    return items


def _require_stable_id(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not _STABLE_ID.fullmatch(value):
        raise ManifestValidationError(f"{field_name} is not a stable identifier: {value!r}")


def _require_semver(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not _SEMVER.fullmatch(value):
        raise ManifestValidationError(f"{field_name} is not a semantic version: {value!r}")


def _require_ref(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value or not _REF.fullmatch(value):
        raise ManifestValidationError(f"{field_name} is not a valid contract reference: {value!r}")


def _reject_unknown(value: Mapping[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ManifestValidationError(f"{label} contains unsupported fields: {unknown}")


def _raise_manifest(message: str) -> Any:
    raise ManifestValidationError(message)
