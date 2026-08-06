"""Render resolved service plans as native systemd units."""

from __future__ import annotations

from typing import Any

from . import (
    RenderedFile,
    generated_header,
    normalize_plan,
    qualified_name,
    renderer_manifest,
    secret_ref_parts,
    systemd_quote,
    validate_rendered_files,
)

_RENDERER = "systemd"
_TARGETS = {
    "critical": "koa-critical.target",
    "core": "koa-core.target",
    "background": "koa-background.target",
    "optional": "koa-optional.target",
}


def _unit_name(service_id: str) -> str:
    return f"{qualified_name(service_id)}.service"


def _container_command(service: dict[str, Any]) -> list[str]:
    argv = [
        "/usr/bin/podman",
        "run",
        "--rm",
        "--name",
        qualified_name(service["id"]),
        "--replace",
        "--cap-drop=all",
    ]
    if service["user"]:
        argv.extend(["--user", service["user"]])
    for capability in service["capabilities"]:
        argv.append(f"--cap-add={capability.removeprefix('CAP_')}")
    for network in service["networks"]:
        argv.extend(["--network", qualified_name(network)])
    for mount in service["mounts"]:
        suffix = ":ro" if mount["read_only"] else ""
        argv.extend(["--volume", f"{qualified_name(mount['volume'])}:{mount['target']}{suffix}"])
    for port in service["ports"]:
        if port["published"] is not None:
            argv.extend([
                "--publish",
                f"{port['host_ip']}:{port['published']}:{port['target']}/{port['protocol']}",
            ])
    resources = service["resources"]
    if "cpu_millis" in resources:
        argv.extend(["--cpus", f"{resources['cpu_millis'] / 1000:.3f}"])
    if "memory_bytes" in resources:
        argv.extend(["--memory", str(resources["memory_bytes"])])
    if "pids" in resources:
        argv.extend(["--pids-limit", str(resources["pids"])])
    for key, value in service["environment"].items():
        if value["kind"] == "literal":
            argv.extend(["--env", f"{key}={value['value']}"])
        else:
            argv.extend(["--volume", f"%d/{key}:/run/secrets/{key}:ro"])
            argv.extend(["--env", f"{key}_FILE=/run/secrets/{key}"])
    argv.append(service["image"])
    argv.extend(service["command"])
    return argv


def _render_unit(plan: dict[str, Any], service: dict[str, Any]) -> RenderedFile:
    dependencies = [_unit_name(item) for item in service["dependencies"]]
    after = list(dependencies)
    if service["networks"] or service["ports"]:
        after.append("network-online.target")
    lines = [
        generated_header(_RENDERER, plan).rstrip(),
        "[Unit]",
        f"Description=kOA generated service {service['id']}",
    ]
    if after:
        lines.append("After=" + " ".join(sorted(set(after))))
    if dependencies:
        lines.append("Requires=" + " ".join(sorted(dependencies)))
    lines.extend([
        "",
        "[Service]",
        "Type=simple",
        "NoNewPrivileges=yes",
        "PrivateTmp=yes",
        f"ProtectHome={'no' if service['kind'] == 'container' else 'yes'}",
        f"ProtectSystem={'full' if service['kind'] == 'container' else 'strict'}",
        "RestrictSUIDSGID=yes",
        "LockPersonality=yes",
        "MemoryDenyWriteExecute=yes",
    ])
    if service["user"]:
        lines.append(f"User={service['user']}")
    capabilities = " ".join(service["capabilities"])
    lines.append(f"CapabilityBoundingSet={capabilities}")
    lines.append(f"AmbientCapabilities={capabilities}")
    for key, value in service["environment"].items():
        if value["kind"] == "literal":
            lines.append("Environment=" + systemd_quote(f"{key}={value['value']}"))
        else:
            secret, secret_key = secret_ref_parts(value["ref"])
            source = f"/run/koa/secrets/{secret}/{secret_key}"
            lines.append(f"LoadCredential={key}:{source}")
            lines.append("Environment=" + systemd_quote(f"{key}_FILE=%d/{key}"))
    command = service["command"] if service["kind"] == "native" else _container_command(service)
    lines.append("ExecStart=" + " ".join(systemd_quote(item) for item in command))
    lines.append("Restart=on-failure")
    lines.append("RestartSec=5s")
    if "memory_bytes" in service["resources"]:
        lines.append(f"MemoryMax={service['resources']['memory_bytes']}")
    if "pids" in service["resources"]:
        lines.append(f"TasksMax={service['resources']['pids']}")
    lines.extend([
        "",
        "[Install]",
        f"WantedBy={_TARGETS.get(service['criticality'], 'koa-core.target')}",
        "",
    ])
    return RenderedFile(
        path=f"systemd/{_unit_name(service['id'])}",
        content="\n".join(lines).encode("utf-8"),
        media_type="text/plain; charset=utf-8",
    )


def render(plan: Any) -> tuple[RenderedFile, ...]:
    normalized = normalize_plan(plan)
    files = [_render_unit(normalized, service) for service in normalized["services"] if service["enabled"]]
    files.append(renderer_manifest(_RENDERER, normalized, files))
    return validate_rendered_files(files)
