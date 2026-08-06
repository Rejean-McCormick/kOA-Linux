"""Immutable migration plans and their local invariants."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from hashlib import sha256
import json
import re
from typing import Any, Mapping

_IDENTIFIER = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)+$")
_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def _identifier(value: str, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise ValueError(f"{field} must be a stable lowercase namespaced identifier")
    return value


def _nonempty(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty")
    if value != value.strip():
        raise ValueError(f"{field} must not contain surrounding whitespace")
    return value


def _unique(values: tuple[str, ...], field: str) -> tuple[str, ...]:
    if not values:
        raise ValueError(f"{field} must not be empty")
    if len(values) != len(set(values)):
        raise ValueError(f"{field} must not contain duplicates")
    return values


class MigrationKind(StrEnum):
    SCHEMA = "schema_migration"
    DATA_TRANSFORMATION = "data_transformation"
    STORAGE = "storage_migration"
    OWNERSHIP = "ownership_migration"
    IDENTIFIER = "identifier_migration"
    SECURITY = "security_migration"
    RETENTION = "retention_migration"
    IMPORT = "import_migration"
    REPAIR = "repair_migration"


class ReversibilityClass(StrEnum):
    REVERSIBLE = "reversible"
    CONDITIONALLY_REVERSIBLE = "conditionally_reversible"
    IRREVERSIBLE = "irreversible"


class LifecycleState(StrEnum):
    PROPOSED = "proposed"
    ANALYZED = "analyzed"
    PLANNED = "planned"
    REHEARSED = "rehearsed"
    VALIDATED = "validated"
    STAGED = "staged"
    EXECUTING = "executing"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"
    VERIFYING = "verifying"
    ACCEPTED = "accepted"
    REVERTING = "reverting"
    REPAIRING = "repairing"
    REVERTED = "reverted"
    REPAIRED = "repaired"
    OBSERVED = "observed"
    COMPATIBILITY_CLOSED = "compatibility_closed"
    RETIRED = "retired"


_ALLOWED_TRANSITIONS: Mapping[LifecycleState, frozenset[LifecycleState]] = {
    LifecycleState.PROPOSED: frozenset({LifecycleState.ANALYZED}),
    LifecycleState.ANALYZED: frozenset({LifecycleState.PLANNED}),
    LifecycleState.PLANNED: frozenset({LifecycleState.REHEARSED}),
    LifecycleState.REHEARSED: frozenset({LifecycleState.VALIDATED}),
    LifecycleState.VALIDATED: frozenset({LifecycleState.STAGED}),
    LifecycleState.STAGED: frozenset({LifecycleState.EXECUTING}),
    LifecycleState.EXECUTING: frozenset({LifecycleState.PAUSED, LifecycleState.FAILED, LifecycleState.COMPLETED}),
    LifecycleState.PAUSED: frozenset({LifecycleState.EXECUTING, LifecycleState.FAILED}),
    LifecycleState.FAILED: frozenset({LifecycleState.REVERTING, LifecycleState.REPAIRING, LifecycleState.EXECUTING}),
    LifecycleState.COMPLETED: frozenset({LifecycleState.VERIFYING}),
    LifecycleState.VERIFYING: frozenset({LifecycleState.ACCEPTED, LifecycleState.FAILED, LifecycleState.REVERTING, LifecycleState.REPAIRING}),
    LifecycleState.ACCEPTED: frozenset({LifecycleState.OBSERVED}),
    LifecycleState.REVERTING: frozenset({LifecycleState.REVERTED, LifecycleState.FAILED}),
    LifecycleState.REPAIRING: frozenset({LifecycleState.REPAIRED, LifecycleState.FAILED}),
    LifecycleState.REPAIRED: frozenset({LifecycleState.VERIFYING}),
    LifecycleState.REVERTED: frozenset({LifecycleState.OBSERVED}),
    LifecycleState.OBSERVED: frozenset({LifecycleState.COMPATIBILITY_CLOSED}),
    LifecycleState.COMPATIBILITY_CLOSED: frozenset({LifecycleState.RETIRED}),
    LifecycleState.RETIRED: frozenset(),
}


class PreflightCheck(StrEnum):
    SOURCE_STATE = "source_state"
    TARGET_CAPACITY = "target_capacity"
    FREE_STORAGE = "free_storage"
    RESOURCE_BUDGET = "resource_budget"
    ACTIVE_VERSIONS = "active_versions"
    BACKUP_READINESS = "backup_readiness"
    CREDENTIALS = "credentials"
    KEYS = "keys"
    DEPENDENCIES = "dependencies"
    CONFLICTING_OPERATIONS = "conflicting_operations"


REQUIRED_PREFLIGHT_CHECKS = frozenset(PreflightCheck)


class ValidationPhase(StrEnum):
    PREFLIGHT = "preflight"
    POST_STEP = "post_step"
    CUTOVER = "cutover"
    POST_CUTOVER = "post_cutover"
    ACCEPTANCE = "acceptance"
    OBSERVATION = "observation"


@dataclass(frozen=True, slots=True)
class ContractReference:
    contract_id: str
    version: str
    digest_sha256: str

    def __post_init__(self) -> None:
        _identifier(self.contract_id, "contract_id")
        if not _VERSION.fullmatch(self.version):
            raise ValueError("contract version must be semantic")
        if not _HEX_64.fullmatch(self.digest_sha256):
            raise ValueError("contract digest must be lowercase SHA-256")

    def to_dict(self) -> dict[str, str]:
        return {
            "contract_id": self.contract_id,
            "version": self.version,
            "digest_sha256": self.digest_sha256,
        }


@dataclass(frozen=True, slots=True)
class ReleaseSetReference:
    release_set_id: str
    digest_sha256: str
    compatible_channels: tuple[str, ...]

    def __post_init__(self) -> None:
        _identifier(self.release_set_id, "release_set_id")
        if not _HEX_64.fullmatch(self.digest_sha256):
            raise ValueError("release set digest must be lowercase SHA-256")
        _unique(self.compatible_channels, "compatible_channels")
        canonical = ("system", "services", "governance", "knowledge")
        if self.compatible_channels != canonical:
            raise ValueError("release set compatibility must cover all four channels in canonical order")

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_set_id": self.release_set_id,
            "digest_sha256": self.digest_sha256,
            "compatible_channels": list(self.compatible_channels),
        }


@dataclass(frozen=True, slots=True)
class CompatibilityWindow:
    window_id: str
    permitted_readers: tuple[str, ...]
    permitted_writers: tuple[str, ...]
    authoritative_write_path: str
    read_precedence: str
    conflict_policy: str
    reconciliation_rule: str
    start_condition: str
    end_condition: str
    rollback_boundary: str
    maximum_duration_seconds: int

    def __post_init__(self) -> None:
        _identifier(self.window_id, "window_id")
        _unique(self.permitted_readers, "permitted_readers")
        _unique(self.permitted_writers, "permitted_writers")
        for field in (
            "authoritative_write_path",
            "read_precedence",
            "conflict_policy",
            "reconciliation_rule",
            "start_condition",
            "end_condition",
            "rollback_boundary",
        ):
            _nonempty(getattr(self, field), field)
        if self.maximum_duration_seconds < 1:
            raise ValueError("compatibility window must be bounded")

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_id": self.window_id,
            "permitted_readers": list(self.permitted_readers),
            "permitted_writers": list(self.permitted_writers),
            "authoritative_write_path": self.authoritative_write_path,
            "read_precedence": self.read_precedence,
            "conflict_policy": self.conflict_policy,
            "reconciliation_rule": self.reconciliation_rule,
            "start_condition": self.start_condition,
            "end_condition": self.end_condition,
            "rollback_boundary": self.rollback_boundary,
            "maximum_duration_seconds": self.maximum_duration_seconds,
        }


@dataclass(frozen=True, slots=True)
class OwnershipTransfer:
    source_owner: str
    target_owner: str
    export_interface_id: str
    import_interface_id: str
    acceptance_rule_id: str
    retire_source_after_acceptance: bool = True

    def __post_init__(self) -> None:
        _identifier(self.source_owner, "source_owner")
        _identifier(self.target_owner, "target_owner")
        if self.source_owner == self.target_owner:
            raise ValueError("ownership transfer requires distinct owners")
        _identifier(self.export_interface_id, "export_interface_id")
        _identifier(self.import_interface_id, "import_interface_id")
        _identifier(self.acceptance_rule_id, "acceptance_rule_id")
        if not self.retire_source_after_acceptance:
            raise ValueError("source authority may retire only after explicit target acceptance")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_owner": self.source_owner,
            "target_owner": self.target_owner,
            "export_interface_id": self.export_interface_id,
            "import_interface_id": self.import_interface_id,
            "acceptance_rule_id": self.acceptance_rule_id,
            "retire_source_after_acceptance": self.retire_source_after_acceptance,
        }


@dataclass(frozen=True, slots=True)
class MigrationStep:
    step_id: str
    sequence: int
    authority_owner: str
    interface_id: str
    operation_id: str
    idempotency_key: str
    maximum_work_units: int
    timeout_seconds: int
    retry_limit: int
    terminal_failure_action: str
    cleanup_operation_id: str
    expected_state: str
    operator_decision_required_on_failure: bool = True
    destructive: bool = False
    crosses_rollback_boundary: bool = False
    allows_mixed_state: bool = False

    def __post_init__(self) -> None:
        for field in ("step_id", "authority_owner", "interface_id", "operation_id", "idempotency_key"):
            _identifier(getattr(self, field), field)
        if self.sequence < 1:
            raise ValueError("step sequence must be positive")
        if self.maximum_work_units < 1:
            raise ValueError("maximum_work_units must be positive")
        if self.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be positive")
        if self.retry_limit < 0:
            raise ValueError("retry_limit must be non-negative")
        allowed_failure_actions = {"pause", "quarantine", "rollback", "forward_repair", "restricted_state"}
        if self.terminal_failure_action not in allowed_failure_actions:
            raise ValueError("terminal_failure_action is not supported")
        _identifier(self.cleanup_operation_id, "cleanup_operation_id")
        _nonempty(self.expected_state, "expected_state")

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "sequence": self.sequence,
            "authority_owner": self.authority_owner,
            "interface_id": self.interface_id,
            "operation_id": self.operation_id,
            "idempotency_key": self.idempotency_key,
            "maximum_work_units": self.maximum_work_units,
            "timeout_seconds": self.timeout_seconds,
            "retry_limit": self.retry_limit,
            "terminal_failure_action": self.terminal_failure_action,
            "cleanup_operation_id": self.cleanup_operation_id,
            "expected_state": self.expected_state,
            "operator_decision_required_on_failure": self.operator_decision_required_on_failure,
            "destructive": self.destructive,
            "crosses_rollback_boundary": self.crosses_rollback_boundary,
            "allows_mixed_state": self.allows_mixed_state,
        }


@dataclass(frozen=True, slots=True)
class ValidationRule:
    rule_id: str
    phase: ValidationPhase
    description: str
    required: bool = True

    def __post_init__(self) -> None:
        _identifier(self.rule_id, "rule_id")
        _nonempty(self.description, "description")

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "phase": self.phase.value,
            "description": self.description,
            "required": self.required,
        }


@dataclass(frozen=True, slots=True)
class MigrationPlan:
    migration_id: str
    owning_component: str
    source_contract: ContractReference
    target_contract: ContractReference
    source_release_set: ReleaseSetReference
    target_release_set: ReleaseSetReference
    affected_scope: tuple[str, ...]
    affected_profiles: tuple[str, ...]
    affected_deployments: tuple[str, ...]
    data_classes: tuple[str, ...]
    authority_domains: tuple[str, ...]
    kind: MigrationKind
    reversibility: ReversibilityClass
    execution_mechanism: str
    resource_requirements: tuple[str, ...]
    storage_requirements: tuple[str, ...]
    expected_duration_seconds: int
    checkpoint_interval_units: int
    security_controls: tuple[str, ...]
    operator_roles: tuple[str, ...]
    reviewer_roles: tuple[str, ...]
    test_evidence_references: tuple[str, ...]
    rehearsal_evidence_reference: str
    preflight_checks: tuple[PreflightCheck, ...]
    steps: tuple[MigrationStep, ...]
    validation_rules: tuple[ValidationRule, ...]
    expected_source_fingerprint: str
    expected_target_fingerprint: str
    backup_reference: str | None = None
    restore_procedure_reference: str | None = None
    rollback_boundary_step_id: str | None = None
    forward_repair_reference: str | None = None
    compatibility_window: CompatibilityWindow | None = None
    ownership_transfer: OwnershipTransfer | None = None
    lifecycle_state: LifecycleState = LifecycleState.PLANNED

    def __post_init__(self) -> None:
        _identifier(self.migration_id, "migration_id")
        _identifier(self.owning_component, "owning_component")
        for field in ("affected_scope", "affected_profiles", "affected_deployments", "data_classes",
                      "authority_domains", "resource_requirements", "storage_requirements",
                      "security_controls", "operator_roles", "reviewer_roles", "test_evidence_references"):
            values = _unique(getattr(self, field), field)
            if values != tuple(sorted(values)):
                raise ValueError(f"{field} must use stable lexical order")
        _identifier(self.execution_mechanism, "execution_mechanism")
        _identifier(self.rehearsal_evidence_reference, "rehearsal_evidence_reference")
        if self.expected_duration_seconds < 1:
            raise ValueError("expected_duration_seconds must be positive")
        if self.checkpoint_interval_units < 1:
            raise ValueError("checkpoint_interval_units must be positive")
        if self.source_contract == self.target_contract:
            raise ValueError("source and target contracts must differ")
        if self.preflight_checks != tuple(PreflightCheck):
            raise ValueError("preflight plan must include every canonical check exactly once in canonical order")
        if not self.steps:
            raise ValueError("migration plan must contain at least one step")
        ordered = tuple(sorted(self.steps, key=lambda item: item.sequence))
        if ordered != self.steps or tuple(step.sequence for step in self.steps) != tuple(range(1, len(self.steps) + 1)):
            raise ValueError("steps must have contiguous deterministic sequence numbers")
        for field, values in (
            ("step_id", tuple(step.step_id for step in self.steps)),
            ("idempotency_key", tuple(step.idempotency_key for step in self.steps)),
            ("operation_id", tuple(step.operation_id for step in self.steps)),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"{field} values must be unique")
        if not self.validation_rules:
            raise ValueError("migration plan must define validation rules")
        if len({rule.rule_id for rule in self.validation_rules}) != len(self.validation_rules):
            raise ValueError("validation rule identifiers must be unique")
        required_phases = {ValidationPhase.CUTOVER, ValidationPhase.POST_CUTOVER, ValidationPhase.ACCEPTANCE, ValidationPhase.OBSERVATION}
        actual_phases = {rule.phase for rule in self.validation_rules if rule.required}
        if not required_phases.issubset(actual_phases):
            raise ValueError("required validation must cover cutover, post-cutover, acceptance, and observation")
        if not _HEX_64.fullmatch(self.expected_source_fingerprint):
            raise ValueError("expected source fingerprint must be lowercase SHA-256")
        if not _HEX_64.fullmatch(self.expected_target_fingerprint):
            raise ValueError("expected target fingerprint must be lowercase SHA-256")
        self._validate_ownership()
        self._validate_recovery()
        self._validate_compatibility()

    @property
    def target_owner(self) -> str:
        return self.ownership_transfer.target_owner if self.ownership_transfer else self.owning_component

    def _validate_ownership(self) -> None:
        if self.ownership_transfer is None:
            if self.kind is MigrationKind.OWNERSHIP:
                raise ValueError("ownership migration requires an explicit OwnershipTransfer")
            foreign = [step.step_id for step in self.steps if step.authority_owner != self.owning_component]
            if foreign:
                raise ValueError("migration steps cannot change authority owner implicitly")
            return
        transfer = self.ownership_transfer
        if self.kind is not MigrationKind.OWNERSHIP:
            raise ValueError("OwnershipTransfer is valid only for ownership migrations")
        if transfer.source_owner != self.owning_component:
            raise ValueError("ownership transfer source must be the current owning component")
        allowed = {transfer.source_owner, transfer.target_owner}
        if any(step.authority_owner not in allowed for step in self.steps):
            raise ValueError("ownership transfer step names an undeclared authority owner")

    def _validate_recovery(self) -> None:
        crossing = [step.step_id for step in self.steps if step.crosses_rollback_boundary]
        if self.reversibility in {ReversibilityClass.REVERSIBLE, ReversibilityClass.CONDITIONALLY_REVERSIBLE}:
            if not self.backup_reference or not self.restore_procedure_reference or not self.rollback_boundary_step_id:
                raise ValueError("reversible migrations require backup, restore procedure, and rollback boundary")
            if crossing != [self.rollback_boundary_step_id]:
                raise ValueError("exactly one step must cross the declared rollback boundary")
        else:
            if not self.forward_repair_reference:
                raise ValueError("irreversible migrations require a tested forward-repair reference")
            if self.rollback_boundary_step_id is not None or crossing:
                raise ValueError("irreversible migrations cannot advertise rollback after transformation")

    def _validate_compatibility(self) -> None:
        if any(step.allows_mixed_state for step in self.steps) and self.compatibility_window is None:
            raise ValueError("mixed-state execution requires a bounded compatibility window")
        if self.compatibility_window is not None and not any(step.allows_mixed_state for step in self.steps):
            raise ValueError("compatibility windows must be tied to an explicit mixed-state step")

    def transition(self, target: LifecycleState) -> MigrationPlan:
        allowed = _ALLOWED_TRANSITIONS.get(self.lifecycle_state, frozenset())
        if target not in allowed:
            raise ValueError(f"invalid migration transition: {self.lifecycle_state.value} -> {target.value}")
        return replace(self, lifecycle_state=target)

    def to_dict(self) -> dict[str, Any]:
        return {
            "migration_id": self.migration_id,
            "owning_component": self.owning_component,
            "target_owner": self.target_owner,
            "source_contract": self.source_contract.to_dict(),
            "target_contract": self.target_contract.to_dict(),
            "source_release_set": self.source_release_set.to_dict(),
            "target_release_set": self.target_release_set.to_dict(),
            "affected_scope": list(self.affected_scope),
            "affected_profiles": list(self.affected_profiles),
            "affected_deployments": list(self.affected_deployments),
            "data_classes": list(self.data_classes),
            "authority_domains": list(self.authority_domains),
            "kind": self.kind.value,
            "reversibility": self.reversibility.value,
            "execution_mechanism": self.execution_mechanism,
            "resource_requirements": list(self.resource_requirements),
            "storage_requirements": list(self.storage_requirements),
            "expected_duration_seconds": self.expected_duration_seconds,
            "checkpoint_interval_units": self.checkpoint_interval_units,
            "security_controls": list(self.security_controls),
            "operator_roles": list(self.operator_roles),
            "reviewer_roles": list(self.reviewer_roles),
            "test_evidence_references": list(self.test_evidence_references),
            "rehearsal_evidence_reference": self.rehearsal_evidence_reference,
            "preflight_checks": [check.value for check in self.preflight_checks],
            "steps": [step.to_dict() for step in self.steps],
            "validation_rules": [rule.to_dict() for rule in self.validation_rules],
            "expected_source_fingerprint": self.expected_source_fingerprint,
            "expected_target_fingerprint": self.expected_target_fingerprint,
            "backup_reference": self.backup_reference,
            "restore_procedure_reference": self.restore_procedure_reference,
            "rollback_boundary_step_id": self.rollback_boundary_step_id,
            "forward_repair_reference": self.forward_repair_reference,
            "compatibility_window": self.compatibility_window.to_dict() if self.compatibility_window else None,
            "ownership_transfer": self.ownership_transfer.to_dict() if self.ownership_transfer else None,
            "lifecycle_state": self.lifecycle_state.value,
        }

    @property
    def digest_sha256(self) -> str:
        document = self.to_dict()
        document.pop("lifecycle_state")
        encoded = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        return sha256(encoded).hexdigest()
