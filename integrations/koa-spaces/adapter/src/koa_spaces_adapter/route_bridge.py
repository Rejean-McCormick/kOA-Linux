"""Presentation-only route composition and capability-aware resolution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from .module_manifest import ValidatedManifest


class RouteCompositionError(ValueError):
    """Raised when independently valid manifests collide after composition."""


class RouteState(StrEnum):
    AVAILABLE = "available"
    CACHED_READ_ONLY = "cached_read_only"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    HIDDEN = "hidden"
    DISABLED = "disabled"
    ACCESS_DENIED = "access_denied"


@dataclass(frozen=True, slots=True)
class RouteDecision:
    route_id: str
    module_id: str
    page_ref: str
    path: str
    state: RouteState
    reason: str | None
    safe_fallback_route_id: str | None
    requires_owner_authorization: bool = True
    authoritative: bool = False

    def __post_init__(self) -> None:
        if self.authoritative:
            raise ValueError("route composition is presentation-only")
        if not self.requires_owner_authorization:
            raise ValueError("route visibility cannot replace owner authorization")


@dataclass(frozen=True, slots=True)
class RouteTable:
    by_id: Mapping[str, Mapping[str, Any]]
    by_path: Mapping[str, str]
    home_by_module: Mapping[str, str]


class RouteBridge:
    """Compose namespaced route contributions without owning page behavior."""

    @staticmethod
    def compose(manifests: Sequence[ValidatedManifest]) -> RouteTable:
        by_id: dict[str, Mapping[str, Any]] = {}
        by_path: dict[str, str] = {}
        homes: dict[str, str] = {}
        modules: set[str] = set()
        for manifest in manifests:
            if manifest.module_id in modules:
                raise RouteCompositionError(f"duplicate module_id {manifest.module_id}")
            modules.add(manifest.module_id)
            doc = manifest.document
            home = str(doc["home_route_id"])
            homes[manifest.module_id] = home
            for route in doc["routes"]:
                route_id = str(route["route_id"])
                if route_id in by_id:
                    raise RouteCompositionError(f"duplicate route_id {route_id}")
                by_id[route_id] = route
                for path in (route["path"], *route.get("aliases", [])):
                    if path in by_path:
                        raise RouteCompositionError(f"path collision: {path}")
                    by_path[str(path)] = route_id
        return RouteTable(
            by_id=MappingProxyType(by_id),
            by_path=MappingProxyType(by_path),
            home_by_module=MappingProxyType(homes),
        )

    @staticmethod
    def resolve(
        table: RouteTable,
        route_or_path: str,
        *,
        granted_capabilities: Iterable[str],
        online: bool,
        enabled_modules: Iterable[str],
        deep_link: bool = False,
    ) -> RouteDecision:
        route_id = table.by_path.get(route_or_path, route_or_path)
        route = table.by_id.get(route_id)
        if route is None:
            raise KeyError(f"unknown route: {route_or_path}")
        module_id = str(route["module_id"])
        fallback = route.get("safe_fallback_route_id")
        if module_id not in set(enabled_modules):
            return RouteDecision(
                route_id=route_id,
                module_id=module_id,
                page_ref=str(route["page_ref"]),
                path=str(route["path"]),
                state=RouteState.UNAVAILABLE,
                reason="module_not_enabled",
                safe_fallback_route_id=fallback,
            )
        if deep_link and route.get("deep_link_allowed", True) is False:
            return RouteDecision(
                route_id=route_id,
                module_id=module_id,
                page_ref=str(route["page_ref"]),
                path=str(route["path"]),
                state=RouteState.ACCESS_DENIED,
                reason="deep_link_prohibited",
                safe_fallback_route_id=fallback,
            )

        required = set(route["capability_policy"]["required_capabilities"])
        missing = required - set(granted_capabilities)
        if missing:
            denied = route["capability_policy"]["denied_behavior"]
            return RouteDecision(
                route_id=route_id,
                module_id=module_id,
                page_ref=str(route["page_ref"]),
                path=str(route["path"]),
                state=RouteState(denied),
                reason="missing_capability:" + ",".join(sorted(missing)),
                safe_fallback_route_id=fallback,
            )

        availability = route["availability"]
        offline = route["offline_behavior"]
        if online and availability == "offline_only":
            state = RouteState.UNAVAILABLE
            reason = "offline_only_route"
        elif not online and availability == "online_only":
            state = RouteState(offline)
            reason = "network_unavailable"
        elif not online:
            state = RouteState(offline)
            reason = None if state is RouteState.AVAILABLE else "offline_behavior"
        else:
            state = RouteState.AVAILABLE
            reason = None
        return RouteDecision(
            route_id=route_id,
            module_id=module_id,
            page_ref=str(route["page_ref"]),
            path=str(route["path"]),
            state=state,
            reason=reason,
            safe_fallback_route_id=fallback,
        )
