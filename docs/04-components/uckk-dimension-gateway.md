<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-UCKK-DG-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component"
  ],
  "component_id": "uckk_dimension_gateway",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/capability_model",
    "generated/component-catalog.json#/components/uckk_dimension_gateway",
    "generated/component-catalog.json#/components/uckk_platform",
    "generated/component-catalog.json#/components/publication_gateway",
    "generated/component-catalog.json",
    "contracts/components/uckk-dimension-gateway.component.json",
    "schemas/component-contract.schema.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-GATE-001",
    "DEC-UCKK-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-DATA-DISCLOSURE-001",
    "DEC-CULT-001",
    "DEC-INT-001"
  ],
  "requirement_ids": [
    "REQ-COMP-UCKK-DG-001",
    "REQ-COMP-UCKK-DG-002",
    "REQ-COMP-UCKK-DG-003",
    "REQ-COMP-UCKK-DG-004",
    "REQ-COMP-UCKK-DG-005",
    "REQ-COMP-UCKK-DG-006",
    "REQ-COMP-UCKK-DG-007",
    "REQ-COMP-UCKK-DG-008",
    "REQ-COMP-UCKK-DG-009",
    "REQ-COMP-UCKK-DG-010",
    "REQ-COMP-UCKK-DG-011",
    "REQ-COMP-UCKK-DG-012",
    "REQ-COMP-UCKK-DG-013",
    "REQ-COMP-UCKK-DG-014",
    "REQ-COMP-UCKK-DG-015",
    "REQ-COMP-UCKK-DG-016",
    "REQ-COMP-UCKK-DG-017",
    "REQ-COMP-UCKK-DG-018",
    "REQ-COMP-UCKK-DG-019",
    "REQ-COMP-UCKK-DG-020",
    "REQ-COMP-UCKK-DG-021",
    "REQ-COMP-UCKK-DG-022",
    "REQ-COMP-UCKK-DG-023",
    "REQ-COMP-UCKK-DG-024",
    "REQ-COMP-UCKK-DG-025",
    "REQ-COMP-UCKK-DG-026",
    "REQ-COMP-UCKK-DG-027",
    "REQ-COMP-UCKK-DG-028",
    "REQ-COMP-UCKK-DG-029",
    "REQ-COMP-UCKK-DG-030",
    "REQ-COMP-UCKK-DG-031",
    "REQ-COMP-UCKK-DG-032",
    "REQ-COMP-UCKK-DG-033",
    "REQ-COMP-UCKK-DG-034",
    "REQ-COMP-UCKK-DG-035",
    "REQ-COMP-UCKK-DG-036"
  ],
  "lock_ids": [
    "LOCK-GATE-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001"
  ],
  "tags": [
    "uckk",
    "uckk-dimension-gateway",
    "selected-media-transfer",
    "controlled-admission",
    "component-boundary",
    "data-authority",
    "provenance",
    "integrity",
    "consent",
    "cultural-rights",
    "offline-transfer",
    "idempotency",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# UCKK Dimension Gateway

## 1. Purpose

UCKK Dimension Gateway controls the transfer and controlled admission of user-selected media into a target UCKK dimension.

The component exists to preserve a clear boundary between:

- the source component that owns the selected media or source record;
- the gateway that owns the transfer transaction;
- UCKK Platform, which owns admitted UCKK media state;
- Governance Policy Runtime, which owns applicable authorization, consent, disclosure, and rights decisions;
- Resource Governor, which owns resource admission and pressure response;
- Audit Broker, which owns protected audit records;
- Publication Gateway, which owns cross-domain disclosure and publication.

The gateway coordinates a deterministic local workflow. It does not become a universal media owner, a publication service, an AI classifier, a policy engine, or a direct database bridge.

The canonical component registry and component contract own the machine-readable component facts. This document explains the boundary, workflow, states, failures, and conformance expectations.

## 2. Scope

This document applies to:

- explicit selection of source media for a UCKK dimension;
- source-owner request and authorization;
- transfer-request creation;
- source and target validation;
- functional content-integrity verification;
- duplicate detection;
- quarantine and staging;
- provenance preservation;
- consent and cultural-rights evaluation;
- UCKK Platform admission;
- transfer receipts;
- retries, resume, reconciliation, conflict, cancellation, and withdrawal;
- profile-specific online and offline behavior;
- offline-transfer bundles;
- resource and storage controls;
- gateway observability, recovery, maintenance, and conformance.

The component can handle local files, component-owned media objects, controlled imports, external-adapter candidate outputs, or offline-transfer artifacts only through registered source and artifact contracts.

This document does not define:

- UCKK Platform's internal media model;
- UCKK indexing and retrieval internals;
- cross-domain publication;
- external provider contracts;
- user identity authority;
- consent or cultural-rights authority;
- host-privileged operations;
- profile hardware values;
- implementation libraries or deployment topology.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Component identity and high-level responsibility | `generated/component-catalog.json#/components/uckk_dimension_gateway` |
| Observable gateway behavior | `contracts/components/uckk-dimension-gateway.component.json` |
| Common component-contract rules | `04-components/01-component-contract-rules.md` |
| UCKK Platform identity and admitted media ownership | `generated/component-catalog.json#/components/uckk_platform` |
| Publication responsibility | `generated/component-catalog.json#/components/publication_gateway` |
| Global capability model | `contracts/system.contract.json#/capability_model` |
| Profile activation and operating envelopes | `contracts/profiles/*.profile.json` |
| External adapters and controlled boundaries | `contracts/integration-types.contract.json` |
| Media, transfer, manifest, receipt, and evidence artifact classes | `contracts/artifact-classes.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file component and gateway invariants | `generated/assertion-index.json` |
| Decision, component, capability, profile, test, and evidence links | `generated/traceability.json` |
| Component conformance tests | `generated/test-catalog.json` |
| Component evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

This document explains the active contract. It does not duplicate the canonical interface inventory, profile matrices, artifact schemas, or test catalog.

## 4. Component Model and Authority

### 4.1 Identity and class

The canonical component identity is:

```text
uckk_dimension_gateway
```

Its component class is `gateway`. Its authority class is `authoritative_executor` for the transfer transaction and `transport` for media movement.

The gateway is authoritative for:

- transfer-request identity;
- canonical request-body binding;
- transfer state;
- selected source and target references;
- staging and quarantine state;
- transfer attempts;
- verified functional integrity records associated with the request;
- destination admission result reference;
- reconciliation state;
- cancellation and withdrawal processing state;
- transfer receipt reference.

The gateway is not authoritative for source media semantics or admitted destination state.

### 4.2 Responsibility partition

The gateway owns:

- request validation;
- selection binding;
- target-dimension routing;
- transfer-state management;
- deterministic integrity verification;
- candidate staging;
- controlled submission to UCKK Platform;
- retry and duplicate protection;
- reconciliation;
- transfer receipt production;
- local transfer observability.

Responsibility owned elsewhere includes:

| Responsibility | Owner |
| --- | --- |
| Source object and source metadata | Source component |
| Admitted UCKK media state | UCKK Platform |
| Identity and trust verification | Identity and Trust |
| Authorization, consent, rights, and obligations | Governance Policy Runtime or another registered policy authority |
| Resource admission and pressure response | Resource Governor |
| Critical audit storage and protected evidence export | Audit Broker |
| Cross-domain disclosure and publication | Publication Gateway |
| External provider processing | Registered integration |
| Privileged host mutation | kOA Node Agent |

### 4.3 Prohibited responsibilities

The gateway does not:

- scan all user or component storage for content to import;
- infer user intent;
- create a transfer from a recommendation alone;
- decide cultural or publication rights;
- publish externally;
- edit source-component authoritative state;
- edit UCKK Platform authoritative state directly;
- perform native AI classification, generation, summarization, embeddings, or autonomous routing;
- treat Suno or Gamma output as admitted media;
- embed credentials in transfer payloads;
- accept arbitrary source paths or arbitrary destination stores;
- convert a duplicate match into automatic acceptance;
- bypass resource, policy, identity, or artifact validation.

### 4.4 Source and destination authority

The source component remains authoritative until destination acceptance completes.

UCKK Platform is the only owner of admitted UCKK media state. It determines:

- whether the candidate is valid for the destination dimension;
- whether an existing destination object is equivalent;
- whether the candidate conflicts with destination state;
- which destination identifier represents an accepted object;
- whether an accepted object is later retired, withdrawn, or corrected.

The gateway records the result. It does not substitute its own decision.

### 4.5 Gateway separation

UCKK Dimension Gateway and Publication Gateway are separate contracts.

UCKK Dimension Gateway controls:

- user-selected media transfer;
- target-dimension routing;
- functional integrity verification;
- quarantine and staging;
- controlled admission into UCKK.

Publication Gateway controls:

- cross-domain disclosure;
- publication;
- release to external audiences.

A workflow can invoke both gateways, but each request, policy decision, artifact, state machine, receipt, and failure remains separate.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-UCKK-DG-001,REQ-COMP-UCKK-DG-002,REQ-COMP-UCKK-DG-003,REQ-COMP-UCKK-DG-004,REQ-COMP-UCKK-DG-005,REQ-COMP-UCKK-DG-006,REQ-COMP-UCKK-DG-007,REQ-COMP-UCKK-DG-008,REQ-COMP-UCKK-DG-009,REQ-COMP-UCKK-DG-010,REQ-COMP-UCKK-DG-011,REQ-COMP-UCKK-DG-012,REQ-COMP-UCKK-DG-013,REQ-COMP-UCKK-DG-014,REQ-COMP-UCKK-DG-015,REQ-COMP-UCKK-DG-016,REQ-COMP-UCKK-DG-017,REQ-COMP-UCKK-DG-018,REQ-COMP-UCKK-DG-019,REQ-COMP-UCKK-DG-020,REQ-COMP-UCKK-DG-021,REQ-COMP-UCKK-DG-022,REQ-COMP-UCKK-DG-023,REQ-COMP-UCKK-DG-024,REQ-COMP-UCKK-DG-025,REQ-COMP-UCKK-DG-026,REQ-COMP-UCKK-DG-027,REQ-COMP-UCKK-DG-028,REQ-COMP-UCKK-DG-029,REQ-COMP-UCKK-DG-030,REQ-COMP-UCKK-DG-031,REQ-COMP-UCKK-DG-032,REQ-COMP-UCKK-DG-033,REQ-COMP-UCKK-DG-034,REQ-COMP-UCKK-DG-035,REQ-COMP-UCKK-DG-036 -->
- **REQ-COMP-UCKK-DG-001 — SHALL:** UCKK Dimension Gateway have one stable component identity and one active component contract matching `uckk_dimension_gateway`.
- **REQ-COMP-UCKK-DG-002 — SHALL:** UCKK Dimension Gateway own the lifecycle and evidence of user-selected transfer requests into a target UCKK dimension.
- **REQ-COMP-UCKK-DG-003 — SHALL NOT:** UCKK Dimension Gateway own admitted UCKK media state, UCKK indexes, source-component records, publication state, user identity, consent authority, or governance policy.
- **REQ-COMP-UCKK-DG-004 — SHALL:** UCKK Platform remain the authoritative owner of media admitted into UCKK and decide final destination acceptance through its registered contract.
- **REQ-COMP-UCKK-DG-005 — SHALL:** The source component remain authoritative for the selected source object until any destination admission completes.
- **REQ-COMP-UCKK-DG-006 — SHALL:** Every transfer begin from an explicit user selection or another explicitly authorized local workflow action bound to an authenticated subject.
- **REQ-COMP-UCKK-DG-007 — SHALL NOT:** Repository presence, background scanning, inferred interest, external provider output, model suggestion, file-system discovery, or prior selection create a new transfer request automatically.
- **REQ-COMP-UCKK-DG-008 — SHALL:** Every request identify the source object, source owner, target UCKK dimension, requesting subject, purpose, profile, policy context, consent context, cultural-rights context, and correlation identity.
- **REQ-COMP-UCKK-DG-009 — SHALL:** Every request use one idempotency identity bound to one canonical request body and reject reuse with different meaning.
- **REQ-COMP-UCKK-DG-010 — SHALL:** The gateway validate source availability, source-owner authorization, target eligibility, destination compatibility, profile scope, resource admission, and required policy decisions before transfer.
- **REQ-COMP-UCKK-DG-011 — SHALL:** The gateway compute or verify functional content-integrity records required by the transfer contract and preserve the algorithm and digest provenance.
- **REQ-COMP-UCKK-DG-012 — SHALL NOT:** A content digest, duplicate match, file name, MIME type, extension, or transport success by itself establish semantic validity, ownership, consent, destination acceptance, or publication authority.
- **REQ-COMP-UCKK-DG-013 — SHALL:** Every transfer preserve source provenance, transformations, integrity records, consent and rights decisions, target scope, and admission outcome.
- **REQ-COMP-UCKK-DG-014 — SHALL:** Candidate media enter a quarantine or staging state before UCKK Platform admission.
- **REQ-COMP-UCKK-DG-015 — SHALL NOT:** Candidate, quarantined, copied, generated, imported, externally processed, or partially transferred media be represented as admitted UCKK media.
- **REQ-COMP-UCKK-DG-016 — SHALL:** The gateway submit destination admission through the UCKK Platform contract and receive an explicit accepted, rejected, duplicate, conflicted, deferred, or failed result.
- **REQ-COMP-UCKK-DG-017 — SHALL NOT:** The gateway write directly to UCKK Platform authoritative stores or any other component's source tables.
- **REQ-COMP-UCKK-DG-018 — SHALL:** The gateway maintain a durable transfer ledger containing request state, idempotency binding, source and target references, integrity records, policy references, attempts, destination results, and receipt references.
- **REQ-COMP-UCKK-DG-019 — SHALL:** A transfer reach completed state only after destination acceptance, destination identity verification, local reconciliation, and durable receipt creation.
- **REQ-COMP-UCKK-DG-020 — SHALL NOT:** Copy completion, queue acknowledgement, transport acknowledgement, checksum match, or remote provider acknowledgement be reported as final UCKK admission.
- **REQ-COMP-UCKK-DG-021 — SHALL:** Interrupted, retried, or duplicate transfers resume or reconcile without creating duplicate authoritative UCKK media records.
- **REQ-COMP-UCKK-DG-022 — SHALL:** A conflict preserve the relevant source, candidate, and destination references and invoke the UCKK Platform conflict policy rather than selecting a winner implicitly.
- **REQ-COMP-UCKK-DG-023 — SHALL:** Cancellation and withdrawal stop new processing, preserve required evidence, and remove or retire staged candidate material according to the active retention and rights policy.
- **REQ-COMP-UCKK-DG-024 — SHALL:** The gateway enforce data minimization and transfer only the media, metadata, provenance, and evidence required by the registered UCKK admission contract.
- **REQ-COMP-UCKK-DG-025 — SHALL NOT:** Credentials, secret material, unrestricted private content, raw private keys, or unrelated source-component records appear in ordinary gateway logs, receipts, metrics, or transfer manifests.
- **REQ-COMP-UCKK-DG-026 — SHALL:** The gateway remain separate from Publication Gateway, which controls cross-domain disclosure, publication, and release to external audiences.
- **REQ-COMP-UCKK-DG-027 — SHALL NOT:** UCKK dimension transfer be treated as public disclosure, and publication approval be treated as UCKK destination admission.
- **REQ-COMP-UCKK-DG-028 — SHALL:** Native gateway selection, validation, routing, integrity verification, staging, and admission coordination remain deterministic and non-AI.
- **REQ-COMP-UCKK-DG-029 — SHALL:** Suno and Gamma remain optional user-triggered external adapters whose returned media remains candidate material until selected and admitted through the local UCKK workflow.
- **REQ-COMP-UCKK-DG-030 — SHALL NOT:** External AI output mutate the transfer ledger, source authority, destination authority, policy state, or admitted UCKK media directly.
- **REQ-COMP-UCKK-DG-031 — SHALL:** The gateway declare per-profile continuous, degraded, deferred, unavailable, and offline-transfer behavior.
- **REQ-COMP-UCKK-DG-032 — SHALL:** Locally selected media transfer to a locally available UCKK dimension continue without external AI or an Internet connection when the effective profile classifies the capability as continuous.
- **REQ-COMP-UCKK-DG-033 — SHALL:** Offline-transfer workflows validate manifests, source identity, signatures where applicable, integrity, replay, compatibility, policy, rights, and destination ownership before admission.
- **REQ-COMP-UCKK-DG-034 — SHALL:** The gateway declare bounded queues, concurrency, storage reserves, timeouts, retry limits, backpressure behavior, and Resource Governor interaction.
- **REQ-COMP-UCKK-DG-035 — SHALL NOT:** The Resource Governor or UCKK Dimension Gateway decide consent, cultural rights, disclosure, publication, privilege, or governance policy from resource state.
- **REQ-COMP-UCKK-DG-036 — SHALL:** Component conformance include ownership separation, explicit selection, request closure, provenance, integrity, quarantine, UCKK Platform admission, idempotency, conflict handling, cancellation, offline behavior, gateway separation, security, resource controls, tests, and current evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Data, Interfaces, and Events

### 6.1 Authoritative stores

The component contract defines these logical stores:

| Store | Purpose | Ownership |
| --- | --- | --- |
| `transfer_request_ledger` | Request identity, canonical body, source, target, policy references, state, attempts, and result references | Gateway authoritative |
| `candidate_staging_index` | References to quarantined or staged candidate media and validation results | Gateway authoritative for staging state |
| `integrity_record_index` | Functional content-integrity records associated with transfer requests | Gateway authoritative for verification record |
| `reconciliation_journal` | Unknown outcomes, duplicate checks, destination verification, and final reconciliation | Gateway authoritative |
| `receipt_outbox` | Durable transfer and failure receipts awaiting Audit Broker delivery | Gateway authoritative until delivery |

The media payload can reside in profile-approved staging storage. Staging does not transfer semantic ownership.

The stores exclude:

- source-component business records;
- destination UCKK authoritative records;
- raw credentials or private keys;
- unrestricted audit payloads;
- unrelated user media;
- external AI conversation history;
- publication records.

### 6.2 Inbound interfaces

The primary inbound interfaces are:

| Interface | Caller | Contract | Boundary |
| --- | --- | --- | --- |
| `create_dimension_transfer` | Authorized local user workflow or component | Dimension transfer request | Local authenticated |
| `cancel_dimension_transfer` | Authorized requester or rights workflow | Transfer cancellation request | Local authenticated |
| `withdraw_staged_candidate` | Authorized rights, privacy, or source-owner workflow | Candidate withdrawal request | Local authenticated |
| `inspect_dimension_transfer` | Authorized user, operator, or owning workflow | Transfer status query | Local authenticated |
| `import_offline_transfer_candidate` | Controlled Import or kOA Node Agent | Offline candidate manifest | Registered offline-transfer path |

Each request uses a closed schema, canonical references, explicit target scope, deadline, correlation identity, and idempotency identity.

### 6.3 Outbound interfaces

The primary outbound interfaces are:

| Interface | Destination | Purpose | Failure behavior |
| --- | --- | --- | --- |
| `verify_identity_and_source` | Identity and Trust and source component | Verify requester, source object, owner, trust, and source state | Block request |
| `verify_policy_and_rights` | Governance Policy Runtime or registered authority | Verify authorization, consent, cultural rights, retention, and obligations | Block or preserve pending policy state |
| `request_resource_admission` | Resource Governor | Admit staging, transfer, hashing, and validation resources | Queue, degrade, or reject |
| `submit_uckk_candidate` | UCKK Platform | Request destination validation and admission | Preserve candidate and pending result |
| `deliver_transfer_receipt` | Audit Broker | Deliver critical transfer, cancellation, withdrawal, and failure receipts | Retain locally and retry |
| `request_privileged_media_access` | kOA Node Agent | Access an allowlisted device or protected offline-transfer path where required | Block affected transfer |
| `resolve_registered_integration` | Integration registry and adapter | Resolve a controlled external or offline source | Reject an unregistered boundary |

No outbound interface grants direct database access.

### 6.4 Request contract

A dimension transfer request includes:

```text
request_id
idempotency_id
requesting_subject_ref
source_component_ref
source_object_ref
source_version_ref
target_dimension_ref
purpose_ref
profile_ref
policy_decision_ref
consent_context_ref
cultural_rights_context_ref
requested_transform_refs
expected_source_state
correlation_id
requested_at
deadline_at
```

Optional transformations are registered deterministic operations. An external transformation has a separate integration request and returns candidate material before any gateway request is created.

### 6.5 Result contract

A result includes:

```text
request_id
transfer_id
status
reason_codes
source_object_ref
target_dimension_ref
candidate_ref
destination_object_ref
integrity_record_refs
policy_decision_refs
started_at
finished_at
receipt_ref
```

Result statuses include:

```text
completed
accepted_pending_reconciliation
deferred
duplicate
rejected
cancelled
withdrawn
failed
conflicted
expired
recovery_required
```

### 6.6 Events

The gateway emits:

- `dimension_transfer_requested`;
- `dimension_transfer_staged`;
- `dimension_transfer_deferred`;
- `dimension_transfer_admitted`;
- `dimension_transfer_duplicate_detected`;
- `dimension_transfer_conflicted`;
- `dimension_transfer_cancelled`;
- `dimension_transfer_withdrawn`;
- `dimension_transfer_failed`;
- `dimension_transfer_recovery_required`.

The gateway consumes:

- source object changed or withdrawn;
- policy or rights decision changed;
- destination admission result;
- destination object retired or corrected where reconciliation requires it;
- resource-pressure state changed;
- trust or revocation state changed.

At-least-once delivery uses idempotent consumers. A malformed event creates an explicit error or gap record.

### 6.7 Integrity records

Functional content-integrity records support:

- transfer corruption detection;
- duplicate detection;
- source-to-candidate verification;
- staged candidate verification;
- offline bundle verification;
- destination-result reconciliation.

They apply to media or transfer artifacts as required by the contract. They do not introduce ordinary Markdown file hashes or transfer semantic authority.

## 7. Workflow and State Transitions

### 7.1 Transfer states

The transfer state model is:

```text
requested
identity_verified
source_verified
scope_verified
policy_and_rights_verified
resource_admitted
candidate_prepared
integrity_verified
quarantined
destination_submitted
destination_pending
destination_accepted
reconciled
receipt_durable
completed
```

Alternative states are:

```text
deferred
duplicate
rejected
cancelled
withdrawn
failed
conflicted
expired
recovery_required
```

### 7.2 Creating a transfer

Transfer creation proceeds through:

1. authenticate the requesting subject;
2. bind one request identity to one canonical request body;
3. resolve the source component and source object;
4. verify the expected source state;
5. resolve the target UCKK dimension;
6. verify profile and capability scope;
7. verify authorization, consent, cultural rights, and obligations;
8. admit resources;
9. create the transfer ledger record;
10. prepare the candidate without changing destination authority.

A failure before ledger creation leaves no active transfer. A failure after ledger creation reaches an explicit state.

### 7.3 Preparing and verifying the candidate

Candidate preparation:

1. reads the source through the source owner's contract;
2. applies only registered deterministic transformations;
3. minimizes metadata;
4. records source provenance;
5. computes or verifies required integrity records;
6. checks duplicates according to the destination contract;
7. places the candidate in profile-approved quarantine or staging;
8. records validation evidence.

A duplicate indication is submitted to UCKK Platform for authoritative destination handling.

### 7.4 Destination admission

Destination admission:

1. submits the candidate reference and manifest through the UCKK Platform contract;
2. preserves source, target, integrity, policy, and rights references;
3. waits for an explicit destination result;
4. verifies the destination identity and result;
5. records accepted, duplicate, rejected, conflicted, or deferred state;
6. reconciles the transfer ledger;
7. creates the transfer receipt;
8. reports completion only after the receipt is durable.

The gateway never writes the destination record itself.

### 7.5 Retry and resume

Before retry or resume, the gateway:

1. verifies request validity and deadline;
2. checks cancellation and withdrawal;
3. revalidates time-sensitive policy and rights;
4. verifies source and candidate integrity;
5. checks existing destination effects;
6. reuses the transfer and idempotency identities;
7. resumes from the last verified state;
8. prevents duplicate destination effects.

An unknown prior destination effect enters reconciliation rather than blind replay.

### 7.6 Conflict handling

A conflict can arise from:

- changed source media;
- changed source rights;
- changed target dimension;
- incompatible destination schema;
- equivalent destination content with different rights;
- concurrent destination modification;
- inconsistent external candidate provenance;
- stale request state.

The gateway preserves all relevant references and asks the owning authorities for a decision. It does not infer a winner.

### 7.7 Cancellation and withdrawal

Cancellation stops a transfer requested but not yet completed.

Withdrawal applies when rights, consent, source state, or policy requires removal of staged material or a follow-up destination action.

The gateway:

1. records the request;
2. prevents new processing;
3. revokes queued attempts;
4. removes or retires staging material according to policy;
5. requests destination action from UCKK Platform when an admitted object is affected;
6. records evidence;
7. preserves only the minimum required ledger and receipt information.

### 7.8 Offline transfer

An offline-transfer candidate follows:

```text
bundle_received
medium_verified
bundle_quarantined
manifest_verified
source_authenticated
integrity_verified
replay_checked
compatibility_verified
policy_and_rights_verified
target_resolved
candidate_staged
destination_submitted
```

Physical possession of media or a signed bundle does not establish destination acceptance.

## 8. Failure, Offline, and Resource Behavior

### 8.1 Failure model

| Failure | Required behavior |
| --- | --- |
| Request schema invalid | Reject before transfer creation. |
| Request identity reused with different body | Reject and record an idempotency violation. |
| Requester or source identity invalid | Block the request. |
| Source object missing or changed | Reject, expire, or conflict according to the expected-state rule. |
| Target dimension invalid | Reject before candidate preparation. |
| Policy, consent, or rights unavailable | Block or defer without preparing an unauthorized candidate. |
| Resource admission denied | Queue, degrade, or reject according to profile policy. |
| Integrity verification fails | Quarantine or reject the candidate. |
| Candidate storage unavailable | Reject new preparation and preserve existing ledger state. |
| UCKK Platform unavailable | Preserve staged candidate and destination-pending state. |
| Destination outcome unknown | Enter reconciliation and prevent blind replay. |
| Destination reports duplicate | Preserve the destination reference and complete only through the destination duplicate policy. |
| Destination reports conflict | Preserve all references and enter conflicted state. |
| Audit Broker unavailable | Retain receipts durably and retry without duplicate delivery. |
| Network unavailable | Continue local transfers where source and destination are local; defer external or remote dependencies. |
| External AI adapter unavailable | Preserve native gateway and UCKK capabilities. |
| Process or power interruption | Reconstruct from the ledger, staging index, reconciliation journal, and receipt outbox. |
| Contract or profile invalid | Block new transfers and preserve the last valid local state. |

### 8.2 Offline behavior

The gateway has no external AI dependency.

A profile can classify:

- local source to local UCKK transfer as continuous;
- transfer with reduced metadata as degraded;
- remote or external-source transfer as deferred;
- external provider transfer as unavailable;
- signed bundle transfer as offline transfer.

Restart while disconnected preserves active ledger state and staging references.

### 8.3 Resource envelope

The component contract declares:

- media size limits;
- staging storage reserve;
- concurrent preparation jobs;
- concurrent destination submissions;
- hashing and validation concurrency;
- queue bounds;
- retry bounds;
- deadlines;
- temporary-file behavior;
- cleanup behavior;
- pressure response.

The Resource Governor can reduce concurrency, pause low-priority preparation, reject new large transfers, or preserve only reconciliation and withdrawal work.

It does not decide whether a transfer is authorized.

### 8.4 Pressure response order

Under pressure, the gateway prioritizes:

1. withdrawal and cancellation;
2. reconciliation of unknown destination outcomes;
3. receipt durability;
4. completion of already accepted bounded transfers;
5. cleanup of expired staging;
6. rejection of new large transfers;
7. suspension of optional transformations.

Authoritative destination records remain with UCKK Platform.

## 9. Security, Privacy, and Cross-Component Boundaries

### 9.1 Identity and authorization

The gateway verifies:

- requesting user or service identity;
- source-component identity;
- source-object authority;
- target-dimension scope;
- policy decision;
- consent;
- cultural rights;
- transfer purpose;
- profile;
- deadline and freshness.

Authentication alone does not authorize transfer.

### 9.2 Secrets and sensitive data

Requests and manifests use managed credential references when credentials are required.

Ordinary logs and receipts contain:

- canonical references;
- status;
- reason codes;
- timing;
- sizes;
- integrity record references;
- correlation identities.

They exclude unrestricted media payloads, secrets, raw keys, and unrelated metadata.

### 9.3 Component boundaries

| Component | Direction | Purpose | Authority boundary |
| --- | --- | --- | --- |
| Source component | Inbound | Read selected source object and current source state | Source remains authoritative |
| Identity and Trust | Bidirectional | Verify subjects, services, signers, and trust | Identity and trust remain external authority |
| Governance Policy Runtime | Bidirectional | Verify authorization, consent, cultural rights, and obligations | Policy authority remains external |
| Resource Governor | Bidirectional | Admit and protect resources | Resource authority remains external |
| UCKK Platform | Outbound | Request destination validation and admission | UCKK Platform owns admitted media |
| Audit Broker | Outbound | Store protected transfer receipts and evidence | Audit ownership remains external |
| kOA Node Agent | Outbound | Use bounded privileged media or device operations | Host privilege remains external |
| Publication Gateway | Separate workflow | Govern cross-domain publication | No substitution or shared contract |
| Registered external adapter | Separate workflow | Produce optional candidate media | Output remains non-authoritative |

Direct database access is prohibited in every row.

### 9.4 External AI boundary

Suno and Gamma are optional external adapters. Their output enters a local candidate workflow with provider provenance.

The gateway performs no native AI. It does not call an external AI provider implicitly. A user selects the returned candidate before a dimension-transfer request begins.

### 9.5 Audit and recourse

Critical receipts include:

- transfer request;
- admission;
- duplicate result;
- conflict;
- cancellation;
- withdrawal;
- failure;
- recovery.

A person or authorized representative can challenge selection, rights, destination, duplicate handling, admission, or withdrawal through the registered recourse process. The gateway preserves the challenged transfer and evidence references.

### 9.6 Publication separation

Transfer into a UCKK dimension is not cross-domain publication.

When a later workflow publishes admitted UCKK media, Publication Gateway receives a separate request and evaluates the applicable disclosure authority. The prior dimension-transfer receipt does not grant publication permission.

## 10. Lifecycle, Exceptions, and Validation

### 10.1 Startup and readiness

Startup:

1. resolves the active profile and component contract;
2. verifies the transfer ledger;
3. verifies staging and quarantine storage;
4. reconstructs incomplete transfers;
5. verifies destination and authority interfaces;
6. reconciles unknown destination outcomes;
7. resumes receipt delivery;
8. reports readiness and degraded capabilities.

Readiness distinguishes local transfer availability from external adapter availability.

### 10.2 Shutdown and upgrade

Shutdown stops new requests, completes or durably suspends accepted work, flushes the ledger and outbox, and preserves staging references.

Upgrade verifies:

- contract compatibility;
- ledger migration;
- staging compatibility;
- integrity-record compatibility;
- destination contract compatibility;
- rollback or forward repair;
- profile tests.

A new implementation does not validate itself through its own unchecked behavior.

### 10.3 Deactivation and replacement

Deactivation resolves:

- active requests;
- staged candidates;
- unknown destination outcomes;
- withdrawal obligations;
- receipt delivery;
- retained evidence;
- profile capability claims.

Replacement preserves transfer identities and compatibility where supported. Historical receipts remain immutable.

### 10.4 Exceptions

A bounded exception can adjust a profile-specific size limit, concurrency value, storage adapter, retry interval, evidence source, compatibility interval, or test environment.

An exception cannot:

- merge the gateway with Publication Gateway;
- transfer ownership of admitted UCKK media;
- permit direct destination database writes;
- remove explicit user selection;
- bypass consent or cultural rights;
- treat an integrity match as admission;
- introduce native AI;
- make external AI output authoritative;
- conceal incomplete or unknown destination state;
- permit secret leakage;
- claim conformance without current tests and evidence.

### 10.5 Validation criteria

This document is conformant when validation confirms:

1. the component identity and active contract match;
2. one gateway owns each transfer ledger record;
3. source and destination ownership remain separate;
4. Publication Gateway and UCKK Dimension Gateway remain separate;
5. every transfer begins from explicit selection or authorized workflow action;
6. request schemas are closed;
7. request identity binds to one canonical body;
8. source, target, profile, policy, consent, and rights references resolve;
9. candidate media enters staging before destination admission;
10. integrity verification is functional and provenance-preserving;
11. integrity matches do not create semantic authority;
12. UCKK Platform performs destination acceptance;
13. no direct cross-component database write exists;
14. completion requires destination verification, reconciliation, and durable receipt;
15. retry and resume prevent duplicate authoritative effects;
16. conflict handling preserves all relevant states;
17. cancellation and withdrawal preserve policy and evidence;
18. logs, receipts, and manifests exclude secrets and unrelated content;
19. local transfer behavior passes without external AI;
20. offline-transfer validation covers manifests, trust, integrity, replay, compatibility, policy, rights, and ownership;
21. resource and queue bounds exist for every applicable profile;
22. startup, restart, upgrade, deactivation, and recovery are tested;
23. all decisions, requirements, locks, profiles, components, interfaces, artifacts, integrations, tests, and evidence resolve;
24. no prohibited open-state marker or implicit authority enters the active contract.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_component_boundaries.py
tools/check_interfile_locks.py
tools/check_artifact_contracts.py
tools/check_profile_inheritance.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_generated_content.py
tools/check_no_unresolved_state.py
```

## 11. Non-Normative Examples

### 11.1 Local media transfer

A user selects a locally owned audio object and a target UCKK dimension. The gateway verifies the source, policy, rights, target, resources, and integrity, stages the candidate, and asks UCKK Platform to admit it. UCKK Platform returns the destination object reference.

### 11.2 Duplicate media

The gateway detects a matching content digest. It does not complete the transfer automatically. UCKK Platform determines whether the existing object is equivalent under destination metadata, rights, and version rules.

### 11.3 Suno candidate

A user explicitly invokes the registered Suno adapter. The returned audio retains provider provenance and remains candidate material. The user then selects it for transfer through UCKK Dimension Gateway.

### 11.4 Publication after admission

Media is admitted into a UCKK dimension. A later external-publication request goes through Publication Gateway with a separate policy decision and receipt. The dimension-transfer result does not authorize publication.

### 11.5 Offline bundle

A sovereign-offline node receives a signed bundle containing selected media. The bundle is quarantined, verified, checked for replay and compatibility, and submitted to UCKK Platform through the normal destination admission contract.

### 11.6 Interrupted destination call

The process stops after submitting a candidate but before recording the result. On restart, the gateway queries the destination by idempotency identity and reconciles the actual state before retrying.

### 11.7 Consent withdrawal

Consent is withdrawn while a candidate is staged. The gateway stops processing, removes or retires staged material under policy, records the withdrawal, and does not submit the candidate.

### 11.8 Resource pressure

Staging storage reaches its reserve threshold. The gateway completes withdrawals and reconciliation, cleans expired candidates, pauses optional transformations, and rejects new large transfers before endangering receipts or existing staged work.
