"""Stage and validate a complete governance policy bundle without activation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

from ..ports.audit_sink import AuditEvidence, AuditSink
from ..ports.bundle_store import (
    BundleStore,
    LifecycleSupportStatus,
    PolicySetRecord,
    PolicySetState,
)
from ..ports.clock import Clock
from ..ports.signature_verifier import SignatureStatus, SignatureVerifier

_REQUIRED_TOP_LEVEL = frozenset(
    {
        "$schema", "artifact_id", "artifact_type", "artifact_class", "release_channel",
        "version", "status", "language", "issued_at", "authority_ref", "decisions_ref",
        "system_ref", "profiles_ref", "components_ref", "integrations_ref",
        "artifact_classes_ref", "release_channels_ref", "requirements_ref", "locks_ref",
        "traceability_ref", "exceptions_ref", "test_catalog_ref", "evidence_ref", "manifest",
        "scope", "runtime", "facts", "modules", "decision_contract", "tests", "governance",
        "compatibility", "activation", "offline", "ai_boundary", "integration_controls",
        "security", "provenance", "lifecycle", "signatures",
    }
)


class StageOutcome(StrEnum):
    STAGED = "staged"
    BLOCKED = "blocked"


@dataclass(frozen=True, slots=True)
class LoadBundleCommand:
    request_id: str
    correlation_id: str
    bundle: Mapping[str, Any]
    target_profiles: tuple[str, ...]
    target_components: tuple[str, ...]
    expected_current_policy_set: str | None
    proposed_policy_set: str
    release_set_ref: str
    authority_version: str
    audit_required: bool = True


@dataclass(frozen=True, slots=True)
class LoadBundleResult:
    outcome: StageOutcome
    policy_set_ref: str
    bundle_ref: str | None
    staged_record: PolicySetRecord | None
    validation_evidence_refs: tuple[str, ...]
    reason_codes: tuple[str, ...] = ()


def _aware(value: datetime, name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")
    return value


def _jsonable(value: Any) -> Any:
    if isinstance(value, datetime):
        return _aware(value, "datetime").isoformat()
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, (set, frozenset)):
        return sorted((_jsonable(v) for v in value), key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"unsupported bundle value: {type(value).__name__}")


def _fingerprint(bundle: Mapping[str, Any]) -> str:
    encoded = json.dumps(_jsonable(bundle), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(encoded.encode()).hexdigest()


def _nonempty_strings(values: Sequence[Any]) -> tuple[str, ...] | None:
    if not isinstance(values, (list, tuple)) or not values:
        return None
    normalized = tuple(str(v).strip() for v in values)
    return normalized if all(normalized) and len(set(normalized)) == len(normalized) else None


def _validate_bundle(command: LoadBundleCommand) -> tuple[str, ...]:
    bundle = command.bundle
    reasons: list[str] = []
    missing = sorted(_REQUIRED_TOP_LEVEL - set(bundle))
    reasons.extend(f"missing:{name}" for name in missing)
    unknown = sorted(set(bundle) - _REQUIRED_TOP_LEVEL)
    reasons.extend(f"undeclared:{name}" for name in unknown)
    if bundle.get("artifact_type") != "governance_policy_bundle":
        reasons.append("artifact_type_invalid")
    if bundle.get("artifact_class") != "policy_bundle":
        reasons.append("artifact_class_invalid")
    if bundle.get("release_channel") != "governance":
        reasons.append("release_channel_invalid")
    if bundle.get("status") not in {"candidate", "validated", "staged"}:
        reasons.append("candidate_status_invalid")

    scope = bundle.get("scope")
    if not isinstance(scope, Mapping):
        reasons.append("scope_invalid")
    else:
        profiles = _nonempty_strings(scope.get("profiles", ()))
        components = _nonempty_strings(scope.get("components", ()))
        if profiles is None or not set(command.target_profiles) <= set(profiles):
            reasons.append("target_profile_mismatch")
        if components is None or not set(command.target_components) <= set(components):
            reasons.append("target_component_mismatch")

    runtime = bundle.get("runtime")
    if not isinstance(runtime, Mapping):
        reasons.append("runtime_invalid")
    else:
        if runtime.get("component_id") != "governance-policy-runtime":
            reasons.append("runtime_component_invalid")
        if runtime.get("deterministic") is not True or runtime.get("side_effect_free") is not True:
            reasons.append("runtime_not_deterministic_and_side_effect_free")
        if not str(runtime.get("minimum_version", "")).strip():
            reasons.append("runtime_minimum_version_missing")

    activation = bundle.get("activation")
    if not isinstance(activation, Mapping):
        reasons.append("activation_invalid")
    else:
        expected = {
            "mode": "atomic",
            "partial_activation_permitted": False,
            "staging_required": True,
            "validation_before_activation": True,
            "last_known_good_required": True,
            "receipt_required": True,
        }
        for key, value in expected.items():
            if activation.get(key) != value:
                reasons.append(f"activation_contract_invalid:{key}")
        if not activation.get("pre_activation_checks") or not activation.get("health_gates"):
            reasons.append("activation_checks_missing")
        if not isinstance(activation.get("rollback"), Mapping):
            reasons.append("rollback_plan_missing")

    tests = bundle.get("tests")
    if not isinstance(tests, Mapping):
        reasons.append("tests_invalid")
    else:
        if not tests.get("required_categories") or not tests.get("vectors"):
            reasons.append("test_plan_incomplete")
        summary = tests.get("execution_summary")
        if not isinstance(summary, Mapping) or summary.get("result") not in {"passed", "pass"}:
            reasons.append("required_tests_not_passed")

    provenance = bundle.get("provenance")
    if not isinstance(provenance, Mapping):
        reasons.append("provenance_invalid")
    else:
        for key in ("producer", "source_revision", "toolchain_ref", "source_refs", "test_evidence_refs", "approval_evidence_refs"):
            if not provenance.get(key):
                reasons.append(f"provenance_missing:{key}")
        if provenance.get("reproducibility") not in {"reproducible", "fully_attributable"}:
            reasons.append("provenance_not_reproducible")

    lifecycle = bundle.get("lifecycle")
    if not isinstance(lifecycle, Mapping):
        reasons.append("lifecycle_invalid")
    else:
        if lifecycle.get("support_status") not in {item.value for item in LifecycleSupportStatus}:
            reasons.append("support_status_invalid")
        if lifecycle.get("rollback_eligibility") not in {"eligible", "eligible_with_validation", "not_eligible_use_forward_repair"}:
            reasons.append("rollback_eligibility_invalid")
        if lifecycle.get("forward_repair_supported") is not True:
            reasons.append("forward_repair_not_supported")

    compatibility = bundle.get("compatibility")
    if not isinstance(compatibility, Mapping):
        reasons.append("compatibility_invalid")
    else:
        for key in ("release_channel_constraints", "profile_rules", "component_contract_refs", "required_validation_refs"):
            if not compatibility.get(key):
                reasons.append(f"compatibility_missing:{key}")

    signatures = bundle.get("signatures")
    if not isinstance(signatures, list) or not signatures:
        reasons.append("signatures_missing")
    return tuple(sorted(set(reasons)))


class LoadBundleHandler:
    """Validate and stage one complete candidate without changing active authority."""

    def __init__(self, *, store: BundleStore, verifier: SignatureVerifier, audit: AuditSink, clock: Clock) -> None:
        self._store = store
        self._verifier = verifier
        self._audit = audit
        self._clock = clock

    def execute(self, command: LoadBundleCommand) -> LoadBundleResult:
        now = _aware(self._clock.now(), "clock.now()")
        if not command.request_id.strip() or not command.correlation_id.strip():
            raise ValueError("request_id and correlation_id are required")
        if not command.proposed_policy_set.strip() or not command.release_set_ref.strip() or not command.authority_version.strip():
            raise ValueError("proposed_policy_set, release_set_ref, and authority_version are required")
        if not command.target_profiles or not command.target_components:
            raise ValueError("target_profiles and target_components are required")

        active = self._store.get_active_policy_set()
        active_ref = active.policy_set_ref if active else None
        if active_ref != command.expected_current_policy_set:
            return LoadBundleResult(
                StageOutcome.BLOCKED,
                command.proposed_policy_set,
                None,
                None,
                (),
                ("GOV_POLICY_STALE:expected_current_policy_set_mismatch",),
            )

        reasons = _validate_bundle(command)
        if reasons:
            return LoadBundleResult(StageOutcome.BLOCKED, command.proposed_policy_set, None, None, (), reasons)

        verification = self._verifier.verify_policy_bundle(command.bundle, at=now)
        if verification.status is not SignatureStatus.VERIFIED:
            reasons = verification.reason_codes or ("signature_or_provenance_verification_failed",)
            return LoadBundleResult(
                StageOutcome.BLOCKED,
                command.proposed_policy_set,
                str(command.bundle.get("artifact_id")) if command.bundle.get("artifact_id") else None,
                None,
                verification.evidence_refs,
                tuple(f"GOV_POLICY_INCOMPATIBLE:{reason}" for reason in reasons),
            )

        if command.audit_required and not self._audit.is_available():
            return LoadBundleResult(
                StageOutcome.BLOCKED,
                command.proposed_policy_set,
                str(command.bundle["artifact_id"]),
                None,
                verification.evidence_refs,
                ("GOV_AUDIT_UNAVAILABLE",),
            )

        bundle_ref = str(command.bundle["artifact_id"])
        lifecycle = command.bundle["lifecycle"]
        runtime = command.bundle["runtime"]
        evidence_id = "policy-stage-" + sha256(f"{command.request_id}\0{bundle_ref}".encode()).hexdigest()
        audit_ref: str | None = None
        if self._audit.is_available():
            submission = self._audit.submit(
                AuditEvidence(
                    evidence_id=evidence_id,
                    event_type="policy_bundle_validated",
                    correlation_id=command.correlation_id,
                    occurred_at=now,
                    subject_refs=(bundle_ref, command.proposed_policy_set),
                    payload={
                        "bundle_ref": bundle_ref,
                        "candidate_policy_set_ref": command.proposed_policy_set,
                        "release_set_ref": command.release_set_ref,
                        "target_profiles": command.target_profiles,
                        "target_components": command.target_components,
                        "semantic_fingerprint": _fingerprint(command.bundle),
                    },
                    evidence_refs=verification.evidence_refs,
                )
            )
            if command.audit_required and not submission.retained:
                return LoadBundleResult(
                    StageOutcome.BLOCKED,
                    command.proposed_policy_set,
                    bundle_ref,
                    None,
                    verification.evidence_refs,
                    ("GOV_AUDIT_UNAVAILABLE:stage_evidence_rejected",),
                )
            audit_ref = submission.evidence_ref

        validation_refs = tuple(dict.fromkeys(verification.evidence_refs + ((audit_ref,) if audit_ref else ())))
        record = PolicySetRecord(
            bundle_ref=bundle_ref,
            policy_set_ref=command.proposed_policy_set,
            authority_version=command.authority_version,
            release_set_ref=command.release_set_ref,
            version=str(command.bundle["version"]),
            evaluator_version=str(runtime["minimum_version"]),
            target_profiles=tuple(command.target_profiles),
            target_components=tuple(command.target_components),
            semantic_fingerprint=_fingerprint(command.bundle),
            state=PolicySetState.VALIDATED,
            support_status=LifecycleSupportStatus(str(lifecycle["support_status"])),
            compatible=True,
            validated_at=now,
            validation_evidence_refs=validation_refs,
            signer_refs=verification.signer_refs,
            previous_policy_set_ref=active_ref,
        )
        staged = self._store.stage_validated_policy_set(record, bundle=command.bundle)
        if staged.state not in {PolicySetState.STAGED, PolicySetState.VALIDATED}:
            return LoadBundleResult(
                StageOutcome.BLOCKED,
                command.proposed_policy_set,
                bundle_ref,
                staged,
                validation_refs,
                ("GOV_ACTIVATION_FAILED:store_did_not_preserve_validated_stage",),
            )
        return LoadBundleResult(StageOutcome.STAGED, command.proposed_policy_set, bundle_ref, staged, validation_refs)
