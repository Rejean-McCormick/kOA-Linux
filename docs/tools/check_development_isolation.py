#!/usr/bin/env python3
"""Validate kOA development-workspace isolation.

This tool checks the development-isolation model selected by DEC-DEV-001,
DEC-DEV-002, LOCK-DEV-001 through LOCK-DEV-005, the Python UV toolchain
contract, and the active volumes-and-persistent-data documentation.

The default checks are static and use only the Python standard library.  They
validate one or more ``.koa/workspace.json`` manifests and the local filesystem
state they declare.  Optional execution checks can also verify Git worktree
registration, frozen UV resolution, the active Python prefix, and rootless
Docker Compose project ownership.

The checker does not create, repair, migrate, delete, or activate workspace
state.  Missing authority or ambiguous ownership is reported as a failure
rather than repaired by inference.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import socket
import stat
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence

TOOL_VERSION = "1.0.0"
MANIFEST_SCHEMA_VERSION = "1.0.0"
DEFAULT_MANIFEST_RELATIVE_PATH = Path(".koa/workspace.json")

SUPPORTED_PROFILES = {
    "developer_linux_workstation",
    "developer_windows_wsl",
    "build_farm",
}
SUPPORTED_TOOLCHAINS = {
    "python_uv",
}
SUPPORTED_PORT_KEYS = (
    "application",
    "api",
    "database",
    "queue",
    "search",
    "metrics",
    "debug",
    "test",
)
REQUIRED_PATH_KEYS = (
    "python_environment",
    "runtime",
    "logs",
    "temporary",
    "secrets",
    "data",
    "artifacts",
    "backups",
    "restore",
)
OPTIONAL_PATH_KEYS = (
    "uploads",
    "queue",
    "search",
    "object_store",
    "sockets",
    "certificates",
    "build_outputs",
    "test_artifacts",
)
ALLOWED_SHARED_RESOURCE_KEYS = {
    "uv_cache",
}
FORBIDDEN_ENVIRONMENT_VARIABLES = {
    "PYTHONPATH",
    "PIP_INDEX_URL",
    "PIP_EXTRA_INDEX_URL",
}
SECRET_NAME_MARKERS = (
    "API_KEY",
    "BEARER",
    "CREDENTIAL",
    "PASSWORD",
    "PRIVATE_KEY",
    "SECRET",
    "TOKEN",
)
SECRET_REFERENCE_SUFFIXES = (
    "_FILE",
    "_PATH",
    "_REF",
)
SECRET_POLICY_SUFFIXES = (
    "_CLASS",
    "_CLASSIFICATION",
    "_KIND",
    "_MODE",
    "_POLICY",
    "_STATUS",
    "_TYPE",
)
ALLOWED_TOP_LEVEL_KEYS = {
    "schema_version",
    "workspace_id",
    "profile_ids",
    "toolchain_id",
    "primary_worktree",
    "worktree_root",
    "worktrees_root",
    "branch",
    "start_ref",
    "compose_project_name",
    "database_name",
    "database_user",
    "port_base",
    "ports",
    "paths",
    "shared_resources",
    "mutable_sharing",
    "storage_resources",
    "services",
    "extensions",
}
EMBEDDED_CREDENTIAL_URI = re.compile(
    r"^[A-Za-z][A-Za-z0-9+.-]*://[^/\s:@]+:[^@\s]+@"
)
PRIVATE_KEY_MARKER = "-----BEGIN PRIVATE KEY-----"
STORAGE_CLASSES = {
    "authoritative_component_data",
    "durable_service_state",
    "build_output",
    "non_authoritative_cache",
    "log_and_diagnostic",
    "temporary",
    "backup",
    "restore_staging",
    "test_fixture",
    "export",
}
PROHIBITED_SHARED_STORAGE_CLASSES = {
    "authoritative_component_data",
    "durable_service_state",
    "build_output",
    "log_and_diagnostic",
    "temporary",
    "backup",
    "restore_staging",
    "export",
}
READ_ONLY_SHAREABLE_STORAGE_CLASSES = {
    "non_authoritative_cache",
    "test_fixture",
}
MUTABLE_SHARING_VALUES = {
    "prohibited",
}
WORKSPACE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,127}$")
NAMESPACE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]{1,127}$")
BRANCH_PATTERN = re.compile(r"^[^\x00-\x20~^:?*\\[]+$")
RESOURCE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.:-]{1,127}$")
PORT_MIN = 1024
PORT_MAX = 65535

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
EXIT_INTERNAL = 3


@dataclass(frozen=True)
class Issue:
    """One stable diagnostic."""

    path: str
    code: str
    message: str
    severity: str = "error"
    workspace_id: str = ""
    field: str = ""
    value: str = ""


@dataclass
class Counters:
    """Execution summary."""

    discovered_manifests: int = 0
    checked_workspaces: int = 0
    checked_environment_files: int = 0
    checked_storage_resources: int = 0
    checked_services: int = 0
    git_checks: int = 0
    uv_checks: int = 0
    python_prefix_checks: int = 0
    docker_checks: int = 0
    listener_checks: int = 0


@dataclass
class Workspace:
    """Normalized workspace declaration."""

    manifest_path: Path
    raw: dict[str, Any]
    workspace_id: str
    profile_ids: tuple[str, ...]
    toolchain_id: str
    primary_worktree: Path | None
    worktree_root: Path
    worktrees_root: Path | None
    branch: str
    compose_project_name: str
    database_name: str
    database_user: str
    port_base: int
    ports: dict[str, int]
    paths: dict[str, Path]
    shared_resources: dict[str, Path]
    mutable_sharing: str
    environment: dict[str, str] = field(default_factory=dict)
    compose_environment: dict[str, str] = field(default_factory=dict)
    storage_resources: list[dict[str, Any]] = field(default_factory=list)
    services: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class ClaimedPath:
    """One path whose ownership must not overlap another workspace."""

    workspace_id: str
    manifest_path: Path
    field: str
    path: Path
    storage_class: str = ""


@dataclass(frozen=True)
class ClaimedPort:
    """One host port claimed by a workspace."""

    workspace_id: str
    manifest_path: Path
    field: str
    port: int


@dataclass(frozen=True)
class ClaimedName:
    """One globally collision-sensitive namespace."""

    workspace_id: str
    manifest_path: Path
    field: str
    value: str


class CheckError(RuntimeError):
    """Expected execution-check failure."""


def tool_root() -> Path:
    """Return the documentation root containing this tool."""

    return Path(__file__).resolve().parents[1]


def normalize_path(path: Path, display_root: Path) -> str:
    """Return a stable display path."""

    try:
        return path.resolve(strict=False).relative_to(
            display_root.resolve(strict=False)
        ).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def issue(
    display_root: Path,
    path: Path,
    code: str,
    message: str,
    *,
    workspace_id: str = "",
    field: str = "",
    value: Any = "",
    severity: str = "error",
) -> Issue:
    """Create one normalized issue."""

    return Issue(
        path=normalize_path(path, display_root),
        code=code,
        message=message,
        severity=severity,
        workspace_id=workspace_id,
        field=field,
        value="" if value is None else str(value),
    )


def load_json(path: Path) -> dict[str, Any]:
    """Load one JSON object."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        raise CheckError(f"{path}: invalid UTF-8: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CheckError(
            f"{path}:{exc.lineno}:{exc.colno}: invalid JSON: {exc.msg}"
        ) from exc
    except OSError as exc:
        raise CheckError(f"{path}: cannot read file: {exc}") from exc

    if not isinstance(value, dict):
        raise CheckError(f"{path}: manifest root must be a JSON object")
    return value


def declared_path_lexical(
    value: Any,
    *,
    manifest_path: Path,
    field_name: str,
) -> Path:
    """Return an absolute path without resolving symbolic links."""

    if not isinstance(value, str) or not value:
        raise CheckError(
            f"{manifest_path}: {field_name} must be a non-empty string path"
        )

    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = manifest_path.parent.parent / candidate
    return Path(os.path.abspath(candidate))


def resolve_declared_path(
    value: Any,
    *,
    manifest_path: Path,
    field_name: str,
) -> Path:
    """Resolve an absolute or worktree-relative path safely."""

    return declared_path_lexical(
        value,
        manifest_path=manifest_path,
        field_name=field_name,
    ).resolve(strict=False)


def path_has_symlink_component(path: Path) -> bool:
    """Return whether an existing path component is a symbolic link."""

    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        if current.is_symlink():
            return True
    return False


def string_field(
    data: Mapping[str, Any],
    key: str,
    manifest_path: Path,
    *,
    pattern: re.Pattern[str] | None = None,
    allow_empty: bool = False,
) -> str:
    """Read and validate a string field."""

    value = data.get(key)
    if not isinstance(value, str):
        raise CheckError(f"{manifest_path}: {key} must be a string")
    if not allow_empty and not value:
        raise CheckError(f"{manifest_path}: {key} cannot be empty")
    if pattern is not None and value and not pattern.fullmatch(value):
        raise CheckError(
            f"{manifest_path}: {key} has unsupported value {value!r}"
        )
    return value


def integer_field(
    data: Mapping[str, Any],
    key: str,
    manifest_path: Path,
) -> int:
    """Read an integer without accepting booleans."""

    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise CheckError(f"{manifest_path}: {key} must be an integer")
    return value


def string_list_field(
    data: Mapping[str, Any],
    key: str,
    manifest_path: Path,
) -> tuple[str, ...]:
    """Read a unique, non-empty string list."""

    value = data.get(key)
    if (
        not isinstance(value, list)
        or not value
        or not all(isinstance(item, str) and item for item in value)
    ):
        raise CheckError(
            f"{manifest_path}: {key} must be a non-empty string array"
        )
    if len(value) != len(set(value)):
        raise CheckError(f"{manifest_path}: {key} contains duplicates")
    return tuple(value)


def optional_path_field(
    data: Mapping[str, Any],
    key: str,
    manifest_path: Path,
) -> Path | None:
    """Resolve an optional path field."""

    value = data.get(key)
    if value is None:
        return None
    return resolve_declared_path(
        value,
        manifest_path=manifest_path,
        field_name=key,
    )


def parse_path_map(
    data: Mapping[str, Any],
    manifest_path: Path,
) -> dict[str, Path]:
    """Parse required and optional workspace paths."""

    value = data.get("paths")
    if not isinstance(value, dict):
        raise CheckError(f"{manifest_path}: paths must be an object")

    missing = set(REQUIRED_PATH_KEYS) - set(value)
    if missing:
        raise CheckError(
            f"{manifest_path}: paths is missing keys {sorted(missing)}"
        )

    allowed = set(REQUIRED_PATH_KEYS) | set(OPTIONAL_PATH_KEYS)
    extra = set(value) - allowed
    if extra:
        raise CheckError(
            f"{manifest_path}: paths has unsupported keys {sorted(extra)}"
        )

    result: dict[str, Path] = {}
    for key, raw_path in value.items():
        result[key] = resolve_declared_path(
            raw_path,
            manifest_path=manifest_path,
            field_name=f"paths.{key}",
        )
    return result


def parse_ports(
    data: Mapping[str, Any],
    manifest_path: Path,
    port_base: int,
) -> dict[str, int]:
    """Parse the eight-port workspace block."""

    value = data.get("ports")
    if not isinstance(value, dict):
        raise CheckError(f"{manifest_path}: ports must be an object")

    if set(value) != set(SUPPORTED_PORT_KEYS):
        raise CheckError(
            f"{manifest_path}: ports must contain exactly "
            f"{list(SUPPORTED_PORT_KEYS)}"
        )

    result: dict[str, int] = {}
    for offset, key in enumerate(SUPPORTED_PORT_KEYS):
        port = value.get(key)
        if isinstance(port, bool) or not isinstance(port, int):
            raise CheckError(
                f"{manifest_path}: ports.{key} must be an integer"
            )
        if port != port_base + offset:
            raise CheckError(
                f"{manifest_path}: ports.{key} must equal "
                f"port_base + {offset}"
            )
        if not PORT_MIN <= port <= PORT_MAX:
            raise CheckError(
                f"{manifest_path}: ports.{key} is outside "
                f"{PORT_MIN}-{PORT_MAX}"
            )
        result[key] = port

    if len(set(result.values())) != len(result):
        raise CheckError(f"{manifest_path}: workspace ports are duplicated")

    return result


def parse_shared_resources(
    data: Mapping[str, Any],
    manifest_path: Path,
) -> dict[str, Path]:
    """Parse explicitly shareable non-authoritative resources."""

    value = data.get("shared_resources")
    if not isinstance(value, dict):
        raise CheckError(
            f"{manifest_path}: shared_resources must be an object"
        )

    extra = set(value) - ALLOWED_SHARED_RESOURCE_KEYS
    if extra:
        raise CheckError(
            f"{manifest_path}: unsupported shared resource keys "
            f"{sorted(extra)}"
        )

    result: dict[str, Path] = {}
    for key, raw_path in value.items():
        result[key] = resolve_declared_path(
            raw_path,
            manifest_path=manifest_path,
            field_name=f"shared_resources.{key}",
        )
    return result


def parse_optional_object_list(
    data: Mapping[str, Any],
    key: str,
    manifest_path: Path,
) -> list[dict[str, Any]]:
    """Read an optional array of objects."""

    value = data.get(key, [])
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise CheckError(
            f"{manifest_path}: {key} must be an array of objects"
        )
    return [dict(item) for item in value]


def parse_workspace(manifest_path: Path) -> Workspace:
    """Parse and normalize one workspace manifest."""

    raw = load_json(manifest_path)

    unsupported_keys = set(raw) - ALLOWED_TOP_LEVEL_KEYS
    if unsupported_keys:
        raise CheckError(
            f"{manifest_path}: unsupported top-level keys "
            f"{sorted(unsupported_keys)}"
        )

    schema_version = string_field(
        raw,
        "schema_version",
        manifest_path,
    )
    if schema_version != MANIFEST_SCHEMA_VERSION:
        raise CheckError(
            f"{manifest_path}: schema_version must be "
            f"{MANIFEST_SCHEMA_VERSION}"
        )

    workspace_id = string_field(
        raw,
        "workspace_id",
        manifest_path,
        pattern=WORKSPACE_ID_PATTERN,
    )
    profile_ids = string_list_field(
        raw,
        "profile_ids",
        manifest_path,
    )
    toolchain_id = string_field(
        raw,
        "toolchain_id",
        manifest_path,
        pattern=RESOURCE_ID_PATTERN,
    )
    primary_worktree = optional_path_field(
        raw,
        "primary_worktree",
        manifest_path,
    )
    worktree_root = resolve_declared_path(
        raw.get("worktree_root"),
        manifest_path=manifest_path,
        field_name="worktree_root",
    )
    worktrees_root = optional_path_field(
        raw,
        "worktrees_root",
        manifest_path,
    )
    branch = string_field(
        raw,
        "branch",
        manifest_path,
        pattern=BRANCH_PATTERN,
    )
    compose_project_name = string_field(
        raw,
        "compose_project_name",
        manifest_path,
        pattern=NAMESPACE_PATTERN,
    )
    database_name = string_field(
        raw,
        "database_name",
        manifest_path,
        pattern=NAMESPACE_PATTERN,
    )
    database_user = string_field(
        raw,
        "database_user",
        manifest_path,
        pattern=NAMESPACE_PATTERN,
    )
    port_base = integer_field(
        raw,
        "port_base",
        manifest_path,
    )
    if not PORT_MIN <= port_base <= PORT_MAX - len(SUPPORTED_PORT_KEYS) + 1:
        raise CheckError(
            f"{manifest_path}: port_base cannot provide a complete "
            f"{len(SUPPORTED_PORT_KEYS)}-port block"
        )

    ports = parse_ports(raw, manifest_path, port_base)
    paths = parse_path_map(raw, manifest_path)
    shared_resources = parse_shared_resources(raw, manifest_path)
    mutable_sharing = string_field(
        raw,
        "mutable_sharing",
        manifest_path,
    )
    storage_resources = parse_optional_object_list(
        raw,
        "storage_resources",
        manifest_path,
    )
    services = parse_optional_object_list(
        raw,
        "services",
        manifest_path,
    )

    return Workspace(
        manifest_path=manifest_path.resolve(strict=False),
        raw=raw,
        workspace_id=workspace_id,
        profile_ids=profile_ids,
        toolchain_id=toolchain_id,
        primary_worktree=primary_worktree,
        worktree_root=worktree_root,
        worktrees_root=worktrees_root,
        branch=branch,
        compose_project_name=compose_project_name,
        database_name=database_name,
        database_user=database_user,
        port_base=port_base,
        ports=ports,
        paths=paths,
        shared_resources=shared_resources,
        mutable_sharing=mutable_sharing,
        storage_resources=storage_resources,
        services=services,
    )


def is_relative_to(path: Path, parent: Path) -> bool:
    """Compatibility helper for path ancestry."""

    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def paths_overlap(first: Path, second: Path) -> bool:
    """Return whether either normalized path contains the other."""

    first_normalized = first.resolve(strict=False)
    second_normalized = second.resolve(strict=False)
    return (
        first_normalized == second_normalized
        or is_relative_to(first_normalized, second_normalized)
        or is_relative_to(second_normalized, first_normalized)
    )


def same_file_if_present(first: Path, second: Path) -> bool:
    """Return whether existing paths resolve to the same filesystem object."""

    try:
        return first.exists() and second.exists() and first.samefile(second)
    except OSError:
        return False


def mode_bits(path: Path) -> int | None:
    """Return permission bits for an existing path."""

    try:
        return stat.S_IMODE(path.stat().st_mode)
    except OSError:
        return None


def parse_shell_environment(path: Path) -> dict[str, str]:
    """Parse the restricted KEY=VALUE or export KEY=VALUE environment format."""

    values: dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise CheckError(f"{path}: cannot read environment file: {exc}") from exc

    for line_number, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("export "):
            stripped = stripped[7:].lstrip()

        if "=" not in stripped:
            raise CheckError(
                f"{path}:{line_number}: expected KEY=VALUE"
            )

        name, raw_value = stripped.split("=", 1)
        name = name.strip()
        if not re.fullmatch(r"[A-Z_][A-Z0-9_]*", name):
            raise CheckError(
                f"{path}:{line_number}: invalid environment variable "
                f"name {name!r}"
            )
        if name in values:
            raise CheckError(
                f"{path}:{line_number}: duplicate variable {name}"
            )

        try:
            tokens = shlex.split(raw_value, posix=True)
        except ValueError as exc:
            raise CheckError(
                f"{path}:{line_number}: invalid shell quoting: {exc}"
            ) from exc

        if not tokens:
            value = ""
        elif len(tokens) == 1:
            value = tokens[0]
        else:
            raise CheckError(
                f"{path}:{line_number}: shell expansion or multiple tokens "
                "are not permitted"
            )

        values[name] = value

    return values


def value_is_secret(variable_name: str) -> bool:
    """Return whether a variable appears to contain a secret value."""

    upper_name = variable_name.upper()
    if upper_name.endswith(SECRET_REFERENCE_SUFFIXES):
        return False
    if upper_name.endswith(SECRET_POLICY_SUFFIXES):
        return False
    return any(marker in upper_name for marker in SECRET_NAME_MARKERS)


def contains_embedded_credential(value: str) -> bool:
    """Return whether a string embeds a credential or private key."""

    return bool(EMBEDDED_CREDENTIAL_URI.search(value)) or (
        PRIVATE_KEY_MARKER in value
    )


def manifest_secret_issues(
    value: Any,
    *,
    workspace: Workspace,
    display_root: Path,
    parts: tuple[str, ...] = (),
) -> list[Issue]:
    """Reject inline secrets and credential-bearing URLs in a manifest."""

    issues: list[Issue] = []

    if isinstance(value, dict):
        for key, child in value.items():
            child_parts = (*parts, str(key))
            upper_key = str(key).upper()
            is_reference = upper_key.endswith(SECRET_REFERENCE_SUFFIXES)
            is_policy = upper_key.endswith(SECRET_POLICY_SUFFIXES)
            path_like_secret_container = str(key) in {
                "secrets",
                "secret_refs",
            }

            if isinstance(child, str):
                if contains_embedded_credential(child):
                    issues.append(
                        issue(
                            display_root,
                            workspace.manifest_path,
                            "embedded_manifest_credential",
                            (
                                "Workspace manifests cannot contain "
                                "credential-bearing URLs or private keys."
                            ),
                            workspace_id=workspace.workspace_id,
                            field="/" + "/".join(child_parts),
                            value="<redacted>",
                        )
                    )
                if (
                    any(marker in upper_key for marker in SECRET_NAME_MARKERS)
                    and not is_reference
                    and not is_policy
                    and not path_like_secret_container
                    and child
                ):
                    issues.append(
                        issue(
                            display_root,
                            workspace.manifest_path,
                            "inline_manifest_secret",
                            (
                                "Workspace manifests may contain secret "
                                "references but not inline secret values."
                            ),
                            workspace_id=workspace.workspace_id,
                            field="/" + "/".join(child_parts),
                            value="<redacted>",
                        )
                    )

            issues.extend(
                manifest_secret_issues(
                    child,
                    workspace=workspace,
                    display_root=display_root,
                    parts=child_parts,
                )
            )
        return issues

    if isinstance(value, list):
        for index, child in enumerate(value):
            issues.extend(
                manifest_secret_issues(
                    child,
                    workspace=workspace,
                    display_root=display_root,
                    parts=(*parts, str(index)),
                )
            )

    return issues


def environment_expectations(workspace: Workspace) -> dict[str, str]:
    """Return required workspace environment values."""

    expectations = {
        "KOA_WORKSPACE_ID": workspace.workspace_id,
        "KOA_WORKSPACE_ROOT": str(workspace.worktree_root),
        "KOA_COMPOSE_PROJECT_NAME": workspace.compose_project_name,
        "COMPOSE_PROJECT_NAME": workspace.compose_project_name,
        "UV_PROJECT_ENVIRONMENT": ".venv",
        "KOA_PORT_BASE": str(workspace.port_base),
        "KOA_DB_NAME": workspace.database_name,
        "KOA_DB_USER": workspace.database_user,
        "KOA_RUNTIME_DIR": str(workspace.paths["runtime"]),
        "KOA_LOG_DIR": str(workspace.paths["logs"]),
        "KOA_TMP_DIR": str(workspace.paths["temporary"]),
        "KOA_DATA_DIR": str(workspace.paths["data"]),
        "KOA_ARTIFACT_DIR": str(workspace.paths["artifacts"]),
        "KOA_BACKUP_DIR": str(workspace.paths["backups"]),
        "KOA_RESTORE_DIR": str(workspace.paths["restore"]),
    }

    if workspace.primary_worktree is not None:
        expectations["KOA_PRIMARY_WORKTREE"] = str(
            workspace.primary_worktree
        )
    if workspace.worktrees_root is not None:
        expectations["KOA_WORKTREES_ROOT"] = str(
            workspace.worktrees_root
        )
    if "uv_cache" in workspace.shared_resources:
        expectations["UV_CACHE_DIR"] = str(
            workspace.shared_resources["uv_cache"]
        )

    port_environment_names = {
        "application": "KOA_APP_PORT",
        "api": "KOA_API_PORT",
        "database": "KOA_DB_PORT",
        "queue": "KOA_QUEUE_PORT",
        "search": "KOA_SEARCH_PORT",
        "metrics": "KOA_METRICS_PORT",
        "debug": "KOA_DEBUG_PORT",
        "test": "KOA_TEST_PORT",
    }
    for key, variable_name in port_environment_names.items():
        expectations[variable_name] = str(workspace.ports[key])

    secret_file = workspace.paths["secrets"] / "db-password"
    expectations["KOA_DB_PASSWORD_FILE"] = str(secret_file)
    return expectations


def compose_environment_expectations(workspace: Workspace) -> dict[str, str]:
    """Return required Compose environment values."""

    expected = environment_expectations(workspace)
    allowed_names = {
        "KOA_WORKSPACE_ID",
        "COMPOSE_PROJECT_NAME",
        "KOA_APP_PORT",
        "KOA_API_PORT",
        "KOA_DB_PORT",
        "KOA_QUEUE_PORT",
        "KOA_SEARCH_PORT",
        "KOA_METRICS_PORT",
        "KOA_DEBUG_PORT",
        "KOA_TEST_PORT",
        "KOA_DB_NAME",
        "KOA_DB_USER",
        "KOA_DB_PASSWORD_FILE",
        "KOA_RUNTIME_DIR",
        "KOA_LOG_DIR",
        "KOA_TMP_DIR",
        "KOA_DATA_DIR",
    }
    return {
        name: value
        for name, value in expected.items()
        if name in allowed_names
    }


def check_manifest_structure(
    workspace: Workspace,
    display_root: Path,
) -> list[Issue]:
    """Validate one normalized workspace declaration."""

    issues: list[Issue] = []
    manifest = workspace.manifest_path
    workspace_id = workspace.workspace_id

    supported_profile_ids = set(workspace.profile_ids) & SUPPORTED_PROFILES
    unsupported_profile_ids = set(workspace.profile_ids) - SUPPORTED_PROFILES
    if unsupported_profile_ids:
        issues.append(
            issue(
                display_root,
                manifest,
                "unsupported_profile",
                (
                    "Workspace profile list contains unsupported profiles. "
                    "Development isolation is defined only for the supported "
                    "developer and build-farm profiles."
                ),
                workspace_id=workspace_id,
                field="profile_ids",
                value=sorted(unsupported_profile_ids),
            )
        )
    if not supported_profile_ids:
        issues.append(
            issue(
                display_root,
                manifest,
                "missing_supported_profile",
                "Workspace does not select a supported development profile.",
                workspace_id=workspace_id,
                field="profile_ids",
                value=list(workspace.profile_ids),
            )
        )

    if workspace.toolchain_id not in SUPPORTED_TOOLCHAINS:
        issues.append(
            issue(
                display_root,
                manifest,
                "unsupported_toolchain",
                "Workspace toolchain is not the active Python UV toolchain.",
                workspace_id=workspace_id,
                field="toolchain_id",
                value=workspace.toolchain_id,
            )
        )

    if workspace.mutable_sharing not in MUTABLE_SHARING_VALUES:
        issues.append(
            issue(
                display_root,
                manifest,
                "mutable_sharing_not_prohibited",
                "Workspace mutable sharing must be explicitly prohibited.",
                workspace_id=workspace_id,
                field="mutable_sharing",
                value=workspace.mutable_sharing,
            )
        )

    expected_manifest_path = (
        workspace.worktree_root / DEFAULT_MANIFEST_RELATIVE_PATH
    ).resolve(strict=False)
    if manifest.resolve(strict=False) != expected_manifest_path:
        issues.append(
            issue(
                display_root,
                manifest,
                "manifest_outside_worktree",
                (
                    "Manifest path does not equal "
                    "worktree_root/.koa/workspace.json."
                ),
                workspace_id=workspace_id,
                field="worktree_root",
                value=workspace.worktree_root,
            )
        )

    declared_worktree_root = declared_path_lexical(
        workspace.raw.get("worktree_root"),
        manifest_path=workspace.manifest_path,
        field_name="worktree_root",
    )
    if path_has_symlink_component(declared_worktree_root):
        issues.append(
            issue(
                display_root,
                manifest,
                "symlinked_worktree_root",
                "Worktree root cannot contain a symbolic-link component.",
                workspace_id=workspace_id,
                field="worktree_root",
                value=declared_worktree_root,
            )
        )

    if not workspace.worktree_root.is_dir():
        issues.append(
            issue(
                display_root,
                manifest,
                "missing_worktree_root",
                "Declared worktree root does not exist as a directory.",
                workspace_id=workspace_id,
                field="worktree_root",
                value=workspace.worktree_root,
            )
        )

    if workspace.worktrees_root is not None and not is_relative_to(
        workspace.worktree_root,
        workspace.worktrees_root,
    ):
        issues.append(
            issue(
                display_root,
                manifest,
                "worktree_outside_worktrees_root",
                "Worktree root is outside the declared worktrees root.",
                workspace_id=workspace_id,
                field="worktrees_root",
                value=workspace.worktrees_root,
            )
        )

    expected_environment = (
        workspace.worktree_root / ".venv"
    ).resolve(strict=False)
    if workspace.paths["python_environment"] != expected_environment:
        issues.append(
            issue(
                display_root,
                manifest,
                "python_environment_not_local",
                "Python environment must be the workspace-local .venv.",
                workspace_id=workspace_id,
                field="paths.python_environment",
                value=workspace.paths["python_environment"],
            )
        )

    for key, path in workspace.paths.items():
        declared_path = declared_path_lexical(
            workspace.raw["paths"][key],
            manifest_path=workspace.manifest_path,
            field_name=f"paths.{key}",
        )
        if path_has_symlink_component(declared_path):
            issues.append(
                issue(
                    display_root,
                    manifest,
                    "symlinked_mutable_path",
                    (
                        "Mutable workspace paths cannot contain symbolic-link "
                        "components to shared or external state."
                    ),
                    workspace_id=workspace_id,
                    field=f"paths.{key}",
                    value=declared_path,
                )
            )
        if not is_relative_to(path, workspace.worktree_root):
            issues.append(
                issue(
                    display_root,
                    manifest,
                    "mutable_path_outside_workspace",
                    (
                        "Mutable workspace paths must remain inside the "
                        "declared worktree root."
                    ),
                    workspace_id=workspace_id,
                    field=f"paths.{key}",
                    value=path,
                )
            )

    path_items = list(workspace.paths.items())
    for first_index, (first_key, first_path) in enumerate(path_items):
        for second_key, second_path in path_items[first_index + 1 :]:
            if paths_overlap(first_path, second_path):
                issues.append(
                    issue(
                        display_root,
                        manifest,
                        "overlapping_workspace_paths",
                        (
                            "Distinct workspace path roles cannot share or "
                            "contain one another."
                        ),
                        workspace_id=workspace_id,
                        field=f"paths.{first_key},paths.{second_key}",
                        value=f"{first_path} <-> {second_path}",
                    )
                )

    lexical_python_environment = (
        workspace.worktree_root / ".venv"
    )
    if path_has_symlink_component(lexical_python_environment):
        issues.append(
            issue(
                display_root,
                manifest,
                "symlinked_python_environment",
                "Workspace .venv cannot contain a symbolic-link component.",
                workspace_id=workspace_id,
                field="paths.python_environment",
                value=lexical_python_environment,
            )
        )

    python_environment = workspace.paths["python_environment"]
    if not python_environment.is_dir():
        issues.append(
            issue(
                display_root,
                manifest,
                "missing_python_environment",
                "Workspace-local .venv directory does not exist.",
                workspace_id=workspace_id,
                field="paths.python_environment",
                value=python_environment,
            )
        )

    required_markers = (
        "pyproject.toml",
        "uv.lock",
        ".python-version",
    )
    for marker in required_markers:
        marker_path = workspace.worktree_root / marker
        if not marker_path.is_file():
            issues.append(
                issue(
                    display_root,
                    manifest,
                    "missing_workspace_marker",
                    "Python UV workspace marker is missing.",
                    workspace_id=workspace_id,
                    field=marker,
                    value=marker_path,
                )
            )

    if workspace.compose_project_name != workspace.workspace_id[:63]:
        issues.append(
            issue(
                display_root,
                manifest,
                "compose_project_not_derived",
                (
                    "Compose project name must be the workspace identity "
                    "truncated to the Compose length limit."
                ),
                workspace_id=workspace_id,
                field="compose_project_name",
                value=workspace.compose_project_name,
            )
        )

    if workspace.database_name == workspace.database_user:
        issues.append(
            issue(
                display_root,
                manifest,
                "database_name_user_not_distinct",
                (
                    "Database name and database identity must be separately "
                    "declared, even when an engine permits equal strings."
                ),
                workspace_id=workspace_id,
                field="database_name,database_user",
                value=workspace.database_name,
            )
        )

    for key, shared_path in workspace.shared_resources.items():
        declared_shared_path = declared_path_lexical(
            workspace.raw["shared_resources"][key],
            manifest_path=workspace.manifest_path,
            field_name=f"shared_resources.{key}",
        )
        if path_has_symlink_component(declared_shared_path):
            issues.append(
                issue(
                    display_root,
                    manifest,
                    "symlinked_shared_resource",
                    "Shared resource paths cannot contain symlink components.",
                    workspace_id=workspace_id,
                    field=f"shared_resources.{key}",
                    value=declared_shared_path,
                )
            )
        if is_relative_to(shared_path, workspace.worktree_root):
            issues.append(
                issue(
                    display_root,
                    manifest,
                    "shared_resource_inside_workspace",
                    (
                        "A declared shared cache must not be represented as "
                        "workspace-owned mutable state."
                    ),
                    workspace_id=workspace_id,
                    field=f"shared_resources.{key}",
                    value=shared_path,
                )
            )

    workspace_id_file = workspace.worktree_root / ".koa/workspace-id"
    if not workspace_id_file.is_file():
        issues.append(
            issue(
                display_root,
                manifest,
                "missing_workspace_identity_file",
                "Workspace identity file .koa/workspace-id is missing.",
                workspace_id=workspace_id,
                field="workspace_id",
                value=workspace_id_file,
            )
        )
    else:
        try:
            recorded_workspace_id = workspace_id_file.read_text(
                encoding="utf-8"
            ).strip()
        except OSError as exc:
            issues.append(
                issue(
                    display_root,
                    manifest,
                    "workspace_identity_file_unreadable",
                    f"Workspace identity file could not be read: {exc}.",
                    workspace_id=workspace_id,
                    field="workspace_id",
                    value=workspace_id_file,
                )
            )
        else:
            if recorded_workspace_id != workspace_id:
                issues.append(
                    issue(
                        display_root,
                        manifest,
                        "workspace_identity_file_mismatch",
                        (
                            "Workspace identity file does not match the "
                            "workspace manifest."
                        ),
                        workspace_id=workspace_id,
                        field="workspace_id",
                        value=(
                            f"recorded={recorded_workspace_id!r} "
                            f"manifest={workspace_id!r}"
                        ),
                    )
                )

    required_secret = workspace.paths["secrets"] / "db-password"
    if not required_secret.is_file():
        issues.append(
            issue(
                display_root,
                manifest,
                "missing_database_secret_reference",
                (
                    "Workspace database secret file is missing. Secret "
                    "values must be injected by file reference."
                ),
                workspace_id=workspace_id,
                field="paths.secrets",
                value=required_secret,
            )
        )

    issues.extend(
        manifest_secret_issues(
            workspace.raw,
            workspace=workspace,
            display_root=display_root,
        )
    )

    return issues


def check_permissions(
    workspace: Workspace,
    display_root: Path,
) -> list[Issue]:
    """Validate workspace metadata and secret permissions."""

    issues: list[Issue] = []
    workspace_id = workspace.workspace_id

    permission_expectations = (
        (
            workspace.worktree_root / ".koa",
            0o077,
            "workspace_control_directory_too_permissive",
            ".koa must not grant group or other permissions.",
        ),
        (
            workspace.paths["secrets"],
            0o077,
            "secret_directory_too_permissive",
            "Secret directory must not grant group or other permissions.",
        ),
        (
            workspace.manifest_path,
            0o077,
            "manifest_too_permissive",
            "Workspace manifest must not grant group or other permissions.",
        ),
        (
            workspace.worktree_root / ".koa/workspace-id",
            0o077,
            "workspace_identity_file_too_permissive",
            "Workspace identity file must not grant group or other permissions.",
        ),
        (
            workspace.worktree_root / ".koa/workspace.env",
            0o077,
            "workspace_environment_too_permissive",
            "Workspace environment file must not grant group or other permissions.",
        ),
        (
            workspace.worktree_root / ".koa/compose.env",
            0o077,
            "compose_environment_too_permissive",
            "Compose environment file must not grant group or other permissions.",
        ),
    )

    for path, prohibited_bits, code, message in permission_expectations:
        if not path.exists():
            continue
        mode = mode_bits(path)
        if mode is not None and mode & prohibited_bits:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    code,
                    message,
                    workspace_id=workspace_id,
                    field=normalize_path(path, workspace.worktree_root),
                    value=oct(mode),
                )
            )

    secret_root = workspace.paths["secrets"]
    if secret_root.is_dir():
        for secret_path in sorted(secret_root.rglob("*")):
            if secret_path.is_symlink():
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "symlinked_secret",
                        "Secret entries cannot be symbolic links.",
                        workspace_id=workspace_id,
                        field="paths.secrets",
                        value=secret_path,
                    )
                )
                continue
            if not secret_path.is_file():
                continue
            mode = mode_bits(secret_path)
            if mode is not None and mode & 0o077:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "secret_file_too_permissive",
                        (
                            "Secret files must not grant group or other "
                            "permissions."
                        ),
                        workspace_id=workspace_id,
                        field="paths.secrets",
                        value=f"{secret_path} mode={oct(mode)}",
                    )
                )

    return issues


def check_environment_files(
    workspace: Workspace,
    display_root: Path,
    counters: Counters,
) -> list[Issue]:
    """Validate workspace and Compose environment projections."""

    issues: list[Issue] = []
    workspace_id = workspace.workspace_id

    file_specs = (
        (
            workspace.worktree_root / ".koa/workspace.env",
            environment_expectations(workspace),
            "workspace",
        ),
        (
            workspace.worktree_root / ".koa/compose.env",
            compose_environment_expectations(workspace),
            "compose",
        ),
    )

    for path, expected, kind in file_specs:
        if not path.is_file():
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    f"missing_{kind}_environment",
                    f"Required {kind} environment file is missing.",
                    workspace_id=workspace_id,
                    field=kind,
                    value=path,
                )
            )
            continue

        counters.checked_environment_files += 1
        try:
            values = parse_shell_environment(path)
        except CheckError as exc:
            issues.append(
                issue(
                    display_root,
                    path,
                    f"invalid_{kind}_environment",
                    str(exc),
                    workspace_id=workspace_id,
                    field=kind,
                )
            )
            continue

        if kind == "workspace":
            workspace.environment = values
        else:
            workspace.compose_environment = values

        for name in FORBIDDEN_ENVIRONMENT_VARIABLES:
            if name in values:
                issues.append(
                    issue(
                        display_root,
                        path,
                        "forbidden_environment_variable",
                        (
                            "Environment file declares a variable forbidden "
                            "by the Python UV toolchain contract."
                        ),
                        workspace_id=workspace_id,
                        field=name,
                        value=values[name],
                    )
                )

        for name, value in values.items():
            if contains_embedded_credential(value):
                issues.append(
                    issue(
                        display_root,
                        path,
                        "embedded_environment_credential",
                        (
                            "Environment values cannot embed credentials "
                            "inside URLs or private keys."
                        ),
                        workspace_id=workspace_id,
                        field=name,
                        value="<redacted>",
                    )
                )
            if value_is_secret(name) and value:
                issues.append(
                    issue(
                        display_root,
                        path,
                        "inline_secret_value",
                        (
                            "Environment files may contain secret references "
                            "but not inline secret values."
                        ),
                        workspace_id=workspace_id,
                        field=name,
                        value="<redacted>",
                    )
                )

        for name, expected_value in expected.items():
            actual_value = values.get(name)
            if actual_value is None:
                issues.append(
                    issue(
                        display_root,
                        path,
                        "missing_environment_projection",
                        (
                            "Environment projection is missing a value "
                            "derived from the workspace manifest."
                        ),
                        workspace_id=workspace_id,
                        field=name,
                        value=expected_value,
                    )
                )
            elif actual_value != expected_value:
                issues.append(
                    issue(
                        display_root,
                        path,
                        "environment_projection_mismatch",
                        (
                            "Environment value does not match the workspace "
                            "manifest."
                        ),
                        workspace_id=workspace_id,
                        field=name,
                        value=f"actual={actual_value!r} expected={expected_value!r}",
                    )
                )

    return issues


def check_storage_resources(
    workspace: Workspace,
    display_root: Path,
    counters: Counters,
) -> tuple[list[Issue], list[ClaimedPath], list[ClaimedName]]:
    """Validate optional storage-resource declarations."""

    issues: list[Issue] = []
    claimed_paths: list[ClaimedPath] = []
    claimed_names: list[ClaimedName] = []
    seen_resource_ids: set[str] = set()

    for index, resource in enumerate(workspace.storage_resources):
        counters.checked_storage_resources += 1
        field_prefix = f"storage_resources[{index}]"

        resource_id = resource.get("resource_id")
        if (
            not isinstance(resource_id, str)
            or not RESOURCE_ID_PATTERN.fullmatch(resource_id)
        ):
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_storage_resource_id",
                    "Storage resource requires a stable resource_id.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.resource_id",
                    value=resource_id,
                )
            )
            continue

        if resource_id in seen_resource_ids:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "duplicate_storage_resource_id",
                    "Storage resource IDs must be unique within a workspace.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.resource_id",
                    value=resource_id,
                )
            )
        seen_resource_ids.add(resource_id)

        declared_workspace_id = resource.get(
            "workspace_id",
            workspace.workspace_id,
        )
        if declared_workspace_id != workspace.workspace_id:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "storage_workspace_mismatch",
                    "Storage resource belongs to a different workspace identity.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.workspace_id",
                    value=declared_workspace_id,
                )
            )

        storage_class = resource.get("storage_class")
        if storage_class not in STORAGE_CLASSES:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_storage_class",
                    "Storage resource uses an unsupported storage class.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.storage_class",
                    value=storage_class,
                )
            )
            storage_class = ""

        access_mode = resource.get("access_mode", "read_write")
        if access_mode not in {"read_only", "read_write"}:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_storage_access_mode",
                    "Storage access mode must be read_only or read_write.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.access_mode",
                    value=access_mode,
                )
            )

        sharing = resource.get("sharing", "prohibited")
        if sharing not in {
            "prohibited",
            "workspace_only",
            "declared_read_only",
            "shared_non_authoritative",
        }:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_storage_sharing",
                    "Storage sharing classification is unsupported.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.sharing",
                    value=sharing,
                )
            )

        if storage_class in PROHIBITED_SHARED_STORAGE_CLASSES and sharing in {
            "declared_read_only",
            "shared_non_authoritative",
        }:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "prohibited_storage_sharing",
                    (
                        "Authoritative, durable, output, diagnostic, "
                        "temporary, backup, restore, or export state cannot "
                        "be shared across workspaces."
                    ),
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.sharing",
                    value=f"{storage_class}:{sharing}",
                )
            )

        if sharing == "declared_read_only":
            if storage_class not in READ_ONLY_SHAREABLE_STORAGE_CLASSES:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "read_only_sharing_not_permitted",
                        (
                            "Only declared caches or test fixtures can use "
                            "read-only sharing."
                        ),
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.storage_class",
                        value=storage_class,
                    )
                )
            if access_mode != "read_only":
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "shared_resource_not_read_only",
                        "Declared read-only sharing requires read_only access.",
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.access_mode",
                        value=access_mode,
                    )
                )

        if sharing == "shared_non_authoritative":
            if storage_class != "non_authoritative_cache":
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "shared_mutable_resource_not_cache",
                        (
                            "Shared mutable resources are limited to "
                            "non-authoritative caches."
                        ),
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.storage_class",
                        value=storage_class,
                    )
                )

        physical_path = resource.get("physical_path")
        if physical_path is not None:
            try:
                normalized_path = resolve_declared_path(
                    physical_path,
                    manifest_path=workspace.manifest_path,
                    field_name=f"{field_prefix}.physical_path",
                )
            except CheckError as exc:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "invalid_storage_path",
                        str(exc),
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.physical_path",
                        value=physical_path,
                    )
                )
            else:
                if sharing in {"prohibited", "workspace_only"}:
                    if not is_relative_to(
                        normalized_path,
                        workspace.worktree_root,
                    ):
                        issues.append(
                            issue(
                                display_root,
                                workspace.manifest_path,
                                "workspace_storage_outside_root",
                                (
                                    "Workspace-owned storage must remain "
                                    "inside the worktree root."
                                ),
                                workspace_id=workspace.workspace_id,
                                field=f"{field_prefix}.physical_path",
                                value=normalized_path,
                            )
                        )
                    claimed_paths.append(
                        ClaimedPath(
                            workspace_id=workspace.workspace_id,
                            manifest_path=workspace.manifest_path,
                            field=f"{field_prefix}.physical_path",
                            path=normalized_path,
                            storage_class=storage_class,
                        )
                    )

        physical_name = resource.get("physical_name")
        if physical_name is not None:
            if not isinstance(physical_name, str) or not NAMESPACE_PATTERN.fullmatch(
                physical_name
            ):
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "invalid_storage_physical_name",
                        (
                            "Storage physical_name must be a stable "
                            "workspace-scoped namespace."
                        ),
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.physical_name",
                        value=physical_name,
                    )
                )
            elif sharing in {"prohibited", "workspace_only"}:
                claimed_names.append(
                    ClaimedName(
                        workspace_id=workspace.workspace_id,
                        manifest_path=workspace.manifest_path,
                        field=f"{field_prefix}.physical_name",
                        value=physical_name,
                    )
                )

    return issues, claimed_paths, claimed_names


def check_services(
    workspace: Workspace,
    display_root: Path,
    counters: Counters,
) -> tuple[list[Issue], list[ClaimedPort], list[ClaimedPath], list[ClaimedName]]:
    """Validate optional service declarations."""

    issues: list[Issue] = []
    claimed_ports: list[ClaimedPort] = []
    claimed_paths: list[ClaimedPath] = []
    claimed_names: list[ClaimedName] = []
    seen_service_ids: set[str] = set()

    for index, service in enumerate(workspace.services):
        counters.checked_services += 1
        field_prefix = f"services[{index}]"
        service_id = service.get("service_id")

        if (
            not isinstance(service_id, str)
            or not RESOURCE_ID_PATTERN.fullmatch(service_id)
        ):
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_service_id",
                    "Service declaration requires a stable service_id.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.service_id",
                    value=service_id,
                )
            )
            continue

        if service_id in seen_service_ids:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "duplicate_service_id",
                    "Service IDs must be unique within a workspace.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.service_id",
                    value=service_id,
                )
            )
        seen_service_ids.add(service_id)

        project_name = service.get(
            "project_name",
            workspace.compose_project_name,
        )
        if project_name != workspace.compose_project_name:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "service_project_mismatch",
                    (
                        "Service project_name must remain inside the "
                        "workspace Compose namespace."
                    ),
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.project_name",
                    value=project_name,
                )
            )

        host_ports = service.get("host_ports", [])
        if (
            not isinstance(host_ports, list)
            or not all(
                isinstance(port, int) and not isinstance(port, bool)
                for port in host_ports
            )
        ):
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_service_host_ports",
                    "Service host_ports must be an integer array.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.host_ports",
                    value=host_ports,
                )
            )
        else:
            for port in host_ports:
                if port not in workspace.ports.values():
                    issues.append(
                        issue(
                            display_root,
                            workspace.manifest_path,
                            "service_port_outside_workspace_block",
                            (
                                "Service host port is outside the declared "
                                "workspace port block."
                            ),
                            workspace_id=workspace.workspace_id,
                            field=f"{field_prefix}.host_ports",
                            value=port,
                        )
                    )
                claimed_ports.append(
                    ClaimedPort(
                        workspace_id=workspace.workspace_id,
                        manifest_path=workspace.manifest_path,
                        field=f"{field_prefix}.host_ports",
                        port=port,
                    )
                )

        for path_key in ("data_paths", "runtime_paths", "log_paths"):
            values = service.get(path_key, [])
            if not isinstance(values, list) or not all(
                isinstance(value, str) and value for value in values
            ):
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "invalid_service_path_list",
                        f"Service {path_key} must be a string array.",
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.{path_key}",
                        value=values,
                    )
                )
                continue

            for raw_path in values:
                normalized = resolve_declared_path(
                    raw_path,
                    manifest_path=workspace.manifest_path,
                    field_name=f"{field_prefix}.{path_key}",
                )
                if not is_relative_to(
                    normalized,
                    workspace.worktree_root,
                ):
                    issues.append(
                        issue(
                            display_root,
                            workspace.manifest_path,
                            "service_path_outside_workspace",
                            (
                                "Service mutable paths must remain inside "
                                "the worktree root."
                            ),
                            workspace_id=workspace.workspace_id,
                            field=f"{field_prefix}.{path_key}",
                            value=normalized,
                        )
                    )
                claimed_paths.append(
                    ClaimedPath(
                        workspace_id=workspace.workspace_id,
                        manifest_path=workspace.manifest_path,
                        field=f"{field_prefix}.{path_key}",
                        path=normalized,
                    )
                )

        for name_key in (
            "container_name",
            "database_name",
            "database_user",
            "queue_namespace",
            "search_index",
            "object_bucket",
        ):
            value = service.get(name_key)
            if value is None:
                continue
            if not isinstance(value, str) or not NAMESPACE_PATTERN.fullmatch(value):
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "invalid_service_namespace",
                        (
                            "Service namespace must use the supported stable "
                            "identifier syntax."
                        ),
                        workspace_id=workspace.workspace_id,
                        field=f"{field_prefix}.{name_key}",
                        value=value,
                    )
                )
                continue
            claimed_names.append(
                ClaimedName(
                    workspace_id=workspace.workspace_id,
                    manifest_path=workspace.manifest_path,
                    field=f"{field_prefix}.{name_key}",
                    value=value,
                )
            )

        secret_refs = service.get("secret_refs", [])
        if not isinstance(secret_refs, list) or not all(
            isinstance(value, str) and value for value in secret_refs
        ):
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_service_secret_refs",
                    "Service secret_refs must be a string array.",
                    workspace_id=workspace.workspace_id,
                    field=f"{field_prefix}.secret_refs",
                    value=secret_refs,
                )
            )
        else:
            for raw_ref in secret_refs:
                secret_ref = resolve_declared_path(
                    raw_ref,
                    manifest_path=workspace.manifest_path,
                    field_name=f"{field_prefix}.secret_refs",
                )
                if not is_relative_to(
                    secret_ref,
                    workspace.paths["secrets"],
                ):
                    issues.append(
                        issue(
                            display_root,
                            workspace.manifest_path,
                            "service_secret_outside_workspace",
                            (
                                "Service secret references must remain inside "
                                "the workspace secret directory."
                            ),
                            workspace_id=workspace.workspace_id,
                            field=f"{field_prefix}.secret_refs",
                            value=secret_ref,
                        )
                    )

    return issues, claimed_ports, claimed_paths, claimed_names


def find_manifest_candidates(
    requested_paths: Sequence[Path],
    *,
    manifest_relative_path: Path,
) -> list[Path]:
    """Discover workspace manifests without following symbolic directories."""

    discovered: set[Path] = set()

    for requested in requested_paths:
        candidate = requested.expanduser()
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve(strict=False)
        else:
            candidate = candidate.resolve(strict=False)

        if not candidate.exists():
            raise CheckError(f"path does not exist: {candidate}")

        if candidate.is_file():
            discovered.add(candidate)
            continue

        direct_manifest = candidate / manifest_relative_path
        if direct_manifest.is_file():
            discovered.add(direct_manifest.resolve(strict=False))

        for manifest in candidate.rglob(manifest_relative_path.name):
            if manifest.is_symlink():
                continue
            if manifest.parent.name != manifest_relative_path.parent.name:
                continue
            if any(
                part in {
                    ".git",
                    ".venv",
                    "__pycache__",
                    "node_modules",
                }
                for part in manifest.parts
            ):
                continue
            discovered.add(manifest.resolve(strict=False))

    return sorted(discovered, key=lambda path: path.as_posix())


def duplicate_name_issues(
    claims: Iterable[ClaimedName],
    display_root: Path,
    code: str,
    message: str,
) -> list[Issue]:
    """Find cross-workspace namespace collisions."""

    by_value: dict[str, list[ClaimedName]] = {}
    for claim in claims:
        by_value.setdefault(claim.value, []).append(claim)

    issues: list[Issue] = []
    for value, colliding_claims in sorted(by_value.items()):
        workspace_ids = {
            claim.workspace_id
            for claim in colliding_claims
        }
        if len(workspace_ids) < 2:
            continue

        detail = ", ".join(
            f"{claim.workspace_id}:{claim.field}"
            for claim in colliding_claims
        )
        for claim in colliding_claims:
            issues.append(
                issue(
                    display_root,
                    claim.manifest_path,
                    code,
                    message,
                    workspace_id=claim.workspace_id,
                    field=claim.field,
                    value=f"{value} claimed by {detail}",
                )
            )
    return issues


def duplicate_port_issues(
    claims: Iterable[ClaimedPort],
    display_root: Path,
) -> list[Issue]:
    """Find host-port collisions across workspaces."""

    by_port: dict[int, list[ClaimedPort]] = {}
    for claim in claims:
        by_port.setdefault(claim.port, []).append(claim)

    issues: list[Issue] = []
    for port, colliding_claims in sorted(by_port.items()):
        workspace_ids = {
            claim.workspace_id
            for claim in colliding_claims
        }
        if len(workspace_ids) < 2:
            continue
        detail = ", ".join(
            f"{claim.workspace_id}:{claim.field}"
            for claim in colliding_claims
        )
        for claim in colliding_claims:
            issues.append(
                issue(
                    display_root,
                    claim.manifest_path,
                    "host_port_collision",
                    "Host port is claimed by more than one workspace.",
                    workspace_id=claim.workspace_id,
                    field=claim.field,
                    value=f"{port} claimed by {detail}",
                )
            )
    return issues


def cross_workspace_path_issues(
    claims: Sequence[ClaimedPath],
    display_root: Path,
) -> list[Issue]:
    """Find overlapping mutable path ownership across workspaces."""

    issues: list[Issue] = []

    for first_index, first in enumerate(claims):
        for second in claims[first_index + 1 :]:
            if first.workspace_id == second.workspace_id:
                continue

            if not (
                paths_overlap(first.path, second.path)
                or same_file_if_present(first.path, second.path)
            ):
                continue

            message = (
                "Mutable path ownership overlaps across workspaces. "
                "Deleting, resetting, migrating, or writing one workspace "
                "could affect another."
            )
            detail = (
                f"{first.workspace_id}:{first.field}={first.path} <-> "
                f"{second.workspace_id}:{second.field}={second.path}"
            )
            issues.append(
                issue(
                    display_root,
                    first.manifest_path,
                    "cross_workspace_path_collision",
                    message,
                    workspace_id=first.workspace_id,
                    field=first.field,
                    value=detail,
                )
            )
            issues.append(
                issue(
                    display_root,
                    second.manifest_path,
                    "cross_workspace_path_collision",
                    message,
                    workspace_id=second.workspace_id,
                    field=second.field,
                    value=detail,
                )
            )

    return issues


def static_cross_workspace_checks(
    workspaces: Sequence[Workspace],
    display_root: Path,
    service_ports: Sequence[ClaimedPort],
    storage_paths: Sequence[ClaimedPath],
    service_paths: Sequence[ClaimedPath],
    storage_names: Sequence[ClaimedName],
    service_names: Sequence[ClaimedName],
) -> list[Issue]:
    """Validate global uniqueness and mutable-state isolation."""

    issues: list[Issue] = []

    workspace_name_claims = [
        ClaimedName(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field="workspace_id",
            value=workspace.workspace_id,
        )
        for workspace in workspaces
    ]
    compose_claims = [
        ClaimedName(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field="compose_project_name",
            value=workspace.compose_project_name,
        )
        for workspace in workspaces
    ]
    database_name_claims = [
        ClaimedName(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field="database_name",
            value=workspace.database_name,
        )
        for workspace in workspaces
    ]
    database_user_claims = [
        ClaimedName(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field="database_user",
            value=workspace.database_user,
        )
        for workspace in workspaces
    ]
    branch_claims = [
        ClaimedName(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field="branch",
            value=workspace.branch,
        )
        for workspace in workspaces
    ]

    issues.extend(
        duplicate_name_issues(
            workspace_name_claims,
            display_root,
            "workspace_identity_collision",
            "Workspace identity is duplicated.",
        )
    )
    issues.extend(
        duplicate_name_issues(
            compose_claims,
            display_root,
            "compose_project_collision",
            "Compose project namespace is duplicated.",
        )
    )
    issues.extend(
        duplicate_name_issues(
            database_name_claims,
            display_root,
            "database_name_collision",
            "Database name is duplicated across workspaces.",
        )
    )
    issues.extend(
        duplicate_name_issues(
            database_user_claims,
            display_root,
            "database_identity_collision",
            "Database user identity is duplicated across workspaces.",
        )
    )
    issues.extend(
        duplicate_name_issues(
            branch_claims,
            display_root,
            "branch_collision",
            "The same writable branch is declared by several workspaces.",
        )
    )
    issues.extend(
        duplicate_name_issues(
            [*storage_names, *service_names],
            display_root,
            "service_or_storage_namespace_collision",
            "Workspace-owned service or storage namespace is duplicated.",
        )
    )

    port_claims = [
        ClaimedPort(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field=f"ports.{key}",
            port=port,
        )
        for workspace in workspaces
        for key, port in workspace.ports.items()
    ]
    issues.extend(
        duplicate_port_issues(
            [*port_claims, *service_ports],
            display_root,
        )
    )

    mutable_path_claims = [
        ClaimedPath(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field=f"paths.{key}",
            path=path,
        )
        for workspace in workspaces
        for key, path in workspace.paths.items()
    ]
    issues.extend(
        cross_workspace_path_issues(
            [
                *mutable_path_claims,
                *storage_paths,
                *service_paths,
            ],
            display_root,
        )
    )

    worktree_claims = [
        ClaimedPath(
            workspace_id=workspace.workspace_id,
            manifest_path=workspace.manifest_path,
            field="worktree_root",
            path=workspace.worktree_root,
        )
        for workspace in workspaces
    ]
    issues.extend(
        cross_workspace_path_issues(
            worktree_claims,
            display_root,
        )
    )

    # Shared resources may repeat only with exactly the same class key.
    shared_path_owners: dict[Path, list[tuple[str, str, Path]]] = {}
    for workspace in workspaces:
        for key, path in workspace.shared_resources.items():
            shared_path_owners.setdefault(
                path.resolve(strict=False),
                [],
            ).append(
                (
                    workspace.workspace_id,
                    key,
                    workspace.manifest_path,
                )
            )

    for shared_path, owners in sorted(
        shared_path_owners.items(),
        key=lambda item: item[0].as_posix(),
    ):
        keys = {key for _, key, _ in owners}
        if len(keys) > 1:
            for workspace_id, key, manifest_path in owners:
                issues.append(
                    issue(
                        display_root,
                        manifest_path,
                        "shared_resource_class_collision",
                        (
                            "One shared path is declared under different "
                            "resource classes."
                        ),
                        workspace_id=workspace_id,
                        field=f"shared_resources.{key}",
                        value=shared_path,
                    )
                )

    return issues


def run_command(
    argv: Sequence[str],
    *,
    cwd: Path | None = None,
    environment: Mapping[str, str] | None = None,
    timeout: float = 30.0,
) -> subprocess.CompletedProcess[str]:
    """Run a bounded command and return captured output."""

    try:
        return subprocess.run(
            list(argv),
            cwd=cwd,
            env=dict(environment) if environment is not None else None,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise CheckError(f"required command not found: {argv[0]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise CheckError(
            f"command timed out after {timeout:g}s: {shlex.join(argv)}"
        ) from exc
    except OSError as exc:
        raise CheckError(
            f"command failed to start: {shlex.join(argv)}: {exc}"
        ) from exc


def git_registered_worktrees(primary_worktree: Path) -> dict[Path, str]:
    """Return Git-registered worktree paths and branches."""

    result = run_command(
        [
            "git",
            "-C",
            str(primary_worktree),
            "worktree",
            "list",
            "--porcelain",
        ],
        timeout=20,
    )
    if result.returncode != 0:
        raise CheckError(
            "git worktree list failed: "
            + (result.stderr.strip() or result.stdout.strip())
        )

    registered: dict[Path, str] = {}
    current_path: Path | None = None
    current_branch = ""

    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            if current_path is not None:
                registered[current_path] = current_branch
            current_path = Path(line.removeprefix("worktree ")).resolve(
                strict=False
            )
            current_branch = ""
        elif line.startswith("branch "):
            current_branch = line.removeprefix("branch refs/heads/")

    if current_path is not None:
        registered[current_path] = current_branch

    return registered


def check_git(
    workspaces: Sequence[Workspace],
    display_root: Path,
    counters: Counters,
) -> list[Issue]:
    """Verify Git worktree registration and branch identity."""

    issues: list[Issue] = []
    registry_cache: dict[Path, dict[Path, str]] = {}

    for workspace in workspaces:
        counters.git_checks += 1
        if workspace.primary_worktree is None:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "missing_primary_worktree",
                    "Git verification requires primary_worktree.",
                    workspace_id=workspace.workspace_id,
                    field="primary_worktree",
                )
            )
            continue

        primary = workspace.primary_worktree.resolve(strict=False)
        if primary not in registry_cache:
            try:
                registry_cache[primary] = git_registered_worktrees(primary)
            except CheckError as exc:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "git_registry_unavailable",
                        str(exc),
                        workspace_id=workspace.workspace_id,
                        field="primary_worktree",
                        value=primary,
                    )
                )
                continue

        registered = registry_cache[primary]
        branch = registered.get(workspace.worktree_root)
        if branch is None:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "worktree_not_registered",
                    "Workspace root is not registered as a Git worktree.",
                    workspace_id=workspace.workspace_id,
                    field="worktree_root",
                    value=workspace.worktree_root,
                )
            )
        elif branch != workspace.branch:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "git_branch_mismatch",
                    "Git worktree branch does not match the manifest.",
                    workspace_id=workspace.workspace_id,
                    field="branch",
                    value=f"git={branch!r} manifest={workspace.branch!r}",
                )
            )

        status = run_command(
            [
                "git",
                "-C",
                str(workspace.worktree_root),
                "rev-parse",
                "--show-toplevel",
            ],
            timeout=10,
        )
        if status.returncode != 0:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "git_worktree_invalid",
                    "Workspace root is not a readable Git worktree.",
                    workspace_id=workspace.workspace_id,
                    field="worktree_root",
                    value=status.stderr.strip(),
                )
            )
        else:
            actual_root = Path(status.stdout.strip()).resolve(strict=False)
            if actual_root != workspace.worktree_root:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "git_root_mismatch",
                        "Git top-level path does not match worktree_root.",
                        workspace_id=workspace.workspace_id,
                        field="worktree_root",
                        value=f"git={actual_root} manifest={workspace.worktree_root}",
                    )
                )

        for ignored_path in (".venv/", ".koa/"):
            ignore_result = run_command(
                [
                    "git",
                    "-C",
                    str(workspace.worktree_root),
                    "check-ignore",
                    "--quiet",
                    "--no-index",
                    ignored_path,
                ],
                timeout=10,
            )
            if ignore_result.returncode != 0:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "workspace_path_not_ignored",
                        (
                            "Canonical Git ignore policy must exclude "
                            ".venv/ and .koa/."
                        ),
                        workspace_id=workspace.workspace_id,
                        field=ignored_path,
                        value=(
                            ignore_result.stderr.strip()
                            or ignore_result.stdout.strip()
                        ),
                    )
                )

    return issues


def uv_environment(workspace: Workspace) -> dict[str, str]:
    """Build a sanitized UV execution environment."""

    environment = os.environ.copy()
    for name in FORBIDDEN_ENVIRONMENT_VARIABLES:
        environment.pop(name, None)

    environment["UV_PROJECT_ENVIRONMENT"] = ".venv"
    if "uv_cache" in workspace.shared_resources:
        environment["UV_CACHE_DIR"] = str(
            workspace.shared_resources["uv_cache"]
        )
    return environment


def check_uv(
    workspaces: Sequence[Workspace],
    display_root: Path,
    counters: Counters,
    *,
    timeout: float,
) -> list[Issue]:
    """Run the canonical frozen lock verification."""

    issues: list[Issue] = []

    for workspace in workspaces:
        counters.uv_checks += 1
        result = run_command(
            ["uv", "lock", "--check"],
            cwd=workspace.worktree_root,
            environment=uv_environment(workspace),
            timeout=timeout,
        )
        if result.returncode != 0:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "uv_lock_check_failed",
                    (
                        "uv lock --check failed. The checker does not "
                        "refresh the lockfile automatically."
                    ),
                    workspace_id=workspace.workspace_id,
                    field="uv.lock",
                    value=(result.stderr.strip() or result.stdout.strip()),
                )
            )

    return issues


def check_python_prefix(
    workspaces: Sequence[Workspace],
    display_root: Path,
    counters: Counters,
    *,
    timeout: float,
) -> list[Issue]:
    """Verify that UV executes the workspace-local Python environment."""

    issues: list[Issue] = []
    probe = (
        "import json,pathlib,sys;"
        "print(json.dumps({"
        "'prefix':str(pathlib.Path(sys.prefix).resolve()),"
        "'base_prefix':str(pathlib.Path(sys.base_prefix).resolve()),"
        "'executable':str(pathlib.Path(sys.executable).resolve())"
        "}))"
    )

    for workspace in workspaces:
        counters.python_prefix_checks += 1
        result = run_command(
            [
                "uv",
                "run",
                "--frozen",
                "python",
                "-c",
                probe,
            ],
            cwd=workspace.worktree_root,
            environment=uv_environment(workspace),
            timeout=timeout,
        )
        if result.returncode != 0:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "uv_python_probe_failed",
                    "UV could not execute the frozen workspace Python.",
                    workspace_id=workspace.workspace_id,
                    field="paths.python_environment",
                    value=(result.stderr.strip() or result.stdout.strip()),
                )
            )
            continue

        try:
            probe_result = json.loads(result.stdout.strip())
            prefix = Path(probe_result["prefix"]).resolve(strict=False)
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "invalid_python_probe_output",
                    f"Python prefix probe returned invalid output: {exc}.",
                    workspace_id=workspace.workspace_id,
                    field="paths.python_environment",
                    value=result.stdout.strip(),
                )
            )
            continue

        if prefix != workspace.paths["python_environment"]:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "python_prefix_outside_workspace",
                    (
                        "UV Python sys.prefix does not match the "
                        "workspace-local .venv."
                    ),
                    workspace_id=workspace.workspace_id,
                    field="paths.python_environment",
                    value=(
                        f"prefix={prefix} "
                        f"expected={workspace.paths['python_environment']}"
                    ),
                )
            )

    return issues


def check_listeners(
    workspaces: Sequence[Workspace],
    display_root: Path,
    counters: Counters,
    *,
    timeout: float,
) -> list[Issue]:
    """Probe whether declared host ports are currently bindable.

    This check is intended for pre-start validation.  Running workspace
    services will legitimately occupy their own ports, so callers must not use
    this option as a health check for active services.
    """

    del timeout
    issues: list[Issue] = []

    for workspace in workspaces:
        for key, port in workspace.ports.items():
            counters.listener_checks += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
                sock.bind(("127.0.0.1", port))
            except OSError as exc:
                issues.append(
                    issue(
                        display_root,
                        workspace.manifest_path,
                        "declared_port_not_bindable",
                        (
                            "Declared host port is not bindable on loopback. "
                            "Use this check only before workspace services start."
                        ),
                        workspace_id=workspace.workspace_id,
                        field=f"ports.{key}",
                        value=f"{port}: {exc}",
                    )
                )
            finally:
                sock.close()

    return issues


def compose_file_for(workspace: Workspace) -> Path | None:
    """Return the first supported Compose file in a workspace."""

    for name in (
        "compose.yaml",
        "compose.yml",
        "docker-compose.yaml",
        "docker-compose.yml",
    ):
        candidate = workspace.worktree_root / name
        if candidate.is_file():
            return candidate
    return None


def check_docker_compose(
    workspaces: Sequence[Workspace],
    display_root: Path,
    counters: Counters,
    *,
    timeout: float,
) -> list[Issue]:
    """Validate rootless Docker Compose project configuration."""

    issues: list[Issue] = []

    version = run_command(
        ["docker", "compose", "version"],
        timeout=timeout,
    )
    if version.returncode != 0:
        return [
            issue(
                display_root,
                workspaces[0].manifest_path,
                "docker_compose_unavailable",
                "docker compose is unavailable for requested execution checks.",
                value=(version.stderr.strip() or version.stdout.strip()),
            )
        ]

    info = run_command(
        ["docker", "info", "--format", "{{json .SecurityOptions}}"],
        timeout=timeout,
    )
    if info.returncode != 0:
        issues.append(
            issue(
                display_root,
                workspaces[0].manifest_path,
                "docker_info_failed",
                "Docker daemon information could not be read.",
                value=(info.stderr.strip() or info.stdout.strip()),
            )
        )
    else:
        rootless = "name=rootless" in info.stdout or "rootless" in info.stdout
        if not rootless:
            issues.append(
                issue(
                    display_root,
                    workspaces[0].manifest_path,
                    "docker_not_rootless",
                    (
                        "Development service containers must use the "
                        "profile-approved rootless runtime."
                    ),
                    value=info.stdout.strip(),
                )
            )

    for workspace in workspaces:
        compose_file = compose_file_for(workspace)
        if compose_file is None:
            continue

        counters.docker_checks += 1
        compose_env = workspace.worktree_root / ".koa/compose.env"
        result = run_command(
            [
                "docker",
                "compose",
                "--file",
                str(compose_file),
                "--env-file",
                str(compose_env),
                "--project-name",
                workspace.compose_project_name,
                "config",
                "--quiet",
            ],
            cwd=workspace.worktree_root,
            timeout=timeout,
        )
        if result.returncode != 0:
            issues.append(
                issue(
                    display_root,
                    workspace.manifest_path,
                    "compose_config_failed",
                    "Workspace Compose configuration is invalid.",
                    workspace_id=workspace.workspace_id,
                    field="compose_project_name",
                    value=(result.stderr.strip() or result.stdout.strip()),
                )
            )

    return issues


def sort_issues(issues: Iterable[Issue]) -> list[Issue]:
    """Return deterministic issue ordering."""

    return sorted(
        issues,
        key=lambda item: (
            item.path,
            item.workspace_id,
            item.field,
            item.code,
            item.message,
            item.value,
        ),
    )


def render_text(
    issues: Sequence[Issue],
    counters: Counters,
    *,
    quiet: bool,
    max_issues: int,
) -> None:
    """Render human-readable diagnostics."""

    if issues:
        print(
            f"DEVELOPMENT ISOLATION CHECK FAILED: {len(issues)} issue(s)",
            file=sys.stderr,
        )
        for item in issues[:max_issues]:
            workspace = (
                f" workspace={item.workspace_id}"
                if item.workspace_id
                else ""
            )
            field = f" field={item.field}" if item.field else ""
            print(
                (
                    f"{item.path}: [{item.code}]"
                    f"{workspace}{field}: {item.message}"
                ),
                file=sys.stderr,
            )
            if item.value:
                print(f"  value: {item.value}", file=sys.stderr)

        omitted = len(issues) - max_issues
        if omitted > 0:
            print(
                f"... {omitted} additional issue(s) omitted",
                file=sys.stderr,
            )

        print(
            (
                "summary: "
                f"manifests={counters.discovered_manifests} "
                f"workspaces={counters.checked_workspaces} "
                f"environment_files={counters.checked_environment_files} "
                f"storage_resources={counters.checked_storage_resources} "
                f"services={counters.checked_services} "
                f"git_checks={counters.git_checks} "
                f"uv_checks={counters.uv_checks} "
                f"python_prefix_checks={counters.python_prefix_checks} "
                f"docker_checks={counters.docker_checks} "
                f"listener_checks={counters.listener_checks}"
            ),
            file=sys.stderr,
        )
        return

    if quiet:
        return

    print("DEVELOPMENT ISOLATION CHECK OK")
    print(f"manifests: {counters.discovered_manifests}")
    print(f"workspaces: {counters.checked_workspaces}")
    print(
        "environment files: "
        f"{counters.checked_environment_files}"
    )
    print(
        "storage resources: "
        f"{counters.checked_storage_resources}"
    )
    print(f"services: {counters.checked_services}")
    print(f"Git checks: {counters.git_checks}")
    print(f"UV checks: {counters.uv_checks}")
    print(
        "Python prefix checks: "
        f"{counters.python_prefix_checks}"
    )
    print(f"Docker checks: {counters.docker_checks}")
    print(f"listener checks: {counters.listener_checks}")


def render_json(
    issues: Sequence[Issue],
    counters: Counters,
    workspaces: Sequence[Workspace],
    *,
    max_issues: int,
) -> None:
    """Render machine-readable diagnostics."""

    payload = {
        "tool": "check_development_isolation",
        "tool_version": TOOL_VERSION,
        "result": "fail" if issues else "pass",
        "counts": asdict(counters),
        "workspace_ids": sorted(
            workspace.workspace_id
            for workspace in workspaces
        ),
        "issue_count": len(issues),
        "issues": [
            asdict(item)
            for item in issues[:max_issues]
        ],
        "omitted_issue_count": max(
            len(issues) - max_issues,
            0,
        ),
    }
    print(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
    )


def build_argument_parser() -> argparse.ArgumentParser:
    """Create the command-line interface."""

    parser = argparse.ArgumentParser(
        description=(
            "Validate kOA development workspace, dependency, port, service, "
            "storage, database, secret, and namespace isolation."
        )
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Workspace manifests or directories containing "
            ".koa/workspace.json. Defaults to the current directory."
        ),
    )
    parser.add_argument(
        "--display-root",
        type=Path,
        default=Path.cwd(),
        help=(
            "Root used to display relative paths. Default: current directory."
        ),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST_RELATIVE_PATH,
        help=(
            "Manifest path relative to a workspace root. "
            "Default: .koa/workspace.json."
        ),
    )
    parser.add_argument(
        "--skip-environment-files",
        action="store_true",
        help=(
            "Skip .koa/workspace.env and .koa/compose.env projection checks."
        ),
    )
    parser.add_argument(
        "--git",
        action="store_true",
        help="Verify Git worktree registration and branch identity.",
    )
    parser.add_argument(
        "--uv",
        action="store_true",
        help="Run the canonical uv lock --check command in each workspace.",
    )
    parser.add_argument(
        "--python-prefix",
        action="store_true",
        help=(
            "Run uv run --frozen python and verify sys.prefix equals "
            "the workspace-local .venv."
        ),
    )
    parser.add_argument(
        "--docker",
        action="store_true",
        help=(
            "Verify rootless Docker and validate repository Compose "
            "configuration when a Compose file exists."
        ),
    )
    parser.add_argument(
        "--probe-listeners",
        action="store_true",
        help=(
            "Verify that declared loopback ports are bindable. Use only "
            "before workspace services start."
        ),
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Enable Git, UV, and Python-prefix checks. Docker and listener "
            "checks remain explicit because they depend on the selected "
            "service topology and current runtime state."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-command timeout in seconds. Default: 30.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Diagnostic output format.",
    )
    parser.add_argument(
        "--max-issues",
        type=int,
        default=200,
        help="Maximum issue details to print. Default: 200.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress successful text output.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {TOOL_VERSION}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run all selected checks."""

    parser = build_argument_parser()
    args = parser.parse_args(argv)

    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.max_issues < 1:
        parser.error("--max-issues must be at least 1")
    if args.manifest.is_absolute():
        parser.error("--manifest must be relative to a workspace root")

    requested_paths = (
        [Path(value) for value in args.paths]
        if args.paths
        else [Path.cwd()]
    )
    display_root = args.display_root.resolve(strict=False)
    counters = Counters()

    try:
        manifest_paths = find_manifest_candidates(
            requested_paths,
            manifest_relative_path=args.manifest,
        )
    except CheckError as exc:
        parser.error(str(exc))

    counters.discovered_manifests = len(manifest_paths)
    if not manifest_paths:
        parser.error(
            f"no {args.manifest.as_posix()} manifests were found"
        )

    workspaces: list[Workspace] = []
    issues: list[Issue] = []
    service_ports: list[ClaimedPort] = []
    storage_paths: list[ClaimedPath] = []
    service_paths: list[ClaimedPath] = []
    storage_names: list[ClaimedName] = []
    service_names: list[ClaimedName] = []

    for manifest_path in manifest_paths:
        try:
            workspace = parse_workspace(manifest_path)
        except CheckError as exc:
            issues.append(
                issue(
                    display_root,
                    manifest_path,
                    "invalid_workspace_manifest",
                    str(exc),
                )
            )
            continue

        counters.checked_workspaces += 1
        workspaces.append(workspace)
        issues.extend(
            check_manifest_structure(workspace, display_root)
        )
        issues.extend(
            check_permissions(workspace, display_root)
        )

        if not args.skip_environment_files:
            issues.extend(
                check_environment_files(
                    workspace,
                    display_root,
                    counters,
                )
            )

        (
            storage_issues,
            workspace_storage_paths,
            workspace_storage_names,
        ) = check_storage_resources(
            workspace,
            display_root,
            counters,
        )
        issues.extend(storage_issues)
        storage_paths.extend(workspace_storage_paths)
        storage_names.extend(workspace_storage_names)

        (
            service_issues,
            workspace_service_ports,
            workspace_service_paths,
            workspace_service_names,
        ) = check_services(
            workspace,
            display_root,
            counters,
        )
        issues.extend(service_issues)
        service_ports.extend(workspace_service_ports)
        service_paths.extend(workspace_service_paths)
        service_names.extend(workspace_service_names)

    if workspaces:
        issues.extend(
            static_cross_workspace_checks(
                workspaces,
                display_root,
                service_ports,
                storage_paths,
                service_paths,
                storage_names,
                service_names,
            )
        )

    run_git = args.git or args.strict
    run_uv_check = args.uv or args.strict
    run_python = args.python_prefix or args.strict
    run_docker = args.docker

    if workspaces and run_git:
        issues.extend(
            check_git(
                workspaces,
                display_root,
                counters,
            )
        )

    if workspaces and run_uv_check:
        try:
            issues.extend(
                check_uv(
                    workspaces,
                    display_root,
                    counters,
                    timeout=args.timeout,
                )
            )
        except CheckError as exc:
            issues.append(
                issue(
                    display_root,
                    workspaces[0].manifest_path,
                    "uv_check_unavailable",
                    str(exc),
                )
            )

    if workspaces and run_python:
        try:
            issues.extend(
                check_python_prefix(
                    workspaces,
                    display_root,
                    counters,
                    timeout=args.timeout,
                )
            )
        except CheckError as exc:
            issues.append(
                issue(
                    display_root,
                    workspaces[0].manifest_path,
                    "python_prefix_check_unavailable",
                    str(exc),
                )
            )

    if workspaces and args.probe_listeners:
        issues.extend(
            check_listeners(
                workspaces,
                display_root,
                counters,
                timeout=args.timeout,
            )
        )

    if workspaces and run_docker:
        try:
            issues.extend(
                check_docker_compose(
                    workspaces,
                    display_root,
                    counters,
                    timeout=args.timeout,
                )
            )
        except CheckError as exc:
            issues.append(
                issue(
                    display_root,
                    workspaces[0].manifest_path,
                    "docker_check_unavailable",
                    str(exc),
                )
            )

    ordered_issues = sort_issues(issues)

    if args.format == "json":
        render_json(
            ordered_issues,
            counters,
            workspaces,
            max_issues=args.max_issues,
        )
    else:
        render_text(
            ordered_issues,
            counters,
            quiet=args.quiet,
            max_issues=args.max_issues,
        )

    return EXIT_FAIL if ordered_issues else EXIT_PASS


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        raise SystemExit(130)
    except Exception as exc:
        print(
            f"internal error: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_INTERNAL)
