"""Render a deterministic system-image assembly manifest."""

from __future__ import annotations

from typing import Any

from . import RenderedFile, generated_json, normalize_plan, validate_rendered_files

_RENDERER = "image"


def render(plan: Any) -> tuple[RenderedFile, ...]:
    normalized = normalize_plan(plan)
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
    return validate_rendered_files([
        RenderedFile("image/image-manifest.json", generated_json(_RENDERER, normalized, payload), "application/json")
    ])
