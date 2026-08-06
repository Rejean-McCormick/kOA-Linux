"""Bounded deterministic text-extraction worker."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Protocol
import re

_DIGEST = re.compile(r"^[0-9a-f]{64,128}$")

class TextExtractionWorkerError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message); self.code = code

@dataclass(frozen=True, slots=True)
class TextExtractionJob:
    job_id: str
    record_id: str
    version_id: str
    source_ref: str
    source_digest: str
    output_ref: str
    resource_admission_ref: str
    max_characters: int = 200_000

@dataclass(frozen=True, slots=True)
class TextExtractionResult:
    job_id: str
    state: str
    output_ref: str
    media_type: str
    character_count: int
    integrity: Mapping[str, str]
    resource_admission_ref: str

class TextExtractor(Protocol):
    def extract(self, *, source_ref: str, source_digest: str, output_ref: str, max_characters: int) -> Mapping[str, object]:
        raise NotImplementedError("text extractor port")

def run(job: TextExtractionJob, extractor: TextExtractor) -> TextExtractionResult:
    if not all((job.job_id, job.record_id, job.version_id, job.source_ref, job.output_ref, job.resource_admission_ref)):
        raise TextExtractionWorkerError("invalid_job", "text extraction job identifiers are required")
    if not _DIGEST.fullmatch(job.source_digest):
        raise TextExtractionWorkerError("invalid_source_digest", "source digest is invalid")
    if not 1 <= job.max_characters <= 2_000_000:
        raise TextExtractionWorkerError("resource_limit_invalid", "text extraction limit is outside the bounded range")
    try:
        result = dict(extractor.extract(source_ref=job.source_ref, source_digest=job.source_digest, output_ref=job.output_ref, max_characters=job.max_characters))
    except Exception as exc:
        raise TextExtractionWorkerError("processing_failed", "text extraction failed closed") from exc
    count = result.get("character_count")
    digest = str(result.get("digest", "")); algorithm = str(result.get("algorithm", "sha256"))
    if result.get("output_ref") != job.output_ref or result.get("media_type") != "text/plain" or not isinstance(count, int) or not 0 <= count <= job.max_characters:
        raise TextExtractionWorkerError("processor_contract_violation", "text extractor returned an invalid result")
    if algorithm not in {"sha256", "sha384", "sha512"} or not _DIGEST.fullmatch(digest):
        raise TextExtractionWorkerError("processor_contract_violation", "text integrity result is invalid")
    return TextExtractionResult(job.job_id, "completed", job.output_ref, "text/plain", count, {"algorithm": algorithm, "digest": digest}, job.resource_admission_ref)
