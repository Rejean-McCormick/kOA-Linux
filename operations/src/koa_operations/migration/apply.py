"""Restart-safe application of an accepted migration plan."""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
import json
import re
from typing import Protocol

from .plan import LifecycleState, MigrationPlan, MigrationStep, PreflightCheck

_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_SENSITIVE_KEY = re.compile(r"(?:secret|password|token|credential|private|payload|record)", re.IGNORECASE)


class RunState(StrEnum):
    BLOCKED = "blocked"
    EXECUTING = "executing"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass(frozen=True, slots=True)
class PreflightResult:
    check: PreflightCheck
    passed: bool
    reason_code: str

    def __post_init__(self) -> None:
        if not self.reason_code or self.reason_code != self.reason_code.strip():
            raise ValueError("preflight reason_code must be non-empty and trimmed")


@dataclass(frozen=True, slots=True)
class StepResult:
    step_id: str
    effect_id: str
    effect_digest_sha256: str
    completed_work_units: int
    state_fingerprint_sha256: str
    quarantined_unit_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.step_id or not self.effect_id:
            raise ValueError("step result identifiers must be non-empty")
        if not _HEX_64.fullmatch(self.effect_digest_sha256):
            raise ValueError("effect digest must be lowercase SHA-256")
        if not _HEX_64.fullmatch(self.state_fingerprint_sha256):
            raise ValueError("state fingerprint must be lowercase SHA-256")
        if self.completed_work_units < 0:
            raise ValueError("completed_work_units must be non-negative")
        if len(self.quarantined_unit_ids) != len(set(self.quarantined_unit_ids)):
            raise ValueError("quarantined work unit identifiers must be unique")


@dataclass(frozen=True, slots=True)
class CompletedStep:
    step_id: str
    effect_id: str
    effect_digest_sha256: str
    completed_work_units: int
    state_fingerprint_sha256: str

    def to_dict(self) -> dict[str, object]:
        return {
            "step_id": self.step_id,
            "effect_id": self.effect_id,
            "effect_digest_sha256": self.effect_digest_sha256,
            "completed_work_units": self.completed_work_units,
            "state_fingerprint_sha256": self.state_fingerprint_sha256,
        }


@dataclass(frozen=True, slots=True)
class MigrationCheckpoint:
    migration_id: str
    plan_digest_sha256: str
    source_fingerprint_sha256: str
    current_state_fingerprint_sha256: str
    expected_target_fingerprint_sha256: str
    state: RunState
    completed_steps: tuple[CompletedStep, ...]
    attempt_counts: tuple[tuple[str, int], ...] = ()
    active_step_id: str | None = None
    failure_reason_code: str | None = None

    def __post_init__(self) -> None:
        if not _HEX_64.fullmatch(self.plan_digest_sha256):
            raise ValueError("checkpoint plan digest must be lowercase SHA-256")
        if not _HEX_64.fullmatch(self.source_fingerprint_sha256):
            raise ValueError("checkpoint source fingerprint must be lowercase SHA-256")
        if not _HEX_64.fullmatch(self.current_state_fingerprint_sha256):
            raise ValueError("checkpoint current-state fingerprint must be lowercase SHA-256")
        if not _HEX_64.fullmatch(self.expected_target_fingerprint_sha256):
            raise ValueError("checkpoint target fingerprint must be lowercase SHA-256")
        attempt_ids = tuple(step_id for step_id, _ in self.attempt_counts)
        if len(attempt_ids) != len(set(attempt_ids)) or any(count < 1 for _, count in self.attempt_counts):
            raise ValueError("checkpoint attempt counts must be unique positive values")
        ids = tuple(item.step_id for item in self.completed_steps)
        if len(ids) != len(set(ids)):
            raise ValueError("checkpoint cannot contain duplicate completed steps")
        effects = tuple(item.effect_id for item in self.completed_steps)
        if len(effects) != len(set(effects)):
            raise ValueError("checkpoint cannot contain duplicate effects")
        if self.state is RunState.FAILED and not self.failure_reason_code:
            raise ValueError("failed checkpoint requires a reason code")

    def to_dict(self) -> dict[str, object]:
        return {
            "migration_id": self.migration_id,
            "plan_digest_sha256": self.plan_digest_sha256,
            "source_fingerprint_sha256": self.source_fingerprint_sha256,
            "current_state_fingerprint_sha256": self.current_state_fingerprint_sha256,
            "expected_target_fingerprint_sha256": self.expected_target_fingerprint_sha256,
            "state": self.state.value,
            "completed_steps": [item.to_dict() for item in self.completed_steps],
            "attempt_counts": {step_id: count for step_id, count in self.attempt_counts},
            "active_step_id": self.active_step_id,
            "failure_reason_code": self.failure_reason_code,
        }

    @property
    def digest_sha256(self) -> str:
        encoded = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    evidence_id: str
    migration_id: str
    plan_digest_sha256: str
    event_type: str
    state: str
    operator_id: str
    occurred_at: str
    reason_code: str
    checkpoint_digest_sha256: str | None = None
    step_id: str | None = None
    attributes: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        if not self.evidence_id or not self.migration_id or not self.event_type:
            raise ValueError("evidence identifiers and event type must be non-empty")
        if not _HEX_64.fullmatch(self.plan_digest_sha256):
            raise ValueError("evidence plan digest must be lowercase SHA-256")
        if self.checkpoint_digest_sha256 is not None and not _HEX_64.fullmatch(self.checkpoint_digest_sha256):
            raise ValueError("checkpoint digest must be lowercase SHA-256")
        parsed = datetime.fromisoformat(self.occurred_at.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("evidence timestamp must include a timezone")
        if len(self.attributes) != len({key for key, _ in self.attributes}):
            raise ValueError("evidence attribute keys must be unique")
        for key, value in self.attributes:
            if _SENSITIVE_KEY.search(key):
                raise ValueError("evidence attributes may not name sensitive payload fields")
            if len(key) > 64 or len(value) > 256 or "\n" in value:
                raise ValueError("evidence attributes must be bounded and single-line")

    def to_dict(self) -> dict[str, object]:
        return {
            "evidence_id": self.evidence_id,
            "migration_id": self.migration_id,
            "plan_digest_sha256": self.plan_digest_sha256,
            "event_type": self.event_type,
            "state": self.state,
            "operator_id": self.operator_id,
            "occurred_at": self.occurred_at,
            "reason_code": self.reason_code,
            "checkpoint_digest_sha256": self.checkpoint_digest_sha256,
            "step_id": self.step_id,
            "attributes": {key: value for key, value in self.attributes},
        }


@dataclass(frozen=True, slots=True)
class MigrationRun:
    state: RunState
    checkpoint: MigrationCheckpoint | None
    reason_code: str
    evidence: tuple[EvidenceRecord, ...]


class MigrationDriver(Protocol):
    def source_fingerprint(self, plan: MigrationPlan) -> str: ...
    def preflight(self, plan: MigrationPlan) -> tuple[PreflightResult, ...]: ...
    def revalidate_resume(self, plan: MigrationPlan, checkpoint: MigrationCheckpoint) -> tuple[PreflightResult, ...]: ...
    def execute_step(self, plan: MigrationPlan, step: MigrationStep, checkpoint: MigrationCheckpoint) -> StepResult: ...


class CheckpointRepository(Protocol):
    def load(self, migration_id: str) -> MigrationCheckpoint | None: ...
    def save(self, checkpoint: MigrationCheckpoint) -> None: ...


class EvidenceWriter(Protocol):
    def write(self, record: EvidenceRecord) -> None: ...


def _utc_timestamp(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("clock must return a timezone-aware datetime")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _evidence_id(plan: MigrationPlan, sequence: int, event_type: str, step_id: str | None) -> str:
    material = f"{plan.digest_sha256}|{sequence}|{event_type}|{step_id or '-'}".encode("utf-8")
    return f"evidence.migration.{sha256(material).hexdigest()[:24]}"


def _emit(
    *,
    plan: MigrationPlan,
    writer: EvidenceWriter,
    records: list[EvidenceRecord],
    now: datetime,
    operator_id: str,
    event_type: str,
    state: str,
    reason_code: str,
    checkpoint: MigrationCheckpoint | None = None,
    step_id: str | None = None,
    attributes: tuple[tuple[str, str], ...] = (),
) -> None:
    record = EvidenceRecord(
        evidence_id=_evidence_id(plan, len(records) + 1, event_type, step_id),
        migration_id=plan.migration_id,
        plan_digest_sha256=plan.digest_sha256,
        event_type=event_type,
        state=state,
        operator_id=operator_id,
        occurred_at=_utc_timestamp(now),
        reason_code=reason_code,
        checkpoint_digest_sha256=checkpoint.digest_sha256 if checkpoint else None,
        step_id=step_id,
        attributes=attributes,
    )
    writer.write(record)
    records.append(record)


def _validate_results(plan: MigrationPlan, results: tuple[PreflightResult, ...]) -> tuple[bool, str]:
    if len(results) != len(set(item.check for item in results)):
        return False, "preflight.duplicate_check"
    expected = set(plan.preflight_checks)
    received = {item.check for item in results}
    if received != expected:
        return False, "preflight.incomplete"
    failed = sorted(item.check.value for item in results if not item.passed)
    if failed:
        return False, f"preflight.failed.{failed[0]}"
    return True, "preflight.passed"


def apply_migration(
    plan: MigrationPlan,
    *,
    driver: MigrationDriver,
    checkpoints: CheckpointRepository,
    evidence_writer: EvidenceWriter,
    operator_id: str,
    now: datetime,
    resume: bool = False,
) -> MigrationRun:
    """Apply bounded steps and persist a checkpoint after each confirmed effect.

    Operational failures return a blocked or failed run and always emit evidence.
    Integrity errors in driver results are converted to failed checkpoints rather
    than being presented as completion.
    """
    if plan.lifecycle_state is not LifecycleState.STAGED:
        raise ValueError("only a staged migration plan may execute")
    if not operator_id or operator_id != operator_id.strip():
        raise ValueError("operator_id must be non-empty and trimmed")

    records: list[EvidenceRecord] = []
    existing = checkpoints.load(plan.migration_id)
    observed_source = driver.source_fingerprint(plan)
    if not _HEX_64.fullmatch(observed_source):
        raise ValueError("driver source fingerprint must be lowercase SHA-256")

    if existing is None:
        if observed_source != plan.expected_source_fingerprint:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_blocked", state=RunState.BLOCKED.value,
                  reason_code="source.fingerprint_mismatch",
                  attributes=(("expected_digest", plan.expected_source_fingerprint), ("observed_digest", observed_source)))
            return MigrationRun(RunState.BLOCKED, None, "source.fingerprint_mismatch", tuple(records))
        valid, reason = _validate_results(plan, driver.preflight(plan))
        if not valid:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_blocked", state=RunState.BLOCKED.value, reason_code=reason)
            return MigrationRun(RunState.BLOCKED, None, reason, tuple(records))
        checkpoint = MigrationCheckpoint(
            migration_id=plan.migration_id,
            plan_digest_sha256=plan.digest_sha256,
            source_fingerprint_sha256=observed_source,
            current_state_fingerprint_sha256=observed_source,
            expected_target_fingerprint_sha256=plan.expected_target_fingerprint,
            state=RunState.EXECUTING,
            completed_steps=(),
        )
        checkpoints.save(checkpoint)
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_started", state=RunState.EXECUTING.value,
              reason_code="execution.started", checkpoint=checkpoint)
    else:
        checkpoint = existing
        if checkpoint.plan_digest_sha256 != plan.digest_sha256:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_blocked", state=RunState.BLOCKED.value,
                  reason_code="resume.plan_changed", checkpoint=checkpoint)
            return MigrationRun(RunState.BLOCKED, checkpoint, "resume.plan_changed", tuple(records))
        if checkpoint.state is RunState.COMPLETED:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_noop", state=RunState.COMPLETED.value,
                  reason_code="execution.already_completed", checkpoint=checkpoint)
            return MigrationRun(RunState.COMPLETED, checkpoint, "execution.already_completed", tuple(records))
        if not resume:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_paused", state=RunState.PAUSED.value,
                  reason_code="resume.explicit_action_required", checkpoint=checkpoint)
            return MigrationRun(RunState.PAUSED, checkpoint, "resume.explicit_action_required", tuple(records))
        if observed_source != checkpoint.current_state_fingerprint_sha256:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_blocked", state=RunState.BLOCKED.value,
                  reason_code="resume.source_changed", checkpoint=checkpoint)
            return MigrationRun(RunState.BLOCKED, checkpoint, "resume.source_changed", tuple(records))
        valid, reason = _validate_results(plan, driver.revalidate_resume(plan, checkpoint))
        if not valid:
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_blocked", state=RunState.BLOCKED.value,
                  reason_code=f"resume.{reason}", checkpoint=checkpoint)
            return MigrationRun(RunState.BLOCKED, checkpoint, f"resume.{reason}", tuple(records))
        checkpoint = replace(checkpoint, state=RunState.EXECUTING, active_step_id=None, failure_reason_code=None)
        checkpoints.save(checkpoint)
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_resumed", state=RunState.EXECUTING.value,
              reason_code="resume.revalidated", checkpoint=checkpoint)

    completed_ids = {item.step_id for item in checkpoint.completed_steps}
    prior_effects = {item.effect_id for item in checkpoint.completed_steps}
    for step in plan.steps:
        if step.step_id in completed_ids:
            continue
        attempts = dict(checkpoint.attempt_counts)
        prior_attempts = attempts.get(step.step_id, 0)
        if prior_attempts > step.retry_limit:
            failed = replace(checkpoint, state=RunState.FAILED, active_step_id=step.step_id,
                             failure_reason_code="step.retry_limit_exhausted")
            checkpoints.save(failed)
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_failed", state=RunState.FAILED.value,
                  reason_code="step.retry_limit_exhausted", checkpoint=failed, step_id=step.step_id)
            return MigrationRun(RunState.FAILED, failed, "step.retry_limit_exhausted", tuple(records))
        attempts[step.step_id] = prior_attempts + 1
        checkpoint = replace(checkpoint, active_step_id=step.step_id, state=RunState.EXECUTING,
                             attempt_counts=tuple(sorted(attempts.items())))
        checkpoints.save(checkpoint)
        _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
              event_type="migration_step_started", state=RunState.EXECUTING.value,
              reason_code="step.started", checkpoint=checkpoint, step_id=step.step_id,
              attributes=(("operation_id", step.operation_id), ("idempotency_key", step.idempotency_key)))
        try:
            result = driver.execute_step(plan, step, checkpoint)
            if result.step_id != step.step_id:
                raise ValueError("driver returned a result for a different step")
            if result.completed_work_units > step.maximum_work_units:
                raise ValueError("driver exceeded the bounded work-unit limit")
            if result.effect_id in prior_effects:
                raise ValueError("driver repeated an already committed effect")
            if result.quarantined_unit_ids:
                raise RuntimeError("step.quarantined_units")
            completed = CompletedStep(
                step_id=result.step_id,
                effect_id=result.effect_id,
                effect_digest_sha256=result.effect_digest_sha256,
                completed_work_units=result.completed_work_units,
                state_fingerprint_sha256=result.state_fingerprint_sha256,
            )
            checkpoint = replace(
                checkpoint,
                completed_steps=checkpoint.completed_steps + (completed,),
                current_state_fingerprint_sha256=result.state_fingerprint_sha256,
                active_step_id=None,
                failure_reason_code=None,
            )
            checkpoints.save(checkpoint)
            prior_effects.add(result.effect_id)
            completed_ids.add(result.step_id)
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_step_completed", state=RunState.EXECUTING.value,
                  reason_code="step.effect_committed", checkpoint=checkpoint, step_id=step.step_id,
                  attributes=(("effect_digest", result.effect_digest_sha256),
                              ("completed_work_units", str(result.completed_work_units))))
        except Exception as exc:
            reason = str(exc) if isinstance(exc, RuntimeError) and str(exc).startswith("step.") else "step.execution_failed"
            failed = replace(checkpoint, state=RunState.FAILED, failure_reason_code=reason)
            checkpoints.save(failed)
            _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
                  event_type="migration_failed", state=RunState.FAILED.value,
                  reason_code=reason, checkpoint=failed, step_id=step.step_id)
            return MigrationRun(RunState.FAILED, failed, reason, tuple(records))

    completed_checkpoint = replace(checkpoint, state=RunState.COMPLETED, active_step_id=None, failure_reason_code=None)
    checkpoints.save(completed_checkpoint)
    _emit(plan=plan, writer=evidence_writer, records=records, now=now, operator_id=operator_id,
          event_type="migration_execution_completed", state=RunState.COMPLETED.value,
          reason_code="execution.completed_pending_verification", checkpoint=completed_checkpoint)
    return MigrationRun(RunState.COMPLETED, completed_checkpoint, "execution.completed_pending_verification", tuple(records))
