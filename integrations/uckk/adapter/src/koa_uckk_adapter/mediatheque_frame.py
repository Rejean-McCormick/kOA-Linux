"""Projection of the shared Mediatheque frame into a local import candidate.

The projection preserves UCKK source identifiers as provenance only.  It never
creates a kOA record or version identity and never writes to the Mediatheque.
The owning component receives the resulting candidate through its public import
interface after package verification and an explicit local decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
from types import MappingProxyType
from typing import Any, Mapping

FRAME_ID = "koa-uckk-shared-mediatheque-frame"
LOCAL_COMPONENT_ID = "koa_mediatheque"

_SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
_DIGEST_LENGTHS = {"sha256": 64, "sha384": 96, "sha512": 128}


class FrameMappingError(RuntimeError):
    """Stable shared-frame failure with no content or credential disclosure."""

    _ALLOWED_CODES = frozenset(
        {
            "FRAME_ID_INVALID",
            "FRAME_VERSION_UNSUPPORTED",
            "MAPPING_VERSION_UNSUPPORTED",
            "MAPPING_METADATA_CONFLICT",
            "SOURCE_AUTHORITY_MISMATCH",
            "SOURCE_IDENTITY_INVALID",
            "SOURCE_PROVENANCE_INVALID",
            "FRAME_INTEGRITY_INVALID",
            "FRAME_RIGHTS_INVALID",
            "FRAME_LIFECYCLE_INVALID",
            "RESOURCE_BOUNDARY_INVALID",
        }
    )

    def __init__(self, code: str, message: str) -> None:
        if code not in self._ALLOWED_CODES:
            raise ValueError(f"undeclared shared-frame error code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class FrameMappingPolicy:
    """Closed compatibility envelope for inbound shared-frame projection."""

    local_authority_domain_id: str
    target_frame_version: str
    supported_source_versions: tuple[str, ...]
    supported_mapping_versions: tuple[str, ...]

    def __post_init__(self) -> None:
        if not _required_text(self.local_authority_domain_id, "local_authority_domain_id"):
            raise ValueError("local_authority_domain_id is required")
        if not _SEMVER.fullmatch(self.target_frame_version):
            raise ValueError("target_frame_version must be semantic version")
        for field_name in ("supported_source_versions", "supported_mapping_versions"):
            values = tuple(getattr(self, field_name))
            if not values or len(values) != len(set(values)):
                raise ValueError(f"{field_name} must be non-empty and unique")
            if any(not _SEMVER.fullmatch(value) for value in values):
                raise ValueError(f"{field_name} must contain semantic versions")
            object.__setattr__(self, field_name, tuple(sorted(values)))


@dataclass(frozen=True, slots=True)
class LocalMediaCandidate:
    """Quarantined projection awaiting Mediatheque-owned identity creation."""

    candidate_id: str
    package_id: str
    resource_id: str
    content_ref: str
    size_bytes: int
    local_authority_domain_id: str
    source_authority_domain_id: str
    source_object_ref: str
    source_version_ref: str
    source_endpoint_id: str
    frame_version: str
    mapping_version: str
    acquisition_method: str
    acquired_at: str
    integrity: Mapping[str, Any]
    media: Mapping[str, Any]
    rights: Mapping[str, Any]
    provenance: Mapping[str, Any]
    source_lifecycle: Mapping[str, Any]
    mapping: Mapping[str, Any]
    review_required: bool

    def __post_init__(self) -> None:
        for name in (
            "candidate_id",
            "package_id",
            "resource_id",
            "content_ref",
            "local_authority_domain_id",
            "source_authority_domain_id",
            "source_object_ref",
            "source_version_ref",
            "source_endpoint_id",
            "frame_version",
            "mapping_version",
            "acquisition_method",
            "acquired_at",
        ):
            _required_text(getattr(self, name), name)
        if self.size_bytes < 0:
            raise ValueError("size_bytes must be non-negative")
        if self.local_authority_domain_id == self.source_authority_domain_id:
            raise ValueError("source and local authority domains must remain separate")
        for name in ("integrity", "media", "rights", "provenance", "source_lifecycle", "mapping"):
            object.__setattr__(self, name, _immutable_json_object(getattr(self, name), name))

    def to_mediatheque_request(self) -> Mapping[str, Any]:
        """Return a public-interface payload without local record identifiers."""

        return _immutable_json_object(
            {
                "candidate_id": self.candidate_id,
                "candidate_state": "quarantined",
                "package_id": self.package_id,
                "resource_id": self.resource_id,
                "authority_domain_id": self.local_authority_domain_id,
                "content": {
                    "content_ref": self.content_ref,
                    "size_bytes": self.size_bytes,
                    "integrity": dict(self.integrity),
                },
                "media": dict(self.media),
                "rights": dict(self.rights),
                "provenance": {
                    **dict(self.provenance),
                    "source_system": "uckk",
                    "source_authority_domain_id": self.source_authority_domain_id,
                    "source_object_ref": self.source_object_ref,
                    "source_version_ref": self.source_version_ref,
                    "source_endpoint_id": self.source_endpoint_id,
                    "acquisition_method": self.acquisition_method,
                    "acquired_at": self.acquired_at,
                },
                "source_lifecycle": dict(self.source_lifecycle),
                "frame_mapping": dict(self.mapping),
                "review_required": self.review_required,
                "local_record_id": None,
                "local_version_id": None,
            },
            "mediatheque request",
        )


class FrameProjector:
    """Validate and project one package resource into quarantine."""

    def __init__(self, policy: FrameMappingPolicy) -> None:
        self._policy = policy

    def project(
        self,
        *,
        package: Mapping[str, Any],
        resource: Mapping[str, Any],
        acquisition_method: str,
        acquired_at: datetime,
    ) -> LocalMediaCandidate:
        package_value = _json_object(package, "package")
        resource_value = _json_object(resource, "resource")
        frame = _json_object(resource_value.get("frame"), "resource.frame")
        compatibility = _json_object(
            package_value.get("frame_compatibility"), "package.frame_compatibility"
        )
        source = _json_object(package_value.get("source"), "package.source")
        package_provenance = _json_object(package_value.get("provenance"), "package.provenance")

        if frame.get("frame_id") != FRAME_ID or compatibility.get("frame_id") != FRAME_ID:
            raise FrameMappingError("FRAME_ID_INVALID", "shared Mediatheque frame id is invalid")

        frame_version = _required_text(frame.get("frame_version"), "frame.frame_version")
        source_frame_version = _required_text(
            compatibility.get("source_frame_version"),
            "frame_compatibility.source_frame_version",
        )
        target_frame_version = _required_text(
            compatibility.get("target_frame_version"),
            "frame_compatibility.target_frame_version",
        )
        mapping_version = _required_text(
            compatibility.get("mapping_version"), "frame_compatibility.mapping_version"
        )
        if frame_version != source_frame_version:
            raise FrameMappingError(
                "MAPPING_METADATA_CONFLICT",
                "resource frame version differs from package compatibility metadata",
            )
        if frame_version not in self._policy.supported_source_versions:
            raise FrameMappingError(
                "FRAME_VERSION_UNSUPPORTED", "source shared-frame version is unsupported"
            )
        if target_frame_version != self._policy.target_frame_version:
            raise FrameMappingError(
                "FRAME_VERSION_UNSUPPORTED", "target shared-frame version is unsupported"
            )
        if mapping_version not in self._policy.supported_mapping_versions:
            raise FrameMappingError(
                "MAPPING_VERSION_UNSUPPORTED", "shared-frame mapping version is unsupported"
            )
        if compatibility.get("rights_preserved") is not True or compatibility.get(
            "provenance_preserved"
        ) is not True:
            raise FrameMappingError(
                "MAPPING_METADATA_CONFLICT",
                "rights and provenance preservation must be explicit",
            )

        object_identity = _json_object(frame.get("object_identity"), "frame.object_identity")
        version_identity = _json_object(frame.get("version_identity"), "frame.version_identity")
        source_authority = _required_text(
            object_identity.get("authority_domain_id"),
            "frame.object_identity.authority_domain_id",
        )
        declared_source_authority = _required_text(
            package_provenance.get("source_authority_domain_id"),
            "package.provenance.source_authority_domain_id",
        )
        if source_authority != declared_source_authority:
            raise FrameMappingError(
                "SOURCE_AUTHORITY_MISMATCH",
                "frame and package provenance declare different source authorities",
            )
        if source_authority == self._policy.local_authority_domain_id:
            raise FrameMappingError(
                "SOURCE_AUTHORITY_MISMATCH",
                "UCKK source identity cannot use the local authority domain",
            )
        if object_identity.get("origin_system") not in (None, "uckk"):
            raise FrameMappingError(
                "SOURCE_IDENTITY_INVALID", "inbound package object must originate from UCKK"
            )
        source_object_ref = _required_text(
            object_identity.get("object_id"), "frame.object_identity.object_id"
        )
        source_version_ref = _required_text(
            version_identity.get("version_id"), "frame.version_identity.version_id"
        )

        integrity = _json_object(frame.get("integrity"), "frame.integrity")
        algorithm = integrity.get("algorithm")
        digest = integrity.get("digest")
        if algorithm not in _DIGEST_LENGTHS or not isinstance(digest, str):
            raise FrameMappingError("FRAME_INTEGRITY_INVALID", "frame integrity is invalid")
        if len(digest) != _DIGEST_LENGTHS[str(algorithm)] or not re.fullmatch(
            r"[0-9a-f]+", digest
        ):
            raise FrameMappingError("FRAME_INTEGRITY_INVALID", "frame digest is invalid")

        rights = _json_object(frame.get("rights"), "frame.rights")
        if rights.get("license_status") not in {
            "declared",
            "restricted",
            "unknown",
            "not_applicable",
        }:
            raise FrameMappingError("FRAME_RIGHTS_INVALID", "frame license status is invalid")
        if rights.get("disclosure_status") not in {
            "private",
            "organization_private",
            "restricted",
            "shareable",
            "public",
        }:
            raise FrameMappingError("FRAME_RIGHTS_INVALID", "frame disclosure status is invalid")

        provenance = _json_object(frame.get("provenance"), "frame.provenance")
        if provenance.get("source_system") != "uckk":
            raise FrameMappingError(
                "SOURCE_PROVENANCE_INVALID", "inbound frame provenance must identify UCKK"
            )
        if provenance.get("source_object_ref") not in (None, source_object_ref):
            raise FrameMappingError(
                "SOURCE_PROVENANCE_INVALID", "source object provenance is inconsistent"
            )
        if provenance.get("source_version_ref") not in (None, source_version_ref):
            raise FrameMappingError(
                "SOURCE_PROVENANCE_INVALID", "source version provenance is inconsistent"
            )
        if acquisition_method not in {"imported_online", "imported_offline_bundle"}:
            raise FrameMappingError(
                "SOURCE_PROVENANCE_INVALID", "unsupported inbound acquisition method"
            )

        lifecycle = _json_object(frame.get("lifecycle"), "frame.lifecycle")
        if lifecycle.get("state") not in {
            "candidate",
            "quarantined",
            "accepted",
            "active",
            "superseded",
            "withdrawn",
            "rejected",
        }:
            raise FrameMappingError("FRAME_LIFECYCLE_INVALID", "source lifecycle state is invalid")
        if lifecycle.get("authority_domain_id") != source_authority:
            raise FrameMappingError(
                "FRAME_LIFECYCLE_INVALID",
                "source lifecycle authority differs from source object authority",
            )

        resource_id = _required_text(resource_value.get("resource_id"), "resource.resource_id")
        content_ref = _required_text(resource_value.get("content_ref"), "resource.content_ref")
        size_bytes = resource_value.get("size_bytes")
        if isinstance(size_bytes, bool) or not isinstance(size_bytes, int) or size_bytes < 0:
            raise FrameMappingError(
                "RESOURCE_BOUNDARY_INVALID", "resource size must be a non-negative integer"
            )

        frame_mapping = _json_object(frame.get("mapping", {}), "frame.mapping")
        for name, expected in (
            ("source_frame_version", source_frame_version),
            ("target_frame_version", target_frame_version),
            ("mapping_version", mapping_version),
        ):
            observed = frame_mapping.get(name)
            if observed not in (None, expected):
                raise FrameMappingError(
                    "MAPPING_METADATA_CONFLICT", f"frame mapping {name} is inconsistent"
                )
        lossy_fields = compatibility.get("lossy_fields", [])
        if not isinstance(lossy_fields, list) or any(
            not isinstance(value, str) or not value for value in lossy_fields
        ):
            raise FrameMappingError(
                "MAPPING_METADATA_CONFLICT", "lossy_fields must be a list of strings"
            )
        unmapped = frame_mapping.get("unmapped_fields", [])
        if not isinstance(unmapped, list) or any(
            not isinstance(value, str) or not value for value in unmapped
        ):
            raise FrameMappingError(
                "MAPPING_METADATA_CONFLICT", "unmapped_fields must be a list of strings"
            )
        lossless = frame_mapping.get("lossless", not lossy_fields and not unmapped)
        if not isinstance(lossless, bool):
            raise FrameMappingError(
                "MAPPING_METADATA_CONFLICT", "mapping lossless flag must be boolean"
            )
        review_required = bool(
            compatibility.get("review_required", False)
            or frame_mapping.get("review_required", False)
            or lossy_fields
            or unmapped
            or not lossless
        )
        normalized_mapping = {
            "frame_id": FRAME_ID,
            "source_frame_version": source_frame_version,
            "target_frame_version": target_frame_version,
            "mapping_version": mapping_version,
            "lossless": lossless,
            "review_required": review_required,
            "unmapped_fields": sorted(set(str(value) for value in (*lossy_fields, *unmapped))),
        }

        package_id = _required_text(package_value.get("package_id"), "package.package_id")
        endpoint_id = _required_text(source.get("endpoint_id"), "package.source.endpoint_id")
        acquired = _utc_timestamp(acquired_at)
        candidate_core = {
            "package_id": package_id,
            "resource_id": resource_id,
            "source_authority_domain_id": source_authority,
            "source_object_ref": source_object_ref,
            "source_version_ref": source_version_ref,
            "content_ref": content_ref,
            "digest": digest,
            "mapping_version": mapping_version,
        }
        candidate_id = "uckk_import_candidate_" + sha256(
            _canonical_json(candidate_core)
        ).hexdigest()
        return LocalMediaCandidate(
            candidate_id=candidate_id,
            package_id=package_id,
            resource_id=resource_id,
            content_ref=content_ref,
            size_bytes=size_bytes,
            local_authority_domain_id=self._policy.local_authority_domain_id,
            source_authority_domain_id=source_authority,
            source_object_ref=source_object_ref,
            source_version_ref=source_version_ref,
            source_endpoint_id=endpoint_id,
            frame_version=frame_version,
            mapping_version=mapping_version,
            acquisition_method=acquisition_method,
            acquired_at=acquired,
            integrity=integrity,
            media=_json_object(frame.get("media"), "frame.media"),
            rights=rights,
            provenance=provenance,
            source_lifecycle=lifecycle,
            mapping=normalized_mapping,
            review_required=review_required,
        )


def _required_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FrameMappingError("RESOURCE_BOUNDARY_INVALID", f"{name} must be a non-empty string")
    return value.strip()


def _json_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise FrameMappingError("RESOURCE_BOUNDARY_INVALID", f"{name} must be an object")
    try:
        normalized = json.loads(_canonical_json(value))
    except (TypeError, ValueError) as exc:
        raise FrameMappingError(
            "RESOURCE_BOUNDARY_INVALID", f"{name} must contain JSON-compatible values"
        ) from exc
    if not isinstance(normalized, dict):
        raise FrameMappingError("RESOURCE_BOUNDARY_INVALID", f"{name} must be an object")
    return normalized


def _immutable_json_object(value: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    return MappingProxyType(_json_object(value, name))


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _utc_timestamp(value: datetime) -> str:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise FrameMappingError(
            "SOURCE_PROVENANCE_INVALID", "acquired_at must be timezone-aware"
        )
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
