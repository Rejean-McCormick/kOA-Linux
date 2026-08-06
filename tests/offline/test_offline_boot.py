"""Plan-level offline boot conformance for the sovereign-offline profile."""

from __future__ import annotations

from pathlib import Path
import json
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import render  # noqa: E402

_SHA_SOURCE = "sha256:" + "3" * 64
_SHA_PACKAGE = "sha256:" + "4" * 64


def _profile() -> dict:
    return json.loads(
        (REPO / "docs/contracts/profiles/sovereign-offline.profile.json").read_text(encoding="utf-8")
    )


def _service(identifier: str) -> dict:
    service_id = identifier.replace("_", "-")
    return {
        "id": service_id,
        "kind": "native",
        "command": [f"/usr/libexec/koa/{service_id}", "serve"],
        "dependencies": [],
        "environment": {"KOA_PROFILE": "sovereign-offline"},
        "ports": [],
        "mounts": [],
        "networks": [],
        "resources": {"cpu_millis": 100, "memory_bytes": 67108864, "pids": 32},
        "capabilities": [],
        "user": service_id,
        "criticality": "critical",
    }


def _boot_plan() -> dict:
    required = _profile()["offline_operation"]["required_local_services"]
    services = [_service(item) for item in required]
    packages = [
        {"name": service["id"], "version": "1.0.0", "digest": _SHA_PACKAGE}
        for service in services
    ]
    files = [
        {"path": service["command"][0], "digest": _SHA_PACKAGE, "mode": "0755"}
        for service in services
    ]
    return {
        "plan_id": "sovereign-offline-boot",
        "profile_id": "sovereign-offline",
        "source_digests": {
            "docs/contracts/profiles/sovereign-offline.profile.json": _SHA_SOURCE
        },
        "services": services,
        "networks": [],
        "volumes": [],
        "packages": packages,
        "files": files,
        "offline": {
            "enabled": True,
            "allow_network": False,
            "verification_policy": "verify-before-use",
            "artifacts": [
                {
                    "id": "offline-core",
                    "path": "artifacts/offline-core.pkg",
                    "digest": _SHA_PACKAGE,
                    "artifact_class": "offline_bundle",
                }
            ],
        },
        "backup": {"owner_coordinated": True},
    }


def test_offline_boot_plan_contains_every_required_local_service() -> None:
    plan = _boot_plan()
    expected = {
        item.replace("_", "-")
        for item in _profile()["offline_operation"]["required_local_services"]
    }
    image = json.loads(render("image", plan)[0].text)
    assert {item["id"] for item in image["services"]} == expected
    assert image["activation"] == {
        "atomic": True,
        "partial_authoritative_state_allowed": False,
        "verification_required": True,
    }


def test_offline_boot_requires_verified_local_material_and_no_network() -> None:
    plan = _boot_plan()
    offline = json.loads(render("offline_bundle", plan)[0].text)
    assert offline["enabled"] is True
    assert offline["network_access_allowed"] is False
    assert offline["verification_policy"] == "verify-before-use"
    assert all(package["digest"] == _SHA_PACKAGE for package in offline["packages"])
    systemd = render("systemd", plan)
    service_paths = {item.path for item in systemd if item.path.endswith(".service")}
    expected_paths = {f"systemd/koa-{item.replace('_', '-')}.service" for item in _profile()["offline_operation"]["required_local_services"]}
    assert service_paths == expected_paths
    assert any(item.path == "systemd/manifest.json" for item in systemd)
    assert all("network-online.target" not in item.text.lower() for item in systemd)
