"""Bounded thumbnail worker using verified payload references only."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Protocol
import re

_DIGEST = re.compile(r"^[0-9a-f]{64,128}$")

class ThumbnailWorkerError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message); self.code = code

@dataclass(frozen=True, slots=True)
class ThumbnailJob:
    job_id: str
    record_id: str
    version_id: str
    source_ref: str
    source_digest: str
    output_ref: str
    resource_admission_ref: str
    max_pixels: int = 4_000_000

@dataclass(frozen=True, slots=True)
class ThumbnailResult:
    job_id: str
    state: str
    output_ref: str
    media_type: str
    integrity: Mapping[str, str]
    resource_admission_ref: str

class ThumbnailProcessor(Protocol):
    def generate(self, *, source_ref: str, source_digest: str, output_ref: str, max_pixels: int) -> Mapping[str, str]:
        raise NotImplementedError("thumbnail processor port")

def run(job: ThumbnailJob, processor: ThumbnailProcessor) -> ThumbnailResult:
    if not all((job.job_id, job.record_id, job.version_id, job.source_ref, job.output_ref, job.resource_admission_ref)):
        raise ThumbnailWorkerError("invalid_job", "thumbnail job identifiers are required")
    if not _DIGEST.fullmatch(job.source_digest):
        raise ThumbnailWorkerError("invalid_source_digest", "source digest is invalid")
    if not 1 <= job.max_pixels <= 16_000_000:
        raise ThumbnailWorkerError("resource_limit_invalid", "thumbnail pixel limit is outside the bounded range")
    try:
        result = dict(processor.generate(source_ref=job.source_ref, source_digest=job.source_digest, output_ref=job.output_ref, max_pixels=job.max_pixels))
    except Exception as exc:
        raise ThumbnailWorkerError("processing_failed", "thumbnail generation failed closed") from exc
    if result.get("output_ref") != job.output_ref or result.get("media_type") not in {"image/png", "image/webp", "image/jpeg"}:
        raise ThumbnailWorkerError("processor_contract_violation", "thumbnail processor returned an invalid result")
    digest = result.get("digest", "")
    algorithm = result.get("algorithm", "sha256")
    if algorithm not in {"sha256", "sha384", "sha512"} or not _DIGEST.fullmatch(digest):
        raise ThumbnailWorkerError("processor_contract_violation", "thumbnail integrity result is invalid")
    return ThumbnailResult(job.job_id, "completed", job.output_ref, result["media_type"], {"algorithm": algorithm, "digest": digest}, job.resource_admission_ref)
