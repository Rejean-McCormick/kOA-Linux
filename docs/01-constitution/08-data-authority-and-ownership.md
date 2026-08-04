<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/cross_component_communication",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-CONST-DATA-001",
    "REQ-CONST-DATA-002",
    "REQ-CONST-DATA-003",
    "REQ-CONST-DATA-004",
    "REQ-CONST-DATA-005",
    "REQ-CONST-DATA-006",
    "REQ-CONST-DATA-007",
    "REQ-CONST-DATA-008",
    "REQ-CONST-DATA-009",
    "REQ-CONST-DATA-010",
    "REQ-CONST-DATA-011",
    "REQ-CONST-DATA-012",
    "REQ-CONST-DATA-013",
    "REQ-CONST-DATA-014",
    "REQ-CONST-DATA-015",
    "REQ-CONST-DATA-016",
    "REQ-CONST-DATA-017",
    "REQ-CONST-DATA-018",
    "REQ-CONST-DATA-019",
    "REQ-CONST-DATA-020",
    "REQ-CONST-DATA-021",
    "REQ-CONST-DATA-022",
    "REQ-CONST-DATA-023",
    "REQ-CONST-DATA-024"
  ],
  "lock_ids": [
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007"
  ],
  "tags": [
    "constitution",
    "data-authority",
    "data-ownership",
    "component-separation",
    "cross-component-communication",
    "gateways",
    "fail-closed"
  ]
}
KOA:DOC-META:END -->

# Data Authority and Ownership

## 1. Purpose

This document defines the constitutional model for data authority and ownership across the kOA operating environment.

It explains how the global data-authority rules in `contracts/system.contract.json` apply to components, profiles, gateways, storage topologies, transfers, derived data, recovery, and conformance.

The model makes these outcomes deterministic:

- every authoritative data domain has one identifiable owner;
- physical colocation does not erase logical boundaries;
- components exchange data through explicit contracts;
- cross-component mutation is controlled and observable;
- derived stores remain subordinate to their sources;
- ambiguity fails closed at the affected authority boundary;
- profile-specific infrastructure choices do not alter global ownership;
- changes to ownership receive full decision, impact, migration, and validation treatment.

This document does not assign component-specific fields, tables, file formats, APIs, events, retention periods, database engines, storage paths, or deployment topology. Those details belong to their canonical registries, component contracts, profile contracts, and artifact contracts.

## 2. Scope

This document applies globally to:

- every active kOA component;
- every authoritative data domain;
- every deployment profile and profile overlay;
- every component contract;
- every cross-component API, command, event, artifact, export, import, publication, and gateway;
- every database, schema, file store, object store, queue, cache, index, read model, analytics store, and backup that contains component data;
- every migration, replication, restore, rollback, and forward-repair operation;
- every external integration that receives from or contributes to component-owned data;
- every conformance claim involving data authority or component separation.

The document governs logical authority independently of physical placement.

A profile can consolidate services onto one host, one database process, one storage pool, one message broker, or one backup system. Consolidation changes operational topology. It does not create shared logical ownership.

A profile can also separate components across hosts, databases, networks, or storage identities. Separation strengthens isolation but does not create a new owner unless an accepted decision and canonical registry update explicitly transfer ownership.

This document excludes:

- component-internal field definitions;
- component-internal algorithms;
- implementation recipes;
- vendor-specific database administration;
- operating-system file permissions except where they enforce a declared authority boundary;
- historical migration sources after their accepted content has been transferred into active authority.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `generated/decision-index.json` | Accepted owner decisions that authorize data-boundary and gateway changes |
| `contracts/system.contract.json#/data_authority` | Global data-authority principles and transfer rules |
| `contracts/system.contract.json#/cross_component_communication` | Permitted and prohibited cross-component communication mechanisms |
| `generated/component-catalog.json` | Component identities, responsibilities, authoritative data domains, prohibited overlaps, and dependencies |
| `generated/component-catalog.json` | Active component-contract inventory and coverage |
| `contracts/components/*.component.json` | Observable inputs, outputs, commands, events, state, data boundaries, failures, and compatibility |
| `generated/profile-catalog.json` | Active profile inventory |
| `contracts/profiles/*.profile.json` | Profile-specific topology, isolation, activation, storage, database, and resource behavior |
| `generated/requirements-index.json` | Canonical requirement text, strength, scope, source, owner, and validation |
| `generated/assertion-index.json` | Interfile assertions protecting data authority, gateway separation, scope, and implementation boundaries |
| `generated/traceability.json` | Links from decisions and requirements through locks, contracts, tests, and evidence |
| `generated/exception-index.json` | Approved, bounded deviations and compensating controls |

Markdown in this file explains the constitutional model. It does not replace the registries or component contracts named above.

## 4. Model and Responsibilities

### 4.1 Authoritative data domain

An authoritative data domain is a coherent set of mutable facts for which one component is accountable.

The owner controls:

- accepted creation and mutation operations;
- validation of incoming commands and transfers;
- authoritative state transitions;
- canonical identifiers within the domain;
- persistence semantics;
- deletion and retention behavior;
- export behavior;
- compatibility and migration;
- backup and recovery responsibility;
- evidence for critical transitions.

Ownership is logical. It is not inferred from:

- the host on which data is stored;
- the database administrator;
- the storage account;
- the backup operator;
- the component that reads the data most often;
- the component that created a cache or index;
- the component that transports the data;
- the component that presents the data in an interface;
- implementation prevalence;
- historical accident.

### 4.2 Owning component

The owning component is the only component permitted to perform authoritative mutation for its declared data domain.

The ownership declaration is split across two canonical layers:

1. `generated/component-catalog.json` identifies the component and summarizes its authoritative data responsibility.
2. The active component contract defines the observable operations, state transitions, inputs, outputs, events, failures, and compatibility rules through which that authority is exercised.

The component document under `04-components/` explains the contract but does not create additional authority.

### 4.3 Source of truth

A source of truth is the active representation controlled by the owning component and recognized by its contract.

A source of truth can be implemented with:

- relational tables;
- document records;
- content-addressed objects;
- files;
- append-only logs;
- event streams;
- signed artifacts;
- another contract-defined store.

The storage technology does not determine authority.

A source of truth remains authoritative only while its owning component, contract version, authority state, and applicable policy are valid.

### 4.4 Derived data

Derived data includes:

- caches;
- search indexes;
- materialized views;
- analytics stores;
- reporting replicas;
- thumbnails and previews;
- extracted text;
- recommendation inputs;
- generated catalogs;
- local convenience copies;
- projections used by another component.

A derived store has a declared source, refresh model, invalidation model, retention rule, and recovery behavior.

The owner of a derived store controls the projection mechanics. It does not acquire ownership of the source facts.

A derived store can contain component-owned operational data of its own, such as indexing progress, retry state, or local diagnostics. Those local facts remain separate from the represented source facts.

### 4.5 Shared infrastructure

Shared infrastructure is permitted when an active profile declares it.

Examples include:

- one PostgreSQL process serving multiple components;
- one object-storage service with separate buckets or namespaces;
- one message broker with separate identities and topics;
- one backup appliance;
- one host file system with separate directories and identities;
- one cache service with namespaced keys.

Shared infrastructure preserves these logical properties:

- distinct component identities;
- distinct namespaces or equivalent boundaries;
- least-privilege access;
- no undeclared mutation of foreign authoritative state;
- contract-mediated transfers;
- traceable administration;
- recoverable ownership mapping.

A shared process is an operational optimization, not a constitutional merger.

### 4.6 Cross-component transfer

A cross-component transfer moves information between authority domains without silently moving ownership.

Permitted transfer mechanisms include:

- a versioned API;
- a validated command;
- a published event;
- a signed artifact;
- a user-authorized export and import;
- a governed gateway;
- another mechanism explicitly registered by the system and component contracts.

The producer remains responsible for the correctness of the exported representation at the producer boundary.

The consumer becomes responsible for validating the input and for any new state created inside the consumer's domain.

The transfer contract identifies:

- producer;
- consumer;
- direction;
- payload or artifact contract;
- version;
- authorization;
- trust and integrity checks;
- replay and idempotency behavior;
- failure ownership;
- receipt or evidence behavior;
- data minimization and retention where applicable.

### 4.7 Mutation and observation

Observation does not imply mutation authority.

A component can receive read access through an active contract without receiving:

- write access;
- deletion authority;
- schema-migration authority;
- retention authority;
- publication authority;
- administrative ownership.

Mutation is accepted only by the owning component through a declared operation or controlled import path.

Database credentials, file permissions, root access, backup access, or infrastructure administration do not replace the application-level ownership model.

### 4.8 Publication Gateway

The Publication Gateway controls cross-domain disclosure and publication to another audience, domain, tenant, organization, or external destination.

Its responsibility includes the publication boundary, applicable authorization, disclosure policy, destination, release evidence, and publication result.

The Publication Gateway does not become the owner of the source domain merely because it transports or releases source data.

### 4.9 UCKK Dimension Gateway

The UCKK Dimension Gateway controls user-selected media admission into a UCKK dimension.

Its responsibility includes:

- the selected-media transfer;
- dimension targeting;
- integrity verification;
- controlled admission;
- transfer result;
- applicable receipt or evidence.

The UCKK Dimension Gateway does not replace the Publication Gateway and does not acquire all UCKK platform authority merely because it performs ingestion.

### 4.10 Profiles and topology

A profile owns conditional deployment behavior, including:

- process placement;
- database topology;
- storage topology;
- network segmentation;
- service activation;
- resource allocation;
- isolation strength;
- backup topology.

A profile does not independently reassign logical data ownership.

Examples:

- `user_lightweight` can use one shared database process while maintaining separate schemas or databases and component identities.
- `sovereign_linux_node` can use separate database instances and storage identities.
- `high_assurance` can increase separation and verification.
- a developer profile can namespace databases, volumes, ports, and secrets by workspace.

These choices alter containment and operational risk. They do not alter the owning component unless the canonical ownership registry changes.

### 4.11 Backup, restore, and rollback

Backup ownership and data ownership are distinct.

A backup service can copy, encrypt, retain, verify, and restore data without becoming its application owner.

A restore operation preserves:

- component identity;
- data-domain identity;
- contract compatibility;
- schema compatibility;
- release compatibility;
- ordering constraints;
- receipt and evidence links.

A restore that would create mixed incompatible authoritative state remains blocked or uses an approved forward-repair process.

### 4.12 Data-authority changes

The following changes affect constitutional data authority:

- assigning a new owner;
- transferring ownership;
- splitting or merging a data domain;
- allowing a new cross-component mutation path;
- changing a gateway responsibility;
- converting a derived store into a source of truth;
- changing deletion or retention authority across components;
- changing restore authority;
- changing the trust boundary of a transfer;
- allowing shared credentials to cross component boundaries.

These changes receive major semantic-change treatment because they alter who can create, modify, disclose, delete, recover, or attest to authoritative state.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-DATA-001,REQ-CONST-DATA-002,REQ-CONST-DATA-003,REQ-CONST-DATA-004,REQ-CONST-DATA-005,REQ-CONST-DATA-006,REQ-CONST-DATA-007,REQ-CONST-DATA-008,REQ-CONST-DATA-009,REQ-CONST-DATA-010,REQ-CONST-DATA-011,REQ-CONST-DATA-012,REQ-CONST-DATA-013,REQ-CONST-DATA-014,REQ-CONST-DATA-015,REQ-CONST-DATA-016,REQ-CONST-DATA-017,REQ-CONST-DATA-018,REQ-CONST-DATA-019,REQ-CONST-DATA-020,REQ-CONST-DATA-021,REQ-CONST-DATA-022,REQ-CONST-DATA-023,REQ-CONST-DATA-024 -->
- **REQ-CONST-DATA-001 — SHALL:** Every authoritative data domain have exactly one owning component.
- **REQ-CONST-DATA-002 — SHALL:** Every owning component declare its authoritative data domains in `generated/component-catalog.json` and its active component contract.
- **REQ-CONST-DATA-003 — SHALL NOT:** A component write directly to another component's authoritative source tables, files, object stores, queues, indexes, or mutable internal state.
- **REQ-CONST-DATA-004 — SHALL NOT:** Shared physical infrastructure create shared logical authority or permit undeclared cross-component mutation.
- **REQ-CONST-DATA-005 — SHALL:** Components sharing a database service use distinct logical namespaces and distinct component identities for authoritative writes.
- **REQ-CONST-DATA-006 — SHALL:** A cross-component mutation use an active versioned API, command, event, signed artifact, user-authorized transfer, or governed gateway contract.
- **REQ-CONST-DATA-007 — SHALL:** The receiving owner validate authorization, contract version, payload integrity, replay behavior, and applicable policy before changing authoritative state.
- **REQ-CONST-DATA-008 — SHALL NOT:** Data transfer, replication, caching, indexing, backup, export, or physical colocation transfer canonical ownership implicitly.
- **REQ-CONST-DATA-009 — SHALL:** Derived projections, indexes, caches, search stores, analytics stores, and read models declare their authoritative source and remain rebuildable from that source.
- **REQ-CONST-DATA-010 — SHALL NOT:** A derived projection, cache, index, search store, or generated view become the sole authoritative source for the data it represents.
- **REQ-CONST-DATA-011 — SHALL:** Every component contract declare owned data domains, accepted inputs, produced outputs, mutable state, derived state, deletion behavior, export behavior, and recovery responsibility.
- **REQ-CONST-DATA-012 — SHALL:** Every cross-domain transfer preserve provenance sufficient to identify the source owner, transfer contract, initiating authority, destination owner, and result.
- **REQ-CONST-DATA-013 — SHALL:** Cross-domain disclosure and publication use the Publication Gateway contract.
- **REQ-CONST-DATA-014 — SHALL:** User-selected media admission into UCKK use the UCKK Dimension Gateway contract.
- **REQ-CONST-DATA-015 — SHALL NOT:** The Publication Gateway and UCKK Dimension Gateway substitute for one another or merge their authority boundaries.
- **REQ-CONST-DATA-016 — SHALL:** A deployment profile preserve logical data ownership when it changes process placement, database topology, storage topology, network topology, or resource allocation.
- **REQ-CONST-DATA-017 — SHALL NOT:** Administrative, database, host, backup, or infrastructure privilege grant an application component authority over another component's data.
- **REQ-CONST-DATA-018 — SHALL:** Backup, restore, rollback, replication, and migration procedures preserve component ownership boundaries and prevent mixed-version authoritative state.
- **REQ-CONST-DATA-019 — SHALL:** A change to data ownership, authoritative boundaries, transfer contracts, or gateway responsibility be classified as a major semantic change.
- **REQ-CONST-DATA-020 — SHALL:** A major data-authority change reference an accepted owner decision, complete impact report, migration plan, compatibility disposition, and rollback or forward-repair plan.
- **REQ-CONST-DATA-021 — SHALL:** Authority ambiguity, ownership collision, unresolved contract version, or failed authorization block the affected mutation.
- **REQ-CONST-DATA-022 — SHALL:** A failed cross-component transfer preserve the last valid authoritative state and report an explicit failure result to the initiating actor or component.
- **REQ-CONST-DATA-023 — SHALL:** Critical cross-domain mutation, disclosure, publication, activation, restore, and migration operations produce machine-readable receipts or evidence records.
- **REQ-CONST-DATA-024 — SHALL:** Any approved exception to a data-authority requirement be explicit, narrowly scoped, registered, time-bounded or condition-bounded, supported by compensating controls, and evidenced.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering a data domain

1. Reference an accepted owner decision.
2. Identify the component that is accountable for the domain.
3. Confirm that no active component already owns the same or an overlapping domain.
4. Add the ownership declaration to `generated/component-catalog.json`.
5. Define the observable data boundary in the component contract.
6. Define accepted inputs, produced outputs, mutations, states, failures, exports, deletion, and recovery.
7. Add applicable requirements and locks.
8. Add tests for ownership collision and prohibited direct writes.
9. Add evidence definitions.
10. Compute direct and transitive impact.
11. Update explanatory documents and generated projections.
12. Run complete validation.
13. Activate the authority set as one release.

Completion occurs only when the component, contract, requirements, locks, tests, evidence, and documentation resolve to one non-overlapping owner.

### 6.2 Performing a cross-component mutation

1. The initiating actor or component selects an active transfer contract.
2. The producer verifies its authority to disclose or transfer the source representation.
3. The producer creates the versioned payload, command, event, or artifact.
4. The transfer mechanism authenticates the participants and protects integrity.
5. The receiving owner verifies contract version, authorization, integrity, policy, and replay behavior.
6. The receiving owner applies its own validation and state-transition rules.
7. The receiving owner either commits a complete local mutation or rejects the operation.
8. The system records the outcome required by the transfer contract.
9. Retries use the declared idempotency or deduplication behavior.
10. Failure leaves the last valid authoritative state intact.

The initiating component never bypasses the receiving owner's contract to mutate the receiving owner's internal store.

### 6.3 Creating a derived projection

1. Identify the authoritative source.
2. Define the projection purpose and scope.
3. Define the source reference and contract version.
4. Define refresh, invalidation, replay, and rebuild behavior.
5. Define local operational state separately from represented source facts.
6. Define access and retention.
7. Define failure behavior when the source is unavailable or incompatible.
8. Validate that the projection is not treated as the source of truth.
9. Register tests and evidence.
10. Activate the projection with its dependent release.

### 6.4 Changing ownership

1. Create an accepted owner decision.
2. Classify the change as major.
3. Generate a complete impact report.
4. Identify predecessor and successor owners.
5. Define the exact transfer boundary and activation condition.
6. Update `generated/component-catalog.json`.
7. Update both affected component contracts.
8. Update transfer, migration, compatibility, backup, restore, rollback, and forward-repair rules.
9. Update requirements, locks, tests, evidence, profiles, documents, and AI contexts.
10. Reserve historical identifiers and preserve succession links.
11. Validate the complete proposed release.
12. Activate all affected objects atomically.
13. Retain the predecessor authority only as historical evidence after activation.

A file move, database move, process move, or team reorganization does not execute this procedure automatically.

### 6.5 Restoring component data

1. Identify the component, data domain, backup set, contract version, and target release.
2. Verify backup integrity and provenance.
3. Verify compatibility among application, schema, artifacts, policies, and related domains.
4. Determine ordering across dependent components.
5. Quiesce or isolate affected mutation paths.
6. Restore into the owning component's authority boundary.
7. Run migrations or forward repair where required.
8. Validate invariants and cross-component references.
9. Resume mutation only after required checks pass.
10. Produce restore evidence and retain the previous valid recovery point according to policy.

A partial restore does not create partial authority.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| Ownership is missing | Block activation and affected mutation | Previous valid owner, when one exists | New or inferred ownership | Ownership-validation report |
| Two components claim the same domain | Block both new claims | Previous valid non-conflicting authority | Overlapping mutation authority | Collision report and impact report |
| Transfer contract is missing | Reject the transfer | Producer and consumer local authority | Cross-component mutation | Contract-resolution diagnostic |
| Contract version is incompatible | Reject or route to an approved adapter | Compatible local operations | Incompatible mutation | Compatibility test evidence |
| Authorization is absent or invalid | Fail closed at the receiving boundary | Unaffected capabilities | Requested mutation or disclosure | Authorization decision and receipt |
| Payload integrity fails | Reject without local commit | Last valid state | Corrupt or unverifiable input | Integrity diagnostic |
| Replay behavior is undefined | Block activation of the transfer path | Existing validated path | New replay-sensitive path | Contract-validation report |
| Derived store is stale | Mark the projection stale or unavailable | Source authority | Projection-based mutation or claim | Projection freshness evidence |
| Source is unavailable | Preserve the last valid local state; use read-only behavior only when explicitly permitted | Declared unaffected or read-only capability | New source-dependent mutation | Degradation evidence |
| Shared credentials cross boundaries | Block activation and credential use | Properly separated identities | Undeclared foreign mutation | Identity and permission audit |
| Restore versions are incompatible | Block restore activation or use forward repair | Existing active release | Mixed-version authoritative state | Restore compatibility report |
| Publication policy fails | Reject publication | Source-domain authority | External disclosure | Publication failure receipt |
| UCKK admission validation fails | Reject admission | Original media and UCKK existing state | New UCKK admission | Admission failure receipt |
| Validation tooling cannot execute | Mark validation blocked | Previous valid release | New release activation | Blocked validation report |

Safe degradation is capability-scoped.

A failure in one transfer or projection does not erase unrelated component authority. It also does not authorize a fallback mutation path.

Read-only or advisory behavior exists only when the owning contract or active profile defines it. Silence, implementation convenience, or a cached copy does not create a fallback source of truth.

## 8. Cross-Component Interactions

### 8.1 Interaction contract

Every cross-component interaction identifies:

| Field | Meaning |
| --- | --- |
| Producer | Component or actor producing the input |
| Consumer | Owning component receiving the input |
| Direction | Producer-to-consumer, consumer-to-producer, or bidirectional |
| Contract | Active API, command, event, artifact, or gateway contract |
| Authority boundary | Owner of source facts and owner of resulting facts |
| Trust | Authentication, authorization, integrity, and policy checks |
| Replay behavior | Idempotency, deduplication, ordering, or rejection rules |
| Evidence | Receipt, event, test evidence, or audit record |
| Failure owner | Component responsible for reporting and recovery |
| Prohibited access | Internal stores or operations unavailable to the peer |

### 8.2 Read interaction

A read interaction can expose a contract-defined representation.

The producer controls:

- the representation;
- authorization;
- visibility;
- version;
- consistency semantics.

The consumer controls its local use of the representation.

The read interaction does not grant mutation authority.

### 8.3 Command interaction

A command requests that the receiving owner evaluate and perform a state transition.

The sender owns the request.

The receiver owns:

- authorization;
- validation;
- acceptance or rejection;
- resulting state;
- response;
- idempotency;
- evidence.

A command is not a remote database write.

### 8.4 Event interaction

An event describes an accepted occurrence in the producer's domain.

Consumers can use the event to update their own domains.

Consumers do not rewrite the producer's event history or source state.

Event replay, ordering, deduplication, retention, and compatibility belong to the event and component contracts.

### 8.5 Artifact interaction

A signed or versioned artifact can carry a stable representation between components or across offline boundaries.

The artifact contract owns its serialized form, integrity properties, compatibility, provenance, and activation rules.

The receiving component owns admission into its own domain.

Possession of an artifact does not imply acceptance or activation.

### 8.6 Gateway interaction

A gateway mediates a defined authority boundary.

It does not erase the producer and consumer owners.

The Publication Gateway mediates publication and disclosure.

The UCKK Dimension Gateway mediates selected-media admission into UCKK.

A gateway can validate, transform, transport, queue, or record a transfer within its contract. It cannot silently absorb the source domain or destination domain.

### 8.7 Infrastructure interaction

Database administrators, backup systems, schedulers, resource managers, operating-system services, and observability systems can interact with component data for infrastructure purposes.

Their access remains constrained to the declared operational responsibility.

Infrastructure access does not create application ownership, business authority, publication authority, or deletion authority beyond the active contract and policy.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision ID | Effect on this document |
| --- | --- |
| `DEC-DATA-001` | Establishes mandatory logical data ownership, permits profile-controlled physical sharing, and prohibits direct writes into another component's authoritative source tables |
| `DEC-GATE-001` | Keeps Publication Gateway and UCKK Dimension Gateway as separate contracts with separate authority boundaries |

### 9.2 Protected alignment locks

| Lock ID | Protected relationship |
| --- | --- |
| `LOCK-DATA-001` | No component writes directly to another component's authoritative source tables |
| `LOCK-GATE-001` | Publication Gateway and UCKK Dimension Gateway remain separate |
| `LOCK-PROFILE-001` | Profile-specific topology and isolation choices do not become global authority |
| `LOCK-IMPL-001` | A recipe or example does not redefine data authority |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- the database owner is the application-data owner;
- a shared database creates shared authority;
- a component that can read data can also modify it;
- a component that stores a copy owns the source facts;
- a cache or search index is authoritative because it is faster or more available;
- a backup service owns the backed-up domain;
- root or administrator access creates product authority;
- physical colocation merges component boundaries;
- physical separation transfers ownership;
- the sender of a command owns the resulting state;
- an event consumer can revise the producer's source event;
- a gateway owns every domain whose data passes through it;
- the Publication Gateway and UCKK Dimension Gateway are interchangeable;
- a development shortcut is acceptable in production authority;
- a recipe can authorize direct database writes;
- a missing contract has an obvious default;
- a failed transfer can be repaired by writing directly to the destination store;
- current implementation behavior overrides the registries;
- historical documentation overrides active authority;
- a user interface view determines the canonical source.

No unresolved data-authority question is permitted inside active authority. A missing owner decision, missing owner, overlapping claim, or undefined transfer contract blocks the affected object.

## 10. Validation Criteria

This document is conformant when all applicable criteria below pass.

1. The file is registered as `DOC-CONST-008` at `01-constitution/08-data-authority-and-ownership.md`.
2. The document class is `normative_markdown`, the status is `active`, the language is `en`, and the scope is global.
3. Every canonical reference resolves to an active registered object.
4. Every requirement ID in metadata appears exactly once in the generated requirement block.
5. Every requirement exists in `generated/requirements-index.json` with matching text, strength, owner, scope, source decision, locks, and validation.
6. Every active component in `generated/component-catalog.json` has exactly one active component contract.
7. Every authoritative data domain has exactly one owner.
8. No two active ownership declarations overlap semantically.
9. Component contracts declare their data boundaries and prohibited foreign mutation.
10. Database roles, schemas, namespaces, storage identities, and permissions do not permit undeclared cross-component authoritative writes.
11. Shared physical infrastructure preserves distinct logical identities and namespaces.
12. Every cross-component mutation path resolves to an active versioned contract.
13. Direct cross-component source-store mutation is rejected by `LOCK-DATA-001`.
14. Publication flows resolve to the Publication Gateway contract.
15. Selected-media admission into UCKK resolves to the UCKK Dimension Gateway contract.
16. `LOCK-GATE-001` confirms that the two gateway contracts remain distinct.
17. Profile contracts do not transfer logical ownership through topology declarations.
18. Derived stores declare source lineage and rebuild behavior.
19. Restore and migration contracts prevent mixed incompatible authoritative state.
20. Major ownership changes include an accepted decision, impact report, migration plan, compatibility disposition, and rollback or forward-repair plan.
21. Every critical transfer, publication, admission, restore, and migration has the required receipt or evidence definition.
22. Every exception is registered and does not silently rewrite the underlying requirement.
23. Traceability connects decisions, requirements, locks, component contracts, profiles, tests, and evidence.
24. Prohibited unresolved markers and unresolved ownership claims are absent.
25. The active document is English-only.
26. Complete documentation validation runs from the declared source tree and does not report success unless tests have executed and valid evidence exists.

Expected validation coverage includes:

```text
TEST-CONST-DATA-001  Unique authoritative owner per data domain
TEST-CONST-DATA-002  Component-contract ownership coverage
TEST-CONST-DATA-003  Direct foreign source-store write rejection
TEST-CONST-DATA-004  Shared infrastructure logical separation
TEST-CONST-DATA-005  Cross-component transfer contract resolution
TEST-CONST-DATA-006  Derived-store source and rebuild declaration
TEST-CONST-DATA-007  Gateway separation
TEST-CONST-DATA-008  Profile topology does not transfer ownership
TEST-CONST-DATA-009  Restore and migration compatibility
TEST-CONST-DATA-010  Receipt and evidence coverage
TEST-CONST-DATA-011  Decision and impact closure
TEST-CONST-DATA-012  Exception and traceability completeness
```

The test catalog and evidence registry own test and evidence definitions. This document does not claim that those tests have already run.

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

### 11.1 Shared PostgreSQL service

A lightweight profile uses one PostgreSQL process.

```text
PostgreSQL process
├── database or schema: orgo
│   └── identity: orgo_runtime
├── database or schema: konnaxion
│   └── identity: konnaxion_runtime
├── database or schema: ariane
│   └── identity: ariane_runtime
└── database or schema: uckk
    └── identity: uckk_platform
```

Each identity can mutate only its own authoritative namespace.

Orgo requests a Konnaxion change through a Konnaxion contract. It does not update Konnaxion tables directly.

### 11.2 Derived search index

Konnaxion publishes a versioned event after accepting a local state transition.

A search component consumes the event and updates a search index.

The search index stores searchable projections and local indexing progress. Konnaxion remains the owner of the represented source facts.

When the index is lost, the search component rebuilds it from the authorized source stream or export.

### 11.3 Publication

A component prepares a publication request that references source objects and the intended audience.

The Publication Gateway evaluates the active disclosure contract, creates the approved release representation, performs the transfer, and returns a publication receipt.

The source component remains the owner of its internal source data. The destination receives authority only according to its own admission and ownership contract.

### 11.4 UCKK admission

A user selects a local media file and invokes the UCKK Dimension Gateway.

The gateway verifies the media, target dimension, transfer authority, and admission contract. The UCKK Platform then decides how the admitted object is represented within its domain.

This flow is not treated as general cross-domain publication.

### 11.5 Sovereign profile

A sovereign profile deploys each component with a separate database instance and storage identity.

The stronger physical separation provides additional assurance. The logical owners remain the same component owners defined in `generated/component-catalog.json`.

### 11.6 Invalid direct write

A recipe suggests that Orgo update a Konnaxion table with a shared database credential.

The example is invalid because it bypasses Konnaxion's component contract and violates `LOCK-DATA-001`. Labeling the procedure as a shortcut, development technique, or recipe does not change that result.
