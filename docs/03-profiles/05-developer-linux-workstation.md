<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "profile:developer_linux_workstation"
  ],
  "canonical_refs": [
    "contracts/profiles/developer-linux-workstation.profile.json",
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "generated/toolchain-catalog.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-K8S-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-SENT-001",
    "DEC-SHELL-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-DEV-LINUX-001",
    "REQ-PROFILE-DEV-LINUX-002",
    "REQ-PROFILE-DEV-LINUX-003",
    "REQ-PROFILE-DEV-LINUX-004",
    "REQ-PROFILE-DEV-LINUX-005",
    "REQ-PROFILE-DEV-LINUX-006",
    "REQ-PROFILE-DEV-LINUX-007",
    "REQ-PROFILE-DEV-LINUX-008",
    "REQ-PROFILE-DEV-LINUX-009",
    "REQ-PROFILE-DEV-LINUX-010",
    "REQ-PROFILE-DEV-LINUX-011",
    "REQ-PROFILE-DEV-LINUX-012",
    "REQ-PROFILE-DEV-LINUX-013",
    "REQ-PROFILE-DEV-LINUX-014",
    "REQ-PROFILE-DEV-LINUX-015",
    "REQ-PROFILE-DEV-LINUX-016",
    "REQ-PROFILE-DEV-LINUX-017",
    "REQ-PROFILE-DEV-LINUX-018",
    "REQ-PROFILE-DEV-LINUX-019",
    "REQ-PROFILE-DEV-LINUX-020",
    "REQ-PROFILE-DEV-LINUX-021",
    "REQ-PROFILE-DEV-LINUX-022",
    "REQ-PROFILE-DEV-LINUX-023",
    "REQ-PROFILE-DEV-LINUX-024",
    "REQ-PROFILE-DEV-LINUX-025",
    "REQ-PROFILE-DEV-LINUX-026",
    "REQ-PROFILE-DEV-LINUX-027",
    "REQ-PROFILE-DEV-LINUX-028",
    "REQ-PROFILE-DEV-LINUX-029",
    "REQ-PROFILE-DEV-LINUX-030",
    "REQ-PROFILE-DEV-LINUX-031",
    "REQ-PROFILE-DEV-LINUX-032",
    "REQ-PROFILE-DEV-LINUX-033",
    "REQ-PROFILE-DEV-LINUX-034",
    "REQ-PROFILE-DEV-LINUX-035",
    "REQ-PROFILE-DEV-LINUX-036"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
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
    "LOCK-PROFILE-002",
    "LOCK-SENT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003"
  ],
  "tags": [
    "deployment-profile",
    "developer-linux-workstation",
    "primary-profile",
    "native-linux",
    "workspace-isolation",
    "uv",
    "rootless-containers",
    "parallel-development",
    "resource-governance",
    "offline-development"
  ]
}
KOA:DOC-META:END -->

# Developer Linux Workstation

> **Document status:** Normative profile explanation.
> **Profile ID:** `developer_linux_workstation`
> **Profile kind:** `primary_profile`
> **Canonical profile contract:** `contracts/profiles/developer-linux-workstation.profile.json`
> **Authority rule:** The profile contract owns profile facts. This document explains how those facts apply.

## 1. Purpose

This document explains the `developer_linux_workstation` profile.

The profile provides a first-class native Linux environment for developing, running, testing, debugging, and validating multiple kOA applications, components, branches, and worktrees in parallel.

Its defining properties are:

- stable workspace identity;
- isolation of mutable dependencies and runtime state;
- UV-managed Python environments;
- workspace-scoped services, data, secrets, ports, and resources;
- rootless service execution where applicable;
- deterministic cleanup and recovery;
- local development continuity without a mandatory external AI or Internet dependency.

The profile is optimized for engineering work. It does not independently prove sovereign-node, build-farm, control-plane, production-release, or high-assurance conformance.

## 2. Scope

### 2.1 Included scope

This profile applies to:

- a native Linux workstation used interactively by one or more authorized developers;
- local source workspaces and Git worktrees;
- parallel development of multiple applications or branches;
- Python development through UV;
- rootless containers and workspace-scoped infrastructure services;
- local component execution, tests, diagnostics, packaging, and candidate artifact creation;
- optional isolated research and enrichment tasks;
- disconnected or intermittently connected development using admitted local inputs.

### 2.2 Excluded scope

This profile does not define:

- a production sovereign Linux node;
- a centralized build farm;
- a production control plane;
- an appliance shell;
- universal Linux distribution, desktop, container-runtime, or orchestration requirements;
- authority to activate a production Release Set;
- authority to treat local build success as release or conformance approval;
- a required native AI runtime;
- a requirement to run every kOA component simultaneously.

### 2.3 Profile classification

<!-- GENERATED:PROFILE-CLASSIFICATION:BEGIN
source=contracts/profiles/developer-linux-workstation.profile.json
renderer=profile-classification-v1
-->
| Property | Value |
| --- | --- |
| Profile ID | `developer_linux_workstation` |
| Kind | `primary_profile` |
| Independently deployable | Yes |
| Host family | Native Linux |
| Interaction model | Interactive developer workstation |
| Default network expectation | Internet optional; external retrieval is never architectural authority |
| Default container model | Rootless OCI-compatible services; rootless Podman preferred |
| Kubernetes | Not required |
| Compatible overlays | `high_assurance`, `sovereign_offline` when their contracts declare compatibility |
| Incompatible overlay | `appliance_shell` |
<!-- GENERATED:PROFILE-CLASSIFICATION:END -->

### 2.4 Hardware envelope

<!-- GENERATED:HARDWARE-ENVELOPE:BEGIN
source=contracts/profiles/developer-linux-workstation.profile.json#/hardware_envelope
renderer=hardware-envelope-v1
-->
| Resource | Minimum | Recommended |
| --- | ---: | ---: |
| CPU | 8 modern cores | 8 or more modern cores |
| Memory | 32 GiB | 64 GiB |
| Storage | 1 TB SSD | More capacity according to active workspaces and local media |
| GPU | Not required | Optional accelerator for explicitly selected workloads |
| Concurrent heavy workspaces | 2 by default | Higher only through a validated resource envelope |
<!-- GENERATED:HARDWARE-ENVELOPE:END -->

The hardware envelope is a profile claim and is not a universal kOA requirement.

## 3. Canonical References

### 3.1 Primary authority

`text
contracts/profiles/developer-linux-workstation.profile.json
`

### 3.2 Supporting authority

| Canonical reference | Owned information |
| --- | --- |
| `contracts/system.contract.json` | Global system baseline, operating modes, AI boundary, and degradation model |
| `generated/component-catalog.json` | Component identities, responsibilities, dependencies, and authoritative data ownership |
| `contracts/toolchains/python-uv.toolchain.json` | Python versioning, UV, `.venv`, lockfile, synchronization, cache, and dependency-update rules |
| `contracts/toolchains/container-runtime.toolchain.json` | Rootless container execution and runtime portability |
| `contracts/artifact-classes.contract.json` | Developer workspace, port allocation, receipts, packages, and artifact lifecycle |
| `contracts/release-channels.contract.json` | Release-channel identities and compatibility |
| `contracts/integration-types.contract.json` | Optional external integrations, including external AI surfaces |
| `generated/requirements-index.json` | Normative requirement statements |
| `generated/assertion-index.json` | Development isolation and cross-file invariants |
| `generated/traceability.json` | Decision, requirement, test, and evidence links |
| `generated/exception-index.json` | Approved profile-scoped deviations |

### 3.3 Terminology

The applicable canonical terms include:

- **developer Linux workstation**;
- **workspace**;
- **workspace identifier**;
- **worktree**;
- **mutable dependency environment**;
- **workspace virtual environment**;
- **UV**;
- **uv.lock**;
- **shared content-addressed UV cache**;
- **workspace port allocation**;
- **Resource Governor**;
- **SenTient**.

A worktree can host a workspace. It does not replace the complete workspace boundary.

## 4. Model and Responsibilities

### 4.1 Profile intent

The profile realizes the global kOA system as a developer-controlled native Linux workstation.

It favors rapid iteration without weakening isolation, data ownership, reproducibility, or explicit authority. A developer may start only the applications and services required for the current task.

### 4.2 Workspace model

Every active development unit has a stable `workspace_id`.

The identifier is derived from:

`text
component-or-application + branch-or-purpose + unique-suffix
`

Examples:

`text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
`

The identifier namespaces:

- installed dependency environments;
- container and process names;
- logical networks;
- host-port allocations;
- volumes and persistent data;
- database names, schemas, and service identities;
- Unix sockets and PID files;
- logs and temporary directories;
- development secrets and generated certificates;
- queues and asynchronous worker identities;
- resource budgets.

### 4.3 Python and UV model

<!-- GENERATED:PYTHON-UV-MODEL:BEGIN
source=contracts/toolchains/python-uv.toolchain.json
renderer=python-uv-profile-v1
-->
| Rule | Profile behavior |
| --- | --- |
| Dependency manager | UV |
| Project configuration | Versioned `pyproject.toml` |
| Dependency lock | Versioned `uv.lock` |
| Python version | Explicitly declared |
| Installed environment | One mutable `.venv` per workspace |
| Reproducible synchronization | `uv sync --frozen` |
| Global application installation | Prohibited |
| Shared mutable `.venv` | Prohibited |
| Shared UV cache | Permitted when content-addressed and non-authoritative |
| Lock refresh | Explicit operation |
| Dependency upgrade | Requires impact analysis and applicable tests |
<!-- GENERATED:PYTHON-UV-MODEL:END -->

UV owns Python dependency and environment management. It does not isolate services, databases, queues, ports, networks, secrets, or persistent application state.

### 4.4 Service and data isolation

Infrastructure services may run as rootless containers, local user services, or another explicitly adopted workspace-scoped mechanism.

Every workspace preserves:

- separate service identities;
- separate mutable data locations;
- separate database ownership or schemas;
- separate credentials;
- separate port allocations;
- separate temporary and cache state where mutation could collide;
- separate cleanup ownership.

A shared PostgreSQL, Redis, Solr, Elasticsearch, or queue process does not create shared logical ownership.

### 4.5 Component and capability envelope

Required profile capabilities include:

- workspace identity and lifecycle;
- source editing and local version-control operations;
- UV-managed Python development;
- local build and test execution;
- service and data isolation;
- port allocation;
- resource enforcement;
- diagnostics and cleanup;
- local artifact and evidence generation.

Conditional or optional capabilities include:

- individual kOA product components;
- component-specific databases and queues;
- containerized development services;
- local signing with authorized development keys;
- external AI assistance;
- SenTient;
- Solr, Elasticsearch, OpenRefine, and model runtimes;
- intensive kOA Mediatheque processing and UCKK package validation or transport;
- high-assurance or sovereign-offline overlays.

A capability being available does not make it permanently active.

### 4.6 Resource model

Resource Governor applies workspace-scoped:

- CPU limits;
- memory limits;
- process limits;
- I/O priorities;
- queue limits;
- worker limits;
- heavy-job concurrency.

The default envelope supports no more than two concurrent heavy workspaces. Lighter workspaces can coexist when their combined validated resource envelopes remain within the host profile.

### 4.7 Offline and AI envelope

Core development does not require native AI.

When source, lock data, toolchains, dependencies, and required services are already admitted locally, the profile supports:

- source editing;
- local builds;
- tests;
- documentation work;
- workspace provisioning from local inputs;
- deterministic component execution;
- diagnostics;
- export and backup of development state.

External AI surfaces are optional. Their results remain candidate inputs and never acquire release, policy, data-ownership, or conformance authority.

SenTient is optional, isolated, task-activated, resource-bounded, and non-authoritative.

### 4.8 Development outputs

Local outputs are classified according to their artifact contracts.

A locally built package, policy, language pack, runtime pack, image, receipt, or Release Set proposal remains a development candidate until the applicable admission, validation, signing, evidence, and release authority completes its workflow.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-PROFILE-DEV-LINUX-001,REQ-PROFILE-DEV-LINUX-002,REQ-PROFILE-DEV-LINUX-003,REQ-PROFILE-DEV-LINUX-004,REQ-PROFILE-DEV-LINUX-005,REQ-PROFILE-DEV-LINUX-006,REQ-PROFILE-DEV-LINUX-007,REQ-PROFILE-DEV-LINUX-008,REQ-PROFILE-DEV-LINUX-009,REQ-PROFILE-DEV-LINUX-010,REQ-PROFILE-DEV-LINUX-011,REQ-PROFILE-DEV-LINUX-012,REQ-PROFILE-DEV-LINUX-013,REQ-PROFILE-DEV-LINUX-014,REQ-PROFILE-DEV-LINUX-015,REQ-PROFILE-DEV-LINUX-016,REQ-PROFILE-DEV-LINUX-017,REQ-PROFILE-DEV-LINUX-018,REQ-PROFILE-DEV-LINUX-019,REQ-PROFILE-DEV-LINUX-020,REQ-PROFILE-DEV-LINUX-021,REQ-PROFILE-DEV-LINUX-022,REQ-PROFILE-DEV-LINUX-023,REQ-PROFILE-DEV-LINUX-024,REQ-PROFILE-DEV-LINUX-025,REQ-PROFILE-DEV-LINUX-026,REQ-PROFILE-DEV-LINUX-027,REQ-PROFILE-DEV-LINUX-028,REQ-PROFILE-DEV-LINUX-029,REQ-PROFILE-DEV-LINUX-030,REQ-PROFILE-DEV-LINUX-031,REQ-PROFILE-DEV-LINUX-032,REQ-PROFILE-DEV-LINUX-033,REQ-PROFILE-DEV-LINUX-034,REQ-PROFILE-DEV-LINUX-035,REQ-PROFILE-DEV-LINUX-036
renderer=requirements-list-v1
-->
- **REQ-PROFILE-DEV-LINUX-001 — SHALL:** The `developer_linux_workstation` profile be an independently deployable primary profile for native Linux development.
- **REQ-PROFILE-DEV-LINUX-002 — SHALL NOT:** Conformance to this profile be represented as conformance to `sovereign_linux_node`, `build_farm`, `control_plane`, or another primary profile.
- **REQ-PROFILE-DEV-LINUX-003 — SHALL:** The profile inherit the global system baseline and explicitly selected compatible overlays without implicit profile inheritance.
- **REQ-PROFILE-DEV-LINUX-004 — SHALL:** The canonical profile contract own the hardware, capability, component, offline, security, lifecycle, and conformance values explained by this document.
- **REQ-PROFILE-DEV-LINUX-005 — SHALL:** Every active development workspace have one stable `workspace_id`.
- **REQ-PROFILE-DEV-LINUX-006 — SHALL:** The `workspace_id` namespace mutable dependency environments, services, networks, ports, data, databases, secrets, temporary files, logs, sockets, queues, certificates, and process state.
- **REQ-PROFILE-DEV-LINUX-007 — SHALL:** Two applications, branches, purposes, or worktrees be runnable concurrently without mutable-state or dependency collisions.
- **REQ-PROFILE-DEV-LINUX-008 — SHALL NOT:** A Git worktree be treated as the complete workspace isolation boundary.
- **REQ-PROFILE-DEV-LINUX-009 — SHALL:** Workspace removal leave every other workspace's dependencies, services, ports, data, secrets, and active processes unchanged.
- **REQ-PROFILE-DEV-LINUX-010 — SHALL:** Each Python workspace use UV as its dependency and environment manager.
- **REQ-PROFILE-DEV-LINUX-011 — SHALL:** Each Python workspace declare `pyproject.toml`, `uv.lock`, and its Python version.
- **REQ-PROFILE-DEV-LINUX-012 — SHALL:** Each Python workspace have its own mutable `.venv`.
- **REQ-PROFILE-DEV-LINUX-013 — SHALL NOT:** Two workspaces share a mutable installed Python environment.
- **REQ-PROFILE-DEV-LINUX-014 — SHALL:** Reproducible Python validation use the committed lock state through `uv sync --frozen` or its canonically registered equivalent.
- **REQ-PROFILE-DEV-LINUX-015 — SHALL NOT:** Application dependencies be installed globally as a substitute for a workspace environment.
- **REQ-PROFILE-DEV-LINUX-016 — MAY:** Workspaces share a content-addressed UV download and build cache that does not represent an installed mutable environment.
- **REQ-PROFILE-DEV-LINUX-017 — SHALL:** Lockfile refresh and dependency upgrades be explicit operations with impact analysis and applicable test results.
- **REQ-PROFILE-DEV-LINUX-018 — SHALL:** Infrastructure services use workspace-scoped identities, data locations, credentials, endpoints, and cleanup behavior.
- **REQ-PROFILE-DEV-LINUX-019 — SHALL NOT:** UV be treated as isolation for databases, queues, search engines, container networks, host ports, secrets, or persistent service data.
- **REQ-PROFILE-DEV-LINUX-020 — SHALL:** Shared infrastructure preserve separate logical ownership, credentials, schemas or databases, namespaces, and prohibited cross-component writes.
- **REQ-PROFILE-DEV-LINUX-021 — SHALL:** Linux development prefer rootless Podman while allowing another explicitly adopted OCI-compatible runtime.
- **REQ-PROFILE-DEV-LINUX-022 — SHALL NOT:** Application or component contracts depend on runtime-specific container behavior unless the profile or applicable toolchain explicitly adopts that behavior.
- **REQ-PROFILE-DEV-LINUX-023 — SHALL NOT:** A single-workstation developer deployment require Kubernetes.
- **REQ-PROFILE-DEV-LINUX-024 — SHALL:** Each workspace have an enforceable CPU, memory, process, I/O, queue, worker, and heavy-job budget.
- **REQ-PROFILE-DEV-LINUX-025 — SHALL:** Resource pressure reduce concurrency, queue work, suspend task-activated services, or reject new heavy work before isolation or authoritative data integrity is weakened.
- **REQ-PROFILE-DEV-LINUX-026 — SHALL:** The default profile envelope permit no more than two concurrent heavy workspaces unless an explicitly validated resource envelope authorizes more.
- **REQ-PROFILE-DEV-LINUX-027 — SHALL:** SenTient, Solr, Elasticsearch, OpenRefine, model runtimes, and intensive kOA Mediatheque processing and UCKK package-validation or transport jobs be optional or task-activated rather than permanent profile dependencies.
- **REQ-PROFILE-DEV-LINUX-028 — SHALL:** SenTient remain isolated, non-authoritative, and unable to write directly to another component's authoritative store.
- **REQ-PROFILE-DEV-LINUX-029 — SHALL NOT:** The profile require native AI or an external AI surface for source editing, local builds, tests, workspace management, or deterministic component operation.
- **REQ-PROFILE-DEV-LINUX-030 — SHALL:** External AI outputs remain candidate inputs and pass normal review, validation, provenance, and import controls.
- **REQ-PROFILE-DEV-LINUX-031 — SHALL:** The profile support development without Internet access for admitted source, cached or vendored dependencies, local toolchains, local tests, and already provisioned services.
- **REQ-PROFILE-DEV-LINUX-032 — SHALL:** Unavailable network dependencies block only operations that require unresolved external inputs and preserve independently usable local workspaces.
- **REQ-PROFILE-DEV-LINUX-033 — SHALL:** Local build, test, package, or signing outputs remain development candidates until admitted through the applicable build, release, artifact, and authority workflow.
- **REQ-PROFILE-DEV-LINUX-034 — SHALL NOT:** The developer workstation activate production Release Sets or make production conformance claims solely from local success.
- **REQ-PROFILE-DEV-LINUX-035 — SHALL:** Workspace provisioning, validation, cleanup, failure, and recovery be observable and produce receipts when the affected transition is classified as critical.
- **REQ-PROFILE-DEV-LINUX-036 — SHALL:** Profile conformance test workspace isolation, parallel execution, cleanup independence, offline behavior, resource limits, data ownership, and the absence of undeclared authority.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Workspace provisioning

Workspace provisioning follows:

1. resolve the active profile and toolchain contracts;
2. select the repository, branch, worktree, or task purpose;
3. allocate a unique `workspace_id`;
4. allocate host ports and service endpoints;
5. create workspace-scoped secret, temporary, log, and data namespaces;
6. create or attach workspace-scoped service identities;
7. create the workspace `.venv`;
8. synchronize dependencies from the committed lock state;
9. apply the workspace resource envelope;
10. start only required services;
11. run readiness and isolation validation;
12. record provisioning evidence when required.

A failed allocation leaves no partially active workspace identity.

### 6.2 Starting services

Before a service starts:

1. resolve the component contract;
2. verify its workspace identity;
3. resolve required ports, networks, data paths, and credentials;
4. verify that no resource or ownership collision exists;
5. apply Resource Governor limits;
6. start the service under the workspace namespace;
7. run health and readiness checks.

Heavy services are task-activated or manually activated. They stop or release resources after their declared task or idle policy.

### 6.3 Dependency synchronization

Normal reproducible synchronization uses:

`bash
uv sync --frozen
`

A lock refresh is separate:

1. record the reason for the change;
2. update dependency declarations;
3. regenerate `uv.lock`;
4. review the dependency diff;
5. run applicable tests and security checks;
6. record impact and evidence;
7. commit the project and lock files together.

A lock refresh does not silently update another workspace.

### 6.4 Parallel workspace execution

Before two workspaces run concurrently, validation confirms that they do not share mutable:

- `.venv` directories;
- service names;
- host ports;
- databases or write schemas;
- service credentials;
- volumes;
- queues;
- Unix sockets;
- PID files;
- temporary directories;
- generated certificates;
- resource allocations.

A collision blocks the affected workspace start.

### 6.5 Workspace suspension and recovery

A workspace can transition through:

`text
defined
→ validated
→ allocated
→ active
→ suspended
→ restoring
→ active
→ retired
→ archived
`

Recovery revalidates identity, ports, dependencies, services, data ownership, resource limits, queued work, and prior failure state before mutation resumes.

### 6.6 Workspace removal

Removal follows:

1. stop workspace-owned processes and workers;
2. cancel or export workspace-owned queued work;
3. revoke workspace credentials and certificates;
4. release port and network allocations;
5. archive or delete mutable data according to the selected retention policy;
6. remove the workspace `.venv`;
7. remove temporary files, sockets, PID files, and logs according to policy;
8. verify that no other workspace resource changed;
9. record cleanup evidence when required.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Duplicate `workspace_id` | Block allocation | Existing workspace remains active |
| Port or service-name collision | Reallocate before start or block start | Other workspaces remain unchanged |
| Shared mutable `.venv` detected | Fail validation | Independent valid environments remain usable |
| Missing or stale `uv.lock` | Block frozen validation | Source inspection and unrelated work |
| Dependency source unavailable | Use already admitted cache or block affected synchronization | Existing synchronized workspaces |
| Container runtime unavailable | Block container-dependent services | Native tools and independent local work |
| Database or queue unavailable | Block or queue dependent capability | Unrelated components and source work |
| Resource threshold reached | Reduce concurrency, suspend heavy work, queue, or reject | Required low-cost workspaces |
| Resource Governor unavailable | Block unconstrained heavy work | Bounded low-risk local work allowed by contract |
| Internet unavailable | Disable unresolved retrieval and external integrations | Local admitted development envelope |
| External AI unavailable | Disable the requested AI-assisted capability | Deterministic local development |
| SenTient failure | Stop or isolate the task | Baseline workstation operation |
| Workspace data write failure | Block affected mutation; allow declared read-only inspection | Last durable state |
| Cleanup failure | Mark workspace `restoring` or `retired_with_residue`; block conflicting reuse | Other workspaces |
| Candidate artifact validation failure | Reject candidate | Previous admitted artifacts and source state |

Safe degradation never shares a mutable environment, bypasses ownership, removes resource limits, or redirects authority to another workspace.

## 8. Cross-Component Interactions

### 8.1 Component ownership

Each component retains authority over its own data and contract even when several components execute on one workstation.

Development convenience does not permit direct writes into another component's authoritative tables or files.

### 8.2 Shared infrastructure

A shared infrastructure process is permitted only when workspace and component boundaries remain explicit through:

- separate credentials;
- separate databases or schemas;
- separate namespaces;
- separate volumes or owned paths;
- separate queue identities;
- controlled network access;
- explicit cleanup ownership.

### 8.3 Resource and policy authorities

Resource Governor controls deterministic resource envelopes and scheduling.

Governance Policy Runtime controls governed authorization, disclosure, consent, and privilege only when the active capability requires it.

Neither authority substitutes for the other.

### 8.4 Privileged host operations

Ordinary workspace operation uses least privilege and rootless execution where practical.

A sensitive host mutation follows the applicable policy-before-privilege path. Developer convenience is not an authorization source.

### 8.5 External integrations

Optional external integrations remain capability-scoped and removable.

A workspace sends only explicitly selected and permitted data. Returned content is validated and imported through the owning component or repository workflow.

### 8.6 Build and release systems

The workstation can produce development candidates and evidence.

Build Farm, release authority, signing authority, artifact admission, and production activation remain separate responsibilities unless an accepted decision explicitly assigns a limited development capability.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- native Linux development is a first-class primary profile;
- every workspace has a stable identity;
- parallel applications, branches, and worktrees are supported;
- mutable dependencies and runtime state are isolated per workspace;
- UV is mandatory for Python workspace dependency management;
- every Python workspace has its own `.venv`;
- a content-addressed UV cache may be shared;
- rootless Podman is preferred but runtime-specific behavior is not globally authoritative;
- Kubernetes is not required for a developer workstation;
- heavy services are optional or task-activated;
- SenTient is optional and non-authoritative;
- external AI is optional and non-authoritative;
- the hardware minimum is 8 modern CPU cores, 32 GiB memory, and 1 TB SSD storage;
- two concurrent heavy workspaces are permitted by default;
- local build success does not grant release or production authority;
- this profile does not prove sovereign Linux conformance.

Prohibited assumptions include:

- treating a worktree as full isolation;
- sharing a mutable `.venv`;
- using globally installed application dependencies;
- reusing ports or service identities without allocation;
- treating a shared database process as shared data ownership;
- running every available component permanently;
- starting heavy services without a resource envelope;
- assuming Internet, an external AI provider, or SenTient is available;
- treating a recipe as profile authority;
- treating current host configuration as the canonical profile contract;
- applying appliance-shell or sovereign-node controls globally;
- treating the workstation as a build farm or production release authority;
- accepting undeclared fallback services after a dependency failure.

## 10. Validation Criteria

This document and the effective profile validate when:

1. the profile contract matches `deployment-profile.schema.json`;
2. the profile ID is unique and registered;
3. profile kind is `primary_profile`;
4. status is `active`;
5. all referenced decisions are accepted;
6. all requirements and locks resolve;
7. hardware minimums and the default heavy-workspace limit match the profile contract;
8. every active workspace has a unique `workspace_id`;
9. every Python workspace has a distinct `.venv`;
10. `pyproject.toml`, `uv.lock`, and the Python version are declared;
11. frozen synchronization reproduces the committed dependency state;
12. global application dependency installation is absent;
13. mutable services, ports, data, databases, secrets, queues, and process state are workspace-scoped;
14. two representative workspaces can run concurrently without collision;
15. removing one representative workspace does not affect the other;
16. shared infrastructure preserves logical ownership and prohibited direct writes;
17. Resource Governor limits heavy work;
18. Kubernetes is not required;
19. external AI and SenTient are not required for core development;
20. offline tests pass with admitted local inputs;
21. local outputs remain development candidates until admitted by release authority;
22. recovery passes through explicit validation;
23. no undeclared authority, profile inheritance, integration, or fallback is introduced;
24. no unresolved marker, placeholder, duplicate owner, or hash field appears.

Applicable checks include:

`bash
python docs/tools/check_profile_composition.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 Parallel branches

A developer runs:

`text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
`

Each workspace has its own `.venv`, ports, database identity, temporary paths, service names, and resource allocation. Stopping the feature workspace does not stop or mutate the main workspace.

### 11.2 Shared PostgreSQL process

Two workspaces use one local PostgreSQL server.

Each workspace has separate credentials and a separate database or owned schema. Neither workspace can write into the other's authoritative objects.

### 11.3 Offline dependency validation

The Internet is unavailable.

A workspace whose exact dependencies are already present in the admitted UV cache can run `uv sync --frozen` and execute local tests. A workspace requiring a new unresolved dependency is blocked from synchronization without affecting existing workspaces.

### 11.4 Optional SenTient task

A developer starts SenTient for a bounded enrichment experiment.

SenTient runs under an isolated resource envelope and returns candidate output. It does not write into source-component storage and stops after the task.

### 11.5 Candidate package

A local package passes workstation tests.

It remains a candidate. Production signing, Release Set compatibility, artifact admission, and activation are performed by their respective authorities.
