from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
STEPS = (
    "preserve_evidence", "verify_rollback_prohibition", "verify_repair_artifact",
    "stage_repair", "owner_apply", "verify_checkpoint", "verify_repaired_state",
    "commit_repaired_authority", "record_completion",
)


def _load():
    path = ROOT / "host/recovery/forward-repair.py"
    spec = importlib.util.spec_from_file_location("forward_repair_system_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _seed(tmp_path: Path, recovery_id: str) -> None:
    base = tmp_path / "state" / recovery_id
    base.mkdir(parents=True)
    (base / "entry.json").write_text(json.dumps({
        "target_id": "node:alpha", "actor_id": "identity:repair-operator",
        "authority_receipt_ref": "receipt:repair:001", "active_release_set_ref": "release-set:failed",
    }), encoding="utf-8")
    (base / "state.json").write_text(json.dumps({"state": "recovery_locked", "sequence": 1}), encoding="utf-8")


def _plan(module, tmp_path: Path):
    artifact = tmp_path / "repair.bin"
    artifact.write_bytes(b"forward repair artifact")
    return module.ForwardRepairPlan.from_mapping({
        "schema_version": "1.0.0", "repair_id": "repair:001", "recovery_id": "recovery:001",
        "target_id": "node:alpha", "actor_id": "identity:repair-operator",
        "created_at": "2026-08-06T16:00:00Z", "current_release_set_ref": "release-set:failed",
        "target_release_set_ref": "release-set:repaired", "authority_receipt_ref": "receipt:repair:001",
        "evidence_refs": ["evidence:incident:001"],
        "rollback_prohibition": {"reason_code": "ROLLBACK_INCOMPATIBLE", "incompatible_state_ref": "state:schema:newer", "evidence_refs": ["evidence:rollback-prohibited"]},
        "artifact": {"artifact_ref": "artifact:repair:001", "owner_ref": "component:owner", "path": str(artifact), "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "provenance_receipt_ref": "receipt:provenance:001"},
        "steps": list(STEPS),
    })


def _policy(module, tmp_path: Path):
    return module.RepairPolicy("koa_host_recovery", tmp_path / "state", tmp_path / "staging", tmp_path / "runtime", "repair.lock", 524288, 1048576, True, True)


class BlockingExecutor:
    def __init__(self, module) -> None:
        self.module = module

    def execute(self, step, context):
        if step == "owner_apply":
            return self.module.RepairStepResult("blocked", "FORWARD_REPAIR_OWNER_INTERFACE_REQUIRED")
        return self.module.RepairStepResult("completed", f"TEST_{step.upper()}", evidence_refs=("evidence:test",))


class CompletingExecutor:
    def __init__(self, module) -> None:
        self.module = module

    def execute(self, step, context):
        receipt = "receipt:repair-commit:001" if step == "commit_repaired_authority" else None
        return self.module.RepairStepResult("completed", f"TEST_{step.upper()}", evidence_refs=("evidence:test",), receipt_ref=receipt)


def test_forward_repair_blocks_before_owner_authority_is_available(tmp_path: Path) -> None:
    module = _load()
    _seed(tmp_path, "recovery:001")
    result = module.run_forward_repair(_plan(module, tmp_path), policy=_policy(module, tmp_path), executor=BlockingExecutor(module))
    assert result["result"] == "recovery_blocked"
    assert result["failed_step"] == "owner_apply"
    assert result["authority_changed"] is False


def test_forward_repair_commits_authority_only_with_terminal_receipt(tmp_path: Path) -> None:
    module = _load()
    _seed(tmp_path, "recovery:001")
    result = module.run_forward_repair(_plan(module, tmp_path), policy=_policy(module, tmp_path), executor=CompletingExecutor(module))
    assert result["result"] == "service_restored"
    assert result["authority_changed"] is True
    assert result["commit_receipt_ref"] == "receipt:repair-commit:001"
    assert [item["step"] for item in result["steps"]][-2:] == ["commit_repaired_authority", "record_completion"]
