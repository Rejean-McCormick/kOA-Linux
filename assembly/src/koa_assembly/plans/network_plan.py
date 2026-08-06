"""Closed-by-default network exposure and public-interface flow plans."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Iterable, Mapping

from .dependency_graph import PlanValidationError, _identifier
from .service_plan import ServicePlan


_VISIBILITIES = frozenset({"unix", "loopback", "lan", "public"})
_PROTOCOLS = frozenset({"http", "https", "grpc", "event", "custom"})
_FORBIDDEN_CROSS_OWNER_PROTOCOLS = frozenset({"sqlite", "postgres", "mysql", "filesystem"})


@dataclass(frozen=True, slots=True)
class NetworkEndpoint:
    endpoint_id: str
    service_id: str
    owner_id: str
    protocol: str
    visibility: str
    interface_id: str
    bind_address: str | None = None
    port: int | None = None
    socket_path: str | None = None

    def __post_init__(self) -> None:
        endpoint_id = _identifier(self.endpoint_id, "endpoint_id")
        service_id = _identifier(self.service_id, "service_id")
        owner_id = _identifier(self.owner_id, "owner_id")
        protocol = _identifier(self.protocol, "protocol")
        visibility = _identifier(self.visibility, "visibility")
        interface_id = _identifier(self.interface_id, "interface_id")
        if protocol not in _PROTOCOLS:
            raise PlanValidationError(f"unsupported network protocol: {protocol}")
        if visibility not in _VISIBILITIES:
            raise PlanValidationError(f"unsupported endpoint visibility: {visibility}")
        if visibility == "unix":
            if self.bind_address is not None or self.port is not None:
                raise PlanValidationError("unix endpoints must not declare bind_address or port")
            if self.socket_path is None:
                raise PlanValidationError("unix endpoint requires socket_path")
            socket_path = _absolute_socket_path(self.socket_path)
        else:
            if self.socket_path is not None:
                raise PlanValidationError("TCP endpoints must not declare socket_path")
            if self.bind_address is None or self.port is None:
                raise PlanValidationError("TCP endpoint requires bind_address and port")
            if not isinstance(self.port, int) or isinstance(self.port, bool) or not 1 <= self.port <= 65535:
                raise PlanValidationError("port must be between 1 and 65535")
            if visibility == "loopback" and self.bind_address not in {"127.0.0.1", "::1"}:
                raise PlanValidationError("loopback endpoint must bind a loopback address")
            if visibility in {"lan", "public"} and self.bind_address in {"127.0.0.1", "::1"}:
                raise PlanValidationError(f"{visibility} endpoint cannot bind only to loopback")
            socket_path = None
        object.__setattr__(self, "endpoint_id", endpoint_id)
        object.__setattr__(self, "service_id", service_id)
        object.__setattr__(self, "owner_id", owner_id)
        object.__setattr__(self, "protocol", protocol)
        object.__setattr__(self, "visibility", visibility)
        object.__setattr__(self, "interface_id", interface_id)
        object.__setattr__(self, "socket_path", socket_path)


@dataclass(frozen=True, slots=True)
class NetworkFlow:
    flow_id: str
    source_service_id: str
    target_endpoint_id: str
    interface_id: str
    required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "flow_id", _identifier(self.flow_id, "flow_id"))
        object.__setattr__(
            self, "source_service_id", _identifier(self.source_service_id, "source_service_id")
        )
        object.__setattr__(
            self, "target_endpoint_id", _identifier(self.target_endpoint_id, "target_endpoint_id")
        )
        object.__setattr__(self, "interface_id", _identifier(self.interface_id, "interface_id"))
        if not isinstance(self.required, bool):
            raise PlanValidationError("flow required flag must be boolean")


class NetworkPlan:
    """A complete endpoint and flow allowlist with default-deny semantics."""

    def __init__(
        self,
        service_plan: ServicePlan,
        endpoints: Iterable[NetworkEndpoint],
        flows: Iterable[NetworkFlow],
        *,
        allow_lan: bool = False,
        allow_public: bool = False,
    ) -> None:
        if not isinstance(service_plan, ServicePlan):
            raise PlanValidationError("service_plan must be a ServicePlan")
        endpoint_map: dict[str, NetworkEndpoint] = {}
        listeners: dict[tuple[object, ...], str] = {}
        for endpoint in endpoints:
            if endpoint.endpoint_id in endpoint_map:
                raise PlanValidationError(f"duplicate network endpoint: {endpoint.endpoint_id}")
            if endpoint.service_id not in service_plan.active_services:
                raise PlanValidationError(f"endpoint references inactive service: {endpoint.service_id}")
            expected_owner = service_plan.owner_of(endpoint.service_id)
            if endpoint.owner_id != expected_owner:
                raise PlanValidationError(
                    f"network owner mismatch for {endpoint.endpoint_id}: "
                    f"expected {expected_owner}, got {endpoint.owner_id}"
                )
            if endpoint.visibility == "lan" and not allow_lan:
                raise PlanValidationError(f"LAN exposure is not allowed: {endpoint.endpoint_id}")
            if endpoint.visibility == "public" and not allow_public:
                raise PlanValidationError(f"public exposure is not allowed: {endpoint.endpoint_id}")
            listener = (
                ("unix", endpoint.socket_path)
                if endpoint.visibility == "unix"
                else ("tcp", endpoint.bind_address, endpoint.port)
            )
            if listener in listeners:
                raise PlanValidationError(
                    f"listener collision between {listeners[listener]} and {endpoint.endpoint_id}"
                )
            listeners[listener] = endpoint.endpoint_id
            endpoint_map[endpoint.endpoint_id] = endpoint

        flow_map: dict[str, NetworkFlow] = {}
        for flow in flows:
            if flow.flow_id in flow_map:
                raise PlanValidationError(f"duplicate network flow: {flow.flow_id}")
            if flow.source_service_id not in service_plan.active_services:
                raise PlanValidationError(
                    f"flow references inactive source service: {flow.source_service_id}"
                )
            target = endpoint_map.get(flow.target_endpoint_id)
            if target is None:
                raise PlanValidationError(
                    f"flow {flow.flow_id} references unknown endpoint {flow.target_endpoint_id}"
                )
            if flow.interface_id != target.interface_id:
                raise PlanValidationError(
                    f"flow {flow.flow_id} interface does not match endpoint contract"
                )
            if target.protocol in _FORBIDDEN_CROSS_OWNER_PROTOCOLS:
                raise PlanValidationError("direct data-store protocols are not valid public interfaces")
            flow_map[flow.flow_id] = flow
        self._endpoints = MappingProxyType(dict(sorted(endpoint_map.items())))
        self._flows = MappingProxyType(dict(sorted(flow_map.items())))
        self._allow_lan = allow_lan
        self._allow_public = allow_public

    @property
    def endpoints(self) -> Mapping[str, NetworkEndpoint]:
        return self._endpoints

    @property
    def flows(self) -> Mapping[str, NetworkFlow]:
        return self._flows

    def to_dict(self) -> dict[str, object]:
        return {
            "default_ingress": "deny",
            "default_egress": "deny",
            "allow_lan": self._allow_lan,
            "allow_public": self._allow_public,
            "endpoints": [
                {
                    "endpoint_id": item.endpoint_id,
                    "service_id": item.service_id,
                    "owner_id": item.owner_id,
                    "protocol": item.protocol,
                    "visibility": item.visibility,
                    "interface_id": item.interface_id,
                    "bind_address": item.bind_address,
                    "port": item.port,
                    "socket_path": item.socket_path,
                }
                for item in self._endpoints.values()
            ],
            "flows": [
                {
                    "flow_id": item.flow_id,
                    "source_service_id": item.source_service_id,
                    "target_endpoint_id": item.target_endpoint_id,
                    "interface_id": item.interface_id,
                    "required": item.required,
                }
                for item in self._flows.values()
            ],
        }


def _absolute_socket_path(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise PlanValidationError("socket_path must be a non-empty string")
    path = PurePosixPath(value)
    if not path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise PlanValidationError(f"socket_path must be normalized and absolute: {value}")
    normalized = str(path)
    if normalized != value or normalized == "/":
        raise PlanValidationError(f"socket_path must be normalized and non-root: {value}")
    return normalized
