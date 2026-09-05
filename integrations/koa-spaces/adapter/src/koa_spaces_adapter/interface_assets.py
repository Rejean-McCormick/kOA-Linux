"""Validation for local-only Koali Spaces interface asset manifests."""
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping
from .receipts import artifact_digest

class AssetManifestValidationError(ValueError):
    """Raised when an interface asset manifest is unsafe or incomplete."""

@dataclass(frozen=True, slots=True)
class ValidatedAssetManifest:
    bundle_id: str
    owner_kind: str
    owner_id: str
    digest: str
    document: Mapping[str, Any]
    paths: tuple[str, ...]


def _local_path(value: Any) -> str:
    if not isinstance(value,str) or not value or value.startswith(("http://","https://","//","/")) or ".." in value.split("/"):
        raise AssetManifestValidationError("asset path must be safe and repository-relative")
    return value


def validate_asset_manifest(document: Mapping[str, Any]) -> ValidatedAssetManifest:
    if not isinstance(document, Mapping):
        raise AssetManifestValidationError("asset manifest must be an object")
    for field in ("bundle_id","version","owner_kind","owner_id","entrypoints","assets","offline_policy","authority_boundary"):
        if field not in document:
            raise AssetManifestValidationError(f"asset manifest missing {field}")
    if document["owner_kind"] not in {"koa_spaces_shell","module"}:
        raise AssetManifestValidationError("invalid asset owner_kind")
    if document.get("remote_runtime_dependencies",[]) != []:
        raise AssetManifestValidationError("remote runtime dependencies are prohibited")
    offline=document["offline_policy"]
    if not isinstance(offline,Mapping) or dict(offline) != {
        "local_assets_complete": True,
        "public_cdn_required": False,
        "remote_fonts_required": False,
        "internet_required_for_shell": False,
    }:
        raise AssetManifestValidationError("offline asset closure is invalid")
    boundary=document["authority_boundary"]
    if not isinstance(boundary,Mapping) or dict(boundary) != {
        "presentation_assets_only": True,
        "contains_business_authority": False,
        "contains_credentials": False,
    }:
        raise AssetManifestValidationError("asset manifest crosses authority boundary")
    entrypoints=document["entrypoints"]
    assets=document["assets"]
    if not isinstance(entrypoints,list) or not entrypoints or not isinstance(assets,list) or not assets:
        raise AssetManifestValidationError("asset manifest requires entrypoints and assets")
    paths=[]
    for raw in assets:
        if not isinstance(raw,Mapping): raise AssetManifestValidationError("asset entry must be object")
        path=_local_path(raw.get("path")); digest=raw.get("sha256")
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in "0123456789abcdef" for c in digest):
            raise AssetManifestValidationError("asset sha256 is invalid")
        paths.append(path)
    if len(paths)!=len(set(paths)): raise AssetManifestValidationError("duplicate asset path")
    known=set(paths)
    for ep in entrypoints:
        if _local_path(ep) not in known: raise AssetManifestValidationError("entrypoint is not in asset inventory")
    return ValidatedAssetManifest(str(document["bundle_id"]),str(document["owner_kind"]),str(document["owner_id"]),artifact_digest(document),MappingProxyType(dict(document)),tuple(sorted(paths)))
