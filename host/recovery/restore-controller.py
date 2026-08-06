#!/usr/bin/env python3
"""Stage and coordinate owner-controlled restore or Release Set rollback."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tomllib
from typing import Any, Mapping, Protocol, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from host.adapters.filesystem import (  # noqa: E402
    DuplicateJsonKeyError,
    FilesystemAdapterError,
    IntegrityError,
    SafeFilesystem,
    UnsafePathError,
)


class RestoreControllerError(RuntimeError):
    """Raised when a restore plan or transition is invalid."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+/-]{2,255}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ALLOWED_METHODS = frozenset({"rollback_release_set", "restore_from_backup", "rebuild_from_artifacts"})
_METHOD_STEPS: dict[str, tuple[str, ...]] = {
    "rollback_release_set": (
        "preserve_evidence",
        "verify_source",
        "stage_source",
        "verify_candidate",
        "request_activation",
        "verify_activation",
        "record_completion",
    ),
    "restore_from_backup": (
        "preserve_evidence",
        "verify_source",
        "stage_source",
        "owner_restore",
        "verify_candidate",
        "request_activation",
        "verify_activation",
        "record_completion",
    ),
    "rebuild_from_artifacts": (
        "preserve_evidence",
        "verify_source",
        "stage_source",
        "owner_restore",
        "verify_candidate",
        "request_activation",
        "verify_activation",
        "record_completion",
    ),
}
_STATE_BY_STEP = {
    "preserve_evidence": "recovery_locked",
    "verify_source": "source_selection",
    "stage_source": "staging",
    "owner_restore": "staging",
    "verify_candidate": "validation",
    "request_activation": "activation_pending",
    "verify_activation": "activation_pending",
    "record_completion": "recovered_normal",
}


def _duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json(path: Path, *, max_bytes: int) -> dict[str, Any]:
    if not path.is_absolute() or path.is_symlink() or not path.is_file():
        raise RestoreControllerError(f"expected an absolute regular non-symlink JSON file: {path}")
    if path.stat().st_size > max_bytes:
        raise RestoreControllerError(f"JSON file exceeds configured size limit: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_duplicate_guard)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RestoreControllerError(f"invalid UTF-8 JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise RestoreControllerError("top-level JSON value must be an object")
    return payload


def _identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value) or ".." in value:
        raise RestoreControllerError(f"invalid identifier in {field}")
    return value


def _timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise RestoreControllerError(f"{field} must be a timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RestoreControllerError(f"invalid timestamp in {field}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise RestoreControllerError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class ControllerPolicy:
    policy_id: str
    state_root: Path
    staging_root: Path
    runtime_root: Path
    lock_name: str
    max_plan_bytes: int
    max_artifact_bytes: int
    require_receipt_before_commit: bool
    require_source_digest: bool
    require_owner_validation: bool
    require_last_known_good_identity: bool
    activate_authority_last: bool
    boot_dependency_bundle: str

    @classmethod
    def load(cls, path: Path) -> "ControllerPolicy":
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise RestoreControllerError(f"unable to load recovery policy: {path}") from exc
        runtime = data.get("runtime")
        authority = data.get("authority")
        recovery = data.get("recovery")
        boot = data.get("boot_boundary")
        if not all(isinstance(section, dict) for section in (runtime, authority, recovery, boot)):
            raise RestoreControllerError("recovery policy is missing required sections")
        try:
            result = cls(
                policy_id=_identifier(data["policy_id"], "policy_id"),
                state_root=Path(runtime["state_root"]),
                staging_root=Path(runtime["staging_root"]),
                runtime_root=Path(runtime["runtime_root"]),
                lock_name=str(runtime["lock_name"]),
                max_plan_bytes=int(runtime["max_plan_bytes"]),
                max_artifact_bytes=int(runtime["max_artifact_bytes"]),
                require_receipt_before_commit=bool(authority["require_receipt_before_commit"]),
                require_source_digest=bool(recovery["require_source_digest"]),
                require_owner_validation=bool(recovery["require_owner_validation"]),
                require_last_known_good_identity=bool(recovery["require_last_known_good_identity"]),
                activate_authority_last=bool(recovery["activate_authority_last"]),
                boot_dependency_bundle=str(boot["dependency_bundle"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise RestoreControllerError("recovery policy contains invalid controller values") from exc
        for root in (result.state_root, result.staging_root, result.runtime_root):
            if not root.is_absolute():
                raise RestoreControllerError("controller roots must be absolute")
        if result.max_plan_bytes <= 0 or result.max_artifact_bytes <= 0:
            raise RestoreControllerError("controller limits must be positive")
        return result


@dataclass(frozen=True, slots=True)
class RestoreSource:
    artifact_ref: str
    owner_ref: str
    source_release_set_ref: str
    path: Path
    sha256: str
    verification_receipt_ref: str
    last_known_good: bool

    @classmethod
    def from_mapping(cls, value: Any) -> "RestoreSource":
        if not isinstance(value, Mapping):
            raise RestoreControllerError("source must be an object")
        required = {
            "artifact_ref",
            "owner_ref",
            "source_release_set_ref",
            "path",
            "sha256",
            "verification_receipt_ref",
            "last_known_good",
        }
        if set(value) != required:
            raise RestoreControllerError(
                f"source fields mismatch; missing={sorted(required - set(value))}, unknown={sorted(set(value) - required)}"
            )
        path = Path(str(value["path"]))
        if not path.is_absolute() or ".." in path.parts:
            raise RestoreControllerError("source.path must be an absolute normalized path")
        digest = str(value["sha256"])
        if not _SHA256.fullmatch(digest):
            raise RestoreControllerError("source.sha256 must be lowercase SHA-256")
        return cls(
            artifact_ref=_identifier(value["artifact_ref"], "source.artifact_ref"),
            owner_ref=_identifier(value["owner_ref"], "source.owner_ref"),
            source_release_set_ref=_identifier(value["source_release_set_ref"], "source.source_release_set_ref"),
            path=path,
            sha256=digest,
            verification_receipt_ref=_identifier(
                value["verification_receipt_ref"], "source.verification_receipt_ref"
            ),
            last_known_good=bool(value["last_known_good"]),
        )


@dataclass(frozen=True, slots=True)
class RestorePlan:
    plan_id: str
    recovery_id: str
    method: str
    target_id: str
    actor_id: str
    created_at: datetime
    expected_active_release_set_ref: str
    target_release_set_ref: str
    authority_receipt_ref: str
    evidence_refs: tuple[str, ...]
    source: RestoreSource
    steps: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any], *, policy: ControllerPolicy) -> "RestorePlan":
        required = {
            "schema_version",
            "plan_id",
            "recovery_id",
            "method",
            "target_id",
            "actor_id",
            "created_at",
            "expected_active_release_set_ref",
            "target_release_set_ref",
            "authority_receipt_ref",
            "evidence_refs",
            "source",
            "steps",
        }
        if set(value) != required:
            raise RestoreControllerError(
                f"plan fields mismatch; missing={sorted(required - set(value))}, unknown={sorted(set(value) - required)}"
            )
        if value["schema_version"] != "1.0.0":
            raise RestoreControllerError("unsupported restore plan schema_version")
        method = str(value["method"])
        if method not in _ALLOWED_METHODS:
            raise RestoreControllerError(f"unsupported restore method: {method}")
        raw_steps = value["steps"]
        if not isinstance(raw_steps, list) or any(not isinstance(item, str) for item in raw_steps):
            raise RestoreControllerError("steps must be an array of strings")
        steps = tuple(raw_steps)
        if steps != _METHOD_STEPS[method]:
            raise RestoreControllerError(f"restore steps must exactly match the registered sequence for {method}")
        evidence = value["evidence_refs"]
        if not isinstance(evidence, list) or not evidence or any(not isinstance(item, str) for item in evidence):
            raise RestoreControllerError("evidence_refs must be a non-empty string array")
        if len(set(evidence)) != len(evidence):
            raise RestoreControllerError("evidence_refs must be unique")
        source = RestoreSource.from_mapping(value["source"])
        target_release = _identifier(value["target_release_set_ref"], "target_release_set_ref")
        if method == "rollback_release_set":
            if policy.require_last_known_good_identity and not source.last_known_good:
                raise RestoreControllerError("rollback source must be declared last-known-good")
            if source.source_release_set_ref != target_release:
                raise RestoreControllerError("rollback target must equal the source Release Set identity")
        return cls(
            plan_id=_identifier(value["plan_id"], "plan_id"),
            recovery_id=_identifier(value["recovery_id"], "recovery_id"),
            method=method,
            target_id=_identifier(value["target_id"], "target_id"),
            actor_id=_identifier(value["actor_id"], "actor_id"),
            created_at=_timestamp(value["created_at"], "created_at"),
            expected_active_release_set_ref=_identifier(
                value["expected_active_release_set_ref"], "expected_active_release_set_ref"
            ),
            target_release_set_ref=target_release,
            authority_receipt_ref=_identifier(value["authority_receipt_ref"], "authority_receipt_ref"),
            evidence_refs=tuple(evidence),
            source=source,
            steps=steps,
        )

    def as_context(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "recovery_id": self.recovery_id,
            "method": self.method,
            "target_id": self.target_id,
            "actor_id": self.actor_id,
            "expected_active_release_set_ref": self.expected_active_release_set_ref,
            "target_release_set_ref": self.target_release_set_ref,
            "authority_receipt_ref": self.authority_receipt_ref,
            "evidence_refs": list(self.evidence_refs),
            "source": {
                "artifact_ref": self.source.artifact_ref,
                "owner_ref": self.source.owner_ref,
                "source_release_set_ref": self.source.source_release_set_ref,
                "path": str(self.source.path),
                "sha256": self.source.sha256,
                "verification_receipt_ref": self.source.verification_receipt_ref,
                "last_known_good": self.source.last_known_good,
            },
        }


@dataclass(frozen=True, slots=True)
class StepResult:
    status: str
    reason_code: str
    evidence_refs: tuple[str, ...] = ()
    receipt_ref: str | None = None
    observations: tuple[str, ...] = ()
    outputs: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.status not in {"completed", "blocked", "failed"}:
            raise ValueError("step status must be completed, blocked, or failed")
        if not re.fullmatch(r"^[A-Z][A-Z0-9_:-]{1,127}$", self.reason_code):
            raise ValueError("reason_code must be a stable uppercase identifier")


class RestoreExecutor(Protocol):
    def execute(self, step: str, context: Mapping[str, Any]) -> StepResult:
        """Execute one registered step without changing the step order."""


class SafePrefixExecutor:
    """Executes only source verification and staging, then fails closed.

    Owner-controlled restore and B-0081 activation are intentionally not
    implemented here.  Production assembly must inject those public ports.
    """

    def __init__(self, *, policy: ControllerPolicy) -> None:
        self._policy = policy
        self._staging = SafeFilesystem(policy.staging_root, create=True)

    def execute(self, step: str, context: Mapping[str, Any]) -> StepResult:
        source = context["source"]
        assert isinstance(source, Mapping)
        if step == "preserve_evidence":
            evidence = tuple(str(item) for item in context["evidence_refs"])
            if not evidence:
                return StepResult("blocked", "RECOVERY_EVIDENCE_MISSING")
            return StepResult("completed", "RECOVERY_EVIDENCE_PRESERVED", evidence_refs=evidence)
        if step == "verify_source":
            path = Path(str(source["path"]))
            if path.is_symlink() or not path.is_file():
                return StepResult("blocked", "RECOVERY_SOURCE_NOT_REGULAR")
            if path.stat().st_size > self._policy.max_artifact_bytes:
                return StepResult("blocked", "RECOVERY_SOURCE_TOO_LARGE")
            digest = hashlib.sha256()
            try:
                with path.open("rb") as handle:
                    while chunk := handle.read(1024 * 1024):
                        digest.update(chunk)
            except OSError as exc:
                return StepResult("blocked", "RECOVERY_SOURCE_UNREADABLE", observations=(str(exc),))
            actual = digest.hexdigest()
            if actual != source["sha256"]:
                return StepResult("blocked", "RECOVERY_SOURCE_DIGEST_MISMATCH")
            return StepResult(
                "completed",
                "RECOVERY_SOURCE_VERIFIED",
                evidence_refs=(str(source["verification_receipt_ref"]),),
                outputs={"sha256": actual, "size": path.stat().st_size},
            )
        if step == "stage_source":
            source_path = Path(str(source["path"]))
            destination = f"{context['recovery_id']}/{context['plan_id']}/{source_path.name}"
            try:
                staged = self._staging.copy_verified(
                    source_path,
                    destination,
                    expected_sha256=str(source["sha256"]),
                    max_bytes=self._policy.max_artifact_bytes,
                    overwrite=False,
                )
            except (FilesystemAdapterError, IntegrityError, UnsafePathError, OSError) as exc:
                return StepResult("failed", "RECOVERY_SOURCE_STAGING_FAILED", observations=(str(exc),))
            return StepResult(
                "completed",
                "RECOVERY_SOURCE_STAGED",
                outputs={"staged_path": str(staged), "sha256": str(source["sha256"])},
            )
        if step == "owner_restore":
            return StepResult("blocked", "COMPONENT_OWNER_RESTORE_INTERFACE_REQUIRED")
        if step in {"verify_candidate", "request_activation", "verify_activation"}:
            return StepResult("blocked", f"{self._policy.boot_dependency_bundle}_PUBLIC_INTERFACE_REQUIRED")
        return StepResult("blocked", "RECOVERY_COMPLETION_NOT_REACHED")


def _state_record(
    *,
    plan: RestorePlan,
    state: str,
    sequence: int,
    timestamp: datetime,
    next_actions: Sequence[str],
    authority_transition_permitted: bool,
    terminal_result: str | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema_version": "1.0.0",
        "recovery_id": plan.recovery_id,
        "plan_id": plan.plan_id,
        "state": state,
        "sequence": sequence,
        "updated_at": timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "authority_transition_permitted": authority_transition_permitted,
        "next_valid_actions": list(next_actions),
    }
    if terminal_result is not None:
        record["terminal_result"] = terminal_result
    return record


def run_restore_plan(
    plan: RestorePlan,
    *,
    policy: ControllerPolicy,
    executor: RestoreExecutor,
    now: datetime | None = None,
) -> dict[str, Any]:
    timestamp = now or datetime.now(timezone.utc)
    state_fs = SafeFilesystem(policy.state_root, create=True)
    runtime_fs = SafeFilesystem(policy.runtime_root, create=True)
    base = plan.recovery_id
    entry = state_fs.read_json(f"{base}/entry.json", max_bytes=policy.max_plan_bytes)
    state = state_fs.read_json(f"{base}/state.json", max_bytes=policy.max_plan_bytes)
    if entry.get("target_id") != plan.target_id or entry.get("actor_id") != plan.actor_id:
        raise RestoreControllerError("restore plan does not match the admitted recovery entry")
    if entry.get("authority_receipt_ref") != plan.authority_receipt_ref:
        raise RestoreControllerError("restore plan authority receipt does not match recovery entry")
    if entry.get("active_release_set_ref") != plan.expected_active_release_set_ref:
        raise RestoreControllerError("expected active Release Set does not match recovery entry")
    if state.get("state") not in {"recovery_locked", "source_selection", "staging", "validation"}:
        raise RestoreControllerError(f"recovery state does not admit a restore plan: {state.get('state')}")

    sequence = int(state.get("sequence", 1))
    results: list[dict[str, Any]] = []
    context = plan.as_context()
    with runtime_fs.exclusive_lock(policy.lock_name):
        state_fs.atomic_write_json(f"{base}/plans/{plan.plan_id}.json", {
            "schema_version": "1.0.0",
            **context,
            "created_at": plan.created_at.isoformat().replace("+00:00", "Z"),
            "steps": list(plan.steps),
        }, overwrite=False)
        state_fs.ensure_directory(f"{base}/plans")
        # The directory may have been created by atomic_write_json; resolve it before checkpoints.
        state_fs.ensure_directory(f"{base}/checkpoints/{plan.plan_id}")
        for index, step in enumerate(plan.steps, start=1):
            step_time = datetime.now(timezone.utc)
            result = executor.execute(step, context)
            sequence += 1
            result_record: dict[str, Any] = {
                "schema_version": "1.0.0",
                "recovery_id": plan.recovery_id,
                "plan_id": plan.plan_id,
                "step": step,
                "step_index": index,
                "status": result.status,
                "reason_code": result.reason_code,
                "timestamp": step_time.isoformat().replace("+00:00", "Z"),
                "evidence_refs": list(result.evidence_refs),
                "observations": list(result.observations),
            }
            if result.receipt_ref is not None:
                result_record["receipt_ref"] = result.receipt_ref
            if result.outputs is not None:
                result_record["outputs"] = dict(result.outputs)
                context = {**context, "step_outputs": {**dict(context.get("step_outputs", {})), step: dict(result.outputs)}}
            state_fs.atomic_write_json(
                f"{base}/checkpoints/{plan.plan_id}/{index:06d}-{step}.json",
                result_record,
                overwrite=False,
            )
            results.append(result_record)

            if result.status != "completed":
                terminal = "recovery_blocked" if result.status == "blocked" else "recovery_failed"
                failure_state = _state_record(
                    plan=plan,
                    state="recovery_failed",
                    sequence=sequence,
                    timestamp=step_time,
                    next_actions=["inspect_evidence", "select_alternate_source", "forward_repair", "decommission"],
                    authority_transition_permitted=False,
                    terminal_result=terminal,
                )
                failure_state["failed_step"] = step
                failure_state["reason_code"] = result.reason_code
                state_fs.atomic_write_json(f"{base}/state.json", failure_state)
                return {
                    "schema_version": "1.0.0",
                    "record_type": "restore_result",
                    "recovery_id": plan.recovery_id,
                    "plan_id": plan.plan_id,
                    "result": terminal,
                    "failed_step": step,
                    "reason_code": result.reason_code,
                    "authority_changed": False,
                    "steps": results,
                }

            if step == "request_activation" and policy.require_receipt_before_commit and not result.receipt_ref:
                raise RestoreControllerError("activation request completed without required durable receipt")
            if step == "verify_activation" and policy.require_receipt_before_commit and not result.receipt_ref:
                raise RestoreControllerError("activation verification completed without required durable receipt")

            next_actions = [plan.steps[index]] if index < len(plan.steps) else []
            state_fs.atomic_write_json(
                f"{base}/state.json",
                _state_record(
                    plan=plan,
                    state=_STATE_BY_STEP[step],
                    sequence=sequence,
                    timestamp=step_time,
                    next_actions=next_actions,
                    authority_transition_permitted=step in {"request_activation", "verify_activation"},
                ),
            )

        if policy.activate_authority_last and plan.steps[-2:] != ("verify_activation", "record_completion"):
            raise RestoreControllerError("authority activation must be verified immediately before completion")
        completion_receipt = results[-2].get("receipt_ref")
        if policy.require_receipt_before_commit and not completion_receipt:
            raise RestoreControllerError("restore completion lacks an activation verification receipt")
        completion = {
            "schema_version": "1.0.0",
            "record_type": "restore_result",
            "recovery_id": plan.recovery_id,
            "plan_id": plan.plan_id,
            "result": "service_restored",
            "active_release_set_ref": plan.target_release_set_ref,
            "previous_release_set_ref": plan.expected_active_release_set_ref,
            "activation_receipt_ref": completion_receipt,
            "authority_changed": True,
            "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "steps": results,
        }
        state_fs.atomic_write_json(f"{base}/result.json", completion, overwrite=False)
        return completion


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Validate the plan and print its fixed step sequence")
    mode.add_argument(
        "--execute-safe-prefix",
        action="store_true",
        help="Verify and stage the source, then stop at the first unavailable owner/B-0081 boundary",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        policy = ControllerPolicy.load(args.policy)
        payload = _load_json(args.plan, max_bytes=policy.max_plan_bytes)
        plan = RestorePlan.from_mapping(payload, policy=policy)
        if args.dry_run:
            result = {
                "schema_version": "1.0.0",
                "record_type": "restore_plan_validation",
                "plan_id": plan.plan_id,
                "recovery_id": plan.recovery_id,
                "method": plan.method,
                "steps": list(plan.steps),
                "result": "admitted_for_staging",
                "authority_changed": False,
                "production_execution_requires": ["component_owner_restore_port", policy.boot_dependency_bundle],
            }
        else:
            result = run_restore_plan(plan, policy=policy, executor=SafePrefixExecutor(policy=policy))
    except (RestoreControllerError, FilesystemAdapterError, OSError) as exc:
        print(f"restore controller failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.get("result") in {"admitted_for_staging", "service_restored"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
