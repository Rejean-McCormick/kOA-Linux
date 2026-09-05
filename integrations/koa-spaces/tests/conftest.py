from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any, Mapping

import pytest

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / "integrations/koa-spaces/adapter/src"
if str(PACKAGE) not in sys.path:
    sys.path.insert(0, str(PACKAGE))

from koa_spaces_adapter.receipts import build_receipt


@pytest.fixture
def fixed_clock():
    return lambda: datetime(2026, 8, 6, 15, 0, tzinfo=timezone.utc)


@pytest.fixture
def interface_theme() -> dict[str, Any]:
    return {
        "theme_id": "koa_spaces.test",
        "version": "1.0.0",
        "design_system_id": "koali.ant5",
        "tokens": {
            "primary_accent": "#1e6864",
            "density": "comfortable",
            "radius_scale": "koali.radius.v1",
            "spacing_scale": "koali.spacing.v1",
            "typography_scale": "koali.type.v1",
            "focus_style": "visible",
        },
        "icon_policy": {"style": "outline", "local_assets_required": True},
        "motion_policy": {"reduced_motion_supported": True, "default_motion": "minimal"},
        "framework_mapping": {"antd.colorPrimary": "#1e6864"},
        "authority_boundary": {
            "presentation_only": True,
            "changes_authorization": False,
            "changes_module_identity": False,
        },
    }


@pytest.fixture
def shell_asset_manifest() -> dict[str, Any]:
    return {
        "bundle_id": "koa_spaces.shell",
        "version": "1.0.0",
        "owner_kind": "koa_spaces_shell",
        "owner_id": "koa_spaces",
        "entrypoints": ["static/shell.js"],
        "assets": [
            {
                "path": "static/shell.js",
                "media_type": "text/javascript",
                "sha256": "0" * 64,
                "offline_required": True,
                "cache_policy": "immutable",
            }
        ],
        "remote_runtime_dependencies": [],
        "offline_policy": {
            "local_assets_complete": True,
            "public_cdn_required": False,
            "remote_fonts_required": False,
            "internet_required_for_shell": False,
        },
        "compatibility": {
            "shell_min_version": "1.0.0",
            "design_system_id": "koali.ant5",
            "module_manifest_version": "1.0.0",
        },
        "authority_boundary": {
            "presentation_assets_only": True,
            "contains_business_authority": False,
            "contains_credentials": False,
        },
    }


@pytest.fixture
def module_manifest() -> dict[str, Any]:
    return {
        "$schema": "https://schemas.koa.local/artifact-contracts/module-interface-manifest.schema.json",
        "manifest_id": "koa_mediatheque.interface",
        "manifest_version": "1.0.0",
        "module_id": "koa_mediatheque",
        "public_name": "Library",
        "description": "Presentation-only access to admitted media records.",
        "icon_ref": "asset:library",
        "home_route_id": "koa_mediatheque.home",
        "required_capabilities": ["koa_mediatheque.read"],
        "routes": [
            {
                "route_id": "koa_mediatheque.home",
                "module_id": "koa_mediatheque",
                "path": "/koa_mediatheque",
                "page_ref": "koa_mediatheque.pages.home",
                "default_label": "Library",
                "availability": "always",
                "offline_behavior": "cached_read_only",
                "deep_link_allowed": True,
                "safe_fallback_route_id": None,
                "aliases": ["/koa_mediatheque/home"],
                "capability_policy": {
                    "required_capabilities": ["koa_mediatheque.read"],
                    "denied_behavior": "access_denied",
                },
            },
            {
                "route_id": "koa_mediatheque.publish",
                "module_id": "koa_mediatheque",
                "path": "/koa_mediatheque/publish",
                "page_ref": "koa_mediatheque.pages.publish",
                "default_label": "Publish",
                "availability": "online_only",
                "offline_behavior": "unavailable",
                "deep_link_allowed": True,
                "safe_fallback_route_id": "koa_mediatheque.home",
                "aliases": [],
                "capability_policy": {
                    "required_capabilities": ["publication.request"],
                    "denied_behavior": "hidden",
                },
            },
        ],
        "sidebar": {
            "module_id": "koa_mediatheque",
            "visible_depth": 2,
            "items": [
                {
                    "item_id": "library",
                    "label": "Library",
                    "order": 0,
                    "route_id": "koa_mediatheque.home",
                    "required_capabilities": ["koa_mediatheque.read"],
                    "availability": "always",
                    "badge_provider_ref": None,
                    "icon_ref": "asset:library",
                },
                {
                    "item_id": "actions",
                    "label": "Actions",
                    "order": 1,
                    "required_capabilities": [],
                    "availability": "always",
                    "badge_provider_ref": None,
                    "icon_ref": None,
                    "children": [
                        {
                            "item_id": "publish",
                            "label": "Publish",
                            "order": 0,
                            "route_id": "koa_mediatheque.publish",
                            "required_capabilities": ["publication.request"],
                            "availability": "online_only",
                            "badge_provider_ref": None,
                            "icon_ref": None,
                        }
                    ],
                },
            ],
        },
        "topbar_widgets": [
            {
                "widget_id": "koa_mediatheque.open_publish",
                "module_id": "koa_mediatheque",
                "scope": "module",
                "slot": "primary",
                "kind": "action",
                "label": "Publish",
                "priority": 10,
                "required_capabilities": ["publication.request"],
                "offline_behavior": "unavailable",
                "compact_only": True,
                "activation": {
                    "kind": "route",
                    "route_id": "koa_mediatheque.publish",
                    "command_ref": None,
                    "status_provider_ref": None,
                },
            }
        ],
        "localization_refs": ["i18n:koa_mediatheque"],
        "accessibility": {
            "keyboard_navigation": True,
            "screen_reader_labels": True,
            "reduced_motion": "supported",
        },
        "offline_behavior": {
            "module_state": "cached_read_only",
            "fallback_route_id": "koa_mediatheque.home",
        },
        "authority_boundary": {
            "presentation_only": True,
            "may_grant_capabilities": False,
            "direct_domain_writes": False,
            "menu_visibility_is_authorization": False,
        },
        "shell_compatibility": {"min_shell_version": "1.0.0", "max_shell_version": None},
        "design_system_compatibility": {"design_system_id": "koali.ant5", "min_version": "1.0.0"},
        "asset_bundle_ref": None,
        "surface_contract_version": "1.0.0",
    }


@pytest.fixture
def optional_manifest() -> dict[str, Any]:
    return {
        "$schema": "https://schemas.koa.local/artifact-contracts/module-interface-manifest.schema.json",
        "manifest_id": "ariane.interface",
        "manifest_version": "1.0.0",
        "module_id": "ariane",
        "public_name": "Assist",
        "home_route_id": "ariane.home",
        "required_capabilities": [],
        "routes": [
            {
                "route_id": "ariane.home",
                "module_id": "ariane",
                "path": "/ariane",
                "page_ref": "ariane.pages.home",
                "default_label": "Assist",
                "availability": "always",
                "offline_behavior": "available",
                "deep_link_allowed": True,
                "safe_fallback_route_id": None,
                "aliases": [],
                "capability_policy": {"required_capabilities": [], "denied_behavior": "disabled"},
            }
        ],
        "sidebar": {
            "module_id": "ariane",
            "visible_depth": 2,
            "items": [
                {
                    "item_id": "assist",
                    "label": "Assist",
                    "order": 0,
                    "route_id": "ariane.home",
                    "required_capabilities": [],
                    "availability": "always",
                    "badge_provider_ref": None,
                    "icon_ref": None,
                }
            ],
        },
        "topbar_widgets": [],
        "localization_refs": [],
        "accessibility": {
            "keyboard_navigation": True,
            "screen_reader_labels": True,
            "reduced_motion": "not_applicable",
        },
        "offline_behavior": {"module_state": "available", "fallback_route_id": "ariane.home"},
        "authority_boundary": {
            "presentation_only": True,
            "may_grant_capabilities": False,
            "direct_domain_writes": False,
            "menu_visibility_is_authorization": False,
        },
        "shell_compatibility": {"min_shell_version": "1.0.0", "max_shell_version": None},
        "design_system_compatibility": {"design_system_id": "koali.ant5", "min_version": "1.0.0"},
        "asset_bundle_ref": None,
        "surface_contract_version": "1.0.0",
    }


@pytest.fixture
def space_definition() -> dict[str, Any]:
    return {
        "$schema": "https://schemas.koa.local/artifact-contracts/space-definition.schema.json",
        "space_id": "community_library",
        "title": "Community Library",
        "version": "1.0.0",
        "description": "A local-first presentation composition.",
        "default_module_id": "koa_mediatheque",
        "module_instances": [
            {"module_id": "koa_mediatheque", "manifest_ref": "manifest:koa_mediatheque", "enabled": True, "required": True, "order": 0, "public_label": "Library", "public_icon_ref": "asset:library", "home_route_override": None},
            {"module_id": "ariane", "manifest_ref": "manifest:ariane", "enabled": True, "required": False, "order": 1, "public_label": "Assist", "public_icon_ref": None, "home_route_override": None},
        ],
        "global_topbar": [],
        "appearance": {
            "theme_ref": "theme:default",
            "density": "comfortable",
            "logo_ref": None,
            "accent_token": None,
            "allow_module_accent": True,
            "design_system_id": "koali.ant5",
            "theme_version": "1.0.0",
        },
        "offline_policy": {
            "shell_available": True,
            "retain_last_validated_definition": True,
            "unavailable_module_behavior": "show_unavailable",
            "network_state_indicator": True,
            "public_cdn_required": False,
            "remote_runtime_assets_required": False,
        },
        "assignment_scope": "installation",
        "authority_boundary": {
            "presentation_only": True,
            "may_grant_capabilities": False,
            "contains_business_state": False,
            "contains_executable_extension": False,
        },
    }


class FakeTransport:
    def __init__(self, responses: Mapping[str, Any] | None = None):
        self.responses = dict(responses or {})
        self.calls: list[tuple[str, dict[str, Any], float]] = []

    def request(self, operation, payload, *, timeout_seconds):
        self.calls.append((operation, dict(payload or {}), timeout_seconds))
        response = self.responses.get(operation)
        if isinstance(response, BaseException):
            raise response
        if callable(response):
            return response(payload)
        if response is None:
            raise ConnectionError(operation)
        return deepcopy(response)


@pytest.fixture
def transport_factory():
    return FakeTransport


@pytest.fixture
def receipt_response(space_definition, interface_theme, shell_asset_manifest, module_manifest, optional_manifest):
    return dict(
        build_receipt(
            operation="activate",
            space_definition=space_definition,
            interface_theme=interface_theme,
            shell_asset_manifest=shell_asset_manifest,
            capability_snapshot={
                "source": "koa",
                "capabilities": ["koa_mediatheque.read", "publication.request"],
                "may_grant_capabilities": False,
            },
            module_manifests=[module_manifest, optional_manifest],
            module_asset_manifests=[],
            profile_id="user_lightweight",
            actor_ref="identity:user-1",
            validation={
                "schema": "pass",
                "signatures": "not_required",
                "routes": "pass",
                "capabilities": "pass",
                "offline": "pass",
                "accessibility": "pass",
                "theme": "pass",
                "assets": "pass",
            },
            result="activated",
            recorded_at="2026-08-06T15:00:00Z",
            evidence_refs=["evidence:validation-1"],
        )
    )


def load_schema(name: str) -> dict[str, Any]:
    path = ROOT / "docs/contracts/artifact-contracts" / name
    return json.loads(path.read_text(encoding="utf-8"))
