<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-015",
  "document_class": "adr",
  "version": "1.0.0",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
  "owner": "development-architecture",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-DEV-001",
    "generated/decision-index.json#/decisions/DEC-DEV-002",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "schemas/developer-workspace.schema.json",
    "contracts/artifact-contracts/developer-workspace.schema.json",
    "contracts/artifact-contracts/workspace-port-allocation.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002"
  ],
  "requirement_ids": [
    "REQ-DEV-UV-001",
    "REQ-DEV-UV-002"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005"
  ],
  "adr_ids": [
    "ADR-015"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
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
    "DOC-DEV-011",
    "DOC-DEV-012",
    "DOC-DEV-013",
    "DOC-DEV-014",
    "DOC-DEV-015",
    "DOC-DEV-016",
    "DOC-CONF-017"
  ],
  "tags": [
    "adr",
    "development",
    "workspace",
    "isolation",
    "uv",
    "python",
    "virtual-environment",
    "parallel-branches",
    "ports",
    "networks",
    "databases",
    "secrets",
    "resources",
    "reproducibility"
  ],
  "effective_at": "2026-08-03T19:36:00-04:00"
}
KOA:DOC-META:END -->

# ADR-015: Development Workspace Isolation with UV

## Status

**Accepted**

- **ADR ID:** `ADR-015`
- **Owner decisions:** `DEC-DEV-001`, `DEC-DEV-002`
- **Effective date:** 2026-08-03
- **Decision owner:** Development Architecture
- **Applicable profiles:** `developer_linux_workstation`, `developer_windows_wsl`
- **Change class:** Major when workspace identity, Python isolation, parallel-execution, or mutable-state boundaries change

## Context

kOA development must support several applications and several branches of the same application on one workstation.

A branch checkout alone is not an isolated workspace. Development activity also creates mutable state in:

- language dependency environments;
- service processes;
- containers or equivalent runtime namespaces;
- networks;
- host ports;
- volumes;
- databases, users, and schemas;
- queues;
- sockets;
- temporary directories;
- logs and process identifiers;
- secret namespaces;
- generated local certificates;
- resource budgets.

Without a stable workspace identity and explicit namespace rules, developers encounter collisions, implicit state sharing, non-reproducible validation, cross-branch database mutation, stale sockets, overwritten secrets, and accidental dependency on production-like global state.

Python dependency isolation solves only one portion of this problem. A virtual environment does not isolate PostgreSQL, Redis, search services, queues, ports, persistent volumes, system libraries, secrets, or resource consumption.

The architecture therefore needs one decision for workspace-local dependency environments and another for collision-free simultaneous workspaces.

## Decision

Every active development workspace has:

```text
one stable workspace_id
one mutable dependency environment
one secret namespace
one temporary-data namespace
one service namespace
one isolated logical network
one host-port allocation set
one database identity set
one resource budget
one explicit lifecycle
```

The canonical workspace identifier is derived from:

```text
component + branch_or_purpose + unique_suffix
```

Examples:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
```

The `workspace_id` prefixes or namespaces every mutable collision domain.

For Python workspaces:

```text
dependency manager: UV
project manifest: pyproject.toml
dependency lock: uv.lock
Python version: explicitly declared
installed environment: one workspace-local .venv
reproducible validation: uv sync --frozen
```

Global application dependency installation is prohibited.

Sharing a mutable `.venv` is prohibited.

A content-addressed UV download cache can be shared because it is a download optimization rather than an installed dependency environment.

At least two applications, or two branches of one application, must be runnable simultaneously without collisions.

## Decision Drivers

The decision is driven by these needs:

1. deterministic dependency installation;
2. reproducible validation from versioned manifests and lockfiles;
3. simultaneous work on main, feature, migration, and repair branches;
4. prevention of port, database, volume, secret, socket, and process-name collisions;
5. independent workspace creation and teardown;
6. explicit ownership of mutable development state;
7. compatibility with both native Linux and Windows WSL profiles;
8. separation of development state from release artifacts;
9. bounded resource use;
10. preservation of component data ownership inside development;
11. clean promotion from source revision to immutable artifact;
12. removal of hidden workstation-global dependencies.

## Workspace Identity

A workspace contract records at least:

```text
workspace_id
component_id
branch_or_purpose
unique_suffix
profile_id
repository identity
source ref
workspace root
runtime versions
service definitions
state namespaces
port allocations
network identity
database identities
secret references
resource envelope
lifecycle state
validation commands
```

The stable workspace identity is not a display label.

The same display name can appear in different contexts only when the full stable identity remains unique.

The identifier prefixes or namespaces:

- containers;
- networks;
- volumes;
- database names;
- database users;
- database schemas;
- Unix sockets or equivalent local IPC paths;
- temporary directories;
- log directories;
- PID files;
- service names;
- secret names;
- local certificates;
- queues;
- allocated host ports.

A workspace contract validates before activation.

## Python and UV

UV owns the canonical Python development workflow for the applicable development profiles.

A conformant Python workspace contains versioned:

```text
pyproject.toml
uv.lock
.python-version
```

Its installed environment is:

```text
<workspace-root>/.venv
```

Reproducible validation begins with:

```text
uv sync --frozen
```

The validation flow does not refresh `uv.lock` implicitly.

Dependency upgrades are explicit changes that include:

- changed project constraints where applicable;
- changed `uv.lock`;
- impact analysis;
- relevant tests;
- review of generated artifacts or migrations;
- updated evidence.

The shared UV cache contains content-addressed downloads. It does not contain an authoritative shared installed environment.

Deleting one workspace's `.venv` does not alter another workspace.

## Non-Python Mutable State

UV does not isolate infrastructure or application state.

Each workspace separately isolates or namespaces:

| State class | Isolation expectation |
| --- | --- |
| Services | Workspace-prefixed service or container identity |
| Network | Isolated logical network with no default cross-workspace connectivity |
| Internal ports | Fixed ports allowed inside the isolated workspace network |
| Host ports | Atomic allocation through the workspace-scoped registry |
| Databases | Workspace-scoped database identity, database or schema |
| Volumes | Workspace-prefixed persistent or temporary volume identity |
| Sockets | Workspace-scoped runtime and socket paths |
| Queues | Workspace-prefixed queue, stream, or topic identity |
| Secrets | Workspace-scoped references and generated local credentials |
| Logs and temporary data | Workspace-scoped paths and retention |
| Resources | Workspace-specific CPU, memory, process, I/O, queue, and heavy-job bounds |

Cross-workspace links are explicit, bounded, attributable, revocable, and separately tested.

A shared physical service is permitted only when the workspace contracts preserve logical identity and mutable-state isolation.

## Component and Data Boundaries

Workspace isolation does not weaken component boundaries.

Each component retains authority over its own source records.

One component does not write directly to another component's authoritative source tables, even when both run inside one workspace or share a physical database server.

Cross-component behavior uses declared:

- commands;
- queries;
- events;
- gateways;
- artifacts.

Development fixtures, migrations, and tests use component-owned interfaces or explicitly owned test setup contracts.

Database-administrator access does not become component business authority.

## Parallel Execution

The passing baseline includes a behavioral parallel-execution test.

The test activates at least two distinct workspace identities and verifies collision-free operation for:

- service names;
- process identifiers;
- internal and host ports;
- networks;
- volumes;
- databases;
- database users and schemas;
- queues;
- sockets;
- secret references;
- local certificates;
- temporary files;
- log paths;
- resource budgets.

The test also removes or tears down one workspace and proves that the other remains operational.

Static name inspection alone is insufficient because collisions can occur in bind addresses, database credentials, runtime directories, or external service configuration.

## Resource Governance

Every workspace declares a resource budget.

The budget includes bounded:

- CPU;
- memory;
- process count;
- I/O;
- queue depth;
- concurrent heavy jobs;
- execution time where applicable.

Heavy services and intensive jobs are task-activated rather than permanently started when the active development profile defines them that way.

Resource Governor evaluates workload admission and limits.

Resource availability does not authorize a component operation or governed disclosure.

## Native Linux and Windows WSL

The two development profiles share the workspace model but remain distinct claims.

### Native Linux

The `developer_linux_workstation` profile evaluates the workspace directly within the declared Linux host boundary.

Rootless containers are preferred when containers are used, but container technology is not the workspace identity model.

### Windows WSL

The `developer_windows_wsl` profile identifies:

- Windows host context;
- selected WSL distribution and version;
- Linux workspace location;
- filesystem boundary;
- container or service runtime;
- host-port exposure;
- name resolution;
- time behavior;
- service lifecycle;
- credential and secret boundary;
- host integrations used by the claim.

Native-Linux evidence is not silently reused as WSL evidence.

Docker or Podman can be selected by the WSL profile. Application contracts remain runtime-independent.

## Workspace Lifecycle

The workspace lifecycle is explicit:

```text
declared
validated
active
suspended
teardown_pending
retired
failed
```

Activation includes:

1. workspace-contract validation;
2. resource reservation;
3. atomic host-port allocation;
4. network and runtime-path creation;
5. database identity creation;
6. secret-reference resolution;
7. service startup;
8. readiness validation;
9. active-state recording.

Teardown includes:

1. stopping workloads;
2. releasing host ports;
3. removing workspace networks and sockets;
4. removing runtime objects;
5. disposing of temporary databases and users;
6. revoking local credentials;
7. removing temporary and log state according to policy;
8. cleaning orphaned processes and identifiers;
9. retaining only approved shared cache material;
10. verifying unaffected peer workspaces.

A partially initialized workspace does not become active.

## Development-to-Release Boundary

Mutable workspace state is not a release artifact.

Promotion follows:

```text
clean source revision
    → declared build
    → tests
    → provenance
    → immutable artifact
    → publication
    → Release Set evaluation
```

The following remain outside release identity:

- `.venv`;
- branch checkout;
- running development container;
- local database;
- temporary volume;
- local queue;
- local secret;
- workspace log;
- mutable generated output not included in an artifact contract.

A successful developer test is evidence for the tested scope. It is not a release claim by itself.

## Consequences

### Positive consequences

- branches and applications can run concurrently;
- Python dependencies are deterministic and local;
- dependency validation does not mutate the lockfile;
- workspace teardown is independent;
- shared downloads remain efficient;
- databases, services, secrets, and ports have explicit owners;
- hidden workstation-global state is reduced;
- development and release boundaries remain clear;
- native Linux and WSL can share architecture without pretending to be identical;
- resource-intensive services remain bounded.

### Costs and tradeoffs

- every workspace requires a machine-readable contract;
- local infrastructure requires namespace-aware configuration;
- host ports need an allocator;
- database and secret creation need lifecycle tooling;
- test suites need parallel-workspace coverage;
- WSL requires additional host-boundary evidence;
- cleanup tooling must detect orphaned state;
- dependency upgrades require explicit lockfile and impact changes;
- developers cannot rely on one globally prepared mutable environment.

### Risks and controls

| Risk | Required control |
| --- | --- |
| Shared cache becomes shared installed state | Enforce content-addressed cache semantics and workspace-local `.venv` |
| Workspace identifier is treated as cosmetic | Validate namespace coverage and behavioral isolation |
| Fixed internal ports are rejected unnecessarily | Permit them inside isolated networks and allocate only host exposure |
| Host ports collide | Use atomic workspace-scoped allocation |
| Database state crosses branches | Use workspace database identities and owner contracts |
| Secrets leak into contracts or logs | Store references and use selective evidence |
| Teardown removes peer state | Test independent lifecycle |
| WSL hides host dependencies | Record and test both sides of the boundary |
| Local success is promoted as release evidence | Require immutable artifact and Release Set flow |
| Resource pressure affects other workspaces | Enforce Resource Governor budgets |

## Alternatives Considered

### One global Python environment

Rejected because application requirements conflict, upgrades affect unrelated branches, and validation cannot reproduce workspace-specific installed state.

### One shared mutable `.venv`

Rejected because it violates dependency isolation and makes concurrent branch validation unsafe.

### Poetry, pip-tools, or unpinned pip as the canonical Python workflow

Not selected for the canonical architecture. The accepted owner decision assigns UV, `pyproject.toml`, and `uv.lock` to the active Python workflow. Other tools can appear only through a successor decision or a bounded non-canonical workflow that does not claim conformance.

### Containers as the complete isolation model

Rejected because containers do not automatically isolate host ports, external databases, secrets, queues, volumes, resource budgets, or component authority.

### One container runtime mandated globally

Rejected because native Linux and Windows WSL have different profile choices, containers are optional for lightweight profiles, and application contracts remain runtime-independent.

### Unique branch names without workspace contracts

Rejected because branch names do not allocate ports, database identities, secrets, sockets, queues, volumes, or resource budgets.

### Sequential development only

Rejected because two applications or branches must be runnable simultaneously.

### Copying mutable workspace state into a release

Rejected because release artifacts require immutable identity, provenance, publication, compatibility, and lifecycle evidence.

## Migration Guidance

Existing development trees migrate in this order:

1. inventory repositories, branches, virtual environments, services, ports, databases, secrets, sockets, volumes, logs, and queues;
2. assign stable `workspace_id` values;
3. create workspace contracts;
4. move Python projects to versioned `pyproject.toml`, `uv.lock`, and declared Python versions;
5. create one local `.venv` per workspace;
6. replace validation installation with `uv sync --frozen`;
7. separate shared downloads from installed environments;
8. namespace services and mutable state;
9. register host ports;
10. create workspace database and secret identities;
11. add resource budgets;
12. test two workspaces concurrently;
13. test independent teardown;
14. remove global application dependency installations and shared mutable environments;
15. preserve deprecated instructions as migration evidence rather than active authority.

Migration does not delete another workspace's state or silently refresh dependency locks.

## Validation

Conformance evidence for this ADR includes:

1. each workspace has a valid stable identity;
2. workspace identity namespaces every declared mutable collision domain;
3. each Python workspace uses UV;
4. `pyproject.toml`, `uv.lock`, and the Python version declaration are versioned;
5. each workspace has exactly one local `.venv`;
6. `uv sync --frozen` completes without modifying `uv.lock`;
7. global application dependency installation is absent;
8. shared mutable `.venv` use is absent;
9. shared cache behavior remains content-addressed and non-installed;
10. two applications or branches run simultaneously;
11. host ports allocate atomically without collision;
12. default cross-workspace network connectivity is absent;
13. database identities and state remain workspace-scoped;
14. direct cross-component authoritative writes are rejected;
15. secret values remain outside contracts and ordinary logs;
16. workspace resource budgets enforce bounded behavior;
17. one workspace can be removed without affecting another;
18. WSL evidence identifies Windows-host and Linux-environment responsibilities;
19. clean-source rebuild and frozen validation are reproducible;
20. development outputs enter release only through immutable artifact and publication contracts.

Expected validation failure codes include:

```text
workspace_identity_missing
workspace_identity_invalid
workspace_contract_invalid
workspace_dependency_environment_shared
workspace_uv_contract_failed
workspace_lockfile_mutated
workspace_shared_cache_became_environment
workspace_mutable_state_collision
workspace_host_port_collision
workspace_network_isolation_failed
workspace_database_identity_shared
workspace_cross_component_write
workspace_secret_embedded
workspace_resource_budget_missing
workspace_parallel_execution_unproven
workspace_teardown_incomplete
workspace_peer_affected_by_teardown
workspace_wsl_boundary_unresolved
workspace_repository_state_unreproducible
workspace_false_release_promotion
```

## Supersession

This ADR remains active until an accepted successor changes `DEC-DEV-001`, `DEC-DEV-002`, the canonical Python toolchain, or the workspace-isolation model.

A successor must:

- preserve explicit profile scope;
- identify compatibility and migration effects;
- define dependency, service, data, network, secret, and resource isolation;
- preserve concurrent workspace execution;
- provide migration and rollback;
- update schemas, locks, tests, evidence, and conformance documents;
- prevent mutable development state from becoming release authority implicitly;
- record supersession in the ADR registry.

Historical copies remain retained and the identifier `ADR-015` remains permanently reserved.
