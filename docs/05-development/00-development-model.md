<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-DEV-000",
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
    "contracts/system.contract.json#/development_model",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-DEV-001",
    "DEC-DEV-MODEL-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-AI-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-DEV-MODEL-001",
    "REQ-DEV-MODEL-002",
    "REQ-DEV-MODEL-003",
    "REQ-DEV-MODEL-004",
    "REQ-DEV-MODEL-005",
    "REQ-DEV-MODEL-006",
    "REQ-DEV-MODEL-007",
    "REQ-DEV-MODEL-008",
    "REQ-DEV-MODEL-009",
    "REQ-DEV-MODEL-010",
    "REQ-DEV-MODEL-011",
    "REQ-DEV-MODEL-012",
    "REQ-DEV-MODEL-013",
    "REQ-DEV-MODEL-014",
    "REQ-DEV-MODEL-015",
    "REQ-DEV-MODEL-016",
    "REQ-DEV-MODEL-017",
    "REQ-DEV-MODEL-018",
    "REQ-DEV-MODEL-019",
    "REQ-DEV-MODEL-020",
    "REQ-DEV-MODEL-021",
    "REQ-DEV-MODEL-022",
    "REQ-DEV-MODEL-023",
    "REQ-DEV-MODEL-024",
    "REQ-DEV-MODEL-025",
    "REQ-DEV-MODEL-026",
    "REQ-DEV-MODEL-027",
    "REQ-DEV-MODEL-028",
    "REQ-DEV-MODEL-029",
    "REQ-DEV-MODEL-030",
    "REQ-DEV-MODEL-031",
    "REQ-DEV-MODEL-032",
    "REQ-DEV-MODEL-033",
    "REQ-DEV-MODEL-034",
    "REQ-DEV-MODEL-035",
    "REQ-DEV-MODEL-036",
    "REQ-DEV-MODEL-037",
    "REQ-DEV-MODEL-038",
    "REQ-DEV-MODEL-039",
    "REQ-DEV-MODEL-040"
  ],
  "lock_ids": [
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001"
  ],
  "tags": [
    "development-model",
    "workspace-isolation",
    "uv",
    "python-toolchain",
    "contracts-first",
    "reproducibility",
    "candidate-artifacts",
    "testing",
    "evidence",
    "ai-boundary",
    "build-release-separation"
  ]
}
KOA:DOC-META:END -->

# Development Model

## 1. Purpose

This document defines the common development model for kOA.

The development model turns canonical architecture, governance, profiles, component contracts, artifact rules, and release rules into a reproducible engineering workflow. It establishes how a developer prepares a workspace, changes a contract or implementation, runs components, manages dependencies, tests behavior, records evidence, produces candidate artifacts, and hands validated work to an authorized build and release path.

The model is designed to preserve these separations:

- canonical contract from implementation;
- workspace from host-global state;
- component ownership from shared infrastructure;
- local success from conformance;
- candidate artifact from release artifact;
- build from signing;
- signing from activation;
- native deterministic behavior from optional external AI;
- development workbench from runtime authority.

A development environment can be convenient without becoming an alternate architecture.

## 2. Scope

This document applies globally to:

- source-code workspaces;
- contract and schema workspaces;
- documentation workspaces;
- component development;
- local integration testing;
- profile testing;
- artifact construction;
- generated-content workflows;
- Python dependency and environment management;
- containers and local services;
- databases, queues, indexes, and caches used for development;
- external developer tools and approved external AI surfaces;
- optional SenTient workbenches;
- offline development;
- test evidence;
- candidate artifacts;
- change review and handoff to build and release processes.

This document applies to both `developer_linux_workstation` and `developer_windows_wsl`, while host, hardware, container-backend, path, privilege, and operating-system values remain owned by their profile contracts.

This document does not make a developer workstation a production node, release signer, build farm, control plane, sovereign node, or high-assurance environment.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Global development model | `contracts/system.contract.json#/development_model` |
| Developer profile facts | `contracts/profiles/developer-linux-workstation.profile.json` and `contracts/profiles/developer-windows-wsl.profile.json` |
| Production build environment | `contracts/profiles/build-farm.profile.json` |
| Python and UV toolchain facts | `contracts/toolchains/python-uv.toolchain.json` |
| Component identities and ownership | `generated/component-catalog.json` |
| Observable component behavior | `contracts/components/*.component.json` |
| Artifact identities and lifecycle | `contracts/artifact-classes.contract.json` |
| Release channels and Release Sets | `contracts/release-channels.contract.json` |
| External integrations and external AI boundaries | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Development and cross-file invariants | `generated/assertion-index.json` |
| Decision, requirement, implementation, test, and evidence links | `generated/traceability.json` |
| Test definitions | `generated/test-catalog.json` |
| Evidence records | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

Source code is authoritative for implementation behavior only within the boundaries of active contracts. It is not authoritative for architecture, policy, profile, requirement, or release facts that have canonical registry owners.

## 4. Development Units and Responsibilities

### 4.1 Workspace

A workspace is the smallest complete development isolation unit.

It contains or references:

- source repositories;
- canonical contracts and schemas required for the change;
- one active development profile;
- workspace configuration;
- dependency lock files;
- local environments;
- selected component services;
- test fixtures;
- generated outputs;
- candidate artifacts;
- test and evidence outputs.

A workspace has a stable identity. That identity appears in mutable infrastructure so parallel workspaces cannot collide or silently share state.

### 4.2 Repository and multi-repository workspace

A repository is a version-controlled source unit. A workspace can contain one repository or an explicitly declared set of repositories.

A multi-repository workspace records:

- repository identities;
- source revisions;
- intended compatibility set;
- canonical-contract source;
- generated-content relationships;
- test and artifact scope.

Repository proximity does not create a component boundary or shared authority.

### 4.3 Canonical contract layer

The canonical contract layer includes:

- decisions;
- requirements;
- locks;
- registries;
- schemas;
- component contracts;
- profile contracts;
- artifact contracts;
- integration contracts;
- traceability;
- test and evidence catalogs.

A semantic implementation change begins by identifying the affected canonical objects. Changes to observable ownership, interfaces, states, compatibility, profiles, offline behavior, security boundaries, artifact behavior, or releases receive contract treatment.

### 4.4 Implementation layer

The implementation layer contains executable source, packages, adapters, migrations, configuration generators, tests, and build definitions.

Implementation conforms to the active contract. An implementation can use a different internal design while preserving the observable contract and compatibility guarantees.

Internal code structure remains non-canonical unless another component or artifact requires that identity for interoperability.

### 4.5 Test layer

The test layer validates:

- pure implementation behavior;
- component contracts;
- cross-component interactions;
- profile composition;
- artifact and release behavior;
- security and privilege;
- offline continuity;
- migration;
- recovery;
- system conformance.

Tests are registered when they support normative requirements, locks, conformance claims, release gates, or evidence.

### 4.6 Artifact layer

Development produces candidate artifacts.

A candidate artifact can be:

- locally executed;
- development-signed where permitted;
- tested;
- inspected;
- exported to an authorized build environment;
- used as test input.

A candidate artifact is not an active release artifact merely because it is complete or passes local tests.

### 4.7 Build and release authorities

The build farm owns authorized production build claims where the active contracts assign that role.

Release-channel owners, signing authorities, approvers, Publication Gateway, kOA Node Agent, and other lifecycle components retain their distinct responsibilities.

The development workflow hands off validated source and candidate evidence. It does not absorb downstream authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-DEV-MODEL-001,REQ-DEV-MODEL-002,REQ-DEV-MODEL-003,REQ-DEV-MODEL-004,REQ-DEV-MODEL-005,REQ-DEV-MODEL-006,REQ-DEV-MODEL-007,REQ-DEV-MODEL-008,REQ-DEV-MODEL-009,REQ-DEV-MODEL-010,REQ-DEV-MODEL-011,REQ-DEV-MODEL-012,REQ-DEV-MODEL-013,REQ-DEV-MODEL-014,REQ-DEV-MODEL-015,REQ-DEV-MODEL-016,REQ-DEV-MODEL-017,REQ-DEV-MODEL-018,REQ-DEV-MODEL-019,REQ-DEV-MODEL-020,REQ-DEV-MODEL-021,REQ-DEV-MODEL-022,REQ-DEV-MODEL-023,REQ-DEV-MODEL-024,REQ-DEV-MODEL-025,REQ-DEV-MODEL-026,REQ-DEV-MODEL-027,REQ-DEV-MODEL-028,REQ-DEV-MODEL-029,REQ-DEV-MODEL-030,REQ-DEV-MODEL-031,REQ-DEV-MODEL-032,REQ-DEV-MODEL-033,REQ-DEV-MODEL-034,REQ-DEV-MODEL-035,REQ-DEV-MODEL-036,REQ-DEV-MODEL-037,REQ-DEV-MODEL-038,REQ-DEV-MODEL-039,REQ-DEV-MODEL-040 -->
- **REQ-DEV-MODEL-001 — SHALL:** Every kOA development activity occur inside an explicitly identified workspace governed by one active development profile.
- **REQ-DEV-MODEL-002 — SHALL:** Every workspace have a stable workspace identity reflected in environments, containers, networks, volumes, ports, databases, logs, artifacts, and test evidence.
- **REQ-DEV-MODEL-003 — SHALL NOT:** A workspace share a mutable dependency environment, mutable runtime store, database schema, container namespace, or generated state directory with another workspace.
- **REQ-DEV-MODEL-004 — SHALL:** Source, contracts, tests, fixtures, generated outputs, and local runtime state be separable and independently cleanable.
- **REQ-DEV-MODEL-005 — SHALL:** Python development use UV as the canonical package and environment manager.
- **REQ-DEV-MODEL-006 — SHALL:** Every Python workspace use one local `.venv`, one `pyproject.toml`, and one committed `uv.lock`.
- **REQ-DEV-MODEL-007 — SHALL:** Normal environment synchronization, continuous integration, evidence-producing tests, and candidate builds use `uv sync --frozen`.
- **REQ-DEV-MODEL-008 — SHALL:** Python command execution use `uv run` or an equivalent invocation that resolves through the workspace-managed environment.
- **REQ-DEV-MODEL-009 — SHALL NOT:** Direct `pip install`, a global mutable Python environment, system-site package mutation, or an untracked interpreter environment be used as the canonical development path.
- **REQ-DEV-MODEL-010 — SHALL:** Dependency-lock changes be explicit reviewable changes with reproducibility and compatibility impact.
- **REQ-DEV-MODEL-011 — SHALL:** Canonical contracts, schemas, accepted decisions, requirements, locks, and traceability be updated before or with implementation changes that alter observable behavior.
- **REQ-DEV-MODEL-012 — SHALL NOT:** Implementation prevalence, test success, installed code, generated documentation, or a user-interface behavior silently redefine a canonical contract.
- **REQ-DEV-MODEL-013 — SHALL:** Every implementation change identify its owning component, affected capabilities, profiles, interfaces, artifacts, integrations, requirements, locks, tests, and evidence.
- **REQ-DEV-MODEL-014 — SHALL:** Each component preserve its canonical data ownership and interact with other components only through declared interfaces, events, gateways, or artifacts.
- **REQ-DEV-MODEL-015 — SHALL NOT:** Development convenience authorize direct writes to another component's authoritative store or creation of shared logical schemas.
- **REQ-DEV-MODEL-016 — SHALL:** Local containers, services, databases, brokers, and workbenches be activated selectively according to workspace needs and the active profile.
- **REQ-DEV-MODEL-017 — SHALL NOT:** All components, heavy workbenches, indexes, external adapters, or optional services be required to run simultaneously for ordinary development.
- **REQ-DEV-MODEL-018 — SHALL:** Container workloads use workspace-scoped names, networks, volumes, ports, and immutable image identities or explicit versions.
- **REQ-DEV-MODEL-019 — SHALL NOT:** Privileged containers, unrestricted host networking, arbitrary host mounts, or mutable state embedded in container images be part of the ordinary development baseline.
- **REQ-DEV-MODEL-020 — SHALL:** The Resource Governor or a profile-defined conservative envelope protect interactive development and core services before optional or background work.
- **REQ-DEV-MODEL-021 — SHALL NOT:** Resource state determine authorization, consent, publication, disclosure, privilege, or governance policy.
- **REQ-DEV-MODEL-022 — SHALL:** The native development and runtime baseline remain non-AI.
- **REQ-DEV-MODEL-023 — SHALL:** ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain optional registered external surfaces invoked through controlled export, provenance-preserving return, and local acceptance.
- **REQ-DEV-MODEL-024 — SHALL NOT:** External AI output modify canonical contracts, authoritative data, source code, tests, releases, publication state, or policy state without explicit human or authorized local workflow acceptance.
- **REQ-DEV-MODEL-025 — SHALL:** SenTient remain optional, isolated, non-authoritative, removable, and limited to eligible development or build profiles.
- **REQ-DEV-MODEL-026 — SHALL NOT:** SenTient, a local model runtime, or any AI workbench become a dependency of the default developer setup, runtime conformance, build reproducibility, or release activation.
- **REQ-DEV-MODEL-027 — SHALL:** Tests be classified as unit, contract, component, integration, profile, artifact, migration, security, offline, recovery, or conformance tests.
- **REQ-DEV-MODEL-028 — SHALL:** Every normative requirement and lock affected by an implementation change have traceability to applicable tests and current evidence.
- **REQ-DEV-MODEL-029 — SHALL:** Evidence-producing tests record workspace identity, profile, source revision, toolchain identity, dependency lock, component versions, artifact identities, execution time, and result.
- **REQ-DEV-MODEL-030 — SHALL NOT:** A passing local test alone establish production, sovereign, high-assurance, release-signing, or control-plane conformance.
- **REQ-DEV-MODEL-031 — SHALL:** Generated documentation, registries, indexes, matrices, and AI context be reproducible from canonical sources and checked for staleness.
- **REQ-DEV-MODEL-032 — SHALL NOT:** Generated output be edited as the sole source of a semantic change.
- **REQ-DEV-MODEL-033 — SHALL:** Candidate artifacts record source revision, toolchain identity, dependency lock, artifact class, version, profile, provenance, integrity, tests, and evidence.
- **REQ-DEV-MODEL-034 — SHALL NOT:** A developer workstation sign, publish, activate, or represent a candidate artifact as a production release unless its active profile explicitly possesses that authority.
- **REQ-DEV-MODEL-035 — SHALL:** Production release claims use the applicable build, signing, release-channel, Release Set, compatibility, approval, and activation contracts.
- **REQ-DEV-MODEL-036 — SHALL:** Development operation continue offline for source editing, locally cached dependency execution, local tests, documentation validation, and locally available component workflows according to the active profile.
- **REQ-DEV-MODEL-037 — SHALL:** Unavailable remote repositories, package sources, artifact services, external providers, and federation peers produce explicit degraded, deferred, or unavailable states without corrupting local work.
- **REQ-DEV-MODEL-038 — SHALL:** Secrets use managed references and remain absent from source files, committed environment files, fixtures, logs, receipts, generated documentation, and candidate artifacts.
- **REQ-DEV-MODEL-039 — SHALL:** Development changes use reviewable change sets, deterministic validation, bounded exceptions, migration treatment where applicable, and rollback or forward-repair planning for semantic changes.
- **REQ-DEV-MODEL-040 — SHALL:** Development-model conformance include workspace isolation, UV enforcement, dependency reproducibility, component-boundary validation, selective service activation, AI-boundary validation, test traceability, generated-content checks, artifact separation, secret scanning, offline behavior, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Workspace and Toolchain Model

### 6.1 Workspace layout

A workspace separates these logical areas:

```text
source
contracts
tests
fixtures
generated
runtime
artifacts
evidence
cache
```

The physical layout can vary by repository, but cleanup and validation need to distinguish them.

Source and canonical contracts are version-controlled. Mutable runtime state, caches, local databases, local queues, and temporary artifacts remain workspace-scoped and excluded from canonical source.

### 6.2 Python environment

Python workspaces use:

```text
pyproject.toml
uv.lock
.venv
```

The normal setup command is:

```bash
uv sync --frozen
```

Python commands execute through:

```bash
uv run <command>
```

A lock update is explicit:

```bash
uv lock
```

The updated lock is reviewed as part of the change.

### 6.3 Toolchain identity

Evidence-producing execution records:

- operating profile;
- host and guest platform where relevant;
- Python version;
- UV version;
- dependency lock identity;
- source revision;
- selected features or dependency groups;
- container backend where applicable;
- component and artifact versions.

A developer's interactive shell state is not sufficient toolchain identity.

### 6.4 Containers and local infrastructure

Containers are selective implementation mechanisms.

A workspace declares:

- one container backend;
- workspace network;
- named volumes;
- ports;
- image identities;
- service activation;
- dependencies;
- cleanup.

Rootless execution is the default. Privileged behavior goes through an explicitly registered mechanism and is not granted to ordinary component containers.

A database or broker can be shared physically only when logical workspace and component isolation remain explicit and validated.

### 6.5 Service activation

Services use activation modes such as:

```text
always_on
session_activated
task_activated
test_activated
manual
```

The active development profile identifies which components are required, available on demand, optional, or excluded.

Heavy workbenches and indexes remain stopped until a task requires them.

### 6.6 Resource behavior

Development work uses a declared resource envelope.

Pressure response protects:

1. active source and contract work;
2. interactive tests;
3. essential component services;
4. mutable authoritative test state;
5. test evidence;
6. optional workbenches;
7. background indexing and caches.

Optional work stops before core workspace state becomes unsafe.

### 6.7 Secrets and configuration

Configuration is separated into:

- committed non-secret defaults;
- profile-owned values;
- workspace-local non-secret overrides;
- managed secret references;
- generated runtime configuration.

Secret values do not enter source control, ordinary environment files, fixture archives, generated documentation, candidate artifacts, or logs.

## 7. Change and Validation Workflow

### 7.1 Classifying a change

A change is classified as:

```text
implementation_only
compatible_contract_change
semantic_contract_change
profile_change
artifact_change
integration_change
migration_change
release_change
```

Classification determines required decisions, impact analysis, tests, evidence, compatibility, and review.

### 7.2 Contracts-first workflow

A semantic change proceeds through:

1. identify canonical owner;
2. record or reference an accepted decision;
3. update requirements and locks;
4. update registries and schemas;
5. update component, profile, artifact, or integration contracts;
6. update traceability;
7. implement behavior;
8. add or update tests;
9. generate evidence;
10. regenerate explanatory and derived content;
11. run validation;
12. prepare candidate artifacts;
13. hand off to authorized build or release workflows.

The sequence can occur in one change set. The canonical and implementation effects remain distinguishable.

### 7.3 Implementation-only workflow

A compatible internal refactor:

1. identifies the unchanged observable contract;
2. changes implementation;
3. runs unit and component tests;
4. runs affected integration and profile tests;
5. demonstrates no contract change;
6. updates evidence when required.

A refactor that changes timing, failure, resource, state, interface, offline, or security behavior is not implementation-only.

### 7.4 Local validation

Local validation includes applicable checks for:

- formatting and static analysis;
- unit behavior;
- contract schemas;
- component boundaries;
- profile inheritance;
- artifact contracts;
- integration boundaries;
- AI boundaries;
- requirements and locks;
- traceability;
- generated content;
- prohibited open-state markers.

The principal documentation and contract command is:

```bash
uv run python docs/tools/validate_docs.py
```

Project-specific commands remain registered in the applicable toolchain and test catalog.

### 7.5 Test isolation

Tests identify:

- workspace;
- profile;
- component instances;
- database and queue namespaces;
- ports;
- temporary directories;
- artifacts;
- external fakes or controlled sandboxes.

Tests clean only their own state. A parallel test cannot depend on another test's mutable result unless an explicit ordered scenario contract defines the relationship.

### 7.6 External dependencies in tests

Tests distinguish:

- deterministic local tests;
- local contract fakes;
- controlled integration sandboxes;
- live external-provider tests;
- offline-transfer tests.

Live provider availability cannot be a prerequisite for ordinary unit, contract, component, or documentation validation.

Provider tests use registered integrations, minimized data, managed credentials, and explicit cost and cleanup controls.

### 7.7 Evidence generation

Evidence-producing tests create immutable evidence records or artifacts with:

- test identity;
- requirement and lock references;
- subject component, profile, artifact, or release;
- source and toolchain identity;
- environment;
- inputs;
- execution result;
- timestamps;
- retained logs or attachments according to classification;
- reviewer or automated verifier where applicable.

Generated evidence does not become current until registered and accepted by the applicable validation workflow.

## 8. AI, Workbench, and Offline Boundaries

### 8.1 Native baseline

Native development commands, builds, tests, validators, migrations, generators, runtime components, and release controls remain deterministic and non-AI.

No AI provider is required for setup, dependency resolution, test execution, documentation validation, candidate artifact construction, or runtime conformance.

### 8.2 Approved external AI surfaces

The approved external surfaces are:

```text
ChatGPT
Suno
Gamma
approved Ariane voice adapter
```

A development use follows:

```text
explicit user selection
controlled export
external processing
provenance-preserving return
controlled local import
human or authorized local review
explicit acceptance
```

Outputs can be candidate source, documentation, tests, media, or analysis. They remain non-authoritative until accepted into the owning workflow.

### 8.3 AI-generated changes

An accepted AI-assisted change receives the same treatment as a human-authored change:

- canonical-owner identification;
- review;
- tests;
- security and license checks;
- traceability;
- generated-content checks;
- artifact and release separation.

The provenance identifies external assistance when required by the active policy.

### 8.4 SenTient

SenTient is an optional isolated workbench.

It:

- is not installed or started by default;
- operates only in eligible development or build profiles;
- uses workspace-scoped data;
- produces candidate output;
- cannot write runtime authoritative stores directly;
- can be removed without breaking the workspace baseline;
- has explicit resource and network policy.

SenTient does not establish a native AI capability.

### 8.5 Offline development

The active developer profile defines exact behavior.

Common continuous or degraded offline work includes:

- source editing;
- contract and documentation reading;
- local Git operations;
- cached dependency execution;
- locally available tests;
- generated-content validation;
- locally available components;
- candidate artifact inspection.

Common unavailable or deferred work includes:

- uncached dependency download;
- remote repository synchronization;
- remote artifact publication;
- live provider tests;
- external AI;
- remote evidence upload.

Offline state is explicit. A deferred external effect is not reported as complete.

## 9. Candidate Artifacts, Build, and Release

### 9.1 Candidate artifact construction

A candidate artifact records:

- artifact identity and class;
- semantic version;
- source revision;
- toolchain identity;
- dependency lock;
- build parameters;
- profile;
- component or contract versions;
- provenance;
- functional integrity record;
- tests;
- evidence;
- intended release channel.

Development artifact integrity is appropriate because artifacts have a functional content-integrity contract. Ordinary Markdown content does not receive file-hash requirements.

### 9.2 Development signing

Development signing can identify an artifact as originating from a development or test authority.

It does not grant:

- production authenticity;
- production release status;
- channel publication;
- activation authority;
- sovereign conformance;
- high-assurance conformance.

The signature identity and trust domain remain explicit.

### 9.3 Production build handoff

A production build handoff includes:

- accepted source revision;
- canonical contract versions;
- dependency locks;
- toolchain requirements;
- build inputs;
- candidate evidence;
- expected artifact classes;
- test obligations;
- known exceptions;
- compatibility requirements.

The build environment independently verifies the handoff.

### 9.4 Release channels

Production release artifacts belong to one of four channels:

```text
system
services
governance
knowledge
```

A compatible Release Set contains one tested version per channel.

A developer workstation does not create a release claim merely by producing four candidate artifacts.

### 9.5 Activation separation

Artifact production, signing, publication, approval, and activation are distinct transitions.

An active release uses:

- authorized build evidence;
- authorized signatures;
- release-channel ownership;
- compatibility validation;
- approval;
- atomic activation;
- rollback or forward repair;
- activation evidence.

Development remains upstream of these authorities.

## 10. Failure, Exceptions, and Conformance

### 10.1 Failure behavior

| Failure | Required behavior |
| --- | --- |
| Workspace identity missing | Block mutable infrastructure and evidence-producing execution. |
| Dependency lock absent or stale | Block frozen synchronization and reproducibility claims. |
| UV unavailable | Block canonical Python setup until the registered toolchain is restored. |
| Shared mutable environment detected | Block conformance and isolate or recreate the workspace. |
| Component ownership conflict | Block integration and affected tests. |
| Contract and implementation disagree | Treat the implementation as non-conformant. |
| Generated content stale | Regenerate from canonical sources and block authority use of stale output. |
| External provider unavailable | Preserve local development and mark affected work unavailable or deferred. |
| Secret detected | Block commit, artifact, evidence, or export according to its location. |
| Test evidence incomplete | Block the affected claim. |
| Candidate artifact incompatible | Quarantine or reject it before downstream handoff. |
| Resource pressure | Stop optional work before core workspace state. |
| Offline cache incomplete | Block only operations requiring missing remote inputs. |
| Exception expired | Revalidate without the exception and block affected claims. |

### 10.2 Exceptions

A bounded exception can adjust:

- a tool version interval;
- a test environment;
- a profile-specific resource value;
- a temporary integration sandbox;
- an evidence source;
- a compatibility interval;
- an implementation adapter.

An exception cannot:

- replace UV as the canonical Python environment manager;
- permit shared mutable dependency environments;
- authorize direct cross-component writes;
- make external AI authoritative;
- make SenTient mandatory;
- permit secrets in source or artifacts;
- convert a candidate into a production release;
- waive a non-waivable lock;
- conceal a failing test or open decision;
- create an unqualified conformance claim.

### 10.3 Conformance criteria

This document is conformant when validation confirms:

1. every active workspace identifies its development profile;
2. mutable workspace resources are uniquely namespaced;
3. Python workspaces use `.venv`, `pyproject.toml`, `uv.lock`, and UV;
4. frozen synchronization is used for normal setup and evidence-producing execution;
5. global or system Python mutation is absent from the canonical path;
6. semantic changes update canonical owners and traceability;
7. component ownership and direct-write boundaries pass;
8. containers and services are selective and workspace-scoped;
9. privileged containers and unrestricted host networking are absent;
10. resource pressure preserves core work;
11. the native baseline contains no AI dependency;
12. approved external AI remains controlled and non-authoritative;
13. SenTient remains optional, isolated, and removable;
14. tests are classified and linked to requirements and locks;
15. evidence contains source, profile, toolchain, lock, and result identity;
16. generated content is reproducible and current;
17. candidate artifacts are distinct from production releases;
18. production release claims use authorized build, signing, channel, Release Set, and activation paths;
19. offline development behavior matches the active profile;
20. secrets remain managed and absent from prohibited locations;
21. exceptions are bounded and current;
22. all canonical references resolve;
23. no prohibited open-state marker enters active authority.

The principal validation entry point is:

```bash
uv run python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_component_boundaries.py
tools/check_profile_inheritance.py
tools/check_interfile_locks.py
tools/check_ai_boundary.py
tools/check_artifact_contracts.py
tools/check_traceability.py
tools/check_generated_content.py
tools/check_no_unresolved_state.py
```

## 11. Non-Normative Examples

### 11.1 New component behavior

A developer adds a component operation. The change updates the component contract, requirements, locks, traceability, tests, implementation, and generated documentation in one reviewable change set.

### 11.2 Python setup

A developer clones a repository, enters the workspace, and runs:

```bash
uv sync --frozen
uv run pytest
```

The environment is created in `.venv` and uses the committed `uv.lock`.

### 11.3 Dependency update

A security update requires a new dependency version. The developer changes the declared constraint, runs `uv lock`, reviews the lock delta, executes compatibility and security tests, and records evidence.

### 11.4 Parallel workspaces

Two branches run simultaneously. Each has a separate `.venv`, network, database name, container names, volumes, ports, logs, and evidence directory.

### 11.5 External AI assistance

A developer sends a selected, non-secret excerpt through the registered ChatGPT surface. Returned code is candidate material. The developer reviews it, modifies it, runs tests, and accepts it through the normal source workflow.

### 11.6 SenTient workbench

A developer explicitly enables SenTient for analysis in an eligible workspace. It uses a bounded resource envelope and workspace-scoped data. Stopping or removing it does not affect ordinary setup, tests, or component execution.

### 11.7 Local candidate artifact

A developer builds a services candidate artifact with source, UV, lock, profile, provenance, test, and integrity records. The artifact remains a candidate until an authorized production build and release path accepts it.

### 11.8 Offline work

A developer loses network access. Source editing, local Git, cached dependency execution, local tests, and documentation validation continue. Remote push, external AI, and uncached downloads become unavailable or deferred.

### 11.9 Failed generated-content check

A registry changes but a generated matrix remains stale. Validation fails. The matrix is regenerated from the registry; it is not edited manually as the semantic source.

### 11.10 Shared database mistake

Two workspaces point to the same mutable logical schema. Validation blocks both conformance claims until separate workspace and component namespaces are restored.
