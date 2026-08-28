from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import tomllib

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



def appliance_systemd_plan() -> dict:
    plan = sample_plan()
    plan["profile_id"] = "sovereign-linux-node"
    plan["plan_id"] = "sovereign-node-appliance-session"
    plan["source_digests"].update(
        {
            "profiles/implementation-settings/appliance-shell.toml": SHA_E,
            "profiles/overlays/appliance-shell.toml": SHA_F,
        }
    )
    plan["services"] = [
        {
            "id": "display-session",
            "kind": "native",
            "command": ["/usr/libexec/koa/display-session"],
            "resources": {"cpu_millis": 300, "memory_bytes": 134217728, "pids": 32},
            "criticality": "critical",
        },
        {
            "id": "session-shell",
            "kind": "native",
            "command": ["/usr/libexec/koa/session-shell"],
            "dependencies": ["display-session"],
            "resources": {"cpu_millis": 250, "memory_bytes": 100663296, "pids": 24},
            "criticality": "critical",
        },
        {
            "id": "presentation-surface",
            "kind": "native",
            "command": ["/usr/libexec/koa/presentation-surface"],
            "dependencies": ["session-shell"],
            "resources": {"cpu_millis": 200, "memory_bytes": 67108864, "pids": 16},
            "criticality": "core",
        },
    ]
    plan["networks"] = []
    plan["volumes"] = []

    def policy(*, unit_class: str, private_devices: bool, restart_delay: int) -> dict:
        return {
            "unit_class": unit_class,
            "restart": {"policy": "on-failure", "delay_seconds": restart_delay},
            "sandbox": {
                "no_new_privileges": True,
                "private_tmp": True,
                "private_devices": private_devices,
                "protect_system": "strict",
                "protect_home": "yes",
                "protect_kernel_tunables": True,
                "protect_kernel_modules": True,
                "protect_kernel_logs": True,
                "protect_control_groups": True,
                "protect_clock": True,
                "protect_hostname": True,
                "protect_proc": "invisible",
                "proc_subset": "pid",
                "restrict_suid_sgid": True,
                "restrict_realtime": True,
                "lock_personality": True,
                "memory_deny_write_execute": True,
                "remove_ipc": True,
                "restrict_namespaces": True,
                "restrict_address_families": ["AF_UNIX"],
                "system_call_architectures": ["native"],
                "system_call_filter": ["@system-service"],
                "umask": "0077",
            },
        }

    plan["systemd_projection"] = {
        "format": "koa.systemd-projection/v1",
        "policy_source": "profiles/implementation-settings/appliance-shell.toml",
        "overlay_source": "profiles/overlays/appliance-shell.toml",
        "services": {
            "display-session": policy(
                unit_class="subsystem", private_devices=False, restart_delay=1
            ),
            "session-shell": policy(
                unit_class="component", private_devices=True, restart_delay=2
            ),
            "presentation-surface": policy(
                unit_class="subsystem", private_devices=True, restart_delay=3
            ),
        },
    }
    return plan


def _service_text(outputs: tuple[RenderedFile, ...], service_id: str) -> str:
    path = f"systemd/koa-{service_id}.service"
    return next(item.text for item in outputs if item.path == path)


def test_appliance_systemd_projection_derives_names_order_policy_and_resources() -> None:
    outputs = render("systemd", appliance_systemd_plan())
    service_paths = {item.path for item in outputs if item.path.endswith(".service")}
    assert service_paths == {
        "systemd/koa-display-session.service",
        "systemd/koa-presentation-surface.service",
        "systemd/koa-session-shell.service",
    }
    assert "systemd/koa-wayland-compositor.service" not in service_paths
    assert "systemd/koa-appliance-shell.service" not in service_paths

    shell = _service_text(outputs, "session-shell")
    assert "# Template-Class: component" in shell
    assert "Requires=koa-display-session.service" in shell
    assert "After=koa-display-session.service" in shell
    assert "Restart=on-failure" in shell
    assert "RestartSec=2s" in shell
    assert "PrivateDevices=yes" in shell
    assert "ProtectSystem=strict" in shell
    assert "ProtectKernelTunables=yes" in shell
    assert "ProtectKernelModules=yes" in shell
    assert "ProtectProc=invisible" in shell
    assert "ProcSubset=pid" in shell
    assert "RestrictRealtime=yes" in shell
    assert "RemoveIPC=yes" in shell
    assert "RestrictAddressFamilies=AF_UNIX" in shell
    assert "SystemCallArchitectures=native" in shell
    assert "SystemCallFilter=@system-service" in shell
    assert "UMask=0077" in shell
    assert "CPUQuota=25%" in shell
    assert "MemoryMax=100663296" in shell
    assert "TasksMax=24" in shell
    assert "WantedBy=koa-critical.target" in shell


def test_appliance_systemd_projection_is_deterministic_under_input_reordering() -> None:
    original = appliance_systemd_plan()
    reordered = deepcopy(original)
    reordered["services"].reverse()
    reordered["source_digests"] = dict(reversed(list(reordered["source_digests"].items())))
    reordered["systemd_projection"]["services"] = dict(
        reversed(list(reordered["systemd_projection"]["services"].items()))
    )
    assert as_bytes(render("systemd", original)) == as_bytes(render("systemd", reordered))


def test_appliance_systemd_projection_fails_closed_on_incomplete_or_unowned_policy() -> None:
    plan = appliance_systemd_plan()
    del plan["systemd_projection"]
    with pytest.raises(RenderError, match="require an explicit systemd_projection"):
        render("systemd", plan)

    plan = appliance_systemd_plan()
    del plan["systemd_projection"]["services"]["session-shell"]
    with pytest.raises(RenderError, match="missing enabled services"):
        render("systemd", plan)

    plan = appliance_systemd_plan()
    plan["systemd_projection"]["services"]["unknown-service"] = deepcopy(
        plan["systemd_projection"]["services"]["session-shell"]
    )
    with pytest.raises(RenderError, match="inactive or unknown services"):
        render("systemd", plan)

    plan = appliance_systemd_plan()
    del plan["source_digests"]["profiles/implementation-settings/appliance-shell.toml"]
    with pytest.raises(RenderError, match="digested profiles/ authority"):
        render("systemd", plan)

    plan = appliance_systemd_plan()
    del plan["systemd_projection"]["services"]["session-shell"]["sandbox"]["private_devices"]
    with pytest.raises(RenderError, match="sandbox.*missing"):
        render("systemd", plan)


def test_appliance_systemd_policy_change_changes_rendered_unit() -> None:
    first = appliance_systemd_plan()
    second = deepcopy(first)
    second["systemd_projection"]["services"]["session-shell"]["restart"]["delay_seconds"] = 7
    assert as_bytes(render("systemd", first)) != as_bytes(render("systemd", second))
    assert "RestartSec=7s" in _service_text(render("systemd", second), "session-shell")


def test_host_service_templates_require_plan_derived_runtime_policy() -> None:
    root = Path(__file__).resolve().parents[2]
    for relative in (
        "host/systemd/templates/koa-component.service.in",
        "host/systemd/templates/koa-subsystem.service.in",
    ):
        template = (root / relative).read_text(encoding="utf-8")
        assert "{{RESTART_POLICY_LINES}}" in template
        assert "{{SANDBOX_POLICY_LINES}}" in template
        assert "{{RESOURCE_ENVELOPE_LINES}}" in template
        assert "Restart=on-failure" not in template
        assert "NoNewPrivileges=yes" not in template
        assert "UMask=0027" not in template


def test_appliance_profile_declares_derived_systemd_projection_without_host_authority() -> None:
    root = Path(__file__).resolve().parents[2]
    settings = tomllib.loads(
        (root / "profiles/implementation-settings/appliance-shell.toml").read_text(encoding="utf-8")
    )
    overlay = tomllib.loads(
        (root / "profiles/overlays/appliance-shell.toml").read_text(encoding="utf-8")
    )
    contract = json.loads(
        (root / "docs/contracts/profiles/appliance-shell.profile.json").read_text(encoding="utf-8")
    )

    projection = settings["implementation"]["systemd_projection"]
    assert projection["format"] == "koa.systemd-projection/v1"
    assert projection["unit_name_source"] == "resolved_service_id"
    assert projection["dependency_source"] == "resolved_service_dependencies"
    assert projection["restart_policy_source"] == "resolved_lifecycle_policy"
    assert projection["sandbox_policy_source"] == "resolved_security_policy"
    assert projection["resource_envelope_source"] == "resolved_resource_plan"
    assert projection["require_explicit_service_policy"] is True
    assert projection["allow_static_profile_units"] is False
    assert projection["presentation_grants_host_authority"] is False
    assert overlay["authority"]["presentation_grants_host_authority"] is False
    assert "static_profile_systemd_unit_is_selected" in overlay["validation"]["reject_when"]
    assert contract["koa_spaces"]["authority"] == "non_authoritative_presentation"
    assert contract["koa_spaces"]["presentation_grants_authority"] is False


def test_existing_generated_root_admits_service_units_and_static_units_are_absent() -> None:
    root = Path(__file__).resolve().parents[2]
    generated = json.loads((root / ".koa/generated-paths.json").read_text(encoding="utf-8"))
    generated_root = next(item for item in generated["roots"] if item["path"] == "generated/")
    assert "service units" in generated_root["allowed_content"]
    assert {item["path"] for item in generated["entries"]} == {"docs/generated", "generated"}
    assert not (root / "host/systemd/units/koa-wayland-compositor.service").exists()
    assert not (root / "host/systemd/units/koa-appliance-shell.service").exists()


def test_image_bundle_projection_has_canonical_owned_paths() -> None:
    from koa_assembly.renderers.image import render_assembly_bundle

    files = render_assembly_bundle(
        sample_plan(),
        bundle_id="B-0092",
        profile_contract_ref="docs/contracts/profiles/sovereign-linux-node.profile.json",
        tool_versions={"koa_assembly": "test"},
        entrypoint_delegates={
            "koa-activation": ("/usr/bin/true",),
            "koa-health-aggregate": ("/usr/bin/true",),
            "koa-offline-import": ("/usr/bin/true",),
        },
    )
    paths = {item.path for item in files}
    assert "assembly/B-0092/bundle.json" in paths
    assert "image/image-manifest.json" in paths
    assert {
        "assembly/B-0092/entrypoints/koa-activation",
        "assembly/B-0092/entrypoints/koa-health-aggregate",
        "assembly/B-0092/entrypoints/koa-offline-import",
    } <= paths
