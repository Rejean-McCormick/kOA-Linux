from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def _load():
    path = ROOT / "host/boot/verify-release-set.py"
    spec = importlib.util.spec_from_file_location("verify_release_set_system_test", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _release_set() -> dict[str, object]:
    channels = {}
    namespaces = {"system": "koa.system", "services": "koa.services", "governance": "koa.governance", "knowledge": "koa.knowledge"}
    for channel_id, namespace in namespaces.items():
        channels[channel_id] = {
            "channel_id": channel_id,
            "release_namespace": namespace,
            "release_id": f"release:{channel_id}:1",
            "version": "1.0.0",
            "release_manifest_ref": f"manifest:{channel_id}:1",
            "artifact_refs": [f"artifact:{channel_id}:1"],
            "provenance_ref": f"provenance:{channel_id}:1",
            "validation_evidence_refs": [f"evidence:{channel_id}:1"],
            "recovery": {"mode": "rollback", "previous_compatible_release_ref": f"release:{channel_id}:0"},
        }
    return {
        "artifact_class": "release_set",
        "release_set_id": "release-set:1",
        "version": "1.0.0",
        "lifecycle_status": "validated",
        "language": "en",
        "issued_at": "2026-08-06T15:00:00Z",
        "issuer": {"id": "issuer:release"},
        "authority": {"id": "authority:release"},
        "channels": channels,
        "compatibility": {"status": "tested_compatible", "constraint_results": [{"constraint_id": "complete", "result": "pass"}], "test_evidence_refs": ["evidence:compatibility"]},
        "target_scope": {"profile_results": [{"profile_id": "sovereign_linux_node", "result": "pass", "evidence_refs": ["evidence:profile"]}]},
        "activation": {"eligibility": "eligible", "partial_activation_allowed": False, "activation_evidence_refs": ["evidence:activation"], "previous_good_release_set_ref": "release-set:0"},
        "signature": {"verification_status": "verified", "verification_evidence_refs": ["evidence:signature"], "signer_identity_ref": "identity:release-signer", "signing_authority_ref": "authority:signing"},
        "provenance": {"release_channels_registry_ref": "contracts/release-channels.contract.json", "artifact_classes_registry_ref": "contracts/artifact-classes.contract.json", "source_release_refs": ["release:system:1", "release:services:1", "release:governance:1", "release:knowledge:1"]},
    }


def test_complete_release_set_produces_terminal_verified_receipt(tmp_path: Path) -> None:
    module = _load()
    release_path = tmp_path / "release-set.json"
    _write(release_path, _release_set())
    digest = hashlib.sha256(release_path.read_bytes()).hexdigest()
    evidence_path = tmp_path / "signature.json"
    _write(evidence_path, {
        "verification_status": "verified",
        "subject": {"sha256": digest},
        "signer_identity_ref": "identity:release-signer",
        "signing_authority_ref": "authority:signing",
        "verification_evidence_refs": ["evidence:signature:1"],
    })
    output = tmp_path / "receipt.json"
    rc = module.main(["--release-set", str(release_path), "--signature-evidence", str(evidence_path), "--profile", "sovereign_linux_node", "--verified-at", "2026-08-06T16:00:00Z", "--output", str(output)])
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert rc == 0
    assert receipt["outcome"] == "verified"
    assert receipt["authorization_effect"] == "none"
    assert [layer["layer"] for layer in receipt["layers"]][-1] == "signature"


def test_incomplete_channel_set_fails_closed_with_terminal_receipt(tmp_path: Path) -> None:
    module = _load()
    release = _release_set()
    del release["channels"]["knowledge"]  # type: ignore[index]
    release_path = tmp_path / "release-set.json"
    _write(release_path, release)
    evidence_path = tmp_path / "signature.json"
    _write(evidence_path, {"verification_status": "verified", "subject": {"sha256": "0" * 64}, "signer_identity_ref": "identity:x", "signing_authority_ref": "authority:x", "verification_evidence_refs": ["evidence:x"]})
    output = tmp_path / "receipt.json"
    rc = module.main(["--release-set", str(release_path), "--signature-evidence", str(evidence_path), "--verified-at", "2026-08-06T16:00:00Z", "--output", str(output)])
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert rc == 2
    assert receipt["outcome"] == "failed"
    assert receipt["authorization_effect"] == "none"
    assert "channels_must_be_exact" in receipt["reason"]
