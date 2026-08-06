#!/usr/bin/env python3
"""Render deterministic AppArmor profiles from the kOA host LSM policy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_ALLOWED_TOP_LEVEL = {
    "schema_version",
    "policy_id",
    "version",
    "status",
    "profile",
    "default_action",
    "controls",
    "authority",
    "backend",
    "objects",
    "domains",
    "prohibitions",
}
_ALLOWED_OBJECT_CLASSES = {"immutable", "executable", "configuration", "state", "runtime", "host_control"}
_ALLOWED_CAPABILITY_MODES = {"none", "external_bounding_set"}
_SAFE_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_SAFE_PROFILE = re.compile(r"^[a-zA-Z0-9_.-]+$")


class PolicyError(ValueError):
    """Raised when the declarative policy is invalid or unsafe."""


def _load_policy(path: Path) -> dict[str, Any]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError(f"cannot load JSON-compatible YAML policy {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise PolicyError("policy root must be an object")
    unknown = sorted(set(raw) - _ALLOWED_TOP_LEVEL)
    if unknown:
        raise PolicyError(f"unknown top-level fields: {', '.join(unknown)}")
    if raw.get("schema_version") != 1:
        raise PolicyError("unsupported schema_version")
    if raw.get("default_action") != "deny":
        raise PolicyError("default_action must be deny")
    return raw


def _validate_path(pattern: str) -> None:
    if not isinstance(pattern, str) or not pattern.startswith("/"):
        raise PolicyError(f"AppArmor path must be absolute: {pattern!r}")
    if "\x00" in pattern or ".." in Path(pattern).parts:
        raise PolicyError(f"unsafe AppArmor path: {pattern!r}")
    if any(ch in pattern for ch in "\n\r,"):
        raise PolicyError(f"unsupported character in AppArmor path: {pattern!r}")


def _index_objects(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}
    for item in policy.get("objects", []):
        if not isinstance(item, dict):
            raise PolicyError("each object entry must be an object")
        object_id = item.get("id")
        if not isinstance(object_id, str) or not _SAFE_ID.fullmatch(object_id):
            raise PolicyError(f"invalid object id: {object_id!r}")
        if object_id in objects:
            raise PolicyError(f"duplicate object id: {object_id}")
        if item.get("class") not in _ALLOWED_OBJECT_CLASSES:
            raise PolicyError(f"invalid class for {object_id}")
        paths = item.get("apparmor_read")
        if not isinstance(paths, list) or not paths:
            raise PolicyError(f"{object_id}.apparmor_read must be a non-empty list")
        for pattern in paths:
            _validate_path(pattern)
        objects[object_id] = item
    if not objects:
        raise PolicyError("policy defines no objects")
    return objects


def _domain_objects(domain: dict[str, Any], field: str, objects: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    refs = domain.get(field, [])
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        raise PolicyError(f"{domain.get('id')}.{field} must be a list of object ids")
    missing = sorted(set(refs) - set(objects))
    if missing:
        raise PolicyError(f"{domain.get('id')}.{field} references unknown objects: {', '.join(missing)}")
    return [objects[ref] for ref in sorted(set(refs))]


def _render_rule(path: str, permission: str) -> str:
    return f"  {path} {permission},"


def _render_domain(domain: dict[str, Any], objects: dict[str, dict[str, Any]]) -> str:
    domain_id = domain.get("id")
    profile = domain.get("apparmor_profile")
    if not isinstance(domain_id, str) or not _SAFE_ID.fullmatch(domain_id):
        raise PolicyError(f"invalid domain id: {domain_id!r}")
    if not isinstance(profile, str) or not _SAFE_PROFILE.fullmatch(profile):
        raise PolicyError(f"invalid AppArmor profile name for {domain_id}")
    if domain.get("capability_mode") not in _ALLOWED_CAPABILITY_MODES:
        raise PolicyError(f"invalid capability mode for {domain_id}")
    if domain.get("ptrace") is not False or domain.get("arbitrary_exec") is not False:
        raise PolicyError(f"{domain_id} must explicitly deny ptrace and arbitrary execution")
    families = domain.get("network_families")
    if families != ["unix"]:
        raise PolicyError(f"{domain_id} may use only the unix network family")

    read_objects = _domain_objects(domain, "read_objects", objects)
    write_objects = _domain_objects(domain, "write_objects", objects)
    execute_objects = _domain_objects(domain, "execute_objects", objects)
    connect_objects = _domain_objects(domain, "connect_sockets", objects)
    accept_objects = _domain_objects(domain, "accept_sockets", objects)

    read_paths = {path for obj in read_objects for path in obj["apparmor_read"]}
    connect_paths = {path for obj in connect_objects for path in obj["apparmor_read"] if not path.endswith(("/", "/**"))}
    accept_paths = {path for obj in accept_objects for path in obj["apparmor_read"] if path.endswith(".sock")}
    write_paths = {path for obj in write_objects + accept_objects for path in obj["apparmor_read"]}
    execute_paths = {path for obj in execute_objects for path in obj["apparmor_read"]}

    lines = [
        f"profile {profile} flags=(attach_disconnected,mediate_deleted) {{",
        f"  # domain={domain_id}; service_identity={domain.get('service_identity')}",
        "  # Network is local-only. Capability grants remain owned by the separate bounding-set policy.",
        "  unix (create, getattr, getopt, setopt, shutdown),",
        "  deny network inet,",
        "  deny network inet6,",
        "  deny network packet,",
        "  deny network netlink,",
        "  deny ptrace,",
        "  deny /bin/** x,",
        "  deny /sbin/** x,",
        "  deny /usr/bin/** x,",
        "  deny /usr/sbin/** x,",
    ]
    if domain["capability_mode"] == "external_bounding_set":
        lines.append(
            "  # No capability rule is emitted; activation remains blocked until the separate bounded capability profile is composed."
        )

    for path in sorted(read_paths - write_paths - execute_paths):
        mode = "mr" if path.startswith(("/lib/", "/lib64/", "/usr/lib/", "/usr/lib64/")) else "r"
        lines.append(_render_rule(path, mode))
    for path in sorted(connect_paths):
        lines.append(_render_rule(path, "rw"))
        lines.append(f'  unix (connect, send, receive) type=stream peer=(addr="@{path}"),')
    for path in sorted(write_paths - execute_paths):
        lines.append(_render_rule(path, "rwk"))
    for path in sorted(accept_paths):
        lines.append(f'  unix (accept, send, receive, getattr, getopt, setopt, shutdown) type=stream addr="@{path}",')
    for path in sorted(execute_paths):
        lines.append(_render_rule(path, "rix"))

    lines.extend(["}", ""])
    return "\n".join(lines)


def render(policy: dict[str, Any]) -> str:
    objects = _index_objects(policy)
    domains = policy.get("domains")
    if not isinstance(domains, list) or not domains:
        raise PolicyError("policy defines no domains")
    domain_ids: set[str] = set()
    rendered: list[str] = [
        "#include <tunables/global>",
        "",
        f"# Generated from {policy['policy_id']} version {policy['version']}.",
        "# Do not hand-edit generated output; default action is deny.",
        "",
    ]
    for domain in sorted(domains, key=lambda item: str(item.get("id"))):
        domain_id = domain.get("id")
        if domain_id in domain_ids:
            raise PolicyError(f"duplicate domain id: {domain_id}")
        domain_ids.add(domain_id)
        rendered.append(_render_domain(domain, objects))
    return "\n".join(rendered).rstrip() + "\n"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path, help="JSON-compatible YAML policy")
    parser.add_argument("--output", type=Path, help="write output atomically instead of stdout")
    return parser.parse_args(argv)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        content = render(_load_policy(args.policy))
        if args.output:
            _atomic_write(args.output, content)
        else:
            sys.stdout.write(content)
    except PolicyError as exc:
        print(f"render-apparmor: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
