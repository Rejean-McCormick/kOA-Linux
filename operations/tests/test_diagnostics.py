from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import pytest

from koa_operations.diagnostics import (
    CollectionManifest,
    CollectorDescriptor,
    DiagnosticDataClass,
    DiagnosticSection,
    HealthObservation,
    HealthState,
    QuarantinedDiagnosticError,
    RedactionPolicy,
    SupportCase,
    SupportMode,
    build_support_bundle,
    summarize_health,
)

NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)


def collector(component="audit-broker"):
    return CollectorDescriptor(
        collector_id=f"{component}.health.v1",
        component_id=component,
        version="1.0.0",
        supported_fields=("status", "reason_code", "tenant_id"),
        data_classes=(DiagnosticDataClass.PUBLIC_OPERATIONAL, DiagnosticDataClass.INTERNAL_OPERATIONAL),
        max_records=4,
        max_age_seconds=60,
        redaction_profile="support.default.v1",
    )


def case():
    return SupportCase(
        case_id="case-001",
        requester_id="identity:requester",
        target_refs=("node:alpha",),
        purpose="diagnose bounded health failure",
        mode=SupportMode.BUNDLE_REVIEW,
        scope=("component-health",),
        authority_refs=("decision:support-001",),
        assigned_identities=("identity:collector",),
        expires_at=NOW + timedelta(hours=2),
        evidence_refs=("evidence:case-opened",),
    )


def manifest(max_bytes=50_000):
    return CollectionManifest(
        manifest_id="manifest-001",
        case_id="case-001",
        collector_ids=("audit-broker.health.v1",),
        diagnostic_categories=("health",),
        time_start=NOW - timedelta(minutes=5),
        time_end=NOW,
        component_scope=("audit-broker",),
        tenant_scope=(),
        data_class_ceiling=DiagnosticDataClass.INTERNAL_OPERATIONAL,
        redaction_policy=RedactionPolicy(policy_id="support.default.v1", pseudonymization_context="case-001"),
        max_bundle_bytes=max_bytes,
        intended_recipient="support-team:local",
        retention_seconds=3600,
        required_approvals=("approval:user",),
        approval_refs=("approval:user",),
        cleanup_behavior="delete staging and recipient copy at expiry; preserve case evidence",
        transport_declaration="encrypted local export",
    )


def section(payload=None):
    return DiagnosticSection(
        collector_id="audit-broker.health.v1",
        component_id="audit-broker",
        category="health",
        data_class=DiagnosticDataClass.INTERNAL_OPERATIONAL,
        collected_at=NOW,
        payload=payload or {"status": "degraded", "reason_code": "dependency_unavailable"},
        evidence_refs=("receipt:health-001",),
    )


def test_collector_rejects_wildcard_and_secret_collection():
    with pytest.raises(ValueError):
        CollectorDescriptor(
            collector_id="bad.collector",
            component_id="bad-component",
            version="1",
            supported_fields=("*",),
            data_classes=(DiagnosticDataClass.INTERNAL_OPERATIONAL,),
            max_records=1,
            max_age_seconds=1,
            redaction_profile="default.profile",
        )
    with pytest.raises(ValueError):
        CollectorDescriptor(
            collector_id="bad.collector",
            component_id="bad-component",
            version="1",
            supported_fields=("status",),
            data_classes=(DiagnosticDataClass.SECRET,),
            max_records=1,
            max_age_seconds=1,
            redaction_profile="default.profile",
        )


def test_health_summary_is_bounded_and_stale_fails_closed():
    descriptors = (collector("audit-broker"), collector("identity-and-trust"))
    observations = (
        HealthObservation(
            component_id="audit-broker",
            observed_at=NOW - timedelta(seconds=120),
            state=HealthState.HEALTHY,
            reason_codes=(),
            recent_event_classes=("receipt_buffered",),
        ),
    )
    result = summarize_health(descriptors, observations, now=NOW, max_components=10)
    assert result.state is HealthState.UNKNOWN
    assert result.authoritative is False
    assert {item.component_id for item in result.components} == {"audit-broker", "identity-and-trust"}
    assert all(item.stale for item in result.components)


def test_health_summary_limit_is_explicit():
    result = summarize_health((collector("alpha"), collector("beta")), (), now=NOW, max_components=1)
    assert len(result.components) == 1
    assert result.omitted_components == 1
    assert "component_limit_applied" in result.reason_codes


def test_support_bundle_is_deterministic_minimized_and_non_authoritative():
    first = build_support_bundle(
        case=case(),
        manifest=manifest(),
        sections=(section({"status": "degraded", "tenant_id": "tenant-alpha"}),),
        collectors=(collector(),),
        collector_identity="identity:collector",
        collector_version="1.0.0",
        profile_refs=("profile:sovereign_linux_node",),
        now=NOW,
    )
    second = build_support_bundle(
        case=case(),
        manifest=manifest(),
        sections=(section({"status": "degraded", "tenant_id": "tenant-alpha"}),),
        collectors=(collector(),),
        collector_identity="identity:collector",
        collector_version="1.0.0",
        profile_refs=("profile:sovereign_linux_node",),
        now=NOW,
    )
    assert first.sha256 == second.sha256
    assert first.bundle.authoritative is False
    assert first.bundle.case_id == "case-001"
    body = first.bundle.to_canonical_bytes()
    assert b"tenant-alpha" not in body
    assert json.loads(body)["intended_recipient"] == "support-team:local"


def test_support_bundle_quarantines_suspected_secret():
    with pytest.raises(QuarantinedDiagnosticError) as error:
        build_support_bundle(
            case=case(),
            manifest=manifest(),
            sections=(section({"status": "failed", "password": "do-not-export"}),),
            collectors=(collector(),),
            collector_identity="identity:collector",
            collector_version="1.0.0",
            profile_refs=(),
            now=NOW,
        )
    assert error.value.report.quarantined
    assert "do-not-export" not in repr(error.value.report)


def test_support_bundle_rejects_expired_case_and_wrong_scope():
    expired_case = SupportCase(
        case_id="case-001",
        requester_id="identity:requester",
        target_refs=("node:alpha",),
        purpose="expired",
        mode=SupportMode.BUNDLE_REVIEW,
        scope=("health",),
        authority_refs=("decision:1",),
        assigned_identities=("identity:collector",),
        expires_at=NOW - timedelta(seconds=1),
    )
    with pytest.raises(ValueError, match="expired"):
        build_support_bundle(
            case=expired_case,
            manifest=manifest(),
            sections=(section(),),
            collectors=(collector(),),
            collector_identity="identity:collector",
            collector_version="1",
            profile_refs=(),
            now=NOW,
        )

    outside = DiagnosticSection(
        collector_id="audit-broker.health.v1",
        component_id="other-component",
        category="health",
        data_class=DiagnosticDataClass.INTERNAL_OPERATIONAL,
        collected_at=NOW,
        payload={"status": "healthy"},
    )
    with pytest.raises(ValueError, match="component scope"):
        build_support_bundle(
            case=case(),
            manifest=manifest(),
            sections=(outside,),
            collectors=(collector(),),
            collector_identity="identity:collector",
            collector_version="1",
            profile_refs=(),
            now=NOW,
        )



def test_support_bundle_rejects_undeclared_collector_fields():
    with pytest.raises(ValueError, match="not declared"):
        build_support_bundle(
            case=case(),
            manifest=manifest(),
            sections=(section({"status": "healthy", "internal_database_row": "not allowed"}),),
            collectors=(collector(),),
            collector_identity="identity:collector",
            collector_version="1.0.0",
            profile_refs=(),
            now=NOW,
        )

def test_support_bundle_size_limit_fails_closed():
    with pytest.raises(ValueError, match="maximum size"):
        build_support_bundle(
            case=case(),
            manifest=manifest(max_bytes=10),
            sections=(section(),),
            collectors=(collector(),),
            collector_identity="identity:collector",
            collector_version="1.0.0",
            profile_refs=(),
            now=NOW,
        )
