"""Reusable test support for integrations/ariane/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping
ADAPTER_SRC = Path(__file__).resolve().parents[1] / 'adapter' / 'src'
from koa_ariane_adapter import ArianeAdapterSettings, ArianeOperationMap, CapabilityId, ConfirmationBinding, NavigationMode, NavigationRequest, bootstrap_adapter
NOW = datetime(2026, 8, 6, 14, 0, tzinfo=timezone.utc)

class FakeTransport:

    def __init__(self) -> None:
        self.calls: list[tuple[str, Mapping[str, Any], float]] = []
        self.fail: Exception | None = None
        self.voice_state = 'unavailable'
        self.navigation_state = 'planned'
        self.navigation_reason = 'ARIANE_ROUTE_PLANNED'

    def invoke(self, operation: str, payload: Mapping[str, Any], *, timeout_seconds: float) -> Mapping[str, Any]:
        self.calls.append((operation, payload, timeout_seconds))
        if self.fail is not None:
            raise self.fail
        request_id = payload['request_id']
        version = payload['contract_version']
        if operation == 'health.read':
            body: Mapping[str, Any] = {'process_state': 'healthy', 'contract_ready': True, 'observed_at': NOW.isoformat().replace('+00:00', 'Z'), 'reason_codes': []}
        elif operation == 'capabilities.read':
            body = {'capabilities': {CapabilityId.LOCAL_NAVIGATION.value: {'capability_id': CapabilityId.LOCAL_NAVIGATION.value, 'state': 'healthy', 'observed_at': NOW.isoformat().replace('+00:00', 'Z'), 'reason_code': 'OK', 'functions': ['deterministic_commands', 'keyboard_navigation'], 'denied_operations': [], 'dependency_refs': []}, CapabilityId.EXTERNAL_VOICE.value: {'capability_id': CapabilityId.EXTERNAL_VOICE.value, 'state': self.voice_state, 'observed_at': NOW.isoformat().replace('+00:00', 'Z'), 'reason_code': 'OK' if self.voice_state == 'healthy' else 'ARIANE_EXTERNAL_VOICE_UNAVAILABLE', 'functions': ['candidate_command'] if self.voice_state == 'healthy' else [], 'denied_operations': [] if self.voice_state == 'healthy' else ['voice_input'], 'dependency_refs': ['integration:ariane-voice']}}, 'application_capabilities': ['route:read', 'route:execute'], 'atlas_refs': ['atlas.example'], 'driver_refs': ['driver.example']}
        else:
            state = self.navigation_state
            body = {'request_id': request_id, 'state': state, 'reason_code': self.navigation_reason, 'observed_state_ref': 'state:after', 'planned_route_ref': 'route:1', 'verification_ref': 'verification:1' if state == 'completed' else None, 'unavailable_capabilities': []}
        return {'contract_version': version, 'request_id': request_id, 'status': 'ok', 'payload': body}

class FailingVoiceService:

    def interpret(self, request: Any, *, timeout_seconds: float) -> Mapping[str, Any]:
        raise TimeoutError('voice service unavailable')

class CandidateVoiceService:

    def interpret(self, request: Any, *, timeout_seconds: float) -> Mapping[str, Any]:
        return {'candidate_id': 'candidate:voice:1', 'source': 'external_voice', 'application_id': request.application_id, 'goal_id': 'goal.open_settings', 'created_at': NOW.isoformat().replace('+00:00', 'Z'), 'parameters': {'section': 'accessibility'}, 'locale': 'fr-CA'}
