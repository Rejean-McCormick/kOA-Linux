"""Command-line entry point for strict authority loading."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
import sys
import tomllib
from typing import Any, Iterable, Mapping, Sequence

from . import __version__
from .contract_loader import ContractLoader, LoadOutcome, LoadPolicy
from .diagnostics import DiagnosticBag
from .profiles import ProfileResolver, normalize_identifier
from .renderers import RenderError, render, write_rendered_files
from .renderers.image import render_assembly_bundle


EXIT_OK = 0
EXIT_BLOCKED = 1
EXIT_USAGE = 2
EXIT_ENVIRONMENT = 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="koa-assembly",
        description="Load and validate canonical kOA assembly authorities.",
    )
    parser.add_argument(
        "--repository-root",
        default=".",
        help="repository root containing docs/contracts (default: current directory)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="diagnostic output format",
    )
    parser.add_argument(
        "--max-bytes",
        type=_positive_integer,
        default=16 * 1024 * 1024,
        help="maximum bytes accepted for one authority document",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser(
        "validate", help="validate one or more explicit authority documents"
    )
    validate.add_argument("paths", nargs="+", help="repository-relative authority paths")

    scan = subparsers.add_parser(
        "scan", help="validate every supported file under an authority directory"
    )
    scan.add_argument("root", help="repository-relative authority file or directory")

    inspect = subparsers.add_parser(
        "inspect", help="validate one authority and print its immutable identity"
    )
    inspect.add_argument("path", help="repository-relative authority path")

    doctor = subparsers.add_parser(
        "doctor", help="check the minimum canonical assembly authorities"
    )
    doctor.add_argument(
        "--authority",
        action="append",
        default=[],
        help="override the authority paths checked by doctor; repeatable",
    )

    resolve_profile = subparsers.add_parser(
        "resolve-profile",
        help="resolve canonical profile authorities into one deterministic effective-profile projection",
    )
    resolve_profile.add_argument("--profile", required=True, help="primary profile identifier")
    resolve_profile.add_argument(
        "--overlay",
        action="append",
        default=[],
        help="explicit overlay identifier; repeatable",
    )
    resolve_profile.add_argument(
        "--output",
        required=True,
        help="repository-relative generated effective-profile JSON path",
    )
    resolve_profile.add_argument(
        "--check",
        action="store_true",
        help="compare the existing projection without writing",
    )

    render_plan = subparsers.add_parser(
        "render-plan",
        help="render one already-resolved deployment plan with a registered deterministic renderer",
    )
    render_plan.add_argument("--plan", required=True, help="repository-relative resolved plan JSON")
    render_plan.add_argument(
        "--renderer",
        required=True,
        choices=("systemd", "quadlet", "compose", "kubernetes", "image", "offline_bundle"),
    )
    render_plan.add_argument(
        "--output",
        required=True,
        help="repository-relative generated output root",
    )
    render_plan.add_argument(
        "--check",
        action="store_true",
        help="compare existing generated files without writing",
    )

    bundle = subparsers.add_parser(
        "render-bundle",
        help="render one deterministic assembly bundle from an already resolved plan",
    )
    bundle.add_argument("--plan", required=True, help="repository-relative resolved plan JSON")
    bundle.add_argument(
        "--settings",
        required=True,
        help="repository-relative system packaging TOML that owns generated entrypoints",
    )
    bundle.add_argument(
        "--overlay",
        action="append",
        default=[],
        help="repository-relative applied overlay authority; repeatable",
    )
    bundle.add_argument(
        "--output",
        required=True,
        help="repository-relative generated output root",
    )
    bundle.add_argument(
        "--check",
        action="store_true",
        help="compare existing generated files without writing",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "resolve-profile":
        return _resolve_profile_command(args)
    if args.command == "render-plan":
        return _render_plan_command(args)
    if args.command == "render-bundle":
        return _render_bundle_command(args)
    try:
        loader = ContractLoader(
            Path(args.repository_root),
            policy=LoadPolicy(max_bytes=args.max_bytes),
        )
    except (OSError, ValueError) as exc:
        _write_environment_error(str(exc), args.format)
        return EXIT_ENVIRONMENT

    if args.command == "validate":
        outcomes = tuple(loader.try_load(path) for path in sorted(set(args.paths)))
        return _render_outcomes(outcomes, args.format)
    if args.command == "scan":
        return _render_outcomes(loader.scan(args.root), args.format)
    if args.command == "inspect":
        outcome = loader.try_load(args.path)
        if not outcome.passed:
            return _render_outcomes((outcome,), args.format)
        contract = outcome.contract
        assert contract is not None
        payload = {
            "result": "pass",
            "identity": {
                "identifier": contract.identity.identifier,
                "version": contract.identity.version,
                "status": contract.identity.status,
                "document_class": contract.identity.document_class.value,
            },
            "source": {
                "reference": str(contract.source.reference),
                "format": contract.source.format.value,
                "sha256": contract.source.sha256,
                "schema_reference": (
                    str(contract.source.schema_reference)
                    if contract.source.schema_reference is not None
                    else None
                ),
            },
        }
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
        else:
            print(f"PASS {payload['identity']['identifier']} {payload['source']['reference']}")
            print(f"  version: {payload['identity']['version'] or '-'}")
            print(f"  status: {payload['identity']['status'] or '-'}")
            print(f"  sha256: {payload['source']['sha256']}")
            print(f"  schema: {payload['source']['schema_reference'] or '-'}")
        return EXIT_OK
    if args.command == "doctor":
        authorities = tuple(args.authority) or (
            "docs/contracts/ai-navigation.contract.json",
            "docs/contracts/system.contract.json",
            "docs/contracts/terminology.contract.json",
        )
        outcomes = tuple(loader.try_load(path) for path in authorities)
        return _render_outcomes(outcomes, args.format)
    parser.error("unreachable command")
    return EXIT_USAGE


class _BundleBlockedError(ValueError):
    """Raised when declared packaging inputs cannot produce a safe bundle."""


def _profile_contract_ref(profile_id: str) -> str:
    normalized = normalize_identifier(profile_id)
    return f"docs/contracts/profiles/{normalized.replace('_', '-')}.profile.json"


def _resolve_profile_command(args: argparse.Namespace) -> int:
    try:
        root = Path(args.repository_root).resolve(strict=True)
        output_path, output_ref = _repository_path(root, args.output, must_exist=False)
        if not output_ref.startswith("generated/"):
            raise _BundleBlockedError("effective-profile output must remain under generated/")

        profile_id = normalize_identifier(args.profile)
        overlay_ids = tuple(normalize_identifier(value) for value in args.overlay)
        if len(overlay_ids) != len(set(overlay_ids)):
            raise _BundleBlockedError("duplicate overlay selection")

        loader = ContractLoader(root, policy=LoadPolicy(max_bytes=args.max_bytes))
        refs = (_profile_contract_ref(profile_id), *(_profile_contract_ref(value) for value in overlay_ids))
        contracts: dict[str, Mapping[str, Any]] = {}
        digests: dict[str, str] = {}
        for ref in refs:
            outcome = loader.try_load(ref)
            if not outcome.passed or outcome.contract is None:
                message = outcome.diagnostics[0].message if outcome.diagnostics else f"cannot load {ref}"
                raise _BundleBlockedError(message)
            contracts[ref] = outcome.contract.data
            digests[ref] = "sha256:" + outcome.contract.source.sha256

        result = ProfileResolver(contracts).resolve(profile_id, overlay_ids)
        if not result.passed:
            detail = "; ".join(f"{issue.code}: {issue.detail}" for issue in result.issues)
            raise _BundleBlockedError("profile composition blocked: " + detail)
        effective = result.require_effective()
        declaration = effective.to_declaration(source_digests=digests)
        payload = (json.dumps(declaration, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
        if args.check:
            if not output_path.is_file() or output_path.read_bytes() != payload:
                raise _BundleBlockedError(f"generated effective-profile drift: {output_ref}")
        else:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(payload)
    except (OSError, UnicodeDecodeError, RenderError, _BundleBlockedError, ValueError) as exc:
        _write_bundle_result("blocked", str(exc), args.format, stream=sys.stderr)
        return EXIT_BLOCKED

    _write_bundle_result("pass", f"resolved {profile_id} to {output_ref}", args.format)
    return EXIT_OK


def _render_plan_command(args: argparse.Namespace) -> int:
    try:
        root = Path(args.repository_root).resolve(strict=True)
        plan_path, plan_ref = _repository_path(root, args.plan, must_exist=True)
        output_root, output_ref = _repository_path(root, args.output, must_exist=False)
        if not (output_ref == "generated" or output_ref.startswith("generated/")):
            raise _BundleBlockedError("render-plan output must remain under generated/")
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if not isinstance(plan, Mapping):
            raise _BundleBlockedError("resolved plan JSON must be an object")
        files = render(args.renderer, plan)
        if args.check:
            mismatches = _render_mismatches(output_root, files)
            if mismatches:
                raise _BundleBlockedError("generated render drift: " + ", ".join(mismatches))
        else:
            write_rendered_files(output_root, files)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RenderError, _BundleBlockedError, ValueError) as exc:
        _write_bundle_result("blocked", str(exc), args.format, stream=sys.stderr)
        return EXIT_BLOCKED

    _write_bundle_result(
        "pass",
        f"rendered {len(files)} deterministic file(s) from {plan_ref}",
        args.format,
    )
    return EXIT_OK


def _render_bundle_command(args: argparse.Namespace) -> int:
    try:
        root = Path(args.repository_root).resolve(strict=True)
        plan_path, plan_ref = _repository_path(root, args.plan, must_exist=True)
        settings_path, settings_ref = _repository_path(root, args.settings, must_exist=True)
        output_root, output_ref = _repository_path(root, args.output, must_exist=False)
        if not (output_ref == "generated" or output_ref.startswith("generated/")):
            raise _BundleBlockedError("render-bundle output must remain under generated/")

        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if not isinstance(plan, Mapping):
            raise _BundleBlockedError("resolved plan JSON must be an object")
        settings_bytes = settings_path.read_bytes()
        settings = tomllib.loads(settings_bytes.decode("utf-8"))
        if not isinstance(settings, Mapping):
            raise _BundleBlockedError("system packaging settings must be a TOML table")

        bundle_id = _required_setting(settings, "assembly_plan_bundle")
        profile_contract_ref = _required_setting(settings, "profile_contract")
        expected_bundle_ref = f"generated/assembly/{bundle_id}/bundle.json"
        if settings.get("assembly_plan_bundle_source") != expected_bundle_ref:
            raise _BundleBlockedError(
                "assembly_plan_bundle_source must identify the derived B-0092 bundle path"
            )
        delegates = _packaging_entrypoint_delegates(settings, bundle_id)
        settings_digest = "sha256:" + sha256(settings_bytes).hexdigest()
        files = render_assembly_bundle(
            plan,
            bundle_id=bundle_id,
            profile_contract_ref=profile_contract_ref,
            overlay_refs=tuple(sorted(set(args.overlay))),
            tool_versions={
                "koa_assembly": __version__,
                "python": (
                    f"{sys.version_info.major}.{sys.version_info.minor}."
                    f"{sys.version_info.micro}"
                ),
            },
            entrypoint_delegates=delegates,
            additional_input_digests={settings_ref: settings_digest},
        )
        if args.check:
            mismatches = _render_mismatches(output_root, files)
            if mismatches:
                raise _BundleBlockedError(
                    "generated bundle drift: " + ", ".join(mismatches)
                )
        else:
            write_rendered_files(output_root, files)
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        tomllib.TOMLDecodeError,
        RenderError,
        _BundleBlockedError,
        ValueError,
    ) as exc:
        _write_bundle_result("blocked", str(exc), args.format, stream=sys.stderr)
        return EXIT_BLOCKED

    _write_bundle_result(
        "pass",
        f"rendered {len(files)} deterministic file(s) from {plan_ref} using {settings_ref}",
        args.format,
    )
    return EXIT_OK


def _repository_path(
    root: Path, value: str, *, must_exist: bool
) -> tuple[Path, str]:
    if not isinstance(value, str) or not value.strip():
        raise _BundleBlockedError("repository path must be a non-empty string")
    reference = value.replace("\\", "/")
    pure = PurePosixPath(reference)
    if pure.is_absolute() or ".." in pure.parts:
        raise _BundleBlockedError(f"repository path must be relative and confined: {value!r}")
    path = (root / pure.as_posix()).resolve(strict=must_exist)
    if path != root and root not in path.parents:
        raise _BundleBlockedError(f"repository path escapes root: {value!r}")
    if must_exist and not path.is_file():
        raise _BundleBlockedError(f"repository input is not a file: {reference}")
    return path, pure.as_posix().rstrip("/")


def _required_setting(settings: Mapping[str, Any], key: str) -> str:
    value = settings.get(key)
    if not isinstance(value, str) or not value.strip():
        raise _BundleBlockedError(f"packaging setting {key} must be a non-empty string")
    return value


def _packaging_entrypoint_delegates(
    settings: Mapping[str, Any], bundle_id: str
) -> dict[str, tuple[str, ...]]:
    expected = ("koa-activation", "koa-health-aggregate", "koa-offline-import")
    executables = settings.get("executables")
    if not isinstance(executables, Mapping):
        raise _BundleBlockedError("packaging settings must declare [executables]")
    result: dict[str, tuple[str, ...]] = {}
    for name in expected:
        entry = executables.get(name)
        if not isinstance(entry, Mapping):
            raise _BundleBlockedError(f"packaging executable {name} is missing")
        expected_source = f"generated/assembly/{bundle_id}/entrypoints/{name}"
        expected_destination = f"/usr/libexec/koa/{name}"
        if entry.get("destination") != expected_destination:
            raise _BundleBlockedError(
                f"packaging executable {name} must install at {expected_destination}"
            )
        if entry.get("provider") != "assembly_generated_entrypoint":
            raise _BundleBlockedError(f"packaging executable {name} has an unsupported provider")
        if entry.get("provider_bundle") != bundle_id:
            raise _BundleBlockedError(f"packaging executable {name} has the wrong provider bundle")
        if entry.get("source") != expected_source:
            raise _BundleBlockedError(
                f"packaging executable {name} must source the derived entrypoint {expected_source}"
            )
        if entry.get("missing_provider") != "block_build":
            raise _BundleBlockedError(
                f"packaging executable {name} must fail closed when its provider is missing"
            )
        argv = entry.get("delegate_argv")
        if (
            not isinstance(argv, list)
            or not argv
            or not all(isinstance(item, str) for item in argv)
        ):
            raise _BundleBlockedError(
                f"packaging executable {name} requires an owner-declared delegate_argv"
            )
        result[name] = tuple(argv)
    return result


def _render_mismatches(root: Path, files: Sequence[Any]) -> tuple[str, ...]:
    mismatches: list[str] = []
    for item in files:
        target = root.joinpath(*PurePosixPath(item.path).parts)
        if not target.is_file() or target.read_bytes() != item.content:
            mismatches.append(item.path)
    return tuple(sorted(mismatches))


def _write_bundle_result(
    result: str, message: str, output_format: str, *, stream: Any = sys.stdout
) -> None:
    if output_format == "json":
        print(json.dumps({"result": result, "message": message}, sort_keys=True), file=stream)
    else:
        print(f"{result.upper()}: {message}", file=stream)


def _render_outcomes(outcomes: Iterable[LoadOutcome], output_format: str) -> int:
    outcomes = tuple(outcomes)
    bag = DiagnosticBag()
    loaded: list[dict[str, object]] = []
    for outcome in outcomes:
        bag.extend(outcome.diagnostics)
        if outcome.contract is not None:
            contract = outcome.contract
            loaded.append(
                {
                    "reference": str(contract.source.reference),
                    "identifier": contract.identity.identifier,
                    "version": contract.identity.version,
                    "status": contract.identity.status,
                    "sha256": contract.source.sha256,
                }
            )
    loaded.sort(key=lambda item: str(item["reference"]))
    blocked = bag.has_errors or len(loaded) != len(outcomes)
    if output_format == "json":
        payload = bag.to_dict()
        payload["result"] = "blocked" if blocked else "pass"
        payload["loaded"] = loaded
        payload["loaded_count"] = len(loaded)
        payload["requested_count"] = len(outcomes)
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    else:
        for item in loaded:
            print(f"LOADED {item['reference']} [{item['identifier']}] {item['sha256']}")
        if len(bag):
            print(bag.render_text())
        else:
            result = "BLOCKED" if blocked else "PASS"
            print(f"{result}: {len(loaded)}/{len(outcomes)} authority document(s) loaded")
    return EXIT_BLOCKED if blocked else EXIT_OK


def _positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def _write_environment_error(message: str, output_format: str) -> None:
    if output_format == "json":
        print(
            json.dumps(
                {
                    "result": "blocked",
                    "error": {
                        "code": "ASSEMBLY_ENVIRONMENT_INVALID",
                        "message": message,
                    },
                },
                sort_keys=True,
                indent=2,
            ),
            file=sys.stderr,
        )
    else:
        print(f"ERROR ASSEMBLY_ENVIRONMENT_INVALID: {message}", file=sys.stderr)
