"""Conformance tests for cached and bundled artifacts used offline."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import json
import sys

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import RenderError, render  # noqa: E402

_SHA_A = "sha256:" + "a" * 64
_SHA_B = "sha256:" + "b" * 64
_SHA_C = "sha256:" + "c" * 64
_SHA_D = "sha256:" + "d" * 64


def _plan() -> dict:
    return {
        "plan_id": "sovereign-offline-cache-test",
        "profile_id": "sovereign-offline",
        "source_digests": {
            "docs/contracts/system.contract.json": _SHA_A,
            "docs/contracts/profiles/sovereign-offline.profile.json": _SHA_B,
        },
        "services": [
            {
                "id": "identity-verification",
                "kind": "native",
                "command": ["/usr/bin/koa-identity", "serve"],
                "dependencies": [],
                "environment": {},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {"cpu_millis": 100, "memory_bytes": 67108864, "pids": 32},
                "capabilities": [],
                "user": "koa-identity",
                "criticality": "critical",
            }
        ],
        "networks": [],
        "volumes": [],
        "packages": [
            {"name": "koa-identity", "version": "1.0.0", "digest": _SHA_C}
        ],
        "files": [
            {"path": "/usr/bin/koa-identity", "digest": _SHA_C, "mode": "0755"}
        ],
        "offline": {
            "enabled": True,
            "allow_network": False,
            "verification_policy": "verify-before-use",
            "artifacts": [
                {
                    "id": "identity-package",
                    "path": "artifacts/koa-identity.pkg",
                    "digest": _SHA_C,
                    "artifact_class": "service_artifact",
                },
                {
                    "id": "trust-bundle",
                    "path": "trust/offline-trust-bundle.json",
                    "digest": _SHA_D,
                    "artifact_class": "trust_bundle",
                },
            ],
        },
        "backup": {"owner_coordinated": True},
    }


def _manifest(plan: dict) -> dict:
    outputs = render("offline_bundle", plan)
    assert len(outputs) == 1
    return json.loads(outputs[0].text)


def test_cached_artifacts_are_explicit_digest_bound_and_non_authoritative() -> None:
    manifest = _manifest(_plan())
    artifacts = manifest["artifacts"]
    assert [item["id"] for item in artifacts] == ["identity-package", "trust-bundle"]
    assert all(item["digest"].startswith("sha256:") for item in artifacts)
    assert manifest["network_access_allowed"] is False
    assert manifest["verification"] == {
        "silent_substitution_allowed": False,
        "transport_grants_authority": False,
        "verify_digests_before_import": True,
        "verify_signatures_when_required_by_artifact_class": True,
    }
    assert manifest["_koa_generated"]["authority"] == "derived_projection"


def test_cache_inventory_is_order_independent_and_contains_no_payload_bytes() -> None:
    first = _plan()
    second = deepcopy(first)
    second["offline"]["artifacts"].reverse()
    second["source_digests"] = dict(reversed(list(second["source_digests"].items())))
    assert render("offline_bundle", first)[0].content == render("offline_bundle", second)[0].content
    text = render("offline_bundle", first)[0].text
    assert "payload_bytes" not in text
    assert "base64" not in text.lower()
    assert "/tmp/" not in text


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("digest", "sha256:not-a-digest", "sha256"),
        ("path", "../escape.pkg", "unsafe path"),
        ("path", "/absolute.pkg", "unsafe path"),
    ],
)
def test_cached_artifact_references_fail_closed(field: str, value: str, message: str) -> None:
    plan = _plan()
    plan["offline"]["artifacts"][0][field] = value
    with pytest.raises(RenderError, match=message):
        render("offline_bundle", plan)
