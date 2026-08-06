"""Render resolved container plans as a deterministic Compose document."""

from __future__ import annotations

from typing import Any

from . import (
    RenderError,
    RenderedFile,
    canonical_json_bytes,
    generated_metadata,
    normalize_plan,
    qualified_name,
    renderer_manifest,
    secret_ref_parts,
    secret_resource_name,
    validate_rendered_files,
)

_RENDERER = "compose"


def _service(service: dict[str, Any], secrets: set[str]) -> dict[str, Any]:
    if service["kind"] != "container":
        raise RenderError(f"Compose renderer cannot represent native service {service['id']}")
    result: dict[str, Any] = {
        "image": service["image"],
        "restart": "on-failure",
        "cap_drop": ["ALL"],
        "security_opt": ["no-new-privileges:true"],
        "labels": {
            "io.koa.component": service["id"],
            "io.koa.authority": "derived-projection",
        },
    }
    if service["command"]:
        result["command"] = service["command"]
    if service["user"]:
        result["user"] = service["user"]
    if service["dependencies"]:
        result["depends_on"] = {
            dependency: {"condition": "service_started", "required": True}
            for dependency in service["dependencies"]
        }
    environment: dict[str, str] = {}
    service_secrets: list[dict[str, str]] = []
    for key, value in service["environment"].items():
        if value["kind"] == "literal":
            environment[key] = value["value"]
        else:
            _, secret_key = secret_ref_parts(value["ref"])
            secret = secret_resource_name(value["ref"])
            secrets.add(secret)
            target = f"{key.lower()}-{secret_key}"
            environment[f"{key}_FILE"] = f"/run/secrets/{target}"
            service_secrets.append({"source": secret, "target": target})
    if environment:
        result["environment"] = environment
    if service_secrets:
        result["secrets"] = sorted(service_secrets, key=lambda item: (item["source"], item["target"]))
    if service["mounts"]:
        result["volumes"] = [
            f"{item['volume']}:{item['target']}{':ro' if item['read_only'] else ''}"
            for item in service["mounts"]
        ]
    if service["networks"]:
        result["networks"] = service["networks"]
    published = [
        f"{item['host_ip']}:{item['published']}:{item['target']}/{item['protocol']}"
        for item in service["ports"]
        if item["published"] is not None
    ]
    if published:
        result["ports"] = published
    if service["capabilities"]:
        result["cap_add"] = [item.removeprefix("CAP_") for item in service["capabilities"]]
    resources = service["resources"]
    limits: dict[str, str | int] = {}
    if "cpu_millis" in resources:
        limits["cpus"] = f"{resources['cpu_millis'] / 1000:.3f}"
    if "memory_bytes" in resources:
        limits["memory"] = str(resources["memory_bytes"])
    if "pids" in resources:
        result["pids_limit"] = resources["pids"]
    if limits:
        result["deploy"] = {"resources": {"limits": limits}}
    if service["healthcheck"]:
        health = service["healthcheck"]
        result["healthcheck"] = {
            "test": ["CMD", *health["command"]],
            "interval": f"{health['interval_seconds']}s",
            "timeout": f"{health['timeout_seconds']}s",
            "retries": health["retries"],
        }
    return result


def render(plan: Any) -> tuple[RenderedFile, ...]:
    normalized = normalize_plan(plan)
    secret_names: set[str] = set()
    services = {
        service["id"]: _service(service, secret_names)
        for service in normalized["services"]
        if service["enabled"]
    }
    document: dict[str, Any] = {
        "name": f"koa-{normalized['profile_id']}",
        "x-koa-generated": generated_metadata(_RENDERER, normalized),
        "services": services,
        "networks": {
            item["id"]: {
                "name": qualified_name(item["id"]),
                "internal": item["internal"],
                "driver": item["driver"],
                "labels": {"io.koa.authority": "derived-projection"},
            }
            for item in normalized["networks"]
        },
        "volumes": {
            item["id"]: {
                "name": qualified_name(item["id"]),
                "labels": {
                    "io.koa.owner": item["owner"],
                    "io.koa.authority": "derived-projection",
                },
            }
            for item in normalized["volumes"]
        },
    }
    if secret_names:
        document["secrets"] = {name: {"external": True, "name": name} for name in sorted(secret_names)}
    compose_file = RenderedFile(
        path="compose/compose.yaml",
        content=canonical_json_bytes(document),
        media_type="application/yaml",
    )
    files = [compose_file]
    files.append(renderer_manifest(_RENDERER, normalized, files))
    return validate_rendered_files(files)
