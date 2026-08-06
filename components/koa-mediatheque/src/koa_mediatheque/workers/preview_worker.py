"""Bounded preview worker using verified payload references only."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Protocol
import re

_DIGEST = re.compile(r"^[0-9a-f]{64,128}$")

class PreviewWorkerError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message); self.code = code

@dataclass(frozen=True, slots=True)
class PreviewJob:
    job_id: str
    record_id: str
    version_id: str
    source_ref: str
    source_digest: str
    output_ref: str
    resource_admission_ref: str
    max_duration_seconds: int = 30
    max_size_bytes: int = 20_000_000

@dataclass(frozen=True, slots=True)
class PreviewResult:
    job_id: str
    state: str
    output_ref: str
    media_type: str
    integrity: Mapping[str, str]
    resource_admission_ref: str

class PreviewProcessor(Protocol):
    def generate(self, *, source_ref: str, source_digest: str, output_ref: str, max_duration_seconds: int, max_size_bytes: int) -> Mapping[str, str]:
        raise NotImplementedError("preview processor port")

def run(job: PreviewJob, processor: PreviewProcessor) -> PreviewResult:
    if not all((job.job_id, job.record_id, job.version_id, job.source_ref, job.output_ref, job.resource_admission_ref)):
        raise PreviewWorkerError("invalid_job", "preview job identifiers are required")
    if not _DIGEST.fullmatch(job.source_digest):
        raise PreviewWorkerError("invalid_source_digest", "source digest is invalid")
    if not 1 <= job.max_duration_seconds <= 300 or not 1 <= job.max_size_bytes <= 100_000_000:
        raise PreviewWorkerError("resource_limit_invalid", "preview limits are outside the bounded range")
    try:
        result = dict(processor.generate(source_ref=job.source_ref, source_digest=job.source_digest, output_ref=job.output_ref, max_duration_seconds=job.max_duration_seconds, max_size_bytes=job.max_size_bytes))
    except Exception as exc:
        raise PreviewWorkerError("processing_failed", "preview generation failed closed") from exc
    if result.get("output_ref") != job.output_ref or not str(result.get("media_type", "")).strip():
        raise PreviewWorkerError("processor_contract_violation", "preview processor returned an invalid result")
    digest = result.get("digest", ""); algorithm = result.get("algorithm", "sha256")
    if algorithm not in {"sha256", "sha384", "sha512"} or not _DIGEST.fullmatch(digest):
        raise PreviewWorkerError("processor_contract_violation", "preview integrity result is invalid")
    return PreviewResult(job.job_id, "completed", job.output_ref, result["media_type"], {"algorithm": algorithm, "digest": digest}, job.resource_admission_ref)
