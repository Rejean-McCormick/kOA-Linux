"""Render resolved container plans as Podman Quadlet files."""

from __future__ import annotations

from typing import Any

from . import (
    RenderError,
    RenderedFile,
    generated_header,
    normalize_plan,
    qualified_name,
    renderer_manifest,
    secret_ref_parts,
    secret_resource_name,
    systemd_quote,
    validate_rendered_files,
)

_RENDERER = "quadlet"
_TARGETS = {
    "critical": "koa-critical.target",
    "core": "koa-core.target",
    "background": "koa-background.target",
    "optional": "koa-optional.target",
}


def _render_network(plan: dict[str, Any], network: dict[str, Any]) -> RenderedFile:
    lines = [
        generated_header(_RENDERER, plan).rstrip(),
        "[Network]",
        f"NetworkName={qualified_name(network['id'])}",
        f"Internal={'true' if network['internal'] else 'false'}",
        "",
    ]
    return RenderedFile(f"quadlet/{qualified_name(network['id'])}.network", "\n".join(lines).encode(), "text/plain; charset=utf-8")


def _render_volume(plan: dict[str, Any], volume: dict[str, Any]) -> RenderedFile:
    lines = [
        generated_header(_RENDERER, plan).rstrip(),
        "[Volume]",
        f"VolumeName={qualified_name(volume['id'])}",
        f"Label=io.koa.owner={volume['owner']}",
        "Label=io.koa.authority=derived-projection",
        "",
    ]
    return RenderedFile(f"quadlet/{qualified_name(volume['id'])}.volume", "\n".join(lines).encode(), "text/plain; charset=utf-8")


def _render_container(plan: dict[str, Any], service: dict[str, Any]) -> RenderedFile:
    if service["kind"] != "container":
        raise RenderError(f"Quadlet renderer cannot represent native service {service['id']}")
    lines = [
        generated_header(_RENDERER, plan).rstrip(),
        "[Unit]",
        f"Description=kOA generated container {service['id']}",
    ]
    dependencies = [f"{qualified_name(item)}.service" for item in service["dependencies"]]
    if dependencies:
        lines.append("After=" + " ".join(dependencies))
        lines.append("Requires=" + " ".join(dependencies))
    lines.extend(["", "[Container]", f"Image={service['image']}", f"ContainerName={qualified_name(service['id'])}"])
    if service["command"]:
        lines.append("Exec=" + " ".join(systemd_quote(item) for item in service["command"]))
    if service["user"]:
        lines.append(f"User={service['user']}")
    for network in service["networks"]:
        lines.append(f"Network={qualified_name(network)}.network")
    for mount in service["mounts"]:
        suffix = ":ro" if mount["read_only"] else ""
        lines.append(f"Volume={qualified_name(mount['volume'])}.volume:{mount['target']}{suffix}")
    for port in service["ports"]:
        if port["published"] is not None:
            lines.append(f"PublishPort={port['host_ip']}:{port['published']}:{port['target']}/{port['protocol']}")
    for key, value in service["environment"].items():
        if value["kind"] == "literal":
            lines.append("Environment=" + systemd_quote(f"{key}={value['value']}"))
        else:
            _, secret_key = secret_ref_parts(value["ref"])
            secret = secret_resource_name(value["ref"])
            lines.append(f"Secret={secret},target={key},type=mount")
            lines.append("Environment=" + systemd_quote(f"{key}_FILE=/run/secrets/{key}"))
    lines.append("DropCapability=all")
    for capability in service["capabilities"]:
        lines.append(f"AddCapability={capability.removeprefix('CAP_')}")
    resources = service["resources"]
    if "memory_bytes" in resources:
        lines.append(f"Memory={resources['memory_bytes']}")
    if "pids" in resources:
        lines.append(f"PidsLimit={resources['pids']}")
    lines.extend([
        "NoNewPrivileges=true",
        "",
        "[Service]",
        "Restart=on-failure",
        "RestartSec=5s",
        "",
        "[Install]",
        f"WantedBy={_TARGETS.get(service['criticality'], 'koa-core.target')}",
        "",
    ])
    return RenderedFile(f"quadlet/{qualified_name(service['id'])}.container", "\n".join(lines).encode(), "text/plain; charset=utf-8")


def render(plan: Any) -> tuple[RenderedFile, ...]:
    normalized = normalize_plan(plan)
    files: list[RenderedFile] = []
    files.extend(_render_network(normalized, item) for item in normalized["networks"])
    files.extend(_render_volume(normalized, item) for item in normalized["volumes"])
    files.extend(_render_container(normalized, item) for item in normalized["services"] if item["enabled"])
    files.append(renderer_manifest(_RENDERER, normalized, files))
    return validate_rendered_files(files)
