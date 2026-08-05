<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-010",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global",
    "profile_conditioned_conformance",
    "canonical_ownership"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/cross_component_communication",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/artifact-contracts/koa-media-record.schema.json",
    "contracts/artifact-contracts/uckk-publication-package.schema.json",
    "contracts/artifact-contracts/uckk-publication-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-REL-001",
    "DEC-DOC-CHANGE-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-CONF-OWN-001",
    "REQ-CONF-OWN-002",
    "REQ-CONF-OWN-003",
    "REQ-CONF-OWN-004",
    "REQ-CONF-OWN-005",
    "REQ-CONF-OWN-006",
    "REQ-CONF-OWN-007",
    "REQ-CONF-OWN-008",
    "REQ-CONF-OWN-009",
    "REQ-CONF-OWN-010",
    "REQ-CONF-OWN-011",
    "REQ-CONF-OWN-012",
    "REQ-CONF-OWN-013",
    "REQ-CONF-OWN-014",
    "REQ-CONF-OWN-015",
    "REQ-CONF-OWN-016",
    "REQ-CONF-OWN-017",
    "REQ-CONF-OWN-018",
    "REQ-CONF-OWN-019",
    "REQ-CONF-OWN-020",
    "REQ-CONF-OWN-021",
    "REQ-CONF-OWN-022",
    "REQ-CONF-OWN-023",
    "REQ-CONF-OWN-024",
    "REQ-CONF-OWN-025",
    "REQ-CONF-OWN-026",
    "REQ-CONF-OWN-027",
    "REQ-CONF-OWN-028",
    "REQ-CONF-OWN-029",
    "REQ-CONF-OWN-030",
    "REQ-CONF-OWN-031",
    "REQ-CONF-OWN-032",
    "REQ-CONF-OWN-033",
    "REQ-CONF-OWN-034",
    "REQ-CONF-OWN-035",
    "REQ-CONF-OWN-036",
    "REQ-CONF-OWN-037",
    "REQ-CONF-OWN-038",
    "REQ-CONF-OWN-039",
    "REQ-CONF-OWN-040",
    "REQ-CONF-OWN-041",
    "REQ-CONF-OWN-042",
    "REQ-CONF-OWN-043",
    "REQ-CONF-OWN-044",
    "REQ-CONF-OWN-045",
    "REQ-CONF-OWN-046",
    "REQ-CONF-OWN-047",
    "REQ-CONF-OWN-048"
  ],
  "lock_ids": [
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-015",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-IMPL-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-008",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-LIFE-015",
    "DOC-LIFE-019",
    "DOC-SEC-001",
    "DOC-SEC-009",
    "DOC-SEC-012",
    "DOC-OPS-000",
    "DOC-OPS-009"
  ],
  "tags": [
    "conformance",
    "canonical-ownership",
    "data-authority",
    "component-boundaries",
    "foreign-write-prohibition",
    "derived-data",
    "gateway-separation",
    "storage-identities",
    "migration",
    "backup",
    "restore",
    "runtime-validation",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Canonical Ownership Validation

## 1. Purpose

This document defines how kOA proves that canonical ownership and data-authority boundaries are both correctly declared and effectively enforced.

The constitutional rule is simple:

`text
one authoritative domain
 ↓
one active owning component
 ↓
registered owner-controlled operations
 ↓
enforced identities and storage boundaries
 ↓
observable state transitions
 ↓
tests and evidence
`

Conformance requires more than consistent documentation.

It requires proof that:

- every authoritative domain has one owner;
- no active ownership overlaps exist;
- foreign components cannot mutate the owner's source state;
- physical co-location does not erase logical boundaries;
- gateways, policy engines, resource controls, audit services, integrations, workbenches, backup systems, and operators remain within their declared authority;
- derived stores remain subordinate and rebuildable;
- migrations, backups, restores, and releases preserve ownership;
- profile-specific topology enforces the declared boundary;
- negative tests fail safely and leave state unchanged;
- evidence binds the exact tested release and environment.

A component is not ownership-conformant merely because its documentation states that it owns data.

The implementation, deployment, credentials, permissions, network routes, migrations, restore procedures, and runtime behavior must agree.

### 1.1 Validation objectives

Canonical ownership validation aims to detect:

1. duplicate owners;
2. ownerless authoritative domains;
3. undeclared mutation paths;
4. shared unrestricted credentials;
5. cross-component database writes;
6. foreign migration or restore writes;
7. derived-state authority drift;
8. gateway responsibility merging;
9. operator or tool authority expansion;
10. profile-specific isolation gaps;
11. integration and AI bypasses;
12. incomplete or false conformance evidence.

### 1.2 Conformance result

A canonical ownership result applies to one exact scope:

- component or component set;
- effective profile and overlays;
- Release Set;
- storage topology;
- identity and permission configuration;
- test catalog version;
- evidence set.

The result does not transfer automatically to another profile, release, topology, migration state, or environment.

## 2. Scope

### 2.1 Included objects

This document applies to:

- component identities;
- authoritative data domains;
- identifier namespaces;
- mutable object classes;
- component state transitions;
- databases and schemas;
- files and object stores;
- queues and streams;
- indexes, caches, and projections;
- APIs, commands, events, artifacts, exports, and imports;
- gateways;
- integrations and external AI;
- workbenches;
- migrations and forward repair;
- backups and restores;
- audit and evidence;
- release and profile validation.

### 2.2 Included validation layers

Ownership validation covers:

| Layer | Validation focus |
| --- | --- |
| Authority | Accepted decisions, registries, locks, requirements, and active versions |
| Contract | Owned domains, interfaces, states, failures, migrations, and non-responsibilities |
| Profile | Selected components, overlays, topology, storage, identities, and strengthening |
| Build | Source, configuration, schemas, migrations, and infrastructure definitions |
| Deployment | Service identities, credentials, permissions, routes, mounts, databases, and queues |
| Runtime | Permitted operations, denied foreign operations, state change, and receipts |
| Lifecycle | Artifacts, Release Sets, migrations, backup, restore, rollback, and retirement |
| Evidence | Test identity, environment, result, unchanged-state proof, and retained diagnostics |

### 2.3 Excluded detail

This document does not assign the fields, tables, database engines, storage paths, APIs, or exact permissions of a component.

Those facts belong to:

- `generated/component-catalog.json`;
- active component contracts;
- effective profiles;
- deployment manifests;
- data and security contracts;
- artifact and lifecycle contracts.

This document defines how those facts are validated.

### 2.4 Logical and physical ownership

Canonical ownership is logical.

A profile can place several components on:

- one node;
- one database server;
- one object-store service;
- one message broker;
- one backup platform;
- one orchestration system.

Co-location is conformant only when independently enforceable boundaries preserve each owner.

A profile can also distribute one component across several processes or nodes.

Distribution does not create several owners.

### 2.5 Historical sources

Historical documentation, migrations, exports, snapshots, and archived implementations can support investigation.

They do not override active ownership declarations.

## 3. Canonical References

### 3.1 Ownership authority

| Reference | Validation responsibility |
| --- | --- |
| `generated/authority-manifest.json` | Resolves the active authority set |
| `generated/decision-index.json` | Authorizes semantic ownership and boundary changes |
| `contracts/system.contract.json#/data_authority` | Declares global ownership principles |
| `contracts/system.contract.json#/global_boundaries` | Declares prohibited authority merges |
| `contracts/system.contract.json#/cross_component_communication` | Declares permitted interaction mechanisms |
| `generated/component-catalog.json` | Declares component identities and authoritative domains |
| `generated/component-catalog.json` | Declares active component-contract coverage |
| `contracts/components/*.component.json` | Declares operations, owned state, dependencies, failures, and compatibility |
| `generated/profile-catalog.json` | Declares active profiles and overlays |
| `contracts/profiles/*.profile.json` | Declares topology, storage, identities, and profile strengthening |
| `generated/requirements-index.json` | Owns canonical requirement text and scope |
| `generated/assertion-index.json` | Protects ownership and gateway relationships |
| `generated/traceability.json` | Links decisions, requirements, tests, and evidence |
| `generated/test-catalog.json` | Owns executable test definitions |
| `generated/evidence-catalog.json` | Owns evidence requirements |
| `generated/exception-index.json` | Owns bounded deviations |

### 3.2 Lifecycle and integrations

`text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/integration-types.contract.json
`

Lifecycle and integration validation must preserve component ownership.

### 3.3 Related documents

`text
01-constitution/08-data-authority-and-ownership.md
02-system/04-component-boundaries.md
02-system/05-data-authority.md
02-system/07-communication-model.md
02-system/09-ai-boundary.md
02-system/10-external-ai-surfaces.md
02-system/15-governance-policy-runtime.md
02-system/16-external-integrations.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/19-artifact-retention.md
07-security/01-security-baseline.md
07-security/09-storage-boundaries.md
07-security/12-external-integration-classification.md
08-operations/00-operating-model.md
08-operations/09-restore.md
`

## 4. Model and Responsibilities

### 4.1 Canonical owner

The canonical owner is the active component accountable for one authoritative domain.

The owner controls:

- accepted creation;
- accepted mutation;
- authoritative state transitions;
- domain identifiers;
- persistence semantics;
- deletion and retention;
- controlled export;
- controlled import;
- schema and compatibility;
- migration;
- backup and restore;
- critical transition evidence.

The owner is not inferred from:

- host administration;
- storage custody;
- backup custody;
- query frequency;
- user-interface presentation;
- transport;
- indexing;
- publication;
- policy evaluation;
- resource scheduling;
- audit;
- external processing.

### 4.2 Ownership declaration set

One ownership claim is complete only when these declarations agree:

1. accepted decision where semantic assignment was required;
2. system registry data-authority model;
3. component registry;
4. active component contract;
5. profile selection and topology;
6. requirements and locks;
7. traceability;
8. tests and evidence.

A mismatch creates an unresolved ownership state.

The validator does not guess which file is correct.

### 4.3 Authoritative-domain inventory

The validator builds an inventory of active domains.

Each inventory entry contains:

- domain identity;
- owner component;
- data or object class;
- identifier namespace;
- accepted mutation operations;
- storage identities;
- interfaces;
- events and artifacts;
- migration owner;
- backup and restore owner;
- profile applicability;
- prohibited overlaps;
- test and evidence references.

The inventory supports duplicate, gap, and overlap analysis.

### 4.4 Duplicate ownership

Duplicate ownership exists when two active components claim authority over the same semantic fact or mutation.

Overlap can occur even when storage is separate.

Examples include:

- two components creating the same canonical identifier;
- two components deciding final status for one object;
- one component editing another component's source record;
- two gateways deciding final publication state;
- an audit store treated as a second transaction source;
- a workbench directly updating runtime state.

Duplicate ownership blocks conformance.

### 4.5 Ownerless authority

Ownerless authority exists when mutable state affects system behavior but no active component contract owns it.

Examples include:

- configuration edited by operators without a registered owner;
- shared tables maintained by scripts;
- an integration callback that writes directly to storage;
- an undeclared queue consumer;
- a manually maintained mapping that drives authorization;
- an orphan migration.

Ownerless state blocks release or profile conformance.

### 4.6 Mutation-path inventory

The validator inventories all possible mutation paths, including:

- public and internal APIs;
- commands;
- event consumers;
- imports;
- file watchers;
- database clients;
- administrative scripts;
- migrations;
- restore utilities;
- privileged operations;
- integrations;
- background jobs;
- scheduled jobs;
- operator procedures;
- maintenance tools.

Every path resolves to an owner-controlled contract or remains prohibited.

### 4.7 Static validation

Static validation examines:

- source imports and client libraries;
- connection strings and secret references;
- database grants;
- schema ownership;
- file and volume mounts;
- queue and topic credentials;
- object-store permissions;
- network policies;
- service definitions;
- infrastructure code;
- migration files;
- backup and restore scripts;
- integration manifests;
- privileged-operation allowlists;
- documentation and generated catalogs.

Static validation identifies possible paths.

Runtime validation proves enforcement.

### 4.8 Runtime positive tests

Positive tests exercise owner-authorized behavior.

A positive test confirms:

- correct caller identity;
- correct target owner;
- accepted operation;
- valid state transition;
- expected authoritative mutation;
- expected event or receipt;
- no foreign mutation;
- stable identifiers;
- correct profile behavior.

Positive tests prove that enforcing isolation did not break the owner's legitimate capability.

### 4.9 Runtime negative tests

Negative tests attempt prohibited behavior.

Examples include:

- direct foreign database write;
- use of another component's credentials;
- foreign queue publication or consumption;
- foreign object-store write;
- bypassing an import interface;
- using an audit record as application source;
- bypassing Publication Gateway;
- writing directly to an external UCKK Moodle database or managed storage;
- external AI direct adoption;
- cross-tenant mutation;
- migration by the wrong owner;
- restore into the wrong domain.

A passing negative test proves:

- denial;
- stable failure classification;
- authoritative state unchanged;
- no partial side effect;
- required evidence produced.

### 4.10 Unchanged-state proof

A prohibited-operation test needs evidence that state remained unchanged.

Evidence can use:

- owner-controlled before-and-after version;
- transaction or sequence identity;
- immutable state receipt;
- bounded authoritative query;
- owner-produced state digest where the component contract defines one;
- event absence plus state verification;
- rollback-free clean fixture reset.

The conformance system does not invent a universal content-hash requirement for ordinary documentation or arbitrary state.

The owning contract defines the appropriate state-verification method.

### 4.11 Service and workload identities

Each component uses a distinct runtime identity.

Validation checks:

- service account;
- workload identity;
- process identity;
- container identity;
- database user;
- queue identity;
- object-store identity;
- secret scope;
- network identity;
- certificate or token audience;
- environment separation.

A shared host administrator can manage infrastructure.

That administrator is not the normal component identity.

### 4.12 Database and storage identity

Database validation checks:

- database or instance;
- schema;
- owner;
- grants;
- migration user;
- runtime user;
- backup user;
- restore user;
- read-only consumers;
- cross-schema access;
- administrative exceptions.

Storage validation checks equivalent boundaries for:

- files;
- volumes;
- objects;
- buckets;
- prefixes;
- keys;
- mounts;
- snapshots;
- archives.

### 4.13 Profile-conditioned storage

Profiles can implement ownership differently.

#### Lightweight profile

Several components can share one host and database process.

Separate database users, schemas, credentials, interfaces, and migration ownership remain required.

#### Developer profiles

Each workspace separates databases, ports, services, secrets, volumes, and caches.

A developer's broad local access does not support a production ownership claim.

#### Build farm

Jobs use isolated mutable state and do not receive production data or foreign component credentials.

#### Sovereign profiles

Stronger storage identities, encrypted durable state, local backup, recovery, and preferably separate database instances protect ownership.

#### High assurance

The overlay can require stronger physical separation, review, control separation, and evidence.

#### Sovereign offline

All ownership and restore controls remain locally enforceable without remote services.

### 4.14 Derived-state inventory

Every derived representation declares:

- derived-state identity;
- operator;
- authoritative source;
- source contract;
- update mechanism;
- freshness;
- invalidation;
- rebuild;
- read consumers;
- retention;
- failure behavior.

The validator proves that removing the derived representation does not remove source authority.

### 4.15 Replicas and read models

A replica or read model can support availability and performance.

It remains non-authoritative unless an accepted component contract defines a controlled replicated-authority model.

Validation checks:

- source identity;
- replication direction;
- lag;
- write prohibition;
- conflict behavior;
- failover authority;
- resynchronization;
- promotion controls.

A read replica cannot accept writes merely because the primary is unavailable.

### 4.16 Events and messages

An event represents an owner-produced fact or state transition.

Validation checks:

- producer ownership;
- schema version;
- event identity;
- source object;
- ordering;
- idempotency;
- tenant or domain;
- consumer permissions;
- replay;
- failure and dead-letter behavior.

A consumer can update its own state in response.

It cannot rewrite the producer's state outside a registered owner interface.

### 4.17 Artifacts and exports

Artifacts and exports carry data across boundaries.

Validation checks:

- source owner;
- artifact class;
- identity;
- provenance;
- audience;
- destination;
- rights and consent;
- compatibility;
- import owner;
- lifecycle state.

Possession of an export does not transfer authority unless a controlled import and accepted ownership transfer explicitly occur.

### 4.18 Integrations and candidate inputs

External integrations and workbenches return untrusted or candidate material.

Validation proves:

- explicit source export;
- minimized transfer;
- no foreign credentials;
- candidate identity;
- provenance;
- destination import;
- review;
- acceptance or rejection;
- no direct source or destination write.

External AI cannot become a hidden mutation client.

### 4.19 Publication Gateway

Publication Gateway owns execution of approved cross-domain publication.

Validation proves that it:

- receives an owner-authorized representation;
- receives policy or consent decisions where required;
- does not decide source truth;
- does not edit source storage;
- transports only approved fields;
- produces publication results and receipts;
- leaves source ownership unchanged.

### 4.20 kOA Mediatheque and UCKK Publication Bridge

kOA Mediatheque owns local media records, file versions, managed local content references, hashes, collections, dimensions, tags, relationships, rights, restrictions, provenance, renditions, lifecycle state, import and export history, and local backup and restore state.

Validation proves that kOA Mediatheque:

- remains usable without UCKK or another remote platform;
- uses owner-controlled local operations and identities;
- performs deterministic local processing for selected capabilities;
- treats XLSX, AI services, and publication targets as interfaces rather than authoritative stores;
- preserves local ownership when an object is exported or published.

The optional UCKK Publication Bridge owns only target-specific Moodle packaging, transport, result handling, and receipt production after an explicit Publication Gateway authorization. The separate UCKK Import Bridge owns retrieval and quarantine transport state; kOA Mediatheque owns local acceptance and separate local identities.

Validation proves that the adapter:

- accepts only an explicitly selected owner-authorized representation;
- verifies rights, restrictions, destination, manifest, and policy inputs;
- calls a declared external UCKK interface;
- records external acceptance or rejection;
- does not write directly to UCKK database tables or managed storage;
- does not own or mutate the source kOA Mediatheque record;
- is not required for local or offline Mediatheque operation;
- does not create background bidirectional synchronization.

### 4.21 Governance Policy Runtime

Governance Policy Runtime owns policy evaluation state and decision receipts.

Validation proves that it does not own:

- application objects;
- identities;
- resource allocation;
- privileged execution;
- publication transport;
- release activation;
- external AI output.

A caller enforces the decision and owns its resulting application state.

### 4.22 Resource Governor

Resource Governor owns resource policy execution.

Validation proves that it can:

- admit;
- defer;
- throttle;
- schedule;
- stop;
- report resource state.

It cannot:

- authorize application actions;
- grant privilege;
- decide disclosure;
- alter application records;
- publish;
- select release authority.

### 4.23 Audit Broker

Audit Broker owns selected evidence handling.

Validation proves that:

- payloads are minimized;
- evidence classes remain separate;
- foreign application data is not replicated without contract;
- receipts remain references or bounded representations;
- audit access is controlled;
- audit loss does not silently mutate application state.

### 4.24 Operators and privileged tools

Operators can perform infrastructure or lifecycle work through bounded authority.

Validation checks:

- role scope;
- temporary privilege;
- operation schema;
- owner authorization;
- before-and-after state;
- receipts;
- closure.

Root, database administrator, backup administrator, and storage administrator access do not become normal application mutation paths.

### 4.25 Migrations

Migration validation examines:

- migration owner;
- source and target versions;
- exact storage scope;
- runtime and migration identities;
- preconditions;
- backup or checkpoint;
- ordering;
- interruption;
- idempotency;
- rollback boundary;
- forward repair;
- tests;
- evidence.

A central orchestrator can sequence migrations.

Each component remains responsible for its own mutation.

### 4.26 Backup

Backup validation proves that backup capture preserves:

- component owner;
- tenant or domain;
- artifact and Release Set identity;
- encryption;
- retention;
- schema and migration state;
- recovery metadata;
- access controls.

Backup operators cannot alter the semantic ownership of captured data.

### 4.27 Restore

Restore validation proves that:

- the target is clean and compatible;
- the owning component restores its state;
- foreign components cannot inject records;
- tenant and domain boundaries remain intact;
- migrations use owner contracts;
- derived state is rebuilt;
- readiness and critical workflows pass;
- normal traffic remains blocked until acceptance.

### 4.28 Release Set validation

Ownership conformance applies to the exact Release Set.

Validation resolves:

- component-contract versions;
- profile versions;
- system artifacts;
- service artifacts;
- governance artifacts;
- knowledge artifacts;
- migrations;
- integrations;
- trust and policy;
- evidence.

A component can pass individually while the combined Release Set fails because topology or permissions introduce an ownership conflict.

### 4.29 Exception validation

An ownership exception is allowed only when the active exception registry permits it.

The validator checks:

- exact requirement;
- exact component and domain;
- profile;
- duration;
- reason;
- compensating control;
- owner;
- tests;
- evidence;
- closure.

A permanent undocumented shared write is not an exception.

### 4.30 Drift validation

Runtime drift detection compares actual state to active contracts.

Drift sources include:

- grants;
- credentials;
- mounts;
- service identities;
- network routes;
- queue permissions;
- migration users;
- backup access;
- restore access;
- integration endpoints;
- privileged allowlists;
- configuration;
- profile composition.

Drift remains nonconformant until removed or accepted through the change protocol.

### 4.31 Evidence model

Ownership evidence can include:

- registry-validation report;
- domain inventory;
- duplicate and gap report;
- permission inventory;
- network-flow inventory;
- static-analysis report;
- deployment-manifest report;
- positive operation result;
- negative mutation result;
- unchanged-state proof;
- migration test;
- backup and restore test;
- profile composition report;
- Release Set report;
- exception report;
- drift report.

Evidence remains tied to exact identities and versions.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-OWN-001,REQ-CONF-OWN-002,REQ-CONF-OWN-003,REQ-CONF-OWN-004,REQ-CONF-OWN-005,REQ-CONF-OWN-006,REQ-CONF-OWN-007,REQ-CONF-OWN-008,REQ-CONF-OWN-009,REQ-CONF-OWN-010,REQ-CONF-OWN-011,REQ-CONF-OWN-012,REQ-CONF-OWN-013,REQ-CONF-OWN-014,REQ-CONF-OWN-015,REQ-CONF-OWN-016,REQ-CONF-OWN-017,REQ-CONF-OWN-018,REQ-CONF-OWN-019,REQ-CONF-OWN-020,REQ-CONF-OWN-021,REQ-CONF-OWN-022,REQ-CONF-OWN-023,REQ-CONF-OWN-024,REQ-CONF-OWN-025,REQ-CONF-OWN-026,REQ-CONF-OWN-027,REQ-CONF-OWN-028,REQ-CONF-OWN-029,REQ-CONF-OWN-030,REQ-CONF-OWN-031,REQ-CONF-OWN-032,REQ-CONF-OWN-033,REQ-CONF-OWN-034,REQ-CONF-OWN-035,REQ-CONF-OWN-036,REQ-CONF-OWN-037,REQ-CONF-OWN-038,REQ-CONF-OWN-039,REQ-CONF-OWN-040,REQ-CONF-OWN-041,REQ-CONF-OWN-042,REQ-CONF-OWN-043,REQ-CONF-OWN-044,REQ-CONF-OWN-045,REQ-CONF-OWN-046,REQ-CONF-OWN-047,REQ-CONF-OWN-048 -->
- **REQ-CONF-OWN-001 — SHALL:** Every authoritative data domain resolve to exactly one active owning component.
- **REQ-CONF-OWN-002 — SHALL:** Every ownership declaration resolve consistently across the system registry, component registry, active component contract, profile composition, requirements, locks, and traceability.
- **REQ-CONF-OWN-003 — SHALL NOT:** Two active components declare overlapping authoritative ownership of the same fact, identifier namespace, mutable object class, state transition, or storage boundary.
- **REQ-CONF-OWN-004 — SHALL:** Every active component contract identify its owned authoritative domains, permitted derived domains, permitted foreign references, and prohibited foreign mutations.
- **REQ-CONF-OWN-005 — SHALL:** Every authoritative mutation operation resolve to a registered interface, command, event-consumer transition, controlled import, migration, restore, or lifecycle operation owned by the target component.
- **REQ-CONF-OWN-006 — SHALL NOT:** A component, operator, workbench, integration, gateway, audit service, backup service, migration orchestrator, or external AI surface write directly to another component's authoritative source tables or equivalent mutable source state.
- **REQ-CONF-OWN-007 — SHALL:** Static validation inspect source, configuration, schemas, migrations, infrastructure definitions, credentials, permissions, network policy, and deployment manifests for undeclared foreign-write paths.
- **REQ-CONF-OWN-008 — SHALL:** Runtime validation demonstrate that unauthorized foreign mutation attempts are denied, leave authoritative state unchanged, and produce the required failure evidence.
- **REQ-CONF-OWN-009 — SHALL:** Every permitted cross-component state-changing interaction preserve the identity of the requesting component, target owner, actor, tenant or security domain, purpose, operation, correlation, and terminal result.
- **REQ-CONF-OWN-010 — SHALL:** Every component use a distinct service or workload identity for authoritative operations.
- **REQ-CONF-OWN-011 — SHALL:** Every component use storage, database, schema, queue, index, object-store, file-store, or credential identities scoped to its declared ownership and profile.
- **REQ-CONF-OWN-012 — SHALL NOT:** A shared administrator, shared database owner, shared root credential, shared writable volume, shared queue credential, or shared unrestricted service account support an ownership-conformance claim.
- **REQ-CONF-OWN-013 — SHALL:** Physical co-location preserve logical ownership through independently enforceable identities, permissions, interfaces, migrations, backups, restores, and evidence.
- **REQ-CONF-OWN-014 — SHALL:** Sovereign and high-assurance profiles use the storage and database separation required by their profile contracts and prefer separate database instances where declared.
- **REQ-CONF-OWN-015 — SHALL:** Every derived cache, index, replica, projection, report, analytics store, rendered output, or generated view identify its authoritative source, owner, refresh rule, invalidation rule, rebuild rule, and permitted consumers.
- **REQ-CONF-OWN-016 — SHALL NOT:** A derived representation become authoritative because it is faster, more available, more searchable, externally hosted, retained longer, or used by more consumers.
- **REQ-CONF-OWN-017 — SHALL:** Loss or corruption of derived state be recoverable from the owning authoritative source without transferring ownership to the derived-state operator.
- **REQ-CONF-OWN-018 — SHALL:** Every event, message, artifact, or export that conveys component-owned facts declare source ownership, schema or contract version, identity, ordering or idempotency behavior, and consumer authority.
- **REQ-CONF-OWN-019 — SHALL NOT:** Delivery of an event, message, artifact, export, or receipt grant the consumer authority to rewrite the source component's state.
- **REQ-CONF-OWN-020 — SHALL:** Every imported candidate or external result enter through the destination component's controlled import and acceptance boundary.
- **REQ-CONF-OWN-021 — SHALL NOT:** ChatGPT, Suno, Gamma, Ariane external voice, SenTient, another integration, or another workbench directly mutate canonical component state.
- **REQ-CONF-OWN-022 — SHALL:** Publication Gateway validation demonstrate that it transports only an owner-authorized representation and does not own or mutate source component data.
- **REQ-CONF-OWN-023 — SHALL:** kOA Mediatheque validation demonstrate exclusive ownership of local media records and managed local content state, deterministic local operation, and independence from UCKK availability.
- **REQ-CONF-OWN-024 — SHALL:** Publication Gateway and the UCKK Publication Bridge remain separately identifiable, separately authorized, separately testable, and non-substitutable; the adapter SHALL NOT bypass disclosure authorization, write directly to Moodle storage, or transfer ownership of the local source record.
- **REQ-CONF-OWN-025 — SHALL:** Governance Policy Runtime validation demonstrate that policy evaluation does not mutate application data, allocate resources, publish content, issue identities, or execute privileged operations.
- **REQ-CONF-OWN-026 — SHALL:** Resource Governor validation demonstrate that resource admission and scheduling do not create application, policy, publication, identity, or data authority.
- **REQ-CONF-OWN-027 — SHALL:** Audit Broker validation demonstrate that receipts and evidence remain records of bounded events rather than replacement application databases or unrestricted replicas.
- **REQ-CONF-OWN-028 — SHALL NOT:** A receipt, audit record, log, trace, report, backup catalog, or observability store be used as the authoritative source of an application fact unless an accepted decision explicitly assigns that artifact class and owner.
- **REQ-CONF-OWN-029 — SHALL:** Every migration identify one owning component, source state, target state, storage scope, version path, backup or checkpoint, rollback boundary, forward-repair behavior, tests, and evidence.
- **REQ-CONF-OWN-030 — SHALL NOT:** A central migration tool or operator rewrite foreign component state outside the owning component's migration contract.
- **REQ-CONF-OWN-031 — SHALL:** Every backup preserve component, tenant, security-domain, Release Set, encryption, retention, and ownership boundaries.
- **REQ-CONF-OWN-032 — SHALL:** Every restore prove that each component accepts its restored state through its own restore and migration contracts.
- **REQ-CONF-OWN-033 — SHALL NOT:** A backup, archive, replica, export, audit store, or derived index become the authoritative source merely because the original owner is unavailable.
- **REQ-CONF-OWN-034 — SHALL:** Tenant-scoped and security-domain-scoped tests prove that foreign tenants and domains remain unreadable and unmodifiable through every component, gateway, migration, backup, restore, and integration path.
- **REQ-CONF-OWN-035 — SHALL:** Every ownership-conformance test bind the exact profile, overlays, Release Set, component contracts, storage topology, identities, permissions, test vector, terminal result, and evidence.
- **REQ-CONF-OWN-036 — SHALL:** Profile-conditioned conformance evaluate the effective composed profile rather than testing a component or profile document in isolation.
- **REQ-CONF-OWN-037 — SHALL NOT:** Passing a lightweight, developer, build-farm, control-plane, sovereign, offline, or high-assurance topology imply ownership conformance for another profile.
- **REQ-CONF-OWN-038 — SHALL:** Ownership validation include positive tests for permitted owner operations and negative tests for prohibited foreign reads, writes, migrations, restores, privilege paths, and bypasses.
- **REQ-CONF-OWN-039 — SHALL:** Ownership validation include static contract checks, deployment checks, permission checks, runtime probes, mutation tests, reconciliation checks, and recovery checks applicable to the profile.
- **REQ-CONF-OWN-040 — SHALL NOT:** A skipped, unavailable, blocked, incomplete, stale, inferred, or manually asserted ownership test be represented as passing.
- **REQ-CONF-OWN-041 — SHALL:** Every release-blocking ownership requirement have valid evidence for the exact candidate Release Set and target profile.
- **REQ-CONF-OWN-042 — SHALL:** A failed ownership test block the affected component, profile, artifact, migration, restore, integration, or Release Set conformance claim.
- **REQ-CONF-OWN-043 — SHALL:** Ownership exceptions identify the exact requirement, component, data domain, profile, duration, reason, compensating controls, tests, evidence, and closure condition.
- **REQ-CONF-OWN-044 — SHALL NOT:** An exception redefine canonical ownership, authorize an undeclared permanent foreign-write path, or survive beyond its registered scope and validity.
- **REQ-CONF-OWN-045 — SHALL:** Ownership drift detection compare active runtime identities, permissions, routes, storage mappings, database grants, migrations, and interfaces against the active contracts.
- **REQ-CONF-OWN-046 — SHALL:** Detected ownership drift enter a blocked or degraded conformance state until reconciled through an accepted change or restored canonical configuration.
- **REQ-CONF-OWN-047 — SHALL:** Ownership evidence preserve enough detail to reproduce the tested topology and verify that authoritative state remained unchanged during prohibited-operation tests.
- **REQ-CONF-OWN-048 — SHALL:** A semantic change to ownership, authoritative domains, identifiers, storage identities, cross-component mutation, gateways, migrations, backup, restore, derived state, or ownership validation use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Build the canonical ownership inventory

1. Resolve the active authority registry.
2. resolve accepted ownership decisions.
3. enumerate active components.
4. enumerate authoritative domains and identifier namespaces.
5. resolve active component contracts.
6. resolve effective profiles and overlays.
7. resolve storage and runtime identities.
8. resolve migration, backup, restore, gateway, integration, and derived-state declarations.
9. link requirements, locks, tests, and evidence.
10. report duplicate, missing, inconsistent, and unresolved declarations.
11. block validation when ownership cannot be resolved uniquely.

### 6.2 Validate one component statically

1. Select the component, profile, and Release Set.
2. resolve owned domains and non-responsibilities.
3. enumerate source and runtime dependencies.
4. inspect database and storage clients.
5. inspect migrations and restore tools.
6. inspect service identities and secret references.
7. inspect queues, events, APIs, files, and object stores.
8. inspect network and deployment configuration.
9. identify every mutation path.
10. classify each path as owner-controlled or prohibited.
11. produce the static validation report.

### 6.3 Validate deployment identities and permissions

1. Inventory service and workload identities.
2. inventory database users and grants.
3. inventory schema ownership.
4. inventory volumes, buckets, objects, and file permissions.
5. inventory queue and stream permissions.
6. inventory network routes and endpoints.
7. inventory secret scopes.
8. compare actual state with component and profile contracts.
9. test prohibited credential use.
10. record mismatches and drift.
11. block readiness for unresolved broad access.

### 6.4 Run positive ownership tests

1. Provision isolated test state.
2. identify the owner component and authorized caller.
3. invoke the registered owner operation.
4. verify the expected state transition.
5. verify stable identifiers and tenant or domain scope.
6. verify expected event or receipt.
7. verify no foreign domain changed.
8. bind result to component, profile, Release Set, test, and evidence.
9. clean the test fixture through the owner contract.

### 6.5 Run negative foreign-write tests

1. Create a controlled source state and before-state proof.
2. select a prohibited caller or path.
3. attempt the foreign mutation.
4. verify denial and stable failure code.
5. verify no partial side effect.
6. verify authoritative state unchanged.
7. verify required security or audit evidence.
8. verify no retry or alternate path bypassed the denial.
9. retain diagnostics.
10. restore the fixture only through the owner contract.

### 6.6 Validate derived state

1. Identify the derived representation.
2. resolve the authoritative source and owner.
3. verify one-way update authority.
4. verify write prohibition or controlled feedback contract.
5. corrupt or remove the derived state in an isolated test.
6. rebuild from the authoritative source.
7. verify consumers do not treat the derived store as source truth.
8. verify retention and failure behavior.
9. record rebuild and authority evidence.

### 6.7 Validate a gateway

1. Resolve gateway identity and contract.
2. resolve source and destination owners.
3. validate permitted inputs and outputs.
4. validate policy and consent dependencies.
5. test accepted operation.
6. test direct source or destination write denial.
7. test responsibility-separation locks.
8. verify terminal receipts.
9. verify failure leaves owner state consistent.
10. bind results to the effective profile and Release Set.

### 6.8 Validate migration ownership

1. Select component, source version, target version, and profile.
2. verify migration identity and owner.
3. verify storage scope and credentials.
4. verify backup or checkpoint.
5. execute migration through the owner contract.
6. attempt foreign migration access.
7. verify denial and unchanged foreign state.
8. test rollback boundary or forward repair.
9. verify readiness.
10. retain migration evidence.

### 6.9 Validate backup and restore ownership

1. Select component or tenant scope.
2. verify backup inventory and ownership metadata.
3. provision a clean compatible target.
4. restore through the owning component contract.
5. verify tenant, domain, encryption, Release Set, and migration state.
6. verify foreign data remains inaccessible and unchanged.
7. rebuild derived state.
8. run owner and cross-component acceptance.
9. retain restore evidence.
10. remove temporary recovery authority.

### 6.10 Validate a profile composition

1. Resolve the primary profile and overlays.
2. enumerate selected components.
3. resolve storage topology and identities.
4. resolve profile-specific strengthening.
5. run static ownership checks.
6. run deployment permission checks.
7. run positive and negative runtime tests.
8. run migration and restore tests applicable to the profile.
9. validate integrations and gateways.
10. produce one profile-scoped ownership result.

### 6.11 Validate a Release Set candidate

1. Resolve all four release channels.
2. resolve component and profile contracts.
3. resolve migrations, integrations, and storage topology.
4. run ownership inventory validation.
5. run release-blocking static and runtime tests.
6. resolve exceptions.
7. verify evidence completeness.
8. reject false or incomplete passes.
9. mark the candidate ownership-conformant only when all required controls pass.
10. attach the result to the exact Release Set candidate.

### 6.12 Respond to ownership drift

1. Detect and record the drift.
2. identify affected component, domain, profile, and Release Set.
3. block or degrade affected conformance claims.
4. revoke broad credentials or routes when safe.
5. preserve evidence.
6. restore canonical configuration or create an accepted change.
7. rerun affected tests.
8. verify no unauthorized mutation occurred.
9. update evidence and final disposition.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved state | Blocked claim or transition |
| --- | --- | --- | --- |
| Domain has no owner | Mark authority unresolved | Existing known-good authority | Component and Release Set conformance |
| Domain has multiple owners | Reject ownership model | Existing active release where safe | New release or profile activation |
| Component contract omits owned domains | Block component conformance | Existing runtime state | New component claim |
| Registry and contract disagree | Report conflict without guessing | Existing active authority | Affected validation |
| Undeclared foreign database grant exists | Revoke or isolate and investigate | Owner state where uncompromised | Deployment conformance |
| Shared unrestricted credential exists | Replace with scoped identities | Existing data and diagnostics | Ownership claim |
| Direct foreign mutation succeeds | Open security and data-integrity incident | Unaffected domains and evidence | Release, profile, and component conformance |
| Prohibited mutation is denied but state changes | Treat as failed control | Before-state evidence and unaffected state | Conformance |
| Unchanged-state proof is unavailable | Mark negative test incomplete | Test diagnostics | Passing result |
| Derived store cannot rebuild | Mark dependent capability degraded | Authoritative source | Derived-state conformance |
| Derived store accepts authoritative writes | Block and isolate path | Source authority | Component and topology conformance |
| Event producer ownership is unresolved | Block event consumption for authority-sensitive paths | Existing owner state | Event conformance |
| Candidate import bypasses destination owner | Reject candidate and investigate | Previous destination state | Adoption |
| Gateway responsibilities overlap | Block affected gateway or profile claim | Source and destination state | Release activation |
| Policy runtime mutates application state | Isolate path and open incident | Unaffected components | Governance conformance |
| Resource scheduler grants application authority | Reject design or deployment | Existing resource state | Resource conformance |
| Audit store is used as application source | Stop path and reconcile owner state | Evidence and true source | Application conformance |
| Migration owner is unresolved | Block migration | Source state and backup | Activation |
| Restore writes through the wrong owner | Stop restore and restart from clean state | Recovery source and unrelated domains | Restore acceptance |
| Cross-tenant access succeeds | Isolate affected environment and open incident | Unaffected tenants and evidence | Profile and security conformance |
| Required test is unavailable or skipped | Mark validation blocked | Existing known-good result | New passing claim |
| Evidence is incomplete | Keep result nonconformant | Diagnostics | Release-blocking claim |
| Exception is expired or too broad | Remove exception authority | Underlying requirement | Continued deviation |
| Runtime drift exists | Mark affected state degraded or blocked | Existing known-good configuration | New conformance claim |
| Complete validation cannot execute | Preserve previous valid authority | Existing release | New ownership-conformance claim |

Failure remains scoped where possible.

A failure does not authorize a shared owner, direct write, emergency migration bypass, silent gateway substitution, AI adoption, or unsupported pass result.

## 8. Cross-Component Interactions

### 8.1 Component registry and contracts

The component registry supplies the active ownership inventory.

Component contracts supply observable operations and state boundaries.

Conformance validates consistency and enforcement without creating new ownership.

### 8.2 Profiles

Profiles determine how ownership is enforced in one topology.

A lightweight profile can use logical separation inside shared infrastructure.

A sovereign or high-assurance profile can require stronger service and storage separation.

The same ownership rule remains global.

### 8.3 Identity and Trust

Identity and Trust supplies verifiable component, workload, operator, signer, and artifact identities.

Ownership validation tests the scope and use of those identities.

Identity does not replace component authorization.

### 8.4 Governance Policy Runtime

Governance Policy Runtime can decide whether a caller may request an operation.

The target component remains the mutation owner.

Conformance tests both policy enforcement and the absence of policy-engine application writes.

### 8.5 Resource Governor

Resource Governor can admit or stop workloads.

It cannot decide or execute component mutations.

Conformance tests that resource-control paths remain authority-neutral.

### 8.6 kOA Node Agent

kOA Node Agent can coordinate closed privileged operations.

Ownership validation checks that privileged operations affect only declared infrastructure or owner-authorized lifecycle state.

It cannot become an arbitrary database or application mutation path.

### 8.7 Audit Broker

Audit Broker receives selected evidence.

Conformance checks evidence minimization, access controls, and non-authoritative status.

### 8.8 Publication Gateway

Publication Gateway transports approved representations.

Conformance checks source ownership, disclosure authority, field minimization, destination, and publication receipts.

### 8.9 kOA Mediatheque and UCKK publication

kOA Mediatheque owns local media records and managed local content state.

Conformance checks deterministic local operation, owner-controlled mutations, backup and restore ownership, and continued availability without UCKK.

When UCKK publication is selected, conformance checks explicit source selection, Publication Gateway authorization, target-specific adapter behavior, external result receipts, no direct Moodle database or storage writes, and no transfer of local source authority.

### 8.10 Integrations and workbenches

Integrations, external AI, and SenTient produce candidates or bounded results.

Conformance checks controlled export, provenance, controlled import, destination acceptance, and no direct canonical mutation.

### 8.11 Lifecycle and operations

Lifecycle validation preserves ownership through:

- build;
- publication;
- activation;
- migration;
- rollback;
- backup;
- restore;
- retention;
- retirement.

Operations execute owner-controlled procedures and provide runtime evidence.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-DATA-001` | Every authoritative domain has one owner and direct foreign source writes are prohibited |
| `DEC-GATE-001` | Publication Gateway authorization and destination-specific transport remain separate |
| `DEC-MEDIATHEQUE-001` | kOA Mediatheque is the internal local media authority |
| `DEC-UCKK-EXT-001` | UCKK is an external online Moodle platform reached through optional controlled directional adapters |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor remain separate authorities |
| `DEC-PROFILE-001` | Profiles alter topology and strengthening without transferring ownership |
| `DEC-AI-001` | External AI remains optional, non-authoritative, and unable to write canonical state |
| `DEC-SENT-001` | SenTient remains an optional isolated candidate-producing workbench |
| `DEC-REL-001` | Ownership conformance applies to exact compatible Release Sets across four channels |
| `DEC-DOC-CHANGE-001` | Semantic ownership changes require accepted decisions and transitive impact analysis |

### 9.2 Protected locks

| Lock | Protected ownership relationship |
| --- | --- |
| `LOCK-DATA-001` | No direct cross-component authoritative write |
| `LOCK-GATE-001` | Publication authorization and destination-specific transport remain separate |
| `LOCK-MEDIATHEQUE-001` | kOA Mediatheque retains local media ownership and offline independence |
| `LOCK-UCKK-EXT-001` | UCKK publication is explicit, optional, receipted, and does not merge Mediatheque authorities |
| `LOCK-GOV-001` | Policy and resource authority remain separate |
| `LOCK-PROFILE-001` | Profile topology does not transfer ownership |
| `LOCK-AI-001`, `LOCK-AI-002` | AI cannot become native or authoritative |
| `LOCK-SENT-001` | SenTient remains optional and non-authoritative |
| `LOCK-COMP-001` | Kristal identity remains separate from tenant workflow and UI ownership |
| `LOCK-COMP-002` | Language construction remains separate from runtime consumption |
| `LOCK-LIFE-001` to `LOCK-LIFE-004` | Partial activation, recovery, Release Sets, and channels preserve ownership |
| `LOCK-DOC-015`, `LOCK-DOC-020` | Major changes receive complete impact and clean validation |
| `LOCK-DOC-019` | Retired identifiers remain reserved |
| `LOCK-IMPL-001` | Implementation and recipes do not create ownership |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- a component owns data because it hosts the database;
- a database administrator owns every schema;
- a backup operator owns restored records;
- a user interface owns the objects it displays;
- a search index is authoritative because users query it;
- a read replica can accept writes during an outage;
- a cache can repair missing source data;
- an audit record can reconstruct authoritative application state;
- a receipt is a mutable transaction record;
- an event consumer can edit the producer's source tables;
- network reachability grants mutation authority;
- one shared service credential proves logical separation;
- one database owner account is sufficient for several components;
- root access is an application interface;
- co-location eliminates the need for boundaries;
- physical separation automatically proves logical ownership;
- a profile can reassign ownership implicitly;
- an integration response can update canonical state directly;
- useful AI output is authoritative;
- SenTient can write canonical state because it is local;
- Publication Gateway owns published source data;
- UCKK owns local kOA Mediatheque records because a publication copy exists;
- the UCKK Publication Bridge owns either the local source record or the external Moodle object;
- a shared Mediatheque frame implies shared storage or shared authority;
- Governance Policy Runtime owns the action it authorizes;
- Resource Governor owns the work it schedules;
- Audit Broker owns the events it records;
- a migration orchestrator owns every migrated schema;
- a restore tool can merge tenants for convenience;
- a backup becomes authoritative when the primary is unavailable;
- passing static analysis proves runtime enforcement;
- passing runtime tests excuses inconsistent contracts;
- one profile result applies to every profile;
- one release result applies after configuration drift;
- a manual assertion can replace negative-test evidence;
- an exception can create permanent shared ownership;
- historical implementation behavior overrides active ownership;
- unavailable tests can be reported as passing.

Missing owner, contract, identity, permission, profile, migration, restore, negative test, or evidence blocks the affected conformance claim.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-CONF-010`;
2. the path is `09-conformance/10-canonical-ownership-validation.md`;
3. the active language is English;
4. every authoritative domain resolves to one active owner;
5. ownership declarations agree across active authority sources;
6. no duplicate ownership exists;
7. no ownerless mutable authority exists;
8. component contracts declare owned, derived, referenced, and prohibited domains;
9. every mutation path resolves to an owner-controlled operation or prohibition;
10. static analysis covers source, configuration, storage, network, migrations, backup, restore, and privileged paths;
11. runtime negative tests deny foreign mutation;
12. prohibited tests prove state unchanged;
13. positive tests prove legitimate owner operations remain functional;
14. every component uses a distinct service or workload identity;
15. storage and database identities match the effective profile;
16. shared unrestricted credentials are absent;
17. physical co-location retains enforceable logical boundaries;
18. sovereign and high-assurance strengthening passes;
19. every derived representation identifies source, rebuild, invalidation, and consumers;
20. derived state cannot become source authority;
21. derived-state rebuild succeeds where required;
22. events and artifacts preserve source ownership;
23. consumers cannot rewrite producer state;
24. imported candidates use destination-owner acceptance;
25. external AI and SenTient cannot mutate canonical state directly;
26. Publication Gateway remains a transport executor;
27. kOA Mediatheque remains the exclusive owner of local media records and local managed content state;
28. the external UCKK platform accepts or rejects its own publication copy through a declared interface, while Publication Gateway and the UCKK Publication Bridge remain separately authorized and tested; the UCKK Import Bridge is independently tested for retrieval, quarantine, validation, and acceptance handoff;
29. Governance Policy Runtime remains non-mutating for application data;
30. Resource Governor remains authority-neutral for application state;
31. Audit Broker remains evidence infrastructure rather than application source;
32. receipts and logs are not used as authoritative application stores;
33. migrations use the owning component contract;
34. central migration tooling cannot write foreign state directly;
35. backups preserve ownership and isolation metadata;
36. restores use owning component contracts;
37. backup and derived stores cannot replace source authority;
38. cross-tenant and cross-domain negative tests pass;
39. every result binds exact profile, overlays, Release Set, contracts, topology, identities, and evidence;
40. effective composed profiles are tested;
41. one profile result is not generalized to another;
42. positive and negative tests both execute;
43. static, deployment, runtime, migration, and recovery checks execute as applicable;
44. incomplete tests are not reported as passing;
45. release-blocking ownership evidence is complete;
46. failed tests block affected conformance claims;
47. exceptions are bounded and cannot redefine ownership;
48. runtime drift is detected and reconciled;
49. semantic changes include accepted decisions and impact analysis;
50. all 48 linked requirements resolve;
51. all required ownership tests execute;
52. all required evidence validates;
53. no unresolved ownership authority remains;
54. generated conformance catalogs and AI context match canonical authority;
55. complete documentation validation passes.

Expected test coverage includes:

`text
TEST-CONF-OWN-001 Authoritative-domain inventory
TEST-CONF-OWN-002 Unique active owner
TEST-CONF-OWN-003 Ownership declaration consistency
TEST-CONF-OWN-004 Ownerless mutable-state detection
TEST-CONF-OWN-005 Mutation-path inventory
TEST-CONF-OWN-006 Static foreign-client detection
TEST-CONF-OWN-007 Distinct service identities
TEST-CONF-OWN-008 Database and schema grants
TEST-CONF-OWN-009 File, object, queue, and secret permissions
TEST-CONF-OWN-010 Positive owner mutation
TEST-CONF-OWN-011 Direct foreign database write denial
TEST-CONF-OWN-012 Foreign queue and object-store denial
TEST-CONF-OWN-013 Unchanged-state proof
TEST-CONF-OWN-014 Cross-tenant and cross-domain denial
TEST-CONF-OWN-015 Derived-state source declaration
TEST-CONF-OWN-016 Derived-state rebuild
TEST-CONF-OWN-017 Read-replica write denial
TEST-CONF-OWN-018 Event producer ownership
TEST-CONF-OWN-019 Consumer cannot rewrite producer state
TEST-CONF-OWN-020 Controlled candidate adoption
TEST-CONF-OWN-021 External AI direct-write denial
TEST-CONF-OWN-022 Publication Gateway source non-ownership
TEST-CONF-OWN-023 kOA Mediatheque local ownership and offline independence
TEST-CONF-OWN-024 Publication Gateway and UCKK adapter separation
TEST-CONF-OWN-025 Governance Policy Runtime non-mutation
TEST-CONF-OWN-026 Resource Governor authority separation
TEST-CONF-OWN-027 Audit Broker non-authority
TEST-CONF-OWN-028 Component-owned migration
TEST-CONF-OWN-029 Foreign migration denial
TEST-CONF-OWN-030 Backup ownership metadata
TEST-CONF-OWN-031 Component-owned restore
TEST-CONF-OWN-032 Profile-composed topology
TEST-CONF-OWN-033 Release Set ownership closure
TEST-CONF-OWN-034 Exception scope and expiry
TEST-CONF-OWN-035 Runtime ownership-drift detection
TEST-CONF-OWN-036 Evidence completeness and reproducibility
`

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid and invalid ownership-validation outcomes. They do not replace component, profile, lifecycle, security, or test contracts.

### 11.1 Shared database process

Orgo and Konnaxion use one PostgreSQL process in a lightweight profile.

Each has:

- a separate database identity;
- a separate schema;
- separate migration credentials;
- separate runtime credentials;
- no cross-schema write grant;
- owner-controlled APIs.

Positive tests prove each component can mutate its own state.

Negative tests prove each component cannot mutate the other schema.

The topology can be conformant despite physical co-location.

### 11.2 Sovereign database separation

A sovereign profile uses separate database instances for Governance Policy Runtime, Identity and Trust, Orgo, and Konnaxion.

The instances strengthen isolation.

Canonical ownership remains the same as in other profiles.

The test result applies only to the tested sovereign topology.

### 11.3 Search index

Konnaxion maintains a search index derived from Konnaxion-owned records.

The index declares its source, refresh, invalidation, and rebuild behavior.

A test deletes the index and rebuilds it from Konnaxion.

The search service cannot update Konnaxion records through the index.

### 11.4 Event consumer

Orgo emits a versioned workflow event.

Konnaxion consumes the event and updates Konnaxion-owned state.

Konnaxion cannot rewrite the Orgo workflow record.

Replay is idempotent and preserves source-event identity.

### 11.5 Publication Gateway

A source component creates an approved publication representation.

Governance Policy Runtime supplies a bounded disclosure decision.

Publication Gateway sends the approved representation and records the result.

It does not edit the source component's record or become the source owner.

### 11.6 kOA Mediatheque publication to UCKK

A user selects a kOA Mediatheque record for publication to a declared UCKK Moodle destination.

The owning Mediatheque creates an owner-authorized publication representation while retaining the local source record and authority.

Governance Policy Runtime supplies the required disclosure decision, and Publication Gateway authorizes the cross-domain release.

The UCKK Publication Bridge creates the target-specific package and manifest, calls the declared external interface, and records the result and receipt.

UCKK accepts or rejects its own external copy. Direct writes to UCKK database tables or managed storage are denied, and local Mediatheque operation remains available when UCKK is offline.

### 11.7 External AI candidate

ChatGPT returns a candidate draft.

The integration adapter cannot write to Orgo or Konnaxion storage.

The destination component validates and explicitly accepts or rejects the candidate.

A negative test proves the adapter credentials have no database access.

### 11.8 Restore validation

A clean environment restores one tenant's Orgo data.

Orgo performs the restore through its contract.

Konnaxion and unrelated tenants remain unchanged.

Derived indexes rebuild after authoritative acceptance.

### 11.9 Invalid audit authority

An operator reconstructs missing Konnaxion records by copying fields directly from audit receipts into Konnaxion tables.

The procedure is invalid.

Receipts are evidence and Konnaxion's restore or repair contract was bypassed.

### 11.10 Invalid shared owner

A shared `platform_admin` service account can write every component schema, publish releases, edit policy, and modify identity records.

The deployment fails canonical ownership validation because no enforceable component boundary remains.
