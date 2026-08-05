<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-019",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "profile:build_farm",
    "profile_conditioned_operations",
    "artifact_build_and_validation"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/build-farm.profile.json",
    "generated/toolchain-catalog.json",
    "contracts/toolchains/python-uv.toolchain.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-DOC-CHANGE-001"
  ],
  "requirement_ids": [
    "REQ-OPS-BF-001",
    "REQ-OPS-BF-002",
    "REQ-OPS-BF-003",
    "REQ-OPS-BF-004",
    "REQ-OPS-BF-005",
    "REQ-OPS-BF-006",
    "REQ-OPS-BF-007",
    "REQ-OPS-BF-008",
    "REQ-OPS-BF-009",
    "REQ-OPS-BF-010",
    "REQ-OPS-BF-011",
    "REQ-OPS-BF-012",
    "REQ-OPS-BF-013",
    "REQ-OPS-BF-014",
    "REQ-OPS-BF-015",
    "REQ-OPS-BF-016",
    "REQ-OPS-BF-017",
    "REQ-OPS-BF-018",
    "REQ-OPS-BF-019",
    "REQ-OPS-BF-020",
    "REQ-OPS-BF-021",
    "REQ-OPS-BF-022",
    "REQ-OPS-BF-023",
    "REQ-OPS-BF-024",
    "REQ-OPS-BF-025",
    "REQ-OPS-BF-026",
    "REQ-OPS-BF-027",
    "REQ-OPS-BF-028",
    "REQ-OPS-BF-029",
    "REQ-OPS-BF-030",
    "REQ-OPS-BF-031",
    "REQ-OPS-BF-032",
    "REQ-OPS-BF-033",
    "REQ-OPS-BF-034",
    "REQ-OPS-BF-035",
    "REQ-OPS-BF-036",
    "REQ-OPS-BF-037",
    "REQ-OPS-BF-038",
    "REQ-OPS-BF-039",
    "REQ-OPS-BF-040",
    "REQ-OPS-BF-041",
    "REQ-OPS-BF-042",
    "REQ-OPS-BF-043",
    "REQ-OPS-BF-044",
    "REQ-OPS-BF-045",
    "REQ-OPS-BF-046",
    "REQ-OPS-BF-047",
    "REQ-OPS-BF-048"
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
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-015",
    "LOCK-DOC-020",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-OPS-000",
    "DOC-OPS-009",
    "DOC-DEV-001",
    "DOC-DEV-002",
    "DOC-DEV-003",
    "DOC-DEV-004",
    "DOC-DEV-005",
    "DOC-DEV-006",
    "DOC-DEV-016",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004",
    "DOC-LIFE-012",
    "DOC-LIFE-018",
    "DOC-LIFE-019",
    "DOC-SEC-001",
    "DOC-SEC-019"
  ],
  "tags": [
    "operations",
    "build-farm",
    "build-workers",
    "job-isolation",
    "oci-runtime",
    "reproducible-builds",
    "toolchains",
    "provenance",
    "sbom",
    "artifact-candidates",
    "resource-governance",
    "worker-quarantine",
    "cache-safety",
    "supply-chain"
  ]
}
KOA:DOC-META:END -->

# Build Farm Operations

## 1. Purpose

This document defines how the kOA build farm executes reproducible builds, validation, packaging, and candidate-artifact production without gaining product, signing, publication, activation, policy, or data authority beyond its registered role.

The build farm exists to transform declared inputs into traceable candidate outputs:

`text
accepted change and exact source
 ↓
admitted isolated job
 ↓
clean worker and declared toolchains
 ↓
reproducible build
 ↓
candidate artifact identity
 ↓
tests, provenance, SBOM, and evidence
 ↓
publication request
 ↓
immutable published artifact
`

The build farm produces evidence and candidates.

It does not decide that a candidate becomes active.

Its core operating properties are:

- clean and isolated jobs;
- replaceable workers;
- exact inputs;
- declared toolchains;
- OCI-compatible execution;
- bounded resources;
- denied-by-default network access;
- cache subordination;
- provenance;
- accurate test results;
- worker quarantine;
- separation of build, signing, publication, and activation;
- capability-scoped degradation.

### 1.1 Operating objectives

The build farm aims to:

1. reproduce release artifacts from declared inputs;
2. prevent cross-job and cross-tenant contamination;
3. keep workers disposable and recoverable;
4. preserve source, dependency, and toolchain provenance;
5. identify every candidate before validation;
6. produce reliable tests and evidence;
7. protect signing and production authority from build workers;
8. scale without making Kubernetes or one runtime an application requirement;
9. isolate optional research workloads;
10. retain enough evidence to diagnose and reproduce failures.

### 1.2 Trust position

A build result is untrusted until the applicable build, integrity, provenance, reproducibility, validation, and evidence gates pass.

A passing build remains a candidate.

A published artifact remains inactive until the release lifecycle selects and activates it.

## 2. Scope

### 2.1 Included workloads

This document applies to build-farm jobs for:

- service artifacts;
- container images;
- system artifacts;
- policy bundles;
- language and runtime packs;
- knowledge artifacts;
- kOA Mediatheque and media artifacts;
- UCKK publication-package and adapter artifacts;
- documentation packages;
- generated catalogs and AI context packages;
- offline bundles;
- Sovereignty Bundles;
- migration and forward-repair artifacts;
- SBOMs and provenance;
- component, profile, integration, artifact, and Release Set validation;
- reproducibility checks;
- security and supply-chain checks.

### 2.2 Included infrastructure

The operating model covers:

- schedulers;
- queues;
- worker pools;
- worker images;
- OCI runtimes;
- optional orchestration;
- toolchain inventories;
- dependency mirrors;
- source mirrors;
- artifact staging;
- caches;
- secret references;
- network policy;
- resource envelopes;
- provenance services;
- evidence storage;
- quarantine;
- recovery;
- handoff;
- decommissioning.

### 2.3 Excluded scope

This document does not define:

- one continuous-integration vendor;
- one cloud provider;
- one scheduler;
- one container runtime;
- one Kubernetes distribution;
- one artifact repository;
- exact worker counts;
- exact queue priorities;
- exact CPU or memory values;
- exact cache product;
- exact build commands;
- exact release-signing implementation;
- production activation procedures.

Those details belong to the active build-farm profile, toolchain contracts, artifact contracts, security contracts, operations configuration, or non-normative runbooks.

### 2.4 Profile applicability

The build farm is a primary deployment profile.

It is not a mode of a developer workstation.

A developer workstation can run local builds, but a release-grade build claim must satisfy the same declared inputs, isolation, reproducibility, provenance, tests, and evidence required by the artifact class.

### 2.5 Kubernetes boundary

Kubernetes can be selected by the build-farm profile when scale, worker diversity, queueing, or operational isolation justify it.

Kubernetes is not required for build-farm conformance.

Job and artifact contracts remain expressed in runtime-independent terms unless the active profile explicitly adopts runtime-specific behavior.

### 2.6 OCI runtime boundary

The build farm provides an OCI-compatible runtime for containerized jobs.

The profile can select Podman, Docker, containerd, Kubernetes-backed execution, or another compatible runtime.

Runtime selection does not change component, artifact, profile, or release authority.

## 3. Canonical References

### 3.1 Build-farm profile

`text
contracts/profiles/build-farm.profile.json
generated/profile-catalog.json
`

The profile owns:

- topology;
- worker classes;
- runtime selection;
- resource envelopes;
- network model;
- security strengthening;
- availability;
- recovery;
- conformance.

### 3.2 Toolchains

`text
generated/toolchain-catalog.json
contracts/toolchains/python-uv.toolchain.json
`

Toolchain contracts own exact versions, lock behavior, build inputs, environment rules, and reproducibility expectations.

### 3.3 Components and artifacts

`text
generated/component-catalog.json
generated/component-catalog.json
contracts/artifact-classes.contract.json
contracts/release-channels.contract.json
contracts/artifact-contracts/*.schema.json
`

### 3.4 Provenance, tests, and evidence

`text
contracts/artifact-contracts/provenance-receipt.schema.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
`

### 3.5 Authority and decisions

`text
generated/authority-manifest.json
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
`

### 3.6 Related documents

`text
05-development/06-service-containers.md
05-development/16-development-to-release-transition.md
06-lifecycle/12-artifact-verification.md
06-lifecycle/18-sbom-provenance-and-signing.md
06-lifecycle/19-artifact-retention.md
07-security/01-security-baseline.md
07-security/19-software-supply-chain.md
08-operations/00-operating-model.md
08-operations/09-restore.md
`

## 4. Model and Responsibilities

### 4.1 Authority model

The build farm coordinates several owners.

| Fact | Primary owner |
| --- | --- |
| Source and change packet | Source owner and accepted change process |
| Artifact structure and lifecycle | Artifact class owner |
| Component compatibility | Component owner |
| Target deployment behavior | Profile owner |
| Build toolchain | Toolchain owner |
| Job resource admission | Resource Governor or profile-equivalent |
| Governance decisions | Governance Policy Runtime where selected |
| Worker identity and trust | Identity and Trust |
| Build execution | Build-farm operator and worker runtime |
| Candidate artifact identity | Artifact build workflow |
| Publication | Artifact-publication authority |
| Signing | Release-signing authority |
| Activation | Release and target-environment authority |
| Evidence | Evidence owner and Audit Broker |

The build-farm operator does not become the owner of source, artifacts, production data, signing keys, or active releases.

### 4.2 Job identity

Every job has a stable identity.

A job record includes:

- job identity;
- request identity;
- change packet;
- source revision;
- artifact class;
- target profile or platform;
- target architecture;
- toolchain set;
- dependency lock state;
- build definition;
- resource envelope;
- network mode;
- required secrets;
- expected outputs;
- tests;
- evidence;
- retry and timeout behavior;
- terminal disposition.

A retry receives either a new attempt identity under the same immutable job request or a new job identity when inputs change.

### 4.3 Worker identity

A worker record includes:

- worker identity;
- pool;
- worker image or host identity;
- effective profile;
- runtime inventory;
- architecture;
- trust state;
- network policy;
- storage state;
- cache policy;
- resource envelope;
- secret-access scope;
- health;
- readiness;
- lifecycle state;
- last clean reset;
- current job;
- quarantine history.

A hostname alone is not sufficient worker identity.

### 4.4 Worker lifecycle

A conceptual worker lifecycle is:

`text
provisioning
 ↓
verifying
 ↓
ready
 ↓
assigned
 ↓
running
 ↓
cleaning
 ↓
ready
`

Exceptional transitions include:

`text
verifying → blocked
running → failed
running → quarantined
cleaning → quarantined
ready → draining
draining → retired
`

The profile owns exact state identifiers.

### 4.5 Job lifecycle

A conceptual job lifecycle is:

`text
submitted
 ↓
validated
 ↓
admitted
 ↓
queued
 ↓
assigned
 ↓
preparing
 ↓
running
 ↓
validating
 ↓
collecting_evidence
 ↓
completed
`

Other terminal or blocked states can include:

- rejected;
- cancelled;
- timed out;
- failed;
- blocked;
- quarantined;
- evidence incomplete;
- non-publishable;
- superseded.

A job is not complete merely because the build command exited successfully.

### 4.6 Clean job workspace

Every job receives isolated mutable state.

Isolation covers:

- source checkout;
- generated files;
- dependency environments;
- `.venv`;
- service containers;
- networks;
- volumes;
- databases;
- ports;
- secrets;
- temporary files;
- logs;
- package-manager state;
- test fixtures;
- caches that are writable by the job.

Read-only shared inputs can be used only when their identity and integrity are verified.

### 4.7 Python environments

A Python job uses UV according to the active toolchain contract.

The job environment includes:

- declared Python version;
- lock state;
- job-local or workspace-local `.venv`;
- declared indexes or mirrors;
- isolated install state;
- no workstation-global dependency assumptions.

A shared download cache can improve performance.

It remains separate from the installed environment and is verified before use.

### 4.8 Toolchain inventory

The build farm maintains an inventory of available toolchains.

A toolchain entry identifies:

- toolchain identity;
- version;
- artifact identity;
- supported architectures;
- supported job classes;
- source;
- provenance;
- trust;
- lifecycle state;
- compatibility;
- deprecation;
- last verification.

A toolchain becomes available to jobs only after verification and profile selection.

### 4.9 Base and worker images

Worker and base images are immutable release artifacts or verified profile-owned images.

They identify:

- source;
- build definition;
- packages;
- runtime;
- toolchains;
- security configuration;
- provenance;
- dependency inventory;
- supported jobs;
- trust;
- lifecycle state.

A mutable image tag can be a human-friendly alias.

The resolved immutable identity is recorded in the job.

### 4.10 Source acquisition

Source acquisition uses the exact declared revision.

The build farm verifies:

- repository or source-package identity;
- revision;
- submodules or nested sources;
- vendored dependencies;
- generated-source inputs;
- change packet;
- integrity;
- access scope.

An uncommitted developer file cannot enter release input through a workspace mount.

### 4.11 Dependency acquisition

Dependencies use locked or immutable references.

The job records:

- dependency identity;
- version;
- source or mirror;
- integrity;
- artifact class;
- license or policy data where required;
- architecture;
- cache result;
- offline retention or reproducibility method.

A network response is not a build input until its identity is captured and verified.

### 4.12 Network modes

A job selects one network mode.

| Mode | Meaning |
| --- | --- |
| `none` | No network access |
| `declared_inputs_only` | Access only to declared source and dependency endpoints |
| `test_fixture_network` | Access only to isolated test services |
| `integration_test_network` | Access only to registered integration-test endpoints |
| `publication_request_only` | Access only to the publication boundary after validation |

The canonical enum belongs to the profile or job schema.

Undeclared egress blocks the job and can quarantine the worker.

### 4.13 Cache model

Caches can include:

- source mirrors;
- dependency downloads;
- OCI layers;
- compiler outputs;
- test fixtures;
- generated intermediate objects.

Caches remain:

- derived;
- integrity-checked;
- namespaced where mutable;
- invalidatable;
- bounded;
- observable;
- outside authoritative release identity.

A cache key includes every semantic input required by its cache contract.

Unknown or incomplete keys force a miss.

### 4.14 Cache poisoning controls

Cache protection can include:

- immutable objects;
- verified digests;
- writer identity;
- tenant or trust-domain separation;
- signed metadata;
- provenance;
- negative cache tests;
- rebuild comparison;
- quarantine;
- eviction.

A suspicious cache result is isolated and the job repeats without it.

### 4.15 Scheduling

The scheduler places jobs according to:

- job class;
- architecture;
- toolchains;
- runtime;
- profile;
- security domain;
- network mode;
- resource envelope;
- secret scope;
- worker trust;
- queue priority;
- data sensitivity;
- optional locality.

A scheduler assignment is resource authority, not publication or data authority.

### 4.16 Queue classes

Queue classes can distinguish:

- release-blocking builds;
- security repair;
- reproducibility verification;
- component validation;
- profile validation;
- routine candidate builds;
- documentation generation;
- optional research;
- SenTient tasks.

Priority policy protects critical release and recovery work from optional heavy jobs.

The exact classes and weights belong to the profile.

### 4.17 Resource envelopes

Each job declares:

- CPU;
- memory;
- process count;
- storage;
- I/O;
- network;
- concurrency;
- wall-clock time;
- queue lifetime;
- output size;
- archive expansion;
- retry count.

Resource admission can reject or defer a valid job.

It does not change the job's governance approval or artifact semantics.

### 4.18 Secrets and credentials

Build-farm credentials are separated by purpose.

Possible classes include:

- source read;
- dependency read;
- private artifact read;
- candidate upload;
- provenance submission;
- evidence submission;
- external test provider;
- publication request;
- worker enrollment.

Release-signing and production-activation credentials remain outside ordinary workers.

Secrets are resolved by protected reference and revoked after the job or worker lifecycle requires it.

### 4.19 Production-data boundary

Release builds and validation do not require unrestricted production data.

Tests use:

- synthetic data;
- minimized fixtures;
- approved snapshots;
- generated data;
- explicitly authorized restricted test sets.

Restricted data receives tenant, domain, privacy, rights, encryption, retention, and evidence controls.

A build worker does not become an application data processor by default.

### 4.20 SenTient on the build farm

SenTient can run as an optional isolated task.

It uses:

- explicit job request;
- separate workspace;
- separate dependencies;
- separate storage;
- separate service identity;
- separate secrets;
- resource envelope;
- controlled inputs;
- candidate outputs;
- provenance;
- destination adoption.

SenTient is not part of release correctness unless an accepted artifact contract explicitly requires a non-AI deterministic output that is independently validated.

Its output cannot directly alter canonical source or release state.

### 4.21 External AI boundary

External AI can assist a person or controlled workflow only through an approved integration.

Build-farm jobs do not silently call ChatGPT, Suno, Gamma, or external voice services.

External outputs remain candidate inputs and cannot support a passing release gate without controlled adoption and complete downstream validation.

### 4.22 Build execution

The worker executes only the declared build definition.

Execution records:

- start and end;
- commands or build steps by stable identifier;
- toolchain versions;
- environment;
- network mode;
- resource use;
- inputs;
- outputs;
- warnings;
- failures;
- cancellation;
- provenance events.

A build script does not gain permission to escape its job boundary.

### 4.23 Candidate artifact identity

Outputs receive candidate identities before tests depend on them.

The candidate record identifies:

- artifact class;
- version;
- immutable identity;
- content location;
- source;
- build;
- target;
- provenance;
- lifecycle state.

A changed output receives a new candidate identity.

### 4.24 Reproducibility verification

Reproducibility can use:

- independent rebuild;
- second worker;
- different clean pool;
- cache-disabled rebuild;
- normalized comparison;
- semantic comparison defined by the artifact class.

The comparison records allowed non-semantic differences.

Unexplained differences block publication and can trigger worker or toolchain quarantine.

### 4.25 Validation

Validation can include:

- schema;
- unit;
- component contract;
- integration;
- profile;
- security;
- migration;
- recovery;
- artifact;
- offline;
- documentation;
- Release Set compatibility.

The job record distinguishes:

- required tests;
- optional tests;
- not applicable tests;
- executed tests;
- unavailable tests;
- skipped tests;
- blocked tests.

Only actual terminal results support claims.

### 4.26 Provenance

Provenance links:

- job request;
- worker;
- source;
- change packet;
- decisions;
- toolchains;
- dependencies;
- base and worker images;
- environment;
- network mode;
- build steps;
- outputs;
- tests;
- evidence;
- publication request.

Provenance is immutable evidence.

It does not replace semantic validation.

### 4.27 SBOM and dependency inventory

Applicable artifacts carry a registered dependency inventory.

The inventory covers the scope defined by the artifact class.

It can include:

- packages;
- libraries;
- base-image contents;
- embedded tools;
- generated dependencies;
- licenses;
- source relationships.

The inventory is tied to the exact candidate.

### 4.28 Publication boundary

A validated candidate enters publication through a registered request.

The publication boundary verifies:

- candidate identity;
- artifact class;
- target release channel;
- provenance;
- SBOM;
- signatures or signing readiness;
- tests;
- evidence;
- compatibility metadata;
- approvals;
- lifecycle state.

The build worker does not mark the artifact active.

### 4.29 Signing separation

Signing authority is isolated from build execution.

A signing service receives:

- exact candidate identity;
- approved signing request;
- artifact class;
- release channel;
- validation and evidence references;
- signer policy.

Signing produces a receipt.

It does not rebuild or modify the candidate.

### 4.30 Worker health and readiness

Health can report process and runtime responsiveness.

Readiness also verifies:

- worker identity;
- trust and revocation;
- worker image;
- runtime;
- storage;
- network policy;
- resource headroom;
- clock;
- secret path;
- cache policy;
- cleanup state;
- evidence path;
- no active quarantine.

A healthy but unready worker receives no jobs.

### 4.31 Worker drift

Drift can include:

- changed packages;
- changed runtime;
- changed toolchain;
- changed network rules;
- changed credentials;
- changed kernel or host;
- undeclared persistent state;
- changed cache policy;
- changed worker image.

Unexpected drift blocks readiness.

The worker is reset from a verified baseline or quarantined.

### 4.32 Quarantine

A worker enters quarantine for conditions such as:

- suspected compromise;
- secret exposure;
- cross-job contamination;
- unexplained output variance;
- integrity failure;
- trust failure;
- undeclared egress;
- cleanup failure;
- cache poisoning;
- repeated isolation failure.

Quarantine removes:

- scheduler eligibility;
- publication access;
- trusted cache write access;
- ordinary credentials;
- normal network access.

Evidence collection remains bounded and protected.

### 4.33 Cleanup

Job cleanup handles:

- processes;
- containers;
- networks;
- volumes;
- databases;
- `.venv`;
- temporary files;
- credentials;
- sockets;
- logs;
- test services;
- writable caches;
- output staging.

Artifacts and evidence explicitly retained by policy remain.

Cleanup verification occurs before the worker returns to readiness.

### 4.34 Worker reset

A worker reset returns to a verified clean image or host baseline.

Reset verifies:

- worker identity;
- image identity;
- trust;
- runtime;
- storage cleanliness;
- network policy;
- resource state;
- secret state;
- cache state;
- evidence path.

Repairing unknown contamination in place is avoided.

### 4.35 Worker pools

Pools can separate:

- architecture;
- toolchain;
- artifact class;
- trust domain;
- network mode;
- restricted data;
- high assurance;
- offline or hermetic builds;
- optional research.

A job cannot cross pool boundaries unless its request and profile permit it.

### 4.36 Scaling

Scaling changes worker capacity, not artifact authority.

Scaling can add or remove:

- workers;
- pools;
- queue capacity;
- storage;
- cache nodes;
- OCI runtime capacity;
- Kubernetes nodes where selected.

New capacity passes identity, trust, image, network, resource, and readiness checks before receiving jobs.

### 4.37 Offline and hermetic builds

A build that claims offline or hermetic behavior has local closure for:

- source;
- dependencies;
- toolchains;
- base images;
- worker image;
- tests;
- provenance;
- evidence.

Missing inputs block the job.

The farm does not retrieve undeclared content silently.

### 4.38 Failure isolation

A failure is scoped to the smallest affected unit:

- job;
- worker;
- pool;
- toolchain;
- dependency source;
- cache;
- platform;
- artifact class;
- evidence service;
- publication boundary.

Unrelated jobs continue when their dependencies and authority remain valid.

### 4.39 Operational inventory

The build-farm inventory includes:

- scheduler version;
- profile and overlays;
- worker pools;
- workers;
- worker images;
- runtimes;
- toolchains;
- dependency mirrors;
- caches;
- network policies;
- credentials classes;
- queues;
- active jobs;
- quarantines;
- artifact staging;
- evidence paths;
- recovery state.

Inventory is reconciled with actual state and canonical contracts.

### 4.40 Backup and restore

Build-farm recovery prioritizes declarative reconstruction.

Retained recovery material includes:

- profile and configuration;
- scheduler and queue definitions;
- worker image identities;
- toolchain inventory;
- dependency mirror metadata;
- cache policy;
- trust and credential configuration;
- artifact and evidence references;
- runbooks;
- active incident and quarantine records.

Mutable workers are replaceable.

A recovery does not depend on restoring an unknown worker disk.

### 4.41 Handoffs

An operational handoff records:

- queue health;
- release-blocking jobs;
- failed and blocked gates;
- active publication requests;
- quarantined workers;
- degraded pools;
- capacity pressure;
- dependency or mirror incidents;
- credential incidents;
- cache incidents;
- evidence backlog;
- next safe actions.

### 4.42 Decommissioning

Decommissioning a build-farm object closes:

- scheduler selection;
- jobs;
- worker credentials;
- network access;
- cache write access;
- secret references;
- storage;
- logs;
- monitoring;
- alerts;
- inventory;
- runbooks;
- retained evidence.

Retired identifiers remain reserved according to lifecycle contracts.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-BF-001,REQ-OPS-BF-002,REQ-OPS-BF-003,REQ-OPS-BF-004,REQ-OPS-BF-005,REQ-OPS-BF-006,REQ-OPS-BF-007,REQ-OPS-BF-008,REQ-OPS-BF-009,REQ-OPS-BF-010,REQ-OPS-BF-011,REQ-OPS-BF-012,REQ-OPS-BF-013,REQ-OPS-BF-014,REQ-OPS-BF-015,REQ-OPS-BF-016,REQ-OPS-BF-017,REQ-OPS-BF-018,REQ-OPS-BF-019,REQ-OPS-BF-020,REQ-OPS-BF-021,REQ-OPS-BF-022,REQ-OPS-BF-023,REQ-OPS-BF-024,REQ-OPS-BF-025,REQ-OPS-BF-026,REQ-OPS-BF-027,REQ-OPS-BF-028,REQ-OPS-BF-029,REQ-OPS-BF-030,REQ-OPS-BF-031,REQ-OPS-BF-032,REQ-OPS-BF-033,REQ-OPS-BF-034,REQ-OPS-BF-035,REQ-OPS-BF-036,REQ-OPS-BF-037,REQ-OPS-BF-038,REQ-OPS-BF-039,REQ-OPS-BF-040,REQ-OPS-BF-041,REQ-OPS-BF-042,REQ-OPS-BF-043,REQ-OPS-BF-044,REQ-OPS-BF-045,REQ-OPS-BF-046,REQ-OPS-BF-047,REQ-OPS-BF-048 -->
- **REQ-OPS-BF-001 — SHALL:** Every build-farm job identify its source revision, change packet, artifact class, target profile or platform, toolchain set, dependency lock state, resource envelope, tests, evidence, and expected outputs before admission.
- **REQ-OPS-BF-002 — SHALL:** Every build-farm worker have an explicit worker identity, worker image or host identity, active profile, trust state, runtime inventory, resource envelope, and lifecycle state.
- **REQ-OPS-BF-003 — SHALL:** Build-farm jobs run in isolated clean workspaces with isolated services, networks, storage, secrets, processes, ports, caches, and temporary state.
- **REQ-OPS-BF-004 — SHALL NOT:** Two jobs share mutable dependency environments, mutable service volumes, mutable databases, mutable secrets, writable workspaces, or installed toolchain state.
- **REQ-OPS-BF-005 — SHALL:** The build farm provide an OCI-compatible runtime for containerized build and validation workloads.
- **REQ-OPS-BF-006 — SHALL NOT:** An application or component contract depend on build-farm runtime-specific behavior unless the active build-farm profile explicitly adopts that behavior.
- **REQ-OPS-BF-007 — SHALL NOT:** Kubernetes be required for build-farm conformance unless the active build-farm profile explicitly selects it for scale or orchestration.
- **REQ-OPS-BF-008 — SHALL:** Python build jobs use UV and a job-local or workspace-local `.venv` when the applicable toolchain contract selects Python.
- **REQ-OPS-BF-009 — SHALL NOT:** A build job use a workstation-global Python environment, mutable shared virtual environment, or undeclared system package as a release input.
- **REQ-OPS-BF-010 — SHALL:** Build inputs be exact, declared, integrity-verified, and either retained or reproducibly resolvable according to their contracts.
- **REQ-OPS-BF-011 — SHALL NOT:** Mutable tags, floating dependencies, undeclared network responses, uncommitted files, local overrides, or mutable shared cache state support a release or conformance claim.
- **REQ-OPS-BF-012 — SHALL:** Every release-grade build execute in a clean reproducible environment whose toolchains, base images, configuration, architecture, and network behavior are identified.
- **REQ-OPS-BF-013 — SHALL:** Every build output receive a candidate artifact identity before validation or publication.
- **REQ-OPS-BF-014 — SHALL:** Every candidate artifact carry provenance linking source, decisions, profiles, component contracts, toolchains, dependencies, environment, build steps, tests, evidence, and outputs.
- **REQ-OPS-BF-015 — SHALL:** Applicable software artifacts include an SBOM or equivalent registered dependency inventory.
- **REQ-OPS-BF-016 — SHALL:** Build-farm caches remain derived, integrity-checked, scoped, invalidatable, and unable to replace declared source, lock state, toolchains, or artifact identity.
- **REQ-OPS-BF-017 — SHALL NOT:** A cache hit alone prove reproducibility, provenance, compatibility, or test execution.
- **REQ-OPS-BF-018 — SHALL:** Job scheduling and resource admission be governed by Resource Governor or the active profile's equivalent resource authority.
- **REQ-OPS-BF-019 — SHALL NOT:** Governance Policy Runtime be merged with queue scheduling, worker placement, CPU allocation, memory allocation, or job-priority execution.
- **REQ-OPS-BF-020 — SHALL:** Queues, retries, attempts, concurrency, CPU, memory, process count, I/O, network, storage, and execution time be explicitly bounded.
- **REQ-OPS-BF-021 — SHALL:** The scheduler preserve reserved capacity for trust verification, provenance, evidence durability, worker recovery, and critical release validation before optional or heavy experimental work.
- **REQ-OPS-BF-022 — SHALL:** SenTient workloads on the build farm remain optional, isolated, task-activated, resource-bounded, and non-authoritative.
- **REQ-OPS-BF-023 — SHALL NOT:** External AI or SenTient output directly approve, sign, publish, activate, or mutate canonical release authority.
- **REQ-OPS-BF-024 — SHALL:** Build workers use dedicated scoped credentials and secret references for source, dependency, artifact, evidence, and provider access.
- **REQ-OPS-BF-025 — SHALL NOT:** Build workers receive unrestricted production data, production application credentials, root trust custody, broad release-signing authority, or production activation authority.
- **REQ-OPS-BF-026 — SHALL:** Build, validation, artifact-publication, release-signing, and activation credentials remain separate authority classes.
- **REQ-OPS-BF-027 — SHALL:** Network access default to deny and permit only declared sources, registries, repositories, endpoints, directions, protocols, identities, and purposes.
- **REQ-OPS-BF-028 — SHALL:** Jobs that claim hermetic or offline reproducibility execute without undeclared network access.
- **REQ-OPS-BF-029 — SHALL:** Every test result identify the exact candidate, job, worker, profile, toolchain, environment, test, terminal result, and evidence.
- **REQ-OPS-BF-030 — SHALL NOT:** A skipped, unavailable, blocked, incomplete, stale, manually asserted, or not-executed test be represented as passing.
- **REQ-OPS-BF-031 — SHALL:** Required test or evidence failure keep the candidate in a non-publishable state.
- **REQ-OPS-BF-032 — SHALL:** Published artifacts be the exact immutable candidate identities that passed the required build, reproducibility, validation, and evidence gates.
- **REQ-OPS-BF-033 — SHALL NOT:** Promotion rebuild or mutate artifact content while preserving the prior artifact identity.
- **REQ-OPS-BF-034 — SHALL:** The build farm publish only through the registered artifact-publication boundary and applicable release channel.
- **REQ-OPS-BF-035 — SHALL NOT:** The build farm activate a Release Set, change active policy, perform production migrations, or grant production privilege merely because a candidate passed validation.
- **REQ-OPS-BF-036 — SHALL:** Worker health remain distinct from worker readiness, and readiness include trust, runtime, storage, network policy, resource, cache, secret, clock, and evidence-path checks.
- **REQ-OPS-BF-037 — SHALL:** A worker suspected of compromise, drift, cross-job contamination, trust failure, or unexplained output variance enter quarantine and stop accepting new jobs.
- **REQ-OPS-BF-038 — SHALL:** Quarantined workers preserve required diagnostics and evidence while remaining isolated from normal scheduling, artifact publication, credentials, and trusted caches.
- **REQ-OPS-BF-039 — SHALL:** Mutable job state be destroyed or explicitly retained according to the job and evidence policy after terminal disposition.
- **REQ-OPS-BF-040 — SHALL:** Worker reset or replacement restore a verified clean baseline rather than repairing unknown mutable state in place.
- **REQ-OPS-BF-041 — SHALL:** Base images, worker images, toolchains, dependency mirrors, and cache policy changes use accepted lifecycle, validation, rollout, rollback, and evidence.
- **REQ-OPS-BF-042 — SHALL:** Build-farm observability expose queue state, worker state, job state, resource pressure, cache behavior, dependency failures, provenance status, test status, and evidence status while excluding secrets and unrestricted source or payload content.
- **REQ-OPS-BF-043 — SHALL:** Operational handoffs identify active jobs, blocked gates, quarantined workers, capacity risks, dependency incidents, credential incidents, pending publication, and next safe actions.
- **REQ-OPS-BF-044 — SHALL:** Build-farm failure degrade only affected jobs, workers, pools, platforms, or artifact classes while preserving unrelated build and validation capability.
- **REQ-OPS-BF-045 — SHALL NOT:** Failure activate a silent toolchain, dependency source, cache source, worker image, external AI provider, credential, policy, or publication fallback.
- **REQ-OPS-BF-046 — SHALL:** Build-farm backup and restore preserve worker definitions, scheduler state required for reconciliation, toolchain and base-image inventories, artifact and evidence references, trust configuration, and recovery procedures without treating mutable workers as irreplaceable pets.
- **REQ-OPS-BF-047 — SHALL:** Decommissioning a worker, pool, runtime, cache, toolchain, or build-farm environment revoke credentials, close network paths, reconcile jobs, preserve required artifacts and evidence, clear mutable state, update inventories, and reserve retired identifiers where applicable.
- **REQ-OPS-BF-048 — SHALL:** A semantic change to build-farm authority, job isolation, runtime, toolchains, caches, credentials, scheduling, network, provenance, validation, publication, quarantine, recovery, or decommissioning use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Admit a build job

1. Receive the immutable job request.
2. verify source revision and change packet.
3. resolve artifact class and target profile or platform.
4. resolve toolchains, dependencies, base images, and worker requirements.
5. resolve resource envelope and network mode.
6. resolve secrets and credentials classes.
7. resolve required tests and evidence.
8. evaluate governance decisions where required.
9. evaluate resource admission.
10. reject unresolved or incompatible requests.
11. assign the job identity and queue class.
12. record admission evidence.

### 6.2 Prepare a worker

1. Select a compatible ready worker.
2. verify worker identity and trust.
3. verify worker image, runtime, architecture, and toolchains.
4. verify network policy.
5. verify storage cleanliness and capacity.
6. verify secret and evidence paths.
7. allocate isolated workspace, services, networks, and volumes.
8. allocate resource limits.
9. materialize exact source and declared inputs.
10. record preparation state before execution.

### 6.3 Execute a build

1. Verify the final input manifest.
2. start the declared clean environment.
3. resolve dependencies through permitted sources.
4. execute declared build steps.
5. record toolchain and environment identity.
6. enforce network and resource limits.
7. capture outputs and diagnostics.
8. assign candidate identities.
9. generate provenance and dependency inventory.
10. mark the job ready for validation or failed.

### 6.4 Verify reproducibility

1. Select an independent clean execution context.
2. disable or segregate caches as required.
3. rebuild from the same declared inputs.
4. compare outputs under the artifact reproducibility contract.
5. explain permitted normalized differences.
6. reject unexplained variance.
7. quarantine suspicious worker, toolchain, or cache state.
8. attach comparison evidence to the candidate.

### 6.5 Run validation

1. Resolve the applicable test matrix.
2. provision isolated test services and fixtures.
3. verify candidate identity.
4. run required tests.
5. record actual terminal results.
6. collect evidence and diagnostics.
7. reject false or incomplete pass claims.
8. mark the candidate release-eligible only when every release-blocking gate passes.
9. preserve the candidate as non-authoritative.

### 6.6 Request publication

1. Freeze the candidate.
2. verify artifact class and release channel.
3. verify provenance and dependency inventory.
4. verify tests, evidence, approvals, and exceptions.
5. create a publication request for the exact candidate identity.
6. submit through the registered publication boundary.
7. receive the publication receipt.
8. preserve artifact identity.
9. leave activation to the release lifecycle.

### 6.7 Clean a completed job

1. Stop processes and test services.
2. revoke job-scoped credentials.
3. remove writable networks, volumes, databases, and temporary state.
4. remove the job-local `.venv`.
5. retain only declared outputs, diagnostics, and evidence.
6. verify no cross-job mutable state remains.
7. verify cache writes according to policy.
8. return the worker to verification.
9. mark it ready only after cleanup passes.

### 6.8 Quarantine a worker

1. Stop new scheduling.
2. stop or isolate the current job safely.
3. revoke ordinary credentials.
4. remove publication and trusted-cache access.
5. isolate network and storage.
6. preserve required diagnostics and evidence.
7. identify affected jobs, candidates, caches, and secrets.
8. invalidate or reverify affected outputs.
9. reset from a clean baseline or retire the worker.
10. record quarantine and final disposition.

### 6.9 Rotate a worker or base image

1. Publish the new immutable image candidate.
2. verify provenance, dependency inventory, and security checks.
3. test representative job classes.
4. verify reproducibility and compatibility.
5. stage a canary pool.
6. compare outputs and worker behavior.
7. expand rollout gradually.
8. preserve previous known-good images.
9. rollback or repair on failure.
10. update inventories and evidence.

### 6.10 Handle dependency-source failure

1. Identify affected source, mirror, packages, jobs, and artifact classes.
2. stop new affected jobs.
3. preserve running jobs only when inputs are already complete and verified.
4. avoid silent alternate mirrors.
5. verify an approved alternate source if the profile permits it.
6. update the declared input manifest.
7. create new attempts where inputs change.
8. record degradation and recovery evidence.

### 6.11 Recover the build farm

1. Provision scheduler and control services from verified artifacts.
2. restore profile configuration, queues, policies, and inventories.
3. restore trust and credential references.
4. restore toolchain and worker-image inventories.
5. restore or rebuild dependency mirrors according to policy.
6. provision clean workers.
7. verify worker readiness.
8. reconcile active, failed, and indeterminate jobs.
9. reconcile candidate artifacts and evidence.
10. resume scheduling gradually.
11. record recovery acceptance.

### 6.12 Decommission a worker or pool

1. Stop new assignments.
2. drain, cancel, or relocate jobs safely.
3. reconcile candidate artifacts and evidence.
4. revoke credentials and worker identity.
5. remove network and cache access.
6. clear mutable storage.
7. remove monitoring and alerts.
8. update scheduler and inventories.
9. retain quarantine or incident evidence where required.
10. reserve retired identifiers.
11. verify unrelated capacity and job classes.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Job request is incomplete | Reject or block admission | Existing queues and workers | Affected job |
| Worker identity is unverifiable | Remove worker from scheduling | Other workers | Assignment |
| Worker is healthy but not ready | Keep worker idle | Other ready workers | New jobs on worker |
| Required toolchain is unavailable | Block affected job class | Other toolchains and jobs | Affected build |
| Source revision cannot be resolved | Block job | Existing artifacts and source records | Build |
| Dependency integrity fails | Quarantine dependency and affected cache entries | Other dependencies | Affected build |
| Undeclared network access occurs | Stop job and evaluate worker quarantine | Other jobs and workers | Affected job |
| Resource envelope is exceeded | Stop or fail job according to policy | Other jobs and reserved capacity | Unbounded continuation |
| Cache result is suspicious | Retry without cache and quarantine affected entry | Declared source and dependencies | Cache use |
| Build outputs vary unexpectedly | Block publication and investigate worker, toolchain, or input | Existing published artifacts | Candidate publication |
| Required test fails | Mark candidate non-publishable | Candidate diagnostics | Publication |
| Required test is unavailable or skipped | Mark validation blocked | Candidate and other jobs | Passing claim |
| Provenance generation fails | Mark candidate non-publishable | Build outputs and diagnostics | Publication |
| Evidence storage is unavailable | Apply evidence policy and block evidence-critical completion | Running job state where safe | Release claim |
| Candidate upload fails | Retain candidate in controlled staging | Other jobs | Publication |
| Signing service is unavailable | Keep candidate unsigned and inactive | Validated candidate | Signed publication |
| Publication boundary is unavailable | Retain validated candidate | Build and validation | Published state |
| Worker cleanup fails | Quarantine worker | Other workers | Reuse |
| Secret exposure is suspected | Stop affected jobs, revoke secrets, and quarantine worker | Other credential classes | Continued affected use |
| Worker compromise is suspected | Quarantine and reverify affected outputs | Other pools | Worker use and affected candidates |
| Scheduler fails | Stop new assignment and preserve job records | Running isolated jobs where safe | New scheduling |
| Queue backlog exceeds policy | Shed or defer lower-priority jobs | Release-blocking and protected work | New low-priority work |
| Optional SenTient pool fails | Disable affected optional jobs | Core build and validation | SenTient jobs |
| Complete validation cannot execute | Keep prior valid state | Existing published artifacts | New conformance claim |

Failure remains scoped to jobs, workers, pools, toolchains, caches, platforms, or artifact classes.

It does not authorize a silent toolchain, dependency, worker, cache, AI provider, credential, or publication fallback.

## 8. Cross-Component Interactions

### 8.1 Source and component owners

Source and component owners provide:

- exact source;
- accepted change identity;
- component contract;
- target profiles;
- tests;
- migration and compatibility expectations.

The build farm does not reinterpret component ownership.

### 8.2 Identity and Trust

Identity and Trust verifies:

- workers;
- schedulers;
- toolchains;
- base images;
- source artifacts;
- signers;
- publication requests.

It does not schedule jobs or decide candidate semantics.

### 8.3 Governance Policy Runtime

Governance Policy Runtime can evaluate:

- restricted source access;
- protected test data use;
- privileged build steps;
- exception use;
- publication requests.

It does not allocate workers or CPU.

### 8.4 Resource Governor

Resource Governor controls queue admission, placement, resource envelopes, and workload shedding.

It does not approve source, data access, signing, publication, or release activation.

### 8.5 Audit Broker

Audit Broker receives selected job, provenance, test, publication, quarantine, credential, and recovery evidence.

It does not store unrestricted source or build outputs by default.

### 8.6 Artifact publication

The publication boundary receives exact validated candidates.

It verifies artifact class, release channel, provenance, tests, evidence, and approvals.

The build farm cannot bypass it.

### 8.7 Signing authority

Signing is a separate protected service or workflow.

Build workers submit exact immutable candidates.

They do not hold unrestricted private signing keys.

### 8.8 Release Set lifecycle

Release Set assembly consumes published artifacts from the four channels.

The build farm can validate compatibility and produce candidate Release Sets.

It does not activate them in target environments.

### 8.9 Developer workstations

Developers submit source and change packets.

Their local mutable state does not become a release input.

The build farm independently resolves declared source and toolchains.

### 8.10 SenTient

SenTient can execute only in isolated optional build-farm jobs.

Its candidate outputs require destination review and acceptance.

Its failure does not affect core build-farm readiness.

### 8.11 External integrations

External sources and services remain registered integrations or dependency sources.

Their credentials, endpoints, terms, failures, and evidence remain explicit.

External AI is not a hidden build dependency.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-PROFILE-001` | Build-farm topology, worker pools, runtime, resources, and assurance remain profile-specific |
| `DEC-CONTAINER-001` | The build farm requires OCI compatibility but does not impose one runtime on application contracts |
| `DEC-K8S-001` | Kubernetes is permitted for build-farm scale but is not required for conformance |
| `DEC-DATA-001` | Build workers do not write foreign component state or receive production-data authority |
| `DEC-GOV-001` | Resource scheduling remains separate from governance policy |
| `DEC-REL-001` | Build outputs enter four independent channels only through artifact and Release Set lifecycle |
| `DEC-AI-001` | External AI remains optional, explicit, and non-authoritative |
| `DEC-SENT-001` | SenTient is an optional isolated developer and build workbench |
| `DEC-DOC-CHANGE-001` | Semantic build-farm changes use accepted decisions and transitive impact analysis |

### 9.2 Protected locks

| Lock group | Protected build-farm boundary |
| --- | --- |
| `LOCK-PROFILE-001` | Build-farm choices do not become global endpoint requirements |
| `LOCK-DEV-001` to `LOCK-DEV-005` | Jobs, dependencies, services, ports, data, and caches remain isolated |
| `LOCK-DATA-001` | Workers cannot write foreign authoritative state |
| `LOCK-GOV-001` | Scheduling and policy authority remain separate |
| `LOCK-AI-001`, `LOCK-AI-002` | No native or external AI release authority |
| `LOCK-SENT-001` | SenTient remains optional and non-authoritative |
| `LOCK-LIFE-001` to `LOCK-LIFE-004` | Candidates, publication, activation, recovery, Release Sets, and channels remain controlled |
| `LOCK-DOC-015`, `LOCK-DOC-020` | Major changes receive transitive impact and clean validation |
| `LOCK-IMPL-001`, `LOCK-IMPL-002` | Runtime and orchestration implementation do not redefine architecture |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- a CI vendor is the build-farm authority;
- a successful job is a release;
- a green pipeline proves every required test ran;
- a worker hostname identifies its full trust state;
- a long-lived worker is safer than a disposable worker;
- one shared writable workspace improves reproducibility;
- a shared `.venv` is an acceptable build optimization;
- a cache entry is a declared dependency;
- a cache hit proves reproducibility;
- a mutable image tag identifies the worker sufficiently;
- root inside a build container is harmless;
- a build worker can hold production signing keys;
- publication credentials and signing credentials are equivalent;
- a build worker can activate a release after publishing it;
- production data is needed for realistic validation by default;
- Kubernetes is required for a scalable build farm;
- Podman, Docker, or containerd behavior belongs in application contracts automatically;
- external network access is harmless during a hermetic build;
- the latest dependency can replace a locked dependency;
- a second attempt can reuse the same identity after inputs change;
- skipped tests can be reported as passing;
- unavailable evidence can be added after release activation;
- promotion can rebuild an artifact under the same identity;
- one unexplained reproducibility mismatch is acceptable;
- cleanup failure can be ignored on the next job;
- a compromised worker can be repaired manually and trusted immediately;
- a quarantined worker can continue writing trusted caches;
- optional SenTient output can approve a release;
- ChatGPT can generate release evidence;
- a scheduler decision grants data or publication authority;
- a runbook creates a toolchain exception;
- frequent manual patches become the worker baseline;
- retired worker or job identifiers can be reused;
- restoring one mutable worker disk is the preferred build-farm recovery strategy;
- current implementation behavior overrides profile and artifact contracts.

Missing source, toolchain, dependency, worker trust, resource, network, provenance, test, evidence, publication, or lifecycle authority blocks the affected job or candidate.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-OPS-019`;
2. the path is `08-operations/19-build-farm-operations.md`;
3. the active language is English;
4. every job identifies exact source, target, toolchains, dependencies, resources, tests, evidence, and outputs;
5. every worker has explicit identity, image, runtime, trust, resource, and lifecycle state;
6. job workspaces and mutable services are isolated;
7. no mutable dependency environment is shared;
8. the build farm exposes an OCI-compatible runtime;
9. application contracts remain runtime independent unless the profile explicitly adopts runtime behavior;
10. Kubernetes is not required unless the profile selects it;
11. Python jobs use UV and isolated `.venv`;
12. global or shared installed Python environments are absent from release inputs;
13. build inputs are exact and verified;
14. mutable tags, floating dependencies, and undeclared state are absent from release claims;
15. release builds run in clean reproducible environments;
16. candidate identities exist before validation;
17. provenance binds source, worker, toolchains, dependencies, tests, evidence, and outputs;
18. applicable dependency inventories are complete;
19. caches remain derived and non-authoritative;
20. cache hits do not support unsupported claims;
21. Resource Governor or profile-equivalent controls job resources;
22. resource scheduling remains separate from governance policy;
23. all queues and resources are bounded;
24. protected capacity is preserved;
25. SenTient remains optional, isolated, and non-authoritative;
26. external AI and SenTient cannot approve or activate releases;
27. credentials remain dedicated and scoped;
28. workers lack production data, signing custody, and activation authority;
29. build, signing, publication, and activation credentials remain separate;
30. network access defaults to deny;
31. hermetic claims have no undeclared egress;
32. every test result binds exact candidate, job, worker, environment, result, and evidence;
33. incomplete tests are not reported as passing;
34. failed gates keep candidates non-publishable;
35. publication uses the exact validated immutable candidate;
36. promotion does not rebuild content;
37. publication uses the registered boundary and release channel;
38. the build farm cannot activate releases or production policy;
39. health and readiness remain distinct;
40. suspicious workers enter quarantine;
41. quarantine blocks scheduling, publication, credentials, and trusted caches;
42. cleanup handles all mutable job state;
43. reset returns to a verified clean baseline;
44. worker and toolchain changes use lifecycle rollout and recovery;
45. observability is complete and minimized;
46. handoffs identify active jobs, failures, quarantine, capacity, credentials, and publication;
47. failure remains capability-scoped;
48. no silent fallback occurs;
49. recovery reconstructs declarative state and replaceable workers;
50. decommissioning closes all dependencies and reserves identifiers;
51. semantic changes include accepted decisions and impact analysis;
52. all 48 linked requirements resolve;
53. all required build-farm tests execute;
54. all required evidence validates;
55. no unresolved build-farm authority remains;
56. generated operating catalogs and AI context match canonical authority;
57. complete documentation validation passes.

Expected test coverage includes:

`text
TEST-OPS-BF-001 Job request completeness
TEST-OPS-BF-002 Worker identity and trust
TEST-OPS-BF-003 Cross-job workspace isolation
TEST-OPS-BF-004 Service, database, and secret isolation
TEST-OPS-BF-005 OCI-compatible runtime
TEST-OPS-BF-006 No mandatory Kubernetes dependency
TEST-OPS-BF-007 UV and job-local virtual environment
TEST-OPS-BF-008 Exact source and dependency closure
TEST-OPS-BF-009 No mutable release inputs
TEST-OPS-BF-010 Clean reproducible environment
TEST-OPS-BF-011 Candidate identity before validation
TEST-OPS-BF-012 Provenance completeness
TEST-OPS-BF-013 SBOM or dependency-inventory completeness
TEST-OPS-BF-014 Cache subordination and poisoning resistance
TEST-OPS-BF-015 Resource and queue bounds
TEST-OPS-BF-016 Scheduling and policy-authority separation
TEST-OPS-BF-017 SenTient isolation and non-authority
TEST-OPS-BF-018 Credential-class separation
TEST-OPS-BF-019 No production signing or activation authority
TEST-OPS-BF-020 Default-deny network behavior
TEST-OPS-BF-021 Hermetic-build egress denial
TEST-OPS-BF-022 Exact test-result binding
TEST-OPS-BF-023 No false pass for incomplete tests
TEST-OPS-BF-024 Reproducibility comparison
TEST-OPS-BF-025 Exact candidate publication
TEST-OPS-BF-026 No rebuild during promotion
TEST-OPS-BF-027 Worker readiness
TEST-OPS-BF-028 Worker quarantine
TEST-OPS-BF-029 Complete job cleanup
TEST-OPS-BF-030 Clean worker reset
TEST-OPS-BF-031 Capability-scoped failure
TEST-OPS-BF-032 Declarative build-farm recovery
TEST-OPS-BF-033 Complete worker and pool decommissioning
`

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid build-farm operation. They do not replace profile, toolchain, artifact, security, or runbook contracts.

### 11.1 Service-image build

A job identifies an exact Orgo source revision, service artifact class, target profile, OCI build definition, dependency lock state, tests, and evidence.

A clean worker builds the candidate image, generates provenance and an SBOM, runs component and profile tests, and submits the immutable candidate to publication.

The worker cannot activate the resulting service.

### 11.2 Python language-tooling job

A GF Wordbench support job uses the declared Python toolchain.

UV creates a job-local `.venv`.

The worker does not use a global Python installation beyond the declared interpreter and bootstrap contract.

The `.venv` is removed after the job.

### 11.3 Hermetic reproducibility job

A candidate is rebuilt in a second clean worker pool with network mode `none`.

All source, dependencies, toolchains, and base images are local verified inputs.

The artifact passes its normalized reproducibility comparison.

### 11.4 Cache poisoning suspicion

A dependency cache returns an object whose integrity does not match the declared identity.

The entry is quarantined.

The job retries from the declared source without the cache.

Affected workers and prior candidates are evaluated.

### 11.5 Worker quarantine

A worker produces unexplained output variance and retains a process after cleanup.

The scheduler removes it from service, credentials are revoked, and trusted-cache access closes.

Required diagnostics are retained.

The worker returns only after reset from a verified image and full readiness checks.

### 11.6 Kubernetes-backed pool

A large build farm uses Kubernetes for one worker pool.

Jobs still declare OCI inputs, resources, toolchains, network, outputs, tests, and evidence.

Endpoint and application contracts remain independent of Kubernetes.

### 11.7 Optional SenTient job

A developer submits a bounded SenTient enrichment task.

The task runs in an isolated optional pool with separate storage, credentials, and resources.

It produces a candidate artifact with provenance.

A destination workflow reviews the result before any canonical adoption.

### 11.8 Signing separation

A worker produces a validated policy-bundle candidate.

The worker submits its exact immutable identity to a separate signing workflow.

The signing service verifies the request and creates a signature receipt.

The worker never receives the private signing key.

### 11.9 Dependency-source outage

A declared dependency mirror becomes unavailable.

Affected jobs remain queued or blocked.

The farm does not switch silently to a public repository.

An approved alternate source creates a new attempt with updated declared inputs.

### 11.10 Invalid shared worker state

Two concurrent jobs use the same writable source directory, database, `.venv`, secret file, and output directory.

One job changes the other's dependencies and outputs.

The arrangement violates job isolation and cannot support release or conformance claims.
