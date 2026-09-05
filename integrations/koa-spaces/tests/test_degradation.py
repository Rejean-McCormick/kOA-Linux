from __future__ import annotations

import pytest

from koa_spaces_adapter import RouteBridge, RouteState, SpaceActivationError, admit_space
from ._support import ROOT


def _admit(
    space_definition,
    module_map,
    interface_theme,
    shell_asset_manifest,
    *,
    permitted_modules,
    available_capabilities,
):
    return admit_space(
        space_definition,
        module_map,
        themes_by_ref={"theme:default": interface_theme},
        asset_manifests_by_ref={},
        shell_asset_manifest=shell_asset_manifest,
        permitted_modules=permitted_modules,
        available_capabilities=available_capabilities,
    )


def test_missing_optional_module_is_omitted_without_substitution(
    space_definition, module_manifest, interface_theme, shell_asset_manifest
):
    admission = _admit(
        space_definition,
        {"manifest:koa_mediatheque": module_manifest},
        interface_theme,
        shell_asset_manifest,
        permitted_modules={"koa_mediatheque", "ariane"},
        available_capabilities={"koa_mediatheque.read", "publication.request"},
    )
    assert admission.disabled_optional_modules == ("ariane",)
    assert set(admission.route_table.home_by_module) == {"koa_mediatheque"}


def test_missing_required_module_blocks_activation(
    space_definition, interface_theme, shell_asset_manifest
):
    with pytest.raises(SpaceActivationError, match="required manifest missing"):
        _admit(
            space_definition,
            {},
            interface_theme,
            shell_asset_manifest,
            permitted_modules={"koa_mediatheque", "ariane"},
            available_capabilities={"koa_mediatheque.read"},
        )


def test_network_loss_and_capability_loss_are_explicit(
    space_definition,
    module_manifest,
    optional_manifest,
    interface_theme,
    shell_asset_manifest,
):
    admission = _admit(
        space_definition,
        {
            "manifest:koa_mediatheque": module_manifest,
            "manifest:ariane": optional_manifest,
        },
        interface_theme,
        shell_asset_manifest,
        permitted_modules={"koa_mediatheque", "ariane"},
        available_capabilities={"koa_mediatheque.read", "publication.request"},
    )
    offline = RouteBridge.resolve(
        admission.route_table,
        "koa_mediatheque.publish",
        granted_capabilities={"koa_mediatheque.read", "publication.request"},
        online=False,
        enabled_modules={"koa_mediatheque", "ariane"},
    )
    denied = RouteBridge.resolve(
        admission.route_table,
        "/koa_mediatheque/publish",
        granted_capabilities={"koa_mediatheque.read"},
        online=True,
        enabled_modules={"koa_mediatheque", "ariane"},
        deep_link=True,
    )
    assert offline.state is RouteState.UNAVAILABLE
    assert offline.reason == "network_unavailable"
    assert denied.state is RouteState.HIDDEN
    assert denied.requires_owner_authorization is True
    assert denied.authoritative is False


def test_asset_failure_never_falls_back_to_public_cdn():
    text = (ROOT / "integrations/koa-spaces/degradation.toml").read_text(encoding="utf-8")
    assert "public_cdn_fallback = false" in text
    assert "substitute_remote_assets = false" in text
