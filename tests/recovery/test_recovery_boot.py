from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load():
    path = ROOT / "host/recovery/recovery-entry.py"
    spec = importlib.util.spec_from_file_location("recovery_entry_system_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _policy(module, tmp_path: Path):
    return module.RecoveryPolicy(
        policy_id="koa_host_recovery",
        profile_id="sovereign_linux_node",
        runtime_root=tmp_path / "runtime",
        state_root=tmp_path / "state",
        evidence_root=tmp_path / "evidence",
        receipts_root=tmp_path / "receipts",
        lock_name="host-recovery.lock",
        max_request_bytes=262144,
        max_session_seconds=3600,
        allowed_methods=frozenset({"rollback_release_set", "forward_repair", "restore_from_backup"}),
        initial_state="recovery_locked",
        allowed_decisions=frozenset({"allow", "approved", "admitted"}),
        allowed_receipt_types=frozenset({"rollback", "forward_repair", "component_transition"}),
        require_authorization_receipt=True,
    )


def _request(tmp_path: Path, receipt_path: Path) -> dict[str, object]:
    return {
        "recovery_id": "recovery:system:001",
        "target_id": "node:alpha",
        "incident_ref": "incident:001",
        "profile_id": "sovereign_linux_node",
        "active_release_set_ref": "release-set:failed",
        "last_verifiable_release_set_ref": "release-set:lkg",
        "method": "rollback_release_set",
        "actor_id": "identity:recovery-operator",
        "requested_at": "2026-08-06T16:00:00Z",
        "expires_at": "2026-08-06T16:30:00Z",
        "reason_codes": ["ACTIVATION_FAILED"],
        "authority_receipt_ref": "receipt:recovery:001",
        "authority_receipt_path": str(receipt_path),
        "authority_receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
    }


def test_recovery_boot_requires_authority_and_starts_locked(tmp_path: Path) -> None:
    module = _load()
    receipt_path = tmp_path / "authority.json"
    receipt_path.write_text(json.dumps({
        "schema_version": "2.0.0", "artifact_class": "decision_receipt",
        "receipt_id": "receipt:recovery:001", "receipt_type": "rollback", "decision": "approved",
        "request": {"subject": "identity:recovery-operator", "resource": "node:alpha"},
        "context": {"effective_profile": "sovereign_linux_node"},
        "validity": {"valid_from": "2026-08-06T15:55:00Z", "valid_until": "2026-08-06T17:00:00Z"},
    }, sort_keys=True), encoding="utf-8")
    policy = _policy(module, tmp_path)
    record = module.admit_recovery_entry(
        _request(tmp_path, receipt_path),
        policy=policy,
        now=datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc),
    )
    state = json.loads((policy.state_root / "recovery:system:001/state.json").read_text(encoding="utf-8"))
    assert record["state"] == "recovery_locked"
    assert record["authority_transition_permitted"] is False
    assert state["next_valid_actions"] == ["collect_evidence", "select_source", "cancel_recovery"]


def test_recovery_boot_rejects_digest_substitution(tmp_path: Path) -> None:
    module = _load()
    receipt_path = tmp_path / "authority.json"
    receipt_path.write_text('{"schema_version":"2.0.0"}', encoding="utf-8")
    request = _request(tmp_path, receipt_path)
    request["authority_receipt_sha256"] = "0" * 64
    with pytest.raises(module.RecoveryAdmissionError, match="digest mismatch"):
        module.admit_recovery_entry(
            request,
            policy=_policy(module, tmp_path),
            now=datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc),
            persist=False,
        )
