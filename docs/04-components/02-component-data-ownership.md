<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/data_authority",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-SEC-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-PORT-001",
    "DEC-LIFE-001",
    "DEC-OFFLINE-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001",
    "DEC-PROFILE-001",
    "DEC-KRISTAL-001"
  ],
  "requirement_ids": [
    "REQ-COMP-DATA-001",
    "REQ-COMP-DATA-002",
    "REQ-COMP-DATA-003",
    "REQ-COMP-DATA-004",
    "REQ-COMP-DATA-005",
    "REQ-COMP-DATA-006",
    "REQ-COMP-DATA-007",
    "REQ-COMP-DATA-008",
    "REQ-COMP-DATA-009",
    "REQ-COMP-DATA-010",
    "REQ-COMP-DATA-011",
    "REQ-COMP-DATA-012",
    "REQ-COMP-DATA-013",
    "REQ-COMP-DATA-014",
    "REQ-COMP-DATA-015",
    "REQ-COMP-DATA-016",
    "REQ-COMP-DATA-017",
    "REQ-COMP-DATA-018",
    "REQ-COMP-DATA-019",
    "REQ-COMP-DATA-020",
    "REQ-COMP-DATA-021",
    "REQ-COMP-DATA-022",
    "REQ-COMP-DATA-023",
    "REQ-COMP-DATA-024"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DATA-002",
    "LOCK-DATA-003",
    "LOCK-DATA-004",
    "LOCK-DATA-005",
    "LOCK-DATA-006",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-020",
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "components",
    "data-ownership",
    "authoritative-data",
    "logical-ownership",
    "physical-isolation",
    "cross-component-references",
    "read-models",
    "events",
    "artifacts",
    "migration",
    "restore",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Component Data Ownership

## 1. Purpose

This document defines the global kOA rules for authoritative data ownership across components.

Its purpose is to ensure that every authoritative state has one accountable owner, every mutation passes through that owner's contract, and physical deployment choices never create accidental shared authority.

The ownership model supports:

- clear responsibility for schemas and state transitions;
- deterministic mutation and conflict handling;
- strict cross-component write boundaries;
- controlled references, events, artifacts, and read models;
- profile-dependent physical isolation without semantic drift;
- safe export, backup, restore, migration, and ownership transfer;
- selective evidence and recourse;
- local-first and offline operation.

Canonical component identities, domains, interfaces, profile membership, requirements, locks, tests, and evidence remain owned by the referenced registries and component contracts.

## 2. Scope

This document applies globally to:

- authoritative component databases and schemas;
- component-owned files and object-store paths;
- private queues and durable job state;
- component-owned event logs;
- identity, trust, policy, workflow, knowledge, media, publication, node, and audit state;
- controlled copies and projections;
- immutable artifacts;
- cross-component references;
- exports, backups, restores, migrations, synchronization, and cutover;
- single-process, single-host, containerized, physically separated, and offline deployments.

It governs logical ownership independently of physical topology.

It applies to all primary profiles and overlays. A profile may strengthen physical isolation, service identity, encryption, recovery, or evidence requirements. A profile does not alter the owner of a data domain unless an accepted decision and canonical contract change explicitly do so.

This document does not prescribe one database engine, one storage system, one process model, one queue, one container runtime, or one deployment topology.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/authority-manifest.json` | Active authority release and canonical ownership activation |
| `generated/decision-index.json` | Accepted component, data, gateway, governance, lifecycle, security, portability, and evidence decisions |
| `contracts/system.contract.json#/data_authority` | Global data-authority model |
| `generated/component-catalog.json` | Component identities and authoritative domain ownership |
| `generated/component-catalog.json` | Active component-contract inventory |
| `contracts/components/*.component.json` | Owned domains, interfaces, references, state transitions, export, restore, and evidence behavior |
| `generated/profile-catalog.json` | Profile composition and physical-isolation conditions |
| `contracts/artifact-classes.contract.json` | Artifact ownership, compatibility, activation, and retention |
| `contracts/integration-types.contract.json` | External integration data-transfer scope and removability |
| `generated/requirements-index.json` | Normative ownership requirements |
| `generated/assertion-index.json` | Ownership, boundary, profile, lifecycle, security, and implementation assertions |
| `generated/traceability.json` | Ownership relationships among decisions, requirements, tests, evidence, components, profiles, and documents |
| `generated/exception-index.json` | Bounded deviations and compensating controls |
| `generated/test-catalog.json` | Ownership uniqueness, isolation, migration, restore, and boundary tests |
| `generated/evidence-catalog.json` | Ownership and transition evidence |

The related system communication model is:

```text
02-system/07-cross-component-communication.md
```

Component-specific data ownership remains canonical in each component contract.

## 4. Model and Responsibilities

### 4.1 Authoritative data domain

An authoritative data domain is a coherent set of records, objects, files, events, state transitions, and rules for which one component is accountable.

The owning component controls:

- stable object identity;
- canonical schema;
- accepted mutations;
- transaction and concurrency rules;
- state-transition validation;
- correction, supersession, withdrawal, revocation, and deletion;
- retention;
- component-owned export;
- component-owned restore and migration;
- emitted domain events;
- evidence for critical transitions.

A domain can contain references to externally owned objects without owning those objects.

### 4.2 Ownership classes

| Class | Meaning | Authority |
| --- | --- | --- |
| Authoritative state | Canonical current and historical state of an owned domain | Owning component |
| External-owner reference | Stable identity and declared relationship to another owner's object | Referenced component |
| Derived projection | Reconstructible view optimized for a consumer | Source owners remain authoritative |
| Cache | Temporary reproducible data used for performance | No independent authority |
| Replica | Copied representation used for availability or locality | Source owner remains authoritative |
| Search or analytics index | Derived query structure | Source owners remain authoritative |
| Immutable artifact | Versioned producer-owned representation | Producer plus receiving activation authority |
| Event | Record of a committed publisher-owned fact | Publishing component |
| Evidence reference | Link from workflow or state to registered evidence | Evidence owner remains authoritative |
| Export package | Portable representation of owned state | Source component until validated restoration |
| Restored staged state | Reconstructed but not yet activated state | No active authority until validation and cutover |

### 4.3 Logical and physical ownership

Logical ownership defines authority.

Physical topology determines isolation and operations.

Permitted physical forms include:

- separate database processes;
- separate logical databases in one process;
- separate schemas in one database;
- component-local SQLite or equivalent stores;
- separate object-store namespaces;
- separate service-owned filesystem roots;
- immutable artifacts;
- profile-declared local queues or event transports.

When components share a physical system, the deployment preserves:

- separate service identities;
- separate write grants;
- separate migration ownership;
- separate logical namespaces;
- separate backup inventory;
- separate restore ordering;
- observable contract boundaries.

Physical consolidation is an optimization, not an ownership change.

### 4.4 Mutation authority

A component changes only the state it owns.

A caller sends a versioned command, artifact, gateway request, or restore request to the owner. The owner validates the actor, target, scope, authority, policy, consent, expected version, payload, and compatibility before commit.

A transport, API gateway, queue, workflow engine, shared library, coordinator, or database trigger cannot substitute for owner validation.

### 4.5 References and copied data

A cross-component reference contains enough information to resolve:

- owning component;
- object class;
- stable object identity;
- reference version or observation context when required;
- relationship type;
- applicable scope or disclosure class.

A copied subset used for display, search, analytics, synchronization, or offline operation declares its source and freshness. It does not become a second source of truth.

When a referenced object is withdrawn, revoked, deleted, superseded, or reclassified, the source owner emits or exposes the declared change. Consumers update their own state without rewriting the source domain.

### 4.6 Events and read models

A domain event is emitted after the publishing owner commits its state.

A consumer validates the event and may change only its own state.

A controlled read model identifies:

- source owners;
- derivation path;
- freshness semantics;
- authorization;
- rebuild procedure;
- retention;
- correction and revocation handling;
- non-authoritative status.

A read model never becomes a shared write surface.

### 4.7 Gateways and special boundaries

Publication Gateway controls governed disclosure and publication across authority domains.

UCKK Publication Bridge owns target-specific packaging, transport, retry, and destination receipt state for an authorized UCKK publication.

Governance Policy Runtime owns applicable policy decisions.

Resource Governor owns resource admission and scheduling.

Audit Broker owns cross-component evidence routing and selective evidence disclosure.

These components can route, decide, schedule, or record without acquiring the participant component's authoritative data ownership.

### 4.8 Multi-component workflows

A workflow coordinator may own:

- workflow identity;
- sequencing;
- participant references;
- partial-completion state;
- compensation or forward-repair instructions;
- workflow-local evidence references.

Each participant retains ownership of its own committed state.

The workflow is not represented as globally atomic unless an active contract defines and validates an atomic protocol.

### 4.9 Synchronization and offline copies

Offline operation can require local copies, queues, and explicit synchronization sessions.

The synchronization contract records:

- peer identity;
- source owner;
- object and event identities;
- version context;
- synchronization scope;
- deterministic merge rules;
- review-required conflict classes;
- partial progress;
- completion and evidence.

Authority-sensitive conflicts are never resolved from arrival order or local clock preference alone.

### 4.10 Privacy, retention, and audit

The source owner defines classification, retention, deletion, export, disclosure, and consent behavior for its domain.

Consumers preserve those restrictions for copied or referenced data.

Audit and evidence paths record accountability with minimized payloads. Recording an event does not grant the audit path unrestricted use of the source data.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-DATA-001,REQ-COMP-DATA-002,REQ-COMP-DATA-003,REQ-COMP-DATA-004,REQ-COMP-DATA-005,REQ-COMP-DATA-006,REQ-COMP-DATA-007,REQ-COMP-DATA-008,REQ-COMP-DATA-009,REQ-COMP-DATA-010,REQ-COMP-DATA-011,REQ-COMP-DATA-012,REQ-COMP-DATA-013,REQ-COMP-DATA-014,REQ-COMP-DATA-015,REQ-COMP-DATA-016,REQ-COMP-DATA-017,REQ-COMP-DATA-018,REQ-COMP-DATA-019,REQ-COMP-DATA-020,REQ-COMP-DATA-021,REQ-COMP-DATA-022,REQ-COMP-DATA-023,REQ-COMP-DATA-024 -->
- **REQ-COMP-DATA-001 — SHALL:** Every authoritative data domain have exactly one active owning component identified in the components registry and the owning component contract.
- **REQ-COMP-DATA-002 — SHALL:** The owning component define the domain's identity, schema, state transitions, mutation rules, retention, correction, export, restore, and evidence behavior.
- **REQ-COMP-DATA-003 — SHALL NOT:** A component write directly to another component's authoritative tables, files, private queues, mutable object-store paths, internal caches, or undocumented runtime state.
- **REQ-COMP-DATA-004 — SHALL:** A cross-component mutation be requested through a versioned interface owned by the component that owns the affected authoritative data.
- **REQ-COMP-DATA-005 — SHALL:** A component independently validate identity, authority, policy, consent, target scope, expected version, payload, and compatibility before changing its owned state.
- **REQ-COMP-DATA-006 — SHALL:** A reference to an object owned by another component preserve the external owner's object identity and not create a second authoritative copy.
- **REQ-COMP-DATA-007 — SHALL:** A copied projection, replica, search index, analytics table, cache, user-interface model, or read model declare its source owners, derivation, freshness, rebuild procedure, authorization boundary, and non-authoritative status.
- **REQ-COMP-DATA-008 — SHALL NOT:** Physical co-location in one process, host, database server, schema engine, queue, object store, filesystem, or container grant shared ownership or cross-owner write authority.
- **REQ-COMP-DATA-009 — SHALL:** A profile that physically consolidates component storage preserve separate service identities, logical namespaces, migration ownership, access controls, backup inventory, and write privileges.
- **REQ-COMP-DATA-010 — SHALL:** A domain event describe an already committed fact owned by its publisher and not transfer ownership of the published domain to a consumer.
- **REQ-COMP-DATA-011 — SHALL:** An immutable artifact crossing a component boundary retain its producer, artifact class, version, scope, compatibility, policy, and activation authority.
- **REQ-COMP-DATA-012 — SHALL:** Publication to external UCKK require Publication Gateway authorization followed by UCKK Publication Bridge packaging and transport.
- **REQ-COMP-DATA-013 — SHALL NOT:** A workflow coordinator, gateway, broker, transport, shared database, integration adapter, AI service, or audit system become the owner of participant component data merely because it routes, processes, records, or coordinates it.
- **REQ-COMP-DATA-014 — SHALL:** Corrections, supersession, withdrawal, revocation, deletion, and retention changes be executed by the owning component and propagated through declared references, events, artifacts, or gateway contracts.
- **REQ-COMP-DATA-015 — SHALL:** Authority-sensitive synchronization conflicts involving identity, delegation, approval, rights, consent, ownership, publication, evidence, closure, or revocation require deterministic resolution or explicit authorized review.
- **REQ-COMP-DATA-016 — SHALL NOT:** Last-write-wins, arrival order, local timestamp, transport success, or implementation prevalence decide authority-sensitive data conflicts.
- **REQ-COMP-DATA-017 — SHALL:** A component-owned export identify the included data domains, external-owner references, schema versions, policy and consent context, artifact dependencies, and restore order.
- **REQ-COMP-DATA-018 — SHALL:** A restore write component-owned state only through the owning component's restore or migration contract and validate ownership before activation.
- **REQ-COMP-DATA-019 — SHALL NOT:** A database dump, filesystem copy, replica, backup, or migration script bypass component ownership or be treated as an active restore before validation.
- **REQ-COMP-DATA-020 — SHALL:** A change of authoritative owner require an accepted decision, complete impact analysis, a versioned migration plan, target validation, an explicit cutover, and evidence that no parallel active owner remains.
- **REQ-COMP-DATA-021 — SHALL:** Ownership cutover preserve stable identities or provide explicit redirects and disposition records for every moved, split, merged, superseded, or rejected object.
- **REQ-COMP-DATA-022 — SHALL:** Critical ownership, migration, restore, publication, revocation, and destructive-transition operations produce machine-readable receipts or evidence records.
- **REQ-COMP-DATA-023 — SHALL:** Logs, metrics, traces, dead-letter records, and evidence references minimize governed payload data and follow the source owner's classification, retention, disclosure, and consent rules.
- **REQ-COMP-DATA-024 — SHALL:** A component data-ownership conformance claim pass only when ownership uniqueness, access isolation, contract routing, reference integrity, migration safety, restore behavior, and evidence tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Ownership Registration and Change Procedure

### 6.1 Register a new data domain

A new authoritative domain is introduced through this sequence:

1. identify the component that is accountable for the domain result;
2. define the domain identity, object identities, schema, states, mutations, retention, export, restore, and evidence;
3. register the owner in `generated/component-catalog.json`;
4. define the domain in the owning component contract;
5. define commands, queries, events, artifacts, references, and failure behavior;
6. link decisions, requirements, locks, tests, and evidence;
7. validate that no existing active owner claims the same domain;
8. activate the updated authority release.

A new table, file, queue, or API does not create a domain owner without this process.

### 6.2 Add a cross-component reference

A reference design records:

- source component;
- referenced owner;
- object identity;
- relationship;
- copied fields, if any;
- freshness;
- revocation and deletion behavior;
- authorization;
- offline behavior.

The copied field set is minimized. Consumers query or subscribe to the owner when current authoritative state is required.

### 6.3 Add a read model or replica

The design records:

- source owners;
- derivation and rebuild process;
- snapshot or lag semantics;
- consumer access controls;
- correction and withdrawal behavior;
- failure state;
- retention;
- explicit non-authoritative classification.

A derived store is deleted and rebuilt rather than manually repaired when canonical reconstruction is possible.

### 6.4 Change an existing owner

Ownership transfer is a semantic architecture change.

The transfer process is:

1. accept an owner decision;
2. freeze the affected ownership definition;
3. inventory every object, reference, event, artifact, test, evidence record, backup, restore path, and consumer;
4. define stable identity preservation or redirects;
5. define source and target schemas;
6. define migration, validation, rollback, and forward repair;
7. stage the target without activating parallel authority;
8. migrate and validate the complete in-scope state;
9. update contracts, requirements, locks, tests, profiles, operations, and documentation;
10. activate the target owner atomically;
11. disable source-owner mutation;
12. verify that references resolve and no parallel owner remains;
13. record cutover evidence;
14. archive or retain the source representation according to migration policy.

A split or merge follows the same procedure for every resulting domain.

### 6.5 Export and restore

Each component exports its own authoritative state.

A coordinator may assemble a package but cannot read or mutate private component storage outside declared interfaces.

Restore proceeds by component contracts in declared order. Each owner validates its package, reconstructs staged state, performs migrations, verifies external references, and reports readiness.

The complete restored composition becomes active only after required system, profile, component, policy, artifact, security, and evidence checks pass.

### 6.6 Destructive operations

Deletion, revocation, withdrawal, and irreversible migration require:

- resolved authority;
- explicit scope;
- owner execution;
- reference and downstream-impact analysis;
- retention and consent checks;
- required approval;
- receipt or evidence;
- recovery or recourse behavior.

A consumer cannot delete source-owned data by deleting its local reference.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained capability | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| Domain has no registered owner | Block activation and mutation | Existing unrelated domains | Guessing an owner | Ownership-resolution result |
| Multiple active owners claim one domain | Block affected authority | Previously valid unaffected state | Dual writes or last-writer selection | Ownership-conflict report |
| Caller attempts direct cross-owner write | Reject and report boundary violation | Owner's valid state | Shared-table mutation | Boundary test result |
| Owner interface is unavailable | Apply declared queue, retry, read-only, or failure path | Unrelated components and cached views with visible freshness | Writing through a replica or database shortcut | Interface-health result |
| Read model is stale | Expose freshness or disable current-state claims | Declared stale read-only use | Presenting it as current authority | Freshness record |
| Event is duplicated | Apply idempotent consumer behavior | Prior committed result | Duplicate authoritative effect | Duplicate-handling record |
| Event ordering is unresolved | Pause affected processing or apply declared partition-local rules | Independent events | Inferring global order from arrival | Ordering result |
| External reference cannot resolve | Mark the relationship unavailable, stale, revoked, or blocked | Source-owned local object where valid | Recreating the external object locally as authority | Reference-resolution result |
| Source object is revoked or withdrawn | Apply declared local effect | Unaffected local state | Continuing to present the copy as valid source state | Revocation result |
| Synchronization conflict affects authority | Enter explicit review or deterministic resolution | Uncontested local work | Last-write-wins | Conflict record |
| Migration validation fails | Keep source owner active or enter declared recovery | Last known valid authority | Partial ownership cutover | Migration result |
| Both source and target accept writes | Block cutover and repair ownership state | Read-only investigation | Parallel active authority | Dual-authority failure |
| Restore package is incomplete | Keep staged state inactive | Current active deployment | Activating partial restore | Restore validation |
| Evidence path is unavailable | Block critical ownership transition | Noncritical operations explicitly permitted | Unevidenced destructive or ownership transition | Evidence-delivery state |
| Physical isolation control fails | Block affected profile claim and writes where ownership can be bypassed | Verified unaffected domains | Treating shared credentials as acceptable | Isolation test |
| Storage integrity fails | Stop writes to affected domain and enter recovery | Verified read-only or unaffected partitions | Silent repair through another component | Integrity evidence |
| Policy or consent is unavailable | Fail closed for affected disclosure or governed mutation | Explicitly safe local use | Inferring prior consent or policy | Policy result |

Safe degradation never invents a new owner, promotes a derived copy, bypasses a component contract, or creates parallel authority.

## 8. Cross-Component Ownership Patterns

### 8.1 Command to the owner

A caller requests mutation from the owning component.

```text
caller
  -> owner command contract
  -> owner validates identity, authority, policy, version, and payload
  -> owner commits owned state
  -> result, event, and required receipt
```

### 8.2 Query and projection

A consumer requests a projection from the owner.

```text
consumer
  -> owner query contract
  -> owner applies authorization and redaction
  -> projection with source and freshness context
```

The consumer can store a declared read model without acquiring source ownership.

### 8.3 External-owner reference

Orgo can reference a Kristal artifact, Konnaxion object, kOA Mediatheque media record, identity, policy result, publication receipt, or audit evidence record.

The reference preserves the external owner. Orgo owns only its workflow relationship to the reference.

### 8.4 Domain event

A component emits a fact after commit.

Consumers update only their own state. Replaying the event rebuilds consumer state and does not repeat the publisher's original mutation.

### 8.5 Immutable artifact exchange

A producer creates a versioned artifact.

The receiver validates compatibility and activation authority. Copying the artifact does not transfer producer authority, and receiving it does not activate it automatically.

### 8.6 Governed publication

A source component submits a publication request to Publication Gateway.

The gateway evaluates the transfer contract and applicable policy, then records publication, rejection, withdrawal, or failure. The destination does not receive direct write authority into the source domain.

### 8.7 Shared database process

A lightweight deployment can place multiple component schemas in one database process.

Each component keeps:

- its own service identity;
- its own schema or logical database;
- its own migrations;
- write access only to its namespace;
- controlled views or query interfaces for consumers;
- separate backup and restore inventory.

### 8.8 Offline synchronization

Two authorized Orgo peers exchange Orgo-owned objects through an explicit session.

The session preserves identities and version context. Assignment, approval, rights, closure, and evidence conflicts enter review rather than last-write-wins.

### 8.9 Export and credible exit

A portability coordinator requests exports from each owner.

Each owner returns a scoped package. The coordinator assembles a manifest. A clean restore or independent consumer validates the data without converting the coordinator into the owner.

### 8.10 Ownership transfer

An accepted decision moves a domain from one component to another.

The target is staged and validated. Cutover activates the target and disables source mutation as one controlled transition. Redirects and disposition records preserve lineage.

## 9. Decision Closure and Prohibited Assumptions

This document is supported by the accepted decisions declared in its metadata.

A semantic ownership change requires:

1. an accepted owner decision;
2. direct and transitive impact analysis;
3. updates to component identity, contracts, profiles, requirements, locks, tests, evidence, lifecycle, operations, migration, and documentation;
4. complete validation before authority activation.

The following assumptions are prohibited:

- a table owner is determined by the service that created it first;
- a database administrator is the semantic owner of every stored domain;
- one database process means one data owner;
- one transaction spanning two schemas grants shared business authority;
- read access grants write authority;
- a foreign key transfers ownership;
- a replicated row is a second source of truth;
- a cache becomes authoritative when the source is offline;
- a search index can repair source data;
- a workflow coordinator owns participant records;
- a gateway owns the source content it transfers;
- Audit Broker owns the operational state that produced evidence;
- Governance Policy Runtime owns the business state affected by a policy decision;
- Resource Governor owns the job result it schedules;
- an integration provider owns local state derived from its response;
- external AI output can become authoritative without owner validation;
- arrival time or local timestamp resolves an authority conflict;
- a backup or dump is active restored state;
- a migration script can change ownership without an accepted decision;
- temporary dual writes are acceptable without a declared and tested cutover protocol;
- source-code behavior can override the active ownership registry;
- a recipe-selected storage topology creates global ownership rules.

No active exception currently weakens a requirement in this document.

## 10. Validation Criteria

This document is conformant when:

1. it is registered as `DOC-COMP-002`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, globally scoped, and testable;
5. every lock exists and applicable assertions pass;
6. every active authoritative data domain has exactly one active owner;
7. every owner is represented consistently in the components registry and component contract;
8. every component has write access only to its owned authoritative namespaces;
9. direct writes to another owner's tables, files, private queues, caches, or object-store paths are absent;
10. every mutation path routes through the owning component contract;
11. every cross-component reference identifies the external owner;
12. every read model, cache, replica, search index, and analytics store declares non-authoritative status and rebuild behavior;
13. event consumers are idempotent and do not repeat publisher mutations;
14. profile-specific physical consolidation preserves logical isolation and write controls;
15. UCKK publication cannot bypass gateway authorization or bridge transport;
16. policy, resource, audit, integration, transport, workflow, and AI systems do not acquire participant data ownership;
17. authority-sensitive synchronization conflicts avoid last-write-wins;
18. exports and restores preserve ownership and external-owner references;
19. restore activation follows owner contracts and complete validation;
20. every ownership change has a decision, migration plan, atomic cutover, lineage, and evidence;
21. no parallel active owner remains after cutover;
22. critical destructive and ownership transitions produce required receipts;
23. logs and evidence comply with source-owner classification and minimization;
24. the active text contains the complete required section structure and no unresolved marker.

Applicable failure codes include:

```text
authoritative_owner_missing
duplicate_authoritative_owner
component_contract_owner_mismatch
direct_cross_component_write
shared_service_identity_violation
cross_owner_write_grant
external_owner_reference_missing
derived_store_marked_authoritative
read_model_freshness_missing
read_model_rebuild_missing
event_duplicate_effect
event_ownership_transfer
gateway_ownership_violation
policy_data_ownership_violation
resource_data_ownership_violation
authority_sensitive_last_write_wins
restore_owner_bypass
migration_owner_decision_missing
parallel_active_owner
ownership_cutover_incomplete
ownership_receipt_missing
governed_payload_overexposure
```

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Orgo references Kristal

Orgo stores a Kristal artifact identity in a case.

Orgo owns the case and its relationship to the artifact. Kristal Runtime owns the artifact identity and epistemic payload. Orgo cannot add workflow metadata to the Kristal identity.

### Example 2 — Shared PostgreSQL process

Konnaxion and Orgo use one PostgreSQL process in a lightweight profile.

They use separate service identities, schemas, migrations, backup entries, and write grants. A controlled view or API exposes selected data. Physical consolidation does not create shared ownership.

### Example 3 — kOA Mediatheque media reference

A task references a kOA Mediatheque media record.

Orgo owns the task. kOA Mediatheque owns the media, derivatives, provenance, and media access state. Media withdrawal is propagated through the declared contract, and Orgo updates the task without rewriting kOA Mediatheque.

### Example 4 — Derived search index

A component builds a search index from several component projections.

The index records source owners and freshness. It is rebuildable and non-authoritative. Search results cannot directly repair or overwrite source records.

### Example 5 — Publication

Orgo requests publication of approved material.

Publication Gateway validates disclosure and performs the transfer. Orgo records the request and receipt. Konnaxion or another destination does not write back into Orgo's private database.

### Example 6 — Offline conflict

Two Orgo nodes modify different ordinary notes and one authority-sensitive assignment.

The ordinary notes can merge under a declared deterministic rule. The assignment conflict enters authorized review. Arrival time does not decide the assignee.

### Example 7 — Clean restore

A portability package contains separate exports for Orgo, Konnaxion, kOA Mediatheque, Identity and Trust, policy state, and evidence references.

Each owner restores its own state through its contract. The coordinator cannot load all tables directly into a shared database and claim success.

### Example 8 — Ownership transfer

An accepted decision moves a distribution-status domain from Orgo to another component.

The migration preserves identifiers, updates references, validates the target, activates the new owner, disables Orgo mutation, and records cutover evidence. Historical Orgo records remain available according to retention and lineage rules.
