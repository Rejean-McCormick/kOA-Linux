from __future__ import annotations

from copy import deepcopy

import pytest

from koa_orgo_adapter import ClientState, TransportResponse, build_adapter


def test_query_forwards_opaque_payload_and_records_receipt(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context
):
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )

    outcome = runtime.tasks.query(
        operation_id="orgo.tasks.query",
        criteria={"filter": {"status": "open"}, "limit": 10},
        identity_context=identity_context,
        request_id="request-1",
        correlation_id="corr-1",
    )

    assert outcome.state is ClientState.SUCCEEDED
    assert outcome.records[0]["opaque_id"] == "task-1"
    assert transport.calls[0]["operation_id"] == "orgo.tasks.query"
    assert transport.calls[0]["payload"] == {"filter": {"status": "open"}, "limit": 10}
    receipt = receipt_sink.receipts[0]
    assert receipt.producer_component_id == "orgo-integration-adapter"
    assert receipt.commit_state == "external_acknowledged"
    assert receipt.evidence["external_acknowledgement_is_local_acceptance"] is False


def test_command_requires_bound_policy_resource_and_idempotency(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context
):
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )

    denied = runtime.commands.submit(
        operation_id="orgo.commands.submit",
        command={"opaque_command": "advance"},
        identity_context=identity_context,
        policy_decision={"decision": "deny", "binding": "orgo.commands.submit"},
        resource_admission={"admitted": True, "binding": "orgo.commands.submit"},
        request_id="request-2",
        correlation_id="corr-2",
        idempotency_key="idem-2",
    )
    assert denied.state is ClientState.REJECTED
    assert denied.reason_code == "explicit_policy_authorization_required"
    assert transport.calls == []

    accepted = runtime.commands.submit(
        operation_id="orgo.commands.submit",
        command={"opaque_command": "advance"},
        identity_context=identity_context,
        policy_decision={"decision": "allow", "binding": "orgo.commands.submit"},
        resource_admission={"admitted": True, "binding": "orgo.commands.submit"},
        request_id="request-3",
        correlation_id="corr-3",
        idempotency_key="idem-3",
    )
    assert accepted.state is ClientState.SUCCEEDED
    assert transport.calls[-1]["idempotency_key"] == "idem-3"


def test_undeclared_operation_and_mode_mismatch_fail_closed(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context
):
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )

    undeclared = runtime.tasks.query(
        operation_id="orgo.internal.magic",
        criteria={},
        identity_context=identity_context,
        request_id="request-4",
        correlation_id="corr-4",
    )
    assert undeclared.state is ClientState.REJECTED
    assert undeclared.reason_code == "undeclared_operation"

    wrong_mode = runtime.tasks.query(
        operation_id="orgo.commands.submit",
        criteria={},
        identity_context=identity_context,
        request_id="request-5",
        correlation_id="corr-5",
    )
    assert wrong_mode.state is ClientState.REJECTED
    assert wrong_mode.reason_code == "operation_mode_mismatch"
    assert transport.calls == []


def test_configuration_rejects_undeclared_capability_operation(adapter_config, transport, receipt_sink):
    broken = deepcopy(adapter_config)
    broken["capabilities"][0]["operation_ids"].append("orgo.hidden.operation")
    with pytest.raises(ValueError, match="undeclared operations"):
        build_adapter(config=broken, transport=transport, receipt_sink=receipt_sink)


def test_cross_domain_publication_must_use_publication_gateway(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context
):
    modified = deepcopy(adapter_config)
    modified["operations"][1]["authority_effect"] = "cross_domain_publication"
    runtime = build_adapter(
        config=modified,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    result = runtime.commands.submit(
        operation_id="orgo.commands.submit",
        command={"public_summary": "not sent"},
        identity_context=identity_context,
        policy_decision={"decision": "allow", "binding": "orgo.commands.submit"},
        resource_admission={"admitted": True, "binding": "orgo.commands.submit"},
        request_id="request-6",
        correlation_id="corr-6",
        idempotency_key="idem-6",
    )
    assert result.state is ClientState.REJECTED
    assert result.reason_code == "publication_gateway_required"
    assert transport.calls == []


def test_receipt_persistence_failure_prevents_success_claim(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context
):
    receipt_sink.fail = True
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    with pytest.raises(RuntimeError, match="orgo_receipt_persistence_failed"):
        runtime.tasks.query(
            operation_id="orgo.tasks.query",
            criteria={},
            identity_context=identity_context,
            request_id="request-7",
            correlation_id="corr-7",
        )


def test_malformed_remote_query_response_is_rejected_and_receipted(
    adapter_config, transport, receipt_sink, receipt_factory, identity_context
):
    transport.response = TransportResponse(
        accepted=True,
        status_code="accepted",
        payload={"records": "not-a-list"},
        remote_reference="orgo-ref-invalid",
    )
    runtime = build_adapter(
        config=adapter_config,
        transport=transport,
        receipt_sink=receipt_sink,
        receipt_factory=receipt_factory,
    )
    result = runtime.tasks.query(
        operation_id="orgo.tasks.query",
        criteria={},
        identity_context=identity_context,
        request_id="request-8",
        correlation_id="corr-8",
    )
    assert result.state is ClientState.UNAVAILABLE
    assert result.reason_code == "orgo_response_contract_invalid"
    assert result.records == ()
    assert receipt_sink.receipts[-1].outcome == "failed"
