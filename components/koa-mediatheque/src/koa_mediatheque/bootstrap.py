"""Fail-closed bootstrap for the kOA Mediatheque process surface."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import os
from pathlib import Path
from typing import Mapping

from .config import MediathequeConfig, QueueMode, ReceiptMode, StoreMode
from .health import Capability, CheckResult, CheckState, ComponentStatus, StoragePressure, evaluate_status


@dataclass(frozen=True, slots=True)
class RuntimeObservation:
    database_ready: CheckState = CheckState.UNKNOWN
    managed_content_root_ready: CheckState = CheckState.UNKNOWN
    integrity_queue_ready: CheckState = CheckState.UNKNOWN
    rendition_queue_ready: CheckState = CheckState.UNKNOWN
    publication_queue_ready: CheckState = CheckState.UNKNOWN
    backup_checkpoint_ready: CheckState = CheckState.UNKNOWN
    storage_pressure: StoragePressure = StoragePressure.UNKNOWN
    contracts_supported: CheckState = CheckState.PASS
    local_authority_loaded: CheckState = CheckState.UNKNOWN
    receipt_sink_ready: CheckState = CheckState.UNKNOWN
    resource_governor_ready: CheckState = CheckState.UNKNOWN
    publication_gateway_ready: CheckState = CheckState.UNKNOWN
    component_implementation_ready: bool = False
    restore_in_progress: bool = False
    record_count: int = 0
    version_count: int = 0
    queued_jobs: int = 0
    failed_jobs: int = 0
    bytes_managed: int = 0
    bytes_staged: int = 0
    publication_attempts: int = 0
    integrity_failures: int = 0

    def __post_init__(self) -> None:
        for field_name in (
            "database_ready",
            "managed_content_root_ready",
            "integrity_queue_ready",
            "rendition_queue_ready",
            "publication_queue_ready",
            "backup_checkpoint_ready",
            "contracts_supported",
            "local_authority_loaded",
            "receipt_sink_ready",
            "resource_governor_ready",
            "publication_gateway_ready",
        ):
            object.__setattr__(self, field_name, CheckState(getattr(self, field_name)))
        object.__setattr__(self, "storage_pressure", StoragePressure(self.storage_pressure))
        metric_names = (
            "record_count",
            "version_count",
            "queued_jobs",
            "failed_jobs",
            "bytes_managed",
            "bytes_staged",
            "publication_attempts",
            "integrity_failures",
        )
        if any(getattr(self, name) < 0 for name in metric_names):
            raise ValueError("runtime metrics cannot be negative")

    @classmethod
    def probe_local_paths(cls, config: MediathequeConfig) -> RuntimeObservation:
        return cls(
            database_ready=_file_check(config.database_path),
            managed_content_root_ready=_directory_check(config.content_root),
        )


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    config: MediathequeConfig
    status: ComponentStatus
    started_at: datetime
    process_id: int

    def to_dict(self, *, view: str = "operational") -> dict[str, object]:
        return {
            "config": self.config.public_dict(),
            "status": self.status.to_dict(view=view),
            "started_at": self.started_at.astimezone(UTC).isoformat().replace("+00:00", "Z"),
            "process_id": self.process_id,
        }


def _file_check(path: Path) -> CheckState:
    if not path.is_file():
        return CheckState.UNKNOWN
    return CheckState.PASS if os.access(path, os.R_OK) else CheckState.FAIL


def _directory_check(path: Path) -> CheckState:
    if not path.is_dir():
        return CheckState.UNKNOWN
    return CheckState.PASS if os.access(path, os.R_OK | os.X_OK) else CheckState.FAIL


def _check(check_id: str, state: CheckState, reason: str) -> CheckResult:
    state = CheckState(state)
    return CheckResult(check_id, state, None if state is CheckState.PASS else reason)


def _store_check(check_id: str, mode: StoreMode, observed: CheckState) -> CheckResult:
    if mode is StoreMode.UNAVAILABLE:
        return CheckResult(check_id, CheckState.FAIL, f"{check_id.upper()}_UNAVAILABLE")
    if mode is StoreMode.READ_ONLY:
        return CheckResult(check_id, CheckState.DEGRADED, f"{check_id.upper()}_READ_ONLY")
    return _check(check_id, observed, f"{check_id.upper()}_NOT_VERIFIED")


def _queue_check(check_id: str, mode: QueueMode, observed: CheckState) -> CheckResult:
    if mode is QueueMode.UNAVAILABLE:
        return CheckResult(check_id, CheckState.DEGRADED, f"{check_id.upper()}_UNAVAILABLE")
    if mode is QueueMode.VOLATILE:
        return CheckResult(check_id, CheckState.DEGRADED, f"{check_id.upper()}_NOT_DURABLE")
    return _check(check_id, observed, f"{check_id.upper()}_NOT_VERIFIED")


def _pressure_check(value: StoragePressure) -> CheckResult:
    if value is StoragePressure.NORMAL:
        return CheckResult("storage_pressure", CheckState.PASS)
    if value is StoragePressure.CRITICAL:
        return CheckResult("storage_pressure", CheckState.FAIL, "STORAGE_PRESSURE_CRITICAL")
    if value is StoragePressure.ELEVATED:
        return CheckResult("storage_pressure", CheckState.DEGRADED, "STORAGE_PRESSURE_ELEVATED")
    return CheckResult("storage_pressure", CheckState.UNKNOWN, "STORAGE_PRESSURE_UNKNOWN")


def bootstrap(
    config: MediathequeConfig,
    *,
    observation: RuntimeObservation | None = None,
    started_at: datetime | None = None,
) -> BootstrapResult:
    """Evaluate process state without creating storage or activating authoritative records."""
    observed = observation or RuntimeObservation.probe_local_paths(config)
    start = started_at or datetime.now(UTC)
    if start.tzinfo is None:
        raise ValueError("started_at must be timezone-aware")

    health_dimensions: Mapping[str, CheckResult] = {
        "database": _store_check("database", config.database_mode, observed.database_ready),
        "managed_content_root": _store_check(
            "managed_content_root", config.content_mode, observed.managed_content_root_ready
        ),
        "integrity_queue": _queue_check(
            "integrity_queue", config.integrity_queue_mode, observed.integrity_queue_ready
        ),
        "rendition_queue": _queue_check(
            "rendition_queue", config.rendition_queue_mode, observed.rendition_queue_ready
        ),
        "publication_queue": _queue_check(
            "publication_queue", config.publication_queue_mode, observed.publication_queue_ready
        ),
        "backup_checkpoint": _check(
            "backup_checkpoint", observed.backup_checkpoint_ready, "BACKUP_CHECKPOINT_NOT_VERIFIED"
        ),
        "storage_pressure": _pressure_check(observed.storage_pressure),
    }
    receipt_state = (
        CheckState.PASS
        if config.receipt_mode is ReceiptMode.DURABLE and observed.receipt_sink_ready is CheckState.PASS
        else CheckState.DEGRADED
        if config.receipt_mode is ReceiptMode.BUFFERED
        else CheckState.FAIL
    )
    readiness_checks: Mapping[str, CheckResult] = {
        "contracts_supported": _check(
            "contracts_supported", observed.contracts_supported, "CONTRACT_VERSION_UNSUPPORTED"
        ),
        "local_authority_loaded": _check(
            "local_authority_loaded", observed.local_authority_loaded, "LOCAL_AUTHORITY_NOT_LOADED"
        ),
        "receipt_sink_ready": _check(
            "receipt_sink_ready", receipt_state, "DURABLE_RECEIPT_PATH_UNAVAILABLE"
        ),
        "component_implementation_ready": CheckResult(
            "component_implementation_ready",
            CheckState.PASS if observed.component_implementation_ready else CheckState.FAIL,
            None if observed.component_implementation_ready else "IMPLEMENTATION_LAYERS_NOT_AVAILABLE",
        ),
    }

    available: set[Capability] = set()
    degraded: set[Capability] = set()
    blocked: set[Capability] = set()
    contracts_ready = observed.contracts_supported is CheckState.PASS
    database_readable = config.database_mode is not StoreMode.UNAVAILABLE and observed.database_ready is CheckState.PASS
    content_readable = config.content_mode is not StoreMode.UNAVAILABLE and observed.managed_content_root_ready is CheckState.PASS
    database_writable = config.database_mode is StoreMode.READ_WRITE and database_readable
    content_writable = config.content_mode is StoreMode.READ_WRITE and content_readable
    implementation_ready = observed.component_implementation_ready
    receipts_durable = receipt_state is CheckState.PASS

    if contracts_ready and database_readable and observed.local_authority_loaded is CheckState.PASS:
        available.add(Capability.LOCAL_CATALOG_QUERY)
    else:
        blocked.add(Capability.LOCAL_CATALOG_QUERY)
    if content_readable and contracts_ready:
        if config.content_mode is StoreMode.READ_ONLY:
            degraded.add(Capability.LOCAL_CONTENT_ACCESS)
        else:
            available.add(Capability.LOCAL_CONTENT_ACCESS)
    else:
        blocked.add(Capability.LOCAL_CONTENT_ACCESS)

    mutation_ready = implementation_ready and database_writable and content_writable and receipts_durable
    for capability in (
        Capability.MEDIA_RECORD_COMMAND,
        Capability.MEDIA_IMPORT_STAGING,
        Capability.MEDIA_IMPORT_ACCEPTANCE,
        Capability.PUBLICATION_RESULT_ATTACHMENT,
        Capability.RESTORE_VERIFICATION,
    ):
        (available if mutation_ready else blocked).add(capability)

    rendition_ready = (
        mutation_ready
        and config.rendition_queue_mode is QueueMode.DURABLE
        and observed.rendition_queue_ready is CheckState.PASS
        and observed.resource_governor_ready is CheckState.PASS
        and observed.storage_pressure is not StoragePressure.CRITICAL
    )
    (available if rendition_ready else blocked).add(Capability.RENDITION_SCHEDULING)

    publication_ready = (
        mutation_ready
        and observed.publication_gateway_ready is CheckState.PASS
        and config.publication_queue_mode is not QueueMode.UNAVAILABLE
    )
    if publication_ready and config.publication_queue_mode is QueueMode.DURABLE:
        available.add(Capability.PUBLICATION_CANDIDATE)
    elif mutation_ready and observed.publication_gateway_ready is CheckState.PASS:
        degraded.add(Capability.PUBLICATION_CANDIDATE)
    else:
        blocked.add(Capability.PUBLICATION_CANDIDATE)

    backup_ready = database_readable and content_readable and observed.backup_checkpoint_ready is CheckState.PASS
    (available if backup_ready else blocked).add(Capability.BACKUP_EXPORT)

    metrics = {
        "record_count": observed.record_count,
        "version_count": observed.version_count,
        "queued_jobs": observed.queued_jobs,
        "failed_jobs": observed.failed_jobs,
        "bytes_managed": observed.bytes_managed,
        "bytes_staged": observed.bytes_staged,
        "publication_attempts": observed.publication_attempts,
        "integrity_failures": observed.integrity_failures,
    }
    status = evaluate_status(
        health_dimensions=health_dimensions,
        readiness_checks=readiness_checks,
        available=available,
        degraded=degraded,
        blocked=blocked,
        metrics=metrics,
    )
    return BootstrapResult(config=config, status=status, started_at=start, process_id=os.getpid())
