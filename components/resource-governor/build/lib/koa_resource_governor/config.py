"""Strict, secret-free configuration for Resource Governor."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import os
from pathlib import Path, PurePosixPath
import re
import tomllib
from typing import Any, Mapping


class ConfigurationError(ValueError):
    """Raised when configuration is missing, ambiguous, or unsafe."""


class EnforcementAdapterMode(StrEnum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"


class ObservationSourceMode(StrEnum):
    AVAILABLE = "available"
    STALE = "stale"
    UNAVAILABLE = "unavailable"


class QueueBackendMode(StrEnum):
    DURABLE = "durable"
    VOLATILE = "volatile"
    UNAVAILABLE = "unavailable"


class ReceiptMode(StrEnum):
    DURABLE = "durable"
    BUFFERED = "buffered"
    UNAVAILABLE = "unavailable"


_PROFILES = frozenset(
    {
        "user_lightweight",
        "developer_linux_workstation",
        "developer_windows_wsl",
        "sovereign_linux_node",
        "sovereign_hub",
        "build_farm",
        "control_plane",
        "high_assurance",
        "sovereign_offline",
        "appliance_shell",
    }
)
_ENV_PREFIX = "KOA_RESOURCE_GOVERNOR_"
_ALLOWED_ENV = frozenset(
    {
        f"{_ENV_PREFIX}INSTANCE_ID",
        f"{_ENV_PREFIX}ENVIRONMENT",
        f"{_ENV_PREFIX}PROFILE",
        f"{_ENV_PREFIX}CONFIG_PATH",
        f"{_ENV_PREFIX}STATE_ROOT",
        f"{_ENV_PREFIX}RUNTIME_ROOT",
        f"{_ENV_PREFIX}SOCKET_PATH",
        f"{_ENV_PREFIX}ENFORCEMENT_ADAPTER_MODE",
        f"{_ENV_PREFIX}OBSERVATION_SOURCE_MODE",
        f"{_ENV_PREFIX}QUEUE_BACKEND_MODE",
        f"{_ENV_PREFIX}RECEIPT_MODE",
        f"{_ENV_PREFIX}RECEIPT_BUFFER_LIMIT",
        f"{_ENV_PREFIX}QUEUE_CAPACITY",
        f"{_ENV_PREFIX}OBSERVATION_MAX_AGE_SECONDS",
        f"{_ENV_PREFIX}ALLOW_LOW_RISK_WITHOUT_OBSERVATION",
        f"{_ENV_PREFIX}RECONCILIATION_REQUIRED",
    }
)
_SECRET_PATTERN = re.compile(
    r"(?:^|_)(?:password|passphrase|private_key|secret|token|credential|key_material)(?:$|_)",
    re.IGNORECASE,
)
_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:@/+\-]{0,255}$")


def _identifier(value: str, field_name: str) -> str:
    normalized = value.strip()
    if not _IDENTIFIER_PATTERN.fullmatch(normalized):
        raise ConfigurationError(f"{field_name} is not a valid bounded identifier")
    return normalized


def _absolute_path(value: str | Path, field_name: str) -> Path:
    raw = str(value).strip()
    if not raw:
        raise ConfigurationError(f"{field_name} cannot be empty")
    path = PurePosixPath(raw)
    if not path.is_absolute():
        raise ConfigurationError(f"{field_name} must be an absolute POSIX path")
    if ".." in path.parts:
        raise ConfigurationError(f"{field_name} cannot contain path traversal")
    if any(part in {"", "."} for part in path.parts[1:]):
        raise ConfigurationError(f"{field_name} must be normalized")
    return Path(path)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _boolean(value: Any, field_name: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True
        if normalized in {"0", "false", "no", "off"}:
            return False
    raise ConfigurationError(f"{field_name} must be a boolean")


def _positive_int(value: Any, field_name: str, *, maximum: int) -> int:
    if isinstance(value, bool):
        raise ConfigurationError(f"{field_name} must be an integer")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{field_name} must be an integer") from exc
    if parsed <= 0 or parsed > maximum:
        raise ConfigurationError(f"{field_name} must be between 1 and {maximum}")
    return parsed


def _nonnegative_int(value: Any, field_name: str, *, maximum: int) -> int:
    if isinstance(value, bool):
        raise ConfigurationError(f"{field_name} must be an integer")
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{field_name} must be an integer") from exc
    if parsed < 0 or parsed > maximum:
        raise ConfigurationError(f"{field_name} must be between 0 and {maximum}")
    return parsed


def _enum(enum_type: type[StrEnum], value: Any, field_name: str) -> StrEnum:
    try:
        return enum_type(str(value).strip().lower())
    except ValueError as exc:
        allowed = ", ".join(item.value for item in enum_type)
        raise ConfigurationError(f"{field_name} must be one of: {allowed}") from exc


def _read_toml(path: Path) -> Mapping[str, Any]:
    if not path.is_absolute():
        raise ConfigurationError("configuration path must be absolute")
    if not path.exists() or not path.is_file():
        raise ConfigurationError(f"configuration file does not exist: {path}")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"unable to read configuration: {exc}") from exc
    allowed_top = {"resource_governor"}
    unknown_top = set(data) - allowed_top
    if unknown_top:
        raise ConfigurationError(f"unknown top-level configuration keys: {sorted(unknown_top)}")
    section = data.get("resource_governor", {})
    if not isinstance(section, dict):
        raise ConfigurationError("resource_governor must be a TOML table")
    return section


@dataclass(frozen=True, slots=True)
class ResourceGovernorConfig:
    """Validated configuration that does not contain resource grants or secrets."""

    instance_id: str = "resource-governor-1"
    environment: str = "development"
    profile: str = "developer_linux_workstation"
    config_path: Path | None = None
    state_root: Path = Path("/var/lib/koa/resource-governor")
    runtime_root: Path = Path("/run/koa/resource-governor")
    socket_path: Path = Path("/run/koa/sockets/resource-governor.sock")
    enforcement_adapter_mode: EnforcementAdapterMode = EnforcementAdapterMode.UNAVAILABLE
    observation_source_mode: ObservationSourceMode = ObservationSourceMode.UNAVAILABLE
    queue_backend_mode: QueueBackendMode = QueueBackendMode.UNAVAILABLE
    receipt_mode: ReceiptMode = ReceiptMode.UNAVAILABLE
    receipt_buffer_limit: int = 256
    queue_capacity: int = 1024
    observation_max_age_seconds: int = 60
    allow_low_risk_without_observation: bool = False
    reconciliation_required: bool = True

    def __post_init__(self) -> None:
        object.__setattr__(self, "instance_id", _identifier(self.instance_id, "instance_id"))
        object.__setattr__(self, "environment", _identifier(self.environment, "environment"))
        if self.profile not in _PROFILES:
            raise ConfigurationError(f"profile is not canonical: {self.profile}")
        for field_name in ("state_root", "runtime_root", "socket_path"):
            object.__setattr__(self, field_name, _absolute_path(getattr(self, field_name), field_name))
        if self.config_path is not None:
            object.__setattr__(self, "config_path", _absolute_path(self.config_path, "config_path"))
        object.__setattr__(
            self,
            "enforcement_adapter_mode",
            EnforcementAdapterMode(self.enforcement_adapter_mode),
        )
        object.__setattr__(
            self,
            "observation_source_mode",
            ObservationSourceMode(self.observation_source_mode),
        )
        object.__setattr__(self, "queue_backend_mode", QueueBackendMode(self.queue_backend_mode))
        object.__setattr__(self, "receipt_mode", ReceiptMode(self.receipt_mode))
        object.__setattr__(
            self,
            "receipt_buffer_limit",
            _nonnegative_int(self.receipt_buffer_limit, "receipt_buffer_limit", maximum=1_000_000),
        )
        object.__setattr__(
            self,
            "queue_capacity",
            _positive_int(self.queue_capacity, "queue_capacity", maximum=10_000_000),
        )
        object.__setattr__(
            self,
            "observation_max_age_seconds",
            _positive_int(
                self.observation_max_age_seconds,
                "observation_max_age_seconds",
                maximum=86_400,
            ),
        )
        if self.state_root == self.runtime_root:
            raise ConfigurationError("state_root and runtime_root must be distinct")
        if _is_relative_to(self.state_root, self.runtime_root) or _is_relative_to(
            self.runtime_root, self.state_root
        ):
            raise ConfigurationError("state_root and runtime_root cannot contain one another")
        if _is_relative_to(self.socket_path, self.state_root):
            raise ConfigurationError("socket_path cannot be stored under persistent state_root")
        if self.receipt_mode is ReceiptMode.BUFFERED and self.receipt_buffer_limit == 0:
            raise ConfigurationError("buffered receipt mode requires a positive receipt_buffer_limit")
        if self.receipt_mode is ReceiptMode.UNAVAILABLE and self.receipt_buffer_limit != 0:
            object.__setattr__(self, "receipt_buffer_limit", 0)
        if self.queue_backend_mode is QueueBackendMode.UNAVAILABLE and self.queue_capacity <= 0:
            raise ConfigurationError("queue_capacity must remain finite even when queueing is unavailable")

    @classmethod
    def load(
        cls,
        *,
        path: Path | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> ResourceGovernorConfig:
        env = dict(os.environ if environ is None else environ)
        unknown = sorted(key for key in env if key.startswith(_ENV_PREFIX) and key not in _ALLOWED_ENV)
        if unknown:
            raise ConfigurationError(f"unknown Resource Governor environment variables: {unknown}")
        secret_like = sorted(key for key in env if key.startswith(_ENV_PREFIX) and _SECRET_PATTERN.search(key))
        if secret_like:
            raise ConfigurationError(f"secret-bearing configuration keys are prohibited: {secret_like}")

        selected_path = path
        env_path = env.get(f"{_ENV_PREFIX}CONFIG_PATH")
        if selected_path is None and env_path:
            selected_path = _absolute_path(env_path, "config_path")
        elif selected_path is not None:
            selected_path = _absolute_path(selected_path, "config_path")

        values: dict[str, Any] = {}
        if selected_path is not None:
            values.update(_read_toml(selected_path))
            values["config_path"] = selected_path

        env_map = {
            f"{_ENV_PREFIX}INSTANCE_ID": "instance_id",
            f"{_ENV_PREFIX}ENVIRONMENT": "environment",
            f"{_ENV_PREFIX}PROFILE": "profile",
            f"{_ENV_PREFIX}STATE_ROOT": "state_root",
            f"{_ENV_PREFIX}RUNTIME_ROOT": "runtime_root",
            f"{_ENV_PREFIX}SOCKET_PATH": "socket_path",
            f"{_ENV_PREFIX}ENFORCEMENT_ADAPTER_MODE": "enforcement_adapter_mode",
            f"{_ENV_PREFIX}OBSERVATION_SOURCE_MODE": "observation_source_mode",
            f"{_ENV_PREFIX}QUEUE_BACKEND_MODE": "queue_backend_mode",
            f"{_ENV_PREFIX}RECEIPT_MODE": "receipt_mode",
            f"{_ENV_PREFIX}RECEIPT_BUFFER_LIMIT": "receipt_buffer_limit",
            f"{_ENV_PREFIX}QUEUE_CAPACITY": "queue_capacity",
            f"{_ENV_PREFIX}OBSERVATION_MAX_AGE_SECONDS": "observation_max_age_seconds",
            f"{_ENV_PREFIX}ALLOW_LOW_RISK_WITHOUT_OBSERVATION": "allow_low_risk_without_observation",
            f"{_ENV_PREFIX}RECONCILIATION_REQUIRED": "reconciliation_required",
        }
        for env_key, field_name in env_map.items():
            if env_key in env:
                values[field_name] = env[env_key]

        allowed_fields = {
            "instance_id",
            "environment",
            "profile",
            "config_path",
            "state_root",
            "runtime_root",
            "socket_path",
            "enforcement_adapter_mode",
            "observation_source_mode",
            "queue_backend_mode",
            "receipt_mode",
            "receipt_buffer_limit",
            "queue_capacity",
            "observation_max_age_seconds",
            "allow_low_risk_without_observation",
            "reconciliation_required",
        }
        unknown_values = sorted(set(values) - allowed_fields)
        if unknown_values:
            raise ConfigurationError(f"unknown resource_governor keys: {unknown_values}")

        if "enforcement_adapter_mode" in values:
            values["enforcement_adapter_mode"] = _enum(
                EnforcementAdapterMode, values["enforcement_adapter_mode"], "enforcement_adapter_mode"
            )
        if "observation_source_mode" in values:
            values["observation_source_mode"] = _enum(
                ObservationSourceMode, values["observation_source_mode"], "observation_source_mode"
            )
        if "queue_backend_mode" in values:
            values["queue_backend_mode"] = _enum(
                QueueBackendMode, values["queue_backend_mode"], "queue_backend_mode"
            )
        if "receipt_mode" in values:
            values["receipt_mode"] = _enum(ReceiptMode, values["receipt_mode"], "receipt_mode")
        for field_name, maximum in (
            ("receipt_buffer_limit", 1_000_000),
            ("queue_capacity", 10_000_000),
            ("observation_max_age_seconds", 86_400),
        ):
            if field_name in values:
                parser = _nonnegative_int if field_name == "receipt_buffer_limit" else _positive_int
                values[field_name] = parser(values[field_name], field_name, maximum=maximum)
        for field_name in ("allow_low_risk_without_observation", "reconciliation_required"):
            if field_name in values:
                values[field_name] = _boolean(values[field_name], field_name)
        return cls(**values)

    def with_config_path(self, path: Path | None) -> ResourceGovernorConfig:
        return replace(self, config_path=path)

    def public_dict(self) -> dict[str, object]:
        """Return a stable, non-secret configuration view."""
        return {
            "instance_id": self.instance_id,
            "environment": self.environment,
            "profile": self.profile,
            "config_path": str(self.config_path) if self.config_path else None,
            "state_root": str(self.state_root),
            "runtime_root": str(self.runtime_root),
            "socket_path": str(self.socket_path),
            "enforcement_adapter_mode": self.enforcement_adapter_mode.value,
            "observation_source_mode": self.observation_source_mode.value,
            "queue_backend_mode": self.queue_backend_mode.value,
            "receipt_mode": self.receipt_mode.value,
            "receipt_buffer_limit": self.receipt_buffer_limit,
            "queue_capacity": self.queue_capacity,
            "observation_max_age_seconds": self.observation_max_age_seconds,
            "allow_low_risk_without_observation": self.allow_low_risk_without_observation,
            "reconciliation_required": self.reconciliation_required,
            "resource_limits_configured_here": False,
            "business_authorization_owned": False,
        }
