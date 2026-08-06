from __future__ import annotations

from datetime import UTC, datetime

from koa_konnaxion_adapter import INTEGRATION_ID, SUBSYSTEM_CONTRACT_VERSION
from koa_konnaxion_adapter.bootstrap import AlignmentState
from koa_konnaxion_adapter.capabilities import CapabilityState
from koa_konnaxion_adapter.client import AdapterRequest, RequestContext


def test_stable_boundary_identity(prepared_runtime):
    assert INTEGRATION_ID == "konnaxion"
    assert SUBSYSTEM_CONTRACT_VERSION == "1.0.0"
    assert prepared_runtime.configuration.alignment_state is AlignmentState.PREPARED_ONLY
    assert prepared_runtime.activable is False


def test_declared_capabilities_are_preserved_without_internal_catalog(runtime):
    ids = tuple(runtime.capabilities.declarations)
    assert ids == (
        "boundary.notifications.read",
        "boundary.publication.request",
        "boundary.routes.read",
    )
    assert all("internal" not in item for item in ids)


def test_transport_acknowledgement_is_candidate_only(runtime):
    request = AdapterRequest(
        operation="boundary.routes.read",
        capability_id="boundary.routes.read",
        context=RequestContext(
            actor_ref="identity:user:1",
            tenant_ref="tenant:local:1",
            purpose="purpose:civic-navigation",
            correlation_id="correlation:1",
            idempotency_key="idempotency:1",
            contract_version="1.0.0",
            identity_verified=True,
            governance_authorized=True,
        ),
        payload={"route_ref": "route:participation"},
    )
    response = runtime.client.invoke(request, observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert response.transport_status == "forwarded"
    assert response.authoritative is False
    assert response.receipt.transfers_authority is False
    assert response.receipt.as_dict()["authoritative_acceptance"] is False


def test_duplicate_effect_is_prevented(runtime):
    request = AdapterRequest(
        operation="boundary.routes.read",
        capability_id="boundary.routes.read",
        context=RequestContext(
            actor_ref="identity:user:1",
            tenant_ref="tenant:local:1",
            purpose="purpose:civic-navigation",
            correlation_id="correlation:2",
            idempotency_key="idempotency:2",
            contract_version="1.0.0",
            identity_verified=True,
            governance_authorized=True,
        ),
        payload={"route_ref": "route:participation"},
    )
    first = runtime.client.invoke(request, observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    second = runtime.client.invoke(request, observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert first.transport_status == "forwarded"
    assert second.transport_status == "duplicate"
    assert second.receipt.outcome.value == "duplicate"
    assert len(runtime.client._transport.calls) == 1
