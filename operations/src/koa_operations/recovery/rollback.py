"""Rollback orchestration for a verified compatible Release Set."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

from . import (
    AuthorityContext,
    Clock,
    DecisionOutcome,
    OperationOutcome,
    RecoveryAuthority,
    RecoveryError,
    RecoveryJournal,
    RecoveryResult,
    RecoverySnapshot,
    RecoveryState,
    RollbackExecutor,
    ValidationResult,
    build_receipt,
    canonical_digest,
    check_idempotency,
    commit_state,
    freeze_mapping,
    require_aware_datetime,
    require_text,
    require_text_tuple,
    validate_authority,
)


_ROLLBACK_START_STATES = (
    RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE,
    RecoveryState.SOURCE_SELECTION,
    RecoveryState.RECOVERY_FAILED,
)


@dataclass(frozen=True, slots=True)
class RollbackPlan:
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
    source_ref: str
    source_producer_ref: str
    source_retention_ref: str
    compatibility_evidence_refs: tuple[str, ...]
    integrity_evidence_refs: tuple[str, ...]
    validation_refs: tuple[str, ...]
    completion_boundary_ref: str
    rollback_eligible: bool
    irreversible_boundary_crossed: bool
    restricted_capability_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "operation_id",
            "plan_ref",
            "target_ref",
            "incident_ref",
            "active_profile_ref",
            "current_release_set_ref",
            "target_release_set_ref",
            "source_ref",
            "source_producer_ref",
            "source_retention_ref",
            "completion_boundary_ref",
        ):
            object.__setattr__(self, name, require_text(getattr(self, name), name))
        if self.expected_revision < 0:
            raise RecoveryError("revision_invalid", "expected revision cannot be negative")
        object.__setattr__(self, "requested_at", require_aware_datetime(self.requested_at, "requested_at"))
        for name in ("compatibility_evidence_refs", "integrity_evidence_refs", "validation_refs"):
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
            raise RecoveryError("rollback_target_invalid", "rollback target must differ from the active set")
        if not self.rollback_eligible:
            raise RecoveryError("rollback_not_eligible", "target Release Set is not recovery eligible")
        if self.irreversible_boundary_crossed:
            raise RecoveryError(
                "rollback_incompatible_boundary_crossed",
                "rollback is prohibited after an irreversible or incompatible boundary",
            )

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
                "source_ref": self.source_ref,
                "source_producer_ref": self.source_producer_ref,
                "source_retention_ref": self.source_retention_ref,
                "compatibility_evidence_refs": self.compatibility_evidence_refs,
                "integrity_evidence_refs": self.integrity_evidence_refs,
                "validation_refs": self.validation_refs,
                "completion_boundary_ref": self.completion_boundary_ref,
                "rollback_eligible": self.rollback_eligible,
                "irreversible_boundary_crossed": self.irreversible_boundary_crossed,
                "restricted_capability_refs": self.restricted_capability_refs,
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


class ExecuteRollback:
    def __init__(
        self,
        *,
        journal: RecoveryJournal,
        authority: RecoveryAuthority,
        executor: RollbackExecutor,
        clock: Clock,
    ) -> None:
        self._journal = journal
        self._authority = authority
        self._executor = executor
        self._clock = clock

    def __call__(self, plan: RollbackPlan) -> RecoveryResult:
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
                action="recovery.rollback",
                target_ref=plan.target_ref,
                authority=plan.authority,
                context={
                    "plan_ref": plan.plan_ref,
                    "incident_ref": plan.incident_ref,
                    "current_release_set_ref": plan.current_release_set_ref,
                    "target_release_set_ref": plan.target_release_set_ref,
                    "source_ref": plan.source_ref,
                    "completion_boundary_ref": plan.completion_boundary_ref,
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
                reason_codes=("rollback_authority_unavailable", type(exc).__name__),
            )
        if decision.outcome is not DecisionOutcome.ALLOW:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                state=snapshot.state,
                reason_codes=(f"rollback_authority_{decision.outcome.value}", *decision.reason_codes),
                evidence_refs=decision.evidence_refs,
            )

        receipt_refs: list[str] = []
        evidence_refs: list[str] = list(
            dict.fromkeys(
                (
                    *decision.evidence_refs,
                    *plan.compatibility_evidence_refs,
                    *plan.integrity_evidence_refs,
                )
            )
        )
        if snapshot.state is not RecoveryState.SOURCE_SELECTION:
            selected_receipt = build_receipt(
                transition_type="rollback_selected",
                operation_id=plan.operation_id,
                target_ref=plan.target_ref,
                authority=plan.authority,
                from_state=snapshot.state,
                to_state=RecoveryState.SOURCE_SELECTION,
                decision="authorized",
                execution_state="source_selected",
                commit_state="committed",
                outcome="rollback_selected",
                recorded_at=now,
                active_release_set_ref=snapshot.active_release_set_ref,
                evidence_refs=evidence_refs,
                details={
                    "source_ref": plan.source_ref,
                    "source_producer_ref": plan.source_producer_ref,
                    "source_retention_ref": plan.source_retention_ref,
                    "target_release_set_ref": plan.target_release_set_ref,
                    "rollback_eligible": True,
                    "irreversible_boundary_crossed": False,
                },
            )
            snapshot = commit_state(
                self._journal,
                snapshot=snapshot,
                operation_id=plan.operation_id,
                request_digest=request_digest,
                next_state=RecoveryState.SOURCE_SELECTION,
                receipt=selected_receipt,
                expected_states=_ROLLBACK_START_STATES,
            )
            receipt_refs.append(selected_receipt.receipt_id)

        staging_receipt = build_receipt(
            transition_type="rollback_staging_started",
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
                "source_ref": plan.source_ref,
                "target_release_set_ref": plan.target_release_set_ref,
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

        staged = self._call_validation(
            "rollback_staging_failed",
            lambda: self._executor.stage(
                plan_mapping,
                staged_at=require_aware_datetime(self._clock.now(), "clock.now"),
            ),
        )
        evidence_refs.extend(staged.evidence_refs)
        if not staged.passed:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.FAILED,
                state=RecoveryState.RECOVERY_FAILED,
                reason_codes=staged.reason_codes,
                receipt_refs=receipt_refs,
                evidence_refs=evidence_refs,
            )

        validation_receipt = build_receipt(
            transition_type="rollback_validation_started",
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
            "rollback_validation_failed",
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
                evidence_refs=evidence_refs,
            )

        activation_receipt = build_receipt(
            transition_type="rollback_authority_activation",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.ACTIVATION_PENDING,
            decision="authorized",
            execution_state="atomic_cutover",
            commit_state="committed",
            outcome="rollback_target_active_pending_confirmation",
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
            "post_rollback_confirmation_failed",
            lambda: self._executor.confirm_active(
                plan_mapping,
                confirmed_at=require_aware_datetime(self._clock.now(), "clock.now"),
            ),
        )
        evidence_refs.extend(confirmation.evidence_refs)
        if not confirmation.passed:
            return self._restore_previous_after_failed_confirmation(
                plan,
                plan_mapping,
                snapshot,
                request_digest,
                receipt_refs,
                evidence_refs,
                confirmation.reason_codes,
            )

        restricted = tuple(
            dict.fromkeys((*plan.restricted_capability_refs, *confirmation.restricted_capability_refs))
        )
        final_state = (
            RecoveryState.RECOVERED_RESTRICTED if restricted else RecoveryState.RECOVERED_NORMAL
        )
        final_outcome = OperationOutcome.RESTRICTED if restricted else OperationOutcome.SUCCEEDED
        completion_receipt = build_receipt(
            transition_type="rollback_completed",
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
                "source_ref": plan.source_ref,
                "restricted_capability_refs": restricted,
            },
        )
        result = RecoveryResult(
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            operation_kind="rollback",
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

    def _restore_previous_after_failed_confirmation(
        self,
        plan: RollbackPlan,
        plan_mapping: Mapping[str, Any],
        snapshot: RecoverySnapshot,
        request_digest: str,
        receipt_refs: Sequence[str],
        evidence_refs: Sequence[str],
        confirmation_reasons: Sequence[str],
    ) -> RecoveryResult:
        compensation_receipt = build_receipt(
            transition_type="rollback_confirmation_compensation",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.RECOVERY_FAILED,
            decision="authorized",
            execution_state="restoring_previous_authority",
            commit_state="receipt_persisted_before_compensation",
            outcome="pending",
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=plan.current_release_set_ref,
            reason_codes=confirmation_reasons,
            evidence_refs=evidence_refs,
            details={
                "failed_target_release_set_ref": plan.target_release_set_ref,
                "restore_release_set_ref": plan.current_release_set_ref,
            },
        )
        try:
            self._journal.retain_receipt(compensation_receipt)
        except Exception as exc:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.FAILED,
                state=RecoveryState.RECOVERY_FAILED,
                reason_codes=(
                    *confirmation_reasons,
                    "compensation_receipt_persistence_failed",
                    type(exc).__name__,
                    "manual_recovery_required",
                ),
                receipt_refs=receipt_refs,
                evidence_refs=evidence_refs,
                active_release_set_ref=plan.target_release_set_ref,
            )

        compensation = self._call_validation(
            "previous_authority_restore_indeterminate",
            lambda: self._executor.restore_previous_authority(
                plan_mapping,
                compensation_receipt,
                restored_at=require_aware_datetime(self._clock.now(), "clock.now"),
            ),
        )
        combined_evidence = tuple(dict.fromkeys((*evidence_refs, *compensation.evidence_refs)))
        if not compensation.passed:
            return self._terminal(
                plan,
                snapshot,
                request_digest,
                outcome=OperationOutcome.FAILED,
                state=RecoveryState.RECOVERY_FAILED,
                reason_codes=(
                    *confirmation_reasons,
                    *compensation.reason_codes,
                    "manual_recovery_required",
                ),
                receipt_refs=(*receipt_refs, compensation_receipt.receipt_id),
                evidence_refs=combined_evidence,
                active_release_set_ref=plan.target_release_set_ref,
            )

        reasons = tuple(dict.fromkeys((*confirmation_reasons, "previous_authority_restored")))
        final_receipt = build_receipt(
            transition_type="rollback_failed_previous_authority_restored",
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            authority=plan.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.RECOVERY_FAILED,
            decision="authorized",
            execution_state="compensated",
            commit_state="committed_safe_state",
            outcome="failed",
            recorded_at=require_aware_datetime(self._clock.now(), "clock.now"),
            active_release_set_ref=plan.current_release_set_ref,
            reason_codes=reasons,
            evidence_refs=combined_evidence,
            details={"ordinary_writes_remain_blocked": True},
        )
        result = RecoveryResult(
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            operation_kind="rollback",
            outcome=OperationOutcome.FAILED,
            state=RecoveryState.RECOVERY_FAILED,
            active_release_set_ref=plan.current_release_set_ref,
            receipt_refs=tuple(
                (*receipt_refs, compensation_receipt.receipt_id, final_receipt.receipt_id)
            ),
            reason_codes=reasons,
            evidence_refs=combined_evidence,
        )
        commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=plan.operation_id,
            request_digest=request_digest,
            next_state=RecoveryState.RECOVERY_FAILED,
            receipt=final_receipt,
            active_release_set_ref=plan.current_release_set_ref,
            terminal_result=result,
        )
        return result

    def _terminal(
        self,
        plan: RollbackPlan,
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
            transition_type="rollback_terminal",
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
            details={"ordinary_writes_remain_blocked": True, "blind_retry_allowed": False},
        )
        result = RecoveryResult(
            operation_id=plan.operation_id,
            target_ref=plan.target_ref,
            operation_kind="rollback",
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
    def _validate_snapshot(plan: RollbackPlan, snapshot: RecoverySnapshot) -> None:
        if snapshot.target_ref != plan.target_ref:
            raise RecoveryError("target_mismatch", "journal returned a different recovery target")
        if snapshot.active_profile_ref != plan.active_profile_ref:
            raise RecoveryError("active_profile_mismatch", "active profile changed before rollback")
        if snapshot.active_release_set_ref != plan.current_release_set_ref:
            raise RecoveryError("active_release_set_mismatch", "rollback source set changed")
        if snapshot.revision != plan.expected_revision and snapshot.active_operation_id != plan.operation_id:
            raise RecoveryError("expected_state_mismatch", "recovery target revision changed")
        if snapshot.state not in _ROLLBACK_START_STATES:
            raise RecoveryError(
                "rollback_state_invalid",
                f"cannot start rollback from {snapshot.state.value}",
            )


__all__ = ["ExecuteRollback", "RollbackPlan"]
