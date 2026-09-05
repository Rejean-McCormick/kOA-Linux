"""Validated projection of the presentation shell state."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .client import BoundaryResponseError, SpacesClient

_ALLOWED={"loading","ready","offline","degraded","unavailable","access_denied","error","empty"}
@dataclass(frozen=True,slots=True)
class ShellState:
    state: str
    active_space_id: str|None
    active_module_id: str|None
    active_route_id: str|None
    network_state: str
    reason: str|None

class ShellStateReader:
    def __init__(self, client: SpacesClient): self.client=client
    def read(self) -> ShellState:
        raw=self.client.read_shell_state(); state=raw.get("state")
        if state not in _ALLOWED: raise BoundaryResponseError("invalid shell state")
        net=raw.get("network_state")
        if net not in {"online","offline","unknown"}: raise BoundaryResponseError("invalid network state")
        def opt(name):
            v=raw.get(name)
            if v is not None and not isinstance(v,str): raise BoundaryResponseError(f"{name} must be string or null")
            return v
        return ShellState(state,opt("active_space_id"),opt("active_module_id"),opt("active_route_id"),net,opt("reason"))
