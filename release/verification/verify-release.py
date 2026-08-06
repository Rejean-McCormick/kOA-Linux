#!/usr/bin/env python3
"""Fail-closed verification of a kOA Release Set and detached signatures.

The verifier deliberately does not sign, publish, stage, activate, download, or
repair a release. It consumes a locally supplied Release Set, detached signature
envelopes, a digest-pinned public trust bundle, and repository-owned policies.

Private keys are neither accepted nor read. Network access is not used.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import math
import os
import re
import sys
import tomllib
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, NoReturn, Sequence

TOOL_ID = "koa-release-verifier"
TOOL_VERSION = "1.0.0"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
STABLE_ID_RE = re.compile(r"^[a-z0-9]+(?:[._:-][a-z0-9]+)*$")
PRIVATE_FIELD_FRAGMENTS = (
    "private_key",
    "secret_key",
    "recovery_secret",
    "bearer_token",
    "passphrase",
)
EXPECTED_CHANNELS = ("governance", "knowledge", "services", "system")
SIGNATURE_FIELDS = frozenset({"schema_version", "signature_id", "statement", "algorithm", "signature"})
STATEMENT_FIELDS = frozenset(
    {
        "domain",
        "subject",
        "purpose",
        "environment",
        "profiles",
        "role_id",
        "signer_id",
        "key_id",
        "issued_at",
        "expires_at",
        "sequence",
        "approval_refs",
        "mode",
    }
)
SUBJECT_FIELDS = frozenset(
    {"path", "sha256", "artifact_class", "release_set_id", "version", "release_channels"}
)
TRUST_BUNDLE_FIELDS = frozenset(
    {
        "schema_version",
        "bundle_id",
        "trust_epoch",
        "issued_at",
        "expires_at",
        "offline_capable",
        "revocation_snapshot",
        "keys",
    }
)
TRUST_KEY_FIELDS = frozenset(
    {
        "key_id",
        "signer_id",
        "role_id",
        "algorithm",
        "public_key_pem",
        "valid_from",
        "valid_until",
        "revoked_at",
        "custody",
        "scopes",
    }
)
TRUST_SCOPE_FIELDS = frozenset(
    {"artifact_classes", "release_channels", "environments", "profiles", "purposes"}
)
REVOCATION_FIELDS = frozenset({"sequence", "issued_at", "expires_at", "revoked_key_ids"})


@dataclass(frozen=True, order=True)
class Diagnostic:
    severity: str
    code: str
    authority: str
    message: str
    path: str = ""
    pointer: str = ""

    def to_dict(self) -> dict[str, str]:
        result = {
            "severity": self.severity,
            "code": self.code,
            "authority": self.authority,
            "message": self.message,
        }
        if self.path:
            result["path"] = self.path
        if self.pointer:
            result["pointer"] = self.pointer
        return result


@dataclass
class VerificationContext:
    diagnostics: list[Diagnostic] = field(default_factory=list)

    def add(
        self,
        code: str,
        message: str,
        *,
        authority: str,
        path: Path | str | None = None,
        pointer: str = "",
        severity: str = "error",
    ) -> None:
        self.diagnostics.append(
            Diagnostic(
                severity=severity,
                code=code,
                authority=authority,
                message=message,
                path=str(path) if path else "",
                pointer=pointer,
            )
        )

    @property
    def failed(self) -> bool:
        return any(item.severity == "error" for item in self.diagnostics)

    def sorted(self) -> list[Diagnostic]:
        return sorted(self.diagnostics)


@dataclass(frozen=True)
class LoadedConfiguration:
    verification: Mapping[str, Any]
    signing: Mapping[str, Any]
    roles: Mapping[str, Mapping[str, Any]]
    offline: Mapping[str, Any]
    paths: Mapping[str, Path]


@dataclass(frozen=True)
class VerifiedSignature:
    signature_id: str
    role_id: str
    signer_id: str
    key_id: str
    algorithm: str
    statement_digest: str
    threshold_context_digest: str
    mode: str


class ConfigurationError(RuntimeError):
    """Raised for an unusable local verifier configuration."""


class InputError(RuntimeError):
    """Raised for an unreadable or unsafe verification input."""


def _die(message: str, *, exit_code: int = 2) -> NoReturn:
    print(f"{TOOL_ID}: {message}", file=sys.stderr)
    raise SystemExit(exit_code)


def _reject_constant(value: str) -> NoReturn:
    raise ValueError(f"non-finite JSON number is forbidden: {value}")


def _reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _read_bounded(path: Path, maximum_bytes: int) -> bytes:
    try:
        stat = path.stat()
    except OSError as exc:
        raise InputError(f"cannot stat {path}: {exc}") from exc
    if not path.is_file():
        raise InputError(f"expected a regular file: {path}")
    if stat.st_size > maximum_bytes:
        raise InputError(f"file exceeds {maximum_bytes} bytes: {path}")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise InputError(f"cannot read {path}: {exc}") from exc


def _load_json(path: Path, maximum_bytes: int) -> Any:
    raw = _read_bounded(path, maximum_bytes)
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InputError(f"JSON is not UTF-8: {path}: {exc}") from exc
    try:
        return json.loads(
            text,
            object_pairs_hook=_reject_duplicates,
            parse_constant=_reject_constant,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise InputError(f"invalid strict JSON in {path}: {exc}") from exc


def _load_toml(path: Path) -> Mapping[str, Any]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigurationError(f"invalid TOML {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ConfigurationError(f"TOML root must be a table: {path}")
    _reject_private_material(data, path)
    return _deep_freeze(data)


def _deep_freeze(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({str(k): _deep_freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_deep_freeze(item) for item in value)
    return value


def _reject_private_material(value: Any, source: Path | str, path: tuple[str, ...] = ()) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if any(fragment in normalized for fragment in PRIVATE_FIELD_FRAGMENTS):
                if child not in (False, None, "", (), [], {}):
                    raise ConfigurationError(
                        f"private or secret material field is forbidden in {source}: {'.'.join(path + (str(key),))}"
                    )
            _reject_private_material(child, source, path + (str(key),))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _reject_private_material(child, source, path + (str(index),))


def _canonical_json(value: Any) -> bytes:
    _validate_canonical_value(value, pointer="")
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _validate_canonical_value(value: Any, *, pointer: str) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InputError(f"non-finite number at {pointer or '/'}")
        raise InputError(f"floating-point values are forbidden in signed statements at {pointer or '/'}")
    if isinstance(value, list):
        for index, child in enumerate(value):
            _validate_canonical_value(child, pointer=f"{pointer}/{index}")
        return
    if isinstance(value, dict):
        for key in sorted(value):
            if not isinstance(key, str):
                raise InputError(f"non-string object key at {pointer or '/'}")
            escaped = key.replace("~", "~0").replace("/", "~1")
            _validate_canonical_value(value[key], pointer=f"{pointer}/{escaped}")
        return
    raise InputError(f"unsupported canonical JSON type at {pointer or '/'}: {type(value).__name__}")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
    except OSError as exc:
        raise InputError(f"cannot hash {path}: {exc}") from exc
    return digest.hexdigest()


def _parse_time(value: Any, *, field_name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise InputError(f"{field_name} must be a non-empty RFC 3339 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise InputError(f"invalid timestamp for {field_name}: {value}") from exc
    if parsed.tzinfo is None:
        raise InputError(f"timestamp lacks timezone for {field_name}: {value}")
    return parsed.astimezone(timezone.utc)


def _resolve_under(root: Path, value: Path | str, *, must_exist: bool = True) -> Path:
    root = root.resolve(strict=True)
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve(strict=must_exist)
    except OSError as exc:
        raise InputError(f"cannot resolve path {candidate}: {exc}") from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise InputError(f"path escapes repository root {root}: {candidate}") from exc
    if must_exist and not resolved.is_file():
        raise InputError(f"expected a regular file: {resolved}")
    return resolved


def _relative_to(root: Path, path: Path) -> str:
    return path.resolve(strict=True).relative_to(root.resolve(strict=True)).as_posix()


def _display_path(root: Path, value: Path | str) -> str:
    try:
        candidate = Path(value)
        resolved = candidate.resolve(strict=False)
        return resolved.relative_to(root.resolve(strict=True)).as_posix()
    except (OSError, ValueError):
        return str(value)


def _expect_mapping(value: Any, field_name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InputError(f"{field_name} must be an object")
    return value


def _expect_sequence(value: Any, field_name: str, *, allow_empty: bool = False) -> Sequence[Any]:
    if not isinstance(value, (list, tuple)) or isinstance(value, (str, bytes)):
        raise InputError(f"{field_name} must be an array")
    if not allow_empty and not value:
        raise InputError(f"{field_name} must not be empty")
    return value


def _expect_string(value: Any, field_name: str, *, stable_id: bool = False) -> str:
    if not isinstance(value, str) or not value:
        raise InputError(f"{field_name} must be a non-empty string")
    if stable_id and not STABLE_ID_RE.fullmatch(value):
        raise InputError(f"{field_name} is not a stable identifier: {value}")
    return value


def _expect_exact_fields(value: Mapping[str, Any], expected: frozenset[str], field_name: str) -> None:
    actual = frozenset(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise InputError(f"{field_name} misses required fields: {', '.join(missing)}")
    if unknown:
        raise InputError(f"{field_name} contains unknown fields: {', '.join(unknown)}")


def _config_path(repository_root: Path, base: Path, value: Any, field_name: str) -> Path:
    ref = _expect_string(value, field_name)
    if ref.startswith("release/") or ref.startswith("docs/"):
        return _resolve_under(repository_root, ref)
    return _resolve_under(repository_root, base.parent / ref)


def load_configuration(
    repository_root: Path,
    verification_policy_path: Path,
    signing_policy_override: Path | None,
    roles_override: Path | None,
    offline_policy_override: Path | None,
) -> LoadedConfiguration:
    verification_path = _resolve_under(repository_root, verification_policy_path)
    verification = _load_toml(verification_path)
    if verification.get("status") != "active":
        raise ConfigurationError("verification policy is not active")

    signing_path = (
        _resolve_under(repository_root, signing_policy_override)
        if signing_policy_override
        else _config_path(
            repository_root,
            verification_path,
            verification.get("signing_policy_ref"),
            "signing_policy_ref",
        )
    )
    roles_path = (
        _resolve_under(repository_root, roles_override)
        if roles_override
        else _config_path(
            repository_root,
            verification_path,
            verification.get("roles_ref"),
            "roles_ref",
        )
    )
    offline_path = (
        _resolve_under(repository_root, offline_policy_override)
        if offline_policy_override
        else _config_path(
            repository_root,
            verification_path,
            verification.get("offline_policy_ref"),
            "offline_policy_ref",
        )
    )
    signing = _load_toml(signing_path)
    roles_document = _load_toml(roles_path)
    offline = _load_toml(offline_path)

    if signing.get("status") != "active" or roles_document.get("status") != "active":
        raise ConfigurationError("signing policy and roles registry must both be active")
    if offline.get("status") != "active":
        raise ConfigurationError("offline signing policy is not active")

    raw_roles = roles_document.get("roles")
    if not isinstance(raw_roles, tuple) or not raw_roles:
        raise ConfigurationError("roles.toml must declare at least one [[roles]] table")
    roles: dict[str, Mapping[str, Any]] = {}
    for role in raw_roles:
        if not isinstance(role, Mapping):
            raise ConfigurationError("every roles entry must be a table")
        role_id = role.get("role_id")
        if not isinstance(role_id, str) or not STABLE_ID_RE.fullmatch(role_id):
            raise ConfigurationError(f"invalid role_id: {role_id!r}")
        if role_id in roles:
            raise ConfigurationError(f"duplicate role_id: {role_id}")
        roles[role_id] = role

    signing_roles_ref = signing.get("roles_ref")
    if signing_roles_ref:
        expected_roles_path = _config_path(
            repository_root, signing_path, signing_roles_ref, "roles_ref"
        )
        if expected_roles_path != roles_path:
            raise ConfigurationError(
                f"signing policy roles_ref resolves to {expected_roles_path}, not {roles_path}"
            )

    return LoadedConfiguration(
        verification=verification,
        signing=signing,
        roles=MappingProxyType(roles),
        offline=offline,
        paths=MappingProxyType(
            {
                "verification": verification_path,
                "signing": signing_path,
                "roles": roles_path,
                "offline": offline_path,
            }
        ),
    )


def _schema_validate_release_set(
    context: VerificationContext,
    release_set: Mapping[str, Any],
    repository_root: Path,
    configuration: LoadedConfiguration,
) -> None:
    verification = configuration.verification
    release_policy = _expect_mapping(verification.get("release_set"), "verification.release_set")
    if release_policy.get("require_schema_validation") is not True:
        context.add(
            "VERIFICATION_POLICY_WEAKENED",
            "release-set schema validation must remain enabled",
            authority=str(configuration.paths["verification"]),
        )
        return
    schema_path = _config_path(
        repository_root,
        configuration.paths["verification"],
        verification.get("release_set_schema_ref"),
        "release_set_schema_ref",
    )
    try:
        schema = _load_json(schema_path, 16 * 1024 * 1024)
        import jsonschema
        from jsonschema import FormatChecker

        validator = jsonschema.Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(release_set), key=lambda error: list(error.absolute_path))
    except ImportError:
        context.add(
            "CRYPTO_OR_SCHEMA_BACKEND_UNAVAILABLE",
            "python package 'jsonschema' is required by the active verification policy",
            authority=str(schema_path),
        )
        return
    except (InputError, jsonschema.SchemaError) as exc:
        context.add(
            "RELEASE_SET_SCHEMA_UNUSABLE",
            str(exc),
            authority=str(schema_path),
        )
        return
    for error in errors:
        pointer = "".join(f"/{str(part).replace('~', '~0').replace('/', '~1')}" for part in error.absolute_path)
        context.add(
            "RELEASE_SET_SCHEMA_VIOLATION",
            error.message,
            authority=str(schema_path),
            pointer=pointer or "/",
        )


def _semantic_validate_release_set(
    context: VerificationContext,
    release_set: Mapping[str, Any],
    configuration: LoadedConfiguration,
    now: datetime,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    verification = configuration.verification
    signing = configuration.signing
    release_policy = _expect_mapping(verification.get("release_set"), "verification.release_set")
    baseline = _expect_mapping(signing.get("baseline"), "signing.baseline")
    statement_policy = _expect_mapping(signing.get("statement"), "signing.statement")

    artifact_class = release_set.get("artifact_class")
    if artifact_class != release_policy.get("required_artifact_class"):
        context.add(
            "RELEASE_SET_WRONG_ARTIFACT_CLASS",
            f"expected artifact_class={release_policy.get('required_artifact_class')!r}, got {artifact_class!r}",
            authority=str(configuration.paths["verification"]),
            pointer="/artifact_class",
        )

    lifecycle_status = release_set.get("lifecycle_status")
    allowed_statuses = tuple(baseline.get("allowed_lifecycle_statuses", ()))
    if lifecycle_status not in allowed_statuses:
        context.add(
            "RELEASE_SET_STATUS_BLOCKED",
            f"lifecycle_status {lifecycle_status!r} is not eligible; allowed={list(allowed_statuses)!r}",
            authority=str(configuration.paths["signing"]),
            pointer="/lifecycle_status",
        )

    expires_at = release_set.get("expires_at")
    if expires_at is not None:
        try:
            if _parse_time(expires_at, field_name="release_set.expires_at") <= now:
                context.add(
                    "RELEASE_SET_EXPIRED",
                    "release set has expired",
                    authority="docs/06-lifecycle/12-artifact-verification.md",
                    pointer="/expires_at",
                )
        except InputError as exc:
            context.add(
                "RELEASE_SET_TIME_INVALID",
                str(exc),
                authority="docs/contracts/artifact-contracts/release-set.schema.json",
                pointer="/expires_at",
            )

    channels = release_set.get("channels")
    required_channels = tuple(sorted(release_policy.get("required_channels", ())))
    actual_channels: tuple[str, ...] = ()
    if not isinstance(channels, Mapping):
        context.add(
            "RELEASE_SET_CHANNELS_INVALID",
            "channels must be an object",
            authority="docs/contracts/artifact-contracts/release-set.schema.json",
            pointer="/channels",
        )
    else:
        actual_channels = tuple(sorted(str(key) for key in channels))
        if actual_channels != required_channels or actual_channels != EXPECTED_CHANNELS:
            context.add(
                "RELEASE_SET_CHANNELS_INCOMPLETE",
                f"expected exactly {list(EXPECTED_CHANNELS)}, got {list(actual_channels)}",
                authority="docs/contracts/release-channels.contract.json",
                pointer="/channels",
            )
        for channel_id in actual_channels:
            member = channels.get(channel_id)
            if not isinstance(member, Mapping) or member.get("channel_id") != channel_id:
                context.add(
                    "RELEASE_SET_CHANNEL_ID_MISMATCH",
                    f"embedded channel_id does not match key {channel_id!r}",
                    authority="docs/contracts/release-channels.contract.json",
                    pointer=f"/channels/{channel_id}/channel_id",
                )

    compatibility = release_set.get("compatibility")
    required_compatibility = baseline.get("require_compatibility_status")
    if not isinstance(compatibility, Mapping) or compatibility.get("status") != required_compatibility:
        context.add(
            "RELEASE_SET_COMPATIBILITY_BLOCKED",
            f"compatibility.status must be {required_compatibility!r}",
            authority="docs/06-lifecycle/02-release-model.md",
            pointer="/compatibility/status",
        )
    elif release_policy.get("require_all_constraint_results_pass") is True:
        results = compatibility.get("constraint_results")
        if not isinstance(results, list) or not results:
            context.add(
                "RELEASE_SET_CONSTRAINT_EVIDENCE_MISSING",
                "compatibility.constraint_results must be non-empty",
                authority="docs/contracts/artifact-contracts/release-set.schema.json",
                pointer="/compatibility/constraint_results",
            )
        else:
            for index, result in enumerate(results):
                if not isinstance(result, Mapping) or result.get("result") != "pass":
                    context.add(
                        "RELEASE_SET_CONSTRAINT_FAILED",
                        "every compatibility constraint must pass",
                        authority="docs/06-lifecycle/02-release-model.md",
                        pointer=f"/compatibility/constraint_results/{index}/result",
                    )
        if release_policy.get("require_test_evidence") is True and not compatibility.get("test_evidence_refs"):
            context.add(
                "RELEASE_SET_TEST_EVIDENCE_MISSING",
                "compatibility test evidence is required",
                authority="docs/06-lifecycle/02-release-model.md",
                pointer="/compatibility/test_evidence_refs",
            )

    activation = release_set.get("activation")
    required_eligibility = baseline.get("require_activation_eligibility")
    if not isinstance(activation, Mapping) or activation.get("eligibility") != required_eligibility:
        context.add(
            "RELEASE_SET_ACTIVATION_BLOCKED",
            f"activation.eligibility must be {required_eligibility!r}",
            authority="docs/06-lifecycle/02-release-model.md",
            pointer="/activation/eligibility",
        )
    elif activation.get("partial_activation_allowed") is not baseline.get("allow_partial_activation"):
        context.add(
            "RELEASE_SET_PARTIAL_ACTIVATION_FORBIDDEN",
            "partial authoritative activation is forbidden",
            authority="docs/06-lifecycle/02-release-model.md",
            pointer="/activation/partial_activation_allowed",
        )
    elif release_policy.get("require_activation_evidence") is True and not activation.get("activation_evidence_refs"):
        context.add(
            "RELEASE_SET_ACTIVATION_EVIDENCE_MISSING",
            "activation evidence is required",
            authority="docs/contracts/artifact-contracts/release-set.schema.json",
            pointer="/activation/activation_evidence_refs",
        )

    provenance = release_set.get("provenance")
    if release_policy.get("require_provenance") is True and not isinstance(provenance, Mapping):
        context.add(
            "RELEASE_SET_PROVENANCE_MISSING",
            "provenance object is required",
            authority="docs/06-lifecycle/18-sbom-provenance-and-signing.md",
            pointer="/provenance",
        )

    signature = release_set.get("signature")
    if not isinstance(signature, Mapping):
        context.add(
            "RELEASE_SET_SIGNATURE_DECLARATION_MISSING",
            "release set must declare its detached signature artifact",
            authority="docs/contracts/artifact-contracts/release-set.schema.json",
            pointer="/signature",
        )
    elif signature.get("verification_status") in {"invalid", "revoked"}:
        context.add(
            "RELEASE_SET_EMBEDDED_SIGNATURE_BLOCKED",
            f"embedded signature state is {signature.get('verification_status')!r}",
            authority="docs/06-lifecycle/12-artifact-verification.md",
            pointer="/signature/verification_status",
        )

    profile_ids: list[str] = []
    target_scope = release_set.get("target_scope")
    if not isinstance(target_scope, Mapping):
        context.add(
            "RELEASE_SET_TARGET_SCOPE_MISSING",
            "target_scope with profile_results is required by verification policy",
            authority=str(configuration.paths["verification"]),
            pointer="/target_scope",
        )
    else:
        profile_results = target_scope.get("profile_results")
        if not isinstance(profile_results, list) or not profile_results:
            context.add(
                "RELEASE_SET_PROFILE_RESULTS_MISSING",
                "target_scope.profile_results must be non-empty",
                authority="docs/contracts/artifact-contracts/release-set.schema.json",
                pointer="/target_scope/profile_results",
            )
        else:
            for index, item in enumerate(profile_results):
                if not isinstance(item, Mapping):
                    context.add(
                        "RELEASE_SET_PROFILE_RESULT_INVALID",
                        "profile result must be an object",
                        authority="docs/contracts/artifact-contracts/release-set.schema.json",
                        pointer=f"/target_scope/profile_results/{index}",
                    )
                    continue
                profile_id = item.get("profile_id")
                if isinstance(profile_id, str):
                    profile_ids.append(profile_id)
                if release_policy.get("require_all_profile_results_pass") is True and item.get("result") != "pass":
                    context.add(
                        "RELEASE_SET_PROFILE_BLOCKED",
                        f"profile {profile_id!r} result is not pass",
                        authority="docs/06-lifecycle/02-release-model.md",
                        pointer=f"/target_scope/profile_results/{index}/result",
                    )
    if len(profile_ids) != len(set(profile_ids)):
        context.add(
            "RELEASE_SET_PROFILE_DUPLICATE",
            "profile_results contains duplicate profile identifiers",
            authority="docs/contracts/artifact-contracts/release-set.schema.json",
            pointer="/target_scope/profile_results",
        )

    declared_channels = tuple(statement_policy.get("required_release_channels", ()))
    if tuple(sorted(declared_channels)) != EXPECTED_CHANNELS:
        context.add(
            "SIGNING_POLICY_CHANNEL_SET_INVALID",
            f"signing policy must bind exactly {list(EXPECTED_CHANNELS)}",
            authority=str(configuration.paths["signing"]),
        )
    return tuple(sorted(set(profile_ids))), actual_channels


def _load_trust_bundle(
    context: VerificationContext,
    path: Path,
    expected_digest: str,
    configuration: LoadedConfiguration,
    now: datetime,
    maximum_bytes: int,
    minimum_trust_epoch: int,
    minimum_revocation_sequence: int,
) -> tuple[Mapping[str, Any], Mapping[str, Mapping[str, Any]]]:
    if not SHA256_RE.fullmatch(expected_digest):
        raise InputError("--trust-bundle-sha256 must be exactly 64 lowercase hexadecimal characters")
    actual_digest = _sha256_file(path)
    if actual_digest != expected_digest:
        context.add(
            "TRUST_BUNDLE_DIGEST_MISMATCH",
            f"expected {expected_digest}, got {actual_digest}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=path,
        )
    bundle = _load_json(path, maximum_bytes)
    if not isinstance(bundle, Mapping):
        raise InputError("trust bundle root must be an object")
    _expect_exact_fields(bundle, TRUST_BUNDLE_FIELDS, "trust bundle")
    _reject_private_material(bundle, path)
    if bundle.get("schema_version") != "1.0":
        context.add(
            "TRUST_BUNDLE_VERSION_UNSUPPORTED",
            f"unsupported trust bundle schema_version {bundle.get('schema_version')!r}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=path,
        )
    _expect_string(bundle.get("bundle_id"), "trust bundle.bundle_id", stable_id=True)
    if not isinstance(bundle.get("trust_epoch"), int) or bundle.get("trust_epoch") < 1:
        raise InputError("trust bundle.trust_epoch must be a positive integer")
    if bundle.get("trust_epoch") < minimum_trust_epoch:
        context.add(
            "TRUST_BUNDLE_EPOCH_DOWNGRADE",
            f"trust epoch {bundle.get('trust_epoch')} is below retained minimum {minimum_trust_epoch}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=path,
        )
    issued_at = _parse_time(bundle.get("issued_at"), field_name="trust bundle.issued_at")
    expires_at = _parse_time(bundle.get("expires_at"), field_name="trust bundle.expires_at")
    if issued_at > now or expires_at <= now or expires_at <= issued_at:
        context.add(
            "TRUST_BUNDLE_NOT_CURRENT",
            "trust bundle is not currently valid",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=path,
        )

    revocation = _expect_mapping(bundle.get("revocation_snapshot"), "trust bundle.revocation_snapshot")
    _expect_exact_fields(revocation, REVOCATION_FIELDS, "trust bundle.revocation_snapshot")
    if not isinstance(revocation.get("sequence"), int) or revocation.get("sequence") < 1:
        raise InputError("revocation_snapshot.sequence must be a positive integer")
    if revocation.get("sequence") < minimum_revocation_sequence:
        context.add(
            "REVOCATION_SEQUENCE_DOWNGRADE",
            f"revocation sequence {revocation.get('sequence')} is below retained minimum {minimum_revocation_sequence}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=path,
        )
    rev_issued = _parse_time(revocation.get("issued_at"), field_name="revocation_snapshot.issued_at")
    rev_expires = _parse_time(revocation.get("expires_at"), field_name="revocation_snapshot.expires_at")
    if rev_issued > now or rev_expires <= now or rev_expires <= rev_issued:
        context.add(
            "REVOCATION_SNAPSHOT_NOT_CURRENT",
            "revocation snapshot is not currently valid",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=path,
        )
    revoked_ids_raw = _expect_sequence(
        revocation.get("revoked_key_ids"), "revocation_snapshot.revoked_key_ids", allow_empty=True
    )
    revoked_ids = tuple(_expect_string(item, "revoked_key_id", stable_id=True) for item in revoked_ids_raw)
    if len(revoked_ids) != len(set(revoked_ids)):
        raise InputError("revocation_snapshot.revoked_key_ids contains duplicates")

    input_policy = _expect_mapping(configuration.verification.get("input"), "verification.input")
    max_keys = int(input_policy.get("maximum_trust_key_count", 256))
    keys_raw = _expect_sequence(bundle.get("keys"), "trust bundle.keys")
    if len(keys_raw) > max_keys:
        raise InputError(f"trust bundle has more than {max_keys} keys")
    keys: dict[str, Mapping[str, Any]] = {}
    for index, item in enumerate(keys_raw):
        key = _expect_mapping(item, f"trust bundle.keys[{index}]")
        _expect_exact_fields(key, TRUST_KEY_FIELDS, f"trust bundle.keys[{index}]")
        key_id = _expect_string(key.get("key_id"), f"keys[{index}].key_id", stable_id=True)
        if key_id in keys:
            raise InputError(f"duplicate trust key_id: {key_id}")
        _expect_string(key.get("signer_id"), f"keys[{index}].signer_id", stable_id=True)
        _expect_string(key.get("role_id"), f"keys[{index}].role_id", stable_id=True)
        _expect_string(key.get("algorithm"), f"keys[{index}].algorithm")
        pem = _expect_string(key.get("public_key_pem"), f"keys[{index}].public_key_pem")
        if "PRIVATE KEY" in pem.upper():
            raise InputError(f"trust key {key_id} contains private key material")
        if "PUBLIC KEY" not in pem.upper():
            raise InputError(f"trust key {key_id} is not a PEM public key")
        _parse_time(key.get("valid_from"), field_name=f"keys[{index}].valid_from")
        _parse_time(key.get("valid_until"), field_name=f"keys[{index}].valid_until")
        revoked_at = key.get("revoked_at")
        if revoked_at is not None:
            _parse_time(revoked_at, field_name=f"keys[{index}].revoked_at")
        scopes = _expect_mapping(key.get("scopes"), f"keys[{index}].scopes")
        _expect_exact_fields(scopes, TRUST_SCOPE_FIELDS, f"keys[{index}].scopes")
        for scope_name in sorted(TRUST_SCOPE_FIELDS):
            values = _expect_sequence(scopes.get(scope_name), f"keys[{index}].scopes.{scope_name}")
            normalized_values = [_expect_string(v, f"scope {scope_name}") for v in values]
            if len(normalized_values) != len(set(normalized_values)):
                raise InputError(f"trust key {key_id} has duplicate {scope_name}")
        if key_id in revoked_ids and revoked_at is None:
            # The snapshot is authoritative even when the key record was not rewritten.
            key = MappingProxyType({**dict(key), "revoked_at": revocation.get("issued_at")})
        keys[key_id] = key
    return _deep_freeze(bundle), MappingProxyType(keys)


def _required_thresholds(configuration: LoadedConfiguration, profiles: Sequence[str]) -> tuple[dict[str, int], bool]:
    baseline = _expect_mapping(configuration.signing.get("baseline"), "signing.baseline")
    raw = _expect_mapping(baseline.get("required_role_thresholds"), "baseline.required_role_thresholds")
    thresholds: dict[str, int] = {}
    for role_id, value in raw.items():
        if role_id not in configuration.roles:
            raise ConfigurationError(f"baseline threshold references unknown role {role_id!r}")
        if not isinstance(value, int) or value < 1:
            raise ConfigurationError(f"threshold for {role_id} must be a positive integer")
        thresholds[role_id] = value
    offline_required = False
    profile_requirements = configuration.signing.get("profile_requirements", {})
    if not isinstance(profile_requirements, Mapping):
        raise ConfigurationError("profile_requirements must be a table")
    for profile_id in sorted(profiles):
        requirement = profile_requirements.get(profile_id)
        if requirement is None:
            continue
        if not isinstance(requirement, Mapping):
            raise ConfigurationError(f"profile requirement for {profile_id} must be a table")
        required_roles = requirement.get("required_role_thresholds", {})
        if not isinstance(required_roles, Mapping):
            raise ConfigurationError(f"profile {profile_id} required_role_thresholds must be a table")
        for role_id, value in required_roles.items():
            if role_id not in configuration.roles:
                raise ConfigurationError(f"profile {profile_id} references unknown role {role_id!r}")
            if not isinstance(value, int) or value < 1:
                raise ConfigurationError(f"profile {profile_id} threshold for {role_id} must be positive")
            thresholds[role_id] = max(thresholds.get(role_id, 0), value)
        offline_required = offline_required or requirement.get("offline_signature_required") is True
    return thresholds, offline_required


def _scope_contains(values: Sequence[Any], expected: str) -> bool:
    normalized = tuple(str(item) for item in values)
    return expected in normalized or "*" in normalized


def _scope_contains_all(values: Sequence[Any], expected: Iterable[str]) -> bool:
    normalized = set(str(item) for item in values)
    expected_set = set(expected)
    return "*" in normalized or expected_set.issubset(normalized)


def _validate_role_and_scope(
    context: VerificationContext,
    key: Mapping[str, Any],
    statement: Mapping[str, Any],
    subject: Mapping[str, Any],
    configuration: LoadedConfiguration,
    profiles: Sequence[str],
    environment: str,
) -> None:
    role_id = str(statement.get("role_id"))
    role = configuration.roles.get(role_id)
    if role is None:
        context.add(
            "SIGNATURE_ROLE_UNKNOWN",
            f"unknown signature role {role_id!r}",
            authority=str(configuration.paths["roles"]),
        )
        return
    if role.get("role_kind") not in {"signer", "co_signer"}:
        context.add(
            "SIGNATURE_ROLE_NOT_SIGNER",
            f"role {role_id!r} cannot satisfy a signature threshold",
            authority=str(configuration.paths["roles"]),
        )
    if key.get("role_id") != role_id:
        context.add(
            "SIGNATURE_KEY_ROLE_MISMATCH",
            f"key role {key.get('role_id')!r} does not match statement role {role_id!r}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
        )
    artifact_class = str(subject.get("artifact_class"))
    channels = tuple(str(value) for value in subject.get("release_channels", ()))
    purpose = str(statement.get("purpose"))
    if not _scope_contains(tuple(role.get("allowed_artifact_classes", ())), artifact_class):
        context.add(
            "SIGNATURE_ROLE_ARTIFACT_SCOPE_INVALID",
            f"role {role_id!r} does not allow artifact class {artifact_class!r}",
            authority=str(configuration.paths["roles"]),
        )
    if not _scope_contains_all(tuple(role.get("allowed_release_channels", ())), channels):
        context.add(
            "SIGNATURE_ROLE_CHANNEL_SCOPE_INVALID",
            f"role {role_id!r} does not cover all Release Set channels",
            authority=str(configuration.paths["roles"]),
        )
    if not _scope_contains(tuple(role.get("allowed_purposes", ())), purpose):
        context.add(
            "SIGNATURE_ROLE_PURPOSE_SCOPE_INVALID",
            f"role {role_id!r} does not allow purpose {purpose!r}",
            authority=str(configuration.paths["roles"]),
        )
    scopes = _expect_mapping(key.get("scopes"), "trust key.scopes")
    checks = (
        ("artifact_classes", (artifact_class,)),
        ("release_channels", channels),
        ("environments", (environment,)),
        ("profiles", tuple(profiles)),
        ("purposes", (purpose,)),
    )
    for scope_name, expected in checks:
        actual = tuple(scopes.get(scope_name, ()))
        if not _scope_contains_all(actual, expected):
            context.add(
                "SIGNATURE_KEY_SCOPE_INVALID",
                f"key {key.get('key_id')!r} scope {scope_name} does not cover {list(expected)!r}",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
            )


def _verify_crypto(
    context: VerificationContext,
    *,
    key: Mapping[str, Any],
    algorithm: str,
    signature: bytes,
    statement_bytes: bytes,
    configuration: LoadedConfiguration,
) -> None:
    crypto_policy = _expect_mapping(configuration.verification.get("crypto"), "verification.crypto")
    if crypto_policy.get("backend") != "python-cryptography":
        context.add(
            "CRYPTO_BACKEND_UNSUPPORTED",
            f"unsupported configured crypto backend {crypto_policy.get('backend')!r}",
            authority=str(configuration.paths["verification"]),
        )
        return
    accepted = tuple(crypto_policy.get("accepted_algorithms", ()))
    if algorithm not in accepted:
        context.add(
            "SIGNATURE_ALGORITHM_BLOCKED",
            f"algorithm {algorithm!r} is not allowed",
            authority=str(configuration.paths["verification"]),
        )
        return
    if key.get("algorithm") != algorithm:
        context.add(
            "SIGNATURE_ALGORITHM_KEY_MISMATCH",
            f"envelope algorithm {algorithm!r} does not match trusted key algorithm {key.get('algorithm')!r}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
        )
        return
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec, ed25519, padding, rsa
    except ImportError:
        context.add(
            "CRYPTO_BACKEND_UNAVAILABLE",
            "python package 'cryptography' is required by the active verification policy",
            authority=str(configuration.paths["verification"]),
        )
        return
    try:
        public_key = serialization.load_pem_public_key(str(key.get("public_key_pem")).encode("ascii"))
    except (ValueError, TypeError, UnicodeEncodeError) as exc:
        context.add(
            "TRUST_KEY_INVALID",
            f"cannot load public key {key.get('key_id')!r}: {exc}",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
        )
        return
    try:
        if algorithm == "ed25519":
            if not isinstance(public_key, ed25519.Ed25519PublicKey):
                raise TypeError("trusted key is not Ed25519")
            public_key.verify(signature, statement_bytes)
        elif algorithm == "ecdsa-p256-sha256":
            if not isinstance(public_key, ec.EllipticCurvePublicKey):
                raise TypeError("trusted key is not elliptic-curve")
            allowed_curves = tuple(crypto_policy.get("allowed_ec_curves", ()))
            if public_key.curve.name not in allowed_curves:
                raise TypeError(f"curve {public_key.curve.name!r} is not allowed")
            public_key.verify(signature, statement_bytes, ec.ECDSA(hashes.SHA256()))
        elif algorithm == "rsa-pss-sha256":
            if not isinstance(public_key, rsa.RSAPublicKey):
                raise TypeError("trusted key is not RSA")
            minimum_bits = int(crypto_policy.get("minimum_rsa_bits", 3072))
            if public_key.key_size < minimum_bits:
                raise TypeError(f"RSA key size {public_key.key_size} is below {minimum_bits}")
            public_key.verify(
                signature,
                statement_bytes,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=hashes.SHA256().digest_size),
                hashes.SHA256(),
            )
        else:
            raise TypeError(f"unimplemented allowed algorithm {algorithm!r}")
    except InvalidSignature:
        context.add(
            "SIGNATURE_CRYPTOGRAPHICALLY_INVALID",
            f"signature made by key {key.get('key_id')!r} is invalid",
            authority="docs/07-security/03-identity-trust-and-signatures.md",
        )
    except (TypeError, ValueError) as exc:
        context.add(
            "SIGNATURE_KEY_INCOMPATIBLE",
            str(exc),
            authority="docs/07-security/03-identity-trust-and-signatures.md",
        )


def _verify_signature_envelope(
    context: VerificationContext,
    envelope_path: Path,
    release_path: Path,
    release_set: Mapping[str, Any],
    release_digest: str,
    repository_root: Path,
    keys: Mapping[str, Mapping[str, Any]],
    configuration: LoadedConfiguration,
    profiles: Sequence[str],
    channels: Sequence[str],
    environment: str,
    now: datetime,
    maximum_bytes: int,
    minimum_sequence: int,
) -> VerifiedSignature | None:
    initial_error_count = sum(item.severity == "error" for item in context.diagnostics)
    try:
        envelope = _load_json(envelope_path, maximum_bytes)
        envelope = _expect_mapping(envelope, "signature envelope")
        _expect_exact_fields(envelope, SIGNATURE_FIELDS, "signature envelope")
        _reject_private_material(envelope, envelope_path)
        if envelope.get("schema_version") != "1.0":
            raise InputError(f"unsupported signature schema_version: {envelope.get('schema_version')!r}")
        signature_id = _expect_string(envelope.get("signature_id"), "signature_id", stable_id=True)
        statement = _expect_mapping(envelope.get("statement"), "signature statement")
        _expect_exact_fields(statement, STATEMENT_FIELDS, "signature statement")
        subject = _expect_mapping(statement.get("subject"), "signature statement.subject")
        _expect_exact_fields(subject, SUBJECT_FIELDS, "signature statement.subject")
        algorithm = _expect_string(envelope.get("algorithm"), "signature algorithm")
        raw_signature = _expect_string(envelope.get("signature"), "signature")
        try:
            signature_bytes = base64.b64decode(raw_signature, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise InputError(f"signature is not valid base64: {exc}") from exc
        if not signature_bytes:
            raise InputError("signature must not be empty")

        statement_policy = _expect_mapping(configuration.signing.get("statement"), "signing.statement")
        if statement.get("domain") != statement_policy.get("domain"):
            context.add(
                "SIGNATURE_DOMAIN_MISMATCH",
                f"expected domain {statement_policy.get('domain')!r}",
                authority=str(configuration.paths["signing"]),
                path=envelope_path,
                pointer="/statement/domain",
            )
        if statement.get("purpose") != statement_policy.get("purpose"):
            context.add(
                "SIGNATURE_PURPOSE_MISMATCH",
                f"expected purpose {statement_policy.get('purpose')!r}",
                authority=str(configuration.paths["signing"]),
                path=envelope_path,
                pointer="/statement/purpose",
            )
        if statement.get("environment") != environment:
            context.add(
                "SIGNATURE_ENVIRONMENT_MISMATCH",
                f"statement environment {statement.get('environment')!r} does not match requested {environment!r}",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
                path=envelope_path,
                pointer="/statement/environment",
            )
        statement_profiles = statement.get("profiles")
        if not isinstance(statement_profiles, list) or tuple(statement_profiles) != tuple(sorted(profiles)):
            context.add(
                "SIGNATURE_PROFILE_SCOPE_MISMATCH",
                f"statement profiles must be exactly {list(sorted(profiles))!r}",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
                path=envelope_path,
                pointer="/statement/profiles",
            )
        if len(set(statement_profiles or [])) != len(statement_profiles or []):
            context.add(
                "SIGNATURE_PROFILE_SCOPE_DUPLICATE",
                "statement profiles contain duplicates",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
                path=envelope_path,
                pointer="/statement/profiles",
            )

        expected_relative_path = _relative_to(repository_root, release_path)
        if subject.get("path") != expected_relative_path:
            context.add(
                "SIGNATURE_SUBJECT_PATH_MISMATCH",
                f"expected subject path {expected_relative_path!r}",
                authority=str(configuration.paths["signing"]),
                path=envelope_path,
                pointer="/statement/subject/path",
            )
        if subject.get("sha256") != release_digest:
            context.add(
                "SIGNATURE_SUBJECT_DIGEST_MISMATCH",
                f"expected subject sha256 {release_digest}",
                authority="docs/06-lifecycle/12-artifact-verification.md",
                path=envelope_path,
                pointer="/statement/subject/sha256",
            )
        expected_subject = {
            "artifact_class": release_set.get("artifact_class"),
            "release_set_id": release_set.get("release_set_id"),
            "version": release_set.get("version"),
        }
        for field_name, expected_value in expected_subject.items():
            if subject.get(field_name) != expected_value:
                context.add(
                    "SIGNATURE_SUBJECT_IDENTITY_MISMATCH",
                    f"subject {field_name} must be {expected_value!r}",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    path=envelope_path,
                    pointer=f"/statement/subject/{field_name}",
                )
        if subject.get("release_channels") != list(sorted(channels)):
            context.add(
                "SIGNATURE_CHANNEL_SCOPE_MISMATCH",
                f"subject release_channels must be exactly {list(sorted(channels))!r}",
                authority="docs/contracts/release-channels.contract.json",
                path=envelope_path,
                pointer="/statement/subject/release_channels",
            )

        role_id = _expect_string(statement.get("role_id"), "statement.role_id", stable_id=True)
        signer_id = _expect_string(statement.get("signer_id"), "statement.signer_id", stable_id=True)
        key_id = _expect_string(statement.get("key_id"), "statement.key_id", stable_id=True)
        key = keys.get(key_id)
        if key is None:
            context.add(
                "SIGNATURE_KEY_UNKNOWN",
                f"key {key_id!r} is not in the digest-pinned trust bundle",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
                path=envelope_path,
            )
        else:
            if key.get("signer_id") != signer_id:
                context.add(
                    "SIGNATURE_SIGNER_KEY_MISMATCH",
                    f"key {key_id!r} belongs to signer {key.get('signer_id')!r}, not {signer_id!r}",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    path=envelope_path,
                )
            valid_from = _parse_time(key.get("valid_from"), field_name=f"key {key_id}.valid_from")
            valid_until = _parse_time(key.get("valid_until"), field_name=f"key {key_id}.valid_until")
            issued_at = _parse_time(statement.get("issued_at"), field_name="statement.issued_at")
            expires_at = _parse_time(statement.get("expires_at"), field_name="statement.expires_at")
            if not (valid_from <= issued_at < valid_until):
                context.add(
                    "SIGNATURE_KEY_NOT_VALID_AT_SIGNING",
                    "key was not valid at statement issuance time",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    path=envelope_path,
                )
            if issued_at > now or expires_at <= now or expires_at <= issued_at:
                context.add(
                    "SIGNATURE_NOT_CURRENT",
                    "signature statement is not currently valid",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    path=envelope_path,
                )
            revoked_at = key.get("revoked_at")
            if revoked_at is not None:
                context.add(
                    "SIGNATURE_KEY_REVOKED",
                    f"key {key_id!r} is revoked at {revoked_at}",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    path=envelope_path,
                )
            _validate_role_and_scope(
                context,
                key,
                statement,
                subject,
                configuration,
                profiles,
                environment,
            )

        sequence = statement.get("sequence")
        if not isinstance(sequence, int) or sequence < 1:
            context.add(
                "SIGNATURE_SEQUENCE_INVALID",
                "statement.sequence must be a positive integer",
                authority=str(configuration.paths["signing"]),
                path=envelope_path,
                pointer="/statement/sequence",
            )
        elif sequence <= minimum_sequence:
            context.add(
                "SIGNATURE_SEQUENCE_REPLAY",
                f"statement sequence {sequence} is not greater than retained sequence {minimum_sequence}",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
                path=envelope_path,
                pointer="/statement/sequence",
            )
        approval_refs = statement.get("approval_refs")
        if not isinstance(approval_refs, list) or not approval_refs:
            context.add(
                "SIGNATURE_APPROVAL_REFS_MISSING",
                "statement.approval_refs must be non-empty",
                authority="docs/06-lifecycle/18-sbom-provenance-and-signing.md",
                path=envelope_path,
                pointer="/statement/approval_refs",
            )
        else:
            if len(approval_refs) != len(set(approval_refs)) or approval_refs != sorted(approval_refs):
                context.add(
                    "SIGNATURE_APPROVAL_REFS_NONCANONICAL",
                    "statement.approval_refs must be unique and sorted",
                    authority=str(configuration.paths["signing"]),
                    path=envelope_path,
                    pointer="/statement/approval_refs",
                )
            release_approvals = set(
                release_set.get("authority", {}).get("approval_refs", [])
                if isinstance(release_set.get("authority"), Mapping)
                else []
            )
            if not set(approval_refs).issubset(release_approvals):
                context.add(
                    "SIGNATURE_APPROVAL_REFS_UNBOUND",
                    "signature statement references approvals absent from the Release Set authority block",
                    authority="docs/06-lifecycle/18-sbom-provenance-and-signing.md",
                    path=envelope_path,
                    pointer="/statement/approval_refs",
                )
        mode = statement.get("mode")
        if mode not in {"online", "offline"}:
            context.add(
                "SIGNATURE_MODE_INVALID",
                "statement.mode must be 'online' or 'offline'",
                authority=str(configuration.paths["offline"]),
                path=envelope_path,
                pointer="/statement/mode",
            )
        if key is not None:
            custody = key.get("custody")
            allowed_custody = {
                "external_signing_service",
                "remote_signing_service",
                "hardware_security_module",
                "offline_custody",
            }
            if custody not in allowed_custody:
                context.add(
                    "SIGNATURE_KEY_CUSTODY_INVALID",
                    f"unapproved key custody class {custody!r}",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    path=envelope_path,
                )
            if mode == "offline" and custody != "offline_custody":
                context.add(
                    "OFFLINE_SIGNATURE_CUSTODY_INVALID",
                    "offline signatures require an offline_custody key",
                    authority=str(configuration.paths["offline"]),
                    path=envelope_path,
                )
            if role_id == "offline_release_authority" and mode != "offline":
                context.add(
                    "OFFLINE_ROLE_MODE_INVALID",
                    "offline_release_authority signatures must use mode='offline'",
                    authority=str(configuration.paths["offline"]),
                    path=envelope_path,
                )

        statement_bytes = _canonical_json(dict(statement))
        statement_digest = _sha256_bytes(statement_bytes)
        threshold_context = {
            "domain": statement.get("domain"),
            "subject": dict(subject),
            "purpose": statement.get("purpose"),
            "environment": statement.get("environment"),
            "profiles": list(statement.get("profiles", [])),
            "approval_refs": list(statement.get("approval_refs", [])),
            "sequence": statement.get("sequence"),
        }
        threshold_context_digest = _sha256_bytes(_canonical_json(threshold_context))
        if key is not None:
            _verify_crypto(
                context,
                key=key,
                algorithm=algorithm,
                signature=signature_bytes,
                statement_bytes=statement_bytes,
                configuration=configuration,
            )
    except (InputError, ConfigurationError) as exc:
        context.add(
            "SIGNATURE_ENVELOPE_INVALID",
            str(exc),
            authority="docs/07-security/03-identity-trust-and-signatures.md",
            path=envelope_path,
        )
        return None

    final_error_count = sum(item.severity == "error" for item in context.diagnostics)
    if final_error_count != initial_error_count:
        return None
    return VerifiedSignature(
        signature_id=signature_id,
        role_id=role_id,
        signer_id=signer_id,
        key_id=key_id,
        algorithm=algorithm,
        statement_digest=statement_digest,
        threshold_context_digest=threshold_context_digest,
        mode=str(mode),
    )


def _resolve_signature_paths(
    repository_root: Path,
    release_set: Mapping[str, Any],
    requested: Sequence[Path],
) -> tuple[Path, ...]:
    values: list[Path | str] = list(requested)
    if not values:
        signature = release_set.get("signature")
        if isinstance(signature, Mapping):
            signature_ref = signature.get("signature_artifact_ref")
            if isinstance(signature_ref, str) and signature_ref:
                values.append(signature_ref)
    if not values:
        raise InputError("no signature envelope supplied and release set has no signature_artifact_ref")
    resolved = tuple(sorted({_resolve_under(repository_root, item) for item in values}, key=lambda path: path.as_posix()))
    return resolved


def _validate_signature_set(
    context: VerificationContext,
    verified: Sequence[VerifiedSignature],
    thresholds: Mapping[str, int],
    offline_required: bool,
    configuration: LoadedConfiguration,
) -> None:
    signature_ids = [item.signature_id for item in verified]
    key_ids = [item.key_id for item in verified]
    signer_ids = [item.signer_id for item in verified]
    if len(signature_ids) != len(set(signature_ids)):
        context.add(
            "SIGNATURE_ID_DUPLICATE",
            "signature identifiers must be unique",
            authority=str(configuration.paths["signing"]),
        )
    baseline = _expect_mapping(configuration.signing.get("baseline"), "signing.baseline")
    if baseline.get("require_distinct_key_ids") is True and len(key_ids) != len(set(key_ids)):
        context.add(
            "SIGNATURE_KEY_REUSE",
            "one key cannot count more than once toward a threshold",
            authority=str(configuration.paths["signing"]),
        )
    if baseline.get("require_distinct_signer_ids") is True and len(signer_ids) != len(set(signer_ids)):
        context.add(
            "SIGNATURE_SIGNER_REUSE",
            "one signer cannot count more than once toward a threshold",
            authority=str(configuration.paths["signing"]),
        )
    if baseline.get("require_all_signatures_over_identical_statement") is True:
        digests = {item.threshold_context_digest for item in verified}
        if len(digests) > 1:
            context.add(
                "SIGNATURE_STATEMENT_DIVERGENCE",
                "all threshold signatures must cover the identical canonical statement",
                authority="docs/07-security/03-identity-trust-and-signatures.md",
            )
    counts = Counter(item.role_id for item in verified)
    for role_id, required in sorted(thresholds.items()):
        actual = counts.get(role_id, 0)
        if actual < required:
            context.add(
                "SIGNATURE_THRESHOLD_NOT_MET",
                f"role {role_id!r} requires {required} distinct signature(s), got {actual}",
                authority=str(configuration.paths["signing"]),
            )
    if offline_required and not any(item.mode == "offline" for item in verified):
        context.add(
            "OFFLINE_SIGNATURE_REQUIRED",
            "the effective profile policy requires at least one offline signature",
            authority=str(configuration.paths["offline"]),
        )


def verify_release(args: argparse.Namespace) -> tuple[int, dict[str, Any]]:
    repository_root = Path(args.repository_root).resolve(strict=True)
    now = datetime.now(timezone.utc)
    context = VerificationContext()
    if args.minimum_sequence < 0 or args.minimum_trust_epoch < 0 or args.minimum_revocation_sequence < 0:
        return 2, {
            "format_version": "1.0",
            "tool": {"id": TOOL_ID, "version": TOOL_VERSION},
            "result": "blocked",
            "diagnostics": [
                Diagnostic(
                    severity="error",
                    code="RETAINED_STATE_INVALID",
                    authority="release/verification/verification-policy.toml",
                    message="minimum sequence and epoch inputs must be non-negative integers",
                ).to_dict()
            ],
        }
    try:
        configuration = load_configuration(
            repository_root,
            Path(args.policy),
            Path(args.signing_policy) if args.signing_policy else None,
            Path(args.roles) if args.roles else None,
            Path(args.offline_policy) if args.offline_policy else None,
        )
    except (ConfigurationError, InputError) as exc:
        return 2, {
            "format_version": "1.0",
            "tool": {"id": TOOL_ID, "version": TOOL_VERSION},
            "result": "blocked",
            "diagnostics": [
                Diagnostic(
                    severity="error",
                    code="VERIFIER_CONFIGURATION_INVALID",
                    authority="release/verification/verification-policy.toml",
                    message=str(exc),
                ).to_dict()
            ],
        }

    input_policy = _expect_mapping(configuration.verification.get("input"), "verification.input")
    maximum_bytes = int(input_policy.get("maximum_json_bytes", 16 * 1024 * 1024))
    maximum_signatures = int(input_policy.get("maximum_signature_count", 32))
    try:
        release_path = _resolve_under(repository_root, args.release_set)
        release_set_raw = _load_json(release_path, maximum_bytes)
        release_set = _expect_mapping(release_set_raw, "release set")
        _reject_private_material(release_set, release_path)
        release_digest = _sha256_file(release_path)
        _schema_validate_release_set(context, release_set, repository_root, configuration)
        profiles, channels = _semantic_validate_release_set(context, release_set, configuration, now)
        environment = _expect_string(args.environment, "--environment")
        target_scope = release_set.get("target_scope")
        if isinstance(target_scope, Mapping):
            labels = target_scope.get("environment_labels")
            if isinstance(labels, list) and labels and environment not in labels:
                context.add(
                    "RELEASE_SET_ENVIRONMENT_SCOPE_MISMATCH",
                    f"requested environment {environment!r} is absent from target_scope.environment_labels",
                    authority="docs/07-security/03-identity-trust-and-signatures.md",
                    pointer="/target_scope/environment_labels",
                )
        trust_path = _resolve_under(repository_root, args.trust_bundle)
        trust_bundle, trust_keys = _load_trust_bundle(
            context,
            trust_path,
            args.trust_bundle_sha256,
            configuration,
            now,
            maximum_bytes,
            args.minimum_trust_epoch,
            args.minimum_revocation_sequence,
        )
        signature_paths = _resolve_signature_paths(repository_root, release_set, tuple(Path(v) for v in args.signature))
        if len(signature_paths) > maximum_signatures:
            raise InputError(f"more than {maximum_signatures} signature envelopes supplied")
        thresholds, offline_required = _required_thresholds(configuration, profiles)
        if args.offline:
            offline_required = True
        if offline_required and trust_bundle.get("offline_capable") is not True:
            context.add(
                "TRUST_BUNDLE_NOT_OFFLINE_CAPABLE",
                "effective policy requires an offline-capable trust bundle",
                authority=str(configuration.paths["offline"]),
                path=trust_path,
            )
        verified: list[VerifiedSignature] = []
        for signature_path in signature_paths:
            item = _verify_signature_envelope(
                context,
                signature_path,
                release_path,
                release_set,
                release_digest,
                repository_root,
                trust_keys,
                configuration,
                profiles,
                channels,
                environment,
                now,
                maximum_bytes,
                args.minimum_sequence,
            )
            if item is not None:
                verified.append(item)
        _validate_signature_set(context, verified, thresholds, offline_required, configuration)
    except (InputError, ConfigurationError, OSError) as exc:
        context.add(
            "VERIFICATION_INPUT_BLOCKED",
            str(exc),
            authority=str(configuration.paths["verification"]),
        )
        release_path = Path(args.release_set)
        release_digest = ""
        profiles = ()
        channels = ()
        environment = str(args.environment)
        thresholds = {}
        verified = []

    result = "pass" if not context.failed else "blocked"
    displayed_diagnostics = []
    for diagnostic in context.sorted():
        item = diagnostic.to_dict()
        item["authority"] = _display_path(repository_root, item["authority"])
        if "path" in item:
            item["path"] = _display_path(repository_root, item["path"])
        displayed_diagnostics.append(item)
    subject_path = _display_path(repository_root, release_path)
    report = {
        "format_version": "1.0",
        "tool": {"id": TOOL_ID, "version": TOOL_VERSION},
        "result": result,
        "verified_at": now.isoformat().replace("+00:00", "Z"),
        "subject": {
            "path": subject_path,
            "sha256": release_digest,
            "profiles": list(profiles),
            "release_channels": list(channels),
            "environment": environment,
        },
        "policy": {
            "verification": _display_path(repository_root, configuration.paths["verification"]),
            "signing": _display_path(repository_root, configuration.paths["signing"]),
            "roles": _display_path(repository_root, configuration.paths["roles"]),
            "offline": _display_path(repository_root, configuration.paths["offline"]),
            "required_role_thresholds": dict(sorted(thresholds.items())),
        },
        "verified_signatures": [
            {
                "signature_id": item.signature_id,
                "role_id": item.role_id,
                "signer_id": item.signer_id,
                "key_id": item.key_id,
                "algorithm": item.algorithm,
                "statement_sha256": item.statement_digest,
                "threshold_context_sha256": item.threshold_context_digest,
                "mode": item.mode,
            }
            for item in sorted(verified, key=lambda signature: signature.signature_id)
        ],
        "retained_state": {
            "minimum_release_sequence": args.minimum_sequence,
            "minimum_trust_epoch": args.minimum_trust_epoch,
            "minimum_revocation_sequence": args.minimum_revocation_sequence,
        },
        "diagnostics": displayed_diagnostics,
    }
    return (0 if result == "pass" else 1), report


def _render_text(report: Mapping[str, Any]) -> str:
    lines = [
        f"{TOOL_ID} {report.get('tool', {}).get('version', TOOL_VERSION)}",
        f"result: {report.get('result')}",
    ]
    subject = report.get("subject")
    if isinstance(subject, Mapping):
        if subject.get("path"):
            lines.append(f"subject: {subject.get('path')}")
        if subject.get("sha256"):
            lines.append(f"subject-sha256: {subject.get('sha256')}")
        lines.append(f"profiles: {', '.join(subject.get('profiles', [])) or '-'}")
        lines.append(f"environment: {subject.get('environment', '-')}")
    signatures = report.get("verified_signatures")
    if isinstance(signatures, list):
        lines.append(f"verified-signatures: {len(signatures)}")
        for item in signatures:
            lines.append(
                "  "
                + f"{item.get('signature_id')} role={item.get('role_id')} "
                + f"signer={item.get('signer_id')} key={item.get('key_id')} "
                + f"algorithm={item.get('algorithm')} mode={item.get('mode')}"
            )
    diagnostics = report.get("diagnostics")
    if isinstance(diagnostics, list) and diagnostics:
        lines.append("diagnostics:")
        for item in diagnostics:
            location = ""
            if item.get("path"):
                location += f" path={item.get('path')}"
            if item.get("pointer"):
                location += f" pointer={item.get('pointer')}"
            lines.append(
                f"  [{str(item.get('severity')).upper()}] {item.get('code')}: "
                f"{item.get('message')} (authority={item.get('authority')}{location})"
            )
    return "\n".join(lines) + "\n"


def _write_report(path: Path, payload: str) -> None:
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    temporary = parent / f".{path.name}.{os.getpid()}.tmp"
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except OSError as exc:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            None
        raise InputError(f"cannot write report {path}: {exc}") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="verify-release.py",
        description="Verify a local kOA Release Set with detached, scoped signatures.",
    )
    parser.add_argument("release_set", help="repository-confined path to the Release Set JSON")
    parser.add_argument(
        "--repository-root",
        default=".",
        help="repository root used to confine all references (default: current directory)",
    )
    parser.add_argument(
        "--policy",
        default="release/verification/verification-policy.toml",
        help="verification policy path",
    )
    parser.add_argument("--signing-policy", help="explicit signing policy override")
    parser.add_argument("--roles", help="explicit roles registry override")
    parser.add_argument("--offline-policy", help="explicit offline policy override")
    parser.add_argument(
        "--signature",
        action="append",
        default=[],
        help="detached signature envelope; repeat for threshold signatures",
    )
    parser.add_argument("--trust-bundle", required=True, help="digest-pinned public trust bundle JSON")
    parser.add_argument(
        "--trust-bundle-sha256",
        required=True,
        help="lowercase SHA-256 digest of the exact trust bundle bytes",
    )
    parser.add_argument("--environment", required=True, help="exact target environment scope")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="require at least one offline-mode signature in addition to profile policy",
    )
    parser.add_argument(
        "--minimum-sequence",
        required=True,
        type=int,
        help="last accepted release-signature sequence; every supplied signature must be greater",
    )
    parser.add_argument(
        "--minimum-trust-epoch",
        required=True,
        type=int,
        help="minimum retained trust epoch used to reject trust-bundle downgrade",
    )
    parser.add_argument(
        "--minimum-revocation-sequence",
        required=True,
        type=int,
        help="minimum retained revocation sequence used to reject stale snapshots",
    )
    parser.add_argument("--json", action="store_true", help="emit deterministic JSON")
    parser.add_argument("--output", help="atomically write the same report to this path")
    parser.add_argument("--version", action="version", version=f"%(prog)s {TOOL_VERSION}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, report = verify_release(args)
        payload = (
            json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            if args.json
            else _render_text(report)
        )
        if args.output:
            _write_report(Path(args.output), payload)
        sys.stdout.write(payload)
        return exit_code
    except (InputError, ConfigurationError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
