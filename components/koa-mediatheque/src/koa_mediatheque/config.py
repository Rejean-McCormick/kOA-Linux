"""Strict, secret-free configuration for kOA Mediatheque."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import os
from pathlib import Path, PurePosixPath
import re
import tomllib
from typing import Any, Mapping


class ConfigurationError(ValueError):
    """Raised when configuration is ambiguous, unsafe, or unsupported."""


class StoreMode(StrEnum):
    READ_WRITE = "read_write"
    READ_ONLY = "read_only"
    UNAVAILABLE = "unavailable"


class QueueMode(StrEnum):
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
_ENV_PREFIX = "KOA_MEDIATHEQUE_"
_ALLOWED_ENV = frozenset(
    {
        f"{_ENV_PREFIX}INSTANCE_ID",
        f"{_ENV_PREFIX}ENVIRONMENT",
        f"{_ENV_PREFIX}PROFILE",
        f"{_ENV_PREFIX}CONFIG_PATH",
        f"{_ENV_PREFIX}STATE_ROOT",
        f"{_ENV_PREFIX}RUNTIME_ROOT",
        f"{_ENV_PREFIX}SOCKET_PATH",
        f"{_ENV_PREFIX}DATABASE_PATH",
        f"{_ENV_PREFIX}CONTENT_ROOT",
        f"{_ENV_PREFIX}STAGING_ROOT",
        f"{_ENV_PREFIX}QUARANTINE_ROOT",
        f"{_ENV_PREFIX}RECEIPT_ROOT",
        f"{_ENV_PREFIX}DATABASE_MODE",
        f"{_ENV_PREFIX}CONTENT_MODE",
        f"{_ENV_PREFIX}INTEGRITY_QUEUE_MODE",
        f"{_ENV_PREFIX}RENDITION_QUEUE_MODE",
        f"{_ENV_PREFIX}PUBLICATION_QUEUE_MODE",
        f"{_ENV_PREFIX}RECEIPT_MODE",
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
    if ".." in path.parts or any(part in {"", "."} for part in path.parts[1:]):
        raise ConfigurationError(f"{field_name} must be normalized and cannot traverse")
    return Path(path)


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _enum(enum_type: type[StrEnum], value: Any, field_name: str) -> StrEnum:
    try:
        return enum_type(str(value).strip().lower())
    except ValueError as exc:
        allowed = ", ".join(item.value for item in enum_type)
        raise ConfigurationError(f"{field_name} must be one of: {allowed}") from exc


def _read_toml(path: Path) -> Mapping[str, Any]:
    if not path.is_absolute() or not path.is_file():
        raise ConfigurationError(f"configuration file does not exist: {path}")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"unable to read configuration: {exc}") from exc
    unknown_top = set(data) - {"koa_mediatheque"}
    if unknown_top:
        raise ConfigurationError(f"unknown top-level configuration keys: {sorted(unknown_top)}")
    section = data.get("koa_mediatheque", {})
    if not isinstance(section, dict):
        raise ConfigurationError("koa_mediatheque must be a TOML table")
    return section


@dataclass(frozen=True, slots=True)
class MediathequeConfig:
    """Validated infrastructure configuration; it contains no rights or policy decisions."""

    instance_id: str = "koa-mediatheque-1"
    environment: str = "development"
    profile: str = "developer_linux_workstation"
    config_path: Path | None = None
    state_root: Path = Path("/var/lib/koa/mediatheque")
    runtime_root: Path = Path("/run/koa/koa-mediatheque")
    socket_path: Path = Path("/run/koa/sockets/koa-mediatheque.sock")
    database_path: Path = Path("/var/lib/koa/mediatheque/catalog.sqlite3")
    content_root: Path = Path("/var/lib/koa/mediatheque/content")
    staging_root: Path = Path("/var/lib/koa/mediatheque/staging")
    quarantine_root: Path = Path("/var/lib/koa/mediatheque/quarantine")
    receipt_root: Path = Path("/var/lib/koa/mediatheque/receipts")
    database_mode: StoreMode = StoreMode.UNAVAILABLE
    content_mode: StoreMode = StoreMode.UNAVAILABLE
    integrity_queue_mode: QueueMode = QueueMode.UNAVAILABLE
    rendition_queue_mode: QueueMode = QueueMode.UNAVAILABLE
    publication_queue_mode: QueueMode = QueueMode.UNAVAILABLE
    receipt_mode: ReceiptMode = ReceiptMode.UNAVAILABLE

    def __post_init__(self) -> None:
        object.__setattr__(self, "instance_id", _identifier(self.instance_id, "instance_id"))
        object.__setattr__(self, "environment", _identifier(self.environment, "environment"))
        if self.profile not in _PROFILES:
            raise ConfigurationError(f"unsupported profile: {self.profile}")
        if self.config_path is not None:
            object.__setattr__(self, "config_path", _absolute_path(self.config_path, "config_path"))
        for field_name in (
            "state_root",
            "runtime_root",
            "socket_path",
            "database_path",
            "content_root",
            "staging_root",
            "quarantine_root",
            "receipt_root",
        ):
            object.__setattr__(self, field_name, _absolute_path(getattr(self, field_name), field_name))
        object.__setattr__(self, "database_mode", StoreMode(self.database_mode))
        object.__setattr__(self, "content_mode", StoreMode(self.content_mode))
        object.__setattr__(self, "integrity_queue_mode", QueueMode(self.integrity_queue_mode))
        object.__setattr__(self, "rendition_queue_mode", QueueMode(self.rendition_queue_mode))
        object.__setattr__(self, "publication_queue_mode", QueueMode(self.publication_queue_mode))
        object.__setattr__(self, "receipt_mode", ReceiptMode(self.receipt_mode))
        if _is_relative_to(self.state_root, self.runtime_root) or _is_relative_to(
            self.runtime_root, self.state_root
        ):
            raise ConfigurationError("state_root and runtime_root must not overlap")
        if not _is_relative_to(self.database_path, self.state_root):
            raise ConfigurationError("database_path must be inside state_root")
        owned_roots = (self.content_root, self.staging_root, self.quarantine_root, self.receipt_root)
        if any(not _is_relative_to(path, self.state_root) for path in owned_roots):
            raise ConfigurationError("content, staging, quarantine, and receipt roots must be inside state_root")
        for index, left in enumerate(owned_roots):
            for right in owned_roots[index + 1 :]:
                if _is_relative_to(left, right) or _is_relative_to(right, left):
                    raise ConfigurationError("component-owned storage roots must not overlap")
        if _is_relative_to(self.socket_path, self.state_root):
            raise ConfigurationError("socket_path cannot be inside authoritative state")

    @classmethod
    def from_sources(
        cls,
        *,
        config_path: str | Path | None = None,
        environ: Mapping[str, str] | None = None,
    ) -> MediathequeConfig:
        env = dict(os.environ if environ is None else environ)
        prefixed = {key: value for key, value in env.items() if key.startswith(_ENV_PREFIX)}
        unknown_env = set(prefixed) - _ALLOWED_ENV
        if unknown_env:
            raise ConfigurationError(f"unknown kOA Mediatheque environment keys: {sorted(unknown_env)}")
        if any(_SECRET_PATTERN.search(key.removeprefix(_ENV_PREFIX)) for key in prefixed):
            raise ConfigurationError("secrets are prohibited in kOA Mediatheque configuration")
        selected = config_path or prefixed.get(f"{_ENV_PREFIX}CONFIG_PATH")
        values: dict[str, Any] = {}
        selected_path: Path | None = None
        if selected is not None:
            selected_path = _absolute_path(selected, "config_path")
            values.update(_read_toml(selected_path))
        allowed_fields = {
            "instance_id",
            "environment",
            "profile",
            "state_root",
            "runtime_root",
            "socket_path",
            "database_path",
            "content_root",
            "staging_root",
            "quarantine_root",
            "receipt_root",
            "database_mode",
            "content_mode",
            "integrity_queue_mode",
            "rendition_queue_mode",
            "publication_queue_mode",
            "receipt_mode",
        }
        unknown_fields = set(values) - allowed_fields
        secret_fields = {field for field in values if _SECRET_PATTERN.search(field)}
        if unknown_fields or secret_fields:
            rejected = sorted(unknown_fields | secret_fields)
            raise ConfigurationError(f"unknown or prohibited configuration fields: {rejected}")
        env_map = {
            f"{_ENV_PREFIX}{field.upper()}": field
            for field in allowed_fields
        }
        for env_name, field_name in env_map.items():
            if env_name in prefixed:
                values[field_name] = prefixed[env_name]
        for field_name, enum_type in {
            "database_mode": StoreMode,
            "content_mode": StoreMode,
            "integrity_queue_mode": QueueMode,
            "rendition_queue_mode": QueueMode,
            "publication_queue_mode": QueueMode,
            "receipt_mode": ReceiptMode,
        }.items():
            if field_name in values:
                values[field_name] = _enum(enum_type, values[field_name], field_name)
        if selected_path is not None:
            values["config_path"] = selected_path
        return cls(**values)

    def with_overrides(self, **changes: object) -> MediathequeConfig:
        unknown = set(changes) - set(self.__dataclass_fields__)
        if unknown:
            raise ConfigurationError(f"unknown override fields: {sorted(unknown)}")
        return replace(self, **changes)

    def public_dict(self) -> dict[str, object]:
        return {
            "instance_id": self.instance_id,
            "environment": self.environment,
            "profile": self.profile,
            "state_root": self.state_root.as_posix(),
            "runtime_root": self.runtime_root.as_posix(),
            "socket_path": self.socket_path.as_posix(),
            "database_path": self.database_path.as_posix(),
            "content_root": self.content_root.as_posix(),
            "staging_root": self.staging_root.as_posix(),
            "quarantine_root": self.quarantine_root.as_posix(),
            "receipt_root": self.receipt_root.as_posix(),
            "database_mode": self.database_mode.value,
            "content_mode": self.content_mode.value,
            "integrity_queue_mode": self.integrity_queue_mode.value,
            "rendition_queue_mode": self.rendition_queue_mode.value,
            "publication_queue_mode": self.publication_queue_mode.value,
            "receipt_mode": self.receipt_mode.value,
        }
