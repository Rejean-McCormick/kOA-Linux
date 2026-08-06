from __future__ import annotations

from koa_orgo_adapter import HealthState, ReadinessState, build_adapter


def test_healthy_probe_is_ready(adapter_config, transport, receipt_sink):
    runtime = build_adapter(config=adapter_config, transport=transport, receipt_sink=receipt_sink)
    report = runtime.health.check(enabled=True)
    assert report.health_state is HealthState.HEALTHY
    assert report.readiness_state is ReadinessState.READY
    assert report.compatible is True
    assert report.authoritative_success_prohibited is True


def test_incompatible_or_degraded_probe_is_not_ready(adapter_config, transport, receipt_sink):
    transport.health_response = {
        "provider_state": "healthy",
        "ready": True,
        "contract_version": "2.0.0",
        "details": {},
    }
    runtime = build_adapter(config=adapter_config, transport=transport, receipt_sink=receipt_sink)
    report = runtime.health.check(enabled=True)
    assert report.health_state is HealthState.DEGRADED
    assert report.readiness_state is ReadinessState.NOT_READY
    assert report.reason_code == "orgo_contract_incompatible"


def test_disabled_integration_is_not_probed(adapter_config, transport, receipt_sink):
    runtime = build_adapter(config=adapter_config, transport=transport, receipt_sink=receipt_sink)
    report = runtime.health.check(enabled=False)
    assert report.health_state is HealthState.DISABLED
    assert report.readiness_state is ReadinessState.DISABLED
    assert transport.probes == []
