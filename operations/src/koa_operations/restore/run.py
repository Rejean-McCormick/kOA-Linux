"""Execution of a restore plan into isolated candidate state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, Callable, Mapping, Protocol

from .plan import RestorePlan, RestoreStage, canonical_digest


class RestoreExecutionError(RuntimeError):
    """Raised for invalid execution wiring, never for a reported stage failure."""


class StageStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    REUSED = "reused"
    PLANNED = "planned"


class RunStatus(str, Enum):
    DRY_RUN = "dry_run"
    CANDIDATE_READY = "candidate_ready"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class StageExecution:
    stage_id: str
    status: StageStatus
    evidence_ref: str
    started_at: datetime
    completed_at: datetime
    checkpoint_ref: str | None = None
    safe_to_resume: bool = False
    candidate_mutated: bool = False
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.stage_id or not self.evidence_ref:
            raise RestoreExecutionError("stage execution requires identifiers and evidence")
        if self.started_at.tzinfo is None or self.completed_at.tzinfo is None:
            raise RestoreExecutionError("stage timestamps must be timezone-aware")
        if self.completed_at < self.started_at:
            raise RestoreExecutionError("stage completion precedes its start")
        object.__setattr__(self, "details", MappingProxyType(dict(sorted(self.details.items()))))
        if self.status is StageStatus.SUCCEEDED and self.safe_to_resume and not self.checkpoint_ref:
            raise RestoreExecutionError("resumable success requires a checkpoint reference")
        if self.status is not StageStatus.SUCCEEDED and self.status is not StageStatus.REUSED and self.safe_to_resume:
            raise RestoreExecutionError("failed or blocked stage cannot claim a safe checkpoint")


@dataclass(frozen=True, slots=True)
class StoredCheckpoint:
    plan_digest: str
    stage_digest: str
    evidence_ref: str
    checkpoint_ref: str
    safe_to_resume: bool


class RestoreExecutor(Protocol):
    def execute(self, plan: RestorePlan, stage: RestoreStage, *, idempotency_key: str) -> StageExecution:
        """Execute one declared stage through its owning public contract."""


class CheckpointStore(Protocol):
    def load(self, plan_id: str, stage_id: str) -> StoredCheckpoint | None:
        """Return the checkpoint for this exact plan and stage, if any."""

    def save(self, plan_id: str, stage_id: str, checkpoint: StoredCheckpoint) -> None:
        """Persist a safe checkpoint after the stage's evidence exists."""


class EvidenceSink(Protocol):
    def record(self, event: Mapping[str, Any]) -> str:
        """Persist minimized immutable evidence and return its reference."""


@dataclass(frozen=True, slots=True)
class RestoreRunResult:
    run_id: str
    plan_id: str
    plan_digest: str
    status: RunStatus
    started_at: datetime
    completed_at: datetime
    stages: tuple[StageExecution, ...]
    evidence_refs: tuple[str, ...]
    failed_stage_id: str | None
    final_disposition: str
    traffic_admitted: bool = False
    authority_active: bool = False
    previous_known_good_preserved: bool = True

    def __post_init__(self) -> None:
        if not self.run_id or not self.plan_id or not self.plan_digest:
            raise RestoreExecutionError("run result requires stable identifiers")
        if self.completed_at < self.started_at:
            raise RestoreExecutionError("run completion precedes its start")
        if self.traffic_admitted or self.authority_active:
            raise RestoreExecutionError("execution may only create isolated candidate state")
        if not self.previous_known_good_preserved:
            raise RestoreExecutionError("execution must preserve previous known-good authority")

    def public_evidence(self) -> Mapping[str, Any]:
        return MappingProxyType(
            {
                "run_id": self.run_id,
                "plan_id": self.plan_id,
                "plan_digest": self.plan_digest,
                "status": self.status.value,
                "started_at": self.started_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "completed_at": self.completed_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
                "stage_statuses": {item.stage_id: item.status.value for item in self.stages},
                "failed_stage_id": self.failed_stage_id,
                "final_disposition": self.final_disposition,
                "traffic_admitted": False,
                "authority_active": False,
                "previous_known_good_preserved": True,
            }
        )


def _idempotency_key(plan: RestorePlan, stage: RestoreStage) -> str:
    return canonical_digest({"plan_digest": plan.plan_digest, "stage_digest": stage.stage_digest})


def _record(
    evidence_sink: EvidenceSink,
    *,
    event_type: str,
    plan: RestorePlan,
    run_id: str,
    now: datetime,
    stage: StageExecution | None = None,
    disposition: str | None = None,
) -> str:
    event: dict[str, Any] = {
        "event_type": event_type,
        "restore_id": plan.scope.restore_id,
        "plan_id": plan.plan_id,
        "plan_digest": plan.plan_digest,
        "run_id": run_id,
        "correlation_id": plan.scope.correlation_id,
        "target_environment_id": plan.target.environment_id,
        "recorded_at": now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    if stage is not None:
        event.update(
            {
                "stage_id": stage.stage_id,
                "stage_status": stage.status.value,
                "stage_evidence_ref": stage.evidence_ref,
                "checkpoint_ref": stage.checkpoint_ref,
            }
        )
    if disposition is not None:
        event["final_disposition"] = disposition
    return evidence_sink.record(event)


def run_restore(
    plan: RestorePlan,
    *,
    run_id: str,
    executor: RestoreExecutor,
    checkpoint_store: CheckpointStore,
    evidence_sink: EvidenceSink,
    clock: Callable[[], datetime],
    dry_run: bool = False,
    cancel_requested: Callable[[], bool] | None = None,
) -> RestoreRunResult:
    """Execute declared stages while keeping traffic and normal authority blocked."""

    if not run_id.strip():
        raise RestoreExecutionError("run_id is required")
    started_at = clock()
    if started_at.tzinfo is None:
        raise RestoreExecutionError("clock must return timezone-aware timestamps")
    evidence_refs: list[str] = [
        _record(evidence_sink, event_type="restore.run.opened", plan=plan, run_id=run_id, now=started_at)
    ]
    stage_results: list[StageExecution] = []

    if dry_run:
        for stage in plan.stages:
            now = clock()
            stage_results.append(
                StageExecution(
                    stage_id=stage.stage_id,
                    status=StageStatus.PLANNED,
                    evidence_ref=f"dry-run:{plan.plan_id}:{stage.stage_id}",
                    started_at=now,
                    completed_at=now,
                    safe_to_resume=False,
                    candidate_mutated=False,
                    details={"stage_digest": stage.stage_digest, "would_mutate_candidate": stage.mutates_candidate},
                )
            )
        completed_at = clock()
        evidence_refs.append(
            _record(
                evidence_sink,
                event_type="restore.run.dry_run_completed",
                plan=plan,
                run_id=run_id,
                now=completed_at,
                disposition="planned_only",
            )
        )
        return RestoreRunResult(
            run_id=run_id,
            plan_id=plan.plan_id,
            plan_digest=plan.plan_digest,
            status=RunStatus.DRY_RUN,
            started_at=started_at,
            completed_at=completed_at,
            stages=tuple(stage_results),
            evidence_refs=tuple(evidence_refs),
            failed_stage_id=None,
            final_disposition="planned_only",
        )

    for stage in plan.stages:
        if cancel_requested is not None and cancel_requested():
            if not stage.cancellable:
                raise RestoreExecutionError(f"cancellation requested at non-cancellable stage {stage.stage_id}")
            now = clock()
            cancelled = StageExecution(
                stage_id=stage.stage_id,
                status=StageStatus.CANCELLED,
                evidence_ref=f"cancelled:{plan.plan_id}:{stage.stage_id}",
                started_at=now,
                completed_at=now,
                details={"reason": "operator_requested"},
            )
            stage_results.append(cancelled)
            evidence_refs.append(
                _record(evidence_sink, event_type="restore.stage.cancelled", plan=plan, run_id=run_id, now=now, stage=cancelled)
            )
            return RestoreRunResult(
                run_id=run_id,
                plan_id=plan.plan_id,
                plan_digest=plan.plan_digest,
                status=RunStatus.CANCELLED,
                started_at=started_at,
                completed_at=now,
                stages=tuple(stage_results),
                evidence_refs=tuple(evidence_refs),
                failed_stage_id=stage.stage_id,
                final_disposition="cancelled_at_safe_boundary",
            )

        checkpoint = checkpoint_store.load(plan.plan_id, stage.stage_id)
        if checkpoint is not None:
            if checkpoint.plan_digest != plan.plan_digest or checkpoint.stage_digest != stage.stage_digest:
                now = clock()
                evidence_refs.append(
                    _record(
                        evidence_sink,
                        event_type="restore.checkpoint.rejected",
                        plan=plan,
                        run_id=run_id,
                        now=now,
                        disposition="restart_from_clean_state",
                    )
                )
                return RestoreRunResult(
                    run_id=run_id,
                    plan_id=plan.plan_id,
                    plan_digest=plan.plan_digest,
                    status=RunStatus.BLOCKED,
                    started_at=started_at,
                    completed_at=now,
                    stages=tuple(stage_results),
                    evidence_refs=tuple(evidence_refs),
                    failed_stage_id=stage.stage_id,
                    final_disposition="checkpoint_mismatch_restart_from_clean_state",
                )
            if not stage.resumable or not checkpoint.safe_to_resume:
                now = clock()
                return RestoreRunResult(
                    run_id=run_id,
                    plan_id=plan.plan_id,
                    plan_digest=plan.plan_digest,
                    status=RunStatus.BLOCKED,
                    started_at=started_at,
                    completed_at=now,
                    stages=tuple(stage_results),
                    evidence_refs=tuple(evidence_refs),
                    failed_stage_id=stage.stage_id,
                    final_disposition="unsafe_checkpoint_restart_from_clean_state",
                )
            now = clock()
            reused = StageExecution(
                stage_id=stage.stage_id,
                status=StageStatus.REUSED,
                evidence_ref=checkpoint.evidence_ref,
                checkpoint_ref=checkpoint.checkpoint_ref,
                started_at=now,
                completed_at=now,
                safe_to_resume=True,
                candidate_mutated=stage.mutates_candidate,
                details={"stage_digest": stage.stage_digest},
            )
            stage_results.append(reused)
            evidence_refs.append(
                _record(evidence_sink, event_type="restore.stage.reused", plan=plan, run_id=run_id, now=now, stage=reused)
            )
            continue

        result = executor.execute(plan, stage, idempotency_key=_idempotency_key(plan, stage))
        if result.stage_id != stage.stage_id:
            raise RestoreExecutionError("executor returned a result for a different stage")
        if result.candidate_mutated and not stage.mutates_candidate:
            raise RestoreExecutionError(f"non-mutating stage {stage.stage_id} reported a candidate mutation")
        stage_results.append(result)
        evidence_refs.append(
            _record(
                evidence_sink,
                event_type=f"restore.stage.{result.status.value}",
                plan=plan,
                run_id=run_id,
                now=result.completed_at,
                stage=result,
            )
        )
        if result.status is not StageStatus.SUCCEEDED:
            disposition = {
                StageStatus.BLOCKED: "blocked_preserve_source_and_known_good",
                StageStatus.CANCELLED: "cancelled_preserve_source_and_known_good",
                StageStatus.FAILED: "failed_use_declared_repair_or_clean_retry",
            }.get(result.status, "failed_preserve_source_and_known_good")
            evidence_refs.append(
                _record(
                    evidence_sink,
                    event_type="restore.run.terminal_failure",
                    plan=plan,
                    run_id=run_id,
                    now=result.completed_at,
                    disposition=disposition,
                )
            )
            return RestoreRunResult(
                run_id=run_id,
                plan_id=plan.plan_id,
                plan_digest=plan.plan_digest,
                status=RunStatus.BLOCKED if result.status is StageStatus.BLOCKED else RunStatus.FAILED,
                started_at=started_at,
                completed_at=result.completed_at,
                stages=tuple(stage_results),
                evidence_refs=tuple(evidence_refs),
                failed_stage_id=stage.stage_id,
                final_disposition=disposition,
            )
        if stage.resumable:
            if not result.safe_to_resume or not result.checkpoint_ref:
                raise RestoreExecutionError(f"resumable stage {stage.stage_id} did not produce a safe checkpoint")
            checkpoint_store.save(
                plan.plan_id,
                stage.stage_id,
                StoredCheckpoint(
                    plan_digest=plan.plan_digest,
                    stage_digest=stage.stage_digest,
                    evidence_ref=result.evidence_ref,
                    checkpoint_ref=result.checkpoint_ref,
                    safe_to_resume=True,
                ),
            )

    completed_at = clock()
    evidence_refs.append(
        _record(
            evidence_sink,
            event_type="restore.run.candidate_ready",
            plan=plan,
            run_id=run_id,
            now=completed_at,
            disposition="candidate_awaiting_acceptance",
        )
    )
    return RestoreRunResult(
        run_id=run_id,
        plan_id=plan.plan_id,
        plan_digest=plan.plan_digest,
        status=RunStatus.CANDIDATE_READY,
        started_at=started_at,
        completed_at=completed_at,
        stages=tuple(stage_results),
        evidence_refs=tuple(evidence_refs),
        failed_stage_id=None,
        final_disposition="candidate_awaiting_acceptance",
    )
