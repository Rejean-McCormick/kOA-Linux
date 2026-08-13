"""Reusable test support for components/resource-governor/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
from koa_resource_governor.api import OPERATIONS, OperationSpec, RequestContext, build_router

def request_for(spec: OperationSpec) -> dict[str, Any]:
    values: dict[str, Any] = {'request_id': f'request:{spec.operation_id}:test', 'envelope_ref': 'resource-envelope:test:1.0.0', 'target_scope': {'kind': 'component', 'identifier': 'sample_component'}, 'requested_activation_time': '2026-08-06T12:00:00Z', 'requesting_actor_ref': 'identity:operator:test', 'workload_owner_ref': 'component:sample_component', 'workload_class': 'background_indexing', 'resource_request': {'cpu': {'millicores': 250}, 'memory': {'MiB': 128}}, 'criticality': 'background', 'priority': 'normal', 'requested_at': '2026-08-06T12:00:00Z', 'observation_id': 'observation:test', 'target_execution_ref': 'execution:test', 'resource_measurements': {'cpu': {'millicores': 120}, 'memory': {'MiB': 96}}, 'observed_at': '2026-08-06T12:01:00Z', 'measurement_source': 'usage-probe:test', 'event_id': 'event:test', 'event_type': 'started', 'occurred_at': '2026-08-06T12:00:30Z', 'command_id': 'command:test', 'queue_item_id': 'queue-item:test', 'view': 'summary'}
    return {field: values[field] for field in spec.required_request_fields}

def response_for(spec: OperationSpec) -> dict[str, Any]:
    values: dict[str, Any] = {'request_id': f'request:{spec.operation_id}:test', 'activation_state': 'active', 'active_envelope_ref': 'resource-envelope:test:1.0.0', 'previous_envelope_ref': 'resource-envelope:test:0.9.0', 'activated_at': '2026-08-06T12:00:01Z', 'receipt_ref': 'receipt:resource:test', 'decision_id': 'decision:test', 'outcome': 'admitted', 'resolved_envelope_refs': ['resource-envelope:test:1.0.0'], 'decision_reason': 'capacity and enforceable limits are available', 'decided_at': '2026-08-06T12:00:01Z', 'observation_id': 'observation:test', 'accepted': True, 'recorded_at': '2026-08-06T12:01:01Z', 'event_id': 'event:test', 'target_execution_ref': 'execution:test', 'recorded_state': 'started', 'binding_id': 'binding:test', 'applied_limits': {'cpu': {'millicores': 250}, 'memory': {'MiB': 128}}, 'lease_or_reservation': {'reservation_id': 'reservation:test'}, 'effective_at': '2026-08-06T12:00:02Z', 'command_id': 'command:test', 'command': 'apply_limits', 'reason': 'admitted workload binding', 'expected_result': 'declared limits are active', 'issued_at': '2026-08-06T12:00:02Z', 'scope': {'kind': 'component', 'identifier': 'sample_component'}, 'pressure_class': 'memory', 'severity': 'warning', 'affected_capabilities': ['background_indexing'], 'active_degradation_actions': ['throttle lower-priority work'], 'occurred_at': '2026-08-06T12:02:00Z', 'queue_item_id': 'queue-item:test', 'workload_request_id': 'request:admit_workload:test', 'state': 'waiting', 'position_or_priority': {'priority': 'normal', 'position': 1}, 'updated_at': '2026-08-06T12:02:00Z', 'health': {'status': 'healthy'}, 'readiness': {'status': 'ready', 'mutation_ready': True}, 'active_envelopes': ['resource-envelope:test:1.0.0'], 'allocation_state': {'active': 1, 'orphaned': 0}, 'queue_state': {'accepted': 1, 'capacity': 10}, 'resource_pressure_state': 'normal', 'degraded_capabilities': [], 'reconciliation_state': {'status': 'reconciled'}}
    return {field: values[field] for field in spec.response_fields}

def headers_for(spec: OperationSpec) -> dict[str, str]:
    headers = {'x-koa-contract-version': '1.0.0', 'x-koa-correlation-id': f'corr:{spec.operation_id}:test'}
    if spec.requires_idempotency_key:
        headers['x-koa-idempotency-key'] = f'idem:{spec.operation_id}:test'
    return headers

@dataclass
class CompleteService:
    calls: list[tuple[str, Mapping[str, Any], RequestContext]] = field(default_factory=list)

    def execute(self, operation_id, payload, context):
        self.calls.append((operation_id, payload, context))
        return response_for(OPERATIONS[operation_id])
