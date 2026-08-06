from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from koa_assembly.plans import (  # noqa: E402
    NetworkEndpoint,
    NetworkFlow,
    NetworkPlan,
    PlanValidationError,
    ServiceDependency,
    ServicePlan,
    ServiceSpec,
)


def _services() -> ServicePlan:
    return ServicePlan(
        [
            ServiceSpec(
                "identity",
                "identity-and-trust",
                "identity-and-trust",
                "always_on",
                capabilities=("identity.verify",),
            ),
            ServiceSpec(
                "audit",
                "audit-broker",
                "audit-broker",
                "always_on",
                dependencies=(ServiceDependency("identity", "identity.verify"),),
                capabilities=("audit.submit",),
            ),
            ServiceSpec(
                "publication",
                "publication-gateway",
                "publication-gateway",
                "on_demand",
                dependencies=(ServiceDependency("audit", "audit.submit"),),
                capabilities=("publication.request",),
            ),
            ServiceSpec(
                "optional-ai",
                "external-ai-adapter",
                "external-ai-adapter",
                "disabled",
                enabled=False,
            ),
        ]
    )


def test_service_plan_preserves_owners_and_orders_lifecycle() -> None:
    plan = _services()
    assert plan.startup_order == ("identity", "audit", "publication")
    assert plan.shutdown_order == ("publication", "audit", "identity")
    assert plan.owner_of("audit") == "audit-broker"
    plan.require_capabilities(("identity.verify", "publication.request"))
    with pytest.raises(PlanValidationError, match="unresolved required capabilities"):
        plan.require_capabilities(("unknown.capability",))


def test_required_dependency_cannot_target_disabled_service() -> None:
    with pytest.raises(PlanValidationError, match="requires disabled service"):
        ServicePlan(
            [
                ServiceSpec("disabled", "optional", "optional", "disabled", enabled=False),
                ServiceSpec(
                    "consumer",
                    "consumer",
                    "consumer",
                    "always_on",
                    dependencies=(ServiceDependency("disabled", "optional.api"),),
                ),
            ]
        )


def test_network_plan_is_closed_default_deny_and_owner_preserving() -> None:
    services = _services()
    endpoints = [
        NetworkEndpoint(
            endpoint_id="identity-api",
            service_id="identity",
            owner_id="identity-and-trust",
            protocol="http",
            visibility="unix",
            interface_id="identity.verify",
            socket_path="/run/koa/identity/api.sock",
        ),
        NetworkEndpoint(
            endpoint_id="audit-api",
            service_id="audit",
            owner_id="audit-broker",
            protocol="http",
            visibility="loopback",
            interface_id="audit.submit",
            bind_address="127.0.0.1",
            port=8021,
        ),
    ]
    plan = NetworkPlan(
        services,
        endpoints,
        [
            NetworkFlow("audit-to-identity", "audit", "identity-api", "identity.verify"),
            NetworkFlow("publication-to-audit", "publication", "audit-api", "audit.submit"),
        ],
    )
    rendered = plan.to_dict()
    assert rendered["default_ingress"] == "deny"
    assert rendered["default_egress"] == "deny"
    assert [item["endpoint_id"] for item in rendered["endpoints"]] == [
        "audit-api",
        "identity-api",
    ]

    with pytest.raises(PlanValidationError, match="network owner mismatch"):
        NetworkPlan(
            services,
            [
                NetworkEndpoint(
                    "bad",
                    "identity",
                    "other-owner",
                    "http",
                    "unix",
                    "identity.verify",
                    socket_path="/run/koa/identity/bad.sock",
                )
            ],
            [],
        )


def test_network_plan_rejects_listener_collisions_and_unapproved_exposure() -> None:
    services = _services()
    with pytest.raises(PlanValidationError, match="listener collision"):
        NetworkPlan(
            services,
            [
                NetworkEndpoint(
                    "one",
                    "identity",
                    "identity-and-trust",
                    "http",
                    "loopback",
                    "identity.verify",
                    bind_address="127.0.0.1",
                    port=9000,
                ),
                NetworkEndpoint(
                    "two",
                    "audit",
                    "audit-broker",
                    "http",
                    "loopback",
                    "audit.submit",
                    bind_address="127.0.0.1",
                    port=9000,
                ),
            ],
            [],
        )

    with pytest.raises(PlanValidationError, match="public exposure is not allowed"):
        NetworkPlan(
            services,
            [
                NetworkEndpoint(
                    "public",
                    "identity",
                    "identity-and-trust",
                    "https",
                    "public",
                    "identity.verify",
                    bind_address="0.0.0.0",
                    port=443,
                )
            ],
            [],
        )
