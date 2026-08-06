"""Forward repair orchestration for rollback-incompatible recovery."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

from . import (
    AuthorityContext,
    Clock,
    DecisionOutcome,
    ForwardRepairExecutor,
    OperationOutcome,
    RecoveryAuthority,
    RecoveryError,
    RecoveryJournal,
    RecoveryResult,
    RecoverySnapshot,
    RecoveryState,
    ValidationResult,
    build_receipt,
    canonical_digest,
    check_idempotency,
    commit_state,
    freeze_mapping,
    require_aware_datetime,
    require_text,
    require_text_tuple,
    thaw_mapping,
    validate_authority,
)


_REPAIR_START_STATES = (
    RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE,
    RecoveryState.SOURCE_SELECTION,
    RecoveryState.RECOVERY_FAILED,
)
_ALLOWED_DEGRADED_MODES = {"blocked", "read_only", "advisory", "queued", "locally_limited"}


@dataclass(frozen=True, slots=True)
class ForwardRepairPlan:
    operation_id: str
    plan_ref: str
    target_ref: str
    incident_ref: str
    active_profile_ref: str
    current_release_set_ref: str
    target_release_set_ref: str
    expected_revision: int
    authority: AuthorityContext
    requested_at: datetime
    rollback_prohibition_ref: str
    last_rollback_safe_state_ref: str
    irreversible_operation_ref: str
    current_authoritative_state_ref: str
    incompatibility_ref: str
    rollback_risk_refs: tuple[str, ...]
    safe_degraded_mode: str
    owner_map: Mapping[str, str]
    repair_artifact_refs: tuple[str, ...]
    ordered_steps: tuple[Mapping[str, Any], ...]
    preserved_state_refs: tuple[str, ...]
    validation_refs: tuple[str, ...]
    completion_boundary_ref: str
    restricted_capability_refs: tuple[str, ...] = ()
    offline: bool = False

    def __post_init__(self) -> None:
        for name in (
            "operation_id",
            "plan_ref",
            "target_ref",
            "incident_ref",
            "active_profile_ref",
            "current_release_set_ref",
            "target_release_set_ref",
            "rollback_prohibition_ref",
            "last_rollback_safe_state_ref",
            "irreversible_operation_ref",
            "current_authoritative_state_ref",
            "incompatibility_ref",
            "safe_degraded_mode",
            "completion_boundary_ref",
        ):
            object.__setattr__(self, name, require_text(getattr(self, name), name))
        if self.expected_revision < 0:
            raise RecoveryError("revision_invalid", "expected revision cannot be negative")
        object.__setattr__(self, "requested_at", require_aware_datetime(self.requested_at, "requested_at"))
        for name in (
            "rollback_risk_refs",
            "repair_artifact_refs",
            "preserved_state_refs",
            "validation_refs",
        ):
            object.__setattr__(self, name, require_text_tuple(getattr(self, name), name))
        object.__setattr__(
            self,
            "restricted_capability_refs",
            require_text_tuple(
                self.restricted_capability_refs,
                "restricted_capability_refs",
                allow_empty=True,
            ),
        )
        if self.current_release_set_ref == self.target_release_set_ref:
            raise RecoveryError(
                "repair_target_not_advanced",
                "forward repair requires a distinct corrected Release Set",
            )
        if self.safe_degraded_mode not in _ALLOWED_DEGRADED_MODES:
            raise RecoveryError("degraded_mode_invalid", "forward repair degraded mode is not declared")
        if self.rollback_prohibition_ref.lower() in {"unknown", "uncertain", "unproved"}:
            raise RecoveryError(
                "rollback_prohibition_unproved",
                "uncertainty about rollback safety blocks forward repair",
            )
        object.__setattr__(self, "owner_map", _validate_owner_map(self.owner_map))
        object.__setattr__(self, "ordered_steps", _validate_steps(self.ordered_steps, self.owner_map))

    def as_mapping(self) -> Mapping[str, Any]:
        return freeze_mapping(
            {
                "operation_id": self.operation_id,
                "plan_ref": self.plan_ref,
                "target_ref": self.target_ref,
                "incident_ref": self.incident_ref,
                "active_profile_ref": self.active_profile_ref,
                "current_release_set_ref": self.current_release_set_ref,
                "target_release_set_ref": self.target_release_set_ref,
                "expected_revision": self.expected_revision,
                "requested_at": self.requested_at,
                "rollback_prohibition_ref": self.rollback_prohibition_ref,
                "last_rollback_safe_state_ref": self.last_rollback_safe_state_ref,
                "irreversible_operation_ref": self.irreversible_operation_ref,
                "current_authoritative_state_ref": self.current_authoritative_state_ref,
                "incompatibility_ref": self.incompatibility_ref,
                "rollback_risk_refs": self.rollback_risk_refs,
                "safe_degraded_mode": self.safe_degraded_mode,
                "owner_map": thaw_mapping(self.owner_map),
                "repair_artifact_refs": self.repair_artifact_refs,
                "ordered_steps": [thaw_mapping(step) for step in self.ordered_steps],
                "preserved_state_refs": self.preserved_state_refs,
                "validation_refs": self.validation_refs,
                "completion_boundary_ref": self.completion_boundary_ref,
                "restricted_capability_refs": self.restricted_capability_refs,
                "offline": self.offline,
                "authority": {
                    "actor_ref": self.authority.actor_ref,
                    "authority_domain": self.authority.authority_domain,
                    "role_refs": self.authority.role_refs,
                    "scope_refs": self.authority.scope_refs,
                    "authorized_until": self.authority.authorized_until,
                    "decision_ref": self.authority.decision_ref,
                },
            }
        )


class ExecuteForwardRepair:
    def __init__(
        self,
        *,
        journal: RecoveryJournal,
        authority: RecoveryAuthority,
        executor: ForwardRepairExecutor,
        clock: Clock,
    ) -> None:
        self._journal = journal
        self._authority = authority
        self._executor = executor
        self._clock = clock

    def __call__(self, plan: ForwardRepairPlan) -> RecoveryResult:
        plan_mapping = plan.as_mapping()
        request_digest = canonical_digest(plan_mapping)
        prior = check_idempotency(
            self._journal,
            operation_id=plan.operation_id,
            request_digest=request_digest,
        )
        if prior is not None:
            return prior

        now = require_aware_datetime(self._clock.now(), "clock.now")
        validate_authority(plan.authority, at=now, target_ref=plan.target_ref)
        snapshot = self._journal.snapshot(plan.target_ref)
        self._validate_snapshot(plan, snapshot)

        try:
            decision = self._authority.authorize(
                action="recovery.forward_repair",
                target_ref=plan.target_ref,
                authority=plan.authority,
                context={
                    "plan_ref": plan.plan_ref,
                    "incident_ref": plan.incident_ref,
                    "current_release_set_ref": plan.current_release_set_ref,
                    "target_release_set_ref": plan.target_release_set_ref,
                    "rollback_prohibition_ref": plan.rollback_prohibition_ref,
                    "incompatibility_ref": plan.incompatibility_ref,
                    "completion_boundary_ref": plan.completion_boundary_ref,
                    "offline": plan.offline,
                },
                evaluated_at=now,
            )
        except Exception as exc:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                state=snapshot.state,
                reason_codes=("repair_authority_unavailable", type(exc).__name__),
            )
        if decision.outcome is not DecisionOutcome.ALLOW:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                state=snapshot.state,
                reason_codes=(f"repair_authority_{decision.outcome.value}", *decision.reason_codes),
                evidence_refs=decision.evidence_refs,
            )

        receipt_refs: list[str] = []
        evidence_refs: list[str] = list(decision.evidence_refs)
        if snapshot.state is not RecoveryState.SOURCE_SELECTION:
            selection_receipt = build_receipt(
                transition_type="forward_repair_selected",
                operation_id=plan.operation_id,
                target_ref=plan.target_ref,
                authority=plan.authority,
                from_state=snapshot.state,
                to_state=RecoveryState.SOURCE_SELECTION,
                decision="authorized",
                execution_state="rollback_prohibition_verified",
                commit_state="committed",
                outcome="forward_repair_selected",
                recorded_at=now,
                active_release_set_ref=snapshot.active_release_set_ref,
                evidence_refs=decision.evidence_refs,
                details={
                    "plan_ref": plan.plan_ref,
                    "rollback_prohibition_ref": plan.rollback_prohibition_ref,
                    "last_rollback_safe_state_ref": plan.last_rollback_safe_state_ref,
                    "irreversible_operation_ref": plan.irreversible_operation_ref,
                    "incompatibility_ref": plan.incompatibility_ref,
                    "safe_degraded_mode": plan.safe_degraded_mode,
                },
            )
            snapshot = commit_state(
                self._journal,
                snapshot=snapshot,
                operation_id=plan.operation_id,
                request_digest=request_digest,
                next_state=RecoveryState.SOURCE_SELECTION,
                receipt=selection_receipt,
                expected_states=_REPAIR_START_STATES,
            )
            receipt_refs.append(selection_receipt.receipt_id)

        staging_receipt = build_receipt(
            transition_type="forward_repair_staging_started",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.STAGING,
            decision="authorized",
            execution_state="staging",
            commit_state="committed",
            outcome="staging_started",
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=snapshot.active_release_set_ref,
            evidence_refs=evidence_refs,
            details={
                "plan_ref": plan.plan_ref,
                "repair_artifact_refs": plan.repair_artifact_refs,
                "preserved_state_refs": plan.preserved_state_refs,
                "owner_map": thaw_mapping(plan.owner_map),
                "authoritative": False,
            },
        )
        snapshot = commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=plan.operation_id,
            request_digest=request_digest,
            next_state=RecoveryState.STAGING,
            receipt=staging_receipt,
        )
        receipt_refs.append(staging_receipt.receipt_id)

        stage_result = self._call_validation(
            "repair_staging_failed",
            lambda: self._executor.stage(
                plan_mapping,
                staged_at=require_aware_datetime(self._clock.now(), "clock.now"),
            ),
        )
        evidence_refs.extend(stage_result.evidence_refs)
        if not stage_result.passed:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.FAILED,
                state=RecoveryState.RECOVERY_FAILED,
                reason_codes=stage_result.reason_codes,
                receipt_refs=receipt_refs,
                evidence_refs=tuple(evidence_refs),
            )

        for step in plan.ordered_steps:
            checkpoint_result, checkpoint_receipt = self._execute_checkpoint(
                plan,
                plan_mapping,
                snapshot,
                step,
                evidence_refs=tuple(evidence_refs),
            )
            receipt_refs.append(checkpoint_receipt.receipt_id)
            evidence_refs.extend(checkpoint_result.evidence_refs)
            if not checkpoint_result.passed:
                return self._terminal(
                    plan,
                    snapshot,
                    request_digest,
                    outcome=OperationOutcome.FAILED,
                    state=RecoveryState.RECOVERY_FAILED,
                    reason_codes=checkpoint_result.reason_codes,
                    receipt_refs=receipt_refs,
                    evidence_refs=tuple(evidence_refs),
                )

        validation_receipt = build_receipt(
            transition_type="forward_repair_validation_started",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.VALIDATION,
            decision="authorized",
            execution_state="verifying",
            commit_state="committed",
            outcome="validation_started",
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=snapshot.active_release_set_ref,
            evidence_refs=evidence_refs,
            details={"validation_refs": plan.validation_refs},
        )
        snapshot = commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=plan.operation_id,
            request_digest=request_digest,
            next_state=RecoveryState.VALIDATION,
            receipt=validation_receipt,
        )
        receipt_refs.append(validation_receipt.receipt_id)

        validation = self._call_validation(
            "repair_validation_failed",
            lambda: self._executor.validate_staged(
                plan_mapping,
                validated_at=require_aware_datetime(self._clock.now(), "clock.now"),
            ),
        )
        evidence_refs.extend(validation.evidence_refs)
        if not validation.passed:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                state=RecoveryState.RECOVERY_FAILED,
                reason_codes=validation.reason_codes,
                receipt_refs=receipt_refs,
                evidence_refs=tuple(evidence_refs),
            )

        activation_receipt = build_receipt(
            transition_type="forward_repair_authority_activation",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.ACTIVATION_PENDING,
            decision="authorized",
            execution_state="atomic_cutover",
            commit_state="committed",
            outcome="target_release_set_active_pending_confirmation",
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=plan.target_release_set_ref,
            evidence_refs=evidence_refs,
            details={
                "previous_release_set_ref": plan.current_release_set_ref,
                "target_release_set_ref": plan.target_release_set_ref,
                "completion_boundary_ref": plan.completion_boundary_ref,
                "atomic_pointer_commit": True,
            },
        )
        snapshot = commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=plan.operation_id,
            request_digest=request_digest,
            next_state=RecoveryState.ACTIVATION_PENDING,
            receipt=activation_receipt,
            active_release_set_ref=plan.target_release_set_ref,
        )
        receipt_refs.append(activation_receipt.receipt_id)

        confirmation = self._call_validation(
            "post_repair_confirmation_failed",
            lambda: self._executor.confirm_active(
                plan_mapping,
                confirmed_at=require_aware_datetime(self._clock.now(), "clock.now"),
            ),
        )
        evidence_refs.extend(confirmation.evidence_refs)
        if not confirmation.passed:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.FAILED,
                state=RecoveryState.RECOVERY_FAILED,
                reason_codes=(*confirmation.reason_codes, "successor_repair_required"),
                receipt_refs=receipt_refs,
                evidence_refs=tuple(evidence_refs),
                active_release_set_ref=plan.target_release_set_ref,
            )

        restricted = tuple(
            dict.fromkeys((*plan.restricted_capability_refs, *confirmation.restricted_capability_refs))
        )
        final_state = (
            RecoveryState.RECOVERED_RESTRICTED if restricted else RecoveryState.RECOVERED_NORMAL
        )
        final_outcome = OperationOutcome.RESTRICTED if restricted else OperationOutcome.SUCCEEDED
        completion_receipt = build_receipt(
            transition_type="forward_repair_completed",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=final_state,
            decision="authorized",
            execution_state="completed",
            commit_state="committed",
            outcome=final_outcome.value,
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=plan.target_release_set_ref,
            evidence_refs=evidence_refs,
            details={
                "plan_ref": plan.plan_ref,
                "completion_boundary_ref": plan.completion_boundary_ref,
                "restricted_capability_refs": restricted,
                "rollback_used": False,
            },
        )
        result = RecoveryResult(
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            operation_kind="forward_repair",
            outcome=final_outcome,
            state=final_state,
            active_release_set_ref=plan.target_release_set_ref,
            receipt_refs=tuple((*receipt_refs, completion_receipt.receipt_id)),
            evidence_refs=tuple(dict.fromkeys(evidence_refs)),
            restricted_capability_refs=restricted,
        )
        commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=plan.operation_id,
            request_digest=request_digest,
            next_state=final_state,
            receipt=completion_receipt,
            active_release_set_ref=plan.target_release_set_ref,
            terminal_result=result,
        )
        return result

    def _execute_checkpoint(
        self,
        plan: ForwardRepairPlan,
        plan_mapping: Mapping[str, Any],
        snapshot: RecoverySnapshot,
        step: Mapping[str, Any],
        *,
        evidence_refs: tuple[str, ...],
    ) -> tuple[ValidationResult, Any]:
        step_id = require_text(step.get("step_id"), "step_id")
        try:
            prepared = self._executor.prepare_checkpoint(
                plan_mapping,
                step,
                prepared_at=require_aware_datetime(self._clock.now(), "clock.now"),
            )
        except Exception as exc:
            receipt = build_receipt(
                transition_type="forward_repair_checkpoint",
                operation_id=plan.operation_id,
                target_ref=plan.target_ref,
                authority=plan.authority,
                from_state=snapshot.state,
                to_state=snapshot.state,
                decision="authorized",
                execution_state="not_prepared",
                commit_state="not_committed",
                outcome="failed",
                recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
                active_release_set_ref=snapshot.active_release_set_ref,
                reason_codes=("checkpoint_prepare_failed", type(exc).__name__),
                evidence_refs=evidence_refs,
                details={"step_id": step_id},
            )
            try:
                self._journal.retain_receipt(receipt)
            except Exception as retain_exc:
                return (
                    ValidationResult(
                        False,
                        (
                            "checkpoint_prepare_failed",
                            type(exc).__name__,
                            "checkpoint_receipt_persistence_failed",
                            type(retain_exc).__name__,
                        ),
                        (),
                        (),
                    ),
                    receipt,
                )
            return ValidationResult(False, receipt.reason_codes, (), ()), receipt
        if not isinstance(prepared, Mapping):
            raise RecoveryError("checkpoint_invalid", "prepared checkpoint must be a mapping")

        checkpoint_receipt = build_receipt(
            transition_type="forward_repair_checkpoint",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=snapshot.state,
            decision="authorized",
            execution_state="prepared",
            commit_state="receipt_persisted_before_owner_commit",
            outcome="checkpoint_authorized",
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=snapshot.active_release_set_ref,
            evidence_refs=evidence_refs,
            details={
                "step_id": step_id,
                "owner_ref": step["owner_ref"],
                "checkpoint_ref": step["checkpoint_ref"],
                "idempotency_key": step["idempotency_key"],
                "prepared_checkpoint": dict(prepared),
            },
        )
        try:
            self._journal.retain_receipt(checkpoint_receipt)
        except Exception as exc:
            return (
                ValidationResult(
                    False,
                    ("checkpoint_receipt_persistence_failed", type(exc).__name__),
                    (),
                    (),
                ),
                checkpoint_receipt,
            )
        return (
            self._call_validation(
                "checkpoint_commit_indeterminate",
                lambda: self._executor.commit_checkpoint(prepared, checkpoint_receipt),
            ),
            checkpoint_receipt,
        )

    def _terminal(
        self,
        plan: ForwardRepairPlan,
        snapshot: RecoverySnapshot,
        request_digest: str,
        *,
        outcome: OperationOutcome,
        state: RecoveryState,
        reason_codes: Sequence[str],
        receipt_refs: Sequence[str] = (),
        evidence_refs: Sequence[str] = (),
        active_release_set_ref: str | None = None,
    ) -> RecoveryResult:
        target_release = active_release_set_ref or snapshot.active_release_set_ref
        receipt = build_receipt(
            transition_type="forward_repair_terminal",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=state,
            decision="blocked" if outcome is OperationOutcome.BLOCKED else "authorized",
            execution_state="stopped",
            commit_state="committed_safe_state",
            outcome=outcome.value,
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=target_release,
            reason_codes=reason_codes,
            evidence_refs=evidence_refs,
            details={
                "plan_ref": plan.plan_ref,
                "ordinary_writes_remain_blocked": True,
                "automatic_destructive_reset": False,
            },
        )
        result = RecoveryResult(
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            operation_kind="forward_repair",
            outcome=outcome,
            state=state,
            active_release_set_ref=target_release,
            receipt_refs=tuple((*receipt_refs, receipt.receipt_id)),
            reason_codes=tuple(reason_codes),
            evidence_refs=tuple(dict.fromkeys(evidence_refs)),
            restricted_capability_refs=plan.restricted_capability_refs,
        )
        commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=plan.operation_id,
            request_digest=request_digest,
            next_state=state,
            receipt=receipt,
            active_release_set_ref=target_release,
            terminal_result=result,
        )
        return result

    @staticmethod
    def _call_validation(code: str, call: Any) -> ValidationResult:
        try:
            result = call()
        except Exception as exc:
            return ValidationResult(False, (code, type(exc).__name__), (), ())
        if not isinstance(result, ValidationResult):
            return ValidationResult(False, (code, "invalid_executor_result"), (), ())
        return result

    @staticmethod
    def _validate_snapshot(plan: ForwardRepairPlan, snapshot: RecoverySnapshot) -> None:
        if snapshot.target_ref != plan.target_ref:
            raise RecoveryError("target_mismatch", "journal returned a different recovery target")
        if snapshot.active_profile_ref != plan.active_profile_ref:
            raise RecoveryError("active_profile_mismatch", "active profile changed before forward repair")
        if snapshot.active_release_set_ref != plan.current_release_set_ref:
            raise RecoveryError("active_release_set_mismatch", "forward repair source set changed")
        if snapshot.revision != plan.expected_revision and snapshot.active_operation_id != plan.operation_id:
            raise RecoveryError("expected_state_mismatch", "recovery target revision changed")
        if snapshot.state not in _REPAIR_START_STATES:
            raise RecoveryError(
                "forward_repair_state_invalid",
                f"cannot start forward repair from {snapshot.state.value}",
            )



def _validate_owner_map(value: Mapping[str, str]) -> Mapping[str, str]:
    if not isinstance(value, Mapping) or not value:
        raise RecoveryError("owner_map_missing", "forward repair requires a canonical owner map")
    clean: dict[str, str] = {}
    for scope_ref, owner_ref in value.items():
        clean[require_text(scope_ref, "owner_scope_ref")] = require_text(owner_ref, "owner_ref")
    if any(owner in {"recovery-coordinator", "generic-operator"} for owner in clean.values()):
        raise RecoveryError(
            "owner_map_invalid",
            "the recovery coordinator cannot become a component data owner",
        )
    return freeze_mapping(clean)


def _validate_steps(
    value: Sequence[Mapping[str, Any]],
    owner_map: Mapping[str, str],
) -> tuple[Mapping[str, Any], ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or not value:
        raise RecoveryError("repair_steps_missing", "forward repair requires ordered steps")
    result: list[Mapping[str, Any]] = []
    seen_steps: set[str] = set()
    seen_checkpoints: set[str] = set()
    for raw in value:
        if not isinstance(raw, Mapping):
            raise RecoveryError("repair_step_invalid", "repair step must be a mapping")
        step = {
            "step_id": require_text(raw.get("step_id"), "step_id"),
            "scope_ref": require_text(raw.get("scope_ref"), "scope_ref"),
            "owner_ref": require_text(raw.get("owner_ref"), "owner_ref"),
            "operation_ref": require_text(raw.get("operation_ref"), "operation_ref"),
            "checkpoint_ref": require_text(raw.get("checkpoint_ref"), "checkpoint_ref"),
            "idempotency_key": require_text(raw.get("idempotency_key"), "idempotency_key"),
            "source_state_ref": require_text(raw.get("source_state_ref"), "source_state_ref"),
            "target_state_ref": require_text(raw.get("target_state_ref"), "target_state_ref"),
        }
        if step["step_id"] in seen_steps:
            raise RecoveryError("repair_step_duplicate", "repair step identifiers must be unique")
        if step["checkpoint_ref"] in seen_checkpoints:
            raise RecoveryError("checkpoint_duplicate", "checkpoint references must be unique")
        if owner_map.get(step["scope_ref"]) != step["owner_ref"]:
            raise RecoveryError("repair_owner_mismatch", "repair step does not use its canonical owner")
        seen_steps.add(step["step_id"])
        seen_checkpoints.add(step["checkpoint_ref"])
        result.append(freeze_mapping(step))
    return tuple(result)


__all__ = ["ExecuteForwardRepair", "ForwardRepairPlan"]
