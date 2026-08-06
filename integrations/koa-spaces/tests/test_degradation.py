from __future__ import annotations

import pytest

from koa_spaces_adapter import RouteBridge, RouteState, SpaceActivationError, admit_space


def test_missing_optional_module_is_omitted_without_substitution(
    space_definition, module_manifest
):
    admission = admit_space(
        space_definition,
        {"manifest:koa_mediatheque": module_manifest},
        permitted_modules={"koa_mediatheque", "ariane"},
        available_capabilities={"koa_mediatheque.read", "publication.request"},
    )
    assert admission.disabled_optional_modules == ("ariane",)
    assert set(admission.route_table.home_by_module) == {"koa_mediatheque"}


def test_missing_required_module_blocks_activation(space_definition):
    with pytest.raises(SpaceActivationError, match="required manifest missing"):
        admit_space(
            space_definition,
            {},
            permitted_modules={"koa_mediatheque", "ariane"},
            available_capabilities={"koa_mediatheque.read"},
        )


def test_network_loss_and_capability_loss_are_explicit(
    space_definition, module_manifest, optional_manifest
):
    admission = admit_space(
        space_definition,
        {
            "manifest:koa_mediatheque": module_manifest,
            "manifest:ariane": optional_manifest,
        },
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
