"""Build and verify canonical four-channel kOA Release Sets."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import total_ordering
from hashlib import sha256
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import FormatChecker
from jsonschema.validators import validator_for

from ..model import canonical_json_bytes, freeze_mapping, thaw_json
from .manifest import CANONICAL_CHANNEL_NAMESPACES, ReleaseManifest


DEFAULT_RELEASE_SET_SCHEMA = (
    Path(__file__).resolve().parents[4]
    / "docs/contracts/artifact-contracts/release-set.schema.json"
)
_VERSION = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
_CONSTRAINT = re.compile(r"^(>=|<=|>|<|==|=)?\s*(.+)$")


class ReleaseSetValidationError(ValueError):
    """Raised when schema or semantic Release Set verification fails."""

    def __init__(self, issues: Iterable[str]) -> None:
        normalized = tuple(sorted(set(str(issue) for issue in issues if str(issue))))
        self.issues = normalized
        super().__init__("; ".join(normalized) or "release set validation failed")


@total_ordering
@dataclass(frozen=True, slots=True)
class SemanticVersion:
    """Comparable SemVer core with deterministic pre-release ordering."""

    major: int
    minor: int
    patch: int
    prerelease: tuple[str, ...] = ()

    @classmethod
    def parse(cls, value: str) -> "SemanticVersion":
        match = _VERSION.fullmatch(value)
        if match is None:
            raise ReleaseSetValidationError([f"invalid semantic version: {value!r}"])
        prerelease = tuple(match.group(4).split(".")) if match.group(4) else ()
        return cls(int(match.group(1)), int(match.group(2)), int(match.group(3)), prerelease)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        core = (self.major, self.minor, self.patch)
        other_core = (other.major, other.minor, other.patch)
        if core != other_core:
            return core < other_core
        if not self.prerelease:
            return False if not other.prerelease else False
        if not other.prerelease:
            return True
        for left, right in zip(self.prerelease, other.prerelease, strict=False):
            if left == right:
                continue
            left_numeric = left.isdigit()
            right_numeric = right.isdigit()
            if left_numeric and right_numeric:
                return int(left) < int(right)
            if left_numeric != right_numeric:
                return left_numeric
            return left < right
        return len(self.prerelease) < len(other.prerelease)


@dataclass(frozen=True, slots=True)
class ReleaseSet:
    """Immutable, schema-validated Release Set document."""

    _document: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "_document", freeze_mapping(self._document))

    @property
    def release_set_id(self) -> str:
        return str(self._document["release_set_id"])

    @property
    def version(self) -> str:
        return str(self._document["version"])

    @property
    def lifecycle_status(self) -> str:
        return str(self._document["lifecycle_status"])

    def to_dict(self) -> dict[str, Any]:
        return thaw_json(self._document)

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self._document)

    @property
    def digest(self) -> str:
        return sha256(self.canonical_bytes()).hexdigest()


def build_release_set(
    *,
    release_set_id: str,
    version: str,
    lifecycle_status: str,
    issued_at: str,
    issuer: Mapping[str, Any],
    authority: Mapping[str, Any],
    manifests: Iterable[ReleaseManifest],
    compatibility: Mapping[str, Any],
    activation: Mapping[str, Any],
    signature: Mapping[str, Any],
    provenance: Mapping[str, Any],
    schema_path: str | Path = DEFAULT_RELEASE_SET_SCHEMA,
    target_scope: Mapping[str, Any] | None = None,
    effective_at: str | None = None,
    expires_at: str | None = None,
    lineage: Mapping[str, Any] | None = None,
    notes: Sequence[str] = (),
) -> ReleaseSet:
    """Build a complete Release Set from four already-owned channel manifests."""

    by_channel = _manifest_map(manifests)
    provenance_value = deepcopy(dict(provenance))
    expected_source_refs = [by_channel[channel].source_release_ref for channel in CANONICAL_CHANNEL_NAMESPACES]
    supplied_source_refs = provenance_value.get("source_release_refs")
    if supplied_source_refs is None:
        provenance_value["source_release_refs"] = expected_source_refs
    elif sorted(supplied_source_refs) != sorted(expected_source_refs):
        raise ReleaseSetValidationError(
            ["provenance.source_release_refs do not correspond one-to-one with channel manifests"]
        )

    document: dict[str, Any] = {
        "$schema": "release-set.schema.json",
        "artifact_class": "release_set",
        "release_set_id": release_set_id,
        "version": version,
        "lifecycle_status": lifecycle_status,
        "language": "en",
        "issued_at": issued_at,
        "issuer": deepcopy(dict(issuer)),
        "authority": deepcopy(dict(authority)),
        "channels": {
            channel: by_channel[channel].to_channel_release()
            for channel in CANONICAL_CHANNEL_NAMESPACES
        },
        "compatibility": _normalize_compatibility(compatibility),
        "activation": deepcopy(dict(activation)),
        "signature": deepcopy(dict(signature)),
        "provenance": provenance_value,
    }
    if target_scope is not None:
        document["target_scope"] = _normalize_target_scope(target_scope)
    if effective_at is not None:
        document["effective_at"] = effective_at
    if expires_at is not None:
        document["expires_at"] = expires_at
    if lineage is not None:
        document["lineage"] = deepcopy(dict(lineage))
    if notes:
        document["notes"] = sorted(set(notes))
    return validate_release_set(document, schema_path=schema_path)


def validate_release_set(
    document: Mapping[str, Any], *, schema_path: str | Path = DEFAULT_RELEASE_SET_SCHEMA
) -> ReleaseSet:
    """Validate schema plus machine-checkable Release Set semantic invariants."""

    if not isinstance(document, Mapping):
        raise ReleaseSetValidationError(["release set must be an object"])
    schema_file = Path(schema_path).expanduser().resolve(strict=True)
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema, format_checker=FormatChecker())
    schema_issues = []
    for error in sorted(
        validator.iter_errors(document),
        key=lambda item: (tuple(str(part) for part in item.absolute_path), item.message),
    ):
        pointer = _pointer(error.absolute_path)
        schema_issues.append(f"schema {pointer or '/'}: {error.message}")
    semantic_issues = _semantic_issues(document)
    if schema_issues or semantic_issues:
        raise ReleaseSetValidationError((*schema_issues, *semantic_issues))
    return ReleaseSet(deepcopy(dict(document)))


def load_release_set(
    path: str | Path, *, schema_path: str | Path = DEFAULT_RELEASE_SET_SCHEMA
) -> ReleaseSet:
    """Load strict JSON and reject duplicate keys before validation."""

    source = Path(path).expanduser().resolve(strict=True)
    try:
        document = json.loads(source.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ReleaseSetValidationError([f"invalid release set JSON: {exc}"]) from exc
    if not isinstance(document, Mapping):
        raise ReleaseSetValidationError(["release set JSON must contain an object"])
    return validate_release_set(document, schema_path=schema_path)


def version_satisfies(actual: str, constraint: str) -> bool:
    """Evaluate a closed comma-separated SemVer constraint expression."""

    candidate = SemanticVersion.parse(actual)
    clauses = [part.strip() for part in constraint.split(",")]
    if not clauses or any(not clause for clause in clauses):
        raise ReleaseSetValidationError([f"invalid semantic version constraint: {constraint!r}"])
    for clause in clauses:
        match = _CONSTRAINT.fullmatch(clause)
        if match is None:
            raise ReleaseSetValidationError([f"invalid semantic version constraint: {clause!r}"])
        operator = match.group(1) or "=="
        expected = SemanticVersion.parse(match.group(2).strip())
        if operator in {"=", "=="} and candidate != expected:
            return False
        if operator == ">" and not candidate > expected:
            return False
        if operator == ">=" and not candidate >= expected:
            return False
        if operator == "<" and not candidate < expected:
            return False
        if operator == "<=" and not candidate <= expected:
            return False
    return True


def _semantic_issues(document: Mapping[str, Any]) -> tuple[str, ...]:
    issues: list[str] = []
    channels = document.get("channels")
    expected_channels = tuple(CANONICAL_CHANNEL_NAMESPACES)
    if not isinstance(channels, Mapping):
        return ("channels must be an object",)
    if set(channels) != set(expected_channels):
        issues.append("channels must contain exactly system, services, governance, and knowledge")
    release_ids: list[str] = []
    manifest_refs: list[str] = []
    artifact_refs: list[str] = []
    for channel_id in expected_channels:
        value = channels.get(channel_id)
        if not isinstance(value, Mapping):
            continue
        if value.get("channel_id") != channel_id:
            issues.append(f"channels.{channel_id}.channel_id does not match its channel key")
        namespace = CANONICAL_CHANNEL_NAMESPACES[channel_id]
        if value.get("release_namespace") != namespace:
            issues.append(f"channels.{channel_id}.release_namespace must be {namespace}")
        release_ids.append(str(value.get("release_id", "")))
        manifest_refs.append(str(value.get("release_manifest_ref", "")))
        refs = value.get("artifact_refs")
        if isinstance(refs, list):
            artifact_refs.extend(str(item) for item in refs)
    for label, values in (
        ("release_id", release_ids),
        ("release_manifest_ref", manifest_refs),
        ("artifact_ref across channels", artifact_refs),
    ):
        if len(values) != len(set(values)):
            issues.append(f"duplicate {label} values are prohibited")

    provenance = document.get("provenance")
    if isinstance(provenance, Mapping):
        source_refs = provenance.get("source_release_refs")
        expected_refs = [_source_ref_from_manifest(value) for value in manifest_refs]
        if isinstance(source_refs, list) and sorted(source_refs) != sorted(expected_refs):
            issues.append(
                "provenance.source_release_refs must correspond one-to-one with channel releases"
            )

    compatibility = document.get("compatibility")
    activation = document.get("activation")
    eligible = isinstance(activation, Mapping) and activation.get("eligibility") == "eligible"
    if isinstance(compatibility, Mapping):
        constraints = compatibility.get("constraint_results")
        if not isinstance(constraints, list) or not constraints:
            issues.append("compatibility.constraint_results must be non-empty")
        else:
            identifiers: list[str] = []
            for constraint in constraints:
                if not isinstance(constraint, Mapping):
                    issues.append("compatibility constraints must be objects")
                    continue
                identifiers.append(str(constraint.get("constraint_id", "")))
                issues.extend(_constraint_issues(constraint))
            if len(identifiers) != len(set(identifiers)):
                issues.append("compatibility constraint_id values must be unique")
        if eligible and compatibility.get("status") != "tested_compatible":
            issues.append("activation eligibility requires tested_compatible status")
        if eligible and isinstance(constraints, list):
            if any(not isinstance(item, Mapping) or item.get("result") != "pass" for item in constraints):
                issues.append("activation eligibility requires every compatibility constraint to pass")

    target_scope = document.get("target_scope")
    if eligible and isinstance(target_scope, Mapping):
        profile_results = target_scope.get("profile_results")
        if isinstance(profile_results, list) and any(
            not isinstance(item, Mapping) or item.get("result") != "pass"
            for item in profile_results
        ):
            issues.append("activation eligibility requires every target profile result to pass")

    if eligible and isinstance(activation, Mapping) and activation.get("partial_activation_allowed") is not False:
        issues.append("partial authoritative activation is prohibited")
    return tuple(sorted(set(issues)))


def _constraint_issues(value: Mapping[str, Any]) -> list[str]:
    constraint_id = str(value.get("constraint_id", "<unknown>"))
    expected = value.get("expected")
    actual = value.get("actual")
    operator = value.get("operator")
    kind = value.get("kind")
    claimed = value.get("result")
    computed: bool | None = None
    try:
        if operator == "equals":
            computed = actual == expected
        elif operator == "not_equals":
            computed = actual != expected
        elif operator == "semver_satisfies":
            if not isinstance(actual, str) or not isinstance(expected, str):
                raise ReleaseSetValidationError(["semver_satisfies requires string actual and expected"])
            computed = version_satisfies(actual, expected)
        elif operator in {"compatible_with", "supports"}:
            if isinstance(expected, list):
                computed = actual in expected
            else:
                computed = actual == expected
        elif operator == "prohibits":
            prohibited = expected if isinstance(expected, list) else [expected]
            computed = actual not in prohibited
        else:
            return [f"constraint {constraint_id} uses unsupported operator {operator!r}"]

        if kind == "minimum_supported_version":
            computed = _version_compare(actual, expected, minimum=True)
        elif kind == "maximum_supported_version":
            computed = _version_compare(actual, expected, minimum=False)
        elif kind == "prohibited_version":
            prohibited = expected if isinstance(expected, list) else [expected]
            computed = actual not in prohibited
    except ReleaseSetValidationError as exc:
        return [f"constraint {constraint_id}: {issue}" for issue in exc.issues]
    expected_result = "pass" if computed else "fail"
    if claimed != expected_result:
        return [
            f"constraint {constraint_id} claims {claimed!r} but evaluates to {expected_result!r}"
        ]
    return [] if computed else [f"constraint {constraint_id} is incompatible"]


def _version_compare(actual: Any, expected: Any, *, minimum: bool) -> bool:
    if not isinstance(actual, str) or not isinstance(expected, str):
        raise ReleaseSetValidationError(["version constraint requires string actual and expected"])
    left = SemanticVersion.parse(actual)
    right = SemanticVersion.parse(expected)
    return left >= right if minimum else left <= right


def _manifest_map(manifests: Iterable[ReleaseManifest]) -> Mapping[str, ReleaseManifest]:
    values = tuple(manifests)
    by_channel = {item.channel_id: item for item in values}
    if len(by_channel) != len(values):
        raise ReleaseSetValidationError(["duplicate channel manifests are prohibited"])
    if set(by_channel) != set(CANONICAL_CHANNEL_NAMESPACES):
        raise ReleaseSetValidationError(
            ["exactly one manifest is required for system, services, governance, and knowledge"]
        )
    return MappingProxyType(by_channel)


def _normalize_compatibility(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    constraints = result.get("constraint_results")
    if isinstance(constraints, list):
        result["constraint_results"] = sorted(
            constraints, key=lambda item: str(item.get("constraint_id", "")) if isinstance(item, Mapping) else ""
        )
    evidence = result.get("test_evidence_refs")
    if isinstance(evidence, list):
        result["test_evidence_refs"] = sorted(set(evidence))
    limitations = result.get("known_limitations")
    if isinstance(limitations, list):
        result["known_limitations"] = sorted(set(limitations))
    return result


def _normalize_target_scope(value: Mapping[str, Any]) -> dict[str, Any]:
    result = deepcopy(dict(value))
    profiles = result.get("profile_results")
    if isinstance(profiles, list):
        result["profile_results"] = sorted(
            profiles, key=lambda item: str(item.get("profile_id", "")) if isinstance(item, Mapping) else ""
        )
    for key in ("deployment_ids", "overlay_ids", "environment_labels"):
        items = result.get(key)
        if isinstance(items, list):
            result[key] = sorted(set(items))
    return result


def _source_ref_from_manifest(manifest_ref: str) -> str:
    return manifest_ref[:-9] if manifest_ref.endswith("/manifest") else manifest_ref


def _pointer(parts: Iterable[Any]) -> str:
    values = [str(part).replace("~", "~0").replace("/", "~1") for part in parts]
    return "" if not values else "/" + "/".join(values)


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key: {key}")
        result[key] = value
    return result
