from __future__ import annotations

from datetime import UTC, datetime

import pytest

from koa_konnaxion_adapter.bootstrap import AdapterConfiguration, DependencyObservation, bootstrap
from koa_konnaxion_adapter.capabilities import CapabilityState, DependencyState
from koa_konnaxion_adapter.client import AdapterRequest, RequestContext, TransportTimeout, TransportUnavailable
from koa_konnaxion_adapter.routes import RouteDeclaration

from ._support import FakeTransport


def _runtime(declarations, observations, manifests, transport):
    return bootstrap(
        configuration=AdapterConfiguration("konnaxion", "1.0.0", True, True),
        transport=transport,
        dependency_observations=(DependencyObservation(k, v) for k, v in observations.items()),
        capability_declarations=declarations,
        allowed_operations={item.capability_id: item.capability_id for item in declarations},
        route_declarations=(RouteDeclaration("/participation", "boundary.routes.read", "boundary.routes.read"),),
        surface_manifests=manifests,
    )


def _request(key="idempotency:degradation"):
    return AdapterRequest(
        operation="boundary.routes.read",
        capability_id="boundary.routes.read",
        context=RequestContext(
            "identity:user:1", "tenant:local:1", "purpose:civic-navigation",
            "correlation:degradation", key, "1.0.0", True, True,
        ),
        payload={"route_ref": "route:participation"},
    )


def test_external_unavailability_affects_only_declared_capabilities(declarations, observations, manifests):
    observations["konnaxion"] = DependencyState.UNAVAILABLE
    runtime = _runtime(declarations, observations, manifests, FakeTransport())
    snapshots = {item.capability_id: item for item in runtime.capabilities.resolve(runtime.observations)}
    assert all(item.state in {CapabilityState.UNAVAILABLE, CapabilityState.DEFERRED} for item in snapshots.values())
    report = runtime.health(observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert report.state.value == "degraded"
    assert report.healthy is True
    assert report.ready is False


def test_timeout_requires_status_lookup_and_no_blind_retry(declarations, observations, manifests):
    transport = FakeTransport(error=TransportTimeout("timeout"))
    runtime = _runtime(declarations, observations, manifests, transport)
    response = runtime.client.invoke(_request(), observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert response.transport_status == "indeterminate"
    assert response.receipt.reason_code == "timeout_status_lookup_required"
    duplicate = runtime.client.invoke(_request(), observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert duplicate.transport_status == "duplicate"
    assert len(transport.calls) == 1


def test_provider_failure_is_explicit(declarations, observations, manifests):
    transport = FakeTransport(error=TransportUnavailable("down"))
    runtime = _runtime(declarations, observations, manifests, transport)
    response = runtime.client.invoke(_request("idempotency:unavailable"), observed_at=datetime(2026, 8, 6, tzinfo=UTC))
    assert response.transport_status == "unavailable"
    assert response.authoritative is False
    assert response.receipt.reason_code == "external_subsystem_unavailable"


def test_secret_like_payload_is_rejected(runtime):
    request = _request("idempotency:secret")
    request = AdapterRequest(request.operation, request.capability_id, request.context, {"token": "not-allowed"})
    with pytest.raises(ValueError, match="secret-like"):
        runtime.client.invoke(request, observed_at=datetime(2026, 8, 6, tzinfo=UTC))
