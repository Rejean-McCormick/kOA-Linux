"""Determinism tests for the offline-bundle renderer."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import render  # noqa: E402

_SHA_A = "sha256:" + "5" * 64
_SHA_B = "sha256:" + "6" * 64
_SHA_C = "sha256:" + "7" * 64


def _plan() -> dict:
    return {
        "plan_id": "bundle-determinism",
        "profile_id": "sovereign-offline",
        "source_digests": {
            "docs/contracts/system.contract.json": _SHA_A,
            "docs/contracts/profiles/sovereign-offline.profile.json": _SHA_B,
        },
        "services": [
            {
                "id": "release-verification",
                "kind": "native",
                "command": ["/usr/bin/koa-verify-release"],
                "dependencies": [],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {},
                "capabilities": [],
                "user": "koa-verifier",
                "criticality": "critical",
            }
        ],
        "networks": [],
        "volumes": [],
        "packages": [{"name": "koa-verifier", "version": "1.0.0", "digest": _SHA_C}],
        "files": [{"path": "/usr/bin/koa-verify-release", "digest": _SHA_C, "mode": "0755"}],
        "offline": {
            "enabled": True,
            "allow_network": False,
            "verification_policy": "verify-before-use",
            "artifacts": [
                {"id": "release-set", "path": "release/release-set.json", "digest": _SHA_A, "artifact_class": "release_set"},
                {"id": "system-image", "path": "images/system.img", "digest": _SHA_B, "artifact_class": "system_image"},
            ],
        },
        "backup": {},
    }


def test_identical_bundle_inputs_are_byte_identical() -> None:
    plan = _plan()
    assert render("offline_bundle", plan)[0].content == render("offline_bundle", deepcopy(plan))[0].content


def test_bundle_output_is_independent_of_mapping_and_artifact_order() -> None:
    first = _plan()
    second = deepcopy(first)
    second["source_digests"] = dict(reversed(list(second["source_digests"].items())))
    second["offline"]["artifacts"].reverse()
    assert render("offline_bundle", first)[0].content == render("offline_bundle", second)[0].content


def test_bundle_digest_changes_for_a_canonical_source_change_only() -> None:
    first = render("offline_bundle", _plan())[0]
    changed = _plan()
    changed["source_digests"]["docs/contracts/system.contract.json"] = "sha256:" + "8" * 64
    second = render("offline_bundle", changed)[0]
    assert first.digest != second.digest
    payload = json.loads(first.text)
    text = first.text.lower()
    assert payload["_koa_generated"]["manual_edits"] == "prohibited"
    assert "generated_at" not in text
    assert "timestamp" not in text
