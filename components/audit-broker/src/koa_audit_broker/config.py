"""Strict, side-effect-free Audit Broker configuration loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import ClassVar, Mapping


class ConfigurationError(ValueError):
    """Raised when configuration would violate the Audit Broker contract."""


@dataclass(frozen=True, slots=True)
class AuditBrokerConfig:
    """Validated startup configuration.

    The object contains operational bounds and references only. It deliberately
    contains no credentials, policy decisions, evidence payloads, or source data.
    """

    COMPONENT_ID: ClassVar[str] = "audit_broker"
    CONTRACT_VERSION: ClassVar[str] = "1.0.0"
    INTERFACE_VERSION: ClassVar[str] = "1.0.0"
    ENV_PREFIX: ClassVar[str] = "KOA_AUDIT_BROKER_"

    component_id: str = COMPONENT_ID
    contract_version: str = CONTRACT_VERSION
    interface_version: str = INTERFACE_VERSION
    service_identity: str = COMPONENT_ID
    unix_socket_path: Path = Path("/run/koa/audit-broker/audit-broker.sock")
    state_directory: Path = Path("/var/lib/koa/audit-broker")
    runtime_directory: Path = Path("/run/koa/audit-broker")
    max_ingestion_queue_depth: int = 4096
    max_query_queue_depth: int = 256
    max_disclosure_queue_depth: int = 128
    storage_warning_percent: int = 80
    storage_read_only_percent: int = 95
    retention_policy_refs: tuple[str, ...] = ()
    last_recovery_point: str | None = None

    def __post_init__(self) -> None:
        errors: list[str] = []
        if self.component_id != self.COMPONENT_ID:
            errors.append(f"component_id must be {self.COMPONENT_ID!r}")
        if self.contract_version != self.CONTRACT_VERSION:
            errors.append(f"unsupported contract_version {self.contract_version!r}")
        if self.interface_version != self.INTERFACE_VERSION:
            errors.append(f"unsupported interface_version {self.interface_version!r}")
        if not self.service_identity.strip():
            errors.append("service_identity must be non-empty")
        if any(ch.isspace() for ch in self.service_identity):
            errors.append("service_identity must not contain whitespace")

        for field_name, value in (
            ("unix_socket_path", self.unix_socket_path),
            ("state_directory", self.state_directory),
            ("runtime_directory", self.runtime_directory),
        ):
            if not value.is_absolute():
                errors.append(f"{field_name} must be an absolute path")
            if ".." in value.parts:
                errors.append(f"{field_name} must not contain parent traversal")

        if self.unix_socket_path.parent != self.runtime_directory:
            errors.append("unix_socket_path must be located directly in runtime_directory")
        if self.state_directory == self.runtime_directory:
            errors.append("state_directory and runtime_directory must remain distinct")

        for field_name, value in (
            ("max_ingestion_queue_depth", self.max_ingestion_queue_depth),
            ("max_query_queue_depth", self.max_query_queue_depth),
            ("max_disclosure_queue_depth", self.max_disclosure_queue_depth),
        ):
            if value <= 0:
                errors.append(f"{field_name} must be greater than zero")
        if self.max_query_queue_depth > self.max_ingestion_queue_depth:
            errors.append("max_query_queue_depth must not exceed max_ingestion_queue_depth")
        if self.max_disclosure_queue_depth > self.max_query_queue_depth:
            errors.append("max_disclosure_queue_depth must not exceed max_query_queue_depth")

        if not 1 <= self.storage_warning_percent < self.storage_read_only_percent <= 100:
            errors.append(
                "storage thresholds must satisfy 1 <= warning < read_only <= 100"
            )

        normalized_refs = tuple(sorted(set(self.retention_policy_refs)))
        if normalized_refs != self.retention_policy_refs:
            errors.append("retention_policy_refs must be unique and sorted")
        if any(not ref or ref.startswith("/") or ".." in Path(ref).parts for ref in normalized_refs):
            errors.append("retention_policy_refs must be non-empty repository-relative references")
        if self.last_recovery_point is not None and not self.last_recovery_point.strip():
            errors.append("last_recovery_point must be omitted rather than empty")

        if errors:
            raise ConfigurationError("; ".join(errors))

    @classmethod
    def from_environment(cls, environment: Mapping[str, str] | None = None) -> AuditBrokerConfig:
        """Load a validated configuration from a supplied environment mapping."""

        env = MappingProxyType(dict(environment or {}))
        prefix = cls.ENV_PREFIX

        def value(name: str, default: str) -> str:
            return env.get(prefix + name, default).strip()

        def positive_int(name: str, default: int) -> int:
            raw = value(name, str(default))
            try:
                parsed = int(raw, 10)
            except ValueError as exc:
                raise ConfigurationError(f"{prefix}{name} must be an integer") from exc
            return parsed

        raw_refs = value("RETENTION_POLICY_REFS", "")
        refs = tuple(sorted({item.strip() for item in raw_refs.split(",") if item.strip()}))
        recovery_point = value("LAST_RECOVERY_POINT", "") or None

        return cls(
            component_id=value("COMPONENT_ID", cls.COMPONENT_ID),
            contract_version=value("CONTRACT_VERSION", cls.CONTRACT_VERSION),
            interface_version=value("INTERFACE_VERSION", cls.INTERFACE_VERSION),
            service_identity=value("SERVICE_IDENTITY", cls.COMPONENT_ID),
            unix_socket_path=Path(
                value("UNIX_SOCKET_PATH", "/run/koa/audit-broker/audit-broker.sock")
            ),
            state_directory=Path(
                value("STATE_DIRECTORY", "/var/lib/koa/audit-broker")
            ),
            runtime_directory=Path(value("RUNTIME_DIRECTORY", "/run/koa/audit-broker")),
            max_ingestion_queue_depth=positive_int("MAX_INGESTION_QUEUE_DEPTH", 4096),
            max_query_queue_depth=positive_int("MAX_QUERY_QUEUE_DEPTH", 256),
            max_disclosure_queue_depth=positive_int("MAX_DISCLOSURE_QUEUE_DEPTH", 128),
            storage_warning_percent=positive_int("STORAGE_WARNING_PERCENT", 80),
            storage_read_only_percent=positive_int("STORAGE_READ_ONLY_PERCENT", 95),
            retention_policy_refs=refs,
            last_recovery_point=recovery_point,
        )

    def as_public_dict(self) -> dict[str, object]:
        """Return the non-sensitive, deterministic configuration projection."""

        return {
            "component_id": self.component_id,
            "contract_version": self.contract_version,
            "interface_version": self.interface_version,
            "service_identity": self.service_identity,
            "unix_socket_path": str(self.unix_socket_path),
            "state_directory": str(self.state_directory),
            "runtime_directory": str(self.runtime_directory),
            "max_ingestion_queue_depth": self.max_ingestion_queue_depth,
            "max_query_queue_depth": self.max_query_queue_depth,
            "max_disclosure_queue_depth": self.max_disclosure_queue_depth,
            "storage_warning_percent": self.storage_warning_percent,
            "storage_read_only_percent": self.storage_read_only_percent,
            "retention_policy_refs": list(self.retention_policy_refs),
            "last_recovery_point": self.last_recovery_point,
        }
