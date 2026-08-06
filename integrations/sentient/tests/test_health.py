from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone

from koa_sentient_adapter import HealthState, SentientHealthProbe, bootstrap_adapter

NOW = datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


def test_healthy_probe_reports_candidate_only_capability(adapter) -> None:
    report = adapter.health.probe(now=NOW)
    assert report.state is HealthState.HEALTHY
    assert report.ready is True
    assert report.core_impact == "none"
    assert report.capability_snapshot is not None
    assert report.capability_snapshot.authority_effect == "candidate_input_only"
    assert report.capability_snapshot.default_enabled is False


def test_missing_documentation_mount_blocks_readiness(settings, transport, gateway) -> None:
    blocked = bootstrap_adapter(
        replace(settings, documentation_alignment_verified=False),
        transport=transport,
        owner_gateway=gateway,
    )
    report = blocked.health.probe(now=NOW)
    assert report.state is HealthState.BLOCKED
    assert report.ready is False
    assert report.reason_code == "SENTIENT_DOCUMENTATION_ALIGNMENT_REQUIRED"
    assert transport.calls == []


def test_default_disabled_state_is_explicit(settings, transport, gateway) -> None:
    disabled = bootstrap_adapter(
        replace(settings, enabled=False),
        transport=transport,
        owner_gateway=gateway,
    )
    report = disabled.health.probe(now=NOW)
    assert report.state is HealthState.UNAVAILABLE
    assert report.reason_code == "SENTIENT_DISABLED_BY_DEFAULT"
    assert report.core_impact == "none"


def test_transport_failure_degrades_only_sentient(adapter, transport) -> None:
    transport.failure = ConnectionError("offline")
    report = adapter.health.probe(now=NOW)
    assert report.state is HealthState.UNAVAILABLE
    assert report.ready is False
    assert report.reason_code == "SENTIENT_UNAVAILABLE"
    assert report.core_impact == "none"


def test_malformed_health_is_blocked_not_success(adapter, transport, operation_map) -> None:
    transport.results[operation_map.health]["state"] = "invented_state"
    report = adapter.health.probe(now=NOW)
    assert report.state is HealthState.BLOCKED
    assert report.ready is False
    assert report.reason_code == "SENTIENT_HEALTH_RESPONSE_INVALID"
