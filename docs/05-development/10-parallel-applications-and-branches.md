<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-010",
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
    "contracts/system.contract.json#/development_model",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-PAR-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-DEV-PAR-001",
    "REQ-DEV-PAR-002",
    "REQ-DEV-PAR-003",
    "REQ-DEV-PAR-004",
    "REQ-DEV-PAR-005",
    "REQ-DEV-PAR-006",
    "REQ-DEV-PAR-007",
    "REQ-DEV-PAR-008",
    "REQ-DEV-PAR-009",
    "REQ-DEV-PAR-010",
    "REQ-DEV-PAR-011",
    "REQ-DEV-PAR-012",
    "REQ-DEV-PAR-013",
    "REQ-DEV-PAR-014",
    "REQ-DEV-PAR-015",
    "REQ-DEV-PAR-016",
    "REQ-DEV-PAR-017",
    "REQ-DEV-PAR-018",
    "REQ-DEV-PAR-019",
    "REQ-DEV-PAR-020",
    "REQ-DEV-PAR-021",
    "REQ-DEV-PAR-022",
    "REQ-DEV-PAR-023",
    "REQ-DEV-PAR-024",
    "REQ-DEV-PAR-025",
    "REQ-DEV-PAR-026",
    "REQ-DEV-PAR-027",
    "REQ-DEV-PAR-028",
    "REQ-DEV-PAR-029",
    "REQ-DEV-PAR-030",
    "REQ-DEV-PAR-031",
    "REQ-DEV-PAR-032",
    "REQ-DEV-PAR-033",
    "REQ-DEV-PAR-034",
    "REQ-DEV-PAR-035",
    "REQ-DEV-PAR-036",
    "REQ-DEV-PAR-037",
    "REQ-DEV-PAR-038",
    "REQ-DEV-PAR-039",
    "REQ-DEV-PAR-040"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-DEV-000"
  ],
  "tags": [
    "parallel-development",
    "branches",
    "worktrees",
    "applications",
    "workspace-isolation",
    "namespace-isolation",
    "port-allocation",
    "database-isolation",
    "artifact-provenance",
    "test-evidence",
    "merge-safety",
    "cleanup"
  ]
}
KOA:DOC-META:END -->

# Parallel Applications and Branches

## 1. Purpose

This document defines how multiple kOA applications, component instances, branches, worktrees, test runs, and development workspaces operate concurrently on one host or shared development substrate.

Parallel development is safe only when mutable state, infrastructure, execution, artifacts, and evidence have explicit ownership. Source isolation alone is insufficient. Two branches can use separate directories while still colliding through a shared virtual environment, database, container volume, port, queue, index, cache, certificate, scheduler, or external sandbox.

The model provides deterministic answers to these questions:

- which workspace owns a resource;
- which source revision produced a process, artifact, or result;
- which application instance can mutate a data store;
- which test created an event or record;
- which port and network belong to a stack;
- which resources cleanup can remove;
- whether a cache or artifact can be reused safely;
- what needs to be rebuilt after merge or rebase.

The common development model remains authoritative for workspaces, UV, contracts, testing, evidence, artifacts, AI boundaries, and release separation. This document specializes that model for concurrency.

## 2. Scope

This document applies to:

- parallel Git branches;
- Git worktrees and separate checkouts;
- multiple repositories in one declared workspace;
- multiple component instances;
- multiple full or partial application stacks;
- parallel unit, component, integration, profile, artifact, migration, security, offline, and recovery tests;
- local containers;
- local processes and service managers;
- databases, queues, indexes, object stores, caches, and temporary storage;
- generated outputs;
- candidate artifacts;
- test and conformance evidence;
- controlled external-provider sandboxes;
- workspace cleanup;
- merge, rebase, branch retirement, and workspace retirement.

It applies to developer Linux and Windows WSL profiles. Host-specific paths, container backends, resource limits, and operating-system behavior remain owned by the applicable profile contract.

This document does not create cross-workspace authority. An intentional interaction between workspaces requires its own explicit test, integration, transfer, or federation contract.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Global development model | `contracts/system.contract.json#/development_model` |
| Developer and build profile facts | `contracts/profiles/*.profile.json` |
| Python and UV toolchain | `contracts/toolchains/python-uv.toolchain.json` |
| Component identities and ownership | `generated/component-catalog.json` |
| Component interfaces and state | `contracts/components/*.component.json` |
| Artifact identity and lifecycle | `contracts/artifact-classes.contract.json` |
| Release channels and Release Sets | `contracts/release-channels.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Parallel-development and ownership locks | `generated/assertion-index.json` |
| Source, requirement, test, artifact, and evidence links | `generated/traceability.json` |
| Registered tests | `generated/test-catalog.json` |
| Accepted evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

The workspace manifest owns local resource allocation facts for one workspace. It does not replace profile, component, artifact, or release contracts.

## 4. Identity and Isolation Model

### 4.1 Identity dimensions

Parallel execution uses three separate identities:

| Identity | Purpose |
| --- | --- |
| `workspace_id` | Owns mutable development resources and evidence |
| `source_revision` | Identifies the exact source state |
| `application_instance_id` | Identifies one running component or application instance |

A branch or change reference can be recorded for human navigation. It is not a stable replacement for the workspace identity or source revision.

A workspace can move between branches. A branch can be checked out in more than one workspace. An application instance can restart while preserving its instance identity.

### 4.2 Workspace manifest

Every active workspace has a local manifest containing:

`text
workspace_id
workspace_root
active_profile_ref
repository_refs
source_revisions
branch_or_change_refs
toolchain_ref
dependency_lock_refs
application_instances
container_project_ref
network_ref
volume_prefix
database_prefix
queue_prefix
port_allocations
artifact_output_root
evidence_output_root
created_at
cleanup_authority
`

The manifest contains no credential values.

It can be generated from canonical and local inputs, but its identity remains stable while owned resources exist.

### 4.3 Workspace labels

Every mutable resource carries ownership labels or equivalent metadata:

`text
koa.workspace.id
koa.instance.id
koa.component.id
koa.profile.id
koa.source.revision
koa.created.by
`

Resources that cannot carry labels use a workspace-scoped parent namespace and an ownership record in the manifest.

### 4.4 Source isolation

Each active branch uses one isolated source tree.

Supported mechanisms include:

- Git worktree;
- separate clone;
- declared multi-repository workspace;
- equivalent immutable source checkout in an automated runner.

Generated and runtime directories remain inside or uniquely bound to that source workspace.

### 4.5 Environment isolation

Each Python workspace uses:

`text
<workspace-root>/.venv
<workspace-root>/pyproject.toml
<workspace-root>/uv.lock
`

Normal synchronization uses:

`bash
uv sync --frozen
`

Commands use:

`bash
uv run <command>
`

Environment reuse is limited to immutable package caches. Installed mutable environments are not shared.

### 4.6 Application-instance isolation

An application instance record identifies:

- instance identity;
- component identity;
- workspace identity;
- source revision;
- profile;
- process or container identity;
- ports;
- database and queue namespaces;
- storage roots;
- active artifact identities;
- startup time;
- health state.

A full application stack is a group of such records, not a replacement for component identities.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-PAR-001,REQ-DEV-PAR-002,REQ-DEV-PAR-003,REQ-DEV-PAR-004,REQ-DEV-PAR-005,REQ-DEV-PAR-006,REQ-DEV-PAR-007,REQ-DEV-PAR-008,REQ-DEV-PAR-009,REQ-DEV-PAR-010,REQ-DEV-PAR-011,REQ-DEV-PAR-012,REQ-DEV-PAR-013,REQ-DEV-PAR-014,REQ-DEV-PAR-015,REQ-DEV-PAR-016,REQ-DEV-PAR-017,REQ-DEV-PAR-018,REQ-DEV-PAR-019,REQ-DEV-PAR-020,REQ-DEV-PAR-021,REQ-DEV-PAR-022,REQ-DEV-PAR-023,REQ-DEV-PAR-024,REQ-DEV-PAR-025,REQ-DEV-PAR-026,REQ-DEV-PAR-027,REQ-DEV-PAR-028,REQ-DEV-PAR-029,REQ-DEV-PAR-030,REQ-DEV-PAR-031,REQ-DEV-PAR-032,REQ-DEV-PAR-033,REQ-DEV-PAR-034,REQ-DEV-PAR-035,REQ-DEV-PAR-036,REQ-DEV-PAR-037,REQ-DEV-PAR-038,REQ-DEV-PAR-039,REQ-DEV-PAR-040 -->
- **REQ-DEV-PAR-001 — SHALL:** Every simultaneously active development branch or application instance operate inside one explicitly identified workspace.
- **REQ-DEV-PAR-002 — SHALL:** Every workspace identity be stable for the lifetime of its mutable resources and be distinct from branch name, repository path, user name, and application display name.
- **REQ-DEV-PAR-003 — SHALL:** Every workspace record its source repository identities, source revisions, active profile, application instances, toolchain identity, and dependency-lock identity.
- **REQ-DEV-PAR-004 — SHALL NOT:** A branch name, Git worktree directory, container project name, process identifier, or automatically truncated path be used as the sole workspace identity.
- **REQ-DEV-PAR-005 — SHALL:** Every parallel branch use a separate checkout, worktree, or equivalent source tree with independent mutable generated and runtime state.
- **REQ-DEV-PAR-006 — SHALL NOT:** Two active branches modify the same generated directory, virtual environment, build directory, test cache, runtime directory, or local evidence directory.
- **REQ-DEV-PAR-007 — SHALL:** Every Python workspace use its own `.venv` and the `uv.lock` associated with that workspace's selected source revision.
- **REQ-DEV-PAR-008 — SHALL NOT:** Parallel branches share a mutable Python virtual environment or rely on environment mutation performed by another branch.
- **REQ-DEV-PAR-009 — SHALL:** Every application instance have a stable instance identity unique within its workspace and component scope.
- **REQ-DEV-PAR-010 — SHALL:** Every mutable service, container, process group, network, volume, queue, topic, bucket, database, schema, index, cache, and temporary directory include the applicable workspace and instance identities.
- **REQ-DEV-PAR-011 — SHALL NOT:** Default global resource names be used when more than one workspace or application instance can run on the same host.
- **REQ-DEV-PAR-012 — SHALL:** Every network listener use a workspace-scoped deterministic or allocated port recorded in the workspace manifest.
- **REQ-DEV-PAR-013 — SHALL:** Port allocation detect collisions before service activation and block the conflicting instance.
- **REQ-DEV-PAR-014 — SHALL NOT:** A parallel workspace resolve a port collision by terminating or reconfiguring another workspace without explicit authority.
- **REQ-DEV-PAR-015 — SHALL:** Every container stack use one workspace-scoped project identity, one workspace network, workspace-scoped volumes, and immutable or explicitly versioned image identities.
- **REQ-DEV-PAR-016 — SHALL NOT:** Parallel workspaces share mutable container volumes, container names, project names, or anonymous volumes that contain authoritative test state.
- **REQ-DEV-PAR-017 — SHALL:** Every component instance use a separate logical database, schema, tenant, or equivalent ownership boundary sufficient to prevent cross-workspace writes.
- **REQ-DEV-PAR-018 — SHALL NOT:** Physical database sharing create shared logical schemas or permit one workspace to read or mutate another workspace's component-authoritative test data.
- **REQ-DEV-PAR-019 — SHALL:** Database migration state be workspace- and component-scoped and match the source revision that owns the migration definitions.
- **REQ-DEV-PAR-020 — SHALL NOT:** A branch apply irreversible migrations to another branch's mutable database or to a production, sovereign, or shared integration database.
- **REQ-DEV-PAR-021 — SHALL:** Every queue, topic, consumer group, event stream, scheduler identity, and idempotency namespace be workspace-scoped.
- **REQ-DEV-PAR-022 — SHALL:** Every asynchronous test wait for events and results produced by its own workspace and correlation identities.
- **REQ-DEV-PAR-023 — SHALL NOT:** A test pass by consuming an event, record, cache entry, file, or process state produced by another workspace unless an explicit cross-workspace test contract defines the exchange.
- **REQ-DEV-PAR-024 — SHALL:** Every build, test, generated output, candidate artifact, receipt, and evidence record identify the workspace, source revision, branch or change reference, profile, toolchain, and dependency lock.
- **REQ-DEV-PAR-025 — SHALL NOT:** An artifact from one branch be silently substituted into another branch's build, runtime, test, or release candidate.
- **REQ-DEV-PAR-026 — SHALL:** Artifact and cache reuse require content-addressed or otherwise verified immutable identity plus compatibility with the consuming source and toolchain context.
- **REQ-DEV-PAR-027 — SHALL:** Ordinary source and documentation caches remain regenerable and separable from authoritative test data and evidence.
- **REQ-DEV-PAR-028 — SHALL:** Every parallel test run use workspace-scoped temporary directories, fixtures, credentials, certificates, object names, clocks, and external sandbox identifiers.
- **REQ-DEV-PAR-029 — SHALL NOT:** Tests depend on execution order across branches, wall-clock coincidence, a developer's shell history, or a globally mutable test fixture.
- **REQ-DEV-PAR-030 — SHALL:** External provider tests use explicit workspace-scoped sandbox accounts or request namespaces and record provider-side cleanup requirements.
- **REQ-DEV-PAR-031 — SHALL:** The Resource Governor or active development profile limit total parallel applications, heavy jobs, databases, indexes, and workbenches according to host capacity.
- **REQ-DEV-PAR-032 — SHALL NOT:** Resource pressure authorize a workspace to evict another workspace's authoritative state, evidence, active transfer, or uncommitted work.
- **REQ-DEV-PAR-033 — SHALL:** Workspace shutdown and cleanup remove only resources whose ownership labels match the workspace identity and current cleanup authority.
- **REQ-DEV-PAR-034 — SHALL NOT:** Cleanup use broad name patterns, shared directory deletion, global container pruning, global volume pruning, or unrestricted process termination as the ordinary path.
- **REQ-DEV-PAR-035 — SHALL:** Before branch deletion or workspace retirement, required source changes, migration state, candidate artifacts, evidence, and pending external operations be committed, exported, cancelled, or explicitly discarded.
- **REQ-DEV-PAR-036 — SHALL:** Branch merge review distinguish source changes, canonical contract changes, generated outputs, migration changes, dependency-lock changes, and candidate artifacts.
- **REQ-DEV-PAR-037 — SHALL NOT:** Generated outputs, local runtime state, workspace manifests, secrets, caches, local databases, or unregistered candidate artifacts be merged as canonical source.
- **REQ-DEV-PAR-038 — SHALL:** After merge or rebase, the receiving workspace recreate or validate its dependency environment, generated outputs, database migrations, component contracts, tests, and evidence from the resulting source state.
- **REQ-DEV-PAR-039 — SHALL:** Conflicting semantic contract changes be resolved through canonical ownership and accepted decisions rather than by textual merge order.
- **REQ-DEV-PAR-040 — SHALL:** Parallel-development conformance include workspace identity, resource namespacing, environment isolation, database and queue isolation, port collision handling, artifact provenance, test attribution, safe cleanup, merge validation, offline behavior, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Runtime, Network, and Data Isolation

### 6.1 Process and service names

Processes and service units use names derived from stable component, workspace, and instance identities.

A display label can include the branch name. Lifecycle operations use the stable identifiers.

Process discovery verifies ownership labels, executable identity, working directory, and active source revision before stopping or reconfiguring an instance.

### 6.2 Container isolation

A workspace container stack uses:

- one project identity;
- one workspace network;
- component- and instance-scoped container names;
- workspace-scoped named volumes;
- explicit image identities;
- explicit port mappings;
- ownership labels;
- bounded cleanup commands.

Anonymous volumes can hold disposable caches only when loss and cross-run reuse are harmless.

### 6.3 Port allocation

Port allocation uses a workspace registry or deterministic allocation algorithm with collision verification.

A port record includes:

`text
workspace_id
application_instance_id
component_id
interface_id
bind_address
host_port
service_port
protocol
allocated_at
`

Loopback remains the default development bind address. LAN or external exposure follows the active profile and integration rules.

Allocation completes before service activation. The service verifies that the bound endpoint matches the manifest.

### 6.4 Database isolation

Every component instance receives a logical database boundary.

Valid strategies include:

- separate database;
- separate schema with enforced component and workspace ownership;
- separate tenant with validated isolation;
- separate database server instance;
- equivalent storage-engine namespace.

The chosen strategy records migration state, owner, cleanup scope, backup behavior, and access identities.

A database user receives access only to the intended workspace and component scope.

### 6.5 Migration isolation

Migration execution records:

- workspace;
- source revision;
- component;
- migration-set identity;
- database target;
- expected prior state;
- resulting state;
- rollback or forward-repair behavior;
- evidence.

Rebase or branch switch invalidates migration assumptions when the migration graph changes. The workspace then recreates or explicitly reconciles its local database.

### 6.6 Queue and event isolation

Queues and event systems use workspace-scoped:

- virtual hosts;
- namespaces;
- topics;
- queues;
- consumer groups;
- stream names;
- dead-letter locations;
- idempotency domains.

Correlation identities include the workspace and test-run identities where applicable.

A dead-letter or poison event remains inside the originating workspace.

### 6.7 Index, cache, and object-store isolation

Mutable indexes and caches include source, workspace, component, and schema compatibility in their identity.

Immutable reusable objects include a verified content or artifact identity.

Object stores use workspace and component prefixes plus access controls. Listing a shared bucket does not authorize access to another workspace's prefix.

### 6.8 Files and temporary state

Temporary files use workspace-scoped roots with bounded permissions.

Shared operating-system temporary directories can host only uniquely named, non-authoritative, short-lived files whose ownership can be verified.

Socket paths, lock files, PID files, journals, and local receipts remain workspace- and instance-scoped.

## 7. Tests, Artifacts, and Evidence

### 7.1 Test-run identity

Every test run has a stable `test_run_id`.

The test-run record includes:

- workspace;
- source revision;
- profile;
- toolchain;
- dependency lock;
- selected tests;
- component instances;
- resource namespaces;
- external sandbox references;
- start and finish times;
- result;
- cleanup status.

### 7.2 Fixture isolation

Fixtures are classified as:

`text
immutable_shared
workspace_copy
test_run_copy
externally_managed_sandbox
`

Mutable fixture use creates a workspace or test-run copy.

A test does not modify a shared immutable fixture.

### 7.3 Time, randomness, and identity

Parallel tests use explicit:

- clocks or time sources;
- random seeds where reproducibility requires them;
- subject identities;
- service identities;
- certificates;
- trust roots;
- tenant or authority scopes.

Identifiers remain unique across test runs while deterministic reconstruction remains possible where required.

### 7.4 External sandboxes

A live external integration test records:

- registered integration;
- sandbox account or project;
- workspace namespace;
- cost boundary;
- data classification;
- credential reference;
- created objects;
- cleanup owner;
- retained external evidence.

A provider response remains attributable to the originating workspace and request.

### 7.5 Candidate artifacts

Candidate artifact identity includes:

`text
artifact_class
artifact_version
workspace_id
source_revision
profile_id
toolchain_identity
dependency_lock_identity
build_parameters
provenance
functional_integrity_record
test_refs
evidence_refs
`

Artifact directories are immutable after the artifact record is finalized.

A branch name can appear as metadata but does not replace source revision.

### 7.6 Cache reuse

Cache reuse follows one of these models:

| Cache class | Reuse condition |
| --- | --- |
| Package download cache | Immutable package identity and integrity |
| Build cache | Source, toolchain, dependency, environment, and parameter compatibility |
| Generated-content cache | Canonical input and generator compatibility |
| Test cache | Test identity, source, environment, fixture, and dependency compatibility |
| Runtime cache | Component contract, schema, source, and profile compatibility |

An unverifiable cache entry is ignored or quarantined.

### 7.7 Evidence attribution

Evidence includes enough identity to reproduce or invalidate the result.

Evidence from one workspace can support another source revision only when the evidence contract explicitly establishes equivalence and every relevant input matches.

A passing result cannot be copied by filename or directory convention.

## 8. Branch, Merge, and Synchronization Workflow

### 8.1 Creating a parallel workspace

Creation proceeds through:

1. allocate a workspace identity;
2. create or select the isolated source tree;
3. record source and branch references;
4. select the active development profile;
5. create the workspace manifest;
6. create `.venv` through UV;
7. allocate ports and namespaces;
8. create component data boundaries;
9. activate only required services;
10. run workspace-isolation validation.

The workspace remains blocked if any owned mutable resource collides with an active workspace.

### 8.2 Switching branches

A branch switch inside an existing workspace:

1. records the prior source revision;
2. stops affected application instances;
3. switches source;
4. records the new revision;
5. validates `uv.lock`;
6. runs frozen synchronization;
7. invalidates incompatible generated, build, test, migration, and runtime caches;
8. reconciles or recreates mutable component state;
9. restarts selected instances;
10. runs affected validation.

A workspace can retain its identity across the switch because its owned resources are explicitly reconciled.

### 8.3 Rebasing

After rebase, the workspace treats the resulting source revision as a new compatibility input.

The workflow validates:

- canonical contracts;
- dependency lock;
- generated content;
- database migration graph;
- interface schemas;
- artifact identities;
- tests and evidence.

Prior candidate artifacts remain linked to the old revision.

### 8.4 Merging

Merge review separates:

- canonical decisions and contracts;
- source implementation;
- database and artifact migrations;
- dependency-lock changes;
- tests;
- generated outputs;
- evidence;
- local-only state.

Semantic conflicts resolve through the canonical owner. Textual merge success is insufficient.

### 8.5 Post-merge reconstruction

The receiving workspace:

1. records the merged revision;
2. executes frozen dependency synchronization;
3. regenerates derived content;
4. verifies component and profile contracts;
5. applies or recreates local migrations;
6. rebuilds candidate artifacts;
7. executes affected tests;
8. creates new evidence;
9. retires stale workspace outputs.

Evidence and candidate artifacts associated with parent revisions remain historical.

### 8.6 Cross-workspace exchange

Intentional exchange uses a declared artifact, controlled import/export, test-fixture, or integration contract.

The exchange records:

- source workspace and revision;
- destination workspace and revision;
- artifact or data class;
- integrity;
- compatibility;
- purpose;
- acceptance;
- cleanup and retention.

Direct access to another workspace's mutable store remains outside the exchange model.

## 9. Cleanup, Recovery, and Offline Behavior

### 9.1 Cleanup authority

The workspace manifest identifies cleanup authority.

Cleanup verifies:

- workspace identity;
- resource ownership labels;
- active processes;
- pending tests;
- pending transfers;
- retained artifacts;
- retained evidence;
- uncommitted source;
- external sandbox objects.

Only positively matched resources enter the cleanup plan.

### 9.2 Cleanup order

Normal cleanup proceeds through:

1. stop new work;
2. complete or cancel test runs;
3. classify pending external operations;
4. preserve required artifacts and evidence;
5. stop owned application instances;
6. close owned queues and databases;
7. remove owned temporary and runtime data;
8. remove owned containers, networks, and volumes;
9. release ports;
10. archive or delete the workspace manifest according to policy.

Global prune commands are not the normal mechanism.

### 9.3 Crash recovery

After host, process, or container failure, recovery:

- reconstructs workspace ownership from manifests and labels;
- identifies incomplete tests and operations;
- restores or invalidates mutable state;
- verifies ports and process ownership;
- reconciles event and database state;
- preserves candidate artifacts and evidence;
- prevents blind restart of ambiguous operations.

### 9.4 Orphan detection

An orphan resource is a resource whose workspace is inactive or whose ownership record is incomplete.

Orphan handling:

1. quarantines the resource;
2. records its observed identity;
3. checks active processes and data;
4. identifies potential owner;
5. obtains cleanup authority;
6. removes or archives it through a bounded plan.

Age alone does not authorize deletion.

### 9.5 Offline operation

Parallel workspaces can continue offline using locally available:

- source trees;
- UV environments and caches;
- containers and images;
- databases and queues;
- tests;
- documentation validation;
- generated-content tools;
- candidate artifact tools.

Remote repository synchronization, uncached dependencies, live provider tests, remote artifacts, and remote evidence become unavailable or deferred.

Network loss does not cause workspaces to share fallback resources.

### 9.6 Resource pressure

The active profile limits total parallel use.

Pressure response can:

- stop optional workbenches;
- pause background indexes;
- reduce test concurrency;
- stop idle stacks;
- reject new heavy instances;
- preserve active source, databases, queues, evidence, and artifacts.

A workspace can be selected for shutdown only through explicit policy and ownership-aware lifecycle handling.

## 10. Exceptions and Validation

### 10.1 Exceptions

A bounded exception can adjust:

- port-allocation strategy;
- database isolation implementation;
- container backend;
- cache location;
- external sandbox mechanism;
- test-runner namespace implementation;
- profile-specific concurrency;
- cleanup retention interval.

An exception cannot:

- allow shared mutable `.venv`;
- allow shared component-authoritative schemas;
- permit one workspace to clean another;
- remove artifact or evidence attribution;
- permit unscoped global resource names;
- permit direct cross-workspace writes;
- treat a branch name as complete resource identity;
- merge local runtime state as canonical source;
- convert local test success into a production conformance claim.

### 10.2 Validation criteria

This document is conformant when validation confirms:

1. every active source tree belongs to one workspace identity;
2. workspace identity is stable and distinct from branch and path;
3. every Python workspace has its own `.venv` and matching `uv.lock`;
4. generated, build, test, runtime, and evidence directories are workspace-scoped;
5. application instance identities are unique;
6. process and service ownership is verifiable;
7. container projects, networks, volumes, and names are workspace-scoped;
8. port collisions are detected before activation;
9. database and migration state is isolated by workspace and component;
10. queue, topic, stream, scheduler, and idempotency namespaces are isolated;
11. indexes, caches, object stores, temporary files, sockets, and locks are attributable;
12. test runs and fixtures are isolated;
13. external sandboxes are workspace-scoped and cleanable;
14. candidate artifacts include complete source and workspace provenance;
15. cache reuse verifies immutable identity and compatibility;
16. evidence is attributable to one source and environment;
17. branch switch, rebase, and merge invalidate incompatible state;
18. cross-workspace exchange uses a declared contract;
19. cleanup removes only positively owned resources;
20. orphan handling is quarantined and authorized;
21. offline behavior preserves workspace isolation;
22. resource pressure preserves authoritative local development state;
23. every canonical reference resolves;
24. no prohibited open-state marker enters active authority.

The principal validation entry point is:

`bash
uv run python docs/tools/validate_docs.py
`

Supporting checks include:

`text
tools/check_workspace_isolation.py
tools/check_parallel_resource_names.py
tools/check_port_allocations.py
tools/check_component_boundaries.py
tools/check_profile_inheritance.py
tools/check_artifact_contracts.py
tools/check_traceability.py
tools/check_generated_content.py
tools/check_no_unresolved_state.py
`

A failed isolation check blocks the affected workspace's conformance claim and prevents activation of colliding resources.

## 11. Non-Normative Examples

### 11.1 Two branches

Two branches run in separate worktrees. Each has its own `.venv`, manifest, container project, network, volumes, ports, database names, queues, artifacts, and evidence directory.

### 11.2 Same branch in two workspaces

Two developers or automated runners use the same source revision. Their workspace identities remain distinct, so mutable resources and evidence do not collide.

### 11.3 Database migration divergence

One branch adds a migration while another modifies an earlier migration. After merge, the receiving workspace recreates its local database and validates the resulting migration graph instead of reusing either branch's mutable database.

### 11.4 Port collision

A new application instance requests a port already allocated to another workspace. Allocation fails before startup. The new workspace receives another port; the existing workspace remains unchanged.

### 11.5 Artifact reuse

A build cache entry matches source revision, toolchain, dependency lock, profile, and parameters. It can be reused. A candidate artifact built from another revision remains separate even when its filename matches.

### 11.6 Event isolation

Two integration tests publish similar events. Their workspace, test-run, and correlation identities differ, and each consumer group reads only its own namespace.

### 11.7 Safe cleanup

A branch is retired. Cleanup reads the manifest, preserves selected evidence, stops labeled processes, removes the matching containers and volumes, deletes only the workspace database, and releases its ports.

### 11.8 Unsafe cleanup prevented

A script attempts a global container and volume prune. The development model rejects it because ownership cannot be limited to one workspace.

### 11.9 Rebase

A branch is rebased onto a dependency and schema update. The workspace runs frozen synchronization, regenerates contracts and documentation, rebuilds local databases and artifacts, and creates new test evidence.

### 11.10 Offline parallel work

Two workspaces continue local tests without network access. Each uses its own local environment and services. Missing remote dependencies block only the affected operations and do not trigger shared fallback state.
