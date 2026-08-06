"""Network-loss tests for deterministic local assembly and offline manifests."""

from __future__ import annotations

from pathlib import Path
import json
import socket
import sys

import pytest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "assembly" / "src"))

from koa_assembly.renderers import render_all  # noqa: E402

_SHA_A = "sha256:" + "1" * 64
_SHA_B = "sha256:" + "2" * 64


def _local_plan() -> dict:
    return {
        "plan_id": "network-loss-test",
        "profile_id": "sovereign-offline",
        "source_digests": {"docs/contracts/system.contract.json": _SHA_A},
        "services": [
            {
                "id": "local-navigation",
                "kind": "container",
                "image": "registry.invalid/koa/ariane@sha256:" + "2" * 64,
                "command": ["/usr/bin/ariane", "navigate", "--local"],
                "dependencies": [],
                "environment": {"KOA_OFFLINE": "true"},
                "ports": [],
                "mounts": [],
                "networks": [],
                "resources": {"cpu_millis": 100, "memory_bytes": 67108864, "pids": 32},
                "capabilities": [],
                "user": "koa-ariane",
                "criticality": "core",
            }
        ],
        "networks": [],
        "volumes": [],
        "packages": [{"name": "ariane", "version": "1.0.0", "digest": _SHA_B}],
        "files": [{"path": "/usr/bin/ariane", "digest": _SHA_B, "mode": "0755"}],
        "offline": {
            "enabled": True,
            "allow_network": False,
            "verification_policy": "verify-before-use",
            "artifacts": [
                {
                    "id": "ariane-local",
                    "path": "artifacts/ariane-local.pkg",
                    "digest": _SHA_B,
                    "artifact_class": "service_artifact",
                }
            ],
        },
        "backup": {},
    }


def _deny_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def denied(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("undeclared network access attempted")

    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
    monkeypatch.setattr(socket.socket, "connect_ex", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
        monkeypatch.delenv(name, raising=False)


def test_all_available_renderers_complete_with_network_access_denied(monkeypatch: pytest.MonkeyPatch) -> None:
    _deny_network(monkeypatch)
    outputs = render_all(_local_plan())
    assert set(outputs) == {"systemd", "quadlet", "compose", "kubernetes", "image", "offline_bundle"}
    assert all(files for files in outputs.values())


def test_network_loss_does_not_relabel_external_effects_as_completed(monkeypatch: pytest.MonkeyPatch) -> None:
    _deny_network(monkeypatch)
    manifest = json.loads(render_all(_local_plan())["offline_bundle"][0].text)
    assert manifest["network_access_allowed"] is False
    assert manifest["enabled"] is True
    serialized = json.dumps(manifest, sort_keys=True).lower()
    assert "published" not in serialized
    assert "synchronized" not in serialized
    assert manifest["verification"]["silent_substitution_allowed"] is False
