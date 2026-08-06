from __future__ import annotations

import importlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
PROMOTION = ROOT / "release/promotion"
if str(PROMOTION) not in sys.path:
    sys.path.insert(0, str(PROMOTION))

promote = importlib.import_module("promote")


def _write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _release_set(release_set_id: str = "release-set:1") -> dict[str, object]:
    channels = {}
    namespaces = {"system": "koa.system", "services": "koa.services", "governance": "koa.governance", "knowledge": "koa.knowledge"}
    for channel_id, namespace in namespaces.items():
        channels[channel_id] = {
            "channel_id": channel_id, "release_namespace": namespace,
            "release_id": f"release:{channel_id}:1", "version": "1.0.0",
            "release_manifest_ref": f"manifest:{channel_id}:1",
            "artifact_refs": [f"artifact:{channel_id}:1"],
            "provenance_ref": f"provenance:{channel_id}:1",
            "validation_evidence_refs": [f"evidence:{channel_id}:1"],
            "recovery": {"mode": "rollback", "previous_compatible_release_ref": "release-set:0"},
        }
    return {
        "artifact_class": "release_set", "release_set_id": release_set_id, "version": "1.0.0",
        "lifecycle_status": "validated", "channels": channels,
        "compatibility": {"status": "tested_compatible"},
        "activation": {"eligibility": "eligible", "partial_activation_allowed": False, "previous_good_release_set_ref": "release-set:0"},
        "signature": {"verification_status": "verified"},
        "provenance": {"source": "test"},
    }


def test_release_activation_is_atomic_and_receipted(tmp_path: Path) -> None:
    release_path = tmp_path / "release.json"
    _write(release_path, _release_set())
    digest = promote.file_digest(release_path)
    verification = tmp_path / "verification.json"
    _write(verification, {
        "verification_class": "release_set_signature_verification",
        "verification_status": "verified",
        "signer_trust_status": "trusted",
        "release_set_id": "release-set:1",
        "subject_digest": digest,
        "verification_evidence_refs": ["evidence:signature"],
        "verified_at": "2026-08-06T15:30:00Z",
    })
    decision = tmp_path / "decision.json"
    _write(decision, {"artifact_class": "decision_receipt", "receipt_type": "release_compatibility", "decision": "approved", "context": {"release_set_ref": "release-set:1"}})
    state = tmp_path / "state.json"
    receipt = tmp_path / "activation-receipt.json"
    args = promote.parser().parse_args([
        "--policy", str(ROOT / "release/promotion/channels.toml"),
        "--release-set", str(release_path),
        "--verification-receipt", str(verification),
        "--decision-receipt", str(decision),
        "--state-file", str(state),
        "--expected-state-digest", "absent",
        "--expected-current-release-set", "none",
        "--receipt-output", str(receipt),
        "--timestamp", "2026-08-06T16:00:00Z",
        "--actor", "identity:release-operator",
        "--correlation-id", "correlation:activation:001",
    ])
    assert promote.execute(args) == 0
    active = json.loads(state.read_text(encoding="utf-8"))
    proof = json.loads(receipt.read_text(encoding="utf-8"))
    assert active["active_release_set"]["release_set_id"] == "release-set:1"
    assert active["previous_active_release_set"] is None
    assert proof["receipt_type"] == "artifact_activation"
    assert proof["decision"] == "approved"
    assert proof["receipt_type"] == "artifact_activation"


def test_invalid_verification_leaves_active_state_unchanged(tmp_path: Path) -> None:
    release_path = tmp_path / "release.json"
    _write(release_path, _release_set())
    verification = tmp_path / "verification.json"
    _write(verification, {"verification_class": "release_set_signature_verification", "verification_status": "failed", "signer_trust_status": "trusted", "release_set_id": "release-set:1", "subject_digest": promote.file_digest(release_path), "verification_evidence_refs": ["evidence:x"], "verified_at": "2026-08-06T15:30:00Z"})
    decision = tmp_path / "decision.json"
    _write(decision, {"artifact_class": "decision_receipt", "receipt_type": "release_compatibility", "decision": "approved", "context": {"release_set_ref": "release-set:1"}})
    state = tmp_path / "state.json"
    state.write_text('{"schema_version":1,"revision":7,"active_release_set":{"release_set_id":"release-set:0"}}\n', encoding="utf-8")
    before = state.read_bytes()
    args = promote.parser().parse_args([
        "--policy", str(ROOT / "release/promotion/channels.toml"), "--release-set", str(release_path),
        "--verification-receipt", str(verification), "--decision-receipt", str(decision),
        "--state-file", str(state), "--expected-state-digest", promote.file_digest(state),
        "--expected-current-release-set", "release-set:0", "--receipt-output", str(tmp_path / "receipt.json"),
        "--timestamp", "2026-08-06T16:00:00Z", "--actor", "identity:operator", "--correlation-id", "correlation:activation:002",
    ])
    assert promote.execute(args) == 2
    assert state.read_bytes() == before
    assert not (tmp_path / "receipt.json").exists()
