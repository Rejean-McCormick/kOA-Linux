<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "development_toolchain",
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json#/artifact_classes/developer_workspace",
    "contracts/artifact-classes.contract.json#/artifact_classes/workspace_port_allocation",
    "contracts/artifact-classes.contract.json#/artifact_classes/resource_envelope",
    "contracts/artifact-contracts/developer-workspace.schema.json",
    "contracts/artifact-contracts/workspace-port-allocation.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-DEV-WS-001",
    "REQ-DEV-WS-002",
    "REQ-DEV-WS-003",
    "REQ-DEV-WS-004",
    "REQ-DEV-WS-005",
    "REQ-DEV-WS-006",
    "REQ-DEV-WS-007",
    "REQ-DEV-WS-008",
    "REQ-DEV-WS-009",
    "REQ-DEV-WS-010",
    "REQ-DEV-WS-011",
    "REQ-DEV-WS-012",
    "REQ-DEV-WS-013",
    "REQ-DEV-WS-014",
    "REQ-DEV-WS-015",
    "REQ-DEV-WS-016",
    "REQ-DEV-WS-017",
    "REQ-DEV-WS-018",
    "REQ-DEV-WS-019",
    "REQ-DEV-WS-020",
    "REQ-DEV-WS-021",
    "REQ-DEV-WS-022",
    "REQ-DEV-WS-023",
    "REQ-DEV-WS-024",
    "REQ-DEV-WS-025",
    "REQ-DEV-WS-026",
    "REQ-DEV-WS-027",
    "REQ-DEV-WS-028",
    "REQ-DEV-WS-029",
    "REQ-DEV-WS-030",
    "REQ-DEV-WS-031",
    "REQ-DEV-WS-032",
    "REQ-DEV-WS-033",
    "REQ-DEV-WS-034",
    "REQ-DEV-WS-035",
    "REQ-DEV-WS-036",
    "REQ-DEV-WS-037",
    "REQ-DEV-WS-038",
    "REQ-DEV-WS-039",
    "REQ-DEV-WS-040",
    "REQ-DEV-WS-041",
    "REQ-DEV-WS-042",
    "REQ-DEV-WS-043",
    "REQ-DEV-WS-044"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
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
    "DOC-PROFILE-005",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002"
  ],
  "tags": [
    "development",
    "workspace",
    "workspace-isolation",
    "workspace-id",
    "parallel-development",
    "worktree",
    "mutable-state",
    "ports",
    "services",
    "data",
    "secrets",
    "resource-governance",
    "cleanup"
  ]
}
KOA:DOC-META:END -->

# Workspace Isolation

> **Document status:** Normative development architecture.  
> **Canonical workspace artifact:** `contracts/artifact-contracts/developer-workspace.schema.json`  
> **Canonical allocation artifact:** `contracts/artifact-contracts/workspace-port-allocation.schema.json`  
> **Authority rule:** Workspace contracts own structured workspace facts. This document defines the global isolation behavior those contracts must satisfy.

## 1. Purpose

This document defines the isolation boundary for kOA development workspaces.

A workspace is the complete logical development unit within which one application, component, branch, worktree, experiment, maintenance activity, or other declared purpose can install dependencies, start services, mutate local state, use secrets, allocate ports, and consume resources without colliding with another workspace.

The architecture supports multiple applications and multiple branches of the same application at the same time.

Isolation exists to provide:

- reproducible dependency state;
- deterministic naming and allocation;
- independent service and data lifecycles;
- safe parallel execution;
- bounded resource use;
- predictable cleanup and recovery;
- protection of component data ownership;
- separation between development success and production authority.

## 2. Scope

### 2.1 Included scope

This document applies to workspaces used by:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- release-oriented or validation workspaces when their profile explicitly adopts the developer workspace artifact class;
- local source development;
- Git branches and worktrees;
- Python and other declared toolchains;
- local processes and rootless or profile-approved service containers;
- databases, queues, search services, caches, and supporting infrastructure;
- local build, test, packaging, evidence, and candidate-artifact workflows.

### 2.2 Resources inside the isolation boundary

The workspace boundary includes:

```text
identity
source checkout
mutable dependency environments
processes and workers
services and containers
networks and endpoints
host-port allocations
volumes and writable paths
databases, schemas, users, and roles
queues and asynchronous state
sockets and PID files
temporary files and logs
secrets and generated certificates
resource reservations and limits
workspace-owned receipts and diagnostics
```

### 2.3 Excluded scope

This document does not define:

- a universal filesystem layout;
- a universal port range;
- a universal container runtime;
- a universal service manager;
- a universal Linux distribution;
- a universal Windows or WSL topology;
- a universal database engine;
- production artifact activation;
- production release authority;
- cross-domain publication authority;
- business authorization or component data ownership.

Those facts remain owned by profile, toolchain, component, artifact, release, and governance contracts.

## 3. Canonical References

### 3.1 Structured workspace authority

| Canonical source | Owned information |
| --- | --- |
| `contracts/artifact-contracts/developer-workspace.schema.json` | Workspace declaration structure and required fields |
| `contracts/artifact-contracts/workspace-port-allocation.schema.json` | Exclusive host-port and endpoint allocation |
| `contracts/artifact-contracts/resource-envelope.schema.json` | CPU, memory, I/O, worker, queue, process, and concurrency limits |
| `contracts/artifact-classes.contract.json#/artifact_classes/developer_workspace` | Workspace artifact lifecycle |
| `contracts/artifact-classes.contract.json#/artifact_classes/workspace_port_allocation` | Port-allocation lifecycle |
| `contracts/artifact-classes.contract.json#/artifact_classes/resource_envelope` | Resource-envelope lifecycle |
| `contracts/toolchains/python-uv.toolchain.json` | Python, UV, `.venv`, lockfile, synchronization, cache, and update rules |
| `contracts/toolchains/container-runtime.toolchain.json` | Profile-approved container-runtime behavior |
| Profile contracts | Profile membership and implementation-specific mechanisms |
| Component contracts | Component data ownership and service boundaries |
| `generated/requirements-index.json` | Normative statements |
| `generated/assertion-index.json` | Cross-file development isolation invariants |

### 3.2 Canonical terminology

The applicable terms are:

- **workspace** — the complete logical isolation unit;
- **workspace identifier** — the stable identifier used to namespace mutable resources;
- **worktree** — a Git checkout mechanism that may host a workspace;
- **mutable dependency environment** — an installed environment that cannot be shared;
- **workspace virtual environment** — the mutable Python `.venv` dedicated to one workspace;
- **shared content-addressed UV cache** — a reusable cache that is not an installed environment;
- **workspace port allocation** — the exclusive host-port allocation for one workspace.

### 3.3 Scope rule

Global isolation requirements apply to every workspace.

Linux, Windows, WSL, container, virtualization, path, networking, and service-manager details apply only when their owning profile or toolchain contract adopts them.

## 4. Model and Responsibilities

### 4.1 Workspace identity

Every active workspace has one stable `workspace_id`.

The canonical derivation model is:

```text
component-or-application + branch-or-purpose + unique-suffix
```

Examples:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
```

The unique suffix prevents collisions between simultaneous workspaces with otherwise equal human-readable names.

A `workspace_id` is stable for the lifecycle of that workspace revision. Recreating a retired workspace can preserve a historical relationship while receiving a new active identity when reuse could create ambiguity.

### 4.2 Workspace and worktree distinction

A workspace can use:

- a primary repository checkout;
- a Git worktree;
- an exported source tree;
- another profile-approved source mechanism.

The source mechanism does not define the isolation boundary.

A worktree isolates Git checkout state. It does not isolate:

- installed dependencies;
- service names;
- networks;
- ports;
- databases;
- queues;
- secrets;
- processes;
- temporary files;
- logs;
- resource limits.

One writable checkout belongs to at most one active workspace at a time.

### 4.3 Namespacing model

The `workspace_id` is included directly or through an unambiguous allocation reference in:

| Resource | Isolation expectation |
| --- | --- |
| Dependency environment | Dedicated mutable environment |
| Process and worker identity | Workspace-owned process-control scope |
| Service or container name | Unique within the applicable runtime |
| Logical network | Workspace-specific network or equivalent namespace |
| Internal endpoint | Resolves inside the intended workspace boundary |
| Host port | Exclusive allocation artifact |
| Writable volume or path | Workspace-owned mutable path |
| Database | Separate database, schema, user, role, or equivalent owner boundary |
| Queue | Separate queue, topic, routing key, consumer group, or equivalent namespace |
| Socket and PID file | Workspace-specific path or name |
| Temporary and log path | Workspace-specific path |
| Secret | Workspace-specific secret namespace and access control |
| Local certificate | Workspace identity and protected private key |
| Resource controls | Workspace-specific resource-envelope binding |

A platform can use another physical implementation when it preserves the same logical isolation and validation properties.

### 4.4 Shareability classes

Workspace resources are classified as follows:

| Class | Sharing rule | Examples |
| --- | --- | --- |
| Mutable and authoritative | Never shared across workspace write owners | `.venv`, writable application data, database write schema, queue state, secrets |
| Mutable but infrastructure-owned | Shared process permitted only with explicit logical isolation | PostgreSQL server, Redis process, search service, container daemon |
| Immutable or content-addressed | Sharing permitted | UV download cache, verified package blobs, read-only image layers |
| Read-only source | Sharing permitted only when no workspace can mutate it | admitted source archive, verified reference data |
| Exclusive allocation | One active workspace per allocation | host ports, exclusive device reservation, writable checkout |
| Derived and disposable | Sharing permitted only when reproducible and non-authoritative | build download cache, local indexes explicitly classified as rebuildable |

Sharing a process does not share data ownership.

### 4.5 Workspace declaration

A developer workspace artifact identifies at least:

- `workspace_id`;
- revision;
- purpose;
- owner or responsible actor;
- source root and checkout identity;
- active profile;
- toolchain references;
- dependency-environment references;
- service declarations;
- network and endpoint declarations;
- port-allocation reference;
- mutable data and database namespaces;
- queue namespaces;
- secret namespace;
- resource-envelope binding;
- retention and cleanup behavior;
- required validations.

The declaration is a contract. A recipe may explain commands but cannot add undeclared authority or canonical defaults.

### 4.6 Python environment boundary

Every Python workspace owns:

```text
pyproject.toml
uv.lock
declared Python version
workspace-specific .venv
```

Normal reproducible validation uses:

```bash
uv sync --frozen
```

The shared content-addressed UV cache can reduce downloads and builds. It does not contain the workspace's authoritative installed environment.

A lock refresh is distinct from frozen synchronization and produces an explicit reviewed change.

### 4.7 Services and databases

A workspace can use dedicated or shared infrastructure.

Dedicated infrastructure uses workspace-specific services, volumes, identities, and endpoints.

Shared infrastructure is conformant only when each workspace and component retains:

- separate credentials;
- separate database or schema ownership;
- separate queue or index namespace;
- separate write permissions;
- separate cleanup responsibility;
- prohibited cross-component writes;
- observable ownership.

A convenient local superuser does not replace the declared logical ownership model.

### 4.8 Port and endpoint allocation

Host ports are allocated before dependent services start.

The allocation artifact records:

- allocation identity;
- `workspace_id`;
- service identity;
- protocol;
- internal endpoint;
- host endpoint;
- allocation state;
- activation time;
- release state.

No canonical numeric range is inferred by this document.

Fixed internal ports are permitted inside distinct isolated workspace networks. Host-facing endpoints remain exclusive.

### 4.9 Secrets and local identities

Workspace secrets include:

- development credentials;
- service passwords;
- API tokens;
- local private keys;
- generated certificates;
- database identities;
- queue identities.

Secrets are stored through the profile-approved secret mechanism and are referenced rather than copied into general workspace files.

A separately authorized shared development identity can be referenced by several workspaces only when its scope, purpose, rotation, revocation, and audit behavior are explicit.

### 4.10 Resource governance

Every active workspace has a resource envelope.

Resource Governor can:

- reserve or limit CPU and memory;
- control process and worker counts;
- set I/O priority;
- limit queues;
- limit heavy jobs;
- throttle, suspend, resume, or reject work;
- preserve required host capabilities during pressure.

Resource Governor does not authorize the business action performed by the workspace.

### 4.11 Workspace lifecycle

The workspace lifecycle is:

```text
defined
→ validated
→ allocated
→ active
→ suspended
→ restoring
→ active
→ retired
→ archived
```

A workspace can move directly from `allocated` or `active` to `retired` after controlled cleanup.

A failed activation returns to an inactive state and does not leave partial allocations authoritative.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-DEV-WS-001,REQ-DEV-WS-002,REQ-DEV-WS-003,REQ-DEV-WS-004,REQ-DEV-WS-005,REQ-DEV-WS-006,REQ-DEV-WS-007,REQ-DEV-WS-008,REQ-DEV-WS-009,REQ-DEV-WS-010,REQ-DEV-WS-011,REQ-DEV-WS-012,REQ-DEV-WS-013,REQ-DEV-WS-014,REQ-DEV-WS-015,REQ-DEV-WS-016,REQ-DEV-WS-017,REQ-DEV-WS-018,REQ-DEV-WS-019,REQ-DEV-WS-020,REQ-DEV-WS-021,REQ-DEV-WS-022,REQ-DEV-WS-023,REQ-DEV-WS-024,REQ-DEV-WS-025,REQ-DEV-WS-026,REQ-DEV-WS-027,REQ-DEV-WS-028,REQ-DEV-WS-029,REQ-DEV-WS-030,REQ-DEV-WS-031,REQ-DEV-WS-032,REQ-DEV-WS-033,REQ-DEV-WS-034,REQ-DEV-WS-035,REQ-DEV-WS-036,REQ-DEV-WS-037,REQ-DEV-WS-038,REQ-DEV-WS-039,REQ-DEV-WS-040,REQ-DEV-WS-041,REQ-DEV-WS-042,REQ-DEV-WS-043,REQ-DEV-WS-044
renderer=requirements-list-v1
-->
- **REQ-DEV-WS-001 — SHALL:** A workspace be the complete logical isolation unit for one active development purpose.
- **REQ-DEV-WS-002 — SHALL:** Every active workspace have one stable and unique `workspace_id`.
- **REQ-DEV-WS-003 — SHALL:** The `workspace_id` be derived from the component or application, branch or purpose, and a unique suffix.
- **REQ-DEV-WS-004 — SHALL:** The workspace declaration validate against `developer-workspace.schema.json` before allocation or start.
- **REQ-DEV-WS-005 — SHALL:** The workspace declaration identify its repository or source root, purpose, active profile, owners, toolchains, services, data namespaces, port allocation, secrets, and resource envelope.
- **REQ-DEV-WS-006 — SHALL:** The `workspace_id` namespace every mutable dependency environment, process, service, container, network, port allocation, volume, database identity, queue, socket, temporary path, log path, PID file, secret, certificate, and resource allocation belonging to the workspace.
- **REQ-DEV-WS-007 — SHALL NOT:** Two active workspaces share a mutable installed dependency environment.
- **REQ-DEV-WS-008 — SHALL NOT:** Two active workspaces share writable service data, database write authority, queue identity, secret namespace, process-control state, or host-port allocation unless an explicit component contract defines a safe shared owner and separate logical namespaces.
- **REQ-DEV-WS-009 — MAY:** Workspaces share immutable, read-only, or content-addressed caches when sharing cannot mutate an installed environment or authoritative workspace state.
- **REQ-DEV-WS-010 — SHALL:** A shared cache remain disposable and reproducible from canonical source, lock, or artifact inputs.
- **REQ-DEV-WS-011 — SHALL NOT:** A shared cache be treated as the sole authoritative copy of source, dependency, build, evidence, or release state.
- **REQ-DEV-WS-012 — SHALL:** A Git worktree be treated only as a source-checkout mechanism that may host one workspace.
- **REQ-DEV-WS-013 — SHALL NOT:** A worktree by itself be treated as isolation for dependencies, services, ports, data, secrets, identities, queues, processes, or resources.
- **REQ-DEV-WS-014 — SHALL NOT:** One writable checkout be controlled concurrently by more than one active workspace.
- **REQ-DEV-WS-015 — SHALL:** Parallel applications, branches, purposes, and worktrees run without collisions in mutable state or dependency resolution.
- **REQ-DEV-WS-016 — SHALL:** Each Python workspace own one mutable `.venv`, one declared Python version, one versioned `pyproject.toml`, and one versioned `uv.lock`.
- **REQ-DEV-WS-017 — SHALL:** Reproducible Python synchronization use `uv sync --frozen` or the canonically registered equivalent.
- **REQ-DEV-WS-018 — SHALL NOT:** Global application dependency installation substitute for a workspace dependency environment.
- **REQ-DEV-WS-019 — MAY:** Python workspaces share the content-addressed UV download and build cache.
- **REQ-DEV-WS-020 — SHALL:** Lockfile refresh and dependency upgrades be explicit changes with impact analysis and applicable test evidence.
- **REQ-DEV-WS-021 — SHALL:** Host ports be assigned through a workspace port allocation artifact before dependent services start.
- **REQ-DEV-WS-022 — SHALL:** A host-port allocation be exclusive for its active allocation lifetime.
- **REQ-DEV-WS-023 — MAY:** Different isolated workspace networks reuse the same internal service port when their host-facing allocations and network identities remain distinct.
- **REQ-DEV-WS-024 — SHALL NOT:** Documentation, a recipe, or an implementation invent a canonical host-port range when no accepted owner decision defines one.
- **REQ-DEV-WS-025 — SHALL:** Service names, network identities, endpoints, sockets, and discovery records resolve to the intended workspace.
- **REQ-DEV-WS-026 — SHALL:** Shared infrastructure preserve separate component and workspace credentials, databases or schemas, namespaces, owned paths, queues, and prohibited cross-component writes.
- **REQ-DEV-WS-027 — SHALL NOT:** A shared database, cache, queue, search engine, container daemon, or host process create shared authoritative ownership.
- **REQ-DEV-WS-028 — SHALL:** Development secrets, local identities, and generated certificates remain workspace-scoped unless a separately authorized shared identity is explicitly referenced.
- **REQ-DEV-WS-029 — SHALL NOT:** Secrets be copied into source control, shared mutable caches, general logs, process arguments, or another workspace's namespace.
- **REQ-DEV-WS-030 — SHALL:** Every active workspace have an enforceable resource budget for CPU, memory, processes, I/O, workers, queues, and heavy-job concurrency.
- **REQ-DEV-WS-031 — SHALL:** Resource Governor enforce workspace resource envelopes without deciding business authorization, disclosure, consent, or privilege.
- **REQ-DEV-WS-032 — SHALL:** Resource pressure queue, throttle, suspend, or reject lower-priority or heavy work before isolation, authoritative data, or required host capabilities are endangered.
- **REQ-DEV-WS-033 — SHALL:** Task-activated heavy services release their workspace resources after completion, cancellation, failure, or declared idle expiry.
- **REQ-DEV-WS-034 — SHALL:** Workspace start be atomic with respect to identity, dependency environment, port allocation, mutable namespaces, and resource controls.
- **REQ-DEV-WS-035 — SHALL:** A failed workspace activation leave the workspace inactive and preserve existing workspaces.
- **REQ-DEV-WS-036 — SHALL:** Workspace suspension preserve enough identity and state to support explicit restoration or retirement.
- **REQ-DEV-WS-037 — SHALL:** Workspace restoration revalidate identity, source checkout, dependency state, ports, services, data ownership, secrets, processes, resource limits, and queued work before mutation resumes.
- **REQ-DEV-WS-038 — SHALL:** Workspace removal stop owned processes, revoke owned credentials, release allocations, and remove or archive owned mutable state according to declared retention.
- **REQ-DEV-WS-039 — SHALL:** Removing one workspace leave every other workspace's dependency environment, services, ports, data, secrets, processes, and resource allocations unchanged.
- **REQ-DEV-WS-040 — SHALL:** Residual resources discovered after removal remain associated with the retired `workspace_id` until reconciled and shall block conflicting reuse.
- **REQ-DEV-WS-041 — SHALL NOT:** A development workspace acquire production release, artifact activation, policy, publication, or conformance authority solely because local validation succeeds.
- **REQ-DEV-WS-042 — SHALL:** Workspace outputs remain development candidates until admitted by the applicable artifact, build, signing, evidence, and release authorities.
- **REQ-DEV-WS-043 — SHALL:** Profile-specific Linux, Windows, WSL, container, virtualization, filesystem, service-manager, or networking mechanisms remain scoped to the profile or toolchain that adopts them.
- **REQ-DEV-WS-044 — SHALL:** Workspace conformance test parallel execution, mutable-state separation, port exclusivity, service and data ownership, secret isolation, resource enforcement, independent cleanup, failure isolation, and absence of undeclared authority.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Define a workspace

1. select the application, component, branch, worktree, or purpose;
2. allocate a unique `workspace_id`;
3. identify the active deployment profile;
4. resolve component and toolchain contracts;
5. declare dependency, service, data, queue, secret, and resource requirements;
6. create the developer workspace artifact;
7. validate the artifact before allocation.

Missing authority or an invalid declaration blocks activation.

### 6.2 Allocate workspace resources

Allocation follows:

1. reserve the writable checkout;
2. establish dependency-environment identity;
3. allocate service and network names;
4. allocate host ports through the port-allocation artifact;
5. create writable data and database namespaces;
6. create queue and search namespaces;
7. provision workspace secrets and local identities;
8. bind the resource envelope;
9. validate collision absence;
10. mark allocation complete atomically.

A partial allocation is released or retained as non-active recovery state. It is not treated as an active workspace.

### 6.3 Start a workspace

Before start:

1. verify workspace declaration and revision;
2. verify checkout ownership and source state;
3. create or verify the workspace dependency environment;
4. synchronize dependencies according to the toolchain contract;
5. verify ports, endpoints, data ownership, and secrets;
6. apply resource controls;
7. start only declared services;
8. run health, readiness, and isolation checks;
9. mark the workspace `active`.

### 6.4 Run parallel workspaces

Before two workspaces run concurrently, validation compares:

- workspace identifiers;
- writable checkouts;
- mutable dependency paths;
- service and container names;
- network names;
- host ports;
- volumes and writable paths;
- databases, schemas, users, and roles;
- queues and consumer identities;
- sockets and PID files;
- temporary and log paths;
- secrets and certificates;
- processes, workers, and resource allocations.

Any unresolved collision blocks the affected workspace start.

### 6.5 Refresh dependencies

Dependency refresh follows:

1. record the change purpose;
2. update declared dependencies;
3. regenerate the lock state;
4. review the dependency and transitive change;
5. synchronize the workspace environment;
6. run applicable tests, security checks, and impact analysis;
7. commit the project and lock state together.

Another workspace is not silently synchronized or modified.

### 6.6 Suspend and restore

Suspension:

1. stop or pause declared processes;
2. preserve workspace identity and retained state;
3. record active allocations and pending work;
4. protect secrets and writable data;
5. mark the workspace `suspended`.

Restoration:

1. enter `restoring`;
2. revalidate the declaration and active profile;
3. verify checkout and dependency state;
4. verify service identities, ports, data, queues, and secrets;
5. reconcile processes and pending work;
6. reapply resource controls;
7. run readiness and isolation checks;
8. return to `active` or remain degraded or blocked.

### 6.7 Retire and remove

Removal follows:

1. prevent new workspace work;
2. stop workspace-owned processes, containers, services, and workers;
3. cancel, export, or resolve workspace-owned queued work;
4. revoke workspace secrets, identities, and certificates;
5. release host ports, networks, and exclusive reservations;
6. archive or delete writable data according to retention;
7. remove the workspace dependency environment;
8. remove temporary files, sockets, PID files, and disposable logs;
9. verify that no other workspace changed;
10. record residual resources;
11. mark the workspace `retired` or `archived`.

Residual resources retain the retired workspace identity until resolved.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Duplicate `workspace_id` | Block definition or allocation | Existing workspace identity |
| Writable checkout already owned | Block second active owner | Current workspace and source state |
| Shared mutable dependency environment detected | Fail isolation validation | Independent valid workspaces |
| Lock state missing or invalid | Block reproducible synchronization | Source inspection and unrelated work |
| Dependency source unavailable | Use admitted content-addressed cache or block affected sync | Existing synchronized workspaces |
| Port collision | Reallocate through the allocation authority or block service start | Other service allocations |
| Service-name or network collision | Block affected start | Existing services and networks |
| Database or queue namespace collision | Block affected service | Existing authoritative data |
| Secret namespace unresolved | Block dependent service | Other workspace capabilities |
| Resource threshold reached | Queue, throttle, suspend, or reject lower-priority work | Required and bounded work |
| Resource Governor unavailable | Block new heavy or unconstrained work | Existing independently enforced limits and bounded low-risk work |
| Shared infrastructure unavailable | Block dependent capability | Workspaces not using that infrastructure |
| Container runtime unavailable | Block container-dependent services | Native tools and independent work |
| Storage write failure | Block affected mutation; permit declared read-only access | Last durable workspace state |
| Partial allocation failure | Release or isolate incomplete resources | Existing active workspaces |
| Cleanup failure | Retire with recorded residue; block conflicting reuse | Other workspaces |
| Profile-specific bridge or host integration unavailable | Degrade only dependent profile capability | Workspace-local capabilities that remain isolated |
| Candidate artifact validation failure | Reject the candidate | Workspace source and prior admitted artifacts |

Safe degradation never permits shared mutable environments, duplicate allocations, secret leakage, direct cross-component writes, or undeclared authority.

## 8. Cross-Component Interactions

### 8.1 Workspace allocator

The workspace allocator creates workspace identities and coordinates exclusive allocations.

It does not own component source, business data, policy, or release decisions.

### 8.2 Resource Governor

Resource Governor binds and enforces the active workspace resource envelope.

A resource decision cannot authorize a component operation or weaken component data ownership.

### 8.3 Component runtimes

A component runtime uses the workspace's allocated identities, endpoints, data namespaces, and secrets.

The component retains authority over its own data. The workspace is an execution boundary, not a substitute component owner.

### 8.4 Identity and policy authorities

Identity and Trust resolves actors and development identities.

Governance Policy Runtime decides governed privilege or disclosure where applicable.

Ordinary workspace allocation does not create host, component, or publication permission.

### 8.5 Service infrastructure

Database, cache, queue, search, and container services expose declared workspace-scoped interfaces.

Shared service processes retain separate credentials and logical namespaces.

### 8.6 Build and release authorities

A workspace can produce source changes, test results, SBOMs, provenance, packages, images, and other candidate artifacts.

Build Farm, signing authority, artifact admission, Release Set authority, and production activation remain separate.

### 8.7 Audit and evidence

Workspace validation emits structured results and required receipts.

Audit Broker and evidence registries retain cross-component evidence without owning workspace source or runtime state.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- workspace is the complete isolation unit;
- every active workspace has one stable `workspace_id`;
- the identifier namespaces all mutable resources;
- worktree is not the complete isolation boundary;
- parallel applications and branches are supported;
- every Python workspace owns its mutable `.venv`;
- UV's content-addressed cache can be shared;
- shared mutable installed environments are prohibited;
- host ports use exclusive workspace allocations;
- fixed internal ports can be reused inside isolated networks;
- shared infrastructure does not create shared data ownership;
- each workspace has a resource budget;
- cleanup of one workspace does not affect another;
- profile-specific mechanisms remain profile-scoped;
- local success does not create production authority.

Prohibited assumptions include:

- using a directory name as the only workspace identity;
- treating a worktree as dependency or service isolation;
- sharing a writable checkout between active workspaces;
- sharing a mutable `.venv`;
- globally installing application dependencies;
- selecting a convenient unused port without an allocation record;
- inventing a canonical port range;
- treating a shared PostgreSQL process as shared database ownership;
- reusing service credentials across workspaces by default;
- writing secrets into `.env` files that are committed or broadly readable;
- using one queue or consumer identity for unrelated workspaces;
- allowing one cleanup command to delete another workspace's resources;
- removing resource controls during pressure;
- treating a container name, database schema, or host process as architectural authority;
- applying Linux, WSL, container, or virtualization implementation details globally;
- treating a recipe as the owner of workspace rules;
- treating local tests as production activation evidence by themselves.

## 10. Validation Criteria

Workspace isolation validates when:

1. the workspace artifact validates against `developer-workspace.schema.json`;
2. `workspace_id` is unique among active and unresolved retired workspaces;
3. the source checkout has one active writable owner;
4. mutable dependency environments are distinct;
5. Python workspaces have distinct `.venv` directories;
6. `pyproject.toml`, `uv.lock`, and Python version declarations resolve;
7. frozen synchronization reproduces the committed dependency state;
8. shared caches are content-addressed, disposable, and non-authoritative;
9. service, container, and network names do not collide;
10. every host port has an exclusive active allocation;
11. database, schema, role, queue, index, and writable-path ownership remains explicit;
12. direct cross-component authoritative writes are absent;
13. secrets, identities, and certificates remain within declared scope;
14. sockets, PID files, temporary paths, and logs are workspace-scoped;
15. resource controls apply before heavy or unbounded work starts;
16. two representative workspaces can run concurrently;
17. failure of one representative workspace does not mutate the other;
18. removal of one representative workspace does not stop, delete, revoke, or reallocate the other;
19. residual resources block conflicting identity or allocation reuse;
20. profile-specific mechanisms remain in profile or toolchain contracts;
21. candidate outputs retain development-candidate status;
22. every referenced decision, requirement, lock, test, evidence item, and exception resolves;
23. no unresolved marker, placeholder, duplicate canonical owner, or hash field appears;
24. `CHECK-DEV-001` and applicable Interfile Alignment Locks pass.

Applicable checks include:

```bash
python docs/tools/check_profile_composition.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

### 11.1 Parallel branches

Two workspaces run:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
```

Each has its own worktree, `.venv`, host ports, database identity, queue namespace, secrets, logs, temporary paths, processes, and resource envelope.

### 11.2 Shared UV cache

The two workspaces use one content-addressed UV cache.

They still have separate `.venv` directories. Removing either `.venv` does not modify the other workspace.

### 11.3 Shared PostgreSQL server

Two workspaces use one PostgreSQL process.

Each uses separate credentials and a separate database or owned schema. A migration in one workspace cannot write into the other's authoritative objects.

### 11.4 Internal and host ports

Two isolated workspace networks both use internal port `5432` for PostgreSQL.

Their host-facing endpoints are separately allocated. This document does not prescribe the numeric host ports.

### 11.5 Failed cleanup

A retired workspace leaves a container volume after cleanup fails.

The volume retains the retired `workspace_id`. A new workspace cannot claim the same mutable resource until reconciliation completes.

### 11.6 Development candidate

A workspace builds and tests a runtime package successfully.

The package remains a candidate until build, signing, evidence, artifact-admission, Release Set, and activation authorities complete their respective procedures.
