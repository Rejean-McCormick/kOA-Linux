"""Acceptance, cleanup, and atomic admission of restored candidate state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol

from .plan import AcceptanceCheck, Gate, RestorePlan
from .run import EvidenceSink, RestoreRunResult, RunStatus


class RestoreVerificationError(RuntimeError):
    """Raised when verification wiring or evidence is internally inconsistent."""


class CheckStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


class VerificationStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class CheckResult:
    check_id: str
    gate: Gate
    status: CheckStatus
    evidence_ref: str
    verified_at: datetime
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.check_id or not self.evidence_ref:
            raise RestoreVerificationError("check result requires identifiers and evidence")
        if self.verified_at.tzinfo is None:
            raise RestoreVerificationError("check timestamp must be timezone-aware")
        object.__setattr__(self, "details", MappingProxyType(dict(sorted(self.details.items()))))


@dataclass(frozen=True, slots=True)
class ControlResult:
    succeeded: bool
    evidence_ref: str
    completed_at: datetime
    disposition: str

    def __post_init__(self) -> None:
        if not self.evidence_ref or not self.disposition:
            raise RestoreVerificationError("control result requires evidence and disposition")
        if self.completed_at.tzinfo is None:
            raise RestoreVerificationError("control timestamp must be timezone-aware")


class AcceptanceVerifier(Protocol):
    def verify(self, plan: RestorePlan, run: RestoreRunResult, check: AcceptanceCheck) -> CheckResult:
        """Evaluate one check through the authority named by its contract."""


class TemporaryAuthorityCleanup(Protocol):
    def cleanup(self, plan: RestorePlan, run: RestoreRunResult) -> ControlResult:
        """Revoke temporary identities, mounts, credentials, paths, and privileges."""


class TrafficAdmission(Protocol):
    def admit(self, plan: RestorePlan, run: RestoreRunResult, evidence_refs: tuple[str, ...]) -> ControlResult:
        """Atomically admit the accepted capability through the owning authority."""


@dataclass(frozen=True, slots=True)
class RestoreVerificationResult:
    verification_id: str
    plan_id: str
    plan_digest: str
    run_id: str
    status: VerificationStatus
    started_at: datetime
    completed_at: datetime
    checks: tuple[CheckResult, ...]
    evidence_refs: tuple[str, ...]
    cleanup_completed: bool
    traffic_admitted: bool
    authority_active: bool
    final_disposition: str
    failed_check_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.verification_id or not self.plan_id or not self.run_id:
            raise RestoreVerificationError("verification result requires stable identifiers")
        if self.completed_at < self.started_at:
            raise RestoreVerificationError("verification completion precedes its start")
        if self.status is VerificationStatus.ACCEPTED:
            if not all((self.cleanup_completed, self.traffic_admitted, self.authority_active)):
                raise RestoreVerificationError("accepted restore requires cleanup and atomic traffic admission")
            if self.failed_check_ids:
                raise RestoreVerificationError("accepted restore cannot contain failed checks")
        else:
            if self.traffic_admitted or self.authority_active:
                raise RestoreVerificationError("rejected or blocked restore cannot admit traffic")

    def public_evidence(self) -> Mapping[str, Any]:
        return MappingProxyType(
            {
                "verification_id": self.verification_id,
                "plan_id": self.plan_id,
                "plan_digest": self.plan_digest,
                "run_id": self.run_id,
                "status": self.status.value,
                "check_statuses": {item.check_id: item.status.value for item in self.checks},
                "failed_check_ids": self.failed_check_ids,
                "cleanup_completed": self.cleanup_completed,
                "traffic_admitted": self.traffic_admitted,
                "authority_active": self.authority_active,
                "final_disposition": self.final_disposition,
                "completed_at": self.completed_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
        )


def _record(
    evidence_sink: EvidenceSink,
    *,
    event_type: str,
    verification_id: str,
    plan: RestorePlan,
    run: RestoreRunResult,
    now: datetime,
    disposition: str | None = None,
    evidence_ref: str | None = None,
) -> str:
    event: dict[str, Any] = {
        "event_type": event_type,
        "verification_id": verification_id,
        "restore_id": plan.scope.restore_id,
        "plan_id": plan.plan_id,
        "plan_digest": plan.plan_digest,
        "run_id": run.run_id,
        "correlation_id": plan.scope.correlation_id,
        "recorded_at": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if disposition is not None:
        event["final_disposition"] = disposition
    if evidence_ref is not None:
        event["control_evidence_ref"] = evidence_ref
    return evidence_sink.record(event)


def _blocked_result(
    *,
    verification_id: str,
    plan: RestorePlan,
    run: RestoreRunResult,
    started_at: datetime,
    completed_at: datetime,
    checks: list[CheckResult],
    evidence_refs: list[str],
    disposition: str,
    failed_ids: tuple[str, ...],
    cleanup_completed: bool = False,
) -> RestoreVerificationResult:
    return RestoreVerificationResult(
        verification_id=verification_id,
        plan_id=plan.plan_id,
        plan_digest=plan.plan_digest,
        run_id=run.run_id,
        status=VerificationStatus.BLOCKED,
        started_at=started_at,
        completed_at=completed_at,
        checks=tuple(checks),
        evidence_refs=tuple(evidence_refs),
        cleanup_completed=cleanup_completed,
        traffic_admitted=False,
        authority_active=False,
        final_disposition=disposition,
        failed_check_ids=failed_ids,
    )


def verify_restore(
    plan: RestorePlan,
    run: RestoreRunResult,
    *,
    verification_id: str,
    verifier: AcceptanceVerifier,
    cleanup: TemporaryAuthorityCleanup,
    traffic_admission: TrafficAdmission,
    evidence_sink: EvidenceSink,
    clock: Callable[[], datetime],
) -> RestoreVerificationResult:
    """Verify all required gates, clean temporary authority, then admit atomically."""

    if not verification_id.strip():
        raise RestoreVerificationError("verification_id is required")
    started_at = clock()
    if started_at.tzinfo is None:
        raise RestoreVerificationError("clock must return timezone-aware timestamps")
    if run.plan_id != plan.plan_id or run.plan_digest != plan.plan_digest:
        raise RestoreVerificationError("run result does not belong to the supplied plan")
    evidence_refs: list[str] = [
        _record(
            evidence_sink,
            event_type="restore.verification.opened",
            verification_id=verification_id,
            plan=plan,
            run=run,
            now=started_at,
        )
    ]
    if run.status is not RunStatus.CANDIDATE_READY:
        completed_at = clock()
        evidence_refs.append(
            _record(
                evidence_sink,
                event_type="restore.verification.blocked",
                verification_id=verification_id,
                plan=plan,
                run=run,
                now=completed_at,
                disposition="candidate_not_ready",
            )
        )
        return _blocked_result(
            verification_id=verification_id,
            plan=plan,
            run=run,
            started_at=started_at,
            completed_at=completed_at,
            checks=[],
            evidence_refs=evidence_refs,
            disposition="candidate_not_ready",
            failed_ids=(),
        )

    checks: list[CheckResult] = []
    failed_ids: list[str] = []
    gate_order = tuple(Gate)
    for gate in gate_order:
        for check in (item for item in plan.acceptance_checks if item.gate is gate):
            result = verifier.verify(plan, run, check)
            if result.check_id != check.check_id or result.gate is not check.gate:
                raise RestoreVerificationError("verifier returned a result for a different acceptance check")
            checks.append(result)
            evidence_refs.append(result.evidence_ref)
            if result.status is not CheckStatus.PASSED:
                failed_ids.append(result.check_id)
        if failed_ids:
            completed_at = clock()
            disposition = f"{gate.value}_gate_failed_keep_candidate_isolated"
            evidence_refs.append(
                _record(
                    evidence_sink,
                    event_type="restore.verification.gate_failed",
                    verification_id=verification_id,
                    plan=plan,
                    run=run,
                    now=completed_at,
                    disposition=disposition,
                )
            )
            return _blocked_result(
                verification_id=verification_id,
                plan=plan,
                run=run,
                started_at=started_at,
                completed_at=completed_at,
                checks=checks,
                evidence_refs=evidence_refs,
                disposition=disposition,
                failed_ids=tuple(failed_ids),
            )

    cleanup_result = cleanup.cleanup(plan, run)
    evidence_refs.append(cleanup_result.evidence_ref)
    if not cleanup_result.succeeded:
        evidence_refs.append(
            _record(
                evidence_sink,
                event_type="restore.cleanup.failed",
                verification_id=verification_id,
                plan=plan,
                run=run,
                now=cleanup_result.completed_at,
                disposition="temporary_authority_cleanup_failed_keep_restricted",
                evidence_ref=cleanup_result.evidence_ref,
            )
        )
        return _blocked_result(
            verification_id=verification_id,
            plan=plan,
            run=run,
            started_at=started_at,
            completed_at=cleanup_result.completed_at,
            checks=checks,
            evidence_refs=evidence_refs,
            disposition="temporary_authority_cleanup_failed_keep_restricted",
            failed_ids=(),
        )

    admission_result = traffic_admission.admit(plan, run, tuple(evidence_refs))
    evidence_refs.append(admission_result.evidence_ref)
    if not admission_result.succeeded:
        evidence_refs.append(
            _record(
                evidence_sink,
                event_type="restore.traffic_admission.failed",
                verification_id=verification_id,
                plan=plan,
                run=run,
                now=admission_result.completed_at,
                disposition="atomic_admission_failed_preserve_previous_authority",
                evidence_ref=admission_result.evidence_ref,
            )
        )
        return _blocked_result(
            verification_id=verification_id,
            plan=plan,
            run=run,
            started_at=started_at,
            completed_at=admission_result.completed_at,
            checks=checks,
            evidence_refs=evidence_refs,
            disposition="atomic_admission_failed_preserve_previous_authority",
            failed_ids=(),
            cleanup_completed=True,
        )

    completed_at = admission_result.completed_at
    evidence_refs.append(
        _record(
            evidence_sink,
            event_type="restore.accepted_and_admitted",
            verification_id=verification_id,
            plan=plan,
            run=run,
            now=completed_at,
            disposition="accepted_normal_authority_active",
            evidence_ref=admission_result.evidence_ref,
        )
    )
    return RestoreVerificationResult(
        verification_id=verification_id,
        plan_id=plan.plan_id,
        plan_digest=plan.plan_digest,
        run_id=run.run_id,
        status=VerificationStatus.ACCEPTED,
        started_at=started_at,
        completed_at=completed_at,
        checks=tuple(checks),
        evidence_refs=tuple(evidence_refs),
        cleanup_completed=True,
        traffic_admitted=True,
        authority_active=True,
        final_disposition="accepted_normal_authority_active",
        failed_check_ids=(),
    )
