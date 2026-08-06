"""Deterministic, fail-closed restore planning.

This module owns operational coordination only.  It never owns component data,
policy, resource admission, privileged execution, or release activation.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import re
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence


class RestorePlanError(ValueError):
    """Raised when a restore request is ambiguous or unsafe."""


class RestoreClass(str, Enum):
    FILE_OR_OBJECT = "file_or_object"
    DATABASE = "database"
    COMPONENT = "component"
    TENANT_OR_DOMAIN = "tenant_or_domain"
    SERVICE_SET = "service_set"
    NODE = "node"
    RELEASE_SET = "release_set"
    SITE_OR_HUB = "site_or_hub"
    OFFLINE = "offline"
    SOVEREIGNTY_OR_EXIT = "sovereignty_or_exit"


class Gate(str, Enum):
    SOURCE = "source"
    ENVIRONMENT = "environment"
    AUTHORITY = "authority"
    DATA = "data"
    CAPABILITY = "capability"
    RECOVERY = "recovery"


RESTORE_EXECUTION_ORDER: tuple[str, ...] = (
    "verify_recovery_source",
    "prepare_recovery_environment",
    "verify_target_profile_and_topology",
    "restore_identity_and_trust",
    "restore_revocation_state",
    "restore_governance_policy",
    "stage_release_sets",
    "stage_system_and_service_artifacts",
    "restore_component_authoritative_data",
    "run_migrations_and_forward_repair",
    "restore_knowledge_and_language_artifacts",
    "rebuild_derived_state",
    "restore_integration_configuration",
)

RESTORE_CLOSURE_ORDER: tuple[str, ...] = (
    "readiness_and_acceptance",
    "traffic_admission",
    "evidence_and_closure",
)

_REQUIRED_GATES = frozenset(Gate)
_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{2,255}$")
_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_SECRET_MARKERS = tuple(
    "-----BEGIN " + prefix + "PRIVATE KEY-----"
    for prefix in ("", "OPENSSH ", "RSA ", "EC ")
)


def _require_id(name: str, value: str) -> str:
    value = value.strip()
    if not _ID_RE.fullmatch(value):
        raise RestorePlanError(f"{name} is missing or is not a stable identifier")
    return value


def _require_text(name: str, value: str, *, maximum: int = 2048) -> str:
    value = value.strip()
    if not value or len(value) > maximum:
        raise RestorePlanError(f"{name} must be non-empty and at most {maximum} characters")
    if any(marker in value for marker in _SECRET_MARKERS):
        raise RestorePlanError(f"{name} contains private key material")
    return value


def _require_digest(name: str, value: str) -> str:
    value = value.strip().lower()
    if not _DIGEST_RE.fullmatch(value):
        raise RestorePlanError(f"{name} must be a sha256 digest")
    return value


def _stable_ids(name: str, values: Iterable[str], *, required: bool = False) -> tuple[str, ...]:
    result = tuple(sorted({_require_id(name, value) for value in values}))
    if required and not result:
        raise RestorePlanError(f"{name} must contain at least one identifier")
    return result


def _stable_refs(name: str, values: Iterable[str], *, required: bool = False) -> tuple[str, ...]:
    cleaned: set[str] = set()
    for value in values:
        ref = _require_text(name, value, maximum=1024)
        if any(character.isspace() for character in ref):
            raise RestorePlanError(f"{name} must not contain whitespace")
        cleaned.add(ref)
    result = tuple(sorted(cleaned))
    if required and not result:
        raise RestorePlanError(f"{name} must contain at least one reference")
    return result


def _stable_mapping(name: str, values: Mapping[str, str], *, required: bool = False) -> Mapping[str, str]:
    cleaned: dict[str, str] = {}
    for key, value in values.items():
        cleaned[_require_id(f"{name}.key", key)] = _require_text(f"{name}[{key}]", value)
    if required and not cleaned:
        raise RestorePlanError(f"{name} must not be empty")
    return MappingProxyType(dict(sorted(cleaned.items())))


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise RestorePlanError("timestamps must be timezone-aware")
    return value.astimezone(timezone.utc).replace(microsecond=0)


def _json_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime):
        return _utc(value).isoformat().replace("+00:00", "Z")
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_json_value(item) for item in value]
    if is_dataclass(value) and not isinstance(value, type):
        return {item.name: _json_value(getattr(value, item.name)) for item in fields(value) if item.init}
    return value


def canonical_json(value: Any) -> str:
    """Return a stable, compact JSON representation."""

    return json.dumps(_json_value(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class Approval:
    approval_id: str
    approver_id: str
    action: str
    decision_ref: str
    expires_at: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "approval_id", _require_id("approval_id", self.approval_id))
        object.__setattr__(self, "approver_id", _require_id("approver_id", self.approver_id))
        object.__setattr__(self, "action", _require_id("approval action", self.action))
        object.__setattr__(self, "decision_ref", _require_id("decision_ref", self.decision_ref))
        object.__setattr__(self, "expires_at", _utc(self.expires_at))


@dataclass(frozen=True, slots=True)
class RestoreScope:
    restore_id: str
    restore_class: RestoreClass
    scenario: str
    owner_id: str
    actor_id: str
    purpose: str
    correlation_id: str
    target_environment_id: str
    effective_profile_id: str
    source_id: str
    active_release_set_id: str
    target_release_set_id: str
    components: tuple[str, ...]
    data_domains: tuple[str, ...]
    tenant_id: str | None = None
    security_domain_id: str | None = None
    expected_data_loss_seconds: int = 0
    expected_downtime_seconds: int = 0
    rpo_seconds: int = 0
    rto_seconds: int = 0
    high_impact_actions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "restore_id",
            "owner_id",
            "actor_id",
            "correlation_id",
            "target_environment_id",
            "effective_profile_id",
            "source_id",
            "active_release_set_id",
            "target_release_set_id",
        ):
            object.__setattr__(self, name, _require_id(name, getattr(self, name)))
        object.__setattr__(self, "scenario", _require_text("scenario", self.scenario))
        object.__setattr__(self, "purpose", _require_text("purpose", self.purpose))
        object.__setattr__(self, "components", _stable_ids("components", self.components, required=True))
        object.__setattr__(self, "data_domains", _stable_ids("data_domains", self.data_domains, required=True))
        object.__setattr__(self, "high_impact_actions", _stable_ids("high_impact_actions", self.high_impact_actions))
        if self.tenant_id is not None:
            object.__setattr__(self, "tenant_id", _require_id("tenant_id", self.tenant_id))
        if self.security_domain_id is not None:
            object.__setattr__(self, "security_domain_id", _require_id("security_domain_id", self.security_domain_id))
        if self.restore_class is RestoreClass.TENANT_OR_DOMAIN and not (self.tenant_id or self.security_domain_id):
            raise RestorePlanError("tenant_or_domain restore requires an explicit tenant or security domain")
        for name in ("expected_data_loss_seconds", "expected_downtime_seconds", "rpo_seconds", "rto_seconds"):
            value = getattr(self, name)
            if not isinstance(value, int) or value < 0:
                raise RestorePlanError(f"{name} must be a non-negative integer")
        if self.expected_data_loss_seconds > self.rpo_seconds:
            raise RestorePlanError("selected recovery point exceeds the declared RPO")
        if self.expected_downtime_seconds > self.rto_seconds:
            raise RestorePlanError("planned recovery duration exceeds the declared RTO")


@dataclass(frozen=True, slots=True)
class RecoverySource:
    source_id: str
    backup_set_id: str
    inventory_digest: str
    release_set_id: str
    profile_id: str
    profile_version: str
    component_versions: Mapping[str, str]
    migration_state: Mapping[str, str]
    trust_state_ref: str
    custody_ref: str
    provenance_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    key_relationship_refs: tuple[str, ...] = ()
    snapshot_set_ids: tuple[str, ...] = ()
    retained_artifact_ids: tuple[str, ...] = ()
    local_closure_refs: tuple[str, ...] = ()
    encrypted: bool = True
    quarantined: bool = True

    def __post_init__(self) -> None:
        for name in ("source_id", "backup_set_id", "release_set_id", "profile_id", "trust_state_ref", "custody_ref"):
            object.__setattr__(self, name, _require_id(name, getattr(self, name)))
        object.__setattr__(self, "inventory_digest", _require_digest("inventory_digest", self.inventory_digest))
        object.__setattr__(self, "profile_version", _require_text("profile_version", self.profile_version))
        object.__setattr__(self, "component_versions", _stable_mapping("component_versions", self.component_versions, required=True))
        object.__setattr__(self, "migration_state", _stable_mapping("migration_state", self.migration_state, required=True))
        for name, required in (
            ("provenance_refs", True),
            ("evidence_refs", True),
            ("key_relationship_refs", False),
            ("snapshot_set_ids", False),
            ("retained_artifact_ids", False),
            ("local_closure_refs", False),
        ):
            object.__setattr__(self, name, _stable_ids(name, getattr(self, name), required=required))
        if not self.quarantined:
            raise RestorePlanError("recovery source must begin in quarantine")


@dataclass(frozen=True, slots=True)
class TargetEnvironment:
    environment_id: str
    profile_id: str
    profile_version: str
    environment_identity_ref: str
    storage_isolated: bool
    network_isolated: bool
    secrets_isolated: bool
    resource_envelope_ref: str
    privileged_boundary_ref: str
    evidence_path_ref: str
    clean: bool = True
    equivalent_isolation_proof_ref: str | None = None
    previous_known_good_ref: str | None = None
    offline_capable: bool = False

    def __post_init__(self) -> None:
        for name in (
            "environment_id",
            "profile_id",
            "environment_identity_ref",
            "resource_envelope_ref",
            "privileged_boundary_ref",
            "evidence_path_ref",
        ):
            object.__setattr__(self, name, _require_id(name, getattr(self, name)))
        object.__setattr__(self, "profile_version", _require_text("profile_version", self.profile_version))
        if self.equivalent_isolation_proof_ref is not None:
            object.__setattr__(
                self,
                "equivalent_isolation_proof_ref",
                _require_id("equivalent_isolation_proof_ref", self.equivalent_isolation_proof_ref),
            )
        if self.previous_known_good_ref is not None:
            object.__setattr__(self, "previous_known_good_ref", _require_id("previous_known_good_ref", self.previous_known_good_ref))
        if not self.clean and not self.equivalent_isolation_proof_ref:
            raise RestorePlanError("in-place target requires explicit equivalent-isolation proof")
        if not all((self.storage_isolated, self.network_isolated, self.secrets_isolated)):
            raise RestorePlanError("restore target must isolate storage, network, and secrets")


@dataclass(frozen=True, slots=True)
class ComponentRestoreSpec:
    component_id: str
    owner_id: str
    restore_contract_ref: str
    data_domains: tuple[str, ...]
    source_version: str
    target_version: str
    migration_contract_ref: str | None = None
    forward_repair_ref: str | None = None
    irreversible_after_checkpoint: str | None = None
    derived_state_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("component_id", "owner_id", "restore_contract_ref"):
            object.__setattr__(self, name, _require_id(name, getattr(self, name)))
        object.__setattr__(self, "data_domains", _stable_ids("component data_domains", self.data_domains, required=True))
        object.__setattr__(self, "source_version", _require_text("source_version", self.source_version))
        object.__setattr__(self, "target_version", _require_text("target_version", self.target_version))
        for name in ("migration_contract_ref", "forward_repair_ref", "irreversible_after_checkpoint"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, _require_id(name, value))
        object.__setattr__(self, "derived_state_ids", _stable_ids("derived_state_ids", self.derived_state_ids))
        if self.source_version != self.target_version and not self.migration_contract_ref:
            raise RestorePlanError(f"{self.component_id} changes version without a migration contract")
        if self.irreversible_after_checkpoint and not self.forward_repair_ref:
            raise RestorePlanError(f"{self.component_id} irreversible migration requires forward repair")


@dataclass(frozen=True, slots=True)
class AcceptanceCheck:
    check_id: str
    gate: Gate
    owner_id: str
    contract_ref: str
    required: bool = True

    def __post_init__(self) -> None:
        for name in ("check_id", "owner_id", "contract_ref"):
            object.__setattr__(self, name, _require_id(name, getattr(self, name)))
        if not self.required:
            raise RestorePlanError("optional checks must not be used to claim restore acceptance")


@dataclass(frozen=True, slots=True)
class RestoreStage:
    ordinal: int
    stage_id: str
    owner_id: str
    contract_refs: tuple[str, ...]
    component_ids: tuple[str, ...] = ()
    resumable: bool = False
    cancellable: bool = True
    mutates_candidate: bool = False

    def __post_init__(self) -> None:
        if self.ordinal < 1:
            raise RestorePlanError("stage ordinal must be positive")
        object.__setattr__(self, "stage_id", _require_id("stage_id", self.stage_id))
        object.__setattr__(self, "owner_id", _require_id("stage owner", self.owner_id))
        object.__setattr__(self, "contract_refs", _stable_refs("stage contract_refs", self.contract_refs, required=True))
        object.__setattr__(self, "component_ids", _stable_ids("stage component_ids", self.component_ids))

    @property
    def stage_digest(self) -> str:
        return canonical_digest(self)


@dataclass(frozen=True, slots=True)
class RestorePlan:
    plan_id: str
    created_at: datetime
    scope: RestoreScope
    source: RecoverySource
    target: TargetEnvironment
    components: tuple[ComponentRestoreSpec, ...]
    approvals: tuple[Approval, ...]
    acceptance_checks: tuple[AcceptanceCheck, ...]
    stages: tuple[RestoreStage, ...]
    release_set_transition_ref: str | None
    dry_run_supported: bool = True
    traffic_initially_blocked: bool = True
    normal_authority_initially_blocked: bool = True
    previous_known_good_preserved: bool = True
    generated_by: str = "koa_operations.restore.plan/v1"
    plan_digest: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "plan_id", _require_id("plan_id", self.plan_id))
        object.__setattr__(self, "created_at", _utc(self.created_at))
        if self.release_set_transition_ref is not None:
            object.__setattr__(
                self,
                "release_set_transition_ref",
                _require_id("release_set_transition_ref", self.release_set_transition_ref),
            )
        if not all((self.traffic_initially_blocked, self.normal_authority_initially_blocked, self.previous_known_good_preserved)):
            raise RestorePlanError("restore must start isolated and preserve known-good authority")
        payload = {
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "scope": self.scope,
            "source": self.source,
            "target": self.target,
            "components": self.components,
            "approvals": self.approvals,
            "acceptance_checks": self.acceptance_checks,
            "stages": self.stages,
            "release_set_transition_ref": self.release_set_transition_ref,
            "dry_run_supported": self.dry_run_supported,
            "traffic_initially_blocked": self.traffic_initially_blocked,
            "normal_authority_initially_blocked": self.normal_authority_initially_blocked,
            "previous_known_good_preserved": self.previous_known_good_preserved,
            "generated_by": self.generated_by,
        }
        object.__setattr__(self, "plan_digest", canonical_digest(payload))

    def public_evidence(self) -> Mapping[str, Any]:
        """Return minimized machine-readable plan evidence with no key material."""

        return MappingProxyType(
            {
                "plan_id": self.plan_id,
                "plan_digest": self.plan_digest,
                "restore_id": self.scope.restore_id,
                "restore_class": self.scope.restore_class.value,
                "source_id": self.source.source_id,
                "source_inventory_digest": self.source.inventory_digest,
                "target_environment_id": self.target.environment_id,
                "profile_id": self.target.profile_id,
                "active_release_set_id": self.scope.active_release_set_id,
                "target_release_set_id": self.scope.target_release_set_id,
                "component_ids": tuple(spec.component_id for spec in self.components),
                "tenant_id": self.scope.tenant_id,
                "security_domain_id": self.scope.security_domain_id,
                "correlation_id": self.scope.correlation_id,
                "created_at": self.created_at.isoformat().replace("+00:00", "Z"),
                "traffic_blocked": True,
                "normal_authority_blocked": True,
            }
        )


def _validate_approvals(scope: RestoreScope, approvals: Sequence[Approval], created_at: datetime) -> tuple[Approval, ...]:
    normalized = tuple(sorted(approvals, key=lambda item: item.approval_id))
    seen: set[str] = set()
    actions: set[str] = set()
    for approval in normalized:
        if approval.approval_id in seen:
            raise RestorePlanError(f"duplicate approval {approval.approval_id}")
        seen.add(approval.approval_id)
        if approval.expires_at <= created_at:
            raise RestorePlanError(f"approval {approval.approval_id} is expired")
        actions.add(approval.action)
    missing = set(scope.high_impact_actions) - actions
    if missing:
        raise RestorePlanError(f"missing explicit approval for high-impact actions: {sorted(missing)}")
    return normalized


def _validate_components(scope: RestoreScope, source: RecoverySource, components: Sequence[ComponentRestoreSpec]) -> tuple[ComponentRestoreSpec, ...]:
    normalized = tuple(sorted(components, key=lambda item: item.component_id))
    ids = tuple(item.component_id for item in normalized)
    if ids != scope.components:
        raise RestorePlanError("component restore specifications must match the declared scope exactly")
    claimed_domains: set[str] = set()
    for item in normalized:
        if item.component_id not in source.component_versions:
            raise RestorePlanError(f"source inventory lacks component version for {item.component_id}")
        if source.component_versions[item.component_id] != item.source_version:
            raise RestorePlanError(f"source version mismatch for {item.component_id}")
        overlap = claimed_domains.intersection(item.data_domains)
        if overlap:
            raise RestorePlanError(f"data domains have multiple component owners: {sorted(overlap)}")
        claimed_domains.update(item.data_domains)
    if tuple(sorted(claimed_domains)) != scope.data_domains:
        raise RestorePlanError("component-owned data domains must match the declared restore scope exactly")
    return normalized


def _validate_checks(checks: Sequence[AcceptanceCheck]) -> tuple[AcceptanceCheck, ...]:
    normalized = tuple(sorted(checks, key=lambda item: (item.gate.value, item.check_id)))
    if len({item.check_id for item in normalized}) != len(normalized):
        raise RestorePlanError("acceptance check identifiers must be unique")
    present = {item.gate for item in normalized}
    missing = _REQUIRED_GATES - present
    if missing:
        raise RestorePlanError(f"acceptance plan lacks required gates: {sorted(item.value for item in missing)}")
    return normalized


def _build_stages(scope: RestoreScope, components: Sequence[ComponentRestoreSpec]) -> tuple[RestoreStage, ...]:
    component_contracts = tuple(item.restore_contract_ref for item in components)
    migration_contracts = tuple(
        item.migration_contract_ref for item in components if item.migration_contract_ref is not None
    )
    derived_ids = tuple(item for component in components for item in component.derived_state_ids)
    contracts_by_stage: dict[str, tuple[str, ...]] = {
        "verify_recovery_source": ("docs/08-operations/09-restore.md#recovery-source-verification",),
        "prepare_recovery_environment": ("docs/08-operations/09-restore.md#clean-target-environment",),
        "verify_target_profile_and_topology": ("docs/contracts/profiles/*.profile.json",),
        "restore_identity_and_trust": ("docs/contracts/components/identity-and-trust.component.json",),
        "restore_revocation_state": ("docs/contracts/components/identity-and-trust.component.json",),
        "restore_governance_policy": ("docs/contracts/components/governance-policy-runtime.component.json",),
        "stage_release_sets": ("docs/contracts/artifact-contracts/release-set.schema.json",),
        "stage_system_and_service_artifacts": ("docs/06-lifecycle/12-artifact-verification.md",),
        "restore_component_authoritative_data": component_contracts,
        "run_migrations_and_forward_repair": migration_contracts or ("docs/06-lifecycle/15-data-schema-evolution.md",),
        "restore_knowledge_and_language_artifacts": ("docs/contracts/artifact-classes.contract.json",),
        "rebuild_derived_state": ("docs/08-operations/09-restore.md#derived-state-rebuild",),
        "restore_integration_configuration": ("docs/02-system/16-external-integrations.md",),
    }
    mutating = {
        "restore_identity_and_trust",
        "restore_revocation_state",
        "restore_governance_policy",
        "stage_release_sets",
        "stage_system_and_service_artifacts",
        "restore_component_authoritative_data",
        "run_migrations_and_forward_repair",
        "restore_knowledge_and_language_artifacts",
        "rebuild_derived_state",
        "restore_integration_configuration",
    }
    resumable = {
        "verify_recovery_source",
        "prepare_recovery_environment",
        "verify_target_profile_and_topology",
        "stage_release_sets",
        "stage_system_and_service_artifacts",
        "rebuild_derived_state",
    }
    stages: list[RestoreStage] = []
    for ordinal, stage_id in enumerate(RESTORE_EXECUTION_ORDER, start=1):
        stage_components = scope.components if stage_id in {
            "restore_component_authoritative_data",
            "run_migrations_and_forward_repair",
            "rebuild_derived_state",
        } else ()
        owner_id = "restore-coordinator"
        if stage_id in {"restore_component_authoritative_data", "run_migrations_and_forward_repair", "rebuild_derived_state"}:
            owner_id = "component-owners"
        stages.append(
            RestoreStage(
                ordinal=ordinal,
                stage_id=stage_id,
                owner_id=owner_id,
                contract_refs=contracts_by_stage[stage_id],
                component_ids=stage_components,
                resumable=stage_id in resumable,
                cancellable=stage_id != "run_migrations_and_forward_repair",
                mutates_candidate=stage_id in mutating,
            )
        )
    if derived_ids and "rebuild_derived_state" not in RESTORE_EXECUTION_ORDER:
        raise RestorePlanError("derived state declared without an explicit rebuild stage")
    return tuple(stages)


def build_restore_plan(
    *,
    plan_id: str,
    created_at: datetime,
    scope: RestoreScope,
    source: RecoverySource,
    target: TargetEnvironment,
    components: Sequence[ComponentRestoreSpec],
    approvals: Sequence[Approval],
    acceptance_checks: Sequence[AcceptanceCheck],
    release_set_transition_ref: str | None = None,
) -> RestorePlan:
    """Build a deterministic plan or fail before any destructive operation."""

    created_at = _utc(created_at)
    if scope.source_id != source.source_id:
        raise RestorePlanError("restore scope and recovery source identity differ")
    if scope.target_environment_id != target.environment_id:
        raise RestorePlanError("restore scope and target environment identity differ")
    if scope.effective_profile_id != target.profile_id:
        raise RestorePlanError("effective profile and target profile differ")
    if source.profile_id != target.profile_id:
        raise RestorePlanError("recovery source profile is incompatible with target profile")
    if source.release_set_id != scope.target_release_set_id and not release_set_transition_ref:
        raise RestorePlanError("Release Set transition requires an explicit compatibility or migration reference")
    required_actions = {"activate_restored_authority"}
    if target.previous_known_good_ref:
        required_actions.add("replace_authoritative_state")
    missing_declared_actions = required_actions - set(scope.high_impact_actions)
    if missing_declared_actions:
        raise RestorePlanError(
            f"restore scope omits required high-impact actions: {sorted(missing_declared_actions)}"
        )
    if target.offline_capable and not source.local_closure_refs:
        raise RestorePlanError("offline target requires a declared local recovery closure")
    normalized_components = _validate_components(scope, source, components)
    normalized_approvals = _validate_approvals(scope, approvals, created_at)
    normalized_checks = _validate_checks(acceptance_checks)
    stages = _build_stages(scope, normalized_components)
    return RestorePlan(
        plan_id=plan_id,
        created_at=created_at,
        scope=scope,
        source=source,
        target=target,
        components=normalized_components,
        approvals=normalized_approvals,
        acceptance_checks=normalized_checks,
        stages=stages,
        release_set_transition_ref=release_set_transition_ref,
    )
