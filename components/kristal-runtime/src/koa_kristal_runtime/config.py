"""Strict, side-effect-free Kristal Runtime configuration."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import ClassVar, Mapping
import re


class ConfigurationError(ValueError):
    """Raised when startup configuration violates the component contract."""


class ActivationMode(StrEnum):
    ALWAYS_AVAILABLE = "always_available"
    EMBEDDED = "embedded_behind_registered_interface"
    SOCKET_ACTIVATED = "socket_activated"
    TASK_ACTIVATED = "task_activated"


class EvidencePolicy(StrEnum):
    BOUNDED_QUEUE = "bounded_queue"
    SYNCHRONOUS_REQUIRED = "synchronous_required"


_REFERENCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,254}$")
_SEMVER = re.compile(r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:[-+][0-9A-Za-z.-]+)?$")


@dataclass(frozen=True, slots=True)
class KristalRuntimeConfig:
    """Validated references and implementation settings for startup.

    No field carries artifact content, raw credentials, signatures, policy
    decisions, resource grants, or any other external authority.
    """

    COMPONENT_ID: ClassVar[str] = "kristal_runtime"
    CONTRACT_VERSION: ClassVar[str] = "1.0.0"
    INTERFACE_VERSION: ClassVar[str] = "1.0.0"
    RUNTIME_VERSION: ClassVar[str] = "0.1.0"
    RELEASE_CHANNEL: ClassVar[str] = "knowledge"
    ENV_PREFIX: ClassVar[str] = "KOA_KRISTAL_RUNTIME_"
    SUPPORTED_ENV_KEYS: ClassVar[frozenset[str]] = frozenset(
        {
            "ACTIVATION_MODE",
            "AUDIT_EVIDENCE_POLICY",
            "COMPONENT_ID",
            "CONTRACT_VERSION",
            "INTERFACE_VERSION",
            "OFFLINE_OPERATION",
            "PROFILE_REF",
            "QUARANTINE_DIRECTORY",
            "RECEIPT_DIRECTORY",
            "RELEASE_CHANNEL",
            "RUNTIME_DIRECTORY",
            "RUNTIME_PACK_DIRECTORY",
            "RUNTIME_VERSION",
            "SERVICE_IDENTITY",
            "STATE_DIRECTORY",
            "TRUST_VALIDATION_REQUIRED",
            "UNIX_SOCKET_PATH",
        }
    )

    component_id: str = COMPONENT_ID
    contract_version: str = CONTRACT_VERSION
    interface_version: str = INTERFACE_VERSION
    runtime_version: str = RUNTIME_VERSION
    release_channel: str = RELEASE_CHANNEL
    service_identity: str = COMPONENT_ID
    profile_ref: str = "profile:active"
    activation_mode: ActivationMode = ActivationMode.SOCKET_ACTIVATED
    audit_evidence_policy: EvidencePolicy = EvidencePolicy.SYNCHRONOUS_REQUIRED
    trust_validation_required: bool = True
    offline_operation: bool = False
    unix_socket_path: Path = Path("/run/koa/sockets/kristal-runtime.sock")
    state_directory: Path = Path("/var/lib/koa/kristal")
    runtime_directory: Path = Path("/run/koa/kristal-runtime")
    runtime_pack_directory: Path = Path("/var/lib/koa/kristal/runtime-packs")
    receipt_directory: Path = Path("/var/lib/koa/kristal/receipts")
    quarantine_directory: Path = Path("/var/lib/koa/quarantine/kristal")

    def __post_init__(self) -> None:
        errors: list[str] = []
        if self.component_id != self.COMPONENT_ID:
            errors.append(f"component_id must be {self.COMPONENT_ID!r}")
        if self.contract_version != self.CONTRACT_VERSION:
            errors.append(f"unsupported contract_version {self.contract_version!r}")
        if self.interface_version != self.INTERFACE_VERSION:
            errors.append(f"unsupported interface_version {self.interface_version!r}")
        if not _SEMVER.fullmatch(self.runtime_version):
            errors.append("runtime_version must be semantic")
        if self.release_channel != self.RELEASE_CHANNEL:
            errors.append("release_channel must be 'knowledge'")
        for name in ("service_identity", "profile_ref"):
            value = getattr(self, name)
            if not _REFERENCE.fullmatch(value):
                errors.append(f"{name} must be a bounded reference")
        paths = {
            "unix_socket_path": self.unix_socket_path,
            "state_directory": self.state_directory,
            "runtime_directory": self.runtime_directory,
            "runtime_pack_directory": self.runtime_pack_directory,
            "receipt_directory": self.receipt_directory,
            "quarantine_directory": self.quarantine_directory,
        }
        for name, value in paths.items():
            if not value.is_absolute():
                errors.append(f"{name} must be absolute")
            if ".." in value.parts:
                errors.append(f"{name} must not traverse parent directories")
        if self.unix_socket_path.suffix != ".sock":
            errors.append("unix_socket_path must end in .sock")
        if not _is_within(self.runtime_pack_directory, self.state_directory):
            errors.append("runtime_pack_directory must be below state_directory")
        if not _is_within(self.receipt_directory, self.state_directory):
            errors.append("receipt_directory must be below state_directory")
        if self.quarantine_directory == self.runtime_pack_directory:
            errors.append("quarantine_directory must be separate from runtime packs")
        if errors:
            raise ConfigurationError("; ".join(errors))

    @classmethod
    def from_environment(cls, environment: Mapping[str, str] | None = None) -> "KristalRuntimeConfig":
        env = dict(environment or {})
        prefixed = {key: value for key, value in env.items() if key.startswith(cls.ENV_PREFIX)}
        unknown = sorted(key.removeprefix(cls.ENV_PREFIX) for key in prefixed if key.removeprefix(cls.ENV_PREFIX) not in cls.SUPPORTED_ENV_KEYS)
        if unknown:
            raise ConfigurationError("unknown configuration keys: " + ", ".join(unknown))
        value = lambda key, default: prefixed.get(cls.ENV_PREFIX + key, default)
        try:
            return cls(
                component_id=value("COMPONENT_ID", cls.COMPONENT_ID),
                contract_version=value("CONTRACT_VERSION", cls.CONTRACT_VERSION),
                interface_version=value("INTERFACE_VERSION", cls.INTERFACE_VERSION),
                runtime_version=value("RUNTIME_VERSION", cls.RUNTIME_VERSION),
                release_channel=value("RELEASE_CHANNEL", cls.RELEASE_CHANNEL),
                service_identity=value("SERVICE_IDENTITY", cls.COMPONENT_ID),
                profile_ref=value("PROFILE_REF", "profile:active"),
                activation_mode=ActivationMode(value("ACTIVATION_MODE", ActivationMode.SOCKET_ACTIVATED.value)),
                audit_evidence_policy=EvidencePolicy(value("AUDIT_EVIDENCE_POLICY", EvidencePolicy.SYNCHRONOUS_REQUIRED.value)),
                trust_validation_required=_boolean(value("TRUST_VALIDATION_REQUIRED", "true"), "TRUST_VALIDATION_REQUIRED"),
                offline_operation=_boolean(value("OFFLINE_OPERATION", "false"), "OFFLINE_OPERATION"),
                unix_socket_path=Path(value("UNIX_SOCKET_PATH", "/run/koa/sockets/kristal-runtime.sock")),
                state_directory=Path(value("STATE_DIRECTORY", "/var/lib/koa/kristal")),
                runtime_directory=Path(value("RUNTIME_DIRECTORY", "/run/koa/kristal-runtime")),
                runtime_pack_directory=Path(value("RUNTIME_PACK_DIRECTORY", "/var/lib/koa/kristal/runtime-packs")),
                receipt_directory=Path(value("RECEIPT_DIRECTORY", "/var/lib/koa/kristal/receipts")),
                quarantine_directory=Path(value("QUARANTINE_DIRECTORY", "/var/lib/koa/quarantine/kristal")),
            )
        except ValueError as exc:
            raise ConfigurationError(str(exc)) from exc

    def as_public_dict(self) -> dict[str, object]:
        return {
            "activation_mode": self.activation_mode.value,
            "audit_evidence_policy": self.audit_evidence_policy.value,
            "component_id": self.component_id,
            "contract_version": self.contract_version,
            "interface_version": self.interface_version,
            "offline_operation": self.offline_operation,
            "profile_ref": self.profile_ref,
            "quarantine_directory": str(self.quarantine_directory),
            "receipt_directory": str(self.receipt_directory),
            "release_channel": self.release_channel,
            "runtime_directory": str(self.runtime_directory),
            "runtime_pack_directory": str(self.runtime_pack_directory),
            "runtime_version": self.runtime_version,
            "service_identity": self.service_identity,
            "state_directory": str(self.state_directory),
            "trust_validation_required": self.trust_validation_required,
            "unix_socket_path": str(self.unix_socket_path),
        }


def _boolean(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ConfigurationError(f"{name} must be true or false")


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return child != parent
    except ValueError:
        return False
