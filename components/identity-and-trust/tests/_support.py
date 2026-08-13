"""Reusable test support for components/identity-and-trust/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
COMPONENT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = COMPONENT_ROOT.parents[1]
SOURCE_ROOT = COMPONENT_ROOT / 'src'
from koa_identity_and_trust.api import CONTRACT_VERSION, RequestContext, build_router

def representative_value(field_name: str, operation_id: str) -> Any:
    if field_name in {'presented_factors', 'evidence_refs', 'active_root_refs', 'applied_changes', 'degraded_capabilities'}:
        return []
    if field_name in {'public_attributes', 'assurance_context', 'validated_scope', 'scope', 'validity', 'requester_context', 'authentication_context', 'presented_credential', 'credential', 'signature', 'expected_scope'}:
        return {'purpose': 'test', 'operation_id': operation_id}
    if field_name in {'current_sequence', 'previous_sequence', 'active_sequence', 'active_trust_contexts'}:
        return 1
    if field_name in {'health', 'readiness', 'rotation_status', 'offline_update_status', 'revocation_freshness'}:
        return 'healthy'
    if field_name == 'identity_result':
        return 'established'
    if field_name == 'trust_result':
        return 'trusted'
    if field_name == 'verification_result':
        return 'trusted'
    if field_name in {'status', 'resulting_status'}:
        return 'active'
    if field_name == 'reason_code':
        return 'verified'
    if field_name.endswith('_at') or field_name in {'expires_at', 'valid_until'}:
        return '2030-01-01T00:00:00Z'
    return f'{field_name}:{operation_id}:test'

def request_for(spec) -> dict[str, Any]:
    return {name: representative_value(name, spec.operation_id) for name in spec.request_fields}

def response_for(spec) -> dict[str, Any]:
    return {name: representative_value(name, spec.operation_id) for name in spec.response_fields}

def headers_for(spec, *, correlation_id: str | None=None) -> dict[str, str]:
    headers = {'x-koa-contract-version': CONTRACT_VERSION, 'x-koa-correlation-id': correlation_id or f'corr:{spec.operation_id}:test'}
    if spec.requires_idempotency_key:
        headers['x-koa-idempotency-key'] = f'idem:{spec.operation_id}:test'
    return headers

@dataclass
class FakeService:
    responses: dict[str, Mapping[str, Any]]
    calls: list[tuple[str, Mapping[str, Any], RequestContext]] = field(default_factory=list)

    def execute(self, operation_id, payload, context):
        self.calls.append((operation_id, dict(payload), context))
        return dict(self.responses[operation_id])
