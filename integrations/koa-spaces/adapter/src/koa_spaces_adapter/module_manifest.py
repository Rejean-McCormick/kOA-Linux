"""Semantic admission for Koali Spaces module interface manifests."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from .receipts import artifact_digest


class ManifestValidationError(ValueError):
    """Raised when a manifest crosses the presentation boundary."""


@dataclass(frozen=True, slots=True)
class ValidatedManifest:
    module_id: str
    manifest_id: str
    version: str
    digest: str
    document: Mapping[str, Any]
    route_ids: tuple[str, ...]
    paths: tuple[str, ...]
    required_capabilities: tuple[str, ...]
    asset_bundle_ref: str | None
    design_system_id: str | None


def _require_object(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ManifestValidationError(f"{label} must be an object")
    return value


def _require_array(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ManifestValidationError(f"{label} must be an array")
    return value


def _assert_unique(values: Iterable[str], label: str) -> tuple[str, ...]:
    items = tuple(values)
    if len(items) != len(set(items)):
        raise ManifestValidationError(f"duplicate {label}")
    return items


def _sidebar_route_ids(sidebar: Mapping[str, Any]) -> tuple[str, ...]:
    if sidebar.get("visible_depth") != 2:
        raise ManifestValidationError("sidebar visible_depth must be 2")
    result: list[str] = []
    for item in _require_array(sidebar.get("items"), "sidebar.items"):
        obj = _require_object(item, "sidebar item")
        if "children" in obj:
            children = _require_array(obj["children"], "sidebar children")
            if not children:
                raise ManifestValidationError("sidebar groups must have children")
            for child in children:
                result.append(str(_require_object(child, "sidebar child").get("route_id")))
        else:
            result.append(str(obj.get("route_id")))
    return _assert_unique(result, "sidebar route reference")


def _detect_fallback_cycles(routes: Mapping[str, Mapping[str, Any]]) -> None:
    for start in routes:
        seen: set[str] = set()
        current = start
        while True:
            fallback = routes[current].get("safe_fallback_route_id")
            if fallback is None:
                break
            if fallback not in routes:
                raise ManifestValidationError(f"unknown fallback route {fallback}")
            if fallback in seen or fallback == start:
                raise ManifestValidationError("circular safe route fallback")
            seen.add(current)
            current = str(fallback)


def validate_manifest(
    document: Mapping[str, Any],
    *,
    reserved_paths: Iterable[str] = (),
) -> ValidatedManifest:
    manifest = _require_object(document, "manifest")
    module_id = manifest.get("module_id")
    manifest_id = manifest.get("manifest_id")
    version = manifest.get("manifest_version")
    home_route_id = manifest.get("home_route_id")
    for value, label in (
        (module_id, "module_id"),
        (manifest_id, "manifest_id"),
        (version, "manifest_version"),
        (home_route_id, "home_route_id"),
    ):
        if not isinstance(value, str) or not value:
            raise ManifestValidationError(f"{label} must be a non-empty string")

    boundary = _require_object(manifest.get("authority_boundary"), "authority_boundary")
    expected_boundary = {
        "presentation_only": True,
        "may_grant_capabilities": False,
        "direct_domain_writes": False,
        "menu_visibility_is_authorization": False,
    }
    if dict(boundary) != expected_boundary:
        raise ManifestValidationError("manifest authority boundary is not presentation-only")

    accessibility = _require_object(manifest.get("accessibility"), "accessibility")
    if accessibility.get("keyboard_navigation") is not True:
        raise ManifestValidationError("keyboard navigation is required")
    if accessibility.get("screen_reader_labels") is not True:
        raise ManifestValidationError("screen-reader labels are required")

    routes_list = _require_array(manifest.get("routes"), "routes")
    if not routes_list:
        raise ManifestValidationError("at least one route is required")
    routes: dict[str, Mapping[str, Any]] = {}
    occupied_paths: set[str] = set()
    namespace = f"/{module_id}"
    reserved = set(reserved_paths)
    for raw in routes_list:
        route = _require_object(raw, "route")
        route_id = route.get("route_id")
        if not isinstance(route_id, str) or not route_id:
            raise ManifestValidationError("route_id must be non-empty")
        if route_id in routes:
            raise ManifestValidationError(f"duplicate route_id {route_id}")
        if route.get("module_id") != module_id:
            raise ManifestValidationError("route module_id must match manifest module_id")
        path = route.get("path")
        if not isinstance(path, str) or not path.startswith("/"):
            raise ManifestValidationError("route path must be absolute")
        if path not in reserved and path != namespace and not path.startswith(namespace + "/"):
            raise ManifestValidationError(f"route path {path} is outside module namespace")
        aliases = _require_array(route.get("aliases", []), "route aliases")
        for candidate in (path, *aliases):
            if candidate in occupied_paths:
                raise ManifestValidationError(f"route path collision: {candidate}")
            occupied_paths.add(str(candidate))
        policy = _require_object(route.get("capability_policy"), "capability_policy")
        _assert_unique(
            (str(item) for item in _require_array(policy.get("required_capabilities"), "required_capabilities")),
            "route capability",
        )
        if route.get("offline_behavior") not in {
            "available",
            "cached_read_only",
            "degraded",
            "unavailable",
        }:
            raise ManifestValidationError("every route must declare offline behavior")
        routes[route_id] = route

    if home_route_id not in routes:
        raise ManifestValidationError("home_route_id does not resolve")
    _detect_fallback_cycles(routes)

    sidebar = _require_object(manifest.get("sidebar"), "sidebar")
    if sidebar.get("module_id") != module_id:
        raise ManifestValidationError("sidebar module_id must match manifest module_id")
    for route_id in _sidebar_route_ids(sidebar):
        if route_id not in routes:
            raise ManifestValidationError(f"sidebar references unknown route {route_id}")

    for widget in _require_array(manifest.get("topbar_widgets"), "topbar_widgets"):
        obj = _require_object(widget, "topbar widget")
        if obj.get("scope") == "module" and obj.get("module_id") != module_id:
            raise ManifestValidationError("module widget has a mismatched module_id")
        activation = _require_object(obj.get("activation"), "widget activation")
        if activation.get("kind") == "route" and activation.get("route_id") not in routes:
            raise ManifestValidationError("widget references an unknown route")
        if obj.get("offline_behavior") not in {
            "available",
            "cached_read_only",
            "degraded",
            "unavailable",
        }:
            raise ManifestValidationError("every widget must declare offline behavior")

    required_capabilities = _assert_unique(
        (str(item) for item in _require_array(manifest.get("required_capabilities", []), "required_capabilities")),
        "manifest capability",
    )
    shell = manifest.get("shell_compatibility", {})
    if shell is not None and not isinstance(shell, Mapping):
        raise ManifestValidationError("shell_compatibility must be an object")
    design = manifest.get("design_system_compatibility", {})
    if design is not None and not isinstance(design, Mapping):
        raise ManifestValidationError("design_system_compatibility must be an object")
    design_system_id = design.get("design_system_id") if isinstance(design, Mapping) else None
    if design_system_id is not None and (not isinstance(design_system_id, str) or not design_system_id):
        raise ManifestValidationError("design_system_id must be a non-empty string")
    asset_bundle_ref = manifest.get("asset_bundle_ref")
    if asset_bundle_ref is not None and (not isinstance(asset_bundle_ref, str) or not asset_bundle_ref or asset_bundle_ref.startswith(("http://", "https://", "//"))):
        raise ManifestValidationError("asset_bundle_ref must be a local admitted reference")
    frozen = MappingProxyType(dict(manifest))
    return ValidatedManifest(
        module_id=str(module_id),
        manifest_id=str(manifest_id),
        version=str(version),
        digest=artifact_digest(manifest),
        document=frozen,
        route_ids=tuple(sorted(routes)),
        paths=tuple(sorted(occupied_paths)),
        required_capabilities=tuple(sorted(required_capabilities)),
        asset_bundle_ref=asset_bundle_ref,
        design_system_id=design_system_id,
    )
