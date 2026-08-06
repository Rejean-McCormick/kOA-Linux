from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path

import pytest

from koa_assembly.renderers import (
    RenderError,
    RenderedFile,
    normalize_plan,
    render,
    render_all,
    write_rendered_files,
)

SHA_A = "sha256:" + "a" * 64
SHA_B = "sha256:" + "b" * 64
SHA_C = "sha256:" + "c" * 64
SHA_D = "sha256:" + "d" * 64
SHA_E = "sha256:" + "e" * 64
SHA_F = "sha256:" + "f" * 64


def sample_plan() -> dict:
    return {
        "plan_id": "sovereign-node-release",
        "profile_id": "sovereign-linux-node",
        "source_digests": {
            "docs/contracts/profiles/sovereign-linux-node.profile.json": SHA_A,
            "docs/contracts/system.contract.json": SHA_B,
            "assembly/plans/service-plan.json": SHA_C,
        },
        "services": [
            {
                "id": "identity-and-trust",
                "kind": "container",
                "image": "registry.invalid/koa/identity-and-trust@" + SHA_D,
                "command": ["/usr/bin/koa-identity-and-trust", "serve"],
                "environment": {
                    "KOA_MODE": "sovereign",
                    "DATABASE_TOKEN": {"secret_ref": "secret://identity-database/token"},
                },
                "ports": [
                    {
                        "name": "api",
                        "target": 8080,
                        "published": 18080,
                        "host_ip": "127.0.0.1",
                        "protocol": "tcp",
                    }
                ],
                "mounts": [
                    {"volume": "identity-data", "target": "/var/lib/koa/identity", "read_only": False}
                ],
                "networks": ["koa-private"],
                "resources": {"cpu_millis": 500, "memory_bytes": 268435456, "pids": 128},
                "capabilities": [],
                "user": "10001",
                "criticality": "critical",
                "healthcheck": {
                    "command": ["/usr/bin/koa-identity-and-trust", "health"],
                    "interval_seconds": 20,
                    "timeout_seconds": 4,
                    "retries": 3,
                },
            },
            {
                "id": "publication-gateway",
                "kind": "container",
                "image": "registry.invalid/koa/publication-gateway@" + SHA_E,
                "command": ["/usr/bin/koa-publication-gateway", "serve"],
                "dependencies": ["identity-and-trust"],
                "environment": {"KOA_MODE": "sovereign"},
                "ports": [{"name": "api", "target": 8090, "protocol": "tcp"}],
                "mounts": [
                    {"volume": "publication-data", "target": "/var/lib/koa/publication", "read_only": False}
                ],
                "networks": ["koa-private"],
                "resources": {"cpu_millis": 250, "memory_bytes": 134217728, "pids": 64},
                "capabilities": [],
                "user": "10002",
                "criticality": "core",
                "healthcheck": {
                    "command": ["/usr/bin/koa-publication-gateway", "health"],
                    "interval_seconds": 30,
                    "timeout_seconds": 5,
                    "retries": 3,
                },
            },
        ],
        "networks": [{"id": "koa-private", "internal": True, "driver": "bridge"}],
        "volumes": [
            {
                "id": "identity-data",
                "owner": "identity-and-trust",
                "persistent": True,
                "size_bytes": 1073741824,
                "mount_path": "/var/lib/koa/identity",
            },
            {
                "id": "publication-data",
                "owner": "publication-gateway",
                "persistent": True,
                "size_bytes": 536870912,
                "mount_path": "/var/lib/koa/publication",
            },
        ],
        "packages": [
            {"name": "koa-identity-and-trust", "version": "1.0.0", "digest": SHA_D},
            {"name": "koa-publication-gateway", "version": "1.0.0", "digest": SHA_E},
        ],
        "files": [
            {"path": "/usr/lib/systemd/system/koa-node.target", "digest": SHA_F, "mode": "0644"}
        ],
        "offline": {
            "enabled": True,
            "allow_network": False,
            "verification_policy": "verify-before-use",
            "artifacts": [
                {
                    "id": "service-bundle",
                    "path": "artifacts/service-bundle.tar.zst",
                    "digest": SHA_D,
                    "artifact_class": "deployable_package",
                }
            ],
        },
        "backup": {"owner_coordinated": True, "consistency": "application-consistent"},
    }


def as_bytes(outputs: tuple[RenderedFile, ...]) -> list[tuple[str, bytes, str, int]]:
    return [(item.path, item.content, item.media_type, item.mode) for item in outputs]


def metadata_for(renderer_name: str, outputs: tuple[RenderedFile, ...]) -> dict:
    manifest_name = f"{renderer_name}/manifest.json"
    for item in outputs:
        if item.path == manifest_name:
            return json.loads(item.text)["_koa_generated"]
    primary = outputs[0]
    return json.loads(primary.text)["_koa_generated"]


def test_every_renderer_is_byte_for_byte_deterministic() -> None:
    plan = sample_plan()
    for name in ("systemd", "quadlet", "compose", "kubernetes", "image", "offline_bundle"):
        assert as_bytes(render(name, plan)) == as_bytes(render(name, deepcopy(plan)))


def test_input_order_does_not_change_outputs() -> None:
    original = sample_plan()
    shuffled = deepcopy(original)
    shuffled["services"].reverse()
    shuffled["networks"].reverse()
    shuffled["volumes"].reverse()
    shuffled["packages"].reverse()
    shuffled["files"].reverse()
    shuffled["offline"]["artifacts"].reverse()
    shuffled["source_digests"] = dict(reversed(list(shuffled["source_digests"].items())))
    assert {name: as_bytes(files) for name, files in render_all(original).items()} == {
        name: as_bytes(files) for name, files in render_all(shuffled).items()
    }


def test_all_renderers_share_one_semantic_digest() -> None:
    outputs = render_all(sample_plan())
    metadata = {name: metadata_for(name, files) for name, files in outputs.items()}
    assert len({item["semantic_digest"] for item in metadata.values()}) == 1
    assert len({item["plan_digest"] for item in metadata.values()}) == 1
    assert all(item["authority"] == "derived_projection" for item in metadata.values())
    assert all(item["manual_edits"] == "prohibited" for item in metadata.values())


def test_formats_parse_and_preserve_the_same_service_inventory() -> None:
    outputs = render_all(sample_plan())
    expected = {"identity-and-trust", "publication-gateway"}

    systemd_paths = {item.path for item in outputs["systemd"]}
    assert {f"systemd/koa-{name}.service" for name in expected} <= systemd_paths
    for item in outputs["systemd"]:
        if item.path.endswith(".service"):
            assert "[Unit]" in item.text and "[Service]" in item.text and "[Install]" in item.text
            assert "/bin/sh" not in item.text

    quadlet_paths = {item.path for item in outputs["quadlet"]}
    assert {f"quadlet/koa-{name}.container" for name in expected} <= quadlet_paths

    compose = json.loads(next(item.text for item in outputs["compose"] if item.path.endswith("compose.yaml")))
    assert set(compose["services"]) == expected

    kubernetes = json.loads(next(item.text for item in outputs["kubernetes"] if item.path.endswith("manifests.yaml")))
    deployments = {
        item["metadata"]["labels"]["koa.io/component"]
        for item in kubernetes["items"]
        if item["kind"] == "Deployment"
    }
    assert deployments == expected

    image = json.loads(outputs["image"][0].text)
    assert {item["id"] for item in image["services"]} == expected

    offline = json.loads(outputs["offline_bundle"][0].text)
    assert {item["id"] for item in offline["artifacts"]} == {"service-bundle"}


def test_every_generated_file_identifies_generator_and_sources() -> None:
    source_digest = SHA_A
    for renderer_name, files in render_all(sample_plan()).items():
        for item in files:
            assert "koa-assembly/" in item.text, (renderer_name, item.path)
            assert source_digest in item.text, (renderer_name, item.path)
            assert "derived" in item.text.lower(), (renderer_name, item.path)


def test_compose_and_kubernetes_do_not_embed_secret_values() -> None:
    outputs = render_all(sample_plan())
    compose = next(item.text for item in outputs["compose"] if item.path.endswith("compose.yaml"))
    kubernetes = next(item.text for item in outputs["kubernetes"] if item.path.endswith("manifests.yaml"))
    assert "identity-database" in compose
    assert "identity-database" in kubernetes
    assert '"DATABASE_TOKEN":' not in compose
    assert '"value": "token"' not in kubernetes


def test_source_digest_change_changes_every_renderer_output() -> None:
    first = sample_plan()
    second = deepcopy(first)
    second["source_digests"]["docs/contracts/system.contract.json"] = SHA_F
    for name in render_all(first):
        assert as_bytes(render(name, first)) != as_bytes(render(name, second))


def test_write_rendered_files_is_confined_and_repeatable(tmp_path: Path) -> None:
    outputs = render("compose", sample_plan())
    first = write_rendered_files(tmp_path, outputs)
    second = write_rendered_files(tmp_path, outputs)
    assert first == second
    assert {path.relative_to(tmp_path).as_posix() for path in first} == {item.path for item in outputs}
    for path, item in zip(first, outputs, strict=True):
        assert path.read_bytes() == item.content
    with pytest.raises(RenderError):
        RenderedFile("../escape", b"no", "text/plain")


def test_rejects_unpinned_container_images() -> None:
    plan = sample_plan()
    plan["services"][0]["image"] = "registry.invalid/koa/identity-and-trust:latest"
    with pytest.raises(RenderError, match="immutable image digest"):
        normalize_plan(plan)


def test_rejects_shell_string_commands() -> None:
    plan = sample_plan()
    plan["services"][0]["command"] = "/bin/sh -c arbitrary"
    with pytest.raises(RenderError, match="argument vector"):
        normalize_plan(plan)


def test_rejects_plaintext_secret_environment_values() -> None:
    plan = sample_plan()
    plan["services"][0]["environment"]["DATABASE_TOKEN"] = "plaintext"
    with pytest.raises(RenderError, match="secret reference"):
        normalize_plan(plan)


def test_rejects_dependency_cycles() -> None:
    plan = sample_plan()
    plan["services"][0]["dependencies"] = ["publication-gateway"]
    with pytest.raises(RenderError, match="cycle"):
        normalize_plan(plan)


def test_rejects_unknown_storage_and_network_references() -> None:
    plan = sample_plan()
    plan["services"][0]["mounts"][0]["volume"] = "missing-volume"
    with pytest.raises(RenderError, match="unknown volumes"):
        normalize_plan(plan)
    plan = sample_plan()
    plan["services"][0]["networks"] = ["missing-network"]
    with pytest.raises(RenderError, match="unknown networks"):
        normalize_plan(plan)


def test_target_specific_renderers_fail_closed_for_native_services() -> None:
    plan = sample_plan()
    service = plan["services"][0]
    service["kind"] = "native"
    service["image"] = None
    for name in ("quadlet", "compose", "kubernetes"):
        with pytest.raises(RenderError, match="cannot represent native service"):
            render(name, plan)
    assert render("systemd", plan)
    assert render("image", plan)
    assert render("offline_bundle", plan)


@dataclass(frozen=True)
class PublicPlan:
    plan_id: str
    profile_id: str
    source_digests: dict
    services: list
    networks: list
    volumes: list
    packages: list
    files: list
    offline: dict
    backup: dict


def test_public_dataclass_plan_is_supported_without_private_imports() -> None:
    plan = sample_plan()
    public = PublicPlan(**plan)
    assert normalize_plan(public) == normalize_plan(plan)


def test_outputs_contain_no_timestamp_or_host_specific_path() -> None:
    forbidden = ("generated_at", "timestamp", str(Path.cwd()), "/tmp/", "\\\\")
    for files in render_all(sample_plan()).values():
        combined = b"\n".join(item.content for item in files).decode("utf-8")
        assert not any(value in combined for value in forbidden)
