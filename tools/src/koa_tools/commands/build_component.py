"""Build canonical upstream component bundles without granting activation authority."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import tomllib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from koa_tools.process import ProcessError, ProcessResult, run_process
from koa_tools.repository import Repository, RepositoryError

from . import CommandDefinition, CommandError, add_repository_options, repository_path, source_date_epoch

BUNDLE_FORMAT = "koa.component-build-bundle"
BUNDLE_VERSION = "1.0.0"
GENERATOR_ID = "koa_tools.commands.build_component"
COMPONENT_MANIFESTS = {
    "audit-broker": "packaging/components/audit-broker.toml",
    "governance-policy-runtime": "packaging/components/governance-policy-runtime.toml",
    "identity-and-trust": "packaging/components/identity-and-trust.toml",
    "koa-mediatheque": "packaging/components/koa-mediatheque.toml",
    "koa-node-agent": "packaging/components/koa-node-agent.toml",
    "kristal-runtime": "packaging/components/kristal-runtime.toml",
    "publication-gateway": "packaging/components/publication-gateway.toml",
    "resource-governor": "packaging/components/resource-governor.toml",
}
SUPPORTED_BUILD_KINDS = {"python_wheel", "rust_binaries"}
NODE_DESTINATIONS = {
    "/usr/bin/koa-node-agentctl",
    "/usr/libexec/koa/koa-node-agent",
    "/usr/libexec/koa/koa-privileged-broker",
}


class ComponentBuildError(CommandError):
    """A fail-closed component bundle configuration or build error."""


@dataclass(frozen=True, slots=True)
class PayloadEntry:
    source: str
    destination: str
    mode: str | None


@dataclass(frozen=True, slots=True)
class BuildSpec:
    slug: str
    component_id: str
    package_ref: str
    payload_ref: str
    contract_ref: str
    project_ref: str
    source_root: str
    lock_ref: str
    output_ref: str
    release_channel: str
    artifact_class: str
    build_kind: str
    version: str
    project_version: str
    entries: tuple[PayloadEntry, ...]
    package: Mapping[str, Any]


def _toml(path: Path, label: str) -> dict[str, Any]:
    if path.is_symlink():
        raise ComponentBuildError(f"{label} must not be a symbolic link: {path}")
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ComponentBuildError(f"cannot load {label} {path}: {exc}") from exc


def _json(path: Path, label: str) -> dict[str, Any]:
    if path.is_symlink():
        raise ComponentBuildError(f"{label} must not be a symbolic link: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ComponentBuildError(f"cannot load {label} {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ComponentBuildError(f"{label} must contain an object: {path}")
    return value


def _text(value: Mapping[str, Any], key: str, location: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip() or item != item.strip() or "\0" in item:
        raise ComponentBuildError(f"{location}.{key} must be a non-empty canonical string")
    return item


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise ComponentBuildError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def _canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical(value))


def _entries(payload: Mapping[str, Any]) -> tuple[PayloadEntry, ...]:
    raw = payload.get("include", payload.get("payload"))
    if not isinstance(raw, list) or not raw:
        raise ComponentBuildError("payload manifest must declare [[include]] or [[payload]] entries")
    entries: list[PayloadEntry] = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ComponentBuildError(f"payload entry {index} must be a table")
        source = _text(item, "source", f"payload[{index}]")
        destination = _text(item, "destination", f"payload[{index}]")
        if item.get("mutable", False) is not False:
            raise ComponentBuildError(f"mutable payload entry is prohibited: {source}")
        if not isinstance(item.get("kind", item.get("class")), str):
            raise ComponentBuildError(f"payload[{index}] must declare kind or class")
        mode = item.get("mode")
        if mode is not None and not isinstance(mode, str):
            raise ComponentBuildError(f"payload[{index}].mode must be a string")
        entries.append(PayloadEntry(source, destination, mode))
    return tuple(entries)


def _safe_tree(path: Path) -> None:
    candidates = [path] if path.is_file() else path.rglob("*")
    for candidate in candidates:
        mode = candidate.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ComponentBuildError(f"symbolic links are prohibited in payloads: {candidate}")
        if not stat.S_ISDIR(mode) and not stat.S_ISREG(mode):
            raise ComponentBuildError(f"special files are prohibited in payloads: {candidate}")


def _validate_role(spec: BuildSpec) -> None:
    if spec.component_id == "koa_node_agent":
        expected = ("system", "system_image", "rust_binaries")
        if (spec.release_channel, spec.artifact_class, spec.build_kind) != expected:
            raise ComponentBuildError("koa_node_agent must remain the declared system-channel Rust fragment")
        fixed = spec.package.get("payload", {}).get("fixed_destination", [])
        declared = {item.get("destination") for item in fixed if isinstance(item, Mapping)}
        if declared != NODE_DESTINATIONS or {item.destination for item in spec.entries} != NODE_DESTINATIONS:
            raise ComponentBuildError("koa_node_agent may contain only its three declared compiled destinations")
        return
    if spec.release_channel != "services":
        raise ComponentBuildError(f"service component {spec.component_id} must remain in release channel 'services'")
    if spec.artifact_class != "component_runtime" or spec.build_kind != "python_wheel":
        raise ComponentBuildError(f"service component {spec.component_id} must remain a python_wheel component_runtime")


def _load_spec(repository: Repository, slug: str) -> BuildSpec:
    package_ref = COMPONENT_MANIFESTS.get(slug)
    if package_ref is None:
        raise ComponentBuildError(f"unsupported component slug: {slug!r}")
    package = _toml(repository.resolve(package_ref, must_exist=True), "component package manifest")
    if (package.get("format"), package.get("format_version")) != ("koa.component-package", "1.0.0"):
        raise ComponentBuildError(f"unsupported component package manifest: {package_ref}")
    if package.get("status") != "blocked_missing_upstream_bundle" or package.get("activation_ready") is not False:
        raise ComponentBuildError("package status must remain blocked and activation_ready must remain false")

    build = package.get("build")
    upstream = package.get("upstream_bundle")
    if not isinstance(build, Mapping) or not isinstance(upstream, Mapping):
        raise ComponentBuildError("package manifest requires [build] and [upstream_bundle] tables")
    build_kind = _text(build, "build_kind", f"{package_ref}.build")
    if build_kind not in SUPPORTED_BUILD_KINDS:
        raise ComponentBuildError(f"unsupported declared build kind: {build_kind!r}")
    expected_build = {
        "network": "denied_unless_package_sources_admit_exact_input",
        "lock_state_required": True,
        "mutable_workspace_state_allowed": False,
        "secret_material_allowed": False,
    }
    if any(build.get(key) != value for key, value in expected_build.items()):
        raise ComponentBuildError("build policy must remain locked, non-secret, immutable, and deny-by-default")
    if (
        upstream.get("format") != BUNDLE_FORMAT
        or upstream.get("format_version") != BUNDLE_VERSION
        or upstream.get("builder") != "build-component"
        or upstream.get("activation_authority") is not False
    ):
        raise ComponentBuildError("invalid upstream bundle contract")

    refs = {
        "payload": _text(package, "source_payload_manifest", package_ref),
        "contract": _text(package, "source_contract", package_ref),
        "project": _text(package, "source_project", package_ref),
        "lock": _text(build, "lock_ref", f"{package_ref}.build"),
    }
    paths = {key: repository.resolve(value, must_exist=True) for key, value in refs.items()}
    output_ref = _text(upstream, "output", f"{package_ref}.upstream_bundle")
    repository_path(repository.root, output_ref, label="component bundle output", generated_output=True)
    payload = _toml(paths["payload"], "component payload manifest")
    contract = _json(paths["contract"], "component contract")
    component_id = _text(package, "component_id", package_ref)
    if payload.get("component_id") != component_id or contract.get("component_id") != component_id:
        raise ComponentBuildError("payload/contract component_id does not match package manifest")
    if contract.get("status") != "active":
        raise ComponentBuildError("component contract must be active")
    source_root = paths["project"].parent.relative_to(repository.root).as_posix()
    if payload.get("source_root", source_root) != source_root:
        raise ComponentBuildError("payload source_root does not match source project root")
    project = _toml(paths["project"], "component source project")
    version_table = project.get("project" if build_kind == "python_wheel" else "package")
    if not isinstance(version_table, Mapping):
        raise ComponentBuildError("source project does not declare its package metadata")

    spec = BuildSpec(
        slug,
        component_id,
        package_ref,
        refs["payload"],
        refs["contract"],
        refs["project"],
        source_root,
        refs["lock"],
        output_ref,
        _text(package, "release_channel", package_ref),
        _text(package, "artifact_class_key", package_ref),
        build_kind,
        _text(contract, "version", refs["contract"]),
        _text(version_table, "version", refs["project"]),
        _entries(payload),
        package,
    )
    _validate_role(spec)
    component_root = repository.resolve(source_root, must_exist=True)
    for entry in spec.entries:
        if build_kind == "rust_binaries" and entry.source.startswith("target/release/"):
            continue
        source = repository.resolve(f"{source_root}/{entry.source}", must_exist=True)
        source.relative_to(component_root)
        _safe_tree(source)
    return spec


def _environment(epoch: str, build_kind: str) -> dict[str, str | None]:
    env: dict[str, str | None] = {key: None for key in os.environ}
    for key in ("PATH", "HOME", "TMPDIR", "CARGO_HOME"):
        if value := os.environ.get(key):
            env[key] = value
    env.update({"LANG": "C", "LC_ALL": "C", "TZ": "UTC", "PYTHONHASHSEED": "0", "SOURCE_DATE_EPOCH": epoch, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    if build_kind == "python_wheel":
        env.update({"UV_OFFLINE": "1", "UV_NO_CACHE": "1", "UV_PYTHON_DOWNLOADS": "never"})
    else:
        env.update({"CARGO_NET_OFFLINE": "true", "CARGO_INCREMENTAL": "0"})
    return env


def _git_revision(repository: Repository, env: Mapping[str, str | None]) -> str:
    revision = run_process(["git", "rev-parse", "--verify", "HEAD"], cwd=repository.root, environment=env, timeout=30).stdout.strip()
    if len(revision) != 40 or any(char not in "0123456789abcdefABCDEF" for char in revision):
        raise ComponentBuildError("git HEAD is not an immutable 40-hex revision")
    dirty = run_process(["git", "status", "--porcelain=v1", "--untracked-files=all"], cwd=repository.root, environment=env, timeout=30)
    if dirty.stdout.strip():
        raise ComponentBuildError("component build requires a clean source worktree")
    return revision.lower()


def _build_argv(spec: BuildSpec, build_root: Path) -> tuple[str, ...]:
    if spec.build_kind == "python_wheel":
        return ("uv", "build", "--offline", "--no-cache", "--no-python-downloads", "--no-build-isolation", "--no-create-gitignore", "--wheel", "--out-dir", str(build_root / "wheel"), spec.source_root)
    return ("cargo", "build", "--locked", "--offline", "--release", "--package", "koa-node-agent", "--bins", "--target-dir", str(build_root / "target"))


def _tool_and_lock(repository: Repository, spec: BuildSpec, env: Mapping[str, str | None]) -> tuple[str, str]:
    tool = "uv" if spec.build_kind == "python_wheel" else "cargo"
    version = run_process([tool, "--version"], cwd=repository.root, environment=env, timeout=30).stdout.strip()
    if not version:
        raise ComponentBuildError(f"{tool} did not report a version")
    if spec.build_kind == "python_wheel":
        run_process(["uv", "lock", "--check", "--offline"], cwd=repository.root, environment=env, timeout=30)
    return tool, version


def _copy(source: Path, destination: Path, mode: int = 0o644) -> None:
    _safe_tree(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    destination.chmod(mode)


def _copy_tree(source: Path, destination: Path) -> None:
    _safe_tree(source)
    for item in sorted(source.rglob("*"), key=lambda path: path.as_posix()):
        target = destination / item.relative_to(source)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            _copy(item, target)


def _materialize(repository: Repository, spec: BuildSpec, build_root: Path, payload_root: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    if spec.build_kind == "python_wheel":
        wheels = sorted((build_root / "wheel").glob("*.whl"))
        if len(wheels) != 1:
            raise ComponentBuildError(f"python_wheel build must produce exactly one wheel; found {len(wheels)}")
        target = payload_root / "artifacts" / wheels[0].name
        _copy(wheels[0], target)
        records.append({"source": spec.project_ref, "destination": target.relative_to(payload_root).as_posix(), "representation": "python_wheel"})
        extra = 0
        for entry in spec.entries:
            if entry.source.startswith("src/"):
                records.append({"source": entry.source, "destination": entry.destination, "representation": "included_in_python_wheel"})
                continue
            extra += 1
            source = repository.resolve(f"{spec.source_root}/{entry.source}", must_exist=True)
            target = payload_root / "declared" / f"{extra:04d}"
            _copy_tree(source, target) if source.is_dir() else _copy(source, target)
            records.append({"source": entry.source, "destination": entry.destination, "representation": f"declared/{extra:04d}"})
        return records
    for entry in spec.entries:
        if not entry.source.startswith("target/release/"):
            raise ComponentBuildError(f"Rust payload is not a declared release binary: {entry.source}")
        name = Path(entry.source).name
        _copy(build_root / "target" / "release" / name, payload_root / "artifacts" / name, 0o755)
        records.append({"source": entry.source, "destination": entry.destination, "representation": f"artifacts/{name}"})
    return records


def _payload_files(payload_root: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(payload_root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_file() and not path.is_symlink():
            rows.append({"path": path.relative_to(payload_root).as_posix(), "sha256": _sha(path), "size_bytes": path.stat().st_size, "mode": f"{stat.S_IMODE(path.stat().st_mode):04o}"})
    if not rows:
        raise ComponentBuildError("component build produced an empty payload")
    return rows


def _compatibility(repository: Repository, spec: BuildSpec) -> dict[str, str]:
    release = _json(repository.resolve("docs/contracts/release-channels.contract.json", must_exist=True), "release-channel contract")
    artifacts = _json(repository.resolve("docs/contracts/artifact-classes.contract.json", must_exist=True), "artifact-class contract")
    channels = release.get("channels")
    if not isinstance(channels, list):
        raise ComponentBuildError("release-channel contract has no channels array")
    matches = [item for item in channels if isinstance(item, Mapping) and item.get("channel_id") == spec.release_channel]
    if len(matches) != 1 or not isinstance(matches[0].get("artifact_class_keys"), list):
        raise ComponentBuildError(f"release channel is not uniquely declared: {spec.release_channel}")
    membership = "compatible" if spec.artifact_class in matches[0]["artifact_class_keys"] else "blocked"
    definitions = artifacts.get("artifact_classes")
    if not isinstance(definitions, Mapping):
        raise ComponentBuildError("artifact-class contract has no artifact_classes object")
    definition = "present" if spec.artifact_class in definitions else "blocked_missing_definition"
    return {"release_channel_membership": membership, "artifact_class_definition": definition, "result": "compatible" if membership == "compatible" and definition == "present" else "blocked"}


def _evidence(repository: Repository, spec: BuildSpec, stage: Path, payload_root: Path, digests: Path, revision: str, tool: str, tool_version: str, argv: Sequence[str], build_root: Path, epoch: str, env: Mapping[str, str | None]) -> tuple[Path, Path]:
    evidence = stage / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.fromtimestamp(int(epoch), tz=UTC).isoformat().replace("+00:00", "Z")
    sbom = evidence / "sbom.spdx.json"
    run_process([sys.executable, "release/sbom/generate-sbom.py", "--subject", str(digests), "--content-root", str(payload_root), "--subject-id", f"koa.component-build.{spec.component_id}@{revision}", "--subject-name", spec.component_id, "--subject-version", spec.version, "--created-at", timestamp, "--creator", "kOA-Linux component builder", "--output", str(sbom)], cwd=repository.root, environment=env, timeout=120)
    if not sbom.is_file():
        raise ComponentBuildError("SBOM generator returned success without producing evidence")
    refs = (spec.package_ref, spec.payload_ref, spec.contract_ref, spec.project_ref, spec.lock_ref)
    provenance_input = stage.parent / f".{stage.name}.provenance.json"
    portable_argv = [value.replace(str(build_root), "<build-root>") for value in argv]
    _write_json(provenance_input, {"subject_path": str(digests), "subject_sha256": _sha(digests), "subject_ref": f"component bundle {spec.component_id}", "subject": {"subject_kind": "component_build_bundle", "artifact_class": spec.artifact_class, "artifact_id": f"koa.component-build.{spec.component_id}", "version": spec.version, "release_channel": spec.release_channel}, "source_refs": [spec.payload_ref, spec.contract_ref, spec.package_ref], "producer_ref": GENERATOR_ID, "producer_component_id": "repository_tooling", "toolchain_ref": tool, "toolchain": {"name": tool, "version": tool_version}, "environment_ref": "deterministic-offline-build", "environment": {"source_date_epoch": epoch, "network": "offline", "workspace_payload": "prohibited"}, "transformations": [{"order": 1, "transformation_id": "component-build", "argv": portable_argv, "started_at": timestamp, "completed_at": timestamp, "result": "succeeded"}], "materials": [{"material_ref": ref, "path": str(repository.resolve(ref, must_exist=True)), "sha256": _sha(repository.resolve(ref, must_exist=True))} for ref in refs], "test_evidence_refs": ["payload-digests"], "tests": [{"test_ref": "payload-digests", "status": "passed", "executed_at": timestamp, "evidence_ref": "payload-digests.json"}], "recorded_at": timestamp})
    provenance = evidence / "provenance.json"
    try:
        run_process([sys.executable, "release/provenance/generate-provenance.py", "--manifest", str(provenance_input), "--output", str(provenance)], cwd=repository.root, environment=env, timeout=120)
    finally:
        provenance_input.unlink(missing_ok=True)
    if not provenance.is_file():
        raise ComponentBuildError("provenance generator returned success without producing evidence")
    return sbom, provenance


def configure(parser: argparse.ArgumentParser) -> None:
    add_repository_options(parser)
    parser.add_argument("--component", required=True, choices=tuple(COMPONENT_MANIFESTS))
    parser.add_argument("--source-date-epoch", required=True, type=int)


def execute(args: argparse.Namespace) -> int:
    repository = Repository(Path(args.repository_root))
    spec = _load_spec(repository, args.component)
    epoch = source_date_epoch(args.source_date_epoch)
    env = _environment(epoch, spec.build_kind)
    output = repository.resolve(spec.output_ref, must_exist=False)
    if output.exists() or output.is_symlink():
        raise ComponentBuildError(f"component bundle output already exists: {spec.output_ref}")
    if args.dry_run:
        print(f"component={spec.slug}\nbuild_kind={spec.build_kind}\noutput={spec.output_ref}")
        print("argv=" + " ".join(_build_argv(spec, Path("<build-root>"))))
        return 0

    build_root = Path(tempfile.mkdtemp(prefix=f".koa-build-{spec.slug}-"))
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent))
    published = False
    try:
        revision = _git_revision(repository, env)
        tool, tool_version = _tool_and_lock(repository, spec, env)
        argv = _build_argv(spec, build_root)
        if args.verbose:
            print("build: " + " ".join(argv))
        run_process(argv, cwd=repository.root, environment=env, timeout=300)
        payload_root = stage / "payload"
        payload_root.mkdir(parents=True)
        declared = _materialize(repository, spec, build_root, payload_root)
        _copy(repository.resolve(spec.payload_ref, must_exist=True), stage / "payload-manifest.toml")
        payload_files = _payload_files(payload_root)
        digest_path = stage / "payload-digests.json"
        _write_json(digest_path, {"algorithm": "sha256", "component_id": spec.component_id, "files": payload_files})
        sbom, provenance = _evidence(repository, spec, stage, payload_root, digest_path, revision, tool, tool_version, argv, build_root, epoch, env)
        compatibility = _compatibility(repository, spec)
        source_refs = (spec.package_ref, spec.payload_ref, spec.contract_ref, spec.project_ref, spec.lock_ref, "docs/contracts/release-channels.contract.json", "docs/contracts/artifact-classes.contract.json")
        source_digests = {ref: _sha(repository.resolve(ref, must_exist=True)) for ref in source_refs}
        admission = spec.package.get("admission")
        if not isinstance(admission, Mapping):
            raise ComponentBuildError("component package manifest has no [admission] table")
        required = sorted(key.removeprefix("requires_") for key, value in admission.items() if key.startswith("requires_") and value is True)
        proven = {"clean_source", "immutable_revision", "payload_digest", "sbom", "provenance"}
        unresolved = sorted(set(required) - proven)
        upstream_complete = compatibility["result"] == "compatible"
        bundle = {"format": BUNDLE_FORMAT, "format_version": BUNDLE_VERSION, "generator_id": GENERATOR_ID, "generator_version": "1.0.0", "source_references": list(source_refs), "source_digest": hashlib.sha256(_canonical(source_digests)).hexdigest(), "output_class": "component_build_bundle", "generator": {"generator_id": GENERATOR_ID, "generator_version": "1.0.0", "output_class": "component_build_bundle"}, "component": {"component_id": spec.component_id, "component_version": spec.version, "project_version": spec.project_version, "source_revision": revision, "release_channel": spec.release_channel, "artifact_class_key": spec.artifact_class}, "sources": {"package_manifest_ref": spec.package_ref, "payload_manifest_ref": spec.payload_ref, "payload_manifest_snapshot": "payload-manifest.toml", "component_contract_ref": spec.contract_ref, "source_project_ref": spec.project_ref, "lock_ref": spec.lock_ref, "digests": source_digests, "source_digest": hashlib.sha256(_canonical(source_digests)).hexdigest()}, "build": {"build_kind": spec.build_kind, "tool": {"name": tool, "version": tool_version}, "network": "offline", "source_date_epoch": epoch, "workspace_as_payload": False, "declared_payload": declared}, "payload": {"digest_manifest_ref": "payload-digests.json", "digest_manifest_sha256": _sha(digest_path), "files": payload_files}, "evidence": {"sbom_ref": "evidence/sbom.spdx.json", "sbom_sha256": _sha(sbom), "provenance_ref": "evidence/provenance.json", "provenance_sha256": _sha(provenance), "downstream_required": required}, "compatibility": {**compatibility, "release_channel_contract_ref": "docs/contracts/release-channels.contract.json", "artifact_class_contract_ref": "docs/contracts/artifact-classes.contract.json"}, "admission": {"upstream_bundle_complete": upstream_complete, "packaging_admissible": upstream_complete and not unresolved, "unresolved_downstream_evidence": unresolved, "activation_ready": False, "activation_authority": False, "missing_or_blocked_evidence_result": "reject"}}
        _write_json(stage / "bundle.json", bundle)
        os.replace(stage, output)
        published = True
        return 0
    finally:
        shutil.rmtree(build_root, ignore_errors=True)
        if not published:
            shutil.rmtree(stage, ignore_errors=True)


COMMAND = CommandDefinition("build-component", "Build one canonical upstream component bundle.", configure, execute)


def main(argv: Sequence[str] | None = None, *, repository_root: str | os.PathLike[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="koa build-component", description=COMMAND.summary)
    configure(parser)
    args = parser.parse_args(argv)
    args.repository_root = Path(repository_root) if repository_root is not None else (args.repository_root or Path.cwd())
    try:
        return execute(args)
    except (CommandError, RepositoryError, ProcessError, OSError, ValueError) as exc:
        print(f"koa build-component: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
