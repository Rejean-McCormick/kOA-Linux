"""Enter a separately governed recovery environment."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from . import (
    AuthorityContext,
    Clock,
    DecisionOutcome,
    EvidencePreserver,
    OperationOutcome,
    RecoveryAuthority,
    RecoveryEnvironmentController,
    RecoveryEnvironmentSpec,
    RecoveryError,
    RecoveryJournal,
    RecoveryPath,
    RecoveryResult,
    RecoverySnapshot,
    RecoveryState,
    build_receipt,
    canonical_digest,
    check_idempotency,
    commit_state,
    require_aware_datetime,
    require_text,
    require_text_tuple,
    validate_authority,
)


_ENTERABLE_STATES = (
    RecoveryState.NORMAL,
    RecoveryState.DEGRADED,
    RecoveryState.RECOVERY_REQUIRED,
)


@dataclass(frozen=True, slots=True)
class EnterRecoveryRequest:
    operation_id: str
    target_ref: str
    incident_ref: str
    initiating_condition: str
    active_profile_ref: str
    last_verified_release_set_ref: str
    intended_result: str
    selected_procedure: RecoveryPath
    authority: AuthorityContext
    environment: RecoveryEnvironmentSpec
    expected_revision: int
    requested_at: datetime
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "operation_id",
            "target_ref",
            "incident_ref",
            "initiating_condition",
            "active_profile_ref",
            "last_verified_release_set_ref",
            "intended_result",
        ):
            object.__setattr__(self, name, require_text(getattr(self, name), name))
        if self.expected_revision < 0:
            raise RecoveryError("revision_invalid", "expected revision cannot be negative")
        object.__setattr__(self, "requested_at", require_aware_datetime(self.requested_at, "requested_at"))
        object.__setattr__(
            self,
            "evidence_refs",
            require_text_tuple(self.evidence_refs, "evidence_refs"),
        )
        if not isinstance(self.selected_procedure, RecoveryPath):
            raise RecoveryError("recovery_path_invalid", "selected_procedure must be a declared recovery path")
        if self.selected_procedure is RecoveryPath.PROTECTED_EXIT and self.intended_result == "recovered_normal":
            raise RecoveryError(
                "recovery_intent_invalid",
                "protected exit cannot claim normal recovery",
            )

    def digest_input(self) -> Mapping[str, Any]:
        return {
            "operation_id": self.operation_id,
            "target_ref": self.target_ref,
            "incident_ref": self.incident_ref,
            "initiating_condition": self.initiating_condition,
            "active_profile_ref": self.active_profile_ref,
            "last_verified_release_set_ref": self.last_verified_release_set_ref,
            "intended_result": self.intended_result,
            "selected_procedure": self.selected_procedure.value,
            "authority": {
                "actor_ref": self.authority.actor_ref,
                "authority_domain": self.authority.authority_domain,
                "role_refs": self.authority.role_refs,
                "scope_refs": self.authority.scope_refs,
                "authorized_until": self.authority.authorized_until,
                "decision_ref": self.authority.decision_ref,
            },
            "environment": {
                "environment_ref": self.environment.environment_ref,
                "version": self.environment.version,
                "profile_ref": self.environment.profile_ref,
                "artifact_ref": self.environment.artifact_ref,
                "trust_ref": self.environment.trust_ref,
                "access_scope_refs": self.environment.access_scope_refs,
                "network_path_refs": self.environment.network_path_refs,
            },
            "expected_revision": self.expected_revision,
            "requested_at": self.requested_at,
            "evidence_refs": self.evidence_refs,
        }


class EnterRecovery:
    def __init__(
        self,
        *,
        journal: RecoveryJournal,
        authority: RecoveryAuthority,
        evidence: EvidencePreserver,
        environment_controller: RecoveryEnvironmentController,
        clock: Clock,
    ) -> None:
        self._journal = journal
        self._authority = authority
        self._evidence = evidence
        self._environment = environment_controller
        self._clock = clock

    def __call__(self, request: EnterRecoveryRequest) -> RecoveryResult:
        request_digest = canonical_digest(request.digest_input())
        prior = check_idempotency(
            self._journal,
            operation_id=request.operation_id,
            request_digest=request_digest,
        )
        if prior is not None:
            return prior

        now = require_aware_datetime(self._clock.now(), "clock.now")
        validate_authority(request.authority, at=now, target_ref=request.target_ref)
        snapshot = self._journal.snapshot(request.target_ref)
        self._validate_snapshot(request, snapshot)

        try:
            decision = self._authority.authorize(
                action="recovery.enter",
                target_ref=request.target_ref,
                authority=request.authority,
                context={
                    "incident_ref": request.incident_ref,
                    "initiating_condition": request.initiating_condition,
                    "active_profile_ref": request.active_profile_ref,
                    "last_verified_release_set_ref": request.last_verified_release_set_ref,
                    "selected_procedure": request.selected_procedure.value,
                    "environment_ref": request.environment.environment_ref,
                    "intended_result": request.intended_result,
                },
                evaluated_at=now,
            )
        except Exception as exc:
            return self._terminal_without_effect(
                request,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                reason_codes=("recovery_authority_unavailable", type(exc).__name__),
            )
        if decision.outcome is not DecisionOutcome.ALLOW:
            return self._terminal_without_effect(
                request,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                reason_codes=(f"recovery_authority_{decision.outcome.value}", *decision.reason_codes),
                evidence_refs=decision.evidence_refs,
            )

        try:
            preserved = self._evidence.preserve(
                target_ref=request.target_ref,
                incident_ref=request.incident_ref,
                active_release_set_ref=snapshot.active_release_set_ref,
                active_profile_ref=snapshot.active_profile_ref,
                requested_evidence_refs=request.evidence_refs,
                preserved_at=now,
            )
        except Exception as exc:
            return self._terminal_without_effect(
                request,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                reason_codes=("incident_evidence_preservation_failed", type(exc).__name__),
                evidence_refs=decision.evidence_refs,
            )
        if preserved.preserved_release_set_ref != snapshot.active_release_set_ref:
            return self._terminal_without_effect(
                request,
                snapshot,
                request_digest,
                outcome=OperationOutcome.BLOCKED,
                reason_codes=("preserved_release_identity_mismatch",),
                evidence_refs=(*decision.evidence_refs, *preserved.evidence_refs),
            )

        evidence_refs = tuple(dict.fromkeys((*decision.evidence_refs, *preserved.evidence_refs)))
        if snapshot.state is not RecoveryState.RECOVERY_LOCKED:
            lock_receipt = build_receipt(
                transition_type="recovery_entry_lock",
                operation_id=request.operation_id,
                target_ref=request.target_ref,
                authority=request.authority,
                from_state=snapshot.state,
                to_state=RecoveryState.RECOVERY_LOCKED,
                decision="authorized",
                execution_state="evidence_preserved",
                commit_state="committed",
                outcome="locked",
                recorded_at=now,
                active_release_set_ref=snapshot.active_release_set_ref,
                evidence_refs=evidence_refs,
                details={
                    "incident_ref": request.incident_ref,
                    "selected_procedure": request.selected_procedure.value,
                    "preserved_state_ref": preserved.preserved_state_ref,
                    "ordinary_writes_blocked": True,
                },
            )
            snapshot = commit_state(
                self._journal,
                snapshot=snapshot,
                operation_id=request.operation_id,
                request_digest=request_digest,
                next_state=RecoveryState.RECOVERY_LOCKED,
                receipt=lock_receipt,
                expected_states=_ENTERABLE_STATES,
            )
            receipt_refs = [lock_receipt.receipt_id]
        else:
            receipt_refs = []

        activation_time = require_aware_datetime(self._clock.now(), "clock.now")
        try:
            activation = self._environment.activate(
                target_ref=request.target_ref,
                environment=request.environment,
                incident_ref=request.incident_ref,
                activated_at=activation_time,
            )
        except Exception as exc:
            activation = None
            failure_reasons = ("recovery_environment_activation_failed", type(exc).__name__)
        else:
            failure_reasons = activation.reason_codes if not activation.passed else ()

        if activation is None or not activation.passed:
            failure_receipt = build_receipt(
                transition_type="recovery_environment_activation",
                operation_id=request.operation_id,
                target_ref=request.target_ref,
                authority=request.authority,
                from_state=snapshot.state,
                to_state=RecoveryState.RECOVERY_FAILED,
                decision="authorized",
                execution_state="failed",
                commit_state="committed_safe_failure",
                outcome="failed",
                recorded_at=activation_time,
                active_release_set_ref=snapshot.active_release_set_ref,
                reason_codes=failure_reasons,
                evidence_refs=evidence_refs,
                details={
                    "environment_ref": request.environment.environment_ref,
                    "ordinary_writes_remain_blocked": True,
                },
            )
            result = RecoveryResult(
                operation_id=request.operation_id,
                target_ref=request.target_ref,
                operation_kind="enter_recovery",
                outcome=OperationOutcome.FAILED,
                state=RecoveryState.RECOVERY_FAILED,
                active_release_set_ref=snapshot.active_release_set_ref,
                receipt_refs=tuple((*receipt_refs, failure_receipt.receipt_id)),
                reason_codes=failure_reasons,
                evidence_refs=evidence_refs,
            )
            commit_state(
                self._journal,
                snapshot=snapshot,
                operation_id=request.operation_id,
                request_digest=request_digest,
                next_state=RecoveryState.RECOVERY_FAILED,
                receipt=failure_receipt,
                terminal_result=result,
            )
            return result

        evidence_refs = tuple(dict.fromkeys((*evidence_refs, *activation.evidence_refs)))
        success_receipt = build_receipt(
            transition_type="recovery_environment_activation",
            operation_id=request.operation_id,
            target_ref=request.target_ref,
            authority=request.authority,
            from_state=snapshot.state,
            to_state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE,
            decision="authorized",
            execution_state="completed",
            commit_state="committed",
            outcome="recovery_environment_active",
            recorded_at=activation_time,
            active_release_set_ref=snapshot.active_release_set_ref,
            evidence_refs=evidence_refs,
            details={
                "incident_ref": request.incident_ref,
                "environment_ref": request.environment.environment_ref,
                "environment_version": request.environment.version,
                "selected_procedure": request.selected_procedure.value,
                "access_scope_refs": request.environment.access_scope_refs,
            },
        )
        result = RecoveryResult(
            operation_id=request.operation_id,
            target_ref=request.target_ref,
            operation_kind="enter_recovery",
            outcome=OperationOutcome.SUCCEEDED,
            state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE,
            active_release_set_ref=snapshot.active_release_set_ref,
            receipt_refs=tuple((*receipt_refs, success_receipt.receipt_id)),
            evidence_refs=evidence_refs,
        )
        commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=request.operation_id,
            request_digest=request_digest,
            next_state=RecoveryState.RECOVERY_ENVIRONMENT_ACTIVE,
            receipt=success_receipt,
            terminal_result=result,
        )
        return result

    @staticmethod
    def _validate_snapshot(request: EnterRecoveryRequest, snapshot: RecoverySnapshot) -> None:
        if snapshot.revision != request.expected_revision and snapshot.state is not RecoveryState.RECOVERY_LOCKED:
            raise RecoveryError("expected_state_mismatch", "recovery target revision changed")
        if snapshot.target_ref != request.target_ref:
            raise RecoveryError("target_mismatch", "journal returned a different recovery target")
        if snapshot.active_profile_ref != request.active_profile_ref:
            raise RecoveryError("active_profile_mismatch", "active profile changed before recovery entry")
        if request.environment.profile_ref != request.active_profile_ref:
            raise RecoveryError(
                "recovery_environment_profile_mismatch",
                "recovery environment is not compatible with the active profile",
            )
        if snapshot.active_release_set_ref != request.last_verified_release_set_ref:
            raise RecoveryError("active_release_set_mismatch", "active Release Set is not the last verified set")
        if snapshot.state in _ENTERABLE_STATES:
            return
        if (
            snapshot.state is RecoveryState.RECOVERY_LOCKED
            and snapshot.active_operation_id == request.operation_id
        ):
            return
        raise RecoveryError(
            "recovery_entry_state_invalid",
            f"cannot enter recovery from {snapshot.state.value}",
        )

    def _terminal_without_effect(
        self,
        request: EnterRecoveryRequest,
        snapshot: RecoverySnapshot,
        request_digest: str,
        *,
        outcome: OperationOutcome,
        reason_codes: tuple[str, ...],
        evidence_refs: tuple[str, ...] = (),
    ) -> RecoveryResult:
        now = require_aware_datetime(self._clock.now(), "clock.now")
        receipt = build_receipt(
            transition_type="recovery_entry_rejected",
            operation_id=request.operation_id,
            target_ref=request.target_ref,
            authority=request.authority,
            from_state=snapshot.state,
            to_state=snapshot.state,
            decision="blocked" if outcome is OperationOutcome.BLOCKED else "failed",
            execution_state="not_executed",
            commit_state="not_committed",
            outcome=outcome.value,
            recorded_at=now,
            active_release_set_ref=snapshot.active_release_set_ref,
            reason_codes=reason_codes,
            evidence_refs=evidence_refs,
            details={"ordinary_writes_changed": False},
        )
        result = RecoveryResult(
            operation_id=request.operation_id,
            target_ref=request.target_ref,
            operation_kind="enter_recovery",
            outcome=outcome,
            state=snapshot.state,
            active_release_set_ref=snapshot.active_release_set_ref,
            receipt_refs=(receipt.receipt_id,),
            reason_codes=reason_codes,
            evidence_refs=evidence_refs,
        )
        commit_state(
            self._journal,
            snapshot=snapshot,
            operation_id=request.operation_id,
            request_digest=request_digest,
            next_state=snapshot.state,
            receipt=receipt,
            terminal_result=result,
        )
        return result


__all__ = ["EnterRecovery", "EnterRecoveryRequest"]
