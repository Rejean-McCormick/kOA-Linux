<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-024",
  "document_class": "architecture_decision_record",
  "status": "active",
  "language": "en",
  "layer": "adrs",
  "adr_id": "ADR-024",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-DATA-001",
  "created_at": "2026-08-03",
  "accepted_at": "2026-08-03",
  "effective_at": "2026-08-03",
  "supersedes": [],
  "superseded_by": null,
  "scope": [
    "component_data_ownership",
    "storage_boundaries",
    "profile_composition",
    "tenant_isolation",
    "backup_and_restore",
    "offline_and_sovereign_operation"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json#/decisions/DEC-DATA-001",
    "generated/decision-index.json#/adrs/ADR-024",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONST-007",
    "REQ-CONST-008",
    "REQ-CONST-009",
    "REQ-CONST-010",
    "REQ-CONST-011",
    "REQ-CONST-012",
    "REQ-DEV-WS-010",
    "REQ-DEV-WS-011",
    "REQ-DEV-WS-012",
    "REQ-DEV-WS-013",
    "REQ-DEV-WS-014",
    "REQ-DEV-WS-015",
    "REQ-DEV-SEC-028",
    "REQ-DEV-SEC-029",
    "REQ-DEV-SEC-030",
    "REQ-LIFE-FR-016",
    "REQ-LIFE-FR-017",
    "REQ-LIFE-FR-018",
    "REQ-OPS-BG-022",
    "REQ-OPS-BG-023",
    "REQ-CONF-SLN-022",
    "REQ-CONF-SLN-023",
    "REQ-CONF-SLN-024",
    "REQ-CONF-SLN-025",
    "REQ-CONF-SLN-026",
    "REQ-CONF-SLN-027",
    "REQ-CONF-SLN-044"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-DEV-003",
    "DOC-DEV-013",
    "DOC-LIFE-016",
    "DOC-SEC-009",
    "DOC-OPS-016",
    "DOC-CONF-005",
    "DOC-CONF-016"
  ],
  "tags": [
    "adr",
    "data-ownership",
    "logical-isolation",
    "physical-isolation",
    "profiles",
    "storage",
    "tenants",
    "backup",
    "restore",
    "sovereignty"
  ]
}
KOA:DOC-META:END -->

# ADR-024 — Logical Data Ownership with Profile-Dependent Physical Isolation

| Field | Value |
| --- | --- |
| ADR | `ADR-024` |
| Owner decision | `DEC-DATA-001` |
| Status | Accepted |
| Decision class | Major |
| Accepted | 2026-08-03 |
| Effective | 2026-08-03 |
| Supersedes | None |
| Superseded by | None |

## 1. Context

kOA components own different authoritative data sets.

Examples include:

- identities and trust relationships;
- governance decisions and policy state;
- component-owned business records;
- operational cases and tasks;
- media and knowledge artifacts;
- publication requests and receipts;
- resource envelopes;
- audit and conformance evidence;
- release and provenance records.

The architecture must preserve clear ownership regardless of deployment scale.

At one extreme, a developer workstation or lightweight endpoint may need to run several components on one machine with limited storage and memory.

At the other extreme, a high-assurance, sovereign, multi-tenant, or hub deployment may require:

- separate storage identities;
- separate database instances;
- separate encryption domains;
- separate backup targets;
- separate operator roles;
- separate failure domains;
- stronger tenant and jurisdictional separation.

Requiring one physical store per component in every profile would create unnecessary cost and operational complexity.

Allowing unrestricted physical co-location would create ambiguity over:

- who can write which data;
- which schema and migration authority applies;
- which backup can be restored into which component;
- whether one component can bypass another component’s interface;
- whether shared credentials create shared ownership;
- whether tenant, cultural, or sovereignty boundaries are preserved;
- whether one failure can corrupt unrelated authoritative state.

The architecture therefore needs one invariant data-ownership model with profile-dependent implementation strength.

## 2. Decision

kOA shall enforce logical data ownership for every authoritative data set in every profile.

Logical ownership means that each authoritative data set has exactly one canonical owning component or authority and exactly one declared write path.

Physical isolation shall be selected by the active profile according to:

- risk;
- assurance level;
- tenant model;
- sovereignty and jurisdiction;
- recovery objectives;
- hardware envelope;
- operational scale;
- performance;
- availability;
- applicable policy and law.

Physical co-location is permitted only when all required logical boundaries remain explicit, enforceable, observable, recoverable, and testable.

Physical co-location shall not create shared ownership.

Physical separation shall not create a second authority owner.

No component, integration, operator, scheduler, test tool, repair tool, backup tool, deployment mechanism, or gateway may write directly into another component’s authoritative store except by executing the owning component’s approved interface under that owner’s authority.

Profiles may require stronger physical separation than the baseline.

A weaker profile shall not silently relax logical ownership.

## 3. Decision Scope

### 3.1 Included storage classes

This decision applies to:

- relational databases;
- document databases;
- key-value stores;
- object stores;
- filesystems;
- queues;
- event logs;
- search indexes;
- caches;
- replicas;
- checkpoints;
- artifact stores;
- audit stores;
- evidence stores;
- backup stores;
- archive stores;
- temporary and repair storage.

### 3.2 Included data states

It applies to:

- active authoritative state;
- staged state;
- replicated state;
- projected state;
- cached state;
- queued state;
- backed-up state;
- archived state;
- restored candidate state;
- migration state;
- repair state;
- exported state.

### 3.3 Included profiles

The decision applies to every profile and overlay.

Profiles can differ in implementation, including:

- one database server with separate databases and credentials;
- one database server with separate schemas where the profile permits it;
- separate database instances;
- separate storage services;
- separate nodes;
- separate encryption domains;
- separate backup targets;
- separate jurisdictional locations.

### 3.4 Excluded decisions

This ADR does not select:

- one universal database engine;
- one filesystem;
- one object store;
- one queue product;
- one backup product;
- one encryption implementation;
- one replication technology;
- one tenancy implementation;
- one mandatory physical topology.

Those choices remain profile-, component-, security-, and operations-specific.

## 4. Definitions and Interpretation

### 4.1 Authoritative data

**Authoritative data** is data whose current accepted value is owned by one declared component or authority.

A copy of authoritative data does not become authoritative merely because it is:

- complete;
- recent;
- indexed;
- replicated;
- signed;
- backed up;
- exported;
- available during an outage.

### 4.2 Logical data ownership

**Logical data ownership** means that one owner controls:

- schema;
- validation;
- accepted writes;
- migrations;
- lifecycle;
- retention;
- deletion;
- export;
- restore;
- conflict resolution;
- domain result.

Logical ownership is independent of physical placement.

### 4.3 Physical isolation

**Physical isolation** is separation through one or more of:

- distinct storage processes;
- distinct database instances;
- distinct volumes;
- distinct devices;
- distinct nodes;
- distinct networks;
- distinct encryption keys;
- distinct backup systems;
- distinct operators;
- distinct jurisdictions.

Physical isolation is a deployment property selected by profile.

### 4.4 Logical isolation

**Logical isolation** is enforced separation within shared infrastructure through:

- distinct storage identities;
- distinct databases or schemas;
- distinct namespaces;
- distinct access-control rules;
- distinct encryption contexts where required;
- distinct migration ownership;
- distinct backup and restore scopes;
- distinct observability and audit;
- prohibition of cross-owner writes.

### 4.5 Non-authoritative copy

A non-authoritative copy includes:

- replica;
- cache;
- projection;
- index;
- export;
- backup;
- archive;
- search document;
- staged import;
- restored candidate;
- offline synchronization package.

It can become authoritative only through the owning component’s declared admission or restoration transaction.

### 4.6 Shared infrastructure

Shared infrastructure is a storage engine or service used by more than one owner.

Shared infrastructure does not imply shared:

- credentials;
- schemas;
- migrations;
- tables;
- buckets;
- queues;
- volumes;
- backup sets;
- retention;
- restoration;
- operator authority.

## 5. Rationale

### 5.1 Stable component boundaries

Logical ownership preserves one architectural model across:

- development;
- lightweight endpoints;
- sovereign nodes;
- hubs;
- build farms;
- control planes.

Component contracts therefore remain stable even when deployment topology changes.

### 5.2 Resource efficiency

Small profiles can safely share infrastructure when the profile proves the necessary isolation.

This avoids requiring a separate storage process for every component on hardware where that separation provides little additional protection.

### 5.3 Stronger profiles without redesign

High-assurance and sovereign profiles can strengthen physical separation without changing component semantics or inventing new owners.

The same owner interface can target a separate database instance, node, volume, or jurisdictional storage domain.

### 5.4 Clear migration authority

The owning component controls its schema and migrations.

A shared database administrator, deployment tool, or migration runner can execute an approved migration but does not become the schema owner.

### 5.5 Safe backup and restore

Ownership makes backup and restoration decisions explicit.

A backup tool copies data.

It does not determine whether the restored data is valid, current, compatible, or authoritative.

### 5.6 Failure containment

Profile-selected physical separation can reduce blast radius where risk justifies it.

Logical separation ensures that even on shared infrastructure, a failure is attributable to a specific owner and boundary.

### 5.7 Credible portability

A component can move from shared to dedicated storage because its ownership, schema, export, restore, and interface contracts are explicit.

This supports profile evolution and credible exit from one storage implementation.

## 6. Required Decision Rules

### 6.1 One-owner rule

Every authoritative data set shall declare exactly one owner.

A data set shall not be jointly owned by:

- two components;
- a component and a gateway;
- a component and a deployment tool;
- a component and an integration;
- a component and a backup service;
- a component and a cache or index.

Collaboration occurs through declared interfaces and exchanged artifacts.

### 6.2 One-write-path rule

Every authoritative mutation shall enter through the owning component’s approved interface or owner-executed maintenance, migration, repair, or restoration path.

Direct cross-component writes are prohibited.

Database credentials alone do not grant architectural write authority.

### 6.3 Shared-engine rule

When multiple owners share a storage engine, the profile shall define:

- separate identities;
- separate credentials;
- separate databases, schemas, buckets, queues, or namespaces;
- access-control enforcement;
- migration ownership;
- backup scope;
- restore scope;
- observability;
- capacity boundaries;
- failure behavior;
- tenant and sovereignty behavior.

Shared superuser credentials shall not be used for ordinary component execution.

### 6.4 Schema rule

Each component owns:

- its authoritative schema;
- schema version;
- migration sequence;
- compatibility rules;
- downgrade or forward-repair behavior;
- validation;
- owner-approved repair procedures.

Another component shall not depend directly on private tables or storage layout.

### 6.5 Query and read rule

Cross-component reads shall occur through:

- declared APIs;
- approved read models;
- published events;
- governed exports;
- owner-created projections;
- another declared integration contract.

Direct read access to another owner’s private storage requires an explicit read interface and does not grant write or schema authority.

### 6.6 Replica and failover rule

A replica remains non-authoritative until an owner-approved failover transition:

- identifies the intended primary;
- verifies data completeness and ordering;
- prevents concurrent writers;
- updates routing;
- records the transition;
- validates owner behavior.

Split-brain authority is prohibited.

### 6.7 Cache and index rule

Caches, projections, and indexes shall be:

- rebuildable;
- owner-attributed;
- invalidatable;
- non-authoritative;
- unable to commit domain changes independently.

Loss of a cache or index shall not redefine authoritative state.

### 6.8 Queue and event rule

A queue or event log may preserve pending delivery or immutable events.

It shall not become the owner of a component’s current domain state unless the component contract explicitly defines that log as its authoritative store.

Delivery metadata does not become business authority.

### 6.9 Backup rule

A backup shall identify:

- source owner;
- exact scope;
- source version;
- capture time;
- consistency model;
- encryption and trust context;
- retention;
- restore target;
- integrity evidence;
- applicable policy.

Backups from different owners shall not be merged into one ambiguous restore unit.

### 6.10 Restore rule

A restore produces candidate restored state.

It becomes authoritative only after the owner verifies:

- identity;
- completeness;
- ordering;
- schema;
- integrity;
- compatibility;
- tenant and sovereignty scope;
- policy;
- dependent artifacts;
- application-level behavior.

### 6.11 Profile-strength rule

A profile shall choose physical isolation using explicit requirements.

Examples of factors that can require dedicated physical isolation include:

- high-assurance operation;
- independent tenant failure domains;
- sovereignty or jurisdiction;
- regulated data;
- separate key custody;
- independent backup or deletion obligations;
- unacceptable shared-administrator risk;
- incompatible availability or performance needs.

### 6.12 Workspace rule

Development workspaces shall namespace or isolate:

- databases;
- volumes;
- queues;
- sockets;
- caches;
- indexes;
- temporary state;
- credentials;
- migrations.

A development workspace shall not use production authoritative storage as its mutable test environment.

### 6.13 Repair rule

Repair tools shall operate through owner-approved procedures.

A break-glass grant can authorize the owner’s repair interface.

It cannot authorize arbitrary direct edits in another component’s store.

### 6.14 Export rule

An export is a non-authoritative representation unless the receiving owner explicitly admits it.

Publication, synchronization, backup, and external processing shall not silently transfer ownership.

### 6.15 Physical-move rule

Moving a component from shared to dedicated storage, or the reverse, shall preserve:

- owner identity;
- exact data scope;
- schema and version;
- ordering;
- access controls;
- migration history;
- backup and restore behavior;
- component interfaces;
- receipts and evidence.

The move is a lifecycle transition, not a change of ownership.

## 7. Consequences

### 7.1 Positive consequences

- Component ownership remains stable across profiles.
- Small deployments can share infrastructure safely.
- High-assurance deployments can strengthen isolation without redesigning components.
- Backup, restore, migration, and repair authority remain explicit.
- Shared database engines do not become architectural owners.
- Components can move between shared and dedicated storage.
- Conformance can test one invariant model with profile-specific physical controls.
- Direct cross-component writes remain identifiable and prohibited.

### 7.2 Costs and constraints

- Shared infrastructure requires careful identity, namespace, migration, and backup design.
- Components cannot use convenient direct joins against another component’s private schema.
- Some read models or projections must be built explicitly.
- Profile matrices must test different physical topologies.
- Storage migration tools need owner-specific procedures.
- Dedicated storage in stronger profiles increases operational cost.
- Backup and restore tests must be scoped per owner.

### 7.3 Operational consequences

Operations shall maintain owner-specific visibility for:

- storage identity;
- capacity;
- latency;
- durability;
- replication;
- backup;
- restore;
- migration;
- retention;
- deletion;
- access;
- incidents.

A shared storage engine shall not collapse these signals into one undifferentiated service status.

## 8. Alternatives Considered

### 8.1 One physical store per component in every profile

**Rejected as a global rule.**

It would impose unnecessary process, memory, storage, backup, monitoring, and operator overhead on small deployments.

Profiles can still require dedicated physical stores where justified.

### 8.2 One shared database with unrestricted cross-component access

**Rejected.**

It would erase component ownership, couple schemas, broaden credentials, weaken restoration boundaries, and create hidden cross-component transactions.

### 8.3 Shared database tables owned jointly by multiple components

**Rejected.**

Joint ownership makes migrations, validation, retention, deletion, and recovery ambiguous.

Shared concepts shall be exchanged through contracts rather than jointly mutated tables.

### 8.4 Let the deployment platform own all persistent data

**Rejected.**

Deployment platforms manage placement and lifecycle.

They do not own component semantics, schemas, retention, migrations, or authoritative results.

### 8.5 Let the data platform team become canonical owner

**Rejected.**

A data-platform team can operate infrastructure and tooling but cannot replace the component owner’s domain authority.

### 8.6 Treat event logs as universal authority

**Rejected as a global rule.**

A component may adopt an authoritative event log explicitly.

Other components shall not be forced into event sourcing, and delivery logs shall not become domain owners by convenience.

### 8.7 Infer ownership from physical location

**Rejected.**

Physical location changes across profiles and lifecycle operations.

Ownership must remain explicit in canonical contracts.

### 8.8 Allow direct read-only database access everywhere

**Rejected as a baseline.**

Read-only access can still expose private schema, bypass minimization, create coupling, and violate tenant or sovereignty rules.

Declared read models and governed exports are preferred.

## 9. Security, Lifecycle, and Profile Implications

### 9.1 Identity and privilege

Each authoritative store shall use component-scoped identities.

Administrative identities shall be separate from runtime identities.

Shared infrastructure administration shall not grant applications cross-owner write access.

### 9.2 Encryption

Encryption requirements are profile- and data-class-specific.

Physical co-location does not permit one encryption key to erase owner, tenant, or sovereignty separation where separate key domains are required.

### 9.3 Tenant and sovereignty boundaries

Profiles shall declare whether tenants or jurisdictions require:

- logical namespace separation;
- separate databases;
- separate instances;
- separate volumes;
- separate nodes;
- separate encryption keys;
- separate backup locations;
- separate operator custody.

A tenant identifier inside one table is not sufficient when the profile requires a stronger boundary.

### 9.4 Lifecycle

Schema changes, migrations, failovers, restores, and physical moves are owner-controlled lifecycle transitions.

Cross-owner migrations shall use explicit exchanged artifacts or interfaces.

Rollback is permitted only when schema and data compatibility remain valid.

Otherwise, forward repair applies.

### 9.5 Release channels

Component schema and service changes normally belong to the `services` release channel.

Governance storage policy belongs to `governance`.

Storage drivers or system-level storage dependencies belong to `system`.

Knowledge artifacts belong to `knowledge`.

A Release Set binds compatible versions when a storage transition crosses channels.

### 9.6 Failure behavior

Failure of shared physical infrastructure can affect several owners.

Recovery shall still preserve:

- separate owner state;
- separate write authority;
- separate restore decisions;
- separate component validation;
- separate receipts and evidence.

Shared failure does not justify merged recovery authority.

### 9.7 Break-glass

Break-glass can authorize narrowly scoped owner-approved operations.

It cannot transfer ownership, bypass schema validation, or authorize arbitrary direct writes across component boundaries.

### 9.8 Supply chain

Storage engines, migration tools, backup tools, drivers, and repair artifacts are supply-chain objects.

Their admission does not grant them authority over component data.

## 10. Conformance and Evidence

Conformance shall verify both logical ownership and the physical isolation required by the active profile.

Required conclusions include:

| Evidence area | Required conclusion |
| --- | --- |
| Ownership registry | Every authoritative data set resolves to one owner |
| Write paths | Every authoritative mutation uses the owner interface |
| Credentials | Runtime identities cannot write another owner’s store |
| Shared infrastructure | Namespaces, schemas, databases, buckets, queues, and permissions remain separated |
| Schema authority | Only the owner controls migrations and validation |
| Reads | Cross-owner reads use declared interfaces or governed projections |
| Replication | Failover preserves one active writer |
| Caches and indexes | Derived stores remain rebuildable and non-authoritative |
| Queues | Delivery metadata does not become domain authority |
| Backup | Scope, owner, integrity, retention, and encryption resolve |
| Restore | Restored state remains candidate until owner validation passes |
| Profile strength | Physical topology matches profile requirements |
| Tenant isolation | Tenant boundaries match declared assurance |
| Sovereignty | Jurisdiction, custody, keys, and backup location match policy |
| Workspace isolation | Development data is namespaced and production-separated |
| Repair | Repair tools use owner-approved paths |
| Physical migration | Ownership and interfaces survive topology changes |
| Failure isolation | Shared infrastructure failure does not merge owner authority |
| Traceability | `DEC-DATA-001` and `LOCK-DATA-001` resolve to tests and evidence |

The following fail conformance:

- one data set with multiple canonical owners;
- shared runtime credentials across component owners;
- direct writes into another component’s tables or objects;
- another component depending on private schema layout;
- one migration authority for unrelated component schemas;
- restoring a backup directly into authoritative service without owner validation;
- promoting a cache, replica, export, or backup to authority without owner transition;
- split-brain writers;
- physical co-location without explicit logical isolation;
- claiming strong tenant or sovereignty isolation with only an unverified label;
- development tests using production authoritative storage;
- break-glass direct database editing outside owner-approved repair;
- profile-required physical isolation absent;
- missing `LOCK-DATA-001` traceability.

Evidence shall follow `docs/09-conformance/05-test-evidence.md`.

## 11. Decision Closure, Review, and Supersession

### 11.1 Closed decisions

This ADR closes the following questions:

- every authoritative data set has one logical owner;
- every authoritative mutation has one declared owner path;
- physical co-location is permitted only when logical boundaries remain enforceable;
- physical isolation is selected by profile;
- stronger profiles can require dedicated instances, nodes, keys, or jurisdictions;
- shared infrastructure does not create shared ownership;
- replicas, caches, indexes, exports, backups, and restored candidates remain non-authoritative until owner transition;
- direct cross-component writes are prohibited;
- backup and restore remain owner-scoped;
- physical topology changes do not change ownership.

### 11.2 Prohibited assumptions

This ADR shall not be interpreted to mean:

- every component requires its own physical database;
- one database engine implies one data owner;
- separate schemas always satisfy high-assurance isolation;
- a database administrator owns application data;
- read-only access is automatically safe;
- a replica is automatically a valid primary;
- a backup is immediately authoritative when restored;
- one shared encryption key always satisfies sovereignty;
- an event log is universally authoritative;
- a deployment platform owns component data;
- physical separation permits direct cross-component writes;
- physical co-location permits shared credentials;
- an exception can create permanent joint ownership.

### 11.3 Review triggers

This ADR shall be reviewed when:

- a new profile requires stronger data or jurisdictional separation;
- one component proposes direct access to another component’s private store;
- a shared database topology cannot preserve migration or restore boundaries;
- tenant, cultural, legal, or sovereignty requirements change;
- a distributed transaction proposal crosses component owners;
- a new data-platform architecture changes failover or backup authority;
- operational evidence shows logical isolation is insufficient for a profile;
- mandatory physical separation becomes economically or technically disproportionate.

### 11.4 Supersession condition

Supersession requires a new accepted major ADR that:

- identifies this ADR;
- defines the replacement ownership and storage-boundary model;
- preserves one accountable authority for schema, writes, migrations, retention, deletion, backup, restore, and recovery;
- addresses profiles, tenants, sovereignty, encryption, failover, lifecycle, and conformance;
- updates `DEC-DATA-001`, `LOCK-DATA-001`, component contracts, profile contracts, tests, and evidence;
- provides migration, rollback or forward-repair, and credible-exit behavior.

Until superseded, this ADR remains the controlling rationale for `DEC-DATA-001`.
