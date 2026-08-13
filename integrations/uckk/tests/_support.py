"""Reusable test support for integrations/uckk/tests.

Pytest fixture registration belongs in conftest.py; this module contains only importable constants, builders, doubles, and helper functions."""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_SRC = REPOSITORY_ROOT / 'integrations' / 'uckk' / 'adapter' / 'src'
from koa_uckk_adapter.learning_import import ImportAction, ImportPolicy, ImportRequest, LearningImportService, LocalPolicyDecision, PolicyOutcome, StoredImport
from koa_uckk_adapter.mediatheque_frame import FrameMappingPolicy, FrameProjector
from koa_uckk_adapter.package_verification import PackageVerifier, SourceEvidence
NOW = datetime(2026, 8, 6, 16, 0, tzinfo=timezone.utc)
LOCAL_AUTHORITY = 'authority://koa/local-mediatheque'
SOURCE_AUTHORITY = 'authority://uckk/site-main'
CONTENT = b'verified offline learning content'
CONTENT_REF = 'uckk-package://content/resource-001'
DIGEST = sha256(CONTENT).hexdigest()

def plain_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): plain_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain_json(item) for item in value]
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
    return value

class SchemaPort:

    def __init__(self, schema_name: str) -> None:
        schema_root = REPOSITORY_ROOT / 'docs' / 'contracts' / 'artifact-contracts'
        resources: list[tuple[str, Resource[Any]]] = []
        for path in sorted(schema_root.glob('*.schema.json')):
            document = json.loads(path.read_text(encoding='utf-8'))
            try:
                resource = Resource.from_contents(document)
            except Exception:
                continue
            resources.append((path.resolve().as_uri(), resource))
            identifier = document.get('$id')
            if isinstance(identifier, str):
                resources.append((identifier, resource))
        schema = json.loads((schema_root / schema_name).read_text(encoding='utf-8'))
        self.validator = Draft202012Validator(schema, registry=Registry().with_resources(resources), format_checker=FormatChecker())

    def validate(self, value: Mapping[str, Any]) -> None:
        self.validator.validate(value)

class ManifestPort:

    def __init__(self, valid: bool=True, events: list[str] | None=None) -> None:
        self.valid = valid
        self.events = events

    def verify(self, package: Mapping[str, Any]) -> bool:
        if self.events is not None:
            self.events.append('verify_manifest')
        return self.valid and package['manifest']['entry_count'] == len(package['resources'])

class SourcePort:

    def __init__(self, *, source_verified: bool=True, signature_verified: bool=True, equivalent_verified: bool=False, events: list[str] | None=None) -> None:
        self.source_verified = source_verified
        self.signature_verified = signature_verified
        self.equivalent_verified = equivalent_verified
        self.events = events

    def verify(self, package: Mapping[str, Any], *, transport_kind: Any) -> SourceEvidence:
        if self.events is not None:
            self.events.append('verify_source')
        return SourceEvidence(self.source_verified, self.signature_verified, self.equivalent_verified, ('evidence:uckk-source-001',))

class IntegrityPort:

    def __init__(self, values: Mapping[str, bytes], *, valid: bool=True, events: list[str] | None=None) -> None:
        self.values = dict(values)
        self.valid = valid
        self.events = events

    def verify(self, *, content_ref: str, algorithm: str, digest: str, size_bytes: int) -> bool:
        if self.events is not None:
            self.events.append('verify_resource')
        data = self.values.get(content_ref)
        return bool(self.valid and data is not None and (len(data) == size_bytes) and (__import__('hashlib').new(algorithm, data).hexdigest() == digest))

class MalwarePort:

    def __init__(self, outcome: str='pass', events: list[str] | None=None) -> None:
        self.outcome = outcome
        self.events = events

    def scan(self, **_: Any) -> str:
        if self.events is not None:
            self.events.append('scan_resource')
        return self.outcome

class OfflineBundlePort:

    def __init__(self, valid: bool=True, events: list[str] | None=None) -> None:
        self.valid = valid
        self.events = events

    def verify(self, *, bundle: Mapping[str, Any], package: Mapping[str, Any]) -> bool:
        if self.events is not None:
            self.events.append('verify_offline_bundle')
        return self.valid and bundle.get('bundle_id') == 'offline_bundle_001'

class QuarantinePort:

    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.packages: list[dict[str, Any]] = []
        self.states: list[dict[str, Any]] = []

    def place(self, package: Mapping[str, Any], *, attempt_id: str, transport_kind: str, received_at: datetime) -> str:
        self.events.append('quarantine_place')
        self.packages.append(deepcopy(dict(package)))
        return f"quarantine://uckk/{package['package_id']}/{attempt_id}"

    def record_state(self, quarantine_ref: str, *, state: str, reason_codes: tuple[str, ...], evidence_refs: tuple[str, ...]) -> None:
        self.events.append(f'quarantine_state:{state}')
        self.states.append({'quarantine_ref': quarantine_ref, 'state': state, 'reason_codes': tuple(reason_codes), 'evidence_refs': tuple(evidence_refs)})

class GovernancePort:

    def __init__(self, events: list[str], outcome: PolicyOutcome=PolicyOutcome.ALLOW, *, expires_at: datetime | None=None) -> None:
        self.events = events
        self.outcome = outcome
        self.expires_at = expires_at
        self.calls: list[dict[str, Any]] = []
        self.failure: BaseException | None = None

    def evaluate_import(self, **request: Any) -> LocalPolicyDecision:
        self.events.append('governance_evaluate')
        if self.failure is not None:
            raise self.failure
        self.calls.append(plain_json(request))
        return LocalPolicyDecision(outcome=self.outcome, decision_ref='decision:governance:uckk-import-001', reason_code='LOCAL_IMPORT_ALLOWED' if self.outcome is PolicyOutcome.ALLOW else 'LOCAL_IMPORT_REVIEW_REQUIRED' if self.outcome is PolicyOutcome.REVIEW else 'LOCAL_IMPORT_DENIED', evidence_refs=('evidence:governance-001',), expires_at=self.expires_at)

class MediathequePort:

    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.accept_calls: list[dict[str, Any]] = []
        self.update_calls: list[dict[str, Any]] = []
        self.accept_response: dict[str, Any] = {'outcome': 'accepted', 'reason_code': 'LOCAL_IDENTITIES_CREATED', 'local_record_refs': ['koa_media_import_001'], 'local_version_refs': ['koa_media_version_import_001'], 'evidence_refs': ['receipt:mediatheque-accept-001']}
        self.update_response: dict[str, Any] = {'outcome': 'update_candidate', 'conflict_state': 'local_changes_present', 'evidence_refs': ['receipt:mediatheque-update-001']}
        self.accept_failure: BaseException | None = None
        self.update_failure: BaseException | None = None

    def accept_import(self, **request: Any) -> Mapping[str, Any]:
        self.events.append('mediatheque_accept')
        if self.accept_failure is not None:
            raise self.accept_failure
        self.accept_calls.append(plain_json(request))
        return deepcopy(self.accept_response)

    def offer_update_candidate(self, **request: Any) -> Mapping[str, Any]:
        self.events.append('mediatheque_update_candidate')
        if self.update_failure is not None:
            raise self.update_failure
        self.update_calls.append(plain_json(request))
        return deepcopy(self.update_response)

class ReceiptPort:

    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.schema = SchemaPort('uckk-import-receipt.schema.json')
        self.values: list[dict[str, Any]] = []

    def persist(self, receipt: Mapping[str, Any]) -> str:
        value = plain_json(receipt)
        self.schema.validate(value)
        self.events.append('receipt_persist')
        self.values.append(value)
        return f"receipt://uckk/import/{receipt['receipt_id']}"

class WorkflowStore:

    def __init__(self) -> None:
        self.values: dict[str, StoredImport] = {}
        self.saves: list[StoredImport] = []

    def load(self, idempotency_key: str) -> StoredImport | None:
        return self.values.get(idempotency_key)

    def save(self, value: StoredImport) -> None:
        self.values[value.idempotency_key] = value
        self.saves.append(value)

class FixedClock:

    def now(self) -> datetime:
        return NOW

class SequenceIds:

    def __init__(self) -> None:
        self.value = 0

    def new(self, prefix: str) -> str:
        self.value += 1
        return f'{prefix}_{self.value:04d}'

@dataclass(frozen=True, slots=True)
class FakeCallReceipt:
    receipt_id: str

@dataclass(frozen=True, slots=True)
class FakeCallResult:
    succeeded: bool
    response: Mapping[str, Any] | None
    receipt: FakeCallReceipt

class ImportClient:

    def __init__(self, package: Mapping[str, Any]) -> None:
        self.package = deepcopy(dict(package))
        self.calls: list[dict[str, Any]] = []
        self.fail_operation: str | None = None

    def execute(self, operation: str, payload: Mapping[str, Any], *, correlation_id: str, idempotency_key: str, authority_domain: str='koa_linux', tenant_id: str | None=None) -> FakeCallResult:
        self.calls.append({'operation': operation, 'payload': deepcopy(dict(payload)), 'correlation_id': correlation_id, 'idempotency_key': idempotency_key, 'authority_domain': authority_domain})
        if self.fail_operation == operation:
            return FakeCallResult(False, None, FakeCallReceipt(f'adapter:{operation}:failed'))
        if operation == 'resolve_selected_source_graph':
            response = {'source_graph_ref': 'uckk://source-graph/course-001'}
        elif operation == 'retrieve_learning_package':
            response = {'learning_package': deepcopy(self.package)}
        else:
            raise AssertionError(f'unexpected import operation: {operation}')
        return FakeCallResult(True, response, FakeCallReceipt(f'adapter:{operation}:ok'))

def make_service(package: Mapping[str, Any], *, manifest_valid: bool=True, integrity_valid: bool=True, malware_outcome: str='pass', source_verified: bool=True, signature_verified: bool=True, offline_bundle_valid: bool=True, policy_outcome: PolicyOutcome=PolicyOutcome.ALLOW) -> tuple[LearningImportService, dict[str, Any]]:
    events: list[str] = []
    client = ImportClient(package)
    quarantine = QuarantinePort(events)
    governance = GovernancePort(events, policy_outcome)
    mediatheque = MediathequePort(events)
    receipts = ReceiptPort(events)
    workflows = WorkflowStore()
    projector = FrameProjector(FrameMappingPolicy(local_authority_domain_id=LOCAL_AUTHORITY, target_frame_version='1.0.0', supported_source_versions=('1.0.0',), supported_mapping_versions=('1.0.0',)))
    verifier = PackageVerifier(schema=SchemaPort('uckk-learning-package.schema.json'), manifest=ManifestPort(manifest_valid, events), source_evidence=SourcePort(source_verified=source_verified, signature_verified=signature_verified, events=events), resource_integrity=IntegrityPort({CONTENT_REF: CONTENT}, valid=integrity_valid, events=events), malware=MalwarePort(malware_outcome, events), frame_projector=projector, offline_bundle=OfflineBundlePort(offline_bundle_valid, events))
    service = LearningImportService(client=client, verifier=verifier, quarantine=quarantine, governance=governance, mediatheque=mediatheque, receipts=receipts, workflows=workflows, clock=FixedClock(), ids=SequenceIds(), policy=ImportPolicy(('uckk-primary',), maximum_resource_count=100))
    return (service, {'events': events, 'client': client, 'quarantine': quarantine, 'governance': governance, 'mediatheque': mediatheque, 'receipts': receipts, 'workflows': workflows, 'verifier': verifier})
