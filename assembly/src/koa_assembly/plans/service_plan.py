"""Closed service plans derived from already-resolved profile membership."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Iterable, Mapping

from .dependency_graph import DependencyGraph, DependencyNode, PlanValidationError, _identifier


_ACTIVATION_MODES = frozenset(
    {
        "always_on",
        "socket_activated",
        "event_activated",
        "task_activated",
        "on_demand",
        "manual",
        "disabled",
    }
)


@dataclass(frozen=True, slots=True)
class ServiceDependency:
    """A service-to-service dependency through a named public interface."""

    service_id: str
    interface_id: str
    required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "service_id", _identifier(self.service_id, "service_id"))
        object.__setattr__(self, "interface_id", _identifier(self.interface_id, "interface_id"))
        if not isinstance(self.required, bool):
            raise PlanValidationError("dependency required flag must be boolean")


@dataclass(frozen=True, slots=True)
class ServiceSpec:
    """One resolved service without renderer-specific details."""

    service_id: str
    component_id: str
    owner_id: str
    activation: str
    dependencies: tuple[ServiceDependency, ...] = field(default_factory=tuple)
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    service_identity: str | None = None
    enabled: bool = True

    def __post_init__(self) -> None:
        service_id = _identifier(self.service_id, "service_id")
        component_id = _identifier(self.component_id, "component_id")
        owner_id = _identifier(self.owner_id, "owner_id")
        activation = _identifier(self.activation, "activation")
        if activation not in _ACTIVATION_MODES:
            raise PlanValidationError(f"unsupported activation mode: {activation}")
        if not isinstance(self.enabled, bool):
            raise PlanValidationError("enabled must be boolean")
        if not self.enabled and activation != "disabled":
            raise PlanValidationError(f"disabled service {service_id} must use activation='disabled'")
        if self.enabled and activation == "disabled":
            raise PlanValidationError(f"enabled service {service_id} cannot use activation='disabled'")
        identity = self.service_identity
        if identity is not None:
            identity = _identifier(identity, "service_identity")
        dependencies = tuple(
            sorted(self.dependencies, key=lambda item: (item.service_id, item.interface_id, item.required))
        )
        keys = [(item.service_id, item.interface_id) for item in dependencies]
        if len(keys) != len(set(keys)):
            raise PlanValidationError(f"duplicate service dependency in {service_id}")
        capabilities = tuple(sorted({_identifier(item, "capability") for item in self.capabilities}))
        object.__setattr__(self, "service_id", service_id)
        object.__setattr__(self, "component_id", component_id)
        object.__setattr__(self, "owner_id", owner_id)
        object.__setattr__(self, "activation", activation)
        object.__setattr__(self, "service_identity", identity)
        object.__setattr__(self, "dependencies", dependencies)
        object.__setattr__(self, "capabilities", capabilities)


class ServicePlan:
    """Validated service membership and deterministic startup/shutdown order."""

    def __init__(self, services: Iterable[ServiceSpec]) -> None:
        by_id: dict[str, ServiceSpec] = {}
        for service in services:
            if service.service_id in by_id:
                raise PlanValidationError(f"duplicate service: {service.service_id}")
            by_id[service.service_id] = service
        if not by_id:
            raise PlanValidationError("service plan must contain at least one service")

        active = {service_id: spec for service_id, spec in by_id.items() if spec.enabled}
        if not active:
            raise PlanValidationError("service plan must contain at least one enabled service")
        for service in active.values():
            for dependency in service.dependencies:
                target = by_id.get(dependency.service_id)
                if target is None:
                    raise PlanValidationError(
                        f"{service.service_id} references unknown service {dependency.service_id}"
                    )
                if dependency.required and not target.enabled:
                    raise PlanValidationError(
                        f"{service.service_id} requires disabled service {dependency.service_id}"
                    )

        graph_nodes = []
        for service in active.values():
            required_dependencies = tuple(
                dependency.service_id
                for dependency in service.dependencies
                if dependency.required and by_id[dependency.service_id].enabled
            )
            graph_nodes.append(
                DependencyNode(
                    node_id=service.service_id,
                    owner_id=service.owner_id,
                    dependencies=required_dependencies,
                    kind="service",
                )
            )
        self._services = MappingProxyType(dict(sorted(by_id.items())))
        self._active = MappingProxyType(dict(sorted(active.items())))
        self._graph = DependencyGraph(graph_nodes)

    @property
    def services(self) -> Mapping[str, ServiceSpec]:
        return self._services

    @property
    def active_services(self) -> Mapping[str, ServiceSpec]:
        return self._active

    @property
    def dependency_graph(self) -> DependencyGraph:
        return self._graph

    @property
    def startup_order(self) -> tuple[str, ...]:
        return self._graph.order

    @property
    def shutdown_order(self) -> tuple[str, ...]:
        return tuple(reversed(self._graph.order))

    @property
    def startup_layers(self) -> tuple[tuple[str, ...], ...]:
        return self._graph.layers

    def require_capabilities(self, required: Iterable[str]) -> None:
        available = {capability for service in self._active.values() for capability in service.capabilities}
        missing = sorted({_identifier(item, "capability") for item in required} - available)
        if missing:
            raise PlanValidationError("unresolved required capabilities: " + ", ".join(missing))

    def owner_of(self, service_id: str) -> str:
        service_id = _identifier(service_id, "service_id")
        try:
            return self._services[service_id].owner_id
        except KeyError as error:
            raise PlanValidationError(f"unknown service: {service_id}") from error

    def to_dict(self) -> dict[str, object]:
        return {
            "services": [
                {
                    "service_id": service.service_id,
                    "component_id": service.component_id,
                    "owner_id": service.owner_id,
                    "service_identity": service.service_identity,
                    "activation": service.activation,
                    "enabled": service.enabled,
                    "capabilities": list(service.capabilities),
                    "dependencies": [
                        {
                            "service_id": dependency.service_id,
                            "interface_id": dependency.interface_id,
                            "required": dependency.required,
                        }
                        for dependency in service.dependencies
                    ],
                }
                for service in self._services.values()
            ],
            "startup_order": list(self.startup_order),
            "shutdown_order": list(self.shutdown_order),
            "startup_layers": [list(layer) for layer in self.startup_layers],
        }
