from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from koa_spaces_adapter import (
    SpacesClient,
    SpaceActivator,
    admit_space,
    validate_manifest,
    validate_receipt,
)

from ._support import ROOT, load_schema


def _validator(name: str) -> Draft202012Validator:
    directory = ROOT / "docs/contracts/artifact-contracts"
    resources = []
    for path in directory.glob("*.schema.json"):
        schema = load_schema(path.name)
        resources.append((schema["$id"], Resource.from_contents(schema)))
    root = load_schema(name)
    registry = Registry().with_resources(resources)
    return Draft202012Validator(
        root,
        registry=registry,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )


def test_artifacts_validate_against_canonical_schemas(
    space_definition, module_manifest, optional_manifest, receipt_response
):
    _validator("space-definition.schema.json").validate(space_definition)
    manifest_validator = _validator("module-interface-manifest.schema.json")
    manifest_validator.validate(module_manifest)
    manifest_validator.validate(optional_manifest)
    _validator("space-activation-receipt.schema.json").validate(receipt_response)


def test_manifest_semantics_and_atomic_activation_receipt(
    space_definition,
    module_manifest,
    optional_manifest,
    receipt_response,
    transport_factory,
):
    first = validate_manifest(module_manifest)
    assert first.module_id == "koa_mediatheque"
    admission = admit_space(
        space_definition,
        {
            "manifest:koa_mediatheque": module_manifest,
            "manifest:ariane": optional_manifest,
        },
        permitted_modules={"koa_mediatheque", "ariane"},
        available_capabilities={"koa_mediatheque.read", "publication.request"},
    )
    transport = transport_factory({"space.activate": receipt_response})
    result = SpaceActivator(SpacesClient(transport)).activate(
        admission,
        profile_id="user_lightweight",
        actor_ref="identity:user-1",
        correlation_id="corr-1",
        idempotency_key="activate-community-library-v1",
    )
    assert result.receipt["result"] == "activated"
    assert result.disabled_optional_modules == ()
    validate_receipt(result.receipt)
    assert transport.calls[0][0] == "space.activate"
