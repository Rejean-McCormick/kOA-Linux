#!/usr/bin/env python3
"""Build a deterministic rootfs tar from an already admitted materialized tree."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import stat
import sys
import tarfile
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


class BuildError(ValueError):
    """Raised when the rootfs input violates the build definition."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuildError(f"duplicate_key:{key}")
        result[key] = value
    return result


def _load_document(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) > 16 * 1024 * 1024:
        raise BuildError(f"input_too_large:{path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BuildError(f"document_must_be_json_compatible_yaml:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise BuildError(f"expected_object:{path}")
    return value, raw


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _safe_archive_name(relative: Path) -> str:
    name = PurePosixPath(*relative.parts).as_posix()
    if not name or name == "." or name.startswith("/") or ".." in PurePosixPath(name).parts:
        raise BuildError(f"unsafe_archive_path:{relative}")
    return name


def _safe_symlink_target(entry: Path, target: str) -> None:
    pure = PurePosixPath(target)
    if pure.is_absolute():
        raise BuildError(f"absolute_symlink_prohibited:{entry}:{target}")
    stack = list(PurePosixPath(*entry.parent.parts).parts)
    for part in pure.parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if not stack:
                raise BuildError(f"escaping_symlink_prohibited:{entry}:{target}")
            stack.pop()
        else:
            stack.append(part)


def _normalized_prefix(value: str) -> str:
    pure = PurePosixPath(value)
    if not pure.is_absolute() or ".." in pure.parts:
        raise BuildError(f"invalid_absolute_prefix:{value}")
    return pure.as_posix().rstrip("/") or "/"


def _relative_to_root(value: str) -> str:
    return _normalized_prefix(value).lstrip("/")


def _is_under(name: str, prefix: str) -> bool:
    clean = name.rstrip("/")
    return clean == prefix or clean.startswith(prefix + "/")


def _iter_source(root: Path) -> Iterable[Path]:
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        directories.sort()
        files.sort()
        current_path = Path(current)
        for directory in list(directories):
            path = current_path / directory
            if path.is_symlink():
                directories.remove(directory)
                yield path
            else:
                yield path
        for filename in files:
            yield current_path / filename


def _tar_info(name: str, mode: int, epoch: int, kind: str, size: int = 0, linkname: str = "") -> tarfile.TarInfo:
    info = tarfile.TarInfo(name=name)
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = epoch
    info.mode = mode & 0o7777
    info.size = size
    if kind == "directory":
        info.type = tarfile.DIRTYPE
    elif kind == "symlink":
        info.type = tarfile.SYMTYPE
        info.linkname = linkname
    elif kind == "file":
        info.type = tarfile.REGTYPE
    else:
        raise BuildError(f"unsupported_tar_kind:{kind}")
    return info


def _validate_package_resolution(base: dict[str, Any], resolution: dict[str, Any]) -> None:
    required = base.get("required_capabilities")
    if not isinstance(required, list) or not required:
        raise BuildError("base_package_capabilities_missing")
    resolved = resolution.get("capabilities")
    if not isinstance(resolved, dict):
        raise BuildError("package_resolution_capabilities_missing")
    expected = {item.get("id") for item in required if isinstance(item, dict)}
    if None in expected or len(expected) != len(required):
        raise BuildError("invalid_base_package_capability")
    if set(resolved) != expected:
        raise BuildError("package_resolution_must_match_required_capabilities_exactly")
    for capability, record in resolved.items():
        if not isinstance(record, dict):
            raise BuildError(f"invalid_package_resolution:{capability}")
        digest = record.get("sha256")
        if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise BuildError(f"invalid_package_digest:{capability}")
        reference = record.get("source_ref")
        if not isinstance(reference, str) or not reference.strip():
            raise BuildError(f"package_source_ref_required:{capability}")


def build(args: argparse.Namespace) -> dict[str, Any]:
    source_root = args.source_root.resolve(strict=True)
    if not source_root.is_dir():
        raise BuildError("source_root_must_be_directory")
    if source_root == Path("/"):
        raise BuildError("source_root_must_not_be_host_root")
    if args.source_date_epoch < 0:
        raise BuildError("source_date_epoch_must_be_nonnegative")

    base, base_raw = _load_document(args.base_packages)
    layout, layout_raw = _load_document(args.filesystem_layout)
    partition, partition_raw = _load_document(args.partition_layout)
    definition, definition_raw = _load_document(args.image_manifest)
    resolution, resolution_raw = _load_document(args.package_resolution)
    _validate_package_resolution(base, resolution)

    if definition.get("artifact_class") != "system_image" or definition.get("release_channel") != "system":
        raise BuildError("image_definition_identity_mismatch")
    build_policy = definition.get("build")
    if not isinstance(build_policy, dict) or build_policy.get("execute_candidate_code") is not False:
        raise BuildError("candidate_code_execution_must_be_disabled")
    if build_policy.get("source_date_epoch_required") is not True:
        raise BuildError("source_date_epoch_requirement_missing")
    if partition.get("mechanism") != "inactive_slot":
        raise BuildError("unsupported_partition_mechanism")

    prohibited = definition.get("prohibited_payload_prefixes")
    if not isinstance(prohibited, list) or not prohibited:
        raise BuildError("prohibited_payload_prefixes_missing")
    prohibited_relative = [_relative_to_root(str(item)) for item in prohibited]

    entries = layout.get("entries")
    if not isinstance(entries, list):
        raise BuildError("filesystem_entries_missing")
    declared_directories: dict[str, int] = {}
    for entry in entries:
        if not isinstance(entry, dict) or entry.get("kind") != "directory":
            raise BuildError("only_directory_layout_entries_supported")
        name = _relative_to_root(str(entry.get("path")))
        mode_text = entry.get("mode")
        try:
            mode = int(mode_text, 8)
        except (TypeError, ValueError) as exc:
            raise BuildError(f"invalid_layout_mode:{name}") from exc
        if not entry.get("runtime_only") and not any(_is_under(name, prefix) for prefix in prohibited_relative):
            declared_directories[name] = mode

    args.output_dir.mkdir(parents=True, exist_ok=True)
    archive = args.output_dir / args.archive_name
    manifest_path = args.output_dir / args.build_manifest_name
    temporary_archive = archive.with_name(f".{archive.name}.tmp-{os.getpid()}")

    seen: set[str] = set()
    file_count = 0
    total_bytes = 0
    with tarfile.open(temporary_archive, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for path in _iter_source(source_root):
            relative = path.relative_to(source_root)
            name = _safe_archive_name(relative)
            if any(_is_under(name, prefix) for prefix in prohibited_relative):
                raise BuildError(f"prohibited_mutable_payload:{name}")
            metadata = path.lstat()
            if stat.S_ISDIR(metadata.st_mode):
                info = _tar_info(name + "/", stat.S_IMODE(metadata.st_mode), args.source_date_epoch, "directory")
                tar.addfile(info)
            elif stat.S_ISREG(metadata.st_mode):
                info = _tar_info(name, stat.S_IMODE(metadata.st_mode), args.source_date_epoch, "file", metadata.st_size)
                with path.open("rb") as handle:
                    tar.addfile(info, handle)
                file_count += 1
                total_bytes += metadata.st_size
            elif stat.S_ISLNK(metadata.st_mode):
                target = os.readlink(path)
                _safe_symlink_target(relative, target)
                info = _tar_info(name, stat.S_IMODE(metadata.st_mode), args.source_date_epoch, "symlink", linkname=target)
                tar.addfile(info)
            else:
                raise BuildError(f"special_file_prohibited:{name}")
            seen.add(name.rstrip("/"))

        for name, mode in sorted(declared_directories.items()):
            if name not in seen:
                tar.addfile(_tar_info(name + "/", mode, args.source_date_epoch, "directory"))
                seen.add(name)

    os.replace(temporary_archive, archive)
    archive_digest = _sha256_file(archive)
    build_manifest = {
        "schema_version": 1,
        "artifact_class": "system_image_rootfs",
        "profile_id": definition.get("profile_id"),
        "archive": {
            "path": archive.name,
            "format": "deterministic-tar",
            "sha256": archive_digest,
            "size_bytes": archive.stat().st_size,
            "file_count": file_count,
            "payload_bytes": total_bytes,
        },
        "source_date_epoch": args.source_date_epoch,
        "inputs": {
            "base_packages_sha256": _sha256_bytes(base_raw),
            "filesystem_layout_sha256": _sha256_bytes(layout_raw),
            "partition_layout_sha256": _sha256_bytes(partition_raw),
            "image_manifest_sha256": _sha256_bytes(definition_raw),
            "package_resolution_sha256": _sha256_bytes(resolution_raw),
        },
        "candidate_code_executed": False,
        "component_owned_state_included": False,
    }
    _atomic_json(manifest_path, build_manifest)
    return build_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--base-packages", type=Path, default=Path(__file__).with_name("base-packages.yaml"))
    parser.add_argument("--filesystem-layout", type=Path, default=Path(__file__).with_name("filesystem-layout.yaml"))
    parser.add_argument("--partition-layout", type=Path, default=Path(__file__).with_name("partition-layout.yaml"))
    parser.add_argument("--image-manifest", type=Path, default=Path(__file__).with_name("image-manifest.yaml"))
    parser.add_argument("--package-resolution", type=Path, required=True)
    parser.add_argument("--source-date-epoch", type=int, default=None)
    parser.add_argument("--archive-name", default="koa-rootfs.tar")
    parser.add_argument("--build-manifest-name", default="rootfs-build.json")
    args = parser.parse_args(argv)
    if args.source_date_epoch is None:
        epoch = os.environ.get("SOURCE_DATE_EPOCH")
        if epoch is None:
            parser.error("--source-date-epoch or SOURCE_DATE_EPOCH is required")
        try:
            args.source_date_epoch = int(epoch)
        except ValueError:
            parser.error("SOURCE_DATE_EPOCH must be an integer")
    try:
        build(args)
        return 0
    except (OSError, BuildError, tarfile.TarError) as exc:
        print(f"rootfs build failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
