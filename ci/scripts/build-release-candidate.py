#!/usr/bin/env python3
"""Build one deterministic release-candidate archive after every gate passes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


class CandidateError(RuntimeError):
    """Raised when candidate construction must fail closed."""


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CandidateError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_reject_duplicates)
    except (OSError, json.JSONDecodeError) as exc:
        raise CandidateError(f"cannot load JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CandidateError(f"JSON root must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CandidateError(f"{label} must be a non-empty string")
    return value


def require_string_list(value: Any, label: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise CandidateError(f"{label} must be an array of non-empty strings")
    if nonempty and not value:
        raise CandidateError(f"{label} must not be empty")
    if len(value) != len(set(value)):
        raise CandidateError(f"{label} contains duplicates")
    return value


def parse_time(value: Any, label: str) -> datetime:
    text = require_string(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CandidateError(f"{label} is not RFC3339-compatible: {text}") from exc
    if parsed.tzinfo is None:
        raise CandidateError(f"{label} must include a timezone")
    return parsed.astimezone(timezone.utc)


def safe_relative_path(value: str, label: str) -> PurePosixPath:
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or not candidate.parts or any(part in {"", ".", ".."} for part in candidate.parts):
        raise CandidateError(f"{label} must be a normalized relative path: {value}")
    return candidate


def resolve_input(root: Path, value: str, label: str) -> tuple[Path, PurePosixPath]:
    relative = safe_relative_path(value, label)
    root_resolved = root.resolve(strict=True)
    path = (root_resolved / Path(*relative.parts)).resolve(strict=True)
    try:
        path.relative_to(root_resolved)
    except ValueError as exc:
        raise CandidateError(f"{label} escapes the input root: {value}") from exc
    if not path.is_file() or path.is_symlink():
        raise CandidateError(f"{label} must identify a regular non-symlink file: {value}")
    return path, relative


def validate_schema(instance: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
    except ImportError as exc:
        raise CandidateError("jsonschema is required to validate the Release Set") from exc
    schema = load_json(schema_path)
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(instance)
    except jsonschema.ValidationError as exc:
        where = "/".join(str(part) for part in exc.absolute_path) or "<root>"
        raise CandidateError(f"Release Set schema failure at {where}: {exc.message}") from exc


def validate_release_set(release_set: dict[str, Any], policy: dict[str, Any], schema_path: Path) -> tuple[str, str]:
    validate_schema(release_set, schema_path)
    candidate_policy = policy["candidate"]
    release_set_id = require_string(release_set.get("release_set_id"), "release_set.release_set_id")
    if release_set.get("artifact_class") != "release_set":
        raise CandidateError("release_set.artifact_class must be release_set")
    if release_set.get("lifecycle_status") not in {"candidate", "validated"}:
        raise CandidateError("release candidate lifecycle_status must be candidate or validated")
    required_channels = set(candidate_policy["required_channel_ids"])
    channels = release_set.get("channels")
    if not isinstance(channels, dict) or set(channels) != required_channels:
        raise CandidateError(f"release_set.channels must contain exactly {sorted(required_channels)}")
    for channel_id, channel in channels.items():
        if not isinstance(channel, dict) or channel.get("channel_id") != channel_id:
            raise CandidateError(f"channel {channel_id} has a mismatched embedded channel_id")
    compatibility = release_set.get("compatibility", {})
    if compatibility.get("status") != candidate_policy["required_compatibility_status"]:
        raise CandidateError("Release Set compatibility is not tested_compatible")
    for result in compatibility.get("constraint_results", []):
        if not isinstance(result, dict) or result.get("result") != "pass":
            raise CandidateError("every compatibility constraint must pass")
    activation = release_set.get("activation", {})
    if activation.get("eligibility") != candidate_policy["required_activation_eligibility"]:
        raise CandidateError("Release Set is not eligible for activation")
    if activation.get("partial_activation_allowed") is not candidate_policy["partial_activation_allowed"]:
        raise CandidateError("partial activation policy mismatch")
    signature = release_set.get("signature", {})
    if signature.get("verification_status") != candidate_policy["required_signature_status"]:
        raise CandidateError("Release Set signature is not verified")
    release_set_sha = sha256_bytes(canonical_bytes(release_set))
    return release_set_id, release_set_sha


GIT_TIMEOUT_SECONDS = 30
_GIT_ENVIRONMENT_KEYS = (
    "PATH",
    "HOME",
    "USERPROFILE",
    "SYSTEMROOT",
    "WINDIR",
    "TMPDIR",
    "TEMP",
    "TMP",
)


def _minimal_git_environment() -> dict[str, str]:
    return {
        key: os.environ[key]
        for key in _GIT_ENVIRONMENT_KEYS
        if key in os.environ and os.environ[key]
    }


def git_output(root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            env=_minimal_git_environment(),
            text=True,
            capture_output=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except FileNotFoundError as exc:
        raise CandidateError("git executable is unavailable") from exc
    except subprocess.TimeoutExpired as exc:
        raise CandidateError(f"git {' '.join(args)} exceeded the bounded timeout") from exc
    if proc.returncode != 0:
        raise CandidateError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def validate_source(root: Path, source_revision: str, pattern: str) -> None:
    if re.fullmatch(pattern, source_revision) is None:
        raise CandidateError("source revision must be a full lowercase immutable Git SHA")
    if git_output(root, "rev-parse", "HEAD") != source_revision:
        raise CandidateError("source revision does not match repository HEAD")
    status = git_output(root, "status", "--porcelain=v1", "--untracked-files=all")
    if status:
        raise CandidateError("repository contains mutable or untracked release inputs: " + "; ".join(status.splitlines()))


def control_path(root: Path, path: Path, label: str, *, directory: bool = False) -> Path:
    root_resolved = root.resolve(strict=True)
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise CandidateError(f"{label} must be inside the declared input root") from exc
    if resolved.is_symlink() or (directory and not resolved.is_dir()) or (not directory and not resolved.is_file()):
        expected = "directory" if directory else "regular file"
        raise CandidateError(f"{label} must be a non-symlink {expected}")
    return resolved


def validate_dependency_files(root: Path, policy: dict[str, Any]) -> None:
    missing: list[str] = []
    for bundle_id, paths in policy["required_dependencies"].items():
        for relative in paths:
            if not (root / relative).is_file():
                missing.append(f"{bundle_id}:{relative}")
    if missing:
        raise CandidateError("required dependency files are missing: " + ", ".join(missing))


def validate_manifest(
    path: Path,
    *,
    kind: str,
    release_set_ref: str,
    source_revision: str,
    input_root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    manifest = load_json(path)
    if manifest.get("schema_version") != "1.0.0":
        raise CandidateError(f"{kind} manifest schema_version must be 1.0.0")
    if manifest.get("release_set_ref") != release_set_ref:
        raise CandidateError(f"{kind} manifest refers to another Release Set")
    if manifest.get("source_revision") != source_revision:
        raise CandidateError(f"{kind} manifest refers to another source revision")
    key = "artifacts" if kind == "artifact" else "evidence"
    id_key = "artifact_id" if kind == "artifact" else "evidence_id"
    items = manifest.get(key)
    if not isinstance(items, list) or not items:
        raise CandidateError(f"{kind} manifest {key} must be a non-empty array")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    checked: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise CandidateError(f"{kind} manifest item {index} must be an object")
        item_id = require_string(item.get(id_key), f"{kind}[{index}].{id_key}")
        source_path = require_string(item.get("path"), f"{kind}[{index}].path")
        expected_sha = require_string(item.get("sha256"), f"{kind}[{index}].sha256")
        if re.fullmatch(r"[0-9a-f]{64}", expected_sha) is None:
            raise CandidateError(f"{kind}[{index}].sha256 is invalid")
        if item_id in seen_ids or source_path in seen_paths:
            raise CandidateError(f"duplicate {kind} identity or path: {item_id}")
        seen_ids.add(item_id)
        seen_paths.add(source_path)
        actual_path, relative = resolve_input(input_root, source_path, f"{kind}[{index}].path")
        actual_sha = sha256_file(actual_path)
        if actual_sha != expected_sha:
            raise CandidateError(f"digest mismatch for {source_path}: expected {expected_sha}, got {actual_sha}")
        size = actual_path.stat().st_size
        if item.get("size") != size:
            raise CandidateError(f"size mismatch for {source_path}: expected {item.get('size')}, got {size}")
        checked.append({**item, "_source": actual_path, "_relative": relative})
    return manifest, checked


def validate_gates(
    gate_dir: Path,
    policy: dict[str, Any],
    *,
    release_set_ref: str,
    release_set_sha: str,
    source_revision: str,
    evidence_ids: set[str],
    now: datetime,
) -> tuple[list[dict[str, Any]], str]:
    gate_policy = policy["gate_results"]
    order: list[str] = gate_policy["mandatory_order"]
    order_index = {gate_class: index for index, gate_class in enumerate(order)}
    required_fields = set(gate_policy["required_fields"])
    entries = sorted(gate_dir.iterdir(), key=lambda item: item.name)
    unexpected = [item.name for item in entries if item.is_symlink() or not item.is_file() or item.suffix != ".json"]
    if unexpected:
        raise CandidateError(f"gate result directory contains unexpected entries: {unexpected}")
    files = entries
    if not files:
        raise CandidateError("no gate result files were found")
    by_class: dict[str, dict[str, Any]] = {}
    for path in files:
        gate = load_json(path)
        missing = sorted(required_fields - set(gate))
        if missing:
            raise CandidateError(f"{path} is missing required fields: {missing}")
        gate_class = require_string(gate["gate_class"], f"{path}.gate_class")
        if gate_class not in order_index:
            raise CandidateError(f"unknown or non-mandatory gate class: {gate_class}")
        if gate_class in by_class:
            raise CandidateError(f"duplicate gate class: {gate_class}")
        if gate["release_set_ref"] != release_set_ref or gate["release_set_sha256"] != release_set_sha:
            raise CandidateError(f"gate {gate_class} is bound to another Release Set")
        if gate["source_revision"] != source_revision:
            raise CandidateError(f"gate {gate_class} is bound to another source revision")
        result = gate["result"]
        if result not in gate_policy["allowed_results"]:
            raise CandidateError(f"gate {gate_class} has an unknown result: {result}")
        if result not in gate_policy["release_eligible_results"]:
            raise CandidateError(f"gate {gate_class} is not release eligible: {result}")
        dependencies = require_string_list(gate["dependencies"], f"gate {gate_class}.dependencies")
        for dependency in dependencies:
            if dependency not in order_index or order_index[dependency] >= order_index[gate_class]:
                raise CandidateError(f"gate {gate_class} has an invalid dependency: {dependency}")
        require_string_list(gate["profile_refs"], f"gate {gate_class}.profile_refs")
        require_string(gate["scope"], f"gate {gate_class}.scope")
        require_string(gate["evaluator"], f"gate {gate_class}.evaluator")
        require_string_list(gate["executed_checks"], f"gate {gate_class}.executed_checks", nonempty=True)
        require_string_list(gate["reason_codes"], f"gate {gate_class}.reason_codes")
        exception_refs = require_string_list(gate["exception_refs"], f"gate {gate_class}.exception_refs")
        approval_refs = require_string_list(gate["approval_refs"], f"gate {gate_class}.approval_refs")
        require_string_list(gate["test_refs"], f"gate {gate_class}.test_refs")
        refs = require_string_list(gate["evidence_refs"], f"gate {gate_class}.evidence_refs", nonempty=True)
        unknown_evidence = sorted(set(refs) - evidence_ids)
        if unknown_evidence:
            raise CandidateError(f"gate {gate_class} references unmanifested evidence: {unknown_evidence}")
        started = parse_time(gate["started_at"], f"gate {gate_class}.started_at")
        finished = parse_time(gate["finished_at"], f"gate {gate_class}.finished_at")
        valid_until = parse_time(gate["valid_until"], f"gate {gate_class}.valid_until")
        if finished < started or valid_until <= finished:
            raise CandidateError(f"gate {gate_class} has an invalid validity interval")
        if valid_until <= now:
            raise CandidateError(f"gate {gate_class} evidence is expired")
        require_string_list(gate["invalidation_triggers"], f"gate {gate_class}.invalidation_triggers", nonempty=True)
        require_string(gate["receipt_ref"], f"gate {gate_class}.receipt_ref")
        if result == "waived_by_approved_exception":
            waiver = gate_policy["waiver_requirements"]
            if gate_class in waiver["prohibited_gate_classes"]:
                raise CandidateError(f"gate {gate_class} cannot be waived")
            if len(exception_refs) < waiver["exception_refs_min_items"] or len(approval_refs) < waiver["approval_refs_min_items"]:
                raise CandidateError(f"gate {gate_class} waiver lacks exception or approval authority")
        elif exception_refs:
            raise CandidateError(f"gate {gate_class} has exception refs but is not waived")
        by_class[gate_class] = gate
    missing_classes = [gate_class for gate_class in order if gate_class not in by_class]
    if missing_classes:
        raise CandidateError(f"mandatory gate results are missing: {missing_classes}")
    for gate_class in order:
        for dependency in by_class[gate_class]["dependencies"]:
            if by_class[dependency]["result"] not in gate_policy["release_eligible_results"]:
                raise CandidateError(f"gate dependency {dependency} is not eligible for {gate_class}")
    decision = "approved_with_exceptions" if any(g["result"] == "waived_by_approved_exception" for g in by_class.values()) else "approved"
    return [by_class[gate_class] for gate_class in order], decision


def add_bytes(archive: tarfile.TarFile, name: str, data: bytes, epoch: int) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mtime = epoch
    info.mode = 0o644
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    import io
    archive.addfile(info, io.BytesIO(data))


def add_file(archive: tarfile.TarFile, name: str, path: Path, epoch: int) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = path.stat().st_size
    info.mtime = epoch
    info.mode = 0o644
    info.uid = info.gid = 0
    info.uname = info.gname = "root"
    with path.open("rb") as stream:
        archive.addfile(info, stream)


def rooted(base: Path, path: Path) -> Path:
    return path if path.is_absolute() else base / path
def build(args: argparse.Namespace) -> dict[str, Any]:
    root = args.repository_root.resolve(strict=True)
    input_root = rooted(root, args.input_root).resolve(strict=True)
    policy_path = control_path(root, rooted(root, args.policy), "policy")
    policy = load_json(policy_path)
    validate_source(root, args.source_revision, policy["candidate"]["source_revision_pattern"])
    validate_dependency_files(root, policy)
    release_set_path = control_path(input_root, rooted(input_root, args.release_set), "release_set")
    artifacts_manifest_path = control_path(input_root, rooted(input_root, args.artifacts_manifest), "artifacts_manifest")
    evidence_manifest_path = control_path(input_root, rooted(input_root, args.evidence_manifest), "evidence_manifest")
    gate_results_path = control_path(input_root, rooted(input_root, args.gate_results), "gate_results", directory=True)
    release_set = load_json(release_set_path)
    policy_sha = sha256_bytes(canonical_bytes(policy))
    schema_path = root / policy["candidate"]["release_set_schema"]
    release_set_ref, release_set_sha = validate_release_set(release_set, policy, schema_path)
    artifact_manifest, artifacts = validate_manifest(
        artifacts_manifest_path,
        kind="artifact",
        release_set_ref=release_set_ref,
        source_revision=args.source_revision,
        input_root=input_root,
    )
    evidence_manifest, evidence = validate_manifest(
        evidence_manifest_path,
        kind="evidence",
        release_set_ref=release_set_ref,
        source_revision=args.source_revision,
        input_root=input_root,
    )
    evidence_classes = {item.get("evidence_class") for item in evidence}
    missing_evidence_classes = sorted(set(policy["required_evidence_classes"]) - evidence_classes)
    if missing_evidence_classes:
        raise CandidateError(f"required evidence classes are missing: {missing_evidence_classes}")
    now = parse_time(args.evaluated_at, "evaluated_at") if args.evaluated_at else datetime.now(timezone.utc)
    gates, release_decision = validate_gates(
        gate_results_path,
        policy,
        release_set_ref=release_set_ref,
        release_set_sha=release_set_sha,
        source_revision=args.source_revision,
        evidence_ids={item["evidence_id"] for item in evidence},
        now=now,
    )
    epoch = args.source_date_epoch
    if epoch < 0:
        raise CandidateError("SOURCE_DATE_EPOCH must be non-negative")
    entries: list[dict[str, Any]] = []
    for kind, records in (("artifacts", artifacts), ("evidence", evidence)):
        for item in records:
            archive_path = f"payload/{kind}/{item['_relative'].as_posix()}"
            entries.append({
                "kind": kind[:-1],
                "id": item["artifact_id"] if kind == "artifacts" else item["evidence_id"],
                "archive_path": archive_path,
                "sha256": item["sha256"],
                "size": item["size"],
            })
    entries.sort(key=lambda item: item["archive_path"])
    subject = {
        "schema_version": "1.0.0",
        "release_set_ref": release_set_ref,
        "release_set_sha256": release_set_sha,
        "source_revision": args.source_revision,
        "source_date_epoch": epoch,
        "release_decision": release_decision,
        "gate_policy": {
            "policy_id": policy["policy_id"],
            "policy_version": policy["policy_version"],
            "sha256": policy_sha,
        },
        "gate_results": [
            {
                "gate_id": gate["gate_id"],
                "gate_version": gate["gate_version"],
                "gate_class": gate["gate_class"],
                "result": gate["result"],
                "receipt_ref": gate["receipt_ref"],
                "evidence_refs": gate["evidence_refs"],
                "valid_until": gate["valid_until"],
            }
            for gate in gates
        ],
        "entries": entries,
        "activation_authorized": False,
    }
    subject_sha = sha256_bytes(canonical_bytes(subject))
    candidate_id = f"{release_set_ref}.{subject_sha[:16]}"
    output = rooted(root, args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="koa-candidate-", dir=str(output.parent)) as tmp_name:
        tmp = Path(tmp_name)
        archive_path = tmp / "release-candidate.tar"
        byte_entries: dict[str, bytes] = {
            "metadata/candidate-subject.json": canonical_bytes(subject),
            "metadata/release-set.json": canonical_bytes(release_set),
            "metadata/artifacts-manifest.json": canonical_bytes(artifact_manifest),
            "metadata/evidence-manifest.json": canonical_bytes(evidence_manifest),
        }
        byte_entries.update({f"metadata/gates/{gate['gate_class']}.json": canonical_bytes(gate) for gate in gates})
        file_entries = {f"payload/artifacts/{item['_relative'].as_posix()}": item["_source"] for item in artifacts}
        file_entries.update({f"payload/evidence/{item['_relative'].as_posix()}": item["_source"] for item in evidence})
        all_names = sorted(set(byte_entries) | set(file_entries))
        if len(all_names) != len(byte_entries) + len(file_entries):
            raise CandidateError("archive entry collision")
        with tarfile.open(archive_path, "w", format=tarfile.USTAR_FORMAT) as archive:
            for name in all_names:
                if name in byte_entries:
                    add_bytes(archive, name, byte_entries[name], epoch)
                else:
                    add_file(archive, name, file_entries[name], epoch)
        archive_sha = sha256_file(archive_path)
        manifest = {
            "schema_version": "1.0.0",
            "candidate_id": candidate_id,
            "release_set_ref": release_set_ref,
            "release_set_sha256": release_set_sha,
            "source_revision": args.source_revision,
            "release_decision": release_decision,
            "gate_policy": {
                "policy_id": policy["policy_id"],
                "policy_version": policy["policy_version"],
                "sha256": policy_sha,
            },
            "subject_manifest_sha256": subject_sha,
            "archive": {"path": "release-candidate.tar", "sha256": archive_sha, "size": archive_path.stat().st_size},
            "gate_count": len(gates),
            "entry_count": len(entries),
            "activation_authorized": False,
        }
        (tmp / "release-candidate-manifest.json").write_bytes(canonical_bytes(manifest))
        (tmp / "release-candidate.sha256").write_text(f"{archive_sha}  release-candidate.tar\n", encoding="ascii")
        if output.exists():
            if not args.replace_output:
                raise CandidateError(f"output already exists: {output}")
            shutil.rmtree(output)
        os.replace(tmp, output)
    return manifest


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--input-root", type=Path, default=Path.cwd())
    parser.add_argument("--policy", type=Path, default=Path("ci/policies/release-gates.json"))
    parser.add_argument("--release-set", type=Path, required=True)
    parser.add_argument("--gate-results", type=Path, required=True)
    parser.add_argument("--artifacts-manifest", type=Path, required=True)
    parser.add_argument("--evidence-manifest", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--source-date-epoch", type=int, required=True)
    parser.add_argument("--evaluated-at")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replace-output", action="store_true")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    try:
        manifest = build(parse_args(argv))
    except CandidateError as exc:
        print(f"build-release-candidate: blocked: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
