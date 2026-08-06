"""Creation of minimized, non-authoritative support bundles."""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from hashlib import sha256
from types import MappingProxyType
from typing import Any, Mapping, Sequence
import json

from .health import CollectorDescriptor, DiagnosticDataClass
from .redaction import QuarantinedDiagnosticError, RedactionPolicy, RedactionReport, redact_payload, require_disclosure_safe


class SupportMode(str, Enum):
    SELF_SERVICE = "self_service"
    LOCAL_GUIDED = "local_guided"
    BUNDLE_REVIEW = "bundle_review"
    OFFLINE_EXCHANGE = "offline_exchange"
    INCIDENT_SUPPORT = "incident_support"
    VENDOR_SUPPORT = "vendor_support"


@dataclass(frozen=True, slots=True)
class SupportCase:
    case_id: str
    requester_id: str
    target_refs: tuple[str, ...]
    purpose: str
    mode: SupportMode
    scope: tuple[str, ...]
    authority_refs: tuple[str, ...]
    assigned_identities: tuple[str, ...]
    expires_at: datetime
    evidence_refs: tuple[str, ...] = ()
    status: str = "open"

    def __post_init__(self) -> None:
        _require_text(self.case_id, "case_id")
        _require_text(self.requester_id, "requester_id")
        _require_text(self.purpose, "purpose")
        _require_aware(self.expires_at, "expires_at")
        if not self.target_refs or not self.scope or not self.authority_refs or not self.assigned_identities:
            raise ValueError("support case target, scope, authority and assigned identities are required")
        if self.status not in {"open", "collecting"}:
            raise ValueError("support case must be open for collection")


@dataclass(frozen=True, slots=True)
class CollectionManifest:
    manifest_id: str
    case_id: str
    collector_ids: tuple[str, ...]
    diagnostic_categories: tuple[str, ...]
    time_start: datetime
    time_end: datetime
    component_scope: tuple[str, ...]
    tenant_scope: tuple[str, ...]
    data_class_ceiling: DiagnosticDataClass
    redaction_policy: RedactionPolicy
    max_bundle_bytes: int
    intended_recipient: str
    retention_seconds: int
    required_approvals: tuple[str, ...]
    approval_refs: tuple[str, ...]
    cleanup_behavior: str
    transport_declaration: str

    def __post_init__(self) -> None:
        _require_text(self.manifest_id, "manifest_id")
        _require_text(self.case_id, "case_id")
        _require_aware(self.time_start, "time_start")
        _require_aware(self.time_end, "time_end")
        if self.time_start > self.time_end:
            raise ValueError("manifest time range is invalid")
        if not self.collector_ids or not self.diagnostic_categories or not self.component_scope:
            raise ValueError("collector, category and component scopes are required")
        if self.data_class_ceiling is DiagnosticDataClass.SECRET:
            raise ValueError("secret collection cannot be authorized")
        if not 1 <= self.max_bundle_bytes <= 100 * 1024 * 1024:
            raise ValueError("max_bundle_bytes must be between 1 byte and 100 MiB")
        if not 1 <= self.retention_seconds <= 365 * 24 * 3600:
            raise ValueError("retention_seconds must be explicit and bounded")
        if not self.intended_recipient or not self.cleanup_behavior or not self.transport_declaration:
            raise ValueError("recipient, cleanup and transport declarations are required")
        if not set(self.required_approvals).issubset(self.approval_refs):
            raise ValueError("required approvals are missing")


@dataclass(frozen=True, slots=True)
class DiagnosticSection:
    collector_id: str
    component_id: str
    category: str
    data_class: DiagnosticDataClass
    collected_at: datetime
    payload: Any
    evidence_refs: tuple[str, ...] = ()
    authority_refs: tuple[str, ...] = ()
    necessity: str | None = None

    def __post_init__(self) -> None:
        _require_aware(self.collected_at, "collected_at")
        for name, value in (
            ("collector_id", self.collector_id),
            ("component_id", self.component_id),
            ("category", self.category),
        ):
            _require_text(value, name)


@dataclass(frozen=True, slots=True)
class SupportBundle:
    bundle_id: str
    case_id: str
    manifest_id: str
    collected_at: str
    collector_identity: str
    collector_version: str
    profile_refs: tuple[str, ...]
    component_refs: tuple[str, ...]
    sections: tuple[Mapping[str, Any], ...]
    data_classes: tuple[str, ...]
    redaction_report: Mapping[str, Any]
    omitted_categories: tuple[str, ...]
    source_evidence_refs: tuple[str, ...]
    transport_declaration: str
    intended_recipient: str
    retention_seconds: int
    expires_at: str
    approval_refs: tuple[str, ...]
    review_instructions: tuple[str, ...]
    authoritative: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "redaction_report", MappingProxyType(dict(self.redaction_report)))

    def to_canonical_bytes(self) -> bytes:
        return _canonical_json(self)


@dataclass(frozen=True, slots=True)
class BundleBuildResult:
    bundle: SupportBundle
    sha256: str
    size_bytes: int


def build_support_bundle(
    *,
    case: SupportCase,
    manifest: CollectionManifest,
    sections: Sequence[DiagnosticSection],
    collectors: Sequence[CollectorDescriptor],
    collector_identity: str,
    collector_version: str,
    profile_refs: tuple[str, ...],
    now: datetime,
) -> BundleBuildResult:
    """Build one deterministic support bundle after redaction and minimization."""

    _require_aware(now, "now")
    if case.case_id != manifest.case_id:
        raise ValueError("support bundle must bind to exactly one case")
    if now > case.expires_at:
        raise ValueError("support case has expired")
    if not collector_identity or collector_identity not in case.assigned_identities:
        raise ValueError("collector identity is not assigned to the case")
    if not collector_version:
        raise ValueError("collector version is required")

    registry = {collector.collector_id: collector for collector in collectors}
    if len(registry) != len(collectors):
        raise ValueError("collector identifiers must be unique")
    if set(manifest.collector_ids) - registry.keys():
        raise ValueError("manifest references undeclared collectors")

    if not sections:
        raise ValueError("support bundle requires at least one diagnostic section")

    redacted_sections: list[Mapping[str, Any]] = []
    reports: list[RedactionReport] = []
    data_classes: set[str] = set()
    evidence_refs: set[str] = set(case.evidence_refs)
    components: set[str] = set()

    for section in sorted(sections, key=lambda item: (item.component_id, item.category, item.collector_id)):
        descriptor = registry.get(section.collector_id)
        if descriptor is None or section.collector_id not in manifest.collector_ids:
            raise ValueError("section uses an undeclared collector")
        if section.component_id != descriptor.component_id or section.component_id not in manifest.component_scope:
            raise ValueError("section is outside component scope")
        if section.category not in manifest.diagnostic_categories:
            raise ValueError("section category is outside the manifest")
        if not manifest.time_start <= section.collected_at <= manifest.time_end:
            raise ValueError("section is outside the declared time range")
        if section.data_class > manifest.data_class_ceiling or section.data_class not in descriptor.data_classes:
            raise ValueError("section exceeds the declared data class")

        result = redact_payload(
            section.payload,
            policy=manifest.redaction_policy,
            data_class=section.data_class,
            authority_refs=section.authority_refs,
            necessity=section.necessity,
        )
        require_disclosure_safe(result)
        if isinstance(section.payload, Mapping):
            unsupported_fields = {str(key) for key in section.payload} - set(descriptor.supported_fields)
            if unsupported_fields:
                raise ValueError("section contains fields not declared by its collector")
        reports.append(result.report)
        data_classes.add(section.data_class.name.lower())
        evidence_refs.update(section.evidence_refs)
        components.add(section.component_id)
        redacted_sections.append(
            MappingProxyType(
                {
                    "collector_id": section.collector_id,
                    "component_id": section.component_id,
                    "category": section.category,
                    "data_class": section.data_class.name.lower(),
                    "collected_at": section.collected_at.astimezone(timezone.utc).isoformat(),
                    "payload": result.value,
                    "evidence_refs": tuple(sorted(section.evidence_refs)),
                }
            )
        )

    expiry = min(case.expires_at, now + timedelta(seconds=manifest.retention_seconds))
    combined_report = _combine_reports(reports, manifest.redaction_policy.policy_id)
    bundle_seed = {
        "case_id": case.case_id,
        "manifest_id": manifest.manifest_id,
        "collected_at": now.astimezone(timezone.utc).isoformat(),
        "collector_identity": collector_identity,
        "collector_version": collector_version,
        "sections": redacted_sections,
        "recipient": manifest.intended_recipient,
        "expires_at": expiry.astimezone(timezone.utc).isoformat(),
    }
    bundle_id = "support:" + sha256(_canonical_json(bundle_seed)).hexdigest()
    bundle = SupportBundle(
        bundle_id=bundle_id,
        case_id=case.case_id,
        manifest_id=manifest.manifest_id,
        collected_at=now.astimezone(timezone.utc).isoformat(),
        collector_identity=collector_identity,
        collector_version=collector_version,
        profile_refs=tuple(sorted(profile_refs)),
        component_refs=tuple(sorted(components)),
        sections=tuple(redacted_sections),
        data_classes=tuple(sorted(data_classes)),
        redaction_report=combined_report,
        omitted_categories=tuple(combined_report["omitted_categories"]),
        source_evidence_refs=tuple(sorted(evidence_refs)),
        transport_declaration=manifest.transport_declaration,
        intended_recipient=manifest.intended_recipient,
        retention_seconds=manifest.retention_seconds,
        expires_at=expiry.astimezone(timezone.utc).isoformat(),
        approval_refs=tuple(sorted(manifest.approval_refs)),
        review_instructions=(
            "Verify case identity, recipient and expiry before review.",
            "Treat this bundle as non-authoritative diagnostic evidence.",
            "Do not reuse content outside the declared support purpose.",
            f"Apply cleanup behavior: {manifest.cleanup_behavior}.",
        ),
    )
    body = bundle.to_canonical_bytes()
    if len(body) > manifest.max_bundle_bytes:
        raise ValueError("support bundle exceeds the declared maximum size")
    return BundleBuildResult(bundle=bundle, sha256=sha256(body).hexdigest(), size_bytes=len(body))


def _combine_reports(reports: Sequence[RedactionReport], policy_id: str) -> Mapping[str, Any]:
    totals = {
        "policy_id": policy_id,
        "section_count": len(reports),
        "fields_examined": sum(item.fields_examined for item in reports),
        "fields_retained": sum(item.fields_retained for item in reports),
        "fields_omitted": sum(item.fields_omitted for item in reports),
        "values_redacted": sum(item.values_redacted for item in reports),
        "values_pseudonymized": sum(item.values_pseudonymized for item in reports),
        "values_truncated": sum(item.values_truncated for item in reports),
        "collection_items_omitted": sum(item.collection_items_omitted for item in reports),
        "omitted_categories": sorted({category for item in reports for category in item.omitted_categories}),
        "reason_codes": sorted({reason for item in reports for reason in item.reason_codes}),
        "quarantined": False,
    }
    return MappingProxyType(totals)


def _canonical_json(value: Any) -> bytes:
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {field.name: _jsonable(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    return value


def _require_text(value: str, name: str) -> None:
    if not value or len(value) > 512:
        raise ValueError(f"{name} must be explicit and bounded")


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
