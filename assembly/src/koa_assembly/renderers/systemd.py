"""Render resolved service plans as native systemd units."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping

from . import (
    RenderError,
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
_PROJECTION_FORMAT = "koa.systemd-projection/v1"
_TARGETS = {
    "critical": "koa-critical.target",
    "core": "koa-core.target",
    "background": "koa-background.target",
    "optional": "koa-optional.target",
}
_ALLOWED_UNIT_CLASSES = frozenset({"component", "subsystem"})
_APPLIANCE_PROFILE_SOURCES = frozenset(
    {
        "profiles/implementation-settings/appliance-shell.toml",
        "profiles/overlays/appliance-shell.toml",
    }
)
_ALLOWED_RESTART_POLICIES = frozenset(
    {"no", "on-success", "on-failure", "on-abnormal", "on-watchdog", "on-abort", "always"}
)
_REQUIRED_SANDBOX_KEYS = frozenset(
    {
        "no_new_privileges",
        "private_tmp",
        "private_devices",
        "protect_system",
        "protect_home",
        "protect_kernel_tunables",
        "protect_kernel_modules",
        "protect_kernel_logs",
        "protect_control_groups",
        "protect_clock",
        "protect_hostname",
        "protect_proc",
        "proc_subset",
        "restrict_suid_sgid",
        "restrict_realtime",
        "lock_personality",
        "memory_deny_write_execute",
        "remove_ipc",
        "restrict_namespaces",
        "restrict_address_families",
        "system_call_architectures",
        "system_call_filter",
        "umask",
    }
)
_ALLOWED_PROTECT_SYSTEM = frozenset({"yes", "full", "strict"})
_ALLOWED_PROTECT_HOME = frozenset({"yes", "no", "read-only", "tmpfs"})
_ALLOWED_PROTECT_PROC = frozenset({"default", "noaccess", "invisible", "ptraceable"})
_ALLOWED_PROC_SUBSET = frozenset({"all", "pid"})


def _unit_name(service_id: str) -> str:
    return f"{qualified_name(service_id)}.service"


def _plain_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    if is_dataclass(value) and not isinstance(value, type):
        plain = asdict(value)
        if isinstance(plain, Mapping):
            return plain
    for method_name in ("to_dict", "model_dump", "as_dict"):
        method = getattr(value, method_name, None)
        if callable(method):
            plain = method()
            if isinstance(plain, Mapping):
                return plain
    return {}


def _yes_no(value: Any, field: str) -> str:
    if not isinstance(value, bool):
        raise RenderError(f"systemd projection {field} must be boolean")
    return "yes" if value else "no"


def _non_negative_int(value: Any, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise RenderError(f"systemd projection {field} must be a non-negative integer")
    return value


def _source_reference(value: Any, field: str, source_digests: Mapping[str, str]) -> str:
    if (
        not isinstance(value, str)
        or not value.startswith("profiles/")
        or value not in source_digests
    ):
        raise RenderError(
            f"systemd projection {field} must reference a digested profiles/ authority"
        )
    return value


def _service_policy(value: Any, service_id: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RenderError(f"systemd projection policy for {service_id} must be an object")
    allowed = {"unit_class", "restart", "sandbox"}
    unknown = sorted(set(value) - allowed)
    missing = sorted(allowed - set(value))
    if unknown:
        raise RenderError(
            f"systemd projection policy for {service_id} has unknown keys: "
            + ", ".join(unknown)
        )
    if missing:
        raise RenderError(
            f"systemd projection policy for {service_id} is missing: "
            + ", ".join(missing)
        )

    unit_class = value["unit_class"]
    if unit_class not in _ALLOWED_UNIT_CLASSES:
        raise RenderError(
            f"systemd projection unit_class for {service_id} is unsupported: {unit_class!r}"
        )

    restart = value["restart"]
    if not isinstance(restart, Mapping) or set(restart) != {"policy", "delay_seconds"}:
        raise RenderError(
            f"systemd projection restart policy for {service_id} must contain exactly "
            "policy and delay_seconds"
        )
    restart_policy = restart["policy"]
    if restart_policy not in _ALLOWED_RESTART_POLICIES:
        raise RenderError(
            f"systemd projection restart policy for {service_id} is unsupported: {restart_policy!r}"
        )
    restart_delay = _non_negative_int(
        restart["delay_seconds"], f"restart.delay_seconds for {service_id}"
    )

    sandbox = value["sandbox"]
    if not isinstance(sandbox, Mapping):
        raise RenderError(f"systemd projection sandbox for {service_id} must be an object")
    sandbox_keys = set(sandbox)
    missing_sandbox = sorted(_REQUIRED_SANDBOX_KEYS - sandbox_keys)
    unknown_sandbox = sorted(sandbox_keys - _REQUIRED_SANDBOX_KEYS)
    if missing_sandbox:
        raise RenderError(
            f"systemd projection sandbox for {service_id} is missing: {', '.join(missing_sandbox)}"
        )
    if unknown_sandbox:
        raise RenderError(
            f"systemd projection sandbox for {service_id} has unknown keys: "
            + ", ".join(unknown_sandbox)
        )

    protect_system = sandbox["protect_system"]
    if protect_system not in _ALLOWED_PROTECT_SYSTEM:
        raise RenderError(f"systemd projection protect_system for {service_id} is unsupported")
    protect_home = sandbox["protect_home"]
    if protect_home not in _ALLOWED_PROTECT_HOME:
        raise RenderError(f"systemd projection protect_home for {service_id} is unsupported")
    protect_proc = sandbox["protect_proc"]
    if protect_proc not in _ALLOWED_PROTECT_PROC:
        raise RenderError(f"systemd projection protect_proc for {service_id} is unsupported")
    proc_subset = sandbox["proc_subset"]
    if proc_subset not in _ALLOWED_PROC_SUBSET:
        raise RenderError(f"systemd projection proc_subset for {service_id} is unsupported")
    address_families = sandbox["restrict_address_families"]
    if (
        not isinstance(address_families, list)
        or not address_families
        or any(not isinstance(item, str) or not item.startswith("AF_") for item in address_families)
    ):
        raise RenderError(
            f"systemd projection restrict_address_families for {service_id} must be a "
            "non-empty AF_* list"
        )
    syscall_architectures = sandbox["system_call_architectures"]
    syscall_filter = sandbox["system_call_filter"]
    umask = sandbox["umask"]
    if not isinstance(umask, str) or len(umask) != 4 or not umask.startswith("0") or any(
        character not in "01234567" for character in umask
    ):
        raise RenderError(
            f"systemd projection umask for {service_id} must be a four-digit octal string"
        )
    for field, values in (
        ("system_call_architectures", syscall_architectures),
        ("system_call_filter", syscall_filter),
    ):
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(item, str) or not item or "\n" in item for item in values)
        ):
            raise RenderError(
                f"systemd projection {field} for {service_id} must be a non-empty string list"
            )

    return {
        "unit_class": unit_class,
        "restart": {"policy": restart_policy, "delay_seconds": restart_delay},
        "sandbox": {
            "no_new_privileges": _yes_no(
                sandbox["no_new_privileges"], f"no_new_privileges for {service_id}"
            ),
            "private_tmp": _yes_no(sandbox["private_tmp"], f"private_tmp for {service_id}"),
            "private_devices": _yes_no(
                sandbox["private_devices"], f"private_devices for {service_id}"
            ),
            "protect_system": protect_system,
            "protect_home": protect_home,
            "protect_kernel_tunables": _yes_no(
                sandbox["protect_kernel_tunables"], f"protect_kernel_tunables for {service_id}"
            ),
            "protect_kernel_modules": _yes_no(
                sandbox["protect_kernel_modules"], f"protect_kernel_modules for {service_id}"
            ),
            "protect_kernel_logs": _yes_no(
                sandbox["protect_kernel_logs"], f"protect_kernel_logs for {service_id}"
            ),
            "protect_control_groups": _yes_no(
                sandbox["protect_control_groups"], f"protect_control_groups for {service_id}"
            ),
            "protect_clock": _yes_no(sandbox["protect_clock"], f"protect_clock for {service_id}"),
            "protect_hostname": _yes_no(
                sandbox["protect_hostname"], f"protect_hostname for {service_id}"
            ),
            "protect_proc": protect_proc,
            "proc_subset": proc_subset,
            "restrict_suid_sgid": _yes_no(
                sandbox["restrict_suid_sgid"], f"restrict_suid_sgid for {service_id}"
            ),
            "restrict_realtime": _yes_no(
                sandbox["restrict_realtime"], f"restrict_realtime for {service_id}"
            ),
            "lock_personality": _yes_no(
                sandbox["lock_personality"], f"lock_personality for {service_id}"
            ),
            "memory_deny_write_execute": _yes_no(
                sandbox["memory_deny_write_execute"], f"memory_deny_write_execute for {service_id}"
            ),
            "remove_ipc": _yes_no(sandbox["remove_ipc"], f"remove_ipc for {service_id}"),
            "restrict_namespaces": _yes_no(
                sandbox["restrict_namespaces"], f"restrict_namespaces for {service_id}"
            ),
            "restrict_address_families": sorted(set(address_families)),
            "system_call_architectures": sorted(set(syscall_architectures)),
            "system_call_filter": list(dict.fromkeys(syscall_filter)),
            "umask": umask,
        },
    }


def _projection_policies(
    plan: Any, normalized: Mapping[str, Any]
) -> dict[str, dict[str, Any]] | None:
    raw = _plain_mapping(plan)
    projection = raw.get("systemd_projection")
    source_digests = normalized["source_digests"]
    if projection is None:
        if _APPLIANCE_PROFILE_SOURCES & set(source_digests):
            raise RenderError("appliance profile sources require an explicit systemd_projection")
        return None
    if not isinstance(projection, Mapping):
        raise RenderError("systemd_projection must be an object")
    allowed = {"format", "policy_source", "overlay_source", "services"}
    unknown = sorted(set(projection) - allowed)
    missing = sorted(allowed - set(projection))
    if unknown:
        raise RenderError("systemd_projection has unknown keys: " + ", ".join(unknown))
    if missing:
        raise RenderError("systemd_projection is missing: " + ", ".join(missing))
    if projection["format"] != _PROJECTION_FORMAT:
        raise RenderError(f"unsupported systemd projection format: {projection['format']!r}")

    _source_reference(projection["policy_source"], "policy_source", source_digests)
    _source_reference(projection["overlay_source"], "overlay_source", source_digests)

    services = projection["services"]
    if not isinstance(services, Mapping):
        raise RenderError("systemd_projection.services must be an object")
    enabled_ids = {service["id"] for service in normalized["services"] if service["enabled"]}
    policy_ids = set(services)
    missing_services = sorted(enabled_ids - policy_ids)
    unknown_services = sorted(policy_ids - enabled_ids)
    if missing_services:
        raise RenderError(
            "systemd projection is missing enabled services: " + ", ".join(missing_services)
        )
    if unknown_services:
        raise RenderError(
            "systemd projection references inactive or unknown services: "
            + ", ".join(unknown_services)
        )
    return {
        service_id: _service_policy(services[service_id], service_id)
        for service_id in sorted(services)
    }


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


def _legacy_sandbox(service: Mapping[str, Any]) -> list[str]:
    return [
        "NoNewPrivileges=yes",
        "PrivateTmp=yes",
        f"ProtectHome={'no' if service['kind'] == 'container' else 'yes'}",
        f"ProtectSystem={'full' if service['kind'] == 'container' else 'strict'}",
        "RestrictSUIDSGID=yes",
        "LockPersonality=yes",
        "MemoryDenyWriteExecute=yes",
    ]


def _profile_sandbox(policy: Mapping[str, Any]) -> list[str]:
    sandbox = policy["sandbox"]
    return [
        f"NoNewPrivileges={sandbox['no_new_privileges']}",
        f"PrivateTmp={sandbox['private_tmp']}",
        f"PrivateDevices={sandbox['private_devices']}",
        f"ProtectSystem={sandbox['protect_system']}",
        f"ProtectHome={sandbox['protect_home']}",
        f"ProtectKernelTunables={sandbox['protect_kernel_tunables']}",
        f"ProtectKernelModules={sandbox['protect_kernel_modules']}",
        f"ProtectKernelLogs={sandbox['protect_kernel_logs']}",
        f"ProtectControlGroups={sandbox['protect_control_groups']}",
        f"ProtectClock={sandbox['protect_clock']}",
        f"ProtectHostname={sandbox['protect_hostname']}",
        f"ProtectProc={sandbox['protect_proc']}",
        f"ProcSubset={sandbox['proc_subset']}",
        f"RestrictSUIDSGID={sandbox['restrict_suid_sgid']}",
        f"RestrictRealtime={sandbox['restrict_realtime']}",
        f"LockPersonality={sandbox['lock_personality']}",
        f"MemoryDenyWriteExecute={sandbox['memory_deny_write_execute']}",
        f"RemoveIPC={sandbox['remove_ipc']}",
        f"RestrictNamespaces={sandbox['restrict_namespaces']}",
        "RestrictAddressFamilies=" + " ".join(sandbox["restrict_address_families"]),
        "SystemCallArchitectures=" + " ".join(sandbox["system_call_architectures"]),
        "SystemCallFilter=" + " ".join(sandbox["system_call_filter"]),
        f"UMask={sandbox['umask']}",
    ]


def _render_unit(
    plan: dict[str, Any], service: dict[str, Any], policy: Mapping[str, Any] | None
) -> RenderedFile:
    dependencies = [_unit_name(item) for item in service["dependencies"]]
    after = list(dependencies)
    if service["networks"] or service["ports"]:
        after.append("network-online.target")
    lines = [
        generated_header(_RENDERER, plan).rstrip(),
        "[Unit]",
        f"Description=kOA generated service {service['id']}",
    ]
    if policy is not None:
        lines.append(f"# Template-Class: {policy['unit_class']}")
    if after:
        lines.append("After=" + " ".join(sorted(set(after))))
    if dependencies:
        lines.append("Requires=" + " ".join(sorted(dependencies)))
    lines.extend(["", "[Service]", "Type=simple"])
    lines.extend(_legacy_sandbox(service) if policy is None else _profile_sandbox(policy))
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
    if policy is None:
        lines.extend(["Restart=on-failure", "RestartSec=5s"])
    else:
        lines.append(f"Restart={policy['restart']['policy']}")
        lines.append(f"RestartSec={policy['restart']['delay_seconds']}s")
    resources = service["resources"]
    if policy is not None and "cpu_millis" in resources:
        lines.append(f"CPUQuota={resources['cpu_millis'] / 10:g}%")
    if "memory_bytes" in resources:
        lines.append(f"MemoryMax={resources['memory_bytes']}")
    if "pids" in resources:
        lines.append(f"TasksMax={resources['pids']}")
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
    policies = _projection_policies(plan, normalized)
    files = [
        _render_unit(normalized, service, None if policies is None else policies[service["id"]])
        for service in normalized["services"]
        if service["enabled"]
    ]
    files.append(renderer_manifest(_RENDERER, normalized, files))
    return validate_rendered_files(files)
