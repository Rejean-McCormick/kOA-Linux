<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "contracts/integration-types.contract.json",
    "generated/profile-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-DATA-001",
    "DEC-SYS-DATA-002",
    "DEC-SYS-DATA-003",
    "DEC-SYS-DATA-004",
    "DEC-SYS-GOV-001",
    "DEC-SYS-GATE-001",
    "DEC-SYS-SENT-001",
    "DEC-SYS-KRISTAL-001"
  ],
  "requirement_ids": [
    "REQ-SYS-DATA-001",
    "REQ-SYS-DATA-002",
    "REQ-SYS-DATA-003",
    "REQ-SYS-DATA-004",
    "REQ-SYS-DATA-005",
    "REQ-SYS-DATA-006",
    "REQ-SYS-DATA-007",
    "REQ-SYS-DATA-008",
    "REQ-SYS-DATA-009",
    "REQ-SYS-DATA-010",
    "REQ-SYS-DATA-011",
    "REQ-SYS-DATA-012",
    "REQ-SYS-DATA-013",
    "REQ-SYS-DATA-014",
    "REQ-SYS-DATA-015",
    "REQ-SYS-DATA-016",
    "REQ-SYS-DATA-017",
    "REQ-SYS-DATA-018",
    "REQ-SYS-DATA-019",
    "REQ-SYS-DATA-020",
    "REQ-SYS-DATA-021",
    "REQ-SYS-DATA-022",
    "REQ-SYS-DATA-023",
    "REQ-SYS-DATA-024"
  ],
  "lock_ids": [
    "LOCK-DATA-001",
    "LOCK-DATA-002",
    "LOCK-DATA-003",
    "LOCK-DATA-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-SENT-001"
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
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004"
  ],
  "tags": [
    "system-baseline",
    "data-authority",
    "data-ownership",
    "authoritative-data",
    "derived-data",
    "cross-domain-transfer",
    "portability",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# Data Authority and Ownership

## 1. Purpose

This document defines the global system model for data authority and ownership in the kOA operating environment.

It establishes how authoritative data is distinguished from derived data, who may mutate authoritative state, how data crosses component and trust boundaries, how deployment profiles affect physical storage without changing logical ownership, and how ambiguity is handled.

The intended result is one deterministic owner for every authoritative data domain and no implicit authority created by copying, co-location, indexing, analysis, backup, or operational convenience.

## 2. Scope

This document applies to:

- component-owned operational data;
- user content and user-controlled collections;
- identity, credential, trust, and authorization data;
- policy, configuration, resource, and deployment state;
- kOA Mediatheque media, metadata, dimensions, derived representations, and ingestion state;
- Kristal artifacts and epistemic identity;
- Orgo workflow and orchestration state;
- Konnaxion domain state;
- Ariane interaction and local experience state;
- receipts, audit evidence, provenance, release records, and conformance evidence;
- caches, indexes, replicas, projections, search stores, analytical stores, exports, and AI contexts;
- backup, restore, migration, synchronization, publication, disclosure, import, and credible-exit operations;
- every active deployment profile and profile overlay.

This document defines logical authority and system-wide ownership behavior.

It does not:

- assign every concrete table, bucket, queue, or filesystem path;
- prescribe one database technology;
- require physical separation where an active profile permits controlled shared infrastructure;
- replace component contracts, profile contracts, security classifications, retention schedules, or artifact contracts;
- make copied or generated data independently authoritative.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/decision-index.json#/decisions` | Owns accepted decisions that establish or transfer data authority. |
| `contracts/system.contract.json#/data_authority` | Owns the global data-authority model, data classes, transfer rules, and failure behavior. |
| `generated/component-catalog.json#/components` | Owns component identities and high-level authoritative data-domain assignments. |
| `generated/component-catalog.json#/components` | Indexes detailed observable mutation, query, event, export, and import contracts. |
| `generated/profile-catalog.json#/profiles` | Owns profile-dependent physical isolation, tenancy, locality, encryption, and deployment requirements. |
| `contracts/integration-types.contract.json#/integrations` | Owns integration identities, classifications, data-transfer direction, and authority boundaries. |
| `generated/requirements-index.json#/requirements` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json#/locks` | Owns data, component, profile, gateway, governance, and SenTient alignment locks. |
| `generated/traceability.json#/links` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/evidence-catalog.json#/evidence` | Owns evidence identity and validity records. |

## 4. Model and Responsibilities

### 4.1 Authority terms

| Term | Meaning |
| --- | --- |
| Authoritative data | Current state whose accepted mutations and invariants are controlled by one canonical owner. |
| Canonical owner | The active registry or component responsible for authoritative semantics and accepted state transitions. |
| Custodian | A service or operator that stores, transports, backs up, or processes data without acquiring semantic ownership. |
| Derived data | Data computed, copied, indexed, summarized, transformed, embedded, cached, or projected from authoritative data. |
| Evidence | A receipt, proof, log record, attestation, or test result describing an event or state without replacing its source authority. |
| Export | A controlled representation emitted by an owner for portability, analysis, transfer, disclosure, or backup. |
| Import | A proposal presented to an owner for validation and possible acceptance into authoritative state. |
| Disclosure | Authorized release of information beyond its existing trust or domain boundary. |
| Ownership transfer | An accepted architectural change that moves canonical responsibility from one owner to another. |

### 4.2 Data classes

The system distinguishes these data classes:

| Data class | Typical canonical owner | Authority behavior |
| --- | --- | --- |
| Component operational state | Owning component contract | Mutated only through the owning component |
| User-controlled content | Component responsible for the user content domain, subject to user authority and policy | Exportable, correctable, restorable, and removable according to active contracts |
| Identity and trust state | Identity and Trust component | Other components consume verified identity assertions |
| Authorization and disclosure policy | Governance Policy Runtime and active policy artifacts | Policy decisions do not own governed application data |
| Resource state | Resource Governor | Resource decisions do not authorize business mutations |
| Release and activation state | Lifecycle and artifact authorities | Application components consume active release identity |
| Epistemic artifacts | Kristal artifact authority | Artifact identity remains separate from operational workflow state |
| Audit and transition evidence | Audit Broker or evidence registry | Evidence records transitions without becoming the source state |
| Profile deployment state | Active profile and deployment contracts | Physical controls remain scoped to the profile |
| Documentation authority | Canonical documentation registries | Product components do not redefine documentation authority |

### 4.3 Ownership dimensions

Data ownership includes several independent dimensions:

- semantic ownership;
- mutation ownership;
- schema ownership;
- identifier ownership;
- retention ownership;
- disclosure ownership;
- custody;
- encryption-key control;
- backup responsibility;
- recovery responsibility;
- portability and export responsibility;
- evidence responsibility.

One component can be the canonical semantic owner while another service acts as custodian, policy evaluator, backup operator, gateway, or evidence recorder. Those roles do not merge automatically.

### 4.4 Authoritative and derived state

A derived representation remains connected to its source through:

- canonical source identity;
- source version or compatibility range;
- derivation method;
- generation or synchronization status;
- purpose and authorized consumers;
- confidentiality and disclosure classification;
- invalidation and deletion behavior.

A derived store can be rebuilt without changing the authoritative owner. A result produced by an analytical tool becomes authoritative only when an owning component accepts it through an explicit import contract.

### 4.5 Logical and physical separation

Logical ownership is global. Physical separation is profile-dependent.

A lightweight profile can place multiple component schemas on one database server while preserving separate database roles, schemas, migrations, interfaces, and ownership.

A sovereign or high-assurance profile can require separate service identities, containers, volumes, databases, encryption domains, hosts, or networks.

Neither arrangement changes which component owns the data.

### 4.6 User authority

User authority is represented through active identity, consent, policy, and component contracts.

The system distinguishes:

- the user as subject or controller of eligible data;
- the component as canonical system owner of storage semantics and mutations;
- the operator as custodian;
- policy authorities as authorization and disclosure evaluators;
- gateways as controlled transfer mechanisms.

User authority does not permit bypassing component invariants. Component ownership does not eliminate user rights to authorized access, correction, export, restoration, deletion, recourse, or credible exit.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-DATA-001,REQ-SYS-DATA-002,REQ-SYS-DATA-003,REQ-SYS-DATA-004,REQ-SYS-DATA-005,REQ-SYS-DATA-006,REQ-SYS-DATA-007,REQ-SYS-DATA-008,REQ-SYS-DATA-009,REQ-SYS-DATA-010,REQ-SYS-DATA-011,REQ-SYS-DATA-012,REQ-SYS-DATA-013,REQ-SYS-DATA-014,REQ-SYS-DATA-015,REQ-SYS-DATA-016,REQ-SYS-DATA-017,REQ-SYS-DATA-018,REQ-SYS-DATA-019,REQ-SYS-DATA-020,REQ-SYS-DATA-021,REQ-SYS-DATA-022,REQ-SYS-DATA-023,REQ-SYS-DATA-024 -->
- **REQ-SYS-DATA-001 — SHALL:** Every authoritative data domain has exactly one declared canonical owner in an active registry or component contract.
- **REQ-SYS-DATA-002 — SHALL:** The canonical owner defines the accepted schema, identifiers, invariants, state transitions, mutation interface, compatibility rules, retention behavior, export behavior, and recovery behavior for its authoritative data.
- **REQ-SYS-DATA-003 — SHALL NOT:** A component, profile, integration, cache, index, replica, analytical store, generated projection, or AI context becomes authoritative solely because it contains a copy of data.
- **REQ-SYS-DATA-004 — SHALL NOT:** A component writes directly to another component's authoritative tables, private files, private queues, internal object namespaces, or private state.
- **REQ-SYS-DATA-005 — SHALL:** Every mutation of authoritative data is accepted, validated, and applied by the canonical owner through an active contract.
- **REQ-SYS-DATA-006 — SHALL:** Every authority-bearing mutation identifies the actor or initiating authority, subject, operation, contract version, authorization result, and mutation outcome.
- **REQ-SYS-DATA-007 — SHALL:** Derived data records its authoritative source, derivation purpose, generation or synchronization state, applicable scope, and invalidation behavior.
- **REQ-SYS-DATA-008 — SHALL NOT:** Derived data is used as a mutation path into authoritative state unless an explicit import contract causes the owning component to validate and accept the proposed change.
- **REQ-SYS-DATA-009 — SHALL:** A cache, index, replica, projection, or analytical copy is invalidated, rejected, rebuilt, or marked unavailable when its source identity, compatibility, or synchronization state cannot be established.
- **REQ-SYS-DATA-010 — SHALL:** Logical ownership remains unchanged when multiple components share a host, process runtime, database server, transport, object store, filesystem, backup system, or observability service.
- **REQ-SYS-DATA-011 — SHALL:** A deployment profile may strengthen physical separation, encryption, tenancy, locality, or replication controls without redefining global logical ownership.
- **REQ-SYS-DATA-012 — SHALL NOT:** A profile-specific storage topology, database technology, filesystem layout, container boundary, or service arrangement is represented as a universal system ownership rule.
- **REQ-SYS-DATA-013 — SHALL:** Cross-domain disclosure and publication pass through the Publication Gateway or another explicitly accepted disclosure contract with policy evaluation and required evidence.
- **REQ-SYS-DATA-014 — SHALL:** Publication of selected kOA Mediatheque records to an external UCKK Moodle destination require Publication Gateway authorization and UCKK Publication Bridge transport.
- **REQ-SYS-DATA-015 — SHALL:** The Governance Policy Runtime evaluates authorization, disclosure, and privilege policy without becoming the owner of the governed application data.
- **REQ-SYS-DATA-016 — SHALL:** The Resource Governor controls resource allocation, scheduling, and degradation without acquiring authority over application data, disclosure, or business state.
- **REQ-SYS-DATA-017 — SHALL NOT:** Kristal is used as a universal operational database, universal workflow state store, or replacement for component-owned authoritative data.
- **REQ-SYS-DATA-018 — SHALL:** SenTient operates only on authorized exports or active integration contracts, and its indexes, annotations, embeddings, and analytical results remain derived workbench data until accepted by an owning component.
- **REQ-SYS-DATA-019 — SHALL:** Evidence and receipts preserve the identity and outcome of critical transitions without granting the evidence system authority to rewrite the source transition.
- **REQ-SYS-DATA-020 — SHALL:** Deletion, retention, legal hold, correction, export, restoration, and credible-exit operations are executed by or coordinated with the canonical owner of each affected authoritative data domain.
- **REQ-SYS-DATA-021 — SHALL:** Backups and recovery copies preserve ownership boundaries, scope, version compatibility, confidentiality classification, and restoration order.
- **REQ-SYS-DATA-022 — SHALL:** When ownership, source identity, authorization, contract compatibility, or synchronization state is ambiguous, the affected mutation, disclosure, import, or conformance claim is blocked.
- **REQ-SYS-DATA-023 — SHALL:** A transfer of canonical ownership is activated atomically with an accepted decision, updated registry entries, migration procedure, compatibility rules, requirements, locks, tests, evidence, and rollback or forward-repair plan.
- **REQ-SYS-DATA-024 — SHALL:** Every active data-authority claim is traceable to an owning object, accepted decision, applicable requirements and locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a new authoritative data domain

The introducing change:

1. defines the data domain and its purpose;
2. identifies the canonical owner;
3. defines stable identifiers and schema authority;
4. defines accepted mutations and invariants;
5. defines query, event, export, import, and disclosure contracts;
6. defines retention, deletion, backup, restoration, and credible-exit behavior;
7. defines security classification and profile-dependent physical controls;
8. registers decisions, requirements, locks, tests, and evidence;
9. updates component and system registries;
10. activates the complete change atomically.

### 6.2 Mutating authoritative state

The owning component:

1. verifies actor or initiating authority;
2. resolves the active mutation contract;
3. verifies policy and subject scope;
4. validates schema, preconditions, compatibility, and replay constraints;
5. applies the state transition;
6. records the new state identity or version;
7. emits required events and evidence;
8. returns a deterministic result.

A custodian, gateway, policy service, cache, index, or analytical tool does not apply the mutation on behalf of the owner unless the active owning contract explicitly designates that execution path.

### 6.3 Producing derived data

The producing component or workbench:

1. resolves the authoritative source;
2. verifies access and purpose;
3. records the derivation metadata;
4. creates the derived representation;
5. prevents reverse mutation through the derived store;
6. monitors invalidation conditions;
7. rebuilds, quarantines, or removes invalid output when required.

### 6.4 Importing a proposed change

An import is treated as a proposal, not as authoritative state.

The owning component:

1. identifies the source and import contract;
2. verifies authenticity, authorization, compatibility, and provenance;
3. validates the proposed content against owner invariants;
4. resolves conflicts according to the active owner policy;
5. accepts or rejects the proposal;
6. records the outcome and evidence;
7. creates authoritative state only after acceptance.

### 6.5 Transferring canonical ownership

An ownership transfer:

1. records an accepted owner decision;
2. freezes incompatible mutations during the cutover window;
3. defines source and target ownership boundaries;
4. migrates data with verifiable completeness;
5. validates identifiers, invariants, retention, security, and compatibility;
6. switches active contracts and registry ownership atomically;
7. verifies rollback or forward repair;
8. prevents the predecessor from remaining a parallel writer;
9. retains historical lineage without retaining current authority.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Authority retained | Blocked action | Evidence |
| --- | --- | --- | --- | --- |
| Canonical owner cannot be resolved | Fail closed for affected state | Existing unaffected owners | Mutation, disclosure, import, or conformance claim | Ownership-resolution failure |
| Mutation contract is missing or incompatible | Reject before mutation | Current authoritative state | Requested transition | Contract-resolution failure |
| Actor or subject authorization is unavailable | Reject the governed action | Existing authorized local state | Mutation or disclosure requiring the decision | Authorization failure |
| Derived source is unknown or stale | Quarantine, invalidate, or rebuild | Authoritative source | Use of derived result as current state | Derivation-state evidence |
| Replica is behind or partitioned | Mark consistency state and restrict operations | Owner's authoritative state | Operations requiring unavailable consistency | Replication health record |
| Publication policy cannot be evaluated | Keep publication unavailable | Source-domain data | Cross-domain disclosure | Gateway or policy failure |
| kOA Mediatheque ingestion fails | Preserve source media and existing kOA Mediatheque state | Source and existing dimension | New ingestion transition | Failed-ingestion receipt |
| SenTient is unavailable | Keep analysis unavailable | All source components | SenTient analysis | Workbench health state |
| Backup compatibility is unknown | Do not restore into active authority | Current active state | Incompatible restore | Restore validation record |
| Ownership transfer is incomplete | Keep the cutover blocked or execute declared recovery | Last valid owner according to cutover state | Parallel writing or partial activation | Migration and cutover evidence |
| Retention or deletion scope is ambiguous | Block destructive action and resolve authority | Current data and legal controls | Deletion or irreversible transformation | Scope-resolution record |
| Evidence service is unavailable | Follow the transition contract's fail-closed or queued-evidence rule | Source component authority | Transition requiring synchronous evidence when mandated | Evidence-service health state |

## 8. Cross-Component Interactions

### 8.1 Permitted interaction forms

| Form | Data-authority effect |
| --- | --- |
| Query | Returns an authorized view without transferring ownership |
| Command | Requests the canonical owner to perform a transition |
| Event | Reports an occurred fact without granting source-state ownership |
| Export | Creates a controlled representation for a declared purpose |
| Import | Proposes data for validation and possible owner acceptance |
| Replication | Creates a consistency-managed copy without changing ownership |
| Projection | Creates a read model, index, catalog, or AI context |
| Gateway transfer | Crosses an explicit trust, disclosure, or ingestion boundary |
| Evidence submission | Records a transition without rewriting the source transition |

### 8.2 Gateway separation

The Publication Gateway controls disclosure outside an existing domain.

The UCKK Publication Bridge controls target-specific package creation, transport, retry, and destination receipt handling after Publication Gateway authorization.

A successful ingestion does not authorize publication. A successful publication does not transfer ownership of upstream authoritative data unless an accepted ownership-transfer contract says otherwise.

### 8.3 Governance and resource separation

The Governance Policy Runtime determines whether a governed action is authorized.

The Resource Governor determines whether resources are available and how work is scheduled or degraded.

Both can affect whether a transition proceeds. Neither replaces the canonical owner that validates and applies the transition.

### 8.4 Evidence separation

The Audit Broker and evidence systems can receive receipts and proofs from components. They preserve evidence integrity and authorized access.

They do not become writers to the originating component's authoritative state and do not change the outcome recorded by that component.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-SYS-DATA-001` | Establishes logical data ownership independently of profile-dependent physical isolation. |
| `DEC-SYS-DATA-002` | Establishes the authoritative, custodial, derived, and evidence data roles. |
| `DEC-SYS-DATA-003` | Establishes controlled export, import, replication, disclosure, and gateway behavior. |
| `DEC-SYS-DATA-004` | Establishes atomic canonical-ownership transfer and predecessor deactivation. |
| `DEC-SYS-GOV-001` | Separates Governance Policy Runtime authority from Resource Governor authority. |
| `DEC-UCKK-EXT-001` | Keeps disclosure authorization in Publication Gateway and UCKK-specific transport in the external integration. |
| `DEC-SYS-SENT-001` | Keeps SenTient optional, isolated, and non-authoritative. |
| `DEC-SYS-KRISTAL-001` | Keeps Kristal transversal without making it a universal operational store. |

### Prohibited assumptions

- physical custody implies semantic ownership;
- database administration implies ownership of application data;
- a shared database creates shared component ownership;
- an index or search result is authoritative because it is faster to query;
- an analytical result can update source state without owner acceptance;
- an AI-generated result is authoritative;
- backup data is automatically safe to restore into any release;
- a user export is a live authoritative replica;
- a policy service owns the data it governs;
- a resource service owns the work it schedules;
- a gateway owns the data it transfers;
- evidence can replace the source state;
- profile-specific storage isolation changes the global owner;
- replication permits multiple independent writers;
- an operational implementation can transfer ownership without an accepted decision;
- deletion can be performed safely when scope or authority is ambiguous.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-SYS-005` is active at `02-system/05-data-authority-and-ownership.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, decision source, and validation mapping.
5. All listed locks exist and are active.
6. Every authoritative data domain resolves to exactly one canonical owner.
7. Every component mutation path terminates at the owning component's active contract.
8. No component contract permits direct writes to another component's private authoritative state.
9. Every derived-data class declares source, purpose, synchronization state, and invalidation behavior.
10. No cache, index, replica, analytical store, AI context, export, or evidence record is classified as authoritative without an accepted ownership decision.
11. Profile contracts can strengthen physical controls without changing global logical ownership.
12. UCKK publication requires gateway authorization before bridge transport.
13. Resource Governor and Governance Policy Runtime remain separate.
14. SenTient remains optional, isolated, and non-authoritative.
15. Kristal is not assigned universal operational database or workflow ownership.
16. Every critical mutation, import, disclosure, activation, ownership transfer, deletion, and restoration maps to required tests and evidence.
17. Every ownership transfer prevents parallel active writers.
18. Backup and restore rules preserve ownership and compatibility.
19. Active prose is English and contains no unresolved-authority marker.
20. No normative keyword appears outside the generated requirements block.
21. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates one valid implementation. It does not redefine canonical ownership.

Konnaxion and Orgo can use separate schemas and database roles on the same PostgreSQL server in a lightweight profile. Each component owns its migrations and mutations. Sharing the server does not allow either component to write the other's tables.

> **Non-normative example:** This example illustrates one valid implementation. It does not redefine canonical ownership.

SenTient can receive an authorized export, build an index, and produce annotations. The index and annotations remain derived. An owning component can later accept selected results through an explicit import contract.

> **Non-normative example:** This example illustrates one valid implementation. It does not redefine canonical ownership.

A kOA Mediatheque thumbnail is derived from authoritative user media. The thumbnail can be deleted and rebuilt. It does not replace the original media or acquire independent publication permission.

> **Non-normative example:** This example illustrates one valid implementation. It does not redefine canonical ownership.

The Audit Broker can store a receipt that Orgo completed a critical transition. The receipt proves the reported outcome; it does not become Orgo's workflow state.

> **Non-normative example:** This example illustrates one valid implementation. It does not redefine canonical ownership.

A sovereign profile can place identity data, kOA Mediatheque data, and component operational data in separate encrypted volumes. A lightweight profile can use one encrypted volume with separate service identities and namespaces. The logical owners remain the same in both profiles.
