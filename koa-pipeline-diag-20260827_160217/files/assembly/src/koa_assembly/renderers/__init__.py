"""Deterministic deployment renderers for the kOA assembly engine.

The renderers consume already-resolved public plans. They do not resolve profiles,
select components, or grant authority. Every result is a derived projection with
stable provenance metadata.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
from typing import Any

GENERATOR_VERSION = "1.0.0"
_IDENTIFIER = re.compile(r"^[a-z0-9](?:[a-z0-9._-]{0,126}[a-z0-9])?$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_SAFE_ENV = re.compile(r"^[A-Z_][A-Z0-9_]*$")
_SECRET_KEY = re.compile(r"(?:SECRET|TOKEN|PASSWORD|PRIVATE_KEY|CREDENTIAL)", re.IGNORECASE)


class RenderError(ValueError):
    """Raised when an input plan cannot be rendered without guessing."""


@dataclass(frozen=True, slots=True)
class RenderedFile:
    """One deterministic generated output."""

    path: str
    content: bytes
    media_type: str
    mode: int = 0o644

    def __post_init__(self) -> None:
        path = PurePosixPath(self.path)
        if path.is_absolute() or not path.parts or ".." in path.parts:
            raise RenderError(f"unsafe rendered path: {self.path!r}")
        if not isinstance(self.content, bytes):
            raise TypeError("RenderedFile.content must be bytes")
        if self.mode not in {0o644, 0o755}:
            raise RenderError(f"unsupported output mode: {oct(self.mode)}")

    @property
    def digest(self) -> str:
        return f"sha256:{sha256(self.content).hexdigest()}"

    @property
    def text(self) -> str:
        return self.content.decode("utf-8")


def _plain(value: Any) -> Any:
    if is_dataclass(value):
        return _plain(asdict(value))
    for method_name in ("model_dump", "to_dict", "as_dict"):
        method = getattr(value, method_name, None)
        if callable(method):
            return _plain(method())
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    if isinstance(value, list):
        return [_plain(item) for item in value]
    return value


def _pick(mapping: Mapping[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in mapping:
            return mapping[name]
    return default


def _identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.fullmatch(value):
        raise RenderError(f"{field} must be a lowercase stable identifier")
    return value


def _digest(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise RenderError(f"{field} must be a sha256 digest")
    normalized = value.lower()
    if not _DIGEST.fullmatch(normalized):
        raise RenderError(f"{field} must match sha256:<64 lowercase hex>")
    return normalized


def _command(value: Any, field: str) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        raise RenderError(f"{field} must be a non-empty argument vector, not a shell string")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item or "\x00" in item or "\n" in item:
            raise RenderError(f"{field}[{index}] must be a non-empty single-line string")
        result.append(item)
    return result


def _section_items(data: Mapping[str, Any], plural: str, section: str) -> list[Any]:
    value = data.get(plural)
    if value is None and section in data:
        nested = _plain(data[section])
        if isinstance(nested, Mapping):
            value = _pick(nested, plural, "items", "entries", default=[])
        else:
            value = nested
    if value is None:
        return []
    if isinstance(value, Mapping):
        expanded = []
        for key, item in value.items():
            item = _plain(item)
            if isinstance(item, Mapping) and not any(name in item for name in ("id", "name", "service_id", "volume_id", "network_id")):
                item = {"id": str(key), **item}
            expanded.append(item)
        return expanded
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise RenderError(f"{plural} must be a sequence or mapping")
    return list(value)


def _normalize_sources(value: Any) -> dict[str, str]:
    if isinstance(value, Mapping):
        pairs = value.items()
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        pairs = []
        for item in value:
            item = _plain(item)
            if not isinstance(item, Mapping):
                raise RenderError("source_digests list entries must be mappings")
            pairs.append((_pick(item, "path", "source", "uri"), _pick(item, "digest", "sha256")))
    else:
        raise RenderError("source_digests must be a non-empty mapping or sequence")
    result: dict[str, str] = {}
    for raw_path, raw_digest in pairs:
        if not isinstance(raw_path, str) or not raw_path or raw_path.startswith("/") or ".." in PurePosixPath(raw_path).parts:
            raise RenderError(f"invalid source path: {raw_path!r}")
        if raw_path in result:
            raise RenderError(f"duplicate source path: {raw_path}")
        result[raw_path] = _digest(raw_digest, f"source_digests[{raw_path!r}]")
    if not result:
        raise RenderError("at least one source digest is required")
    return dict(sorted(result.items()))


def _normalize_environment(value: Any, service_id: str) -> dict[str, dict[str, str]]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise RenderError(f"services[{service_id}].environment must be a mapping")
    result: dict[str, dict[str, str]] = {}
    for raw_key, raw_value in value.items():
        key = str(raw_key)
        if not _SAFE_ENV.fullmatch(key):
            raise RenderError(f"invalid environment key {key!r} for {service_id}")
        if isinstance(raw_value, Mapping):
            ref = _pick(raw_value, "secret_ref", "secret", "credential")
            if not isinstance(ref, str) or not ref.startswith("secret://") or len(ref) <= len("secret://"):
                raise RenderError(f"environment {key} has an invalid secret reference")
            result[key] = {"kind": "secret_ref", "ref": ref}
        elif isinstance(raw_value, (str, int, float, bool)):
            literal = str(raw_value).lower() if isinstance(raw_value, bool) else str(raw_value)
            if "\x00" in literal or "\n" in literal:
                raise RenderError(f"environment {key} must be single-line")
            if _SECRET_KEY.search(key):
                raise RenderError(f"environment {key} must use a secret reference")
            result[key] = {"kind": "literal", "value": literal}
        else:
            raise RenderError(f"environment {key} has unsupported value type")
    return dict(sorted(result.items()))


def _normalize_ports(value: Any, service_id: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise RenderError(f"services[{service_id}].ports must be a sequence")
    result: list[dict[str, Any]] = []
    names: set[str] = set()
    for index, raw in enumerate(value):
        raw = _plain(raw)
        if not isinstance(raw, Mapping):
            raise RenderError(f"services[{service_id}].ports[{index}] must be a mapping")
        target = _pick(raw, "target", "container_port", "port")
        published = _pick(raw, "published", "host_port")
        if not isinstance(target, int) or not 1 <= target <= 65535:
            raise RenderError(f"invalid target port for {service_id}")
        if published is not None and (not isinstance(published, int) or not 1 <= published <= 65535):
            raise RenderError(f"invalid published port for {service_id}")
        name = _identifier(_pick(raw, "name", default=f"port-{target}"), f"services[{service_id}].ports.name")
        if name in names:
            raise RenderError(f"duplicate port name {name!r} for {service_id}")
        names.add(name)
        protocol = str(_pick(raw, "protocol", default="tcp")).lower()
        if protocol not in {"tcp", "udp"}:
            raise RenderError(f"unsupported protocol {protocol!r}")
        result.append({
            "name": name,
            "target": target,
            "published": published,
            "protocol": protocol,
            "host_ip": str(_pick(raw, "host_ip", default="127.0.0.1")),
        })
    return sorted(result, key=lambda item: (item["name"], item["target"]))


def _normalize_mounts(value: Any, service_id: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise RenderError(f"services[{service_id}].mounts must be a sequence")
    result: list[dict[str, Any]] = []
    for index, raw in enumerate(value):
        raw = _plain(raw)
        if not isinstance(raw, Mapping):
            raise RenderError(f"services[{service_id}].mounts[{index}] must be a mapping")
        volume = _identifier(_pick(raw, "volume", "source", "volume_id"), f"services[{service_id}].mounts.volume")
        target = _pick(raw, "target", "destination", "mount_path")
        if not isinstance(target, str) or not target.startswith("/") or ".." in PurePosixPath(target).parts:
            raise RenderError(f"invalid mount target for {service_id}: {target!r}")
        result.append({"volume": volume, "target": target, "read_only": bool(_pick(raw, "read_only", "readonly", default=False))})
    return sorted(result, key=lambda item: (item["target"], item["volume"]))


def _normalize_resources(value: Any, service_id: str) -> dict[str, int]:
    if value is None:
        return {}
    value = _plain(value)
    if not isinstance(value, Mapping):
        raise RenderError(f"services[{service_id}].resources must be a mapping")
    result: dict[str, int] = {}
    aliases = {
        "cpu_millis": ("cpu_millis", "cpu_millicores"),
        "memory_bytes": ("memory_bytes", "memory"),
        "pids": ("pids", "pids_limit"),
    }
    for canonical, names in aliases.items():
        raw = _pick(value, *names)
        if raw is None:
            continue
        if not isinstance(raw, int) or raw <= 0:
            raise RenderError(f"services[{service_id}].resources.{canonical} must be a positive integer")
        result[canonical] = raw
    return result


def _normalize_service(raw: Any) -> dict[str, Any]:
    raw = _plain(raw)
    if not isinstance(raw, Mapping):
        raise RenderError("service entries must be mappings or dataclasses")
    service_id = _identifier(_pick(raw, "id", "service_id", "component_id", "name"), "service.id")
    image = _pick(raw, "image", "image_ref")
    command_value = _pick(raw, "command", "argv", "exec_start")
    kind = _pick(raw, "kind", "runtime", "deployment_kind")
    if kind is None:
        if image is not None:
            kind = "container"
        elif command_value is not None:
            kind = "native"
        else:
            raise RenderError(f"service {service_id} must declare kind or executable material")
    kind = str(kind).lower().replace("_", "-")
    if kind not in {"native", "container"}:
        raise RenderError(f"service {service_id} has unsupported kind {kind!r}")
    command = _command(command_value, f"services[{service_id}].command") if command_value is not None else []
    if kind == "native" and not command:
        raise RenderError(f"native service {service_id} requires a command")
    if kind == "container":
        if not isinstance(image, str) or "@sha256:" not in image:
            raise RenderError(f"container service {service_id} requires an immutable image digest")
        image_digest = "sha256:" + image.rsplit("@sha256:", 1)[1].lower()
        _digest(image_digest, f"services[{service_id}].image")
    dependencies = _pick(raw, "dependencies", "requires", "depends_on", default=[])
    if not isinstance(dependencies, Sequence) or isinstance(dependencies, (str, bytes)):
        raise RenderError(f"services[{service_id}].dependencies must be a sequence")
    deps = sorted({_identifier(dep, f"services[{service_id}].dependency") for dep in dependencies})
    networks = _pick(raw, "networks", "network_ids", default=[])
    if not isinstance(networks, Sequence) or isinstance(networks, (str, bytes)):
        raise RenderError(f"services[{service_id}].networks must be a sequence")
    network_ids = sorted({_identifier(item, f"services[{service_id}].network") for item in networks})
    capabilities = _pick(raw, "capabilities", default=[])
    if not isinstance(capabilities, Sequence) or isinstance(capabilities, (str, bytes)):
        raise RenderError(f"services[{service_id}].capabilities must be a sequence")
    caps = sorted({str(item) for item in capabilities})
    for cap in caps:
        if not re.fullmatch(r"CAP_[A-Z0-9_]+", cap):
            raise RenderError(f"service {service_id} has invalid Linux capability {cap!r}")
    health = _pick(raw, "healthcheck", "health")
    healthcheck: dict[str, Any] | None = None
    if health is not None:
        health = _plain(health)
        if not isinstance(health, Mapping):
            raise RenderError(f"services[{service_id}].healthcheck must be a mapping")
        healthcheck = {
            "command": _command(_pick(health, "command", "argv", "test"), f"services[{service_id}].healthcheck.command"),
            "interval_seconds": int(_pick(health, "interval_seconds", "interval", default=30)),
            "timeout_seconds": int(_pick(health, "timeout_seconds", "timeout", default=5)),
            "retries": int(_pick(health, "retries", default=3)),
        }
        if any(healthcheck[key] <= 0 for key in ("interval_seconds", "timeout_seconds", "retries")):
            raise RenderError(f"service {service_id} healthcheck values must be positive")
    user = _pick(raw, "user", "run_as")
    if user is not None and (not isinstance(user, str) or not user or "\n" in user):
        raise RenderError(f"service {service_id} user must be a non-empty string")
    return {
        "id": service_id,
        "kind": kind,
        "image": image,
        "command": command,
        "dependencies": deps,
        "environment": _normalize_environment(_pick(raw, "environment", "env"), service_id),
        "ports": _normalize_ports(_pick(raw, "ports"), service_id),
        "mounts": _normalize_mounts(_pick(raw, "mounts", "volumes"), service_id),
        "networks": network_ids,
        "resources": _normalize_resources(_pick(raw, "resources"), service_id),
        "capabilities": caps,
        "user": user,
        "healthcheck": healthcheck,
        "criticality": str(_pick(raw, "criticality", "tier", default="core")),
        "enabled": bool(_pick(raw, "enabled", default=True)),
    }


def _normalize_network(raw: Any) -> dict[str, Any]:
    raw = _plain(raw)
    if not isinstance(raw, Mapping):
        raise RenderError("network entries must be mappings")
    network_id = _identifier(_pick(raw, "id", "network_id", "name"), "network.id")
    return {
        "id": network_id,
        "internal": bool(_pick(raw, "internal", default=True)),
        "driver": str(_pick(raw, "driver", default="bridge")),
    }


def _normalize_volume(raw: Any) -> dict[str, Any]:
    raw = _plain(raw)
    if not isinstance(raw, Mapping):
        raise RenderError("volume entries must be mappings")
    volume_id = _identifier(_pick(raw, "id", "volume_id", "name"), "volume.id")
    owner = _identifier(_pick(raw, "owner", "owner_id", "service_id"), f"volumes[{volume_id}].owner")
    size = _pick(raw, "size_bytes", "capacity_bytes")
    if size is not None and (not isinstance(size, int) or size <= 0):
        raise RenderError(f"volumes[{volume_id}].size_bytes must be positive")
    mount_path = _pick(raw, "mount_path", "path")
    if mount_path is not None and (not isinstance(mount_path, str) or not mount_path.startswith("/") or ".." in PurePosixPath(mount_path).parts):
        raise RenderError(f"volumes[{volume_id}].mount_path is invalid")
    return {
        "id": volume_id,
        "owner": owner,
        "persistent": bool(_pick(raw, "persistent", default=True)),
        "size_bytes": size,
        "mount_path": mount_path,
        "read_only": bool(_pick(raw, "read_only", default=False)),
    }


def _normalize_package(raw: Any) -> dict[str, str]:
    raw = _plain(raw)
    if not isinstance(raw, Mapping):
        raise RenderError("package entries must be mappings")
    name = _identifier(_pick(raw, "name", "id", "package_id"), "package.name")
    version = _pick(raw, "version")
    if not isinstance(version, str) or not version:
        raise RenderError(f"package {name} requires a version")
    return {"name": name, "version": version, "digest": _digest(_pick(raw, "digest"), f"packages[{name}].digest")}


def _normalize_file(raw: Any) -> dict[str, Any]:
    raw = _plain(raw)
    if not isinstance(raw, Mapping):
        raise RenderError("file entries must be mappings")
    path = _pick(raw, "path", "destination")
    if not isinstance(path, str) or not path.startswith("/") or ".." in PurePosixPath(path).parts:
        raise RenderError(f"invalid installed file path: {path!r}")
    mode = _pick(raw, "mode", default="0644")
    if isinstance(mode, int):
        mode = f"{mode:04o}"
    if not isinstance(mode, str) or not re.fullmatch(r"0[0-7]{3}", mode):
        raise RenderError(f"invalid mode for installed file {path}")
    return {"path": path, "digest": _digest(_pick(raw, "digest"), f"files[{path}].digest"), "mode": mode}


def _normalize_offline(value: Any) -> dict[str, Any]:
    if value is None:
        return {"enabled": False, "allow_network": False, "artifacts": []}
    value = _plain(value)
    if not isinstance(value, Mapping):
        raise RenderError("offline must be a mapping")
    artifacts_value = _pick(value, "artifacts", "includes", default=[])
    if not isinstance(artifacts_value, Sequence) or isinstance(artifacts_value, (str, bytes)):
        raise RenderError("offline.artifacts must be a sequence")
    artifacts: list[dict[str, str]] = []
    for raw in artifacts_value:
        raw = _plain(raw)
        if not isinstance(raw, Mapping):
            raise RenderError("offline artifact entries must be mappings")
        artifact_id = _identifier(_pick(raw, "id", "artifact_id", "name"), "offline.artifact.id")
        path = _pick(raw, "path", "source")
        if not isinstance(path, str) or path.startswith("/") or ".." in PurePosixPath(path).parts:
            raise RenderError(f"offline artifact {artifact_id} has an unsafe path")
        artifacts.append({
            "id": artifact_id,
            "path": path,
            "digest": _digest(_pick(raw, "digest"), f"offline.artifacts[{artifact_id}].digest"),
            "artifact_class": str(_pick(raw, "artifact_class", "class", default="deployable_package")),
        })
    return {
        "enabled": bool(_pick(value, "enabled", default=bool(artifacts))),
        "allow_network": bool(_pick(value, "allow_network", default=False)),
        "verification_policy": str(_pick(value, "verification_policy", default="verify-before-use")),
        "artifacts": sorted(artifacts, key=lambda item: item["id"]),
    }


def _assert_dependency_graph(services: list[dict[str, Any]]) -> None:
    ids = {service["id"] for service in services}
    graph = {service["id"]: set(service["dependencies"]) for service in services}
    for service_id, dependencies in graph.items():
        unknown = dependencies - ids
        if unknown:
            raise RenderError(f"service {service_id} depends on unknown services: {sorted(unknown)}")
        if service_id in dependencies:
            raise RenderError(f"service {service_id} depends on itself")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visited:
            return
        if node in visiting:
            raise RenderError(f"service dependency cycle detected at {node}")
        visiting.add(node)
        for dependency in sorted(graph[node]):
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in sorted(graph):
        visit(node)


def normalize_plan(plan: Any) -> dict[str, Any]:
    """Convert a public plan object into the renderer's closed canonical input."""

    data = _plain(plan)
    if not isinstance(data, Mapping):
        raise RenderError("render input must be a mapping, dataclass, or public model")
    profile_id = _identifier(_pick(data, "profile_id", "effective_profile_id", "profile"), "profile_id")
    plan_id = _identifier(_pick(data, "plan_id", "id", default=f"{profile_id}-deployment"), "plan_id")
    sources = _normalize_sources(_pick(data, "source_digests", "sources"))
    services = sorted((_normalize_service(item) for item in _section_items(data, "services", "service_plan")), key=lambda item: item["id"])
    if not services:
        raise RenderError("at least one service is required")
    if len({item["id"] for item in services}) != len(services):
        raise RenderError("service identifiers must be unique")
    _assert_dependency_graph(services)
    networks = sorted((_normalize_network(item) for item in _section_items(data, "networks", "network_plan")), key=lambda item: item["id"])
    volumes = sorted((_normalize_volume(item) for item in _section_items(data, "volumes", "storage_plan")), key=lambda item: item["id"])
    if len({item["id"] for item in networks}) != len(networks):
        raise RenderError("network identifiers must be unique")
    if len({item["id"] for item in volumes}) != len(volumes):
        raise RenderError("volume identifiers must be unique")
    network_ids = {item["id"] for item in networks}
    volume_ids = {item["id"] for item in volumes}
    for service in services:
        unknown_networks = set(service["networks"]) - network_ids
        unknown_volumes = {mount["volume"] for mount in service["mounts"]} - volume_ids
        if unknown_networks:
            raise RenderError(f"service {service['id']} references unknown networks: {sorted(unknown_networks)}")
        if unknown_volumes:
            raise RenderError(f"service {service['id']} references unknown volumes: {sorted(unknown_volumes)}")
    packages = sorted((_normalize_package(item) for item in _section_items(data, "packages", "package_plan")), key=lambda item: item["name"])
    files = sorted((_normalize_file(item) for item in _section_items(data, "files", "image_plan")), key=lambda item: item["path"])
    backup = _plain(_pick(data, "backup", "backup_plan", default={}))
    if not isinstance(backup, Mapping):
        raise RenderError("backup plan must be a mapping")
    normalized = {
        "schema_version": "1.0",
        "plan_id": plan_id,
        "profile_id": profile_id,
        "source_digests": sources,
        "services": services,
        "networks": networks,
        "volumes": volumes,
        "packages": packages,
        "files": files,
        "offline": _normalize_offline(_pick(data, "offline", "offline_plan")),
        "backup": _plain(dict(sorted((str(k), v) for k, v in backup.items()))),
    }
    return normalized


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, separators=(",", ": ")) + "\n").encode("utf-8")


def plan_digest(plan: Mapping[str, Any]) -> str:
    return f"sha256:{sha256(canonical_json_bytes(plan)).hexdigest()}"


def semantic_digest(plan: Mapping[str, Any]) -> str:
    semantic = {
        "profile_id": plan["profile_id"],
        "services": plan["services"],
        "networks": plan["networks"],
        "volumes": plan["volumes"],
        "packages": plan["packages"],
        "files": plan["files"],
        "offline": plan["offline"],
        "backup": plan["backup"],
    }
    return f"sha256:{sha256(canonical_json_bytes(semantic)).hexdigest()}"


def generated_metadata(renderer: str, plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "generator": f"koa-assembly/{renderer}@{GENERATOR_VERSION}",
        "authority": "derived_projection",
        "manual_edits": "prohibited",
        "plan_id": plan["plan_id"],
        "profile_id": plan["profile_id"],
        "plan_digest": plan_digest(plan),
        "semantic_digest": semantic_digest(plan),
        "source_digests": plan["source_digests"],
    }


def generated_json(renderer: str, plan: Mapping[str, Any], payload: Mapping[str, Any]) -> bytes:
    if "_koa_generated" in payload:
        raise RenderError("payload may not override _koa_generated")
    return canonical_json_bytes({"_koa_generated": generated_metadata(renderer, plan), **payload})


def generated_header(renderer: str, plan: Mapping[str, Any], comment: str = "#") -> str:
    metadata = generated_metadata(renderer, plan)
    lines = [
        f"{comment} Generated by {metadata['generator']}",
        f"{comment} Authority: derived projection; manual edits are prohibited.",
        f"{comment} Plan-Digest: {metadata['plan_digest']}",
        f"{comment} Semantic-Digest: {metadata['semantic_digest']}",
    ]
    for path, digest in metadata["source_digests"].items():
        lines.append(f"{comment} Source: {path}={digest}")
    return "\n".join(lines) + "\n"


def renderer_manifest(renderer: str, plan: Mapping[str, Any], files: Iterable[RenderedFile]) -> RenderedFile:
    entries = [
        {"path": item.path, "media_type": item.media_type, "mode": f"{item.mode:04o}", "digest": item.digest}
        for item in sorted(files, key=lambda item: item.path)
    ]
    return RenderedFile(
        path=f"{renderer}/manifest.json",
        content=generated_json(renderer, plan, {"format": renderer, "artifacts": entries}),
        media_type="application/json",
    )


def validate_rendered_files(files: Iterable[RenderedFile]) -> tuple[RenderedFile, ...]:
    result = tuple(sorted(files, key=lambda item: item.path))
    paths = [item.path for item in result]
    if len(paths) != len(set(paths)):
        raise RenderError("renderer produced duplicate output paths")
    if not result:
        raise RenderError("renderer produced no output")
    return result


def secret_ref_parts(ref: str) -> tuple[str, str]:
    payload = ref.removeprefix("secret://")
    if "/" not in payload:
        return _identifier(payload, "secret name"), "value"
    name, key = payload.split("/", 1)
    return _identifier(name, "secret name"), _identifier(key, "secret key")


def secret_resource_name(ref: str) -> str:
    """Map a structured secret reference to a target-safe external object name."""

    name, key = secret_ref_parts(ref)
    return _identifier(f"{name}-{key}", "external secret name")


def qualified_name(value: str) -> str:
    """Return a stable kOA resource name without duplicating the prefix."""

    return value if value.startswith("koa-") else f"koa-{value}"


def systemd_quote(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_./:@%+=,-]+", value):
        return value
    return json.dumps(value, ensure_ascii=False)


def render(renderer: str, plan: Any) -> tuple[RenderedFile, ...]:
    """Render one target format by stable renderer identifier."""

    modules = {
        "systemd": ".systemd",
        "quadlet": ".quadlet",
        "compose": ".compose",
        "kubernetes": ".kubernetes",
        "image": ".image",
        "offline_bundle": ".offline_bundle",
    }
    if renderer not in modules:
        raise RenderError(f"unknown renderer: {renderer}")
    from importlib import import_module

    module = import_module(modules[renderer], __name__)
    return module.render(plan)


def render_all(plan: Any) -> dict[str, tuple[RenderedFile, ...]]:
    return {name: render(name, plan) for name in ("systemd", "quadlet", "compose", "kubernetes", "image", "offline_bundle")}


def write_rendered_files(root: Path | str, files: Iterable[RenderedFile]) -> tuple[Path, ...]:
    """Write generated files beneath *root* without permitting path escape."""

    base = Path(root)
    base.mkdir(parents=True, exist_ok=True)
    base_resolved = base.resolve()
    written: list[Path] = []
    for item in validate_rendered_files(files):
        destination = base / PurePosixPath(item.path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        parent_resolved = destination.parent.resolve()
        if parent_resolved != base_resolved and base_resolved not in parent_resolved.parents:
            raise RenderError(f"output escapes render root: {item.path}")
        temporary = destination.with_name(destination.name + ".tmp-koa-render")
        temporary.write_bytes(item.content)
        os.chmod(temporary, item.mode)
        os.replace(temporary, destination)
        written.append(destination)
    return tuple(written)


__all__ = [
    "GENERATOR_VERSION",
    "RenderError",
    "RenderedFile",
    "canonical_json_bytes",
    "generated_header",
    "generated_json",
    "generated_metadata",
    "normalize_plan",
    "plan_digest",
    "qualified_name",
    "render",
    "render_all",
    "renderer_manifest",
    "semantic_digest",
    "secret_ref_parts",
    "secret_resource_name",
    "systemd_quote",
    "validate_rendered_files",
    "write_rendered_files",
]
