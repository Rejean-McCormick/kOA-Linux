"""Governed outbound UCKK publication workflow.

This module implements only ``publish_to_uckk``.  It does not import from UCKK,
read UCKK as a kOA authority, write another component's database, or infer
remote acceptance from a local send.  Authority, source-state verification,
manifest verification, payload resolution, workflow persistence, queueing and
receipt persistence are explicit injected ports owned by their canonical
components or by the B-0072 resilience layer.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
from typing import Any, Mapping, Protocol, Sequence

from .moodle_client import BinaryPayload, MoodleClientError

PACKAGE_SCHEMA_ID = "https://schemas.koa.local/artifact-contracts/uckk-publication-package.schema.json"
RECEIPT_SCHEMA_ID = "https://schemas.koa.local/artifact-contracts/uckk-publication-receipt.schema.json"
WORKFLOW_SCHEMA_ID = "https://schemas.koa.local/artifact-contracts/distributed-workflow.schema.json"
WORKFLOW_ID = "uckk.publish_to_uckk"
WORKFLOW_VERSION = "1.0.0"
FRAME_ID = "koa-uckk-shared-mediatheque-frame"

_PACKAGE_ID = re.compile(r"^uckk_pub_pkg_[A-Za-z0-9][A-Za-z0-9._-]*$")
_DIGEST = re.compile(r"^[0-9a-f]{64,128}$")
_TERMINAL_WORKFLOW_STATES = frozenset(
    {"completed", "failed_closed", "cancelled", "forward_repair_required", "human_intervention_required"}
)
_SUCCESS_ITEM_OUTCOMES = frozenset({"published", "updated", "skipped_idempotent"})


class PublicationError(RuntimeError):
    """Stable publication failure that never contains media or credentials."""

    _ALLOWED_CODES = frozenset(
        {
            "AUTHORIZATION_EXPIRED",
            "CONTENT_INTEGRITY_FAILED",
            "DESTINATION_UNAVAILABLE",
            "DESTINATION_UNSUPPORTED",
            "IDEMPOTENCY_CONFLICT",
            "INVALID_PACKAGE",
            "MAPPING_INCOMPATIBLE",
            "PAYLOAD_UNAVAILABLE",
            "RECEIPT_INVALID",
            "REMOTE_RESULT_AMBIGUOUS",
            "RIGHTS_CHANGED",
            "SOURCE_VERSION_CHANGED",
            "WORKFLOW_STATE_UNAVAILABLE",
        }
    )

    def __init__(self, code: str, message: str) -> None:
        if code not in self._ALLOWED_CODES:
            raise ValueError(f"undeclared publication error code: {code}")
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class StoredPublication:
    idempotency_key: str
    package_fingerprint: str
    workflow: Mapping[str, Any]
    receipt: Mapping[str, Any] | None


class PackageSchemaPort(Protocol):
    def validate(self, package: Mapping[str, Any]) -> None:
        raise NotImplementedError("canonical package schema validator")


class ManifestVerificationPort(Protocol):
    def verify(self, package: Mapping[str, Any]) -> bool:
        raise NotImplementedError("canonical publication manifest verification")


class AuthorizationPort(Protocol):
    def authorization_is_current(self, package: Mapping[str, Any], *, at: datetime) -> bool:
        raise NotImplementedError("Publication Gateway authorization check")


class SourceAuthorityPort(Protocol):
    def source_item_is_current(self, item: Mapping[str, Any], *, at: datetime) -> bool:
        raise NotImplementedError("kOA Mediatheque version and rights check")


class PayloadResolverPort(Protocol):
    def resolve_verified(
        self,
        *,
        transfer_ref: str,
        integrity: Mapping[str, Any],
        size_bytes: int,
        media_type: str,
        filename: str | None,
    ) -> BinaryPayload:
        raise NotImplementedError("verified large-payload reference resolver")


class WorkflowStorePort(Protocol):
    def load(self, idempotency_key: str) -> StoredPublication | None:
        raise NotImplementedError("durable idempotency lookup")

    def save(self, publication: StoredPublication) -> None:
        raise NotImplementedError("durable workflow and idempotency persistence")


class QueuePort(Protocol):
    def enqueue(
        self,
        *,
        package: Mapping[str, Any],
        workflow: Mapping[str, Any],
        reason_code: str,
    ) -> str:
        raise NotImplementedError("protected visible outbound queue")


class ReceiptPort(Protocol):
    def persist(self, receipt: Mapping[str, Any]) -> str:
        raise NotImplementedError("immutable publication receipt persistence")


class Clock(Protocol):
    def now(self) -> datetime:
        raise NotImplementedError("UTC clock")


class IdGenerator(Protocol):
    def new(self, prefix: str) -> str:
        raise NotImplementedError("stable identifier generator")


class MoodlePublicationPort(Protocol):
    def authenticate(self, *, correlation_id: str) -> Mapping[str, Any]: ...

    def validate_destination_capability(
        self,
        *,
        mapping_version: str,
        object_kinds: Sequence[str],
        correlation_id: str,
    ) -> Mapping[str, Any]: ...

    def query_publication_status(
        self,
        *,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]: ...

    def create_or_update_remote_representation(
        self,
        *,
        item: Mapping[str, Any],
        idempotency_key: str,
        mapping_version: str,
        correlation_id: str,
    ) -> Mapping[str, Any]: ...

    def upload_content(
        self,
        *,
        remote_object_ref: str,
        payload: BinaryPayload,
        integrity: Mapping[str, Any],
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]: ...

    def attach_metadata(
        self,
        *,
        remote_object_ref: str,
        metadata: Mapping[str, Any],
        rights_assertion: Mapping[str, Any],
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]: ...

    def receive_publication_receipt(
        self,
        *,
        idempotency_key: str,
        correlation_id: str,
    ) -> Mapping[str, Any]: ...


class PublicationService:
    """Orchestrates one directional, receipted UCKK publication workflow."""

    def __init__(
        self,
        *,
        moodle: MoodlePublicationPort,
        package_schema: PackageSchemaPort,
        manifest_verifier: ManifestVerificationPort,
        authorization: AuthorizationPort,
        source_authority: SourceAuthorityPort,
        payloads: PayloadResolverPort,
        workflows: WorkflowStorePort,
        queue: QueuePort,
        receipts: ReceiptPort,
        clock: Clock,
        ids: IdGenerator,
    ) -> None:
        self._moodle = moodle
        self._package_schema = package_schema
        self._manifest_verifier = manifest_verifier
        self._authorization = authorization
        self._source_authority = source_authority
        self._payloads = payloads
        self._workflows = workflows
        self._queue = queue
        self._receipts = receipts
        self._clock = clock
        self._ids = ids

    def publish(self, package: Mapping[str, Any], *, correlation_id: str) -> Mapping[str, Any]:
        now = _utc(self._clock.now())
        normalized = _validate_package_boundary(package, now=now)
        self._package_schema.validate(normalized)
        if not self._manifest_verifier.verify(normalized):
            raise PublicationError("CONTENT_INTEGRITY_FAILED", "the publication manifest is invalid")

        idempotency_key = str(normalized["idempotency_key"])
        fingerprint = _package_fingerprint(normalized)
        previous = self._workflows.load(idempotency_key)
        if previous is not None:
            if previous.package_fingerprint != fingerprint:
                return self._terminal_rejection(
                    normalized,
                    correlation_id=correlation_id,
                    now=now,
                    fingerprint=fingerprint,
                    failure_code="IDEMPOTENCY_CONFLICT",
                )
            if previous.receipt is not None:
                return deepcopy(dict(previous.receipt))

        workflow = _new_workflow(
            package=normalized,
            correlation_id=correlation_id,
            instance_id=self._ids.new("uckk_pub_workflow"),
        )
        self._save(idempotency_key, fingerprint, workflow, None)
        _complete_step(workflow, "verify_package")

        if not self._authorization.authorization_is_current(normalized, at=now):
            return self._finalize(
                package=normalized,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
                outcome="cancelled",
                workflow_state="cancelled",
                item_results=_failure_results(normalized, "AUTHORIZATION_EXPIRED", retryable=False),
                retry_allowed=False,
                reconciliation_required=False,
                authorization_valid=False,
            )
        _complete_step(workflow, "verify_authorization")

        stale_items = [
            item for item in normalized["items"]
            if not self._source_authority.source_item_is_current(item, at=now)
        ]
        if stale_items:
            return self._finalize(
                package=normalized,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
                outcome="cancelled",
                workflow_state="cancelled",
                item_results=_failure_results(
                    normalized,
                    "SOURCE_VERSION_CHANGED",
                    retryable=False,
                    only_item_ids={str(item["item_id"]) for item in stale_items},
                ),
                retry_allowed=False,
                reconciliation_required=False,
                authorization_valid=True,
            )
        _complete_step(workflow, "verify_source_state")

        try:
            self._moodle.authenticate(correlation_id=correlation_id)
            self._moodle.validate_destination_capability(
                mapping_version=str(normalized["target"]["mapping_version"]),
                object_kinds=tuple(
                    str(item["destination_mapping"]["object_kind"])
                    for item in normalized["items"]
                ),
                correlation_id=correlation_id,
            )
            _complete_step(workflow, "validate_destination")
            reconciled = self._reconcile_existing(
                package=normalized,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
            )
            if reconciled is not None:
                return reconciled
            return self._transmit(
                package=normalized,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
            )
        except MoodleClientError as error:
            return self._handle_client_failure(
                package=normalized,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
                error=error,
            )

    def _reconcile_existing(
        self,
        *,
        package: Mapping[str, Any],
        workflow: dict[str, Any],
        fingerprint: str,
        correlation_id: str,
        now: datetime,
    ) -> Mapping[str, Any] | None:
        status = self._moodle.query_publication_status(
            idempotency_key=str(package["idempotency_key"]),
            correlation_id=correlation_id,
        )
        remote_outcome = str(status.get("outcome", "not_found"))
        if remote_outcome in {"not_found", "pending"}:
            _complete_step(workflow, "reconcile_idempotency")
            return None
        if remote_outcome not in {
            "published",
            "partially_published",
            "failed",
            "rejected",
            "unknown_reconciliation_required",
        }:
            raise MoodleClientError(
                "REMOTE_RESULT_AMBIGUOUS",
                "the remote publication status cannot be reconciled",
                retryable=True,
                ambiguous=True,
            )
        item_results = status.get("item_results")
        if not isinstance(item_results, list) or not item_results:
            raise MoodleClientError("RECEIPT_INVALID", "the reconciled result has no item outcomes")
        state = {
            "published": "completed",
            "partially_published": "forward_repair_required",
            "failed": "failed_closed",
            "rejected": "failed_closed",
            "unknown_reconciliation_required": "human_intervention_required",
        }[remote_outcome]
        return self._finalize(
            package=package,
            workflow=workflow,
            fingerprint=fingerprint,
            correlation_id=correlation_id,
            now=now,
            outcome=remote_outcome,
            workflow_state=state,
            item_results=item_results,
            retry_allowed=remote_outcome in {"failed", "partially_published"},
            reconciliation_required=remote_outcome == "unknown_reconciliation_required",
            authorization_valid=True,
            remote_response=status.get("remote_response"),
        )

    def _transmit(
        self,
        *,
        package: Mapping[str, Any],
        workflow: dict[str, Any],
        fingerprint: str,
        correlation_id: str,
        now: datetime,
    ) -> Mapping[str, Any]:
        item_results: list[dict[str, Any]] = []
        ambiguous = False
        for item in package["items"]:
            item_key = f"{package['idempotency_key']}:{item['item_id']}"
            try:
                content = item["content"]
                payload = self._payloads.resolve_verified(
                    transfer_ref=str(content["transfer_ref"]),
                    integrity=item["integrity"],
                    size_bytes=int(content["size_bytes"]),
                    media_type=str(item["media_type"]),
                    filename=content.get("original_filename"),
                )
                remote = self._moodle.create_or_update_remote_representation(
                    item=item,
                    idempotency_key=item_key,
                    mapping_version=str(package["target"]["mapping_version"]),
                    correlation_id=correlation_id,
                )
                remote_ref = _required_remote_ref(remote)
                upload = self._moodle.upload_content(
                    remote_object_ref=remote_ref,
                    payload=payload,
                    integrity=item["integrity"],
                    idempotency_key=item_key,
                    correlation_id=correlation_id,
                )
                self._moodle.attach_metadata(
                    remote_object_ref=remote_ref,
                    metadata=item.get("metadata", {}),
                    rights_assertion=item["rights_assertion"],
                    idempotency_key=item_key,
                    correlation_id=correlation_id,
                )
                item_results.append(
                    {
                        "item_id": item["item_id"],
                        "record_id": item["record_id"],
                        "version_id": item["version_id"],
                        "outcome": "updated" if remote.get("updated") is True else "published",
                        "remote_object_refs": [remote_ref],
                        "remote_version_ref": str(upload.get("remote_version_ref", "unversioned")),
                        "http_status": int(upload.get("http_status", 200)),
                        "retryable": False,
                    }
                )
            except MoodleClientError as error:
                if error.ambiguous:
                    reconciled = self._moodle.query_publication_status(
                        idempotency_key=item_key,
                        correlation_id=correlation_id,
                    )
                    if reconciled.get("outcome") in _SUCCESS_ITEM_OUTCOMES:
                        item_results.append(
                            {
                                "item_id": item["item_id"],
                                "record_id": item["record_id"],
                                "version_id": item["version_id"],
                                "outcome": str(reconciled["outcome"]),
                                "remote_object_refs": list(reconciled.get("remote_object_refs", [])),
                                "retryable": False,
                            }
                        )
                        continue
                    ambiguous = True
                    item_results.append(_item_failure(item, "REMOTE_RESULT_AMBIGUOUS", True, unknown=True))
                else:
                    item_results.append(_item_failure(item, error.code, error.retryable))
            except PublicationError as error:
                item_results.append(_item_failure(item, error.code, False))

        _complete_step(workflow, "transmit_items")
        successes = sum(result["outcome"] in _SUCCESS_ITEM_OUTCOMES for result in item_results)
        failures = len(item_results) - successes
        if ambiguous:
            outcome = "unknown_reconciliation_required"
            state = "human_intervention_required"
        elif successes and failures:
            outcome = "partially_published"
            state = "forward_repair_required"
        elif successes == len(item_results):
            outcome = "published"
            state = "completed"
        else:
            retryable = any(result.get("retryable") is True for result in item_results)
            if retryable and _offline_queue_allowed(package):
                return self._queue_publication(
                    package=package,
                    workflow=workflow,
                    fingerprint=fingerprint,
                    correlation_id=correlation_id,
                    now=now,
                    reason_code="DESTINATION_UNAVAILABLE",
                    item_results=item_results,
                )
            outcome = "failed"
            state = "failed_closed"

        remote_response: Mapping[str, Any] | None = None
        if outcome == "published":
            try:
                remote_receipt = self._moodle.receive_publication_receipt(
                    idempotency_key=str(package["idempotency_key"]),
                    correlation_id=correlation_id,
                )
                remote_response = {
                    "remote_receipt_ref": str(remote_receipt.get("receipt_ref", "remote-receipt")),
                    "request_ref": str(remote_receipt.get("request_ref", package["idempotency_key"])),
                }
            except MoodleClientError:
                outcome = "unknown_reconciliation_required"
                state = "human_intervention_required"

        return self._finalize(
            package=package,
            workflow=workflow,
            fingerprint=fingerprint,
            correlation_id=correlation_id,
            now=now,
            outcome=outcome,
            workflow_state=state,
            item_results=item_results,
            retry_allowed=outcome in {"failed", "partially_published"},
            reconciliation_required=outcome == "unknown_reconciliation_required",
            authorization_valid=True,
            remote_response=remote_response,
        )

    def _handle_client_failure(
        self,
        *,
        package: Mapping[str, Any],
        workflow: dict[str, Any],
        fingerprint: str,
        correlation_id: str,
        now: datetime,
        error: MoodleClientError,
    ) -> Mapping[str, Any]:
        if error.ambiguous:
            return self._finalize(
                package=package,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
                outcome="unknown_reconciliation_required",
                workflow_state="human_intervention_required",
                item_results=_failure_results(package, "REMOTE_RESULT_AMBIGUOUS", retryable=True, unknown=True),
                retry_allowed=True,
                reconciliation_required=True,
                authorization_valid=True,
            )
        if error.retryable and _offline_queue_allowed(package):
            return self._queue_publication(
                package=package,
                workflow=workflow,
                fingerprint=fingerprint,
                correlation_id=correlation_id,
                now=now,
                reason_code=error.code,
                item_results=_failure_results(package, error.code, retryable=True),
            )
        return self._finalize(
            package=package,
            workflow=workflow,
            fingerprint=fingerprint,
            correlation_id=correlation_id,
            now=now,
            outcome="failed",
            workflow_state="failed_closed",
            item_results=_failure_results(package, error.code, retryable=error.retryable),
            retry_allowed=error.retryable,
            reconciliation_required=False,
            authorization_valid=True,
        )

    def _queue_publication(
        self,
        *,
        package: Mapping[str, Any],
        workflow: dict[str, Any],
        fingerprint: str,
        correlation_id: str,
        now: datetime,
        reason_code: str,
        item_results: Sequence[Mapping[str, Any]],
    ) -> Mapping[str, Any]:
        workflow["state"] = "waiting_remote"
        queue_ref = self._queue.enqueue(
            package=deepcopy(dict(package)),
            workflow=deepcopy(workflow),
            reason_code=reason_code,
        )
        receipt = _receipt(
            package=package,
            receipt_id=self._ids.new("uckk_pub_receipt"),
            attempt_id=str(workflow["instance_id"]),
            occurred_at=now,
            outcome="queued",
            item_results=item_results,
            authorization_valid=True,
            retry_allowed=True,
            reconciliation_required=False,
            evidence_refs=[queue_ref],
        )
        receipt_ref = self._receipts.persist(receipt)
        workflow["evidence"]["terminal_receipt_ref"] = receipt_ref
        self._save(str(package["idempotency_key"]), fingerprint, workflow, receipt)
        return deepcopy(receipt)

    def _terminal_rejection(
        self,
        package: Mapping[str, Any],
        *,
        correlation_id: str,
        now: datetime,
        fingerprint: str,
        failure_code: str,
    ) -> Mapping[str, Any]:
        workflow = _new_workflow(
            package=package,
            correlation_id=correlation_id,
            instance_id=self._ids.new("uckk_pub_workflow"),
        )
        receipt = _receipt(
            package=package,
            receipt_id=self._ids.new("uckk_pub_receipt"),
            attempt_id=str(workflow["instance_id"]),
            occurred_at=now,
            outcome="rejected",
            item_results=_failure_results(package, failure_code, retryable=False),
            authorization_valid=False,
            retry_allowed=False,
            reconciliation_required=False,
        )
        receipt_ref = self._receipts.persist(receipt)
        workflow["state"] = "failed_closed"
        _complete_step(workflow, "record_receipt")
        workflow["evidence"]["terminal_receipt_ref"] = receipt_ref
        # The original idempotency binding is deliberately not overwritten.
        return deepcopy(receipt)

    def _finalize(
        self,
        *,
        package: Mapping[str, Any],
        workflow: dict[str, Any],
        fingerprint: str,
        correlation_id: str,
        now: datetime,
        outcome: str,
        workflow_state: str,
        item_results: Sequence[Mapping[str, Any]],
        retry_allowed: bool,
        reconciliation_required: bool,
        authorization_valid: bool,
        remote_response: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        if workflow_state not in _TERMINAL_WORKFLOW_STATES:
            raise PublicationError("WORKFLOW_STATE_UNAVAILABLE", "a terminal workflow state is required")
        receipt = _receipt(
            package=package,
            receipt_id=self._ids.new("uckk_pub_receipt"),
            attempt_id=str(workflow["instance_id"]),
            occurred_at=now,
            outcome=outcome,
            item_results=item_results,
            authorization_valid=authorization_valid,
            retry_allowed=retry_allowed,
            reconciliation_required=reconciliation_required,
            remote_response=remote_response,
        )
        receipt_ref = self._receipts.persist(receipt)
        workflow["state"] = workflow_state
        _complete_step(workflow, "record_receipt")
        workflow["evidence"]["terminal_receipt_ref"] = receipt_ref
        self._save(str(package["idempotency_key"]), fingerprint, workflow, receipt)
        return deepcopy(receipt)

    def _save(
        self,
        idempotency_key: str,
        fingerprint: str,
        workflow: Mapping[str, Any],
        receipt: Mapping[str, Any] | None,
    ) -> None:
        self._workflows.save(
            StoredPublication(
                idempotency_key=idempotency_key,
                package_fingerprint=fingerprint,
                workflow=deepcopy(dict(workflow)),
                receipt=deepcopy(dict(receipt)) if receipt is not None else None,
            )
        )


def _validate_package_boundary(package: Mapping[str, Any], *, now: datetime) -> dict[str, Any]:
    if not isinstance(package, Mapping):
        raise PublicationError("INVALID_PACKAGE", "the publication package must be an object")
    normalized = deepcopy(dict(package))
    required = {
        "package_id",
        "package_version",
        "created_at",
        "source",
        "target",
        "authorization",
        "items",
        "manifest",
        "idempotency_key",
        "frame_compatibility",
    }
    if not required.issubset(normalized):
        raise PublicationError("INVALID_PACKAGE", "the publication package is incomplete")
    if not _PACKAGE_ID.fullmatch(str(normalized["package_id"])):
        raise PublicationError("INVALID_PACKAGE", "the publication package identity is invalid")
    if normalized["source"].get("system_id") != "koa-linux" or normalized["source"].get("component_id") != "koa_mediatheque":
        raise PublicationError("INVALID_PACKAGE", "the publication source is invalid")
    if normalized["source"].get("source_authority_preserved") is not True:
        raise PublicationError("INVALID_PACKAGE", "local source authority must be preserved")
    if normalized["target"].get("system_id") != "uckk" or normalized["target"].get("platform_type") != "moodle":
        raise PublicationError("INVALID_PACKAGE", "the publication target is invalid")
    if normalized["authorization"].get("decision_outcome") != "allow":
        raise PublicationError("INVALID_PACKAGE", "an allow decision is required")
    if normalized["frame_compatibility"].get("frame_id") != FRAME_ID:
        raise PublicationError("MAPPING_INCOMPATIBLE", "the shared Mediatheque frame is invalid")
    if normalized["frame_compatibility"].get("rights_preserved") is not True or normalized["frame_compatibility"].get("provenance_preserved") is not True:
        raise PublicationError("MAPPING_INCOMPATIBLE", "rights and provenance must be preserved")
    if normalized["frame_compatibility"].get("mapping_version") != normalized["target"].get("mapping_version"):
        raise PublicationError("MAPPING_INCOMPATIBLE", "package and target mapping versions differ")
    expires_at = normalized.get("expires_at")
    if expires_at is not None and _parse_time(expires_at) <= now:
        raise PublicationError("AUTHORIZATION_EXPIRED", "the publication package has expired")
    items = normalized.get("items")
    if not isinstance(items, list) or not items:
        raise PublicationError("INVALID_PACKAGE", "the publication package has no items")
    seen: set[str] = set()
    total_size = 0
    for item in items:
        if not isinstance(item, Mapping):
            raise PublicationError("INVALID_PACKAGE", "publication items must be objects")
        item_id = str(item.get("item_id", ""))
        if not item_id or item_id in seen:
            raise PublicationError("INVALID_PACKAGE", "publication item identities must be unique")
        seen.add(item_id)
        content = item.get("content")
        integrity = item.get("integrity")
        rights = item.get("rights_assertion")
        if not isinstance(content, Mapping) or not str(content.get("transfer_ref", "")).startswith("koa-object://"):
            raise PublicationError("INVALID_PACKAGE", "content must use a verified kOA object reference")
        prohibited = {"bytes", "content_bytes", "data", "payload"}.intersection(content)
        if prohibited:
            raise PublicationError("INVALID_PACKAGE", "inline media payloads are prohibited")
        if not isinstance(integrity, Mapping) or integrity.get("algorithm") not in {"sha256", "sha384", "sha512"}:
            raise PublicationError("CONTENT_INTEGRITY_FAILED", "item integrity metadata is invalid")
        if not _DIGEST.fullmatch(str(integrity.get("digest", ""))):
            raise PublicationError("CONTENT_INTEGRITY_FAILED", "item digest is invalid")
        if not isinstance(rights, Mapping) or rights.get("publication_allowed") is not True or rights.get("target_allowed") is not True:
            raise PublicationError("RIGHTS_CHANGED", "item rights do not permit UCKK publication")
        total_size += int(content.get("size_bytes", -1))
    manifest = normalized["manifest"]
    if manifest.get("item_count") != len(items) or manifest.get("total_size_bytes") != total_size:
        raise PublicationError("CONTENT_INTEGRITY_FAILED", "the publication manifest does not match its items")
    if not _DIGEST.fullmatch(str(manifest.get("digest", ""))):
        raise PublicationError("CONTENT_INTEGRITY_FAILED", "the publication manifest digest is invalid")
    queue_policy = normalized.get("queue_policy")
    if queue_policy is not None:
        if queue_policy.get("cancel_on_authorization_change") is not True or queue_policy.get("cancel_on_source_version_change") is not True:
            raise PublicationError("INVALID_PACKAGE", "queued work must cancel on authority or source changes")
    return normalized


def _new_workflow(
    *,
    package: Mapping[str, Any],
    correlation_id: str,
    instance_id: str,
) -> dict[str, Any]:
    return {
        "$schema": WORKFLOW_SCHEMA_ID,
        "artifact_class": "distributed_workflow",
        "authority": "koa-linux",
        "workflow_id": WORKFLOW_ID,
        "instance_id": instance_id,
        "version": WORKFLOW_VERSION,
        "workflow_type": "orchestrated",
        "authority_domains": [
            "koa-linux:koa_mediatheque",
            "koa-linux:publication_gateway",
            "uckk:moodle",
        ],
        "state": "pending",
        "idempotency_key": package["idempotency_key"],
        "steps": [
            _step("verify_package", "uckk-publication-bridge", "verify package schema and manifest"),
            _step("verify_authorization", "publication_gateway", "verify authorization remains current"),
            _step("verify_source_state", "koa_mediatheque", "verify selected source versions and rights"),
            _step("validate_destination", "uckk-publication-bridge", "authenticate and validate destination capability"),
            _step("reconcile_idempotency", "uckk-publication-bridge", "reconcile prior remote outcome"),
            _step("transmit_items", "uckk-publication-bridge", "publish selected items"),
            _step("record_receipt", "uckk-publication-bridge", "persist terminal publication evidence"),
        ],
        "repair_policy": {
            "reverse_order_when_safe": True,
            "hidden_partial_success_prohibited": True,
            "human_intervention_state_required": True,
        },
        "visibility": {
            "intermediate_state_label": "publish_to_uckk",
            "terminal_state_required": True,
        },
        "evidence": {
            "correlation_id": correlation_id,
            "terminal_receipt_required": True,
            "terminal_receipt_ref": None,
        },
    }


def _step(step_id: str, owner_id: str, action: str) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "owner_id": owner_id,
        "action": action,
        "state": "not_started",
        "timeout_seconds": 60,
        "irreversible": step_id == "transmit_items",
        "compensation_mode": "forward_repair" if step_id == "transmit_items" else "not_applicable_before_execution",
        "compensation_action": "send supported withdrawal notice" if step_id == "transmit_items" else None,
        "receipt_ref": None,
    }


def _complete_step(workflow: dict[str, Any], step_id: str) -> None:
    for step in workflow["steps"]:
        if step["step_id"] == step_id:
            step["state"] = "completed"
            return
    raise PublicationError("WORKFLOW_STATE_UNAVAILABLE", "the distributed workflow step is missing")


def _receipt(
    *,
    package: Mapping[str, Any],
    receipt_id: str,
    attempt_id: str,
    occurred_at: datetime,
    outcome: str,
    item_results: Sequence[Mapping[str, Any]],
    authorization_valid: bool,
    retry_allowed: bool,
    reconciliation_required: bool,
    evidence_refs: Sequence[str] = (),
    remote_response: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "$schema": RECEIPT_SCHEMA_ID,
        "receipt_id": receipt_id,
        "package_id": package["package_id"],
        "attempt_id": attempt_id,
        "idempotency_key": package["idempotency_key"],
        "occurred_at": _format_time(occurred_at),
        "source": {"system_id": "koa-linux", "component_id": "koa_mediatheque"},
        "target": {
            "system_id": "uckk",
            "platform_type": "moodle",
            "endpoint_id": package["target"]["endpoint_id"],
            **(
                {"site_ref": package["target"]["destination"]["site_ref"]}
                if "site_ref" in package["target"]["destination"]
                else {}
            ),
        },
        "outcome": outcome,
        "source_authority_preserved": True,
        "remote_authority_separate": True,
        "authorization": {
            "publication_request_ref": package["authorization"]["publication_request_ref"],
            "decision_ref": package["authorization"]["decision_ref"],
            "authorization_valid_at_attempt": authorization_valid,
        },
        "item_results": [dict(item) for item in item_results],
        "integrity": {
            "package_digest_verified": True,
            "response_signature_verified": False,
            "response_digest": "sha256:" + sha256(_canonical_json(item_results)).hexdigest(),
        },
        "retry": {
            "retry_allowed": retry_allowed,
            "next_attempt_after": None,
            "remaining_attempts": _remaining_attempts(package),
            "reconciliation_required": reconciliation_required,
        },
        "evidence_refs": list(evidence_refs),
        "frame_mapping": {
            "frame_id": FRAME_ID,
            "mapping_version": package["frame_compatibility"]["mapping_version"],
            "mapping_validated": True,
            "rights_preserved": True,
            "provenance_preserved": True,
        },
    }
    if remote_response:
        allowed = {"request_ref", "response_ref", "remote_receipt_ref", "remote_timestamp"}
        result["remote_response"] = {key: value for key, value in remote_response.items() if key in allowed}
    return result


def _failure_results(
    package: Mapping[str, Any],
    failure_code: str,
    *,
    retryable: bool,
    only_item_ids: set[str] | None = None,
    unknown: bool = False,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for item in package["items"]:
        selected = only_item_ids is None or str(item["item_id"]) in only_item_ids
        code = failure_code if selected else "SOURCE_VERSION_CHANGED"
        results.append(_item_failure(item, code, retryable if selected else False, unknown=unknown and selected))
    return results


def _item_failure(
    item: Mapping[str, Any],
    failure_code: str,
    retryable: bool,
    *,
    unknown: bool = False,
) -> dict[str, Any]:
    return {
        "item_id": item["item_id"],
        "record_id": item["record_id"],
        "version_id": item["version_id"],
        "outcome": "unknown" if unknown else "failed",
        "failure_code": failure_code,
        "failure_message": "publication did not reach a verified remote outcome",
        "retryable": retryable,
    }


def _required_remote_ref(response: Mapping[str, Any]) -> str:
    value = response.get("remote_object_ref")
    if not isinstance(value, str) or not value:
        raise MoodleClientError("INVALID_REMOTE_RESPONSE", "the remote object reference is missing")
    return value


def _offline_queue_allowed(package: Mapping[str, Any]) -> bool:
    policy = package.get("queue_policy")
    return isinstance(policy, Mapping) and policy.get("offline_queue_allowed") is True


def _remaining_attempts(package: Mapping[str, Any]) -> int:
    policy = package.get("queue_policy")
    if not isinstance(policy, Mapping):
        return 0
    return max(int(policy.get("maximum_attempts", 1)) - 1, 0)


def _package_fingerprint(package: Mapping[str, Any]) -> str:
    return "sha256:" + sha256(_canonical_json(package)).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _parse_time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise PublicationError("INVALID_PACKAGE", "a date-time value is invalid")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PublicationError("INVALID_PACKAGE", "a date-time value is invalid") from exc
    if parsed.tzinfo is None:
        raise PublicationError("INVALID_PACKAGE", "date-time values require an explicit timezone")
    return parsed.astimezone(timezone.utc)


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise PublicationError("WORKFLOW_STATE_UNAVAILABLE", "the workflow clock must be timezone-aware")
    return value.astimezone(timezone.utc)


def _format_time(value: datetime) -> str:
    return _utc(value).isoformat().replace("+00:00", "Z")
