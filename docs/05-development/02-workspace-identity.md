<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-CONTAINER-001",
    "DEC-OFFLINE-001"
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
    "REQ-DEV-WS-024"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DATA-001",
    "LOCK-COMP-002",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-DEV-000"
  ],
  "tags": [
    "development",
    "workspace",
    "identity",
    "worktree",
    "namespace",
    "isolation"
  ]
}
KOA:DOC-META:END -->

# Workspace Identity

## 1. Purpose

This document defines the stable identity model for kOA development workspaces.

A development workspace is an independently executable and removable unit associated with one repository checkout, branch workspace, or worktree. It can host source code, a toolchain environment, local services, ports, databases, secrets, temporary state, generated files, logs, test evidence, and resource budgets.

The workspace identity model prevents two concurrent development activities from silently sharing mutable state. It also permits a workspace to move, reconnect, restart, or recover without changing the identity of its resources.

The model supports:

- native Linux development;
- Windows development through WSL;
- repositories with one active checkout;
- several branches active in parallel;
- several worktrees from the same repository;
- several components active on the same host;
- native processes and rootless containers;
- online and offline development;
- deterministic cleanup and recovery;
- profile-specific implementation without profile-specific identity semantics.

The identity is architectural metadata. It is not a user identity, tenant identity, component identity, release identity, artifact identity, Git commit identity, or host identity.

## 2. Scope

### 2.1 Included workspace units

This document applies to every active development unit classified as one of:

- repository workspace;
- branch workspace;
- Git worktree;
- temporary migration workspace;
- validation workspace;
- component workbench workspace;
- integration-test workspace.

A repository can contain several active workspaces. A branch can also have several independent workspace instances when their state must remain separate.

### 2.2 Included namespaced resources

Workspace identity applies to mutable or collision-prone resources, including:

- Python virtual environments;
- dependency installation state;
- process and service names;
- rootless container names;
- container networks;
- container volumes;
- database names or schemas;
- database service identities;
- message queues and topics used for local development;
- local object-store buckets;
- Unix sockets;
- named pipes used by WSL tooling;
- PID files;
- temporary directories;
- log directories;
- generated local certificates;
- development secrets;
- host ports;
- test fixtures with mutable lifecycle;
- local caches that are not safely content-addressed;
- resource budgets;
- heavy-job slots;
- diagnostic captures;
- local service discovery records.

### 2.3 Resources outside workspace authority

Workspace identity does not own:

- component identities;
- source repository identity;
- Git commit identity;
- accepted architectural decisions;
- canonical requirements or locks;
- release-channel identities;
- published artifacts;
- production credentials;
- production data;
- user profile identity;
- shared immutable or content-addressed download caches;
- host operating-system package state;
- another workspace’s state.

### 2.4 Profile applicability

The model applies to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- another development profile that explicitly adopts the same workspace contract.

A profile owns its storage locations, service manager, port allocator, secret backend, resource-control implementation, and host integration. Those implementation choices do not change the identity lifecycle described here.

### 2.5 Explicit non-goals

This document does not:

- require containers;
- require Kubernetes;
- require one repository per component;
- require one branch per workspace;
- require a globally unique Internet identifier;
- derive identity from an absolute filesystem path;
- derive identity from a file-content hash;
- define Git branching policy;
- define the internal structure of every toolchain;
- publish development state as a runtime artifact;
- make a shared cache authoritative;
- allow production state in a development workspace.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/profiles/developer-linux-workstation.profile.json` | Owns the Linux implementation profile, required isolation outcomes, workspace resource namespaces, and local development behavior. |
| `contracts/profiles/developer-windows-wsl.profile.json` | Owns the Windows and WSL implementation profile, host-to-WSL boundary, filesystem placement, port exposure, and equivalent isolation outcomes. |
| `contracts/toolchains/python-uv.toolchain.json` | Owns Python and UV-specific workspace behavior, including one workspace-owned `.venv`, lockfile use, and frozen synchronization. |

Supporting authority is owned by:

- `generated/decision-index.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/component-catalog.json`;
- `contracts/integration-types.contract.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- `generated/exception-index.json`.

This document explains the identity model. The registries and contracts above own canonical values and lifecycle status.

## 4. Model and Responsibilities

### 4.1 Workspace identity fields

A workspace identity contains at least:

| Field | Meaning |
| --- | --- |
| `workspace_id` | Stable machine identifier for one workspace instance. |
| `component_id` | Primary component or bounded workbench associated with the workspace. |
| `purpose_slug` | Human-readable branch, task, migration, or workbench purpose. |
| `unique_suffix` | Locally collision-resistant suffix assigned at creation. |
| `profile_id` | Active development profile. |
| `repository_ref` | Stable repository identity or configured repository reference. |
| `checkout_ref` | Branch, worktree, detached commit, or other source checkout reference. |
| `workspace_root` | Current profile-local filesystem location. |
| `created_at` | Creation time recorded by the local allocator. |
| `lifecycle_state` | Current identity state. |

Optional fields can record:

- parent workspace;
- migration source;
- host identifier;
- WSL distribution;
- selected workbenches;
- allocated ports;
- allocated service names;
- allocated data namespaces;
- secret namespace;
- resource budget;
- last validation result;
- retirement evidence.

### 4.2 Canonical identifier format

The machine identifier uses the pattern:

```text
^[a-z0-9]+(?:-[a-z0-9]+)*-[a-z0-9]{4,12}$
```

The intended derivation is:

```text
component-or-workbench + purpose-slug + unique-suffix
```

Examples:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-migration-b114
uckk-preview-fix-71ac2
```

The suffix provides local collision resistance. It is not a content hash and does not claim global uniqueness.

### 4.3 Stable identity and mutable labels

`workspace_id` remains stable for the lifetime of the workspace.

The following can change without changing the workspace identity:

- directory path;
- human label;
- branch name;
- worktree location;
- host mount point;
- WSL distribution path;
- display name;
- selected local port numbers after controlled reallocation.

A new independent copy receives a new workspace identity even when source content, branch, commit, or directory name is identical.

### 4.4 Identity registry responsibility

Each development host or profile provides a local workspace identity registry or equivalent machine-readable allocator.

The allocator is responsible for:

- assigning unique active identifiers;
- preventing duplicate active registrations;
- recording current root paths;
- binding resources to workspace identity;
- recording lifecycle transitions;
- preserving retired identifiers from accidental immediate reuse;
- validating cleanup;
- supporting recovery after host or service restart.

The implementation location is profile-owned. The identity semantics remain global.

### 4.5 Resource namespace derivation

Every mutable resource derives a namespace from `workspace_id` or stores an explicit binding to it.

Examples include:

```text
service name: koa-<workspace_id>-<service>
network name: koa-<workspace_id>
volume name: koa-<workspace_id>-<purpose>
database: koa_<workspace_id_normalized>_<component>
socket directory: <profile-runtime-root>/<workspace_id>/
secret scope: workspace/<workspace_id>/
log scope: <profile-state-root>/<workspace_id>/logs/
```

A profile can use another transformation when it is deterministic, reversible to the workspace record, collision-safe on the target platform, and validated.

### 4.6 Filesystem location

The absolute workspace path is an attribute, not the identity.

Native Linux profiles keep mutable environments and services in Linux-native locations selected by the profile.

Windows and WSL profiles preserve Linux toolchain and mutable dependency state inside the selected WSL filesystem when required by the toolchain contract. Windows-visible source or editor integration does not authorize sharing one mutable environment across WSL workspaces.

Case-insensitive host paths, path aliases, mount aliases, symbolic links, junctions, and WSL path translations are normalized before duplicate-root validation.

### 4.7 Toolchain responsibility

A toolchain uses the workspace identity to bind mutable installation state.

For Python with UV:

- the workspace owns one `.venv`;
- `uv.lock` is the version-controlled dependency resolution;
- frozen synchronization validates installed dependencies;
- a shared download cache remains non-authoritative;
- another workspace cannot activate or modify this workspace’s `.venv`.

Other toolchains adopt equivalent isolation through their own contracts.

### 4.8 Service and port responsibility

A workspace receives its own service namespace and host-port allocation.

Internal container or process ports can be fixed when isolation prevents collisions. Host ports are allocated per workspace and recorded.

A service process validates its workspace binding before opening authoritative local state.

### 4.9 Data and secret responsibility

Development databases, schemas, buckets, queues, temporary data, and secrets are bound to one workspace.

A shared database engine is permitted only when each workspace has separate database or schema identity, separate credentials, and no direct cross-component authoritative writes.

Production credentials and production user data remain outside the development workspace contract.

### 4.10 Resource responsibility

Each workspace has a resource budget.

The budget can include:

- CPU;
- memory;
- process count;
- storage;
- I/O priority;
- network egress;
- queue depth;
- concurrent heavy jobs.

Resource Governor or a profile-approved equivalent enforces these limits without changing workspace identity.

### 4.11 Lifecycle states

The workspace identity lifecycle is:

```text
allocated
  -> initializing
  -> active
  -> suspended
  -> recovering
  -> active
  -> retiring
  -> retired
```

Failure states can include:

```text
conflicted
orphaned
cleanup_incomplete
```

A retired identity remains historical. Reactivating the same source in a new independent workspace creates a new identifier.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-WS-001,REQ-DEV-WS-002,REQ-DEV-WS-003,REQ-DEV-WS-004,REQ-DEV-WS-005,REQ-DEV-WS-006,REQ-DEV-WS-007,REQ-DEV-WS-008,REQ-DEV-WS-009,REQ-DEV-WS-010,REQ-DEV-WS-011,REQ-DEV-WS-012,REQ-DEV-WS-013,REQ-DEV-WS-014,REQ-DEV-WS-015,REQ-DEV-WS-016,REQ-DEV-WS-017,REQ-DEV-WS-018,REQ-DEV-WS-019,REQ-DEV-WS-020,REQ-DEV-WS-021,REQ-DEV-WS-022,REQ-DEV-WS-023,REQ-DEV-WS-024 -->
- **REQ-DEV-WS-001 — SHALL:** Every active repository workspace, branch workspace, worktree, migration workspace, validation workspace, and component workbench have one explicit `workspace_id`.
- **REQ-DEV-WS-002 — SHALL:** `workspace_id` remain stable for the workspace lifetime and match the canonical identifier pattern.
- **REQ-DEV-WS-003 — SHALL NOT:** An absolute path, branch name, commit identifier, user name, process identifier, port, container identifier, or file-content hash be the sole workspace identity.
- **REQ-DEV-WS-004 — SHALL:** A copied, cloned, duplicated, or independently initialized workspace receive a new `workspace_id`.
- **REQ-DEV-WS-005 — SHALL NOT:** Two active workspaces share the same `workspace_id`, mutable dependency environment, secret namespace, service namespace, temporary-data namespace, or resource budget.
- **REQ-DEV-WS-006 — SHALL:** Every mutable or collision-prone development resource be namespaced by or explicitly bound to one workspace identity.
- **REQ-DEV-WS-007 — SHALL:** Every Python and UV workspace own one local `.venv` and use its declared lockfile and Python-version contract.
- **REQ-DEV-WS-008 — SHALL NOT:** A shared cache contain or become a shared mutable installed workspace environment.
- **REQ-DEV-WS-009 — SHALL:** Host ports be allocated per workspace and recorded in a collision-checked allocation mechanism.
- **REQ-DEV-WS-010 — SHALL:** Shared service engines preserve separate workspace database, schema, queue, bucket, volume, credential, and authority boundaries.
- **REQ-DEV-WS-011 — SHALL NOT:** A workspace write directly into another workspace’s mutable state or another component’s authoritative storage.
- **REQ-DEV-WS-012 — SHALL:** Development secrets and generated local credentials remain scoped to one workspace and outside source control.
- **REQ-DEV-WS-013 — SHALL NOT:** Production credentials or production user data be included in a development workspace by default.
- **REQ-DEV-WS-014 — SHALL:** Each active workspace have a bounded CPU, memory, process, storage, queue, and heavy-work resource policy appropriate to its profile.
- **REQ-DEV-WS-015 — SHALL:** Moving or renaming a workspace update its registered path without changing its identity.
- **REQ-DEV-WS-016 — SHALL:** Path normalization detect aliases, symbolic links, junctions, mounts, case-folding collisions, and Windows-to-WSL path equivalence before activation.
- **REQ-DEV-WS-017 — SHALL:** Workspace startup validate identity, root path, toolchain environment, service namespace, data namespace, secret namespace, ports, and resource budget.
- **REQ-DEV-WS-018 — SHALL:** Workspace recovery reconcile registered resources before starting processes or accepting mutable operations.
- **REQ-DEV-WS-019 — SHALL NOT:** Recovery silently adopt unbound services, databases, secrets, ports, environments, or files from another workspace.
- **REQ-DEV-WS-020 — SHALL:** Workspace retirement stop services, release ports, revoke local credentials, remove or archive mutable state according to policy, and record cleanup results.
- **REQ-DEV-WS-021 — SHALL NOT:** Workspace retirement remove another workspace’s state, shared immutable caches, source repository history, or published artifacts.
- **REQ-DEV-WS-022 — SHALL:** Retired workspace identifiers remain traceable and not be immediately reused for an unrelated workspace.
- **REQ-DEV-WS-023 — SHALL:** Offline workspace operation preserve identity and local resource bindings without requiring a remote registry or control plane.
- **REQ-DEV-WS-024 — SHALL NOT:** A profile, recipe, editor integration, container runtime, generated context, migration shortcut, or implementation convenience silently weaken workspace identity or isolation.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Workspace allocation

Allocation proceeds through:

1. Select the development profile.
2. Identify the repository.
3. Identify the component or workbench.
4. Select the branch, worktree, commit, migration, or validation purpose.
5. Normalize the proposed workspace root.
6. Check for an existing registered workspace at the same effective root.
7. Create the human-readable purpose slug.
8. Generate a locally collision-resistant suffix.
9. Compose the candidate `workspace_id`.
10. Verify that the candidate is not active or retired under a conflicting record.
11. Register the identity in `allocated` state.
12. Allocate resource namespaces.
13. Create the toolchain environment and local configuration.
14. Validate isolation.
15. Transition to `active`.

### 6.2 Workspace startup

Startup includes:

1. Resolve the workspace record.
2. Normalize and compare the current root path.
3. Validate repository and checkout references.
4. Validate the toolchain contract.
5. Validate the workspace-owned mutable environment.
6. Resolve ports and service names.
7. Resolve database, schema, queue, bucket, and volume bindings.
8. Resolve secrets and generated local credentials.
9. Apply the resource budget.
10. Detect active collisions.
11. Start bounded services.
12. Record successful activation.

A failed validation leaves the workspace inactive or conflicted.

### 6.3 Path move or rename

A move or rename proceeds through:

1. Stop mutable services or place the workspace in a safe suspended state.
2. Verify that the destination path does not alias an active workspace.
3. Move or remount the workspace.
4. Update the root path in the identity registry.
5. Update profile-specific path bindings.
6. Revalidate the toolchain environment and service configuration.
7. Preserve `workspace_id`.
8. Return to active state.

### 6.4 Branch rename or checkout change

A branch rename does not change workspace identity.

A controlled checkout change records the new checkout reference and validates whether existing mutable state remains compatible. Incompatible dependency, database, generated-state, or service changes require migration, reset, or a new workspace.

A checkout change that creates a distinct concurrent activity uses a new workspace.

### 6.5 Copy, clone, or duplicate

When a workspace is copied:

1. Treat copied identity metadata as non-active source material.
2. Allocate a new workspace identity.
3. Remove or regenerate local credentials.
4. Allocate new ports and service names.
5. Create new database, schema, queue, bucket, and volume identities.
6. Rebuild or validate the toolchain environment.
7. Preserve only explicitly shareable immutable caches.
8. Validate before activation.

### 6.6 Collision handling

When a collision is detected:

1. Mark the candidate or affected workspace as conflicted.
2. Stop new mutable operations.
3. Identify the colliding resource.
4. Identify the legitimate owning workspace.
5. Preserve evidence and existing authoritative local state.
6. Reallocate the candidate resource or recover the correct owner binding.
7. Revalidate both workspaces.
8. Resume only after isolation passes.

### 6.7 Recovery after host or service failure

Recovery proceeds through:

1. Load the local workspace registry.
2. Discover workspace roots and bound resources.
3. Compare discovered state with registered ownership.
4. Mark missing, duplicate, or unbound resources.
5. Keep unbound mutable services stopped.
6. Restore or reallocate ports.
7. Restore service, data, secret, and resource bindings.
8. Validate toolchain environments.
9. Start only reconciled workspaces.
10. Record recovery results.

### 6.8 Retirement

Retirement proceeds through:

1. Transition the workspace to `retiring`.
2. Stop processes and services.
3. Drain or cancel bounded development queues.
4. Release host ports.
5. Revoke workspace-local credentials and certificates.
6. Export required diagnostics or evidence.
7. Remove the workspace-owned mutable dependency environment.
8. Remove or archive databases, schemas, queues, buckets, volumes, logs, and temporary data according to policy.
9. Preserve source history and explicitly shared immutable caches.
10. Validate that no live resource remains bound to the workspace.
11. Record cleanup exceptions.
12. Transition to `retired`.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Duplicate active `workspace_id` | Mark conflict and block activation. | Existing validated owner | Candidate activation |
| Root path aliases another workspace | Block activation until paths are separated. | Existing workspace | Duplicate root |
| Copied identity metadata detected | Allocate a new identity. | Copied source content | Reuse of copied identity |
| `.venv` belongs to another workspace | Refuse activation and rebuild locally. | Source and lockfile | Shared mutable environment |
| Lockfile and installed environment disagree | Require frozen synchronization or explicit update. | Source editing | Validated execution claim |
| Port collision | Allocate another port or keep service stopped. | Other services | Colliding service |
| Database identity collision | Block affected service. | Existing database owner | Ambiguous database writes |
| Secret namespace collision | Block workspace activation. | Existing secret owner | Shared secret use |
| Resource budget missing | Apply profile-safe default or block heavy work. | Lightweight local tasks | Unbounded heavy work |
| Local registry unavailable | Use validated local cached record only when profile policy permits. | Existing offline workspace | New uncertain allocation |
| Unbound service discovered | Keep it stopped and quarantine its state. | Registered services | Unowned execution |
| Root path missing | Mark workspace orphaned. | Registry and recoverable resources | Normal startup |
| Partial cleanup | Mark `cleanup_incomplete` and preserve evidence. | Other workspaces | Identity retirement completion |
| WSL distribution unavailable | Keep Windows-side metadata inactive. | Source backup and registry | Linux toolchain execution |
| Case-folding collision | Block the newer conflicting root. | Existing root | Ambiguous activation |
| Shared cache unavailable | Continue with available local state or retrieve later. | Existing installed workspace environment | Uncached retrieval |
| Network unavailable | Continue local registered operation. | Local source, tools, services, tests | Remote synchronization |
| Host restart | Reconcile resources before restart. | Persistent workspace state | Blind automatic process adoption |
| Identity record corrupt | Stop mutable services and recover from evidence or backup. | Source repository | Unverified state mutation |
| Another workspace failure | Isolate the failure. | Unrelated workspaces | Only the affected workspace |

Safe degradation keeps uncertain workspaces inactive. It does not merge identities, share mutable environments, adopt unknown services, reuse credentials, or delete another workspace’s state.

## 8. Cross-Component Interactions

### 8.1 Workspace and component contracts

A workspace selects one primary component or bounded workbench. Component contracts continue to own application responsibilities and authoritative data boundaries.

Workspace identity namespaces local execution state but does not create a new component identity.

### 8.2 Workspace and toolchain contracts

The toolchain reads the workspace identity and creates workspace-owned mutable installation state.

The workspace document does not redefine UV, Python, Node, Rust, container, or another toolchain’s internal behavior.

### 8.3 Workspace and Resource Governor

The workspace registers a resource budget with Resource Governor or a profile-approved equivalent.

Resource decisions can pause, throttle, queue, or deny work without changing workspace identity or component authority.

### 8.4 Workspace and local services

Local databases, queues, search services, caches, and object stores receive workspace-scoped service and data identities.

A shared engine can host several isolated workspace namespaces. It cannot expose unrestricted cross-workspace mutation.

### 8.5 Workspace and secret storage

The secret backend resolves the exact workspace identity before returning a secret.

A user or service credential reused intentionally across workspaces is represented as separately authorized references, not as one silently shared mutable secret namespace.

### 8.6 Workspace and source control

Source control owns repository, commit, branch, and worktree relationships.

Workspace identity references those objects but remains distinct. A Git operation does not allocate or retire infrastructure resources by itself.

### 8.7 Workspace and editor integration

An editor can discover the current workspace and activate its tools.

Editor state does not become the canonical workspace registry. Opening the same directory in another editor does not create a second identity.

### 8.8 Workspace and containers

Container names, networks, volumes, labels, and service identities include or bind to workspace identity.

Changing container runtime does not change workspace identity or application contract semantics.

### 8.9 Workspace and WSL

Windows host tools and WSL development services exchange explicit path and port mappings.

The active Linux toolchain environment remains bound to one WSL workspace. Windows filesystem aliases, WSL mount aliases, and distribution boundaries are checked before activation.

### 8.10 Workspace and publication lifecycle

Development outputs are candidate artifacts.

Workspace environments, local services, secrets, ports, caches, logs, and test databases are not published as runtime artifacts. Publication uses artifact and release contracts independently from workspace identity.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the workspace identity baseline.

The following assumptions are prohibited:

1. A directory path is a stable workspace identity.
2. A branch name is a stable workspace identity.
3. One branch can have only one workspace instance.
4. A copied workspace can reuse copied identity metadata.
5. The same commit implies the same workspace.
6. A process identifier can identify a workspace permanently.
7. A fixed host port can be reused safely by every worktree.
8. A shared database engine implies shared database identity.
9. A shared download cache is a shared installed environment.
10. A `.venv` can be shared by two active worktrees.
11. A global Python environment is part of the workspace contract.
12. An editor workspace file is the canonical identity registry.
13. A container name assigned by a runtime is sufficient identity.
14. A Windows path and WSL path are always distinct.
15. Paths that differ only by case are always distinct.
16. A symbolic link creates a new workspace.
17. Moving a workspace creates a new identity.
18. Renaming a branch creates a new identity.
19. Changing a checkout is always safe with existing mutable state.
20. An unbound local service can be adopted automatically.
21. A retired workspace identifier can be immediately reused.
22. Retirement can delete shared immutable caches or another workspace’s data.
23. Remote connectivity is required to preserve identity.
24. A profile can omit isolation because the host is personal.
25. A recipe or editor convenience can weaken the identity model.

When identity, path, ownership, namespace, or lifecycle state is ambiguous, activation remains blocked until the local record and resources are reconciled.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-DEV-002`.
2. Its path is `05-development/02-workspace-identity.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `development`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every active workspace has one valid `workspace_id`.
16. Active workspace identifiers are unique.
17. Workspace identifiers match the canonical pattern.
18. Duplicate source content receives a new identity.
19. Workspace paths are normalized and collision-checked.
20. Moves and renames preserve identity.
21. Each Python and UV workspace has one workspace-owned `.venv`.
22. Shared caches contain no mutable installed environment.
23. Ports, services, data, secrets, temporary state, and resource budgets are workspace-scoped.
24. Direct cross-workspace and cross-component authoritative writes fail validation.
25. Recovery does not adopt unbound mutable state.
26. Retirement releases or records every workspace-owned mutable resource.
27. Retired identifiers remain traceable.
28. Native Linux and Windows/WSL profiles produce equivalent identity and isolation outcomes.
29. Offline operation preserves identity without remote authority.
30. Runtime publication excludes workspace environments and mutable development state.
31. Traceability and active evidence are complete.
32. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
33. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Two worktrees from one repository

A developer creates `konnaxion-main-a31f` and `konnaxion-feature-voting-92cd`. Each worktree has its own `.venv`, ports, database identity, secrets, logs, and resource budget even though both use the same repository and shared UV download cache.

### 11.2 Directory rename

The directory for `orgo-migration-b114` is renamed. The local registry updates `workspace_root`, but the workspace identifier, ports, service names, database identity, and evidence remain unchanged.

### 11.3 Copied workspace

A developer copies a directory to investigate a defect. Copied local identity metadata is not activated. The allocator creates a new workspace identifier and new resource namespaces before services start.

### 11.4 Shared PostgreSQL engine

Two workspaces use one local PostgreSQL process. They have separate database names, credentials, and schema ownership. Neither workspace can write to the other database.

### 11.5 Linux and WSL parity

A Linux host and a Windows/WSL host use different profile-owned storage locations and port exposure mechanisms. Both assign the same kind of stable workspace identity and enforce one mutable environment per workspace.

### 11.6 Port collision

A manually started process occupies a requested host port. The allocator assigns another available port and updates the workspace record rather than stopping the unrelated process or reusing the port.

### 11.7 Offline startup

The developer starts a registered workspace without network access. Local source, `.venv`, services, tests, and identity validation work. Remote fetch and uncached dependency retrieval remain unavailable.

### 11.8 Orphaned workspace

The registry contains a workspace whose root directory is missing after a disk change. The workspace becomes orphaned. Services remain stopped until the root is restored or the identity is retired.

### 11.9 Incomplete cleanup

A database volume cannot be removed during retirement. The workspace enters `cleanup_incomplete`, the unresolved volume remains bound to the retired identity, and the identifier is not reused.

### 11.10 Branch rename

A feature branch is renamed for clarity. The workspace keeps its existing identity because the workspace instance and its mutable state continue unchanged.
