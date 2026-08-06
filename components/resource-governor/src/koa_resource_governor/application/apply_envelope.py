"""Validate and apply one resource envelope through the narrow node boundary."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from ..domain import (
    EnvelopeKind,
    EnvelopeStatus,
    Environment,
    OverloadBehavior,
    PriorityClass,
    ResourceDimension,
    ResourceEnvelope,
    ResourceLimit,
)
from ..ports import AuditSink, Clock, NodeAgent, ProfileProvider
from . import (
    Conflict,
    DependencyUnavailable,
    InvalidRequest,
    ReconciliationRequired,
    audit_record,
    limit_values,
    require_text,
    require_utc,
    stable_ref,
    timestamp,
)


@dataclass(frozen=True, slots=True)
class ApplyEnvelopeCommand:
    request_id: str
    correlation_id: str
    envelope_ref: str
    target_scope: str
    target_execution_ref: str
    requested_activation_time: datetime
    requesting_actor_ref: str
    expected_current_state: Mapping[str, object]
    enclosing_envelopes: tuple[ResourceEnvelope, ...] = ()
    policy_decision_ref: str | None = None
    receipt_required: bool = True


@dataclass(frozen=True, slots=True)
class ApplyEnvelopeResult:
    request_id: str
    envelope_ref: str
    envelope_id: str
    binding_id: str
    target_execution_ref: str
    applied_at: datetime
    node_receipt_ref: str | None
    audit_receipt_refs: tuple[str, ...]
    authorizes_business_action: bool = False


class ApplyEnvelope:
    """Apply verified limits without creating profile, policy, or workload authority."""

    operation_id = "apply_resource_envelope"

    def __init__(
        self,
        profiles: ProfileProvider,
        node_agent: NodeAgent,
        clock: Clock,
        audit: AuditSink,
    ) -> None:
        self._profiles = profiles
        self._node_agent = node_agent
        self._clock = clock
        self._audit = audit

    def execute(self, command: ApplyEnvelopeCommand) -> ApplyEnvelopeResult:
        now = require_utc(self._clock.now(), "clock.now")
        requested = require_utc(command.requested_activation_time, "requested_activation_time")
        if requested > now:
            raise InvalidRequest("future activation must be staged by the lifecycle owner")
        request_id = require_text(command.request_id, "request_id")
        correlation_id = require_text(command.correlation_id, "correlation_id")
        envelope_ref = require_text(command.envelope_ref, "envelope_ref")
        target_scope = require_text(command.target_scope, "target_scope")
        target_execution_ref = require_text(command.target_execution_ref, "target_execution_ref")
        require_text(command.requesting_actor_ref, "requesting_actor_ref")
        if not isinstance(command.expected_current_state, Mapping) or not command.expected_current_state:
            raise InvalidRequest("expected_current_state must be a non-empty mapping")

        try:
            profile_document = self._profiles.get_active_profile()
            candidate = _decode_envelope(self._profiles.get_resource_envelope(envelope_ref))
        except (OSError, ValueError, TypeError) as exc:
            raise DependencyUnavailable(
                "profile or resource envelope could not be resolved",
                reason_code="active_envelope_unresolved",
            ) from exc
        profile_refs = _active_profile_refs(profile_document)
        if not profile_refs.intersection(candidate.profile_refs):
            raise Conflict(
                "candidate envelope is incompatible with the active profile",
                reason_code="profile_incompatible",
            )
        accepted_targets = {
            candidate.target_id,
            candidate.target_scope,
            f"{candidate.target_scope}:{candidate.target_id}",
        }
        if target_scope not in accepted_targets:
            raise InvalidRequest("candidate envelope does not match target_scope")
        if not candidate.is_effective_at(now):
            raise Conflict("candidate envelope is not active at the requested time", reason_code="envelope_not_effective")
        parents = tuple(command.enclosing_envelopes)
        parent_ids = {item.envelope_id for item in parents}
        missing = set(candidate.parent_envelope_refs) - parent_ids
        if missing:
            raise DependencyUnavailable(
                "enclosing envelope chain is incomplete",
                reason_code="enclosing_envelope_missing",
            )
        for parent in parents:
            candidate.assert_within(parent)

        requested_receipt = self._audit.record(
            audit_record(
                event_type="envelope_activation_requested",
                correlation_id=correlation_id,
                occurred_at=now,
                payload={
                    "interface_id": "RG-IF-001",
                    "request_id": request_id,
                    "envelope_ref": envelope_ref,
                    "envelope_id": candidate.envelope_id,
                    "target_scope": target_scope,
                    "requesting_actor_ref": command.requesting_actor_ref,
                },
            ),
            required_receipt=command.receipt_required,
        )
        command_id = stable_ref("command", self.operation_id, request_id, candidate.envelope_id)
        control_record = {
            "command_id": command_id,
            "target_execution_ref": target_execution_ref,
            "command": "apply_limits",
            "reason": "resource_envelope_activation",
            "expected_result": "limits_applied",
            "issued_at": timestamp(now),
            "envelope_ref": envelope_ref,
            "applied_limits": limit_values(candidate.limits),
        }
        try:
            raw_result = self._node_agent.apply_resource_control(
                control_record,
                expected_current_state=dict(command.expected_current_state),
                policy_decision_ref=command.policy_decision_ref,
                receipt_required=command.receipt_required,
            )
            status, node_receipt = _control_result(raw_result)
        except Exception as exc:
            raise DependencyUnavailable(
                "resource limits could not be applied by the node boundary",
                reason_code="enforcement_unavailable",
            ) from exc
        if status != "completed":
            raise Conflict(f"node control did not complete: {status}", reason_code="enforcement_not_completed")
        if command.receipt_required and node_receipt is None:
            raise ReconciliationRequired(
                "completed critical node control has no receipt",
                reason_code="node_receipt_missing",
            )
        binding_id = stable_ref("binding", request_id, candidate.envelope_id, target_execution_ref)
        try:
            completed_receipt = self._audit.record(
                audit_record(
                    event_type="envelope_activated",
                    correlation_id=correlation_id,
                    occurred_at=now,
                    payload={
                        "interface_id": "RG-IF-004",
                        "request_id": request_id,
                        "binding_id": binding_id,
                        "envelope_ref": envelope_ref,
                        "target_execution_ref": target_execution_ref,
                        "node_receipt_ref": node_receipt,
                    },
                ),
                required_receipt=command.receipt_required,
            )
        except Exception as exc:
            raise ReconciliationRequired(
                "limits were applied but completion evidence could not be persisted",
                reason_code="activation_receipt_missing",
            ) from exc
        audit_receipts = tuple(item for item in (requested_receipt, completed_receipt) if item)
        return ApplyEnvelopeResult(
            request_id=request_id,
            envelope_ref=envelope_ref,
            envelope_id=candidate.envelope_id,
            binding_id=binding_id,
            target_execution_ref=target_execution_ref,
            applied_at=now,
            node_receipt_ref=node_receipt,
            audit_receipt_refs=audit_receipts,
        )


def _control_result(value: object) -> tuple[str, str | None]:
    if isinstance(value, Mapping):
        status = value.get("status")
        receipt = value.get("receipt_ref")
    else:
        status = getattr(value, "status", None)
        receipt = getattr(value, "receipt_ref", None)
    if not isinstance(status, str):
        raise InvalidRequest("node control returned no status")
    if receipt is not None and not isinstance(receipt, str):
        raise InvalidRequest("node control receipt_ref is invalid")
    return status, receipt


def _active_profile_refs(document: Mapping[str, object]) -> set[str]:
    refs: set[str] = set()
    for key in ("profile_id", "id", "profile_ref"):
        value = document.get(key)
        if isinstance(value, str) and value.strip():
            refs.add(value.strip())
    primary = document.get("primary_profile")
    if isinstance(primary, Mapping):
        for key in ("profile_id", "id", "profile_ref"):
            value = primary.get(key)
            if isinstance(value, str) and value.strip():
                refs.add(value.strip())
    if not refs:
        raise InvalidRequest("active profile has no stable identity")
    return refs


def _decode_envelope(value: ResourceEnvelope | Mapping[str, object]) -> ResourceEnvelope:
    if isinstance(value, ResourceEnvelope):
        return value
    if not isinstance(value, Mapping):
        raise InvalidRequest("resource envelope document must be an object")
    scope = value.get("scope")
    resources = value.get("resources")
    scheduling = value.get("scheduling")
    degradation = value.get("degradation")
    composition = value.get("composition", {})
    if not all(isinstance(item, Mapping) for item in (scope, resources, scheduling, degradation, composition)):
        raise InvalidRequest("resource envelope document lacks canonical sections")
    limits = _decode_limits(resources)
    max_concurrency = _nested_int(resources, "concurrency", "global_max_active", default=1)
    queue_capacity = _queue_capacity(resources)
    retry_limit = _queue_retry_limit(resources)
    return ResourceEnvelope(
        envelope_id=str(value["envelope_id"]),
        version=str(value["version"]),
        status=EnvelopeStatus(str(value["status"])),
        envelope_kind=EnvelopeKind(str(value["envelope_kind"])),
        target_scope=str(scope["target_type"]),
        target_id=str(scope["target_id"]),
        profile_refs=tuple(str(item) for item in scope["profile_ids"]),
        environment=Environment(str(scope["environment"])),
        priority_class=_priority_class(str(scheduling.get("workload_class", "background"))),
        priority=int(scheduling["priority"]),
        limits=limits,
        max_concurrency=max_concurrency,
        queue_capacity=queue_capacity,
        retry_limit=retry_limit,
        overload_behavior=OverloadBehavior(str(degradation["default_behavior"])),
        effective_at=_parse_datetime(value["effective_at"]),
        expires_at=_parse_datetime(value["expires_at"]) if value.get("expires_at") else None,
        parent_envelope_refs=tuple(str(item) for item in composition.get("parent_envelope_ids", ())),
        evidence_refs=tuple(str(item) for item in value.get("evidence_ids", ())),
    )


def _decode_limits(resources: Mapping[str, object]) -> tuple[ResourceLimit, ...]:
    limits: list[ResourceLimit] = []
    cpu = resources.get("cpu")
    if isinstance(cpu, Mapping):
        limits.append(ResourceLimit(ResourceDimension.CPU, "millicores", cpu["reservation_millicores"], cpu["limit_millicores"]))
    memory = resources.get("memory")
    if isinstance(memory, Mapping):
        limits.append(ResourceLimit(ResourceDimension.MEMORY, "bytes", memory["reservation_bytes"], memory["hard_limit_bytes"], memory["soft_limit_bytes"]))
    processes = resources.get("processes")
    if isinstance(processes, Mapping):
        limits.append(ResourceLimit(ResourceDimension.PROCESSES, "processes", 0, processes["max_processes"]))
    if not limits:
        raise InvalidRequest("canonical envelope has no supported enforceable limits")
    return tuple(limits)


def _nested_int(resources: Mapping[str, object], section: str, key: str, *, default: int) -> int:
    value = resources.get(section)
    if not isinstance(value, Mapping):
        return default
    raw = value.get(key, default)
    return int(raw)


def _queue_capacity(resources: Mapping[str, object]) -> int:
    section = resources.get("queues")
    if not isinstance(section, Mapping):
        return 0
    queues = section.get("queues")
    if not isinstance(queues, list):
        return 0
    return min((int(item.get("capacity_items", 0)) for item in queues if isinstance(item, Mapping)), default=0)


def _queue_retry_limit(resources: Mapping[str, object]) -> int:
    section = resources.get("queues")
    if not isinstance(section, Mapping):
        return 0
    queues = section.get("queues")
    if not isinstance(queues, list):
        return 0
    return min((int(item.get("retry_limit", 0)) for item in queues if isinstance(item, Mapping)), default=0)


def _parse_datetime(value: Any) -> datetime:
    if not isinstance(value, str):
        raise InvalidRequest("resource envelope timestamp must be a string")
    return require_utc(datetime.fromisoformat(value.replace("Z", "+00:00")), "resource envelope timestamp")


def _priority_class(workload_class: str) -> PriorityClass:
    return {
        "interactive": PriorityClass.INTERACTIVE,
        "recovery": PriorityClass.CRITICAL_INTEGRITY,
        "maintenance": PriorityClass.OPERATIONAL,
        "background": PriorityClass.BACKGROUND,
        "batch": PriorityClass.HEAVY_BATCH,
        "build": PriorityClass.HEAVY_BATCH,
        "test": PriorityClass.BACKGROUND,
        "media": PriorityClass.HEAVY_BATCH,
        "indexing": PriorityClass.BACKGROUND,
        "backup": PriorityClass.BACKGROUND,
        "restore": PriorityClass.CRITICAL_INTEGRITY,
        "synchronization": PriorityClass.BACKGROUND,
        "migration": PriorityClass.OPERATIONAL,
        "custom": PriorityClass.BEST_EFFORT,
    }.get(workload_class, PriorityClass.BEST_EFFORT)
