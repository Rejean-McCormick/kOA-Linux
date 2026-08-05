<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/data_authority_and_ownership",
    "contracts/system.contract.json#/cross_component_communication",
    "contracts/system.contract.json#/external_integrations",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/artifact-contracts/cultural-rights-policy.schema.json",
    "contracts/artifact-contracts/publication-request.schema.json",
    "contracts/artifact-contracts/publication-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SEC-PRIV-001",
    "REQ-SEC-PRIV-002",
    "REQ-SEC-PRIV-003",
    "REQ-SEC-PRIV-004",
    "REQ-SEC-PRIV-005",
    "REQ-SEC-PRIV-006",
    "REQ-SEC-PRIV-007",
    "REQ-SEC-PRIV-008",
    "REQ-SEC-PRIV-009",
    "REQ-SEC-PRIV-010",
    "REQ-SEC-PRIV-011",
    "REQ-SEC-PRIV-012",
    "REQ-SEC-PRIV-013",
    "REQ-SEC-PRIV-014",
    "REQ-SEC-PRIV-015",
    "REQ-SEC-PRIV-016",
    "REQ-SEC-PRIV-017",
    "REQ-SEC-PRIV-018",
    "REQ-SEC-PRIV-019",
    "REQ-SEC-PRIV-020",
    "REQ-SEC-PRIV-021",
    "REQ-SEC-PRIV-022",
    "REQ-SEC-PRIV-023",
    "REQ-SEC-PRIV-024",
    "REQ-SEC-PRIV-025",
    "REQ-SEC-PRIV-026",
    "REQ-SEC-PRIV-027",
    "REQ-SEC-PRIV-028",
    "REQ-SEC-PRIV-029",
    "REQ-SEC-PRIV-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-020",
    "DOC-COMP-IDT-001",
    "DOC-LIFE-000",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-011",
    "DOC-SEC-012"
  ],
  "tags": [
    "security",
    "privacy",
    "disclosure",
    "data-minimization",
    "purpose-limitation",
    "consent",
    "cultural-rights",
    "publication",
    "external-transfer",
    "selective-disclosure",
    "private-proof",
    "receipts",
    "retention",
    "recourse"
  ]
}
KOA:DOC-META:END -->

# Privacy and Disclosure

## 1. Purpose

This document defines the kOA privacy and disclosure model.

Privacy governs how protected data is collected, used, transformed, queried, retained, restored, exported, deleted, and evidenced.

Disclosure governs when a representation leaves its current authority or audience boundary.

The model distinguishes:

`text
collection
internal use
cross-component access
derived processing
external transfer
publication
audit disclosure
public proof
retention and deletion
`

These stages are not interchangeable.

A component can be authorized to store data without being authorized to publish it. A service can be authorized to process a selected representation without receiving unrestricted access to the source object. An auditor can verify a critical decision without viewing the protected payload. A destination can receive bytes without the system truthfully recording a completed publication commit.

The model centers on:

- explicit purpose;
- minimization;
- tenant and component ownership;
- disclosure authority;
- consent and cultural-rights context;
- selective evidence;
- truthful receipts;
- bounded retention;
- correction and revocation;
- portability, exit, and recourse.

This is an architecture and control model. Applicable legal, contractual, community, and jurisdictional requirements remain represented through accepted policy artifacts and profile-specific controls rather than inferred in this document.

## 2. Scope

This document applies globally to protected data handled by:

- user-facing components;
- identity and trust;
- governance policy;
- kOA Mediatheque;
- external UCKK publication integration;
- Ariane;
- Kristal and language runtimes;
- Konnaxion and Orgo;
- Publication Gateway;
- external integrations;
- external AI surfaces;
- SenTient where deployed;
- development workspaces;
- build and release systems;
- observability;
- audit and evidence;
- backup and restore;
- offline bundles;
- portability and exit.

Protected data can include:

- identity and contact data;
- credentials and authentication evidence;
- component business data;
- user content;
- media and renditions;
- personal preferences;
- voice inputs and candidate transcripts;
- governance decisions;
- cultural-rights and consent records;
- location or device context;
- operational metadata;
- logs and diagnostics;
- receipts and restricted evidence;
- derived views, indexes, analytics, and caches;
- backup and recovery copies.

This document does not create a universal data-classification registry, retention schedule, consent taxonomy, or legal basis catalog. Those values belong to canonical data, policy, artifact, integration, profile, and component contracts.

It does not authorize collection merely by describing it.

## 3. Canonical References

The canonical sources for this document are:

`text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/data_authority_and_ownership
contracts/system.contract.json#/cross_component_communication
contracts/system.contract.json#/external_integrations
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json
generated/profile-catalog.json
contracts/integration-types.contract.json
contracts/artifact-classes.contract.json
contracts/components/identity-and-trust.component.json
contracts/components/governance-policy-runtime.component.json
contracts/components/publication-gateway.component.json
contracts/components/audit-broker.component.json
contracts/artifact-contracts/cultural-rights-policy.schema.json
contracts/artifact-contracts/publication-request.schema.json
contracts/artifact-contracts/publication-receipt.schema.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `data_authority_and_ownership` | Canonical component ownership and prohibited direct writes |
| `cross_component_communication` | Declared command, query, event, gateway, and artifact paths |
| `external_integrations` and `integrations.registry.json` | External identity, destination, data classes, authentication, limits, failure, and removal |
| `receipts_and_critical_transitions` | Request, decision, execution, commit, rollback, and reconciliation evidence |
| Component contracts | Data classes, actions, views, interfaces, failures, retention, and component authority |
| Governance Policy Runtime contract | Governed disclosure, consent, privilege, cultural-rights, and exception decisions |
| Publication Gateway contract | External audience, destination, disclosure, transfer, and publication commit |
| Identity and Trust contract | Subject identity, signer identity, trust, credential, and revocation evidence |
| Audit Broker contract | Receipt validation, storage, indexing, verification, and selective disclosure |
| Cultural-rights policy contract | Versioned cultural-rights, consent, audience, reuse, attribution, and disclosure rules |
| Publication request and receipt contracts | Machine-readable disclosure request and truthful publication result |
| Profile contracts | Encryption, residency, isolation, offline, assurance, retention, and operating constraints |
| `requirements.registry.json` | Normative privacy and disclosure requirements |
| `locks.registry.json` | Data, gateway, AI, governance, lifecycle, profile, and decision-closure invariants |
| `traceability.registry.json` | Requirement, component, profile, policy, test, and evidence relationships |
| `test-catalog.registry.json` | Executable minimization, disclosure, privacy, and receipt validation |
| `evidence.registry.json` | Privacy, disclosure, consent, publication, retention, and recourse evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create missing authority or unrestricted disclosure |

This Markdown document explains the model and does not replace the canonical policy or data-class definitions.

## 4. Model and Responsibilities

### 4.1 Processing context

Every protected-data operation has a processing context:

`text
operation identity
owning component
tenant
subject or community context
data classes
source objects
selected representations
purpose
authority references
consent and rights references
recipients or audience
destination
validity
retention
correlation
expected result
`

An incomplete context cannot support a governed disclosure.

### 4.2 Data lifecycle

The privacy lifecycle is:

`text
admit or collect
classify
store under owner authority
use for declared purpose
derive bounded views
share through declared interfaces
transfer or publish through a gateway
retain or restrict
correct, revoke, or delete
export and exit
preserve required evidence
`

Each transition preserves provenance and scope.

### 4.3 Data classification

A data class can declare:

- canonical owner;
- tenant scope;
- subject or community relationship;
- sensitivity;
- permitted purposes;
- permitted processors;
- permitted representations;
- audience constraints;
- destination constraints;
- consent or rights requirements;
- retention;
- backup;
- deletion;
- derived-data propagation;
- evidence class;
- export and exit behavior.

Classification applies to values and meaningful combinations. Individually ordinary fields can become protected when combined.

### 4.4 Purpose limitation

A purpose is a stable, declared reason for processing.

Examples include:

- deliver a requested component function;
- authenticate a subject;
- verify an artifact;
- create a selected rendition;
- support a declared governance workflow;
- publish to a named audience;
- diagnose a specific failure;
- restore a specific domain;
- produce required evidence.

Purposes such as “future use,” “analytics,” or “improvement” are insufficient unless a canonical policy defines their boundaries, data classes, recipients, retention, and recourse.

### 4.5 Minimization

Minimization operates across several dimensions:

| Dimension | Minimization question |
| --- | --- |
| Fields | Which attributes are needed? |
| Objects | Which records or source objects are needed? |
| Precision | Is exact precision necessary? |
| Time | How long is access or retention needed? |
| Audience | Who needs the representation? |
| Destination | Which endpoint or domain needs it? |
| Copies | How many durable or temporary copies are needed? |
| Derived data | Which indexes, previews, analytics, or candidates are needed? |
| Evidence | Which fields prove the result without exposing payloads? |

A minimized representation can be created by the owning component or an approved gateway. It remains traceable to its source without becoming the source record.

### 4.6 Authority separation

Privacy decisions can involve several authorities:

| Authority owner | Responsibility |
| --- | --- |
| Owning component | Ordinary access, business use, source data, and component state |
| Governance Policy Runtime | Governed disclosure, consent, cultural rights, privilege, and exceptions |
| Identity and Trust | Identity, credential, trust, signature, and revocation evidence |
| Publication Gateway | External audience and destination publication decision and commit |
| Audit Broker | Receipt storage and selective evidence disclosure |
| Resource Governor | Workload capacity only |

Identity success, resource availability, or system privilege does not create disclosure authority.

### 4.7 Internal access

Internal access can be:

- same-component use;
- cross-component query;
- cross-component command;
- event delivery;
- derived artifact consumption;
- restricted evidence access.

Same-host or same-database deployment does not make all data internal to one authority.

A cross-component query returns an authorized view. It does not expose the destination component's source tables or reusable database credential.

### 4.8 External transfer and publication

External transfer sends selected data to a registered destination for a declared capability.

Publication is a stronger state: the system records that a representation was released to an external audience or destination under an authoritative disclosure decision.

The Publication Gateway controls:

- request validation;
- source and representation selection;
- audience;
- destination;
- purpose;
- disclosure and consent context;
- transfer;
- destination response;
- commit state;
- publication receipt.

The kOA Mediatheque controls user-selected local media admission. Publication Gateway controls disclosure to external audiences, including UCKK, through destination-specific adapters.

### 4.9 Consent and cultural rights

Consent and cultural-rights records can constrain:

- access;
- transformation;
- reproduction;
- attribution;
- language or representation;
- audience;
- destination;
- commercial or non-commercial reuse;
- machine processing;
- external AI transfer;
- publication;
- retention;
- archival;
- revocation;
- community authority;
- recourse.

A valid record has explicit scope and evidence.

Silence, possession, previous access, public availability, technical accessibility, or one prior approval does not imply unrestricted reuse.

### 4.10 Derived data

Derived data includes:

- indexes;
- search tokens;
- previews;
- thumbnails;
- transcripts;
- extracted text;
- analytics;
- classifications received from an external source;
- external AI candidates;
- summaries;
- caches;
- de-identified or aggregated views;
- embeddings received through an approved integration;
- public evidence projections.

Derived data retains source provenance, owner, tenant, purpose, and disclosure constraints unless an accepted transformation contract establishes a new valid classification.

Deletion or restriction of source data triggers the derived-data behavior declared by the owning contract.

### 4.11 De-identification and aggregation

De-identification and aggregation are controlled transformations rather than automatic exemptions.

Their contracts identify:

- input classes;
- transformation method;
- residual risk;
- minimum group or cohort rules where applicable;
- prohibited joins;
- re-identification controls;
- recipient and purpose;
- retention;
- verification evidence.

A derived view that can reasonably be linked back under available system context remains protected.

### 4.12 Selective disclosure

Selective disclosure provides the smallest evidence view needed for the recipient.

An ordinary receipt view can expose:

`text
receipt identity
producer component
authority class
decision
execution state
commit state
target class
time
outcome
reason code
`

Restricted fields can remain referenced:

`text
subject identity details
policy inputs
source payload
credential evidence
private proof
personal data
cultural content
secret values
external transfer payload
`

A restricted evidence request receives a separately authorized view and can generate an access receipt.

### 4.13 Public evidence and private proof

Public evidence demonstrates accountability without publishing the underlying private proof.

Examples include proof that:

- a policy decision existed;
- a signer was trusted under a declared scope;
- an activation committed;
- a publication was denied;
- a receipt chain verifies;
- a release passed required tests.

The private proof remains in the appropriate protected domain.

### 4.14 Retention and deletion

Retention classes distinguish:

- active authoritative records;
- superseded records;
- derived data;
- operational caches;
- temporary transfer data;
- backups;
- recovery copies;
- receipts;
- provenance;
- legal or cultural holds;
- published copies;
- externally controlled copies.

Deletion capability depends on ownership and location. The system can delete its own copy and issue a destination deletion request without falsely claiming deletion from an external system unless that result is verified.

### 4.15 Notice and recourse

A privacy or disclosure interaction can expose:

- what was requested;
- which data classes were involved;
- purpose;
- authority;
- recipients;
- destination;
- validity;
- result;
- reason code;
- correction path;
- restriction or revocation path;
- export path;
- challenge or appeal path;
- responsible owner.

The view is adapted to the actor and does not expose unrelated protected information.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-PRIV-001,REQ-SEC-PRIV-002,REQ-SEC-PRIV-003,REQ-SEC-PRIV-004,REQ-SEC-PRIV-005,REQ-SEC-PRIV-006,REQ-SEC-PRIV-007,REQ-SEC-PRIV-008,REQ-SEC-PRIV-009,REQ-SEC-PRIV-010,REQ-SEC-PRIV-011,REQ-SEC-PRIV-012,REQ-SEC-PRIV-013,REQ-SEC-PRIV-014,REQ-SEC-PRIV-015,REQ-SEC-PRIV-016,REQ-SEC-PRIV-017,REQ-SEC-PRIV-018,REQ-SEC-PRIV-019,REQ-SEC-PRIV-020,REQ-SEC-PRIV-021,REQ-SEC-PRIV-022,REQ-SEC-PRIV-023,REQ-SEC-PRIV-024,REQ-SEC-PRIV-025,REQ-SEC-PRIV-026,REQ-SEC-PRIV-027,REQ-SEC-PRIV-028,REQ-SEC-PRIV-029,REQ-SEC-PRIV-030 -->
- **REQ-SEC-PRIV-001 — SHALL:** Every collection, use, query, derivation, disclosure, transfer, publication, audit view, backup, restore, and deletion involving protected data declare its owning component, tenant context, purpose, data classes, subject or community context where applicable, authority, recipients, retention, and expected outcome.
- **REQ-SEC-PRIV-002 — SHALL:** Protected data processing use the minimum fields, precision, volume, duration, audience, and number of copies necessary for the approved purpose.
- **REQ-SEC-PRIV-003 — SHALL NOT:** Data collected or admitted for one purpose be reused for a materially different purpose without an explicit compatible authority, updated disclosure context, and any required consent or rights evaluation.
- **REQ-SEC-PRIV-004 — SHALL:** Every data class have a canonical owner, classification, permitted purposes, disclosure constraints, retention behavior, derived-data treatment, backup treatment, and deletion or archival behavior.
- **REQ-SEC-PRIV-005 — SHALL:** Tenant, identity, component, environment, profile, audience, destination, and cultural-rights scopes remain explicit throughout processing and disclosure.
- **REQ-SEC-PRIV-006 — SHALL NOT:** Authentication, trust verification, network reachability, resource admission, operating-system privilege, repository access, or possession of a copy substitute for disclosure authority.
- **REQ-SEC-PRIV-007 — SHALL:** Governance Policy Runtime, where required by the active profile, evaluate governed disclosure, consent, privilege, cultural-rights, and exception rules independently from Resource Governor decisions.
- **REQ-SEC-PRIV-008 — SHALL:** The owning component evaluate ordinary business access and data-use authority for its data while retaining the option to require a separate governance decision for governed disclosure.
- **REQ-SEC-PRIV-009 — SHALL:** Every cross-component data request use a declared interface and return an authorized view rather than direct access to another component's authoritative source records.
- **REQ-SEC-PRIV-010 — SHALL NOT:** A component, analytics process, indexer, workbench, integration, gateway, or auditor write directly to another component's authoritative source tables or convert a derived view into authoritative state without owner acceptance.
- **REQ-SEC-PRIV-011 — SHALL:** Every external transfer identify the selected source objects, representations, data classes, destination, audience, purpose, integration identity, authority references, consent or rights context, expiry, and failure behavior.
- **REQ-SEC-PRIV-012 — SHALL:** Publication Gateway control cross-domain disclosure, publication, and release to external audiences separately from kOA Mediatheque admission; UCKK publication shall use the authorized outbound adapter and disclose only the approved package, while UCKK import shall use a separate quarantined inbound path and preserve local acceptance authority.
- **REQ-SEC-PRIV-013 — SHALL NOT:** Successful transfer, upload, staging, or destination acceptance be reported as publication unless the Publication Gateway's authoritative commit state records completion.
- **REQ-SEC-PRIV-014 — SHALL:** External AI operations require explicit user initiation, a registered integration, a bounded capability, declared transferred data, an approved destination, and candidate-output handling.
- **REQ-SEC-PRIV-015 — SHALL NOT:** External AI outputs, voice-derived intents, enrichment results, or imported metadata become authoritative or trigger protected actions before provenance, validation, review, and owner acceptance.
- **REQ-SEC-PRIV-016 — SHALL:** Consent and cultural-rights conditions be evaluated at every applicable access, transformation, export, publication, reuse, audience expansion, and retention boundary.
- **REQ-SEC-PRIV-017 — SHALL:** A consent or rights record identify its scope, subject or community authority, permitted purposes, audiences, destinations, representations, validity, revocation behavior, attribution, reuse conditions, and evidence.
- **REQ-SEC-PRIV-018 — SHALL NOT:** Consent for one representation, audience, destination, purpose, or time interval be generalized silently to another.
- **REQ-SEC-PRIV-019 — SHALL:** Revocation, expiry, correction, restriction, or audience reduction prevent new incompatible disclosure and reevaluate pending operations while preserving required historical evidence.
- **REQ-SEC-PRIV-020 — SHALL:** Derived data, caches, indexes, previews, thumbnails, embeddings received from external sources, transcripts, analytics, and exported representations retain provenance, ownership, tenant, purpose, and disclosure constraints from their sources.
- **REQ-SEC-PRIV-021 — SHALL:** Public evidence and ordinary audit views expose only the fields needed to prove identity, authority class, decision, execution, commit, time, target class, and outcome.
- **REQ-SEC-PRIV-022 — SHALL:** Restricted evidence, private proof, secrets, credentials, private keys, personal data, protected cultural content, raw voice recordings, and unnecessary payloads remain behind explicit access authority and selective disclosure.
- **REQ-SEC-PRIV-023 — SHALL:** Access to restricted evidence produce an accountable access record when required by the active policy without copying the protected evidence into that access record.
- **REQ-SEC-PRIV-024 — SHALL:** Receipts for governed disclosure distinguish request, decision, execution, destination acceptance, authoritative commit, failure, cancellation, rollback, and reconciliation truthfully.
- **REQ-SEC-PRIV-025 — SHALL:** Privacy and disclosure failures remain capability-scoped, fail closed for the affected use, preserve independently authorized local access, and expose stable reason codes.
- **REQ-SEC-PRIV-026 — SHALL:** Offline operation enforce the last valid local privacy, disclosure, consent, cultural-rights, trust, and retention state without assuming approval from unavailable external authorities.
- **REQ-SEC-PRIV-027 — SHALL:** Backup, restore, migration, portability, export, and exit preserve classifications, ownership, tenant scope, consent and rights context, disclosure history, retention, deletion obligations, and evidence references.
- **REQ-SEC-PRIV-028 — SHALL:** Deletion and retention workflows distinguish authoritative records, derived data, caches, backups, receipts, legal or cultural holds, published copies, and externally transferred copies.
- **REQ-SEC-PRIV-029 — SHALL:** Users, subjects, communities, operators, and authorized representatives receive truthful notice, status, correction, restriction, revocation, export, challenge, and recourse paths where those capabilities apply.
- **REQ-SEC-PRIV-030 — SHALL:** Profile-specific encryption, residency, physical isolation, audit depth, retention, hardware, offline, and high-assurance controls remain explicit and cannot become global privacy requirements through repetition.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Collection or admission

Collection or admission follows this sequence:

1. resolve the owning component and tenant;
2. identify the source and subject or community context;
3. declare purpose and data classes;
4. resolve the authority, consent, and rights context;
5. minimize requested fields and precision;
6. validate retention and deletion behavior;
7. capture provenance;
8. admit the data into the owner's domain;
9. record notice or receipt where required;
10. reject or quarantine incomplete input.

### 6.2 Same-component use

The owning component:

1. authenticates the caller where required;
2. resolves the operation and purpose;
3. evaluates ordinary business authority;
4. selects required records and fields;
5. applies consent, rights, restriction, and retention conditions;
6. executes the operation;
7. records critical or restricted use where required.

### 6.3 Cross-component query

A cross-component query:

1. identifies source and destination components;
2. identifies tenant and purpose;
3. requests a declared view;
4. authenticates the caller and service;
5. evaluates owner and governance authority;
6. creates a minimized representation;
7. applies redaction and derived-data labels;
8. returns the bounded result;
9. records restricted access where required.

The receiving component cannot reuse the result for an undeclared purpose automatically.

### 6.4 External integration transfer

An external transfer:

1. resolves the registered integration and capability;
2. requires explicit user initiation where the integration is an approved external AI surface;
3. identifies selected source objects and representations;
4. evaluates disclosure, consent, and rights;
5. displays or records destination and transferred data classes;
6. applies minimization and redaction;
7. transfers under bounded credentials, timeout, retry, and resource limits;
8. records the transfer result;
9. imports returned material as candidate or quarantine state;
10. routes it to owner review and acceptance.

### 6.5 Publication request

A publication request:

1. identifies source ownership;
2. identifies selected representations;
3. declares audience, destination, purpose, and validity;
4. provides actor and authority context;
5. resolves consent and cultural-rights conditions;
6. creates the minimal publication package;
7. obtains the Publication Gateway decision;
8. transfers only after authorization;
9. records destination acceptance;
10. commits publication state;
11. produces a publication receipt.

### 6.6 Publication failure

When publication fails:

1. preserve the request and decision;
2. determine whether transfer started;
3. determine whether the destination accepted data;
4. determine whether authoritative publication commit occurred;
5. cancel or reconcile pending work;
6. record the actual state;
7. avoid reporting publication when commit did not occur;
8. preserve local source validity.

### 6.7 Consent or rights update

A consent or rights update:

1. verifies the authorized subject, community, or representative;
2. identifies the current scope;
3. records the new grant, restriction, correction, expiry, or revocation;
4. prevents incompatible new use;
5. reevaluates pending disclosures;
6. notifies affected owners and gateways;
7. updates derived-data and retention obligations;
8. preserves historical evidence;
9. records the transition.

### 6.8 Restricted evidence access

Restricted evidence access:

1. authenticates the requester;
2. identifies the evidence and requested fields;
3. evaluates purpose and authority;
4. creates a selective view;
5. redacts secrets and unrelated payloads;
6. returns the view;
7. records accountable access where required;
8. preserves the original evidence unchanged.

### 6.9 Correction

Correction:

1. resolves the canonical owner;
2. verifies subject or representative authority;
3. validates the proposed correction;
4. updates the authoritative record through the owner;
5. marks or regenerates affected derived data;
6. propagates correction notices through declared contracts;
7. preserves required history;
8. records the outcome.

A correction does not rewrite immutable receipts. A superseding or corrective receipt links to prior evidence.

### 6.10 Deletion and restriction

Deletion or restriction:

1. identifies authoritative, derived, cached, backup, published, and external copies;
2. resolves retention and hold constraints;
3. stops new incompatible use;
4. deletes, restricts, anonymizes, or retains each copy according to its owner contract;
5. issues bounded external requests where applicable;
6. records verified outcomes separately from requests;
7. preserves required receipts and identifiers;
8. reports unresolved external copies truthfully.

### 6.11 Portability and exit

Portability or exit:

1. verifies the requester and scope;
2. identifies owner-approved export classes;
3. applies consent, rights, disclosure, and minimization;
4. creates open, documented representations;
5. includes provenance, classifications, relationships, and restrictions;
6. verifies the export;
7. transfers or provides the package;
8. records delivery;
9. continues retention or deletion according to the exit contract.

### 6.12 Offline privacy evaluation

Offline processing:

1. uses the last valid local identity, trust, policy, consent, rights, and profile state;
2. rejects operations whose required authority is unavailable or stale beyond its bound;
3. preserves local ordinary access that remains valid;
4. buffers receipts within declared limits;
5. avoids claiming external transfer or publication completion without evidence;
6. reconciles after connectivity returns.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `privacy_owner_missing` | Data owner cannot be resolved | Processing and disclosure are denied | Preserve existing protected state |
| `privacy_purpose_missing` | Purpose is absent or too broad for the contract | Processing is denied | Request a bounded purpose |
| `privacy_data_class_unknown` | Data classification is absent or inactive | Protected use is denied | Quarantine or classify through the owner |
| `privacy_scope_mismatch` | Tenant, subject, component, audience, destination, or environment scope conflicts | Operation is denied | Use the correct scoped context |
| `privacy_minimization_failed` | A bounded representation cannot be produced | Disclosure is denied | Local owner use can continue where authorized |
| `privacy_authority_missing` | Required owner or governance authority is absent | Protected action is denied | Non-disclosive preparation where declared |
| `privacy_consent_missing` | Applicable consent is absent | Affected use is denied | Other authorized purposes remain |
| `privacy_consent_expired` | Consent validity has ended | New affected use is denied | Renewal or alternative authority path |
| `privacy_consent_revoked` | Consent or rights grant is revoked | New and pending incompatible use is blocked | Historical evidence remains protected |
| `privacy_cultural_rights_conflict` | Proposed use conflicts with active cultural-rights conditions | Access, transformation, or disclosure is denied | Owner-approved representation or audience |
| `privacy_cross_component_direct_access` | Caller attempts direct source-record access | Access is denied | Use an authorized component view |
| `privacy_external_integration_undefined` | Destination or transfer capability lacks an active integration contract | Transfer is denied | Native local capability continues |
| `privacy_external_candidate_unaccepted` | Returned external result lacks owner acceptance | Result remains candidate or quarantined | Source state remains authoritative |
| `privacy_publication_commit_unknown` | Transfer occurred but authoritative publication state is unresolved | Publication is not reported complete | Reconcile or record failure |
| `privacy_destination_scope_mismatch` | Destination does not match consent, rights, or authority | Transfer is denied | Select an approved destination |
| `privacy_selective_disclosure_failed` | Required redaction or proof projection cannot be created | Evidence view is denied | Protected evidence remains restricted |
| `privacy_restricted_evidence_authority_missing` | Restricted evidence requester lacks authority | Access is denied | Public or ordinary evidence view |
| `privacy_retention_conflict` | Deletion conflicts with a hold or required evidence | Immediate deletion is blocked | Restrict use and report retention reason |
| `privacy_external_deletion_unverified` | External destination deletion cannot be verified | Deletion is not reported complete | Preserve request and unresolved status |
| `privacy_offline_authority_stale` | Required local policy, consent, rights, or trust state exceeds its offline bound | Affected operation is denied | Independently valid local access continues |
| `privacy_receipt_path_unavailable` | Governed disclosure lacks its required receipt path | Critical disclosure is blocked | Non-critical local use continues where authorized |
| `privacy_status_ambiguous` | System cannot report request, decision, execution, or commit truthfully | New governed transition is blocked | Preserve current protected state |
| `privacy_backup_scope_mismatch` | Backup or restore changes tenant, rights, or classification scope | Restored copy remains inactive | Repair mapping or use another recovery point |
| `privacy_recourse_path_missing` | Required correction, challenge, or review path is unavailable | Affected automated closure is blocked | Escalate to accountable operator review |

Failure remains scoped to the affected purpose, representation, audience, destination, or operation. A denied publication does not invalidate the local source object. An unavailable external integration does not remove valid local capabilities.

## 8. Cross-Component Interactions

### 8.1 Owning components

Each component owns ordinary access to its data and produces authorized views.

It remains responsible for data accuracy, correction, derived-data behavior, retention, and component-level recourse.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates governed disclosure, consent, cultural rights, privilege, and bounded exceptions for applicable profiles.

Its decision does not transfer bytes or mutate another component's source data.

### 8.3 Publication Gateway

Publication Gateway owns cross-domain publication decision, audience, destination, transfer, commit, and receipt state.

It consumes selected representations rather than unrestricted source-table access.

### 8.4 kOA Mediatheque admission and UCKK publication

The kOA Mediatheque handles selected local media admission. Publication Gateway with the UCKK adapter handles controlled external publication after rights, consent, audience, and disclosure checks.

Its admission does not authorize public release.

### 8.5 Identity and Trust

Identity and Trust establishes subjects, services, representatives, communities where represented by approved identity records, signers, credentials, and trust.

It does not infer consent or disclosure rights from identity alone.

### 8.6 Audit Broker

Audit Broker stores and verifies receipts and produces authorized evidence views.

It does not receive unrestricted source payloads merely because an event is auditable.

### 8.7 External integrations

Integration manifests define endpoint, capability, authentication, transferred data, failure, and removal.

External AI results remain candidate inputs. Removing an optional integration leaves the native baseline operational.

### 8.8 Resource Governor

Resource Governor bounds privacy-related queries, exports, transformations, deletion jobs, and publication workers.

Capacity does not authorize collection or disclosure.

### 8.9 Backup and recovery

Backup services preserve classifications, ownership, tenant scope, consent and rights references, encryption context, retention, and recovery evidence.

Restore activates data only after the owning component validates the recovered context.

### 8.10 Development and test

Development workspaces use isolated identities, secrets, databases, logs, exports, and fixtures.

Production protected data enters development only through an explicit approved process with minimization and environment-specific authority.

## 9. Decision Closure and Prohibited Assumptions

This document closes the privacy and disclosure interpretation as follows:

- every protected operation has an owner and purpose;
- minimization applies to fields, precision, time, audience, destination, copies, and evidence;
- component ownership and governed disclosure authority are separate;
- identity, resource capacity, privilege, and reachability do not create disclosure authority;
- cross-component access uses authorized views;
- Publication Gateway owns external publication;
- kOA Mediatheque admission does not substitute for publication;
- the UCKK adapter does not substitute for Publication Gateway authorization;
- external AI transfer is explicit and candidate-only on return;
- consent and cultural rights are scoped and reevaluated at relevant boundaries;
- derived data retains provenance and constraints;
- public evidence remains separate from private proof;
- receipts report request, decision, execution, destination, and commit distinctly;
- deletion status distinguishes local and external copies;
- offline operation does not assume unavailable approval;
- recourse and correction remain visible.

The following assumptions are prohibited:

- internal network location makes data unrestricted;
- authenticated users can disclose every object they can view;
- a valid signature grants disclosure authority;
- a database administrator owns component data;
- public availability removes cultural-rights conditions;
- prior consent covers new audiences or destinations;
- one published representation authorizes every representation;
- derived data is ownerless;
- de-identification is automatically irreversible;
- audit requires raw payload disclosure;
- destination acceptance proves publication commit;
- an external deletion request proves deletion;
- an external AI provider can retain or reuse data outside its integration contract;
- a backup can omit consent and classification context;
- offline mode permits authority expansion;
- profile-specific residency or encryption choices apply globally.

A new global data class, purpose class, disclosure authority, consent semantic, public-proof model, or implicit reuse rule requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 30 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. every protected data class has an owner, classification, purposes, disclosure, retention, derived-data, backup, and deletion behavior;
7. every processing request identifies tenant, component, purpose, data classes, authority, recipients, retention, and expected outcome;
8. minimization tests cover fields, objects, precision, time, audience, destination, copies, derived data, and evidence;
9. purpose tests reject incompatible reuse without updated authority;
10. identity, trust, privilege, network, and resource tests prove they do not create disclosure authority;
11. cross-component tests reject direct source access and validate bounded views;
12. Publication Gateway tests cover request, decision, transfer, destination response, commit, failure, cancellation, and reconciliation;
13. tests prove that local Mediatheque admission does not create publication authority and that UCKK delivery requires explicit disclosure authorization;
14. integration tests identify destination, data classes, purpose, credential, timeout, retry, failure, and removal;
15. external AI tests require explicit user initiation and candidate-output handling;
16. consent tests cover scope, representation, purpose, audience, destination, validity, revocation, attribution, reuse, and evidence;
17. cultural-rights tests cover relevant access, transformation, export, publication, reuse, and retention boundaries;
18. derived-data tests preserve source owner, tenant, purpose, provenance, and disclosure constraints;
19. selective-disclosure tests prove ordinary evidence views exclude restricted payloads;
20. restricted-evidence tests require authority and produce accountable access evidence where required;
21. receipt tests distinguish request, decision, execution, destination acceptance, commit, rollback, failure, and reconciliation;
22. failure tests preserve valid local access while denying the affected disclosure;
23. offline tests prove local policy enforcement, expiry bounds, no assumed approval, bounded receipt buffering, and truthful status;
24. backup and restore tests preserve classification, consent, rights, tenant, owner, retention, and references;
25. deletion tests distinguish authoritative, derived, cache, backup, published, and external copies;
26. portability tests preserve open representations, provenance, relationships, and restrictions;
27. recourse tests cover notice, correction, restriction, revocation, export, challenge, and accountable owner;
28. profile tests keep encryption, residency, isolation, audit depth, hardware, retention, and offline controls profile-scoped;
29. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
30. active prose is English;
31. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

`text
privacy_owner_missing
privacy_purpose_missing
privacy_data_class_unknown
privacy_scope_mismatch
privacy_minimization_failed
privacy_authority_missing
privacy_consent_missing
privacy_consent_expired
privacy_consent_revoked
privacy_cultural_rights_conflict
privacy_cross_component_direct_access
privacy_external_integration_undefined
privacy_external_candidate_unaccepted
privacy_publication_commit_unknown
privacy_destination_scope_mismatch
privacy_selective_disclosure_failed
privacy_restricted_evidence_authority_missing
privacy_retention_conflict
privacy_external_deletion_unverified
privacy_offline_authority_stale
privacy_receipt_path_unavailable
privacy_status_ambiguous
privacy_backup_scope_mismatch
privacy_recourse_path_missing
`

## 11. Non-Normative Examples

### 11.1 Minimized cross-component query

Orgo needs a Konnaxion status indicator. Konnaxion returns a bounded status view rather than account records, internal notes, or source-table access. Orgo cannot reuse the view for unrelated analytics automatically.

### 11.2 External voice candidate

A user explicitly sends a short voice sample through the approved Ariane voice integration. The integration returns candidate text. The local Ariane runtime validates the command and obtains any required authority before the target component acts. The raw recording is not copied into an ordinary receipt.

### 11.3 Cultural audience restriction

A knowledge object permits access to a named community audience but prohibits public indexing and external AI transfer. Local authorized use continues. Publication Gateway denies a request for a public destination and records the reason without exposing the content.

### 11.4 Public proof

A public evidence view proves that a policy bundle was verified and activated at a given time. It exposes artifact identity, signer trust result, activation outcome, and receipt chain. It does not expose private keys, policy inputs, personal data, or restricted evidence.

### 11.5 Unverified external deletion

A user requests deletion of a locally owned export and its external copy. kOA deletes the local export and sends a request to the external destination. The status distinguishes local deletion from external deletion pending verification.
