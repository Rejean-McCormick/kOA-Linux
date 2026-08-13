"""Reusable test support for integrations/konnaxion/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from koa_konnaxion_adapter.bootstrap import AdapterConfiguration, DependencyObservation, bootstrap
from koa_konnaxion_adapter.capabilities import CapabilityDeclaration, DependencyState, FailureMode
from koa_konnaxion_adapter.client import AdapterRequest, TransportResponse
from koa_konnaxion_adapter.routes import RouteDeclaration

@dataclass
class FakeTransport:
    response: TransportResponse = field(default_factory=lambda: TransportResponse(status_code=200, payload={'candidate_ref': 'candidate:konnaxion:1'}, remote_reference='konnaxion:request:1'))
    calls: list[AdapterRequest] = field(default_factory=list)
    error: Exception | None = None

    def send(self, request: AdapterRequest) -> TransportResponse:
        self.calls.append(request)
        if self.error is not None:
            raise self.error
        return self.response
