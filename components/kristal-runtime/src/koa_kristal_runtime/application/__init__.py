"""Application boundary for Kristal Runtime.

The application layer accepts JSON-compatible mappings so that the concrete
B-0045 domain objects and B-0017 interface bindings can be connected without
this bundle importing or recreating them.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
import re
from types import MappingProxyType
from typing import Any, Final

_JSON_SCALAR = str | int | float | bool | None
JsonValue = _JSON_SCALAR | list["JsonValue"] | dict[str, "JsonValue"]
JsonMapping = Mapping[str, JsonValue]

ACCEPTED_ARTIFACT_CLASSES: Final[frozenset[str]] = frozenset(
    {"kristal_artifact", "runtime_pack"}
)
TERMINAL_LIFECYCLE_STATES: Final[frozenset[str]] = frozenset(
    {"revoked", "retired"}
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_RUNTIME_DIGEST_RE = re.compile(r"^sha(?:256|384|512):[0-9a-f]+$")


class ApplicationError(RuntimeError):
    """Closed, machine-readable application failure."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        details: Mapping[str, JsonValue] | None = None,
    ) -> None:
        if not code or not re.fullmatch(r"[a-z][a-z0-9_]*", code):
            raise ValueError("application error codes must be lower snake case")
        super().__init__(message)
        self.code = code
        self.details = freeze_mapping(details or {})


@dataclass(frozen=True, slots=True)
class ArtifactRef:
    """Stable reference to an admitted artifact."""

    artifact_class: str
    artifact_id: str
    artifact_version: str
    content_digest: str

    def as_mapping(self) -> Mapping[str, JsonValue]:
        return freeze_mapping(
            {
                "artifact_class": self.artifact_class,
                "artifact_id": self.artifact_id,
                "artifact_version": self.artifact_version,
                "content_digest": self.content_digest,
            }
        )


def as_mapping(value: object, *, name: str) -> Mapping[str, JsonValue]:
    """Convert a mapping, dataclass, or public ``to_mapping`` object safely."""

    candidate: object
    if isinstance(value, Mapping):
        candidate = value
    elif is_dataclass(value) and not isinstance(value, type):
        candidate = asdict(value)
    else:
        converter = getattr(value, "to_mapping", None)
        if not callable(converter):
            raise ApplicationError(
                "invalid_input",
                f"{name} must be a mapping or expose to_mapping()",
            )
        candidate = converter()
    if not isinstance(candidate, Mapping):
        raise ApplicationError("invalid_input", f"{name} did not resolve to a mapping")
    return freeze_mapping(candidate)


def freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, JsonValue]:
    """Return an immutable, detached, JSON-compatible mapping."""

    try:
        detached = json.loads(
            json.dumps(thaw(value), ensure_ascii=False, allow_nan=False, sort_keys=True)
        )
    except (TypeError, ValueError) as exc:
        raise ApplicationError(
            "non_json_value",
            "application inputs and port results must be JSON-compatible",
        ) from exc
    if not isinstance(detached, dict):
        raise ApplicationError("invalid_mapping", "expected a JSON object")
    return _deep_freeze(detached)


def thaw(value: JsonValue | Mapping[str, JsonValue] | Sequence[JsonValue]) -> JsonValue:
    """Return a detached mutable JSON value for a port invocation."""

    if isinstance(value, Mapping):
        return {str(k): thaw(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [thaw(v) for v in value]
    if isinstance(value, list):
        return [thaw(v) for v in value]
    return deepcopy(value)


def _deep_freeze(value: JsonValue) -> JsonValue:
    if isinstance(value, dict):
        return MappingProxyType({k: _deep_freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(v) for v in value)  # type: ignore[return-value]
    return value


def canonical_json(value: object) -> bytes:
    mapping = as_mapping(value, name="canonical value") if not isinstance(value, Mapping) else value
    try:
        return json.dumps(
            thaw(mapping),
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ApplicationError("non_json_value", "value is not canonical JSON") from exc


def deterministic_id(prefix: str, *values: object) -> str:
    digest = sha256()
    for value in values:
        if isinstance(value, Mapping):
            digest.update(canonical_json(value))
        else:
            digest.update(str(value).encode("utf-8"))
        digest.update(b"\x00")
    return f"{prefix}:{digest.hexdigest()}"


def require_non_empty_string(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ApplicationError("artifact_invalid", f"{key} must be a non-empty string")
    return value.strip()


def require_mapping(mapping: Mapping[str, Any], key: str) -> Mapping[str, JsonValue]:
    value = mapping.get(key)
    if not isinstance(value, Mapping):
        raise ApplicationError("artifact_invalid", f"{key} must be an object")
    return freeze_mapping(value)


def require_sequence(mapping: Mapping[str, Any], key: str) -> tuple[JsonValue, ...]:
    value = mapping.get(key)
    if not isinstance(value, (list, tuple)) or isinstance(value, (str, bytes)):
        raise ApplicationError("artifact_invalid", f"{key} must be an array")
    return tuple(value)


def artifact_ref_from(artifact: Mapping[str, JsonValue]) -> ArtifactRef:
    artifact_class = require_non_empty_string(artifact, "artifact_class")
    if artifact_class not in ACCEPTED_ARTIFACT_CLASSES:
        raise ApplicationError(
            "unsupported_artifact_class",
            f"unsupported artifact class: {artifact_class}",
        )
    if artifact_class == "kristal_artifact":
        artifact_id = require_non_empty_string(artifact, "artifact_id")
        artifact_version = require_non_empty_string(artifact, "artifact_version")
        identity = require_mapping(artifact, "content_identity")
        algorithm = require_non_empty_string(identity, "algorithm")
        digest = require_non_empty_string(identity, "digest")
        if algorithm != "sha256" or not _SHA256_RE.fullmatch(digest):
            raise ApplicationError(
                "content_identity_invalid",
                "Kristal content identity must be a lowercase sha256 digest",
            )
        return ArtifactRef(artifact_class, artifact_id, artifact_version, f"sha256:{digest}")

    artifact_id = require_non_empty_string(artifact, "artifact_identity")
    artifact_version = require_non_empty_string(artifact, "artifact_version")
    digest = require_non_empty_string(artifact, "artifact_digest")
    if not artifact_id.startswith("runtime-pack:") or not _RUNTIME_DIGEST_RE.fullmatch(digest):
        raise ApplicationError(
            "content_identity_invalid",
            "Runtime Pack identity or digest is invalid",
        )
    return ArtifactRef(artifact_class, artifact_id, artifact_version, digest)


def validate_artifact_structure(artifact: Mapping[str, JsonValue]) -> ArtifactRef:
    """Validate contract-critical invariants without replacing schema validation."""

    ref = artifact_ref_from(artifact)
    manifest = require_mapping(artifact, "manifest")
    entries = require_sequence(manifest, "entries")
    if not entries:
        raise ApplicationError("manifest_invalid", "manifest entries cannot be empty")
    seen_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise ApplicationError("manifest_invalid", "manifest entries must be objects")
        path = require_non_empty_string(entry, "path")
        if path.startswith("/") or ".." in path.split("/") or "\\" in path:
            raise ApplicationError("unsafe_manifest_path", f"unsafe manifest path: {path}")
        if path in seen_paths:
            raise ApplicationError("manifest_invalid", f"duplicate manifest path: {path}")
        seen_paths.add(path)
        digest = entry.get("sha256") or entry.get("digest")
        if not isinstance(digest, str) or not digest:
            raise ApplicationError("manifest_invalid", f"manifest digest missing for {path}")

    provenance = require_mapping(artifact, "provenance")
    producer = provenance.get("producer")
    if isinstance(producer, Mapping):
        producer_id = producer.get("producer_id") or producer.get("id")
        if not isinstance(producer_id, str) or not producer_id.strip():
            raise ApplicationError("missing_provenance", "provenance producer identity is required")
    elif not isinstance(producer, str) or not producer.strip():
        raise ApplicationError("missing_provenance", "provenance producer is required")

    if ref.artifact_class == "runtime_pack":
        if artifact.get("release_channel") != "knowledge":
            raise ApplicationError(
                "release_channel_invalid",
                "Runtime Packs must use the knowledge release channel",
            )
        lifecycle = require_mapping(artifact, "lifecycle")
        status = require_non_empty_string(lifecycle, "status")
        if status in TERMINAL_LIFECYCLE_STATES:
            raise ApplicationError(
                "artifact_not_admissible",
                f"a {status} Runtime Pack cannot be admitted",
            )
        handling = require_mapping(artifact, "content_handling")
        if handling.get("secret_values_allowed") is not False:
            raise ApplicationError(
                "secret_content_forbidden",
                "Runtime Packs cannot permit secret values",
            )
    else:
        require_mapping(artifact, "rights")
        require_mapping(artifact, "compatibility")
    return ref



def evaluate_policy_port(
    evaluator: object,
    action: str,
    actor_context: Mapping[str, Any],
    resource: Mapping[str, Any],
    context: Mapping[str, Any],
) -> Any:
    """Invoke the policy authority and convert transport failure to blocked."""

    method = getattr(evaluator, "evaluate", None)
    if not callable(method):
        raise ApplicationError("policy_protocol_error", "policy evaluator has no evaluate method")
    try:
        decision = method(action, thaw(actor_context), thaw(resource), thaw(context))
    except ApplicationError:
        raise
    except Exception as exc:
        raise ApplicationError(
            "policy_unavailable",
            f"policy evaluation is unavailable for {action}",
        ) from exc
    outcome = getattr(decision, "outcome", None)
    if outcome not in {"allow", "deny", "blocked"}:
        raise ApplicationError("policy_protocol_error", "policy returned an unknown outcome")
    for field in ("decision_id", "policy_ref", "receipt_ref"):
        value = getattr(decision, field, None)
        if not isinstance(value, str) or not value:
            raise ApplicationError("policy_protocol_error", f"policy decision lacks {field}")
    obligations = getattr(decision, "obligations", None)
    if not isinstance(obligations, Mapping):
        raise ApplicationError("policy_protocol_error", "policy obligations must be an object")
    return decision


def record_evidence_port(audit_sink: object, event: Mapping[str, Any], operation: str) -> str:
    """Secure a durable evidence receipt or fail the operation explicitly."""

    method = getattr(audit_sink, "record", None)
    if not callable(method):
        raise ApplicationError("audit_unavailable", "audit sink has no record method")
    try:
        receipt = method(thaw(event))
    except ApplicationError:
        raise
    except Exception as exc:
        raise ApplicationError("audit_unavailable", f"{operation} evidence is unavailable") from exc
    if not isinstance(receipt, str) or not receipt:
        raise ApplicationError("audit_unavailable", f"{operation} evidence was not secured")
    return receipt



from .admit_artifact import AdmitArtifact, AdmissionResult
from .execute_query import ExecuteQuery, QueryResult
from .render_artifact import RenderArtifact, RenderResult
from .revoke_artifact import RevokeArtifact, RevocationResult
from .verify_artifact import VerifyArtifact, VerificationResult

__all__ = [
    "AdmitArtifact",
    "AdmissionResult",
    "ApplicationError",
    "ArtifactRef",
    "ExecuteQuery",
    "QueryResult",
    "RenderArtifact",
    "RenderResult",
    "RevokeArtifact",
    "RevocationResult",
    "VerificationResult",
    "VerifyArtifact",
]
