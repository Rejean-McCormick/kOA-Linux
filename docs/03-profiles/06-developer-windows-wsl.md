<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "developer_windows_wsl"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-SENT-001",
    "DEC-AI-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-WSL-001",
    "REQ-PROFILE-WSL-002",
    "REQ-PROFILE-WSL-003",
    "REQ-PROFILE-WSL-004",
    "REQ-PROFILE-WSL-005",
    "REQ-PROFILE-WSL-006",
    "REQ-PROFILE-WSL-007",
    "REQ-PROFILE-WSL-008",
    "REQ-PROFILE-WSL-009",
    "REQ-PROFILE-WSL-010",
    "REQ-PROFILE-WSL-011",
    "REQ-PROFILE-WSL-012",
    "REQ-PROFILE-WSL-013",
    "REQ-PROFILE-WSL-014",
    "REQ-PROFILE-WSL-015",
    "REQ-PROFILE-WSL-016",
    "REQ-PROFILE-WSL-017",
    "REQ-PROFILE-WSL-018",
    "REQ-PROFILE-WSL-019",
    "REQ-PROFILE-WSL-020",
    "REQ-PROFILE-WSL-021",
    "REQ-PROFILE-WSL-022",
    "REQ-PROFILE-WSL-023",
    "REQ-PROFILE-WSL-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DATA-001",
    "LOCK-SENT-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-010",
    "DOC-SYS-018",
    "DOC-PROFILE-005",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003"
  ],
  "tags": [
    "profile",
    "developer",
    "windows",
    "wsl",
    "wsl2",
    "workspace-isolation",
    "uv",
    "containers",
    "parallel-workspaces",
    "non-sovereign"
  ]
}
KOA:DOC-META:END -->

# Developer Windows WSL Profile

## 1. Purpose

The `developer_windows_wsl` profile defines a reproducible kOA development environment for contributors whose host operating system is Windows and whose Linux development workloads run inside WSL 2.

The profile provides a convenience-oriented development path. It supports local editing, building, testing, databases, service containers, parallel branches, optional research workbenches, and controlled use of external integrations.

It does not convert Windows into a sovereign Linux node. It does not establish production-node, high-assurance, sovereign-offline, or appliance-shell conformance. Release authority remains determined by release, build-farm, artifact, test, and evidence contracts.

## 2. Scope

This profile applies to:

- a supported Windows host;
- one or more WSL 2 Linux distributions used for kOA development;
- source repositories stored and executed in the WSL Linux filesystem;
- isolated application and branch workspaces;
- Linux-native developer tools installed inside WSL;
- Docker or Podman configurations that expose services to WSL workspaces;
- local databases, queues, web services, workers, and test dependencies;
- Windows editors or terminals connected to the WSL environment;
- optional SenTient operation under explicit isolation;
- explicit user-initiated external integrations.

This profile does not cover:

- production deployment on Windows;
- sovereign Linux conformance;
- immutable signed operating-system images;
- appliance-shell behavior;
- guaranteed sovereign-offline operation;
- Kubernetes-based endpoint architecture;
- release-authoritative build execution unless a release contract explicitly accepts the evidence;
- direct Windows execution of Linux service contracts.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/profiles/developer-windows-wsl.profile.json` | Profile membership, capabilities, implementation constraints, resources, and conformance claims |
| `generated/profile-catalog.json#/primary_profiles` | Registration as a primary profile |
| `generated/profile-catalog.json#/profile_overlays` | Overlay compatibility and incompatibility |
| `contracts/system.contract.json#/profile_model` | One-primary-profile composition and explicit inheritance |
| `contracts/system.contract.json#/global_boundaries` | Component, data, privilege, and implementation boundaries |
| `contracts/system.contract.json#/implementation_policy` | Desktop, container-runtime, and Kubernetes scoping |
| `contracts/system.contract.json#/hardware_envelope_classes/1` | Developer-workstation hardware envelope |
| `contracts/toolchains/python-uv.toolchain.json` | Python, UV, lockfile, environment, and reproducibility rules |
| `contracts/toolchains/container-runtime.toolchain.json` | Docker and Podman development-service behavior |
| `generated/component-catalog.json` | Component responsibility and authoritative data ownership |
| `contracts/integration-types.contract.json` | External integration activation, transfer, authority, failure, and removal rules |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Profile, workspace, data, AI, and implementation invariants |
| `generated/traceability.json` | Links among profile claims, decisions, requirements, tests, and evidence |
| `generated/test-catalog.json` | Registered profile and development tests |
| `generated/evidence-catalog.json` | Valid profile and workspace evidence |

## 4. Model and Responsibilities

### 4.1 Host and Linux boundary

Windows is the host operating system. WSL 2 supplies the Linux execution boundary for kOA development.

The profile treats these as distinct responsibility domains:

| Domain | Responsibility |
| --- | --- |
| Windows host | User login, hardware access, host security, WSL lifecycle, optional editor user interface, host networking, and host resource allocation |
| WSL distribution | Linux source tree, development tools, dependency environments, service processes, databases, sockets, Linux permissions, and workspace runtime state |
| Workspace | One component-and-branch or purpose-specific mutable development environment |
| Container runtime | Optional isolated service execution under a declared Docker or Podman configuration |
| Build farm | Release-authorized reproducible builds and release evidence when required |

The active repository and mutable Linux runtime state remain in the WSL Linux filesystem. Windows-mounted paths may be used for explicit import, export, or user-selected interchange, but they are not the canonical location for an active mutable workspace.

### 4.2 Profile identity and composition

`developer_windows_wsl` is one primary profile.

It has no default overlays. The profile does not compose with:

- `high_assurance`;
- `sovereign_offline`;
- `appliance_shell`.

A developer may use security controls or offline techniques that resemble stronger profiles, but those practices do not create the corresponding profile claim without an accepted profile contract.

### 4.3 Workspace identity

Each workspace uses a stable identifier derived from:

```text
component + branch_or_purpose + unique_suffix
```

Examples:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
```

The identifier prefixes or namespaces:

- containers;
- networks;
- volumes;
- database names;
- database users;
- sockets;
- temporary directories;
- log directories;
- process-identifier files;
- service names;
- secret names;
- allocated host ports.

Two branches of one application remain operational at the same time without sharing mutable state.

### 4.4 Python and dependency isolation

Python development uses UV.

Every Python workspace contains:

```text
pyproject.toml
uv.lock
.venv/
```

The Python version is declared. Installed dependencies remain inside the workspace `.venv`. Reproducible validation uses:

```bash
uv sync --frozen
```

A content-addressed UV download cache may be shared. A mutable `.venv` may not be shared.

Global installation of application dependencies is outside the profile contract.

### 4.5 Services and containers

Development services may run:

- directly inside WSL;
- in Docker with WSL integration;
- in Podman inside or integrated with WSL.

The selected runtime is recorded by the workspace. Application contracts remain OCI- and runtime-neutral unless a separate accepted decision authorizes a narrower dependency.

Fixed service ports are acceptable inside an isolated workspace network. Host-facing ports are allocated from a workspace-scoped registry.

Kubernetes is outside this profile's conformance model.

### 4.6 Data ownership

A development host may consolidate multiple component databases into one database process. Logical ownership remains separate.

Each component uses:

- a separate database or schema;
- a separate database identity;
- component-owned migrations;
- declared APIs, commands, events, gateways, artifacts, or read models for cross-component access.

Physical consolidation does not permit cross-component authoritative writes.

### 4.7 Filesystem and interoperability controls

Profile validation covers differences that commonly cross the Windows and Linux boundary:

- line endings;
- case sensitivity;
- executable bits;
- symbolic links;
- file permissions;
- path separators;
- path length;
- filename validity;
- socket and process behavior;
- host-to-WSL port exposure;
- clock and timestamp behavior relevant to builds;
- environment-variable and secret injection.

The repository configuration and tests determine accepted behavior. Windows-host convenience does not override Linux contract semantics.

### 4.8 Resource model

The profile uses the `developer_workstation` envelope:

| Resource | Canonical baseline |
| --- | --- |
| CPU | 8 modern cores minimum |
| Memory | 32 GiB minimum; 64 GiB recommended |
| Storage | 1 TB SSD minimum |
| GPU | Optional |
| Heavy workspaces | Default maximum of 2 concurrently |

The capacity is evaluated across Windows, WSL, container services, databases, editors, and active workspaces. Host hardware totals alone do not prove available WSL capacity.

### 4.9 Optional workbenches and integrations

SenTient is permitted as an optional isolated workbench. It remains stopped until explicitly activated and has separate dependencies, storage, service identity, temporary data, network access, CPU, and memory limits.

ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain optional external surfaces. Their operations remain explicit, capability-scoped, disclosed, removable, and non-authoritative.

No external surface controls builds, tests, databases, services, privilege, or release activation automatically.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-WSL-001,REQ-PROFILE-WSL-002,REQ-PROFILE-WSL-003,REQ-PROFILE-WSL-004,REQ-PROFILE-WSL-005,REQ-PROFILE-WSL-006,REQ-PROFILE-WSL-007,REQ-PROFILE-WSL-008,REQ-PROFILE-WSL-009,REQ-PROFILE-WSL-010,REQ-PROFILE-WSL-011,REQ-PROFILE-WSL-012,REQ-PROFILE-WSL-013,REQ-PROFILE-WSL-014,REQ-PROFILE-WSL-015,REQ-PROFILE-WSL-016,REQ-PROFILE-WSL-017,REQ-PROFILE-WSL-018,REQ-PROFILE-WSL-019,REQ-PROFILE-WSL-020,REQ-PROFILE-WSL-021,REQ-PROFILE-WSL-022,REQ-PROFILE-WSL-023,REQ-PROFILE-WSL-024 -->
- **REQ-PROFILE-WSL-001 — SHALL:** The developer Windows WSL profile shall use WSL 2 as the Linux execution environment for kOA development workloads.
- **REQ-PROFILE-WSL-002 — SHALL:** The active source tree, mutable dependency environments, Linux service data, sockets, and temporary runtime data shall reside in the WSL Linux filesystem.
- **REQ-PROFILE-WSL-003 — SHALL NOT:** The profile shall not present the Windows host, WSL kernel, or WSL integration layer as sovereign Linux, high-assurance, appliance, or production-node conformance.
- **REQ-PROFILE-WSL-004 — SHALL:** Each development workspace shall have one stable workspace identifier derived from component, branch or purpose, and a unique suffix.
- **REQ-PROFILE-WSL-005 — SHALL:** Each workspace shall have isolated mutable dependencies, services, networks, host ports, volumes, secrets, temporary data, database identities, logs, process identifiers, and resource budgets.
- **REQ-PROFILE-WSL-006 — SHALL:** Two applications or two branches of the same application shall be runnable concurrently without namespace, port, database, volume, secret, or dependency collisions.
- **REQ-PROFILE-WSL-007 — SHALL:** Every Python workspace shall declare its Python version and contain `pyproject.toml`, `uv.lock`, and its own `.venv`.
- **REQ-PROFILE-WSL-008 — SHALL:** UV shall be the Python dependency manager, and reproducible validation shall use `uv sync --frozen`.
- **REQ-PROFILE-WSL-009 — SHALL NOT:** Two workspaces shall not share a mutable `.venv`, globally installed application dependencies, or an undeclared mutable service environment.
- **REQ-PROFILE-WSL-010 — SHALL:** A content-addressed download cache may be shared only when installed dependency environments remain workspace-local and immutable validation inputs remain locked.
- **REQ-PROFILE-WSL-011 — SHALL:** Containerized services shall use Docker or Podman through a declared WSL-compatible configuration, while application contracts remain independent of runtime-specific behavior.
- **REQ-PROFILE-WSL-012 — SHALL NOT:** Kubernetes shall not be required or used as a conformance dependency for the developer Windows WSL profile.
- **REQ-PROFILE-WSL-013 — SHALL:** Host-facing ports shall be allocated through a workspace-scoped registry, while fixed service ports may be used only inside isolated workspace networks.
- **REQ-PROFILE-WSL-014 — SHALL:** Every component shall retain separate logical data ownership and database credentials, even when development services share one database process.
- **REQ-PROFILE-WSL-015 — SHALL NOT:** A component shall not write directly to another component's authoritative source tables.
- **REQ-PROFILE-WSL-016 — SHALL:** Windows and WSL path, line-ending, case-sensitivity, executable-bit, and file-permission differences shall be detected by profile validation before merge or release evidence is accepted.
- **REQ-PROFILE-WSL-017 — SHALL:** The profile shall use the developer-workstation hardware envelope and shall bound concurrent heavy workspaces according to measured capacity.
- **REQ-PROFILE-WSL-018 — SHALL:** SenTient may run only as an explicitly activated, isolated, resource-bounded, non-authoritative workbench.
- **REQ-PROFILE-WSL-019 — SHALL:** External AI surfaces shall remain explicitly user-initiated, capability-scoped, transparent about transferred data, non-authoritative, and removable without breaking local development.
- **REQ-PROFILE-WSL-020 — SHALL:** Loss of Windows-to-WSL integration, container integration, network access, or an external service shall fail only affected capabilities and shall preserve valid workspace source and data.
- **REQ-PROFILE-WSL-021 — SHALL:** Workspace cleanup shall remove workspace-scoped services, networks, ports, volumes, temporary data, logs, and secrets without deleting shared immutable caches or another workspace's state.
- **REQ-PROFILE-WSL-022 — SHALL:** Development evidence produced by this profile shall identify the Windows host, WSL distribution, WSL kernel, active workspace identifier, dependency locks, container runtime, and relevant tool versions.
- **REQ-PROFILE-WSL-023 — SHALL:** Release-authoritative builds shall be reproduced or independently validated in an approved Linux build-farm or other release-authorized environment when the release contract requires it.
- **REQ-PROFILE-WSL-024 — SHALL:** Every active profile claim shall be traceable to accepted decisions, active requirements, locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a WSL development environment

1. Install or select a WSL 2 Linux distribution.
2. Record the Windows version, WSL version, distribution, Linux kernel, architecture, and available resources.
3. Create the repository location in the WSL Linux filesystem.
4. Install declared developer toolchains inside WSL.
5. Configure Docker or Podman only when the workspace needs service containers.
6. Configure host integration without granting undeclared repository, secret, or service access.
7. Run profile preflight checks.
8. Record the environment identity used by development evidence.

### 6.2 Creating a workspace

1. Select the component and branch or purpose.
2. Generate a unique `workspace_id`.
3. Create a workspace-local source checkout or worktree.
4. Allocate host ports.
5. Create workspace network, volume, temporary-data, log, and secret namespaces.
6. Create component-specific database names and identities.
7. Create the workspace dependency environment.
8. Apply the workspace resource budget.
9. Start only required services.
10. Validate isolation before development begins.

### 6.3 Synchronizing a Python workspace

1. Confirm the declared Python version.
2. Confirm the presence of `pyproject.toml` and `uv.lock`.
3. Create or select the workspace-local `.venv`.
4. Run `uv sync --frozen`.
5. Reject undeclared lockfile changes during reproducible validation.
6. Record UV, Python, and lockfile identity in test evidence.

### 6.4 Running parallel branches

1. Resolve each workspace identifier.
2. Verify distinct mutable dependency environments.
3. Verify distinct host-port allocations.
4. Verify distinct service, network, volume, secret, temporary-data, and log namespaces.
5. Verify distinct database names and identities.
6. Start the workspaces independently.
7. Execute collision and cross-write tests.
8. Stop or clean either workspace without affecting the other.

### 6.5 Running tests

1. Resolve the active workspace and profile evidence context.
2. Synchronize locked dependencies.
3. Start required isolated services.
4. Apply test fixtures only within the workspace.
5. Run contract, integration, development-profile, and cross-platform tests.
6. Record host, WSL, workspace, runtime, dependency, and tool identities.
7. Stop test-only services.
8. Preserve or register required evidence.
9. Mark release authority separately from development success.

### 6.6 Cleaning a workspace

1. Stop workspace processes and containers.
2. Remove workspace service registrations.
3. Release host ports.
4. Remove workspace networks.
5. Remove disposable volumes and temporary data.
6. Remove workspace secrets.
7. Remove workspace database identities and data only when cleanup policy permits.
8. Remove logs according to evidence and retention rules.
9. Preserve shared immutable caches.
10. Verify that other workspaces remain operational.

### 6.7 Host, WSL, or integration recovery

1. Stop new mutations when the Linux execution environment becomes unstable.
2. Preserve source control state and component-owned data.
3. Record the affected workspace and failure boundary.
4. Restart only the failed host, WSL, runtime, or workspace layer.
5. Revalidate ports, mounts, permissions, databases, services, and dependency locks.
6. Resume only after workspace isolation checks pass.
7. Reproduce release-relevant evidence in an approved environment when validity is uncertain.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved state | Blocked or reduced behavior |
| --- | --- | --- | --- |
| WSL distribution unavailable | Stop Linux development operations and preserve repository and workspace data | Windows host and stored data | Linux builds, tests, and services |
| Windows editor integration unavailable | Use a WSL terminal or Linux-side editor path | WSL workspace and services | Windows-integrated editing only |
| Container runtime unavailable | Run non-containerized supported services or block only container-dependent tasks | Source, dependencies, and direct WSL tools | Container-dependent services |
| Host port collision | Reject startup and allocate a different workspace port | Existing workspaces | Conflicting service exposure |
| Workspace network collision | Reject or recreate the affected workspace network | Other workspace networks | Affected service startup |
| Dependency lock mismatch | Block reproducible validation | Existing locked environment and source | Unlocked validation claim |
| Shared mutable environment detected | Block both affected workspace claims until separated | Source repositories | Isolation and reproducibility claim |
| Database identity collision | Block service startup or migration | Existing component data | Colliding database operation |
| Windows-mounted active workspace detected | Block the profile claim or migrate the workspace into the Linux filesystem | Source content | WSL profile conformance |
| Permission or executable-bit drift | Block affected build or test | Source history and unrelated files | Invalid executable or packaging result |
| Network unavailable | Continue cached local development where dependencies and services are present | Local source and services | Remote fetches and external integrations |
| External AI unavailable | Disable only the external assistance capability | Local development | External request |
| SenTient unavailable | Disable only the optional workbench | Ordinary development | SenTient task |
| Resource pressure | Reduce concurrent heavy workspaces and stop optional services | Source, databases, and core tools | Additional heavy tasks |
| WSL or host restart changes network state | Revalidate exposed ports and service endpoints | Workspace identities and data | Unverified network access |
| Evidence context incomplete | Block the affected profile, release, or reproducibility claim | Development results as non-authoritative information | Unsupported claim |

Failure does not authorize sharing mutable state, bypassing locks, or treating Windows-host behavior as canonical Linux behavior.

## 8. Cross-Component Interactions

| Producer | Consumer | Contract | Profile boundary |
| --- | --- | --- | --- |
| Windows host | WSL distribution | WSL lifecycle, resources, filesystem integration, and networking | Host control does not become application authority |
| WSL workspace manager | Workspace services | Workspace identity, namespaces, ports, secrets, data, and limits | One workspace cannot mutate another workspace's state |
| UV cache | Python workspace | Content-addressed downloaded packages | Shared cache does not become a shared `.venv` |
| Python workspace | Test runner | Locked dependency environment and declared Python version | Test runner does not modify the lock during frozen validation |
| Container runtime | Workspace | Isolated services and networks | Runtime administration does not grant component-data authority |
| Port allocator | Workspace | Workspace-scoped host-port assignment | Ports are not hardcoded across parallel workspaces |
| Database process | Components | Separate databases or schemas and separate identities | Shared process does not transfer logical ownership |
| Component | Another component | API, command, event, gateway, artifact, or declared read model | Direct source-table writes remain prohibited |
| SenTient | Owning component | Candidate artifact and provenance | Workbench output remains non-authoritative |
| External integration | User or owning component | Controlled export and candidate import | Provider output cannot mutate development or release authority directly |
| Developer WSL profile | Build farm | Source revision, locks, tests, and candidate evidence | Release authority remains with approved release workflows |
| Evidence producer | Evidence registry | Test-evidence record | Evidence describes the environment; it does not redefine the profile |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-PROFILE-001` | `developer_windows_wsl` is a primary profile with explicit composition. |
| `DEC-DEV-001` | Workspaces have isolated mutable environments and Python uses UV with locked per-workspace environments. |
| `DEC-DEV-002` | Parallel applications and branches use stable workspace identifiers and isolated namespaces. |
| `DEC-DATA-001` | Logical component ownership remains mandatory under physically shared development infrastructure. |
| `DEC-CONTAINER-001` | Docker or Podman selection is profile-scoped and application contracts remain runtime-neutral. |
| `DEC-K8S-001` | Kubernetes is not an endpoint or WSL development-profile requirement. |
| `DEC-SENT-001` | SenTient is optional, isolated, task-activated, and non-authoritative. |
| `DEC-AI-001` | External AI is optional, explicit, and non-authoritative; native AI is absent from the baseline. |
| `DEC-HW-001` | The developer-workstation envelope defines the profile's baseline capacity class. |

### Prohibited assumptions

- WSL is equivalent to a sovereign Linux installation.
- A Windows administrator is an application-governance authority.
- A Windows path is interchangeable with a Linux workspace path.
- WSL 1 satisfies this profile.
- Every Windows-mounted repository satisfies Linux permission and filesystem semantics.
- Docker Desktop is mandatory.
- Podman is mandatory.
- systemd is a global requirement.
- Kubernetes is required or profile-authoritative.
- One `.venv` may be shared across branches.
- A shared database process permits shared component tables or credentials.
- A host port may be hardcoded for every workspace.
- A shared download cache is a shared mutable environment.
- Successful local tests automatically produce release authority.
- Windows-host or WSL-specific success proves native Linux behavior.
- SenTient is always running.
- External AI may automate builds, tests, migrations, or release activation.
- Loss of a remote integration invalidates local development.
- A recipe or current developer preference changes the profile contract.
- Missing evidence may be replaced by developer confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-PROFILE-006`, status `active`, language `en`, profile layer, and `developer_windows_wsl` scope.
2. All eleven required sections exist in numerical order.
3. The profile is registered as one active primary profile.
4. Overlay compatibility matches `generated/profile-catalog.json`.
5. `TEST-PROFILE-WSL-001` verifies WSL 2 and rejects WSL 1 for the profile claim.
6. `TEST-PROFILE-WSL-002` verifies that active workspaces and mutable Linux runtime state reside in the WSL Linux filesystem.
7. `TEST-PROFILE-WSL-003` verifies unique and stable workspace identifiers.
8. `TEST-PROFILE-WSL-004` starts two branches concurrently and verifies dependency, service, network, port, volume, secret, temporary-data, log, process, and database isolation.
9. `TEST-PROFILE-WSL-005` verifies `pyproject.toml`, `uv.lock`, declared Python, workspace `.venv`, and `uv sync --frozen`.
10. `TEST-PROFILE-WSL-006` rejects shared mutable `.venv` and globally installed application dependencies.
11. `TEST-PROFILE-WSL-007` verifies Docker and Podman profile compatibility without runtime-specific application contracts.
12. `TEST-PROFILE-WSL-008` verifies workspace-scoped host-port allocation and fixed internal network ports.
13. `TEST-PROFILE-WSL-009` verifies component database identity separation and rejects direct cross-component source-table writes.
14. `TEST-PROFILE-WSL-010` verifies line endings, case sensitivity, executable bits, symbolic links, permissions, paths, and host-to-WSL interoperability.
15. `TEST-PROFILE-WSL-011` verifies the developer-workstation envelope and bounded heavy-workspace concurrency.
16. `TEST-PROFILE-WSL-012` verifies SenTient isolation, task activation, resource limits, and candidate-output handling.
17. `TEST-PROFILE-WSL-013` verifies explicit external-integration activation, disclosed transfer, candidate output, and removal behavior.
18. `TEST-PROFILE-WSL-014` verifies cleanup without cross-workspace deletion.
19. `TEST-PROFILE-WSL-015` verifies safe degradation under WSL, container, network, integration, and resource failures.
20. `TEST-PROFILE-WSL-016` verifies that evidence records Windows, WSL, workspace, dependency, container, and tool identities.
21. `TEST-PROFILE-WSL-017` verifies that profile evidence does not claim sovereign Linux, high-assurance, sovereign-offline, appliance-shell, or production-node conformance.
22. `TEST-PROFILE-WSL-018` verifies release-authoritative reproduction or independent validation when required by the release contract.
23. Every decision ID is accepted, every requirement ID is unique, and every lock ID resolves.
24. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
25. The generated requirement projection matches `generated/requirements-index.json`.
26. Every active profile claim resolves to registered tests and valid evidence.

These criteria define required validation. They do not claim that a particular Windows host or workspace already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A developer stores `konnaxion-main-a31f` under the WSL home directory. UV creates a workspace-local `.venv`. PostgreSQL runs once, but Konnaxion and Orgo have separate databases and identities. Docker exposes the Konnaxion service through a port allocated specifically to that workspace.

> **Non-normative example:** The same developer creates `konnaxion-feature-voting-92cd`. It receives a different host port, network, database, secret namespace, temporary directory, log directory, and `.venv`. Stopping or deleting the feature workspace does not affect the main workspace.

> **Non-normative example:** Docker Desktop integration is unavailable. A workspace that can run its dependencies directly in WSL continues. A container-dependent workspace reports only its service capability as unavailable.

> **Non-normative example:** A developer uses a Windows editor connected to WSL. The editor interface runs on Windows, while source, commands, dependencies, tests, databases, and services remain in WSL.

> **Non-normative example:** Local tests pass in WSL. The release contract requires reproducible Linux build-farm evidence, so the same locked source is built and tested by a clean build worker before release activation.

> **Non-normative example:** A developer explicitly asks ChatGPT to review a selected error message. The selected text is disclosed and transferred. The response remains advice and cannot change source, tests, services, or release state without local developer action.
