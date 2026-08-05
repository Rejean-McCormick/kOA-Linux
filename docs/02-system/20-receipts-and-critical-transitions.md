<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-020",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/publication-gateway.component.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SYS-RCT-001",
    "REQ-SYS-RCT-002",
    "REQ-SYS-RCT-003",
    "REQ-SYS-RCT-004",
    "REQ-SYS-RCT-005",
    "REQ-SYS-RCT-006",
    "REQ-SYS-RCT-007",
    "REQ-SYS-RCT-008",
    "REQ-SYS-RCT-009",
    "REQ-SYS-RCT-010",
    "REQ-SYS-RCT-011",
    "REQ-SYS-RCT-012",
    "REQ-SYS-RCT-013",
    "REQ-SYS-RCT-014",
    "REQ-SYS-RCT-015",
    "REQ-SYS-RCT-016",
    "REQ-SYS-RCT-017",
    "REQ-SYS-RCT-018",
    "REQ-SYS-RCT-019",
    "REQ-SYS-RCT-020",
    "REQ-SYS-RCT-021",
    "REQ-SYS-RCT-022",
    "REQ-SYS-RCT-023",
    "REQ-SYS-RCT-024"
  ],
  "lock_ids": [
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-003",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-019"
  ],
  "tags": [
    "system",
    "receipts",
    "critical-transitions",
    "evidence",
    "audit",
    "selective-disclosure",
    "activation",
    "rollback",
    "publication",
    "privilege",
    "recovery",
    "traceability"
  ]
}
KOA:DOC-META:END -->

# Receipts and Critical Transitions

## 1. Purpose

This document defines the kOA system model for machine-readable receipts and critical transitions.

A receipt is a durable, structured account of a decision or state transition produced by the component responsible for that decision or transition. It supports accountability, recovery, validation, selective audit, recourse, migration, and conformance without turning every application event into constitutional evidence.

The model exists to ensure that:

- protected actions have truthful machine-readable outcomes;
- authorization and execution are not confused;
- successful preparation is not confused with authoritative commit;
- failed or denied operations are not represented as success;
- cross-component transitions remain traceable without merging component authority;
- private evidence can remain protected while public or ordinary receipt views remain useful;
- lifecycle activation and rollback can be reconstructed;
- external integrations and AI surfaces preserve provenance;
- recovery and recourse can identify what happened, why, and under which authority;
- receipt storage does not become a universal operational database.

Receipts complement logs, metrics, traces, notifications, and evidence records. They do not replace those mechanisms.

## 2. Scope

This document applies globally to critical transitions involving:

- policy authorization;
- privilege grants and privileged operations;
- break-glass activation, use, expiration, and closure;
- governed publication and cross-domain disclosure;
- controlled external data transfer;
- external AI requests and authoritative acceptance of returned candidates;
- UCKK publication, export, re-import, deletion, restoration, and publication handoff;
- artifact and release verification;
- activation, rollback, forward repair, supersession, and recovery;
- backup restoration;
- authoritative data migration;
- trust-root, certificate-authority, or revocation changes;
- governed host mutation;
- documentation authority cutover and rollback;
- approved exceptions and waivers when they affect a protected transition;
- access to restricted evidence where accountability is required.

The model applies across user, developer, service, maintenance, recovery, offline, degraded, and break-glass contexts.

The model does not classify every event as critical. Routine reads, ordinary interface navigation, transient health samples, internal debug events, cache activity, and non-authoritative display changes remain ordinary telemetry unless a canonical policy explicitly elevates a specific action.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/integration-types.contract.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/exception-index.json
contracts/components/audit-broker.component.json
contracts/components/governance-policy-runtime.component.json
contracts/components/publication-gateway.component.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `system.registry.json#/receipts_and_critical_transitions` | Global receipt classes, critical-transition classes, required fields, and state model |
| `components.registry.json` | Component identity and responsibility boundaries |
| `release-channels.registry.json` | Release-channel identities involved in lifecycle receipts |
| `artifact-classes.registry.json` | Artifact identities, activation behavior, and recovery classes |
| `integrations.registry.json` | External transfer and integration classifications |
| `test-catalog.registry.json` | Receipt and transition test definitions |
| `evidence.registry.json` | Evidence identity, location, validity, and protection |
| `requirements.registry.json` | Normative receipt requirements |
| `locks.registry.json` | Data, authority, gateway, lifecycle, and identifier invariants |
| `traceability.registry.json` | Links among transitions, receipts, requirements, tests, and evidence |
| `exceptions.registry.json` | Bounded deviations and conformance effects |
| `audit-broker.component.json` | Receipt collection, indexing, verification, disclosure, and export behavior |
| `governance-policy-runtime.component.json` | Governance decision production where deployed |
| `publication-gateway.component.json` | Publication and disclosure decision receipts |

This document explains the system model. It does not own individual receipt instances or replace component-specific transition contracts.

## 4. Model and Responsibilities

### 4.1 Receipt, log, evidence, and notification

| Object | Purpose | Canonical treatment |
| --- | --- | --- |
| `receipt` | Structured account of a critical decision or transition | Durable, versioned, correlated, and attributable |
| `log_event` | Operational diagnostic or activity event | Useful telemetry, not automatically constitutional evidence |
| `metric` | Numeric observation over time | Operational measurement |
| `trace_span` | Execution-path observation | Diagnostic correlation |
| `evidence_record` | Registered proof, artifact, validation output, or protected source | Separately controlled and referenced by receipts |
| `notification` | User-facing or operator-facing message | Presentation of status, not the canonical transition record |

A receipt can reference logs, traces, evidence, artifacts, or reports. It does not embed all underlying data.

### 4.2 Receipt classes

The global receipt classes are:

| Receipt class | Purpose |
| --- | --- |
| `decision_receipt` | Records an authorization, policy, disclosure, privilege, or acceptance decision |
| `transition_receipt` | Records preparation, commit, denial, failure, rollback, repair, or closure of a protected state transition |
| `verification_receipt` | Records verification of identity, integrity, compatibility, signature, provenance, or conformance |
| `transfer_receipt` | Records controlled export, import, publication handoff, or cross-domain movement |
| `recovery_receipt` | Records restore, rollback, forward repair, reconciliation, or recovery closure |
| `evidence_access_receipt` | Records access to restricted evidence |
| `cutover_receipt` | Records activation or rollback of an authority, release, policy, documentation, or migration cutover |

A single workflow can produce multiple receipts because different components own different decisions and commit boundaries.

### 4.3 Common receipt envelope

The logical common envelope contains:

```text
receipt_id
receipt_schema_version
receipt_class
transition_type
producer_component_id
producer_instance_id
subject_ref
actor_ref
target_refs
scope
request_id
correlation_id
causation_id
authority_refs
decision
execution_state
commit_state
outcome
reason_code
requested_at
decided_at
committed_at
recorded_at
profile_refs
component_contract_refs
artifact_refs
release_refs
exception_refs
test_refs
evidence_refs
disclosure_class
retention_class
```

Fields not applicable to a particular class are omitted rather than populated with ambiguous values.

### 4.4 Decision, execution, and commit separation

A protected operation has distinct stages:

| Stage | Question |
| --- | --- |
| request | What action was requested, by whom, and against which target? |
| decision | Was the requested action authorized, denied, or indeterminate? |
| execution | Did the responsible implementation complete the requested work? |
| commit | Did the authoritative state transition complete? |
| recovery | Was the prior state restored or a declared forward repair applied? |

An authorized decision does not guarantee successful execution. Successful execution preparation does not guarantee authoritative commit. A receipt exposes the distinction.

### 4.5 Outcome states

Receipt outcomes use explicit states such as:

```text
authorized
denied
indeterminate
prepared
committed
failed
cancelled
rolled_back
forward_repaired
expired
revoked
superseded
closed
```

Component contracts can define narrower internal states, but their receipts map those states to the global outcome model.

### 4.6 Producer responsibility

The component that owns a decision or authoritative commit produces the corresponding receipt.

Examples:

- Governance Policy Runtime produces its policy decision receipt;
- Publication Gateway produces its publication or disclosure decision and commit receipts;
- a privileged broker produces host-mutation execution and commit receipts;
- lifecycle services produce activation, rollback, repair, and recovery receipts;
- UCKK Publication Bridge produces package, transfer, retry, destination-response, and publication-result receipts within its boundary;
- kOA Mediatheque produces object-lifecycle receipts within its boundary;
- the owning component produces acceptance receipts for external candidate data;
- documentation governance tooling produces authority-cutover receipts.

The Audit Broker collects and serves receipts. It does not retroactively become the decision owner.

### 4.7 Audit Broker responsibilities

The Audit Broker provides:

- receipt ingestion;
- schema and reference validation;
- indexing and correlation;
- selective disclosure;
- retention and archival routing;
- export for review or recourse;
- integrity verification for signed or release-bound receipt sets;
- access control for restricted receipt details and evidence links;
- detection of duplicate or contradictory receipt identities.

The Audit Broker keeps public or ordinary receipt views separate from restricted evidence.

### 4.8 Selective disclosure

A receipt has a disclosure class appropriate to its content and audience.

Typical classes include:

```text
public_summary
tenant_visible
operator_restricted
security_restricted
evidence_restricted
```

An ordinary view can expose:

- receipt identity;
- transition class;
- producer;
- subject;
- high-level target;
- outcome;
- reason category;
- timestamps;
- public authority references.

Protected views can additionally expose evidence references, detailed actor identifiers, sensitive target details, operational diagnostics, or protected policy context.

Secrets, credentials, private keys, unrestricted content payloads, and unnecessary personal data remain outside ordinary receipt content.

### 4.9 Correlation across components

A multi-component workflow uses one correlation identifier and component-local receipts.

For example, an external publication workflow can contain:

1. a source-component selection receipt;
2. a policy decision receipt;
3. a Publication Gateway transfer receipt;
4. an external-destination result receipt;
5. a local relationship or publication-state commit receipt.

The correlation does not merge data ownership or decision authority.

### 4.10 Receipt durability

Receipt durability depends on transition criticality and profile.

A producer can use:

- immediate durable delivery to the Audit Broker;
- durable local append before commit;
- bounded local buffering followed by delivery;
- a signed receipt set embedded in a release or offline bundle.

A missing durable path blocks a transition when its canonical contract requires durable evidence before commit. Lower-risk asynchronous delivery remains bounded and observable.

### 4.11 Receipt integrity

Ordinary repository Markdown does not require content hashes. Receipt integrity is applied where the receipt or bundle is itself an integrity-bearing release, signed package, provenance object, offline bundle, or supply-chain artifact.

Integrity mechanisms can include:

- schema validation;
- stable identity;
- canonical references;
- append-only storage controls;
- signatures;
- signed manifests;
- content digests for referenced artifacts;
- release-set binding;
- trusted timestamps where required.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-RCT-001,REQ-SYS-RCT-002,REQ-SYS-RCT-003,REQ-SYS-RCT-004,REQ-SYS-RCT-005,REQ-SYS-RCT-006,REQ-SYS-RCT-007,REQ-SYS-RCT-008,REQ-SYS-RCT-009,REQ-SYS-RCT-010,REQ-SYS-RCT-011,REQ-SYS-RCT-012,REQ-SYS-RCT-013,REQ-SYS-RCT-014,REQ-SYS-RCT-015,REQ-SYS-RCT-016,REQ-SYS-RCT-017,REQ-SYS-RCT-018,REQ-SYS-RCT-019,REQ-SYS-RCT-020,REQ-SYS-RCT-021,REQ-SYS-RCT-022,REQ-SYS-RCT-023,REQ-SYS-RCT-024 -->
- **REQ-SYS-RCT-001 — SHALL:** Every critical transition produce a stable machine-readable receipt from the component responsible for deciding or committing that transition.
- **REQ-SYS-RCT-002 — SHALL:** A receipt identify its receipt class, transition type, producer, subject, actor, target, scope, requested action, decision, outcome, timestamps, applicable authority, and correlation context.
- **REQ-SYS-RCT-003 — SHALL:** A receipt distinguish request, authorization decision, execution result, and authoritative commit result rather than representing them as one ambiguous success state.
- **REQ-SYS-RCT-004 — SHALL NOT:** A receipt report a transition as committed when the protected authoritative state did not commit successfully.
- **REQ-SYS-RCT-005 — SHALL:** A denied, indeterminate, failed, rolled-back, forward-repaired, cancelled, or partially prepared transition record its actual terminal or pending state and stable reason code.
- **REQ-SYS-RCT-006 — SHALL:** Receipt identifiers remain unique, immutable, and permanently reserved after issuance.
- **REQ-SYS-RCT-007 — SHALL:** Receipt content use selective disclosure so that ordinary receipt views exclude secrets, unrestricted personal data, protected evidence, content payloads, and unnecessary operational detail.
- **REQ-SYS-RCT-008 — SHALL:** Protected evidence referenced by a receipt remain separately access-controlled and every access to restricted evidence produce its own accountable access record.
- **REQ-SYS-RCT-009 — SHALL:** A receipt preserve canonical references to applicable decisions, requirements, locks, profiles, component contracts, artifact identities, release identities, exceptions, tests, and evidence when those objects govern the transition.
- **REQ-SYS-RCT-010 — SHALL:** Receipt production remain inside the owning component or declared receipt-producing boundary and never transfer canonical ownership of the underlying business or system state to the Audit Broker.
- **REQ-SYS-RCT-011 — SHALL:** The Audit Broker store, index, disclose, export, and verify receipts according to its contract without becoming the authority that made the underlying policy, publication, privilege, lifecycle, or data decision.
- **REQ-SYS-RCT-012 — SHALL:** Policy authorization, privilege grants and uses, break-glass activation and closure, governed publication, cross-domain disclosure, and controlled external data transfer be classified as critical transitions.
- **REQ-SYS-RCT-013 — SHALL:** Artifact and release verification, activation, rollback, forward repair, supersession, and recovery be classified as critical transitions.
- **REQ-SYS-RCT-014 — SHALL:** Backup restoration, authoritative data migration, trust-root or revocation change, governed host mutation, and documentation authority cutover be classified as critical transitions.
- **REQ-SYS-RCT-015 — SHALL:** Local Mediatheque lifecycle changes and external UCKK publication transitions produce distinct receipts linked to the affected local record and external destination result.
- **REQ-SYS-RCT-016 — SHALL:** External AI operations record explicit user initiation, transferred data classes, destination surface, purpose, returned candidate identity, provenance, and authoritative acceptance outcome when applicable.
- **REQ-SYS-RCT-017 — SHALL NOT:** Routine reads, ordinary navigation, transient health sampling, internal debug events, or non-authoritative interface actions require constitutional transition receipts unless a canonical policy classifies the specific action as critical.
- **REQ-SYS-RCT-018 — SHALL:** A transition spanning multiple components use a shared correlation identifier while each component emits the receipt for the decision or commit it owns.
- **REQ-SYS-RCT-019 — SHALL:** Atomic transitions emit a commit receipt only after the authoritative commit boundary succeeds and emit rollback or repair receipts when recovery changes the resulting state.
- **REQ-SYS-RCT-020 — SHALL:** Receipt persistence tolerate temporary Audit Broker unavailability through bounded local buffering without allowing missing receipt delivery to fabricate or broaden transition authority.
- **REQ-SYS-RCT-021 — SHALL:** A critical transition whose contract requires durable receipt persistence fail closed before commit when no approved durable or bounded local receipt path is available.
- **REQ-SYS-RCT-022 — SHALL:** Receipt retention, archival, export, deletion, and legal-hold behavior follow the receipt class, evidence policy, applicable profile, and declared retention schedule.
- **REQ-SYS-RCT-023 — SHALL:** Receipt verification detect structural invalidity, broken canonical references, unsupported versions, inconsistent outcomes, missing evidence links, and tampering with release or signed-bundle receipts.
- **REQ-SYS-RCT-024 — SHALL:** Receipt schemas and producers remain versioned so that consumers can reject unsupported semantics without guessing or silently reinterpreting historical receipts.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Standard critical transition

A critical transition follows this sequence:

1. identify the actor, requested action, target, scope, and correlation context;
2. resolve the owning component and applicable authority;
3. validate profile, component, artifact, release, exception, and integration context;
4. produce the decision result;
5. emit or stage the decision receipt;
6. prepare the transition;
7. validate pre-commit conditions;
8. commit the authoritative state atomically;
9. emit the commit receipt;
10. deliver or durably queue the receipt;
11. expose truthful machine-readable and user-facing status.

A denied or indeterminate request ends without authoritative commit.

### 6.2 Failed execution

When execution fails after authorization:

1. preserve the authorization decision receipt;
2. record the failed execution state and reason;
3. leave the authoritative state unchanged when commit did not occur;
4. enter rollback or forward repair when partial external effects require recovery;
5. produce the resulting failure and recovery receipts;
6. expose the actual outcome.

### 6.3 Activation and rollback

Artifact or release activation follows this receipt sequence:

1. verification receipt;
2. compatibility decision receipt;
3. activation preparation receipt where preparation is itself critical;
4. activation commit receipt after atomic success;
5. rollback receipt when the previous valid state is restored;
6. forward-repair receipt when repair replaces rollback;
7. recovery-closure receipt after validation.

The active release identity in a commit receipt matches the actual active state.

### 6.4 Publication and disclosure

Governed publication follows this sequence:

1. source selection and handoff receipt;
2. disclosure or publication decision receipt;
3. transfer receipt;
4. destination response receipt where available;
5. local publication-state commit receipt;
6. denial, cancellation, failure, or reconciliation receipt when the workflow does not complete.

A locally available draft does not become published merely because export preparation succeeded.

### 6.5 External AI operation

An approved external AI operation records:

1. explicit user initiation;
2. selected source references and transferred representations;
3. destination surface and declared purpose;
4. authority and disclosure decision;
5. controlled transfer;
6. returned candidate identity and provenance;
7. review decision;
8. authoritative acceptance or rejection;
9. optional publication workflow.

The external result remains candidate input until the owning workflow accepts it.

### 6.6 Break-glass operation

Break-glass receipt flow contains:

1. invocation request;
2. emergency-condition verification;
3. temporary grant decision;
4. grant activation;
5. every protected action performed under the grant;
6. expiration or revocation;
7. review outcome;
8. remediation or closure.

The receipts demonstrate narrow scope and automatic end of the temporary authority.

### 6.7 Evidence access

Access to restricted evidence follows this sequence:

1. identify requester and evidence target;
2. evaluate purpose and access authority;
3. record grant, denial, or indeterminate result;
4. expose only the authorized evidence view;
5. record access completion or failure;
6. correlate the access with the originating receipt or review case.

### 6.8 Offline and buffered receipt delivery

During disconnected operation:

1. resolve the active offline receipt policy;
2. determine whether the transition requires immediate durable local recording;
3. append the receipt to the approved local store;
4. enforce buffer size, retention, and failure thresholds;
5. synchronize after connectivity returns;
6. verify successful ingestion;
7. preserve the original producer and event timestamps;
8. record reconciliation failures.

Buffer exhaustion does not create permission to discard required receipts silently.

### 6.9 Documentation authority cutover

Documentation cutover records:

1. source release identity;
2. target release identity;
3. validation result;
4. active registry and schema set;
6. activation decision;
7. atomic authority-manifest switch;
8. archival disposition;
9. rollback result when activation fails.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `receipt_schema_invalid` | Receipt does not match its active schema | Receipt is rejected | Producer repairs and resubmits |
| `receipt_identifier_conflict` | Duplicate identity carries inconsistent content | Both records are quarantined | Investigation without authority change |
| `receipt_reference_unresolved` | Canonical decision, requirement, artifact, release, or evidence reference cannot resolve | Receipt cannot support a conformance claim | Preserve for repair as non-validated evidence |
| `receipt_outcome_inconsistent` | Decision, execution, commit, and outcome fields contradict one another | Transition evidence is invalid | Reconstruct from owning component state and evidence |
| `receipt_false_commit` | Receipt claims commit but authoritative state did not commit | Receipt is invalid and incident handling begins | Preserve actual state and produce correction evidence |
| `receipt_producer_unauthorized` | Producer does not own the decision or transition | Receipt carries no authority | Route to the canonical owner |
| `receipt_delivery_unavailable` | Audit Broker cannot receive receipts | Follow the declared durable-buffer policy | Continue only when the transition contract permits buffering |
| `receipt_buffer_exhausted` | Approved local receipt buffer is full or invalid | Required transition is blocked | Read-only or non-critical functions continue |
| `receipt_evidence_unavailable` | Referenced private evidence cannot be accessed | Ordinary receipt remains readable | Evidence-dependent claim remains unverified |
| `receipt_disclosure_violation` | Receipt view exposes protected content improperly | Access is denied and incident handling begins | Serve a permitted reduced view |
| `receipt_retention_conflict` | Retention, deletion, hold, or archival policies conflict | Destructive action is blocked | Preserve the receipt pending resolution |
| `receipt_version_unsupported` | Consumer cannot interpret receipt semantics | Consumer rejects semantic use | Preserve raw receipt for compatible tooling |
| `critical_transition_receipt_missing` | A required receipt is absent | Related conformance or transition claim is blocked | Reconstruct only through an approved recovery process |
| `transition_commit_partial` | Critical commit does not complete atomically | Partial state remains non-authoritative | Rollback or declared forward repair |

A receipt-system failure does not automatically stop unrelated non-critical capabilities. It blocks only transitions whose contracts require the unavailable receipt guarantee.

## 8. Cross-Component Interactions

### 8.1 Governance Policy Runtime

The Governance Policy Runtime records governance authorization, disclosure, privilege, and exception-related decisions where deployed.

Its receipt states the evaluated context and outcome. It does not claim execution or commit performed by another component.

### 8.2 Resource Governor

The Resource Governor can record admission, throttling, suspension, or rejection of critical workloads.

Resource receipts do not become policy authorization receipts. Resource capacity and governance permission remain separate.

### 8.3 Audit Broker

The Audit Broker validates, stores, correlates, discloses, exports, and verifies receipts. It maintains receipt availability without owning the underlying business state or decision.

### 8.4 Publication Gateway

The Publication Gateway produces receipts for disclosure decisions, transfer preparation, publication commit, denial, failure, cancellation, and reconciliation.

The source component retains ownership of its canonical source state.

### 8.5 kOA Mediatheque and UCKK publication integration

kOA Mediatheque records local object creation, version and rendition registration, candidate acceptance, deletion, restoration, and lifecycle changes. After Publication Gateway authorization, UCKK Publication Bridge records package creation, transport attempts, destination responses, and publication results.

Publication remains with the Publication Gateway.

### 8.6 Identity and Trust

Identity and Trust provides actor, service, key, certificate, package, and evidence identity.

Trust-root and revocation changes are critical transitions. Identity proof alone does not create authorization.

### 8.7 Lifecycle services

Lifecycle services produce verification, activation, rollback, repair, supersession, migration, restore, and recovery receipts. Release and artifact identities remain tied to the actual resulting state.

### 8.8 External integrations

External integrations provide destination acknowledgments or result records where available. kOA retains its own transfer and acceptance receipts even when the external system supplies no compatible receipt.

### 8.9 AI surfaces

ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain external surfaces. Their outputs remain candidates, and the authoritative acceptance receipt belongs to the accepting kOA component.

## 9. Decision Closure and Prohibited Assumptions

This document closes the receipt model as follows:

- receipts apply to critical transitions rather than every application event;
- the owning component produces the receipt for its decision or commit;
- Audit Broker collection does not transfer decision authority;
- authorization, execution, and commit remain distinct;
- receipt outcome matches actual authoritative state;
- rollback and forward repair produce their own receipts;
- multi-component workflows use correlation without merging ownership;
- private evidence remains separately protected;
- ordinary views use selective disclosure;
- external AI results remain candidates until acceptance;
- durable receipt requirements are transition-specific;
- cryptographic integrity is reserved for integrity-bearing receipt sets, releases, provenance, bundles, and comparable artifacts.

The following assumptions are prohibited:

- a successful request receipt proves authoritative commit;
- authorization guarantees successful execution;
- the Audit Broker made every recorded decision;
- logs automatically satisfy receipt requirements;
- every user-interface action requires a constitutional receipt;
- a missing receipt can be recreated from memory without an approved recovery process;
- a receipt can contain unrestricted secrets or personal data for convenience;
- external acknowledgments replace kOA transfer and acceptance receipts;
- one component can issue a receipt for another component's canonical commit;
- a rollback erases the original transition history;
- offline operation permits silent loss of required receipts;
- a receipt identifier can be reused after deletion or archival;
- unsupported historical receipt semantics can be guessed;
- file hashes are required for ordinary Markdown documentation.

A new receipt class, critical-transition class, disclosure class, or commit-state semantic requires an accepted owner decision, canonical registry updates, impact analysis, tests, evidence, and authority activation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 24 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. the system registry defines receipt classes, critical-transition classes, common envelope fields, outcomes, and correlation behavior;
7. component contracts identify the producer for each decision and commit receipt;
8. schema tests reject missing identifiers, producers, outcomes, timestamps, and required authority references;
9. state tests distinguish request, decision, execution, commit, rollback, repair, and closure;
10. false-commit tests reject receipts that disagree with authoritative state;
11. correlation tests preserve component ownership across multi-component workflows;
12. selective-disclosure tests exclude secrets, unrestricted personal data, protected evidence, and content payloads from ordinary views;
13. restricted-evidence access produces accountable access records;
14. lifecycle tests cover verification, activation, rollback, forward repair, supersession, restore, and recovery;
15. publication tests cover selection, disclosure decision, transfer, commit, denial, failure, and reconciliation;
16. kOA Mediatheque tests cover local ingestion, candidate acceptance, deletion, restoration, export, and import; UCKK integration tests separately cover authorization, package transport, and destination receipts;
17. external AI tests record explicit initiation, transferred data, destination, provenance, candidate state, and acceptance outcome;
18. break-glass tests cover grant, use, expiration, review, and closure;
19. offline tests cover durable local append, bounded buffering, synchronization, and exhaustion;
20. retention tests cover archival, legal hold, deletion, and protected evidence;
21. signed receipt-set or release receipt tests verify applicable signatures and artifact digests;
22. unsupported receipt versions fail explicitly;
23. missing required receipts block related conformance claims;
24. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
25. active prose is English;
26. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

```text
receipt_schema_invalid
receipt_identifier_conflict
receipt_reference_unresolved
receipt_outcome_inconsistent
receipt_false_commit
receipt_producer_unauthorized
receipt_delivery_unavailable
receipt_buffer_exhausted
receipt_disclosure_violation
receipt_retention_conflict
receipt_version_unsupported
critical_transition_receipt_missing
transition_commit_partial
```

## 11. Non-Normative Examples

### 11.1 Denied publication

A user requests publication of a kOA Mediatheque rendition. The Publication Gateway records a denied disclosure decision. No publication commit receipt exists, and the rendition remains locally available.

### 11.2 Failed service activation

A service artifact passes integrity verification but fails compatibility validation. Verification and failure receipts remain available. The previous service version remains active, so no new activation commit receipt is issued.

### 11.3 Buffered offline receipt

A sovereign offline node performs an authorized local restore. The recovery receipt is appended to the approved local durable store and synchronized to the Audit Broker after connectivity returns. The original producer and event timestamps remain unchanged.

### 11.4 External AI candidate

A user explicitly exports selected content to Gamma. The transfer receipt identifies the selected representation and destination. Returned content is registered as a candidate. A later acceptance receipt records the owning component's review decision.

### 11.5 Restricted evidence access

An investigator opens protected evidence referenced by a break-glass receipt. The ordinary receipt remains unchanged, while a separate evidence-access receipt records the requester, purpose, authority, and outcome.
