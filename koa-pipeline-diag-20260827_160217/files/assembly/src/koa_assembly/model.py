"""Core immutable model for contract-driven kOA assembly.

This module deliberately contains no component or service inventory.  Membership
is loaded from canonical contracts by later assembly stages.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
import json
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence, TypeAlias


JsonScalar: TypeAlias = None | bool | int | float | str
FrozenJson: TypeAlias = JsonScalar | tuple["FrozenJson", ...] | Mapping[str, "FrozenJson"]


class ContractFormat(StrEnum):
    JSON = "json"
    TOML = "toml"
    YAML = "yaml"


class DocumentClass(StrEnum):
    CONTRACT = "contract"
    SCHEMA = "schema"
    DECLARATION = "declaration"


class CompositionStatus(StrEnum):
    PASS = "pass"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class ContractReference:
    """Repository-relative document reference with an optional JSON pointer."""

    path: str
    pointer: str = ""

    def __post_init__(self) -> None:
        path = self.path.strip().replace("\\", "/")
        if not path:
            raise ValueError("contract reference path must not be empty")
        pure = PurePosixPath(path)
        if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
            raise ValueError("contract reference must be a normalized repository-relative path")
        pointer = self.pointer.strip()
        if pointer and not pointer.startswith("/"):
            raise ValueError("JSON pointer must be empty or start with '/'")
        object.__setattr__(self, "path", pure.as_posix())
        object.__setattr__(self, "pointer", pointer)

    @classmethod
    def parse(cls, value: str) -> "ContractReference":
        if not isinstance(value, str) or not value.strip():
            raise ValueError("contract reference must be a non-empty string")
        path, separator, fragment = value.partition("#")
        if separator and fragment and not fragment.startswith("/"):
            raise ValueError("only JSON Pointer fragments are supported")
        return cls(path=path, pointer=fragment)

    def __str__(self) -> str:
        return self.path + (f"#{self.pointer}" if self.pointer else "")


@dataclass(frozen=True, slots=True)
class ContractIdentity:
    """Stable identity extracted from a loaded authority document."""

    identifier: str
    version: str | None
    status: str | None
    document_class: DocumentClass

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise ValueError("contract identifier must not be empty")
        if self.version is not None and not self.version.strip():
            raise ValueError("contract version must be non-empty when present")
        if self.status is not None and not self.status.strip():
            raise ValueError("contract status must be non-empty when present")


@dataclass(frozen=True, slots=True)
class ContractSource:
    """Provenance for one loaded contract or schema."""

    reference: ContractReference
    format: ContractFormat
    sha256: str
    schema_reference: ContractReference | None = None

    def __post_init__(self) -> None:
        digest = self.sha256.lower()
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValueError("sha256 must be a 64-character lowercase hexadecimal digest")
        object.__setattr__(self, "sha256", digest)


@dataclass(frozen=True, slots=True)
class LoadedContract:
    """Validated immutable authority document."""

    identity: ContractIdentity
    source: ContractSource
    data: Mapping[str, FrozenJson]

    def __post_init__(self) -> None:
        object.__setattr__(self, "data", freeze_mapping(self.data))

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.data)

    def resolve_pointer(self, pointer: str | None = None) -> FrozenJson:
        selected = self.source.reference.pointer if pointer is None else pointer
        return resolve_json_pointer(self.data, selected)


@dataclass(frozen=True, slots=True)
class AssemblyRequest:
    """Inputs selected for a later profile-composition run."""

    primary_profile: ContractReference
    overlays: tuple[ContractReference, ...] = ()
    implementation_settings: tuple[ContractReference, ...] = ()
    requested_by: str = ""

    def __post_init__(self) -> None:
        overlays = _unique_references(self.overlays, "overlay")
        settings = _unique_references(self.implementation_settings, "implementation setting")
        object.__setattr__(self, "overlays", tuple(sorted(overlays, key=str)))
        object.__setattr__(self, "implementation_settings", tuple(sorted(settings, key=str)))
        if self.primary_profile in self.overlays:
            raise ValueError("a primary profile cannot also be selected as an overlay")

    def to_dict(self) -> dict[str, Any]:
        return {
            "primary_profile": str(self.primary_profile),
            "overlays": [str(item) for item in self.overlays],
            "implementation_settings": [str(item) for item in self.implementation_settings],
            "requested_by": self.requested_by,
        }

    @property
    def request_digest(self) -> str:
        return sha256(canonical_json_bytes(self.to_dict())).hexdigest()


@dataclass(frozen=True, slots=True)
class AssemblyInputSet:
    """Validated input contracts grouped without inferring membership."""

    request: AssemblyRequest
    primary_profile: LoadedContract
    overlays: tuple[LoadedContract, ...] = ()
    implementation_settings: tuple[LoadedContract, ...] = ()
    additional_authorities: tuple[LoadedContract, ...] = ()

    def __post_init__(self) -> None:
        if self.primary_profile.source.reference != self.request.primary_profile:
            raise ValueError("loaded primary profile does not match the request")
        _ensure_loaded_match(self.request.overlays, self.overlays, "overlay")
        _ensure_loaded_match(
            self.request.implementation_settings,
            self.implementation_settings,
            "implementation setting",
        )
        object.__setattr__(
            self,
            "additional_authorities",
            tuple(sorted(self.additional_authorities, key=lambda item: str(item.source.reference))),
        )

    @property
    def source_digest(self) -> str:
        records = [
            {
                "reference": str(contract.source.reference),
                "sha256": contract.source.sha256,
                "identifier": contract.identity.identifier,
                "version": contract.identity.version,
            }
            for contract in (
                self.primary_profile,
                *self.overlays,
                *self.implementation_settings,
                *self.additional_authorities,
            )
        ]
        return sha256(canonical_json_bytes(records)).hexdigest()


@dataclass(frozen=True, slots=True)
class AssemblyResult:
    """Core result envelope; later bundles populate effective-profile data."""

    status: CompositionStatus
    request_digest: str
    source_digest: str
    diagnostic_codes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for field_name in ("request_digest", "source_digest"):
            value = getattr(self, field_name)
            if len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
                raise ValueError(f"{field_name} must be a SHA-256 digest")
        codes = tuple(sorted(set(self.diagnostic_codes)))
        object.__setattr__(self, "diagnostic_codes", codes)
        if self.status is CompositionStatus.PASS and codes:
            raise ValueError("a passing result cannot carry blocking diagnostic codes")


_IDENTITY_FIELDS = (
    "contract_id",
    "component_id",
    "subsystem_id",
    "profile_id",
    "integration_id",
    "toolchain_id",
    "schema_id",
    "$id",
)


def infer_contract_identity(
    data: Mapping[str, Any], *, fallback_identifier: str
) -> ContractIdentity:
    """Extract an identity without assuming a component or service inventory."""

    found: list[tuple[str, str]] = []
    for field_name in _IDENTITY_FIELDS:
        value = data.get(field_name)
        if isinstance(value, str) and value.strip():
            found.append((field_name, value.strip()))
    if found:
        # Identity fields are ordered by authority specificity.  A contract may
        # describe a nested system/component identity without changing the
        # identity of the contract document itself.
        identifier = found[0][1]
        same_priority = {value for field, value in found if field == found[0][0]}
        if len(same_priority) > 1:
            raise ValueError(f"authority document exposes conflicting identifiers: {sorted(same_priority)}")
    else:
        system = data.get("system")
        system_id = system.get("system_id") if isinstance(system, Mapping) else None
        identifier = (
            system_id.strip()
            if isinstance(system_id, str) and system_id.strip()
            else fallback_identifier
        )
    document_class = (
        DocumentClass.SCHEMA
        if "$schema" in data and ("$id" in data or "$defs" in data) and "type" in data
        else DocumentClass.CONTRACT
    )
    version = data.get("version")
    status = data.get("status")
    return ContractIdentity(
        identifier=identifier,
        version=version if isinstance(version, str) else None,
        status=status if isinstance(status, str) else None,
        document_class=document_class,
    )


def freeze_json(value: Any) -> FrozenJson:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("non-finite numbers are not valid contract data")
        return value
    if isinstance(value, Mapping):
        return freeze_mapping(value)
    if isinstance(value, (list, tuple)):
        return tuple(freeze_json(item) for item in value)
    raise TypeError(f"contract value is not JSON-compatible: {type(value).__name__}")


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, FrozenJson]:
    normalized: dict[str, FrozenJson] = {}
    for key in sorted(value):
        if not isinstance(key, str):
            raise TypeError("contract object keys must be strings")
        normalized[key] = freeze_json(value[key])
    return MappingProxyType(normalized)


def thaw_json(value: FrozenJson) -> Any:
    if isinstance(value, Mapping):
        return {key: thaw_json(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [thaw_json(item) for item in value]
    return value


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            thaw_json(freeze_json(value)),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def resolve_json_pointer(document: FrozenJson, pointer: str) -> FrozenJson:
    if not pointer:
        return document
    if not pointer.startswith("/"):
        raise ValueError("JSON pointer must start with '/'")
    current: FrozenJson = document
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, Mapping):
            if token not in current:
                raise KeyError(pointer)
            current = current[token]
        elif isinstance(current, tuple):
            if not token.isdigit():
                raise KeyError(pointer)
            index = int(token)
            if index >= len(current):
                raise KeyError(pointer)
            current = current[index]
        else:
            raise KeyError(pointer)
    return current


def _unique_references(
    references: Sequence[ContractReference], label: str
) -> tuple[ContractReference, ...]:
    normalized = tuple(references)
    if any(not isinstance(item, ContractReference) for item in normalized):
        raise TypeError(f"every {label} must be a ContractReference")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"duplicate {label} reference")
    return normalized


def _ensure_loaded_match(
    expected: Iterable[ContractReference], loaded: Sequence[LoadedContract], label: str
) -> None:
    expected_set = set(expected)
    actual = {item.source.reference for item in loaded}
    if expected_set != actual:
        raise ValueError(f"loaded {label} contracts do not match the request")
