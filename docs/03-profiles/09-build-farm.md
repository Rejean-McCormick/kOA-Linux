<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PRO-009",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profiles",
  "scope": [
    "profile:build_farm"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/system.contract.json#/profile_model",
    "contracts/system.contract.json#/release_model",
    "generated/component-catalog.json",
    "generated/toolchain-catalog.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/integration-types.contract.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-LINUX-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-PRO-BUILD-001",
    "REQ-PRO-BUILD-002",
    "REQ-PRO-BUILD-003",
    "REQ-PRO-BUILD-004",
    "REQ-PRO-BUILD-005",
    "REQ-PRO-BUILD-006",
    "REQ-PRO-BUILD-007",
    "REQ-PRO-BUILD-008",
    "REQ-PRO-BUILD-009",
    "REQ-PRO-BUILD-010",
    "REQ-PRO-BUILD-011",
    "REQ-PRO-BUILD-012",
    "REQ-PRO-BUILD-013",
    "REQ-PRO-BUILD-014",
    "REQ-PRO-BUILD-015",
    "REQ-PRO-BUILD-016",
    "REQ-PRO-BUILD-017",
    "REQ-PRO-BUILD-018",
    "REQ-PRO-BUILD-019",
    "REQ-PRO-BUILD-020",
    "REQ-PRO-BUILD-021",
    "REQ-PRO-BUILD-022",
    "REQ-PRO-BUILD-023",
    "REQ-PRO-BUILD-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-GOV-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PRO-000",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-013",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-SYS-020"
  ],
  "tags": [
    "build-farm",
    "reproducible-builds",
    "clean-workers",
    "artifact-publication",
    "provenance",
    "signing",
    "supply-chain",
    "ci"
  ]
}
KOA:DOC-META:END -->

# Build Farm Profile

## 1. Purpose

This document defines the `build_farm` primary deployment profile.

The build farm is a controlled environment for producing, testing, attesting, signing, and publishing kOA artifacts. Its purpose is to turn declared source revisions and canonical build inputs into reproducible candidate artifacts and release evidence without transferring product authority to the build infrastructure.

The profile provides:

- isolated build jobs;
- reproducible toolchains;
- clean and disposable workers;
- controlled dependency acquisition;
- source, toolchain, and target-platform identity;
- test and conformance execution;
- software bill of materials production;
- provenance and attestation production;
- artifact signing through a bounded signing path;
- controlled publication to declared release channels;
- retention of build records and evidence;
- resource governance for concurrent builds;
- offline or restricted-network build modes where applicable.

The build farm is not a general user workstation, application runtime, universal control plane, product database, or permanent research environment.

A successful build does not itself authorize release activation, deployment, publication across a product-domain boundary, or acceptance of generated content into an authoritative component.

## 2. Scope

This document applies to instances whose selected primary profile is:

`text
build_farm
`

It governs:

- build coordinators;
- build workers;
- source acquisition;
- dependency resolution;
- toolchain selection;
- workspace creation;
- job isolation;
- test execution;
- artifact creation;
- artifact caching;
- provenance generation;
- SBOM generation;
- signing requests;
- release-candidate assembly;
- publication;
- evidence retention;
- build-farm recovery;
- resource allocation;
- approved optional workbenches used for build-time analysis.

It applies to artifacts in all active release channels:

- system;
- services;
- governance;
- knowledge.

It applies to local, clustered, virtualized, containerized, and Kubernetes-based build-farm implementations when those implementations remain within the profile contract.

It does not define:

- end-user interaction behavior;
- production service activation;
- product-domain business workflows;
- authoritative product data;
- unrestricted developer experimentation;
- endpoint orchestration requirements;
- the internal format of every artifact class;
- signing-key custody details owned by security contracts;
- source-control governance owned by repository policy;
- release approval authority owned by lifecycle and governance contracts.

The `high_assurance` and `sovereign_offline` overlays may add constraints when explicitly compatible with the build-farm profile. The `appliance_shell` overlay is not applicable to ordinary build-farm operation.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/profiles/build-farm.profile.json` | Complete machine-readable build-farm capability, component, platform, resource, security, lifecycle, and conformance definition. |
| `generated/profile-catalog.json` | Profile identity, version, class, lifecycle, and overlay compatibility. |
| `contracts/system.contract.json#/release_model` | Global release model and Release Set semantics. |
| `generated/component-catalog.json` | Component identities, responsibilities, dependencies, and authoritative data ownership. |
| `generated/toolchain-catalog.json` | Active build and development toolchain inventory. |
| `contracts/toolchains/python-uv.toolchain.json` | Canonical Python environment, dependency, validation, and build rules where Python applies. |
| `contracts/release-channels.contract.json` | The system, services, governance, and knowledge release channels. |
| `contracts/artifact-classes.contract.json` | Artifact classes, lifecycle properties, compatibility, integrity, and activation expectations. |
| `generated/test-catalog.json` | Canonical tests and test targets. |
| `generated/evidence-catalog.json` | Build, test, provenance, signing, publication, and conformance evidence. |
| `contracts/integration-types.contract.json` | Source, dependency, signing, transparency, and publication integrations. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Cross-file profile, development, lifecycle, data, AI, and component invariants. |
| `generated/traceability.json` | Links among source decisions, profile requirements, tests, evidence, artifacts, and documents. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

This document explains the build-farm contract. It does not become the owner of tool versions, dependency locks, release-channel membership, artifact structures, signing policies, hardware values, or test catalogs.

## 4. Model and Responsibilities

### 4.1 Profile identity

The canonical profile identifier is:

`text
build_farm
`

It is a primary profile.

One build-farm instance has:

- one instance identity;
- one active profile version;
- zero or more compatible overlays;
- one declared platform configuration;
- one worker inventory;
- one resource envelope;
- one trust configuration;
- one build-record namespace;
- one artifact-staging namespace;
- one conformance record.

A build farm may consist of multiple nodes. The nodes remain one profile instance only when identity, policy, scheduling, evidence, artifact, and administrative boundaries are governed as one declared instance.

### 4.2 Functional boundary

The build farm owns the execution and evidence of build operations. It does not own the semantic authority of the source, the product behavior encoded by source, the release decision, or the deployed artifact.

Its responsibilities include:

- obtaining an explicitly identified source revision;
- verifying declared source and dependency inputs;
- selecting an approved toolchain;
- provisioning an isolated clean workspace;
- executing declared build and test commands;
- collecting outputs;
- validating artifact structure and policy;
- producing provenance, SBOMs, and test evidence;
- requesting signing through an approved boundary;
- staging or publishing approved artifacts;
- preserving build records.

Its non-responsibilities include:

- modifying source to make a failing build pass;
- inventing missing release metadata;
- approving a release;
- activating production deployments;
- rewriting canonical requirements;
- accepting advisory AI output as source authority;
- retaining hidden mutable state between builds;
- acting as an authoritative product database.

### 4.3 Core service classes

The profile may contain the following logical service classes:

| Service class | Responsibility |
| --- | --- |
| Build coordinator | Accepts declared build requests, validates job contracts, assigns workers, and records job state. |
| Worker manager | Creates, isolates, resets, and destroys build workers. |
| Source fetcher | Obtains and verifies declared source revisions and source bundles. |
| Dependency proxy or mirror | Provides approved dependency content and records the resolved inputs. |
| Artifact cache | Stores non-authoritative reusable build inputs and outputs under integrity controls. |
| Test executor | Runs declared test suites in the applicable environment. |
| Evidence collector | Collects machine-readable build, test, SBOM, provenance, and publication evidence. |
| Signing adapter | Sends artifact identities to the approved signing service without exposing signing authority to ordinary workers. |
| Publication adapter | Publishes approved artifacts only to declared destinations and release channels. |
| Resource Governor | Applies CPU, memory, I/O, process, queue, and concurrency limits. |
| Identity and Trust | Verifies worker, source, toolchain, artifact, signer, and publisher identities. |
| Audit Broker | Receives declared critical events and evidence references. |
| kOA Node Agent | Performs bounded node lifecycle, health, activation, and recovery operations where deployed. |

These are logical responsibilities. A physical implementation may consolidate services when component identities, credentials, data ownership, and evidence remain distinct.

### 4.4 Worker model

A worker is a bounded execution environment for one build job or one explicitly declared job group.

Worker types may include:

- ephemeral virtual machines;
- rootless containers;
- disposable bare-metal images;
- isolated Kubernetes jobs;
- equivalent clean execution environments.

Every worker has:

- a unique worker identity;
- a unique job identity;
- a unique workspace identity;
- a declared toolchain;
- a declared target platform;
- an isolated mutable filesystem;
- isolated credentials;
- isolated temporary data;
- bounded network access;
- bounded resources;
- a declared cleanup result.

The default worker lifecycle is:

`text
provisioned
 ↓
verified
 ↓
assigned
 ↓
running
 ↓
collecting
 ↓
sanitized
 ↓
destroyed
`

A worker is not reused as a trusted clean worker until reset and verification pass. A reset that cannot be proved results in destruction or quarantine.

### 4.5 Build job contract

Every job declares:

- job identifier;
- source identity and revision;
- source acquisition method;
- build purpose;
- target artifact classes;
- target platforms and architectures;
- toolchain identities and versions;
- manifest and lockfile identities;
- dependency sources;
- network policy;
- secret policy;
- required commands;
- required tests;
- required evidence;
- resource limits;
- timeout and cancellation behavior;
- output paths;
- publication eligibility;
- retention policy.

A job request with incomplete authority remains blocked.

### 4.6 Reproducibility model

Reproducibility is evaluated from declared inputs.

The reproducibility input set includes:

- source revision or verified source bundle;
- submodule and nested-source identities;
- toolchain identity and exact versions;
- build command identity;
- environment and target-platform identity;
- dependency manifests;
- dependency lockfiles;
- resolved dependency identities;
- declared build-time environment variables;
- declared feature flags;
- declared generated-source inputs;
- build policy version;
- artifact-class version.

Release-candidate builds use frozen or equivalently immutable dependency resolution.

A clean rebuild of the same input set is compared according to the artifact class's reproducibility policy. Byte-identical output is required only where the artifact class declares it. When byte identity is not required, normalized semantic comparison and a documented source of allowed variation are required.

### 4.7 Clean workers

A clean worker contains no undeclared mutable state from an earlier job.

Permitted shared state is limited to declared non-authoritative caches whose content is:

- integrity-addressed or otherwise verifiable;
- not trusted merely because it is cached;
- read-only to ordinary jobs where practical;
- replaceable without changing authority;
- excluded from the job's authoritative output unless explicitly declared.

Examples include content-addressed package and compiler caches.

Shared mutable workspaces, mutable dependency environments, signing credentials, product databases, and undeclared build outputs are prohibited.

### 4.8 Source acquisition

Source is accepted only through a declared source contract.

The build record preserves:

- repository or bundle identity;
- revision;
- tag when applicable;
- signer or source attestation when applicable;
- acquisition time;
- acquisition integration;
- submodule or nested source identities;
- verification result.

The build farm does not build an unspecified moving branch head as a release candidate.

A mutable branch may support non-release validation only when the resulting artifact is identified as non-release and the exact resolved revision is recorded.

### 4.9 Dependency acquisition

Dependency sources are allow-listed by the applicable toolchain and profile contracts.

Resolution may use:

- approved package indexes;
- approved source repositories;
- verified offline bundles;
- profile-managed mirrors;
- local workspace dependencies explicitly declared by the job.

Release-candidate jobs resolve from a lockfile or equivalent immutable resolution record.

Network access is denied after dependency acquisition when the toolchain and build procedure support an offline build phase.

Dependencies retrieved from a cache remain subject to integrity and policy verification.

### 4.10 Toolchains

Toolchains are canonical contracts rather than worker-local conventions.

Each toolchain defines:

- required tools;
- version-selection policy;
- workspace markers;
- isolation model;
- manifests and lockfiles;
- commands;
- reproducibility properties;
- security restrictions;
- output declarations.

For Python builds, the active Python toolchain uses UV with one workspace environment, declared Python version, versioned `pyproject.toml`, versioned `uv.lock`, and frozen validation resolution.

A build job does not install undeclared application dependencies globally.

### 4.11 Orchestration

An OCI-compatible execution environment is required for the canonical build-farm profile.

Kubernetes is permitted but not required.

When Kubernetes is used:

- jobs use bounded service accounts;
- privileged pods are prohibited unless a separate narrow contract authorizes them;
- namespaces, storage, secrets, and network policy are isolated by job or trusted job class;
- cluster control-plane authority remains separate from artifact and release authority;
- Kubernetes-specific behavior does not enter application contracts.

When Kubernetes is not used, equivalent isolation and scheduling properties remain required.

### 4.12 Platform and hardware envelope

The canonical hardware and platform values are owned by `contracts/profiles/build-farm.profile.json`.

<!-- GENERATED:BEGIN
source=contracts/profiles/build-farm.profile.json#/hardware_envelope
renderer=profile-hardware-envelope-v1
-->
| Property | Required profile value |
| --- | --- |
| CPU | 16 modern cores minimum |
| Memory | 64 GiB minimum |
| Storage | 2 TB SSD minimum |
| Artifact cache | Required |
| Worker cleanliness | Reproducible clean workers required |
<!-- GENERATED:END -->

The values describe the minimum conformant instance envelope, not a per-worker minimum.

A larger farm scales workers, cache, network, and evidence storage according to measured workload while preserving job isolation.

### 4.13 Resource governance

The Resource Governor controls:

- per-job CPU;
- per-job memory;
- process counts;
- I/O priority and limits;
- queue depth;
- worker concurrency;
- heavy-job concurrency;
- storage quotas;
- cache quotas;
- job timeout;
- cancellation;
- task activation for optional heavy services.

Resource limits are recorded in the job evidence.

A job exceeding its declared envelope is throttled, paused, cancelled, or failed according to the job contract. Resource pressure does not authorize omission of tests, integrity verification, provenance, or policy.

### 4.14 Artifact staging

Build outputs first enter a non-authoritative staging area.

Staged artifacts are identified by:

- artifact class;
- artifact name;
- artifact version;
- build job;
- source revision;
- toolchain;
- target platform;
- integrity identity;
- compatibility metadata;
- test status;
- provenance status;
- signing status;
- release-channel eligibility.

A staging object does not become a released or active artifact merely because it exists.

### 4.15 Four release channels

The build farm can produce artifacts for these independent channels:

| Channel | Typical output |
| --- | --- |
| `system` | Operating-system, node, boot, recovery, or system-image artifacts. |
| `services` | Component services, containers, packages, and service bundles. |
| `governance` | Policy bundles, governance configuration, trust material, and governed contract artifacts. |
| `knowledge` | Kristal, language, PGF, Atlas, Runtime Pack, and related knowledge artifacts. |

A build may target one or more channels only when the job contract declares each target.

A Release Set binds compatible versions across channels. Independent channel publication does not imply arbitrary cross-version compatibility.

### 4.16 Tests and conformance

A candidate artifact runs all applicable:

- unit tests;
- integration tests;
- contract tests;
- schema tests;
- security tests;
- policy tests;
- reproducibility checks;
- artifact-class checks;
- profile compatibility checks;
- migration checks;
- installation tests;
- activation and rollback tests;
- conformance tests.

Tests are selected from `generated/test-catalog.json`.

A skipped mandatory test is a failed or blocked release gate unless an active exception explicitly covers it.

### 4.17 Provenance and SBOM

Every release candidate includes machine-readable provenance that identifies:

- source;
- build job;
- worker;
- toolchain;
- dependencies;
- target;
- commands;
- policy;
- test results;
- artifact identity;
- build time;
- publication target when applicable.

Every artifact class that contains software or packaged dependencies includes an SBOM according to its artifact contract.

Provenance and SBOM records are evidence. They do not replace the artifact contract or release decision.

### 4.18 Signing boundary

Ordinary workers do not hold release-signing private keys.

The signing path receives:

- artifact identity;
- artifact bytes or an approved digest reference;
- artifact class;
- release channel;
- provenance reference;
- required approval reference;
- signing-policy identity.

The signing service returns a signature and receipt or a rejection.

A successful build cannot compel signing.

A successful signature cannot compel publication.

### 4.19 Publication boundary

Publication occurs only through a declared publication integration.

The publication request includes:

- artifact identity;
- artifact class;
- release channel;
- destination;
- signature;
- provenance;
- SBOM when applicable;
- test evidence;
- release approval;
- compatibility metadata.

Publication success produces a receipt.

The build farm does not report publication when only staging or upload initiation succeeded.

### 4.20 SenTient and external AI

SenTient may be installed as an optional isolated workbench for explicitly approved build-time research, enrichment, or analysis.

It is:

- task-activated;
- separately resourced;
- separately networked;
- separately credentialed;
- non-authoritative;
- excluded from reproducible build inputs unless an accepted artifact contract explicitly defines a reviewed imported output.

External AI services are not native build dependencies.

An external AI result is candidate input and requires provenance, review, controlled import, and acceptance by the canonical source owner before it participates in a release build.

### 4.21 Data ownership

The build farm owns build-job records, worker state, cache indexes, staged-artifact records, and build evidence within their declared domains.

It does not own:

- application source;
- product-domain records;
- release approval decisions;
- signing keys;
- deployed service state;
- canonical documentation facts;
- source-component authoritative data.

Physical database consolidation may be used, but logical ownership, identities, schemas, permissions, backup, restore, and retention remain distinct.

### 4.22 Retention and cleanup

Retention classes distinguish:

- temporary worker state;
- transient build outputs;
- caches;
- failed-build diagnostics;
- successful build evidence;
- release-candidate artifacts;
- published artifact records;
- security and audit evidence.

Temporary worker state is destroyed after collection and sanitization.

Evidence required for a release or conformance claim is retained according to the applicable lifecycle contract.

Caches may be evicted without changing authority.

### 4.23 Offline and restricted-network operation

The build farm may apply the `sovereign_offline` overlay.

An offline-capable build uses:

- verified source bundles;
- verified dependency bundles or mirrors;
- declared toolchain bundles;
- offline trust material;
- local test catalogs;
- local artifact staging;
- controlled export for publication.

An offline build does not claim current remote dependency state. It records the identities and validity of the imported bundles.

### 4.24 Conformance claim

A complete build-farm conformance claim identifies:

- profile and overlay versions;
- instance identity;
- platform and hardware;
- worker-isolation mechanism;
- orchestration mechanism;
- toolchains;
- release-channel capabilities;
- security controls;
- test results;
- evidence;
- exceptions;
- validity conditions.

The claim applies to the evaluated build-farm instance, not automatically to every artifact it produces.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PRO-BUILD-001,REQ-PRO-BUILD-002,REQ-PRO-BUILD-003,REQ-PRO-BUILD-004,REQ-PRO-BUILD-005,REQ-PRO-BUILD-006,REQ-PRO-BUILD-007,REQ-PRO-BUILD-008,REQ-PRO-BUILD-009,REQ-PRO-BUILD-010,REQ-PRO-BUILD-011,REQ-PRO-BUILD-012,REQ-PRO-BUILD-013,REQ-PRO-BUILD-014,REQ-PRO-BUILD-015,REQ-PRO-BUILD-016,REQ-PRO-BUILD-017,REQ-PRO-BUILD-018,REQ-PRO-BUILD-019,REQ-PRO-BUILD-020,REQ-PRO-BUILD-021,REQ-PRO-BUILD-022,REQ-PRO-BUILD-023,REQ-PRO-BUILD-024 -->
- **REQ-PRO-BUILD-001 — SHALL:** Every build job shall identify its source revision, toolchain, target platform, target artifact classes, commands, tests, resource envelope, network policy, secret policy, and evidence requirements.
- **REQ-PRO-BUILD-002 — SHALL:** Release-candidate builds shall execute in verified clean workers with isolated mutable workspaces, credentials, temporary data, processes, and resource limits.
- **REQ-PRO-BUILD-003 — SHALL NOT:** A build worker shall trust undeclared mutable state from an earlier job.
- **REQ-PRO-BUILD-004 — MAY:** The build farm may share declared non-authoritative caches when cached content remains integrity-verifiable, replaceable, and unable to broaden job authority.
- **REQ-PRO-BUILD-005 — SHALL:** Release-candidate dependency resolution shall use lockfiles or equivalent immutable resolution records from approved sources.
- **REQ-PRO-BUILD-006 — SHALL:** Every produced artifact shall remain non-authoritative staging output until all applicable validation, evidence, approval, signing, and publication gates pass.
- **REQ-PRO-BUILD-007 — SHALL:** Every release candidate shall be traceable to exact source, toolchain, dependency, command, worker, target-platform, test, and policy identities.
- **REQ-PRO-BUILD-008 — SHALL:** Every software-bearing release candidate shall include the SBOM required by its artifact contract.
- **REQ-PRO-BUILD-009 — SHALL:** Every release candidate shall include machine-readable provenance and applicable test evidence.
- **REQ-PRO-BUILD-010 — SHALL NOT:** Ordinary build workers shall hold release-signing private keys or unrestricted publication credentials.
- **REQ-PRO-BUILD-011 — SHALL:** Signing and publication shall occur through separate declared authority boundaries and shall each produce an independently verifiable result.
- **REQ-PRO-BUILD-012 — SHALL NOT:** A successful build, test, signature, upload, or staging operation shall be represented as release approval or production activation.
- **REQ-PRO-BUILD-013 — SHALL:** Build outputs shall declare their artifact class, release channel, version, compatibility metadata, integrity identity, provenance, and evidence references.
- **REQ-PRO-BUILD-014 — SHALL:** The build farm shall preserve the independence of the system, services, governance, and knowledge release channels.
- **REQ-PRO-BUILD-015 — SHALL:** A multi-channel Release Set shall declare and validate compatibility among its referenced channel artifacts.
- **REQ-PRO-BUILD-016 — SHALL:** Every mandatory test selected by the artifact, profile, component, lifecycle, security, or release contract shall pass or be covered by an active approved exception before publication.
- **REQ-PRO-BUILD-017 — SHALL:** The Resource Governor shall enforce per-job and per-worker resource, concurrency, queue, storage, and timeout limits.
- **REQ-PRO-BUILD-018 — SHALL NOT:** Resource pressure, worker scarcity, or schedule pressure shall not authorize omission of integrity checks, mandatory tests, provenance, SBOM generation, signing policy, or publication policy.
- **REQ-PRO-BUILD-019 — SHALL:** Kubernetes use shall remain optional, profile-scoped, and unable to introduce Kubernetes-specific behavior into application contracts.
- **REQ-PRO-BUILD-020 — SHALL:** Build-farm databases and storage shall preserve logical ownership, identities, access controls, retention, backup, and restoration boundaries.
- **REQ-PRO-BUILD-021 — SHALL NOT:** SenTient or an external AI service shall become an undeclared or authoritative build input.
- **REQ-PRO-BUILD-022 — SHALL:** Any accepted SenTient or external AI output used by a build shall have provenance, explicit review, controlled import, source-owner acceptance, and a declared artifact or source identity.
- **REQ-PRO-BUILD-023 — SHALL:** Worker cleanup shall produce a verified result; a worker whose cleanliness cannot be verified shall be quarantined or destroyed before reassignment.
- **REQ-PRO-BUILD-024 — SHALL:** A complete build-farm conformance claim shall identify the effective profile, instance, platform, isolation, orchestration, toolchains, release capabilities, tests, evidence, exceptions, and validity conditions.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Build request admission

A build request follows this sequence:

1. receive the request through an authenticated interface;
2. assign a job identifier;
3. resolve the requesting identity and authority;
4. validate the source identity;
5. validate target artifact classes and release channels;
6. resolve the canonical toolchains;
7. validate manifests and lockfiles;
8. select required tests and evidence;
9. validate resource and network policy;
10. validate secret requirements;
11. check active exceptions;
12. admit the job or return a blocked result.

Admission does not approve publication.

### 6.2 Worker provisioning

The worker manager:

1. selects an allowed worker class;
2. provisions a clean image or environment;
3. assigns worker, job, and workspace identities;
4. applies CPU, memory, process, I/O, storage, and network limits;
5. injects only job-scoped credentials;
6. verifies toolchain availability;
7. verifies worker cleanliness;
8. records the provisioning evidence;
9. assigns the job.

A failed verification returns the worker to quarantine or destroys it.

### 6.3 Source and dependency preparation

The job:

1. obtains the exact source revision or verified source bundle;
2. verifies source identity and nested sources;
3. loads declared manifests and lockfiles;
4. obtains dependencies from approved sources or verified bundles;
5. records exact resolved dependencies;
6. verifies cached content before use;
7. closes network access for the build phase when required;
8. records the prepared-input identity.

### 6.4 Build execution

The worker:

1. initializes the isolated workspace;
2. synchronizes the declared toolchain environment;
3. executes commands by command identifier;
4. records command lines, environment, timing, and exit status;
5. collects declared outputs only;
6. rejects undeclared outputs from release staging;
7. performs cleanup required between command stages;
8. emits build execution evidence.

### 6.5 Test execution

The test executor:

1. resolves applicable tests;
2. provisions required test fixtures;
3. runs tests in the declared environment;
4. records results and evidence;
5. marks skipped mandatory tests as blocked or failed;
6. prevents release eligibility when a required gate does not pass.

### 6.6 Reproducibility verification

When required, the build farm:

1. schedules an independent clean rebuild;
2. prevents shared mutable state between the builds;
3. compares source and input identities;
4. compares output according to the artifact class;
5. records differences;
6. accepts, rejects, or blocks reproducibility;
7. links the result to the candidate artifact.

### 6.7 Artifact finalization

For each candidate:

1. validate artifact structure;
2. assign artifact identity and version;
3. compute required integrity values;
4. generate the SBOM;
5. generate provenance;
6. attach test evidence;
7. validate profile and component compatibility;
8. determine release-channel eligibility;
9. place the candidate in controlled staging.

### 6.8 Signing

The signing procedure:

1. verifies release eligibility;
2. verifies required approval;
3. sends the candidate identity to the signing boundary;
4. validates signing policy;
5. signs or rejects;
6. records the signature and receipt;
7. returns the candidate to staging.

Signing credentials are never returned to the worker.

### 6.9 Publication

The publication procedure:

1. verify the artifact, signature, provenance, SBOM, tests, compatibility, and approval;
2. verify the target release channel and destination;
3. submit through the publication integration;
4. verify the destination result;
5. record the publication receipt;
6. update the staged-artifact record;
7. preserve rollback, withdrawal, or supersession information.

### 6.10 Worker cleanup

After collection:

1. revoke job credentials;
2. detach declared outputs and evidence;
3. erase workspace and temporary state;
4. release or reset storage;
5. clear job network identity;
6. validate cleanup;
7. destroy or return the worker to the clean pool;
8. quarantine on any uncertainty.

### 6.11 Cancellation

Cancellation:

1. marks the job as cancelling;
2. stops new stages;
3. terminates bounded processes;
4. revokes credentials;
5. collects permitted diagnostics;
6. marks partial outputs non-authoritative;
7. performs worker cleanup;
8. records cancellation evidence.

### 6.12 Recovery

After coordinator, worker, cache, storage, or publication failure:

1. reconstruct job state from durable records;
2. identify authoritative completed stages;
3. invalidate partial outputs;
4. verify worker and cache state;
5. resume only idempotent declared stages;
6. restart non-idempotent stages in a clean worker;
7. re-run affected validation;
8. record recovery evidence.

## 7. Failure States and Safe Degradation

| Failure state | Required response |
| --- | --- |
| Source revision does not resolve | The job is blocked; no substitute revision is selected. |
| Source verification fails | The job fails and the source is quarantined from release use. |
| Lockfile or immutable resolution record is missing | Release-candidate admission is blocked. |
| Dependency source is unavailable | The job uses a verified approved mirror or offline bundle, or remains queued or blocked according to policy. |
| Cached dependency fails integrity verification | The cache entry is discarded and the job does not use it. |
| Clean worker cannot be provisioned | The job remains queued or blocked; an unverified worker is not used. |
| Worker isolation fails | The job is stopped, outputs are non-authoritative, and the worker is quarantined. |
| Resource limit is reached | The job is throttled, paused, cancelled, or failed according to its contract. |
| Mandatory test fails | Release eligibility is denied. |
| Mandatory test infrastructure is unavailable | The gate is blocked, not passed. |
| Reproducibility comparison fails | The candidate is denied release eligibility unless the artifact policy permits and explains the measured variation. |
| SBOM generation fails | Applicable software artifacts are denied release eligibility. |
| Provenance generation fails | The candidate is denied release eligibility. |
| Signing service is unavailable | The unsigned candidate remains staged and unpublished. |
| Signing rejects the candidate | Publication is denied. |
| Publication service is unavailable | The signed candidate remains staged; publication is not claimed. |
| Publication result cannot be verified | Publication state is unknown and requires reconciliation before retry. |
| Evidence storage is unavailable | Evidence-required transitions are blocked. |
| Cache is unavailable | Jobs continue without cache when resource policy permits; authority is unchanged. |
| SenTient is unavailable | Ordinary deterministic build operation continues. |
| External AI integration is unavailable | Only the explicitly dependent optional analysis operation is unavailable. |
| Coordinator restarts | Durable job records are reconciled; partial stages are not assumed complete. |
| Worker cleanup is uncertain | The worker is quarantined or destroyed. |
| Signing credential exposure is suspected | Signing is blocked, incident handling begins, and affected signatures are reviewed under the security contract. |

Safe degradation never converts a failed release gate into a pass.

## 8. Cross-Component Interactions

### 8.1 Resource Governor

The build coordinator submits job resource declarations.

The Resource Governor applies limits and scheduling. It does not approve source, tests, signatures, or publication.

### 8.2 Identity and Trust

Identity and Trust verifies:

- requesting identities;
- worker identities;
- source identities;
- dependency sources;
- toolchain identities;
- signing services;
- publication destinations.

A failed trust evaluation blocks the affected operation.

### 8.3 Governance Policy Runtime

Where required by the effective profile, the Governance Policy Runtime evaluates:

- release approval conditions;
- sensitive source access;
- disclosure;
- privileged build operations;
- governed exceptions;
- restricted publication.

It does not execute the build or own artifact bytes.

### 8.4 Audit Broker

The build farm emits declared critical events for:

- job admission;
- source verification;
- worker verification;
- mandatory test results;
- reproducibility results;
- signing;
- publication;
- exception use;
- security-relevant failures.

The Audit Broker does not own build-job or artifact state.

### 8.5 kOA Node Agent

The Node Agent may manage build-node health, worker-image activation, host updates, recovery, and bounded privileged operations.

Build jobs do not inherit Node Agent privilege.

### 8.6 Toolchains

The build farm invokes toolchains through their canonical command and isolation contracts.

A job does not modify a toolchain contract or silently select a newer tool version.

### 8.7 Artifact and release registries

Artifact classes determine structure, compatibility, integrity, activation, and required evidence.

Release channels determine publication membership.

The build farm implements those contracts but does not redefine them.

### 8.8 Signing integration

The signing integration is a separate authority boundary with its own credentials, policy, and evidence.

Workers receive signatures and receipts, not key custody.

### 8.9 Publication integration

Publication adapters have destination-scoped credentials.

A system-channel publisher does not automatically have governance- or knowledge-channel authority.

### 8.10 Source and dependency integrations

Source and dependency adapters are classified integrations.

Their network, credentials, data transfer, caching, and failure behavior are explicit.

### 8.11 SenTient

SenTient runs as an optional isolated workbench.

Its outputs are advisory until imported into a canonical source or artifact workflow through explicit review and acceptance.

### 8.12 Component teams

Component owners provide:

- build manifests;
- toolchain declarations;
- test requirements;
- artifact-class targets;
- compatibility metadata;
- migration tests.

The build farm returns artifacts and evidence. It does not become the owner of component behavior.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect on this profile |
| --- | --- |
| `DEC-PROFILE-001` | Establishes `build_farm` as a primary profile and defines overlays separately. |
| `DEC-PROFILE-BASELINE-001` | Keeps build-farm implementation requirements profile-scoped rather than global. |
| `DEC-LINUX-001` | Requires a standard maintained Linux kernel for the conformant Linux build-farm platform. |
| `DEC-CONTAINER-001` | Requires an OCI-compatible execution capability without imposing one runtime-specific application contract. |
| `DEC-K8S-001` | Permits Kubernetes for the build farm but does not require it. |
| `DEC-HW-001` | Defines the build-farm minimum hardware envelope and clean-worker requirement. |
| `DEC-REL-001` | Defines four independent release channels bound by compatible Release Sets. |
| `DEC-DEV-001` | Establishes isolated and reproducible development and build toolchains. |
| `DEC-DEV-002` | Requires parallel jobs and workspaces to remain isolated. |
| `DEC-DATA-001` | Preserves logical ownership across shared or separate physical data services. |
| `DEC-GOV-001` | Separates resource authority from governance-policy authority. |
| `DEC-AI-001` | Keeps native AI outside the baseline and treats external AI as optional candidate-input integrations. |
| `DEC-SENT-001` | Allows SenTient only as an optional isolated and non-authoritative workbench. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-005` | Profile-scoped rootless container guidance without universal runtime coupling. |
| `ADR-005` | Kubernetes is permitted for the build farm but not required on endpoints. |
| `ADR-015` | Isolated reproducible workspaces with UV. |
| `ADR-019` | Resource Governor and Governance Policy Runtime separation. |
| `ADR-024` | Logical data ownership with profile-dependent physical isolation. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a successful build is a release approval;
- a successful upload is a verified publication;
- a signed artifact is automatically compatible;
- a cache is an authoritative source;
- a worker is clean because its process exited;
- a container is isolated merely because it is a container;
- Kubernetes is required for conformance;
- Kubernetes control-plane identity grants release authority;
- the newest tool version is the correct tool version;
- an unlocked dependency set is reproducible;
- a branch name identifies an exact source revision;
- a skipped test is a passed test;
- a flaky test may be ignored without an exception;
- resource scarcity permits reducing required validation;
- build infrastructure owns product behavior;
- build records own source authority;
- signing keys may be exposed to improve throughput;
- one release-channel credential grants authority over every channel;
- SenTient output is a deterministic build input;
- external AI output is source authority;
- a worker may write directly to a product component's authoritative store;
- a build-farm conformance claim proves artifact conformance;
- historical build success proves a current job will succeed.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `03-profiles/09-build-farm.md`;
3. all metadata identifiers and canonical references resolve;
4. all listed decisions are accepted;
5. all requirements exist with identical text and strength;
6. all locks exist and pass;
7. `build_farm` is registered as one active primary profile;
8. the profile contract validates against `deployment-profile.schema.json`;
9. compatible overlays are explicit;
10. platform and kernel requirements match the profile contract;
11. the hardware envelope matches the profile contract;
12. an OCI-compatible execution capability is available;
13. Kubernetes is optional rather than mandatory;
14. every job has a complete job contract;
15. clean-worker verification exists before assignment;
16. workers, workspaces, credentials, storage, processes, and network are job-scoped;
17. shared caches are non-authoritative and integrity-verifiable;
18. release-candidate dependency resolution is immutable;
19. toolchain identities and exact versions are recorded;
20. undeclared global application dependencies are absent;
21. every candidate has artifact-class and release-channel identity;
22. every applicable candidate has provenance and SBOM evidence;
23. mandatory tests pass or have an active approved exception;
24. signing keys are absent from ordinary workers;
25. signing and publication have separate identities and receipts;
26. publication credentials are destination- and channel-scoped;
27. Release Sets pass compatibility validation;
28. Resource Governor limits are enforced and evidenced;
29. Resource pressure cannot suppress release gates;
30. SenTient and external AI are optional and non-authoritative;
31. logical data ownership is preserved;
32. worker cleanup is verified before reuse;
33. recovery does not promote partial output;
34. complete profile claims include tests, evidence, exceptions, and validity conditions;
35. active content is English;
36. no unresolved-authority marker or template token appears.

The validator reports actionable failures, including:

`text
build_farm_profile_contract_missing
build_farm_job_contract_incomplete
build_farm_source_revision_unresolved
build_farm_lockfile_missing
build_farm_dependency_source_unapproved
build_farm_worker_not_clean
build_farm_worker_isolation_failed
build_farm_shared_mutable_state
build_farm_toolchain_identity_missing
build_farm_mandatory_test_not_passed
build_farm_reproducibility_failed
build_farm_sbom_missing
build_farm_provenance_missing
build_farm_signing_boundary_violation
build_farm_publication_boundary_violation
build_farm_release_channel_invalid
build_farm_release_set_incompatible
build_farm_resource_limit_unenforced
build_farm_ai_input_not_reviewed
build_farm_cleanup_unverified
build_farm_claim_missing_evidence
`

## 11. Non-Normative Examples

### 11.1 Python service build

A job resolves an exact source revision, validates `pyproject.toml` and `uv.lock`, provisions an isolated worker, runs `uv sync --frozen`, executes tests, creates the service package, generates an SBOM and provenance, and stages the candidate in the services channel.

The worker is destroyed after outputs and evidence are collected.

### 11.2 Cache hit

A worker retrieves a compiler object from a content-addressed cache.

The object is verified before use. Deleting the cache would affect performance but not the job's authority or declared inputs.

### 11.3 Kubernetes implementation

A large farm uses Kubernetes Jobs.

Each job has a dedicated service account, bounded namespace resources, restricted network policy, isolated temporary storage, and no signing key. The produced application remains independent from Kubernetes APIs.

### 11.4 Non-Kubernetes implementation

A smaller farm uses rootless OCI containers managed by a local coordinator.

It satisfies the same worker identity, clean-state, resource, network, evidence, and cleanup requirements without claiming Kubernetes.

### 11.5 Multi-channel Release Set

One release process produces a system image, service containers, a governance policy bundle, and language packs.

Each artifact is independently built, tested, signed, and published in its channel. A Release Set records the compatible versions and passes compatibility validation before coordinated activation is permitted.

### 11.6 Signing outage

The build and tests pass, but the signing service is unavailable.

The candidate remains unsigned in controlled staging. The build farm reports a blocked signing stage and does not attempt publication.

### 11.7 Failed mandatory test

A service candidate passes unit tests but fails an integration contract test.

The candidate remains in staging and is not release eligible. Re-running the job requires a new recorded test result; the failed result is preserved.

### 11.8 Offline build

A farm with the `sovereign_offline` overlay imports a verified source bundle, dependency bundle, and toolchain bundle.

The build runs without external network access, records imported bundle identities, creates local provenance, and exports the signed candidate through a controlled transfer procedure.

### 11.9 SenTient analysis

An authorized job runs SenTient in an isolated workbench to suggest metadata for a knowledge artifact.

The result is reviewed and imported into the canonical source repository through an accepted change before a deterministic release build uses it.

### 11.10 Unverified cleanup

A worker's storage reset reports an error.

The worker is quarantined and later destroyed. It is not returned to the clean pool even though the previous build completed successfully.
