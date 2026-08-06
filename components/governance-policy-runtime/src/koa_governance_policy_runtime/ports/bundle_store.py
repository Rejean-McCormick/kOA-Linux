"""Governance Policy Runtime-owned state and evaluator boundary.

The port exposes semantic operations only. Adapters may use a database and a
registered deterministic evaluator, but application code never receives raw
connections, tables, or executable policy source.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol, runtime_checkable

from .decision_receipt_store import DecisionObligation, DecisionResult


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


class LifecycleSupportStatus(StrEnum):
    SUPPORTED = "supported"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"
    WITHDRAWN = "withdrawn"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class PolicySetRecord:
    bundle_ref: str
    policy_set_ref: str
    authority_version: str
    release_set_ref: str
    version: str
    evaluator_version: str
    target_profiles: tuple[str, ...]
    target_components: tuple[str, ...]
    semantic_fingerprint: str
    state: PolicySetState
    support_status: LifecycleSupportStatus
    compatible: bool
    validated_at: datetime
    validation_evidence_refs: tuple[str, ...]
    signer_refs: tuple[str, ...]
    previous_policy_set_ref: str | None = None
    activated_at: datetime | None = None
    withdrawn_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class PolicyEngineRequest:
    decision_class: str
    requester_ref: str
    action_ref: str
    target_ref: str
    scope: tuple[str, ...]
    context: Mapping[str, Any]
    exception_ids: tuple[str, ...]
    prior_receipt_refs: tuple[str, ...]
    evaluated_at: datetime


@dataclass(frozen=True, slots=True)
class PolicyEngineDecision:
    result: DecisionResult
    obligations: tuple[DecisionObligation, ...] = ()
    diagnostics: tuple[str, ...] = ()
    verified_context_refs: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ActivationTransition:
    activated: bool
    candidate_policy_set_ref: str
    active_policy_set_ref: str | None
    previous_policy_set_ref: str | None
    state: PolicySetState
    evidence_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RevocationTransition:
    bundle_ref: str
    affected_policy_set_ref: str
    was_active: bool
    support_status: LifecycleSupportStatus
    active_policy_set_ref: str | None
    restored_policy_set_ref: str | None
    state: PolicySetState
    evidence_refs: tuple[str, ...] = ()
    reason_codes: tuple[str, ...] = ()


@runtime_checkable
class BundleStore(Protocol):
    """Own policy-set lifecycle state and invoke the registered evaluator."""

    @abstractmethod
    def get_active_policy_set(self) -> PolicySetRecord | None:
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def get_policy_set(self, policy_set_ref: str) -> PolicySetRecord | None:
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def get_staged_policy_set(self, policy_set_ref: str) -> PolicySetRecord | None:
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def stage_validated_policy_set(
        self,
        record: PolicySetRecord,
        *,
        bundle: Mapping[str, Any],
    ) -> PolicySetRecord:
        """Persist one complete validated candidate in non-active state."""
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def evaluate(
        self,
        policy_set_ref: str,
        request: PolicyEngineRequest,
    ) -> PolicyEngineDecision:
        """Evaluate with the exact registered deterministic policy set."""
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def activate_policy_set(
        self,
        candidate_policy_set_ref: str,
        *,
        expected_current_policy_set_ref: str | None,
        activated_at: datetime,
    ) -> ActivationTransition:
        """Atomically switch the complete active policy set."""
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def restore_previous_policy_set(
        self,
        failed_policy_set_ref: str,
        *,
        restored_at: datetime,
    ) -> ActivationTransition:
        """Restore the previous compatible complete policy set when safe."""
        raise NotImplementedError("a BundleStore adapter is required")

    @abstractmethod
    def revoke_bundle(
        self,
        bundle_ref: str,
        *,
        authority_ref: str,
        reason: str,
        revoked_at: datetime,
    ) -> RevocationTransition:
        """Withdraw future activation while preserving historical evidence."""
        raise NotImplementedError("a BundleStore adapter is required")
