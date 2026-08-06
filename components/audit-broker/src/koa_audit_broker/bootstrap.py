"""Audit Broker bootstrap and lifecycle orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Mapping

from .config import AuditBrokerConfig
from .health import (
    AuditBrokerHealth,
    ComponentState,
    DependencyState,
    IntegrityAlarmState,
    RetentionJobState,
    StorageCapacityState,
)
from .receipts import AuditReceiptFactory


@dataclass(frozen=True, slots=True)
class DependencySnapshot:
    """Startup dependency states supplied by the deployment boundary."""

    identity_and_trust: DependencyState
    governance_policy_runtime: DependencyState
    record_store_available: bool
    retention_policies_resolvable: bool
    resource_envelope_available: bool
    chain_of_custody_available: bool = True

    @classmethod
    def unavailable(cls) -> DependencySnapshot:
        return cls(
            identity_and_trust=DependencyState.UNKNOWN,
            governance_policy_runtime=DependencyState.UNKNOWN,
            record_store_available=False,
            retention_policies_resolvable=False,
            resource_envelope_available=False,
            chain_of_custody_available=False,
        )


@dataclass(slots=True)
class AuditBrokerRuntime:
    config: AuditBrokerConfig
    health: AuditBrokerHealth
    receipt_factory: AuditReceiptFactory
    dependencies: DependencySnapshot
    started: bool = False

    def start(self) -> None:
        if self.started:
            return
        self.health.update(component_state=ComponentState.STARTING)

        hard_failures: list[str] = []
        if self.dependencies.identity_and_trust is not DependencyState.AVAILABLE:
            hard_failures.append("identity_and_trust_unavailable")
        if not self.dependencies.record_store_available:
            hard_failures.append("record_store_unavailable")
        if not self.dependencies.retention_policies_resolvable:
            hard_failures.append("retention_policies_unresolvable")
        if not self.dependencies.resource_envelope_available:
            hard_failures.append("resource_envelope_unavailable")
        if not self.dependencies.chain_of_custody_available:
            hard_failures.append("chain_of_custody_unavailable")

        policy_state = self.dependencies.governance_policy_runtime
        component_state = ComponentState.READY
        if hard_failures:
            component_state = ComponentState.UNAVAILABLE
        elif policy_state is not DependencyState.AVAILABLE:
            component_state = ComponentState.DEGRADED

        self.health.update(
            component_state=component_state,
            storage_capacity_state=(
                StorageCapacityState.NORMAL
                if self.dependencies.record_store_available
                else StorageCapacityState.UNKNOWN
            ),
            retention_job_state=(
                RetentionJobState.IDLE
                if self.dependencies.retention_policies_resolvable
                else RetentionJobState.BLOCKED
            ),
            policy_path_state=policy_state,
            identity_path_state=self.dependencies.identity_and_trust,
            integrity_alarm_state=(
                IntegrityAlarmState.CLEAR
                if self.dependencies.chain_of_custody_available
                else IntegrityAlarmState.UNKNOWN
            ),
            last_successful_backup_or_recovery_point=self.config.last_recovery_point,
            submission_interface_ready=not hard_failures,
            record_store_ready=self.dependencies.record_store_available,
            chain_of_custody_ready=self.dependencies.chain_of_custody_available,
            receipt_generation_ready=self.dependencies.chain_of_custody_available,
        )
        self.started = True

    def stop(self) -> None:
        if not self.started:
            return
        self.health.update(component_state=ComponentState.STOPPING)
        self.started = False
        self.health.update(component_state=ComponentState.UNAVAILABLE)


def bootstrap(
    *,
    environment: Mapping[str, str] | None = None,
    dependencies: DependencySnapshot | None = None,
) -> AuditBrokerRuntime:
    """Build and start an Audit Broker runtime without creating adapters.

    Deployment code must supply actual dependency observations. Omitting them is
    fail-closed and results in an unavailable runtime rather than guessed readiness.
    """

    config = AuditBrokerConfig.from_environment(environment)
    health = AuditBrokerHealth(clock=lambda: datetime.now(UTC))
    runtime = AuditBrokerRuntime(
        config=config,
        health=health,
        receipt_factory=AuditReceiptFactory(),
        dependencies=dependencies or DependencySnapshot.unavailable(),
    )
    runtime.start()
    return runtime
