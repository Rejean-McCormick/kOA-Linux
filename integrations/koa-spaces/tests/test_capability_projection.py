from __future__ import annotations
from copy import deepcopy
from koa_spaces_adapter.receipts import artifact_digest
from koa_spaces_adapter.space_activation import admit_space

def test_admission_carries_non_authoritative_koa_capability_snapshot(space_definition, module_manifest, interface_theme, shell_asset_manifest):
    admission = admit_space(
        space_definition,
        {"manifest:koa_mediatheque": module_manifest},
        themes_by_ref={"theme:default": interface_theme},
        asset_manifests_by_ref={},
        shell_asset_manifest=shell_asset_manifest,
        permitted_modules={"koa_mediatheque"},
        available_capabilities={"koa_mediatheque.read", "publication.request"},
    )
    assert admission.capability_snapshot == {
        "source": "koa",
        "capabilities": ["koa_mediatheque.read", "publication.request"],
        "may_grant_capabilities": False,
    }
    assert len(artifact_digest(admission.capability_snapshot)) == 64

def test_deferred_space_templates_do_not_enable_unadmitted_subsystems():
    import json
    from pathlib import Path
    repository_root = Path(__file__).resolve().parents[3]
    for name in ("community-space.json", "school-space.json"):
        document = json.loads((repository_root / "integrations/koa-spaces/interface" / name).read_text(encoding="utf-8"))
        assert all(instance["module_id"] == "space_home" or instance["enabled"] is False for instance in document["module_instances"])
