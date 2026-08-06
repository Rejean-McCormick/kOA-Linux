from __future__ import annotations

from koa_ariane_adapter import CapabilityState, ProcessState


def test_optional_voice_failure_does_not_hide_local_navigation(adapter, transport) -> None:
    transport.voice_state = "unavailable"
    report = adapter.health.probe(request_id="health:voice-down")
    assert report.process_state is ProcessState.HEALTHY
    assert report.capabilities.local_navigation.state is CapabilityState.HEALTHY
    assert report.capabilities.external_voice.state is CapabilityState.UNAVAILABLE
    assert report.ready_for_local_navigation is True
    assert report.ready_for_external_voice is False


def test_healthy_voice_is_reported_separately(adapter, transport) -> None:
    transport.voice_state = "healthy"
    report = adapter.health.probe(request_id="health:all-up")
    assert report.ready_for_local_navigation is True
    assert report.ready_for_external_voice is True


def test_transport_failure_produces_explicit_unavailable_health(adapter, transport) -> None:
    transport.fail = ConnectionError("down")
    report = adapter.health.probe(request_id="health:transport-down")
    assert report.process_state is ProcessState.UNAVAILABLE
    assert report.contract_ready is False
    assert report.ready_for_local_navigation is False
    assert report.capabilities.local_navigation.state is CapabilityState.UNAVAILABLE
    assert "ARIANE_TRANSPORT_UNAVAILABLE" in report.reason_codes


def test_unverified_documentation_forces_non_ready_health(operation_map, transport) -> None:
    from koa_ariane_adapter import ArianeAdapterSettings, bootstrap_adapter

    settings = ArianeAdapterSettings(
        subsystem_id="ariane",
        subsystem_contract_version="1.0.0",
        adapter_contract_version="1.0.0",
        operations=operation_map,
        documentation_alignment_verified=False,
    )
    adapter = bootstrap_adapter(settings, transport=transport)
    report = adapter.health.probe(request_id="health:unaligned")
    assert report.contract_ready is False
    assert report.ready_for_local_navigation is False
    assert "ARIANE_DOCUMENTATION_ALIGNMENT_UNVERIFIED" in report.reason_codes


def test_malformed_capability_response_is_explicitly_unavailable(adapter, transport) -> None:
    original_invoke = transport.invoke

    def malformed(operation, payload, *, timeout_seconds):
        response = dict(original_invoke(operation, payload, timeout_seconds=timeout_seconds))
        if operation == "capabilities.read":
            response["payload"] = {"capabilities": {}}
        return response

    transport.invoke = malformed
    report = adapter.health.probe(request_id="health:malformed")
    assert report.ready_for_local_navigation is False
    assert "ARIANE_HEALTH_RESPONSE_INVALID" in report.reason_codes
