<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-PUBGATE",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component:publication_gateway"
  ],
  "canonical_refs": [
    "generated/component-catalog.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/subsystems/orgo.subsystem.json",
    "contracts/subsystems/konnaxion.subsystem.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-GATE-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-COMP-PUBGATE-001",
    "REQ-COMP-PUBGATE-002",
    "REQ-COMP-PUBGATE-003",
    "REQ-COMP-PUBGATE-004",
    "REQ-COMP-PUBGATE-005",
    "REQ-COMP-PUBGATE-006",
    "REQ-COMP-PUBGATE-007",
    "REQ-COMP-PUBGATE-008",
    "REQ-COMP-PUBGATE-009",
    "REQ-COMP-PUBGATE-010",
    "REQ-COMP-PUBGATE-011",
    "REQ-COMP-PUBGATE-012",
    "REQ-COMP-PUBGATE-013",
    "REQ-COMP-PUBGATE-014",
    "REQ-COMP-PUBGATE-015",
    "REQ-COMP-PUBGATE-016",
    "REQ-COMP-PUBGATE-017",
    "REQ-COMP-PUBGATE-018",
    "REQ-COMP-PUBGATE-019",
    "REQ-COMP-PUBGATE-020",
    "REQ-COMP-PUBGATE-021",
    "REQ-COMP-PUBGATE-022",
    "REQ-COMP-PUBGATE-023",
    "REQ-COMP-PUBGATE-024",
    "REQ-COMP-PUBGATE-025",
    "REQ-COMP-PUBGATE-026",
    "REQ-COMP-PUBGATE-027",
    "REQ-COMP-PUBGATE-028",
    "REQ-COMP-PUBGATE-029",
    "REQ-COMP-PUBGATE-030",
    "REQ-COMP-PUBGATE-031",
    "REQ-COMP-PUBGATE-032"
  ],
  "lock_ids": [
    "LOCK-GATE-001",
    "LOCK-DATA-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-AUTH-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-012",
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-COMP-000"
  ],
  "tags": [
    "publication-gateway",
    "private-to-public",
    "disclosure",
    "classification",
    "rights",
    "consent",
    "redaction",
    "approval",
    "withdrawal",
    "supersession",
    "konnaxion",
    "orgo"
  ]
}
KOA:DOC-META:END -->

# Publication Gateway

## 1. Purpose

Publication Gateway is the controlled disclosure boundary between private operational domains and public or commons-oriented surfaces.

Its primary system flow is:

`text
Orgo private result
-> publication candidate
-> Publication Gateway validation and policy
-> approved publication bundle
-> Konnaxion admission
-> publication receipt
`

The component prevents direct database coupling and converts one explicit private-domain candidate into one controlled public-domain handoff.

It owns disclosure processing and evidence. It does not own the originating Orgo workflow or the accepted Konnaxion public object.

The machine-readable owner of detailed stores, interfaces, states, events, workflows, failures, security, resources, and conformance is:

`text
contracts/components/publication-gateway.component.json
`

## 2. Scope

Publication Gateway covers:

- publication request intake;
- candidate identity and schema validation;
- source and correlation preservation;
- data classification;
- privacy and disclosure policy;
- rights, consent, attribution, and cultural authority;
- audience and purpose restrictions;
- declared redaction and transformation;
- human, community, steward, legal, or dual approval;
- publication-bundle creation;
- Konnaxion delivery;
- publication receipts;
- withdrawal;
- supersession;
- recovery and evidence.

It does not define:

- Orgo workflow execution or closure;
- Konnaxion participation, discovery, or public-object persistence;
- public-to-private Orgo intake;
- kOA Mediatheque local media ingestion;
- general document conversion;
- native generative AI;
- a direct database bridge;
- unrestricted data export;
- profile-specific topology;
- exact network protocols or storage technologies.

A public signal moving into private operational work uses its own explicit intake contract. It is not reclassified as a Publication Gateway output flow.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/component-catalog.json` | Publication Gateway identity, global responsibility domains, data ownership, prohibited responsibilities, and relationships. |
| `contracts/components/publication-gateway.component.json` | Detailed stores, interfaces, states, events, workflows, failure behavior, security, resources, operations, artifacts, and tests. |
| `contracts/components/orgo.component.json` | Originating private workflow, result, candidate creation, source authorization, and private retention. |
| `contracts/components/konnaxion.component.json` | Public-object admission, public persistence, indexing, discovery, distribution, and receiving receipts. |
| `contracts/components/governance-policy-runtime.component.json` | Disclosure, audience, consent, rights, redaction, approval, exception, withdrawal, and privilege decisions. |
| `contracts/components/identity-and-trust.component.json` | Human, role, organization, tenant, service, publisher, artifact, destination, and revocation identity. |
| `contracts/components/audit-broker.component.json` | Classified publication, approval, withdrawal, supersession, and recovery evidence. |
| `contracts/components/resource-governor.component.json` | Queue bounds, resource priority, cancellation, delivery limits, and degradation controls. |
| `contracts/integrations/uckk-publication.integration.json` | Separate local media-ingestion boundary. |
| `contracts/artifact-classes.contract.json` | Publication bundle, transformation record, receipt, and offline artifact contracts. |
| `contracts/profiles/*.profile.json` | Component membership, activation, topology, resource, storage, network, and offline envelope. |
| `generated/requirements-index.json` | Requirement statements displayed in section 5. |
| `generated/test-catalog.json` | Component, cross-component, system, security, operations, lifecycle, and exit tests. |
| `generated/evidence-catalog.json` | Executed results and publication evidence. |

## 4. Model and Responsibilities

### 4.1 Boundary model

Publication Gateway is a policy-enforced transformation and handoff boundary.

`text
private authoritative state
-> explicit candidate
-> validation
-> classification
-> disclosure and rights decision
-> declared transformation
-> required review and approval
-> immutable publication bundle
-> public-domain admission
-> accountable receipt
`

The private and public records remain distinct objects with explicit provenance.

### 4.2 Responsibility domains

| Responsibility domain | Meaning |
| --- | --- |
| `publication_request_validation` | publication request validation |
| `data_classification_enforcement` | data classification enforcement |
| `disclosure_policy_application` | disclosure policy application |
| `rights_and_consent_enforcement` | rights and consent enforcement |
| `redaction_and_declared_transformation` | redaction and declared transformation |
| `publication_approval_control` | publication approval control |
| `publication_bundle_creation` | publication bundle creation |
| `publication_receipts` | publication receipts |
| `withdrawal_and_supersession` | withdrawal and supersession |

### 4.3 Authoritative data domains

| Data domain | Role | Owner |
| --- | --- | --- |
| `publication_requests` | Authoritative | Publication Gateway |
| `publication_transformation_records` | Authoritative | Publication Gateway |
| `publication_approval_records` | Authoritative | Publication Gateway |
| `publication_receipts` | Authoritative | Publication Gateway |
| `publication_withdrawal_records` | Authoritative | Publication Gateway |
| `publication_supersession_records` | Authoritative | Publication Gateway |

These domains do not include Orgo cases, tasks, approvals, or result state. They do not include accepted Konnaxion public records.

### 4.4 Publication request

A publication request identifies:

- request identity;
- source component;
- source object and version;
- source workflow or decision context;
- tenant and environment;
- requester;
- requested destination;
- requested audience;
- requested publication effect;
- candidate artifact or structured payload;
- provenance;
- classification context;
- rights and consent context;
- correlation identity;
- expiry or review deadline when applicable.

The request remains a candidate until all required evaluation succeeds.

### 4.5 Classification and disclosure

The gateway evaluates the complete payload and every referenced artifact.

Evaluation can include:

- public, internal, personal, sensitive, restricted, secret, and culturally governed classes;
- field-level classification;
- source-purpose compatibility;
- destination and audience;
- consent;
- rights and attribution;
- community or steward authority;
- legal and policy obligations;
- retention;
- export restrictions;
- withdrawal requirements;
- no-AI restrictions;
- exception applicability.

An unknown classification produces a blocked outcome.

### 4.6 Transformation model

A transformation can include:

- field removal;
- redaction;
- pseudonymization;
- aggregation;
- format conversion;
- deterministic summary;
- deterministic translation;
- audience-specific presentation;
- link or reference substitution;
- approved excerpt selection.

Each transformation records:

- transformation identity and version;
- input identity;
- output identity;
- declared method;
- affected fields or artifacts;
- reviewer when required;
- policy decision;
- reproducibility data;
- reason codes;
- evidence references.

External AI can propose candidate wording or redaction only through an explicit integration flow. Binding output still passes deterministic checks and required review.

### 4.7 Approval model

Approval is separate from validation and transformation.

Policy can require:

- source-owner approval;
- privacy review;
- legal review;
- community or cultural-steward approval;
- dual approval;
- publication-authority approval;
- final preview confirmation.

An approval applies only to the exact output, audience, destination, policy version, and expiry presented for review.

### 4.8 Publication bundle

An approved publication bundle contains:

- bundle identity;
- source and correlation identities;
- approved public payload or artifact;
- destination and audience;
- provenance;
- attribution;
- applicable rights and restrictions;
- transformation record;
- policy and approval references;
- withdrawal and supersession instructions;
- compatibility and artifact metadata;
- replay-protection identity;
- evidence references.

The bundle excludes unapproved source fields and unrelated private state.

### 4.9 Konnaxion admission

Publication Gateway delivers the bundle through Konnaxion's explicit admission contract.

Konnaxion independently:

- authenticates the sender;
- verifies the bundle;
- checks compatibility;
- accepts or rejects the public object;
- assigns or confirms its public identity;
- stores accepted public state;
- returns a receiving receipt.

Publication Gateway does not write Konnaxion persistence.

### 4.10 Publication receipts

A completed receipt connects:

`text
Orgo source
-> publication request
-> policy and approvals
-> transformation
-> publication bundle
-> Konnaxion receiving identity
-> public result
`

Public accountability evidence and restricted evidence remain separate.

### 4.11 Withdrawal and supersession

Withdrawal is an explicit lifecycle transition.

It can affect:

- the public object;
- public derivatives;
- indexes;
- caches;
- distribution records;
- audience-scoped artifacts;
- mirrors or peers covered by the receiving contract.

Supersession preserves the predecessor and replacement relationship.

Withdrawal and supersession do not erase required historical evidence.

### 4.12 Architectural relationships

| Component | Relationship | Purpose |
| --- | --- | --- |
| `orgo` | `receives_publication_candidates_from` | Accept controlled candidates from the private operational domain. |
| `konnaxion` | `delivers_approved_publications_to` | Transfer validated and approved public outputs. |
| `governance_policy_runtime` | `requests_disclosure_and_consent_decisions_from` | Apply audience, rights, redaction, approval, and exception policy. |
| `audit_broker` | `emits_publication_and_withdrawal_receipts_to` | Preserve accountable publication evidence. |

### 4.13 UCKK publication bridge separation

Publication Gateway controls cross-domain disclosure.

UCKK Publication Bridge performs UCKK-specific packaging and transport after Publication Gateway authorizes publication.

They have separate:

- purposes;
- identities;
- stores;
- interfaces;
- events;
- state machines;
- profiles;
- tests;
- receipts.

Local media ingestion does not imply publication.

### 4.14 Security and privacy

The gateway uses scoped identities and explicit authority.

It preserves:

- tenant and domain separation;
- authentication and authorization separation;
- least disclosure;
- field- and artifact-level classification;
- rights and consent;
- cultural authority;
- destination allowlisting;
- no direct store access;
- no unrestricted shell;
- secret exclusion;
- classified evidence;
- audited protected-evidence access.

### 4.15 Resource and deployment model

Profile contracts decide:

- component inclusion;
- activation mode;
- process and storage placement;
- queue and concurrency limits;
- network exposure;
- offline behavior;
- Konnaxion connectivity;
- review-surface availability;
- evidence-forwarding topology.

Resource Governor prioritizes policy, confirmation, cancellation, withdrawal, and evidence over optional transformation work.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-PUBGATE-001,REQ-COMP-PUBGATE-002,REQ-COMP-PUBGATE-003,REQ-COMP-PUBGATE-004,REQ-COMP-PUBGATE-005,REQ-COMP-PUBGATE-006,REQ-COMP-PUBGATE-007,REQ-COMP-PUBGATE-008,REQ-COMP-PUBGATE-009,REQ-COMP-PUBGATE-010,REQ-COMP-PUBGATE-011,REQ-COMP-PUBGATE-012,REQ-COMP-PUBGATE-013,REQ-COMP-PUBGATE-014,REQ-COMP-PUBGATE-015,REQ-COMP-PUBGATE-016,REQ-COMP-PUBGATE-017,REQ-COMP-PUBGATE-018,REQ-COMP-PUBGATE-019,REQ-COMP-PUBGATE-020,REQ-COMP-PUBGATE-021,REQ-COMP-PUBGATE-022,REQ-COMP-PUBGATE-023,REQ-COMP-PUBGATE-024,REQ-COMP-PUBGATE-025,REQ-COMP-PUBGATE-026,REQ-COMP-PUBGATE-027,REQ-COMP-PUBGATE-028,REQ-COMP-PUBGATE-029,REQ-COMP-PUBGATE-030,REQ-COMP-PUBGATE-031,REQ-COMP-PUBGATE-032 -->
- **REQ-COMP-PUBGATE-001 — SHALL:** Publication Gateway owns publication requests, transformation records, approval records, publication receipts, withdrawal records, and supersession records.
- **REQ-COMP-PUBGATE-002 — SHALL NOT:** Publication Gateway owns originating Orgo workflow state or accepted Konnaxion public state.
- **REQ-COMP-PUBGATE-003 — SHALL:** Private-to-public disclosure follows the explicit Orgo to Publication Gateway to Konnaxion path.
- **REQ-COMP-PUBGATE-004 — SHALL NOT:** Orgo publishes directly into Konnaxion persistence or bypasses Publication Gateway for a governed cross-domain disclosure.
- **REQ-COMP-PUBGATE-005 — SHALL:** Publication Gateway authorize disclosure before invoking the UCKK publication integration; the integration shall not share authority state or own local media.
- **REQ-COMP-PUBGATE-006 — SHALL:** Every publication candidate identifies its source object, source component, source workflow or decision context, correlation identity, requested audience, requested publication effect, and provenance.
- **REQ-COMP-PUBGATE-007 — SHALL:** Every candidate passes schema, identity, scope, classification, provenance, and compatibility validation before disclosure evaluation.
- **REQ-COMP-PUBGATE-008 — SHALL:** Unknown, conflicting, unsupported, or unverifiable data classification blocks publication.
- **REQ-COMP-PUBGATE-009 — SHALL:** Disclosure evaluation applies privacy, consent, rights, cultural authority, attribution, audience, purpose, retention, export, and withdrawal policy when applicable.
- **REQ-COMP-PUBGATE-010 — SHALL:** Redaction, minimization, aggregation, translation, summarization, and other publication transformations are declared, reproducible, versioned, and linked to their inputs and outputs.
- **REQ-COMP-PUBGATE-011 — SHALL NOT:** An AI-generated transformation becomes binding publication content without deterministic validation and the review required by active policy.
- **REQ-COMP-PUBGATE-012 — SHALL:** The publication bundle contains only fields and artifacts approved for the declared destination and audience.
- **REQ-COMP-PUBGATE-013 — SHALL:** Required human, community, steward, legal, or dual approval completes before bundle delivery.
- **REQ-COMP-PUBGATE-014 — SHALL:** Request, review, approval, transformation, publication, withdrawal, and supersession capabilities remain separately grantable.
- **REQ-COMP-PUBGATE-015 — SHALL:** Publication authority is bound to the exact candidate, transformed output, destination, audience, policy version, obligations, expiry, and replay-protection identity.
- **REQ-COMP-PUBGATE-016 — SHALL:** Publication delivery is idempotent and duplicate requests return or reconcile the prior result without creating duplicate public objects.
- **REQ-COMP-PUBGATE-017 — SHALL:** A publication becomes completed only after Konnaxion confirms durable contract-bound acceptance and required local evidence is secured.
- **REQ-COMP-PUBGATE-018 — SHALL:** Publication receipts identify the source, approved output, destination, audience, policy decision, approvals, transformation record, receiving identity, result, and evidence references.
- **REQ-COMP-PUBGATE-019 — SHALL:** A publication failure blocks disclosure and preserves the originating Orgo workflow and private result.
- **REQ-COMP-PUBGATE-020 — SHALL NOT:** Publication Gateway writes directly to Orgo or Konnaxion authoritative databases or permits either component to write its authoritative stores directly.
- **REQ-COMP-PUBGATE-021 — SHALL:** Withdrawal applies to every applicable public object, derivative, index, cache, distribution record, and audience-scoped artifact through explicit receiving contracts.
- **REQ-COMP-PUBGATE-022 — SHALL:** Supersession preserves predecessor identity, replacement identity, reason, effective state, audience effect, and receipt history.
- **REQ-COMP-PUBGATE-023 — SHALL:** Backup, export, restore, and recovery preserve publication, withdrawal, supersession, provenance, rights, audience, and receipt state.
- **REQ-COMP-PUBGATE-024 — SHALL:** Restoration does not reactivate withdrawn, revoked, expired, or superseded publication authority.
- **REQ-COMP-PUBGATE-025 — SHALL:** Publication Gateway operates without a native AI dependency and remains able to validate, redact, approve, bundle, withdraw, and record evidence through deterministic local controls.
- **REQ-COMP-PUBGATE-026 — SHALL:** Optional external integrations and AI surfaces remain user or workflow initiated, removable, non-authoritative, and unable to deliver directly to Konnaxion.
- **REQ-COMP-PUBGATE-027 — SHALL:** Logs, metrics, traces, review views, receipts, and support evidence minimize sensitive content and exclude secrets and unrestricted private payloads.
- **REQ-COMP-PUBGATE-028 — SHALL:** Profile contracts own Publication Gateway inclusion, activation, topology, resource limits, storage, network exposure, offline behavior, and exclusions.
- **REQ-COMP-PUBGATE-029 — SHALL:** Resource pressure preserves confirmation, cancellation, policy evaluation, withdrawal, evidence, and recovery before optional transformation or delivery work.
- **REQ-COMP-PUBGATE-030 — SHALL:** Interrupted validation, transformation, approval, delivery, withdrawal, or supersession resumes idempotently or enters controlled recovery without partial public authority.
- **REQ-COMP-PUBGATE-031 — SHALL:** Manual review evaluates contextual disclosure risk, redaction sufficiency, rights, cultural authority, audience suitability, and public accountability when automated checks are insufficient.
- **REQ-COMP-PUBGATE-032 — SHALL:** Every active Publication Gateway claim has complete decision, requirement, lock, test, evidence, exception, profile, component, artifact, and publication traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Publication request intake

1. Receive one authenticated Orgo publication candidate.
2. resolve source object, version, workflow, requester, tenant, and environment.
3. validate request and candidate schema.
4. verify provenance and correlation identity.
5. identify the destination and requested audience.
6. classify every field and referenced artifact.
7. reject, quarantine, or admit the request for disclosure evaluation.
8. record intake evidence.

### 6.2 Disclosure evaluation

1. Resolve current identity, delegation, consent, rights, and policy state.
2. evaluate source purpose against requested public purpose.
3. evaluate destination and audience.
4. identify required redaction or transformation.
5. identify required approvals and separation of duties.
6. identify retention, withdrawal, and supersession obligations.
7. return an approved, denied, blocked, or review-required result with stable reason codes.

### 6.3 Transformation

1. Freeze the admitted candidate identity.
2. select only declared transformation methods.
3. create a transformed candidate.
4. record every changed, removed, aggregated, or substituted field.
5. validate the transformed output deterministically.
6. compare the output with the policy decision.
7. preserve the original private candidate in Orgo.
8. create an immutable transformation record.

### 6.4 Review and approval

1. Present the exact transformed output.
2. present source, destination, audience, provenance, attribution, and restrictions.
3. present material disclosure risks and reversibility.
4. obtain every required reviewer decision.
5. invalidate approval after a material output, audience, destination, policy, or authority change.
6. bind valid approval to the exact publication operation.
7. record approval evidence.

### 6.5 Bundle creation and delivery

1. Create the immutable publication bundle.
2. verify bundle structure, identity, policy, approvals, restrictions, and replay protection.
3. authenticate the Konnaxion destination.
4. deliver through the explicit Konnaxion interface.
5. receive durable acceptance or rejection.
6. retry only through the bounded idempotent delivery policy.
7. preserve the bundle and request state.
8. avoid any direct public-store mutation.

### 6.6 Completion

1. Resolve the Konnaxion receiving identity.
2. verify the receiving result.
3. secure required local evidence.
4. create the publication receipt.
5. notify Orgo through its explicit result interface.
6. mark the publication request completed.
7. preserve the private Orgo result independently.

### 6.7 Withdrawal

1. Receive an authenticated withdrawal request or policy decision.
2. resolve the published object, audience, derivatives, indexes, caches, and distribution scope.
3. evaluate authority and obligations.
4. create a withdrawal instruction.
5. deliver it through every applicable explicit receiving contract.
6. verify receiving outcomes.
7. record unresolved propagation targets.
8. create the withdrawal record and evidence.
9. preserve historical provenance.

### 6.8 Supersession

1. Identify the active public object.
2. identify the approved replacement bundle.
3. verify compatibility, rights, audience, and authority.
4. publish the replacement.
5. confirm durable receiving identity.
6. link predecessor and replacement.
7. apply the declared predecessor state.
8. create supersession evidence.

### 6.9 Recovery

1. Identify the last verified request, transformation, approval, bundle, delivery, and receipt state.
2. inspect the interrupted operation identity.
3. resume only an idempotent declared step.
4. otherwise return to the last verified state.
5. revalidate authority, rights, classification, destination, and revocation.
6. verify withdrawn and superseded status after restoration.
7. register recovery evidence.
8. avoid duplicate public objects.

## 7. Failure and Degradation

### 7.1 Invalid candidate

Schema, identity, provenance, compatibility, or source-context failure blocks the request.

The originating Orgo workflow remains intact.

### 7.2 Unknown classification

An unknown, conflicting, or unverifiable classification blocks publication.

The gateway does not choose a less restrictive class by default.

### 7.3 Policy or authority failure

Missing, stale, expired, revoked, incompatible, or ambiguous authority blocks the affected disclosure.

A previous approval is not reused for a changed output, destination, or audience.

### 7.4 Transformation failure

A failed or non-reproducible transformation does not create an approved bundle.

The original Orgo candidate remains unchanged.

### 7.5 Review failure

Rejected, incomplete, expired, or conflicting review leaves the publication blocked or reviewable.

No public object is created.

### 7.6 Konnaxion unavailability

A verified immutable bundle can remain queued within declared bounds.

Before retry, the gateway revalidates:

- destination identity;
- authority;
- revocation;
- audience;
- rights;
- bundle identity;
- expiry;
- compatibility.

### 7.7 Partial delivery

An uncertain receiving result does not produce a completed receipt.

The gateway uses idempotent reconciliation with Konnaxion before retrying or creating another public object.

### 7.8 Withdrawal failure

Failed withdrawal propagation remains visible and reviewable.

The gateway records every unresolved target and continues bounded retries or escalation according to policy.

### 7.9 Audit failure

Required local evidence remains durable.

Critical publication, withdrawal, or supersession completion waits until its local evidence requirement is satisfied.

### 7.10 Resource pressure

Optional transformations and delivery concurrency reduce before:

- policy evaluation;
- final review;
- cancellation;
- withdrawal;
- evidence;
- recovery.

### 7.11 Offline operation

Local validation, classification, transformation, review preparation, approval recording, withdrawal preparation, and evidence can continue when local authority permits.

Remote Konnaxion delivery remains deferred.

External AI and optional integrations remain unavailable without blocking deterministic local controls.

## 8. Cross-Component Interactions

| Counterparty | Interaction | Ownership boundary |
| --- | --- | --- |
| Orgo | Supplies explicit private-domain publication candidates and receives publication outcomes. | Orgo retains workflow, task, approval, and private-result authority. |
| Konnaxion | Receives approved bundles, withdrawal instructions, and supersession relationships. | Konnaxion owns accepted public state and public-object lifecycle. |
| Governance Policy Runtime | Decides disclosure, consent, audience, rights, redaction, review, exception, withdrawal, and supersession policy. | It does not perform transformation or public-store mutation. |
| Identity and Trust | Resolves requester, reviewer, organization, tenant, workload, publisher, destination, artifact, and revocation identity. | Authentication remains distinct from authorization. |
| Audit Broker | Stores classified publication, approval, withdrawal, supersession, and recovery evidence. | Audit evidence does not grant publication authority. |
| Resource Governor | Controls queue bounds, priorities, concurrency, cancellation, and resource degradation. | Resource control does not decide disclosure. |
| Publication artifacts | Carry immutable bundles, transformation records, receipts, and offline instructions. | Artifact presence does not equal approval or acceptance. |
| External integrations and AI | Can return explicit candidate transformations or assistive material. | They cannot approve, deliver, withdraw, or write authoritative state directly. |
| UCKK Publication Bridge | Performs UCKK-specific packaging and transport of an authorized representation. | It cannot authorize disclosure or own the local media record. |

Every cross-component mutation uses an explicit API, command, event, gateway, or versioned artifact.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-UCKK-EXT-001` | Publication Gateway authorization precedes the UCKK publication integration. |
| `DEC-DATA-001` | Publication Gateway owns only its registered publication, transformation, approval, receipt, withdrawal, and supersession domains. |
| `DEC-COMP-001` | Cross-domain publication uses explicit component boundaries rather than shared persistence. |
| `DEC-AUTH-001` | Disclosure, approval, publication, withdrawal, and supersession use explicit bounded authority. |
| `DEC-IDENT-001` | Source, requester, reviewer, destination, audience, publisher, artifact, and public-object identities remain distinct. |
| `DEC-GOV-001` | Governance Policy Runtime decides policy; Publication Gateway enforces the decision in its workflow. |
| `DEC-AI-001` | External AI remains optional and its output remains a non-authoritative candidate. |
| `DEC-LIFE-001` | Publication artifacts and receipts use explicit verification, lifecycle, recovery, and evidence. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- Orgo can write Konnaxion persistence;
- Publication Gateway owns the Orgo workflow;
- Publication Gateway owns accepted Konnaxion public state;
- local media ingestion is publication;
- a valid source record is automatically safe for public disclosure;
- a public classification applies to every field and referenced artifact;
- missing classification means public;
- redaction can be inferred without a declared transformation;
- an AI-generated summary is approved publication content;
- one approval applies to a changed audience or destination;
- a successful network request proves durable Konnaxion acceptance;
- retrying delivery can create a duplicate public object;
- publication failure rolls back completed private work;
- deletion of private state withdraws public state automatically;
- restore can reactivate withdrawn or revoked publication authority;
- audit evidence can expose the complete private payload;
- network reachability grants publication authority;
- a profile-specific protocol applies globally;
- ordinary Markdown requires publication-artifact content hashes.

A new implementation-affecting publication choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Component contract | `TEST-COMP-PUBGATE-001`, `TEST-COMP-PUBGATE-002`, `TEST-COMP-PUBGATE-003`, `TEST-COMP-PUBGATE-004`, `TEST-COMP-PUBGATE-005`, `TEST-COMP-PUBGATE-006`, `TEST-COMP-PUBGATE-007`, `TEST-COMP-PUBGATE-008`, `TEST-COMP-PUBGATE-009`, `TEST-COMP-PUBGATE-010` |
| Domain separation | `TEST-CROSS-002`, `TEST-CROSS-003`, `TEST-CROSS-015`, `TEST-SYS-013`, `TEST-SYS-014` |
| Authority and evidence | `TEST-SYS-004`, `TEST-SYS-011`, `TEST-CROSS-009`, `TEST-CROSS-014`, `TEST-SEC-005`, `TEST-SEC-006`, `TEST-SEC-011` |
| Rights, audience, and withdrawal | `TEST-SEC-009`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-EXIT-007` |
| AI and integration boundary | `TEST-SYS-002`, `TEST-SYS-003`, `TEST-SYS-012`, `TEST-CROSS-013`, `TEST-SEC-012`, `TEST-EXIT-008` |
| Profile and operations | `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-OPS-002`, `TEST-OPS-003`, `TEST-OPS-005`, `TEST-OPS-006`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-009`, `TEST-OPS-010` |
| Lifecycle and recovery | `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-015`, `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005` |

Additional validation confirms:

1. the component identity, kind, documentation path, decisions, locks, and data domains match `generated/component-catalog.json`;
2. every authoritative data domain has one owner;
3. Publication Gateway and UCKK publication integration have distinct identities, state, interfaces, and receipts;
4. Orgo and Konnaxion direct writes are rejected;
5. every interface has stable identity, direction, authorization, idempotency, and failure behavior;
6. every state transition rejects invalid or partial changes;
7. every publication bundle retains source, policy, approval, transformation, audience, destination, and evidence relationships;
8. every completed publication has a durable Konnaxion receiving result;
9. every withdrawal and supersession propagates through explicit receiving contracts;
10. restore preserves withdrawn, revoked, expired, and superseded state;
11. external AI output remains non-authoritative;
12. profile resource and offline envelopes resolve;
13. manual review has evidence when required;
14. every requirement maps to an active test or approved manual control;
15. no unresolved authority marker exists;
16. all active prose is in English.

A failed required test blocks the affected publication or component claim.

## 11. Non-Normative Examples

### 11.1 Public progress summary

Orgo completes a private operational milestone and creates a publication candidate.

Publication Gateway removes private assignee information, converts internal status details into an approved public summary, verifies attribution and audience, obtains the required approval, creates a bundle, and delivers it to Konnaxion.

The private Orgo result remains unchanged.

### 11.2 Redacted accountability report

An accountability report contains public findings and restricted evidence.

The gateway publishes only the approved findings and bounded evidence references. Restricted evidence remains in its protected domain. The receipt links the public report to the private source without disclosing the restricted payload.

### 11.3 AI-proposed summary

An authorized workflow sends eligible source material to an approved external AI surface for a candidate summary.

The returned text is recorded with provenance. Deterministic checks and a human reviewer evaluate it. Only the reviewed output can enter the publication bundle.

The external service cannot deliver to Konnaxion.

### 11.4 Failed publication

Konnaxion rejects a bundle because its artifact version is incompatible.

Publication Gateway records the rejection and leaves the request blocked or ready for correction. Orgo retains its completed private workflow and result.

### 11.5 Duplicate delivery

A delivery acknowledgement is lost.

Publication Gateway reconciles using the bundle and replay identities. Konnaxion returns the prior receiving result rather than creating a second public object.

### 11.6 Withdrawal

A cultural steward withdraws authority for a public artifact.

The gateway creates a withdrawal instruction covering the public object, audience-scoped artifacts, indexes, caches, and applicable distribution records. Konnaxion applies the withdrawal and returns evidence.

Historical provenance remains controlled and reviewable.

### 11.7 Supersession

A corrected public report replaces an earlier report.

The new bundle is approved and admitted first. The gateway then links the predecessor and replacement and applies the approved predecessor state.

Both identities remain historically traceable.

### 11.8 Offline preparation

The deployment loses network access while reviewers prepare a publication.

Local validation, classification, deterministic transformation, review, and approval recording continue when local authority permits. Delivery to Konnaxion remains deferred and is fully revalidated after connectivity returns.
