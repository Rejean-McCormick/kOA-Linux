<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-017",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "profile:developer_linux_workstation",
    "profile:developer_windows_wsl"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/operating_modes",
    "contracts/system.contract.json#/data_authority_and_ownership",
    "contracts/system.contract.json#/resource_governance",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "schemas/developer-workspace.schema.json",
    "contracts/artifact-contracts/developer-workspace.schema.json",
    "contracts/artifact-contracts/workspace-port-allocation.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-CONF-DEV-001",
    "REQ-CONF-DEV-002",
    "REQ-CONF-DEV-003",
    "REQ-CONF-DEV-004",
    "REQ-CONF-DEV-005",
    "REQ-CONF-DEV-006",
    "REQ-CONF-DEV-007",
    "REQ-CONF-DEV-008",
    "REQ-CONF-DEV-009",
    "REQ-CONF-DEV-010",
    "REQ-CONF-DEV-011",
    "REQ-CONF-DEV-012",
    "REQ-CONF-DEV-013",
    "REQ-CONF-DEV-014",
    "REQ-CONF-DEV-015",
    "REQ-CONF-DEV-016",
    "REQ-CONF-DEV-017",
    "REQ-CONF-DEV-018",
    "REQ-CONF-DEV-019",
    "REQ-CONF-DEV-020",
    "REQ-CONF-DEV-021",
    "REQ-CONF-DEV-022",
    "REQ-CONF-DEV-023",
    "REQ-CONF-DEV-024",
    "REQ-CONF-DEV-025",
    "REQ-CONF-DEV-026",
    "REQ-CONF-DEV-027",
    "REQ-CONF-DEV-028",
    "REQ-CONF-DEV-029",
    "REQ-CONF-DEV-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-005",
    "LOCK-DOC-006",
    "LOCK-DOC-008",
    "LOCK-DOC-009",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-DOC-020",
    "LOCK-DOC-021",
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
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONF-000",
    "DOC-CONF-001",
    "DOC-CONF-002",
    "DOC-CONF-003",
    "DOC-CONF-004",
    "DOC-CONF-005",
    "DOC-CONF-006",
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
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003",
    "DOC-PROFILE-005",
    "DOC-PROFILE-006",
    "DOC-COMP-RG-001",
    "DOC-LIFE-000",
    "DOC-SEC-002"
  ],
  "tags": [
    "conformance",
    "development",
    "developer-profile",
    "linux-workstation",
    "windows-wsl",
    "workspace-identity",
    "uv",
    "virtual-environment",
    "isolation",
    "parallel-workspaces",
    "ports",
    "networks",
    "databases",
    "secrets",
    "resources",
    "reproducibility",
    "release-transition"
  ]
}
KOA:DOC-META:END -->

# Development Profile Conformance

## 1. Purpose

This document defines conformance evaluation for the two kOA development primary profiles:

```text
developer_linux_workstation
developer_windows_wsl
```

Development-profile conformance proves that a workstation can host reproducible, isolated, concurrently runnable development workspaces without confusing mutable development state with release artifacts or production authority.

The evaluation has three related subjects:

```text
developer workstation profile
    → workspace contract
        → executed workspace evidence
```

The workstation claim proves that the selected primary profile and its host boundary are correctly implemented.

The workspace claim proves that one workspace has a stable identity, isolated dependencies, namespaced services and state, bounded resources, reproducible inputs, and an independent lifecycle.

The parallel-execution evidence proves that multiple branches or applications can operate simultaneously without collisions or implicit mutable sharing.

A passing development-profile claim does not prove:

- release conformance;
- production readiness;
- sovereign-node conformance;
- high-assurance conformance;
- offline production conformance;
- component business correctness beyond the tests executed;
- publication or artifact activation.

The model preserves these distinctions:

```text
development convenience
is not architectural authority

shared download cache
is not shared installed state

container readiness
is not application authorization

local success
is not release evidence
```

## 2. Scope

This document applies to claims for:

- `developer_linux_workstation`;
- `developer_windows_wsl`;
- individual developer workspaces;
- branch checkouts;
- Git worktrees;
- task workspaces;
- Python dependency environments;
- service containers or equivalent workspace namespaces;
- local databases;
- local queues;
- workspace networks;
- host-port allocations;
- local sockets;
- local certificates;
- secret references;
- temporary and log state;
- resource budgets;
- concurrent workspace execution;
- clean-environment rebuild;
- build and test execution;
- transition from development to immutable artifacts.

It governs:

- claim scope;
- profile distinction;
- workspace identity;
- contract validation;
- UV and Python environment rules;
- mutable-state isolation;
- database and secret isolation;
- ports, networks, and sockets;
- resource governance;
- reproducibility;
- lifecycle and teardown;
- Windows WSL boundary evidence;
- parallel-execution testing;
- evidence;
- result calculation;
- reevaluation.

It does not mandate one container engine, Linux distribution, Windows edition, WSL distribution, init system, desktop environment, database engine, editor, integrated development environment, or shell.

Those choices remain owned by active profile contracts, component contracts, toolchain contracts, or non-normative recipes.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/operating_modes
contracts/system.contract.json#/data_authority_and_ownership
contracts/system.contract.json#/resource_governance
generated/profile-catalog.json
contracts/profiles/developer-linux-workstation.profile.json
contracts/profiles/developer-windows-wsl.profile.json
schemas/developer-workspace.schema.json
contracts/artifact-contracts/developer-workspace.schema.json
contracts/artifact-contracts/workspace-port-allocation.schema.json
contracts/artifact-contracts/resource-envelope.schema.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| Profile index and profile contracts | Primary-profile identity, inheritance, capabilities, host boundary, hardware, operating modes, and conditional behavior |
| Developer-workspace schema | Workspace identity, isolation, resource, reproducibility, lifecycle, and validation structure |
| Workspace-port-allocation contract | Atomic host-port reservation, activation, release, ownership, protocol, and bind scope |
| Resource-envelope contract | Resource limits, queues, concurrency, pressure behavior, and recovery |
| System data-ownership model | Component source-data authority and prohibited direct writes |
| System resource-governance model | Separation of Resource Governor from Governance Policy Runtime |
| `requirements.registry.json` | Normative development and conformance requirements |
| `locks.registry.json` | Development isolation, profile scope, implementation scope, data ownership, and lifecycle invariants |
| `traceability.registry.json` | Profile, workspace, requirement, test, evidence, decision, and exception links |
| `test-catalog.registry.json` | Required profile, workspace, parallel-execution, reproducibility, and teardown tests |
| `evidence.registry.json` | Evidence identity, subject, environment, result, verification, access, and retention |
| `exceptions.registry.json` | Approved bounded deviations and compensating controls |

This document explains evaluation and does not own tool versions, workspace instances, port allocations, or profile membership.

## 4. Model and Responsibilities

### 4.1 Claim hierarchy

The claim hierarchy is:

```text
development_profile_claim
    → host_boundary_claim
    → workspace_contract_claim
    → workspace_runtime_claim
    → parallel_execution_claim
    → reproducibility_claim
    → teardown_claim
```

A profile claim can include several workspace claims. Every mandatory subordinate claim must pass before the profile claim passes.

### 4.2 Profile distinction

The profiles remain distinct:

| Profile | Host boundary |
| --- | --- |
| `developer_linux_workstation` | Native Linux development workstation |
| `developer_windows_wsl` | Windows host with an explicitly identified WSL Linux environment |

The profiles can share workspace semantics without sharing every implementation check.

Native-Linux evidence and WSL evidence remain separately attributable.

### 4.3 Claim scope

A profile claim records:

```text
claim_id
profile_id
profile_contract_version
host operating-system identity
Linux environment identity
architecture
hardware envelope
container or namespace implementation
filesystem roots
network exposure model
included workspace_ids
evaluator
validator versions
test refs
evidence refs
exceptions
result
validity
```

A workspace claim records the exact source revision and workspace contract version.

### 4.4 Workspace identity

A workspace identity derives from:

```text
component + branch_or_purpose + unique_suffix
```

Examples:

```text
konnaxion-main-a31f
konnaxion-feature-voting-92cd
orgo-main-b114
```

The `workspace_id` prefixes or namespaces mutable collision domains.

The display name can change. The stable identity and namespace relationship remain testable.

### 4.5 Source-control context

The workspace declares:

- repository identity;
- workspace kind;
- ref name;
- optional commit identity;
- repository-relative root;
- clean-state requirement for validation.

A branch, worktree, or task workspace remains development state rather than a release artifact.

### 4.6 Dependency environment

Every workspace owns one mutable dependency environment.

For Python, the canonical model is:

```text
UV
pyproject.toml
uv.lock
.python-version
.venv
uv sync --frozen
```

A content-addressed UV download cache can be shared. Installed packages and the mutable `.venv` cannot.

Lockfile refresh is an explicit development action rather than a validation side effect.

### 4.7 Service and state isolation

Mutable services use workspace-prefixed identities.

Namespaced state includes at least:

```text
dependency_environment
containers
networks
volumes
database_names
database_users
database_schemas
unix_sockets
temporary_directories
log_directories
pid_files
service_names
secret_names
local_certificates
development_queues
host_ports
```

The implementation can use rootless containers, workspace namespaces, or a profile-approved equivalent.

The isolation claim concerns behavior, not product branding.

### 4.8 Database isolation

Every workspace uses workspace-scoped database identities.

Permitted profile-owned models can include:

- separate database;
- separate schema;
- separate instance;
- a declared combination.

Mutable database sharing across workspaces is not part of the passing baseline.

Component data ownership remains active inside development. One component does not write directly to another component's authoritative source records.

### 4.9 Secret isolation

Workspace contracts contain secret references rather than values.

Secret evidence verifies:

- workspace namespace;
- reference resolution;
- source or provider identity;
- non-reuse across workspaces unless an explicit safe shared credential class exists;
- generated local-certificate namespace;
- cleanup or revocation at teardown;
- absence from ordinary logs and reports.

Production credentials are not a development conformance prerequisite.

### 4.10 Ports, networks, and sockets

The endpoint model separates:

```text
workspace-internal endpoints
host-exposed endpoints
workspace-local interprocess communication
```

Fixed internal ports are compatible with isolated networks.

Host ports are allocated through a workspace-scoped allocation registry.

Workspace networks are isolated and prefixed. Cross-workspace connectivity is off by default.

Socket and runtime paths are workspace-scoped and recoverable after stale-state detection.

### 4.11 Parallel execution

The minimum behavioral proof runs at least two workspaces concurrently.

The pair can represent:

- two branches of one component;
- two applications;
- one main workspace and one migration workspace;
- one ordinary workspace and one test workspace.

The test exercises the actual collision domains rather than checking names statically only.

### 4.12 Resource governance

Every workspace declares bounded:

- CPU;
- memory;
- process count;
- I/O priority;
- pending queue depth;
- heavy-job concurrency.

Heavy services such as search engines, workbenches, model runtimes, SenTient, or intensive UCKK jobs are task-activated where included.

Resource Governor admission remains separate from business and governance authority.

### 4.13 Reproducibility

Reproducibility evidence includes:

- exact runtime versions;
- versioned manifests;
- versioned lockfiles;
- frozen synchronization;
- clean rebuild;
- validation commands;
- dependency-upgrade impact;
- exact source revision;
- validator and tool versions.

A shared cache can accelerate the rebuild without becoming an installed environment.

### 4.14 Windows WSL boundary

The WSL claim records both sides of the boundary.

The Windows-host evidence can include:

- host identity and supported version class;
- selected WSL environment;
- host-to-guest integration;
- host-port exposure;
- filesystem boundary;
- lifecycle start and stop behavior;
- time, DNS, and name-resolution behavior;
- credential and secret boundary;
- editor or tool integration used by the claim.

The Linux-environment evidence executes the ordinary workspace contract inside the selected WSL environment.

A result cannot hide which side supplied a service, filesystem, port, credential, or process.

### 4.15 Workspace lifecycle

Workspace lifecycle states can include:

```text
declared
validated
active
suspended
teardown_pending
retired
failed
```

Creation, activation, teardown, and removal are explicit.

Removing one workspace cannot alter another workspace. Shared content-addressed download caches can remain.

Orphan cleanup covers ports, containers, networks, volumes, sockets, processes, temporary files, logs, database identities, and local credentials.

### 4.16 Development-to-release boundary

Development output becomes a release candidate through:

```text
clean source revision
    → declared build
    → tests
    → provenance
    → immutable artifact
    → publication
    → Release Set evaluation
```

The mutable workspace does not cross this boundary as an artifact.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-DEV-001,REQ-CONF-DEV-002,REQ-CONF-DEV-003,REQ-CONF-DEV-004,REQ-CONF-DEV-005,REQ-CONF-DEV-006,REQ-CONF-DEV-007,REQ-CONF-DEV-008,REQ-CONF-DEV-009,REQ-CONF-DEV-010,REQ-CONF-DEV-011,REQ-CONF-DEV-012,REQ-CONF-DEV-013,REQ-CONF-DEV-014,REQ-CONF-DEV-015,REQ-CONF-DEV-016,REQ-CONF-DEV-017,REQ-CONF-DEV-018,REQ-CONF-DEV-019,REQ-CONF-DEV-020,REQ-CONF-DEV-021,REQ-CONF-DEV-022,REQ-CONF-DEV-023,REQ-CONF-DEV-024,REQ-CONF-DEV-025,REQ-CONF-DEV-026,REQ-CONF-DEV-027,REQ-CONF-DEV-028,REQ-CONF-DEV-029,REQ-CONF-DEV-030 -->
- **REQ-CONF-DEV-001 — SHALL:** Every development-profile conformance claim identify the exact primary profile, profile-contract version, host operating-system context, Linux environment context where applicable, architecture, evaluator, validator versions, evaluation interval, included workspaces, excluded capabilities, exception set, evidence set, and result.
- **REQ-CONF-DEV-002 — SHALL:** The developer_linux_workstation and developer_windows_wsl profiles be evaluated as distinct primary profiles with explicit applicability, boundaries, inherited requirements, and evidence.
- **REQ-CONF-DEV-003 — SHALL NOT:** Evidence from native Linux be generalized silently to Windows WSL, or evidence from Windows WSL be generalized silently to native Linux.
- **REQ-CONF-DEV-004 — SHALL:** Every claimed development workspace have a stable workspace_id derived from component, branch_or_purpose, and unique_suffix, and use that identity as its namespace prefix.
- **REQ-CONF-DEV-005 — SHALL:** Every workspace claim validate its active developer-workspace contract against the canonical schema and semantic validators before activation.
- **REQ-CONF-DEV-006 — SHALL:** Every Python workspace use UV, pyproject.toml, uv.lock, a declared Python version, one workspace-local .venv, and uv sync --frozen for reproducible validation.
- **REQ-CONF-DEV-007 — SHALL NOT:** A Python development-profile claim permit global application dependency installation, a shared mutable .venv, an undeclared mutable dependency environment, or implicit lockfile refresh during validation.
- **REQ-CONF-DEV-008 — SHALL:** A shared content-addressed download cache remain distinguishable from each workspace's installed dependency environment and be safe to retain when a workspace is removed.
- **REQ-CONF-DEV-009 — SHALL:** Every workspace namespace its mutable services, containers, networks, volumes, databases, database users, schemas, sockets, temporary directories, logs, process identifiers, service names, secrets, local certificates, queues, and allocated host ports.
- **REQ-CONF-DEV-010 — SHALL NOT:** Two active workspaces share mutable dependency state, service identity, database identity, secret values, sockets, process names, temporary state, or another mutable collision domain implicitly.
- **REQ-CONF-DEV-011 — SHALL:** Development-profile evidence demonstrate that at least two applications or branches can run concurrently without collisions in host ports, process names, service names, databases, users, schemas, networks, volumes, secrets, sockets, temporary files, and logs.
- **REQ-CONF-DEV-012 — SHALL:** Workspace-internal service ports be permitted to remain fixed inside isolated logical networks while host ports use the workspace-scoped allocation registry.
- **REQ-CONF-DEV-013 — SHALL NOT:** Host-port collisions, unregistered host-port assumptions, shared socket paths, or default cross-workspace network connectivity satisfy the parallel-workspace claim.
- **REQ-CONF-DEV-014 — SHALL:** Every workspace use an isolated logical network with workspace-prefixed identity and deny cross-workspace connectivity by default.
- **REQ-CONF-DEV-015 — SHALL:** Any cross-workspace connection be explicit, bounded, attributable, revocable, tested, and represented separately from the default isolation claim.
- **REQ-CONF-DEV-016 — SHALL:** Every workspace use workspace-scoped database identities and prohibit cross-workspace mutable database sharing and direct cross-component authoritative writes.
- **REQ-CONF-DEV-017 — SHALL:** Every workspace use a workspace-scoped secret namespace, store references rather than embedded secret values in its contract, prohibit implicit cross-workspace secret reuse, and namespace generated local certificates.
- **REQ-CONF-DEV-018 — SHALL NOT:** Production credentials, production trust roots, production mutable data, production privileged control paths, or unrestricted protected data be required for a development-profile conformance test.
- **REQ-CONF-DEV-019 — SHALL:** Every workspace declare and validate bounded CPU, memory, process, I/O, queue, and heavy-job limits under the Resource Governor model.
- **REQ-CONF-DEV-020 — SHALL:** Heavy development services and intensive jobs be explicitly task-activated and remain bounded by the workspace resource budget.
- **REQ-CONF-DEV-021 — SHALL NOT:** Resource availability, container readiness, network reachability, or host privilege substitute for component authorization, data ownership, or governance decisions.
- **REQ-CONF-DEV-022 — SHALL:** Reproducibility evidence cover declared runtime versions, versioned project manifests, versioned lockfiles, frozen dependency synchronization, clean-environment rebuild, dependency-upgrade impact validation, and exact validation commands.
- **REQ-CONF-DEV-023 — SHALL:** Repository-dependent validation execute from a clean repository state and identify undeclared local files, generated outputs, modified lockfiles, and uncommitted configuration that could affect results.
- **REQ-CONF-DEV-024 — SHALL:** The developer_windows_wsl claim identify and test the Windows host boundary, selected WSL distribution and version, Linux workspace location, filesystem boundary, network and host-port exposure, service lifecycle, time and name-resolution assumptions, and host integration used by the claim.
- **REQ-CONF-DEV-025 — SHALL NOT:** The Windows host, WSL distribution, container technology, init system, filesystem path, networking mode, or desktop integration become a universal development requirement unless the active profile contract owns it.
- **REQ-CONF-DEV-026 — SHALL:** Workspace creation, activation, suspension where supported, teardown, orphan cleanup, and removal be explicit, independently verifiable, and unable to remove or mutate another workspace.
- **REQ-CONF-DEV-027 — SHALL:** A development workspace produce release candidates only through declared build, test, provenance, artifact-publication, and release-transition contracts using immutable outputs.
- **REQ-CONF-DEV-028 — SHALL NOT:** Mutable workspace state, a local .venv, a running development container, a branch checkout, an unpinned tag, a local database, or a successful developer test be treated as a published artifact or release claim.
- **REQ-CONF-DEV-029 — SHALL:** Development-profile reports expose profile identity, workspace identities, pass, fail, or blocked result, failed and blocked checks, collisions tested, validator and tool versions, evidence references, exceptions, timestamps, and remediation without exposing secrets or unrestricted protected data.
- **REQ-CONF-DEV-030 — SHALL:** Development-profile evaluation produce deterministic mandatory results for identical profile contracts, workspace contracts, repository state, runtime and tool versions, validators, tests, evidence, exceptions, and evaluation scope.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Profile-claim preparation

Preparation:

1. identify the primary profile;
2. resolve the active profile contract and inheritance;
3. identify host, Linux environment, architecture, and hardware;
4. identify the implementation choices used by the claim;
5. identify included workspaces;
6. load applicable requirements and locks;
7. resolve validators, tests, evidence, and exceptions;
8. block the claim when profile identity or ownership is unresolved.

### 6.2 Host-boundary validation

For native Linux:

1. identify the Linux host and architecture;
2. validate profile capabilities and hardware envelope;
3. validate service, storage, network, and resource implementations;
4. record implementation-specific evidence without making it global.

For WSL:

1. identify the Windows host;
2. identify the selected WSL environment;
3. map host and Linux responsibilities;
4. test filesystem, process, network, port, secret, time, and lifecycle boundaries;
5. record which side produced each result.

### 6.3 Workspace-contract validation

The evaluator:

1. validates the workspace object against the developer-workspace schema;
2. verifies required decisions, requirements, and locks;
3. verifies workspace-id derivation;
4. verifies source-control context;
5. verifies dependency, service, state, database, secret, port, network, parallel, resource, reproducibility, lifecycle, and validation sections;
6. runs semantic reference checks;
7. records pass, fail, or blocked.

### 6.4 Dependency-environment validation

For a Python workspace:

1. verify `pyproject.toml`;
2. verify `uv.lock`;
3. verify `.python-version`;
4. verify workspace-local `.venv`;
5. remove or isolate the installed environment for the clean test;
6. run `uv sync --frozen`;
7. verify that no lockfile refresh occurred;
8. execute declared validation commands;
9. compare installed state to the declared lock;
10. record evidence.

### 6.5 Workspace activation

Activation:

1. verify contract pass;
2. reserve resource budget;
3. allocate host ports atomically;
4. create workspace network and runtime paths;
5. resolve secret references;
6. create database identities and state;
7. start declared services;
8. validate readiness and endpoint ownership;
9. mark the workspace active;
10. record activation evidence.

A partially initialized workspace remains inactive.

### 6.6 Parallel-workspace test

The evaluator:

1. selects two distinct workspace identities;
2. activates both from declared contracts;
3. starts overlapping service sets;
4. exercises internal ports and allocated host ports;
5. exercises databases, queues, sockets, secrets, volumes, temporary files, logs, and process names;
6. verifies no default cross-workspace network path;
7. performs concurrent component tests;
8. tears down one workspace;
9. verifies the other remains operational;
10. records collision evidence.

### 6.7 Data and secret test

The evaluator:

1. verifies database names and identities;
2. verifies component-owner boundaries;
3. attempts prohibited cross-workspace and cross-component mutations;
4. verifies denial;
5. verifies secret references and namespace;
6. verifies absence of values from contracts and ordinary logs;
7. verifies generated local-certificate identity;
8. records cleanup behavior.

### 6.8 Resource test

The evaluator:

1. loads the workspace budget;
2. validates limits and queue bounds;
3. starts ordinary workloads;
4. task-activates included heavy services;
5. applies bounded pressure;
6. verifies admission, throttling, queueing, or denial behavior;
7. verifies that another workspace remains protected;
8. records Resource Governor evidence.

### 6.9 Reproducibility test

Reproducibility testing:

1. records exact source revision;
2. verifies a clean repository;
3. rebuilds the dependency environment;
4. rebuilds generated development outputs required by the test;
5. executes declared validation commands;
6. repeats in another clean environment where required;
7. compares mandatory results;
8. records all tool versions and inputs.

### 6.10 Teardown test

Teardown:

1. stop workspace workloads;
2. release host ports;
3. remove workspace networks and sockets;
4. remove containers or namespace state;
5. remove temporary databases and identities according to the contract;
6. revoke or remove local secrets and certificates;
7. remove temporary and log state according to retention;
8. clean orphaned processes and identifiers;
9. retain only approved shared cache material;
10. verify another workspace remains unaffected.

### 6.11 Result calculation

The evaluator:

1. collects profile, host-boundary, workspace, parallel, reproducibility, resource, and teardown results;
2. verifies evidence scope and freshness;
3. verifies exceptions;
4. identifies failed checks;
5. identifies blocked checks;
6. calculates pass, fail, or blocked;
7. produces machine-readable and human-readable reports;
8. protects secrets through selective disclosure.

### 6.12 Reevaluation

Reevaluation occurs after material changes to:

- profile contract;
- WSL or Linux environment;
- architecture;
- workspace schema;
- dependency manager;
- runtime version;
- lockfile;
- container or namespace implementation;
- port allocator;
- network behavior;
- database model;
- resource policy;
- validator;
- test;
- evidence;
- exception.

Affected claims receive linked successors rather than silent extension.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `dev_conformance_profile_identity_missing` | Primary profile or contract version is absent | Claim is blocked | Resolve the active profile |
| `dev_conformance_profile_scope_mismatch` | Native Linux and WSL evidence are mixed without attribution | Claim is blocked | Separate the scopes |
| `dev_conformance_wsl_boundary_unresolved` | Windows and Linux responsibilities cannot be identified | WSL claim is blocked | Complete boundary evidence |
| `dev_conformance_workspace_contract_missing` | Workspace lacks its canonical contract | Workspace claim is blocked | Create and validate the contract |
| `dev_conformance_workspace_schema_failed` | Workspace object fails schema validation | Workspace claim fails | Correct the object |
| `dev_conformance_workspace_id_invalid` | Identity does not match component, purpose, and suffix | Workspace claim fails | Recreate the identity |
| `dev_conformance_dependency_environment_shared` | Mutable installed dependencies are shared | Workspace and profile claims fail | Create isolated environments |
| `dev_conformance_uv_contract_failed` | UV, files, `.venv`, or frozen synchronization rules fail | Python workspace claim fails | Restore the canonical environment |
| `dev_conformance_lockfile_changed_during_validation` | Validation refreshes the lockfile | Reproducibility claim fails | Perform explicit upgrade and retest |
| `dev_conformance_shared_cache_became_environment` | Shared cache contains or acts as shared installed state | Isolation claim fails | Restore content-addressed cache semantics |
| `dev_conformance_mutable_state_collision` | Workspaces share a mutable collision domain | Parallel claim fails | Namespace the resource |
| `dev_conformance_host_port_collision` | Host-port allocation conflicts | Affected activation fails | Reallocate atomically |
| `dev_conformance_port_unregistered` | Exposed host port lacks registry ownership | Workspace claim fails | Register and verify allocation |
| `dev_conformance_cross_workspace_connectivity` | Default network path exists between workspaces | Isolation claim fails | Close the path |
| `dev_conformance_socket_collision` | Workspace-local socket or runtime path collides | Parallel claim fails | Recreate namespaced paths |
| `dev_conformance_database_identity_shared` | Mutable database identity is shared implicitly | Isolation claim fails | Create workspace identities |
| `dev_conformance_cross_component_write` | Test proves direct write to another component's source records | Component and profile claims fail | Use the owner contract |
| `dev_conformance_secret_embedded` | Workspace contract, log, or report contains a secret value | Claim fails and material is protected | Rotate and remove the secret |
| `dev_conformance_secret_reused` | Secret is reused across workspaces without an explicit safe class | Isolation claim fails | Issue workspace-scoped credentials |
| `dev_conformance_production_authority_required` | Test depends on production identity, trust, data, or privilege | Claim is blocked or fails according to exposure | Replace with development fixtures |
| `dev_conformance_resource_budget_missing` | Workspace lacks a complete budget | Activation claim is blocked | Declare and validate limits |
| `dev_conformance_resource_isolation_failed` | One workspace displaces another beyond declared behavior | Profile claim fails | Repair enforcement |
| `dev_conformance_heavy_service_unbounded` | Heavy service starts without task activation or limit | Resource claim fails | Apply bounded activation |
| `dev_conformance_repository_dirty` | Undeclared repository state affects validation | Reproducibility claim fails | Clean and rerun |
| `dev_conformance_parallel_test_not_executed` | No concurrent behavioral test ran | Profile claim is blocked | Execute the test |
| `dev_conformance_teardown_incomplete` | Ports, services, processes, data, secrets, or sockets remain | Lifecycle claim fails | Complete orphan cleanup |
| `dev_conformance_cross_workspace_teardown_effect` | Removing one workspace changes another | Parallel and lifecycle claims fail | Restore independent lifecycle |
| `dev_conformance_false_release_claim` | Mutable workspace state is reported as a published artifact or release | Release-transition claim fails | Produce immutable artifacts |
| `dev_conformance_evidence_stale` | Evidence no longer matches profile, workspace, source, tools, or scope | Claim is blocked | Refresh evidence |
| `dev_conformance_result_nondeterministic` | Identical inputs produce different mandatory results | Automation claim fails | Repair evaluator determinism |

A failed workspace remains isolated from other valid workspaces. A failed heavy service does not invalidate unrelated lightweight workspace capabilities. A blocked release transition does not prevent ordinary local development.

## 8. Cross-Component Interactions

### 8.1 Profile owners

Profile owners define native-Linux and WSL applicability, host boundaries, capabilities, hardware, and conditional implementation rules.

The evaluator does not merge the two profiles.

### 8.2 Workspace tooling

Workspace tooling derives identities, validates contracts, creates namespaces, allocates resources, and performs cleanup.

It does not become the owner of component business data.

### 8.3 UV and language toolchains

UV owns the Python dependency workflow defined by the active toolchain contract.

Other language toolchains can use their own declared isolated environments without weakening the workspace-isolation model.

### 8.4 Resource Governor

Resource Governor enforces CPU, memory, I/O, process, queue, and heavy-job bounds.

It does not authorize component actions or governed disclosures.

### 8.5 Identity and secrets systems

Development identity and secret providers issue workspace-scoped references and local credentials.

They remain separate from production authority.

### 8.6 Database services

Database services provide workspace-scoped identities and component-owned logical stores.

A shared physical server can support several workspaces only while identities and mutable state remain isolated.

### 8.7 Port allocator and network runtime

The port allocator owns host-port reservations.

The network runtime implements isolated logical networks and explicit bounded links.

Neither endpoint reachability nor port ownership grants component authority.

### 8.8 Component owners

Components define development service behavior, schemas, migrations, tests, and data ownership.

Workspace isolation does not permit direct cross-component source writes.

### 8.9 Build and lifecycle systems

Build systems consume clean source and declared environments to produce immutable outputs.

Lifecycle systems verify, publish, activate, roll back, and repair artifacts. They do not activate `.venv` or workspace containers as release artifacts.

### 8.10 Evidence and conformance systems

Test runners and validators produce exact-scope evidence.

Audit and evidence systems store results with selective disclosure and without embedded secrets.

## 9. Decision Closure and Prohibited Assumptions

This document closes development-profile conformance as follows:

- native Linux and Windows WSL are distinct primary profiles;
- every workspace has a stable derived identity;
- every mutable dependency environment is workspace-local;
- every Python workspace uses UV and one `.venv`;
- a shared content-addressed cache is permitted but is not an installed environment;
- services, state, databases, secrets, ports, networks, and sockets are namespaced;
- two branches or applications run concurrently without collisions;
- fixed internal ports are allowed inside isolated networks;
- host ports use a workspace-scoped allocation registry;
- cross-workspace connectivity is off by default;
- database identities are workspace-scoped;
- direct cross-component writes remain prohibited;
- production authority is not a development prerequisite;
- resource limits are explicit;
- heavy services are task-activated;
- clean rebuild and frozen validation are evidenced;
- teardown is independent;
- WSL host and Linux boundaries remain explicit;
- development outputs cross into release only as immutable artifacts.

The following assumptions are prohibited:

- one `.venv` can be shared by several workspaces;
- an activated global Python environment proves workspace conformance;
- a shared cache is a shared environment;
- unique branch names prevent all collisions;
- fixed internal ports imply host-port collisions;
- WSL is identical to native Linux for every check;
- Windows-host services can be attributed to Linux silently;
- a container name alone proves isolation;
- a shared database administrator identity proves database separation;
- production credentials improve development conformance;
- resource availability authorizes a component action;
- rootless containers are mandatory for every platform;
- Podman, Docker, systemd, or another implementation is globally required;
- a successful local test proves release conformance;
- a running development container is an immutable artifact;
- cleanup of one workspace can remove shared mutable state from another;
- ordinary Markdown hashes determine development conformance.

A new global workspace identity rule, dependency-sharing rule, profile-merging rule, or mutable-state promotion path requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 30 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. native-Linux and WSL claims identify distinct profile contracts and evidence;
7. WSL tests identify the Windows host, selected Linux environment, filesystem, network, ports, lifecycle, time, name resolution, secrets, and host integration;
8. every workspace identity matches component, branch or purpose, and unique suffix;
9. every active workspace contract validates against the canonical schema;
10. Python tests verify UV, `pyproject.toml`, `uv.lock`, `.python-version`, one `.venv`, and `uv sync --frozen`;
11. tests reject global installation, shared mutable environments, and implicit lockfile refresh;
12. shared-cache tests prove that installed state remains workspace-local;
13. namespace tests cover dependencies, services, containers, networks, volumes, databases, users, schemas, sockets, temporary files, logs, process identifiers, service names, secrets, certificates, queues, and host ports;
14. parallel tests run at least two workspaces concurrently;
15. collision tests cover ports, processes, services, databases, users, schemas, networks, volumes, secrets, sockets, temporary files, and logs;
16. port tests permit fixed internal ports and reject host-port collisions or unregistered exposure;
17. network tests prove isolation and no default cross-workspace connectivity;
18. explicit-link tests verify scope, attribution, revocation, and teardown;
19. database tests prove workspace-scoped identity and reject cross-workspace sharing and cross-component writes;
20. secret tests prove references, namespace, non-reuse, certificate identity, cleanup, and absence from ordinary logs;
21. tests reject production credentials, mutable production data, production trust roots, and production privileged paths as prerequisites;
22. resource tests cover CPU, memory, processes, I/O, queues, heavy jobs, and cross-workspace protection;
23. reproducibility tests cover runtime versions, manifests, lockfiles, frozen synchronization, clean rebuild, upgrade impact, and validation commands;
24. repository tests identify undeclared local state;
25. lifecycle tests cover creation, activation, teardown, orphan cleanup, removal, and unaffected peer workspaces;
26. release-transition tests require immutable artifacts, provenance, publication, and Release Set evaluation;
27. evidence tests identify exact profile, workspace, source revision, tools, validators, time, environment, result, and scope;
28. exception tests validate approval, scope, expiry, controls, tests, and evidence;
29. result tests calculate exactly pass, fail, or blocked and expose all failed and blocked checks;
30. deterministic-evaluation tests compare identical inputs and mandatory results;
31. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
32. active prose is English;
33. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

```text
dev_conformance_profile_identity_missing
dev_conformance_profile_scope_mismatch
dev_conformance_wsl_boundary_unresolved
dev_conformance_workspace_contract_missing
dev_conformance_workspace_schema_failed
dev_conformance_workspace_id_invalid
dev_conformance_dependency_environment_shared
dev_conformance_uv_contract_failed
dev_conformance_lockfile_changed_during_validation
dev_conformance_shared_cache_became_environment
dev_conformance_mutable_state_collision
dev_conformance_host_port_collision
dev_conformance_port_unregistered
dev_conformance_cross_workspace_connectivity
dev_conformance_socket_collision
dev_conformance_database_identity_shared
dev_conformance_cross_component_write
dev_conformance_secret_embedded
dev_conformance_secret_reused
dev_conformance_production_authority_required
dev_conformance_resource_budget_missing
dev_conformance_resource_isolation_failed
dev_conformance_heavy_service_unbounded
dev_conformance_repository_dirty
dev_conformance_parallel_test_not_executed
dev_conformance_teardown_incomplete
dev_conformance_cross_workspace_teardown_effect
dev_conformance_false_release_claim
dev_conformance_evidence_stale
dev_conformance_result_nondeterministic
```

## 11. Non-Normative Examples

### 11.1 Native Linux parallel branches

Two Konnaxion workspaces use separate `.venv` directories, networks, databases, users, volumes, secrets, sockets, logs, and allocated host ports. Both run concurrently. Removing the feature workspace leaves the main workspace operational.

### 11.2 Windows WSL profile

A Windows host runs one declared WSL environment. Source, `.venv`, sockets, databases, and service state live inside the declared Linux workspace boundary. Host-exposed ports use the allocation registry. The report identifies which host integration and network mode were tested.

### 11.3 Shared UV cache

Two Python workspaces use the same content-addressed UV download cache. Each creates its own `.venv` from its own `uv.lock`. Deleting one `.venv` does not change the other workspace or the cache.

### 11.4 Failed isolation claim

Two branches use different container names but the same database user and schema. The static naming check passes, but the behavioral isolation test fails. The parallel-workspace claim fails.

### 11.5 Development-to-release transition

A clean workspace builds an immutable service package, produces provenance and test evidence, and publishes the package to the services channel. The workspace `.venv`, branch checkout, local database, and running development container remain outside the artifact and release claim.
