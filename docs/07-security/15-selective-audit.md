<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-015",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/publication-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "10-adrs/ADR-010-selective-audit.md"
  ],
  "decision_ids": [
    "DEC-AUD-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-AUDIT-001",
    "REQ-SEC-AUDIT-002",
    "REQ-SEC-AUDIT-003",
    "REQ-SEC-AUDIT-004",
    "REQ-SEC-AUDIT-005",
    "REQ-SEC-AUDIT-006",
    "REQ-SEC-AUDIT-007",
    "REQ-SEC-AUDIT-008",
    "REQ-SEC-AUDIT-009",
    "REQ-SEC-AUDIT-010",
    "REQ-SEC-AUDIT-011",
    "REQ-SEC-AUDIT-012",
    "REQ-SEC-AUDIT-013",
    "REQ-SEC-AUDIT-014",
    "REQ-SEC-AUDIT-015",
    "REQ-SEC-AUDIT-016",
    "REQ-SEC-AUDIT-017",
    "REQ-SEC-AUDIT-018",
    "REQ-SEC-AUDIT-019",
    "REQ-SEC-AUDIT-020",
    "REQ-SEC-AUDIT-021",
    "REQ-SEC-AUDIT-022",
    "REQ-SEC-AUDIT-023",
    "REQ-SEC-AUDIT-024",
    "REQ-SEC-AUDIT-025",
    "REQ-SEC-AUDIT-026",
    "REQ-SEC-AUDIT-027",
    "REQ-SEC-AUDIT-028",
    "REQ-SEC-AUDIT-029",
    "REQ-SEC-AUDIT-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-010",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-COMP-000",
    "DOC-LIFE-002",
    "DOC-LIFE-012",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-013",
    "DOC-SEC-014"
  ],
  "tags": [
    "security",
    "selective-audit",
    "private-proof",
    "public-evidence",
    "audit-broker",
    "data-minimization",
    "authorized-views",
    "recourse",
    "retention",
    "privacy"
  ]
}
KOA:DOC-META:END -->

# Selective Audit

## 1. Purpose

This document defines the selective-audit model of the kOA operating environment.

Selective audit provides accountability without creating total transparency or a surveillance log. The system captures evidence needed to prove critical actions, decisions, releases, publications, access, privilege use, and lifecycle transitions while restricting each view to an authorized purpose and audience.

The model separates public transparency receipts, tenant audit, restricted evidence, privacy records, cultural-rights records, security audit, and private proof. These objects can be linked without exposing all underlying evidence to every consumer.

## 2. Scope

This document applies to:

- source-component audit events;
- Audit Broker custody and evidence indexes;
- governance and authorization decisions;
- resource-admission and privileged-operation receipts;
- artifact verification, publication, activation, rollback, and recovery evidence;
- cross-domain publication requests and receipts;
- tenant audit and authorized cross-tenant investigations;
- personal-data, consent, privacy, and cultural-rights records;
- security, incident, break-glass, and recovery audit;
- public transparency receipts and public evidence;
- restricted evidence and private proof packages;
- authorized views, aggregation, pseudonymization, transformation, and redaction;
- audit requests, access decisions, export, sharing, retention, legal hold, correction, recourse, withdrawal, destruction, and proof of disposition;
- online, offline, disconnected, sovereign, development, build, and control-plane profiles.

This document does not:

- make all system events public;
- make the Audit Broker a universal operational database;
- transfer component data ownership to evidence custody;
- permit direct writes into component-owned state;
- prescribe one log database, message broker, transparency ledger, cryptographic accumulator, storage engine, or visualization product;
- require every profile to retain identical evidence or use identical implementation mechanisms;
- replace privacy, consent, cultural-rights, identity, policy, incident, lifecycle, or component contracts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `contracts/components/audit-broker.component.json` | Owns evidence ingestion, custody, indexing, authorized views, access records, receipts, and failure behavior. |
| `generated/component-catalog.json` and component contracts | Own source-component responsibilities, business records, event production, and prohibited direct writes. |
| `contracts/components/governance-policy-runtime.component.json` | Owns policy-gated audit access, disclosure, redaction, exception, legal-hold, and public-evidence decisions. |
| `contracts/components/identity-and-trust.component.json` | Owns requester identity, credential, role, trust, validity, and revocation verification. |
| `contracts/components/publication-gateway.component.json` | Owns cross-domain publication decisions and public disclosure boundaries. |
| `contracts/profiles/*.profile.json` | Owns profile-specific retention, offline custody, assurance, synchronization, resource, and evidence controls. |
| `contracts/artifact-contracts/decision-receipt.schema.json` | Defines machine-readable access, authorization, transition, and audit decision receipts. |
| `contracts/artifact-contracts/publication-receipt.schema.json` | Defines publication evidence and public or restricted receipt relationships. |
| `contracts/artifact-contracts/provenance-receipt.schema.json` | Defines provenance evidence for artifacts and transformations. |
| `generated/evidence-catalog.json` | Owns evidence identities, classes, owners, required views, and conformance relationships. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns canonical ownership, component separation, authority separation, gateway separation, and profile-scope assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, component, profile, test, and evidence relationships. |
| `10-adrs/ADR-010-selective-audit.md` | Records the accepted choice of selective audit instead of total transparency. |

This Markdown document explains the audit model. Canonical event, evidence, receipt, access-policy, retention, and disclosure fields remain machine-readable.

## 4. Model and Responsibilities

### 4.1 Selective-audit principle

The audit system answers bounded questions for bounded audiences.

Examples include:

- whether a governed operation was authorized;
- whether an artifact was verified before activation;
- whether a public disclosure passed its policy and rights checks;
- whether a privileged operation occurred under an approved decision;
- whether a subject's record was accessed;
- whether a release or recovery transition completed;
- whether evidence was retained or destroyed according to policy.

Answering one question does not authorize disclosure of every related event or source record.

### 4.2 Evidence object model

| Object | Purpose | Authority |
| --- | --- | --- |
| Source record | Business or operational fact owned by a component | Source component |
| Source event | Component-produced statement that an auditable occurrence happened | Source component |
| Captured evidence | Preserved event payload or proof admitted by an evidence contract | Audit Broker custody |
| Custody record | Chain of ingestion, storage, transformation, access, export, and disposition | Audit Broker |
| Authorized audit view | Purpose-limited projection of evidence | Derived by Audit Broker under policy |
| Private proof package | Restricted evidence sufficient for an authorized investigation or claim | Restricted evidence authority |
| Public transparency receipt | Minimal public statement that a declared event or control outcome occurred | Public-evidence contract |
| Access receipt | Evidence of a successful or denied audit request | Audit Broker and policy authority |
| Recourse record | Challenge, review, correction, annotation, withdrawal, or appeal history | Declared recourse authority |

A derived view never becomes the owner of its source data.

### 4.3 Audit categories

The categories below explain distinct policy domains. They are not a competing canonical enum.

| Category | Typical audience | Typical content |
| --- | --- | --- |
| Public transparency | General public | Minimal event identity, public outcome, time, responsible authority, public proof reference |
| Tenant audit | Authorized tenant roles | Tenant-scoped activity, decisions, changes, access, exports, and receipts |
| Restricted evidence | Investigators, adjudicators, designated operators | Detailed event payload, sensitive context, chain of custody, private proof |
| Privacy and consent | Subject, privacy role, authorized reviewer | Personal-data access, consent, disclosure, correction, retention, and recourse |
| Cultural-rights evidence | Rights holders and authorized governance roles | Consent, permitted use, restrictions, withdrawal, and disclosure history |
| Security audit | Security and incident roles | Authentication, privilege, integrity, compromise, containment, and recovery evidence |
| Operational audit | Service and operations roles | Health transitions, administrative actions, maintenance, recovery, and bounded diagnostics |
| Conformance evidence | Validators and assurance roles | Requirement, test, release, profile, artifact, and control outcomes |

Each category has separate field, access, retention, and disclosure policies.

### 4.4 Source authority and custody

A source component creates the source event and remains responsible for the truth and correction process of its business record.

The Audit Broker:

- validates the event envelope;
- admits evidence through an active contract;
- records custody;
- protects integrity and classification;
- indexes only declared fields;
- generates authorized views;
- records every access and disposition action.

Custody does not authorize the Audit Broker to rewrite source business state.

### 4.5 Classification and minimization

Evidence capture begins with classification.

Classification can include:

- public;
- authorized internal;
- tenant confidential;
- restricted;
- personal;
- security sensitive;
- cultural rights restricted;
- secret-bearing prohibited;
- privileged-operation restricted;
- restricted provenance.

The source and evidence contracts define which fields are necessary. Fields not required for the evidence purpose remain at the source or are excluded, transformed, tokenized, pseudonymized, aggregated, or redacted.

### 4.6 Authorized views

An authorized view records:

- view identity and version;
- requesting subject and role;
- purpose and authority;
- source evidence references;
- permitted fields;
- transformations and redactions;
- time and subject scope;
- audience and destination;
- validity and reuse conditions;
- integrity and provenance;
- access receipt.

The view can be materialized or generated at query time. Its authority never exceeds the intersection of source classification, evidence contract, policy decision, identity scope, profile controls, consent or rights conditions, and destination contract.

### 4.7 Public evidence and private proof

Public evidence is intentionally minimal.

A public receipt can identify:

- public event or control identity;
- responsible authority;
- public outcome;
- occurrence or decision time;
- public policy or requirement reference;
- integrity or proof reference;
- withdrawal or supersession status.

Private proof retains the restricted facts needed to substantiate the receipt. The public receipt links to a controlled proof relationship rather than embedding the private payload.

### 4.8 Integrity and custody history

Integrity controls apply to evidence artifacts where their contracts require them.

A custody history can record:

- source capture;
- ingestion;
- validation;
- storage;
- replication;
- transformation;
- redaction;
- access;
- export;
- legal hold;
- correction;
- supersession;
- destruction.

Integrity does not determine disclosure authority. A valid proof can remain restricted.

### 4.9 Retention and disposition

Retention is evidence-class specific.

A retention contract defines:

- retention start;
- minimum and maximum periods;
- review points;
- legal hold;
- archival eligibility;
- correction and recourse implications;
- key and encryption lifecycle;
- deletion or destruction method;
- residual metadata;
- disposition receipt.

A public receipt can outlive private evidence only when the active contracts define what remains provable and how withdrawal, expiry, or destruction is represented.

### 4.10 Recourse

Selective audit supports recourse.

An affected subject or authorized representative can, within applicable privacy and security limits:

- learn that an auditable decision or access occurred;
- obtain the permitted audit view;
- request the decision basis;
- challenge identity, classification, context, or outcome;
- submit correction evidence;
- obtain a review decision;
- see annotations, supersession, withdrawal, or correction relationships;
- appeal through the declared process.

Recourse preserves history rather than silently rewriting the original record.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-AUDIT-001,REQ-SEC-AUDIT-002,REQ-SEC-AUDIT-003,REQ-SEC-AUDIT-004,REQ-SEC-AUDIT-005,REQ-SEC-AUDIT-006,REQ-SEC-AUDIT-007,REQ-SEC-AUDIT-008,REQ-SEC-AUDIT-009,REQ-SEC-AUDIT-010,REQ-SEC-AUDIT-011,REQ-SEC-AUDIT-012,REQ-SEC-AUDIT-013,REQ-SEC-AUDIT-014,REQ-SEC-AUDIT-015,REQ-SEC-AUDIT-016,REQ-SEC-AUDIT-017,REQ-SEC-AUDIT-018,REQ-SEC-AUDIT-019,REQ-SEC-AUDIT-020,REQ-SEC-AUDIT-021,REQ-SEC-AUDIT-022,REQ-SEC-AUDIT-023,REQ-SEC-AUDIT-024,REQ-SEC-AUDIT-025,REQ-SEC-AUDIT-026,REQ-SEC-AUDIT-027,REQ-SEC-AUDIT-028,REQ-SEC-AUDIT-029,REQ-SEC-AUDIT-030 -->
- **REQ-SEC-AUDIT-001 — SHALL:** Every auditable event has a stable event identity, source authority, event class, subject scope, occurrence time, capture time, classification, integrity claim, retention class, and evidence owner.
- **REQ-SEC-AUDIT-002 — SHALL:** The audit model distinguishes source records, captured evidence, custody records, authorized audit views, private proof packages, and public transparency receipts.
- **REQ-SEC-AUDIT-003 — SHALL NOT:** A single universally visible log, globally queryable event store, or unrestricted transparency stream is used as the system audit model.
- **REQ-SEC-AUDIT-004 — SHALL:** The source component retains authority over its business records while the Audit Broker owns only declared evidence custody, indexes, access records, and derived audit views.
- **REQ-SEC-AUDIT-005 — SHALL NOT:** Audit custody transfers component data ownership, workflow authority, governance authority, resource authority, publication authority, or host privilege to the Audit Broker.
- **REQ-SEC-AUDIT-006 — SHALL NOT:** The Audit Broker or an audit consumer writes directly to another component's authoritative data, source tables, private queues, private files, or internal state.
- **REQ-SEC-AUDIT-007 — SHALL:** Each captured event contains only the fields required by its active audit contract, classification, retention purpose, and evidence obligation.
- **REQ-SEC-AUDIT-008 — SHALL:** Personal data, secret values, private keys, cultural-rights material, restricted provenance, security-sensitive details, tenant-confidential data, and privileged-operation details remain separately classified and selectively disclosed.
- **REQ-SEC-AUDIT-009 — SHALL NOT:** A public transparency receipt contains secret values, private keys, raw personal data, unrestricted tenant content, protected cultural material, exploit-enabling security detail, or private evidence payloads.
- **REQ-SEC-AUDIT-010 — SHALL:** Tenant audit views remain isolated by tenant and declared cross-tenant authority.
- **REQ-SEC-AUDIT-011 — SHALL:** Restricted evidence is available only through an authorized request that identifies requester, role, purpose, scope, subject, time range, legal or policy basis, requested fields, and disclosure destination.
- **REQ-SEC-AUDIT-012 — SHALL:** Privacy records, consent records, cultural-rights records, security audit, operational audit, tenant audit, and public transparency evidence have distinct access and retention policies.
- **REQ-SEC-AUDIT-013 — SHALL:** Governance Policy Runtime evaluates policy-gated audit access, disclosure, exception, redaction, legal-hold, and public-evidence decisions.
- **REQ-SEC-AUDIT-014 — SHALL:** Identity and Trust verifies requester identity, role credentials, trust scope, validity, and revocation when required for an audit operation.
- **REQ-SEC-AUDIT-015 — SHALL:** An authorized audit view is a reproducible derived projection whose fields, transformations, redactions, aggregation, pseudonymization, and disclosure scope are recorded.
- **REQ-SEC-AUDIT-016 — SHALL NOT:** A derived audit view broadens the authority, classification, audience, retention, or permissible use of its source evidence.
- **REQ-SEC-AUDIT-017 — SHALL:** Every audit access, denied request, exported view, public receipt, private proof package, retention override, legal hold, redaction, correction, withdrawal, and destruction action produces a machine-readable receipt.
- **REQ-SEC-AUDIT-018 — SHALL:** Audit evidence uses integrity and provenance mechanisms appropriate to its artifact class while preserving the distinction between proof of integrity and authority to disclose.
- **REQ-SEC-AUDIT-019 — SHALL:** Evidence capture, custody transfer, view generation, access, export, retention, and destruction preserve a verifiable custody and transformation history.
- **REQ-SEC-AUDIT-020 — SHALL NOT:** A missing, invalid, expired, revoked, ambiguous, or unavailable required identity, policy, trust, classification, consent, rights, retention, or evidence condition is treated as authorization to disclose.
- **REQ-SEC-AUDIT-021 — SHALL:** Evidence-delivery queues, retries, storage growth, view generation, export size, query duration, and concurrent audit work remain bounded by active contracts and effective profiles.
- **REQ-SEC-AUDIT-022 — SHALL:** When required evidence custody is unavailable, the source transition follows its declared synchronous-fail, bounded-queue, local-receipt, or degraded-evidence behavior without silently discarding mandatory evidence.
- **REQ-SEC-AUDIT-023 — SHALL:** Every evidence class declares retention start, minimum and maximum retention, review points, deletion or destruction procedure, legal-hold behavior, archival eligibility, and proof of disposition.
- **REQ-SEC-AUDIT-024 — SHALL:** A retention extension, legal hold, preservation order, or exception is scoped, time-bounded, authorized, traceable, reviewable, and prevented from silently changing unrelated evidence classes.
- **REQ-SEC-AUDIT-025 — SHALL:** Correction or recourse preserves the original evidence identity and records the challenge, decision, correction, annotation, supersession, or withdrawal relationship without rewriting history invisibly.
- **REQ-SEC-AUDIT-026 — SHALL:** A subject or authorized representative can obtain the applicable audit view, challenge an adverse or incorrect record, receive the decision basis, and invoke the active recourse path subject to privacy and security boundaries.
- **REQ-SEC-AUDIT-027 — SHALL:** Public evidence and private proof can demonstrate the same event or control outcome through linked receipts without requiring the public object to contain the private evidence payload.
- **REQ-SEC-AUDIT-028 — SHALL:** Offline and disconnected profiles preserve required local evidence, access decisions, custody transitions, and later synchronization or reconciliation behavior through profile-owned controls.
- **REQ-SEC-AUDIT-029 — SHALL:** Validation detects missing events, duplicate event identities, custody gaps, unauthorized fields, classification mismatch, cross-tenant leakage, invalid redaction, stale access grants, excessive retention, missing destruction evidence, and public-to-private linkage failure.
- **REQ-SEC-AUDIT-030 — SHALL:** Every active selective-audit requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Capturing evidence

Evidence capture:

1. resolves the source component and event contract;
2. assigns or verifies the event identity;
3. validates source authority, event class, subject scope, time, and correlation;
4. applies classification and field minimization;
5. validates the evidence envelope;
6. calculates required integrity claims;
7. records provenance and custody admission;
8. persists the evidence in its declared class and scope;
9. updates only authorized indexes;
10. returns an ingestion receipt.

When mandatory custody is unavailable, the source follows its declared failure or bounded-queue behavior.

### 6.2 Requesting an audit view

An audit request:

1. identifies requester, role, purpose, subject, scope, time range, fields, and destination;
2. verifies identity, trust, validity, and revocation;
3. resolves tenant, profile, privacy, rights, security, and evidence policies;
4. evaluates authorization;
5. resolves permitted evidence and fields;
6. applies transformation, minimization, aggregation, pseudonymization, and redaction;
7. creates a reproducible view;
8. records the decision and access receipt;
9. delivers only to the authorized destination.

A denied request also produces a receipt without disclosing restricted evidence.

### 6.3 Producing a public transparency receipt

Public evidence production:

1. resolves the public-evidence contract and source event;
2. confirms that public disclosure is permitted;
3. selects the minimal public fields;
4. removes or transforms private, tenant, security, rights, and provenance detail;
5. verifies the public statement against private proof;
6. records the public-to-private proof relationship;
7. publishes through the declared gateway when cross-domain disclosure applies;
8. emits public and restricted receipts separately.

### 6.4 Supporting an investigation

Restricted investigation access:

1. resolves the investigation authority and case scope;
2. verifies requester identity and role;
3. obtains policy authorization and any required multi-party approval;
4. freezes the requested evidence set logically without broadening unrelated retention;
5. produces the least-disclosing sufficient view or proof package;
6. records every access, export, and onward disclosure;
7. closes or renews access according to policy;
8. removes temporary investigation material at the end of the authorization.

### 6.5 Correcting or challenging evidence

Recourse:

1. receives the challenge and identifies affected evidence;
2. preserves the original evidence and custody history;
3. verifies the challenger and authority;
4. gathers permitted supporting evidence;
5. records the review process;
6. decides correction, annotation, supersession, withdrawal, rejection, or escalation;
7. updates derived views and public status where required;
8. emits the recourse decision and evidence receipts.

### 6.6 Expiring or destroying evidence

Disposition:

1. resolves retention class, current policy, holds, exceptions, and recourse state;
2. confirms that deletion or destruction is authorized;
3. identifies copies, indexes, exports, derived views, and cryptographic material;
4. destroys or renders inaccessible the required payload;
5. updates residual metadata according to contract;
6. prevents stale views from remaining valid;
7. records proof of disposition;
8. preserves only the history explicitly permitted after disposition.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved authority | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Source event identity is missing or duplicated | Reject or block ingestion | Existing valid evidence | Candidate event | Identity-validation result |
| Event contract cannot be resolved | Keep the event outside authoritative custody | Existing evidence | Candidate ingestion | Contract-resolution failure |
| Classification is missing or ambiguous | Treat the event as restricted and block disclosure | Source authority and existing evidence | View and publication generation | Classification outcome |
| Mandatory evidence custody is unavailable | Apply declared synchronous-fail, bounded queue, or local receipt behavior | Source-component authority | Transition requiring unavailable evidence | Custody-path state |
| Queue or storage bound is reached | Stop unbounded intake and expose degraded evidence capability | Existing admitted evidence | New evidence capture | Capacity receipt |
| Requester identity or role is invalid | Deny access | Evidence confidentiality | Requested view | Access-decision receipt |
| Policy authority is unavailable | Keep gated disclosure blocked | Existing authorized views within validity | New gated view | Policy-path state |
| Cross-tenant scope is unresolved | Deny the request | Tenant isolation | Cross-tenant view | Scope-mismatch receipt |
| Redaction or transformation fails | Suppress delivery and invalidate the candidate view | Source evidence | Candidate disclosure | Transformation failure |
| Public receipt cannot be linked to private proof | Block publication or mark the public claim invalid according to contract | Private evidence | Public evidence claim | Linkage-validation result |
| Integrity or custody gap is detected | Quarantine affected evidence and begin investigation | Unaffected evidence | Affected proof claim | Integrity incident |
| Required consent or rights condition is absent | Block disclosure or use | Protected source material | Rights-dependent view | Rights-policy outcome |
| Retention rule is ambiguous | Preserve the evidence under the safest applicable temporary state and require resolution | Evidence and recourse capability | Automatic destruction or disclosure | Retention-resolution record |
| Legal hold expires without review | Block further extension until reauthorized | Existing evidence pending decision | Silent indefinite retention | Hold-expiry receipt |
| Disposition fails partially | Keep the case open and invalidate affected deletion claims | Remaining evidence authority | Proof of complete destruction | Disposition failure |
| Audit Broker is unavailable | Source components retain their own authority and declared local evidence behavior | Source records and local receipts | Central views and custody operations | Broker-health state |

## 8. Cross-Component Interactions

### 8.1 Source components

Each component emits only events declared by its active contract.

The source component remains responsible for business-state truth, source correction, and accepting any recourse outcome into its authoritative state. Audit Broker custody does not create a reverse write path.

### 8.2 Audit Broker

The Audit Broker admits evidence, preserves custody, maintains evidence indexes, creates authorized views, and records access.

It does not become the source of business truth or the universal query interface for all component data.

### 8.3 Governance Policy Runtime

Governance Policy Runtime evaluates access, disclosure, redaction, exception, legal-hold, public-evidence, and recourse authorization when applicable.

The policy decision does not itself reveal evidence or mutate source state.

### 8.4 Identity and Trust

Identity and Trust verifies requesters, service identities, roles, signatures, validity, and revocation.

A trusted identity remains constrained by the audit policy, purpose, subject, tenant, field, destination, and time scope.

### 8.5 Publication Gateway

Public or cross-domain audit evidence uses the Publication Gateway when the destination crosses an authority or disclosure boundary.

The gateway controls disclosure. It does not gain ownership of source events, restricted evidence, or destination business state.

### 8.6 Resource Governor

Resource Governor supplies bounded admission for evidence ingestion, indexing, queries, transformation, exports, investigations, and disposition work.

A resource grant does not authorize access or disclosure.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-AUD-001` | Establishes separate public transparency receipts, tenant audit, restricted evidence, privacy records, and security audit instead of one public log. |
| `DEC-DATA-001` | Preserves source-component data ownership and prohibits direct cross-component writes. |
| `DEC-GOV-001` | Preserves the distinction between policy authorization and deterministic resource admission or evidence custody. |
| `DEC-PROFILE-001` | Keeps profile-specific retention, offline, assurance, and evidence mechanisms within explicit profile scope. |

`ADR-010-selective-audit.md` records the accepted rationale: civic accountability and sensitive operations both matter, while one public log would create surveillance.

### Prohibited assumptions

- accountability requires publishing every event;
- an immutable log is safe to expose without classification;
- Audit Broker custody transfers ownership of business data;
- a valid signature authorizes disclosure;
- a resource grant authorizes an audit query;
- a tenant administrator can inspect another tenant by default;
- a public receipt must contain the private evidence payload;
- restricted evidence can be copied into support tickets or diagnostics;
- pseudonymization automatically removes privacy risk;
- aggregation automatically makes cultural-rights material public;
- a denied request does not need an audit record;
- legal hold can continue indefinitely without review;
- retention applies uniformly to every evidence class;
- deleting an index proves that every payload copy was destroyed;
- correcting evidence means silently rewriting history;
- an offline node can discard evidence until connectivity returns;
- a profile-specific transparency mechanism applies globally;
- total observability and selective audit are interchangeable;
- public evidence can expose secrets, private keys, or exploit-enabling details.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-SEC-015` is active at `07-security/15-selective-audit.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. `ADR-010` exists with status `accepted`.
5. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
6. Every listed lock exists and is active.
7. Source records, source events, captured evidence, custody records, views, private proof, and public receipts remain distinct.
8. Public transparency, tenant audit, restricted evidence, privacy, cultural-rights, security, operational, and conformance policies remain separable.
9. Every event has unique identity, source, classification, retention, integrity, and evidence ownership.
10. Evidence capture contains only contract-required fields.
11. Public receipts contain no prohibited private or sensitive payload.
12. Tenant views cannot cross tenant boundaries without explicit authority.
13. Every audit request records identity, role, purpose, subject, scope, time, fields, destination, and decision.
14. Authorized views are reproducible and never broaden source authority.
15. Every access, denial, export, disclosure, hold, correction, withdrawal, and disposition action maps to a receipt.
16. Evidence integrity and disclosure authority remain independent checks.
17. Custody history covers every required transformation and transfer.
18. Missing identity, policy, trust, classification, consent, rights, retention, or evidence authority fails closed.
19. Evidence intake, storage, queries, transformations, exports, and retries are bounded.
20. Retention rules define review, hold, archive, destruction, and disposition evidence.
21. Correction and recourse preserve the original record and visible relationships.
22. Public receipts resolve controlled links to sufficient private proof.
23. Offline profiles define local custody and later reconciliation.
24. Audit Broker interfaces contain no direct writes to component-owned state.
25. Critical audit paths map to tests and evidence.
26. Active prose is English and contains no unresolved-authority marker.
27. No normative keyword appears outside the generated requirement block.
28. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates public evidence and private proof.

A public receipt can state that a release passed its required verification and name the responsible authority. Detailed vulnerability findings, private provenance, internal topology, and signer evidence remain in a restricted proof package.

> **Non-normative example:** This example illustrates tenant isolation.

A tenant auditor can inspect the tenant's own publication and administrative receipts. The view excludes another tenant's events even when both tenants use the same physical Audit Broker.

> **Non-normative example:** This example illustrates privacy recourse.

A user can receive a permitted view showing that a personal record was accessed, challenge an incorrect access purpose, and obtain a review decision. The original access receipt remains linked to the correction rather than disappearing.

> **Non-normative example:** This example illustrates bounded offline custody.

A sovereign-offline node can preserve required local receipts while disconnected. On reconnection, it synchronizes custody records according to its profile without treating the absence of central connectivity as permission to drop evidence.

> **Non-normative example:** This example illustrates authority separation.

The Audit Broker can prove that a privileged operation had a valid policy decision and execution receipt. It does not gain the right to repeat the privileged operation or modify the affected component.
