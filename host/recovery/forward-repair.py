#!/usr/bin/env python3
"""Coordinate a declared forward repair without bypassing owner authority."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
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
    SafeFilesystem,
)


class ForwardRepairError(RuntimeError):
    """Raised when forward repair admission or execution fails."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+/-]{2,255}$")
_REASON = re.compile(r"^[A-Z][A-Z0-9_:-]{1,127}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_STEPS = (
    "preserve_evidence",
    "verify_rollback_prohibition",
    "verify_repair_artifact",
    "stage_repair",
    "owner_apply",
    "verify_checkpoint",
    "verify_repaired_state",
    "commit_repaired_authority",
    "record_completion",
)
_STATE_BY_STEP = {
    "preserve_evidence": "recovery_locked",
    "verify_rollback_prohibition": "source_selection",
    "verify_repair_artifact": "source_selection",
    "stage_repair": "staging",
    "owner_apply": "staging",
    "verify_checkpoint": "validation",
    "verify_repaired_state": "validation",
    "commit_repaired_authority": "activation_pending",
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
        raise ForwardRepairError(f"expected an absolute regular non-symlink JSON file: {path}")
    if path.stat().st_size > max_bytes:
        raise ForwardRepairError(f"JSON file exceeds configured limit: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_duplicate_guard)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ForwardRepairError(f"invalid UTF-8 JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ForwardRepairError("top-level JSON value must be an object")
    return payload


def _identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value) or ".." in value:
        raise ForwardRepairError(f"invalid identifier in {field}")
    return value


def _timestamp(value: Any, field: str) -> datetime:
    if not isinstance(value, str):
        raise ForwardRepairError(f"{field} must be a timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ForwardRepairError(f"invalid timestamp in {field}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ForwardRepairError(f"{field} must include a timezone")
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class RepairPolicy:
    policy_id: str
    state_root: Path
    staging_root: Path
    runtime_root: Path
    lock_name: str
    max_plan_bytes: int
    max_artifact_bytes: int
    require_receipt_before_commit: bool
    activate_authority_last: bool

    @classmethod
    def load(cls, path: Path) -> "RepairPolicy":
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise ForwardRepairError(f"unable to load recovery policy: {path}") from exc
        runtime = data.get("runtime")
        authority = data.get("authority")
        recovery = data.get("recovery")
        if not all(isinstance(section, dict) for section in (runtime, authority, recovery)):
            raise ForwardRepairError("recovery policy is missing required sections")
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
                activate_authority_last=bool(recovery["activate_authority_last"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ForwardRepairError("recovery policy contains invalid repair values") from exc
        for root in (result.state_root, result.staging_root, result.runtime_root):
            if not root.is_absolute():
                raise ForwardRepairError("repair roots must be absolute")
        return result


@dataclass(frozen=True, slots=True)
class RollbackProhibition:
    reason_code: str
    incompatible_state_ref: str
    evidence_refs: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Any) -> "RollbackProhibition":
        if not isinstance(value, Mapping):
            raise ForwardRepairError("rollback_prohibition must be an object")
        required = {"reason_code", "incompatible_state_ref", "evidence_refs"}
        if set(value) != required:
            raise ForwardRepairError("rollback_prohibition has unexpected fields")
        reason = str(value["reason_code"])
        if not _REASON.fullmatch(reason):
            raise ForwardRepairError("rollback prohibition reason_code is invalid")
        refs = value["evidence_refs"]
        if not isinstance(refs, list) or not refs or any(not isinstance(item, str) for item in refs):
            raise ForwardRepairError("rollback prohibition requires evidence_refs")
        if len(set(refs)) != len(refs):
            raise ForwardRepairError("rollback prohibition evidence_refs must be unique")
        return cls(
            reason_code=reason,
            incompatible_state_ref=_identifier(value["incompatible_state_ref"], "incompatible_state_ref"),
            evidence_refs=tuple(refs),
        )


@dataclass(frozen=True, slots=True)
class RepairArtifact:
    artifact_ref: str
    owner_ref: str
    path: Path
    sha256: str
    provenance_receipt_ref: str

    @classmethod
    def from_mapping(cls, value: Any) -> "RepairArtifact":
        if not isinstance(value, Mapping):
            raise ForwardRepairError("artifact must be an object")
        required = {"artifact_ref", "owner_ref", "path", "sha256", "provenance_receipt_ref"}
        if set(value) != required:
            raise ForwardRepairError("repair artifact has unexpected fields")
        path = Path(str(value["path"]))
        if not path.is_absolute() or ".." in path.parts:
            raise ForwardRepairError("repair artifact path must be absolute and normalized")
        digest = str(value["sha256"])
        if not _SHA256.fullmatch(digest):
            raise ForwardRepairError("repair artifact sha256 must be lowercase SHA-256")
        return cls(
            artifact_ref=_identifier(value["artifact_ref"], "artifact_ref"),
            owner_ref=_identifier(value["owner_ref"], "owner_ref"),
            path=path,
            sha256=digest,
            provenance_receipt_ref=_identifier(value["provenance_receipt_ref"], "provenance_receipt_ref"),
        )


@dataclass(frozen=True, slots=True)
class ForwardRepairPlan:
    repair_id: str
    recovery_id: str
    target_id: str
    actor_id: str
    created_at: datetime
    current_release_set_ref: str
    target_release_set_ref: str
    authority_receipt_ref: str
    evidence_refs: tuple[str, ...]
    rollback_prohibition: RollbackProhibition
    artifact: RepairArtifact
    steps: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ForwardRepairPlan":
        required = {
            "schema_version",
            "repair_id",
            "recovery_id",
            "target_id",
            "actor_id",
            "created_at",
            "current_release_set_ref",
            "target_release_set_ref",
            "authority_receipt_ref",
            "evidence_refs",
            "rollback_prohibition",
            "artifact",
            "steps",
        }
        if set(value) != required:
            raise ForwardRepairError(
                f"repair plan fields mismatch; missing={sorted(required - set(value))}, unknown={sorted(set(value) - required)}"
            )
        if value["schema_version"] != "1.0.0":
            raise ForwardRepairError("unsupported forward repair schema_version")
        steps_raw = value["steps"]
        if not isinstance(steps_raw, list) or tuple(steps_raw) != _STEPS:
            raise ForwardRepairError("forward repair steps must exactly match the registered sequence")
        evidence = value["evidence_refs"]
        if not isinstance(evidence, list) or not evidence or any(not isinstance(item, str) for item in evidence):
            raise ForwardRepairError("evidence_refs must be a non-empty string array")
        if len(set(evidence)) != len(evidence):
            raise ForwardRepairError("evidence_refs must be unique")
        current = _identifier(value["current_release_set_ref"], "current_release_set_ref")
        target = _identifier(value["target_release_set_ref"], "target_release_set_ref")
        if current == target:
            raise ForwardRepairError("forward repair target must differ from the current Release Set")
        return cls(
            repair_id=_identifier(value["repair_id"], "repair_id"),
            recovery_id=_identifier(value["recovery_id"], "recovery_id"),
            target_id=_identifier(value["target_id"], "target_id"),
            actor_id=_identifier(value["actor_id"], "actor_id"),
            created_at=_timestamp(value["created_at"], "created_at"),
            current_release_set_ref=current,
            target_release_set_ref=target,
            authority_receipt_ref=_identifier(value["authority_receipt_ref"], "authority_receipt_ref"),
            evidence_refs=tuple(evidence),
            rollback_prohibition=RollbackProhibition.from_mapping(value["rollback_prohibition"]),
            artifact=RepairArtifact.from_mapping(value["artifact"]),
            steps=tuple(steps_raw),
        )

    def context(self) -> dict[str, Any]:
        return {
            "repair_id": self.repair_id,
            "recovery_id": self.recovery_id,
            "target_id": self.target_id,
            "actor_id": self.actor_id,
            "current_release_set_ref": self.current_release_set_ref,
            "target_release_set_ref": self.target_release_set_ref,
            "authority_receipt_ref": self.authority_receipt_ref,
            "evidence_refs": list(self.evidence_refs),
            "rollback_prohibition": {
                "reason_code": self.rollback_prohibition.reason_code,
                "incompatible_state_ref": self.rollback_prohibition.incompatible_state_ref,
                "evidence_refs": list(self.rollback_prohibition.evidence_refs),
            },
            "artifact": {
                "artifact_ref": self.artifact.artifact_ref,
                "owner_ref": self.artifact.owner_ref,
                "path": str(self.artifact.path),
                "sha256": self.artifact.sha256,
                "provenance_receipt_ref": self.artifact.provenance_receipt_ref,
            },
        }


@dataclass(frozen=True, slots=True)
class RepairStepResult:
    status: str
    reason_code: str
    evidence_refs: tuple[str, ...] = ()
    receipt_ref: str | None = None
    observations: tuple[str, ...] = ()
    outputs: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.status not in {"completed", "blocked", "failed"}:
            raise ValueError("invalid repair step status")
        if not _REASON.fullmatch(self.reason_code):
            raise ValueError("invalid repair step reason code")


class ForwardRepairExecutor(Protocol):
    def execute(self, step: str, context: Mapping[str, Any]) -> RepairStepResult:
        """Execute one registered repair step."""


class SafePrefixRepairExecutor:
    """Verifies and stages a repair artifact, then requires owner interfaces."""

    def __init__(self, policy: RepairPolicy) -> None:
        self._policy = policy
        self._staging = SafeFilesystem(policy.staging_root, create=True)

    @staticmethod
    def _sha256(path: Path, max_bytes: int) -> tuple[str, int]:
        if path.is_symlink() or not path.is_file():
            raise ForwardRepairError("repair artifact must be a regular non-symlink file")
        size = path.stat().st_size
        if size > max_bytes:
            raise ForwardRepairError("repair artifact exceeds configured size")
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
        return digest.hexdigest(), size

    def execute(self, step: str, context: Mapping[str, Any]) -> RepairStepResult:
        artifact = context["artifact"]
        prohibition = context["rollback_prohibition"]
        assert isinstance(artifact, Mapping)
        assert isinstance(prohibition, Mapping)
        if step == "preserve_evidence":
            refs = tuple(str(item) for item in context["evidence_refs"])
            return RepairStepResult("completed", "FORWARD_REPAIR_EVIDENCE_PRESERVED", evidence_refs=refs)
        if step == "verify_rollback_prohibition":
            refs = tuple(str(item) for item in prohibition["evidence_refs"])
            if not refs:
                return RepairStepResult("blocked", "ROLLBACK_PROHIBITION_EVIDENCE_MISSING")
            return RepairStepResult(
                "completed",
                "ROLLBACK_PROHIBITION_VERIFIED",
                evidence_refs=refs,
                outputs={"reason_code": prohibition["reason_code"]},
            )
        if step == "verify_repair_artifact":
            try:
                actual, size = self._sha256(Path(str(artifact["path"])), self._policy.max_artifact_bytes)
            except (ForwardRepairError, OSError) as exc:
                return RepairStepResult("blocked", "FORWARD_REPAIR_ARTIFACT_UNAVAILABLE", observations=(str(exc),))
            if actual != artifact["sha256"]:
                return RepairStepResult("blocked", "FORWARD_REPAIR_ARTIFACT_DIGEST_MISMATCH")
            return RepairStepResult(
                "completed",
                "FORWARD_REPAIR_ARTIFACT_VERIFIED",
                evidence_refs=(str(artifact["provenance_receipt_ref"]),),
                outputs={"sha256": actual, "size": size},
            )
        if step == "stage_repair":
            path = Path(str(artifact["path"]))
            destination = f"{context['recovery_id']}/{context['repair_id']}/{path.name}"
            try:
                staged = self._staging.copy_verified(
                    path,
                    destination,
                    expected_sha256=str(artifact["sha256"]),
                    max_bytes=self._policy.max_artifact_bytes,
                    overwrite=False,
                )
            except (FilesystemAdapterError, OSError) as exc:
                return RepairStepResult("failed", "FORWARD_REPAIR_STAGING_FAILED", observations=(str(exc),))
            return RepairStepResult(
                "completed",
                "FORWARD_REPAIR_STAGED",
                outputs={"staged_path": str(staged), "sha256": artifact["sha256"]},
            )
        if step == "owner_apply":
            return RepairStepResult("blocked", "FORWARD_REPAIR_OWNER_INTERFACE_REQUIRED")
        if step in {"verify_checkpoint", "verify_repaired_state", "commit_repaired_authority"}:
            return RepairStepResult("blocked", "FORWARD_REPAIR_VERIFICATION_INTERFACE_REQUIRED")
        return RepairStepResult("blocked", "FORWARD_REPAIR_COMPLETION_NOT_REACHED")


def run_forward_repair(
    plan: ForwardRepairPlan,
    *,
    policy: RepairPolicy,
    executor: ForwardRepairExecutor,
) -> dict[str, Any]:
    state_fs = SafeFilesystem(policy.state_root, create=True)
    runtime_fs = SafeFilesystem(policy.runtime_root, create=True)
    entry = state_fs.read_json(f"{plan.recovery_id}/entry.json", max_bytes=policy.max_plan_bytes)
    state = state_fs.read_json(f"{plan.recovery_id}/state.json", max_bytes=policy.max_plan_bytes)
    if entry.get("target_id") != plan.target_id or entry.get("actor_id") != plan.actor_id:
        raise ForwardRepairError("forward repair plan does not match the admitted recovery entry")
    if entry.get("authority_receipt_ref") != plan.authority_receipt_ref:
        raise ForwardRepairError("forward repair authority receipt mismatch")
    if entry.get("active_release_set_ref") != plan.current_release_set_ref:
        raise ForwardRepairError("current Release Set does not match admitted recovery state")
    if state.get("state") not in {"recovery_locked", "source_selection", "staging", "validation"}:
        raise ForwardRepairError(f"recovery state does not admit forward repair: {state.get('state')}")

    context = plan.context()
    sequence = int(state.get("sequence", 1))
    results: list[dict[str, Any]] = []
    with runtime_fs.exclusive_lock(policy.lock_name):
        state_fs.ensure_directory(f"{plan.recovery_id}/repairs")
        state_fs.ensure_directory(f"{plan.recovery_id}/checkpoints/{plan.repair_id}")
        state_fs.atomic_write_json(
            f"{plan.recovery_id}/repairs/{plan.repair_id}.json",
            {
                "schema_version": "1.0.0",
                **context,
                "created_at": plan.created_at.isoformat().replace("+00:00", "Z"),
                "steps": list(plan.steps),
            },
            overwrite=False,
        )
        for index, step in enumerate(plan.steps, start=1):
            result = executor.execute(step, context)
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            sequence += 1
            record: dict[str, Any] = {
                "schema_version": "1.0.0",
                "repair_id": plan.repair_id,
                "recovery_id": plan.recovery_id,
                "step": step,
                "step_index": index,
                "status": result.status,
                "reason_code": result.reason_code,
                "timestamp": timestamp,
                "evidence_refs": list(result.evidence_refs),
                "observations": list(result.observations),
            }
            if result.receipt_ref:
                record["receipt_ref"] = result.receipt_ref
            if result.outputs is not None:
                record["outputs"] = dict(result.outputs)
                context = {**context, "step_outputs": {**dict(context.get("step_outputs", {})), step: dict(result.outputs)}}
            state_fs.atomic_write_json(
                f"{plan.recovery_id}/checkpoints/{plan.repair_id}/{index:06d}-{step}.json",
                record,
                overwrite=False,
            )
            results.append(record)
            if result.status != "completed":
                terminal = "recovery_blocked" if result.status == "blocked" else "recovery_failed"
                state_fs.atomic_write_json(
                    f"{plan.recovery_id}/state.json",
                    {
                        "schema_version": "1.0.0",
                        "recovery_id": plan.recovery_id,
                        "repair_id": plan.repair_id,
                        "state": "recovery_failed",
                        "sequence": sequence,
                        "updated_at": timestamp,
                        "terminal_result": terminal,
                        "failed_step": step,
                        "reason_code": result.reason_code,
                        "authority_transition_permitted": False,
                        "next_valid_actions": ["inspect_evidence", "supersede_repair", "decommission"],
                    },
                )
                return {
                    "schema_version": "1.0.0",
                    "record_type": "forward_repair_result",
                    "repair_id": plan.repair_id,
                    "recovery_id": plan.recovery_id,
                    "result": terminal,
                    "failed_step": step,
                    "reason_code": result.reason_code,
                    "authority_changed": False,
                    "steps": results,
                }
            if step == "commit_repaired_authority" and policy.require_receipt_before_commit and not result.receipt_ref:
                raise ForwardRepairError("authority commit completed without a required durable receipt")
            next_actions = [plan.steps[index]] if index < len(plan.steps) else []
            state_fs.atomic_write_json(
                f"{plan.recovery_id}/state.json",
                {
                    "schema_version": "1.0.0",
                    "recovery_id": plan.recovery_id,
                    "repair_id": plan.repair_id,
                    "state": _STATE_BY_STEP[step],
                    "sequence": sequence,
                    "updated_at": timestamp,
                    "authority_transition_permitted": step == "commit_repaired_authority",
                    "next_valid_actions": next_actions,
                },
            )

        if policy.activate_authority_last and plan.steps[-2:] != ("commit_repaired_authority", "record_completion"):
            raise ForwardRepairError("forward repair authority commit must occur immediately before completion")
        commit_receipt = results[-2].get("receipt_ref")
        if policy.require_receipt_before_commit and not commit_receipt:
            raise ForwardRepairError("forward repair completion lacks a commit receipt")
        completion = {
            "schema_version": "1.0.0",
            "record_type": "forward_repair_result",
            "repair_id": plan.repair_id,
            "recovery_id": plan.recovery_id,
            "result": "service_restored",
            "previous_release_set_ref": plan.current_release_set_ref,
            "active_release_set_ref": plan.target_release_set_ref,
            "commit_receipt_ref": commit_receipt,
            "authority_changed": True,
            "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "steps": results,
        }
        state_fs.atomic_write_json(f"{plan.recovery_id}/forward-repair-result.json", completion, overwrite=False)
        return completion


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--execute-safe-prefix", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        policy = RepairPolicy.load(args.policy)
        payload = _load_json(args.plan, max_bytes=policy.max_plan_bytes)
        plan = ForwardRepairPlan.from_mapping(payload)
        if args.dry_run:
            result = {
                "schema_version": "1.0.0",
                "record_type": "forward_repair_plan_validation",
                "repair_id": plan.repair_id,
                "recovery_id": plan.recovery_id,
                "result": "admitted_for_staging",
                "steps": list(plan.steps),
                "authority_changed": False,
                "production_execution_requires": ["component_owner_repair_port", "authority_commit_port"],
            }
        else:
            result = run_forward_repair(plan, policy=policy, executor=SafePrefixRepairExecutor(policy))
    except (ForwardRepairError, FilesystemAdapterError, OSError) as exc:
        print(f"forward repair failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result.get("result") in {"admitted_for_staging", "service_restored"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
