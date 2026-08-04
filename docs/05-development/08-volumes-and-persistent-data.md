<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-008",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:build_farm"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/development_isolation",
    "generated/component-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "schemas/developer-workspace.schema.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-DEV-VOL-001",
    "REQ-DEV-VOL-002",
    "REQ-DEV-VOL-003",
    "REQ-DEV-VOL-004",
    "REQ-DEV-VOL-005",
    "REQ-DEV-VOL-006",
    "REQ-DEV-VOL-007",
    "REQ-DEV-VOL-008",
    "REQ-DEV-VOL-009",
    "REQ-DEV-VOL-010",
    "REQ-DEV-VOL-011",
    "REQ-DEV-VOL-012",
    "REQ-DEV-VOL-013",
    "REQ-DEV-VOL-014",
    "REQ-DEV-VOL-015",
    "REQ-DEV-VOL-016",
    "REQ-DEV-VOL-017",
    "REQ-DEV-VOL-018",
    "REQ-DEV-VOL-019",
    "REQ-DEV-VOL-020",
    "REQ-DEV-VOL-021",
    "REQ-DEV-VOL-022"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001"
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
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-PRO-000"
  ],
  "tags": [
    "development",
    "workspaces",
    "volumes",
    "persistent-data",
    "storage-isolation",
    "parallel-workspaces",
    "cleanup",
    "backup",
    "restore"
  ]
}
KOA:DOC-META:END -->

# Volumes and Persistent Data

## 1. Purpose

This document defines the storage-isolation model for development workspaces.

It explains how volumes, host paths, persistent service state, caches, build outputs, temporary data, logs, backups, and restore targets are classified and controlled in the `developer_linux_workstation`, `developer_windows_wsl`, and `build_farm` profiles.

The model exists to make these outcomes deterministic:

- two applications, branches, or worktrees can run concurrently without data collision;
- deleting or resetting one workspace does not damage another workspace;
- component data ownership remains intact in development;
- authoritative state is not mixed with disposable data;
- shared caches do not become shared mutable environments;
- backups and restores remain attributable and testable;
- storage pressure degrades safely;
- development convenience does not create hidden host-global dependencies.

This document does not own exact host paths, volume-driver selection, database-engine configuration, per-profile quota values, or implementation-specific container commands. Those values belong to workspace, profile, component, toolchain, resource, and implementation contracts.

## 2. Scope

This document applies to workspace-scoped storage used by:

- native Linux development;
- Windows development inside WSL2;
- rootless development containers;
- build-farm workers;
- local service dependencies;
- component test environments;
- integration-test environments;
- isolated data migrations;
- artifact builds and validation;
- optional task-activated workbenches.

It covers:

- named volumes;
- bind mounts;
- workspace directories;
- database data directories;
- queue and search-engine state;
- uploaded test fixtures;
- component-owned development data;
- service state;
- caches;
- build outputs;
- logs;
- temporary files;
- backups;
- restore targets;
- orphaned-resource detection;
- cleanup and retention.

It does not govern production data retention, production disaster recovery, release-repository retention, signing-key storage, or user-facing product backup policy except where a development test reproduces those contracts.

Secrets are referenced here only to define their separation from ordinary persistent data. Secret ownership and injection are governed by `05-development/09-secrets-and-local-identities.md`.

Local database identity, schema ownership, and migration execution are expanded in `05-development/11-local-databases-and-migrations.md`.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/system.contract.json#/development_isolation` | Global development-workspace isolation and namespace model. |
| `schemas/developer-workspace.schema.json` | Workspace identity, storage-resource declarations, lifecycle fields, and validation structure. |
| `contracts/profiles/developer-linux-workstation.profile.json` | Native Linux storage topology, permitted services, resource envelope, and isolation implementation. |
| `contracts/profiles/developer-windows-wsl.profile.json` | WSL2 storage boundary, host-interoperability constraints, and supported persistent-service topology. |
| `contracts/profiles/build-farm.profile.json` | Clean-worker, ephemeral-workspace, cache, evidence, and artifact-staging behavior. |
| `contracts/toolchains/python-uv.toolchain.json` | Per-workspace `.venv`, permitted shared UV cache, build-output declarations, and environment cleanup. |
| `generated/component-catalog.json` | Component identities and logical authoritative-data ownership. |
| `contracts/artifact-classes.contract.json` | Artifact identity, staging, evidence, retention, and publication classification. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Cross-workspace, data-ownership, cache, profile, and component alignment invariants. |
| `generated/traceability.json` | Links among decisions, requirements, workspaces, profiles, tests, and evidence. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |
| `generated/evidence-catalog.json` | Storage-isolation, cleanup, backup, restore, migration, and recovery evidence. |

Repository paths and examples in this document are explanatory. A profile or workspace contract owns any path that becomes canonical.

## 4. Model and Responsibilities

### 4.1 Workspace storage identity

Every workspace has one stable `workspace_id`.

The workspace identity namespaces mutable storage resources, including:

- named volumes;
- persistent directories;
- database names or schemas;
- database data directories;
- database users;
- queue state;
- search indexes;
- object-storage test buckets;
- upload directories;
- logs;
- temporary directories;
- sockets and runtime directories;
- generated local certificates;
- backup staging;
- restore staging;
- service-specific cache indexes.

A storage resource also has a `resource_id` that is stable inside the workspace.

The conceptual resource identity is:

```text
workspace_id + resource_id
```

An implementation can transform this identity to meet platform naming limits, but the transformation remains deterministic and collision-resistant.

### 4.2 Storage classes

Every declared storage resource belongs to one class.

| Storage class | Meaning | Authoritative | Default sharing | Default cleanup |
| --- | --- | ---: | --- | --- |
| `authoritative_component_data` | Development instance of data owned by a component contract. | Yes within the development instance | Prohibited | Protected until explicit reset or workspace retirement |
| `durable_service_state` | Mutable state required by a supporting service, such as queue, search, or object-store state. | Service-dependent | Prohibited | Explicit reset or workspace retirement |
| `build_output` | Compiled packages, generated bundles, reports, and candidate artifacts. | No until accepted by an artifact lifecycle | Prohibited | Retain by declared build policy |
| `non_authoritative_cache` | Replaceable content used only to improve performance. | No | Permitted through an explicit cache contract | Evictable |
| `log_and_diagnostic` | Structured logs, traces, crash data, and diagnostics. | Evidence only when registered | Prohibited by default | Time- or size-bounded |
| `temporary` | Intermediate state that is not required after the operation or process completes. | No | Prohibited | Automatic |
| `backup` | Integrity-verifiable copy of declared durable state. | No until selected for restore | Prohibited | Retain by declared backup policy |
| `restore_staging` | Isolated target used to verify a restore before activation. | No | Prohibited | Remove after verified activation or failed-restore retention |
| `test_fixture` | Versioned or generated input used by tests. | No | Read-only sharing permitted when declared | Recreate or retain with test source |
| `export` | Portable output created from a bounded source snapshot. | No | Prohibited unless explicitly published | Retain by export purpose |

The selected workspace schema owns the machine-readable enum and required fields. This table explains the intended distinction.

### 4.3 Storage resource declaration

A workspace storage manifest records for each resource:

- workspace identity;
- resource identity;
- storage class;
- owning component or tool;
- service identity;
- physical implementation;
- mount target;
- access mode;
- data classification;
- lifecycle;
- retention;
- cleanup policy;
- backup eligibility;
- restore procedure reference;
- quota or resource-policy reference;
- migration ownership;
- sharing policy;
- evidence requirements.

A resource absent from the manifest is not presumed safe to delete, share, migrate, or reuse.

### 4.4 Ownership

Component-owned development data retains the same logical owner as production data.

A development profile can consolidate physical services. For example, several components can use one PostgreSQL process. The profile still preserves separate:

- logical databases or schemas;
- component identities;
- permissions;
- migration histories;
- backup mappings;
- restore mappings;
- authoritative write paths.

A volume driver, filesystem owner, database administrator, container engine, or workspace controller does not become the logical data owner.

### 4.5 Access modes

Permitted access modes are conceptually:

- `exclusive_read_write`;
- `exclusive_read_only`;
- `shared_read_only`;
- `shared_cache`;
- `backup_source_read_only`;
- `restore_target_exclusive`.

Authoritative component data and durable service state use exclusive workspace ownership unless a specific component contract defines a safe multi-instance topology.

A read-only fixture or integrity-verifiable cache can be shared only when the sharing contract prevents it from becoming authoritative mutable state.

### 4.6 Named volumes and bind mounts

Named volumes and bind mounts are implementation mechanisms, not authority classes.

A named volume is suitable when:

- lifecycle should follow the workspace resource manifest;
- host path knowledge is unnecessary;
- a service expects a persistent directory;
- rootless ownership mapping is supported;
- cleanup can be verified by resource identity.

A bind mount is suitable when:

- the user intentionally edits source or fixture files;
- the path is declared in the workspace contract;
- host and runtime ownership are compatible;
- the mount does not expose unrelated host state;
- access mode is explicit.

Broad mounts such as a complete home directory, host root, shared global application-data directory, or another workspace root are outside the conforming baseline.

### 4.7 Source, data, and generated output

The source checkout is not used as an implicit home for all mutable service state.

Recommended separation is conceptual:

```text
workspace source
workspace runtime state
workspace persistent component data
workspace service data
workspace logs
workspace temporary data
workspace build output
workspace backup staging
workspace restore staging
```

Generated output that can be reproduced from source and declared inputs remains distinct from authoritative data.

Build output remains distinct from runtime service data.

Logs remain distinct from databases and uploaded source objects.

### 4.8 Shared caches

A shared cache is permitted only when it is non-authoritative and replaceable.

Examples can include:

- UV download cache;
- compiler download cache;
- content-addressed package cache;
- read-only base-image store;
- test-fixture object cache.

A cache contract identifies:

- cache owner;
- cache key semantics;
- integrity check;
- mutation mechanism;
- eviction behavior;
- corruption behavior;
- credential behavior;
- maximum scope;
- consumers.

A shared cache does not contain:

- installed `.venv` environments;
- component databases;
- mutable service state;
- secrets;
- workspace-specific configuration;
- authoritative user data;
- signing material;
- unreleased authoritative artifacts.

Cache loss affects performance, not authority.

### 4.9 Persistent service state

Infrastructure services can require durable state, including:

- PostgreSQL;
- Redis when persistence is enabled;
- message queues;
- Solr;
- Elasticsearch;
- object stores;
- local artifact repositories;
- development mail or event sinks.

Each service state resource is workspace-scoped.

Heavy optional services remain task-activated where the profile requires it. Stopping a service does not transfer or merge its storage with another workspace.

### 4.10 Databases and migrations

Database files are not copied or mounted into another active workspace as an informal migration.

Data movement uses one of:

- component export and import;
- database-native backup and restore;
- verified snapshot and isolated restore;
- declared migration tool;
- versioned seed or fixture process.

A migration records the component owner, source schema version, target schema version, workspace, operation identity, backup, result, and recovery path.

Local database names, roles, schemas, and migration histories remain workspace-scoped.

### 4.11 Logs and diagnostics

Logs and diagnostics have bounded retention.

They do not contain secrets or unrestricted sensitive records.

When diagnostics need sensitive context, the system uses references, redacted values, or a separately controlled evidence artifact.

A log directory can be removed without deleting authoritative component state.

### 4.12 Temporary data

Temporary data is scoped by workspace and operation.

Temporary paths are not shared as a coordination mechanism between unrelated workspaces.

Cleanup occurs after:

- command completion;
- service shutdown;
- job cancellation;
- worker destruction;
- workspace removal;
- expiration;
- explicit recovery.

Uncertain temporary data is quarantined or retained for bounded investigation rather than silently promoted to persistent state.

### 4.13 Backups

Development backups are used for:

- migration safety;
- destructive test preparation;
- restore testing;
- fixture creation through a controlled process;
- incident recovery;
- portability testing.

A backup manifest records:

- backup identity;
- workspace identity;
- component owner;
- source resource;
- data-schema version;
- contract version;
- creation time;
- integrity identity;
- encryption or protection state;
- compatibility;
- retention;
- evidence.

A backup is not a live shared database and is not mounted read-write by multiple workspaces.

### 4.14 Restore staging

Restore is verified before activation.

The preferred flow is:

```text
backup
    ↓
isolated restore target
    ↓
integrity and compatibility validation
    ↓
migration when declared
    ↓
representative read and write tests
    ↓
activation or rejection
```

A failed restore target remains non-authoritative.

Activation avoids partial state.

### 4.15 Workspace cleanup

Workspace cleanup classifies each resource as:

- delete;
- retain;
- export;
- back up then delete;
- quarantine;
- external shared resource, do not delete.

Cleanup verifies ownership through the workspace manifest and implementation metadata.

Name prefix alone is insufficient proof when deleting durable data.

A cleanup report lists every discovered resource and its disposition.

### 4.16 Orphan detection

An orphan is a resource that:

- is labeled or named as workspace-scoped;
- has no active workspace record;
- is not protected by retention or evidence policy;
- is not an approved shared cache;
- is not assigned to migration or recovery.

Orphan detection does not automatically delete data. It produces a reviewable inventory and a proposed disposition.

### 4.17 Resource governance

Storage participates in workspace resource governance.

Applicable controls include:

- volume size;
- filesystem quota;
- database quota;
- cache quota;
- log retention;
- temporary-data limit;
- backup-staging limit;
- I/O priority;
- I/O bandwidth;
- inode or object count;
- cleanup thresholds.

The Resource Governor owns enforcement where integrated. The workspace and profile contracts own declared limits.

Storage pressure does not authorize cross-workspace sharing, test omission, backup corruption, secret exposure, or unsafe cleanup.

### 4.18 WSL2 considerations

In the Windows/WSL2 profile, Linux service state remains inside the declared Linux workspace storage boundary unless a contract explicitly requires Windows-host access.

Performance-sensitive database and service data is not placed in an incidental cross-filesystem path merely for convenience.

Windows-visible exports and source files remain distinct from Linux service data.

A Windows host path is not implicitly trusted or shared across workspaces.

### 4.19 Build-farm considerations

Build-farm workspaces are clean and disposable by default.

Build workers can use:

- ephemeral writable workspaces;
- verified read-only source inputs;
- integrity-verifiable shared caches;
- controlled artifact staging;
- evidence storage;
- bounded diagnostics.

A worker cannot reuse mutable service or application state from an earlier job.

Release candidates and evidence are detached from the worker before sanitization or destruction.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-VOL-001,REQ-DEV-VOL-002,REQ-DEV-VOL-003,REQ-DEV-VOL-004,REQ-DEV-VOL-005,REQ-DEV-VOL-006,REQ-DEV-VOL-007,REQ-DEV-VOL-008,REQ-DEV-VOL-009,REQ-DEV-VOL-010,REQ-DEV-VOL-011,REQ-DEV-VOL-012,REQ-DEV-VOL-013,REQ-DEV-VOL-014,REQ-DEV-VOL-015,REQ-DEV-VOL-016,REQ-DEV-VOL-017,REQ-DEV-VOL-018,REQ-DEV-VOL-019,REQ-DEV-VOL-020,REQ-DEV-VOL-021,REQ-DEV-VOL-022 -->
- **REQ-DEV-VOL-001 — SHALL:** Every development workspace shall declare a stable workspace identity and use it to namespace every mutable volume and persistent-data resource.
- **REQ-DEV-VOL-002 — SHALL:** Every workspace storage resource shall declare its owner, storage class, lifecycle, access mode, retention policy, cleanup policy, and backup eligibility.
- **REQ-DEV-VOL-003 — SHALL NOT:** Two independent workspaces shall not share mutable persistent application or service state.
- **REQ-DEV-VOL-004 — MAY:** Workspaces may share a non-authoritative cache only when its content is integrity-verifiable, replaceable, and unable to act as an installed environment or authoritative data source.
- **REQ-DEV-VOL-005 — SHALL:** Workspace removal shall affect only resources owned by that workspace unless an explicit shared-resource contract authorizes a different disposition.
- **REQ-DEV-VOL-006 — SHALL:** Persistent component data shall preserve the logical data owner, component identity, access controls, migration path, backup mapping, and restore mapping defined by the component and profile contracts.
- **REQ-DEV-VOL-007 — SHALL NOT:** A development volume, bind mount, database directory, cache, backup, or export shall not provide a direct write path into another component's authoritative state.
- **REQ-DEV-VOL-008 — SHALL:** Authoritative or durable service data shall be stored separately from caches, generated artifacts, logs, temporary data, and reproducible derivatives.
- **REQ-DEV-VOL-009 — SHALL:** Temporary data shall have a bounded workspace-local location and a deterministic cleanup condition.
- **REQ-DEV-VOL-010 — SHALL:** Build outputs and generated artifacts shall be stored outside authoritative application-data volumes and shall declare whether they are disposable, retained evidence, or release candidates.
- **REQ-DEV-VOL-011 — SHALL:** Sensitive persistent data shall use the encryption, permissions, and identity controls required by the selected profile and data classification.
- **REQ-DEV-VOL-012 — SHALL NOT:** Secrets shall not be stored in ordinary persistent-data volumes, source trees, caches, build-output directories, logs, or unencrypted backups.
- **REQ-DEV-VOL-013 — SHALL:** Every destructive cleanup, reset, or volume-removal operation shall verify workspace ownership before deleting data.
- **REQ-DEV-VOL-014 — SHALL:** A persistent-data reset shall require an explicit target, an explicit scope, and an observable result.
- **REQ-DEV-VOL-015 — SHALL:** Backups of development authoritative or durable service state shall identify the workspace, component owner, data-schema version, source volume, creation time, integrity result, and restore compatibility.
- **REQ-DEV-VOL-016 — SHALL:** Restore operations shall use an isolated target or verified stopped state and shall complete validation before restored data becomes authoritative.
- **REQ-DEV-VOL-017 — SHALL:** Irreversible development data migrations shall be declared before execution and shall have a verified backup and a forward-repair procedure.
- **REQ-DEV-VOL-018 — SHALL:** Parallel applications, branches, and worktrees shall run without volume-name, mount-path, database-directory, socket, log-directory, temporary-directory, or persistent-state collisions.
- **REQ-DEV-VOL-019 — SHALL:** Volume and persistent-data quotas, I/O controls, and retention limits shall be enforceable per workspace through the selected profile and Resource Governor integration.
- **REQ-DEV-VOL-020 — SHALL:** A workspace storage manifest shall be sufficient to identify owned resources, detect orphaned resources, and distinguish safe cleanup from protected retention.
- **REQ-DEV-VOL-021 — SHALL NOT:** An undeclared host path or user-global mutable directory shall become an implicit dependency of a conforming workspace.
- **REQ-DEV-VOL-022 — SHALL:** Storage failure, quota exhaustion, or cleanup uncertainty shall preserve existing authoritative data, stop unsafe mutations, and expose an accurate degraded state.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Provisioning workspace storage

Provisioning follows this order:

1. validate the workspace identity;
2. load the selected profile and workspace contract;
3. resolve component and service ownership;
4. generate the storage manifest;
5. detect naming or path collisions;
6. create workspace-scoped identities and permissions;
7. create volumes and directories;
8. apply quotas and I/O controls;
9. initialize services or restore declared seed data;
10. verify mount ownership and access mode;
11. record provisioning evidence;
12. start dependent services.

A partially provisioned resource remains inactive until verification completes.

### 6.2 Starting a service with persistent data

Service startup:

1. verifies workspace and service identity;
2. resolves the declared storage resources;
3. verifies that no resource belongs to another workspace;
4. verifies permissions and access mode;
5. checks schema and migration state;
6. checks available capacity;
7. starts the service;
8. verifies health and data accessibility;
9. records the active resource identities.

A service does not create an undeclared user-global data directory as a fallback.

### 6.3 Creating a shared cache

A shared cache is created through:

1. accepted profile or toolchain authority;
2. a declared cache identity;
3. integrity and key semantics;
4. consumer scope;
5. read/write rules;
6. eviction and corruption behavior;
7. credential restrictions;
8. quota and retention;
9. validation that the cache is non-authoritative;
10. registration in each consuming workspace manifest by reference.

### 6.4 Resetting workspace data

Reset:

1. selects the workspace and resource identifiers;
2. displays the owner and storage class;
3. verifies that no other workspace owns the resource;
4. checks retention, backup, and evidence requirements;
5. stops dependent services;
6. creates a backup when required;
7. deletes or recreates the selected data;
8. initializes the required schema or seed state;
9. verifies service health;
10. records the reset result.

A reset does not use a broad name pattern as the sole deletion selector.

### 6.5 Snapshot and backup

Backup:

1. identifies the component owner and resources;
2. obtains a consistent source state;
3. records source schema and contract versions;
4. applies encryption or protection;
5. creates the backup;
6. generates the manifest and integrity identity;
7. verifies the backup;
8. applies retention;
9. records evidence.

A backup that fails verification is not eligible for restore authority.

### 6.6 Restore

Restore:

1. selects a verified backup;
2. creates an isolated restore target;
3. verifies compatibility;
4. restores data;
5. applies declared migrations;
6. validates ownership and permissions;
7. runs representative integrity and behavior tests;
8. stops the prior active target when replacement is intended;
9. activates atomically or switches through the declared service mechanism;
10. retains rollback or forward-repair state;
11. records restore evidence.

### 6.7 Workspace removal

Removal:

1. stops workspace services;
2. revokes workspace credentials;
3. loads the storage manifest;
4. discovers implementation resources;
5. reconciles declared and discovered resources;
6. classifies each disposition;
7. performs required export or backup;
8. deletes only verified workspace-owned resources;
9. preserves approved shared caches;
10. removes temporary and runtime state;
11. verifies that no dependent resource remains active;
12. records the cleanup report.

### 6.8 Branch or worktree duplication

Creating a second branch workspace:

1. assigns a new workspace identity;
2. shares only declared read-only source or non-authoritative caches;
3. creates new mutable volumes;
4. creates new database identities and state;
5. allocates new host-facing resources;
6. restores or seeds data through a declared process;
7. verifies simultaneous operation;
8. records isolation evidence.

Copying a mutable data directory while its source service is active is not a conforming duplication method.

### 6.9 Orphan review

Orphan review:

1. scans supported storage backends;
2. maps resources to workspace identities;
3. compares them with active and retained workspace records;
4. excludes approved shared caches and protected evidence;
5. produces a proposed disposition;
6. requires explicit approval for durable data deletion;
7. executes cleanup;
8. records the result.

## 7. Failure States and Safe Degradation

| Failure state | Required response |
| --- | --- |
| Storage resource belongs to another workspace | Startup or mutation is blocked. |
| Volume name or mount target collides | Provisioning is blocked and no existing resource is reused implicitly. |
| Storage manifest is missing | Destructive cleanup and authoritative startup remain blocked. |
| Physical resource exists but ownership cannot be verified | The resource is quarantined from automatic deletion or reuse. |
| Quota is exhausted | New unsafe mutations stop; reads and controlled export continue when integrity permits. |
| Filesystem becomes read-only | Services enter declared read-only or unavailable behavior and expose the condition. |
| Database or service data is corrupt | The affected resource is isolated; restore or forward repair begins from verified evidence. |
| Shared cache is corrupt | The cache entry or cache is discarded and rebuilt; authoritative data is unchanged. |
| Shared cache is unavailable | Work continues without the cache when resource policy permits. |
| Temporary-data cleanup fails | The path is retained or quarantined and reported; it is not treated as authoritative. |
| Backup verification fails | The backup is rejected and cannot support restore. |
| Restore validation fails | The restore target remains non-authoritative and the prior valid state remains active when available. |
| Migration fails after an irreversible transition | The component remains blocked or degraded while forward repair executes. |
| Cleanup discovers undeclared durable data | Automatic deletion stops and review is required. |
| Workspace process exits unexpectedly | Persistent data remains owned by the workspace; no other workspace assumes it. |
| WSL2 host path is unavailable | Linux services stop or degrade according to contract; an alternate undeclared path is not selected. |
| Worker cleanup cannot be verified | The build-farm worker is quarantined or destroyed. |
| Resource Governor is unavailable | Storage growth remains within the last verified envelope or mutations stop. |

Failure never converts a cache, backup, copied directory, stale volume, or restore target into authoritative active state without validation.

## 8. Cross-Component Interactions

### 8.1 Workspace controller

The workspace controller owns workspace-resource orchestration and the storage manifest.

It does not become the owner of component data.

### 8.2 Component services

A component service owns its logical data and migration semantics.

The workspace layer supplies isolated storage, identities, lifecycle operations, and evidence.

A component accesses only its declared data resources.

### 8.3 Resource Governor

The Resource Governor applies quotas, I/O constraints, queue limits, and storage-pressure policy.

It does not decide component data ownership, backup eligibility, or deletion authority.

### 8.4 Identity and Trust

Workspace and service identities control access to persistent resources.

The identity system does not become the owner of stored component records.

### 8.5 Container runtime

A container runtime creates or attaches declared volumes and mounts.

Runtime metadata supports ownership verification but does not override the canonical workspace manifest.

Container deletion does not automatically authorize deletion of retained durable data.

### 8.6 Python and UV

The Python toolchain owns the per-workspace `.venv` and permits a shared non-authoritative UV cache.

The shared UV cache does not become an installed dependency environment.

Removing one workspace `.venv` does not affect another workspace.

### 8.7 Databases and queues

Database, queue, and search services preserve workspace and component identities.

Cross-component and cross-workspace mutation uses declared interfaces rather than shared storage access.

### 8.8 Build and publication

Build outputs remain outside application-data volumes.

Release candidates move to controlled artifact staging with provenance and evidence.

Publication credentials and release repositories are not ordinary workspace volumes.

### 8.9 Backup and evidence systems

Backup systems hold protected copies and manifests.

Evidence systems hold receipts and validation results.

Neither becomes the active component-data owner.

### 8.10 Optional workbenches

SenTient, search engines, media-processing workers, and other heavy development services use separate task-activated storage.

Their removal does not delete or redefine core component data.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect on this document |
| --- | --- |
| `DEC-DEV-001` | Establishes one isolated mutable environment, service namespace, temporary-data namespace, database identity set, and resource budget per workspace. |
| `DEC-DEV-002` | Requires simultaneous applications, branches, and worktrees without volume, data, service, or identity collision. |
| `DEC-DATA-001` | Preserves logical component data ownership across shared or separate physical storage. |
| `DEC-PROFILE-BASELINE-001` | Keeps development storage implementation requirements profile-scoped. |
| `DEC-GOV-001` | Keeps resource enforcement separate from authorization and data ownership. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-005` | Supports profile-scoped rootless container and volume implementation without universal runtime coupling. |
| `ADR-013` | Separates global component and data semantics from profile topology. |
| `ADR-015` | Establishes isolated development workspaces and permitted shared download caches. |
| `ADR-019` | Separates resource control from governance policy. |
| `ADR-023` | Keeps overlay effects explicit. |
| `ADR-024` | Preserves logical ownership across profile-dependent physical isolation. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a volume name proves ownership;
- a stopped container owns no durable data;
- a shared filesystem permits shared mutable service state;
- one branch can reuse another branch's database directory;
- a copied database directory is a valid backup;
- a backup is valid without verification;
- a restore target is authoritative before validation;
- a cache can be trusted because it is local;
- a cache can replace a lockfile;
- a shared `.venv` is equivalent to a shared download cache;
- deleting a workspace directory removes every owned resource safely;
- every resource with a workspace-like prefix can be deleted;
- a host-global application directory is acceptable when convenient;
- build output can share an authoritative application-data volume;
- logs can contain secrets because they are local;
- physical database consolidation merges logical ownership;
- storage pressure authorizes cross-workspace reuse;
- a recipe path becomes canonical through common use;
- WSL2 and native Linux have identical path and filesystem semantics;
- an orphan is safe to delete without retention and evidence checks.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `05-development/08-volumes-and-persistent-data.md`;
3. all identifiers and canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirements registry;
6. all locks exist and pass;
7. every active workspace has a unique workspace identity;
8. every mutable storage resource has a unique workspace-scoped identity;
9. every storage resource has an owner, class, lifecycle, access mode, retention, cleanup policy, and backup disposition;
10. no independent workspaces share authoritative or durable mutable state;
11. every approved shared cache is non-authoritative, verifiable, and replaceable;
12. no shared cache is an installed dependency environment;
13. `.venv` remains workspace-local;
14. no undeclared host-global mutable dependency exists;
15. component data ownership matches `generated/component-catalog.json`;
16. direct cross-component writes are absent;
17. direct cross-workspace writes are absent;
18. authoritative data is separated from caches, logs, temporary data, and build output;
19. secrets are absent from ordinary volumes, caches, logs, and unencrypted backups;
20. destructive cleanup verifies ownership before deletion;
21. workspace removal cannot affect another workspace;
22. simultaneous branch and application tests show no storage collisions;
23. quotas and I/O policies can be enforced per workspace;
24. backup manifests identify source, owner, schema, integrity, and compatibility;
25. restore tests use isolated targets and validate before activation;
26. irreversible migration tests include backup and forward repair;
27. orphan detection distinguishes protected resources from safe cleanup candidates;
28. WSL2 tests validate declared host/Linux storage boundaries;
29. build-farm tests prove clean-worker storage and verified cleanup;
30. failure tests preserve existing authoritative data and accurate degraded state;
31. active content is English;
32. placeholder and unresolved-authority markers are absent.

The validator reports actionable failures, including:

```text
workspace_storage_manifest_missing
workspace_storage_owner_missing
workspace_storage_class_missing
workspace_volume_collision
workspace_mount_collision
workspace_cross_write_detected
workspace_shared_mutable_state
workspace_cache_became_authoritative
workspace_cache_became_environment
workspace_undeclared_host_path
workspace_data_class_mixed
workspace_cleanup_owner_unverified
workspace_cleanup_cross_workspace_effect
workspace_backup_unverified
workspace_restore_not_isolated
workspace_restore_not_validated
workspace_migration_missing_backup
workspace_migration_missing_forward_repair
workspace_orphan_disposition_missing
workspace_storage_quota_unenforced
workspace_storage_degradation_inaccurate
```

## 11. Non-Normative Examples

### 11.1 Two Konnaxion branches

Two worktrees use:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
```

Each receives separate database state, upload storage, logs, temporary files, and service volumes. They can share the verified UV download cache but not a `.venv` or PostgreSQL data directory.

### 11.2 Shared PostgreSQL process

A lightweight developer topology uses one PostgreSQL process for Konnaxion and Orgo.

Each component and workspace has a separate database or schema and a separate database identity. The PostgreSQL service volume belongs to the workspace, while logical data ownership remains component-specific.

### 11.3 Rootless container volume

A workspace controller creates a rootless named volume for an Elasticsearch development index.

The storage manifest records the workspace, SenTient service owner, quota, cleanup policy, task-activated lifecycle, and non-authoritative rebuild behavior.

### 11.4 Bind-mounted source

The source checkout is bind-mounted read-write into a development container.

Database files, queue state, logs, and temporary files use separate declared storage resources. The container does not mount the complete host home directory.

### 11.5 Shared UV cache

Several workspaces use one content-addressed UV download cache.

Each workspace keeps its own `.venv` and lockfile. Cache deletion slows the next synchronization but does not alter dependency authority.

### 11.6 Migration test

A developer snapshots a Konnaxion test database, runs an irreversible schema migration in an isolated workspace, and verifies representative queries and civic-reading recalculation.

The original workspace remains untouched. A failed migration uses forward repair inside the test workspace.

### 11.7 Verified restore

A backup is restored into a new volume, migrated to the current schema, and tested.

Only after integrity, ownership, permissions, and behavior checks pass does the workspace switch the service to the restored target.

### 11.8 Workspace deletion

A feature workspace is removed.

The cleanup report deletes its `.venv`, temporary data, logs, service volumes, database identity, and build output. It retains a declared migration backup and leaves the shared UV cache unchanged.

### 11.9 Orphaned volume

A container runtime lists a volume with a former workspace label, but no matching workspace record exists.

The resource is reported as an orphan candidate. It is not deleted until retention, backup, evidence, and ownership checks complete.

### 11.10 Storage exhaustion

A workspace reaches its data-volume quota during an import.

The component stops unsafe writes, preserves committed records, reports degraded status, and allows controlled cleanup or export. It does not attach another workspace's volume as emergency capacity.
