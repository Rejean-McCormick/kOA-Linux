"""Determinism and provenance tests for image manifests."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import render  # noqa: E402

_SHA_A = "sha256:" + "9" * 64
_SHA_B = "sha256:" + "a" * 64
_SHA_C = "sha256:" + "b" * 64


def _plan() -> dict:
    return {
        "plan_id": "image-manifest-determinism",
        "profile_id": "sovereign-linux-node",
        "source_digests": {
            "docs/contracts/system.contract.json": _SHA_A,
            "docs/contracts/profiles/sovereign-linux-node.profile.json": _SHA_B,
        },
        "services": [
            {
                "id": "audit-broker",
                "kind": "native",
                "command": ["/usr/bin/koa-audit-broker"],
                "dependencies": [],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {},
                "capabilities": [],
                "user": "koa-audit",
                "criticality": "critical",
            },
            {
                "id": "resource-governor",
                "kind": "native",
                "command": ["/usr/bin/koa-resource-governor"],
                "dependencies": ["audit-broker"],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {},
                "capabilities": [],
                "user": "koa-resource",
                "criticality": "critical",
            },
        ],
        "networks": [],
        "volumes": [],
        "packages": [
            {"name": "koa-audit-broker", "version": "1.0.0", "digest": _SHA_C},
            {"name": "koa-resource-governor", "version": "1.0.0", "digest": _SHA_B},
        ],
        "files": [
            {"path": "/usr/bin/koa-audit-broker", "digest": _SHA_C, "mode": "0755"},
            {"path": "/usr/bin/koa-resource-governor", "digest": _SHA_B, "mode": "0755"},
        ],
        "offline": {"enabled": True, "allow_network": False, "artifacts": []},
        "backup": {},
    }


def test_image_manifest_is_byte_stable() -> None:
    plan = _plan()
    assert render("image", plan)[0].content == render("image", deepcopy(plan))[0].content


def test_image_manifest_is_order_independent_and_atomic() -> None:
    first = _plan()
    second = deepcopy(first)
    second["services"].reverse()
    second["packages"].reverse()
    second["files"].reverse()
    assert render("image", first)[0].content == render("image", second)[0].content
    manifest = json.loads(render("image", first)[0].text)
    assert manifest["activation"]["atomic"] is True
    assert manifest["activation"]["verification_required"] is True
    assert manifest["activation"]["partial_authoritative_state_allowed"] is False


def test_image_manifest_records_generator_sources_and_no_host_time() -> None:
    manifest_file = render("image", _plan())[0]
    metadata = json.loads(manifest_file.text)["_koa_generated"]
    assert metadata["generator"].startswith("koa-assembly/image@")
    assert set(metadata["source_digests"]) == {
        "docs/contracts/system.contract.json",
        "docs/contracts/profiles/sovereign-linux-node.profile.json",
    }
    lower = manifest_file.text.lower()
    assert "timestamp" not in lower
    assert "generated_at" not in lower
    assert str(REPO).lower() not in lower
