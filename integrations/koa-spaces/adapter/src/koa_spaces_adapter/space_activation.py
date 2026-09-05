"""Admission and receipt verification for atomic Koali Spaces activation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, Mapping
from .client import SpacesClient
from .interface_assets import AssetManifestValidationError, ValidatedAssetManifest, validate_asset_manifest
from .interface_theme import ThemeValidationError, ValidatedTheme, validate_theme
from .module_manifest import ManifestValidationError, ValidatedManifest, validate_manifest
from .receipts import artifact_digest, validate_receipt
from .route_bridge import RouteBridge, RouteCompositionError, RouteTable

class SpaceActivationError(RuntimeError):
    """Raised when a Space cannot be safely admitted or activated."""

@dataclass(frozen=True, slots=True)
class AdmissionResult:
    space_definition: Mapping[str, Any]
    theme: ValidatedTheme
    shell_asset_manifest: ValidatedAssetManifest
    admitted_manifests: tuple[ValidatedManifest, ...]
    admitted_asset_manifests: tuple[ValidatedAssetManifest, ...]
    disabled_optional_modules: tuple[str, ...]
    route_table: RouteTable
    capability_snapshot: Mapping[str, Any]

@dataclass(frozen=True, slots=True)
class ActivationResult:
    operation: str
    receipt: Mapping[str, Any]
    disabled_optional_modules: tuple[str, ...]

def _validate_space_boundary(space: Mapping[str, Any]) -> None:
    expected = {
        "presentation_only": True,
        "may_grant_capabilities": False,
        "contains_business_state": False,
        "contains_executable_extension": False,
    }
    if not isinstance(space.get("authority_boundary"), Mapping) or dict(space["authority_boundary"]) != expected:
        raise SpaceActivationError("Space definition crosses authority boundary")
    offline = space.get("offline_policy")
    if not isinstance(offline, Mapping) or offline.get("shell_available") is not True or offline.get("retain_last_validated_definition") is not True or offline.get("network_state_indicator") is not True:
        raise SpaceActivationError("Space offline policy is incomplete")
    if offline.get("public_cdn_required", False) is not False or offline.get("remote_runtime_assets_required", False) is not False:
        raise SpaceActivationError("Space requires remote presentation assets")

def _capability_snapshot(values: Iterable[str]) -> Mapping[str, Any]:
    capabilities = sorted(set(values))
    if any(not isinstance(value, str) or not value for value in capabilities):
        raise SpaceActivationError("available capabilities must be non-empty strings")
    return {
        "source": "koa",
        "capabilities": capabilities,
        "may_grant_capabilities": False,
    }

def admit_space(
    space: Mapping[str, Any],
    manifests_by_ref: Mapping[str, Mapping[str, Any]],
    *,
    themes_by_ref: Mapping[str, Mapping[str, Any]],
    asset_manifests_by_ref: Mapping[str, Mapping[str, Any]],
    shell_asset_manifest: Mapping[str, Any],
    permitted_modules: Iterable[str],
    available_capabilities: Iterable[str],
    reserved_paths: Iterable[str] = (),
) -> AdmissionResult:
    if not isinstance(space, Mapping):
        raise SpaceActivationError("Space definition must be object")
    _validate_space_boundary(space)
    appearance = space.get("appearance")
    if not isinstance(appearance, Mapping) or not isinstance(appearance.get("theme_ref"), str):
        raise SpaceActivationError("Space must select an interface theme")
    try:
        theme = validate_theme(themes_by_ref[appearance["theme_ref"]])
    except (KeyError, ThemeValidationError) as exc:
        raise SpaceActivationError("required interface theme missing or invalid") from exc
    ds = appearance.get("design_system_id")
    if ds is not None and ds != theme.design_system_id:
        raise SpaceActivationError("Space design system does not match selected theme")
    try:
        shell_assets = validate_asset_manifest(shell_asset_manifest)
    except AssetManifestValidationError as exc:
        raise SpaceActivationError("shell asset manifest invalid") from exc
    if shell_assets.owner_kind != "koa_spaces_shell" or shell_assets.owner_id != "koa_spaces":
        raise SpaceActivationError("shell asset manifest identity mismatch")

    instances = space.get("module_instances")
    if not isinstance(instances, list) or not instances:
        raise SpaceActivationError("Space definition requires module instances")
    permitted = set(permitted_modules)
    snapshot = _capability_snapshot(available_capabilities)
    capabilities = set(snapshot["capabilities"])
    admitted: list[ValidatedManifest] = []
    assets: list[ValidatedAssetManifest] = []
    disabled: list[str] = []
    seen: set[str] = set()

    for instance in sorted(instances, key=lambda item: int(item.get("order", 0))):
        if not isinstance(instance, Mapping):
            raise SpaceActivationError("module instance must be object")
        module_id = instance.get("module_id")
        ref = instance.get("manifest_ref")
        enabled = instance.get("enabled") is True
        required = instance.get("required") is True
        if not isinstance(module_id, str) or not isinstance(ref, str):
            raise SpaceActivationError("module instance identity invalid")
        if module_id in seen:
            raise SpaceActivationError(f"duplicate module instance {module_id}")
        seen.add(module_id)
        if not enabled:
            continue
        if module_id not in permitted:
            if required:
                raise SpaceActivationError(f"required module {module_id} is not permitted")
            disabled.append(module_id)
            continue
        raw = manifests_by_ref.get(ref)
        if raw is None:
            if required:
                raise SpaceActivationError(f"required manifest missing for {module_id}")
            disabled.append(module_id)
            continue
        try:
            manifest = validate_manifest(raw, reserved_paths=reserved_paths)
        except ManifestValidationError as exc:
            if required:
                raise SpaceActivationError(f"required manifest invalid for {module_id}") from exc
            disabled.append(module_id)
            continue
        if manifest.module_id != module_id or set(manifest.required_capabilities) - capabilities:
            if required:
                raise SpaceActivationError(f"required module {module_id} is incompatible or lacks capabilities")
            disabled.append(module_id)
            continue
        if manifest.design_system_id is not None and manifest.design_system_id != theme.design_system_id:
            if required:
                raise SpaceActivationError(f"required module {module_id} design system mismatch")
            disabled.append(module_id)
            continue
        if manifest.asset_bundle_ref:
            raw_assets = asset_manifests_by_ref.get(manifest.asset_bundle_ref)
            try:
                asset = validate_asset_manifest(raw_assets) if raw_assets is not None else None
            except AssetManifestValidationError as exc:
                if required:
                    raise SpaceActivationError(f"required module assets invalid for {module_id}") from exc
                disabled.append(module_id)
                continue
            if asset is None or asset.owner_kind != "module" or asset.owner_id != module_id:
                if required:
                    raise SpaceActivationError(f"required module assets missing for {module_id}")
                disabled.append(module_id)
                continue
            assets.append(asset)
        admitted.append(manifest)

    if space.get("default_module_id") not in {m.module_id for m in admitted}:
        raise SpaceActivationError("default module is not admitted and permitted")
    try:
        route_table = RouteBridge.compose(admitted)
    except RouteCompositionError as exc:
        raise SpaceActivationError("route composition failed") from exc
    return AdmissionResult(
        space_definition=space,
        theme=theme,
        shell_asset_manifest=shell_assets,
        admitted_manifests=tuple(admitted),
        admitted_asset_manifests=tuple(assets),
        disabled_optional_modules=tuple(sorted(disabled)),
        route_table=route_table,
        capability_snapshot=snapshot,
    )

@dataclass(frozen=True, slots=True)
class SpaceActivator:
    client: SpacesClient

    def activate(self, admission: AdmissionResult, *, profile_id: str, actor_ref: str | None, correlation_id: str, idempotency_key: str) -> ActivationResult:
        payload = {
            "space_definition": dict(admission.space_definition),
            "interface_theme": dict(admission.theme.document),
            "shell_asset_manifest": dict(admission.shell_asset_manifest.document),
            "module_manifests": [dict(m.document) for m in admission.admitted_manifests],
            "module_asset_manifests": [dict(a.document) for a in admission.admitted_asset_manifests],
            "capability_snapshot": dict(admission.capability_snapshot),
            "profile_id": profile_id,
            "actor_ref": actor_ref,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
        }
        receipt = validate_receipt(self.client.activate_space(payload))
        self._verify_receipt("activate", admission, profile_id, receipt)
        return ActivationResult("activate", receipt, admission.disabled_optional_modules)

    def rollback(self, admission: AdmissionResult, *, profile_id: str, previous_receipt_ref: str, actor_ref: str | None, correlation_id: str, idempotency_key: str) -> ActivationResult:
        payload = {
            "space_id": admission.space_definition["space_id"],
            "space_version": admission.space_definition["version"],
            "previous_receipt_ref": previous_receipt_ref,
            "profile_id": profile_id,
            "actor_ref": actor_ref,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
        }
        receipt = validate_receipt(self.client.rollback_space(payload))
        self._verify_receipt("rollback", admission, profile_id, receipt)
        return ActivationResult("rollback", receipt, admission.disabled_optional_modules)

    def deactivate(self, admission: AdmissionResult, *, profile_id: str, actor_ref: str | None, correlation_id: str, idempotency_key: str) -> ActivationResult:
        payload = {
            "space_id": admission.space_definition["space_id"],
            "space_version": admission.space_definition["version"],
            "profile_id": profile_id,
            "actor_ref": actor_ref,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
        }
        receipt = validate_receipt(self.client.deactivate_space(payload))
        self._verify_receipt("deactivate", admission, profile_id, receipt)
        return ActivationResult("deactivate", receipt, admission.disabled_optional_modules)

    @staticmethod
    def _verify_receipt(operation: str, admission: AdmissionResult, profile_id: str, receipt: Mapping[str, Any]) -> None:
        checks = [
            (receipt["operation"] == operation, "operation"),
            (receipt["space_id"] == admission.space_definition["space_id"], "space_id"),
            (receipt["space_version"] == admission.space_definition["version"], "space_version"),
            (receipt["profile_id"] == profile_id, "profile_id"),
            (receipt["space_definition_digest"] == artifact_digest(admission.space_definition), "Space digest"),
            (receipt["interface_theme_digest"] == admission.theme.digest, "theme digest"),
            (receipt["shell_asset_manifest_digest"] == admission.shell_asset_manifest.digest, "shell asset digest"),
            (receipt["capability_snapshot_digest"] == artifact_digest(admission.capability_snapshot), "capability snapshot digest"),
        ]
        for ok, label in checks:
            if not ok:
                raise SpaceActivationError(f"receipt {label} mismatch")
        expected = sorted((m.module_id, m.digest) for m in admission.admitted_manifests)
        actual = sorted((x["module_id"], x["digest"]) for x in receipt["module_manifest_digests"])
        if expected != actual:
            raise SpaceActivationError("receipt module manifest digests mismatch")
        expected_assets = sorted((a.bundle_id, a.digest) for a in admission.admitted_asset_manifests)
        actual_assets = sorted((x["bundle_id"], x["digest"]) for x in receipt["module_asset_manifest_digests"])
        if expected_assets != actual_assets:
            raise SpaceActivationError("receipt module asset digests mismatch")
        if receipt["result"] == "rejected":
            raise SpaceActivationError(f"Space {operation} rejected: {receipt.get('failure_code')}")
