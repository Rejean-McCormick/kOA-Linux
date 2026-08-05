<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "development",
  "scope": [
    "development_toolchain:python_uv",
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl",
    "profile:build_farm"
  ],
  "canonical_refs": [
    "contracts/toolchains/python-uv.toolchain.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
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
    "DEC-LIFE-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001"
  ],
  "requirement_ids": [
    "REQ-DEV-UV-001",
    "REQ-DEV-UV-002",
    "REQ-DEV-UV-003",
    "REQ-DEV-UV-004",
    "REQ-DEV-UV-005",
    "REQ-DEV-UV-006",
    "REQ-DEV-UV-007",
    "REQ-DEV-UV-008",
    "REQ-DEV-UV-009",
    "REQ-DEV-UV-010",
    "REQ-DEV-UV-011",
    "REQ-DEV-UV-012",
    "REQ-DEV-UV-013",
    "REQ-DEV-UV-014",
    "REQ-DEV-UV-015",
    "REQ-DEV-UV-016",
    "REQ-DEV-UV-017",
    "REQ-DEV-UV-018",
    "REQ-DEV-UV-019",
    "REQ-DEV-UV-020"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-009",
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-003",
    "DOC-DEV-004"
  ],
  "tags": [
    "python",
    "uv",
    "dependency-management",
    "workspace-isolation",
    "virtual-environment",
    "lockfile",
    "reproducibility",
    "parallel-development",
    "offline-development",
    "build-farm"
  ]
}
KOA:DOC-META:END -->

# Python Dependency Isolation with UV

## 1. Purpose

This document defines the kOA development model for Python dependency isolation with UV.

The model gives every Python workspace an independently reproducible installed environment while permitting safe reuse of immutable or content-addressed downloads.

It separates:

- project dependency declarations from installed packages;
- lockfile resolution from frozen synchronization;
- workspace-local mutable environments from shared download caches;
- Python dependency isolation from service and infrastructure isolation;
- development authority from release, signing, and production activation authority;
- normative toolchain behavior from command-oriented recipes.

The canonical machine-readable owner is:

`text
contracts/toolchains/python-uv.toolchain.json
`

This document explains that contract for developers, build systems, validators, maintainers, and AI agents. It does not replace the contract or profile-specific realization.

## 2. Scope

This document applies to Python workspaces in profiles that explicitly adopt the Python and UV toolchain, including:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `build_farm`.

It covers:

- `pyproject.toml`;
- `uv.lock`;
- declared Python compatibility;
- one workspace-local `.venv`;
- frozen synchronization;
- explicit dependency changes;
- shared UV download cache use;
- parallel branches and applications;
- reproducible validation;
- offline restoration;
- workspace cleanup;
- dependency-upgrade impact;
- boundary with databases, services, secrets, ports, and other mutable resources.

It does not define:

- one mandatory operating-system distribution;
- one UV installation method;
- one exact UV binary version for every profile;
- one Python release for every project;
- exact service-container commands;
- exact workspace naming commands;
- database, queue, port, volume, certificate, or secret isolation;
- production packaging and activation;
- signing-key custody;
- release-channel composition.

Those values belong to the toolchain contract, project metadata, profile contracts, service contracts, artifact contracts, security documents, and recipes.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/toolchains/python-uv.toolchain.json` | Dependency manager, environment isolation, project files, Python declaration, synchronization, cache, upgrade, validation, and cleanup rules. |
| `contracts/profiles/developer-linux-workstation.profile.json` | Native Linux development adoption, workspace realization, resources, local services, and network boundaries. |
| `contracts/profiles/developer-windows-wsl.profile.json` | Windows and WSL development adoption, filesystem and process boundary, resources, services, and limitations. |
| `contracts/profiles/build-farm.profile.json` | Release-grade build execution, worker isolation, concurrency, toolchain identity, and build evidence. |
| `generated/profile-catalog.json` | Profile identity and toolchain applicability. |
| `contracts/system.contract.json` | Global offline, authority, lifecycle, degradation, and reproducibility context. |
| `contracts/artifact-classes.contract.json` | Source, build, package, evidence, and release artifact lifecycle. |
| `contracts/release-channels.contract.json` | Channel publication and activation relationships. |
| `generated/requirements-index.json` | Requirement statements displayed in section 5. |
| `generated/assertion-index.json` | Development isolation, mutable-state, parallel-workspace, and shared-cache invariants. |
| `generated/traceability.json` | Decision, requirement, lock, profile, document, test, evidence, and claim relationships. |
| `generated/test-catalog.json` | Profile, operations, security, lifecycle, exit, and documentation test definitions. |
| `generated/evidence-catalog.json` | Executed environment, build, validation, restore, and conformance evidence. |
| `11-recipes/development/python-uv-workspace.md` | Non-authoritative command examples for workspace creation, synchronization, lock refresh, validation, and cleanup. |

The development document explains the model. The recipe demonstrates commands. The toolchain contract remains the canonical owner.

## 4. Model and Responsibilities

### 4.1 Workspace model

Each development workspace is an independently mutable unit.

A complete workspace context includes:

| Context element | Purpose |
| --- | --- |
| `workspace_id` | Stable identity for one application, branch, task, or build purpose. |
| project source | Workspace-specific mutable source tree. |
| `pyproject.toml` | Version-controlled Python project and dependency declarations. |
| `uv.lock` | Version-controlled resolved dependency graph. |
| Python declaration | Project-compatible interpreter version or range. |
| `.venv` | Workspace-local installed dependency environment. |
| UV download cache | Reusable content-addressed downloads that are not installed workspace state. |
| secret namespace | Workspace-specific development credentials and local secret references. |
| service namespace | Workspace-specific databases, queues, search services, and dependent processes. |
| network and ports | Workspace-specific logical network and collision-free host allocations. |
| data namespace | Workspace-specific mutable service volumes, databases, schemas, and temporary state. |
| resource budget | Profile-owned CPU, memory, process, I/O, queue, and heavy-job limits. |

UV owns only the Python dependency and environment portion of this context.

### 4.2 Project declarations

`pyproject.toml` is the version-controlled declaration of the Python project.

It records or references:

- project identity;
- project versioning model;
- supported Python compatibility;
- runtime dependencies;
- development dependency groups;
- optional features;
- build-system configuration;
- tool configuration owned by the project;
- source and package layout.

A local edit to project declarations remains incomplete until the lockfile and required validation are updated explicitly.

### 4.3 Lockfile model

`uv.lock` records the dependency resolution selected for the workspace project.

The lockfile supports:

- reproducible synchronization;
- review of transitive changes;
- offline use when required artifacts are already available;
- build and conformance evidence;
- explicit upgrade review;
- comparison between branches and releases.

Frozen validation consumes the committed lockfile without treating validation as a dependency-resolution operation.

### 4.4 Installed environment

The installed dependency environment belongs to one workspace.

The ordinary location is:

`text
<workspace>/.venv
`

The environment contains mutable installed state derived from:

- `pyproject.toml`;
- `uv.lock`;
- the selected compatible Python interpreter;
- the active platform and profile;
- explicitly selected dependency groups or extras.

Deleting or recreating this environment is a workspace-local operation.

### 4.5 Shared cache boundary

A UV download cache can be shared because cached objects are reusable acquisition inputs rather than installed application state.

The cache does not contain:

- the authoritative project declaration;
- the authoritative lockfile;
- workspace-local editable installation state;
- workspace secrets;
- workspace process state;
- workspace database state;
- a shared mutable site-packages environment.

Cache corruption or loss can require reacquisition but does not redefine project dependencies.

### 4.6 Frozen synchronization

The reproducible synchronization boundary is:

`text
committed pyproject.toml
+
committed uv.lock
+
declared compatible Python
+
declared profile and platform
-> uv sync --frozen
-> workspace-local .venv
`

A frozen synchronization failure reveals one of the following classes:

- missing or incompatible Python;
- project and lock inconsistency;
- unavailable required package material;
- unsupported platform;
- invalid project metadata;
- filesystem or permission failure;
- toolchain identity failure.

The failure does not authorize an implicit lockfile update.

### 4.7 Dependency change model

Dependency declaration changes and frozen synchronization are separate operations.

A dependency addition, removal, version change, source change, or group change follows an explicit change path:

1. edit the project declaration;
2. refresh the lockfile intentionally;
3. inspect direct and transitive changes;
4. evaluate licenses, provenance, vulnerabilities, platform support, and build impact when applicable;
5. synchronize the workspace;
6. run affected tests;
7. record impact and evidence;
8. submit the declaration and lockfile together.

A lockfile-only change without an explainable project, resolution, platform, or tooling reason remains reviewable rather than self-authorizing.

### 4.8 Parallel workspace identity

Two branches or applications can run simultaneously.

A workspace identity can be derived from:

`text
component + branch_or_purpose + unique_suffix
`

Examples:

`text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
`

The identity is reused consistently for:

- workspace directory;
- secret namespace;
- service project;
- network;
- ports;
- volumes;
- database or schema;
- queues;
- temporary directories;
- process and log labels.

The `.venv` remains inside the corresponding workspace.

### 4.9 Service isolation boundary

UV does not isolate:

- PostgreSQL;
- Redis;
- Solr;
- Elasticsearch;
- queues;
- host ports;
- Unix sockets;
- persistent volumes;
- databases or schemas;
- service identities;
- certificates;
- secrets;
- operating-system libraries;
- system services.

Profiles and development-service contracts provide workspace isolation through rootless containers, explicit namespaces, separate identities, separate volumes, separate database identities, or equivalent mechanisms.

A passing `.venv` isolation check does not prove service-state isolation.

### 4.10 Build-farm boundary

A build-farm worker uses a clean or controlled workspace with:

- exact source identity;
- committed project metadata;
- committed lockfile;
- declared Python and UV toolchain identity;
- isolated installed environment;
- bounded resources;
- controlled package acquisition;
- no release-signing private key in the ordinary build process;
- test and build evidence.

Build success does not grant release publication, signing, or activation authority.

### 4.11 Authority and secrets

Workspace access, dependency sources, private indexes, credentials, build publication, and release actions use explicit scoped identity and authority.

Secrets remain outside:

- `pyproject.toml`;
- `uv.lock`;
- committed source;
- logs;
- ordinary command transcripts;
- build reports;
- shared caches;
- exported support bundles.

A private dependency reference records the source contract without embedding unrestricted credentials.

### 4.12 Profiles and portability

Profiles can differ in:

- UV installation;
- Python interpreter provisioning;
- native or WSL filesystem placement;
- container use;
- cache placement;
- network access;
- offline package mirrors;
- resource limits;
- service topology.

They preserve the same environment-isolation and frozen-synchronization model.

Linux-specific or WSL-specific realization does not become a global Python requirement.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-UV-001,REQ-DEV-UV-002,REQ-DEV-UV-003,REQ-DEV-UV-004,REQ-DEV-UV-005,REQ-DEV-UV-006,REQ-DEV-UV-007,REQ-DEV-UV-008,REQ-DEV-UV-009,REQ-DEV-UV-010,REQ-DEV-UV-011,REQ-DEV-UV-012,REQ-DEV-UV-013,REQ-DEV-UV-014,REQ-DEV-UV-015,REQ-DEV-UV-016,REQ-DEV-UV-017,REQ-DEV-UV-018,REQ-DEV-UV-019,REQ-DEV-UV-020 -->
- **REQ-DEV-UV-001 — SHALL:** Each Python workspace has one distinct installed dependency environment.
- **REQ-DEV-UV-002 — SHALL NOT:** Two workspaces share the same mutable `.venv`.
- **REQ-DEV-UV-003 — SHALL:** UV is the canonical dependency and environment manager for Python development workspaces.
- **REQ-DEV-UV-004 — SHALL:** Each Python workspace contains a version-controlled `pyproject.toml`.
- **REQ-DEV-UV-005 — SHALL:** Each Python workspace contains a version-controlled `uv.lock`.
- **REQ-DEV-UV-006 — SHALL:** Each Python workspace declares the Python version or compatible Python-version range used for synchronization and validation.
- **REQ-DEV-UV-007 — SHALL:** The workspace-local installed environment uses the workspace `.venv` path unless an active profile contract declares an equivalent workspace-local path.
- **REQ-DEV-UV-008 — SHALL:** Reproducible validation begins with `uv sync --frozen` against the committed lockfile.
- **REQ-DEV-UV-009 — SHALL NOT:** Release, conformance, or reproducibility validation silently changes `uv.lock`, dependency declarations, or the selected Python version.
- **REQ-DEV-UV-010 — MAY:** Development workspaces share the content-addressed UV download cache.
- **REQ-DEV-UV-011 — SHALL NOT:** A shared UV download cache becomes a shared installed environment, shared mutable site-packages directory, or shared workspace state.
- **REQ-DEV-UV-012 — SHALL NOT:** Application dependencies are installed globally as the normal development or validation mechanism.
- **REQ-DEV-UV-013 — SHALL:** Lockfile refresh and dependency upgrades are explicit operations separate from frozen synchronization.
- **REQ-DEV-UV-014 — SHALL:** A dependency upgrade records the changed declarations and lock state and produces applicable impact analysis and test results.
- **REQ-DEV-UV-015 — SHALL:** Removing, resetting, or recreating one workspace environment leaves every other workspace environment unchanged.
- **REQ-DEV-UV-016 — SHALL:** Parallel branches and applications use distinct workspace identities and isolated mutable dependency state.
- **REQ-DEV-UV-017 — SHALL:** Workspace commands execute with the workspace's declared dependency, Python, profile, secret, service, and resource context.
- **REQ-DEV-UV-018 — SHALL NOT:** UV environment isolation is treated as isolation for databases, ports, queues, volumes, persistent service data, system libraries, certificates, or secrets.
- **REQ-DEV-UV-019 — SHALL:** Python workspaces remain restorable from version-controlled project metadata, the committed lockfile, declared Python compatibility, and separately managed workspace resources.
- **REQ-DEV-UV-020 — SHALL:** Every active Python and UV conformance claim has complete decision, requirement, lock, profile, test, evidence, exception, and toolchain traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Create a Python workspace

1. Assign one stable `workspace_id`.
2. create an isolated source directory.
3. resolve the applicable development profile.
4. create or validate `pyproject.toml`.
5. declare compatible Python.
6. create or validate `uv.lock`.
7. synchronize the workspace-local environment.
8. allocate service, secret, network, port, data, and resource namespaces separately.
9. run the workspace validation set.
10. register the workspace and toolchain evidence when required.

The command-oriented recipe owns exact creation commands.

### 6.2 Synchronize an existing workspace

A reproducible validation sequence begins with:

`bash
uv sync --frozen
`

After synchronization, project commands run inside the synchronized workspace context, for example:

`bash
uv run --frozen <project-command>
`

The command placeholder is resolved by the project or validation contract.

The sequence does not refresh dependency resolution.

### 6.3 Add or remove a dependency

1. Open an explicit dependency-change task.
2. edit `pyproject.toml`.
3. refresh `uv.lock` intentionally.
4. inspect the resolution difference.
5. evaluate affected platforms and profiles.
6. evaluate package source, provenance, licensing, vulnerability, and build impact when applicable.
7. synchronize without frozen mode only as part of the explicit change operation.
8. return to frozen synchronization for validation.
9. run affected tests.
10. commit the declaration and lockfile in the same coherent change.

### 6.4 Upgrade dependencies

1. Declare the intended upgrade scope.
2. identify direct and transitive candidates.
3. refresh resolution explicitly.
4. reject unexplained substitutions, source changes, or incompatible platform changes.
5. run unit, integration, component, profile, security, lifecycle, and build tests applicable to the change.
6. record impact and evidence.
7. retain a recoverable predecessor in source control.
8. merge only after the required validation result.

### 6.5 Recreate a workspace environment

1. Stop processes using the workspace environment.
2. preserve project source, `pyproject.toml`, and `uv.lock`.
3. remove only the workspace `.venv`.
4. retain or clear the shared cache independently.
5. verify compatible Python.
6. run frozen synchronization.
7. run environment and project validation.
8. confirm that other workspaces remain unchanged.

### 6.6 Run parallel branches

1. Assign distinct workspace identities.
2. create distinct source directories and `.venv` paths.
3. allocate distinct service names, networks, ports, volumes, databases, schemas, queues, secrets, temporary paths, and logs.
4. synchronize each workspace from its own lockfile.
5. start each workspace through its own profile context.
6. verify simultaneous operation.
7. stop or remove one workspace without affecting the other.

### 6.7 Offline synchronization

1. resolve the committed project and lockfile.
2. verify that the required Python interpreter is locally available.
3. verify that required package material is locally cached or available through an approved offline source.
4. run frozen synchronization without silently reaching an undeclared source.
5. record unavailable artifacts as a blocked result.
6. preserve existing valid environments.
7. reacquire or import missing package material through an approved procedure.

### 6.8 Cleanup

Workspace cleanup distinguishes:

- `.venv`;
- UV download cache;
- source tree;
- temporary build outputs;
- service containers;
- volumes;
- databases and schemas;
- queues;
- ports;
- secrets;
- certificates;
- logs.

Removing one class does not imply removal of the others.

The cleanup procedure identifies retained evidence and backup obligations before deleting authoritative or non-regenerable state.

### 6.9 Restore

1. restore the source revision.
2. restore `pyproject.toml` and `uv.lock`.
3. resolve the declared compatible Python.
4. restore separately managed secrets and service state through their own procedures.
5. perform frozen synchronization.
6. run project, service, and profile validation.
7. compare the restored environment and behavior with the expected evidence.
8. record the restore result.

## 7. Failure and Degradation

### 7.1 Project and lock mismatch

When project declarations and the lockfile disagree, frozen synchronization fails.

The workspace remains unchanged or returns a bounded failure result.

The validation path does not repair the lockfile automatically.

### 7.2 Missing Python interpreter

When no compatible interpreter is available:

- environment creation remains blocked;
- existing unrelated workspaces remain usable;
- service and data state remain unchanged;
- the profile's interpreter provisioning procedure becomes applicable.

### 7.3 Missing package material

When required package material cannot be obtained:

- synchronization remains blocked;
- the existing valid `.venv` can remain usable according to project policy;
- no alternate unapproved package source is selected silently;
- offline acquisition follows a bounded artifact or mirror procedure.

### 7.4 Shared cache loss or corruption

Cache loss does not alter `pyproject.toml`, `uv.lock`, or another workspace's `.venv`.

Affected packages are reacquired from approved sources when connectivity or offline media permits.

A shared cache failure does not justify sharing an installed environment.

### 7.5 Workspace environment corruption

A corrupted `.venv` is disposable installed state.

Recovery removes only that workspace environment and recreates it from committed metadata.

Other workspaces remain unchanged.

### 7.6 Dependency upgrade regression

A failing test, unsupported platform, provenance concern, vulnerability, licensing issue, or incompatible transitive change blocks the dependency-change claim.

The predecessor project and lock state remain available through source control.

### 7.7 Resource pressure

Profile resource controls can:

- delay environment creation;
- reduce concurrent test workers;
- stop optional heavy services;
- reject new build tasks;
- preserve active source and lockfile state;
- retain explicit queue and failure outcomes.

Resource pressure does not permit global dependency installation or environment sharing.

### 7.8 Network loss

Existing synchronized workspaces continue to run.

New synchronization succeeds only when all required interpreter and package material is locally available.

Loss of network access does not alter dependency authority or permit an undeclared package source.

### 7.9 Service collision

A database, port, queue, volume, secret, or process collision is a workspace-isolation failure even when the Python `.venv` is distinct.

The affected workspaces stop or enter degraded state until their non-Python namespaces are corrected.

### 7.10 Build-farm failure

An interrupted or failed build preserves source, project metadata, lockfile identity, toolchain identity, diagnostics, and evidence.

Incomplete build output remains inactive.

A new clean or controlled worker can reproduce the task from the same declared inputs.

## 8. Cross-System Interactions

| Counterparty | Interaction | Boundary |
| --- | --- | --- |
| Development profile | Selects toolchain adoption, interpreter provisioning, resource limits, storage, network, cache, service, and offline realization. | The profile cannot weaken one-environment-per-workspace isolation. |
| Source control | Stores source, `pyproject.toml`, `uv.lock`, review history, and dependency-change evidence. | Source control does not contain the installed `.venv` or normal secrets. |
| Approved package source or mirror | Supplies package artifacts used by UV. | Source availability does not change the committed dependency graph. |
| Shared UV cache | Reuses content-addressed downloads. | It is not a mutable installed environment. |
| Python interpreter provider | Supplies a compatible interpreter. | Interpreter availability does not resolve project dependencies by itself. |
| Workspace services | Provide databases, queues, search, storage, and integration dependencies. | They use separate workspace namespaces outside UV environment isolation. |
| Resource Governor or profile controls | Bound CPU, memory, processes, I/O, queues, concurrency, and heavy jobs. | Resource controls do not change dependency declarations. |
| Build farm | Reproduces validation and build outputs from fixed inputs. | Build workers do not receive ordinary release-signing authority. |
| Artifact lifecycle | Verifies, publishes, activates, rolls back, or revokes build outputs. | A synchronized `.venv` is not a production activation mechanism. |
| Audit and evidence | Records required dependency, build, validation, upgrade, and restore evidence. | Evidence does not become dependency authority. |

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed rule |
| --- | --- |
| `DEC-DEV-001` | Native Linux development is first class, UV is the Python dependency manager, and each workspace owns one mutable installed environment. |
| `DEC-DEV-002` | Parallel branches and applications use distinct workspace identities and isolated mutable resources. |
| `DEC-LIFE-001` | Build and release artifacts follow explicit verification, publication, activation, rollback, and evidence. |
| `DEC-AUTH-001` | Private sources, dependency changes, build publication, signing, and activation use explicit bounded authority. |
| `DEC-IDENT-001` | Workspace, project, Python, package source, artifact, worker, publisher, signer, and environment identities remain distinct. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- one machine needs only one Python virtual environment;
- one repository needs only one mutable environment across branches;
- a shared cache is equivalent to a shared `.venv`;
- an activated shell proves the correct workspace environment;
- global package installation is a reproducible development method;
- `pyproject.toml` alone fixes transitive dependencies;
- `uv.lock` alone declares project intent;
- frozen validation can update dependency resolution;
- deleting `.venv` deletes project or service data;
- deleting a workspace source tree safely deletes its databases, volumes, secrets, or queues;
- UV isolates host ports or service processes;
- WSL and native Linux use identical path and process realization;
- a developer profile implies production activation authority;
- build success implies signing or publication authority;
- network access is required for an already synchronized environment;
- the newest available package is the intended compatible package;
- an alternate index can be selected without explicit authority;
- a lockfile change without impact review is self-justifying;
- ordinary Markdown requires dependency-artifact content hashing.

A new implementation-affecting Python toolchain choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

| Validation group | Required tests |
| --- | --- |
| Python workspace isolation | `TEST-PROF-011`, `TEST-PROF-012` |
| Profile ownership and boundaries | `TEST-PROF-001`, `TEST-PROF-004`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-009`, `TEST-PROF-013` |
| Resource and operational isolation | `TEST-OPS-003`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-006`, `TEST-OPS-008`, `TEST-OPS-009`, `TEST-OPS-010` |
| Security and supply chain | `TEST-SEC-008`, `TEST-SEC-009`, `TEST-SEC-012`, `TEST-SEC-015` |
| Artifact and release behavior | `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-009`, `TEST-LIFE-011`, `TEST-LIFE-015` |
| Portability and recovery | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-005`, `TEST-EXIT-008` |
| Documentation alignment | `TEST-DOC-VAL-003`, `TEST-DOC-VAL-005`, `TEST-DOC-VAL-006`, `TEST-DOC-VAL-007`, `TEST-DOC-VAL-008`, `TEST-DOC-VAL-009`, `TEST-DOC-VAL-010`, `TEST-DOC-VAL-016`, `TEST-DOC-VAL-020` |

Repository and workspace validation additionally confirms:

1. every applicable Python project has `pyproject.toml`;
2. every applicable Python project has `uv.lock`;
3. the project declares compatible Python;
4. the workspace has its own `.venv` or profile-declared equivalent workspace-local path;
5. no two active workspaces resolve to the same mutable environment path;
6. frozen synchronization succeeds without modifying project metadata or the lockfile;
7. the shared cache path does not contain workspace-installed mutable state;
8. ordinary project execution does not depend on globally installed application packages;
9. deleting and recreating one `.venv` does not change another workspace;
10. parallel branches use collision-free service, port, data, secret, and process namespaces;
11. dependency upgrades include lockfile change, impact analysis, and applicable test evidence;
12. build-farm validation records source, lock, Python, UV, platform, and test identity;
13. backup and restore preserve project and lock identity and reconstruct the environment;
14. external package sources and private indexes use scoped credentials without committing secrets;
15. profile-specific realization remains profile scoped;
16. every active claim has current traceability and evidence;
17. no unresolved authority marker exists;
18. all active prose is in English.

A failed required check blocks the affected workspace, build, release, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Two branches of one application

A developer creates:

`text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
`

Each directory has its own:

`text
pyproject.toml
uv.lock
.venv
`

They can share the UV download cache.

Their databases, ports, service projects, volumes, queues, secrets, and logs use their separate workspace identities.

### 11.2 Frozen validation

A clean workspace checks out a source revision and runs:

`bash
uv sync --frozen
uv run --frozen pytest
`

A mismatch between `pyproject.toml` and `uv.lock` causes validation failure rather than an automatic lock refresh.

### 11.3 Explicit dependency upgrade

A maintainer opens a dependency-upgrade change.

The maintainer edits the declaration, refreshes the lockfile intentionally, reviews transitive changes, runs affected tests, and submits both files with impact evidence.

The ordinary conformance job then returns to frozen synchronization.

### 11.4 Recreating one environment

A local `.venv` becomes inconsistent.

The developer stops that workspace, removes only its `.venv`, and runs frozen synchronization again.

Another branch's `.venv`, database, queue, and services remain unchanged.

### 11.5 Shared cache

Linux and WSL workspaces use a profile-approved shared cache location.

Both retrieve the same immutable package material when compatible. Each still installs into its own workspace-local environment.

### 11.6 Offline work

A developer disconnects from the network after synchronizing the workspace and obtaining required service artifacts.

Project commands and tests continue locally.

A new missing package remains blocked until it is obtained through an approved cache, mirror, or offline procedure.

### 11.7 Build farm

A build worker receives a fixed source revision, committed lockfile, declared Python version, and pinned UV toolchain.

It creates an isolated environment, runs frozen synchronization and tests, produces build evidence, and discards the mutable worker environment after completion.

Release signing and production activation occur through separate authorities.

### 11.8 UV and services

A Python workspace has a correctly isolated `.venv` but reuses another workspace's PostgreSQL database and Redis namespace.

The Python dependency check passes, but the development-isolation claim fails because mutable service state is shared.
