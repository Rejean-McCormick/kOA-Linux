"""Validation for presentation-only Koali Spaces interface themes."""
from __future__ import annotations
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping
from .receipts import artifact_digest

class ThemeValidationError(ValueError):
    """Raised when an interface theme crosses the presentation contract."""

@dataclass(frozen=True, slots=True)
class ValidatedTheme:
    theme_id: str
    version: str
    design_system_id: str
    digest: str
    document: Mapping[str, Any]


def validate_theme(document: Mapping[str, Any]) -> ValidatedTheme:
    if not isinstance(document, Mapping):
        raise ThemeValidationError("theme must be an object")
    required = {"theme_id","version","design_system_id","tokens","icon_policy","motion_policy","authority_boundary"}
    if not required.issubset(document):
        raise ThemeValidationError(f"theme missing fields: {sorted(required-set(document))}")
    boundary=document["authority_boundary"]
    if not isinstance(boundary, Mapping) or dict(boundary)!={
        "presentation_only": True,
        "changes_authorization": False,
        "changes_module_identity": False,
    }:
        raise ThemeValidationError("theme crosses authority boundary")
    motion=document["motion_policy"]
    if not isinstance(motion, Mapping) or motion.get("reduced_motion_supported") is not True:
        raise ThemeValidationError("reduced-motion support is required")
    tokens=document["tokens"]
    if not isinstance(tokens, Mapping) or tokens.get("density") not in {"comfortable","compact","touch"}:
        raise ThemeValidationError("theme density is invalid")
    return ValidatedTheme(
        theme_id=str(document["theme_id"]), version=str(document["version"]),
        design_system_id=str(document["design_system_id"]), digest=artifact_digest(document),
        document=MappingProxyType(dict(document)),
    )
