"""Strict, secret-free configuration for Identity and Trust."""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from enum import StrEnum
import os
from pathlib import Path, PurePosixPath
import re
import tomllib
from typing import Any, Mapping


class ConfigurationError(ValueError):
    """Raised when configuration is missing, ambiguous, or unsafe."""


class Profile(StrEnum):
    USER_LIGHTWEIGHT = "user_lightweight"
    DEVELOPER_LINUX_WORKSTATION = "developer_linux_workstation"
    DEVELOPER_WINDOWS_WSL = "developer_windows_wsl"
    SOVEREIGN_LINUX_NODE = "sovereign_linux_node"
    SOVEREIGN_HUB = "sovereign_hub"
    BUILD_FARM = "build_farm"
    CONTROL_PLANE = "control_plane"


class ReceiptMode(StrEnum):
    DURABLE = "durable"
    BUFFERED = "buffered"
    UNAVAILABLE = "unavailable"


class ProviderMode(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


_COMPONENT_ID = "identity_and_trust"
_PREFIX = "KOA_IDENTITY_TRUST_"
_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]{0,127}$")
_SECRET_NAMES = {
    "password",
    "password_file",
    "private_key",
    "private_key_file",
    "secret",
    "secret_file",
    "token",
    "bearer_token",
    "credential",
    "authentication_factor",
}
_ENV_TO_FIELD = {
    f"{_PREFIX}INSTANCE_ID": "instance_id",
    f"{_PREFIX}ENVIRONMENT": "environment",
    f"{_PREFIX}PROFILE": "profile",
    f"{_PREFIX}CONFIG_PATH": "config_path",
    f"{_PREFIX}STATE_ROOT": "state_root",
    f"{_PREFIX}RUNTIME_ROOT": "runtime_root",
    f"{_PREFIX}SOCKET_PATH": "socket_path",
    f"{_PREFIX}RECEIPT_MODE": "receipt_mode",
    f"{_PREFIX}RECEIPT_BUFFER_LIMIT": "receipt_buffer_limit",
    f"{_PREFIX}KEY_PROVIDER_MODE": "key_provider_mode",
    f"{_PREFIX}REVOCATION_MAX_AGE_SECONDS": "revocation_max_age_seconds",
    f"{_PREFIX}OFFLINE": "offline",
}


def _parse_bool(value: Any, *, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ConfigurationError(f"{field_name} must be an explicit boolean")


def _parse_positive_int(value: Any, *, field_name: str, allow_zero: bool = False) -> int:
    if isinstance(value, bool):
        raise ConfigurationError(f"{field_name} must be an integer")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{field_name} must be an integer") from exc
    minimum = 0 if allow_zero else 1
    if result < minimum:
        raise ConfigurationError(f"{field_name} must be >= {minimum}")
    return result


def _absolute_path(value: Any, *, field_name: str) -> Path:
    path = Path(str(value)).expanduser()
    if not path.is_absolute():
        raise ConfigurationError(f"{field_name} must be an absolute path")
    if ".." in PurePosixPath(path.as_posix()).parts:
        raise ConfigurationError(f"{field_name} cannot contain parent traversal")
    return path


def _safe_identifier(value: Any, *, field_name: str) -> str:
    result = str(value).strip().lower()
    if not _ID_PATTERN.fullmatch(result):
        raise ConfigurationError(f"{field_name} must match {_ID_PATTERN.pattern}")
    return result


@dataclass(frozen=True, slots=True)
class IdentityTrustConfig:
    """Validated component configuration containing references, never secret material."""

    component_id: str = _COMPONENT_ID
    instance_id: str = "identity-and-trust.local"
    environment: str = "development"
    profile: Profile = Profile.DEVELOPER_LINUX_WORKSTATION
    config_path: Path = Path("/etc/koa/components/identity-and-trust/config.toml")
    state_root: Path = Path("/var/lib/koa/identity-and-trust")
    runtime_root: Path = Path("/run/koa/identity-and-trust")
    socket_path: Path = Path("/run/koa/sockets/identity-and-trust.sock")
    receipt_mode: ReceiptMode = ReceiptMode.UNAVAILABLE
    receipt_buffer_limit: int = 1024
    key_provider_mode: ProviderMode = ProviderMode.UNAVAILABLE
    revocation_max_age_seconds: int = 86400
    offline: bool = False

    def __post_init__(self) -> None:
        if self.component_id != _COMPONENT_ID:
            raise ConfigurationError(f"component_id is fixed to {_COMPONENT_ID}")
        object.__setattr__(self, "instance_id", _safe_identifier(self.instance_id, field_name="instance_id"))
        object.__setattr__(self, "environment", _safe_identifier(self.environment, field_name="environment"))
        object.__setattr__(self, "profile", Profile(self.profile))
        object.__setattr__(self, "config_path", _absolute_path(self.config_path, field_name="config_path"))
        object.__setattr__(self, "state_root", _absolute_path(self.state_root, field_name="state_root"))
        object.__setattr__(self, "runtime_root", _absolute_path(self.runtime_root, field_name="runtime_root"))
        object.__setattr__(self, "socket_path", _absolute_path(self.socket_path, field_name="socket_path"))
        object.__setattr__(self, "receipt_mode", ReceiptMode(self.receipt_mode))
        object.__setattr__(self, "key_provider_mode", ProviderMode(self.key_provider_mode))
        object.__setattr__(
            self,
            "receipt_buffer_limit",
            _parse_positive_int(self.receipt_buffer_limit, field_name="receipt_buffer_limit", allow_zero=True),
        )
        object.__setattr__(
            self,
            "revocation_max_age_seconds",
            _parse_positive_int(self.revocation_max_age_seconds, field_name="revocation_max_age_seconds"),
        )
        object.__setattr__(self, "offline", _parse_bool(self.offline, field_name="offline"))
        if self.receipt_mode is ReceiptMode.BUFFERED and self.receipt_buffer_limit == 0:
            raise ConfigurationError("buffered receipt mode requires a positive receipt_buffer_limit")
        if self.config_path.suffix != ".toml":
            raise ConfigurationError("config_path must identify a TOML file")
        if self.socket_path.suffix != ".sock":
            raise ConfigurationError("socket_path must identify a Unix socket file")
        if self.state_root == Path("/") or self.runtime_root == Path("/"):
            raise ConfigurationError("state_root and runtime_root cannot be the filesystem root")
        if self.state_root == self.runtime_root:
            raise ConfigurationError("state_root and runtime_root must remain distinct")
        if self.state_root.is_relative_to(self.runtime_root) or self.runtime_root.is_relative_to(self.state_root):
            raise ConfigurationError("state_root and runtime_root cannot overlap")
        if self.socket_path.is_relative_to(self.state_root):
            raise ConfigurationError("socket_path cannot be stored in authoritative state")

    @classmethod
    def from_mapping(cls, values: Mapping[str, Any]) -> IdentityTrustConfig:
        """Build from a closed component table."""
        allowed = {field.name for field in fields(cls)} - {"component_id"}
        unknown = sorted(set(values) - allowed - {"component_id"})
        secret = sorted(name for name in values if name.lower() in _SECRET_NAMES)
        if secret:
            raise ConfigurationError(f"secret-bearing configuration keys are prohibited: {', '.join(secret)}")
        if unknown:
            raise ConfigurationError(f"unknown identity-and-trust configuration keys: {', '.join(unknown)}")
        if "component_id" in values and values["component_id"] != _COMPONENT_ID:
            raise ConfigurationError(f"component_id is fixed to {_COMPONENT_ID}")
        return cls(**{name: value for name, value in values.items() if name != "component_id"})

    @classmethod
    def from_toml(cls, path: Path | str) -> IdentityTrustConfig:
        config_path = _absolute_path(path, field_name="config_path")
        try:
            with config_path.open("rb") as stream:
                document = tomllib.load(stream)
        except FileNotFoundError as exc:
            raise ConfigurationError(f"configuration file does not exist: {config_path}") from exc
        except tomllib.TOMLDecodeError as exc:
            raise ConfigurationError(f"invalid TOML configuration: {exc}") from exc
        unknown_tables = sorted(set(document) - {"identity_and_trust"})
        if unknown_tables:
            raise ConfigurationError(f"unknown top-level TOML tables: {', '.join(unknown_tables)}")
        table = document.get("identity_and_trust")
        if not isinstance(table, dict):
            raise ConfigurationError("TOML must contain an [identity_and_trust] table")
        return replace(cls.from_mapping(table), config_path=config_path)

    @classmethod
    def load(
        cls,
        *,
        path: Path | str | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> IdentityTrustConfig:
        env = os.environ if environ is None else environ
        unknown_env = sorted(name for name in env if name.startswith(_PREFIX) and name not in _ENV_TO_FIELD)
        if unknown_env:
            raise ConfigurationError(f"unknown identity-and-trust environment variables: {', '.join(unknown_env)}")

        selected_path = path or env.get(f"{_PREFIX}CONFIG_PATH")
        config = cls.from_toml(selected_path) if selected_path else cls()
        overrides: dict[str, Any] = {}
        for env_name, field_name in _ENV_TO_FIELD.items():
            if env_name not in env or field_name == "config_path":
                continue
            overrides[field_name] = env[env_name]
        return replace(config, **overrides) if overrides else config

    def public_dict(self) -> dict[str, object]:
        """Return an operational view containing no secret material."""
        return {
            "component_id": self.component_id,
            "instance_id": self.instance_id,
            "environment": self.environment,
            "profile": self.profile.value,
            "config_path": str(self.config_path),
            "state_root": str(self.state_root),
            "runtime_root": str(self.runtime_root),
            "socket_path": str(self.socket_path),
            "receipt_mode": self.receipt_mode.value,
            "receipt_buffer_limit": self.receipt_buffer_limit,
            "key_provider_mode": self.key_provider_mode.value,
            "revocation_max_age_seconds": self.revocation_max_age_seconds,
            "offline": self.offline,
        }
