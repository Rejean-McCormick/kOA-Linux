"""Presentation route declarations; no Konnaxion routing logic is reproduced."""

from __future__ import annotations

from dataclasses import dataclass
import re
from types import MappingProxyType
from typing import Iterable, Mapping

from .capabilities import CapabilitySnapshot


_ID = re.compile(r"^[a-z][a-z0-9_.:-]{2,127}$")
_ALIAS = re.compile(r"^/[A-Za-z0-9][A-Za-z0-9/_-]{0,126}$")


@dataclass(frozen=True, slots=True)
class AuthorityContext:
    actor_ref: str
    tenant_ref: str
    identity_verified: bool
    governance_authorized: bool


@dataclass(frozen=True, slots=True)
class RouteDeclaration:
    alias: str
    operation: str
    capability_id: str
    user_visible: bool = True

    def __post_init__(self) -> None:
        if not _ALIAS.fullmatch(self.alias) or ".." in self.alias or "//" in self.alias:
            raise ValueError("route alias must be an absolute normalized presentation path")
        for name in ("operation", "capability_id"):
            if not _ID.fullmatch(getattr(self, name)):
                raise ValueError(f"{name} must be a stable lowercase identifier")


@dataclass(frozen=True, slots=True)
class RouteResolution:
    alias: str
    operation: str
    capability_id: str
    presentation_only: bool = True
    authoritative: bool = False
    transfers_authority: bool = False


class RouteBridge:
    def __init__(self, declarations: Iterable[RouteDeclaration]) -> None:
        by_alias: dict[str, RouteDeclaration] = {}
        for declaration in declarations:
            if declaration.alias in by_alias:
                raise ValueError(f"duplicate route alias: {declaration.alias}")
            by_alias[declaration.alias] = declaration
        if not by_alias:
            raise ValueError("at least one route declaration is required")
        self._routes = MappingProxyType(dict(sorted(by_alias.items())))

    @property
    def routes(self) -> Mapping[str, RouteDeclaration]:
        return self._routes

    def resolve(
        self,
        alias: str,
        *,
        authority: AuthorityContext,
        capability: CapabilitySnapshot,
    ) -> RouteResolution:
        if not authority.identity_verified:
            raise PermissionError("route resolution requires verified identity")
        if not authority.governance_authorized:
            raise PermissionError("route resolution requires governance authorization")
        try:
            declaration = self._routes[alias]
        except KeyError as exc:
            raise KeyError(f"undeclared route alias: {alias}") from exc
        if declaration.capability_id != capability.capability_id:
            raise ValueError("route capability mismatch")
        if not capability.usable:
            raise RuntimeError(f"route capability is {capability.state.value}")
        return RouteResolution(
            alias=declaration.alias,
            operation=declaration.operation,
            capability_id=declaration.capability_id,
        )
