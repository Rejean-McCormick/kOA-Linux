"""Strict local loader for canonical JSON, TOML, and YAML authorities."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from pathlib import Path
import tomllib
from typing import Any, Mapping
from urllib.parse import urlparse

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
import yaml

from .diagnostics import AssemblyDiagnosticError, Diagnostic, DiagnosticBag
from .model import (
    ContractFormat,
    ContractReference,
    ContractSource,
    LoadedContract,
    freeze_mapping,
    infer_contract_identity,
)


AUTHORITY_CONTRACT = "docs/contracts/ai-navigation.contract.json"
AUTHORITY_SCHEMA = "declared $schema"


@dataclass(frozen=True, slots=True)
class LoadPolicy:
    """Closed policy for local authority loading."""

    allowed_roots: tuple[str, ...] = (
        "docs/contracts",
        "docs/schemas",
        "profiles",
        ".koa",
    )
    max_bytes: int = 16 * 1024 * 1024
    require_declared_schema: bool = True

    def __post_init__(self) -> None:
        if not self.allowed_roots:
            raise ValueError("at least one authority root is required")
        normalized: list[str] = []
        for root in self.allowed_roots:
            reference = ContractReference(root + "/placeholder")
            normalized.append(str(Path(reference.path).parent).replace("\\", "/"))
        object.__setattr__(self, "allowed_roots", tuple(sorted(set(normalized))))
        if self.max_bytes <= 0:
            raise ValueError("max_bytes must be positive")


@dataclass(frozen=True, slots=True)
class LoadOutcome:
    contract: LoadedContract | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def passed(self) -> bool:
        return self.contract is not None and not any(
            item.severity.value == "error" for item in self.diagnostics
        )

    def require(self) -> LoadedContract:
        if not self.passed or self.contract is None:
            raise AssemblyDiagnosticError("contract loading was blocked", self.diagnostics)
        return self.contract


class ContractLoader:
    """Loads only local, repository-contained authority documents."""

    def __init__(
        self,
        repository_root: str | Path,
        *,
        policy: LoadPolicy | None = None,
    ) -> None:
        self.repository_root = Path(repository_root).expanduser().resolve(strict=True)
        if not self.repository_root.is_dir():
            raise ValueError("repository_root must be a directory")
        self.policy = policy or LoadPolicy()
        self._schema_registry: Registry[Any] | None = None

    def load(self, reference: str | ContractReference) -> LoadedContract:
        return self.try_load(reference).require()

    def try_load(self, reference: str | ContractReference) -> LoadOutcome:
        diagnostics = DiagnosticBag()
        try:
            parsed = (
                reference if isinstance(reference, ContractReference) else ContractReference.parse(reference)
            )
        except (TypeError, ValueError) as exc:
            diagnostics.error(
                "ASSEMBLY_REFERENCE_INVALID",
                str(exc),
                authority=AUTHORITY_CONTRACT,
                source_path=str(reference),
            )
            return LoadOutcome(None, diagnostics.sorted())

        source_path = parsed.path
        path = self._resolve_authority_path(parsed, diagnostics)
        if path is None:
            return LoadOutcome(None, diagnostics.sorted())

        raw = self._read_bytes(path, source_path, diagnostics)
        if raw is None:
            return LoadOutcome(None, diagnostics.sorted())

        fmt = _format_for_path(path, diagnostics, source_path)
        if fmt is None:
            return LoadOutcome(None, diagnostics.sorted())

        data = self._parse(raw, fmt, source_path, diagnostics)
        if data is None:
            return LoadOutcome(None, diagnostics.sorted())
        if not isinstance(data, dict):
            diagnostics.error(
                "ASSEMBLY_TOP_LEVEL_NOT_OBJECT",
                "authority documents must have an object at the top level",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
                pointer="/",
            )
            return LoadOutcome(None, diagnostics.sorted())

        declared_schema = data.get("$schema")
        schema_reference = self._declared_schema_reference(path, data, diagnostics)
        if schema_reference is not None:
            self._validate_against_schema(data, schema_reference, source_path, diagnostics)
        elif _is_json_schema_dialect(declared_schema) and _looks_like_schema(data):
            self._validate_schema_document(data, source_path, diagnostics)
        elif self.policy.require_declared_schema and declared_schema is None:
            diagnostics.error(
                "ASSEMBLY_SCHEMA_REQUIRED",
                "authority document does not declare $schema",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
                pointer="/$schema",
                hint="Add the canonical local schema reference in the owning contract bundle.",
            )

        try:
            identity = infer_contract_identity(data, fallback_identifier=Path(source_path).stem)
            frozen = freeze_mapping(data)
        except (TypeError, ValueError) as exc:
            diagnostics.error(
                "ASSEMBLY_MODEL_INVALID",
                str(exc),
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
            )
            return LoadOutcome(None, diagnostics.sorted())

        if diagnostics.has_errors:
            return LoadOutcome(None, diagnostics.sorted())

        contract = LoadedContract(
            identity=identity,
            source=ContractSource(
                reference=parsed,
                format=fmt,
                sha256=sha256(raw).hexdigest(),
                schema_reference=schema_reference,
            ),
            data=frozen,
        )
        return LoadOutcome(contract, diagnostics.sorted())

    def scan(self, root: str | ContractReference) -> tuple[LoadOutcome, ...]:
        """Load supported files under one allowed authority directory in sorted order."""

        reference = root if isinstance(root, ContractReference) else ContractReference.parse(root)
        bag = DiagnosticBag()
        path = self._resolve_authority_path(reference, bag, allow_directory=True)
        if path is None:
            return (LoadOutcome(None, bag.sorted()),)
        if not path.is_dir():
            return (self.try_load(reference),)
        outcomes: list[LoadOutcome] = []
        for candidate in sorted(path.rglob("*")):
            if candidate.is_file() and candidate.suffix.lower() in {".json", ".toml", ".yaml", ".yml"}:
                relative = candidate.relative_to(self.repository_root).as_posix()
                outcomes.append(self.try_load(ContractReference(relative)))
        return tuple(outcomes)

    def _resolve_authority_path(
        self,
        reference: ContractReference,
        diagnostics: DiagnosticBag,
        *,
        allow_directory: bool = False,
    ) -> Path | None:
        source_path = reference.path
        lexical = self.repository_root.joinpath(*Path(source_path).parts)
        try:
            resolved = lexical.resolve(strict=True)
        except FileNotFoundError:
            diagnostics.error(
                "ASSEMBLY_SOURCE_MISSING",
                "authority source does not exist",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
            )
            return None
        if not resolved.is_relative_to(self.repository_root):
            diagnostics.error(
                "ASSEMBLY_SOURCE_ESCAPE",
                "authority source resolves outside the repository",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
            )
            return None
        relative = resolved.relative_to(self.repository_root).as_posix()
        if not any(relative == root or relative.startswith(root + "/") for root in self.policy.allowed_roots):
            diagnostics.error(
                "ASSEMBLY_SOURCE_ROOT_FORBIDDEN",
                "source is outside the closed authority roots",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
                context={"allowed_roots": ",".join(self.policy.allowed_roots)},
            )
            return None
        if allow_directory:
            if not (resolved.is_file() or resolved.is_dir()):
                diagnostics.error(
                    "ASSEMBLY_SOURCE_TYPE_INVALID",
                    "source must be a regular file or directory",
                    authority=AUTHORITY_CONTRACT,
                    source_path=source_path,
                )
                return None
        elif not resolved.is_file():
            diagnostics.error(
                "ASSEMBLY_SOURCE_NOT_FILE",
                "authority source must be a regular file",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
            )
            return None
        return resolved

    def _read_bytes(
        self, path: Path, source_path: str, diagnostics: DiagnosticBag
    ) -> bytes | None:
        size = path.stat().st_size
        if size > self.policy.max_bytes:
            diagnostics.error(
                "ASSEMBLY_SOURCE_TOO_LARGE",
                "authority source exceeds the configured size limit",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
                context={"bytes": size, "max_bytes": self.policy.max_bytes},
            )
            return None
        raw = path.read_bytes()
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            diagnostics.error(
                "ASSEMBLY_UTF8_REQUIRED",
                f"authority source is not valid UTF-8: {exc}",
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
            )
            return None
        return raw

    def _parse(
        self,
        raw: bytes,
        fmt: ContractFormat,
        source_path: str,
        diagnostics: DiagnosticBag,
    ) -> Any | None:
        try:
            if fmt is ContractFormat.JSON:
                value = json.loads(
                    raw,
                    object_pairs_hook=_reject_duplicate_json_keys,
                    parse_constant=_reject_non_finite_constant,
                )
            elif fmt is ContractFormat.TOML:
                value = tomllib.loads(raw.decode("utf-8"))
            else:
                value = yaml.load(raw.decode("utf-8"), Loader=_UniqueKeySafeLoader)
            _validate_json_compatibility(value)
            return value
        except (UnicodeDecodeError, ValueError, TypeError, tomllib.TOMLDecodeError, yaml.YAMLError) as exc:
            diagnostics.error(
                "ASSEMBLY_PARSE_FAILED",
                str(exc),
                authority=AUTHORITY_CONTRACT,
                source_path=source_path,
            )
            return None

    def _declared_schema_reference(
        self,
        source_path: Path,
        data: Mapping[str, Any],
        diagnostics: DiagnosticBag,
    ) -> ContractReference | None:
        declared = data.get("$schema")
        source_relative = source_path.relative_to(self.repository_root).as_posix()
        if declared is None:
            return None
        if not isinstance(declared, str) or not declared.strip():
            diagnostics.error(
                "ASSEMBLY_SCHEMA_REFERENCE_INVALID",
                "$schema must be a non-empty string",
                authority=AUTHORITY_CONTRACT,
                source_path=source_relative,
                pointer="/$schema",
            )
            return None
        parsed = urlparse(declared)
        if parsed.scheme in {"http", "https"}:
            if parsed.netloc != "json-schema.org":
                diagnostics.error(
                    "ASSEMBLY_REMOTE_SCHEMA_FORBIDDEN",
                    "remote authority schemas are not fetched",
                    authority=AUTHORITY_CONTRACT,
                    source_path=source_relative,
                    pointer="/$schema",
                )
            return None
        if parsed.scheme:
            diagnostics.error(
                "ASSEMBLY_SCHEMA_SCHEME_FORBIDDEN",
                "only repository-relative schemas or the JSON Schema dialect URI are allowed",
                authority=AUTHORITY_CONTRACT,
                source_path=source_relative,
                pointer="/$schema",
            )
            return None
        schema_path = (source_path.parent / parsed.path).resolve(strict=False)
        if not schema_path.is_relative_to(self.repository_root):
            diagnostics.error(
                "ASSEMBLY_SCHEMA_ESCAPE",
                "declared schema resolves outside the repository",
                authority=AUTHORITY_CONTRACT,
                source_path=source_relative,
                pointer="/$schema",
            )
            return None
        relative = schema_path.relative_to(self.repository_root).as_posix()
        try:
            return ContractReference(relative, parsed.fragment)
        except ValueError as exc:
            diagnostics.error(
                "ASSEMBLY_SCHEMA_REFERENCE_INVALID",
                str(exc),
                authority=AUTHORITY_CONTRACT,
                source_path=source_relative,
                pointer="/$schema",
            )
            return None

    def _validate_against_schema(
        self,
        data: Mapping[str, Any],
        schema_reference: ContractReference,
        source_path: str,
        diagnostics: DiagnosticBag,
    ) -> None:
        schema_path = self.repository_root / schema_reference.path
        if not schema_path.is_file():
            diagnostics.error(
                "ASSEMBLY_SCHEMA_MISSING",
                "declared local schema does not exist",
                authority=AUTHORITY_SCHEMA,
                source_path=source_path,
                pointer="/$schema",
                context={"schema": str(schema_reference)},
            )
            return
        try:
            schema_document = json.loads(
                schema_path.read_bytes(),
                object_pairs_hook=_reject_duplicate_json_keys,
                parse_constant=_reject_non_finite_constant,
            )
            if not isinstance(schema_document, dict):
                raise ValueError("schema must be a JSON object")
            schema = _resolve_plain_pointer(schema_document, schema_reference.pointer)
            if not isinstance(schema, dict):
                raise ValueError("selected schema fragment must be a JSON object")
            validator_class = validator_for(schema_document)
            validator_class.check_schema(schema_document)
            validator = validator_class(
                schema,
                registry=self._get_schema_registry(),
                format_checker=FormatChecker(),
            )
            errors = sorted(
                validator.iter_errors(data),
                key=lambda error: (
                    tuple(str(part) for part in error.absolute_path),
                    tuple(str(part) for part in error.absolute_schema_path),
                    error.message,
                ),
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError, Unresolvable) as exc:
            diagnostics.error(
                "ASSEMBLY_SCHEMA_INVALID",
                str(exc),
                authority=schema_reference.path,
                source_path=source_path,
                pointer="/$schema",
            )
            return
        for error in errors:
            diagnostics.error(
                "ASSEMBLY_CONTRACT_SCHEMA_VIOLATION",
                error.message,
                authority=schema_reference.path,
                source_path=source_path,
                pointer=_json_pointer(error.absolute_path),
                context={"schema_pointer": _json_pointer(error.absolute_schema_path)},
            )


    def _validate_schema_document(
        self,
        data: Mapping[str, Any],
        source_path: str,
        diagnostics: DiagnosticBag,
    ) -> None:
        try:
            validator_class = validator_for(data)
            validator_class.check_schema(data)
        except (ValueError, TypeError) as exc:
            diagnostics.error(
                "ASSEMBLY_SCHEMA_INVALID",
                str(exc),
                authority=str(data.get("$schema", "JSON Schema dialect")),
                source_path=source_path,
                pointer="/$schema",
            )

    def _get_schema_registry(self) -> Registry[Any]:
        if self._schema_registry is not None:
            return self._schema_registry
        registry: Registry[Any] = Registry()
        schema_root = self.repository_root / "docs" / "schemas"
        if schema_root.is_dir():
            resources: list[tuple[str, Resource[Any]]] = []
            for path in sorted(schema_root.rglob("*.json")):
                try:
                    contents = json.loads(
                        path.read_bytes(),
                        object_pairs_hook=_reject_duplicate_json_keys,
                        parse_constant=_reject_non_finite_constant,
                    )
                    if not isinstance(contents, dict):
                        continue
                    resource = Resource.from_contents(contents)
                except (ValueError, TypeError, json.JSONDecodeError):
                    continue
                resources.append((path.resolve().as_uri(), resource))
                identifier = contents.get("$id")
                if isinstance(identifier, str) and identifier:
                    resources.append((identifier, resource))
            registry = registry.with_resources(resources)
        self._schema_registry = registry
        return registry


def _format_for_path(
    path: Path, diagnostics: DiagnosticBag, source_path: str
) -> ContractFormat | None:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return ContractFormat.JSON
    if suffix == ".toml":
        return ContractFormat.TOML
    if suffix in {".yaml", ".yml"}:
        return ContractFormat.YAML
    diagnostics.error(
        "ASSEMBLY_FORMAT_UNSUPPORTED",
        "supported authority formats are JSON, TOML, and YAML",
        authority=AUTHORITY_CONTRACT,
        source_path=source_path,
    )
    return None


def _reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result


def _reject_non_finite_constant(value: str) -> Any:
    raise ValueError(f"non-finite number is forbidden: {value}")


class _UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: _UniqueKeySafeLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueKeySafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _validate_json_compatibility(value: Any, pointer: str = "") -> None:
    if value is None or isinstance(value, (bool, int, str)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"non-finite number at {pointer or '/'}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_json_compatibility(item, f"{pointer}/{index}")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(f"non-string object key at {pointer or '/'}")
            token = key.replace("~", "~0").replace("/", "~1")
            _validate_json_compatibility(item, f"{pointer}/{token}")
        return
    raise TypeError(f"non-JSON value {type(value).__name__} at {pointer or '/'}")


def _json_pointer(parts: Any) -> str:
    encoded = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "" if not encoded else "/" + "/".join(encoded)


def _is_json_schema_dialect(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and parsed.netloc == "json-schema.org"


def _looks_like_schema(data: Mapping[str, Any]) -> bool:
    return any(key in data for key in ("$id", "$defs", "type", "properties", "allOf"))


def _resolve_plain_pointer(document: Any, pointer: str) -> Any:
    if not pointer:
        return document
    if not pointer.startswith("/"):
        raise ValueError("schema fragment must be a JSON Pointer")
    current = document
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            raise ValueError(f"schema fragment does not resolve: {pointer}")
    return current
