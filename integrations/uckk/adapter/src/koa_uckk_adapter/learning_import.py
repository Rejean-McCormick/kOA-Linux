"""Governed directional ``import_from_uckk`` workflow.

The workflow is deliberately not a synchronizer.  It processes one explicit
selection, places every retrieved package in quarantine before verification,
and calls the public Mediatheque acceptance interface only after verification
and a current local policy decision.  Remote updates are offered as candidates
and never overwrite local records automatically.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from hashlib import sha256
import json
import re
from types import MappingProxyType
from typing import Any, Mapping, Protocol, Sequence

from .package_verification import (
    PackageVerifier,
    TransportKind,
    VerificationDisposition,
    VerificationReport,
)

_RECEIPT_SCHEMA = (
    "https://schemas.koa.local/artifact-contracts/uckk-import-receipt.schema.json"
)
_PACKAGE_ID = re.compile(r"^uckk_learning_package_[A-Za-z0-9][A-Za-z0-9._-]*$")
_LOCAL_RECORD_ID = re.compile(r"^koa_media_[A-Za-z0-9][A-Za-z0-9._-]*$")
_LOCAL_VERSION_ID = re.compile(r"^koa_media_version_[A-Za-z0-9][A-Za-z0-9._-]*$")
_ALLOWED_SELECTIONS = frozenset(
    {"course", "learning_path", "instruction_collection", "manual", "resource_collection"}
)


class ImportAction(StrEnum):
    VALIDATE_ONLY = "validate_only"
    REQUEST_ACCEPTANCE = "request_acceptance"
    OFFER_UPDATE_CANDIDATE = "offer_update_candidate"


class PolicyOutcome(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    REVIEW = "review"


class ImportWorkflowError(RuntimeError):
    """Stable fail-closed import error."""

    _ALLOWED_CODES = frozenset(
        {
            "DEPENDENCY_UNAVAILABLE",
            "ENDPOINT_NOT_ALLOWLISTED",
            "EXPLICIT_SELECTION_REQUIRED",
            "IDEMPOTENCY_CONFLICT",
            "INVALID_IMPORT_REQUEST",
            "INVALID_LOCAL_ACCEPTANCE",
            "PACKAGE_ID_MISMATCH",
            "REMOTE_RETRIEVAL_FAILED",
            "REMOTE_RESPONSE_INVALID",
        }
    )

    def __init__(self, code: str, message: str) -> None:
        if code not in self._ALLOWED_CODES:
            raise ValueError(f"undeclared import workflow error code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class ImportRequest:
    request_id: str
    package_id: str
    idempotency_key: str
    correlation_id: str
    actor_ref: str
    authority_domain_id: str
    endpoint_id: str
    selection_type: str
    source_object_refs: tuple[str, ...]
    source_version_refs: tuple[str, ...] = ()
    action: ImportAction = ImportAction.VALIDATE_ONLY

    def __post_init__(self) -> None:
        for name in (
            "request_id",
            "idempotency_key",
            "correlation_id",
            "actor_ref",
            "authority_domain_id",
            "endpoint_id",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.package_id, str) or not _PACKAGE_ID.fullmatch(self.package_id):
            raise ValueError("package_id must be a canonical UCKK learning package id")
        if self.selection_type not in _ALLOWED_SELECTIONS:
            raise ValueError("selection_type is not supported by the import contract")
        object.__setattr__(
            self,
            "source_object_refs",
            _unique_texts(self.source_object_refs, "source_object_refs", required=True),
        )
        object.__setattr__(
            self,
            "source_version_refs",
            _unique_texts(self.source_version_refs, "source_version_refs", required=False),
        )
        if not isinstance(self.action, ImportAction):
            object.__setattr__(self, "action", ImportAction(self.action))

    def selection_payload(self) -> Mapping[str, Any]:
        return MappingProxyType(
            {
                "selection_type": self.selection_type,
                "source_object_refs": list(self.source_object_refs),
                "source_version_refs": list(self.source_version_refs),
                "requested_by_ref": self.actor_ref,
            }
        )


@dataclass(frozen=True, slots=True)
class ImportPolicy:
    allowed_endpoint_ids: tuple[str, ...]
    maximum_resource_count: int = 10_000

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "allowed_endpoint_ids",
            _unique_texts(self.allowed_endpoint_ids, "allowed_endpoint_ids", required=True),
        )
        if not 1 <= self.maximum_resource_count <= 1_000_000:
            raise ValueError("maximum_resource_count must be in [1, 1000000]")


@dataclass(frozen=True, slots=True)
class LocalPolicyDecision:
    outcome: PolicyOutcome
    decision_ref: str
    reason_code: str
    evidence_refs: tuple[str, ...] = ()
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, PolicyOutcome):
            object.__setattr__(self, "outcome", PolicyOutcome(self.outcome))
        for name in ("decision_ref", "reason_code"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        object.__setattr__(
            self,
            "evidence_refs",
            _unique_texts(self.evidence_refs, "evidence_refs", required=False),
        )
        if self.expires_at is not None:
            object.__setattr__(self, "expires_at", _utc(self.expires_at))

    def is_current_at(self, value: datetime) -> bool:
        return self.expires_at is None or _utc(value) < self.expires_at


class DirectionalImportClientPort(Protocol):
    def execute(
        self,
        operation: str,
        payload: Mapping[str, Any],
        *,
        correlation_id: str,
        idempotency_key: str,
        authority_domain: str = "koa_linux",
        tenant_id: str | None = None,
    ) -> Any:
        raise RuntimeError("B-0072 directional client")


class QuarantinePort(Protocol):
    def place(
        self,
        package: Mapping[str, Any],
        *,
        attempt_id: str,
        transport_kind: str,
        received_at: datetime,
    ) -> str:
        raise RuntimeError("monitored quarantine storage")

    def record_state(
        self,
        quarantine_ref: str,
        *,
        state: str,
        reason_codes: Sequence[str],
        evidence_refs: Sequence[str],
    ) -> None:
        raise RuntimeError("visible quarantine state transition")


class GovernancePolicyPort(Protocol):
    def evaluate_import(
        self,
        *,
        package: Mapping[str, Any],
        candidates: Sequence[Mapping[str, Any]],
        actor_ref: str,
        authority_domain_id: str,
        at: datetime,
    ) -> LocalPolicyDecision:
        raise RuntimeError("Governance Policy Runtime public evaluation")


class MediathequeImportPort(Protocol):
    def accept_import(
        self,
        *,
        package_id: str,
        candidates: Sequence[Mapping[str, Any]],
        actor_ref: str,
        authority_domain_id: str,
        decision_ref: str,
        idempotency_key: str,
    ) -> Mapping[str, Any]:
        raise RuntimeError("kOA Mediatheque public candidate acceptance")

    def offer_update_candidate(
        self,
        *,
        package_id: str,
        candidates: Sequence[Mapping[str, Any]],
        actor_ref: str,
        authority_domain_id: str,
        decision_ref: str,
        idempotency_key: str,
    ) -> Mapping[str, Any]:
        raise RuntimeError("kOA Mediatheque public update-candidate interface")


class ImportReceiptPort(Protocol):
    def persist(self, receipt: Mapping[str, Any]) -> str:
        raise RuntimeError("immutable UCKK import receipt persistence")


class ImportWorkflowStorePort(Protocol):
    def load(self, idempotency_key: str) -> "StoredImport | None":
        raise RuntimeError("durable import idempotency lookup")

    def save(self, value: "StoredImport") -> None:
        raise RuntimeError("durable import workflow persistence")


class Clock(Protocol):
    def now(self) -> datetime:
        raise RuntimeError("timezone-aware UTC clock")


class IdGenerator(Protocol):
    def new(self, prefix: str) -> str:
        raise RuntimeError("stable identifier generator")


@dataclass(frozen=True, slots=True)
class ImportResult:
    outcome: str
    receipt: Mapping[str, Any]
    receipt_ref: str
    quarantine_ref: str | None
    local_record_refs: tuple[str, ...] = ()
    local_version_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "receipt", _immutable_json_object(self.receipt, "receipt"))
        object.__setattr__(
            self,
            "local_record_refs",
            _unique_texts(self.local_record_refs, "local_record_refs", required=False),
        )
        object.__setattr__(
            self,
            "local_version_refs",
            _unique_texts(self.local_version_refs, "local_version_refs", required=False),
        )


@dataclass(frozen=True, slots=True)
class StoredImport:
    idempotency_key: str
    request_fingerprint: str
    result: ImportResult


class LearningImportService:
    """Orchestrate one explicit UCKK import attempt."""

    def __init__(
        self,
        *,
        client: DirectionalImportClientPort,
        verifier: PackageVerifier,
        quarantine: QuarantinePort,
        governance: GovernancePolicyPort,
        mediatheque: MediathequeImportPort,
        receipts: ImportReceiptPort,
        workflows: ImportWorkflowStorePort,
        clock: Clock,
        ids: IdGenerator,
        policy: ImportPolicy,
    ) -> None:
        self._client = client
        self._verifier = verifier
        self._quarantine = quarantine
        self._governance = governance
        self._mediatheque = mediatheque
        self._receipts = receipts
        self._workflows = workflows
        self._clock = clock
        self._ids = ids
        self._policy = policy

    def import_online(self, request: ImportRequest) -> ImportResult:
        if request.endpoint_id not in self._policy.allowed_endpoint_ids:
            raise ImportWorkflowError(
                "ENDPOINT_NOT_ALLOWLISTED", "the selected UCKK endpoint is not allowlisted"
            )
        previous = self._load_previous(request)
        if previous is not None:
            return previous

        graph_call = self._client.execute(
            "resolve_selected_source_graph",
            {
                "endpoint_id": request.endpoint_id,
                "package_id": request.package_id,
                "selection": dict(request.selection_payload()),
            },
            correlation_id=request.correlation_id,
            idempotency_key=request.idempotency_key + ":resolve",
            authority_domain=request.authority_domain_id,
        )
        graph_response = self._successful_response(graph_call)
        if graph_response is None:
            return self._boundary_failure(request, graph_call, "SOURCE_GRAPH_UNAVAILABLE")
        source_graph_ref = graph_response.get("source_graph_ref")
        if not isinstance(source_graph_ref, str) or not source_graph_ref:
            return self._boundary_failure(request, graph_call, "SOURCE_GRAPH_INVALID")

        package_call = self._client.execute(
            "retrieve_learning_package",
            {
                "endpoint_id": request.endpoint_id,
                "package_id": request.package_id,
                "source_graph_ref": source_graph_ref,
                "selection": dict(request.selection_payload()),
            },
            correlation_id=request.correlation_id,
            idempotency_key=request.idempotency_key + ":retrieve",
            authority_domain=request.authority_domain_id,
        )
        package_response = self._successful_response(package_call)
        if package_response is None:
            return self._boundary_failure(request, package_call, "PACKAGE_RETRIEVAL_FAILED")
        package = package_response.get("learning_package")
        if not isinstance(package, Mapping):
            return self._boundary_failure(request, package_call, "PACKAGE_RESPONSE_INVALID")
        return self._process_package(
            request,
            package,
            transport_kind=TransportKind.ONLINE,
            offline_bundle=None,
            boundary_evidence=(
                _call_receipt_id(graph_call),
                _call_receipt_id(package_call),
            ),
        )

    def import_offline(
        self,
        request: ImportRequest,
        *,
        package: Mapping[str, Any],
        offline_bundle: Mapping[str, Any],
    ) -> ImportResult:
        if request.endpoint_id not in self._policy.allowed_endpoint_ids:
            raise ImportWorkflowError(
                "ENDPOINT_NOT_ALLOWLISTED", "the selected UCKK endpoint is not allowlisted"
            )
        previous = self._load_previous(request)
        if previous is not None:
            return previous
        return self._process_package(
            request,
            package,
            transport_kind=TransportKind.OFFLINE_BUNDLE,
            offline_bundle=offline_bundle,
            boundary_evidence=(),
        )

    def _load_previous(self, request: ImportRequest) -> ImportResult | None:
        previous = self._workflows.load(request.idempotency_key)
        if previous is None:
            return None
        expected = _request_fingerprint(request)
        if previous.request_fingerprint != expected:
            raise ImportWorkflowError(
                "IDEMPOTENCY_CONFLICT",
                "the idempotency key is already bound to a different import request",
            )
        return previous.result

    def _process_package(
        self,
        request: ImportRequest,
        package: Mapping[str, Any],
        *,
        transport_kind: TransportKind,
        offline_bundle: Mapping[str, Any] | None,
        boundary_evidence: Sequence[str],
    ) -> ImportResult:
        now = _utc(self._clock.now())
        normalized = _json_object(package, "learning package")
        if normalized.get("package_id") != request.package_id:
            raise ImportWorkflowError(
                "PACKAGE_ID_MISMATCH", "retrieved package identity differs from the selection"
            )
        resources = normalized.get("resources")
        if not isinstance(resources, list) or len(resources) > self._policy.maximum_resource_count:
            raise ImportWorkflowError(
                "INVALID_IMPORT_REQUEST", "package resource count exceeds the import policy"
            )
        attempt_id = self._ids.new("uckk_import_attempt")

        # Quarantine is intentionally the first local state transition.
        quarantine_ref = self._quarantine.place(
            normalized,
            attempt_id=attempt_id,
            transport_kind=transport_kind.value,
            received_at=now,
        )
        report = self._verifier.verify(
            normalized,
            transport_kind=transport_kind,
            verified_at=now,
            offline_bundle=offline_bundle,
        )
        all_evidence = tuple(
            sorted(set((*boundary_evidence, *report.evidence_refs, quarantine_ref)))
        )

        if report.disposition is not VerificationDisposition.VERIFIED:
            outcome = (
                "rejected"
                if report.disposition is VerificationDisposition.REJECTED
                else "quarantined"
            )
            return self._finalize(
                request=request,
                report=report,
                outcome=outcome,
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=report.failure_codes,
            )

        if request.action is ImportAction.VALIDATE_ONLY:
            return self._finalize(
                request=request,
                report=report,
                outcome="quarantined",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=("EXPLICIT_LOCAL_ACCEPTANCE_REQUIRED",),
                notes=("package verified and retained in quarantine pending explicit acceptance",),
            )

        candidate_payloads = tuple(
            candidate.to_mediatheque_request() for candidate in report.candidates
        )
        try:
            policy_decision = self._governance.evaluate_import(
                package=normalized,
                candidates=candidate_payloads,
                actor_ref=request.actor_ref,
                authority_domain_id=request.authority_domain_id,
                at=now,
            )
        except Exception as exc:
            return self._finalize(
                request=request,
                report=report,
                outcome="quarantined",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=("GOVERNANCE_EVALUATION_UNAVAILABLE",),
                notes=(f"governance evaluation failed: {type(exc).__name__}",),
            )
        if not isinstance(policy_decision, LocalPolicyDecision):
            return self._finalize(
                request=request,
                report=report,
                outcome="quarantined",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=("GOVERNANCE_DECISION_INVALID",),
            )
        all_evidence = tuple(
            sorted(
                set(
                    (
                        *all_evidence,
                        policy_decision.decision_ref,
                        *policy_decision.evidence_refs,
                    )
                )
            )
        )
        if not policy_decision.is_current_at(now):
            return self._finalize(
                request=request,
                report=report,
                outcome="rejected",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=("POLICY_DECISION_EXPIRED",),
            )
        if policy_decision.outcome is PolicyOutcome.DENY:
            return self._finalize(
                request=request,
                report=report,
                outcome="rejected",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=(policy_decision.reason_code,),
            )
        if policy_decision.outcome is PolicyOutcome.REVIEW:
            return self._finalize(
                request=request,
                report=report,
                outcome="quarantined",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=(policy_decision.reason_code,),
                notes=("local governance review is required before acceptance",),
            )

        if request.action is ImportAction.OFFER_UPDATE_CANDIDATE:
            try:
                response = self._mediatheque.offer_update_candidate(
                    package_id=request.package_id,
                    candidates=candidate_payloads,
                    actor_ref=request.actor_ref,
                    authority_domain_id=request.authority_domain_id,
                    decision_ref=policy_decision.decision_ref,
                    idempotency_key=request.idempotency_key,
                )
                update = _json_object(response, "Mediatheque update-candidate response")
            except Exception as exc:
                return self._finalize(
                    request=request,
                    report=report,
                    outcome="failed",
                    quarantine_ref=quarantine_ref,
                    occurred_at=now,
                    evidence_refs=all_evidence,
                    reason_codes=("LOCAL_UPDATE_INTERFACE_UNAVAILABLE",),
                    notes=(f"Mediatheque update interface failed: {type(exc).__name__}",),
                )
            if update.get("outcome") != "update_candidate":
                return self._finalize(
                    request=request,
                    report=report,
                    outcome="failed",
                    quarantine_ref=quarantine_ref,
                    occurred_at=now,
                    evidence_refs=tuple(sorted(set((*all_evidence, *_response_evidence(update))))),
                    reason_codes=("LOCAL_UPDATE_RESPONSE_INVALID",),
                )
            return self._finalize(
                request=request,
                report=report,
                outcome="update_candidate",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=tuple(
                    sorted(set((*all_evidence, *_response_evidence(update))))
                ),
                reason_codes=("REMOTE_VERSION_REQUIRES_LOCAL_DECISION",),
                update_policy={
                    "automatic_remote_overwrite": False,
                    "remote_version_ref": _remote_version_ref(normalized),
                    "local_decision_required": True,
                    "conflict_state": _conflict_state(update),
                },
            )

        try:
            response = self._mediatheque.accept_import(
                package_id=request.package_id,
                candidates=candidate_payloads,
                actor_ref=request.actor_ref,
                authority_domain_id=request.authority_domain_id,
                decision_ref=policy_decision.decision_ref,
                idempotency_key=request.idempotency_key,
            )
            accepted = _json_object(response, "Mediatheque acceptance response")
        except Exception as exc:
            return self._finalize(
                request=request,
                report=report,
                outcome="failed",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=all_evidence,
                reason_codes=("LOCAL_ACCEPTANCE_UNAVAILABLE",),
                notes=(f"Mediatheque acceptance failed: {type(exc).__name__}",),
            )
        outcome = accepted.get("outcome")
        try:
            if outcome not in {"accepted", "partially_accepted", "rejected"}:
                raise ImportWorkflowError(
                    "INVALID_LOCAL_ACCEPTANCE",
                    "Mediatheque acceptance returned an unsupported outcome",
                )
            record_refs = _local_refs(
                accepted.get("local_record_refs", []), _LOCAL_RECORD_ID, "local_record_refs"
            )
            version_refs = _local_refs(
                accepted.get("local_version_refs", []), _LOCAL_VERSION_ID, "local_version_refs"
            )
            if outcome in {"accepted", "partially_accepted"} and (
                not record_refs or not version_refs
            ):
                raise ImportWorkflowError(
                    "INVALID_LOCAL_ACCEPTANCE",
                    "accepted import requires Mediatheque-owned record and version identities",
                )
        except ImportWorkflowError as exc:
            return self._finalize(
                request=request,
                report=report,
                outcome="failed",
                quarantine_ref=quarantine_ref,
                occurred_at=now,
                evidence_refs=tuple(sorted(set((*all_evidence, *_response_evidence(accepted))))),
                reason_codes=(exc.code,),
                notes=(exc.message,),
            )
        acceptance = None
        if outcome in {"accepted", "partially_accepted"}:
            acceptance = {
                "accepted_by_ref": request.actor_ref,
                "decision_ref": policy_decision.decision_ref,
                "accepted_at": _timestamp(now),
                "local_record_refs": list(record_refs),
                "local_version_refs": list(version_refs),
            }
        return self._finalize(
            request=request,
            report=report,
            outcome=str(outcome),
            quarantine_ref=quarantine_ref,
            occurred_at=now,
            evidence_refs=tuple(
                sorted(set((*all_evidence, *_response_evidence(accepted))))
            ),
            reason_codes=(str(accepted.get("reason_code", "LOCAL_ACCEPTANCE_COMPLETED")),),
            acceptance=acceptance,
            local_record_refs=record_refs,
            local_version_refs=version_refs,
        )

    def _boundary_failure(
        self, request: ImportRequest, call: Any, reason_code: str
    ) -> ImportResult:
        now = _utc(self._clock.now())
        evidence = tuple(ref for ref in (_call_receipt_id(call),) if ref)
        report = VerificationReport(
            package_id=request.package_id,
            disposition=VerificationDisposition.QUARANTINED,
            manifest_complete=False,
            integrity_verified=False,
            signature_verified=False,
            source_verified=False,
            license_resolved=False,
            offline_use_allowed=False,
            frame_compatible=False,
            provenance_preserved=False,
            malware_scan_outcome="unavailable_blocked",
            review_required=False,
            failure_codes=(reason_code,),
            evidence_refs=evidence,
            candidates=(),
        )
        return self._finalize(
            request=request,
            report=report,
            outcome="failed",
            quarantine_ref=None,
            occurred_at=now,
            evidence_refs=evidence,
            reason_codes=(reason_code,),
        )

    def _finalize(
        self,
        *,
        request: ImportRequest,
        report: VerificationReport,
        outcome: str,
        quarantine_ref: str | None,
        occurred_at: datetime,
        evidence_refs: Sequence[str],
        reason_codes: Sequence[str],
        notes: Sequence[str] = (),
        acceptance: Mapping[str, Any] | None = None,
        update_policy: Mapping[str, Any] | None = None,
        local_record_refs: Sequence[str] = (),
        local_version_refs: Sequence[str] = (),
    ) -> ImportResult:
        normalized_reasons = tuple(sorted(set(str(value) for value in reason_codes if value)))
        receipt = _build_import_receipt(
            request=request,
            report=report,
            outcome=outcome,
            occurred_at=occurred_at,
            evidence_refs=evidence_refs,
            notes=tuple(notes) + tuple(f"reason:{value}" for value in normalized_reasons),
            acceptance=acceptance,
            update_policy=update_policy,
        )
        receipt_ref = self._receipts.persist(receipt)
        if quarantine_ref is not None:
            state = "accepted" if outcome in {"accepted", "partially_accepted"} else outcome
            self._quarantine.record_state(
                quarantine_ref,
                state=state,
                reason_codes=normalized_reasons,
                evidence_refs=tuple(sorted(set((*evidence_refs, receipt_ref)))),
            )
        result = ImportResult(
            outcome=outcome,
            receipt=receipt,
            receipt_ref=receipt_ref,
            quarantine_ref=quarantine_ref,
            local_record_refs=tuple(local_record_refs),
            local_version_refs=tuple(local_version_refs),
        )
        self._workflows.save(
            StoredImport(
                idempotency_key=request.idempotency_key,
                request_fingerprint=_request_fingerprint(request),
                result=result,
            )
        )
        return result

    @staticmethod
    def _successful_response(call: Any) -> Mapping[str, Any] | None:
        if getattr(call, "succeeded", False) is not True:
            return None
        response = getattr(call, "response", None)
        return response if isinstance(response, Mapping) else None


def _build_import_receipt(
    *,
    request: ImportRequest,
    report: VerificationReport,
    outcome: str,
    occurred_at: datetime,
    evidence_refs: Sequence[str],
    notes: Sequence[str],
    acceptance: Mapping[str, Any] | None,
    update_policy: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    core: dict[str, Any] = {
        "$schema": _RECEIPT_SCHEMA,
        "package_id": request.package_id,
        "attempt_id": request.request_id,
        "occurred_at": _timestamp(occurred_at),
        "source": {
            "system_id": "uckk",
            "endpoint_id": request.endpoint_id,
            "source_object_refs": list(request.source_object_refs),
            "source_version_refs": list(request.source_version_refs),
        },
        "destination": {
            "system_id": "koa-linux",
            "component_id": "koa_mediatheque",
            "authority_domain_id": request.authority_domain_id,
        },
        "outcome": outcome,
        "validation": dict(report.validation_payload()),
        "authority_separation_preserved": True,
        "evidence_refs": sorted(set(str(value) for value in evidence_refs if value)),
        "notes": sorted(set(str(value) for value in notes if value)),
    }
    if acceptance is not None:
        core["acceptance"] = _json_object(acceptance, "acceptance")
    if update_policy is not None:
        core["update_policy"] = _json_object(update_policy, "update_policy")
    digest = sha256(_canonical_json(core)).hexdigest()
    core["receipt_id"] = "uckk_import_receipt_" + digest
    return _immutable_json_object(core, "import receipt")


def _request_fingerprint(request: ImportRequest) -> str:
    return sha256(
        _canonical_json(
            {
                "request_id": request.request_id,
                "package_id": request.package_id,
                "idempotency_key": request.idempotency_key,
                "correlation_id": request.correlation_id,
                "actor_ref": request.actor_ref,
                "authority_domain_id": request.authority_domain_id,
                "endpoint_id": request.endpoint_id,
                "selection_type": request.selection_type,
                "source_object_refs": list(request.source_object_refs),
                "source_version_refs": list(request.source_version_refs),
                "action": request.action.value,
            }
        )
    ).hexdigest()


def _call_receipt_id(call: Any) -> str:
    receipt = getattr(call, "receipt", None)
    value = getattr(receipt, "receipt_id", None)
    return value if isinstance(value, str) else ""


def _response_evidence(response: Mapping[str, Any]) -> tuple[str, ...]:
    raw = response.get("evidence_refs", [])
    if not isinstance(raw, list):
        return ()
    return tuple(sorted(set(value for value in raw if isinstance(value, str) and value)))


def _remote_version_ref(package: Mapping[str, Any]) -> str:
    selection = package.get("selection")
    if isinstance(selection, Mapping):
        refs = selection.get("source_version_refs")
        if isinstance(refs, list) and refs and isinstance(refs[0], str):
            return refs[0]
    return str(package.get("package_version", "unknown"))


def _conflict_state(response: Mapping[str, Any]) -> str:
    value = response.get("conflict_state", "unknown")
    return value if value in {
        "none",
        "local_changes_present",
        "rights_changed",
        "source_withdrawn",
        "unknown",
    } else "unknown"


def _local_refs(value: Any, pattern: re.Pattern[str], name: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise ImportWorkflowError("INVALID_LOCAL_ACCEPTANCE", f"{name} must be a list")
    refs = tuple(sorted(set(item for item in value if isinstance(item, str))))
    if len(refs) != len(value) or any(not pattern.fullmatch(item) for item in refs):
        raise ImportWorkflowError(
            "INVALID_LOCAL_ACCEPTANCE", f"{name} contains a non-canonical local identity"
        )
    return refs


def _unique_texts(
    values: Sequence[str], name: str, *, required: bool
) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{name} must be a sequence")
    normalized = tuple(str(value).strip() for value in values)
    if any(not value for value in normalized) or len(set(normalized)) != len(normalized):
        raise ValueError(f"{name} must contain unique non-empty strings")
    if required and not normalized:
        raise ValueError(f"{name} must not be empty")
    return tuple(sorted(normalized))


def _json_object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ImportWorkflowError("REMOTE_RESPONSE_INVALID", f"{name} must be an object")
    try:
        normalized = json.loads(_canonical_json(_plain_json(value)))
    except (TypeError, ValueError) as exc:
        raise ImportWorkflowError(
            "REMOTE_RESPONSE_INVALID", f"{name} must contain JSON-compatible values"
        ) from exc
    if not isinstance(normalized, dict):
        raise ImportWorkflowError("REMOTE_RESPONSE_INVALID", f"{name} must be an object")
    return normalized


def _immutable_json_object(value: Mapping[str, Any], name: str) -> Mapping[str, Any]:
    return MappingProxyType(_json_object(value, name))


def _plain_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _plain_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain_json(item) for item in value]
    return value


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _utc(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("clock must return a timezone-aware datetime")
    return value.astimezone(timezone.utc)


def _timestamp(value: datetime) -> str:
    return _utc(value).isoformat().replace("+00:00", "Z")
