<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "development_toolchain",
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:build_farm"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/data_authority",
    "contracts/system.contract.json#/cross_component_communication",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/control-plane.profile.json",
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
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-DEV-CONT-001",
    "REQ-DEV-CONT-002",
    "REQ-DEV-CONT-003",
    "REQ-DEV-CONT-004",
    "REQ-DEV-CONT-005",
    "REQ-DEV-CONT-006",
    "REQ-DEV-CONT-007",
    "REQ-DEV-CONT-008",
    "REQ-DEV-CONT-009",
    "REQ-DEV-CONT-010",
    "REQ-DEV-CONT-011",
    "REQ-DEV-CONT-012",
    "REQ-DEV-CONT-013",
    "REQ-DEV-CONT-014",
    "REQ-DEV-CONT-015",
    "REQ-DEV-CONT-016",
    "REQ-DEV-CONT-017",
    "REQ-DEV-CONT-018",
    "REQ-DEV-CONT-019",
    "REQ-DEV-CONT-020",
    "REQ-DEV-CONT-021",
    "REQ-DEV-CONT-022",
    "REQ-DEV-CONT-023",
    "REQ-DEV-CONT-024",
    "REQ-DEV-CONT-025",
    "REQ-DEV-CONT-026",
    "REQ-DEV-CONT-027",
    "REQ-DEV-CONT-028",
    "REQ-DEV-CONT-029",
    "REQ-DEV-CONT-030",
    "REQ-DEV-CONT-031",
    "REQ-DEV-CONT-032"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-005",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005"
  ],
  "tags": [
    "development",
    "service-containers",
    "oci",
    "podman",
    "docker",
    "rootless",
    "workspace-isolation",
    "parallel-workspaces",
    "container-images",
    "kubernetes-boundary"
  ]
}
KOA:DOC-META:END -->

# Service Containers

## 1. Purpose

This document defines how development and build profiles use service containers without changing kOA component authority.

Service containers provide isolated execution and packaging for databases, queues, indexes, application services, workers, and supporting infrastructure that a workspace needs.

The container boundary is an implementation boundary.

It does not replace:

- the component registry;
- component contracts;
- data ownership;
- profile authority;
- release-channel ownership;
- artifact contracts;
- resource governance;
- security and privilege boundaries.

The development model uses containers to achieve reproducibility and workspace isolation while keeping application contracts portable across permitted runtimes.

The governing decisions are:

- Linux development prefers rootless Podman;
- Windows and WSL development permit Docker or Podman;
- sovereign Linux prefers rootless Podman and Quadlet;
- the build farm requires an OCI-compatible runtime;
- containers remain optional in the lightweight user profile;
- endpoint development does not depend on Kubernetes.

## 2. Scope

### 2.1 Included scope

This document applies to service containers used by:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`;
- development workflows that target a profile while running outside that target profile;
- local integration tests;
- component contract tests;
- database and migration tests;
- artifact builds;
- reproducible validation;
- parallel branch, worktree, and application execution.

Containerized service categories can include:

- PostgreSQL or another registered database;
- Redis or another cache;
- Solr, Elasticsearch, or another registered index;
- queues and brokers;
- object storage;
- local mail or notification test services;
- application APIs;
- web services;
- background workers;
- media workers;
- test fixtures;
- provenance and artifact services;
- other profile-authorized development infrastructure.

### 2.2 Excluded scope

This document does not define:

- the global container runtime;
- a universal orchestration platform;
- production sovereign-node Quadlet files;
- endpoint Kubernetes;
- component interfaces;
- product data schemas;
- database migration semantics;
- production release activation;
- a privileged container-management broker;
- exact commands for a particular runtime.

Commands and complete runtime manifests belong in non-normative recipes or profile-owned generated configuration.

### 2.3 Profile applicability

| Profile | Container rule |
| --- | --- |
| `developer_linux_workstation` | Rootless Podman is preferred |
| `developer_windows_wsl` | Docker or Podman is permitted |
| `build_farm` | An OCI-compatible runtime is required |
| `user_lightweight` | Containers are optional |
| `sovereign_linux_node` | Rootless Podman and Quadlet are preferred by that profile |
| `control_plane` | Kubernetes is permitted by the control-plane profile |
| `sovereign_hub` | Kubernetes is permitted only when measured scale justifies it |

These are conditional profile rules.

They do not become global application requirements.

### 2.4 Relationship to Kubernetes

Kubernetes is not required for:

- a developer laptop;
- a single developer workstation;
- one branch or worktree;
- a lightweight user installation;
- a sovereign Linux endpoint.

A build farm, control plane, or scaled sovereign hub can adopt Kubernetes through its active profile.

The application and component contracts remain usable without Kubernetes unless a profile-specific contract explicitly adopts a Kubernetes-only capability.

### 2.5 Relationship to production

A development container can approximate a production service boundary.

It is not automatically a production artifact or deployment specification.

Production use requires:

- an active target profile;
- a published artifact;
- provenance;
- release-channel placement;
- compatibility validation;
- profile-specific activation and recovery;
- production evidence.

## 3. Canonical References

### 3.1 Architecture and decisions

```text
generated/decision-index.json
contracts/system.contract.json#/global_boundaries
contracts/system.contract.json#/data_authority
contracts/system.contract.json#/cross_component_communication
```

Relevant accepted decisions include:

```text
DEC-CONTAINER-001
DEC-K8S-001
DEC-PROFILE-001
DEC-DATA-001
DEC-GOV-001
DEC-REL-001
```

### 3.2 Components and interfaces

```text
generated/component-catalog.json
generated/component-catalog.json
contracts/components/*.component.json
```

The component contract defines the service boundary.

A container image, compose file, Quadlet file, or Kubernetes object does not create another component definition.

### 3.3 Profiles

```text
generated/profile-catalog.json
contracts/profiles/developer-linux-workstation.profile.json
contracts/profiles/developer-windows-wsl.profile.json
contracts/profiles/build-farm.profile.json
contracts/profiles/sovereign-linux-node.profile.json
contracts/profiles/control-plane.profile.json
```

The profile owns runtime selection and runtime-specific adoption.

### 3.4 Development toolchains

```text
contracts/toolchains/python-uv.toolchain.json
```

UV owns Python dependency-environment behavior.

Containers isolate non-Python infrastructure and service state that UV does not isolate.

### 3.5 Artifacts, releases, and evidence

```text
contracts/artifact-classes.contract.json
contracts/release-channels.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
```

Published service images are artifacts rather than mutable development state.

## 4. Model and Responsibilities

### 4.1 Contract before container

The correct direction is:

```text
component responsibility
        ↓
component contract
        ↓
profile applicability
        ↓
artifact and image
        ↓
runtime-specific service definition
        ↓
workspace instance
```

The reverse direction is invalid.

A container discovered in a repository does not define a component, authority, dependency, or production requirement.

### 4.2 Workspace identity

Every active workspace has a stable `workspace_id`.

The identifier namespaces mutable development resources.

A conceptual naming form is:

```text
<workspace_id>-<component_or_service>-<resource>
```

The exact syntax belongs to the active development profile or workspace contract.

The namespace covers:

- containers;
- networks;
- volumes;
- database instances, names, or schemas;
- database users;
- queues;
- indexes;
- service identities;
- sockets;
- temporary directories;
- logs;
- PID files;
- credentials;
- certificates;
- allocated host ports.

### 4.3 Runtime selection

#### Linux development

Rootless Podman is preferred because it supports OCI images without requiring a privileged daemon for ordinary workspace services.

The preference does not make Podman behavior part of an application contract.

#### Windows and WSL development

Docker or Podman can be used according to the active profile.

A Linux-only runtime feature cannot be assumed unless the Windows/WSL profile adopts an equivalent or explicitly excludes the workflow.

#### Build farm

The build farm provides an OCI-compatible runtime.

The worker can use a runtime selected by the build-farm profile.

A job definition focuses on declared OCI inputs, outputs, isolation, resources, and evidence rather than developer-machine assumptions.

#### Sovereign Linux comparison

Rootless Podman and Quadlet are preferred for the sovereign Linux profile.

Quadlet is not a global development requirement.

Production Quadlet examples belong under sovereign Linux recipes and remain non-normative unless adopted by the profile contract.

### 4.4 Service identity

Each service instance has:

- a workspace identity;
- a component or infrastructure-service identity;
- a runtime instance identity;
- a network identity;
- a storage identity;
- an applicable database or queue identity;
- a declared credential scope.

Two workspaces cannot share one mutable service identity.

A shared immutable image cache does not create shared mutable runtime identity.

### 4.5 Image identity and build inputs

A reproducible service instance uses:

- an immutable published image identity; or
- a reproducible local image build tied to declared source and build inputs.

Declared build inputs include:

- source revision;
- build definition;
- base image identity;
- toolchain version;
- dependency lock state;
- build arguments that are not secrets;
- target architecture;
- generated inputs;
- expected artifact class.

An unqualified mutable tag is unsuitable as the only input to reproducible validation.

A convenient local alias can point to an immutable identity when the validation record preserves the resolved identity.

### 4.6 Rootless and least privilege

Ordinary development services run rootless where the selected runtime supports it.

The service receives only the access needed for its contract.

The default development container does not use:

- unrestricted host root;
- privileged mode;
- host PID namespace;
- host IPC namespace;
- host networking;
- broad device access;
- broad host-file-system mounts;
- foreign database credentials;
- production secrets.

A narrowly justified exception identifies the exact profile, workspace, service, operation, duration, compensating controls, and evidence.

### 4.7 Network model

Workspace networks are explicit and namespaced.

Common logical network classes can include:

| Network class | Use |
| --- | --- |
| Private service network | Component-to-component development traffic |
| Public test edge | Explicit host or browser access |
| Database network | Service-to-owned-database traffic |
| Build network | Dependency or artifact acquisition according to build policy |
| No-network task | Build or test that requires no network |

Network class names are illustrative.

The active profile or workspace contract owns actual networks and permitted connections.

Host networking is not the default because it weakens workspace isolation and port collision controls.

### 4.8 Port allocation

Container-internal ports can remain stable within a service contract.

Host ports are workspace allocations.

A host-port allocation records:

- workspace;
- service;
- protocol;
- container port;
- host bind address;
- allocated host port;
- lifetime;
- collision check;
- exposure class.

A service definition does not claim a global host port merely because an internal service port is conventional.

### 4.9 Volumes and persistent state

Persistent state is explicit.

Each volume identifies:

- workspace;
- owning component or infrastructure service;
- purpose;
- mutable or immutable classification;
- backup requirement;
- migration behavior;
- cleanup behavior;
- sharing policy.

A writable volume is not shared between workspaces.

Read-only immutable fixtures or caches can be shared only when the relevant contract preserves integrity and prevents mutable cross-workspace state.

### 4.10 Databases, queues, and indexes

Containerizing a database does not remove data-authority rules.

A database service can host several logical domains only when the active profile preserves:

- distinct component identities;
- distinct database or schema boundaries;
- least-privilege credentials;
- explicit migration ownership;
- no direct foreign writes;
- recoverable ownership mapping.

The same rules apply to:

- queues;
- indexes;
- caches;
- object stores;
- search services.

Development convenience does not create shared application authority.

### 4.11 Secrets

Secrets enter a service through the runtime and profile's approved secret mechanism.

Secrets remain outside:

- image layers;
- source-controlled manifests;
- ordinary environment examples;
- build arguments;
- general logs;
- generated catalogs.

A workspace secret is distinct from:

- another workspace secret;
- production secret material;
- a developer's unrelated credential;
- a shared mutable `.env` file.

Secret cleanup is part of workspace removal.

### 4.12 Health and readiness

Health answers whether the process or container is responsive.

Readiness answers whether the service can satisfy its critical contract.

Readiness can depend on:

- schema compatibility;
- required owned storage;
- required dependency interfaces;
- active profile;
- migrations;
- policy or trust dependencies;
- resource envelope;
- artifact compatibility.

A health check does not mutate authoritative state.

A passing health check does not prove readiness.

### 4.13 Restart and terminal failure

Each long-running service declares:

- startup timeout;
- readiness timeout;
- restart policy;
- retry limit or backoff;
- terminal failure condition;
- diagnostic retention;
- dependent-service behavior;
- cleanup behavior.

An endless restart loop is not a substitute for a terminal failure state.

A service that cannot satisfy its contract remains not ready.

### 4.14 Resource governance

Each workspace has a resource envelope.

Containerized services receive explicit limits or budgets for:

- CPU;
- memory;
- process count;
- I/O;
- storage;
- concurrency;
- worker count;
- heavy jobs.

Heavy optional services remain stopped until a task or development session needs them.

Examples include:

- SenTient;
- Solr;
- Elasticsearch;
- OpenRefine;
- model runtimes;
- intensive UCKK workers.

Resource pressure in one workspace should not make another workspace or the host unusable.

### 4.15 Cross-component communication

Containers communicate through the same registered mechanisms as non-containerized services:

- APIs;
- commands;
- events;
- signed artifacts;
- user-authorized transfers;
- governed gateways.

A shared network does not permit a direct foreign database write.

A container runtime's service discovery does not create a component dependency unless the component contracts declare it.

### 4.16 Migrations

Database and state migrations belong to the owning component.

A migration workflow identifies:

- workspace;
- component;
- source and target schema or state version;
- migration artifact or command;
- preconditions;
- backup or reset behavior;
- rollback or forward repair;
- evidence.

Starting a newer container image does not silently authorize an undeclared migration.

### 4.17 Published images

A development image becomes a published service artifact only through the artifact-publication workflow.

Publication records:

- source;
- immutable image identity;
- build inputs;
- provenance;
- tests;
- vulnerabilities or policy checks required by the target profile;
- target release channel;
- component-contract compatibility;
- supported profiles;
- rollback or replacement behavior.

A local image in a developer cache is not an active production artifact.

### 4.18 Kubernetes boundary

Kubernetes is one permitted implementation for profiles that select it.

It is not the abstraction layer for every component contract.

A Kubernetes manifest can realize:

- a service;
- identity;
- networking;
- volumes;
- secrets;
- health and readiness;
- resource limits;
- rollout behavior.

The same facts can be realized by another profile using rootless containers and a local service manager.

The component contract remains independent unless an accepted profile decision explicitly adopts Kubernetes-specific behavior.

### 4.19 Quadlet boundary

Quadlet can realize OCI service definitions under a systemd-managed sovereign Linux profile.

In this development document, Quadlet is:

- a relevant production comparison;
- a possible Linux-specific testing target;
- not the universal local-development manifest;
- not required under Windows or WSL;
- not application authority.

Complete Quadlet files belong in recipes or generated profile configuration.

### 4.20 Cleanup and retention

Workspace cleanup handles:

- containers;
- pods where used;
- networks;
- volumes;
- databases;
- queues;
- indexes;
- allocated ports;
- sockets;
- temporary directories;
- logs;
- credentials;
- certificates;
- task artifacts.

State marked for retention remains explicit and attributable to the workspace.

Deleting one workspace cannot remove another workspace's resources.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-CONT-001,REQ-DEV-CONT-002,REQ-DEV-CONT-003,REQ-DEV-CONT-004,REQ-DEV-CONT-005,REQ-DEV-CONT-006,REQ-DEV-CONT-007,REQ-DEV-CONT-008,REQ-DEV-CONT-009,REQ-DEV-CONT-010,REQ-DEV-CONT-011,REQ-DEV-CONT-012,REQ-DEV-CONT-013,REQ-DEV-CONT-014,REQ-DEV-CONT-015,REQ-DEV-CONT-016,REQ-DEV-CONT-017,REQ-DEV-CONT-018,REQ-DEV-CONT-019,REQ-DEV-CONT-020,REQ-DEV-CONT-021,REQ-DEV-CONT-022,REQ-DEV-CONT-023,REQ-DEV-CONT-024,REQ-DEV-CONT-025,REQ-DEV-CONT-026,REQ-DEV-CONT-027,REQ-DEV-CONT-028,REQ-DEV-CONT-029,REQ-DEV-CONT-030,REQ-DEV-CONT-031,REQ-DEV-CONT-032 -->
- **REQ-DEV-CONT-001 — SHALL:** Service containers preserve the component responsibilities, data authority, interfaces, and prohibited interactions defined by active component contracts.
- **REQ-DEV-CONT-002 — SHALL NOT:** An application contract depend on container-runtime-specific behavior unless the active profile explicitly adopts that behavior.
- **REQ-DEV-CONT-003 — SHALL:** Linux development prefer a rootless Podman runtime.
- **REQ-DEV-CONT-004 — SHALL:** Windows and WSL development permit Docker or Podman according to the active profile.
- **REQ-DEV-CONT-005 — SHALL:** A build-farm worker provide an OCI-compatible runtime.
- **REQ-DEV-CONT-006 — SHALL NOT:** A single-node user or developer installation require Kubernetes.
- **REQ-DEV-CONT-007 — SHALL:** Every active development workspace assign a stable `workspace_id` to all mutable container resources.
- **REQ-DEV-CONT-008 — SHALL:** Container names, network names, volume names, service names, database names or schemas, sockets, logs, temporary paths, credentials, and allocated host ports be namespaced by `workspace_id`.
- **REQ-DEV-CONT-009 — SHALL NOT:** Two workspaces share one mutable service volume, mutable database, mutable secret namespace, container identity, or installed dependency environment.
- **REQ-DEV-CONT-010 — SHALL:** Two applications, branches, or worktrees run concurrently without collisions in services, ports, processes, databases, users, schemas, networks, volumes, secrets, sockets, temporary files, or logs.
- **REQ-DEV-CONT-011 — SHALL:** A service-container definition reference an immutable image identity or a reproducible local build definition.
- **REQ-DEV-CONT-012 — SHALL NOT:** Reproducible validation depend on an unqualified mutable image tag.
- **REQ-DEV-CONT-013 — SHALL:** Container images be built from declared source, dependency, base-image, toolchain, and build inputs.
- **REQ-DEV-CONT-014 — SHALL:** Published service images carry provenance and belong to the applicable artifact class and release channel.
- **REQ-DEV-CONT-015 — SHALL:** Normal development service containers run without unrestricted host root privilege.
- **REQ-DEV-CONT-016 — SHALL NOT:** A development service container use privileged mode, host PID, host IPC, host network, unrestricted device access, or broad host mounts unless an active profile exception explicitly authorizes the exact need.
- **REQ-DEV-CONT-017 — SHALL:** Service containers use dedicated identities and least-privilege access to networks, volumes, databases, and secrets.
- **REQ-DEV-CONT-018 — SHALL NOT:** Secrets be embedded in container images, committed service definitions, image build arguments, or general logs.
- **REQ-DEV-CONT-019 — SHALL:** Persistent service state be stored in explicit workspace-scoped volumes or external stores with declared ownership and cleanup behavior.
- **REQ-DEV-CONT-020 — SHALL NOT:** A service container write directly to another component's authoritative source tables or equivalent mutable source state.
- **REQ-DEV-CONT-021 — SHALL:** Cross-component container traffic use registered component interfaces, commands, events, artifacts, or governed gateways.
- **REQ-DEV-CONT-022 — SHALL:** Containerized databases, queues, indexes, caches, and object stores use workspace-scoped identities, data namespaces, and migration state.
- **REQ-DEV-CONT-023 — SHALL:** Database migrations run through an explicit workspace and component-owned migration workflow.
- **REQ-DEV-CONT-024 — SHALL:** Host-port publication use the workspace port-allocation mechanism and avoid undeclared fixed global ports.
- **REQ-DEV-CONT-025 — SHALL:** Each long-running containerized service define health, readiness, restart, timeout, and terminal failure behavior.
- **REQ-DEV-CONT-026 — SHALL:** Health checks remain distinct from readiness checks and avoid mutating authoritative state.
- **REQ-DEV-CONT-027 — SHALL:** Each workspace apply explicit CPU, memory, process, I/O, storage, and heavy-job limits to its containerized services.
- **REQ-DEV-CONT-028 — SHALL:** Heavy optional services activate for a task or declared development session rather than remaining permanently active by default.
- **REQ-DEV-CONT-029 — SHALL:** Workspace startup, shutdown, reset, and deletion be idempotent and avoid modifying another workspace.
- **REQ-DEV-CONT-030 — SHALL:** Workspace cleanup remove or explicitly retain container, network, volume, port, temporary, log, and secret state according to the declared retention policy.
- **REQ-DEV-CONT-031 — SHALL:** Container-based validation record the exact workspace, profile, image identities, build inputs, service definitions, tests, and evidence used.
- **REQ-DEV-CONT-032 — SHALL:** A semantic change to container-runtime applicability, isolation, privilege, data ownership, networking, artifact identity, or Kubernetes use an accepted decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Create a containerized workspace service

1. Resolve the workspace identity.
2. resolve the active development profile.
3. identify the component or infrastructure-service purpose.
4. resolve the component contract where the service implements a component.
5. select the runtime permitted by the profile.
6. resolve an immutable image or reproducible build.
7. allocate container, network, volume, port, database, and credential namespaces.
8. apply rootless identity and least privilege.
9. apply the workspace resource envelope.
10. define health, readiness, restart, failure, and cleanup behavior.
11. validate that no foreign authoritative-state write path exists.
12. create the service instance.
13. record the resolved runtime inputs.

### 6.2 Start a workspace service set

1. Validate the workspace manifest or generated service definitions.
2. verify image identities and required local build outputs.
3. create workspace networks.
4. create or resolve workspace-scoped volumes.
5. create database, queue, cache, and index identities.
6. allocate host ports.
7. resolve secrets without writing them into image or source control.
8. start infrastructure dependencies.
9. run explicit migrations where required.
10. start application services.
11. evaluate health and readiness.
12. report a complete ready or blocked state.

### 6.3 Run parallel workspaces

1. Assign a different `workspace_id` to each branch or worktree.
2. generate distinct runtime resource names.
3. allocate non-colliding host ports.
4. create separate mutable volumes and database state.
5. create separate secret namespaces.
6. apply independent resource envelopes.
7. start both service sets.
8. run collision tests.
9. verify that stop, reset, and delete actions affect only their target workspace.

### 6.4 Build a service image

1. Resolve source revision and build definition.
2. resolve the declared base-image identity.
3. resolve toolchain and dependency lock state.
4. remove secrets from the build context and build arguments.
5. execute the reproducible build.
6. record the resulting immutable image identity.
7. run image and component-contract tests.
8. generate provenance.
9. retain the result as a local candidate or submit it to artifact publication.

### 6.5 Run an integration test

1. Resolve the exact workspace and profile.
2. resolve the service-image identities.
3. create isolated service and data state.
4. apply test fixtures through component-owned interfaces or migration workflows.
5. start the required service graph.
6. verify readiness.
7. execute tests.
8. capture evidence and diagnostics.
9. stop services.
10. retain or delete state according to the test policy.

### 6.6 Reset mutable service state

1. Identify the target workspace.
2. stop affected services.
3. preserve evidence or debugging state when required.
4. remove only the target workspace's mutable volumes and databases.
5. recreate clean state.
6. run component-owned migrations.
7. restart services.
8. verify readiness.
9. confirm that other workspaces were unchanged.

### 6.7 Publish a service image

1. Select a validated candidate image.
2. verify source and build provenance.
3. verify the component-contract version.
4. verify target-profile compatibility.
5. verify artifact-class and release-channel placement.
6. execute required security, compatibility, migration, and recovery tests.
7. create the published immutable artifact.
8. update release compatibility.
9. retain rollback or replacement information.
10. produce publication evidence.

### 6.8 Remove a workspace

1. Stop new task activation.
2. stop workspace services.
3. record required diagnostics and evidence.
4. revoke workspace-scoped credentials.
5. release allocated ports.
6. remove containers and networks.
7. remove or retain volumes according to policy.
8. remove temporary data, sockets, PID files, and logs according to policy.
9. remove workspace-specific dependency environments.
10. verify that no other workspace was modified.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Runtime is unavailable | Mark workspace service activation blocked | Source and non-containerized work | Containerized service set |
| Image identity cannot be resolved | Reject reproducible startup | Existing valid service state | Candidate service |
| Local image build fails | Preserve build diagnostics | Previous valid local image | New candidate image |
| Workspace name collision occurs | Reject creation | Existing workspace | Colliding workspace |
| Host port collision occurs | Allocate another permitted port or block | Existing service | Colliding bind |
| Mutable volume is shared across workspaces | Reject startup | Existing isolated data | Shared mutable service state |
| Secret namespace is missing | Reject dependent service | Unaffected services | Service requiring the secret |
| Privileged or host-wide access is undeclared | Reject service definition | Rootless services | Overprivileged container |
| Health passes but readiness fails | Keep service not ready | Diagnostics and unaffected services | Dependent workflow |
| Migration fails | Preserve pre-migration or resettable state | Previous compatible service state | New schema-dependent service |
| Foreign authoritative write is detected | Reject and report lock violation | Existing authoritative data | Prohibited mutation |
| Resource limits cannot be enforced | Block or stop resource-sensitive services | Lightweight host and workspace functions | Unbounded work |
| One optional heavy service fails | Disable that service | Core workspace services | Optional capability |
| Container cleanup fails | Isolate residual resources and report them | Other workspaces | Resource-name reuse |
| Kubernetes is unavailable on an endpoint | Continue with the profile-selected non-Kubernetes runtime | Endpoint development | Kubernetes-only local workflow |
| Build-farm OCI runtime is unavailable | Mark worker unavailable | Other workers | OCI job on affected worker |
| Required evidence cannot be retained | Mark validation blocked | Workspace diagnostics | Successful validation claim |

Failure does not authorize:

- a shared mutable fallback volume;
- a direct host installation that changes another workspace;
- a global fixed port;
- a direct cross-component database write;
- privileged mode;
- a mutable image tag as unrecorded replacement;
- Kubernetes as an emergency endpoint dependency.

## 8. Cross-Component Interactions

### 8.1 Component contracts

A containerized application service implements a component contract.

The contract remains authoritative for:

- interfaces;
- commands;
- events;
- data ownership;
- state;
- failures;
- compatibility.

The runtime definition implements those requirements for one profile and workspace.

### 8.2 Databases

The owning component controls its migrations and authoritative writes.

A database container supplies infrastructure.

It does not become the owner of every domain stored by the database process.

Database credentials remain component and workspace scoped.

### 8.3 Resource Governor

A development profile can use Resource Governor or an equivalent profile-owned mechanism to enforce workspace limits.

The resource mechanism controls budgets and scheduling.

It does not grant application or data authority.

### 8.4 Governance Policy Runtime

A profile that selects governed development operations can use Governance Policy Runtime for authorization, disclosure, privilege, or exception decisions.

The policy runtime does not operate the container runtime or allocate resources.

### 8.5 Identity and Trust

Identity and Trust can verify:

- published image identity;
- artifact signatures;
- service identities;
- provenance;
- release inputs.

Development runtimes still use workspace-scoped local identities.

### 8.6 Artifact publication

A local image enters lifecycle authority only through artifact publication.

The published artifact links the component contract, supported profiles, release channel, tests, provenance, and compatibility.

### 8.7 Parallel applications and branches

Two branches can run the same component simultaneously.

They remain distinguishable through workspace-scoped:

- service identities;
- host ports;
- networks;
- volumes;
- databases;
- credentials;
- logs;
- process names.

The component identity remains the same canonical component identity, while runtime instances remain separate development instances.

### 8.8 Production sovereign Linux

A development workflow can test the service image intended for `sovereign_linux_node`.

The production profile can use rootless Podman and Quadlet.

The development workspace does not gain production privilege, production secrets, or production data because it targets that profile.

### 8.9 Build farm

A build-farm worker receives declared source and build inputs.

It produces an OCI artifact and provenance.

The build worker does not activate the artifact into a production profile automatically.

### 8.10 Control plane

The control-plane profile can use Kubernetes.

A Kubernetes-based integration test remains profile-scoped.

It does not make Kubernetes mandatory for local component development or endpoint operation.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-CONTAINER-001` | Linux development prefers rootless Podman; Windows/WSL permits Docker or Podman; sovereign Linux prefers Podman and Quadlet; build farm requires OCI compatibility |
| `DEC-K8S-001` | Kubernetes is not an endpoint requirement and is limited to profiles that explicitly select it |
| `DEC-PROFILE-001` | Runtime adoption remains profile-specific |
| `DEC-DATA-001` | Containers do not alter data ownership or permit foreign source writes |
| `DEC-GOV-001` | Resource and policy authorities remain separate from the container runtime |
| `DEC-REL-001` | Published service artifacts participate in explicit release channels and compatible Release Sets |

### 9.2 Protected locks

| Lock | Protected relationship |
| --- | --- |
| `LOCK-PROFILE-001` | A profile-specific runtime choice does not become global |
| `LOCK-DEV-001` | Each workspace has an isolated mutable dependency environment |
| `LOCK-DEV-002` | Each Python workspace has its own UV-managed virtual environment |
| `LOCK-DEV-003` | Mutable service state is namespaced by workspace |
| `LOCK-DEV-004` | Parallel branches avoid service, port, database, volume, secret, and process collisions |
| `LOCK-DEV-005` | Shared caches do not become shared installed environments |
| `LOCK-DATA-001` | No direct foreign authoritative-source write |
| `LOCK-GOV-001` | Container runtime does not merge resource and policy authority |
| `LOCK-LIFE-001` | Published artifacts do not activate partially |
| `LOCK-LIFE-003` | Release Sets bind compatible channel versions |
| `LOCK-IMPL-001` | Recipes and observed runtime behavior do not define architecture |
| `LOCK-IMPL-002` | Podman, Quadlet, systemd, Wayland, and related Linux choices remain profile-scoped |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- every kOA service runs in a container;
- one container equals one canonical component;
- a compose service creates a component dependency;
- Linux development requires Docker;
- Windows/WSL development requires Podman;
- Quadlet is required for every developer;
- Kubernetes is required for local development;
- Kubernetes is required because production can use it;
- a running container is ready;
- a container image tag proves reproducibility;
- a local image is a published release artifact;
- root inside a container is equivalent to an acceptable least-privilege design;
- privileged mode is harmless in development;
- host networking is the default;
- broad host mounts are acceptable for convenience;
- a shared volume is safe because workspaces use different branches;
- a shared database user preserves component ownership;
- one `.env` file is an acceptable global secret store;
- an internal container port reserves the same host port globally;
- starting a newer image silently authorizes migration;
- a shared runtime cache can hold mutable installed state;
- a test container can write directly to another component's source tables;
- production credentials are acceptable development fixtures;
- a runtime-specific manifest overrides the component contract;
- a unvalidated Quadlet example is production-ready;
- a recipe creates a profile rule;
- current developer-machine behavior defines architecture.

Missing runtime authority, workspace identity, image identity, isolation, privilege scope, migration ownership, or evidence blocks the affected workflow.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-DEV-006`;
2. the path is `05-development/06-service-containers.md`;
3. the active language is English;
4. the scope is limited to the declared development toolchain and profiles;
5. all accepted decisions resolve;
6. all listed locks resolve;
7. Linux development prefers rootless Podman;
8. Windows/WSL permits Docker or Podman;
9. build-farm workers expose an OCI-compatible runtime;
10. endpoint development has no Kubernetes dependency;
11. component contracts remain runtime independent unless a profile explicitly adopts runtime behavior;
12. every workspace has a stable identity;
13. all mutable service resources are workspace scoped;
14. two parallel workspaces run without collisions;
15. no mutable service volume or database is shared across workspaces;
16. image identities or local build inputs are reproducible;
17. unqualified mutable tags are absent from reproducible validation inputs;
18. images exclude embedded secrets;
19. normal services run rootless or under an explicitly justified equivalent isolation;
20. privileged, host-wide, and device access is rejected unless an active exception applies;
21. network access is explicit;
22. host ports are allocated by workspace;
23. persistent state has ownership and cleanup rules;
24. database and state migrations are component owned;
25. foreign authoritative-source writes are rejected;
26. health and readiness are distinct;
27. resource limits are enforced;
28. optional heavy services are task-activated;
29. workspace lifecycle operations are idempotent;
30. workspace deletion does not affect another workspace;
31. published images have provenance, artifact class, release channel, tests, and compatibility;
32. container-based validation records exact runtime inputs;
33. semantic changes include an accepted decision and impact report;
34. all linked requirements, tests, and evidence resolve;
35. no unresolved state exists;
36. complete documentation validation passes.

Expected test coverage includes:

```text
TEST-DEV-CONT-001  Profile-specific runtime selection
TEST-DEV-CONT-002  Runtime-independent component contract
TEST-DEV-CONT-003  Rootless Linux development runtime
TEST-DEV-CONT-004  Windows/WSL Docker or Podman compatibility
TEST-DEV-CONT-005  Build-farm OCI runtime
TEST-DEV-CONT-006  No endpoint Kubernetes dependency
TEST-DEV-CONT-007  Workspace resource-name isolation
TEST-DEV-CONT-008  Parallel workspace collision freedom
TEST-DEV-CONT-009  Immutable image or reproducible build identity
TEST-DEV-CONT-010  Secret exclusion from images and manifests
TEST-DEV-CONT-011  Least-privilege container configuration
TEST-DEV-CONT-012  Workspace network and port isolation
TEST-DEV-CONT-013  Volume and database isolation
TEST-DEV-CONT-014  Component-owned migration workflow
TEST-DEV-CONT-015  Foreign authoritative-write rejection
TEST-DEV-CONT-016  Health and readiness distinction
TEST-DEV-CONT-017  Workspace resource limits
TEST-DEV-CONT-018  Idempotent workspace lifecycle
TEST-DEV-CONT-019  Artifact provenance and release placement
TEST-DEV-CONT-020  Exact validation-input evidence
```

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate possible implementations. They do not redefine profile contracts, component contracts, or runtime authority.

### 11.1 Linux developer workspace

A Linux developer creates workspace `alpha`.

The workspace uses rootless Podman.

Its services use names such as:

```text
alpha-orgo-api
alpha-postgres
alpha-private-network
alpha-orgo-data
```

Host ports are allocated for `alpha` rather than hardcoded globally.

### 11.2 Parallel branch

A second worktree uses workspace `beta`.

It builds the same component revision family but uses:

```text
beta-orgo-api
beta-postgres
beta-private-network
beta-orgo-data
```

Both workspaces run concurrently with different host ports, databases, volumes, credentials, logs, and processes.

### 11.3 Windows/WSL workspace

A Windows/WSL profile selects Docker.

The component contract remains unchanged.

The workspace uses the same declared OCI images and component interfaces while the profile adapts paths, networking, and runtime integration.

### 11.4 Local database

Konnaxion and Orgo use separate database identities and workspace-scoped data.

They can share one database engine process when the profile preserves logical boundaries.

Orgo does not update Konnaxion tables directly.

### 11.5 Task-activated search service

A workspace needs Elasticsearch for one integration test.

The service starts for the test session under a bounded resource envelope.

It stops after evidence and diagnostics are retained.

The workspace does not keep it permanently active.

### 11.6 Sovereign Linux target

A developer builds and tests an OCI image locally.

The target sovereign Linux profile later uses a profile-adopted Quadlet definition.

The local development manifest and production Quadlet file are different implementation projections of the same component contract.

### 11.7 Build farm

A clean build worker receives a source revision, build definition, base-image identity, dependency lock state, and target architecture.

It produces a service image and provenance.

The image remains a candidate until artifact publication and Release Set compatibility complete.

### 11.8 Invalid shared workspace

Two branches use the same database volume, database user, host port, secret file, and container name.

Stopping one branch damages the other.

The arrangement violates workspace isolation and cannot support reproducible parallel development.

### 11.9 Invalid endpoint Kubernetes dependency

A local service can run as one OCI container but its developer instructions require a Kubernetes cluster and reject every other permitted runtime.

The arrangement is invalid unless an accepted profile-specific decision makes that behavior necessary for the exact workflow.

### 11.10 Invalid privileged shortcut

A development container runs privileged with the host root file system mounted so that it can rewrite another component's data directory.

The arrangement is invalid even when used only for debugging.
