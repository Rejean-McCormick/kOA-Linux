from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from koa_konnaxion_adapter.bootstrap import AdapterConfiguration, DependencyObservation, bootstrap
from koa_konnaxion_adapter.capabilities import CapabilityDeclaration, DependencyState, FailureMode
from koa_konnaxion_adapter.client import AdapterRequest, TransportResponse
from koa_konnaxion_adapter.routes import RouteDeclaration


@dataclass
class FakeTransport:
    response: TransportResponse = field(
        default_factory=lambda: TransportResponse(
            status_code=200,
            payload={"candidate_ref": "candidate:konnaxion:1"},
            remote_reference="konnaxion:request:1",
        )
    )
    calls: list[AdapterRequest] = field(default_factory=list)
    error: Exception | None = None

    def send(self, request: AdapterRequest) -> TransportResponse:
        self.calls.append(request)
        if self.error is not None:
            raise self.error
        return self.response


@pytest.fixture
def declarations():
    # Synthetic boundary declarations; they are not claims about Konnaxion internals.
    return (
        CapabilityDeclaration(
            "boundary.routes.read",
            ("konnaxion", "boundary_contract", "official_documentation_alignment", "identity_and_trust", "governance_policy_runtime"),
            ("audit_broker",),
            FailureMode.UNAVAILABLE,
            True,
        ),
        CapabilityDeclaration(
            "boundary.notifications.read",
            ("konnaxion", "boundary_contract", "official_documentation_alignment", "identity_and_trust"),
            ("audit_broker",),
            FailureMode.UNAVAILABLE,
            True,
        ),
        CapabilityDeclaration(
            "boundary.publication.request",
            (
                "konnaxion",
                "boundary_contract",
                "identity_and_trust",
                "governance_policy_runtime",
                "publication_gateway",
                "official_documentation_alignment",
            ),
            ("audit_broker", "resource_governor"),
            FailureMode.DEFERRED,
            True,
        ),
    )


@pytest.fixture
def observations():
    return {
        "audit_broker": DependencyState.AVAILABLE,
        "boundary_contract": DependencyState.AVAILABLE,
        "governance_policy_runtime": DependencyState.AVAILABLE,
        "identity_and_trust": DependencyState.AVAILABLE,
        "konnaxion": DependencyState.AVAILABLE,
        "official_documentation_alignment": DependencyState.AVAILABLE,
        "publication_gateway": DependencyState.AVAILABLE,
        "resource_governor": DependencyState.AVAILABLE,
    }


@pytest.fixture
def manifests():
    return {
        "module-interface": {"version": "1.0.0", "module_ref": "module:konnaxion"},
        "sidebar": {"version": "1.0.0", "entries": [{"route": "/participation"}]},
        "widgets": {"version": "1.0.0", "widgets": []},
    }


@pytest.fixture
def runtime(declarations, observations, manifests):
    transport = FakeTransport()
    result = bootstrap(
        configuration=AdapterConfiguration(
            integration_id="konnaxion",
            subsystem_contract_version="1.0.0",
            official_documentation_mounted=True,
            official_alignment_verified=True,
        ),
        transport=transport,
        dependency_observations=(DependencyObservation(k, v) for k, v in observations.items()),
        capability_declarations=declarations,
        allowed_operations={
            "boundary.notifications.read": "boundary.notifications.read",
            "boundary.publication.request": "boundary.publication.request",
            "boundary.routes.read": "boundary.routes.read",
        },
        route_declarations=(
            RouteDeclaration("/participation", "boundary.routes.read", "boundary.routes.read"),
        ),
        surface_manifests=manifests,
    )
    return result


@pytest.fixture
def prepared_runtime(declarations, observations, manifests):
    prepared = dict(observations)
    prepared["official_documentation_alignment"] = DependencyState.UNKNOWN
    return bootstrap(
        configuration=AdapterConfiguration(
            integration_id="konnaxion",
            subsystem_contract_version="1.0.0",
            official_documentation_mounted=False,
            official_alignment_verified=False,
        ),
        transport=FakeTransport(),
        dependency_observations=(DependencyObservation(k, v) for k, v in prepared.items()),
        capability_declarations=declarations,
        allowed_operations={
            "boundary.notifications.read": "boundary.notifications.read",
            "boundary.publication.request": "boundary.publication.request",
            "boundary.routes.read": "boundary.routes.read",
        },
        route_declarations=(
            RouteDeclaration("/participation", "boundary.routes.read", "boundary.routes.read"),
        ),
        surface_manifests=manifests,
    )
