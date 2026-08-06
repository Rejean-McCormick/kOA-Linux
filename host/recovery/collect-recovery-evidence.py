#!/usr/bin/env python3
"""Collect minimized, attributable evidence for one host recovery session."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import sys
import tomllib
from typing import Any, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from host.adapters.filesystem import FilesystemAdapterError, SafeFilesystem  # noqa: E402
from host.adapters.network import NetworkAdapter, NetworkAdapterError  # noqa: E402
from host.adapters.podman import PodmanAdapter, PodmanAdapterError  # noqa: E402
from host.adapters.storage import StorageAdapter, StorageAdapterError  # noqa: E402
from host.adapters.systemd import SystemdAdapter, SystemdAdapterError  # noqa: E402


class EvidenceCollectionError(RuntimeError):
    """Raised when required recovery evidence cannot be collected safely."""


_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+/-]{2,255}$")
_REDACTED_KEYS = {
    "secret",
    "secrets",
    "password",
    "passphrase",
    "token",
    "access_token",
    "refresh_token",
    "private_key",
    "credential",
    "credentials",
    "authorization",
    "cookie",
}


def _identifier(value: str, field: str) -> str:
    if not _IDENTIFIER.fullmatch(value) or ".." in value:
        raise EvidenceCollectionError(f"invalid identifier in {field}")
    return value


def _canonical_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sanitize(value: Any, *, key: str | None = None) -> Any:
    if key is not None and key.lower() in _REDACTED_KEYS:
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(item_key): _sanitize(item_value, key=str(item_key)) for item_key, item_value in sorted(value.items())}
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, str) and len(value) > 4096:
        return value[:4096] + "...[TRUNCATED]"
    return value


class EvidencePolicy:
    def __init__(self, path: Path) -> None:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise EvidenceCollectionError(f"unable to load recovery policy: {path}") from exc
        runtime = data.get("runtime")
        containment = data.get("containment")
        if not isinstance(runtime, dict) or not isinstance(containment, dict):
            raise EvidenceCollectionError("recovery policy lacks runtime or containment sections")
        try:
            self.policy_id = _identifier(str(data["policy_id"]), "policy_id")
            self.profile_id = _identifier(str(data["profile_id"]), "profile_id")
            self.state_root = Path(runtime["state_root"])
            self.evidence_root = Path(runtime["evidence_root"])
            self.max_file_bytes = int(runtime["max_evidence_file_bytes"])
            self.max_plan_bytes = int(runtime["max_plan_bytes"])
            self.allowed_units = tuple(str(value) for value in containment["allowed_systemd_units"])
            self.allowed_containers = tuple(str(value) for value in containment["allowed_containers"])
            self.allowed_interfaces = tuple(str(value) for value in containment["allowed_interfaces"])
            self.allowed_storage_sources = tuple(str(value) for value in containment["allowed_storage_sources"])
            self.allowed_storage_targets = tuple(str(value) for value in containment["allowed_storage_targets"])
        except (KeyError, TypeError, ValueError) as exc:
            raise EvidenceCollectionError("recovery policy contains invalid evidence values") from exc
        if not self.state_root.is_absolute() or not self.evidence_root.is_absolute():
            raise EvidenceCollectionError("evidence roots must be absolute")
        if self.max_file_bytes <= 0 or self.max_plan_bytes <= 0:
            raise EvidenceCollectionError("evidence size limits must be positive")
        self.policy_digest = hashlib.sha256(path.read_bytes()).hexdigest()


def _read_os_release() -> dict[str, str]:
    permitted = {"ID", "ID_LIKE", "NAME", "VERSION", "VERSION_ID", "VARIANT_ID"}
    result: dict[str, str] = {}
    path = Path("/etc/os-release")
    if not path.is_file() or path.is_symlink():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line:
            continue
        key, raw = line.split("=", 1)
        if key in permitted:
            result[key] = raw.strip().strip('"')[:256]
    return result


def _collect_session_files(policy: EvidencePolicy, recovery_id: str) -> list[dict[str, Any]]:
    root = policy.state_root / recovery_id
    if not root.exists() or not root.is_dir() or root.is_symlink():
        raise EvidenceCollectionError(f"recovery session does not exist: {recovery_id}")
    authority_root = policy.state_root.resolve(strict=False)
    try:
        root.resolve(strict=False).relative_to(authority_root)
    except ValueError as exc:
        raise EvidenceCollectionError("recovery session path escapes state root") from exc
    records: list[dict[str, Any]] = []
    for index, path in enumerate(sorted(root.rglob("*"))):
        if index >= 1000:
            raise EvidenceCollectionError("recovery session contains too many evidence candidates")
        relative = path.relative_to(policy.state_root).as_posix()
        if path.is_symlink():
            records.append({"path": relative, "status": "rejected_symlink"})
            continue
        if not path.is_file():
            continue
        info = path.stat()
        record: dict[str, Any] = {
            "path": relative,
            "size": info.st_size,
            "mode": oct(info.st_mode & 0o777),
            "modified_ns": info.st_mtime_ns,
        }
        if info.st_size > policy.max_file_bytes:
            record["status"] = "metadata_only_size_limit"
            records.append(record)
            continue
        content = path.read_bytes()
        record["sha256"] = hashlib.sha256(content).hexdigest()
        if path.suffix == ".json":
            try:
                parsed = json.loads(content.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                record["status"] = "invalid_json"
            else:
                record["status"] = "captured_minimized"
                record["content"] = _sanitize(parsed)
        else:
            record["status"] = "metadata_only_non_json"
        records.append(record)
    return records


def _collect_host_observations(policy: EvidencePolicy) -> dict[str, Any]:
    observations: dict[str, Any] = {
        "platform": {
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "kernel_release": platform.release(),
            "os_release": _read_os_release(),
        },
        "systemd": [],
        "containers": [],
        "network_links": [],
        "storage_mounts": [],
    }
    if policy.allowed_units:
        adapter = SystemdAdapter(policy.allowed_units)
        for unit in policy.allowed_units:
            try:
                state = adapter.inspect(unit)
                observations["systemd"].append(
                    {
                        "unit": state.unit,
                        "load_state": state.load_state,
                        "active_state": state.active_state,
                        "sub_state": state.sub_state,
                        "result": state.result,
                        "exec_main_status": state.exec_main_status,
                    }
                )
            except (SystemdAdapterError, OSError) as exc:
                observations["systemd"].append({"unit": unit, "status": "unavailable", "error": str(exc)[:300]})
    if policy.allowed_containers:
        adapter = PodmanAdapter(policy.allowed_containers)
        for name in policy.allowed_containers:
            try:
                state = adapter.inspect(name)
                observations["containers"].append(
                    {
                        "name": state.name,
                        "container_id": state.container_id,
                        "status": state.status,
                        "running": state.running,
                        "paused": state.paused,
                        "exit_code": state.exit_code,
                        "image_digest": state.image_digest,
                    }
                )
            except (PodmanAdapterError, OSError) as exc:
                observations["containers"].append({"name": name, "status": "unavailable", "error": str(exc)[:300]})
    if policy.allowed_interfaces:
        adapter = NetworkAdapter(policy.allowed_interfaces)
        for interface in policy.allowed_interfaces:
            try:
                state = adapter.inspect(interface)
                observations["network_links"].append(
                    {
                        "interface": state.interface,
                        "index": state.index,
                        "operational_state": state.operational_state,
                        "flags": list(state.flags),
                        "mtu": state.mtu,
                    }
                )
            except (NetworkAdapterError, OSError) as exc:
                observations["network_links"].append(
                    {"interface": interface, "status": "unavailable", "error": str(exc)[:300]}
                )
    if policy.allowed_storage_targets:
        adapter = StorageAdapter(policy.allowed_storage_sources, policy.allowed_storage_targets)
        for target in policy.allowed_storage_targets:
            try:
                state = adapter.inspect(target)
                if state is None:
                    observations["storage_mounts"].append({"target": target, "status": "not_mounted"})
                else:
                    observations["storage_mounts"].append(
                        {
                            "source": state.source,
                            "target": state.target,
                            "filesystem_type": state.filesystem_type,
                            "options": list(state.options),
                            "read_only": state.read_only,
                        }
                    )
            except (StorageAdapterError, OSError) as exc:
                observations["storage_mounts"].append(
                    {"target": target, "status": "unavailable", "error": str(exc)[:300]}
                )
    return observations


def collect_recovery_evidence(
    recovery_id: str,
    *,
    policy: EvidencePolicy,
    recorded_at: datetime | None = None,
    persist: bool = True,
) -> dict[str, Any]:
    admitted_id = _identifier(recovery_id, "recovery_id")
    timestamp = (recorded_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    files = _collect_session_files(policy, admitted_id)
    payload: dict[str, Any] = {
        "schema_version": "1.0.0",
        "artifact_class": "recovery_evidence",
        "evidence_id": f"recovery-evidence:{admitted_id}:{timestamp.strftime('%Y%m%dT%H%M%SZ')}",
        "recovery_id": admitted_id,
        "profile_id": policy.profile_id,
        "policy_id": policy.policy_id,
        "policy_sha256": policy.policy_digest,
        "recorded_at": timestamp.isoformat().replace("+00:00", "Z"),
        "disclosure_class": "restricted",
        "retention_class": "incident_lifetime",
        "authority": "non_authoritative_evidence",
        "session_files": files,
        "host_observations": _collect_host_observations(policy),
        "redaction": {
            "applied": True,
            "prohibited_content": [
                "private_keys",
                "passwords",
                "tokens",
                "unrestricted_application_payloads",
                "environment_variables",
                "process_command_lines",
            ],
        },
    }
    payload["evidence_sha256"] = _canonical_digest(payload)
    if persist:
        evidence_fs = SafeFilesystem(policy.evidence_root, create=True)
        evidence_fs.ensure_directory(admitted_id)
        file_name = f"{admitted_id}/{timestamp.strftime('%Y%m%dT%H%M%SZ')}.json"
        evidence_fs.atomic_write_json(file_name, payload, overwrite=False)
        payload["stored_at"] = str(policy.evidence_root / file_name)
    return payload


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--recovery-id", required=True)
    parser.add_argument("--dry-run", action="store_true", help="Collect and print evidence without persisting it")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        policy = EvidencePolicy(args.policy)
        evidence = collect_recovery_evidence(args.recovery_id, policy=policy, persist=not args.dry_run)
    except (EvidenceCollectionError, FilesystemAdapterError, OSError) as exc:
        print(f"recovery evidence collection failed: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(evidence, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
