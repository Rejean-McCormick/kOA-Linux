from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
STEPS = ("preserve_evidence", "verify_source", "stage_source", "verify_candidate", "request_activation", "verify_activation", "record_completion")


def _load():
    path = ROOT / "host/recovery/restore-controller.py"
    spec = importlib.util.spec_from_file_location("restore_controller_lkg_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _policy(module, tmp_path: Path):
    return module.ControllerPolicy("koa_host_recovery", tmp_path / "state", tmp_path / "staging", tmp_path / "runtime", "restore.lock", 524288, 1048576, True, True, True, True, True, "B-0081")


def _mapping(tmp_path: Path, *, last_known_good: bool = True):
    source = tmp_path / "lkg.bundle"
    source.write_bytes(b"retained last known good")
    return {
        "schema_version": "1.0.0", "plan_id": "restore-plan:lkg:001", "recovery_id": "recovery:lkg:001",
        "method": "rollback_release_set", "target_id": "node:alpha", "actor_id": "identity:recovery-operator",
        "created_at": "2026-08-06T16:00:00Z", "expected_active_release_set_ref": "release-set:failed",
        "target_release_set_ref": "release-set:lkg", "authority_receipt_ref": "receipt:rollback:001",
        "evidence_refs": ["evidence:failed-activation"],
        "source": {"artifact_ref": "artifact:lkg", "owner_ref": "release:owner", "source_release_set_ref": "release-set:lkg", "path": str(source), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "verification_receipt_ref": "receipt:lkg-verification", "last_known_good": last_known_good},
        "steps": list(STEPS),
    }


class Executor:
    def __init__(self, module) -> None:
        self.module = module

    def execute(self, step, context):
        receipt = "receipt:activation-verified:001" if step == "verify_activation" else ("receipt:activation-request:001" if step == "request_activation" else None)
        return self.module.StepResult("completed", f"TEST_{step.upper()}", evidence_refs=("evidence:test",), receipt_ref=receipt)


def _seed(tmp_path: Path) -> None:
    base = tmp_path / "state/recovery:lkg:001"
    base.mkdir(parents=True)
    (base / "entry.json").write_text(json.dumps({"target_id": "node:alpha", "actor_id": "identity:recovery-operator", "authority_receipt_ref": "receipt:rollback:001", "active_release_set_ref": "release-set:failed"}), encoding="utf-8")
    (base / "state.json").write_text(json.dumps({"state": "recovery_locked", "sequence": 1}), encoding="utf-8")


def test_rollback_plan_requires_explicit_last_known_good_identity(tmp_path: Path) -> None:
    module = _load()
    with pytest.raises(module.RestoreControllerError, match="last-known-good"):
        module.RestorePlan.from_mapping(_mapping(tmp_path, last_known_good=False), policy=_policy(module, tmp_path))


def test_restore_last_known_good_keeps_previous_and_target_distinct(tmp_path: Path) -> None:
    module = _load()
    policy = _policy(module, tmp_path)
    plan = module.RestorePlan.from_mapping(_mapping(tmp_path), policy=policy)
    _seed(tmp_path)
    result = module.run_restore_plan(plan, policy=policy, executor=Executor(module), now=datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc))
    assert result["result"] == "service_restored"
    assert result["previous_release_set_ref"] == "release-set:failed"
    assert result["active_release_set_ref"] == "release-set:lkg"
    assert result["activation_receipt_ref"] == "receipt:activation-verified:001"
    assert result["authority_changed"] is True
