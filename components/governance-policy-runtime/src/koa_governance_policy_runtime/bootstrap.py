"""Governance Policy Runtime bootstrap and bounded lifecycle orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Mapping

from .config import AuditEvidencePolicy, GovernancePolicyRuntimeConfig
from .health import (
    CheckState,
    ComponentState,
    DependencyState,
    GovernancePolicyHealth,
)
from .receipts import PolicyReceiptFactory


@dataclass(frozen=True, slots=True)
class DependencySnapshot:
    """Explicit startup observations supplied by deployment adapters.

    Boolean values are observations, not permissions. Policy, identity, audit,
    node, and resource authority remain with their owning components.
    """

    identity_and_trust: DependencyState
    audit_broker: DependencyState
    koa_node_agent: DependencyState
    resource_governor: DependencyState
    local_storage_accessible: bool
    receipt_store_accessible: bool
    evaluation_engine_available: bool
    active_policy_set_ref: str | None
    previous_valid_policy_set_ref: str | None
    policy_set_compatible_with_profile: bool
    policy_set_compatible_with_components: bool
    authority_version: str | None
    required_exception_data_resolves: bool
    evaluator_version_compatible: bool
    critical_receipt_path_ready: bool
    bundle_stage_path_ready: bool = False

    @classmethod
    def unavailable(cls) -> DependencySnapshot:
        return cls(
            identity_and_trust=DependencyState.UNKNOWN,
            audit_broker=DependencyState.UNKNOWN,
            koa_node_agent=DependencyState.UNKNOWN,
            resource_governor=DependencyState.UNKNOWN,
            local_storage_accessible=False,
            receipt_store_accessible=False,
            evaluation_engine_available=False,
            active_policy_set_ref=None,
            previous_valid_policy_set_ref=None,
            policy_set_compatible_with_profile=False,
            policy_set_compatible_with_components=False,
            authority_version=None,
            required_exception_data_resolves=False,
            evaluator_version_compatible=False,
            critical_receipt_path_ready=False,
            bundle_stage_path_ready=False,
        )

    @classmethod
    def ready_for_local_evaluation(cls) -> DependencySnapshot:
        """Return explicit development probe observations, never authority."""

        return cls(
            identity_and_trust=DependencyState.AVAILABLE,
            audit_broker=DependencyState.AVAILABLE,
            koa_node_agent=DependencyState.AVAILABLE,
            resource_governor=DependencyState.AVAILABLE,
            local_storage_accessible=True,
            receipt_store_accessible=True,
            evaluation_engine_available=True,
            active_policy_set_ref="policy-set:development-active@1.0.0",
            previous_valid_policy_set_ref="policy-set:development-previous@1.0.0",
            policy_set_compatible_with_profile=True,
            policy_set_compatible_with_components=True,
            authority_version="1.0.0",
            required_exception_data_resolves=True,
            evaluator_version_compatible=True,
            critical_receipt_path_ready=True,
            bundle_stage_path_ready=True,
        )


@dataclass(slots=True)
class GovernancePolicyRuntime:
    config: GovernancePolicyRuntimeConfig
    health: GovernancePolicyHealth
    receipt_factory: PolicyReceiptFactory
    dependencies: DependencySnapshot
    started: bool = False

    def start(self) -> None:
        if self.started:
            return
        self.health.update(
            component_state=ComponentState.STARTING,
            process_responsive=CheckState.PASS,
            profile_ref=self.config.profile_ref,
            offline_governed_operation=self.config.offline_governed_operation,
        )

        dep = self.dependencies
        local_storage = _check(dep.local_storage_accessible)
        receipt_store = _check(dep.receipt_store_accessible)
        trust = _dependency_check(dep.identity_and_trust)
        active_policy = _check(dep.active_policy_set_ref is not None)
        authority = _check(dep.authority_version is not None)
        receipt_path_ready = dep.critical_receipt_path_ready and dep.receipt_store_accessible

        reasons: list[str] = []
        audit_path = dep.audit_broker
        if self.config.audit_evidence_policy is AuditEvidencePolicy.REQUIRED_DELIVERY:
            if audit_path is not DependencyState.AVAILABLE:
                receipt_path_ready = False
                reasons.append("required_audit_delivery_unavailable")
        elif self.config.audit_evidence_policy is AuditEvidencePolicy.LOCAL_BUFFER_PERMITTED:
            if audit_path is not DependencyState.AVAILABLE:
                if dep.receipt_store_accessible:
                    reasons.append("audit_delivery_buffered_locally")
                else:
                    receipt_path_ready = False
                    reasons.append("audit_delivery_and_local_buffer_unavailable")

        healthy = dep.local_storage_accessible and dep.receipt_store_accessible
        ready = all(
            (
                healthy,
                dep.evaluation_engine_available,
                dep.active_policy_set_ref is not None,
                dep.policy_set_compatible_with_profile,
                dep.policy_set_compatible_with_components,
                dep.authority_version is not None,
                dep.identity_and_trust is DependencyState.AVAILABLE,
                dep.required_exception_data_resolves,
                dep.evaluator_version_compatible,
                receipt_path_ready,
            )
        )
        if not healthy:
            component_state = ComponentState.UNAVAILABLE
        elif ready and not reasons:
            component_state = ComponentState.READY
        else:
            component_state = ComponentState.DEGRADED

        self.health.update(
            component_state=component_state,
            local_storage_accessible=local_storage,
            receipt_store_accessible=receipt_store,
            active_policy_set_resolves=active_policy,
            policy_set_compatible_with_profile=_check(
                dep.policy_set_compatible_with_profile
            ),
            policy_set_compatible_with_components=_check(
                dep.policy_set_compatible_with_components
            ),
            authority_version_resolves=authority,
            required_trust_sources_resolve=trust,
            required_exception_data_resolves=_check(
                dep.required_exception_data_resolves
            ),
            evaluator_version_compatible=_check(dep.evaluator_version_compatible),
            critical_receipt_path_ready=_check(receipt_path_ready),
            evaluation_engine_available=dep.evaluation_engine_available,
            bundle_stage_path_ready=(
                dep.bundle_stage_path_ready
                and dep.local_storage_accessible
                and dep.identity_and_trust is DependencyState.AVAILABLE
            ),
            activation_path_state=dep.koa_node_agent,
            audit_path_state=dep.audit_broker,
            resource_peer_state=dep.resource_governor,
            active_policy_set_ref=dep.active_policy_set_ref,
            previous_valid_policy_set_ref=dep.previous_valid_policy_set_ref,
            authority_version=dep.authority_version,
            additional_reasons=tuple(reasons),
        )
        self.started = True

    def stop(self) -> None:
        if not self.started:
            return
        self.health.update(component_state=ComponentState.STOPPING)
        self.started = False
        self.health.update(
            component_state=ComponentState.UNAVAILABLE,
            process_responsive=CheckState.FAIL,
            evaluation_engine_available=False,
        )


def bootstrap(
    *,
    environment: Mapping[str, str] | None = None,
    dependencies: DependencySnapshot | None = None,
) -> GovernancePolicyRuntime:
    """Build and start the runtime without creating adapters or policy authority."""

    config = GovernancePolicyRuntimeConfig.from_environment(environment)
    health = GovernancePolicyHealth(
        runtime_version=config.runtime_version,
        clock=lambda: datetime.now(UTC),
    )
    runtime = GovernancePolicyRuntime(
        config=config,
        health=health,
        receipt_factory=PolicyReceiptFactory(evaluator_version=config.runtime_version),
        dependencies=dependencies or DependencySnapshot.unavailable(),
    )
    runtime.start()
    return runtime


def _check(value: bool) -> CheckState:
    return CheckState.PASS if value else CheckState.FAIL


def _dependency_check(value: DependencyState) -> CheckState:
    if value is DependencyState.AVAILABLE:
        return CheckState.PASS
    if value is DependencyState.UNKNOWN:
        return CheckState.UNKNOWN
    return CheckState.FAIL
