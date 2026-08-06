"""Render a deterministic offline-bundle manifest without embedding payloads."""

from __future__ import annotations

from typing import Any

from . import RenderedFile, generated_json, normalize_plan, validate_rendered_files

_RENDERER = "offline_bundle"


def render(plan: Any) -> tuple[RenderedFile, ...]:
    normalized = normalize_plan(plan)
    offline = normalized["offline"]
    payload = {
        "artifact_class": "offline_bundle_manifest",
        "profile_id": normalized["profile_id"],
        "enabled": offline["enabled"],
        "network_access_allowed": offline["allow_network"],
        "verification_policy": offline["verification_policy"],
        "artifacts": offline["artifacts"],
        "packages": normalized["packages"],
        "source_files": normalized["files"],
        "verification": {
            "verify_digests_before_import": True,
            "verify_signatures_when_required_by_artifact_class": True,
            "transport_grants_authority": False,
            "silent_substitution_allowed": False,
        },
    }
    return validate_rendered_files([
        RenderedFile(
            "offline_bundle/offline-bundle-manifest.json",
            generated_json(_RENDERER, normalized, payload),
            "application/json",
        )
    ])
