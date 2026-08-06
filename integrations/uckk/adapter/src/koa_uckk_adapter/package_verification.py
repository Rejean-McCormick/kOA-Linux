"""Fail-closed verification of inbound UCKK learning packages."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import json
from types import MappingProxyType
from typing import Any, Mapping, Protocol, Sequence

from .mediatheque_frame import FrameMappingError, FrameProjector, LocalMediaCandidate


class VerificationDisposition(StrEnum):
    VERIFIED = "verified"
    REVIEW_REQUIRED = "review_required"
    QUARANTINED = "quarantined"
    REJECTED = "rejected"


class TransportKind(StrEnum):
    ONLINE = "online"
    OFFLINE_BUNDLE = "offline_bundle"


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    source_verified: bool
    signature_verified: bool
    equivalent_evidence_verified: bool = False
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        refs = _unique_texts(self.evidence_refs, "evidence_refs")
        object.__setattr__(self, "evidence_refs", refs)

    @property
    def acceptable(self) -> bool:
        return self.source_verified and (
            self.signature_verified or self.equivalent_evidence_verified
        )


class PackageSchemaPort(Protocol):
    def validate(self, package: Mapping[str, Any]) -> None:
        raise RuntimeError("canonical UCKK learning package schema validator")


class ManifestVerificationPort(Protocol):
    def verify(self, package: Mapping[str, Any]) -> bool:
        raise RuntimeError("complete package-manifest verification")


class SourceEvidencePort(Protocol):
    def verify(
        self, package: Mapping[str, Any], *, transport_kind: TransportKind
    ) -> SourceEvidence:
        raise RuntimeError("allowlisted source and signature verification")


class ResourceIntegrityPort(Protocol):
    def verify(
        self,
        *,
        content_ref: str,
        algorithm: str,
        digest: str,
        size_bytes: int,
    ) -> bool:
        raise RuntimeError("verified resource-reference resolution")


class MalwareScanPort(Protocol):
    def scan(
        self, *, content_ref: str, algorithm: str, digest: str, size_bytes: int
    ) -> str:
        raise RuntimeError("profile-declared malware scanning")


class OfflineBundleVerificationPort(Protocol):
    def verify(
        self, *, bundle: Mapping[str, Any], package: Mapping[str, Any]
    ) -> bool:
        raise RuntimeError("offline-bundle trust and completeness verification")


@dataclass(frozen=True, slots=True)
class VerificationReport:
    package_id: str
    disposition: VerificationDisposition
    manifest_complete: bool
    integrity_verified: bool
    signature_verified: bool
    source_verified: bool
    license_resolved: bool
    offline_use_allowed: bool
    frame_compatible: bool
    provenance_preserved: bool
    malware_scan_outcome: str
    review_required: bool
    failure_codes: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    candidates: tuple[LocalMediaCandidate, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.disposition, VerificationDisposition):
            object.__setattr__(
                self, "disposition", VerificationDisposition(self.disposition)
            )
        object.__setattr__(
            self, "failure_codes", _unique_texts(self.failure_codes, "failure_codes")
        )
        object.__setattr__(
            self, "evidence_refs", _unique_texts(self.evidence_refs, "evidence_refs")
        )
        if self.malware_scan_outcome not in {
            "pass",
            "fail",
            "not_applicable",
            "unavailable_blocked",
        }:
            raise ValueError("invalid malware_scan_outcome")
        if self.disposition is VerificationDisposition.VERIFIED and self.failure_codes:
            raise ValueError("verified report cannot contain failure codes")
        if self.acceptance_ready and not self.candidates:
            raise ValueError("acceptance-ready report requires projected candidates")

    @property
    def acceptance_ready(self) -> bool:
        return self.disposition is VerificationDisposition.VERIFIED

    def validation_payload(self) -> Mapping[str, Any]:
        return MappingProxyType(
            {
                "manifest_complete": self.manifest_complete,
                "integrity_verified": self.integrity_verified,
                "signature_verified": self.signature_verified,
                "source_verified": self.source_verified,
                "license_resolved": self.license_resolved,
                "offline_use_allowed": self.offline_use_allowed,
                "frame_compatible": self.frame_compatible,
                "provenance_preserved": self.provenance_preserved,
                "malware_scan_outcome": self.malware_scan_outcome,
                "review_required": self.review_required,
                "failure_codes": list(self.failure_codes),
            }
        )


class PackageVerifier:
    """Verify a package already placed in quarantine."""

    def __init__(
        self,
        *,
        schema: PackageSchemaPort,
        manifest: ManifestVerificationPort,
        source_evidence: SourceEvidencePort,
        resource_integrity: ResourceIntegrityPort,
        malware: MalwareScanPort,
        frame_projector: FrameProjector,
        offline_bundle: OfflineBundleVerificationPort | None = None,
    ) -> None:
        self._schema = schema
        self._manifest = manifest
        self._source_evidence = source_evidence
        self._resource_integrity = resource_integrity
        self._malware = malware
        self._frame_projector = frame_projector
        self._offline_bundle = offline_bundle

    def verify(
        self,
        package: Mapping[str, Any],
        *,
        transport_kind: TransportKind,
        verified_at: datetime,
        offline_bundle: Mapping[str, Any] | None = None,
    ) -> VerificationReport:
        normalized = _json_object(package, "package")
        package_id = normalized.get("package_id")
        if not isinstance(package_id, str) or not package_id:
            package_id = "unknown_package"
        failures: set[str] = set()
        evidence_refs: set[str] = set()
        candidates: list[LocalMediaCandidate] = []
        manifest_complete = False
        integrity_verified = False
        signature_verified = False
        source_verified = False
        license_resolved = False
        offline_use_allowed = False
        frame_compatible = False
        provenance_preserved = False
        malware_outcomes: list[str] = []
        review_required = False

        try:
            self._schema.validate(normalized)
        except Exception:
            failures.add("PACKAGE_SCHEMA_INVALID")
            return _report(
                package_id=package_id,
                failures=failures,
                evidence_refs=evidence_refs,
                candidates=candidates,
                manifest_complete=False,
                integrity_verified=False,
                signature_verified=False,
                source_verified=False,
                license_resolved=False,
                offline_use_allowed=False,
                frame_compatible=False,
                provenance_preserved=False,
                malware_scan_outcome="unavailable_blocked",
                review_required=False,
            )

        now = _utc(verified_at)
        expires_at = normalized.get("expires_at")
        if isinstance(expires_at, str) and _parse_time(expires_at) <= now:
            failures.add("PACKAGE_EXPIRED")

        resources = normalized.get("resources")
        manifest = normalized.get("manifest")
        if not isinstance(resources, list) or not resources:
            failures.add("RESOURCE_GRAPH_INCOMPLETE")
            resources = []
        resource_ids = [
            item.get("resource_id") for item in resources if isinstance(item, Mapping)
        ]
        if len(resource_ids) != len(resources) or len(set(resource_ids)) != len(resources):
            failures.add("RESOURCE_GRAPH_INCOMPLETE")
        if isinstance(manifest, Mapping):
            manifest_complete = bool(
                manifest.get("complete") is True
                and manifest.get("entry_count") == len(resources)
            )
        if not manifest_complete:
            failures.add("MANIFEST_INCOMPLETE")
        else:
            try:
                if not self._manifest.verify(normalized):
                    failures.add("MANIFEST_INVALID")
            except Exception:
                failures.add("MANIFEST_INVALID")

        if transport_kind is TransportKind.OFFLINE_BUNDLE:
            if offline_bundle is None or self._offline_bundle is None:
                failures.add("OFFLINE_BUNDLE_EVIDENCE_MISSING")
            else:
                try:
                    if not self._offline_bundle.verify(
                        bundle=_json_object(offline_bundle, "offline_bundle"),
                        package=normalized,
                    ):
                        failures.add("OFFLINE_BUNDLE_INVALID")
                except Exception:
                    failures.add("OFFLINE_BUNDLE_INVALID")

        try:
            source = self._source_evidence.verify(
                normalized, transport_kind=transport_kind
            )
        except Exception:
            source = SourceEvidence(False, False, False, ())
            failures.add("SOURCE_EVIDENCE_INVALID")
        source_verified = source.source_verified
        signature_verified = source.signature_verified
        evidence_refs.update(source.evidence_refs)
        if not source.source_verified:
            failures.add("SOURCE_UNTRUSTED")
        if not (source.signature_verified or source.equivalent_evidence_verified):
            failures.add("SOURCE_SIGNATURE_OR_EQUIVALENT_MISSING")

        rights = normalized.get("rights")
        if isinstance(rights, Mapping):
            license_status = rights.get("license_status")
            license_ref = rights.get("license_ref")
            license_resolved = license_status in {"declared", "restricted"} and isinstance(
                license_ref, str
            ) and bool(license_ref.strip())
            offline_use_allowed = rights.get("offline_use_allowed") is True
            if rights.get("local_copy_allowed") is not True:
                failures.add("LOCAL_COPY_PROHIBITED")
            if not license_resolved:
                failures.add("LICENSE_UNRESOLVED")
            if transport_kind is TransportKind.OFFLINE_BUNDLE and not offline_use_allowed:
                failures.add("OFFLINE_USE_PROHIBITED")
            rights_expiry = rights.get("expiry")
            if isinstance(rights_expiry, str) and _parse_time(rights_expiry) <= now:
                failures.add("RIGHTS_EXPIRED")
            if license_status == "restricted":
                failures.add("RIGHTS_REVIEW_REQUIRED")
                review_required = True
        else:
            failures.add("LICENSE_UNRESOLVED")

        provenance = normalized.get("provenance")
        provenance_preserved = bool(
            isinstance(provenance, Mapping)
            and isinstance(provenance.get("source_authority_domain_id"), str)
            and provenance.get("source_authority_domain_id")
            and isinstance(provenance.get("export_receipt_refs"), list)
            and provenance.get("export_receipt_refs")
        )
        if not provenance_preserved:
            failures.add("PROVENANCE_INCOMPLETE")
        elif isinstance(provenance, Mapping):
            evidence_refs.update(
                ref
                for ref in provenance.get("export_receipt_refs", [])
                if isinstance(ref, str) and ref
            )

        resource_integrity_ok = bool(resources)
        frame_ok = bool(resources)
        acquisition_method = (
            "imported_offline_bundle"
            if transport_kind is TransportKind.OFFLINE_BUNDLE
            else "imported_online"
        )
        for resource in resources:
            if not isinstance(resource, Mapping):
                resource_integrity_ok = False
                frame_ok = False
                failures.add("RESOURCE_GRAPH_INCOMPLETE")
                continue
            frame = resource.get("frame")
            integrity = frame.get("integrity") if isinstance(frame, Mapping) else None
            if not isinstance(integrity, Mapping):
                resource_integrity_ok = False
                failures.add("RESOURCE_INTEGRITY_FAILED")
                continue
            content_ref = resource.get("content_ref")
            size_bytes = resource.get("size_bytes")
            algorithm = integrity.get("algorithm")
            digest = integrity.get("digest")
            valid_boundary = (
                isinstance(content_ref, str)
                and bool(content_ref)
                and isinstance(size_bytes, int)
                and not isinstance(size_bytes, bool)
                and size_bytes >= 0
                and isinstance(algorithm, str)
                and isinstance(digest, str)
            )
            if not valid_boundary:
                resource_integrity_ok = False
                failures.add("RESOURCE_INTEGRITY_FAILED")
                continue
            try:
                verified = self._resource_integrity.verify(
                    content_ref=content_ref,
                    algorithm=algorithm,
                    digest=digest,
                    size_bytes=size_bytes,
                )
            except Exception:
                verified = False
            if not verified:
                resource_integrity_ok = False
                failures.add("RESOURCE_INTEGRITY_FAILED")
            try:
                scan = self._malware.scan(
                    content_ref=content_ref,
                    algorithm=algorithm,
                    digest=digest,
                    size_bytes=size_bytes,
                )
            except Exception:
                scan = "unavailable_blocked"
            if scan not in {"pass", "fail", "not_applicable", "unavailable_blocked"}:
                scan = "unavailable_blocked"
            malware_outcomes.append(scan)
            if scan == "fail":
                failures.add("MALWARE_DETECTED")
            elif scan == "unavailable_blocked":
                failures.add("MALWARE_SCAN_UNAVAILABLE")
            try:
                candidate = self._frame_projector.project(
                    package=normalized,
                    resource=resource,
                    acquisition_method=acquisition_method,
                    acquired_at=now,
                )
                candidates.append(candidate)
                if candidate.review_required:
                    review_required = True
                    failures.add("FRAME_REVIEW_REQUIRED")
            except FrameMappingError as exc:
                frame_ok = False
                failures.add(exc.code)

        integrity_verified = resource_integrity_ok and "MANIFEST_INVALID" not in failures
        frame_compatible = frame_ok and len(candidates) == len(resources)
        if not frame_compatible:
            failures.add("FRAME_INCOMPATIBLE")
        compatibility = normalized.get("frame_compatibility")
        if not (
            isinstance(compatibility, Mapping)
            and compatibility.get("provenance_preserved") is True
            and compatibility.get("rights_preserved") is True
        ):
            provenance_preserved = False
            failures.add("PROVENANCE_INCOMPLETE")

        malware_scan_outcome = _aggregate_malware(malware_outcomes)
        return _report(
            package_id=package_id,
            failures=failures,
            evidence_refs=evidence_refs,
            candidates=candidates,
            manifest_complete=manifest_complete,
            integrity_verified=integrity_verified,
            signature_verified=signature_verified,
            source_verified=source_verified,
            license_resolved=license_resolved,
            offline_use_allowed=offline_use_allowed,
            frame_compatible=frame_compatible,
            provenance_preserved=provenance_preserved,
            malware_scan_outcome=malware_scan_outcome,
            review_required=review_required,
        )


def _report(
    *,
    package_id: str,
    failures: set[str],
    evidence_refs: set[str],
    candidates: Sequence[LocalMediaCandidate],
    manifest_complete: bool,
    integrity_verified: bool,
    signature_verified: bool,
    source_verified: bool,
    license_resolved: bool,
    offline_use_allowed: bool,
    frame_compatible: bool,
    provenance_preserved: bool,
    malware_scan_outcome: str,
    review_required: bool,
) -> VerificationReport:
    reject_codes = {
        "LOCAL_COPY_PROHIBITED",
        "RESOURCE_INTEGRITY_FAILED",
        "MALWARE_DETECTED",
    }
    review_codes = {"FRAME_REVIEW_REQUIRED", "RIGHTS_REVIEW_REQUIRED"}
    if failures & reject_codes:
        disposition = VerificationDisposition.REJECTED
    elif failures and failures <= review_codes:
        disposition = VerificationDisposition.REVIEW_REQUIRED
    elif failures:
        disposition = VerificationDisposition.QUARANTINED
    else:
        disposition = VerificationDisposition.VERIFIED
    return VerificationReport(
        package_id=package_id,
        disposition=disposition,
        manifest_complete=manifest_complete,
        integrity_verified=integrity_verified,
        signature_verified=signature_verified,
        source_verified=source_verified,
        license_resolved=license_resolved,
        offline_use_allowed=offline_use_allowed,
        frame_compatible=frame_compatible,
        provenance_preserved=provenance_preserved,
        malware_scan_outcome=malware_scan_outcome,
        review_required=review_required,
        failure_codes=tuple(sorted(failures)),
        evidence_refs=tuple(sorted(evidence_refs)),
        candidates=tuple(candidates),
    )


def _aggregate_malware(outcomes: Sequence[str]) -> str:
    if not outcomes:
        return "unavailable_blocked"
    if "fail" in outcomes:
        return "fail"
    if "unavailable_blocked" in outcomes:
        return "unavailable_blocked"
    if "pass" in outcomes:
        return "pass"
    return "not_applicable"


def _json_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be an object")
    normalized = json.loads(
        json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    if not isinstance(normalized, dict):
        raise TypeError(f"{name} must be an object")
    return normalized


def _unique_texts(values: Sequence[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{name} must be a sequence")
    normalized = tuple(str(value).strip() for value in values)
    if any(not value for value in normalized) or len(set(normalized)) != len(normalized):
        raise ValueError(f"{name} must be non-empty and unique")
    return tuple(sorted(normalized))


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return _utc(parsed)


def _utc(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("verification time must be timezone-aware")
    return value.astimezone(timezone.utc)
