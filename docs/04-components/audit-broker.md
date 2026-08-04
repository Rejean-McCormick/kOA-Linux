<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "audit_broker"
  ],
  "canonical_refs": [
    "contracts/components/audit-broker.component.json",
    "generated/component-catalog.json#/components/audit_broker",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/resource_governance",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "schemas/test-evidence.schema.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-COMP-AUDIT-001",
    "REQ-COMP-AUDIT-002",
    "REQ-COMP-AUDIT-003",
    "REQ-COMP-AUDIT-004",
    "REQ-COMP-AUDIT-005",
    "REQ-COMP-AUDIT-006",
    "REQ-COMP-AUDIT-007",
    "REQ-COMP-AUDIT-008",
    "REQ-COMP-AUDIT-009",
    "REQ-COMP-AUDIT-010",
    "REQ-COMP-AUDIT-011",
    "REQ-COMP-AUDIT-012",
    "REQ-COMP-AUDIT-013",
    "REQ-COMP-AUDIT-014",
    "REQ-COMP-AUDIT-015",
    "REQ-COMP-AUDIT-016",
    "REQ-COMP-AUDIT-017",
    "REQ-COMP-AUDIT-018",
    "REQ-COMP-AUDIT-019",
    "REQ-COMP-AUDIT-020",
    "REQ-COMP-AUDIT-021",
    "REQ-COMP-AUDIT-022",
    "REQ-COMP-AUDIT-023",
    "REQ-COMP-AUDIT-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-AI-001",
    "LOCK-AI-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000"
  ],
  "tags": [
    "audit_broker",
    "selective_audit",
    "evidence",
    "private_proof",
    "recourse",
    "chain_of_custody",
    "retention",
    "disclosure",
    "component_separation",
    "non_ai"
  ]
}
KOA:DOC-META:END -->

# Audit Broker

## 1. Purpose

The Audit Broker provides selective, bounded, and verifiable accountability for critical kOA actions and claims.

It accepts declared audit events, receipts, and evidence references from authenticated producers. It validates and retains the minimum audit material needed for an authorized purpose, maintains chain of custody, executes bounded audit queries, and creates minimized disclosure packages and machine-readable receipts.

The Audit Broker is not a universal event lake, surveillance system, source-data replica, policy engine, privilege broker, release controller, or publication gateway. It owns audit records and audit-disclosure state only. The source component retains authority over the operation and data being observed.

The canonical component contract is `contracts/components/audit-broker.component.json`.

## 2. Scope

This document applies to:

- Audit Broker ingestion, validation, retention, query, disclosure, invalidation, archival, and disposition behavior;
- registered component submissions;
- policy decisions used for governed audit access;
- chain-of-custody records;
- audit access, denial, disclosure, retention, and disposition receipts;
- private-proof, redaction, pseudonymization, and aggregation workflows;
- profile-conditioned integrity, signing, storage, backup, restore, and recovery;
- offline and disconnected audit operation;
- Audit Broker conformance claims, tests, and evidence.

This document does not define:

- source-component event semantics beyond registered submission contracts;
- source business or tenant data;
- identity and trust authority;
- authorization, consent, exception, or privilege policy;
- component resource-allocation policy;
- release, artifact, or publication authority;
- test definitions or evidence validity;
- profile membership;
- external-provider processing.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/components/audit-broker.component.json` | Audit Broker responsibilities, authority, data, interfaces, security, lifecycle, failure behavior, and conformance |
| `generated/component-catalog.json#/components/audit_broker` | Component identity, class, and registry membership |
| `contracts/system.contract.json#/global_boundaries` | Component, data, privilege, and implementation boundaries |
| `contracts/system.contract.json#/resource_governance` | Resource Governor and Governance Policy Runtime separation |
| `generated/profile-catalog.json` | Profile and overlay membership |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | System, component, data, governance, lifecycle, and AI invariants |
| `generated/traceability.json` | Links among claims, decisions, requirements, tests, and evidence |
| `generated/test-catalog.json` | Registered Audit Broker tests |
| `generated/evidence-catalog.json` | Registered evidence and validity |
| `schemas/test-evidence.schema.json` | Structure of individual test-evidence records |
| `contracts/artifact-classes.contract.json` | Receipt, evidence, integrity, signing, retention, and recovery classes |

## 4. Model and Responsibilities

### 4.1 Component identity

The canonical identifier is `audit_broker`. The component class is `accountability_and_evidence_service`.

Its central principle is selective accountability: preserve enough verified evidence for accountability, conformance, investigation, and recourse without copying all source data or expanding disclosure authority.

### 4.2 Owned and excluded authority

The Audit Broker owns:

- audit-record identity;
- accepted audit-event records;
- event-validation results;
- retention and hold state for its records;
- audit-query execution state;
- disclosure packages;
- access, denial, disclosure, and disposition receipts;
- redaction results;
- chain-of-custody records.

It does not own source-component authoritative state, source business data, identity, policy, privilege, resources, release compatibility, publication, test definitions, or evidence validity.

Copying a reference, receipt, digest, or bounded field set does not transfer source authority.

### 4.3 Primary responsibilities

The component:

- accepts registered audit event classes;
- validates producer identity, schema, scope, purpose, classification, and retention;
- preserves bounded records;
- maintains chain of custody;
- executes authorized deterministic queries;
- minimizes and transforms disclosure output;
- records access and disclosure outcomes;
- supports authorized review and recourse;
- enforces retention, holds, archival, and disposition;
- exposes bounded health and readiness.

### 4.4 Authoritative entities

<!-- GENERATED:BEGIN
source=contracts/components/audit-broker.component.json#/data_model/authoritative_entities
renderer=canonical-table-v1
-->
| Entity | Purpose | Required fields |
| --- | --- | --- |
| `audit_record` | Accepted bounded record of one registered auditable event. | `audit_record_id`, `event_class_id`, `producer_component_id`, `producer_identity`, `occurred_at`, `received_at`, `subject_references`, `action_or_transition`, `outcome`, `purpose`, `classification`, `retention_class`, `correlation_id`, `source_receipt_or_evidence_refs` |
| `audit_access_receipt` | Record of an allowed, denied, partial, cancelled, expired, or failed access request. | `receipt_id`, `request_id`, `requester_identity`, `purpose`, `policy_decision_ref`, `requested_scope`, `effective_scope`, `outcome`, `occurred_at` |
| `audit_disclosure_package` | Minimized result of one authorized audit disclosure operation. | `package_id`, `request_id`, `purpose`, `scope`, `record_refs`, `redaction_profile`, `generated_at`, `expiry_or_validity`, `chain_of_custody_ref` |
| `audit_chain_of_custody` | Ordered record of material transitions affecting an audit record or disclosure package. | `chain_id`, `subject_ref`, `transition_type`, `actor_or_component_identity`, `occurred_at`, `result`, `receipt_ref` |
| `audit_retention_state` | Current retention, hold, archive, or disposition state of an Audit Broker-owned record. | `record_ref`, `retention_class`, `state`, `effective_at`, `policy_or_hold_ref`, `next_review_or_disposition_at` |
<!-- GENERATED:END -->

The record lifecycle includes `received`, `validated`, `accepted`, `quarantined`, `retained`, `held`, `archived`, `expired`, `disposed`, and `invalidated`.

A correction appends lineage. It does not silently replace accepted history.

### 4.5 Registered event classes

<!-- GENERATED:BEGIN
source=contracts/components/audit-broker.component.json#/registered_event_classes
renderer=canonical-table-v1
-->
| Event class | Registered producer references | Minimum content | Full source payload required |
| --- | --- | --- | ---: |
| `policy_decision_event` | `generated/component-catalog.json#/components/governance_policy_runtime` | `decision_ref`, `decision_outcome`, `scope`, `purpose`, `actor_or_subject_refs`, `occurred_at` | No |
| `privileged_operation_event` | `generated/component-catalog.json#/components/koa_node_agent` | `operation_class`, `authorization_ref`, `target_ref`, `outcome`, `receipt_ref`, `occurred_at` | No |
| `artifact_activation_event` | `generated/component-catalog.json#/components/koa_node_agent` | `artifact_class_id`, `artifact_id`, `previous_artifact_id`, `release_set_ref`, `outcome`, `receipt_ref`, `occurred_at` | No |
| `publication_event` | `generated/component-catalog.json#/components/publication_gateway` | `publication_request_ref`, `source_domain_ref`, `destination_scope`, `policy_decision_ref`, `outcome`, `publication_receipt_ref`, `occurred_at` | No |
| `integration_import_event` | `generated/component-catalog.json` | `integration_id`, `owning_component_id`, `candidate_artifact_ref`, `acceptance_outcome`, `provenance_ref`, `occurred_at` | No |
| `test_or_evidence_event` | `generated/test-catalog.json`<br>`generated/evidence-catalog.json` | `test_id`, `evidence_id`, `subject_ref`, `outcome`, `validity_state`, `occurred_at` | No |
| `security_or_incident_event` | `generated/component-catalog.json` | `event_type`, `source_component_id`, `severity`, `subject_refs`, `outcome_or_state`, `occurred_at` | No |
| `audit_access_or_disclosure_event` | `generated/component-catalog.json#/components/audit_broker` | `request_id`, `requester_identity`, `purpose`, `policy_decision_ref`, `effective_scope`, `outcome`, `receipt_ref`, `occurred_at` | No |
<!-- GENERATED:END -->

The default submission contains metadata and declared receipt or evidence references. Full source payload collection is not the default.

### 4.6 Commands and queries

<!-- GENERATED:BEGIN
source=contracts/components/audit-broker.component.json#/interfaces/commands
renderer=canonical-table-v1
-->
| Command | Caller | Request fields | Responses | Additional condition |
| --- | --- | --- | --- | --- |
| `submit_audit_event` | `registered_component` | `event_class_id`, `producer_identity`, `event_payload`, `classification`, `purpose`, `retention_class`, `correlation_id` | `accepted`, `rejected`, `quarantined` | idempotency key |
| `request_audit_disclosure` | `authorized_actor_or_component` | `request_id`, `requester_identity`, `purpose`, `requested_scope`, `subject_or_record_selectors`, `desired_output_class`, `expiry` | `allowed`, `partially_allowed`, `denied`, `expired`, `failed` | policy decision |
| `apply_retention_action` | `authorized_lifecycle_or_policy_component` | `record_selectors`, `action`, `policy_or_hold_ref`, `effective_at` | `applied`, `partially_applied`, `denied`, `failed` | receipt |
| `invalidate_audit_record` | `source_component_or_authorized_governance_actor` | `record_ref`, `source_correction_or_retraction_ref`, `reason`, `effective_at` | `invalidated`, `denied`, `not_found`, `failed` | append-only invalidation |
<!-- GENERATED:END -->

<!-- GENERATED:BEGIN
source=contracts/components/audit-broker.component.json#/interfaces/queries
renderer=canonical-table-v1
-->
| Query | Authorization | Default result |
| --- | ---: | --- |
| `get_audit_record_metadata` | Required | `metadata_only` |
| `get_audit_request_status` | Required | `status_without_protected_content` |
| `get_audit_health` | Required | `bounded_health_and_readiness` |
<!-- GENERATED:END -->

All component interfaces are versioned. Direct database access and unregistered interfaces are outside the contract.

### 4.7 Disclosure model

An audit request identifies a requester, purpose, requested scope, record selectors, output class, and expiry.

The disclosure path uses Governance Policy Runtime for governed authorization. The resulting policy decision constrains purpose, subjects, records, fields, rights, consent, exceptions, validity, and delivery.

The Audit Broker then applies minimization, redaction, pseudonymization, aggregation, or private-proof processing. It cannot broaden the policy scope.

Cross-domain publication remains a separate Publication Gateway operation.

### 4.8 Security and privacy model

Component submissions use authenticated identities and replay protection. Mutating commands use idempotency controls. Transport protection, storage protection, integrity, and signing depend on active profile and artifact requirements.

Audit data remains purpose-bound. Routine health output does not contain protected record content.

Break-glass access uses a separate governed procedure with actor, scope, duration, review, and receipt constraints. It does not silently bypass normal authority.

Cultural-rights, consent, privacy, disclosure, hold, and recourse constraints remain attached to records and packages.

### 4.9 Resource, retention, and integrity model

Resource Governor limits ingestion, validation workers, query workers, redaction workers, package size, storage growth, retention work, temporary export space, and outbound bandwidth.

Retention is explicit. Holds prevent disposition. Disposition checks authorization, expiry, references, dependencies, and chain of custody.

Integrity failures quarantine affected material and invalidate dependent claims. Corrections use append-only lineage.

### 4.10 External integration boundary

The Audit Broker has no native or automatic external AI path.

ChatGPT, Suno, Gamma, and the approved Ariane voice adapter do not receive automatic audit content and do not perform event classification, summarization, redaction, disclosure selection, policy decisions, or evidence-validity decisions for this component.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-AUDIT-001,REQ-COMP-AUDIT-002,REQ-COMP-AUDIT-003,REQ-COMP-AUDIT-004,REQ-COMP-AUDIT-005,REQ-COMP-AUDIT-006,REQ-COMP-AUDIT-007,REQ-COMP-AUDIT-008,REQ-COMP-AUDIT-009,REQ-COMP-AUDIT-010,REQ-COMP-AUDIT-011,REQ-COMP-AUDIT-012,REQ-COMP-AUDIT-013,REQ-COMP-AUDIT-014,REQ-COMP-AUDIT-015,REQ-COMP-AUDIT-016,REQ-COMP-AUDIT-017,REQ-COMP-AUDIT-018,REQ-COMP-AUDIT-019,REQ-COMP-AUDIT-020,REQ-COMP-AUDIT-021,REQ-COMP-AUDIT-022,REQ-COMP-AUDIT-023,REQ-COMP-AUDIT-024 -->
- **REQ-COMP-AUDIT-001 — SHALL:** The Audit Broker shall accept only registered, authenticated, versioned, and schema-valid audit event classes.
- **REQ-COMP-AUDIT-002 — SHALL:** Each accepted audit record shall identify its producer, event class, subjects, action or transition, outcome, purpose, classification, retention class, correlation identifier, and applicable receipt or evidence references.
- **REQ-COMP-AUDIT-003 — SHALL:** The Audit Broker shall collect only the fields and evidence references required for the declared accountability, recourse, retention, investigation, or conformance purpose.
- **REQ-COMP-AUDIT-004 — SHALL NOT:** The Audit Broker shall not acquire source-component authority through observation, copying, caching, indexing, storage, or disclosure.
- **REQ-COMP-AUDIT-005 — SHALL NOT:** The Audit Broker shall not write directly to another component's authoritative source tables.
- **REQ-COMP-AUDIT-006 — SHALL:** Governed audit disclosure shall require an applicable Governance Policy Runtime decision that identifies requester, purpose, scope, consent, rights, exceptions, and validity conditions.
- **REQ-COMP-AUDIT-007 — SHALL NOT:** The Audit Broker shall not broaden, infer, replace, or override the scope of a policy decision.
- **REQ-COMP-AUDIT-008 — SHALL:** An audit disclosure shall minimize records and fields and shall apply authorized redaction, pseudonymization, aggregation, or private-proof techniques before delivery.
- **REQ-COMP-AUDIT-009 — SHALL:** Every audit access or disclosure attempt shall produce a machine-readable receipt recording the request, policy decision, effective scope, outcome, and time.
- **REQ-COMP-AUDIT-010 — SHALL:** The Audit Broker shall preserve an ordered chain of custody for material ingestion, validation, redaction, access, disclosure, hold, archive, invalidation, export, and disposition transitions.
- **REQ-COMP-AUDIT-011 — SHALL:** Each Audit Broker-owned record shall have an explicit retention class and resolvable policy or contract reference.
- **REQ-COMP-AUDIT-012 — SHALL:** A legal, cultural-rights, consent, or governance hold shall prevent disposition until an authorized release of the hold is recorded.
- **REQ-COMP-AUDIT-013 — SHALL:** Disposition shall verify authorization, retention expiry, holds, references, dependencies, and chain-of-custody updates before deleting or rendering an Audit Broker-owned record inaccessible.
- **REQ-COMP-AUDIT-014 — SHALL NOT:** Audit-record disposition shall not delete, rewrite, or invalidate source-component data.
- **REQ-COMP-AUDIT-015 — SHALL:** Corrections and retractions shall be represented by append-only correction or invalidation records rather than silent mutation of accepted audit history.
- **REQ-COMP-AUDIT-016 — SHALL:** Integrity or signature verification shall be applied when required by the active profile, artifact class, trust scope, or evidence contract.
- **REQ-COMP-AUDIT-017 — SHALL:** Detected integrity failure shall quarantine the affected record or package, update chain of custody, and block claims that depend on the affected material.
- **REQ-COMP-AUDIT-018 — SHALL:** Resource Governor shall bound audit ingestion, validation, queries, redaction, disclosure package size, storage growth, retention work, temporary export space, and outbound bandwidth.
- **REQ-COMP-AUDIT-019 — SHALL:** Under resource pressure, the Audit Broker shall preserve critical transition receipts, policy and access receipts, chain of custody, operator control, and previously valid records before noncritical indexing or disclosure work.
- **REQ-COMP-AUDIT-020 — SHALL:** Routine health output, metrics, and logs shall exclude protected record content, secrets, and unnecessary subject identifiers.
- **REQ-COMP-AUDIT-021 — SHALL NOT:** The Audit Broker shall use native or automatic external AI for event classification, summarization, redaction, disclosure selection, policy decisions, or evidence-validity decisions.
- **REQ-COMP-AUDIT-022 — SHALL:** Offline and disconnected operation shall preserve locally authorized ingestion, records, queries, receipts, and bounded queues without expanding disclosure authority or recording undelivered packages as delivered.
- **REQ-COMP-AUDIT-023 — SHALL:** Backup, restore, and recovery shall preserve audit records, receipts, retention and hold state, chain of custody, schema state, and required component configuration without partial authority.
- **REQ-COMP-AUDIT-024 — SHALL:** Every active Audit Broker claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Audit-event ingestion

1. Receive a submission through `submit_audit_event`.
2. Authenticate the producer.
3. Validate the event class and interface version.
4. Validate schema, time, purpose, classification, retention class, correlation identifier, and idempotency key.
5. Validate required receipt or evidence references.
6. Minimize the accepted field set.
7. Reject, quarantine, or accept the submission.
8. Create the Audit Broker-owned record.
9. Add chain-of-custody state.
10. Emit the applicable acceptance, rejection, or quarantine event.

Source-component state remains unchanged.

### 6.2 Audit disclosure

1. Receive `request_audit_disclosure`.
2. Authenticate the requester and validate request expiry.
3. Resolve requested records and subjects.
4. obtain or validate the applicable Governance Policy Runtime decision;
5. apply purpose, consent, rights, exception, and scope constraints;
6. retrieve source content separately only when authorized and necessary;
7. minimize records and fields;
8. apply redaction, pseudonymization, aggregation, or private-proof processing;
9. verify chain of custody;
10. create the bounded disclosure package;
11. create access and disclosure receipts;
12. deliver through the authorized local interface or Publication Gateway.
13. record delivery success only after confirmed delivery.

A partial authorization creates a partial package and records the reduced effective scope.

### 6.3 Retention and hold transition

1. Resolve the target records.
2. authenticate the lifecycle or policy authority;
3. validate the retention, hold, archive, release, expiry, or disposition action;
4. verify active holds and dependencies;
5. update Audit Broker-owned retention state;
6. update chain of custody;
7. create a transition receipt;
8. emit the retention-state event.

A hold remains active until its authorized release is recorded.

### 6.4 Correction or invalidation

1. Receive `invalidate_audit_record`.
2. verify source-component or governance authority;
3. resolve the original record.
4. validate the correction or retraction reference.
5. append an invalidation or correction record.
6. preserve the original record according to retention requirements.
7. update chain of custody and dependent evidence status.
8. block unsupported claims.
9. emit the invalidation event.

### 6.5 Startup and readiness

1. Validate configuration and contract versions.
2. initialize component identity.
3. open the record store.
4. resolve retention policies.
5. activate resource limits.
6. initialize chain-of-custody and receipt generation.
7. verify identity and policy decision paths.
8. expose readiness only for available capabilities.
9. declare degraded state explicitly when a dependency is unavailable.

### 6.6 Backup, restore, and recovery

1. Create a profile-authorized recovery point.
2. include records, receipts, retention and hold state, chain of custody, schema state, and rebuild configuration;
3. verify backup integrity and signatures when applicable;
4. restore into an isolated target;
5. validate schema and trust scope;
6. preserve retention and hold state;
7. validate record and chain-of-custody consistency;
8. activate recovered state without partial authority;
9. create a recovery receipt;
10. complete post-restore tests.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Invalid submission | Reject the submission and leave source-component state unchanged. | Previously accepted audit records and source authority | Authority or evidence claim based on the rejected submission |
| Untrusted producer | Reject or quarantine the record without granting record authority. | Existing trusted records | Use of the untrusted record |
| Governance Policy Runtime unavailable | Block new governed disclosures and preserve existing records. | Storage, chain of custody, and independently authorized ingestion | New policy-conditioned disclosure |
| Identity or trust unavailable | Block new authenticated submissions and disclosure requests. | Existing records and bounded health state | Identity-dependent mutation or access |
| Storage pressure | Reduce noncritical ingestion and indexing, prioritize critical receipts, and enter read-only mode before integrity risk. | Critical receipts, chain of custody, and valid records | Additional noncritical growth |
| Integrity failure | Quarantine affected material, update chain of custody, and block dependent claims. | Unaffected valid records | Use of affected material |
| Source component unavailable | Return locally retained records and references within existing authority; mark source-content retrieval partial or blocked. | Audit Broker-owned records | Inferred or fabricated source authority |
| Disclosure delivery failure | Retain the package as undelivered or failed and do not record successful disclosure. | Package and access receipts | False delivery claim |
| Audit Broker unavailable | Preserve source-component authority; block transitions whose contracts require an Audit Broker receipt unless an explicitly authorized bounded local receipt path exists. | Source-component state and unrelated operation | Unsupported audit or conformance claim |

Failure never grants broader collection, retention, access, disclosure, publication, or source authority.

## 8. Cross-Component Interactions

| Component or owner | Interaction | Audit Broker responsibility | Retained external authority |
| --- | --- | --- | --- |
| Source component | Submit a registered event, receipt, evidence reference, correction, or retraction | Validate and preserve the bounded audit record | Source event semantics and source state |
| Identity and Trust | Verify producer, requester, signer, trust scope, and revocation | Consume verification result | Identity and trust authority |
| Governance Policy Runtime | Return authorization, purpose, disclosure, consent, exception, retention override, or hold-release decision | Apply the decision without broadening it | Policy authority |
| Resource Governor | Apply CPU, memory, I/O, queue, worker, storage, and bandwidth limits | Classify work and respect limits | Resource authority |
| Publication Gateway | Deliver authorized cross-domain evidence | Create the bounded package and disclosure receipt | Publication authority |
| kOA Node Agent | Submit privileged-operation and activation receipts | Validate and retain registered event records | Node-local execution and privilege path |
| Evidence registry | Register evidence identity and validity | Preserve evidence references and relevant audit events | Evidence validity |
| Test catalog | Define test identity and expected evidence | Preserve test and evidence event references | Test definition |
| Consumer or reviewer | Request authorized access or recourse package | Execute bounded query and produce receipts | Acceptance or adjudication outside Audit Broker scope |

No interaction provides direct access to another component's source tables.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Accountability operates inside the local-first, modular, explicit-authority system baseline. |
| `DEC-DATA-001` | Logical source ownership remains with each component and direct cross-component source writes are prohibited. |
| `DEC-GOV-001` | Governance Policy Runtime owns policy decisions and Resource Governor owns resource control. |
| `DEC-REL-001` | Receipts, evidence, and lifecycle artifacts use registered classes and release compatibility. |
| `DEC-AI-001` | Native and automatic external AI do not perform authoritative audit processing. |

### Prohibited assumptions

- Audit visibility grants source authority.
- Copying data transfers ownership.
- A shared physical database permits cross-component writes.
- The Audit Broker is the policy engine.
- The Audit Broker can grant privilege.
- An administrator identity has unlimited audit access.
- Collection purpose may be inferred after ingestion.
- Every available field should be retained.
- Full source payload is the default audit record.
- A disclosure request is self-authorizing.
- Redaction can broaden the authorized record set.
- A denied request may omit a receipt.
- A correction silently rewrites accepted history.
- Retention may be inferred from storage availability.
- A hold can be ignored during cleanup.
- Disposition of an audit copy deletes source data.
- Health metrics may expose protected content.
- An external AI service can classify, summarize, redact, or decide disclosure automatically.
- Audit Broker failure transfers audit responsibility or source authority to another component.
- Missing evidence can be replaced by operator confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-COMP-005`, status `active`, language `en`, component layer, and `audit_broker` scope.
2. All eleven required sections exist in numerical order.
3. The event-class projection matches `contracts/components/audit-broker.component.json#/registered_event_classes`.
4. The command and query projections match the canonical component contract.
5. The authoritative-entity projection matches the canonical component contract.
6. Every decision ID is accepted in `generated/decision-index.json`.
7. Every requirement ID appears exactly once in `generated/requirements-index.json`.
8. Every lock ID resolves to an active lock.
9. `TEST-COMP-AUDIT-001` verifies registered, authenticated, schema-valid event ingestion.
10. `TEST-COMP-AUDIT-002` verifies source authority preservation and absence of direct source-store access.
11. `TEST-COMP-AUDIT-003` verifies field and record minimization.
12. `TEST-COMP-AUDIT-004` verifies governed disclosure and inability to broaden policy scope.
13. `TEST-COMP-AUDIT-005` verifies redaction, pseudonymization, aggregation, and private-proof output.
14. `TEST-COMP-AUDIT-006` verifies access, denial, partial-disclosure, failure, retention, and disposition receipts.
15. `TEST-COMP-AUDIT-007` verifies complete chain of custody.
16. `TEST-COMP-AUDIT-008` verifies retention, holds, archival, and disposition without source-data deletion.
17. `TEST-COMP-AUDIT-009` verifies integrity-failure quarantine and dependent-claim blocking.
18. `TEST-COMP-AUDIT-010` verifies safe degradation under policy, identity, source, storage, delivery, and connectivity failures.
19. `TEST-COMP-AUDIT-011` verifies protected content remains absent from routine health and logs.
20. `TEST-COMP-AUDIT-012` verifies absence of native or automatic external AI processing.
21. `TEST-COMP-AUDIT-013` verifies backup and restore without partial authority.
22. `TEST-COMP-AUDIT-014` verifies complete traceability to decisions, requirements, locks, tests, and evidence.
23. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
24. The generated requirement block matches the canonical requirement registry.
25. Generated tables match the canonical component contract and contain no manual semantic changes.

These criteria define validation requirements. They do not claim that a deployed Audit Broker already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** Governance Policy Runtime records a disclosure denial. The Audit Broker stores the decision reference, actor and subject references, purpose, effective scope, outcome, and time. It does not copy the protected source content.

> **Non-normative example:** A reviewer requests evidence for one artifact activation. Policy permits the activation receipt, artifact identity, target profile, outcome, and chain of custody but not unrelated node logs. The resulting package contains only the permitted fields.

> **Non-normative example:** A source component retracts an incorrect event. The Audit Broker appends an invalidation record linked to the source correction. The original audit record remains available according to retention policy and is no longer used for unsupported claims.

> **Non-normative example:** Storage pressure increases. Nonurgent indexing and disclosure work is deferred. Critical policy, privilege, activation, publication, access, and chain-of-custody receipts retain priority.

> **Non-normative example:** A disclosure package is created while the delivery destination is unreachable. The package remains local with an undelivered state. No successful disclosure receipt is produced.

> **Non-normative example:** An operator asks ChatGPT to summarize all protected audit records automatically. The Audit Broker has no such integration path. Any separately authorized human workflow remains outside automatic component processing and cannot replace policy, minimization, or evidence-validity controls.
