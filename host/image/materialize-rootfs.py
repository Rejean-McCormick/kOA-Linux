#!/usr/bin/env python3
"""Materialize a rootfs from exact, locally available, policy-admitted package archives."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tarfile
import tempfile
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any

class MaterializationError(ValueError):
    """Raised when package resolution or rootfs materialization must fail closed."""

_REQUIRED_PACKAGE_FIELDS = (
    "package_id",
    "version",
    "sha256",
    "source_id",
    "source_ref",
    "artifact_path",
    "owner",
    "trust_scope",
    "provenance_ref",
    "admission_checks",
    "evidence_refs",
)
_REQUIRED_ADMISSION_CHECKS = ("trust_scope_verified", "provenance_verified", "revocation_checked", "license_policy_checked")
_FLOATING_VERSION_TOKENS = {"latest", "stable", "current", "main", "master", "head"}
_MAX_INPUT_BYTES = 16 * 1024 * 1024
_MAX_ARCHIVE_MEMBERS = 1_000_000

def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise MaterializationError(f"duplicate_key:{key}")
        result[key] = value
    return result

def _load_json_document(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > _MAX_INPUT_BYTES:
        raise MaterializationError(f"input_too_large:{path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MaterializationError(f"document_must_be_json_compatible_yaml:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise MaterializationError(f"expected_object:{path}")
    return value, raw

def _load_toml_document(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > _MAX_INPUT_BYTES:
        raise MaterializationError(f"input_too_large:{path}")
    try:
        value = tomllib.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise MaterializationError(f"invalid_toml:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise MaterializationError(f"expected_object:{path}")
    return value, raw

def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def _require_sha256(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise MaterializationError(f"{field}_must_be_sha256")
    digest = value.strip().lower()
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise MaterializationError(f"{field}_must_be_sha256")
    return digest

def _require_nonempty(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MaterializationError(f"{field}_required")
    return value.strip()

def _require_exact_version(value: Any, field: str) -> str:
    version = _require_nonempty(value, field)
    lowered = version.casefold()
    if lowered in _FLOATING_VERSION_TOKENS or any(token in version for token in "*<>=^~,"):
        raise MaterializationError(f"{field}_must_be_exact")
    if any(character.isspace() for character in version):
        raise MaterializationError(f"{field}_must_be_exact")
    return version

def _relative_path(value: Any, field: str) -> str:
    text = _require_nonempty(value, field)
    if "\\" in text:
        raise MaterializationError(f"{field}_must_be_posix_relative")
    pure = PurePosixPath(text)
    if pure.is_absolute() or text.startswith("./") or ".." in pure.parts or "." in pure.parts:
        raise MaterializationError(f"{field}_must_be_normalized_relative")
    normalized = pure.as_posix()
    if normalized in {"", "."}:
        raise MaterializationError(f"{field}_must_be_normalized_relative")
    return normalized.rstrip("/")

def _is_under(path: str, prefix: str) -> bool:
    clean_path = path.rstrip("/")
    clean_prefix = prefix.rstrip("/")
    return clean_path == clean_prefix or clean_path.startswith(clean_prefix + "/")

def _source_catalog(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if policy.get("default_action") != "reject":
        raise MaterializationError("package_sources_must_be_deny_by_default")
    if policy.get("floating_version_allowed") is not False:
        raise MaterializationError("floating_versions_must_be_prohibited")
    if policy.get("undeclared_mirror_allowed") is not False:
        raise MaterializationError("undeclared_mirrors_must_be_prohibited")
    materialization = policy.get("materialization")
    if not isinstance(materialization, dict):
        raise MaterializationError("materialization_policy_missing")
    if materialization.get("resolver") != "exact_manifest_only":
        raise MaterializationError("unsupported_materialization_resolver")
    if materialization.get("network_access") != "prohibited":
        raise MaterializationError("materialization_network_must_be_prohibited")
    sources = materialization.get("sources")
    if not isinstance(sources, list) or not sources:
        raise MaterializationError("materialization_sources_missing")
    catalog: dict[str, dict[str, Any]] = {}
    for item in sources:
        if not isinstance(item, dict):
            raise MaterializationError("invalid_materialization_source")
        source_id = _require_nonempty(item.get("source_id"), "source_id")
        if source_id in catalog:
            raise MaterializationError(f"duplicate_materialization_source:{source_id}")
        if item.get("admitted") is not True:
            raise MaterializationError(f"materialization_source_not_admitted:{source_id}")
        if item.get("source_kind") != "system_channel_artifact" or item.get("transport") != "filesystem":
            raise MaterializationError(f"unsupported_materialization_source:{source_id}")
        if item.get("admission") != "signed_manifest_and_digest_only":
            raise MaterializationError(f"materialization_source_admission_mismatch:{source_id}")
        if item.get("network") is not False or item.get("artifact_path_mode") != "package_store_relative":
            raise MaterializationError(f"unsafe_materialization_source:{source_id}")
        catalog[source_id] = item
    return catalog

def _base_requirements(base: dict[str, Any]) -> tuple[list[str], list[str]]:
    required = base.get("required_capabilities")
    if not isinstance(required, list) or not required:
        raise MaterializationError("base_package_capabilities_missing")
    capabilities: list[str] = []
    for item in required:
        if not isinstance(item, dict):
            raise MaterializationError("invalid_base_package_capability")
        capability = _require_nonempty(item.get("id"), "base_package_capability_id")
        if capability in capabilities:
            raise MaterializationError(f"duplicate_base_package_capability:{capability}")
        capabilities.append(capability)

    contract = base.get("resolution_contract")
    if not isinstance(contract, dict):
        raise MaterializationError("base_package_resolution_contract_missing")
    if contract.get("materializer") != "host/image/materialize-rootfs.py":
        raise MaterializationError("base_package_materializer_mismatch")
    fields = contract.get("required_fields")
    if fields != list(_REQUIRED_PACKAGE_FIELDS):
        raise MaterializationError("base_package_resolution_fields_mismatch")
    if contract.get("exact_version_required") is not True or contract.get("content_digest_required") is not True:
        raise MaterializationError("base_package_exact_identity_requirement_missing")

    prefixes = base.get("prohibited_path_prefixes")
    if not isinstance(prefixes, list) or not prefixes:
        raise MaterializationError("prohibited_path_prefixes_missing")
    normalized_prefixes = [_relative_path(value, "prohibited_path_prefix") for value in prefixes]
    return capabilities, normalized_prefixes

def _validate_plan(
    base: dict[str, Any],
    plan: dict[str, Any],
    source_catalog: dict[str, dict[str, Any]],
) -> dict[str, dict[str, str]]:
    if plan.get("schema_version") != 1:
        raise MaterializationError("package_plan_schema_version_unsupported")
    package_set_id = _require_nonempty(base.get("package_set_id"), "base_package_set_id")
    profile_id = _require_nonempty(base.get("profile_id"), "base_profile_id")
    if plan.get("package_set_id") != package_set_id or plan.get("profile_id") != profile_id:
        raise MaterializationError("package_plan_identity_mismatch")

    capabilities, _ = _base_requirements(base)
    resolved = plan.get("capabilities")
    if not isinstance(resolved, dict):
        raise MaterializationError("package_plan_capabilities_missing")
    if set(resolved) != set(capabilities):
        raise MaterializationError("package_plan_must_match_required_capabilities_exactly")

    validated: dict[str, dict[str, str]] = {}
    for capability in sorted(capabilities):
        record = resolved.get(capability)
        if not isinstance(record, dict):
            raise MaterializationError(f"invalid_package_plan:{capability}")
        unknown = set(record) - set(_REQUIRED_PACKAGE_FIELDS)
        if unknown:
            raise MaterializationError(f"unknown_package_plan_fields:{capability}:{','.join(sorted(unknown))}")
        package_id = _require_nonempty(record.get("package_id"), f"{capability}.package_id")
        version = _require_exact_version(record.get("version"), f"{capability}.version")
        digest = _require_sha256(record.get("sha256"), f"{capability}.sha256")
        source_id = _require_nonempty(record.get("source_id"), f"{capability}.source_id")
        source_ref = _require_nonempty(record.get("source_ref"), f"{capability}.source_ref")
        artifact_path = _relative_path(record.get("artifact_path"), f"{capability}.artifact_path")
        owner = _require_nonempty(record.get("owner"), f"{capability}.owner")
        trust_scope = _require_nonempty(record.get("trust_scope"), f"{capability}.trust_scope")
        provenance_ref = _require_nonempty(record.get("provenance_ref"), f"{capability}.provenance_ref")
        checks = record.get("admission_checks")
        if not isinstance(checks, dict) or set(checks) != set(_REQUIRED_ADMISSION_CHECKS):
            raise MaterializationError(f"package_admission_checks_incomplete:{capability}")
        if any(checks[check] is not True for check in _REQUIRED_ADMISSION_CHECKS):
            raise MaterializationError(f"package_admission_check_failed:{capability}")
        evidence_refs = record.get("evidence_refs")
        if not isinstance(evidence_refs, list) or not evidence_refs or not all(isinstance(item, str) and item.strip() for item in evidence_refs):
            raise MaterializationError(f"package_admission_evidence_required:{capability}")
        if source_id not in source_catalog:
            raise MaterializationError(f"package_source_not_admitted:{capability}:{source_id}")
        source = source_catalog[source_id]
        validated[capability] = {
            "package_id": package_id,
            "version": version,
            "sha256": digest,
            "source_id": source_id,
            "source_ref": source_ref,
            "artifact_path": artifact_path,
            "source_kind": str(source["source_kind"]),
            "owner": owner,
            "immutable_identity": source_ref,
            "content_digest": digest,
            "trust_scope": trust_scope,
            "provenance_ref": provenance_ref,
            "admission_checks": {check: True for check in _REQUIRED_ADMISSION_CHECKS},
            "evidence_refs": sorted(set(item.strip() for item in evidence_refs)),
        }
    return validated

def _resolve_archive(package_store: Path, relative: str) -> Path:
    candidate = package_store / Path(*PurePosixPath(relative).parts)
    if candidate.is_symlink():
        raise MaterializationError(f"package_archive_symlink_prohibited:{relative}")
    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise MaterializationError(f"package_archive_missing:{relative}") from exc
    try:
        resolved.relative_to(package_store)
    except ValueError as exc:
        raise MaterializationError(f"package_archive_escapes_store:{relative}") from exc
    if not resolved.is_file():
        raise MaterializationError(f"package_archive_must_be_file:{relative}")
    return resolved

def _safe_member_name(value: str) -> str:
    return _relative_path(value.rstrip("/"), "archive_member")

def _safe_symlink_target(member_name: str, target: str) -> str:
    if not target or "\\" in target:
        raise MaterializationError(f"invalid_symlink_target:{member_name}")
    pure = PurePosixPath(target)
    if pure.is_absolute():
        raise MaterializationError(f"absolute_symlink_prohibited:{member_name}:{target}")
    stack = list(PurePosixPath(member_name).parent.parts)
    for part in pure.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not stack:
                raise MaterializationError(f"escaping_symlink_prohibited:{member_name}:{target}")
            stack.pop()
        else:
            stack.append(part)
    return target

def _ensure_parents(root: Path, name: str, entries: dict[str, dict[str, Any]]) -> None:
    parts = PurePosixPath(name).parts[:-1]
    current: list[str] = []
    for part in parts:
        current.append(part)
        parent_name = PurePosixPath(*current).as_posix()
        existing = entries.get(parent_name)
        if existing is not None:
            if existing["kind"] != "directory":
                raise MaterializationError(f"archive_parent_not_directory:{name}:{parent_name}")
            continue
        path = root / Path(*current)
        path.mkdir(exist_ok=True)
        os.chmod(path, 0o755)
        entries[parent_name] = {"kind": "directory", "mode": 0o755, "explicit": False}

def _extract_archive(
    archive: Path,
    root: Path,
    entries: dict[str, dict[str, Any]],
    prohibited_prefixes: list[str],
) -> None:
    try:
        with tarfile.open(archive, mode="r:*") as tar:
            members = tar.getmembers()
            if len(members) > _MAX_ARCHIVE_MEMBERS:
                raise MaterializationError(f"archive_member_limit_exceeded:{archive.name}")
            normalized: list[tuple[str, tarfile.TarInfo]] = []
            names: set[str] = set()
            for member in members:
                name = _safe_member_name(member.name)
                if name in names:
                    raise MaterializationError(f"duplicate_archive_member:{archive.name}:{name}")
                names.add(name)
                if any(_is_under(name, prefix) for prefix in prohibited_prefixes):
                    raise MaterializationError(f"prohibited_rootfs_payload:{name}")
                normalized.append((name, member))

            for name, member in sorted(normalized, key=lambda item: (len(PurePosixPath(item[0]).parts), item[0])):
                _ensure_parents(root, name, entries)
                target = root / Path(*PurePosixPath(name).parts)
                mode = member.mode & 0o7777
                existing = entries.get(name)

                if member.isdir():
                    if existing is not None:
                        if existing["kind"] != "directory":
                            raise MaterializationError(f"package_path_collision:{name}")
                        if existing.get("explicit") and existing["mode"] != mode:
                            raise MaterializationError(f"directory_mode_collision:{name}")
                        os.chmod(target, mode)
                        entries[name] = {"kind": "directory", "mode": mode, "explicit": True}
                    else:
                        target.mkdir()
                        os.chmod(target, mode)
                        entries[name] = {"kind": "directory", "mode": mode, "explicit": True}
                    continue

                if existing is not None or target.exists() or target.is_symlink():
                    raise MaterializationError(f"package_path_collision:{name}")

                if member.isreg():
                    source = tar.extractfile(member)
                    if source is None:
                        raise MaterializationError(f"archive_file_unreadable:{name}")
                    with source, target.open("xb") as handle:
                        shutil.copyfileobj(source, handle, length=1024 * 1024)
                    os.chmod(target, mode)
                    entries[name] = {"kind": "file", "mode": mode, "explicit": True}
                elif member.issym():
                    link_target = _safe_symlink_target(name, member.linkname)
                    os.symlink(link_target, target)
                    entries[name] = {"kind": "symlink", "mode": 0o777, "explicit": True}
                else:
                    raise MaterializationError(f"unsupported_archive_member:{name}")
    except (tarfile.TarError, OSError) as exc:
        if isinstance(exc, MaterializationError):
            raise
        raise MaterializationError(f"archive_materialization_failed:{archive.name}:{exc}") from exc

def _iter_tree(root: Path) -> list[Path]:
    result: list[Path] = []
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        directories.sort()
        files.sort()
        current_path = Path(current)
        for directory in list(directories):
            path = current_path / directory
            if path.is_symlink():
                directories.remove(directory)
            result.append(path)
        for filename in files:
            result.append(current_path / filename)
    return sorted(result, key=lambda path: PurePosixPath(*path.relative_to(root).parts).as_posix())

def _normalize_tree_metadata(root: Path) -> None:
    paths = _iter_tree(root)
    for path in paths:
        if path.is_symlink():
            try:
                os.utime(path, (0, 0), follow_symlinks=False)
            except (NotImplementedError, OSError):
                pass
        elif path.is_file():
            os.utime(path, (0, 0))
    for path in sorted((item for item in paths if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
        os.utime(path, (0, 0))
    os.chmod(root, 0o755)
    os.utime(root, (0, 0))

def _tree_digest(root: Path) -> tuple[str, int]:
    digest = hashlib.sha256()
    count = 0
    for path in _iter_tree(root):
        relative = PurePosixPath(*path.relative_to(root).parts).as_posix()
        metadata = path.lstat()
        if stat.S_ISDIR(metadata.st_mode):
            record: dict[str, Any] = {"kind": "directory", "mode": f"{stat.S_IMODE(metadata.st_mode):04o}", "path": relative}
        elif stat.S_ISREG(metadata.st_mode):
            record = {
                "kind": "file",
                "mode": f"{stat.S_IMODE(metadata.st_mode):04o}",
                "path": relative,
                "sha256": _sha256_file(path),
                "size": metadata.st_size,
            }
        elif stat.S_ISLNK(metadata.st_mode):
            record = {"kind": "symlink", "mode": "0777", "path": relative, "target": os.readlink(path)}
        else:
            raise MaterializationError(f"special_file_prohibited:{relative}")
        digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        digest.update(b"\n")
        count += 1
    return digest.hexdigest(), count

def _write_json(path: Path, value: dict[str, Any]) -> None:
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

def materialize(args: argparse.Namespace) -> dict[str, Any]:
    if args.output_dir.exists():
        raise MaterializationError("output_dir_must_not_exist")
    package_store = args.package_store.resolve(strict=True)
    if not package_store.is_dir() or args.package_store.is_symlink():
        raise MaterializationError("package_store_must_be_non_symlink_directory")

    base, base_raw = _load_json_document(args.base_packages)
    plan, plan_raw = _load_json_document(args.package_plan)
    policy, policy_raw = _load_toml_document(args.package_sources)
    source_catalog = _source_catalog(policy)
    resolved = _validate_plan(base, plan, source_catalog)
    _, prohibited_prefixes = _base_requirements(base)

    args.output_dir.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{args.output_dir.name}.stage-", dir=args.output_dir.parent))
    try:
        rootfs = stage / "rootfs"
        rootfs.mkdir(mode=0o755)
        entries: dict[str, dict[str, Any]] = {}
        for capability in sorted(resolved):
            record = resolved[capability]
            archive = _resolve_archive(package_store, record["artifact_path"])
            actual_digest = _sha256_file(archive)
            if actual_digest != record["sha256"]:
                raise MaterializationError(f"package_digest_mismatch:{capability}")
            _extract_archive(archive, rootfs, entries, prohibited_prefixes)

        _normalize_tree_metadata(rootfs)
        tree_sha256, entry_count = _tree_digest(rootfs)
        resolution = {
            "schema_version": 1,
            "package_set_id": base["package_set_id"],
            "profile_id": base["profile_id"],
            "capabilities": resolved,
            "materialization": {
                "status": "materialized",
                "network_accessed": False,
                "candidate_code_executed": False,
                "base_packages_sha256": _sha256_bytes(base_raw),
                "package_plan_sha256": _sha256_bytes(plan_raw),
                "package_sources_sha256": _sha256_bytes(policy_raw),
                "rootfs_tree_sha256": tree_sha256,
                "rootfs_entry_count": entry_count,
            },
        }
        _write_json(stage / "package-resolution.json", resolution)
        os.replace(stage, args.output_dir)
        return resolution
    except Exception:
        shutil.rmtree(stage, ignore_errors=True)
        raise

def main(argv: list[str] | None = None) -> int:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-plan", type=Path, required=True)
    parser.add_argument("--package-store", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--base-packages", type=Path, default=Path(__file__).with_name("base-packages.yaml"))
    parser.add_argument("--package-sources", type=Path, default=repository_root / "packaging/system/package-sources.toml")
    args = parser.parse_args(argv)
    try:
        materialize(args)
        return 0
    except (OSError, MaterializationError) as exc:
        print(f"rootfs materialization failed: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
