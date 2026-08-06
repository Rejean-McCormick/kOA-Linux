"""Application use cases for the kOA Mediatheque."""

from __future__ import annotations

from hashlib import sha256


def stable_identifier(prefix: str, *parts: str) -> str:
    """Build a deterministic opaque identifier from canonical text inputs."""
    if not prefix.strip() or not parts or any(not part.strip() for part in parts):
        raise ValueError("stable identifier inputs must not be empty")
    material = "\x1f".join(parts).encode("utf-8")
    return f"{prefix}-{sha256(material).hexdigest()[:32]}"


from .build_rendition import BuildRendition, BuildRenditionRequest, BuildRenditionResult
from .delete_media import DeleteMedia, DeleteMediaRequest, DeleteMediaResult
from .export_media import ExportCandidate, ExportMedia, ExportMediaRequest, ExportMediaResult
from .ingest_media import IngestMedia, IngestMediaRequest, IngestMediaResult
from .update_metadata import UpdateMetadata, UpdateMetadataRequest, UpdateMetadataResult
from .verify_integrity import VerifyIntegrity, VerifyIntegrityRequest, VerifyIntegrityResult

__all__ = [
    "BuildRendition", "BuildRenditionRequest", "BuildRenditionResult",
    "DeleteMedia", "DeleteMediaRequest", "DeleteMediaResult", "ExportCandidate",
    "ExportMedia", "ExportMediaRequest", "ExportMediaResult", "IngestMedia",
    "IngestMediaRequest", "IngestMediaResult", "UpdateMetadata",
    "UpdateMetadataRequest", "UpdateMetadataResult", "VerifyIntegrity",
    "VerifyIntegrityRequest", "VerifyIntegrityResult", "stable_identifier",
]
