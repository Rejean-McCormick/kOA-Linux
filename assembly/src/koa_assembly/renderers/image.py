"""Render deterministic system-image and B-0092 assembly projections."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from hashlib import sha256
from pathlib import PurePosixPath
from typing import Any

from ..releases.manifest import ManifestValidationError
from ..releases.release_set import build_assembly_bundle
from . import (
    GENERATOR_VERSION,
    RenderError,
    RenderedFile,
    canonical_json_bytes,
    generated_header,
    generated_json,
    normalize_plan,
    validate_rendered_files,
)

_RENDERER = "image"
_BUNDLE_RENDERER = "image-bundle"
_REQUIRED_ENTRYPOINTS = (
    "koa-activation",
    "koa-health-aggregate",
    "koa-offline-import",
)
_SHELL_EXECUTABLE_NAMES = frozenset({"sh", "bash", "dash", "zsh", "ksh", "fish"})
_GENERATED_RUNTIME_ENTRYPOINTS = frozenset(
    f"/usr/libexec/koa/{name}" for name in _REQUIRED_ENTRYPOINTS
)


def render(plan: Any) -> tuple[RenderedFile, ...]:
    """Render the existing deterministic system-image manifest projection."""

    return _render_normalized_image(normalize_plan(plan))


def _render_normalized_image(normalized: Mapping[str, Any]) -> tuple[RenderedFile, ...]:
    payload = {
        "artifact_class": "system_image_manifest",
        "profile_id": normalized["profile_id"],
        "packages": normalized["packages"],
        "files": normalized["files"],
        "services": [
            {
                "id": service["id"],
                "kind": service["kind"],
                "image": service["image"],
                "command": service["command"],
                "enabled": service["enabled"],
                "criticality": service["criticality"],
            }
            for service in normalized["services"]
        ],
        "storage": normalized["volumes"],
        "network": normalized["networks"],
        "activation": {
            "atomic": True,
            "verification_required": True,
            "partial_authoritative_state_allowed": False,
        },
    }
    return validate_rendered_files(
        [
            RenderedFile(
                "image/image-manifest.json",
                generated_json(_RENDERER, normalized, payload),
                "application/json",
            )
        ]
    )


def render_assembly_bundle(
    plan: Any,
    *,
    bundle_id: str,
    profile_contract_ref: str,
    overlay_refs: Sequence[str] = (),
    tool_versions: Mapping[str, str],
    entrypoint_delegates: Mapping[str, Sequence[str]],
    projection_refs: Mapping[str, str] | None = None,
    additional_input_digests: Mapping[str, str] | None = None,
) -> tuple[RenderedFile, ...]:
    """Render one B-0092 assembly bundle plus thin generated entrypoint adapters.

    Delegates are explicit structured argv supplied by the owning packaging input.
    Assembly never invents a runtime operation or shell command.
    """

    normalized = normalize_plan(plan)
    delegates = _normalize_entrypoint_delegates(entrypoint_delegates)
    bundle_root = f"assembly/{bundle_id}"
    generated_bundle_ref = f"generated/{bundle_root}/bundle.json"
    generated_entrypoint_refs = {
        name: f"generated/{bundle_root}/entrypoints/{name}"
        for name in _REQUIRED_ENTRYPOINTS
    }

    projections = {
        "assembly_bundle": generated_bundle_ref,
        "image_manifest": "generated/image/image-manifest.json",
        **{f"entrypoint.{name}": ref for name, ref in generated_entrypoint_refs.items()},
    }
    for key, value in sorted((projection_refs or {}).items()):
        if key in projections and projections[key] != value:
            raise RenderError(f"projection reference {key!r} conflicts with the bundle-owned path")
        projections[key] = value

    input_digests = dict(normalized["source_digests"])
    for path, digest in sorted((additional_input_digests or {}).items()):
        if path in input_digests and input_digests[path] != digest:
            raise RenderError(f"input digest {path!r} conflicts with the resolved plan")
        input_digests[path] = digest

    versions = {"koa_assembly.image_renderer": GENERATOR_VERSION}
    for key, value in sorted(tool_versions.items()):
        if key in versions and versions[key] != value:
            raise RenderError(f"tool version {key!r} conflicts with the renderer version")
        versions[key] = value

    try:
        bundle = build_assembly_bundle(
            bundle_id=bundle_id,
            resolved_plan=normalized,
            profile_id=normalized["profile_id"],
            profile_contract_ref=profile_contract_ref,
            overlay_refs=overlay_refs,
            input_digests=input_digests,
            tool_versions=versions,
            projection_refs=projections,
        )
    except ManifestValidationError as exc:
        raise RenderError(str(exc)) from exc

    entrypoints = tuple(
        _render_entrypoint(
            name,
            delegates[name],
            normalized,
            bundle_ref=generated_bundle_ref,
            output_path=f"{bundle_root}/entrypoints/{name}",
        )
        for name in _REQUIRED_ENTRYPOINTS
    )
    image_manifest = _render_normalized_image(normalized)[0]
    output_records = [
        {
            "path": f"generated/{item.path}",
            "digest": item.digest,
            "mode": f"{item.mode:04o}",
            "media_type": item.media_type,
        }
        for item in sorted((image_manifest, *entrypoints), key=lambda item: item.path)
    ]
    source_digest = "sha256:" + sha256(
        canonical_json_bytes(dict(bundle.input_digests))
    ).hexdigest()
    payload = bundle.to_dict()
    payload["generation"] = {
        "generator_id": "koa-assembly/image-bundle",
        "generator_version": GENERATOR_VERSION,
        "source_references": [path for path, _ in bundle.input_digests],
        "source_digest": source_digest,
        "output_class": "code_and_deployment_build_output",
    }
    payload["outputs"] = output_records
    bundle_file = RenderedFile(
        f"{bundle_root}/bundle.json",
        generated_json(_BUNDLE_RENDERER, normalized, payload),
        "application/json",
    )
    return validate_rendered_files((image_manifest, bundle_file, *entrypoints))


def _normalize_entrypoint_delegates(
    value: Mapping[str, Sequence[str]],
) -> dict[str, tuple[str, ...]]:
    if set(value) != set(_REQUIRED_ENTRYPOINTS):
        missing = sorted(set(_REQUIRED_ENTRYPOINTS) - set(value))
        extra = sorted(set(value) - set(_REQUIRED_ENTRYPOINTS))
        details = []
        if missing:
            details.append("missing=" + ",".join(missing))
        if extra:
            details.append("extra=" + ",".join(extra))
        raise RenderError(
            "entrypoint delegates must match the packaging set exactly: " + "; ".join(details)
        )
    result: dict[str, tuple[str, ...]] = {}
    for name in _REQUIRED_ENTRYPOINTS:
        argv = value[name]
        if isinstance(argv, (str, bytes)) or not isinstance(argv, Sequence) or not argv:
            raise RenderError(f"entrypoint delegate {name} must be a non-empty argv sequence")
        normalized: list[str] = []
        for index, item in enumerate(argv):
            if not isinstance(item, str) or not item or "\x00" in item or "\n" in item:
                raise RenderError(
                    f"entrypoint delegate {name}[{index}] must be a single-line string"
                )
            normalized.append(item)
        executable = PurePosixPath(normalized[0])
        if not executable.is_absolute() or ".." in executable.parts:
            raise RenderError(f"entrypoint delegate {name} executable must be an absolute path")
        if executable.name in _SHELL_EXECUTABLE_NAMES:
            raise RenderError(f"entrypoint delegate {name} may not invoke a shell executable")
        if executable.as_posix() in _GENERATED_RUNTIME_ENTRYPOINTS:
            raise RenderError(f"entrypoint delegate {name} may not target a generated entrypoint")
        result[name] = tuple(normalized)
    return result


def _render_entrypoint(
    name: str,
    delegate: tuple[str, ...],
    plan: Mapping[str, Any],
    *,
    bundle_ref: str,
    output_path: str,
) -> RenderedFile:
    header = generated_header(_BUNDLE_RENDERER, plan, comment="#").rstrip()
    argv_literal = repr(delegate)
    content = (
        "#!/usr/bin/python3\n"
        f"{header}\n"
        f"# Bundle-Manifest: {bundle_ref}\n"
        "# Thin adapter only: lifecycle and business behavior remain with the delegated owner.\n"
        "from __future__ import annotations\n\n"
        "import os\n"
        "import sys\n\n"
        f"_OWNER_ARGV = {argv_literal}\n"
        "_ENV = {\"LANG\": \"C\", \"LC_ALL\": \"C\", "
        "\"PATH\": \"/usr/bin:/usr/sbin:/bin:/sbin\"}\n\n"
        "def main() -> int:\n"
        "    os.chdir(\"/\")\n"
        "    argv = [*_OWNER_ARGV, *sys.argv[1:]]\n"
        "    os.execve(_OWNER_ARGV[0], argv, _ENV)\n"
        "    return 70\n\n"
        "if __name__ == \"__main__\":\n"
        "    raise SystemExit(main())\n"
    ).encode("utf-8")
    return RenderedFile(output_path, content, "text/x-python", mode=0o755)
