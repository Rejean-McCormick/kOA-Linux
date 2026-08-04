<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-022",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "component:uckk-platform"
  ],
  "adr_id": "ADR-022",
  "decision_class": "major",
  "decision_owner": "system-architecture",
  "accepted_at": "2026-08-03T15:13:00-04:00",
  "effective_at": "2026-08-03T15:13:00-04:00",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/uckk",
    "generated/component-catalog.json#/components/uckk-platform",
    "generated/component-catalog.json#/components/uckk-dimension-gateway",
    "generated/component-catalog.json#/components/publication-gateway",
    "contracts/subsystems/uckk.subsystem.json",
    "contracts/components/uckk-dimension-gateway.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-UCKK-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-LIFE-001",
    "DEC-AUDIT-001",
    "DEC-RECEIPT-001",
    "DEC-PORT-001",
    "DEC-INTEGRATION-001",
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-ADR-022-001",
    "REQ-ADR-022-002",
    "REQ-ADR-022-003",
    "REQ-ADR-022-004",
    "REQ-ADR-022-005",
    "REQ-ADR-022-006",
    "REQ-ADR-022-007",
    "REQ-ADR-022-008",
    "REQ-ADR-022-009",
    "REQ-ADR-022-010",
    "REQ-ADR-022-011",
    "REQ-ADR-022-012",
    "REQ-ADR-022-013",
    "REQ-ADR-022-014",
    "REQ-ADR-022-015",
    "REQ-ADR-022-016",
    "REQ-ADR-022-017",
    "REQ-ADR-022-018",
    "REQ-ADR-022-019",
    "REQ-ADR-022-020",
    "REQ-ADR-022-021",
    "REQ-ADR-022-022",
    "REQ-ADR-022-023",
    "REQ-ADR-022-024",
    "REQ-ADR-022-025",
    "REQ-ADR-022-026",
    "REQ-ADR-022-027",
    "REQ-ADR-022-028",
    "REQ-ADR-022-029",
    "REQ-ADR-022-030",
    "REQ-ADR-022-031",
    "REQ-ADR-022-032"
  ],
  "lock_ids": [
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-OFFLINE-001",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "related_adr_ids": [
    "ADR-014",
    "ADR-019",
    "ADR-020",
    "ADR-024"
  ],
  "supersedes_deprecated_refs": [
    "02-system/12-uckk-system-boundary.md",
    "04-components/subsystems/uckk.md"
  ],
  "depends_on": [
    "DOC-ADR-README",
    "DOC-ADR-019",
    "DOC-ADR-020",
    "DOC-ADR-024",
    "DOC-CONST-000",
    "DOC-SYS-007",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-LIFE-004",
    "DOC-LIFE-011",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-SEC-003",
    "DOC-SEC-005",
    "DOC-SEC-007",
    "DOC-SEC-011",
    "DOC-SEC-018",
    "DOC-OPS-004",
    "DOC-OPS-014",
    "DOC-CONF-008",
    "DOC-CONF-009",
    "DOC-CONF-010",
    "DOC-CONF-011",
    "DOC-CONF-019"
  ],
  "tags": [
    "architecture-decision",
    "uckk",
    "deterministic-pipeline",
    "native-media-processing",
    "media-identity",
    "media-versions",
    "provenance",
    "dimension-gateway",
    "publication-gateway",
    "local-first",
    "offline",
    "external-ai-boundary",
    "suno",
    "gamma",
    "controlled-export",
    "controlled-reimport"
  ]
}
KOA:DOC-META:END -->

# ADR-022 — Deterministic Native UCKK Pipeline

**ADR ID:** `ADR-022`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `system-architecture`  
**Owner decision:** `DEC-UCKK-001`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Related ADRs:** `ADR-014`, `ADR-019`, `ADR-020`, `ADR-024`

## 1. Decision Summary

UCKK Platform uses a native deterministic local pipeline for controlled media ingestion, verification, metadata capture, identity and version creation, original storage, thumbnail and preview generation, transcoding, deterministic extraction, local index inputs, export, backup, restore, and recovery.

Native UCKK does not perform AI classification, summarization, category generation, tagging, autonomous routing, transcription, translation, recommendation, embedding generation, or content generation.

User-selected categories, dimensions, visibility, destinations, and workflow choices remain explicit. Deterministic rules can validate or route declared states, but they do not infer semantic meaning from media content.

UCKK Dimension Gateway remains the controlled user-selected admission boundary. UCKK Platform becomes the owner of admitted media and its versions after accepted transfer. Publication Gateway remains the separate governed disclosure and publication boundary.

Suno and Gamma are optional user-triggered external adapters. External processing follows controlled export, provenance, controlled re-import, user or component acceptance, and optional separate publication. External providers never become hidden native stages and never write UCKK authoritative state directly.

## 2. Scope and Canonical References

### 2.1 Included scope

This decision covers:

- UCKK Platform native media processing;
- UCKK Dimension Gateway admission;
- media identity and versioning;
- originals and deterministic derivatives;
- metadata and provenance;
- collections and relationships;
- processing jobs and queues;
- Resource Governor integration;
- Governance Policy Runtime integration;
- Publication Gateway separation;
- external Suno and Gamma workflows;
- controlled export and re-import;
- offline operation;
- backup, restore, migration, rollback, recovery, and credible exit.

### 2.2 Excluded scope

This decision does not define:

- a universal media taxonomy;
- autonomous content classification;
- native AI or model execution;
- a mandatory external creative workflow;
- one desktop or shell implementation;
- a publication policy;
- rights or consent ownership;
- general-purpose workflow ownership;
- external provider business terms;
- a single physical storage topology;
- direct writes into another component's data domain.

### 2.3 Canonical owner decision

`DEC-UCKK-001` is the accepted owner decision.

Its scope is `component:uckk-platform` and its owner is `system-architecture`.

The decision establishes that native UCKK ingestion and processing remain local deterministic functions and that AI classification, summarization, tagging, autonomous routing, transcription, translation, and generation remain outside native UCKK.

### 2.4 Canonical objects

Primary canonical objects are:

```text
contracts/system.contract.json#/uckk
generated/component-catalog.json#/components/uckk-platform
contracts/components/uckk-platform.component.json
contracts/components/uckk-dimension-gateway.component.json
contracts/components/publication-gateway.component.json
generated/profile-catalog.json
contracts/integration-types.contract.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/test-catalog.json
generated/evidence-catalog.json
```

### 2.5 Authority relationship

The owner decision authorizes the component behavior.

This ADR records context, alternatives, rationale, consequences, and cross-system impact.

Component, profile, integration, release, artifact, requirement, lock, test, and evidence registries own the active executable facts.

### 2.6 Related decisions and ADRs

- `ADR-014` and `DEC-AI-001` define the strict external AI boundary.
- `ADR-019` and `DEC-GOV-001` preserve Resource Governor and Governance Policy Runtime separation.
- `ADR-020` and `DEC-GATE-001` separate Publication Gateway from UCKK Dimension Gateway.
- `ADR-024` and `DEC-DATA-001` preserve one owner per authoritative data domain.

## 3. Context and Decision Drivers

### 3.1 Inherited context

The inherited UCKK material established a local multimedia platform with stable media identity, explicit versions, provenance, user-defined categories, a controlled Dimension Gateway, deterministic thumbnails and previews, and no automatic AI interpretation.

The inherited material also named Suno and Gamma only as possible external tools and left detailed multimedia production channels undefined.

This decision retains the boundary while replacing unresolved workflow assumptions with explicit external-adapter contracts and lifecycle rules.

### 3.2 Problem

A media platform can easily drift into an opaque ingestion system that:

- assigns categories automatically;
- interprets content through a model;
- invokes remote providers in background jobs;
- overwrites originals with derivatives;
- merges admission and publication;
- loses version lineage;
- lets workers write unrelated stores;
- treats generated output as authoritative;
- fails offline;
- cannot export or restore independently.

Such a design would weaken user control, local operation, reproducibility, provenance, component ownership, privacy, and recovery.

### 3.3 Why an architecture decision is required

Implementation code alone cannot safely decide:

- whether AI is a native dependency;
- who owns admitted media;
- whether admission authorizes publication;
- whether external processing can be automatic;
- how external output returns;
- whether originals or derivatives are authoritative;
- how profiles include UCKK workers and gateways;
- how offline capability is preserved;
- how resource pressure affects processing;
- how versions, backup, restore, and exit behave.

These are authority and lifecycle decisions.

### 3.4 Decision drivers

Ranked drivers are:

1. stable media identity and explicit versions;
2. deterministic local processing;
3. user-selected classification and destinations;
4. no native AI dependency;
5. explicit gateway and ownership boundaries;
6. provenance for every source and derivative;
7. preservation of authoritative originals;
8. bounded resource use on lightweight hardware;
9. offline continuity;
10. optional removable external integrations;
11. controlled re-import and publication;
12. backup, restore, recovery, and credible exit.

### 3.5 Constraints

The decision preserves:

- no native AI baseline;
- external AI candidate-only behavior;
- one owner per authoritative data domain;
- no direct cross-component writes;
- separate admission and publication gateways;
- separate governance and resource authority;
- profile-scoped implementation;
- four release channels;
- atomic lifecycle activation;
- explicit offline envelopes;
- selective audit and receipts;
- portability and recovery.

## 4. Considered Options

### 4.1 Option A — Deterministic native local pipeline

**Description**

UCKK owns a local deterministic pipeline with explicit user choices, stable identities, versions, originals, derivatives, provenance, bounded workers, and optional external adapters outside the native path.

**Advantages**

- predictable operation;
- reproducible results;
- complete offline capability;
- clear ownership;
- strong provenance;
- controllable resources;
- independent backup and restore;
- removable external providers;
- no automatic disclosure;
- credible exit.

**Disadvantages and costs**

- explicit metadata and workflow design;
- derivative toolchain management;
- user review for semantic classification;
- integration contracts for external creative tools;
- controlled export and re-import steps;
- more visible states and receipts.

**Selection**

Selected.

### 4.2 Option B — Native AI media understanding

**Description**

Add local models for classification, summarization, tagging, routing, transcription, translation, embeddings, and recommendations.

**Advantages**

- automatic organization;
- richer search features;
- reduced manual metadata entry;
- possible local privacy benefits compared with remote providers.

**Disadvantages and costs**

- nondeterministic or model-dependent behavior;
- hardware and resource expansion;
- model lifecycle and supply-chain burden;
- taxonomy drift;
- difficult replay;
- implicit authority over user categories;
- weak minimum-hardware fit;
- tension with the no-native-AI baseline.

**Reason rejected**

The global and component decisions explicitly exclude native AI interpretation from UCKK.

### 4.3 Option C — Remote AI-first ingestion

**Description**

Send admitted media to remote services for classification, metadata, routing, transcription, or derivative generation as part of ingestion.

**Advantages**

- broad provider capabilities;
- rapid feature access;
- less local compute.

**Disadvantages and costs**

- automatic disclosure;
- provider dependency;
- network dependency;
- jurisdiction and account coupling;
- weak offline operation;
- difficult provenance and deletion guarantees;
- ingestion failure when providers are unavailable;
- provider output pressure on authoritative state.

**Reason rejected**

External services remain explicit optional workflows and cannot become native ingestion dependencies.

### 4.4 Option D — Merge UCKK Dimension Gateway into UCKK Platform

**Description**

Use one component for transfer admission and media ownership.

**Advantages**

- fewer components;
- fewer service calls;
- simpler local deployment.

**Disadvantages and costs**

- admission security and media ownership become conflated;
- profile-specific gateway policies become harder to isolate;
- transfer retry and media lifecycle responsibilities mix;
- audit and failure boundaries weaken.

**Reason rejected**

The gateway is a distinct controlled admission boundary.

### 4.5 Option E — Merge admission and publication

**Description**

Treat admission to a dimension as permission to disclose or publish.

**Advantages**

- simplified user workflow;
- fewer explicit transitions.

**Disadvantages and costs**

- private imports can become public;
- rights and consent checks are bypassed;
- publication receipts become ambiguous;
- withdrawal and destination state mix with admission state.

**Reason rejected**

Admission and publication have different authorities, targets, risks, and lifecycle.

## 5. Decision and Normative Requirements

### 5.1 Selected architecture

The selected architecture is:

```text
user or authorized component
        |
        | explicit source, dimension, category, visibility, intent
        v
UCKK Dimension Gateway
        |
        | verified, resumable, user-selected admission
        v
UCKK Platform
        |
        | stable media identity and version
        | authoritative original
        | deterministic metadata and derivatives
        | provenance and relationships
        | bounded processing jobs
        v
local use, controlled export, backup, restore, recovery

optional user-triggered external path:

UCKK controlled export
        -> declared external adapter
        -> provenance-bearing external result
        -> controlled re-import as candidate media or derivative
        -> user or component acceptance
        -> optional Publication Gateway transition
```

### 5.2 Normative effect

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-ADR-022-001,REQ-ADR-022-002,REQ-ADR-022-003,REQ-ADR-022-004,REQ-ADR-022-005,REQ-ADR-022-006,REQ-ADR-022-007,REQ-ADR-022-008,REQ-ADR-022-009,REQ-ADR-022-010,REQ-ADR-022-011,REQ-ADR-022-012,REQ-ADR-022-013,REQ-ADR-022-014,REQ-ADR-022-015,REQ-ADR-022-016,REQ-ADR-022-017,REQ-ADR-022-018,REQ-ADR-022-019,REQ-ADR-022-020,REQ-ADR-022-021,REQ-ADR-022-022,REQ-ADR-022-023,REQ-ADR-022-024,REQ-ADR-022-025,REQ-ADR-022-026,REQ-ADR-022-027,REQ-ADR-022-028,REQ-ADR-022-029,REQ-ADR-022-030,REQ-ADR-022-031,REQ-ADR-022-032 -->
- **REQ-ADR-022-001 — SHALL:** UCKK Platform provide a native deterministic local pipeline for controlled ingestion, verification, metadata capture, media identity, versioning, original storage, derivative production, deterministic extraction, indexing inputs, export, backup, restore, and recovery.
- **REQ-ADR-022-002 — SHALL:** UCKK Platform remain the canonical owner of admitted media identities, media versions, originals, deterministic derivatives, UCKK metadata, collections, relationships, processing jobs, provenance, export state, and restore state.
- **REQ-ADR-022-003 — SHALL:** UCKK Dimension Gateway remain a separate component that controls user-selected verified media admission and transfers accepted material to UCKK Platform without becoming the owner of the resulting media object.
- **REQ-ADR-022-004 — SHALL NOT:** UCKK Platform substitute for UCKK Dimension Gateway when the active profile composition requires the controlled admission boundary.
- **REQ-ADR-022-005 — SHALL:** Publication Gateway remain the separate authority for governed cross-domain disclosure, publication, withdrawal, and publication receipts, even when the source material entered through UCKK Dimension Gateway.
- **REQ-ADR-022-006 — SHALL NOT:** Admission into UCKK imply publication authorization, public visibility, external disclosure, consent, rights clearance, or transfer to an external provider.
- **REQ-ADR-022-007 — SHALL:** Native pipeline stages use explicit inputs, deterministic algorithms, declared tool versions, bounded resource envelopes, stable result classes, provenance, and reproducible validation.
- **REQ-ADR-022-008 — SHALL NOT:** Native UCKK perform AI classification, summarization, category generation, tagging, autonomous routing, transcription, translation, recommendation, embedding generation, or content generation.
- **REQ-ADR-022-009 — SHALL:** Media category, collection, dimension, visibility, routing destination, and publication intent originate from explicit user selection, accepted component state, or declared deterministic policy rather than inferred content meaning.
- **REQ-ADR-022-010 — SHALL:** Every admitted media object receive a stable UCKK identity and an explicit first version without silently overwriting or conflating an existing media identity.
- **REQ-ADR-022-011 — SHALL:** Every new source revision create an explicit version relationship, preserve provenance and restrictions, and identify whether it supersedes, derives from, or remains independent of prior versions.
- **REQ-ADR-022-012 — SHALL:** Original admitted representations remain distinct from thumbnails, previews, transcodes, extracted text, indexes, and other reproducible derivatives.
- **REQ-ADR-022-013 — SHALL NOT:** Failure, absence, staleness, or removal of a derivative invalidate or destroy an otherwise valid authoritative original.
- **REQ-ADR-022-014 — SHALL:** Deterministic extraction and derivative generation record producer, toolchain, source version, result identity, parameters, status, failure reason, and reproducibility evidence.
- **REQ-ADR-022-015 — SHALL:** Every native processing job be idempotent or explicitly non-repeatable, bounded by Resource Governor, owned by UCKK Platform, and associated with safe retry, cancellation, cleanup, and receipt behavior.
- **REQ-ADR-022-016 — SHALL NOT:** Resource Governor grant media authority, change UCKK metadata, select categories, approve publication, or write UCKK authoritative state.
- **REQ-ADR-022-017 — SHALL:** Governance Policy Runtime evaluate rights, consent, disclosure, exception, or governed processing decisions where the active profile requires it without becoming the owner of media state or processing capacity.
- **REQ-ADR-022-018 — SHALL NOT:** UCKK Platform, gateways, workers, migration tools, or external adapters write directly to another component's authoritative data store.
- **REQ-ADR-022-019 — SHALL:** Native UCKK remain functional for its declared local capability envelope without ChatGPT, Suno, Gamma, external voice, remote classification, remote transcription, remote translation, or another AI provider.
- **REQ-ADR-022-020 — SHALL:** Suno and Gamma remain optional removable external adapters invoked only by an explicit user action or an explicitly accepted user workflow step.
- **REQ-ADR-022-021 — SHALL NOT:** Ingestion, verification, derivative generation, indexing, queue processing, recovery, or background scheduling automatically invoke Suno, Gamma, ChatGPT, or another external AI service.
- **REQ-ADR-022-022 — SHALL:** External processing use controlled export, declared data scope, destination and provider identity, user approval, provenance, external result identity, controlled re-import, and optional separate publication.
- **REQ-ADR-022-023 — SHALL NOT:** External provider output directly mutate UCKK authoritative state, replace an original, create a current version, assign a category, publish content, grant rights, or become authoritative without component-owned validation and acceptance.
- **REQ-ADR-022-024 — SHALL:** Controlled re-import represent external output as a new candidate source, derivative, or related media object with explicit provenance, restrictions, validation, and user or component acceptance.
- **REQ-ADR-022-025 — SHALL:** Profiles declare whether UCKK Platform, UCKK Dimension Gateway, Publication Gateway, native workers, external adapters, offline operation, and physical isolation are required, permitted, conditional, or excluded.
- **REQ-ADR-022-026 — SHALL:** Offline profiles retain the local runtime, media state, metadata, provenance, worker tools, queues, receipts, export, backup, restore, recovery, and validation inputs required for their declared UCKK capability envelope.
- **REQ-ADR-022-027 — SHALL NOT:** Offline operation weaken media identity, integrity, rights, provenance, ownership, gateway, publication, receipt, resource, or recovery validation or silently substitute a remote provider.
- **REQ-ADR-022-028 — SHALL:** UCKK service, schema, worker, migration, and artifact changes activate only through validated services and knowledge artifacts in a compatible complete Release Set.
- **REQ-ADR-022-029 — SHALL:** Backup, restore, migration, rollback, and forward repair preserve UCKK media identities, versions, originals, provenance, restrictions, ownership, derivative relationships, external-processing lineage, and active Release Set compatibility.
- **REQ-ADR-022-030 — SHALL:** UCKK exports support credible exit through documented media, metadata, provenance, rights, relationships, version, and restore representations without requiring an external AI provider.
- **REQ-ADR-022-031 — SHALL:** UCKK conformance include ownership, admission, deterministic replay, versioning, original-versus-derivative, no-native-AI, external-adapter, gateway separation, offline, resource, export, backup, restore, migration, and failure-containment tests.
- **REQ-ADR-022-032 — SHALL:** This decision be considered implemented only when the component contracts, profile declarations, integration contracts, resource envelopes, lifecycle artifacts, receipts, tests, evidence, migration records, and related gateway and AI-boundary ADRs all validate.
<!-- GENERATED:REQUIREMENTS:END -->

### 5.3 Default classification rule

UCKK does not impose a universal taxonomy.

Category, collection, dimension, visibility, and routing intent are supplied explicitly or derived from deterministic declared state.

An unclassified or inbox state can preserve media until the user or owning workflow assigns further organization.

### 5.4 Default original rule

The admitted source representation is the authoritative original for that version.

Thumbnails, previews, transcodes, extracted text, indexes, and provider outputs remain derivatives or related media until explicitly accepted under the component contract.

### 5.5 Default external-processing rule

External processing is optional, explicit, provenance-aware, and removable.

It is not part of native ingestion, verification, identity creation, version creation, or background routing.

## 6. Ownership and Deterministic Pipeline Model

### 6.1 UCKK-owned domains

UCKK Platform owns:

| Domain | Owned state |
| --- | --- |
| Dimensions | Logical UCKK scope, membership, state, and local organization |
| Media objects | Stable identity, class, current version, lifecycle, and local visibility |
| Media versions | Version identity, source relation, provenance, restrictions, and status |
| Originals | Authoritative admitted representation and storage reference |
| Derivatives | Thumbnail, preview, transcode, deterministic extraction, and related result state |
| Metadata | User-supplied and deterministic technical metadata with provenance |
| Collections | User-defined grouping without original duplication |
| Relationships | Source, derived-from, excerpt, translation-reference, evidence, and membership relations |
| Processing jobs | Intent, state, owner, resources, result, retry, cancellation, and cleanup |
| Export state | Scope, versions, restrictions, dependencies, destination class, and result |
| Restore state | Staging, validation, migration, activation, rollback, and recovery state |

Identity and Trust owns identities and delegation.

Governance Policy Runtime owns policy decisions where deployed.

Resource Governor owns resource admission.

Publication Gateway owns governed cross-domain publication.

### 6.2 Admission pipeline

The admission pipeline is:

1. identify actor and target dimension;
2. collect explicit user or component intent;
3. validate source accessibility and declared size limits;
4. queue and resume transfer through UCKK Dimension Gateway;
5. verify transfer integrity and source metadata;
6. submit an admission request to UCKK Platform;
7. create or resolve the media identity according to explicit intent;
8. create the first or next media version;
9. commit the authoritative original;
10. record provenance and restrictions;
11. schedule bounded deterministic derivatives;
12. expose completion and receipt state.

Admission success does not imply derivative success or publication.

### 6.3 Media identity

A media identity is independent of:

- filesystem path;
- object-store location;
- user-interface route;
- category;
- collection;
- derivative availability;
- publication destination;
- external provider;
- another component's workflow state.

Replacing a file at the same path does not silently replace the UCKK identity.

### 6.4 Version model

Each source revision records:

- media identity;
- version identity;
- source relationship;
- admission source;
- producer and contract version;
- technical representation;
- provenance;
- rights and restrictions;
- creation time;
- current or superseded status;
- derivative relationships;
- validation result.

The current version is explicit.

Older versions follow retention and rights rules rather than silent overwrite.

### 6.5 Deterministic derivatives

Native derivative classes include:

- thumbnail;
- preview;
- format-compatible transcode;
- deterministic text extraction;
- technical metadata extraction;
- local index input;
- accessibility-oriented deterministic representation when declared.

Each derivative records its exact source version and producer toolchain.

### 6.6 Processing jobs

Processing jobs use explicit states such as:

```text
queued
admitted
running
paused
completed
failed
cancelled
superseded
```

A job has one owner, one source version, one declared result class, one resource class, and bounded retry behavior.

Workers do not remain resident without a profile-declared reason.

### 6.7 Failure isolation

A failed derivative preserves the original and other valid derivatives.

A failed external adapter preserves local state.

A failed index update does not become media loss.

A failed publication does not reverse admission.

### 6.8 Cross-component writes

Gateways, workers, integrations, migration tools, and operators use UCKK public contracts.

They do not directly modify UCKK tables or files that represent authoritative state.

UCKK likewise does not directly write identity, workflow, publication, governance, or integration stores.

## 7. Profiles, Security, AI, Offline, and Resources

### 7.1 Profile effects

| Profile or overlay | UCKK effect | Native pipeline | External adapters |
| --- | --- | --- | --- |
| `user_lightweight` | Local personal media, bounded workers, one heavy job, zero idle workers | required when UCKK is included | optional and user-triggered |
| `developer_linux_workstation` | Full development, tests, adapters, and local runtime | permitted | optional |
| `developer_windows_wsl` | Development and tests inside the WSL workspace boundary | permitted | optional |
| `sovereign_linux_node` | Local authoritative media with strong offline, recovery, and isolation | required when UCKK is included | removable and nonessential |
| `sovereign_hub` | Organizational dimensions and higher concurrency | profile-declared | removable and nonessential |
| `build_farm` | Builds and tests UCKK artifacts and deterministic tools | build and validation only | test stubs or approved adapters |
| `control_plane` | No default media authority unless explicitly composed | conditional | excluded by default |
| `high_assurance` | Stronger separation, provenance, review, and evidence | required when UCKK is included | tightly scoped |
| `sovereign_offline` | Complete local processing, export, backup, restore, and recovery | required | unavailable without capability loss to native pipeline |
| `appliance_shell` | Shell exposes selected UCKK interactions | profile-composed | optional |

### 7.2 Security effects

Security controls include:

- authenticated actors and services;
- target-dimension authorization;
- bounded admission and parser behavior;
- safe media-type handling;
- no source execution during admission;
- original and derivative separation;
- rights and visibility propagation;
- controlled temporary storage;
- worker isolation;
- service identities;
- no unrestricted provider credentials;
- minimized logs and receipts;
- protected backup and restore;
- migration validation;
- incident and recovery paths.

### 7.3 Privacy, rights, and consent

UCKK records rights and restrictions associated with media state but does not become the owner of external rights or consent truth.

Governed disclosure and external processing use current policy and owner facts where required.

Preview, search, export, external transfer, and publication preserve applicable restrictions.

### 7.4 AI boundary

Native UCKK contains no generative model, classifier, summarizer, embedding model, autonomous routing model, transcription model, translation model, recommendation model, or content-generation model.

Optional external tools remain outside the native pipeline.

External output is candidate material until UCKK validates and accepts it through its own contract.

### 7.5 Suno and Gamma

Suno and Gamma are optional external adapters for explicit user workflows.

Their contracts identify:

- provider and account;
- input media and metadata scope;
- purpose;
- destination;
- user action;
- credentials;
- transfer status;
- provider result identity;
- provenance;
- controlled re-import;
- deletion or retention expectations;
- optional publication transition.

Removing either adapter leaves native UCKK operational.

### 7.6 Offline operation

Offline UCKK retains:

- media identities and versions;
- originals and local derivatives;
- metadata and provenance;
- categories and collections;
- local processing tools;
- job queues;
- receipts;
- export;
- backup;
- restore;
- recovery.

Remote-dependent adapter jobs remain deferred or unavailable without changing native authority.

### 7.7 Resource effects

Resource Governor controls:

- worker admission;
- heavy-job concurrency;
- CPU and memory ceilings;
- temporary storage;
- I/O weight;
- queue bounds;
- pause and resumption;
- pressure behavior.

The `user_lightweight` baseline allows one heavy job and no idle task workers.

Under pressure, UCKK preserves originals and active authoritative state before reproducible derivatives and background index work.

### 7.8 Observability and receipts

Operational interfaces expose:

- admitted media and version counts;
- original storage state;
- derivative job state;
- queue age and saturation;
- external adapter status;
- export and re-import status;
- backup and restore readiness;
- resource pressure;
- failure reason codes;
- active services release;
- receipt-buffer health.

Metrics omit unrestricted content and secret material.

## 8. Lifecycle, External Processing, Migration, and Recovery

### 8.1 Release-channel effects

| Release channel | UCKK effect |
| --- | --- |
| `system` | Operating environment, storage, isolation, codecs, and protected execution support |
| `services` | UCKK Platform, gateways, workers, service interfaces, and migrations |
| `governance` | Rights, disclosure, external-transfer, exception, and publication policy where applicable |
| `knowledge` | Compatible deterministic language, metadata, schema, or knowledge artifacts used through declared contracts |

The complete Release Set establishes compatibility.

### 8.2 Service and worker lifecycle

UCKK service changes use registered signed artifacts.

Worker tools and codecs are versioned and validated.

A copied executable, local script, ad hoc container, or manually replaced tool does not become active product state.

### 8.3 Schema and data migration

UCKK owns its migrations for:

- media identities;
- versions;
- provenance;
- derivatives;
- collections;
- relationships;
- jobs;
- exports;
- restore state.

Migration preserves stable identity and explicit version lineage.

A coordinator does not write UCKK state directly.

### 8.4 Controlled export

Controlled export identifies:

- media and versions;
- original or derivative selection;
- metadata;
- provenance;
- rights and restrictions;
- relationships;
- destination class;
- recipient or provider;
- purpose;
- expiry and retention where applicable;
- receipt.

Export does not imply publication.

### 8.5 External result and controlled re-import

An external result is represented by:

- provider identity;
- provider result identity;
- source export identity;
- input media versions;
- transformation purpose;
- returned representation;
- provider metadata;
- restrictions;
- received time;
- validation result.

Controlled re-import creates a candidate source, derivative, or related media object.

Acceptance chooses the exact relationship and never silently replaces the original.

### 8.6 Backup and restore

Backup includes UCKK-owned authoritative state and the representations needed for declared recovery.

Restore validates:

- target and profile;
- source Release Set;
- schemas;
- media identities and versions;
- original availability;
- provenance;
- rights and restrictions;
- derivative relationships;
- external-processing lineage;
- storage mappings;
- receipts;
- recovery readiness.

A backup result alone does not prove restore.

### 8.7 Rollback and forward repair

Rollback validates current data and artifact compatibility.

Forward repair is used when an older service or schema cannot safely represent newer media, rights, provenance, migration, or external-processing state.

The rollback unit includes services, schemas, migrations, worker toolchains, profile composition, storage contracts, and complete Release Set identity.

### 8.8 Recovery and credible exit

Recovery preserves originals, identity, versions, provenance, restrictions, and evidence before reproducible derivatives.

Credible exit exports documented open representations for media, metadata, versions, provenance, relationships, restrictions, and restore instructions.

No external AI provider is required to restore or interpret the authoritative UCKK package.

### 8.9 Migration from inherited sources

Retained inherited meaning includes:

- personal logical dimensions;
- user-defined categories;
- an unclassified holding state;
- controlled Dimension Gateway admission;
- stable media identity and explicit versions;
- authoritative originals;
- deterministic thumbnails and previews;
- provenance;
- publication not implied by admission;
- no automatic AI interpretation.

Added explicit meaning includes:

- component ownership;
- Resource Governor integration;
- separate Publication Gateway;
- external adapter contracts;
- controlled re-import;
- profile scope;
- Release Set lifecycle;
- offline, recovery, portability, tests, and evidence.

The non-authoritative sources become historical evidence after migration cutover.

## 9. Interfile Impact and Validation

### 9.1 Canonical impact

The decision affects or constrains:

```text
generated/decision-index.json
generated/decision-index.json
contracts/system.contract.json
generated/component-catalog.json
contracts/components/uckk-platform.component.json
contracts/components/uckk-dimension-gateway.component.json
contracts/components/publication-gateway.component.json
contracts/components/resource-governor.component.json
contracts/components/governance-policy-runtime.component.json
generated/profile-catalog.json
contracts/integration-types.contract.json
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
```

### 9.2 Documentation impact

Affected document families include:

- system AI and offline boundaries;
- UCKK platform and gateways;
- component ownership;
- cross-component communication;
- profiles and resource envelopes;
- external integrations;
- lifecycle and Release Sets;
- security, privacy, secrets, and offline import;
- backup, restore, maintenance, and recovery;
- conformance, locks, ownership, migration, and release gates;
- ADR and generated indexes.

### 9.3 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-UCKK-ADR-001` | Admit media through UCKK Dimension Gateway | `pass` |
| `TEST-UCKK-ADR-002` | Create stable media identity and first version | `pass` |
| `TEST-UCKK-ADR-003` | Preserve original and generate deterministic derivatives | `pass` |
| `TEST-UCKK-ADR-004` | Replay derivative generation reproducibly | `pass` |
| `TEST-UCKK-ADR-005` | Prove no native AI classification, tagging, routing, transcription, translation, or generation | `pass` |
| `TEST-UCKK-ADR-006` | Prove admission does not authorize publication | `pass` |
| `TEST-UCKK-ADR-007` | Prove Dimension Gateway and Publication Gateway separation | `pass` |
| `TEST-UCKK-ADR-008` | Prove no direct cross-component writes | `pass` |
| `TEST-UCKK-ADR-009` | Enforce Resource Governor worker and queue limits | `pass` |
| `TEST-UCKK-ADR-010` | Continue native operation without external providers | `pass` |
| `TEST-UCKK-ADR-011` | Run user-triggered Suno and Gamma export workflows | `pass` |
| `TEST-UCKK-ADR-012` | Re-import provider output as candidate state with provenance | `pass` |
| `TEST-UCKK-ADR-013` | Preserve identities, versions, provenance, and restrictions through backup and restore | `pass` |
| `TEST-UCKK-ADR-014` | Validate services, schemas, migrations, and complete Release Set lifecycle | `pass` |
| `TEST-UCKK-ADR-015` | Export a provider-independent credible-exit package | `pass` |
| `TEST-UCKK-ADR-016` | Validate migration from inherited UCKK sources | `pass` |

### 9.4 Required evidence

| Evidence ID | Evidence |
| --- | --- |
| `EVID-UCKK-ADR-001` | Component and gateway contract validation |
| `EVID-UCKK-ADR-002` | Deterministic pipeline and replay results |
| `EVID-UCKK-ADR-003` | Media identity, version, original, and derivative validation |
| `EVID-UCKK-ADR-004` | No-native-AI and external-adapter boundary validation |
| `EVID-UCKK-ADR-005` | Offline, resource, and failure-containment validation |
| `EVID-UCKK-ADR-006` | Export, re-import, publication separation, and provenance validation |
| `EVID-UCKK-ADR-007` | Backup, restore, migration, recovery, and credible-exit validation |
| `EVID-UCKK-ADR-008` | Decision closure, lock alignment, and inherited-source migration validation |

### 9.5 Acceptance criteria

Acceptance is satisfied when:

1. `DEC-UCKK-001` is accepted;
2. UCKK Platform has one canonical component identity and owner;
3. UCKK Dimension Gateway remains a separate admission boundary;
4. Publication Gateway remains a separate publication boundary;
5. native pipeline stages are deterministic and locally executable;
6. no native AI processing or automatic external invocation exists;
7. external adapters are explicit, user-triggered, removable, and provenance-aware;
8. provider output returns only through controlled re-import;
9. originals and derivatives remain distinct;
10. media identity and version lineage pass tests;
11. Resource Governor and Governance Policy Runtime boundaries pass;
12. offline, backup, restore, recovery, and credible-exit tests pass;
13. all affected objects have final impact dispositions;
14. no required validation result is failed or blocked.

## 10. Consequences, Rejected Alternatives, and Decision Record

### 10.1 Positive consequences

- UCKK remains predictable and locally operable;
- users retain explicit control over categories and destinations;
- media identities and versions remain stable;
- originals remain protected from derivative failure;
- provenance covers native and external processing;
- external tools remain removable;
- admission and publication remain distinct;
- lightweight profiles can bound workers tightly;
- sovereign-offline profiles retain complete native operation;
- backup, restore, recovery, and exit do not depend on AI providers.

### 10.2 Negative consequences and costs

- less automatic semantic organization;
- more explicit user metadata and review;
- deterministic toolchains and codecs require lifecycle management;
- controlled export and re-import add visible workflow steps;
- provider integrations require contracts, credentials, provenance, and receipts;
- derivative regression testing is required;
- storage for originals and versions requires retention planning;
- profile-specific worker and queue tuning is required.

### 10.3 Operational obligations

Operations maintains:

- gateway health;
- UCKK service health;
- worker and queue state;
- original storage capacity;
- derivative cleanup under owner rules;
- external-adapter status;
- backup and restore readiness;
- offline operation;
- recovery procedures;
- receipt and evidence buffering.

### 10.4 Rejected alternatives

| Alternative | Decisive reason | Reconsideration trigger |
| --- | --- | --- |
| Native AI interpretation | Conflicts with deterministic local and no-native-AI decisions | A future accepted decision replaces the baseline and proves equivalent authority, offline, replay, resource, privacy, and recovery behavior |
| Remote AI-first ingestion | Creates hidden disclosure and provider dependency | No active profile requires local or offline UCKK and explicit user control is replaced by accepted authority |
| Merge Dimension Gateway into UCKK | Conflates admission security and media ownership | The admission boundary is removed by an accepted component decision with equivalent isolation |
| Merge publication with admission | Conflates local admission and external disclosure | Publication ceases to be a distinct governed transition |
| Overwrite originals with provider output | Breaks provenance, user control, and recovery | An accepted data-model decision replaces explicit versions and lineage |

### 10.5 Exceptions

No active exception changes this ADR.

A bounded integration exception cannot make an external provider native, automatic, authoritative, or required for local UCKK operation.

### 10.6 Decision record

```json
{
  "adr_id": "ADR-022",
  "status": "accepted",
  "decision_class": "major",
  "decision_ids": [
    "DEC-UCKK-001"
  ],
  "decision_owner": "system-architecture",
  "selected_option": "deterministic_native_local_uckk_pipeline",
  "related_adr_ids": [
    "ADR-014",
    "ADR-019",
    "ADR-020",
    "ADR-024"
  ],
  "legacy_sources": [
    "02-system/12-uckk-system-boundary.md",
    "04-components/subsystems/uckk.md"
  ],
  "compatibility_class": "profile_scoped_compatible",
  "affected_release_channels": [
    "services",
    "knowledge"
  ],
  "validation_status": "pass"
}
```

### 10.7 Historical integrity

When superseded:

1. this identifier remains reserved;
2. the file remains readable;
3. the ADR registry records the replacement;
4. reciprocal succession links identify the new ADR;
5. owner decisions and canonical contracts receive explicit replacement;
6. requirements, locks, profiles, integrations, tests, evidence, migration, and generated indexes update;
7. no active component or profile continues to treat this ADR as current without the replacement relationship.

## 11. Non-Normative Examples

### Example 1 — Explicit category selection

A user sends an image to a personal UCKK dimension and selects `Unclassified`.

UCKK creates the media identity and first version, stores the original, records provenance, and schedules a thumbnail. It does not classify the image or create a category from its content.

### Example 2 — Deterministic preview

A document preview is generated with a declared renderer version and parameters.

Repeating the job against the same source version and toolchain produces the same declared result class. If the preview fails, the original remains valid and available according to policy.

### Example 3 — Publication separation

A video is admitted through UCKK Dimension Gateway and becomes ready locally.

It remains private. A later external publication request passes independently through Publication Gateway with current rights, consent, destination, and receipt checks.

### Example 4 — User-triggered Suno workflow

A user selects an audio source and explicitly starts an approved Suno workflow.

UCKK creates a controlled export with the selected source version and metadata. The returned result has provider provenance and re-enters as a candidate related media object. It does not overwrite the source.

### Example 5 — Gamma result

A user exports selected text and images to Gamma for a presentation candidate.

The returned presentation is validated and re-imported as a new candidate media object with relationships to its source materials. Publication remains a separate decision.

### Example 6 — Offline sovereign node

A sovereign-offline node loses all network access.

UCKK continues local admission, identity and version creation, original storage, thumbnails, previews, deterministic extraction, collections, export, backup, restore, and recovery. External adapter jobs remain unavailable without affecting native state.

### Example 7 — Resource pressure

A restore-validation job already occupies the single heavy-job slot on a lightweight endpoint.

A new transcode job is deferred by Resource Governor. Existing originals and completed derivatives remain available, and UCKK does not invoke remote compute as a substitute.

### Example 8 — Credible exit

A user exports a UCKK dimension for independent restoration.

The package includes selected originals, versions, metadata, provenance, relationships, restrictions, and restore instructions. It requires no Suno, Gamma, ChatGPT, or native AI service to interpret the authoritative package.
