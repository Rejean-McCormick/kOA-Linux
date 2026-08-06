"""Policy-bundle, module and complete policy-set aggregates."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
import re
from typing import Iterable

from .decision import (
    DomainValidationError,
    _aware_datetime,
    _matching_text,
    _required_text,
    _semantic_version,
    _unique_texts,
    _SIMPLE_ID,
)
from .policy_rule import PolicyRule


class PolicyDomain(StrEnum):
    AUTHORIZATION = "authorization"
    SEPARATION_OF_DUTIES = "separation_of_duties"
    WORKFLOW_TRANSITION = "workflow_transition"
    DISCLOSURE = "disclosure"
    PUBLICATION = "publication"
    ARTIFACT_ACTIVATION = "artifact_activation"
    RELEASE_ACTIVATION = "release_activation"
    IDENTITY_AND_DELEGATION = "identity_and_delegation"
    RIGHTS_AND_CONSENT = "rights_and_consent"
    RETENTION_AND_DELETION = "retention_and_deletion"
    EXPORT_AND_EXIT = "export_and_exit"
    EMERGENCY_AND_BREAK_GLASS = "emergency_and_break_glass"
    AI_CAPABILITY = "ai_capability"
    INTEGRATION_CAPABILITY = "integration_capability"
    EXCEPTION_HANDLING = "exception_handling"
    READER_POLICY = "reader_policy"
    RECOVERY = "recovery"
    ADVISORY = "advisory"


class PolicyBundleStatus(StrEnum):
    CANDIDATE = "candidate"
    VALIDATED = "validated"
    STAGED = "staged"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    WITHDRAWN = "withdrawn"
    ARCHIVED = "archived"
    RECOVERY_ELIGIBLE = "recovery_eligible"


class PolicySetState(StrEnum):
    ABSENT = "absent"
    STAGED = "staged"
    VALIDATING = "validating"
    VALIDATED = "validated"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    ACTIVATION_FAILED = "activation_failed"
    ROLLBACK_REQUIRED = "rollback_required"
    FORWARD_REPAIR_REQUIRED = "forward_repair_required"


_FACT_ID = re.compile(r"^fact\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_POLICY_BUNDLE_ID = re.compile(r"^policy-bundle\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")
_POLICY_MODULE_ID = re.compile(r"^policy-module\.[a-z0-9]+(?:[._-][a-z0-9]+)*$")

_ALLOWED_TRANSITIONS: dict[tuple[PolicySetState, PolicySetState], tuple[str, str]] = {
    (PolicySetState.ABSENT, PolicySetState.STAGED): (
        "TRANSITION-GOV-POL-001",
        "stage_verified_policy_bundle",
    ),
    (PolicySetState.STAGED, PolicySetState.VALIDATING): (
        "TRANSITION-GOV-POL-002",
        "begin_policy_validation",
    ),
    (PolicySetState.VALIDATING, PolicySetState.VALIDATED): (
        "TRANSITION-GOV-POL-003",
        "all_required_validation_passes",
    ),
    (PolicySetState.VALIDATED, PolicySetState.ACTIVE): (
        "TRANSITION-GOV-POL-004",
        "atomic_activation_authorized",
    ),
    (PolicySetState.ACTIVE, PolicySetState.SUPERSEDED): (
        "TRANSITION-GOV-POL-005",
        "compatible_replacement_activated",
    ),
    (PolicySetState.VALIDATING, PolicySetState.ACTIVATION_FAILED): (
        "TRANSITION-GOV-POL-006",
        "validation_or_compatibility_failure",
    ),
    (PolicySetState.VALIDATED, PolicySetState.ACTIVATION_FAILED): (
        "TRANSITION-GOV-POL-007",
        "atomic_activation_failure",
    ),
    (PolicySetState.ACTIVATION_FAILED, PolicySetState.ACTIVE): (
        "TRANSITION-GOV-POL-008",
        "previous_valid_policy_set_restored",
    ),
    (PolicySetState.ACTIVATION_FAILED, PolicySetState.FORWARD_REPAIR_REQUIRED): (
        "TRANSITION-GOV-POL-009",
        "rollback_incompatible",
    ),
}


@dataclass(frozen=True, slots=True)
class PolicyModule:
    """One deterministic policy module within a bundle."""

    module_id: str
    version: str
    title: str
    description: str
    domain: PolicyDomain
    evaluation_order: int
    dependencies: tuple[str, ...] = ()
    exports: tuple[str, ...] = ()
    rules: tuple[PolicyRule, ...] = ()
    module_artifact_ref: str | None = None
    entrypoint: str | None = None
    required_fact_ids: tuple[str, ...] = ()
    compatibility_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "module_id",
            _matching_text(self.module_id, "module_id", _POLICY_MODULE_ID),
        )
        object.__setattr__(self, "version", _semantic_version(self.version, "version"))
        object.__setattr__(self, "title", _required_text(self.title, "title"))
        object.__setattr__(
            self,
            "description",
            _required_text(self.description, "description"),
        )
        try:
            domain = PolicyDomain(self.domain)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("domain is not registered") from exc
        object.__setattr__(self, "domain", domain)
        if (
            not isinstance(self.evaluation_order, int)
            or isinstance(self.evaluation_order, bool)
            or self.evaluation_order < 0
        ):
            raise DomainValidationError("evaluation_order must be a non-negative integer")
        object.__setattr__(
            self,
            "dependencies",
            _unique_texts(
                self.dependencies,
                "dependencies",
                pattern=_POLICY_MODULE_ID,
            ),
        )
        if self.module_id in self.dependencies:
            raise DomainValidationError("a module must not depend on itself")
        object.__setattr__(
            self,
            "exports",
            _unique_texts(self.exports, "exports", pattern=_SIMPLE_ID),
        )
        rules = tuple(self.rules)
        if not all(isinstance(rule, PolicyRule) for rule in rules):
            raise DomainValidationError("rules must contain PolicyRule values")
        rule_ids = [rule.rule_id for rule in rules]
        if len(set(rule_ids)) != len(rule_ids):
            raise DomainValidationError("rules must not contain duplicate identifiers")
        priorities = [rule.priority for rule in rules]
        if len(set(priorities)) != len(priorities):
            raise DomainValidationError(
                "inline rules must have unique priorities; file order is not precedence"
            )
        has_inline = bool(rules)
        has_external = self.module_artifact_ref is not None or self.entrypoint is not None
        if has_inline == has_external:
            raise DomainValidationError(
                "module must define either inline rules or artifact_ref plus entrypoint"
            )
        if has_external:
            if self.module_artifact_ref is None or self.entrypoint is None:
                raise DomainValidationError(
                    "external module requires module_artifact_ref and entrypoint"
                )
            object.__setattr__(
                self,
                "module_artifact_ref",
                _required_text(self.module_artifact_ref, "module_artifact_ref"),
            )
            object.__setattr__(
                self,
                "entrypoint",
                _matching_text(self.entrypoint, "entrypoint", _SIMPLE_ID),
            )
        object.__setattr__(
            self,
            "rules",
            tuple(sorted(rules, key=lambda rule: (-rule.priority, rule.rule_id))),
        )
        object.__setattr__(
            self,
            "required_fact_ids",
            _unique_texts(self.required_fact_ids, "required_fact_ids", pattern=_FACT_ID),
        )
        object.__setattr__(
            self,
            "compatibility_refs",
            _unique_texts(self.compatibility_refs, "compatibility_refs"),
        )

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "module_id": self.module_id,
            "version": self.version,
            "title": self.title,
            "description": self.description,
            "domain": self.domain.value,
            "evaluation_order": self.evaluation_order,
            "dependencies": list(self.dependencies),
            "exports": list(self.exports),
            "required_fact_ids": list(self.required_fact_ids),
            "compatibility_refs": list(self.compatibility_refs),
        }
        if self.rules:
            result["rules"] = [rule.as_dict() for rule in self.rules]
        else:
            result["module_artifact_ref"] = self.module_artifact_ref
            result["entrypoint"] = self.entrypoint
        return result


@dataclass(frozen=True, slots=True)
class PolicyBundle:
    """Immutable complete candidate or admitted governance-channel artifact."""

    artifact_id: str
    version: str
    status: PolicyBundleStatus
    issued_at: datetime
    policy_namespace: str
    target_profiles: tuple[str, ...]
    minimum_runtime_version: str
    maximum_runtime_version: str
    modules: tuple[PolicyModule, ...]
    compatibility_refs: tuple[str, ...]
    required_test_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    signature_refs: tuple[str, ...]
    provenance_ref: str
    recovery_ref: str
    authority_ref: str = "generated/authority-manifest.json"
    release_channel: str = "governance"
    deterministic: bool = True
    side_effect_free: bool = True
    partial_activation_permitted: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "artifact_id",
            _matching_text(self.artifact_id, "artifact_id", _POLICY_BUNDLE_ID),
        )
        object.__setattr__(self, "version", _semantic_version(self.version, "version"))
        try:
            status = PolicyBundleStatus(self.status)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("status is not registered") from exc
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "issued_at", _aware_datetime(self.issued_at, "issued_at"))
        object.__setattr__(
            self,
            "policy_namespace",
            _matching_text(self.policy_namespace, "policy_namespace", _SIMPLE_ID),
        )
        object.__setattr__(
            self,
            "target_profiles",
            _unique_texts(self.target_profiles, "target_profiles", required=True),
        )
        minimum = _semantic_version(self.minimum_runtime_version, "minimum_runtime_version")
        maximum = _semantic_version(self.maximum_runtime_version, "maximum_runtime_version")
        if _semver_key(minimum) > _semver_key(maximum):
            raise DomainValidationError(
                "minimum_runtime_version must not exceed maximum_runtime_version"
            )
        object.__setattr__(self, "minimum_runtime_version", minimum)
        object.__setattr__(self, "maximum_runtime_version", maximum)
        modules = tuple(self.modules)
        if not modules or not all(isinstance(module, PolicyModule) for module in modules):
            raise DomainValidationError("modules must contain at least one PolicyModule")
        module_ids = [module.module_id for module in modules]
        if len(set(module_ids)) != len(module_ids):
            raise DomainValidationError("modules must not contain duplicate identifiers")
        orders = [module.evaluation_order for module in modules]
        if len(set(orders)) != len(orders):
            raise DomainValidationError(
                "modules must have unique evaluation_order; file order is not precedence"
            )
        module_map = {module.module_id: module for module in modules}
        for module in modules:
            unresolved = set(module.dependencies) - set(module_map)
            if unresolved:
                raise DomainValidationError(
                    f"module {module.module_id} has unresolved dependencies: "
                    + ", ".join(sorted(unresolved))
                )
            for dependency_id in module.dependencies:
                dependency = module_map[dependency_id]
                if dependency.evaluation_order >= module.evaluation_order:
                    raise DomainValidationError(
                        "module dependencies must precede dependants in evaluation_order"
                    )
        _assert_acyclic(module_map)
        object.__setattr__(
            self,
            "modules",
            tuple(sorted(modules, key=lambda module: module.evaluation_order)),
        )
        object.__setattr__(
            self,
            "compatibility_refs",
            _unique_texts(
                self.compatibility_refs,
                "compatibility_refs",
                required=True,
            ),
        )
        object.__setattr__(
            self,
            "required_test_refs",
            _unique_texts(
                self.required_test_refs,
                "required_test_refs",
                required=True,
            ),
        )
        object.__setattr__(
            self,
            "evidence_refs",
            _unique_texts(self.evidence_refs, "evidence_refs", required=True),
        )
        object.__setattr__(
            self,
            "signature_refs",
            _unique_texts(self.signature_refs, "signature_refs"),
        )
        object.__setattr__(
            self,
            "provenance_ref",
            _required_text(self.provenance_ref, "provenance_ref"),
        )
        object.__setattr__(
            self,
            "recovery_ref",
            _required_text(self.recovery_ref, "recovery_ref"),
        )
        if self.authority_ref != "generated/authority-manifest.json":
            raise DomainValidationError("authority_ref must use the canonical authority manifest")
        if self.release_channel != "governance":
            raise DomainValidationError("release_channel must be governance")
        if self.deterministic is not True or self.side_effect_free is not True:
            raise DomainValidationError("policy bundles must be deterministic and side-effect-free")
        if self.partial_activation_permitted is not False:
            raise DomainValidationError("partial policy activation is prohibited")
        admitted = {
            PolicyBundleStatus.VALIDATED,
            PolicyBundleStatus.STAGED,
            PolicyBundleStatus.ACTIVE,
            PolicyBundleStatus.SUPERSEDED,
            PolicyBundleStatus.RECOVERY_ELIGIBLE,
        }
        if status in admitted and not self.signature_refs:
            raise DomainValidationError("admitted policy bundle status requires signatures")

    def supports_runtime(self, runtime_version: str) -> bool:
        version = _semantic_version(runtime_version, "runtime_version")
        return _semver_key(self.minimum_runtime_version) <= _semver_key(version) <= _semver_key(
            self.maximum_runtime_version
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "artifact_id": self.artifact_id,
            "artifact_type": "governance_policy_bundle",
            "artifact_class": "policy_bundle",
            "release_channel": self.release_channel,
            "version": self.version,
            "status": self.status.value,
            "issued_at": self.issued_at.isoformat(),
            "authority_ref": self.authority_ref,
            "policy_namespace": self.policy_namespace,
            "target_profiles": list(self.target_profiles),
            "minimum_runtime_version": self.minimum_runtime_version,
            "maximum_runtime_version": self.maximum_runtime_version,
            "modules": [module.as_dict() for module in self.modules],
            "compatibility_refs": list(self.compatibility_refs),
            "required_test_refs": list(self.required_test_refs),
            "evidence_refs": list(self.evidence_refs),
            "signature_refs": list(self.signature_refs),
            "provenance_ref": self.provenance_ref,
            "recovery_ref": self.recovery_ref,
            "deterministic": self.deterministic,
            "side_effect_free": self.side_effect_free,
            "partial_activation_permitted": self.partial_activation_permitted,
        }


@dataclass(frozen=True, slots=True)
class PolicySet:
    """One complete policy set with canonical lifecycle transitions."""

    policy_set_ref: str
    bundles: tuple[PolicyBundle, ...]
    state: PolicySetState
    previous_valid_policy_set_ref: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "policy_set_ref",
            _required_text(self.policy_set_ref, "policy_set_ref"),
        )
        try:
            state = PolicySetState(self.state)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("state is not registered") from exc
        object.__setattr__(self, "state", state)
        bundles = tuple(self.bundles)
        if state is PolicySetState.ABSENT:
            if bundles:
                raise DomainValidationError("absent policy set must not contain bundles")
        elif not bundles:
            raise DomainValidationError("non-absent policy set requires a complete bundle set")
        if not all(isinstance(bundle, PolicyBundle) for bundle in bundles):
            raise DomainValidationError("bundles must contain PolicyBundle values")
        identities = [(bundle.artifact_id, bundle.version) for bundle in bundles]
        if len(set(identities)) != len(identities):
            raise DomainValidationError("policy set must not contain duplicate bundle identities")
        artifact_ids = [bundle.artifact_id for bundle in bundles]
        if len(set(artifact_ids)) != len(artifact_ids):
            raise DomainValidationError("mixed versions of one bundle identity are prohibited")
        object.__setattr__(
            self,
            "bundles",
            tuple(sorted(bundles, key=lambda bundle: bundle.artifact_id)),
        )
        if self.previous_valid_policy_set_ref is not None:
            object.__setattr__(
                self,
                "previous_valid_policy_set_ref",
                _required_text(
                    self.previous_valid_policy_set_ref,
                    "previous_valid_policy_set_ref",
                ),
            )
        if state is PolicySetState.ACTIVE:
            if self.previous_valid_policy_set_ref is None:
                raise DomainValidationError(
                    "active policy set requires previous valid or recovery reference"
                )
            invalid = [
                bundle.artifact_id
                for bundle in bundles
                if bundle.status
                not in {PolicyBundleStatus.ACTIVE, PolicyBundleStatus.RECOVERY_ELIGIBLE}
            ]
            if invalid:
                raise DomainValidationError(
                    "active policy set contains non-active bundles: "
                    + ", ".join(sorted(invalid))
                )

    def transition(
        self,
        target: PolicySetState,
        *,
        trigger: str,
        bundles: Iterable[PolicyBundle] | None = None,
        previous_valid_policy_set_ref: str | None = None,
    ) -> "PolicySet":
        try:
            target_state = PolicySetState(target)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("target state is not registered") from exc
        normalized_trigger = _required_text(trigger, "trigger")
        transition = _ALLOWED_TRANSITIONS.get((self.state, target_state))
        if transition is None:
            raise DomainValidationError(
                f"transition {self.state.value} -> {target_state.value} is not canonical"
            )
        _, required_trigger = transition
        if normalized_trigger != required_trigger:
            raise DomainValidationError(
                f"transition requires trigger {required_trigger}"
            )
        replacement_bundles = self.bundles if bundles is None else tuple(bundles)
        previous_ref = (
            self.previous_valid_policy_set_ref
            if previous_valid_policy_set_ref is None
            else previous_valid_policy_set_ref
        )
        return replace(
            self,
            state=target_state,
            bundles=replacement_bundles,
            previous_valid_policy_set_ref=previous_ref,
        )

    @staticmethod
    def transition_identity(
        source: PolicySetState,
        target: PolicySetState,
    ) -> str:
        try:
            normalized_source = PolicySetState(source)
            normalized_target = PolicySetState(target)
        except (TypeError, ValueError) as exc:
            raise DomainValidationError("state is not registered") from exc
        transition = _ALLOWED_TRANSITIONS.get((normalized_source, normalized_target))
        if transition is None:
            raise DomainValidationError("transition is not canonical")
        return transition[0]

    def as_dict(self) -> dict[str, object]:
        return {
            "policy_set_ref": self.policy_set_ref,
            "bundles": [bundle.as_dict() for bundle in self.bundles],
            "state": self.state.value,
            "previous_valid_policy_set_ref": self.previous_valid_policy_set_ref,
        }


def _semver_key(value: str) -> tuple[int, int, int, str]:
    core, separator, suffix = value.partition("-")
    core = core.split("+", 1)[0]
    major, minor, patch = (int(part) for part in core.split("."))
    prerelease = suffix.split("+", 1)[0] if separator else "~"
    return major, minor, patch, prerelease


def _assert_acyclic(modules: dict[str, PolicyModule]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(module_id: str) -> None:
        if module_id in visited:
            return
        if module_id in visiting:
            raise DomainValidationError("policy module dependency graph contains a cycle")
        visiting.add(module_id)
        for dependency in modules[module_id].dependencies:
            visit(dependency)
        visiting.remove(module_id)
        visited.add(module_id)

    for module_id in sorted(modules):
        visit(module_id)
