<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-004",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "developer_linux_workstation",
    "developer_windows_wsl",
    "build_farm"
  ],
  "canonical_refs": [
    "contracts/toolchains/python-uv.toolchain.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "generated/component-catalog.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-SENT-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-DEV-DEP-001",
    "REQ-DEV-DEP-002",
    "REQ-DEV-DEP-003",
    "REQ-DEV-DEP-004",
    "REQ-DEV-DEP-005",
    "REQ-DEV-DEP-006",
    "REQ-DEV-DEP-007",
    "REQ-DEV-DEP-008",
    "REQ-DEV-DEP-009",
    "REQ-DEV-DEP-010",
    "REQ-DEV-DEP-011",
    "REQ-DEV-DEP-012",
    "REQ-DEV-DEP-013",
    "REQ-DEV-DEP-014",
    "REQ-DEV-DEP-015",
    "REQ-DEV-DEP-016",
    "REQ-DEV-DEP-017",
    "REQ-DEV-DEP-018",
    "REQ-DEV-DEP-019",
    "REQ-DEV-DEP-020",
    "REQ-DEV-DEP-021",
    "REQ-DEV-DEP-022",
    "REQ-DEV-DEP-023",
    "REQ-DEV-DEP-024"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-PROFILE-001",
    "LOCK-DATA-001",
    "LOCK-SENT-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-DEV-000",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003"
  ],
  "tags": [
    "development",
    "dependencies",
    "workspace-isolation",
    "uv",
    "lockfiles",
    "venv",
    "caches",
    "containers",
    "reproducibility",
    "supply-chain"
  ]
}
KOA:DOC-META:END -->

# Dependency Isolation

## 1. Purpose

This document defines how kOA development workspaces isolate, lock, install, validate, share, update, and remove software dependencies.

Dependency isolation exists to make parallel development safe and reproducible. One branch, repository, user, test run, or optional workbench cannot silently change another workspace's installed environment.

The canonical Python rules are owned by `contracts/toolchains/python-uv.toolchain.json`. Profile contracts determine where the toolchain applies. This document explains the development model and does not create a second owner for tool versions, commands, lock formats, or profile membership.

## 2. Scope

This document applies to:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`;
- application repositories and worktrees;
- Python runtime and build dependencies;
- non-Python language and build toolchains registered by active contracts;
- local editable dependencies;
- native libraries and operating-system build dependencies;
- container images and build-worker images;
- service dependencies such as databases, queues, search services, and test fixtures;
- shared download and build caches;
- optional isolated workbenches such as SenTient;
- dependency updates, validation evidence, cleanup, and development-to-release transitions.

This document does not define profile membership, component data ownership, package-manager internals, provider repositories, product-specific dependency lists, or release approval.

Secrets, credentials, ports, volumes, and databases are not software dependencies, but their isolation is required when a dependency uses them.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/toolchains/python-uv.toolchain.json` | Python runtime declaration, UV usage, lock state, workspace `.venv`, frozen synchronization, cache policy, and supported commands |
| `contracts/toolchains/container-runtime.toolchain.json` | Container-runtime-neutral development-service and image-identity rules |
| `generated/profile-catalog.json` | Active development and build profiles |
| `contracts/profiles/developer-linux-workstation.profile.json` | Linux developer applicability and strengthened requirements |
| `contracts/profiles/developer-windows-wsl.profile.json` | WSL developer applicability and host-boundary requirements |
| `contracts/profiles/build-farm.profile.json` | Clean worker, cache, reproducibility, and release-evidence requirements |
| `generated/component-catalog.json` | Component identity and logical data ownership |
| `contracts/artifact-classes.contract.json` | Dependency, build, provenance, SBOM, evidence, and release artifact behavior |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Development isolation, reproducibility, data, lifecycle, and implementation invariants |
| `generated/traceability.json` | Links among workspaces, toolchains, profiles, requirements, tests, and evidence |
| `generated/test-catalog.json` | Registered dependency-isolation tests |
| `generated/evidence-catalog.json` | Registered evidence supporting isolation and reproducibility claims |

## 4. Model and Responsibilities

### 4.1 Isolation unit

The isolation unit is the workspace identified by `workspace_id`.

A workspace contains or owns references to:

- one source checkout or worktree;
- one mutable installed dependency environment per applicable toolchain;
- one declared runtime version set;
- one service namespace;
- one network namespace or equivalent logical isolation;
- one port-allocation set;
- one volume and temporary-data namespace;
- one secret namespace;
- one database identity set;
- one resource budget;
- one evidence context.

The repository is not the isolation unit when two branches or worktrees run concurrently. The user account and host are not dependency environments.

### 4.2 Dependency-state classes

| State class | Examples | Mutability | Sharing rule | Authority |
| --- | --- | --- | --- | --- |
| Source declarations | `pyproject.toml`, manifests, build definitions | Changed through reviewed source changes | Shared through version control | Declares requested dependencies |
| Resolution locks | `uv.lock`, immutable image digests, locked manifests | Changed only through controlled resolution | Shared through version control or registered artifacts | Defines the resolved graph |
| Installed environment | `.venv`, installed modules, compiled local dependencies | Mutable during workspace synchronization | One per workspace | Execution environment only |
| Download cache | Wheels, archives, source objects, OCI layers | Entries immutable by content identity; index metadata bounded | May be shared | Performance optimization only |
| Build cache | Compiler and build outputs keyed by complete inputs | Evictable and reproducible | May be shared when collision-safe | Performance optimization only |
| Service dependency state | Database files, queue state, search indexes, fixtures | Mutable | Workspace-scoped | Owned by the applicable component or fixture |
| Toolchain or worker image | Runtime, compiler, native tools, operating-system packages | Immutable or reproducibly defined | May be reused by identity | Declares the execution base |
| Secrets and local identities | Tokens, passwords, certificates, service users | Mutable and revocable | Workspace-scoped unless a separate contract states otherwise | Access identity, not dependency resolution |

A shared cache never becomes the installed environment. Eviction of a cache may increase execution time but cannot alter the committed dependency graph.

### 4.3 Python and UV

Every Python workspace contains:

`text
pyproject.toml
uv.lock
.venv/
`

The Python version is declared by the repository or active toolchain contract.

The workspace-local `.venv` contains installed mutable state. It is not committed, copied between branches, or shared across workspaces.

Frozen validation uses:

`bash
uv sync --frozen
`

A content-addressed UV cache may be shared. Global application dependency installation is outside the development contract.

### 4.4 Non-Python toolchains

A non-Python toolchain follows the same separation:

1. versioned declarations;
2. a committed lock or equivalent immutable resolution identity;
3. a workspace-local installed environment or immutable worker image;
4. declared runtime and build-tool versions;
5. frozen or reproducible installation;
6. bounded immutable caches;
7. evidence identifying all material inputs.

Where a language ecosystem has no lock format, the active toolchain contract defines the equivalent reproducible identity. This document does not infer one.

### 4.5 Local and editable dependencies

A local editable dependency is permitted only when its relationship is explicit.

The dependency resolves:

- inside the same workspace;
- through a declared workspace mapping; or
- through a versioned immutable artifact.

A sibling checkout discovered through `PATH`, `PYTHONPATH`, editor configuration, shell aliases, user-site packages, or undeclared filesystem layout is not a valid dependency declaration.

### 4.6 Native and host dependencies

Native compilers, libraries, headers, system tools, and operating-system packages are material dependencies.

They are declared by:

- the profile contract;
- a toolchain contract;
- a locked container or worker image;
- a reproducible environment definition;
- a registered build artifact.

The current developer host is not a reproducibility contract. A successful local build does not establish that all host inputs were declared.

### 4.7 Service dependency isolation

Databases, queues, search services, object stores, and equivalent dependencies use workspace-scoped identities.

One physical process may serve multiple workspaces only when:

- logical databases, schemas, users, queues, indexes, buckets, or namespaces are separate;
- credentials are separate;
- cleanup is workspace-scoped;
- cross-workspace writes are blocked;
- resource limits prevent one workspace from exhausting all others.

Physical sharing does not transfer component or workspace ownership.

### 4.8 Cache model

A shared cache is acceptable when:

- objects are keyed by content identity or complete reproducible inputs;
- an object is immutable after publication under its key;
- corruption is detected;
- invalid content is rejected and evicted;
- cache absence does not change resolution;
- cache metadata does not inject undeclared dependencies;
- credentials and private source material follow separate security rules.

A shared mutable installation directory is not a cache.

### 4.9 Dependency updates

A dependency update is one controlled semantic change.

The change includes declarations, lock state, relevant toolchain or image identity, compatibility evaluation, security and license review, tests, evidence, and impact on profiles, components, artifacts, and releases.

Automatic background updates cannot modify active workspace or release authority.

### 4.10 Development and release boundary

A development environment may produce candidate build and test results.

Release-authoritative installation uses a clean isolated worker or another release-authorized environment. The worker consumes the committed source, declarations, locks, toolchain identity, and required immutable artifacts.

A local cache hit, developer workstation success, or existing `.venv` does not replace release-environment reproduction when the release contract requires it.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-DEP-001,REQ-DEV-DEP-002,REQ-DEV-DEP-003,REQ-DEV-DEP-004,REQ-DEV-DEP-005,REQ-DEV-DEP-006,REQ-DEV-DEP-007,REQ-DEV-DEP-008,REQ-DEV-DEP-009,REQ-DEV-DEP-010,REQ-DEV-DEP-011,REQ-DEV-DEP-012,REQ-DEV-DEP-013,REQ-DEV-DEP-014,REQ-DEV-DEP-015,REQ-DEV-DEP-016,REQ-DEV-DEP-017,REQ-DEV-DEP-018,REQ-DEV-DEP-019,REQ-DEV-DEP-020,REQ-DEV-DEP-021,REQ-DEV-DEP-022,REQ-DEV-DEP-023,REQ-DEV-DEP-024 -->
- **REQ-DEV-DEP-001 — SHALL:** Every active development workspace shall have one distinct mutable dependency environment identified by its `workspace_id`.
- **REQ-DEV-DEP-002 — SHALL NOT:** Two workspaces shall not share an installed mutable application dependency environment.
- **REQ-DEV-DEP-003 — SHALL:** Dependency declarations, lockfiles, runtime versions, build-tool versions, and resolution settings shall be versioned or referenced through an active toolchain contract.
- **REQ-DEV-DEP-004 — SHALL:** Reproducible validation shall resolve and install dependencies from the committed lock state without silently updating that state.
- **REQ-DEV-DEP-005 — SHALL NOT:** A globally installed application dependency shall not satisfy a workspace dependency requirement.
- **REQ-DEV-DEP-006 — SHALL:** Python workspaces shall use UV, shall contain `pyproject.toml` and `uv.lock`, shall declare the Python version, and shall maintain one workspace-local `.venv`.
- **REQ-DEV-DEP-007 — SHALL:** Frozen Python validation shall use `uv sync --frozen` or the exact canonical equivalent declared by the active UV toolchain contract.
- **REQ-DEV-DEP-008 — SHALL NOT:** A mutable `.venv` shall not be shared across repositories, worktrees, branches, users, or workspaces.
- **REQ-DEV-DEP-009 — SHALL:** A shared dependency-download cache shall be content-addressed or equivalently immutable, shall be treated as non-authoritative, and shall not contain workspace-installed state.
- **REQ-DEV-DEP-010 — SHALL:** Cache corruption, eviction, or absence shall affect performance only and shall not change the locked dependency graph.
- **REQ-DEV-DEP-011 — SHALL:** Local editable or path dependencies shall be declared explicitly and shall resolve within the current workspace or through a versioned immutable artifact.
- **REQ-DEV-DEP-012 — SHALL NOT:** An undeclared host path, user directory, sibling checkout, shell state, or editor environment shall not become an implicit dependency.
- **REQ-DEV-DEP-013 — SHALL:** Workspace command execution shall use a deterministic tool and runtime search path that prioritizes the workspace environment over host-global installations.
- **REQ-DEV-DEP-014 — SHALL:** Service dependencies shall be isolated by workspace-scoped service, network, port, volume, secret, database, and temporary-data identities.
- **REQ-DEV-DEP-015 — SHALL NOT:** Sharing one physical database, container runtime, package cache, or service process shall not transfer logical data ownership or permit cross-workspace mutation.
- **REQ-DEV-DEP-016 — SHALL:** Container images and build environments used for reproducible validation shall be identified by immutable digest, locked manifest, or reproducible build definition.
- **REQ-DEV-DEP-017 — SHALL:** System-level and native build dependencies shall be declared by the applicable profile, toolchain, container image, build-worker image, or reproducible environment contract.
- **REQ-DEV-DEP-018 — SHALL NOT:** A successful build that depends on undeclared host packages or mutable host configuration shall not support a reproducibility or release claim.
- **REQ-DEV-DEP-019 — SHALL:** SenTient and other optional heavy workbenches shall maintain dependency environments separate from ordinary application workspaces.
- **REQ-DEV-DEP-020 — SHALL:** Dependency updates shall modify declarations and lock state in one controlled change and shall run compatibility, security, license, build, test, and profile-impact checks applicable to the changed graph.
- **REQ-DEV-DEP-021 — SHALL:** Dependency evidence shall identify the workspace, source revision, runtime, toolchain, declarations, lockfiles, installed-environment identity, container or worker identity, and relevant cache policy.
- **REQ-DEV-DEP-022 — SHALL:** Release-authoritative dependency installation shall occur in a clean, isolated, reproducible environment using the committed lock state.
- **REQ-DEV-DEP-023 — SHALL:** Workspace deletion shall remove its mutable dependency environment without deleting another workspace's environment or a valid shared immutable cache.
- **REQ-DEV-DEP-024 — SHALL:** Every active dependency-isolation claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Create a dependency environment

1. Resolve the active profile and workspace identifier.
2. verify the declared runtime and toolchain contract;
3. verify source declarations and lock state;
4. create the workspace-local installed environment;
5. configure workspace-local runtime and tool search paths;
6. configure allowed immutable caches;
7. install from the committed lock state;
8. validate that global and sibling-workspace dependencies are absent;
9. record the environment identity.

### 6.2 Frozen synchronization

1. Enter the selected workspace.
2. verify that the runtime version matches the declaration;
3. verify that declarations and lock state are consistent;
4. run the toolchain's frozen synchronization command;
5. reject lockfile mutation;
6. reject undeclared dependency discovery;
7. run import, build, or runtime smoke checks;
8. record the toolchain, lock, and installed-environment identities.

For Python, the canonical command is `uv sync --frozen`.

### 6.3 Add or update a dependency

1. Create a dedicated source change.
2. modify the canonical dependency declaration;
3. resolve the graph with the registered toolchain;
4. update the lock state in the same change;
5. review direct and transitive changes;
6. evaluate compatibility, security, license, platform, profile, and resource effects;
7. rebuild the workspace environment from the new lock state;
8. execute applicable tests;
9. update SBOM, provenance, evidence, and impact records when required;
10. merge only after validation passes.

### 6.4 Use a local editable dependency

1. Declare the local relationship in the applicable toolchain configuration.
2. bind it to the current workspace identity;
3. verify that the target path is inside the workspace or a declared mapping;
4. prevent fallback to an arbitrary sibling checkout;
5. include the source revision in evidence;
6. replace the editable relation with an immutable artifact where the release process requires it.

### 6.5 Run parallel workspaces

1. Resolve each workspace identifier.
2. verify distinct installed dependency environments;
3. verify distinct runtime search paths;
4. verify service, database, network, port, volume, secret, and temporary-data isolation;
5. start both workspaces;
6. run collision and cross-write checks;
7. change a dependency in one workspace;
8. verify that the other workspace remains unchanged.

### 6.6 Clean a dependency environment

1. Stop workspace processes that use the environment.
2. remove the workspace-local installed environment;
3. remove workspace-specific build outputs and temporary dependency state;
4. retain shared immutable cache entries according to cache policy;
5. preserve another workspace's environments and service data;
6. verify that frozen synchronization can reconstruct the removed environment.

### 6.7 Transition to release validation

1. Select the committed source revision.
2. resolve committed declarations and lockfiles;
3. select the registered clean worker or immutable build environment;
4. provision no prior workspace-installed state;
5. synchronize using the frozen or reproducible toolchain path;
6. record native, runtime, toolchain, image, and lock identities;
7. build and test;
8. generate required SBOM, provenance, test evidence, and artifacts;
9. compare results with supported profiles and release requirements;
10. admit only validated outputs to the release workflow.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Missing lockfile | Block frozen validation and release-relevant installation. | Source and existing workspace environment | Reproducibility claim |
| Lockfile and declaration mismatch | Reject frozen synchronization and require one controlled dependency update. | Committed source and previous valid lock state | Silent lock regeneration |
| Shared mutable environment detected | Block isolation and reproducibility claims until separate environments are created. | Source repositories | Parallel-workspace conformance |
| Global dependency satisfies an import | Fail the isolation check and recreate the workspace using only declared dependencies. | Committed declarations and lockfiles | Environment-validity claim |
| Cache unavailable | Fetch or rebuild locked artifacts through an authorized source when connectivity and policy permit. | Locked dependency graph | Cache-dependent correctness assumption |
| Cache entry corrupt | Reject and evict the entry, then obtain or rebuild the same locked content. | Workspace installed environment until safely replaced | Use of corrupt content |
| Undeclared local path dependency | Reject the build or test and require an explicit workspace or immutable-artifact declaration. | Other declared dependencies | Host-path-dependent result |
| Runtime version mismatch | Block synchronization or validation under the wrong runtime. | Source and lock state | Cross-version conformance claim |
| Native system dependency missing | Block only affected builds or tests and report the missing declared environment capability. | Other workspace operations | Fallback to an undeclared host package |
| Container image tag moved | Reject digest-sensitive validation and resolve the registered immutable identity. | Previous verified image or worker state | Mutable-tag reproducibility claim |
| Security or license policy failure | Block affected dependency update or release claim according to policy. | Previous valid lock state | Unsupported activation |
| Workspace cleanup failure | Mark the workspace incomplete and preserve other workspaces and shared immutable caches. | Other workspace environments | Cross-workspace deletion |

A dependency failure cannot authorize lockfile guessing, host-global fallback, cross-workspace environment reuse, or release claims based on undeclared inputs.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Boundary |
| --- | --- | --- | --- |
| Workspace identity model | Toolchain | Supplies `workspace_id` and namespace | Toolchain cannot merge mutable environments |
| Source repository | Dependency resolver | Supplies declarations and lock state | Resolver cannot silently create architectural authority |
| UV or registered toolchain | Workspace | Installs the resolved graph | Installed environment remains workspace-local |
| Shared cache | Toolchain or build worker | Supplies immutable content by identity | Cache is non-authoritative and evictable |
| Container or worker image | Build and test process | Supplies declared native and toolchain dependencies | Mutable host state is not inherited implicitly |
| Service container or local service | Application workspace | Supplies a declared service dependency | Service data and identity remain workspace-scoped |
| Component contract | Database or service dependency | Defines component data ownership | Physical sharing cannot permit cross-component writes |
| Resource Governor | Workspaces and dependency jobs | Limits CPU, memory, I/O, concurrency, storage, and queues | Resource limits do not define the dependency graph |
| SenTient workbench | Owning development workflow | Produces candidate output in its own isolated environment | Its dependencies and outputs do not enter ordinary application authority automatically |
| Build farm | Release process | Produces clean build, test, SBOM, provenance, and evidence | Development workstation state does not become release authority |
| Evidence producer | Evidence registry | Records material dependency identities | Evidence reports inputs and results; it does not change them |

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-DEV-001` | Every development workspace has a distinct mutable environment; Python uses UV, a declared Python version, `pyproject.toml`, `uv.lock`, a workspace `.venv`, and frozen synchronization. |
| `DEC-DEV-002` | Parallel applications and branches use stable workspace identifiers and isolated namespaces. |
| `DEC-PROFILE-001` | Dependency rules apply through explicit development and build profiles. |
| `DEC-CONTAINER-001` | Container-runtime choice is profile-scoped and application contracts remain runtime-neutral. |
| `DEC-DATA-001` | Physical service sharing does not transfer logical component data ownership. |
| `DEC-SENT-001` | SenTient has its own isolated task-activated environment. |
| `DEC-REL-001` | Release artifacts require registered compatibility, provenance, tests, evidence, and activation. |

### Prohibited assumptions

- One repository needs only one dependency environment when branches run concurrently.
- A user account or host is a dependency-isolation boundary.
- A shared `.venv` is safe when dependencies currently match.
- A globally installed package may satisfy an undeclared dependency.
- `PATH`, `PYTHONPATH`, user-site packages, shell aliases, or editor settings are declarations.
- A lockfile can be regenerated during frozen validation.
- A cache entry is authoritative because it already exists.
- A shared mutable installation directory is a cache.
- A moving container tag is an immutable build identity.
- A successful local build proves native and host dependencies are declared.
- One database process permits shared component tables or identities.
- An editable sibling checkout may be discovered implicitly.
- SenTient may install into an ordinary application environment.
- Dependency updates may occur in the background.
- Development workstation success automatically creates release authority.
- Cleanup may delete another workspace's state.
- Missing lock or toolchain values may be filled from industry practice.
- A recipe command overrides the active toolchain contract.
- Missing evidence may be replaced by developer confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-DEV-004`, status `active`, language `en`, development layer, and the three declared profile scopes.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-DEV-DEP-001` verifies one distinct mutable installed environment per workspace.
7. `TEST-DEV-DEP-002` detects and rejects shared mutable `.venv` or equivalent installed state.
8. `TEST-DEV-DEP-003` verifies committed declarations, lockfiles, runtime versions, and toolchain identity.
9. `TEST-DEV-DEP-004` verifies frozen synchronization without lockfile mutation.
10. `TEST-DEV-DEP-005` verifies that global and user-site application dependencies cannot satisfy workspace imports.
11. `TEST-DEV-DEP-006` verifies the Python UV contract, including `pyproject.toml`, `uv.lock`, declared Python, workspace `.venv`, and `uv sync --frozen`.
12. `TEST-DEV-DEP-007` verifies shared cache content identity, immutability, corruption handling, and non-authority.
13. `TEST-DEV-DEP-008` verifies explicit local editable dependencies and rejection of undeclared sibling paths.
14. `TEST-DEV-DEP-009` verifies deterministic runtime and tool search paths.
15. `TEST-DEV-DEP-010` verifies service, database, network, port, volume, secret, and temporary-data isolation.
16. `TEST-DEV-DEP-011` verifies immutable or reproducible container and worker identities.
17. `TEST-DEV-DEP-012` verifies declaration of native system and build dependencies.
18. `TEST-DEV-DEP-013` verifies isolation of SenTient and other optional workbenches.
19. `TEST-DEV-DEP-014` verifies dependency-update compatibility, security, license, profile, and impact checks.
20. `TEST-DEV-DEP-015` verifies cleanup without cross-workspace deletion.
21. `TEST-DEV-DEP-016` verifies clean release-authoritative installation from committed lock state.
22. `TEST-DEV-DEP-017` verifies that evidence records all material source, runtime, toolchain, lock, environment, image, worker, and cache-policy identities.
23. `TEST-DEV-DEP-018` verifies traceability to decisions, requirements, locks, tests, and evidence.
24. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
25. The generated requirement block matches the canonical requirements registry.

These criteria define validation requirements. They do not claim that a particular workspace, dependency graph, cache, image, or build already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** Two Konnaxion branches share the UV download cache but each branch has a separate `.venv`. Updating the feature branch lockfile changes only its environment.

> **Non-normative example:** A package exists in the developer's global Python installation. The workspace does not declare it. An isolation test starts Python without global or user-site packages and correctly fails the undeclared import.

> **Non-normative example:** PostgreSQL runs as one local process. Two workspaces use different databases, users, credentials, volumes, ports, and cleanup scopes. Neither workspace can write the other's data.

> **Non-normative example:** A cached wheel fails integrity verification. The cache entry is removed and the same locked wheel is obtained from an authorized source. The lockfile does not change.

> **Non-normative example:** A developer uses an editable local library in one workspace. The relationship is declared explicitly and its source revision is recorded. The release build replaces it with a versioned artifact or reconstructs it from the committed source graph.

> **Non-normative example:** A local build succeeds because an undeclared system header exists on the workstation. A clean build worker lacks that header and fails. The result exposes the missing environment declaration; it does not justify adding an ad hoc package to the worker.
