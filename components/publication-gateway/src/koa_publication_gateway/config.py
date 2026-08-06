"""Strict, side-effect-free Publication Gateway configuration."""

from __future__ import annotations

from dataclasses import dataclass, fields
import os
from pathlib import Path
from types import MappingProxyType
from typing import Any, ClassVar, Mapping
import tomllib


class ConfigurationError(ValueError):
    """Raised when configuration violates the Publication Gateway contract."""


_SECRET_MARKERS = (
    "api_key",
    "authorization",
    "credential",
    "password",
    "private_key",
    "secret",
    "token",
)


def _text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if any(character.isspace() for character in normalized):
        raise ConfigurationError(f"{field_name} must not contain whitespace")
    return normalized


def _path(value: object, field_name: str) -> Path:
    if isinstance(value, Path):
        result = value
    elif isinstance(value, str):
        result = Path(value.strip())
    else:
        raise ConfigurationError(f"{field_name} must be a path string")
    if not result.is_absolute():
        raise ConfigurationError(f"{field_name} must be an absolute path")
    if ".." in result.parts:
        raise ConfigurationError(f"{field_name} must not contain parent traversal")
    return result


def _positive_int(value: object, field_name: str, *, maximum: int) -> int:
    if isinstance(value, bool):
        raise ConfigurationError(f"{field_name} must be an integer")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{field_name} must be an integer") from exc
    if not 1 <= parsed <= maximum:
        raise ConfigurationError(f"{field_name} must be between 1 and {maximum}")
    return parsed


def _boolean(value: object, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ConfigurationError(f"{field_name} must be a boolean")


@dataclass(frozen=True, slots=True)
class PublicationGatewayConfig:
    """Validated operational bounds and non-secret references."""

    COMPONENT_ID: ClassVar[str] = "publication_gateway"
    CONTRACT_VERSION: ClassVar[str] = "1.0.0"
    INTERFACE_VERSION: ClassVar[str] = "1.0.0"
    ENV_PREFIX: ClassVar[str] = "KOA_PUBLICATION_GATEWAY_"

    component_id: str = COMPONENT_ID
    contract_version: str = CONTRACT_VERSION
    interface_version: str = INTERFACE_VERSION
    service_identity: str = COMPONENT_ID
    instance_id: str = "publication_gateway.local"
    unix_socket_path: Path = Path("/run/koa/sockets/publication-gateway.sock")
    state_directory: Path = Path("/var/lib/koa/publication-gateway")
    runtime_directory: Path = Path("/run/koa/publication")
    receipt_directory: Path = Path("/var/lib/koa/receipts/publication-gateway")
    staging_directory: Path = Path("/var/lib/koa/publication-gateway/staging")
    cache_directory: Path = Path("/var/cache/koa/publication-gateway")
    max_queue_depth: int = 1024
    max_concurrent_publications: int = 8
    max_request_bytes: int = 8 * 1024 * 1024
    max_retry_attempts: int = 3
    audit_required: bool = True

    def __post_init__(self) -> None:
        if self.component_id != self.COMPONENT_ID:
            raise ConfigurationError(f"component_id must be {self.COMPONENT_ID!r}")
        if self.contract_version != self.CONTRACT_VERSION:
            raise ConfigurationError(
                f"unsupported contract_version {self.contract_version!r}"
            )
        if self.interface_version != self.INTERFACE_VERSION:
            raise ConfigurationError(
                f"unsupported interface_version {self.interface_version!r}"
            )
        object.__setattr__(self, "service_identity", _text(self.service_identity, "service_identity"))
        object.__setattr__(self, "instance_id", _text(self.instance_id, "instance_id"))
        for field_name in (
            "unix_socket_path",
            "state_directory",
            "runtime_directory",
            "receipt_directory",
            "staging_directory",
            "cache_directory",
        ):
            object.__setattr__(self, field_name, _path(getattr(self, field_name), field_name))
        if self.unix_socket_path.name in {"", ".", ".."}:
            raise ConfigurationError("unix_socket_path must identify a socket file")
        if self.state_directory == self.runtime_directory:
            raise ConfigurationError("state_directory and runtime_directory must remain distinct")
        if not self.staging_directory.is_relative_to(self.state_directory):
            raise ConfigurationError("staging_directory must remain within state_directory")
        for field_name, maximum in (
            ("max_queue_depth", 1_000_000),
            ("max_concurrent_publications", 100_000),
            ("max_request_bytes", 1_073_741_824),
            ("max_retry_attempts", 1000),
        ):
            object.__setattr__(
                self,
                field_name,
                _positive_int(getattr(self, field_name), field_name, maximum=maximum),
            )
        if self.max_concurrent_publications > self.max_queue_depth:
            raise ConfigurationError(
                "max_concurrent_publications must not exceed max_queue_depth"
            )
        object.__setattr__(self, "audit_required", _boolean(self.audit_required, "audit_required"))

    @classmethod
    def from_mapping(cls, values: Mapping[str, object]) -> "PublicationGatewayConfig":
        if not isinstance(values, Mapping):
            raise ConfigurationError("configuration must be a mapping")
        allowed = {item.name for item in fields(cls) if not item.name.isupper()}
        unknown = sorted(set(values) - allowed)
        if unknown:
            raise ConfigurationError("unknown configuration fields: " + ", ".join(unknown))
        for key in values:
            lowered = key.lower()
            if any(marker in lowered for marker in _SECRET_MARKERS):
                raise ConfigurationError(f"secret-bearing configuration field is prohibited: {key}")
        return cls(**dict(values))

    @classmethod
    def from_toml(cls, path: str | Path) -> "PublicationGatewayConfig":
        source = Path(path)
        if not source.is_file():
            raise ConfigurationError(f"configuration file does not exist: {source}")
        try:
            document = tomllib.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise ConfigurationError(f"invalid TOML configuration: {exc}") from exc
        section = document.get("publication_gateway", document)
        if not isinstance(section, Mapping):
            raise ConfigurationError("publication_gateway configuration must be a table")
        return cls.from_mapping(section)

    @classmethod
    def from_environment(
        cls, environment: Mapping[str, str] | None = None
    ) -> "PublicationGatewayConfig":
        env = MappingProxyType(dict(os.environ if environment is None else environment))
        prefix = cls.ENV_PREFIX
        mapping: dict[str, object] = {}
        names = {item.name: item for item in fields(cls) if not item.name.isupper()}
        for name, item in names.items():
            key = prefix + name.upper()
            if key not in env:
                continue
            raw: object = env[key]
            if item.type in {int, "int"}:
                raw = _positive_int(raw, name, maximum=1_073_741_824)
            elif item.type in {bool, "bool"}:
                raw = _boolean(raw, name)
            elif "Path" in str(item.type):
                raw = Path(str(raw).strip())
            mapping[name] = raw
        declared_keys = {prefix + name.upper() for name in names}
        prefixed_keys = {key for key in env if key.startswith(prefix)}
        forbidden = sorted(
            key
            for key in prefixed_keys
            if any(marker.upper() in key for marker in _SECRET_MARKERS)
        )
        if forbidden:
            raise ConfigurationError(
                "secret-bearing environment variables are prohibited: " + ", ".join(forbidden)
            )
        unknown = sorted(prefixed_keys - declared_keys)
        if unknown:
            raise ConfigurationError(
                "unknown Publication Gateway environment variables: " + ", ".join(unknown)
            )
        return cls.from_mapping(mapping)

    @classmethod
    def load(
        cls,
        *,
        path: str | Path | None = None,
        environment: Mapping[str, str] | None = None,
    ) -> "PublicationGatewayConfig":
        if path is not None and environment is not None:
            raise ConfigurationError("select exactly one configuration source")
        if path is not None:
            return cls.from_toml(path)
        return cls.from_environment(environment)

    def as_public_dict(self) -> dict[str, object]:
        return {
            "audit_required": self.audit_required,
            "cache_directory": str(self.cache_directory),
            "component_id": self.component_id,
            "contract_version": self.contract_version,
            "instance_id": self.instance_id,
            "interface_version": self.interface_version,
            "max_concurrent_publications": self.max_concurrent_publications,
            "max_queue_depth": self.max_queue_depth,
            "max_request_bytes": self.max_request_bytes,
            "max_retry_attempts": self.max_retry_attempts,
            "receipt_directory": str(self.receipt_directory),
            "runtime_directory": str(self.runtime_directory),
            "service_identity": self.service_identity,
            "staging_directory": str(self.staging_directory),
            "state_directory": str(self.state_directory),
            "unix_socket_path": str(self.unix_socket_path),
        }
