<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "authoritative_storage",
    "component_data_ownership",
    "shared_storage_infrastructure",
    "replication_and_projections",
    "backup_and_restore",
    "workspace_storage",
    "artifact_and_evidence_storage"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
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
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SEC-STOR-001",
    "REQ-SEC-STOR-002",
    "REQ-SEC-STOR-003",
    "REQ-SEC-STOR-004",
    "REQ-SEC-STOR-005",
    "REQ-SEC-STOR-006",
    "REQ-SEC-STOR-007",
    "REQ-SEC-STOR-008",
    "REQ-SEC-STOR-009",
    "REQ-SEC-STOR-010",
    "REQ-SEC-STOR-011",
    "REQ-SEC-STOR-012",
    "REQ-SEC-STOR-013",
    "REQ-SEC-STOR-014",
    "REQ-SEC-STOR-015",
    "REQ-SEC-STOR-016",
    "REQ-SEC-STOR-017",
    "REQ-SEC-STOR-018",
    "REQ-SEC-STOR-019",
    "REQ-SEC-STOR-020",
    "REQ-SEC-STOR-021",
    "REQ-SEC-STOR-022",
    "REQ-SEC-STOR-023",
    "REQ-SEC-STOR-024",
    "REQ-SEC-STOR-025",
    "REQ-SEC-STOR-026",
    "REQ-SEC-STOR-027",
    "REQ-SEC-STOR-028",
    "REQ-SEC-STOR-029",
    "REQ-SEC-STOR-030",
    "REQ-SEC-STOR-031",
    "REQ-SEC-STOR-032",
    "REQ-SEC-STOR-033",
    "REQ-SEC-STOR-034",
    "REQ-SEC-STOR-035",
    "REQ-SEC-STOR-036",
    "REQ-SEC-STOR-037",
    "REQ-SEC-STOR-038",
    "REQ-SEC-STOR-039",
    "REQ-SEC-STOR-040",
    "REQ-SEC-STOR-041",
    "REQ-SEC-STOR-042",
    "REQ-SEC-STOR-043",
    "REQ-SEC-STOR-044",
    "REQ-SEC-STOR-045",
    "REQ-SEC-STOR-046",
    "REQ-SEC-STOR-047",
    "REQ-SEC-STOR-048",
    "REQ-SEC-STOR-049",
    "REQ-SEC-STOR-050",
    "REQ-SEC-STOR-051",
    "REQ-SEC-STOR-052",
    "REQ-SEC-STOR-053",
    "REQ-SEC-STOR-054"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-003",
    "DOC-DEV-013",
    "DOC-LIFE-007",
    "DOC-LIFE-009",
    "DOC-LIFE-010",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-008"
  ],
  "tags": [
    "security",
    "storage-boundaries",
    "data-ownership",
    "authoritative-store",
    "database-isolation",
    "replicas",
    "caches",
    "indexes",
    "backup",
    "restore",
    "artifact-store",
    "evidence-store",
    "workspace-storage",
    "portability"
  ]
}
KOA:DOC-META:END -->

# Storage Boundaries

> **Document status:** Normative security architecture.
> **Primary invariant:** Physical co-location does not create shared authority.
> **Authority rule:** Every authoritative data set has one owner, one declared write boundary, and one owner-approved lifecycle.

## 1. Purpose

This document defines storage security boundaries across kOA components, profiles, workspaces, artifacts, evidence, backups, replicas, caches, indexes, temporary storage, and external storage services.

A storage boundary determines:

- who owns the stored data;
- which identity can write it;
- which identities can read it;
- whether the stored copy is authoritative, derived, replicated, archived, or temporary;
- which tenant, domain, profile, and component scope applies;
- how the data is migrated, replicated, backed up, restored, exported, deleted, and recovered;
- what happens when storage is unavailable, exhausted, corrupted, or unverifiable.

The physical storage technology does not determine authority.

One server, database engine, filesystem, object store, queue cluster, search service, or backup device can host several logically separate boundaries only when ownership and enforcement remain explicit.

## 2. Scope

### 2.1 Included scope

This document applies to:

- component-owned relational and non-relational databases;
- filesystems and persistent volumes;
- object stores and artifact stores;
- queues, streams, logs, and event persistence;
- caches, indexes, search services, and materialized projections;
- local and remote replicas;
- audit and evidence stores;
- backup, archive, restore, portability, and exit storage;
- development workspace storage;
- temporary, staging, spool, scratch, and migration storage;
- external managed storage services;
- storage used in connected, controlled-network, intermittent, and disconnected deployments.

### 2.2 Excluded ownership

This document does not own:

| Fact | Canonical owner |
| --- | --- |
| Component business-data schemas and domain semantics | Component contract |
| Exact profile topology and physical storage implementation | Active profile contract |
| Exact encryption algorithms and key handling | Data-at-rest, secrets, identity, and trust contracts |
| Migration algorithms and state transitions | Component migration contract |
| Backup schedule, RPO, RTO, and operational runbook | Operations and profile contracts |
| Artifact integrity and activation | Artifact and lifecycle contracts |
| External provider behavior | Integration manifest |
| Resource capacity and I/O scheduling | Resource Governor and resource envelopes |
| Governed access, disclosure, consent, and exceptions | Governance Policy Runtime |

### 2.3 Boundary classes

The storage architecture recognizes these classes:

`text
authoritative component storage
canonical registry storage
artifact storage
audit and evidence storage
replica storage
projection, cache, and index storage
backup and archive storage
workspace storage
temporary and staging storage
external managed storage
`

Each stored object belongs to one declared class.

## 3. Canonical References

### 3.1 Canonical ownership

| Canonical source | Owned information |
| --- | --- |
| `generated/component-catalog.json` and component contracts | Component identity, authoritative data ownership, interfaces, migrations, and failure behavior |
| `generated/profile-catalog.json` and profile contracts | Physical separation, storage layout, capacity, encryption posture, backup target, and offline requirements |
| `contracts/system.contract.json#/capability_degradation` | Storage failure, read-only degradation, restoration, and preserved-state behavior |
| `contracts/artifact-classes.contract.json` | Artifact, receipt, bundle, and activation lifecycle |
| `contracts/release-channels.contract.json` | Channel identity and compatibility of stored release artifacts |
| `contracts/integration-types.contract.json` | External storage integration scope, credentials, retention, removal, and failure |
| `generated/requirements-index.json` | Normative storage obligations |
| `generated/assertion-index.json` | Data ownership, profile scope, workspace isolation, and lifecycle invariants |
| `generated/exception-index.json` | Approved bounded deviations |

### 3.2 Core invariant references

The applicable global rules include:

`text
one authoritative owner per data set
no direct cross-component authoritative writes
declared interfaces preserve provenance
backup, restore, portability, and credible exit
storage failure blocks unsafe writes
cache and replica unavailability never transfers authority
profile-specific physical separation remains profile-scoped
`

### 3.3 Relationship to data at rest

This document defines separation and authority.

The data-at-rest security contract defines encryption and cryptographic protection details. A storage boundary is not conformant merely because its media is encrypted.

## 4. Model and Responsibilities

### 4.1 Authority classes

| Authority class | Meaning | Write behavior |
| --- | --- | --- |
| `authoritative` | The current source of truth owned by one component or registry | Only the owning write identity and owner-approved procedures |
| `canonical_artifact` | Immutable published artifact or bundle | Created through artifact lifecycle; never edited in place |
| `audit_or_evidence` | Receipt, evidence, or append-only security record | Written only through its owning evidence or audit interface |
| `replica` | Copy maintained from an authoritative source | No independent domain writes |
| `projection` | Derived representation for presentation, search, reporting, or interoperability | Rebuilt from source; no authoritative write-back |
| `cache` | Disposable acceleration copy | Invalidated or rebuilt from source |
| `backup` | Recovery copy of identified source state | Read during verification and restore only |
| `archive` | Retained historical state | No ordinary operational writes |
| `workspace` | Development-owned mutable state isolated by `workspace_id` | Only the owning workspace and component interfaces |
| `temporary` | Staging, spool, scratch, or transaction support | Bounded lifetime; never authority by persistence |
| `external_managed` | Storage supplied by an external service | Authority depends on the owning component and profile, never on the provider |

### 4.2 Owner and operator distinction

The data owner defines:

- data semantics;
- authoritative identity;
- write interfaces;
- schema and migration ownership;
- validation;
- retention and deletion;
- replication and backup behavior;
- restore and recovery;
- export and portability.

A storage operator can provision capacity, monitor health, apply bounded maintenance, and execute owner-approved procedures.

Operator access does not make the operator the data owner.

### 4.3 Physical and logical separation

Physical co-location is permitted only when logical separation remains enforceable.

For a shared relational service, separation includes:

- separate databases or schemas;
- separate database users or service identities;
- separate write grants;
- separate migration ownership;
- separate backup inventory;
- observable ownership;
- prohibited cross-component writes.

For a shared object store, separation includes:

- separate buckets or prefixes;
- separate credentials and policies;
- separate object lifecycle and retention;
- separate inventory and deletion authority;
- distinct encryption scope where required.

For a shared filesystem, separation includes:

- separate ownership and write permissions;
- explicit mounts or path boundaries;
- separate retention and cleanup;
- no broad shared writable parent used as an authority shortcut.

For sovereign and high-assurance profiles, separate storage identities are mandatory. Separate service instances are preferred where the profile determines that the risk and operating envelope justify them.

### 4.4 Storage-domain map

| Domain | Typical content | Authority |
| --- | --- | --- |
| Component domain | Cases, tasks, knowledge objects, runtime state, component configuration | Owning component |
| Identity and trust domain | Identities, certificates, delegations, trust references | Identity and Trust |
| Governance domain | Policy bundles, decisions, rights, consent, exceptions | Governance authorities |
| Resource domain | Active resource envelopes, allocations, queue metadata | Resource Governor for resource state |
| Audit and evidence domain | Receipts, evidence references, incident records | Audit or evidence authority |
| Artifact domain | Immutable packages, bundles, manifests, SBOMs, provenance | Artifact lifecycle authority |
| Workspace domain | Source checkout, `.venv`, local services, development data | Workspace and component contracts |
| Backup and archive domain | Protected recovery and historical copies | Source owner plus backup authority |
| External integration domain | Provider-held or provider-mediated copies | Source owner retains authority; integration contract constrains provider |

One physical system can host multiple domains only when their identities and controls remain distinct.

### 4.5 Replica and failover model

A replica is not an alternate owner.

Every replica declares:

- source authority;
- replication direction;
- consistency and lag;
- state-version identity;
- read behavior;
- write prohibition;
- failover eligibility;
- promotion authority;
- fencing and single-writer enforcement;
- reconciliation and demotion.

Failover can transfer active write responsibility only through an owner-approved procedure. It does not transfer component ownership.

A replica with unknown freshness is not presented as current authoritative state.

### 4.6 Projection, cache, and index model

A projection, cache, or index records:

- source component;
- source object or version;
- derivation;
- generated time;
- freshness policy;
- invalidation;
- rebuild procedure;
- permitted readers;
- prohibited write-back.

If the source owner is unavailable, a verified projection can remain readable only when its contract permits read-only use and its provenance and freshness are visible.

It cannot accept authoritative mutation.

### 4.7 Artifact and evidence storage

Artifact stores preserve immutable identity and integrity.

A stored artifact has distinct states such as:

`text
candidate
admitted
staged
active
rejected
revoked
archived
`

Storage presence does not change lifecycle state.

Audit and evidence stores retain only the evidence needed for policy, incident response, lifecycle, or conformance. They do not become shadow operational databases.

### 4.8 Backup and archive model

Backups are:

- source-identified;
- tenant- and domain-scoped;
- integrity-protected;
- encryption-scoped;
- versioned or checkpointed;
- retention-governed;
- inventory-complete;
- restorable into a clean compatible boundary;
- tested by restore.

Immutable artifacts can be referenced rather than duplicated only when their independent availability and exact identity are guaranteed by the backup contract.

Archives preserve historical state and legal or operational retention. They do not participate in ordinary writes or routing.

### 4.9 Restore model

Restore creates a candidate recovered state.

The recovered state remains non-authoritative until validation confirms:

- backup identity and integrity;
- source owner and scope;
- tenant and domain;
- decryption and trust continuity;
- schema and migration compatibility;
- artifact and Release Set compatibility;
- policy, rights, and consent state;
- component write identities;
- queue and event state;
- application-level invariants;
- absence of a newer conflicting authoritative state.

Restore activation uses one owner-approved atomic boundary.

### 4.10 Workspace storage

The `workspace_id` namespaces:

- writable source checkout;
- mutable dependency environment;
- databases and schemas;
- database identities;
- volumes and writable paths;
- queues and indexes;
- sockets and PID files;
- logs and temporary directories;
- secrets and local certificates;
- resource allocations.

A shared content-addressed cache can be used across workspaces. A shared mutable installed environment cannot.

### 4.11 External storage

An external managed storage service is used only through:

- an active profile declaration;
- an integration manifest;
- scoped credentials;
- declared data classes;
- location and retention controls;
- export and deletion behavior;
- outage and removal behavior;
- credible exit.

The provider does not become the data owner.

A profile claiming offline continuity preserves the authoritative data required for that capability without relying exclusively on an unavailable external provider.

### 4.12 Capacity and failure safety

Storage capacity and I/O are governed resources.

Before exhaustion threatens durability, the system can:

- reject new heavy writes;
- reduce optional logging;
- pause indexes or rebuilds;
- queue bounded work;
- suspend optional services;
- preserve required recovery capacity;
- enter read-only mode where declared.

The system never silently truncates, discards, or partially commits authoritative data to remain available.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-SEC-STOR-001,REQ-SEC-STOR-002,REQ-SEC-STOR-003,REQ-SEC-STOR-004,REQ-SEC-STOR-005,REQ-SEC-STOR-006,REQ-SEC-STOR-007,REQ-SEC-STOR-008,REQ-SEC-STOR-009,REQ-SEC-STOR-010,REQ-SEC-STOR-011,REQ-SEC-STOR-012,REQ-SEC-STOR-013,REQ-SEC-STOR-014,REQ-SEC-STOR-015,REQ-SEC-STOR-016,REQ-SEC-STOR-017,REQ-SEC-STOR-018,REQ-SEC-STOR-019,REQ-SEC-STOR-020,REQ-SEC-STOR-021,REQ-SEC-STOR-022,REQ-SEC-STOR-023,REQ-SEC-STOR-024,REQ-SEC-STOR-025,REQ-SEC-STOR-026,REQ-SEC-STOR-027,REQ-SEC-STOR-028,REQ-SEC-STOR-029,REQ-SEC-STOR-030,REQ-SEC-STOR-031,REQ-SEC-STOR-032,REQ-SEC-STOR-033,REQ-SEC-STOR-034,REQ-SEC-STOR-035,REQ-SEC-STOR-036,REQ-SEC-STOR-037,REQ-SEC-STOR-038,REQ-SEC-STOR-039,REQ-SEC-STOR-040,REQ-SEC-STOR-041,REQ-SEC-STOR-042,REQ-SEC-STOR-043,REQ-SEC-STOR-044,REQ-SEC-STOR-045,REQ-SEC-STOR-046,REQ-SEC-STOR-047,REQ-SEC-STOR-048,REQ-SEC-STOR-049,REQ-SEC-STOR-050,REQ-SEC-STOR-051,REQ-SEC-STOR-052,REQ-SEC-STOR-053,REQ-SEC-STOR-054
renderer=requirements-list-v1
-->
- **REQ-SEC-STOR-001 — SHALL:** Every authoritative data set have exactly one owning component or canonical registry.
- **REQ-SEC-STOR-002 — SHALL:** Every storage location declare its owner, data classes, authority class, tenant or domain scope, permitted readers, permitted writers, retention, recovery behavior, and active profile.
- **REQ-SEC-STOR-003 — SHALL:** Storage authority derive from component, registry, artifact, profile, and policy contracts rather than from physical location, database engine, file path, administrator access, or deployment convenience.
- **REQ-SEC-STOR-004 — SHALL NOT:** A shared database process, storage device, object store, filesystem, cache, queue, search engine, backup target, or replica create shared authoritative ownership.
- **REQ-SEC-STOR-005 — SHALL NOT:** A component write directly into another component's authoritative database, schema, table, collection, bucket, object prefix, file tree, queue, index, or source record.
- **REQ-SEC-STOR-006 — SHALL:** Cross-component reads and writes use declared interfaces, events, contracts, import procedures, or gateways that preserve source authority and provenance.
- **REQ-SEC-STOR-007 — SHALL:** Each authoritative store have a distinct write identity and an access-control boundary enforceable independently of other components.
- **REQ-SEC-STOR-008 — SHALL:** A physically shared relational database preserve separate component databases or schemas, separate database identities, separate migration ownership, and prohibited cross-component writes.
- **REQ-SEC-STOR-009 — SHALL:** A physically shared object store preserve separate component buckets or prefixes, credentials, policies, lifecycle rules, inventory, and deletion authority.
- **REQ-SEC-STOR-010 — SHALL:** A physically shared filesystem preserve separate ownership, write permissions, mount boundaries, retention, and cleanup responsibility.
- **REQ-SEC-STOR-011 — SHALL:** A physically shared queue, cache, or search service preserve separate namespaces, credentials, quotas, ownership, and prohibited authoritative cross-writes.
- **REQ-SEC-STOR-012 — SHALL:** Sovereign and high-assurance deployments use separate storage identities for each component and security domain.
- **REQ-SEC-STOR-013 — SHOULD:** Sovereign and high-assurance deployments use separate database or storage service instances when practical and justified by the active profile.
- **REQ-SEC-STOR-014 — SHALL:** Profile-specific physical separation requirements remain owned by the active profile and shall not become universal system requirements.
- **REQ-SEC-STOR-015 — SHALL:** Authoritative storage, replicas, projections, caches, indexes, backups, archives, evidence stores, artifact stores, workspaces, and temporary storage be explicitly classified.
- **REQ-SEC-STOR-016 — SHALL NOT:** A replica, cache, projection, index, search result, export, backup, archive, integration mirror, or AI-held copy acquire authority because the owner is unavailable.
- **REQ-SEC-STOR-017 — SHALL:** A projection or cache record its source owner, source identity or version, derivation, freshness, invalidation, rebuild, and write-back prohibition.
- **REQ-SEC-STOR-018 — SHALL:** A replica declare replication direction, source authority, consistency model, lag tolerance, promotion prohibition or promotion procedure, conflict behavior, and recovery behavior.
- **REQ-SEC-STOR-019 — SHALL NOT:** A replica be promoted to authoritative ownership without an explicit owner-approved failover procedure that preserves component identity, trust, data version, and write exclusivity.
- **REQ-SEC-STOR-020 — SHALL:** A cache or index be disposable and reproducible from authoritative inputs unless a separate artifact contract explicitly classifies it otherwise.
- **REQ-SEC-STOR-021 — SHALL NOT:** Loss of a cache, index, or derived projection cause loss of the authoritative source record.
- **REQ-SEC-STOR-022 — SHALL:** Artifact stores preserve immutable artifact identities, channel classification, provenance, integrity material, lifecycle state, and activation authority boundaries.
- **REQ-SEC-STOR-023 — SHALL NOT:** Presence of an artifact in a local or remote store make it admitted, active, compatible, or authoritative.
- **REQ-SEC-STOR-024 — SHALL:** Audit and evidence stores preserve immutable or append-only behavior required by their contracts while excluding unnecessary authoritative business payload.
- **REQ-SEC-STOR-025 — SHALL NOT:** An audit or evidence store become the operational source of truth for a component's domain objects.
- **REQ-SEC-STOR-026 — SHALL:** Secret values and private keys use the approved secret or key storage boundary and shall not be stored in ordinary databases, object stores, logs, caches, backups, artifacts, or workspaces without an explicit secret-storage contract.
- **REQ-SEC-STOR-027 — SHALL:** Storage encryption, key ownership, key scope, rotation, revocation, recovery, and cryptographic erasure behavior comply with the applicable data-at-rest and secrets contracts.
- **REQ-SEC-STOR-028 — SHALL:** Storage access be limited by component identity, tenant or domain, purpose, role, data class, and operation.
- **REQ-SEC-STOR-029 — SHALL NOT:** Host administrator, database administrator, storage administrator, backup operator, or infrastructure service identity imply application-level data authority.
- **REQ-SEC-STOR-030 — SHALL:** Privileged storage maintenance use the active profile's approved narrow privileged path and applicable identity and policy authority.
- **REQ-SEC-STOR-031 — SHALL:** Storage migrations be owned and executed through the authoritative component's approved migration interface or procedure.
- **REQ-SEC-STOR-032 — SHALL NOT:** A deployment tool, repair tool, reporting service, integration, or operator edit another component's authoritative store outside an explicitly authorized owner procedure.
- **REQ-SEC-STOR-033 — SHALL:** Every authoritative write be atomic at the data owner's declared transaction boundary or use a declared idempotent, compensating, or forward-repair procedure.
- **REQ-SEC-STOR-034 — SHALL:** Partial writes, failed migrations, and incomplete artifact activation preserve the previous verified authoritative state or enter an explicit blocked or restoring state.
- **REQ-SEC-STOR-035 — SHALL:** Storage exhaustion, quota exhaustion, durability loss, or write-path failure block new authoritative writes before silent truncation, overwrite, corruption, or partial commit.
- **REQ-SEC-STOR-036 — SHALL:** Resource Governor enforce storage capacity, I/O, queue, worker, concurrency, and heavy-operation envelopes without becoming the data owner.
- **REQ-SEC-STOR-037 — SHALL NOT:** Resource Governor substitute for Governance Policy Runtime or Governance Policy Runtime substitute for Resource Governor in storage access or recovery decisions.
- **REQ-SEC-STOR-038 — SHALL:** Backups preserve component, tenant, domain, data-class, retention, rights, consent, trust, and encryption boundaries.
- **REQ-SEC-STOR-039 — SHALL:** Every backup identify the authoritative source, source version or checkpoint, included and excluded data classes, integrity state, encryption context, retention, and restore prerequisites.
- **REQ-SEC-STOR-040 — SHALL NOT:** A backup success claim be made until the backup is durably stored, integrity-protected, inventory-complete, and verifiable.
- **REQ-SEC-STOR-041 — SHALL:** Restore occur into a clean compatible boundary and remain non-authoritative until identity, trust, schema, migration, policy, ownership, integrity, completeness, and application-level validation pass.
- **REQ-SEC-STOR-042 — SHALL NOT:** A restored cache, replica, backup, archive, export, or snapshot overwrite a newer authoritative owner state without an explicit owner-approved restore transaction.
- **REQ-SEC-STOR-043 — SHALL:** Restore and disaster-recovery procedures preserve separate component write identities and prohibit accidental multi-writer activation.
- **REQ-SEC-STOR-044 — SHALL:** Authoritative user and tenant data support governed export, backup, restore, portability, deletion, and credible exit according to the owning contracts.
- **REQ-SEC-STOR-045 — SHALL:** Export packages preserve source ownership, schema and version identity, provenance, rights, consent, retention, and import validation requirements.
- **REQ-SEC-STOR-046 — SHALL NOT:** Export, portability, or exit material include unrelated tenants, secret values, private signing keys, or data classes outside the authorized scope.
- **REQ-SEC-STOR-047 — SHALL:** Workspace storage namespace writable paths, databases, volumes, queues, caches, secrets, sockets, logs, and temporary state by `workspace_id`.
- **REQ-SEC-STOR-048 — SHALL NOT:** Two active workspaces share mutable installed environments, writable component data, database write identities, volume ownership, queue identities, secrets, or exclusive allocations.
- **REQ-SEC-STOR-049 — MAY:** Workspaces share immutable, read-only, or content-addressed caches that remain disposable, non-authoritative, and isolated from installed mutable environments.
- **REQ-SEC-STOR-050 — SHALL:** Temporary, staging, spool, scratch, and failed-activation storage have bounded lifetime, explicit ownership, cleanup, recovery, and prohibition from becoming authoritative by persistence.
- **REQ-SEC-STOR-051 — SHALL:** External storage services be declared through the active profile and integration contracts, use minimum scoped credentials, preserve owner authority, and define failure, removal, export, and deletion behavior.
- **REQ-SEC-STOR-052 — SHALL NOT:** A deployment claiming offline continuity make an unavailable external storage service the sole holder of authoritative state required for the claimed offline capability.
- **REQ-SEC-STOR-053 — SHALL:** Recovery revalidate storage identities, owners, write exclusivity, schemas, versions, migrations, replicas, caches, backups, queues, resources, policy, and receipts before normal mutation resumes.
- **REQ-SEC-STOR-054 — SHALL:** Storage-boundary conformance test ownership, identity separation, direct-write prohibition, shared-infrastructure isolation, replica and cache non-authority, backup and restore, workspace separation, exhaustion behavior, offline continuity, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Register a storage boundary

1. resolve the owning component or registry;
2. identify the authority class;
3. identify profile, tenant, domain, and data classes;
4. declare physical and logical location;
5. declare read and write identities;
6. declare schema, namespace, and migration owner;
7. declare encryption and key references;
8. declare retention, deletion, backup, restore, export, and recovery;
9. declare capacity and resource envelope;
10. validate absence of authority overlap;
11. activate the boundary only after controls pass.

### 6.2 Provision shared infrastructure

For a shared database, object store, filesystem, queue, cache, or search service:

1. establish infrastructure identity and operator scope;
2. allocate separate component namespaces;
3. create separate credentials and write grants;
4. deny cross-component writes;
5. assign migration and cleanup ownership;
6. assign quotas and resource limits;
7. configure backup inventory by owner and data class;
8. test independent failure and removal;
9. record the shared-infrastructure relationship without changing data ownership.

### 6.3 Write authoritative data

An authoritative write follows:

`text
resolve owner and target
→ authenticate writer
→ evaluate applicable policy
→ validate input and current version
→ commit at owner transaction boundary
→ verify postcondition
→ emit required event or receipt
`

A failed check leaves the previous authoritative state intact or invokes the owner's declared idempotent, compensating, or forward-repair procedure.

### 6.4 Build or refresh a projection

1. resolve the source owner and permitted source version;
2. read through a declared interface or approved export;
3. record provenance and derivation;
4. build into non-authoritative storage;
5. validate completeness and freshness;
6. atomically replace the prior projection;
7. preserve write-back prohibition;
8. expose source identity and freshness to consumers.

### 6.5 Replicate data

1. resolve source and replica identities;
2. verify one-way or declared multi-stage replication direction;
3. verify compatible schema and state versions;
4. transfer through the approved replication interface;
5. record checkpoints and lag;
6. verify replica integrity;
7. preserve single-writer authority;
8. reconcile after interruption.

### 6.6 Back up

1. resolve source owners and exact included scope;
2. quiesce, checkpoint, or use an owner-approved consistent snapshot;
3. inventory all included and excluded data classes;
4. preserve schema, version, policy, rights, consent, and trust references;
5. encrypt and integrity-protect the backup;
6. transfer to the approved backup boundary;
7. verify durability and inventory completeness;
8. record backup evidence;
9. test restore according to the operational schedule.

### 6.7 Restore

1. provision a clean compatible target boundary;
2. verify backup identity, integrity, encryption, and scope;
3. resolve current owner and restore authority;
4. verify no newer conflicting authoritative state will be overwritten;
5. restore component boundaries with separate write identities;
6. apply owner-approved migrations;
7. rebuild disposable projections and indexes;
8. reconcile queues, events, replicas, and artifact references;
9. execute component-level validation;
10. enter `restoring`;
11. activate the restored boundary atomically only after all checks pass.

### 6.8 Fail over a replica

1. detect and confirm source failure;
2. fence the prior writer;
3. resolve replica freshness and required recovery point;
4. resolve owner, identity, policy, and operator authority;
5. reconcile pending writes and replication checkpoints;
6. promote through the owner-approved procedure;
7. activate exactly one writer;
8. validate component behavior;
9. record failover evidence;
10. keep the original source fenced until reconciliation and demotion complete.

### 6.9 Retire or delete storage

1. stop new writes;
2. verify retention, legal, rights, consent, and evidence requirements;
3. export or back up required state;
4. revoke write identities and credentials;
5. detach replicas, projections, and integrations;
6. delete or cryptographically erase according to contract;
7. verify deletion within the owned scope;
8. preserve required deletion evidence;
9. ensure unrelated component and tenant storage remains unchanged.

### 6.10 Recover from exhaustion or write-path failure

1. block unsafe authoritative writes;
2. preserve the last durable state;
3. classify affected capabilities;
4. protect recovery and receipt capacity;
5. free only disposable or owner-approved data;
6. expand or replace storage through the active profile;
7. verify durability and ownership;
8. reconcile partial operations and queues;
9. enter `restoring`;
10. resume writes only after post-recovery validation.

## 7. Failure States and Safe Degradation

| Failure condition | Required state or response | Preserved behavior |
| --- | --- | --- |
| Authoritative writer identity unresolved | `blocked` | Verified read-only access when declared |
| Storage authorization or policy unresolved | `blocked` | Unrelated owners and stores |
| Write path unavailable | Write capability `blocked` | Last durable authoritative state |
| Capacity or quota exhausted | Block writes before corruption; reduce optional work | Required reads and recovery operations |
| Durability cannot be verified | Block commit acknowledgment | Previous verified state |
| Shared database process unavailable | Block dependent component stores | Components using independent storage |
| One component namespace corrupted | Isolate affected namespace | Other component namespaces when separation remains verified |
| Replica lag unknown | Remove current-state claim | Source authority and other verified replicas |
| Primary unavailable | Keep replica read-only until failover procedure passes | Verified replicated reads where permitted |
| Cache unavailable | Rebuild or bypass | Authoritative source |
| Cache stale or unverifiable | Invalidate; do not present as current | Source owner |
| Search index unavailable | Degrade search | Direct owner retrieval |
| Backup target unavailable | Backup `blocked` or `queued` | Active authoritative state |
| Backup integrity fails | Reject backup | Prior verified backups and source |
| Restore validation fails | Remain `restoring` or `blocked` | Last verified active state |
| Artifact store unavailable | Block affected admission or activation | Active verified artifacts |
| Evidence store unavailable | Keep receipt-before-commit transition uncommitted | Previous authoritative state |
| Secret store unavailable | Block secret-dependent capability | Capabilities not requiring the secret |
| External storage unavailable | Degrade only dependent capability | Local authoritative state required by profile |
| Migration fails | Preserve prior state or enter forward repair | Last verified owner checkpoint |
| Cleanup fails | Retain ownership and block conflicting reuse | Other storage boundaries |
| Cross-component write detected | Stop offending writer and contain affected scope | Unaffected owner states |

Safe degradation never promotes a cache, replica, backup, archive, external service, or operator copy to authority by convenience.

## 8. Cross-Component Interactions

### 8.1 Component owner

The component owner controls writes, migrations, domain validation, retention, export, and restore for its authoritative data.

Infrastructure components cannot redefine those semantics.

### 8.2 Identity and Trust

Identity and Trust resolves component writers, operators, nodes, services, certificates, and trust roots.

A database user or filesystem owner is an implementation identity and must map to an authorized component or operator role.

### 8.3 Governance Policy Runtime

Governance Policy Runtime evaluates governed access, disclosure, consent, rights, deletion, exceptions, and privileged maintenance where applicable.

It does not allocate storage or become the data owner.

### 8.4 Resource Governor

Resource Governor controls storage capacity reservations, I/O, background jobs, queues, and heavy backup, restore, migration, indexing, and replication work.

It does not authorize data access or determine domain retention.

### 8.5 Audit Broker

Audit Broker retains required access, migration, backup, restore, failover, deletion, and incident receipts.

Audit storage remains separate from operational component state.

### 8.6 kOA Node Agent

Where deployed, kOA Node Agent can coordinate volume attachment, service lifecycle, artifact activation, backup, restore, and node recovery.

It acts through owner and profile contracts and does not gain direct domain-data ownership.

### 8.7 Publication and ingestion gateways

kOA Mediatheque admission uses the local component boundary. Cross-domain publication, including publication to external UCKK, uses Publication Gateway and a destination-specific adapter.

Shared storage paths do not bypass disclosure, admission, rights, provenance, or target-owner validation.

### 8.8 External integrations

External storage and synchronization integrations transfer or host only declared data classes under scoped credentials.

Their mirrors, exports, and provider copies remain governed by source ownership and explicit return, deletion, and exit procedures.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- logical data ownership is mandatory;
- every authoritative data set has one owner;
- no component writes directly into another component's authoritative store;
- physical co-location does not create shared authority;
- shared relational infrastructure uses separate databases or schemas and identities;
- sovereign and high-assurance profiles require separate storage identities;
- replicas, caches, indexes, backups, and exports are non-authoritative unless an explicit owner-approved transition changes active write responsibility;
- storage failure blocks unsafe writes before corruption;
- restores remain non-authoritative until verified;
- workspaces isolate all mutable storage by `workspace_id`;
- Resource Governor and Governance Policy Runtime remain separate;
- profile-specific physical mechanisms remain profile-scoped;
- portability and exit preserve ownership and governed scope.

Prohibited assumptions include:

- inferring ownership from a database name or filesystem path;
- granting all components one database superuser for convenience;
- treating read access as write authority;
- treating administrator access as domain authority;
- using foreign keys or cross-schema writes across component owners;
- using a shared bucket without component-scoped credentials and lifecycle rules;
- writing operational state into an audit database;
- treating a search index as the source of truth;
- promoting a stale replica because the primary is unavailable;
- overwriting current state from a backup without owner validation;
- treating encryption as permission to share data;
- including secrets or private signing keys in ordinary backups;
- using production data in a development workspace without explicit controls;
- allowing one workspace cleanup to remove another workspace's volume or database;
- making an external provider the sole holder of offline-required state;
- deleting data because a retention job ran without rights and policy validation;
- applying a high-assurance physical-separation rule globally;
- assuming a successful storage mount proves application readiness or data integrity.

## 10. Validation Criteria

Storage boundaries validate when:

1. every authoritative data set has one registered owner;
2. every store declares authority class, scope, identities, readers, writers, retention, and recovery;
3. component write identities are distinct;
4. direct cross-component writes are technically denied and tested;
5. shared database processes preserve separate databases or schemas and migration ownership;
6. shared object and filesystem storage preserves separate credentials, policies, and cleanup;
7. sovereign and high-assurance profile requirements are satisfied without becoming global;
8. replicas declare direction, lag, failover, and single-writer behavior;
9. caches, projections, and indexes expose provenance and cannot write back;
10. artifact storage preserves immutable identity and lifecycle state;
11. audit and evidence storage does not become operational authority;
12. secret values and private keys are absent from ordinary storage boundaries;
13. privileged maintenance uses the approved bounded path;
14. migrations use owner-approved interfaces;
15. authoritative writes are atomic or have declared recovery;
16. exhaustion and durability failures block unsafe writes;
17. Resource Governor limits storage work without becoming owner;
18. Governance Policy Runtime governs applicable access and exceptions;
19. backup inventory, integrity, encryption scope, retention, and restore prerequisites resolve;
20. restore uses a clean compatible boundary and remains non-authoritative until validated;
21. restored component write identities remain separate;
22. export and portability preserve tenant, domain, rights, consent, and provenance scope;
23. workspace mutable storage remains isolated by `workspace_id`;
24. shared workspace caches remain immutable or content-addressed and disposable;
25. temporary storage cannot become authority by persistence;
26. external storage integrations define outage, removal, export, and deletion;
27. offline-capable profiles retain required local authority;
28. recovery passes through `restoring`;
29. all decisions, requirements, locks, exceptions, tests, and evidence references resolve;
30. no unresolved marker, placeholder, duplicate canonical owner, or ordinary documentation hash appears.

Applicable checks include:

`bash
python docs/tools/check_component_boundaries.py
python docs/tools/check_profile_composition.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 Shared PostgreSQL process

Konnaxion and Orgo use one PostgreSQL process in a lightweight profile.

Each component has a separate database or schema, separate credentials, separate migration ownership, and denied cross-component writes. The shared process does not create a shared data owner.

### 11.2 Sovereign storage identities

A sovereign hub uses separate database service identities and storage identities for Orgo, Konnaxion, identity, governance, and audit domains.

The active profile may additionally require separate service instances. That physical rule remains profile-scoped.

### 11.3 Search projection

A search service indexes Orgo cases through a declared event or export interface.

The index records source versions and can be rebuilt. If Orgo is unavailable, the index can provide a clearly marked read-only projection when permitted, but it cannot accept case changes.

### 11.4 Replica failover

A primary component database fails.

The replica remains read-only until the prior writer is fenced, freshness is verified, the owner-approved failover procedure runs, and exactly one write identity becomes active.

### 11.5 Backup restore

A tenant backup restores into a clean compatible node.

The restored databases remain non-authoritative while schemas, trust, policies, rights, receipts, artifacts, queues, and component invariants are checked. Activation occurs only after the complete restore passes.

### 11.6 Workspace cache

Two developer workspaces share a content-addressed UV cache.

Each workspace still owns its `.venv`, databases, volumes, secrets, and logs. Deleting the cache affects download performance, not installed environments or authoritative component data.

### 11.7 External object storage

A profile stores encrypted artifact copies in a managed object service.

The integration manifest defines scoped credentials, region, retention, deletion, export, outage, and removal. Artifact lifecycle authority remains local, and offline-required active artifacts remain available through the profile's admitted local store.
