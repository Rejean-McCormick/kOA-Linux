<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/development",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "generated/toolchain-catalog.json",
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
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-PROFILE-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-SEC-001",
    "DEC-PRIV-001",
    "DEC-OFFLINE-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-PORT-001",
    "DEC-AUDIT-001",
    "DEC-RECEIPT-001",
    "DEC-DOC-003",
    "DEC-DOC-004",
    "DEC-DOC-005"
  ],
  "requirement_ids": [
    "REQ-DEV-DB-001",
    "REQ-DEV-DB-002",
    "REQ-DEV-DB-003",
    "REQ-DEV-DB-004",
    "REQ-DEV-DB-005",
    "REQ-DEV-DB-006",
    "REQ-DEV-DB-007",
    "REQ-DEV-DB-008",
    "REQ-DEV-DB-009",
    "REQ-DEV-DB-010",
    "REQ-DEV-DB-011",
    "REQ-DEV-DB-012",
    "REQ-DEV-DB-013",
    "REQ-DEV-DB-014",
    "REQ-DEV-DB-015",
    "REQ-DEV-DB-016",
    "REQ-DEV-DB-017",
    "REQ-DEV-DB-018",
    "REQ-DEV-DB-019",
    "REQ-DEV-DB-020",
    "REQ-DEV-DB-021",
    "REQ-DEV-DB-022",
    "REQ-DEV-DB-023",
    "REQ-DEV-DB-024",
    "REQ-DEV-DB-025",
    "REQ-DEV-DB-026",
    "REQ-DEV-DB-027",
    "REQ-DEV-DB-028",
    "REQ-DEV-DB-029",
    "REQ-DEV-DB-030"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DEV-006",
    "LOCK-DEV-007",
    "LOCK-DEV-008",
    "LOCK-DEV-009",
    "LOCK-DEV-010",
    "LOCK-DATA-001",
    "LOCK-DATA-002",
    "LOCK-DATA-003",
    "LOCK-DATA-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-007",
    "DOC-DEV-008",
    "DOC-DEV-009",
    "DOC-DEV-010",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "development",
    "local-databases",
    "migrations",
    "workspace-isolation",
    "data-ownership",
    "schema-evolution",
    "fixtures",
    "rollback",
    "forward-repair",
    "release-transition",
    "restore",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Local Databases and Migrations

## 1. Purpose

This document defines how kOA development workspaces create, isolate, evolve, test, destroy, and promote database state and migration definitions.

Local databases are mutable development resources. They allow developers to test component schemas, state transitions, queries, events, restore behavior, and compatibility without touching operational authority.

Migration definitions are candidate lifecycle artifacts. They become release inputs only after ownership, compatibility, safety, recovery, and evidence validation.

The purpose of this model is to prevent:

- cross-workspace state collisions;
- cross-component schema ownership;
- accidental production access;
- rewritten migration history;
- untested destructive transitions;
- promotion of developer volumes or dumps;
- false rollback confidence;
- release activation without complete migration evidence.

Canonical component ownership remains defined by the components registry and component contracts. A development database does not alter that ownership.

## 2. Scope

This document applies globally to development and migration-validation uses of:

- PostgreSQL or equivalent service databases;
- SQLite and other component-local embedded databases;
- DuckDB or equivalent analytical development stores;
- queue or job persistence;
- object-store metadata databases;
- search and derived-index stores;
- migration history tables;
- schema registries embedded in component storage;
- test databases;
- ephemeral integration databases;
- staged migration-validation targets;
- local backups and restore fixtures;
- database containers and volumes;
- WSL-hosted databases;
- Build Farm migration tests.

It governs:

- workspace naming and target resolution;
- service identities and write grants;
- schema ownership;
- migration authoring;
- fixture and seed data;
- migration execution;
- interruption and recovery;
- rollback and forward repair;
- cross-component release ordering;
- development-to-release packaging;
- cleanup and evidence.

It does not prescribe a universal database engine, migration framework, container runtime, service manager, or SQL dialect.

The owning component and toolchain contracts select those implementations within the active development profile.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/component-catalog.json` | Component identity and authoritative data ownership |
| `generated/component-catalog.json` | Active component-contract inventory |
| `contracts/components/*.component.json` | Owned schemas, state transitions, migration behavior, export, restore, and evidence |
| `generated/profile-catalog.json` | Development, build, user, sovereign, and staged-target profile boundaries |
| `generated/toolchain-catalog.json` | Migration tools, database clients, test runners, and supported versions |
| `contracts/artifact-classes.contract.json` | Migration, service, release, backup, and restore artifact classes |
| `contracts/release-channels.contract.json` | Services and related release compatibility |
| `generated/requirements-index.json` | Normative database and migration requirements |
| `generated/assertion-index.json` | Development, ownership, lifecycle, security, and release assertions |
| `generated/traceability.json` | Migration relationships to decisions, components, tests, evidence, releases, and documents |
| `generated/exception-index.json` | Bounded migration exceptions and compensating controls |
| `generated/test-catalog.json` | Empty-store, upgrade, interruption, rollback, restore, isolation, and release tests |
| `generated/evidence-catalog.json` | Migration and restore evidence |
| `generated/authority-manifest.json` | Active contract and release authority |
| `generated/decision-index.json` | Accepted ownership, development, lifecycle, release, and security decisions |

The related ownership and workspace documents are:

`text
04-components/02-component-data-ownership.md
05-development/01-development-profile-boundaries.md
05-development/02-workspace-identity.md
05-development/03-workspace-isolation.md
05-development/07-ports-networks-and-sockets.md
05-development/08-volumes-and-persistent-data.md
05-development/09-secrets-and-local-identities.md
05-development/10-parallel-applications-and-branches.md
05-development/16-development-to-release-transition.md
`

## 4. Model and Responsibilities

### 4.1 Database instance

A database instance is a physical or logical engine realization used by one or more isolated component namespaces.

A conforming development database instance records:

- workspace identity;
- engine family and version;
- instance or container identity;
- network endpoint or local path;
- storage root or volume;
- component namespaces;
- service identities;
- lifecycle state;
- backup and destruction behavior.

One engine process can host multiple component namespaces only when the active profile permits consolidation and each namespace remains independently owned and access-controlled.

### 4.2 Component database namespace

A component database namespace is the physical realization of one component's owned development state.

It can be:

- a separate database;
- a separate schema;
- a separate embedded database file;
- a separate object-store namespace;
- a separate queue namespace;
- another toolchain-declared isolated store.

The namespace has one component owner.

Database administrators and workspace tooling can operate the physical engine without becoming semantic owners of component data.

### 4.3 Migration

A migration is a versioned component-owned transition from one declared state representation to another.

A migration can change:

- tables;
- columns;
- constraints;
- indexes;
- permissions;
- stored representations;
- reference structures;
- event or outbox structures;
- derived indexes;
- workflow state encoding;
- retention structures;
- component-local migration metadata.

A migration does not change component ownership unless an accepted architecture decision and ownership-cutover plan explicitly do so.

### 4.4 Migration identity and history

A migration has a stable identifier that is unique within its component's migration namespace.

The identifier remains reserved after publication.

The component-owned migration history records:

- migration identifier;
- migration artifact version;
- start and completion state;
- source and target schema versions;
- executor identity;
- applied time;
- validation result;
- recovery state;
- supersession or repair relationship.

The history table is operational evidence for the component. It is not a substitute for registered release and conformance evidence.

### 4.5 Candidate and released migrations

A candidate migration can be revised inside its isolated development branch before publication, subject to source review.

A released migration is immutable.

A defect in a released migration is corrected by:

- a new repair migration;
- a new forward migration;
- an explicit supersession;
- withdrawal of an unreleased release candidate;
- restoration and re-execution under a declared recovery plan.

Applied migration history is never edited merely to make the database appear current.

### 4.6 Fixtures, seeds, and migrated data

| Data class | Purpose | Authority |
| --- | --- | --- |
| Fixture | Deterministic test input for a test scenario | Test-only |
| Seed | Initial development or test state declared by a component | Environment-scoped |
| Generated synthetic data | Load, behavior, or privacy-safe testing | Test-only |
| Authorized governed test data | Explicit bounded validation using controlled source material | Procedure-scoped |
| Migrated component data | State transformed by the migration under test | Target component owns the resulting test state |
| Derived index | Rebuildable projection | Non-authoritative |

Fixtures and seeds do not become release data merely because a migration processed them.

### 4.7 Target classes

Supported migration target classes include:

| Target class | Use |
| --- | --- |
| Empty ephemeral target | Fresh-install and baseline-schema validation |
| Workspace target | Interactive component development |
| Integration target | Multi-component contract and compatibility testing |
| Prior-version target | Upgrade testing from a supported release |
| Restored test target | Migration after validated backup restoration |
| Build Farm target | Clean automated migration and compatibility testing |
| Authorized staged target | Release or operations validation under a separate contract |

An operational production target is not a development target.

### 4.8 Roles

| Role | Responsibility |
| --- | --- |
| Component owner | Owns migration semantics, ordering, validation, and recovery |
| Developer | Authors and tests candidate migrations in isolated targets |
| Reviewer | Reviews ownership, safety, data transformation, and recovery |
| Test executor | Runs declared migration and restore tests |
| Build Farm | Recreates tests from declared inputs on clean workers |
| Release coordinator | Orders compatible component-owned migrations |
| Operations or lifecycle owner | Executes approved migration packages on staged or active targets |
| Evidence producer | Records attributable results |
| Database administrator | Maintains physical engine health within component ownership boundaries |

### 4.9 Cross-component coordination

A release can require several component migrations.

The release coordinator defines order and compatibility windows.

Each component executes its own migration through its own contract and identity.

The coordinator does not run one unrestricted script that writes all component domains.

### 4.10 Migration phases

A migration uses the phases needed for its risk and compatibility:

1. **expand** — add compatible structures;
2. **migrate** — transform or backfill data;
3. **verify** — prove completeness and invariants;
4. **switch** — activate the new representation or application behavior;
5. **contract** — remove obsolete structures after the compatibility window.

A simple compatible migration can combine phases when tests prove safety.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-DB-001,REQ-DEV-DB-002,REQ-DEV-DB-003,REQ-DEV-DB-004,REQ-DEV-DB-005,REQ-DEV-DB-006,REQ-DEV-DB-007,REQ-DEV-DB-008,REQ-DEV-DB-009,REQ-DEV-DB-010,REQ-DEV-DB-011,REQ-DEV-DB-012,REQ-DEV-DB-013,REQ-DEV-DB-014,REQ-DEV-DB-015,REQ-DEV-DB-016,REQ-DEV-DB-017,REQ-DEV-DB-018,REQ-DEV-DB-019,REQ-DEV-DB-020,REQ-DEV-DB-021,REQ-DEV-DB-022,REQ-DEV-DB-023,REQ-DEV-DB-024,REQ-DEV-DB-025,REQ-DEV-DB-026,REQ-DEV-DB-027,REQ-DEV-DB-028,REQ-DEV-DB-029,REQ-DEV-DB-030 -->
- **REQ-DEV-DB-001 — SHALL:** Every development database, schema, queue-backed store, object-store namespace, and persistent volume have a unique workspace identity, component owner, purpose, and lifecycle state.
- **REQ-DEV-DB-002 — SHALL NOT:** Two development workspaces share mutable database state, migration history, service credentials, write-capable volumes, or component-owned storage namespaces.
- **REQ-DEV-DB-003 — SHALL:** Each component own the schema definitions, migration sequence, migration history interpretation, seed rules, backup mapping, restore behavior, and destructive operations for its authoritative data domains.
- **REQ-DEV-DB-004 — SHALL NOT:** A component migration write another component's authoritative tables, files, queues, indexes, or private migration history.
- **REQ-DEV-DB-005 — SHALL:** A development profile that consolidates components in one database process preserve separate logical databases or schemas, service identities, write grants, migration ownership, and backup inventory.
- **REQ-DEV-DB-006 — SHALL:** Every migration have a stable identifier, owner, source schema version, target schema version, ordered dependencies, applicability rule, forward procedure, validation procedure, and failure strategy.
- **REQ-DEV-DB-007 — SHALL:** A migration identifier and released migration body remain immutable after publication in an active artifact or release channel.
- **REQ-DEV-DB-008 — SHALL:** A corrected released migration use a new migration identifier and an explicit supersession, repair, or compatibility relationship rather than rewriting applied history.
- **REQ-DEV-DB-009 — SHALL:** Every schema-changing candidate be tested from an empty store and from every supported prior schema version declared by the component and release contract.
- **REQ-DEV-DB-010 — SHALL:** Migration validation cover schema, constraints, indexes, data transformation, reference integrity, permissions, idempotency, restart behavior, failure behavior, and application compatibility.
- **REQ-DEV-DB-011 — SHALL:** Destructive, lossy, long-running, locking, repartitioning, ownership-changing, or externally visible migrations declare additional review, backup, recovery, evidence, and rollout controls.
- **REQ-DEV-DB-012 — SHALL NOT:** A development migration connect to or mutate a production, sovereign, user, shared staging, another workspace's, or otherwise undeclared target.
- **REQ-DEV-DB-013 — SHALL:** Migration targets be resolved from explicit workspace or staged-target configuration and validated before any write or lock is acquired.
- **REQ-DEV-DB-014 — SHALL:** Development data use synthetic, fixture, generated, minimized, anonymized, or specifically authorized test data with declared retention and destruction behavior.
- **REQ-DEV-DB-015 — SHALL NOT:** Ordinary migrations, fixtures, seeds, tests, examples, or developer tools contain production credentials, private signing keys, recovery secrets, or undeclared governed data.
- **REQ-DEV-DB-016 — SHALL:** Seed data and fixtures be versioned, attributable, deterministic where required, scoped to their test purpose, and distinguishable from authoritative migrated data.
- **REQ-DEV-DB-017 — SHALL:** Parallel migration execution use a component-owned lock, lease, or equivalent serialization mechanism and expose stale-lock recovery without permitting concurrent schema authority.
- **REQ-DEV-DB-018 — SHALL:** A migration be restart-safe, explicitly non-restartable with a recovery plan, or divided into resumable phases with durable progress.
- **REQ-DEV-DB-019 — SHALL:** Rollback be provided when safe and validated; when rollback is unsafe or impossible, the migration define forward repair, restoration, and operator decision points.
- **REQ-DEV-DB-020 — SHALL NOT:** The presence of a down migration, transaction wrapper, snapshot, backup, or database rollback command be treated as proof that reversal is safe.
- **REQ-DEV-DB-021 — SHALL:** Cross-component release migration be coordinated as an ordered set of component-owned migrations with explicit compatibility windows and without a coordinator directly writing participant domains.
- **REQ-DEV-DB-022 — SHALL:** Expand, migrate, verify, switch, and contract phases be used when an immediate incompatible schema transition would break supported application or event versions.
- **REQ-DEV-DB-023 — SHALL:** Migration tests include interrupted execution, retry, duplicate invocation, partial worker failure, stale application version, backup restore, and clean-target restoration where applicable.
- **REQ-DEV-DB-024 — SHALL:** Generated migration artifacts and release candidates identify their source revision, component contract version, toolchain, database engine family and supported version range, profile, test results, and producer.
- **REQ-DEV-DB-025 — SHALL NOT:** A mutable local database volume, copied database directory, developer snapshot, unregistered dump, or manually edited migration history be promoted directly into an active deployment.
- **REQ-DEV-DB-026 — SHALL:** The development-to-release transition package migration definitions, compatibility declarations, preflight checks, required backups, execution order, health gates, evidence rules, rollback or forward-repair behavior, and post-migration validation.
- **REQ-DEV-DB-027 — SHALL:** Migration logs and evidence identify the target, owner, migration identifiers, source and target versions, executor, start and completion state, validation results, failures, and recovery actions without exposing governed payloads.
- **REQ-DEV-DB-028 — SHALL:** Workspace cleanup stop database processes, remove workspace-owned mutable stores and credentials, preserve required migration evidence, and prove that other workspaces and operational targets were unchanged.
- **REQ-DEV-DB-029 — SHALL:** Local database and migration failure remain workspace-scoped or staged-target-scoped and fail closed before release activation or operational ownership changes.
- **REQ-DEV-DB-030 — SHALL:** Local database and migration conformance pass only when ownership, isolation, target resolution, fixture, compatibility, interruption, rollback or repair, release packaging, cleanup, and evidence tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Local Database Procedure

### 6.1 Provision the target

Provisioning resolves:

1. workspace identity;
2. development profile;
3. component owner;
4. database engine and supported version;
5. instance and namespace identity;
6. storage or volume;
7. service identity and credentials;
8. network endpoint, port, or local path;
9. migration toolchain;
10. test-data classification;
11. cleanup policy.

The provisioning process validates that no mutable namespace collides with another workspace.

### 6.2 Establish access controls

Each component receives write access only to its own namespace.

Cross-component development access uses:

- versioned APIs;
- controlled read models;
- explicit read-only test grants where the component contract permits them;
- declared artifacts;
- events.

A shared administrative identity is limited to engine maintenance and cannot be used by ordinary component services.

### 6.3 Initialize an empty store

An empty target is initialized from the active component baseline and ordered migration set.

The initialization test verifies:

- schema creation;
- ownership and permissions;
- required constraints;
- indexes;
- migration history;
- seed behavior;
- application startup;
- clean shutdown and restart.

An empty-store pass does not replace upgrade testing.

### 6.4 Load fixtures or synthetic data

Test data is loaded after schema initialization.

The loader records:

- fixture or generator identity;
- version;
- target component;
- intended tests;
- data classification;
- expected object counts or invariants;
- cleanup behavior.

Governed data uses a separately authorized path and remains isolated.

### 6.5 Run local component services

The component uses its workspace identity and component-scoped database credentials.

The service validates its expected schema version before accepting writes.

A schema mismatch yields a clear blocked or compatibility state rather than automatic unreviewed mutation.

### 6.6 Reset the workspace database

A reset is permitted only for workspace-owned or ephemeral test state.

The reset process:

1. verifies target identity;
2. stops affected services;
3. removes or recreates the component namespace;
4. reruns baseline and migrations;
5. reloads declared fixtures;
6. validates the result;
7. records the reset when required.

A reset command cannot accept an unresolved or production-like default target.

### 6.7 Back up local migration targets

Local backups are useful for:

- repeatable upgrade tests;
- failure injection;
- restore-before-migrate tests;
- investigation.

A backup records the component, schema version, engine version, fixture or data class, and intended test.

A local backup is not a release artifact unless registered and validated under an artifact contract.

### 6.8 Clean up

Cleanup stops the component and database process, revokes workspace credentials, removes owned volumes and files, clears local secrets, and retains only required test evidence and registered artifacts.

It verifies that other workspace namespaces still exist and remain unchanged.

## 7. Migration Lifecycle

### 7.1 Author

The developer defines:

- migration identifier;
- component owner;
- source and target versions;
- prerequisites;
- forward transformation;
- validation queries or checks;
- expected duration and lock scope;
- restart behavior;
- rollback or forward repair;
- compatibility window;
- backup requirements;
- evidence requirements.

The migration is reviewed as code and as a state transition.

### 7.2 Static validation

Static checks confirm:

- identifier uniqueness;
- ownership;
- ordering;
- syntax;
- prohibited cross-owner writes;
- target-engine compatibility;
- absence of embedded production secrets;
- required metadata;
- relationship to the component contract.

Static success does not prove execution safety.

### 7.3 Empty-store test

The complete baseline and migration sequence are applied to an empty target.

The resulting schema and application behavior are compared with the declared target version.

### 7.4 Supported-upgrade tests

Each supported prior version is restored or constructed in a clean target.

The candidate migration is applied using the declared application and engine compatibility window.

Tests verify current and transitional readers and writers where rolling compatibility is part of the release contract.

### 7.5 Data transformation tests

Transformation tests cover:

- valid records;
- boundary values;
- null and absent values;
- duplicate or conflicting records;
- orphaned references;
- large records;
- restricted data classes;
- retained historical state;
- records requiring explicit rejection or quarantine.

The expected disposition of every unsupported record class is declared.

### 7.6 Interruption and retry tests

The migration is interrupted at declared points.

The test restarts or resumes it and verifies:

- durable progress;
- lock recovery;
- duplicate safety;
- no repeated destructive effect;
- no false completion;
- stable failure reporting;
- valid recovery action.

### 7.7 Rollback or forward-repair tests

A safe rollback restores the prior supported representation and application behavior.

When reversal is unsafe, tests verify:

- restoration from a validated backup;
- forward repair;
- operator decision points;
- preservation of evidence;
- no activation of partial state.

### 7.8 Cross-component compatibility tests

For a coordinated release, tests execute the declared order of component-owned migrations.

They verify:

- application compatibility before and after each phase;
- event and artifact compatibility;
- cross-component reference integrity;
- no direct cross-owner write;
- failure containment;
- partial-completion reporting;
- safe retry or repair.

### 7.9 Package for release

A migration release package contains:

`text
component identity
component contract version
migration identifiers and ordered dependencies
source and target schema versions
supported engine versions
profile applicability
preflight checks
backup requirements
execution phases
compatibility window
health gates
validation checks
rollback or forward-repair procedure
required tests
required evidence
operator-facing failure codes
`

The package is immutable once published in an active release candidate.

### 7.10 Staged execution

An operations or lifecycle contract, not the development workspace, executes the package on an authorized staged target.

The target verifies release identity, component ownership, profile, engine, schema, backup readiness, capacity, and evidence path before mutation.

### 7.11 Activation

Application or artifact activation occurs only after migration health gates pass.

A services release cannot claim active compatibility while its required component migration is incomplete or unverified.

### 7.12 Supersession

A later migration can supersede a candidate or repair a released transition.

The relationship is explicit and traceable.

Historical migration identifiers and evidence remain retained.

## 8. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained state | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| Target identity is absent or ambiguous | Block before connection or lock | Source and migration files | Guessing a database target | Target-resolution result |
| Target belongs to another workspace | Reject access | Caller workspace | Reusing the foreign namespace | Isolation failure |
| Target is operational or production-like | Block development execution and alert | Candidate migration | Continuing in read-only mode as a workaround | Boundary incident |
| Component owner does not match namespace | Block migration | Existing target state | Cross-owner schema mutation | Ownership result |
| Migration identifier is duplicated | Block packaging and execution | Earlier valid migration | Choosing one by filename order | Registry result |
| Released migration body changed | Reject the altered package | Previously published migration | Rewriting applied history | Immutability result |
| Migration lock is active | Wait, fail, or follow declared stale-lock review | Current schema state | Concurrent migration authority | Lock-state evidence |
| Process exits during migration | Resume, repair, restore, or fail according to contract | Last verified state and durable progress | Marking completion from process exit | Interruption result |
| Validation check fails | Keep target inactive or workspace-scoped | Prior active release or isolated test target | Activating failed state | Validation evidence |
| Rollback is unsafe | Use declared restoration or forward repair | Backup and staged state | Running an untested down migration | Recovery decision |
| Backup is missing for a required migration | Block execution | Current state | Proceeding because the change appears small | Preflight result |
| Fixture contains undeclared governed data | Quarantine and remove it under incident handling | Approved synthetic fixtures | Continuing the test | Data-boundary incident |
| Service version is incompatible | Hold the relevant phase or use the declared compatibility window | Compatible readers and writers | Uncoordinated switch | Compatibility result |
| Cross-component migration partially completes | Report partial state and run declared repair sequence | Independently valid committed domains | Claiming atomic success | Coordination evidence |
| Derived index rebuild fails | Keep source authoritative and mark the index unavailable | Source data and direct access | Repairing source from the index | Rebuild result |
| Storage or capacity is insufficient | Block or pause before unsafe mutation | Current verified target | Continuing into disk exhaustion | Capacity result |
| Evidence path is unavailable | Block required staged or critical transition | Workspace tests and current active state | Unevidenced activation | Evidence-delivery result |
| Cleanup cannot prove isolation | Mark workspace retirement blocked | Source and evidence | Reusing the namespace | Cleanup result |

Safe degradation keeps failures inside the workspace or authorized staged target. It does not promote partial state, bypass ownership, weaken target checks, or alter an operational deployment from a development path.

## 9. Cross-System Interactions

### 9.1 Component contracts

The component contract owns schema and migration semantics.

Development tooling consumes that contract and cannot create a second schema owner.

### 9.2 Workspace tooling

Workspace tooling allocates instances, namespaces, credentials, ports, sockets, and volumes.

It operates physical resources without owning component data semantics.

### 9.3 Container runtimes

A database can run in a container when the development profile permits it.

The container identity, volume, network, credentials, and cleanup remain workspace-scoped.

Container availability is not a global database requirement.

### 9.4 Windows and WSL

A WSL database target resides in the declared Linux or profile-approved storage boundary.

Windows-mounted files, Windows database clients, forwarded ports, and host credentials are explicit interop surfaces.

A Windows-side database is used only when the profile and workspace contract declare its trust, performance, identity, and cleanup behavior.

### 9.5 Build Farm

Build Farm reconstructs migration targets from declared artifacts or supported prior versions.

It does not consume the developer's mutable database volume or manually edited migration history.

### 9.6 Release coordinator

The release coordinator resolves migration order across components and release channels.

Each component migration runs under its owner identity and validation contract.

### 9.7 Operations and lifecycle

Operations validates the target and executes approved packages.

Lifecycle controls staging, health gates, activation, rollback, forward repair, and receipts.

Development tooling cannot directly activate the operational result.

### 9.8 Backup, restore, and portability

Migration tests consume component-owned backups or exports through declared contracts.

A clean restore can become a prior-version migration target.

Restore success and migration success remain distinct results.

### 9.9 Audit and evidence

Migration evidence records target identity, versions, execution, validation, and recovery without copying unrestricted data rows into general logs.

Audit Broker owns cross-component evidence routing where deployed.

### 9.10 AI and workbenches

An AI assistant, SenTient, notebook, IDE, or database tool can propose migration text or analysis.

The output remains candidate material.

The component owner reviews it, deterministic tests validate it, and the release process controls publication.

## 10. Decision Closure and Validation Criteria

This document is supported by the accepted decisions declared in its metadata.

A semantic change requires:

1. an accepted owner decision;
2. impact analysis across component ownership, profiles, toolchains, schemas, events, artifacts, release channels, lifecycle, security, backup, restore, tests, evidence, and documentation;
3. updated canonical contracts;
4. complete validation before authority activation.

The following assumptions are prohibited:

- a database engine owns the component data stored in it;
- one database process creates one semantic owner;
- an administrator account can be used by all component services;
- a migration can update another component's schema for convenience;
- filename order is sufficient migration identity;
- an already released migration can be edited because it has not reached every target;
- a down migration is necessarily safe;
- a transaction makes every schema change reversible;
- a snapshot proves restore;
- an empty-store test proves upgrade safety;
- one prior-version test covers every supported prior version;
- successful SQL execution proves application compatibility;
- a developer's local database is a release artifact;
- a copied database directory is a valid deployment;
- a development connection can point to production for read-only validation;
- a default connection string is safe when the target is not supplied;
- fixture data is harmless because it is used only locally;
- a database container isolates credentials automatically;
- WSL and Windows database state are the same trust boundary;
- a coordinator may write all component schemas because it owns release ordering;
- last-write-wins can resolve ownership, rights, approval, consent, or evidence conflicts;
- an index can repair authoritative source data;
- build success authorizes operational migration;
- migration completion authorizes application activation;
- local logs replace registered evidence;
- a failed migration can be hidden by editing migration history;
- cleanup is complete when the database process stops.

This document is conformant when:

1. it is registered as `DOC-DEV-011`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists and applicable assertions pass;
6. every local store has a unique workspace identity and component owner;
7. no mutable database, volume, credentials, or migration history is shared across workspaces;
8. component service identities have write access only to their owned namespaces;
9. migration identifiers are stable and released migrations are immutable;
10. corrected released migrations use new identifiers and traceable repair relationships;
11. empty-store and every supported-prior-version upgrade test pass;
12. transformation, constraint, reference, permission, restart, interruption, retry, and compatibility tests pass;
13. destructive and high-risk migrations have backup, recovery, review, and evidence controls;
14. target resolution blocks undeclared, operational, production, or foreign-workspace stores;
15. fixtures and seeds are attributable, scoped, and free of undeclared governed data and secrets;
16. migration serialization and stale-lock recovery are tested;
17. rollback is proven safe or forward repair and restoration are proven;
18. cross-component releases preserve component-owned execution and compatibility windows;
19. no mutable local store, dump, snapshot, or manually edited history enters an active release;
20. release packages contain preflight, order, health, evidence, and recovery behavior;
21. staged execution and product activation remain separate from development execution;
22. migration evidence is complete and minimizes governed payloads;
23. cleanup removes workspace-owned mutable state and credentials without affecting other targets;
24. failures remain workspace-scoped or staged-target-scoped;
25. profile-specific engine and deployment choices remain profile-scoped;
26. no unresolved marker, duplicate migration authority, or cross-owner write exists;
27. required conformance tests and evidence resolve through traceability;
28. the active text contains the complete required section structure.

Applicable failure codes include:

`text
development_database_identity_missing
development_database_identity_duplicate
workspace_database_collision
shared_mutable_database_state
component_database_owner_mismatch
cross_component_migration_write
migration_identifier_duplicate
released_migration_modified
migration_target_unresolved
migration_target_forbidden
migration_lock_conflict
migration_restart_unsafe
migration_validation_failed
supported_upgrade_path_missing
fixture_governed_data_violation
fixture_secret_exposure
rollback_safety_unproven
forward_repair_missing
required_backup_missing
cross_component_migration_coordination_failed
mutable_database_promoted
migration_release_metadata_missing
migration_evidence_missing
workspace_database_cleanup_incomplete
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Parallel PostgreSQL workspaces

Two branches run the same component against one PostgreSQL server.

Each workspace uses a different database, service identity, port-facing service namespace, migration history, and volume inventory. A migration in one branch cannot see or alter the other branch's schema.

### Example 2 — Embedded SQLite component

A component uses SQLite for local development.

The database file resides under the workspace-owned component data root. Tests create fresh copies, execute migrations, validate restart behavior, and delete the files during cleanup.

### Example 3 — Shared engine, separate owners

Orgo and Konnaxion use separate schemas in one development database process.

Each service identity writes only its own schema. The release coordinator orders their migrations but cannot run cross-schema mutation as a shortcut.

### Example 4 — Released migration defect

A migration published in a services release contains an incomplete backfill.

The file is not edited. A new repair migration identifies the affected prior migration, completes the transformation, validates the result, and records evidence.

### Example 5 — Unsafe reversal

A migration transforms and consolidates historical records.

Testing shows that a down migration would lose accepted state. The release package omits false rollback claims and instead defines backup restoration, forward repair, health gates, and operator decision points.

### Example 6 — WSL database

A Windows developer runs PostgreSQL inside WSL.

The workspace, volume, credentials, and Unix socket remain in the Linux boundary. A Windows database client can connect only through an explicitly configured local endpoint using development credentials.

### Example 7 — Interrupted migration

A long backfill is stopped halfway through.

The migration resumes from durable progress, skips already validated records, retains one component-owned migration lock, and reports completion only after all validation checks pass.

### Example 8 — Development-to-release transition

A developer validates a migration locally.

Build Farm recreates empty and supported-prior-version targets from declared inputs, runs interruption and restore tests, and publishes an immutable migration package with evidence. Operations later executes that package against an authorized staged target and activates the service only after health gates pass.
