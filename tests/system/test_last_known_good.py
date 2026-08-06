from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def _load(relative: str, name: str):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _verification() -> dict[str, object]:
    return {
        "schema_version": 1,
        "receipt_type": "system_image_verification",
        "outcome": "verified",
        "profile_id": "sovereign_linux_node",
        "image": {"image_id": "image:b", "sha256": "b" * 64},
        "release_set": {"release_set_id": "release-set:b"},
    }


def _state(verification_digest: str) -> dict[str, object]:
    return {
        "schema_version": 1,
        "generation": 1,
        "active_slot": "a",
        "candidate_slot": "b",
        "previous_good_slot": "c",
        "recovery_slot": "recovery",
        "pending_boot": None,
        "slots": {
            "a": {"state": "active", "accepted": True, "image_id": "image:a", "sha256": "a" * 64, "release_set_id": "release-set:a", "verification_receipt_sha256": "1" * 64},
            "b": {"state": "candidate", "accepted": False, "image_id": "image:b", "sha256": "b" * 64, "release_set_id": "release-set:b", "verification_receipt_sha256": verification_digest, "boot_attempts": 0},
            "c": {"state": "previous_good", "accepted": True, "rollback_safe": True, "image_id": "image:c", "sha256": "c" * 64, "release_set_id": "release-set:c", "verification_receipt_sha256": "2" * 64, "rollback_boot_attempts": 0},
            "recovery": {"state": "recovery", "accepted": True, "image_id": "image:recovery", "sha256": "d" * 64, "release_set_id": "release-set:recovery"},
        },
    }


def _health(slot: str, image_id: str, digest: str, release_set_id: str, failed_check: str | None = None) -> dict[str, object]:
    checks = []
    for check_id in ("boot", "storage", "identity", "services", "governance", "data_mounts", "recovery"):
        checks.append({"check_id": check_id, "outcome": "failed" if check_id == failed_check else "pass"})
    return {
        "receipt_type": "profile_health_verdict",
        "outcome": "pass",
        "profile_id": "sovereign_linux_node",
        "slot": slot,
        "image": {"image_id": image_id, "sha256": digest},
        "release_set": {"release_set_id": release_set_id},
        "checks": checks,
    }


def test_candidate_acceptance_rotates_active_into_distinct_last_known_good(tmp_path: Path) -> None:
    select = _load("host/boot/select-release-slot.py", "select_release_slot_lkg_test")
    accept = _load("host/boot/mark-boot-success.py", "mark_boot_success_lkg_test")
    verification_path = tmp_path / "image-verification.json"
    _write(verification_path, _verification())
    verification_digest = hashlib.sha256(verification_path.read_bytes()).hexdigest()
    state_path = tmp_path / "slot-state.json"
    _write(state_path, _state(verification_digest))

    selection = select.select(argparse.Namespace(
        policy=ROOT / "host/boot/boot-policy.toml",
        state=state_path,
        slot="b",
        image_verification=verification_path,
        actor="identity:operator",
        correlation_id="correlation:boot:001",
        selected_at="2026-08-06T16:00:00Z",
        receipt=tmp_path / "selection.json",
    ))
    assert selection["acceptance_effect"] == "none"

    health_path = tmp_path / "health.json"
    _write(health_path, _health("b", "image:b", "b" * 64, "release-set:b"))
    receipt = accept.accept(argparse.Namespace(
        policy=ROOT / "host/boot/boot-policy.toml",
        state=state_path,
        slot="b",
        health_verdict=health_path,
        actor="identity:operator",
        correlation_id="correlation:boot:001",
        accepted_at="2026-08-06T16:01:00Z",
        receipt=tmp_path / "acceptance.json",
    ))
    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert receipt["active_slot"] == "b"
    assert receipt["previous_good_slot"] == "a"
    assert state["slots"]["a"]["state"] == "previous_good"
    assert state["slots"]["c"]["state"] == "retired"
    assert len({state["active_slot"], state["previous_good_slot"], state["recovery_slot"]}) == 3
