<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global",
    "profile_conditioned_security",
    "external_integration"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/external_integrations",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/degradation_baseline",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-contracts/integration-manifest.schema.json",
    "contracts/examples/integration-manifest.example.yaml",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-001",
    "DEC-ARI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-INT-001",
    "REQ-SEC-INT-002",
    "REQ-SEC-INT-003",
    "REQ-SEC-INT-004",
    "REQ-SEC-INT-005",
    "REQ-SEC-INT-006",
    "REQ-SEC-INT-007",
    "REQ-SEC-INT-008",
    "REQ-SEC-INT-009",
    "REQ-SEC-INT-010",
    "REQ-SEC-INT-011",
    "REQ-SEC-INT-012",
    "REQ-SEC-INT-013",
    "REQ-SEC-INT-014",
    "REQ-SEC-INT-015",
    "REQ-SEC-INT-016",
    "REQ-SEC-INT-017",
    "REQ-SEC-INT-018",
    "REQ-SEC-INT-019",
    "REQ-SEC-INT-020",
    "REQ-SEC-INT-021",
    "REQ-SEC-INT-022",
    "REQ-SEC-INT-023",
    "REQ-SEC-INT-024",
    "REQ-SEC-INT-025",
    "REQ-SEC-INT-026",
    "REQ-SEC-INT-027",
    "REQ-SEC-INT-028",
    "REQ-SEC-INT-029",
    "REQ-SEC-INT-030",
    "REQ-SEC-INT-031",
    "REQ-SEC-INT-032",
    "REQ-SEC-INT-033",
    "REQ-SEC-INT-034",
    "REQ-SEC-INT-035",
    "REQ-SEC-INT-036",
    "REQ-SEC-INT-037",
    "REQ-SEC-INT-038",
    "REQ-SEC-INT-039",
    "REQ-SEC-INT-040",
    "REQ-SEC-INT-041",
    "REQ-SEC-INT-042",
    "REQ-SEC-INT-043",
    "REQ-SEC-INT-044"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-007",
    "DOC-SEC-008",
    "DOC-SEC-009",
    "DOC-SEC-011",
    "DOC-SEC-013",
    "DOC-SEC-014",
    "DOC-SEC-015",
    "DOC-SEC-017",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-016",
    "DOC-SYS-017"
  ],
  "tags": [
    "security",
    "external-integrations",
    "classification",
    "external-ai",
    "federation",
    "data-transfer",
    "egress",
    "candidate-output",
    "profile-applicability",
    "offline-degradation",
    "integration-manifest",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# External Integration Classification

## 1. Purpose

This document defines how kOA classifies, authorizes, operates, degrades, and retires integrations with systems outside the active kOA authority boundary.

An external integration can provide:

- a service;
- data;
- assertions;
- transport;
- external execution;
- a federation relationship;
- user-triggered assistance;
- artifact or dependency delivery.

The provider's technical capability and the authority granted to its result are separate facts.

For example, a provider can generate text, transform media, authenticate an identity, transmit a notification, or return a search result without gaining authority to:

- write canonical component state;
- grant privilege;
- create policy;
- activate a release;
- determine consent;
- publish binding output;
- transfer data ownership.

The classification model makes that separation machine-readable.

The canonical registry is:

```text
contracts/integration-types.contract.json
```

The human-readable model is:

```text
registry classification
        ↓
profile applicability
        ↓
validated integration manifest
        ↓
bounded adapter and network path
        ↓
request or transfer
        ↓
untrusted result or bounded external action
        ↓
destination validation and receipts
```

An integration remains unavailable until every required classification and authority field resolves.

## 2. Scope

### 2.1 Included integrations

This document applies to integrations such as:

- approved external AI surfaces;
- external media-generation or presentation services;
- external voice services;
- notification and delivery services;
- third-party data sources;
- federation peers;
- external identity or trust providers;
- external artifact and dependency repositories;
- external observability, support, or incident services;
- external action executors;
- registered webhooks and callbacks;
- other provider or peer relationships represented in the integration registry.

The current approved external AI surfaces include:

- ChatGPT;
- Suno;
- Gamma;
- Ariane external voice.

Their approval is capability-specific rather than general provider authority.

### 2.2 Excluded systems

This document does not classify as external integrations:

- native kOA components;
- component-to-component interfaces inside one active authority system;
- Resource Governor;
- Governance Policy Runtime;
- Publication Gateway;
- UCKK Dimension Gateway;
- local Ariane navigation;
- GF Wordbench;
- SemantiK Architect Runtime;
- SenTient.

SenTient is an optional isolated workbench, not an external provider integration.

Its outputs follow similar candidate-adoption controls but remain governed by its component contract and profile applicability.

### 2.3 Included lifecycle

The classification covers:

- proposal;
- registration;
- profile selection;
- adapter deployment;
- credential provisioning;
- network enablement;
- operation;
- degradation;
- disablement;
- revocation;
- replacement;
- retirement;
- evidence retention.

Exact state identifiers remain owned by the integration registry and manifest schema.

### 2.4 Profile interpretation

A registered integration is not globally enabled.

The effective profile decides whether the capability is:

- supported;
- prohibited;
- available only with an overlay;
- unavailable offline;
- available only to developers or operators;
- available only through a local peer;
- required for one profile-specific workflow;
- optional.

The `sovereign_offline` overlay excludes Internet-dependent external AI and provider operations.

Native local operation remains available without them.

## 3. Canonical References

### 3.1 Integration authority

```text
contracts/integration-types.contract.json
contracts/artifact-contracts/integration-manifest.schema.json
contracts/examples/integration-manifest.example.yaml
```

The registry owns integration identity, class, capability, authority role, profile applicability, and required controls.

The schema owns integration-manifest structure.

The example is non-authoritative.

### 3.2 System authority

```text
contracts/system.contract.json#/external_integrations
contracts/system.contract.json#/ai_boundary
contracts/system.contract.json#/global_boundaries
contracts/system.contract.json#/data_authority
contracts/system.contract.json#/degradation_baseline
```

### 3.3 Components and profiles

```text
generated/component-catalog.json
generated/component-catalog.json
generated/profile-catalog.json
contracts/profiles/*.profile.json
```

### 3.4 Security and lifecycle authority

```text
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
```

### 3.5 Related documents

```text
02-system/09-ai-boundary.md
02-system/10-external-ai-surfaces.md
02-system/16-external-integrations.md
02-system/17-capability-degradation.md
07-security/01-security-baseline.md
07-security/08-network-boundaries.md
07-security/11-ai-boundaries.md
07-security/13-privacy-and-disclosure.md
07-security/14-cultural-rights-and-consent.md
07-security/15-selective-audit.md
07-security/17-cross-domain-publication.md
```

## 4. Model and Responsibilities

### 4.1 Classification dimensions

Every integration is classified across independent dimensions.

| Dimension | Question |
| --- | --- |
| Provider class | What external capability or peer relationship exists? |
| Result authority | What authority, if any, can kOA accept from the result? |
| Direction | Does data move outward, inward, or both? |
| Trigger | Who or what initiates the operation? |
| Data classes | What information can cross the boundary? |
| State effect | Can the operation request a local state change, an external action, or only produce a candidate? |
| Profile applicability | Where is the integration permitted? |
| Connectivity | Is online connectivity required? |
| Criticality | Is the capability optional, workflow-dependent, profile-required, or recovery-critical? |
| Credentials | What identity and secret class authorizes the provider relationship? |
| Network exposure | Does the integration require egress, ingress, callbacks, or federation listeners? |
| Failure behavior | What capability becomes unavailable and what remains? |
| Adoption path | How does an inbound result become authoritative, if ever? |
| Evidence | What requests, transfers, results, and decisions are recorded? |
| Lifecycle | How is the integration enabled, disabled, revoked, replaced, and retired? |

These dimensions are orthogonal.

A bidirectional integration is not automatically authoritative.

A profile-required integration is not automatically permitted to write local state.

### 4.2 Provider classes

The exact enum is owned by the integration registry.

The following conceptual classes explain expected boundaries.

| Conceptual class | Typical provider capability | Default kOA treatment |
| --- | --- | --- |
| External AI candidate surface | Generates or transforms content | Non-authoritative candidate |
| External processing adapter | Performs bounded media, document, or computational processing | Candidate artifact or bounded processing result |
| External data source | Supplies observations, records, or reference data | Untrusted import requiring validation and ownership mapping |
| External action or delivery service | Sends a message, notification, payment-like instruction, or other external action | Bounded action result with request and provider receipt |
| Federation peer | Exchanges scoped peer state under a federation contract | Peer state limited to declared domains and conflict rules |
| External identity or trust provider | Supplies identity or trust assertions | Bounded assertion, never product authorization by itself |
| External artifact or dependency source | Supplies packages, images, updates, or reference artifacts | Untrusted artifact requiring supply-chain verification |
| External observability or support service | Receives selected telemetry or support data | Minimized export with no application authority |

Classification does not approve a provider.

The registry entry and active profile supply approval.

### 4.3 Result-authority classes

The most important classification is the authority accepted from the result.

#### Non-authoritative candidate

The result can be reviewed and imported.

It cannot change canonical state directly.

Examples include:

- ChatGPT draft output;
- Suno output;
- Gamma output;
- external enrichment;
- external translation candidate.

#### Bounded assertion

The result asserts a scoped fact, such as identity or verification status.

The consuming component still evaluates:

- issuer trust;
- scope;
- freshness;
- revocation;
- policy;
- target operation.

An assertion is not general authorization.

#### Bounded external action result

The provider reports whether one declared external action was accepted, completed, rejected, or failed.

The result does not prove unrelated local state.

A local component owns any corresponding local workflow transition.

#### Imported external data

The provider supplies data for controlled import.

The destination validates:

- identity;
- provenance;
- schema;
- rights;
- compatibility;
- duplicate and conflict behavior;
- ownership.

#### Federated peer state

A peer supplies state inside one declared federation domain.

The federation contract defines:

- peer identity;
- tenant or domain scope;
- ownership;
- conflict handling;
- revocation;
- withdrawal;
- evidence.

Peer state cannot escape those boundaries.

### 4.4 Trigger classes

A trigger identifies the initiating authority.

| Trigger | Interpretation |
| --- | --- |
| Explicit user action | One user initiates one visible bounded operation |
| Bounded component transaction | A component requests a declared provider operation as part of its contract |
| Authorized operator action | An operator initiates a maintenance or administrative integration |
| Declared schedule | A profile or component contract permits a scheduled operation |
| Registered event | An active contract permits an event-driven operation |
| Provider callback | A prior registered operation permits a bounded inbound callback |

External AI uses explicit user action.

It does not use background, scheduled, or autonomous triggers.

### 4.5 Direction classes

An integration declares each permitted direction.

#### Outbound-only

kOA sends a bounded request or notification.

The provider returns only transport or action status.

#### Inbound-only

A provider or peer submits a bounded artifact, assertion, callback, or message.

The inbound path is authenticated, rate-limited, schema-validated, and isolated.

#### Request-response

kOA sends a request and receives a bounded result.

External AI normally uses this pattern.

#### Bidirectional federation

Both sides exchange scoped peer state under one federation contract.

Network symmetry does not imply authority symmetry.

### 4.6 Data classification

An integration manifest declares permitted and prohibited data classes.

Possible permitted classes include:

- public content;
- user instruction;
- explicitly selected text;
- minimized internal metadata;
- approved structured request;
- declared external action payload;
- public artifact metadata;
- bounded identity assertion input.

Sensitive classes require additional controls.

Examples include:

- personal data;
- confidential organizational data;
- restricted cultural content;
- protected evidence;
- location data;
- unpublished governance material;
- private media.

Prohibited transfer classes include:

- private keys;
- unrestricted secrets;
- recovery material;
- foreign database credentials;
- full unapproved authoritative-store exports;
- undeclared personal data;
- undeclared restricted cultural content;
- machine privilege material.

### 4.7 Data minimization and representation

The source component creates the smallest representation required by the operation.

Minimization can include:

- field selection;
- redaction;
- pseudonymization;
- aggregation;
- truncation;
- format conversion;
- replacing payloads with references;
- removing unrelated history;
- excluding hidden application context.

A provider's maximum context capacity is not a transfer requirement.

### 4.8 User disclosure and confirmation

User-triggered transfers present enough information to support an informed action.

The interface can identify:

- provider;
- purpose;
- selected content;
- sensitive categories;
- destination;
- provider retention or reuse assumptions;
- expected result class;
- limitations;
- cancellation behavior.

Confirmation applies to the exact bounded request.

It does not create permanent consent for future background transfer.

### 4.9 Provider terms and data handling

Provider terms are security-relevant inputs.

The integration record resolves:

- service terms;
- retention;
- training or secondary reuse;
- data location;
- subprocessors where required;
- account configuration;
- deletion controls;
- incident notification;
- export or retrieval capability;
- rate and availability constraints.

When required terms cannot be resolved, the affected operation remains blocked.

Documentation memory of old terms is not sufficient authority.

### 4.10 Credentials

Integration credentials have:

- owner;
- provider account;
- environment;
- scope;
- capability;
- secret class;
- rotation;
- revocation;
- incident response;
- recovery;
- access evidence.

Development, validation, and production accounts remain separate where the integration contract requires it.

User credentials are not reused as broad service credentials without an explicit contract.

### 4.11 Network boundary

Integration network access defaults to deny.

The manifest declares:

- endpoint references;
- protocols;
- directions;
- DNS or name-resolution behavior;
- proxy behavior;
- TLS or transport protection;
- certificate validation;
- callback or webhook exposure;
- timeout;
- payload limit;
- rate limit;
- failure state.

An endpoint reference resolves through controlled configuration.

Hard-coded hidden endpoints are invalid.

### 4.12 Inbound callbacks and webhooks

Inbound callbacks are higher-risk than outbound request-response operations.

A callback contract addresses:

- provider identity;
- request authentication;
- replay protection;
- event identity;
- event age;
- idempotency;
- schema;
- size;
- rate;
- tenant and domain routing;
- unknown-event behavior;
- evidence;
- temporary failure and retry behavior.

A callback does not write directly to canonical state.

It enters the owning component through a registered interface.

### 4.13 Candidate adoption

Candidate-producing integrations use this flow:

```text
authorized source selection
        ↓
minimized controlled export
        ↓
external processing
        ↓
untrusted candidate + provenance
        ↓
controlled import
        ↓
destination validation and review
        ↓
explicit acceptance or rejection
```

The destination component owns:

- final validation;
- compatibility;
- policy and consent checks;
- conflict behavior;
- state mutation;
- rejection;
- evidence.

The external provider does not own adoption.

### 4.14 External action execution

An external action integration can perform one declared provider-side action.

Examples can include delivery, notification, or another registered remote operation.

The local request includes:

- action identity;
- requester;
- purpose;
- destination;
- payload;
- idempotency key;
- validity;
- retry policy;
- cancellation behavior.

The provider result is correlated to the request.

A provider success result does not mutate unrelated local state.

### 4.15 Federation

Federation is not a generic bidirectional API.

A federation contract defines:

- peer identity and trust;
- domains;
- ownership;
- object identity;
- versioning;
- conflict rules;
- revocation;
- withdrawal;
- privacy;
- cultural restrictions;
- replay;
- delivery;
- offline behavior;
- evidence;
- exit.

A peer receives only the authority explicitly delegated for the federation domain.

Transitive peer trust remains prohibited unless separately declared.

### 4.16 External identity and trust providers

An external identity or trust provider can produce bounded assertions.

The local system verifies:

- issuer;
- audience;
- subject;
- scope;
- time;
- nonce or replay state;
- revocation;
- assurance;
- tenant and domain;
- active profile.

The local component or Governance Policy Runtime still decides the operation.

Identity federation does not grant product, data, publication, release, or host privilege.

### 4.17 External artifact and dependency sources

External artifact sources remain supply-chain inputs.

Before use, the system verifies:

- artifact identity;
- source;
- integrity;
- provenance;
- signature;
- trust;
- revocation;
- license or policy where required;
- compatibility;
- artifact class;
- lifecycle state.

A package repository response does not become trusted merely because transport encryption succeeded.

### 4.18 External observability and support

External observability or support services receive selected minimized data.

They do not receive unrestricted:

- application databases;
- user content;
- secrets;
- protected cultural material;
- full evidence stores;
- private receipts;
- recovery material.

Support access is bounded, attributable, time-limited where required, and auditable.

### 4.19 External AI surfaces

Approved external AI surfaces remain optional.

#### ChatGPT

ChatGPT can support explicit user-requested candidate generation or analysis.

Transferred context is selected and minimized.

Output returns as candidate material.

#### Suno

Suno can process explicitly selected UCKK-related material through a controlled export.

Returned media remains candidate material.

Native UCKK does not invoke Suno automatically.

#### Gamma

Gamma can process explicitly selected material for a declared external presentation or media-generation workflow.

Returned output remains candidate material.

Native UCKK does not invoke Gamma automatically.

#### Ariane external voice

Ariane external voice supplies one optional voice capability.

It remains separate from local navigation.

Voice failure leaves local keyboard, pointer, touch, menus, shortcuts, accessibility controls, and deterministic commands available.

### 4.20 SenTient distinction

SenTient is not an external integration.

It is a local optional workbench limited to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`.

Its candidate outputs require the same destination-adoption boundary.

Its isolation, profiles, resources, and lifecycle remain owned by its component contract.

### 4.21 Publication classification

An integration operation that releases content to an external audience is classified as publication.

The controlled path is:

```text
source component
        ↓
disclosure policy and consent
        ↓
Publication Gateway
        ↓
external destination
        ↓
publication receipt
```

A provider adapter does not bypass Publication Gateway.

An external AI candidate workflow is not publication unless a later separate publication request is accepted.

### 4.22 UCKK integration classification

Native UCKK operation is local and deterministic.

UCKK Dimension Gateway handles explicit admission to UCKK dimensions.

Publication Gateway handles external publication.

Suno and Gamma handle optional external processing.

These are separate contracts.

No adapter absorbs the other gateway's authority.

### 4.23 Profile applicability

Integration applicability can vary by profile.

A profile record addresses:

- enabled capabilities;
- prohibited capabilities;
- required user or operator role;
- allowed data classes;
- network availability;
- secret source;
- local proxy or gateway;
- offline behavior;
- degraded behavior;
- evidence.

A developer profile can permit a test integration using separate credentials without making it available in production.

### 4.24 Offline behavior

Internet-dependent integrations become unavailable under `sovereign_offline`.

The system preserves:

- local identities;
- local policy;
- local Ariane navigation;
- local language runtime;
- native UCKK;
- local component workflows;
- local artifacts;
- recovery.

Queued external requests are not retained indefinitely by default.

A new explicit user action is required after service recovery unless the integration contract declares a different safe behavior.

### 4.25 Failure and degradation

Integration failure is capability-scoped.

Possible terminal results include:

- unavailable;
- blocked;
- rejected;
- timed out;
- provider failed;
- candidate invalid;
- action indeterminate;
- adoption rejected;
- revoked.

The integration record defines whether safe retry is possible.

Indeterminate external actions receive reconciliation rather than blind replay.

### 4.26 Retry and idempotency

Retry is permitted only for declared transient conditions.

A retryable state identifies:

- request identity;
- idempotency key;
- provider behavior;
- maximum attempts;
- backoff;
- expiration;
- cancellation;
- evidence.

Authentication rejection, prohibited data, missing consent, invalid authority, and contract failure do not use automatic retry.

### 4.27 Receipts

Integration receipts can cover:

- authorization;
- user confirmation;
- transfer;
- provider request;
- provider result;
- candidate creation;
- destination adoption;
- external action completion;
- publication;
- failure;
- revocation;
- removal.

Receipts contain references and summaries rather than raw payloads by default.

### 4.28 Observability

Integration observability can include:

- operation identity;
- profile;
- adapter version;
- endpoint reference;
- duration;
- bytes transferred;
- result;
- retry count;
- provider rate-limit state;
- candidate or external action reference;
- adoption result;
- degradation state.

Sensitive payloads and credentials remain excluded from general logs.

### 4.29 Integration manifest

A conforming manifest addresses:

- manifest and integration identity;
- classification;
- profile applicability;
- activation;
- operations;
- transfer contracts;
- authority and adoption;
- authentication;
- network;
- security and privacy;
- resources and resilience;
- offline and degradation;
- receipts and observability;
- failures;
- lifecycle;
- validation;
- traceability.

The schema owns exact field names and enums.

### 4.30 Lifecycle

An integration lifecycle can include:

```text
registered
configured
enabled
degraded
disabled
revoked
superseded
retired
```

The registry owns canonical states.

Enablement requires validated configuration, credentials, network policy, profile compatibility, and evidence readiness.

Disablement removes active use without necessarily deleting historical receipts.

Revocation stops trust and use immediately according to incident policy.

Retirement preserves identity and history.

### 4.31 Removal

Removal closes:

- adapter processes;
- credentials;
- provider accounts where applicable;
- endpoint allowlists;
- inbound listeners;
- callbacks;
- scheduled jobs;
- queues;
- pending requests;
- local staging;
- generated configuration.

Removal preserves required:

- receipts;
- candidate dispositions;
- external action reconciliation;
- audit;
- incident evidence;
- identifier history.

Native core operation is verified after removal.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-INT-001,REQ-SEC-INT-002,REQ-SEC-INT-003,REQ-SEC-INT-004,REQ-SEC-INT-005,REQ-SEC-INT-006,REQ-SEC-INT-007,REQ-SEC-INT-008,REQ-SEC-INT-009,REQ-SEC-INT-010,REQ-SEC-INT-011,REQ-SEC-INT-012,REQ-SEC-INT-013,REQ-SEC-INT-014,REQ-SEC-INT-015,REQ-SEC-INT-016,REQ-SEC-INT-017,REQ-SEC-INT-018,REQ-SEC-INT-019,REQ-SEC-INT-020,REQ-SEC-INT-021,REQ-SEC-INT-022,REQ-SEC-INT-023,REQ-SEC-INT-024,REQ-SEC-INT-025,REQ-SEC-INT-026,REQ-SEC-INT-027,REQ-SEC-INT-028,REQ-SEC-INT-029,REQ-SEC-INT-030,REQ-SEC-INT-031,REQ-SEC-INT-032,REQ-SEC-INT-033,REQ-SEC-INT-034,REQ-SEC-INT-035,REQ-SEC-INT-036,REQ-SEC-INT-037,REQ-SEC-INT-038,REQ-SEC-INT-039,REQ-SEC-INT-040,REQ-SEC-INT-041,REQ-SEC-INT-042,REQ-SEC-INT-043,REQ-SEC-INT-044 -->
- **REQ-SEC-INT-001 — SHALL:** Every external integration have one active registry entry and one explicit owner before it can be enabled.
- **REQ-SEC-INT-002 — SHALL:** Every external integration declare its provider or peer, capability, classification, authority role, direction, trigger, profiles, data classes, credentials, network endpoints, failure behavior, and removal behavior.
- **REQ-SEC-INT-003 — SHALL:** Every enabled integration resolve to a validated integration manifest compatible with the active integration registry and effective profile.
- **REQ-SEC-INT-004 — SHALL NOT:** Repository presence, installed software, reachable endpoints, provider accounts, environment variables, or user familiarity enable an integration implicitly.
- **REQ-SEC-INT-005 — SHALL:** Integration classification distinguish provider capability from the authority kOA grants to the result.
- **REQ-SEC-INT-006 — SHALL NOT:** An external provider's ability to generate, transform, store, transmit, authenticate, or execute content create authority over canonical kOA state.
- **REQ-SEC-INT-007 — SHALL:** Every integration declare whether its result is candidate input, bounded assertion, bounded external action result, imported external data, or federated peer state.
- **REQ-SEC-INT-008 — SHALL:** Every outbound transfer declare source owner, requesting actor, requesting component, purpose, selected fields, data classes, destination, retention assumptions, and required consent or policy decisions.
- **REQ-SEC-INT-009 — SHALL:** Outbound data be minimized to the fields and representations required for the declared operation.
- **REQ-SEC-INT-010 — SHALL NOT:** Secrets, private keys, unrestricted credentials, foreign database credentials, undeclared personal data, or undeclared restricted cultural content be sent through an integration.
- **REQ-SEC-INT-011 — SHALL:** Every inbound response, callback, artifact, assertion, or peer message be treated as untrusted until its applicable identity, integrity, schema, provenance, policy, and compatibility checks pass.
- **REQ-SEC-INT-012 — SHALL:** Every candidate-producing integration preserve source ownership and require controlled import, destination validation, and explicit authoritative acceptance.
- **REQ-SEC-INT-013 — SHALL NOT:** An external integration write directly to another component's authoritative database, source files, queues, indexes, policy stores, identity stores, release stores, or publication state.
- **REQ-SEC-INT-014 — SHALL:** Every integration use registered component interfaces, artifacts, commands, events, or governed gateways for all state-changing interactions.
- **REQ-SEC-INT-015 — SHALL:** Every integration declare an activation trigger of explicit user action, bounded component transaction, authorized operator action, declared schedule, or registered event.
- **REQ-SEC-INT-016 — SHALL NOT:** An integration run autonomously, in the background, on a schedule, or from an event unless that trigger is explicitly permitted by its classification and active profile.
- **REQ-SEC-INT-017 — SHALL:** Approved external AI operations be initiated explicitly by a user for one declared capability and one bounded request.
- **REQ-SEC-INT-018 — SHALL NOT:** ChatGPT, Suno, Gamma, Ariane external voice, or another external AI surface be invoked automatically by ingestion, indexing, classification, routing, policy, release, recovery, or privilege workflows.
- **REQ-SEC-INT-019 — SHALL:** Every external AI output remain non-authoritative candidate material until provenance, review, controlled import, destination validation, and explicit acceptance complete.
- **REQ-SEC-INT-020 — SHALL NOT:** An external AI result grant privilege, create policy authority, select an active release, determine final consent or cultural rights, publish binding output, or become the sole path to correctness or recovery.
- **REQ-SEC-INT-021 — SHALL:** Every integration declare profile applicability, overlay compatibility, network dependency, offline behavior, and unsupported-profile result.
- **REQ-SEC-INT-022 — SHALL NOT:** A profile-specific integration requirement become global through implementation prevalence, documentation repetition, or provider availability.
- **REQ-SEC-INT-023 — SHALL:** The `sovereign_offline` overlay prohibit Internet-dependent integrations unless a separate accepted profile decision defines a bounded local or deferred behavior without weakening offline authority.
- **REQ-SEC-INT-024 — SHALL:** Failure or removal of an optional integration preserve all unrelated native and local capabilities.
- **REQ-SEC-INT-025 — SHALL NOT:** Integration failure activate a silent alternate provider, local AI model, stale credential, weaker policy, broader data transfer, or direct authoritative fallback.
- **REQ-SEC-INT-026 — SHALL:** Every integration declare bounded timeouts, attempts, backoff, concurrency, queueing, payload size, and provider-rate-limit behavior.
- **REQ-SEC-INT-027 — SHALL NOT:** An integration use unbounded retries, unbounded payloads, unbounded callbacks, or unbounded queued work.
- **REQ-SEC-INT-028 — SHALL:** Integration network policy default to deny and permit only declared endpoints, directions, protocols, identities, and purposes.
- **REQ-SEC-INT-029 — SHALL NOT:** Inbound provider connectivity, webhooks, callbacks, remote administration, or federation listeners exist unless explicitly declared and protected by their integration contract.
- **REQ-SEC-INT-030 — SHALL:** Integration credentials use dedicated owners, environments, scopes, rotation, revocation, and protected secret references.
- **REQ-SEC-INT-031 — SHALL NOT:** Integration credentials be embedded in source, images, manifests, build arguments, general logs, receipts, candidate artifacts, or user-visible error messages.
- **REQ-SEC-INT-032 — SHALL:** Every integration declare applicable provider terms, data retention, training or reuse behavior, data location, account separation, and unresolved-terms failure behavior.
- **REQ-SEC-INT-033 — SHALL:** A transfer involving personal, confidential, restricted, culturally governed, or regulated content resolve all applicable purpose, consent, audience, minimization, and disclosure controls before transmission.
- **REQ-SEC-INT-034 — SHALL:** Federated integrations preserve tenant, domain, identity, provenance, policy, revocation, and conflict boundaries defined by the federation contract.
- **REQ-SEC-INT-035 — SHALL NOT:** A federation peer gain transitive trust, local machine privilege, foreign tenant authority, or unrestricted write access from network membership alone.
- **REQ-SEC-INT-036 — SHALL:** Publication Gateway remain the only registered cross-domain publication executor for workflows classified as external publication.
- **REQ-SEC-INT-037 — SHALL:** UCKK Dimension Gateway remain separate from Publication Gateway and from Suno or Gamma external-processing adapters.
- **REQ-SEC-INT-038 — SHALL:** Every integration produce the request, transfer, provider-result, candidate, adoption, publication, or failure receipts required by its classification without placing raw payloads in receipts by default.
- **REQ-SEC-INT-039 — SHALL:** Integration observability identify operation, profile, endpoint reference, result, duration, retry state, candidate or action reference, and correlation identity while minimizing sensitive content.
- **REQ-SEC-INT-040 — SHALL:** Every integration define lifecycle states for registration, enablement, disablement, degradation, revocation, replacement, and retirement as applicable.
- **REQ-SEC-INT-041 — SHALL:** Integration removal revoke credentials, close network paths, stop adapters, preserve required evidence, reconcile pending candidates or actions, and verify native capability independence.
- **REQ-SEC-INT-042 — SHALL NOT:** A retired, revoked, removed, or superseded integration identifier be reused.
- **REQ-SEC-INT-043 — SHALL:** Every conformance claim bind the exact integration registry version, manifest, profile, adapter artifact, endpoint policy, credentials class, tests, and evidence.
- **REQ-SEC-INT-044 — SHALL:** A semantic change to integration classification, authority, trigger, data transfer, credentials, provider terms, profile applicability, degradation, adoption, federation, publication, or lifecycle use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Register an integration

1. Identify the provider or peer.
2. identify the capability and owner.
3. classify provider capability and result authority.
4. classify direction and trigger.
5. define permitted and prohibited data classes.
6. define profile and overlay applicability.
7. define credentials and network endpoints.
8. define terms, retention, and data handling.
9. define adoption or external-action behavior.
10. define failure, degradation, and removal.
11. define tests and evidence.
12. create the registry entry.
13. validate the integration manifest.
14. keep the integration disabled until all authority resolves.

### 6.2 Enable an integration

1. Resolve the active registry entry.
2. resolve the effective profile.
3. validate the manifest.
4. verify adapter artifact identity.
5. provision scoped credentials.
6. apply default-deny network policy.
7. verify endpoint configuration.
8. verify receipts and evidence paths.
9. run connectivity and negative tests.
10. verify native capability independence.
11. enable the bounded capability.
12. record enablement evidence.

### 6.3 Execute a user-triggered external AI request

1. Identify the user, requesting component, capability, and purpose.
2. select the exact source material.
3. classify and minimize the payload.
4. resolve consent, disclosure, privacy, and cultural-rights constraints.
5. present provider and transfer information.
6. obtain explicit confirmation.
7. create request and correlation identities.
8. resolve scoped credentials and endpoint policy.
9. perform one bounded request.
10. validate the response as untrusted input.
11. create candidate identity and provenance.
12. submit the candidate to the destination component.
13. record adoption or rejection separately.

### 6.4 Execute a bounded external action

1. Resolve the operation contract.
2. authenticate the requester.
3. validate destination and payload.
4. apply policy and consent.
5. create an idempotency key.
6. send the bounded request.
7. receive provider acceptance or terminal result.
8. reconcile indeterminate results before retry.
9. let the owning component update its local workflow.
10. record provider and local receipts.

### 6.5 Receive an inbound callback

1. Accept only on the registered endpoint.
2. authenticate the provider.
3. verify event identity, age, and replay state.
4. enforce size and rate limits.
5. validate schema and tenant or domain routing.
6. reject unknown or unsupported events.
7. pass the event to the owning component interface.
8. process idempotently.
9. return a bounded response.
10. retain selected evidence.

### 6.6 Import external data or an artifact

1. Identify source and expected artifact or data contract.
2. receive through the registered boundary.
3. quarantine the input.
4. verify identity, integrity, provenance, and trust.
5. validate schema, size, rights, and compatibility.
6. identify destination owner.
7. resolve duplicate and conflict behavior.
8. obtain required review or policy decisions.
9. invoke the destination import interface.
10. accept or reject authoritatively.
11. preserve source and destination ownership.
12. record import evidence.

### 6.7 Establish federation

1. Identify the peer and federation domain.
2. establish trust roots and revocation behavior.
3. define objects and ownership.
4. define tenant and security-domain mapping.
5. define conflict and replay behavior.
6. define privacy, consent, and cultural restrictions.
7. define network and callback paths.
8. define offline and withdrawal behavior.
9. test positive and negative cases.
10. enable only the declared federation scope.
11. record peer and lifecycle evidence.

### 6.8 Handle provider unavailability

1. Mark the integration capability unavailable.
2. stop new provider requests.
3. resolve pending request state.
4. reconcile indeterminate external actions.
5. preserve native and unrelated local capability.
6. report user-visible status.
7. avoid silent provider or local AI substitution.
8. recover credentials or connectivity.
9. require a new explicit request where the manifest specifies it.
10. record degradation and recovery evidence.

### 6.9 Revoke an integration

1. Identify revocation reason and scope.
2. stop new requests.
3. revoke credentials and provider sessions.
4. close endpoint allowlists and inbound listeners.
5. quarantine untrusted pending outputs.
6. identify affected candidates, external actions, and releases.
7. preserve incident evidence.
8. reconcile provider-side state where possible.
9. update registry lifecycle state.
10. verify native capability independence.

### 6.10 Remove or retire an integration

1. Disable the capability.
2. drain or cancel pending requests safely.
3. revoke and remove credentials.
4. remove network configuration.
5. stop and remove adapter services.
6. reconcile pending candidates and action results.
7. retain required receipts and evidence.
8. remove profile selection.
9. reserve the identifier.
10. verify complete core operation without the integration.
11. publish retirement or removal evidence.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Registry entry is missing | Keep integration disabled | Native system | Integration |
| Manifest is invalid | Keep integration disabled | Native system and prior valid configuration | New configuration |
| Profile does not permit the integration | Report unavailable | Profile-native capability | Integration operation |
| Required user confirmation is missing | Block request | Source and destination state | Transfer |
| Data minimization fails | Block request | Source state | External transfer |
| Prohibited data is detected | Block and record reason | All authoritative state | External transfer |
| Provider terms are unresolved | Block affected operation | Native capability | Provider request |
| Credential cannot be resolved | Mark unavailable | Native capability | Authenticated provider operation |
| Credential is compromised | Revoke integration authority | Unaffected integrations and local core | New provider use |
| Endpoint is undeclared | Block network request | Local state | External connection |
| TLS or provider identity verification fails | Block and report | Local state | External connection |
| Provider rate limit is reached | Defer or reject according to manifest | Local core | New request |
| Provider is unavailable | Disable affected capability | Native local operation | Provider operation |
| Response schema or provenance is invalid | Reject or quarantine result | Destination state | Adoption |
| External action result is indeterminate | Reconcile before retry | Existing local state | Blind replay |
| Callback authentication fails | Reject callback | Existing state | Callback processing |
| Replay is detected | Reject duplicate | Existing state | Duplicate action |
| Federation trust is stale | Block affected peer operations | Other peers and local data | New peer state |
| Destination validation rejects candidate | Record rejection | Previous authoritative state | Adoption |
| Publication Gateway is unavailable | Block external publication | Source state and internal workflows | Publication |
| Offline overlay is active | Disable Internet-dependent integration | Local offline capability | External request |
| Receipt path is unavailable | Apply manifest evidence policy | Existing state | Receipt-critical transition |
| Removal is incomplete | Keep lifecycle open and capability disabled | Native core | Complete retirement claim |
| Complete validation cannot execute | Keep prior valid state | Native system and prior integration configuration | New conformance claim |

Safe degradation removes only the affected external capability.

It does not relax data classification, consent, policy, network, credentials, candidate adoption, or publication controls.

## 8. Cross-Component Interactions

### 8.1 Requesting component

The requesting component owns:

- request purpose;
- source authority;
- selected representation;
- local workflow;
- result interpretation;
- resulting local state.

The adapter does not acquire source ownership.

### 8.2 Destination component

For candidate and imported-data workflows, the destination component owns:

- validation;
- compatibility;
- conflict behavior;
- review;
- acceptance or rejection;
- authoritative state mutation;
- adoption evidence.

### 8.3 Identity and Trust

Identity and Trust verifies users, workloads, providers, peers, signers, assertions, and artifacts where applicable.

It does not grant the final component operation.

### 8.4 Governance Policy Runtime

Governance Policy Runtime can evaluate:

- transfer authorization;
- disclosure;
- consent;
- privilege;
- exception use.

It does not make the network request or adopt the result.

### 8.5 Resource Governor

Resource Governor controls local adapter, queue, parser, transfer, and processing resources.

It does not approve provider use or data disclosure.

### 8.6 Publication Gateway

Publication Gateway owns cross-domain publication execution.

Provider-specific transport can exist behind its registered adapter boundary.

A direct provider call from a source component is not a valid publication path.

### 8.7 UCKK Dimension Gateway

UCKK Dimension Gateway owns explicit media admission to UCKK.

Suno and Gamma adapters own external request and candidate-return behavior only.

Publication Gateway owns later external publication.

### 8.8 Audit Broker

Audit Broker receives selected transfer, provider, candidate, adoption, publication, failure, revocation, and removal evidence.

It does not store unrestricted provider payloads by default.

### 8.9 Profiles

Profiles enable or prohibit integration capabilities and strengthen:

- credential assurance;
- network isolation;
- data restrictions;
- review;
- evidence;
- offline behavior;
- provider account separation.

### 8.10 Artifact lifecycle

Adapters and integration manifests are versioned release artifacts where their contracts classify them as such.

Publication and activation follow the applicable release channel and Release Set rules.

Provider configuration changes do not bypass lifecycle validation.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-AI-001` | Approved external AI surfaces are explicit, removable, user-triggered, and non-authoritative |
| `DEC-SENT-001` | SenTient is a local optional workbench rather than an external integration |
| `DEC-UCKK-001` | Native UCKK is deterministic and local; Suno and Gamma remain explicit external adapters |
| `DEC-ARI-001` | Ariane local navigation remains independent of optional external voice |
| `DEC-PROFILE-001` | Integration applicability remains profile-specific |
| `DEC-DATA-001` | Integrations cannot write directly to foreign authoritative state |
| `DEC-GOV-001` | Policy and resource authority remain outside provider adapters |
| `DEC-GATE-001` | Publication Gateway and UCKK Dimension Gateway remain separate |

### 9.2 Protected locks

| Lock | Protected boundary |
| --- | --- |
| `LOCK-AI-001` | No native external-AI dependency enters the baseline |
| `LOCK-AI-002` | External AI output remains candidate input |
| `LOCK-SENT-001` | SenTient remains optional, local, isolated, and non-authoritative |
| `LOCK-UCKK-001` | Native UCKK remains deterministic |
| `LOCK-UCKK-002` | Suno and Gamma remain user-triggered external adapters |
| `LOCK-ARI-001` | Local Ariane navigation remains non-AI |
| `LOCK-ARI-002` | Voice failure does not disable local navigation |
| `LOCK-DATA-001` | No direct foreign authoritative write |
| `LOCK-GOV-001` | Provider adapters do not merge policy and resource authority |
| `LOCK-GATE-001` | External publication and UCKK dimension admission remain separate |
| `LOCK-PROFILE-001` | Profile-specific integration rules do not become global |
| `LOCK-LIFE-001` | Adapter and manifest artifacts do not activate partially |
| `LOCK-LIFE-003` | Release Set compatibility remains explicit |
| `LOCK-IMPL-001` | Example configuration does not define integration authority |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- a reachable provider is approved;
- an API key enables a capability;
- installed adapter code enables a capability;
- a provider's technical ability creates local authority;
- a user once consented to every future request;
- a long context window justifies transferring more data;
- provider encryption permits secret transfer;
- external AI output is authoritative because it is useful;
- a provider response can update a database directly;
- an identity assertion is authorization;
- federation membership creates transitive trust;
- a callback endpoint can process unknown events;
- retries are always safe;
- a timeout means an external action did not occur;
- a provider success result proves every local obligation;
- an optional provider can become core through frequent use;
- `sovereign_offline` can queue Internet requests indefinitely;
- a local AI model is an automatic fallback;
- ChatGPT can run background classification;
- Suno or Gamma can run from native UCKK ingestion;
- Ariane voice can replace local navigation silently;
- SenTient is an external provider;
- Publication Gateway is merely one optional HTTP adapter;
- UCKK Dimension Gateway can perform publication;
- external support services can receive unrestricted logs;
- provider terms can be assumed unchanged;
- test credentials can be reused in production;
- one credential can serve all environments;
- webhook transport creates component authority;
- repository examples are production configuration;
- integration removal permits identifier reuse;
- unavailable tests can support conformance.

Missing registry, profile, terms, consent, data classification, credential, endpoint, adoption, federation, lifecycle, or evidence authority blocks the affected integration operation.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-SEC-012`;
2. the path is `07-security/12-external-integration-classification.md`;
3. the active language is English;
4. every enabled integration has one active registry entry;
5. every integration has an explicit owner;
6. provider capability and result authority are distinct;
7. direction and trigger are explicit;
8. outbound data has source, purpose, fields, classes, destination, and authority;
9. transfer minimization passes;
10. prohibited data cannot leave the boundary;
11. inbound results are treated as untrusted;
12. candidate results require controlled destination adoption;
13. direct authoritative writes are rejected;
14. background, scheduled, event, and callback triggers require explicit authority;
15. external AI is explicitly user-triggered;
16. ChatGPT, Suno, Gamma, and Ariane external voice are absent from autonomous workflows;
17. external AI output remains candidate material;
18. external AI cannot grant privilege, policy, release, consent, or publication authority;
19. profile and overlay applicability resolves;
20. Internet-dependent integrations are prohibited under `sovereign_offline`;
21. optional integration failure preserves native capability;
22. no silent provider or local AI fallback occurs;
23. timeouts, retries, queues, concurrency, and payloads are bounded;
24. network policy defaults to deny;
25. inbound listeners and callbacks have explicit contracts;
26. credentials are dedicated, scoped, rotated, and protected;
27. credentials are absent from source, images, manifests, logs, and receipts;
28. provider terms and data handling resolve;
29. sensitive transfers satisfy purpose, consent, rights, and disclosure controls;
30. federation preserves tenant, domain, trust, conflict, and withdrawal boundaries;
31. federation does not create transitive trust or privilege;
32. Publication Gateway remains the publication executor;
33. UCKK admission, external processing, and publication remain separate;
34. receipts are complete and minimized;
35. observability excludes sensitive payloads;
36. lifecycle state and removal behavior resolve;
37. removal closes credentials, endpoints, adapters, and pending work;
38. retired integration identifiers remain reserved;
39. conformance binds exact registry, manifest, profile, adapter, endpoint, tests, and evidence;
40. semantic changes include accepted decisions and impact analysis;
41. all 44 linked requirements resolve;
42. all required tests execute;
43. all required evidence validates;
44. no unresolved integration authority remains;
45. generated catalogs and AI context match canonical authority;
46. complete documentation validation passes.

Expected test coverage includes:

```text
TEST-SEC-INT-001  Integration registry and owner resolution
TEST-SEC-INT-002  Provider capability and result-authority separation
TEST-SEC-INT-003  Manifest schema and registry alignment
TEST-SEC-INT-004  Explicit trigger classification
TEST-SEC-INT-005  Outbound data minimization
TEST-SEC-INT-006  Prohibited data rejection
TEST-SEC-INT-007  Inbound untrusted-result handling
TEST-SEC-INT-008  Candidate adoption boundary
TEST-SEC-INT-009  Direct authoritative-write rejection
TEST-SEC-INT-010  External AI explicit user trigger
TEST-SEC-INT-011  No automatic ChatGPT, Suno, Gamma, or voice invocation
TEST-SEC-INT-012  Profile and overlay applicability
TEST-SEC-INT-013  Sovereign-offline prohibition
TEST-SEC-INT-014  Capability-scoped degradation
TEST-SEC-INT-015  No silent provider or local AI fallback
TEST-SEC-INT-016  Bounded timeout, retry, queue, and concurrency
TEST-SEC-INT-017  Default-deny endpoint policy
TEST-SEC-INT-018  Callback authentication, replay, and idempotency
TEST-SEC-INT-019  Credential isolation and secret exclusion
TEST-SEC-INT-020  Provider terms and retention resolution
TEST-SEC-INT-021  Sensitive-content consent and disclosure controls
TEST-SEC-INT-022  Federation trust and tenant isolation
TEST-SEC-INT-023  Publication Gateway enforcement
TEST-SEC-INT-024  UCKK gateway and external-adapter separation
TEST-SEC-INT-025  Receipt and observability minimization
TEST-SEC-INT-026  Revocation, removal, and identifier reservation
```

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid classifications. They do not replace the integration registry or manifest schema.

### 11.1 ChatGPT draft assistance

Classification:

- provider class: external AI candidate surface;
- result authority: non-authoritative candidate;
- direction: request-response;
- trigger: explicit user action;
- criticality: optional;
- offline behavior: unavailable;
- adoption: destination validation and explicit acceptance.

The user selects text and confirms the transfer.

The returned draft cannot update the source component directly.

### 11.2 Suno media workflow

Classification:

- provider class: external processing adapter;
- result authority: candidate media;
- direction: request-response;
- trigger: explicit user action;
- source: explicit UCKK selection;
- destination: controlled UCKK re-import;
- publication: separate later workflow.

Native UCKK ingestion remains deterministic and local.

### 11.3 Ariane external voice

Classification:

- provider class: external AI or voice service;
- result authority: bounded interaction result;
- trigger: explicit user voice interaction;
- criticality: optional;
- offline behavior: unavailable;
- degradation: local navigation preserved.

The provider cannot perform arbitrary component actions without local command validation and authorization.

### 11.4 External identity provider

Classification:

- provider class: external identity or trust provider;
- result authority: bounded identity assertion;
- direction: request-response or callback;
- trigger: user authentication flow;
- local decision: component authorization remains local.

A valid assertion does not grant product, release, publication, or host privilege.

### 11.5 Federation peer

Classification:

- provider class: federation peer;
- result authority: peer state inside one declared domain;
- direction: bidirectional;
- trigger: registered events and synchronization;
- trust: peer-scoped;
- conflicts: contract-defined;
- exit: withdrawal and retained evidence.

The peer cannot access unrelated tenants or local machine privilege.

### 11.6 External notification service

Classification:

- provider class: external action or delivery service;
- result authority: bounded delivery status;
- direction: request-response with optional callback;
- trigger: bounded component transaction;
- retry: idempotent and limited;
- local state: owned by the requesting component.

A provider timeout is reconciled before another delivery attempt.

### 11.7 Sovereign-offline profile

An Internet-dependent integration is registered but disabled by the active overlay.

The UI reports unavailable status.

Local navigation, UCKK, language runtime, governance, recovery, and native workflows remain available.

No request is silently redirected to another provider.

### 11.8 Invalid direct adoption

An external AI adapter receives a response and writes it directly into Konnaxion's authoritative tables.

The design is invalid.

The valid path creates a candidate and invokes Konnaxion's controlled import and acceptance interface.

### 11.9 Invalid background AI

A scheduled job sends every new UCKK file to an external AI service for automatic classification.

The design is invalid because external AI must be explicitly user-triggered and native UCKK ingestion remains deterministic and non-AI.

### 11.10 Invalid integration removal

An adapter process is deleted, but its credentials, callback endpoint, scheduled job, network allowlist, and pending queue remain active.

The integration is not fully removed and its lifecycle cannot be marked retired.
