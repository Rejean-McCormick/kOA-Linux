<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-001",
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
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "generated/toolchain-catalog.json",
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
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-SENT-001",
    "DEC-AI-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-SHELL-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-PRIV-001",
    "DEC-REL-001",
    "DEC-LIFE-001",
    "DEC-SEC-001",
    "DEC-OFFLINE-001",
    "DEC-INTEGRATION-001",
    "DEC-IMAGE-001",
    "DEC-OS-001",
    "DEC-LANG-001"
  ],
  "requirement_ids": [
    "REQ-DEV-BOUND-001",
    "REQ-DEV-BOUND-002",
    "REQ-DEV-BOUND-003",
    "REQ-DEV-BOUND-004",
    "REQ-DEV-BOUND-005",
    "REQ-DEV-BOUND-006",
    "REQ-DEV-BOUND-007",
    "REQ-DEV-BOUND-008",
    "REQ-DEV-BOUND-009",
    "REQ-DEV-BOUND-010",
    "REQ-DEV-BOUND-011",
    "REQ-DEV-BOUND-012",
    "REQ-DEV-BOUND-013",
    "REQ-DEV-BOUND-014",
    "REQ-DEV-BOUND-015",
    "REQ-DEV-BOUND-016",
    "REQ-DEV-BOUND-017",
    "REQ-DEV-BOUND-018",
    "REQ-DEV-BOUND-019",
    "REQ-DEV-BOUND-020",
    "REQ-DEV-BOUND-021",
    "REQ-DEV-BOUND-022",
    "REQ-DEV-BOUND-023",
    "REQ-DEV-BOUND-024",
    "REQ-DEV-BOUND-025",
    "REQ-DEV-BOUND-026",
    "REQ-DEV-BOUND-027",
    "REQ-DEV-BOUND-028"
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
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-REL-001",
    "LOCK-REL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-DEV-000",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003",
    "DOC-PROFILE-004",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-PROFILE-007",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-CONST-000",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "development",
    "profile-boundaries",
    "developer-workstation",
    "windows-wsl",
    "build-farm",
    "workspace-isolation",
    "uv",
    "sentient",
    "toolchains",
    "artifacts",
    "release-transition",
    "production-separation"
  ]
}
KOA:DOC-META:END -->

# Development Profile Boundaries

## 1. Purpose

This document defines the boundary between kOA development environments and active user, sovereign, hub, control, and other operational environments.

Development environments are intentionally mutable. They contain source trees, compilers, editors, test harnesses, workbenches, temporary services, local databases, generated files, candidate artifacts, and diagnostic tooling. Those capabilities are necessary for development but cannot become implicit product dependencies or operational authority.

The boundary model ensures that:

- each development workspace is isolated;
- parallel branches and applications can run safely;
- development tools remain non-authoritative;
- test data remains separated from operational data;
- credentials and privilege remain bounded;
- Build Farm remains distinct from interactive development;
- Windows and WSL boundaries are explicit;
- product releases are built from declared inputs;
- only validated artifacts cross into release and deployment.

Canonical profile identities and requirements remain owned by the profile contracts and registries. This document explains their shared development boundary.

## 2. Scope

This document applies globally to:

- Developer Linux Workstation;
- Developer Windows WSL;
- Build Farm;
- local source workspaces;
- parallel branches and worktrees;
- local services and databases;
- development containers;
- virtual environments;
- compiler and language workbenches;
- SenTient;
- test harnesses;
- local integration adapters;
- candidate artifact production;
- development-to-release transfer.

It also constrains interactions between development profiles and:

- `user_lightweight`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `control_plane`;
- profile overlays;
- release channels;
- artifact repositories;
- operational data and credentials.

This document does not define detailed workspace naming, UV commands, port-allocation algorithms, database recipes, or CI implementation. Those details are owned by the remaining documents in `05-development/` and by canonical toolchain contracts.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/profiles/developer-linux-workstation.profile.json` | Linux developer host, tools, components, resources, isolation, and conformance |
| `contracts/profiles/developer-windows-wsl.profile.json` | Windows host and WSL development boundaries |
| `contracts/profiles/build-farm.profile.json` | Non-interactive build execution, artifact production, isolation, and evidence |
| `contracts/profiles/user-lightweight.profile.json` | User-profile exclusions and runtime-only expectations |
| `contracts/profiles/sovereign-linux-node.profile.json` | Immutable production boundary and prohibited development state |
| `generated/profile-catalog.json` | Profile classification, composition, overlays, and compatibility |
| `generated/toolchain-catalog.json` | Active toolchains and workspace realization |
| `contracts/artifact-classes.contract.json` | Candidate and release artifact classes, validation, and activation |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge release identities |
| `contracts/integration-types.contract.json` | Developer and external integration scope |
| `generated/component-catalog.json` | Component identities, ownership, and profile membership |
| `generated/requirements-index.json` | Normative development requirements |
| `generated/assertion-index.json` | Development, profile, data, security, lifecycle, and release alignment |
| `generated/traceability.json` | Decision, profile, toolchain, requirement, test, artifact, and evidence relationships |
| `generated/exception-index.json` | Bounded development exceptions |
| `generated/test-catalog.json` | Isolation, build, artifact, transition, and profile tests |
| `generated/evidence-catalog.json` | Build, test, publication, and conformance evidence |

The detailed development corpus is:

`text
05-development/00-development-model.md
05-development/02-workspace-identity.md
05-development/03-workspace-isolation.md
05-development/04-dependency-isolation.md
05-development/05-python-uv.md
05-development/06-service-containers.md
05-development/07-ports-networks-and-sockets.md
05-development/08-volumes-and-persistent-data.md
05-development/09-secrets-and-local-identities.md
05-development/10-parallel-applications-and-branches.md
05-development/11-local-databases-and-migrations.md
05-development/12-development-resource-governance.md
05-development/13-development-security.md
05-development/14-build-test-and-validation.md
05-development/15-artifact-publication.md
05-development/16-development-to-release-transition.md
`

## 4. Development Profile Model

### 4.1 Developer Linux Workstation

Developer Linux Workstation is the primary full Linux development profile.

It can include:

- source workspaces;
- editors and IDEs;
- UV-managed Python environments;
- compilers;
- GF Wordbench;
- local component services;
- isolated databases and queues;
- development containers;
- test harnesses;
- candidate artifact creation;
- SenTient as an optional isolated workbench;
- local integration testing.

It is not a sovereign production node.

Its mutable host and workspace state cannot be promoted directly into a system image or operational component store.

### 4.2 Developer Windows WSL

Developer Windows WSL provides a Linux development environment inside WSL while retaining an explicit Windows host boundary.

The profile distinguishes:

- Windows host identity and security;
- WSL distribution identity;
- Linux workspace identity;
- Linux filesystem and Windows-mounted filesystem;
- Windows and Linux credentials;
- host and WSL networking;
- Windows process interop;
- clipboard and file transfer;
- development containers and virtual environments.

The preferred active workspace resides in the Linux filesystem for predictable semantics and performance.

Windows interop is an explicit capability, not an invisible shortcut around workspace isolation.

### 4.3 Build Farm

Build Farm is a non-interactive production-of-artifacts profile.

It can include:

- clean build workers;
- declared toolchains;
- compiler and packaging environments;
- test execution;
- candidate signing requests;
- artifact publication;
- provenance and evidence production;
- bounded caches;
- SenTient or GF Wordbench only when the build contract explicitly requires them.

Build workers do not host ordinary user or sovereign operational state.

Build Farm produces candidate artifacts. Release authority remains governed by release contracts, approvals, validation, and publication.

### 4.4 Non-development profiles

The following profiles are not development environments:

- User Lightweight;
- Sovereign Linux Node;
- Sovereign Hub;
- Control Plane when used only for operations;
- composed high-assurance, sovereign-offline, or appliance-shell deployments.

These profiles consume validated artifacts.

They do not require:

- source trees;
- editable installs;
- compilers;
- GF Wordbench;
- SenTient;
- development databases;
- local IDE state;
- mutable developer containers;
- workspace secrets;
- unregistered test services.

### 4.5 Workspace identity

A workspace identity distinguishes one source and runtime realization from every other workspace.

It includes:

- repository identity;
- branch, worktree, or source revision;
- workspace identifier;
- active development profile;
- toolchain identity;
- virtual environment;
- service namespace;
- port and socket namespace;
- storage and volume namespace;
- local database and migration identity;
- local credentials;
- integration configuration;
- generated-output roots.

Deleting one workspace does not alter another workspace or an operational deployment.

### 4.6 Authority boundary

Development work can propose:

- source changes;
- documentation changes;
- registry changes;
- migrations;
- artifacts;
- tests;
- evidence;
- decisions.

It cannot activate those changes merely by producing them.

Canonical ownership, accepted decisions, review, validation, artifact publication, and authority activation remain separate steps.

### 4.7 Tool classes

| Tool class | Permitted role | Authority |
| --- | --- | --- |
| Editor or IDE | Modify workspace source | No independent product authority |
| UV | Resolve and realize workspace Python dependencies | No shared runtime authority |
| Compiler | Produce candidate output | Output requires artifact validation |
| GF Wordbench | Author and compile language sources | Development and build only |
| SenTient | Optional isolated analytical workbench | Non-authoritative |
| Test harness | Evaluate declared behavior | Test result authority only through registered evidence |
| Container runtime | Isolate declared services and builds | Profile-scoped implementation |
| Database tool | Operate workspace or authorized test stores | No production ownership |
| AI assistant | Produce candidate suggestions | Human review and validation required |
| Build worker | Produce candidate artifacts and evidence | No release activation authority |
| Publication client | Submit validated candidates | Publication contract controls acceptance |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-BOUND-001,REQ-DEV-BOUND-002,REQ-DEV-BOUND-003,REQ-DEV-BOUND-004,REQ-DEV-BOUND-005,REQ-DEV-BOUND-006,REQ-DEV-BOUND-007,REQ-DEV-BOUND-008,REQ-DEV-BOUND-009,REQ-DEV-BOUND-010,REQ-DEV-BOUND-011,REQ-DEV-BOUND-012,REQ-DEV-BOUND-013,REQ-DEV-BOUND-014,REQ-DEV-BOUND-015,REQ-DEV-BOUND-016,REQ-DEV-BOUND-017,REQ-DEV-BOUND-018,REQ-DEV-BOUND-019,REQ-DEV-BOUND-020,REQ-DEV-BOUND-021,REQ-DEV-BOUND-022,REQ-DEV-BOUND-023,REQ-DEV-BOUND-024,REQ-DEV-BOUND-025,REQ-DEV-BOUND-026,REQ-DEV-BOUND-027,REQ-DEV-BOUND-028 -->
- **REQ-DEV-BOUND-001 — SHALL:** Every development environment declare exactly one active development profile and every selected overlay in its workspace or deployment identity.
- **REQ-DEV-BOUND-002 — SHALL NOT:** A development profile claim user, sovereign-node, sovereign-hub, high-assurance, control-plane, or operational-production conformance merely because it can execute equivalent binaries or services.
- **REQ-DEV-BOUND-003 — SHALL:** Developer Linux Workstation, Developer Windows WSL, and Build Farm remain distinct profiles with separate host, privilege, storage, networking, toolchain, evidence, and lifecycle envelopes.
- **REQ-DEV-BOUND-004 — SHALL:** Every development workspace have a stable workspace identity, isolated mutable state, declared source revision, declared profile, declared toolchain, and declared local resource namespace.
- **REQ-DEV-BOUND-005 — SHALL NOT:** Parallel workspaces share a mutable Python environment, component database, migration state, service volume, queue, socket, port allocation, secret store, runtime identity, or generated authoritative output.
- **REQ-DEV-BOUND-006 — SHALL:** Python workspaces use `pyproject.toml`, `uv.lock`, one workspace-local `.venv`, and `uv sync --frozen` for validated dependency realization.
- **REQ-DEV-BOUND-007 — SHALL NOT:** A shared download cache, package cache, container layer cache, compiler cache, or artifact cache become a shared mutable installed environment or authoritative workspace state.
- **REQ-DEV-BOUND-008 — SHALL:** Development services, databases, queues, volumes, ports, networks, sockets, and local identities be namespaced by workspace identity or otherwise proven collision-free.
- **REQ-DEV-BOUND-009 — SHALL:** Development components write only to workspace-owned or explicitly provisioned test state and never to production, sovereign, user, shared staging, or another workspace's authoritative state.
- **REQ-DEV-BOUND-010 — SHALL:** Real production or governed user data be excluded from ordinary development use unless an explicit authorized test-data procedure defines scope, minimization, isolation, retention, and destruction.
- **REQ-DEV-BOUND-011 — SHALL:** Development identities, credentials, signing keys, trust roots, policy authorities, publication destinations, and integration accounts remain separate from production authorities.
- **REQ-DEV-BOUND-012 — SHALL NOT:** A developer workstation hold unrestricted production signing authority, production root credentials, production recovery secrets, or a general privileged path into an operational deployment.
- **REQ-DEV-BOUND-013 — SHALL:** SenTient remain an optional isolated non-authoritative workbench limited to Developer Linux Workstation, Developer Windows WSL, and Build Farm where their active contracts permit it.
- **REQ-DEV-BOUND-014 — SHALL NOT:** SenTient, GF Wordbench, a compiler, a notebook, an IDE, a test harness, an AI tool, or another development workbench directly mutate canonical registries, active product authority, operational component stores, or published release state.
- **REQ-DEV-BOUND-015 — SHALL:** External AI and developer assistance output remain candidate material requiring human review, deterministic validation, provenance, and canonical owner acceptance before entering authoritative source or documentation.
- **REQ-DEV-BOUND-016 — SHALL:** Containers, virtual machines, WSL, service managers, desktop shells, and orchestration tools remain profile-scoped implementation mechanisms and not global application requirements.
- **REQ-DEV-BOUND-017 — SHALL NOT:** Kubernetes be required for a developer endpoint, user endpoint, or sovereign single-node profile solely because it is used by Build Farm or Control Plane.
- **REQ-DEV-BOUND-018 — SHALL:** Developer Windows WSL treat the Windows host, WSL distribution, Linux workspace, filesystem placement, networking, credentials, and interop as explicit trust and performance boundaries.
- **REQ-DEV-BOUND-019 — SHALL NOT:** Windows-host paths, Windows credentials, host process invocation, clipboard transfer, or automatic interop silently bypass Linux workspace isolation or product security controls.
- **REQ-DEV-BOUND-020 — SHALL:** Build Farm consume declared source and toolchain inputs, produce immutable candidate artifacts and evidence, and avoid interactive authoritative product operation.
- **REQ-DEV-BOUND-021 — SHALL:** The transition from development to release occur only through registered artifact classes, required tests, provenance, release-channel compatibility, approval, and publication contracts.
- **REQ-DEV-BOUND-022 — SHALL NOT:** A mutable workspace, local virtual environment, editable install, running development container, database volume, unregistered binary, or local service image be copied directly into an active product deployment.
- **REQ-DEV-BOUND-023 — SHALL:** Generated artifacts be reproducible or otherwise fully attributable to source revision, toolchain version, declared inputs, build profile, test results, and producing identity.
- **REQ-DEV-BOUND-024 — SHALL:** Development migrations execute only against isolated development or ephemeral test stores unless a separately authorized release or operations contract governs a staged target.
- **REQ-DEV-BOUND-025 — SHALL:** Development failures remain workspace-scoped and preserve other workspaces, shared read-only caches, source history, registered evidence, and operational deployments.
- **REQ-DEV-BOUND-026 — SHALL:** Every development profile define its offline envelope, external integration dependencies, resource limits, cleanup behavior, backup needs, and reproducibility expectations.
- **REQ-DEV-BOUND-027 — SHALL:** A development profile conformance claim identify the host, workspace, source revision, toolchain, active services, local identities, test data, external integrations, and generated evidence.
- **REQ-DEV-BOUND-028 — SHALL:** Development-profile conformance pass only when boundary, isolation, dependency, data, secret, privilege, WSL where applicable, build, artifact, release-transition, cleanup, and evidence tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Workspace and Environment Procedure

### 6.1 Create a workspace

A development workspace is created through this sequence:

1. assign a stable workspace identifier;
2. record the repository and source revision;
3. select the applicable development profile;
4. resolve the active toolchain;
5. create workspace-local mutable roots;
6. create the workspace-local Python virtual environment;
7. allocate service, network, port, socket, volume, and database namespaces;
8. provision development-only identities and secrets;
9. realize dependencies from locked inputs;
10. validate isolation before services start.

A directory copy without a distinct workspace identity is not sufficient for parallel execution.

### 6.2 Realize Python dependencies

The Python workspace contains:

`text
pyproject.toml
uv.lock
.venv/
`

Dependency realization uses:

`bash
uv sync --frozen
`

A shared download cache is permitted.

A shared installed environment, shared mutable site-packages tree, or one virtual environment reused across workspaces is not permitted.

### 6.3 Start development services

Service startup resolves:

- workspace identity;
- component identity;
- service version;
- local service identity;
- port or socket allocation;
- network namespace;
- database and migration state;
- volume ownership;
- test-data scope;
- integration credentials;
- resource limits.

Service discovery uses declared workspace endpoints rather than global assumptions.

### 6.4 Use test data

Development data is one of:

- generated synthetic data;
- fixtures;
- anonymized and minimized data authorized for development;
- ephemeral integration-test data;
- explicitly approved governed test data.

The data classification and destruction path are recorded.

Ordinary development never connects to production stores for convenience.

### 6.5 Run workbenches

SenTient, GF Wordbench, notebooks, compilers, and AI tools run inside their declared workspace or build boundary.

Outputs are candidate files, reports, test results, or artifacts.

A canonical registry or product store changes only after its owner accepts a reviewed and validated change.

### 6.6 Execute migrations

A development migration targets:

- a workspace-owned development database;
- an ephemeral test database;
- a clean migration-validation target;
- a separately authorized staged release target.

The target identity is explicit before execution.

A migration cannot infer its target from a convenient default connection.

### 6.7 Produce candidate artifacts

Artifact production records:

- source revision;
- workspace or build identity;
- toolchain version;
- active profile;
- declared inputs;
- build command or pipeline identity;
- test results;
- producer identity;
- artifact class;
- compatibility targets;
- evidence references.

The candidate remains inactive until the release and activation contracts accept it.

### 6.8 Clean up a workspace

Workspace cleanup:

1. stops workspace services;
2. cancels or completes jobs;
3. removes workspace containers and mutable volumes;
4. revokes workspace credentials;
5. destroys governed test data according to policy;
6. removes local virtual environments and generated state;
7. retains required source history, candidate artifacts, and registered evidence;
8. confirms that other workspaces and operational deployments are unchanged.

## 7. Profile Boundaries and Transitions

### 7.1 Development to user profile

A user-profile release receives:

- validated runtime artifacts;
- runtime dependency declarations;
- precompiled language artifacts;
- required migration packages;
- release metadata;
- tests and evidence.

It does not receive:

- source workspaces;
- compilers;
- GF Wordbench;
- SenTient;
- editable installs;
- development containers;
- local databases;
- test identities;
- developer secrets.

### 7.2 Development to sovereign node

A sovereign-node transition produces a signed candidate Release Set and, when applicable, an immutable signed system image.

The sovereign node independently validates:

- release identity;
- signatures;
- profile compatibility;
- artifacts;
- migrations;
- policy;
- recovery;
- evidence.

A developer workstation never becomes a sovereign node through in-place hardening alone.

### 7.3 Development to Build Farm

A developer submits declared source and build inputs.

Build Farm starts from a clean worker state, resolves the build profile and toolchain, produces candidates, runs required tests, records evidence, and discards mutable worker state.

Developer-local success is useful but does not replace clean Build Farm validation when that validation is required.

### 7.4 Build Farm to release channels

Build Farm submits candidate artifacts to the relevant channel:

- system;
- services;
- governance;
- knowledge.

Each channel applies its artifact class, compatibility, approval, and publication rules.

A build result is not an activated Release Set.

### 7.5 Windows to WSL boundary

Windows-host actions crossing into WSL are explicit.

Examples include:

- copying a file;
- invoking a Windows program;
- using a Windows credential;
- accessing a mounted Windows filesystem;
- forwarding a port;
- sharing clipboard data;
- launching a browser or editor.

The workspace contract declares which actions are permitted and how data, identity, and provenance are preserved.

### 7.6 Development integration boundary

External services used for development have development accounts, scopes, credentials, and destinations.

A development integration does not silently reuse a production endpoint.

Candidate output from external AI or creative services remains non-authoritative.

### 7.7 Emergency operational work

An operational incident does not turn a development workstation into an unrestricted administration platform.

Any exceptional access uses a separately authorized operations or emergency path, time-bounded credentials, explicit scope, required receipts, and post-event review.

## 8. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained state | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| Workspace identity is missing or duplicated | Block service startup and artifact claims | Source files remain inspectable | Guessing a namespace | Workspace-validation result |
| Lockfile and environment disagree | Recreate the local environment from locked inputs | Source and caches | Continuing with undeclared dependencies | Dependency result |
| Shared mutable environment is detected | Block conformance and isolate the workspace | Read-only shared caches | Reusing the shared installation | Isolation result |
| Port, socket, network, database, or volume collision occurs | Stop the affected workspace and allocate a new namespace | Other workspaces | Reusing another workspace's mutable state | Collision report |
| Production credential is detected | Revoke or quarantine it and block affected work | Non-sensitive source work | Continuing the development session | Secret-boundary incident |
| Production or governed data appears without authorization | Stop processing, isolate data, and follow incident handling | Unaffected synthetic data | Copying or retaining the data informally | Data-boundary incident |
| SenTient or another workbench is unavailable | Disable the optional workbench | Source, deterministic tools, builds, and tests | Treating workbench output as required authority | Capability status |
| External AI is unavailable | Disable AI assistance | Local development and deterministic validation | Silent provider substitution | Integration status |
| WSL interop violates policy | Block the crossing action | Linux workspace operation | Falling back to unrestricted host access | WSL-boundary result |
| Container runtime is unavailable | Use a declared non-container path or block the affected service | Workspace source and other tools | Declaring containers globally mandatory | Service result |
| Local database migration fails | Discard or repair the isolated target | Source and other workspaces | Applying the failed state to production | Migration evidence |
| Build worker fails | Mark the candidate build failed or blocked | Source revision and prior artifacts | Publishing partial worker output | Build result |
| Required test cannot run | Mark the artifact or claim blocked | Completed valid tests | Reporting pass | Test evidence |
| Artifact compatibility fails | Reject the candidate | Current active product artifacts | Partial activation | Compatibility result |
| Publication is unavailable | Retain the validated candidate | Local artifact and evidence | Copying directly to an active deployment | Publication status |
| Workspace cleanup is incomplete | Mark decommissioning blocked | Retained source and evidence | Reassigning the namespace as clean | Cleanup result |
| Cache corruption occurs | Discard and rebuild the cache | Workspace-owned authoritative state | Treating cache as source truth | Cache-rebuild result |

Development degradation remains workspace-scoped and cannot weaken product authority, operational security, or release validation.

## 9. Cross-System Interactions

### 9.1 Source repository and workspace

The repository supplies versioned source.

The workspace supplies mutable realization.

Generated state remains outside canonical source locations unless the artifact or documentation contract explicitly places it there.

### 9.2 Resource Governor

Development Resource Governor applies workspace resource limits and avoids host exhaustion.

It does not authorize source changes, tests, publication, or production access.

### 9.3 Component services

Development component instances use the same semantic contracts as product components where applicable.

They use isolated identities, stores, ports, and queues.

A development instance cannot write an operational component's authoritative state.

### 9.4 Build Farm

Build Farm consumes source and toolchain inputs and returns candidates plus evidence.

It does not inherit the developer's local virtual environment, database volume, container state, or unregistered files.

### 9.5 Artifact and release registries

Candidate artifacts are registered by class and validated.

Release-channel owners assemble compatible identities and publish the active release candidates.

Activation occurs in the target profile, not in the development workspace.

### 9.6 Identity and secrets

Development identities are scoped to the workspace, test environment, or development integration.

Production identity enrollment and operational privilege remain outside the ordinary development profile.

### 9.7 External integrations

Development integrations use declared adapters and development destinations.

Transferred data is minimized and classified.

Returned output remains candidate material.

### 9.8 Documentation and canonical registries

A developer edits source files and generated candidates in a workspace.

Canonical JSON registries remain the owners of structured facts.

Validation and review precede merge and authority activation.

### 9.9 AI agents

An AI development agent:

1. loads the active workspace context;
2. identifies candidate files;
3. preserves profile and authority boundaries;
4. avoids production credentials and data;
5. produces reviewable changes;
6. runs deterministic validation;
7. records provenance;
8. does not claim activation or release completion.

## 10. Decision Closure and Validation Criteria

This document is supported by the accepted decisions declared in its metadata.

A semantic change to development boundaries requires:

1. an accepted owner decision;
2. impact analysis across profiles, toolchains, components, workspaces, security, integrations, artifacts, releases, lifecycle, tests, evidence, and operations;
3. updates to canonical contracts;
4. complete validation before authority activation.

The following assumptions are prohibited:

- a developer workstation is an operational production profile;
- a locally running service is a deployed product service;
- developer access implies production access;
- one virtual environment can be shared by parallel workspaces;
- a shared package cache is a shared installed environment;
- different branches can safely use the same database volume;
- default ports are safe for parallel applications;
- a container name or network need not include workspace identity;
- a test database can point to production when no writes are intended;
- a production secret is acceptable in development because the developer is trusted;
- WSL automatically isolates Windows credentials and files;
- Windows interop is harmless because it is local;
- SenTient is part of the user or sovereign runtime;
- GF Wordbench belongs in the ordinary user profile;
- an AI suggestion is authoritative source;
- a successful developer build proves Build Farm or release conformance;
- a build artifact is active because it was signed or uploaded;
- a running development container can be copied into production;
- Kubernetes is required on endpoints because it exists in another profile;
- Podman, Docker, systemd, Quadlet, GNOME, KDE, or Wayland is globally required by development use;
- a local migration proves operational migration safety;
- copying a database volume is a valid release transition;
- cleanup can omit credential revocation;
- development exceptions silently weaken product requirements.

This document is conformant when:

1. it is registered as `DOC-DEV-001`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists and applicable assertions pass;
6. every development environment declares one development profile and explicit overlays;
7. Linux workstation, Windows WSL, and Build Farm remain distinguishable;
8. every workspace has a unique identity and isolated mutable state;
9. every Python workspace has a local `.venv` realized from `pyproject.toml` and `uv.lock`;
10. no mutable installed dependency environment is shared;
11. service ports, networks, sockets, volumes, databases, queues, and identities are collision-free;
12. development services cannot write production or another workspace's authoritative state;
13. production data and secrets are absent unless a specific authorized procedure applies;
14. SenTient and GF Wordbench remain limited to permitted development and build profiles;
15. external AI output remains candidate material;
16. WSL tests verify filesystem, identity, networking, credential, and interop boundaries;
17. Build Farm starts from declared inputs and clean mutable worker state;
18. artifacts retain source, toolchain, profile, test, and producer attribution;
19. product profiles receive validated artifacts rather than mutable workspace state;
20. release-channel publication and target activation remain separate from build success;
21. development migrations use isolated or explicitly authorized staged targets;
22. failures remain workspace-scoped;
23. cleanup removes mutable state and revokes workspace identities;
24. every profile's offline and external-dependency envelope is tested;
25. conformance claims contain target, source, toolchain, workspace, services, data, integrations, tests, and evidence;
26. no development implementation choice is promoted to global authority;
27. no unresolved marker or parallel operational authority exists;
28. the active text contains the complete required section structure.

Applicable failure codes include:

`text
development_profile_missing
development_profile_role_collision
workspace_identity_missing
workspace_identity_duplicate
shared_mutable_environment
workspace_namespace_collision
cross_workspace_data_write
production_data_in_development
production_secret_in_development
production_privilege_in_development
sentient_profile_violation
development_workbench_authority_violation
external_ai_source_authority_violation
uv_lock_mismatch
workspace_venv_missing
wsl_boundary_violation
build_input_undeclared
build_worker_state_leak
artifact_provenance_missing
mutable_workspace_promoted
release_transition_bypass
development_migration_target_invalid
workspace_cleanup_incomplete
development_evidence_missing
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Parallel Python branches

Two branches are checked out as separate workspaces.

Each has its own `.venv`, database, ports, socket path, service identities, and generated-output root. Both use the same read-only UV download cache. Updating dependencies in one workspace does not alter the other.

### Example 2 — WSL workspace

A developer uses Windows 11 with a WSL Linux distribution.

The repository, `.venv`, database, and service volumes live in the Linux filesystem. Opening a browser on Windows is an explicit interop action. Windows credentials are not automatically imported into Linux services.

### Example 3 — SenTient analysis

SenTient analyzes candidate architecture material in an isolated developer workspace.

It produces a report. A human reviews the report, updates canonical source through the ordinary review path, and runs deterministic validation. SenTient does not write the active authority registry.

### Example 4 — User release

A developer builds a services candidate locally.

Build Farm rebuilds it from declared source and locked toolchains, runs tests, and publishes a validated candidate. User Lightweight consumes the released runtime artifact without the compiler, source workspace, SenTient, or GF Wordbench.

### Example 5 — Sovereign system image

A Linux developer tests a service inside a mutable container.

The sovereign-node release process does not copy that container state. It produces registered service artifacts and a signed immutable system-image candidate, validates a compatible Release Set, and activates it atomically on the sovereign target.

### Example 6 — Migration test

A developer creates a database migration.

The migration runs against an ephemeral copy created for validation. It records forward, rollback, and forward-repair results. No connection string points to an operational store.

### Example 7 — External AI assistance

An external AI service proposes a code change.

The result is stored as candidate text with provenance. The developer reviews it, runs tests and security checks, and submits it through the normal source-review process. The provider cannot merge or release it.

### Example 8 — Workspace deletion

A feature workspace is retired.

Its services stop, credentials are revoked, test data and volumes are destroyed, and `.venv` is removed. Required source history, build evidence, and registered artifacts remain. Other workspaces continue unchanged.
