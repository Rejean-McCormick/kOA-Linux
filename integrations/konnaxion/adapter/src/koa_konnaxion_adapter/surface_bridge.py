"""Non-authoritative projection of boundary-owned interface manifests."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
import json
from types import MappingProxyType
from typing import Any


_FORBIDDEN_CATALOG_KEYS = {
    "complete_api",
    "internal_domain_model",
    "internal_state_machine",
    "internal_validation_logic",
    "internal_workflow",
}
_SECRET_KEYS = {"access_token", "api_key", "authorization", "cookie", "password", "private_key", "secret", "token"}


@dataclass(frozen=True, slots=True)
class SurfaceSnapshot:
    manifests: Mapping[str, Mapping[str, Any]]
    alignment_state: str
    presentation_only: bool = True
    authoritative: bool = False
    transfers_authority: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "integration_id": "konnaxion",
            "alignment_state": self.alignment_state,
            "presentation_only": True,
            "authoritative": False,
            "transfers_authority": False,
            "manifests": deepcopy({name: dict(value) for name, value in self.manifests.items()}),
        }


class SurfaceBridge:
    EXPECTED_MANIFESTS = ("module-interface", "sidebar", "widgets")

    def __init__(self, manifests: Mapping[str, Mapping[str, Any]], *, alignment_state: str) -> None:
        if set(manifests) != set(self.EXPECTED_MANIFESTS):
            raise ValueError(f"surface manifests must be exactly {self.EXPECTED_MANIFESTS!r}")
        normalized: dict[str, Mapping[str, Any]] = {}
        for name in self.EXPECTED_MANIFESTS:
            value = deepcopy(dict(manifests[name]))
            _validate_json_boundary(value, path=name, depth=0)
            encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
            if len(encoded) > 131072:
                raise ValueError(f"{name} exceeds the boundary manifest size")
            normalized[name] = MappingProxyType(value)
        if alignment_state not in {"prepared_only", "aligned"}:
            raise ValueError("invalid alignment_state")
        self._snapshot = SurfaceSnapshot(
            manifests=MappingProxyType(normalized), alignment_state=alignment_state
        )

    def snapshot(self) -> SurfaceSnapshot:
        return self._snapshot


def _validate_json_boundary(value: Any, *, path: str, depth: int) -> None:
    if depth > 16:
        raise ValueError(f"{path} exceeds maximum nesting depth")
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise ValueError(f"{path} contains a non-string key")
            lowered = key.lower()
            if lowered in _SECRET_KEYS:
                raise ValueError(f"{path} contains secret-like field {key!r}")
            if lowered in _FORBIDDEN_CATALOG_KEYS:
                raise ValueError(f"{path} duplicates prohibited Konnaxion internal catalog {key!r}")
            _validate_json_boundary(child, path=f"{path}.{key}", depth=depth + 1)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            _validate_json_boundary(child, path=f"{path}[{index}]", depth=depth + 1)
    elif value is not None and not isinstance(value, (str, int, float, bool)):
        raise ValueError(f"{path} contains a non-JSON value")
