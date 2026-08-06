"""Admission and receipt verification for atomic Space activation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from .client import SpacesClient
from .module_manifest import ManifestValidationError, ValidatedManifest, validate_manifest
from .receipts import artifact_digest, validate_receipt
from .route_bridge import RouteBridge, RouteCompositionError, RouteTable


class SpaceActivationError(RuntimeError):
    """Raised when a Space cannot be safely admitted or activated."""


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    space_definition: Mapping[str, Any]
    admitted_manifests: tuple[ValidatedManifest, ...]
    disabled_optional_modules: tuple[str, ...]
    route_table: RouteTable


@dataclass(frozen=True, slots=True)
class ActivationResult:
    operation: str
    receipt: Mapping[str, Any]
    disabled_optional_modules: tuple[str, ...]


def _validate_space_boundary(space: Mapping[str, Any]) -> None:
    boundary = space.get("authority_boundary")
    expected = {
        "presentation_only": True,
        "may_grant_capabilities": False,
        "contains_business_state": False,
        "contains_executable_extension": False,
    }
    if not isinstance(boundary, Mapping) or dict(boundary) != expected:
        raise SpaceActivationError("Space definition crosses the authority boundary")
    offline = space.get("offline_policy")
    if not isinstance(offline, Mapping):
        raise SpaceActivationError("Space definition must declare offline policy")
    if offline.get("shell_available") is not True:
        raise SpaceActivationError("offline shell must remain available")
    if offline.get("retain_last_validated_definition") is not True:
        raise SpaceActivationError("last validated Space definition must be retained")
    if offline.get("network_state_indicator") is not True:
        raise SpaceActivationError("network state indicator is required")


def admit_space(
    space: Mapping[str, Any],
    manifests_by_ref: Mapping[str, Mapping[str, Any]],
    *,
    permitted_modules: Iterable[str],
    available_capabilities: Iterable[str],
    reserved_paths: Iterable[str] = (),
) -> AdmissionResult:
    if not isinstance(space, Mapping):
        raise SpaceActivationError("Space definition must be an object")
    _validate_space_boundary(space)
    instances = space.get("module_instances")
    if not isinstance(instances, list) or not instances:
        raise SpaceActivationError("Space definition requires module instances")
    permitted = set(permitted_modules)
    capabilities = set(available_capabilities)
    admitted: list[ValidatedManifest] = []
    disabled: list[str] = []
    seen_modules: set[str] = set()

    for instance in sorted(instances, key=lambda item: int(item.get("order", 0))):
        if not isinstance(instance, Mapping):
            raise SpaceActivationError("module instance must be an object")
        module_id = instance.get("module_id")
        manifest_ref = instance.get("manifest_ref")
        enabled = instance.get("enabled") is True
        required = instance.get("required") is True
        if not isinstance(module_id, str) or not isinstance(manifest_ref, str):
            raise SpaceActivationError("module instance identity is invalid")
        if module_id in seen_modules:
            raise SpaceActivationError(f"duplicate module instance {module_id}")
        seen_modules.add(module_id)
        if not enabled:
            continue
        if module_id not in permitted:
            if required:
                raise SpaceActivationError(f"required module {module_id} is not permitted")
            disabled.append(module_id)
            continue
        raw_manifest = manifests_by_ref.get(manifest_ref)
        if raw_manifest is None:
            if required:
                raise SpaceActivationError(f"required manifest missing for {module_id}")
            disabled.append(module_id)
            continue
        try:
            manifest = validate_manifest(raw_manifest, reserved_paths=reserved_paths)
        except ManifestValidationError as exc:
            if required:
                raise SpaceActivationError(f"required manifest invalid for {module_id}") from exc
            disabled.append(module_id)
            continue
        if manifest.module_id != module_id:
            if required:
                raise SpaceActivationError("required manifest module identity mismatch")
            disabled.append(module_id)
            continue
        missing = set(manifest.required_capabilities) - capabilities
        if missing:
            if required:
                raise SpaceActivationError(
                    f"required module {module_id} lacks capabilities: {sorted(missing)}"
                )
            disabled.append(module_id)
            continue
        admitted.append(manifest)

    default_module = space.get("default_module_id")
    admitted_ids = {item.module_id for item in admitted}
    if default_module not in admitted_ids:
        raise SpaceActivationError("default module is not admitted and permitted")
    try:
        route_table = RouteBridge.compose(admitted)
    except RouteCompositionError as exc:
        raise SpaceActivationError("route composition failed") from exc
    return AdmissionResult(
        space_definition=space,
        admitted_manifests=tuple(admitted),
        disabled_optional_modules=tuple(sorted(disabled)),
        route_table=route_table,
    )


@dataclass(frozen=True, slots=True)
class SpaceActivator:
    client: SpacesClient

    def activate(
        self,
        admission: AdmissionResult,
        *,
        profile_id: str,
        actor_ref: str | None,
        correlation_id: str,
        idempotency_key: str,
    ) -> ActivationResult:
        payload = {
            "space_definition": dict(admission.space_definition),
            "module_manifests": [dict(item.document) for item in admission.admitted_manifests],
            "profile_id": profile_id,
            "actor_ref": actor_ref,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
        }
        receipt = validate_receipt(self.client.activate_space(payload))
        self._verify_receipt("activate", admission, profile_id, receipt)
        return ActivationResult(
            operation="activate",
            receipt=receipt,
            disabled_optional_modules=admission.disabled_optional_modules,
        )

    def rollback(
        self,
        admission: AdmissionResult,
        *,
        profile_id: str,
        previous_receipt_ref: str,
        actor_ref: str | None,
        correlation_id: str,
        idempotency_key: str,
    ) -> ActivationResult:
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

    def deactivate(
        self,
        admission: AdmissionResult,
        *,
        profile_id: str,
        actor_ref: str | None,
        correlation_id: str,
        idempotency_key: str,
    ) -> ActivationResult:
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
    def _verify_receipt(
        operation: str,
        admission: AdmissionResult,
        profile_id: str,
        receipt: Mapping[str, Any],
    ) -> None:
        if receipt["operation"] != operation:
            raise SpaceActivationError("receipt operation mismatch")
        if receipt["space_id"] != admission.space_definition["space_id"]:
            raise SpaceActivationError("receipt space_id mismatch")
        if receipt["space_version"] != admission.space_definition["version"]:
            raise SpaceActivationError("receipt space_version mismatch")
        if receipt["profile_id"] != profile_id:
            raise SpaceActivationError("receipt profile_id mismatch")
        if receipt["space_definition_digest"] != artifact_digest(admission.space_definition):
            raise SpaceActivationError("receipt Space digest mismatch")
        expected = sorted(
            (item.module_id, item.digest) for item in admission.admitted_manifests
        )
        actual = sorted(
            (item["module_id"], item["digest"])
            for item in receipt["module_manifest_digests"]
        )
        if expected != actual:
            raise SpaceActivationError("receipt module manifest digests mismatch")
        if receipt["result"] == "rejected":
            raise SpaceActivationError(
                f"Space {operation} rejected: {receipt.get('failure_code')}"
            )
