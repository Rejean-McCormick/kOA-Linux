from __future__ import annotations

from koa_orgo_adapter import CapabilityState, ClientState, build_adapter


def test_query_unavailability_is_explicit_and_never_fabricates_records(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context, transient_error
):
    transport.fail_with = transient_error
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    outcome = runtime.tasks.query(
        operation_id="orgo.tasks.query",
        criteria={},
        identity_context=identity_context,
        request_id="request-d1",
        correlation_id="corr-d1",
    )
    assert outcome.state is ClientState.UNAVAILABLE
    assert outcome.records == ()
    assert outcome.reason_code == "orgo_timeout"


def test_ambiguous_command_failure_is_indeterminate_not_success(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context, transient_error
):
    transport.fail_with = transient_error
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    outcome = runtime.commands.submit(
        operation_id="orgo.commands.submit",
        command={"opaque_command": "advance"},
        identity_context=identity_context,
        policy_decision={"decision": "allow", "binding": "orgo.commands.submit"},
        resource_admission={"admitted": True, "binding": "orgo.commands.submit"},
        request_id="request-d2",
        correlation_id="corr-d2",
        idempotency_key="idem-d2",
    )
    assert outcome.state is ClientState.INDETERMINATE
    assert outcome.retryable is True
    assert receipt_sink.receipts[-1].execution_state == "unknown_remote_state"


def test_circuit_opens_and_fails_fast_after_bounded_failures(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context, transient_error
):
    transport.fail_with = transient_error
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    for index in range(2):
        runtime.tasks.query(
            operation_id="orgo.tasks.query",
            criteria={"attempt": index},
            identity_context=identity_context,
            request_id=f"request-c{index}",
            correlation_id=f"corr-c{index}",
        )
    call_count = len(transport.calls)
    third = runtime.tasks.query(
        operation_id="orgo.tasks.query",
        criteria={"attempt": 3},
        identity_context=identity_context,
        request_id="request-c3",
        correlation_id="corr-c3",
    )
    assert third.state is ClientState.UNAVAILABLE
    assert third.reason_code == "orgo_circuit_open"
    assert len(transport.calls) == call_count


def test_capabilities_report_degradation_without_substitution(adapter_config, transport, receipt_sink):
    runtime = build_adapter(config=adapter_config, transport=transport, receipt_sink=receipt_sink)
    snapshot = runtime.capabilities.snapshot(integration_enabled=True, health_state="unavailable")
    assert {item.state for item in snapshot} == {CapabilityState.UNAVAILABLE}
    assert all(item.substitute_capability_id is None for item in snapshot)
    assert all(item.authoritative_success_prohibited for item in snapshot)


def test_declared_offline_and_removal_states_are_applied(adapter_config, transport, receipt_sink):
    runtime = build_adapter(config=adapter_config, transport=transport, receipt_sink=receipt_sink)
    offline = runtime.capabilities.snapshot(
        integration_enabled=True, health_state="unavailable", boundary_condition="offline"
    )
    offline_states = {item.capability_id: item.state for item in offline}
    assert offline_states["orgo.surface"] is CapabilityState.DEGRADED
    assert offline_states["orgo.task-read"] is CapabilityState.UNAVAILABLE

    removed = runtime.capabilities.snapshot(
        integration_enabled=True, health_state="healthy", boundary_condition="removed"
    )
    assert {item.state for item in removed} == {CapabilityState.DISABLED}
    assert all(item.substitute_capability_id is None for item in removed)
