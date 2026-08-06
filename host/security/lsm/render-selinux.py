#!/usr/bin/env python3
"""Render deterministic SELinux reference-policy and file-context fragments."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

_SAFE_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_SAFE_TYPE = re.compile(r"^[a-z][a-z0-9_]*_t$")
_ALLOWED_CLASSES = {"immutable", "executable", "configuration", "state", "runtime", "host_control"}


class PolicyError(ValueError):
    """Raised when the declarative policy cannot safely become SELinux policy."""


def _load_policy(path: Path) -> dict[str, Any]:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError(f"cannot load JSON-compatible YAML policy {path}: {exc}") from exc
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        raise PolicyError("unsupported or invalid policy root")
    if policy.get("default_action") != "deny":
        raise PolicyError("default_action must be deny")
    return policy


def _validate_context_regex(value: str) -> None:
    if not isinstance(value, str) or not value.startswith("/"):
        raise PolicyError(f"SELinux file context must start with '/': {value!r}")
    base = value.replace("(/.*)?", "").replace("\\.", ".")
    if "\x00" in value or "\n" in value or "\r" in value or ".." in Path(base).parts:
        raise PolicyError(f"unsafe SELinux file context: {value!r}")


def _index_objects(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for item in policy.get("objects", []):
        if not isinstance(item, dict):
            raise PolicyError("object entries must be mappings")
        object_id = item.get("id")
        selinux_type = item.get("selinux_type")
        if not isinstance(object_id, str) or not _SAFE_ID.fullmatch(object_id):
            raise PolicyError(f"invalid object id: {object_id!r}")
        if object_id in result:
            raise PolicyError(f"duplicate object id: {object_id}")
        if item.get("class") not in _ALLOWED_CLASSES:
            raise PolicyError(f"invalid object class for {object_id}")
        if not isinstance(selinux_type, str) or not _SAFE_TYPE.fullmatch(selinux_type):
            raise PolicyError(f"invalid SELinux type for {object_id}")
        peer = item.get("peer_selinux_type")
        if peer is not None and (not isinstance(peer, str) or not _SAFE_TYPE.fullmatch(peer)):
            raise PolicyError(f"invalid peer SELinux type for {object_id}")
        contexts = item.get("selinux_file_contexts", [])
        if not isinstance(contexts, list):
            raise PolicyError(f"{object_id}.selinux_file_contexts must be a list")
        for context in contexts:
            _validate_context_regex(context)
        if bool(item.get("managed_label")) != bool(contexts):
            raise PolicyError(f"{object_id} managed_label and file-context declaration disagree")
        result[object_id] = item
    if not result:
        raise PolicyError("policy defines no objects")
    return result


def _index_domains(policy: dict[str, Any]) -> list[dict[str, Any]]:
    domains = policy.get("domains")
    if not isinstance(domains, list) or not domains:
        raise PolicyError("policy defines no domains")
    seen: set[str] = set()
    for domain in domains:
        if not isinstance(domain, dict):
            raise PolicyError("domain entries must be mappings")
        domain_id = domain.get("id")
        domain_type = domain.get("selinux_type")
        if not isinstance(domain_id, str) or not _SAFE_ID.fullmatch(domain_id):
            raise PolicyError(f"invalid domain id: {domain_id!r}")
        if domain_id in seen:
            raise PolicyError(f"duplicate domain id: {domain_id}")
        seen.add(domain_id)
        if not isinstance(domain_type, str) or not _SAFE_TYPE.fullmatch(domain_type):
            raise PolicyError(f"invalid domain type for {domain_id}")
        if domain.get("network_families") != ["unix"]:
            raise PolicyError(f"{domain_id} may use only AF_UNIX")
        if domain.get("ptrace") is not False or domain.get("arbitrary_exec") is not False:
            raise PolicyError(f"{domain_id} must deny ptrace and arbitrary execution")
        if domain.get("capability_mode") not in {"none", "external_bounding_set"}:
            raise PolicyError(f"invalid capability mode for {domain_id}")
    return domains


def _object_refs(domain: dict[str, Any], field: str, objects: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    refs = domain.get(field, [])
    if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
        raise PolicyError(f"{domain.get('id')}.{field} must be a list")
    missing = sorted(set(refs) - set(objects))
    if missing:
        raise PolicyError(f"{domain.get('id')}.{field} references unknown objects: {', '.join(missing)}")
    return [objects[ref] for ref in sorted(set(refs))]


def _type_declaration(item: dict[str, Any]) -> list[str]:
    if not item["managed_label"]:
        return []
    object_class = item["class"]
    macro = "files_config_file" if object_class == "configuration" else "files_pid_file" if object_class == "runtime" else "files_type"
    return [f"type {item['selinux_type']};", f"{macro}({item['selinux_type']})"]


def _external_types(objects: dict[str, dict[str, Any]], domains: list[dict[str, Any]]) -> list[str]:
    local = {domain["selinux_type"] for domain in domains}
    local.update(item["selinux_type"] for item in objects.values() if item["managed_label"])
    external = {item["selinux_type"] for item in objects.values() if not item["managed_label"]}
    external.update(item["peer_selinux_type"] for item in objects.values() if item.get("peer_selinux_type"))
    return sorted(external - local)


def _render_domain(domain: dict[str, Any], objects: dict[str, dict[str, Any]]) -> list[str]:
    domain_type = domain["selinux_type"]
    read_objects = _object_refs(domain, "read_objects", objects)
    write_objects = _object_refs(domain, "write_objects", objects)
    execute_objects = _object_refs(domain, "execute_objects", objects)
    connect_objects = _object_refs(domain, "connect_sockets", objects)
    accept_objects = _object_refs(domain, "accept_sockets", objects)

    lines = [
        f"type {domain_type};",
        f"domain_type({domain_type})",
        f"# service_identity={domain.get('service_identity')}; systemd selects this domain explicitly.",
    ]
    for item in read_objects:
        target = item["selinux_type"]
        lines.append(f"read_files_pattern({domain_type}, {target}, {target})")
        if item["class"] == "runtime":
            lines.append(f"allow {domain_type} {target}:sock_file {{ getattr open read }};")
    for item in write_objects:
        target = item["selinux_type"]
        if item["class"] == "host_control":
            lines.append(f"allow {domain_type} {target}:sock_file {{ getattr open read write }};")
        else:
            lines.extend(
                [
                    f"manage_dirs_pattern({domain_type}, {target}, {target})",
                    f"manage_files_pattern({domain_type}, {target}, {target})",
                ]
            )
            if item["class"] == "runtime":
                lines.append(f"manage_sock_files_pattern({domain_type}, {target}, {target})")
    for item in execute_objects:
        lines.append(f"can_exec({domain_type}, {item['selinux_type']})")
    for item in connect_objects:
        target = item["selinux_type"]
        peer = item.get("peer_selinux_type")
        if not peer:
            raise PolicyError(f"socket object {item['id']} has no peer_selinux_type")
        lines.append(f"allow {domain_type} {target}:sock_file {{ getattr open read write }};")
        lines.append(f"allow {domain_type} {peer}:unix_stream_socket connectto;")
    for item in accept_objects:
        target = item["selinux_type"]
        lines.append(f"allow {domain_type} {target}:sock_file {{ getattr open read write }};")
        lines.append(
            f"allow {domain_type} self:unix_stream_socket "
            "{ accept read write getattr getopt setopt shutdown };"
        )
    if domain["capability_mode"] == "external_bounding_set":
        lines.extend(
            [
                "# Capability permissions are intentionally absent here.",
                "# Compose them from host/security/capabilities/ and the active operation catalog.",
            ]
        )
    lines.append("")
    return lines


def render(policy: dict[str, Any]) -> tuple[str, str]:
    objects = _index_objects(policy)
    domains = _index_domains(policy)
    module_name = policy.get("backend", {}).get("selinux_module_name")
    module_version = policy.get("backend", {}).get("selinux_module_version")
    if not isinstance(module_name, str) or not _SAFE_ID.fullmatch(module_name):
        raise PolicyError("invalid SELinux module name")
    if not isinstance(module_version, str) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){1,2}", module_version):
        raise PolicyError("invalid SELinux module version")

    te: list[str] = [
        f"policy_module({module_name}, {module_version})",
        "",
        "# Generated default-deny fragment. No domain is inferred from UID or path.",
        "# Capability permissions remain a separate policy authority.",
        "",
    ]
    external = _external_types(objects, domains)
    if external:
        te.extend(["gen_require(`"] + [f"    type {item};" for item in external] + ["')", ""])
    for item in sorted(objects.values(), key=lambda value: value["id"]):
        te.extend(_type_declaration(item))
    te.append("")
    for domain in sorted(domains, key=lambda value: value["id"]):
        te.extend(_render_domain(domain, objects))

    contexts = [
        f"# Generated file contexts for {policy['policy_id']} {policy['version']}.",
        "# Apply only after package ownership and path validation.",
    ]
    for item in sorted(objects.values(), key=lambda value: value["id"]):
        for context in sorted(item["selinux_file_contexts"]):
            contexts.append(f"{context}    gen_context(system_u:object_r:{item['selinux_type']},s0)")
    return "\n".join(te).rstrip() + "\n", "\n".join(contexts).rstrip() + "\n"


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("policy", type=Path, help="JSON-compatible YAML policy")
    parser.add_argument("--te-output", type=Path, help="write the reference-policy TE fragment")
    parser.add_argument("--file-contexts-output", type=Path, help="write file-context mappings")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    if bool(args.te_output) != bool(args.file_contexts_output):
        print("render-selinux: both output paths are required together", file=sys.stderr)
        return 2
    try:
        te, contexts = render(_load_policy(args.policy))
        if args.te_output:
            _atomic_write(args.te_output, te)
            _atomic_write(args.file_contexts_output, contexts)
        else:
            sys.stdout.write(te)
            sys.stdout.write("\n# ----- file_contexts -----\n")
            sys.stdout.write(contexts)
    except PolicyError as exc:
        print(f"render-selinux: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
