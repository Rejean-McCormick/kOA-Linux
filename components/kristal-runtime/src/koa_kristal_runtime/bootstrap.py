"""Kristal Runtime bootstrap using explicit non-authoritative observations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Mapping

from .config import EvidencePolicy, KristalRuntimeConfig
from .health import CheckState, DependencyState, KristalRuntimeHealth, RuntimeState
from .receipts import KristalReceiptFactory


@dataclass(frozen=True, slots=True)
class DependencySnapshot:
    """Explicit probe results supplied by deployment adapters.

    These observations are not identity assertions, authorizations, resource
    grants, release-channel decisions, or evidence-custody acknowledgements.
    """

    identity_and_trust: DependencyState
    resource_governor: DependencyState
    governance_policy_runtime: DependencyState
    audit_broker: DependencyState
    process_responsive: bool
    local_state_accessible: bool
    active_record_accessible: bool
    receipt_store_accessible: bool
    profile_membership_resolved: bool
    artifact_contracts_resolved: bool
    knowledge_release_channel_resolved: bool
    interface_version_compatible: bool
    runtime_state_resolved: bool
    canonical_content_resolver_available: bool
    validation_engine_available: bool
    activation_executor_available: bool
    rollback_executor_available: bool
    active_runtime_pack_ref: str | None
    last_valid_runtime_pack_ref: str | None
    revocation_freshness_ref: str | None
    runtime_state: RuntimeState
    durable_local_evidence_ready: bool
    bounded_evidence_queue_ready: bool

    @classmethod
    def unavailable(cls) -> "DependencySnapshot":
        return cls(
            identity_and_trust=DependencyState.UNKNOWN,
            resource_governor=DependencyState.UNKNOWN,
            governance_policy_runtime=DependencyState.UNKNOWN,
            audit_broker=DependencyState.UNKNOWN,
            process_responsive=True,
            local_state_accessible=False,
            active_record_accessible=False,
            receipt_store_accessible=False,
            profile_membership_resolved=False,
            artifact_contracts_resolved=False,
            knowledge_release_channel_resolved=False,
            interface_version_compatible=False,
            runtime_state_resolved=False,
            canonical_content_resolver_available=False,
            validation_engine_available=False,
            activation_executor_available=False,
            rollback_executor_available=False,
            active_runtime_pack_ref=None,
            last_valid_runtime_pack_ref=None,
            revocation_freshness_ref=None,
            runtime_state=RuntimeState.BLOCKED,
            durable_local_evidence_ready=False,
            bounded_evidence_queue_ready=False,
        )

    @classmethod
    def ready_for_local_probe(cls) -> "DependencySnapshot":
        """Return development-only observations without creating authority."""
        return cls(
            identity_and_trust=DependencyState.AVAILABLE,
            resource_governor=DependencyState.AVAILABLE,
            governance_policy_runtime=DependencyState.AVAILABLE,
            audit_broker=DependencyState.AVAILABLE,
            process_responsive=True,
            local_state_accessible=True,
            active_record_accessible=True,
            receipt_store_accessible=True,
            profile_membership_resolved=True,
            artifact_contracts_resolved=True,
            knowledge_release_channel_resolved=True,
            interface_version_compatible=True,
            runtime_state_resolved=True,
            canonical_content_resolver_available=True,
            validation_engine_available=True,
            activation_executor_available=True,
            rollback_executor_available=True,
            active_runtime_pack_ref="runtime-pack:development-active@1.0.0",
            last_valid_runtime_pack_ref="runtime-pack:development-previous@1.0.0",
            revocation_freshness_ref="revocation-epoch:development",
            runtime_state=RuntimeState.ACTIVE,
            durable_local_evidence_ready=True,
            bounded_evidence_queue_ready=True,
        )


@dataclass(slots=True)
class KristalRuntime:
    config: KristalRuntimeConfig
    health: KristalRuntimeHealth
    receipt_factory: KristalReceiptFactory
    dependencies: DependencySnapshot
    started: bool = False

    def start(self) -> None:
        if self.started:
            return
        dep = self.dependencies
        evidence_ready, evidence_reason = _evidence_state(self.config.audit_evidence_policy, dep)
        reasons = [] if evidence_reason is None else [evidence_reason]
        if dep.runtime_state is RuntimeState.ACTIVE and dep.active_runtime_pack_ref is None:
            reasons.append("active_state_without_active_runtime_pack_ref")
        runtime_state = dep.runtime_state
        if not dep.local_state_accessible or not dep.active_record_accessible:
            runtime_state = RuntimeState.FAILED
        elif reasons and runtime_state is RuntimeState.ACTIVE:
            runtime_state = RuntimeState.DEGRADED
        self.health.update(
            runtime_state=runtime_state,
            process_responsive=_check(dep.process_responsive),
            local_state_accessible=_check(dep.local_state_accessible),
            active_record_accessible=_check(dep.active_record_accessible),
            receipt_store_accessible=_check(dep.receipt_store_accessible),
            profile_membership_resolves=_check(dep.profile_membership_resolved),
            artifact_contracts_resolve=_check(dep.artifact_contracts_resolved),
            knowledge_release_channel_resolves=_check(dep.knowledge_release_channel_resolved),
            interface_version_compatible=_check(dep.interface_version_compatible),
            runtime_state_resolves=_check(dep.runtime_state_resolved),
            evidence_path_resolves=_check(evidence_ready),
            canonical_content_resolver_available=dep.canonical_content_resolver_available,
            validation_engine_available=dep.validation_engine_available,
            activation_executor_available=dep.activation_executor_available,
            rollback_executor_available=dep.rollback_executor_available,
            active_runtime_pack_ref=dep.active_runtime_pack_ref,
            last_valid_runtime_pack_ref=dep.last_valid_runtime_pack_ref,
            profile_ref=self.config.profile_ref,
            revocation_freshness_ref=dep.revocation_freshness_ref,
            identity_and_trust=dep.identity_and_trust,
            resource_governor=dep.resource_governor,
            governance_policy_runtime=dep.governance_policy_runtime,
            audit_broker=dep.audit_broker,
            trust_validation_required=self.config.trust_validation_required,
            offline_operation=self.config.offline_operation,
            additional_reasons=tuple(reasons),
        )
        self.started = True

    def stop(self) -> None:
        if not self.started:
            return
        self.started = False
        self.health.update(
            runtime_state=RuntimeState.INACTIVE,
            process_responsive=CheckState.FAIL,
            canonical_content_resolver_available=False,
            validation_engine_available=False,
            activation_executor_available=False,
            rollback_executor_available=False,
            additional_reasons=("runtime_stopped",),
        )


def bootstrap(*, environment: Mapping[str, str] | None = None, dependencies: DependencySnapshot | None = None) -> KristalRuntime:
    config = KristalRuntimeConfig.from_environment(environment)
    health = KristalRuntimeHealth(runtime_version=config.runtime_version, clock=lambda: datetime.now(UTC))
    runtime = KristalRuntime(
        config=config,
        health=health,
        receipt_factory=KristalReceiptFactory(runtime_version=config.runtime_version),
        dependencies=dependencies or DependencySnapshot.unavailable(),
    )
    runtime.start()
    return runtime


def _check(value: bool) -> CheckState:
    return CheckState.PASS if value else CheckState.FAIL


def _evidence_state(policy: EvidencePolicy, dep: DependencySnapshot) -> tuple[bool, str | None]:
    if policy is EvidencePolicy.SYNCHRONOUS_REQUIRED:
        ready = dep.receipt_store_accessible and dep.durable_local_evidence_ready and dep.audit_broker is DependencyState.AVAILABLE
        return ready, None if ready else "required_synchronous_evidence_path_unavailable"
    ready = dep.receipt_store_accessible and (dep.audit_broker is DependencyState.AVAILABLE or dep.bounded_evidence_queue_ready)
    if ready and dep.audit_broker is not DependencyState.AVAILABLE:
        return True, "evidence_forwarding_queued_within_bound"
    return ready, None if ready else "bounded_evidence_path_unavailable"
