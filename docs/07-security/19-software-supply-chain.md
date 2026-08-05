<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-019",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "software_supply_chain",
    "source_admission",
    "dependency_admission",
    "build_provenance",
    "artifact_admission",
    "release_promotion"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/ai_boundary",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/component-catalog.json#/components/audit_broker",
    "generated/profile-catalog.json",
    "contracts/profiles/build-farm.profile.json",
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
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-CONTAINER-001",
    "DEC-DATA-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-GOV-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-SEC-SC-001",
    "REQ-SEC-SC-002",
    "REQ-SEC-SC-003",
    "REQ-SEC-SC-004",
    "REQ-SEC-SC-005",
    "REQ-SEC-SC-006",
    "REQ-SEC-SC-007",
    "REQ-SEC-SC-008",
    "REQ-SEC-SC-009",
    "REQ-SEC-SC-010",
    "REQ-SEC-SC-011",
    "REQ-SEC-SC-012",
    "REQ-SEC-SC-013",
    "REQ-SEC-SC-014",
    "REQ-SEC-SC-015",
    "REQ-SEC-SC-016",
    "REQ-SEC-SC-017",
    "REQ-SEC-SC-018",
    "REQ-SEC-SC-019",
    "REQ-SEC-SC-020",
    "REQ-SEC-SC-021",
    "REQ-SEC-SC-022",
    "REQ-SEC-SC-023",
    "REQ-SEC-SC-024",
    "REQ-SEC-SC-025",
    "REQ-SEC-SC-026",
    "REQ-SEC-SC-027",
    "REQ-SEC-SC-028",
    "REQ-SEC-SC-029",
    "REQ-SEC-SC-030",
    "REQ-SEC-SC-031",
    "REQ-SEC-SC-032",
    "REQ-SEC-SC-033",
    "REQ-SEC-SC-034",
    "REQ-SEC-SC-035",
    "REQ-SEC-SC-036",
    "REQ-SEC-SC-037",
    "REQ-SEC-SC-038",
    "REQ-SEC-SC-039",
    "REQ-SEC-SC-040",
    "REQ-SEC-SC-041",
    "REQ-SEC-SC-042",
    "REQ-SEC-SC-043",
    "REQ-SEC-SC-044",
    "REQ-SEC-SC-045",
    "REQ-SEC-SC-046",
    "REQ-SEC-SC-047",
    "REQ-SEC-SC-048",
    "REQ-SEC-SC-049",
    "REQ-SEC-SC-050",
    "REQ-SEC-SC-051",
    "REQ-SEC-SC-052",
    "REQ-SEC-SC-053",
    "REQ-SEC-SC-054",
    "REQ-SEC-SC-055",
    "REQ-SEC-SC-056"
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
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-003",
    "DOC-DEV-013",
    "DOC-LIFE-006",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-017",
    "DOC-LIFE-018",
    "DOC-LIFE-019",
    "DOC-SEC-009"
  ],
  "tags": [
    "security",
    "software-supply-chain",
    "source-provenance",
    "dependency-integrity",
    "reproducible-builds",
    "clean-builders",
    "sbom",
    "provenance",
    "attestation",
    "signing",
    "artifact-admission",
    "release-set",
    "offline-bundle",
    "revocation"
  ]
}
KOA:DOC-META:END -->

# Software Supply Chain

> **Document status:** Normative security architecture.
> **Security objective:** Preserve exact identity, provenance, integrity, review, authority, and compatibility from source admission through artifact activation.
> **Authority rule:** No single repository, builder, registry, signer, verifier, release service, or operator owns the complete promotion chain.

## 1. Purpose

This document defines the kOA software supply-chain security model.

The model protects the path from source and dependencies to build outputs, evidence, signatures, releases, Release Sets, offline bundles, and active artifacts.

The supply chain provides assurance that an active artifact:

- originates from admitted source;
- uses declared dependencies and toolchains;
- was produced by an authorized clean builder;
- can be independently traced and, where claimed, reproduced;
- has an applicable SBOM and provenance;
- was signed by the correct authority;
- passed artifact admission;
- is compatible with its target profile and release channels;
- became active only through the appropriate release and activation authority;
- can be revoked, rebuilt, rolled back, or forward-repaired according to its lifecycle contract.

A valid digest or signature is necessary where required, but neither is sufficient to authorize activation.

## 2. Scope

### 2.1 Included scope

This document applies to:

- source repositories and source bundles;
- reviewed revisions, tags, commits, and generated source;
- vendored dependencies;
- package registries, mirrors, and repositories;
- dependency lock state;
- compilers, interpreters, package managers, generators, scanners, and build tools;
- container base images and build images;
- developer and build-farm handoff;
- clean and isolated build workers;
- build secrets;
- software bills of materials;
- provenance and attestations;
- signing keys and signing services;
- artifact stores and registries;
- artifact verification and admission;
- services, system, governance, and knowledge release channels;
- Release Sets;
- offline bundles;
- revocation, quarantine, rebuild, and recovery;
- optional AI-assisted and integration-assisted development.

### 2.2 Excluded scope

This document does not define:

- component business responsibilities;
- component-owned data schemas;
- profile-specific build technology;
- one mandatory source-control system;
- one package registry;
- one container registry;
- one transparency service;
- one signing implementation;
- one build orchestrator;
- production activation procedures beyond their supply-chain preconditions.

Those facts remain owned by component, profile, toolchain, artifact, release, integration, and lifecycle contracts.

### 2.3 Trust is not transitive by convenience

Trust in one supply-chain stage does not automatically trust another.

Examples:

- a reviewed commit does not prove a dependency is safe;
- a locked dependency does not prove its package bytes are authentic;
- an authentic package does not prove policy compatibility;
- a successful build does not prove reproducibility;
- a reproducible artifact does not prove release authorization;
- a valid signature does not prove the signer had current authority;
- registry presence does not prove admission;
- admission does not prove target compatibility;
- compatibility does not activate the artifact.

## 3. Canonical References

### 3.1 Canonical ownership

| Information | Canonical owner |
| --- | --- |
| Source repository and revision policy | Repository and development contracts |
| Dependency resolution and toolchain identity | Toolchain contracts |
| Build-farm capabilities and resource envelope | Build-farm profile |
| Component outputs, interfaces, and data boundaries | Component contracts |
| Artifact classes and lifecycle | Artifact classes registry and artifact contracts |
| Four release channels | Release-channels registry |
| Exact compatible channel versions | Release Set |
| Integration source and transfer boundaries | Integrations registry and integration manifests |
| Identity, keys, and trust | Identity and Trust |
| Governed exceptions, privilege, and approval | Governance Policy Runtime |
| Build resource constraints | Resource Governor |
| Receipts and retained security evidence | Audit Broker and evidence registry |
| Requirements and cross-file invariants | Requirements and locks registries |

### 3.2 Four-channel model

The release channels are:

`text
system
services
governance
knowledge
`

Software supply-chain evidence follows the artifact it describes but does not become an additional release channel.

A Release Set binds exact compatible versions across all four channels.

### 3.3 Intrinsic integrity material

The following are intrinsic supply-chain integrity material:

- cryptographic digests;
- signatures;
- signature certificates or trust chains;
- SBOMs;
- provenance;
- attestations;
- transparency references where adopted;
- sealed bundle manifests;
- decision and provenance receipts.

Their formats remain owned by applicable artifact, trust, and release contracts.

## 4. Model and Responsibilities

### 4.1 Supply-chain stages

The canonical stages are:

`text
source admission
→ dependency and toolchain resolution
→ clean build
→ build verification
→ SBOM and provenance generation
→ signing
→ artifact admission
→ release-channel publication
→ Release Set compatibility binding
→ transfer and staging
→ activation verification
`

A stage can reject a candidate without changing the active artifact.

### 4.2 Authority separation

| Authority | Responsibility |
| --- | --- |
| Source owner | Owns source revisions and review policy |
| Dependency and toolchain owner | Owns resolution, lock, source, and version rules |
| Build authority | Executes declared builds in controlled workers |
| Evidence producer | Produces tests, SBOM, provenance, and attestations |
| Signing authority | Signs exact approved statements and artifact identities |
| Artifact verifier | Verifies integrity, trust, provenance, evidence, and admissibility |
| Release authority | Publishes channel releases and Release Sets |
| Deployment authority | Admits and activates artifacts on target deployments |
| Identity and Trust | Resolves actors, services, builders, keys, certificates, and trust roots |
| Governance Policy Runtime | Decides governed exceptions and privileged supply-chain actions |
| Resource Governor | Limits builders, scanners, queues, storage, and repair work |
| Audit Broker | Retains required receipts and evidence |

One actor can perform multiple roles only when the applicable separation-of-duties policy permits it.

### 4.3 Source admission

An admitted source revision identifies:

- repository or source-bundle identity;
- immutable revision identity;
- source owner;
- review result;
- required signatures or trust evidence;
- generated or vendored content;
- applicable policy and exceptions;
- release intent.

A branch name is not an immutable revision identity.

Generated source identifies its generator, generator version, inputs, procedure, and review status.

### 4.4 Dependency resolution

Dependency state includes:

- direct declarations;
- transitive resolution;
- package source;
- exact package or image identity;
- integrity evidence;
- lock or immutable resolution record;
- policy and vulnerability disposition;
- applicable exceptions.

For Python, UV and `uv.lock` provide the registered resolution mechanism.

A content-addressed cache can accelerate retrieval. It does not replace dependency declarations, lock state, or artifact verification.

### 4.5 Toolchain identity

A toolchain identity covers every execution environment capable of changing output bytes or semantics, including:

- compiler or interpreter;
- build backend;
- package manager;
- code generator;
- linker and packager;
- container builder;
- scanner;
- compression and archive tool;
- operating environment where material to output;
- declared build parameters.

Toolchain drift produces a different build environment and requires explicit compatibility or reproduction analysis.

### 4.6 Clean build model

A clean builder starts from a verified baseline and receives only declared inputs.

It does not inherit:

- developer home state;
- arbitrary environment variables;
- unrelated credentials;
- untracked source;
- mutable local package installations;
- undeclared network services;
- unrelated workspace caches;
- host container-control sockets;
- production keys.

Build workers are reset, destroyed, or independently verified before reuse.

### 4.7 Reproducibility

A reproducibility claim identifies:

- source revision;
- dependency resolution;
- toolchain identity;
- build parameters;
- build environment;
- expected artifact identity;
- allowed nondeterministic fields, when explicitly normalized;
- comparison procedure.

A mismatch is evidence requiring investigation, not an acceptable random outcome.

### 4.8 SBOM and provenance

An SBOM describes the software components present in the shipped artifact.

Provenance describes how the artifact was produced.

They are complementary:

| Evidence | Primary question |
| --- | --- |
| SBOM | What software components are present? |
| Provenance | From which source, dependencies, tools, builder, and procedure was this artifact produced? |
| Signature | Which signing identity authenticated the signed statement? |
| Digest | Which exact bytes does the statement describe? |
| Admission result | Did the artifact satisfy current rules for a declared use? |
| Release Set | Is the artifact compatible with the other active release channels? |

### 4.9 Signing model

Signing is a governed operation.

A signing request binds:

- exact artifact digest;
- artifact class;
- release channel;
- intended scope;
- evidence set;
- signer and key identity;
- policy decision;
- time and expiry where applicable.

Keys are separated according to authority and risk. Development and test keys cannot authorize production artifacts.

### 4.10 Artifact admission

Artifact admission evaluates the candidate for a declared target and purpose.

Admission includes:

- structural validation;
- content identity;
- required signatures;
- trust chain and revocation status;
- source and build provenance;
- SBOM completeness;
- vulnerability and exception disposition;
- component and data-boundary compliance;
- profile compatibility;
- release-channel compatibility;
- required tests and evidence.

An admitted artifact remains inactive until release and activation procedures complete.

### 4.11 Release and promotion

Promotion preserves one exact artifact identity through:

`text
builder output
→ verified candidate
→ signed artifact
→ admitted artifact
→ channel release
→ Release Set
→ offline or connected transfer
→ staged artifact
→ active artifact
`

Rebuilding from the same source creates a new build result unless reproducibility proves equivalent bytes and the owning release contract permits reuse of the same content identity.

### 4.12 AI and generated content

AI can assist source creation, tests, documentation, configuration, and analysis.

AI output remains candidate input.

The same source review, untrusted execution, dependency, provenance, signing, admission, and promotion rules apply regardless of whether a human, generator, or AI produced the initial content.

### 4.13 Compromise and revocation

A compromise can affect:

- source history;
- dependency package;
- toolchain;
- build image;
- builder;
- registry or mirror;
- signing key;
- artifact;
- Release Set;
- offline bundle;
- active deployment.

Revocation identifies the affected scope and prevents future admission or activation. Active remediation follows applicable rollback or forward-repair contracts.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-SEC-SC-001,REQ-SEC-SC-002,REQ-SEC-SC-003,REQ-SEC-SC-004,REQ-SEC-SC-005,REQ-SEC-SC-006,REQ-SEC-SC-007,REQ-SEC-SC-008,REQ-SEC-SC-009,REQ-SEC-SC-010,REQ-SEC-SC-011,REQ-SEC-SC-012,REQ-SEC-SC-013,REQ-SEC-SC-014,REQ-SEC-SC-015,REQ-SEC-SC-016,REQ-SEC-SC-017,REQ-SEC-SC-018,REQ-SEC-SC-019,REQ-SEC-SC-020,REQ-SEC-SC-021,REQ-SEC-SC-022,REQ-SEC-SC-023,REQ-SEC-SC-024,REQ-SEC-SC-025,REQ-SEC-SC-026,REQ-SEC-SC-027,REQ-SEC-SC-028,REQ-SEC-SC-029,REQ-SEC-SC-030,REQ-SEC-SC-031,REQ-SEC-SC-032,REQ-SEC-SC-033,REQ-SEC-SC-034,REQ-SEC-SC-035,REQ-SEC-SC-036,REQ-SEC-SC-037,REQ-SEC-SC-038,REQ-SEC-SC-039,REQ-SEC-SC-040,REQ-SEC-SC-041,REQ-SEC-SC-042,REQ-SEC-SC-043,REQ-SEC-SC-044,REQ-SEC-SC-045,REQ-SEC-SC-046,REQ-SEC-SC-047,REQ-SEC-SC-048,REQ-SEC-SC-049,REQ-SEC-SC-050,REQ-SEC-SC-051,REQ-SEC-SC-052,REQ-SEC-SC-053,REQ-SEC-SC-054,REQ-SEC-SC-055,REQ-SEC-SC-056
renderer=requirements-list-v1
-->
- **REQ-SEC-SC-001 — SHALL:** Every software supply-chain object have a stable identity, owner, version or revision, provenance, and lifecycle state.
- **REQ-SEC-SC-002 — SHALL:** Source, dependency, toolchain, build, artifact, evidence, release, and activation authorities remain independently identifiable.
- **REQ-SEC-SC-003 — SHALL NOT:** Repository access, developer approval, build success, registry availability, or artifact possession grant release or activation authority.
- **REQ-SEC-SC-004 — SHALL:** Release inputs originate from admitted source revisions and declared repositories or source bundles.
- **REQ-SEC-SC-005 — SHALL:** Source admission verify repository identity, revision identity, applicable signatures or trust evidence, ownership, review status, and required policy.
- **REQ-SEC-SC-006 — SHALL NOT:** An unreviewed local modification, untracked file, mutable workspace state, or undeclared generated file be used as a published release input.
- **REQ-SEC-SC-007 — SHALL:** Generated source and vendored source identify their generator or upstream origin, input revision, generation procedure, and review result.
- **REQ-SEC-SC-008 — SHALL:** Every dependency and build tool be declared through an applicable toolchain or build contract.
- **REQ-SEC-SC-009 — SHALL:** Dependency resolution use versioned lock state or an equivalent immutable resolution record.
- **REQ-SEC-SC-010 — SHALL:** Package sources, registries, mirrors, and artifact repositories be explicitly admitted and scoped.
- **REQ-SEC-SC-011 — SHALL NOT:** An undeclared package source, mutable branch, floating version, mutable container tag, or latest-version selector be treated as a reproducible release input.
- **REQ-SEC-SC-012 — SHALL:** Downloaded packages, tools, images, and artifacts be verified through applicable digest, signature, provenance, trusted-source, or transparency evidence.
- **REQ-SEC-SC-013 — SHALL:** Dependency changes include direct and transitive diff review, vulnerability review, policy and license compatibility where applicable, impact analysis, and tests.
- **REQ-SEC-SC-014 — SHALL:** Known vulnerabilities be resolved through remediation, bounded mitigation, rejection, or an active exact-scope exception with owner and expiry.
- **REQ-SEC-SC-015 — SHALL NOT:** A vulnerability or policy exception silently extend to another version, dependency, artifact, profile, release, architecture, or cloned environment.
- **REQ-SEC-SC-016 — SHALL:** Toolchain identity include exact versions or immutable identities for compilers, interpreters, build backends, package managers, generators, scanners, and container builders.
- **REQ-SEC-SC-017 — SHALL:** Release builds execute in clean, isolated, reproducible build environments controlled by the active build-farm profile or an equivalently authorized builder.
- **REQ-SEC-SC-018 — SHALL NOT:** A release build depend on undeclared host files, developer home state, workstation caches, interactive credentials, local service state, or ambient environment variables.
- **REQ-SEC-SC-019 — SHALL:** Build workers begin from verified baseline state and be reset, destroyed, or independently verified before reuse.
- **REQ-SEC-SC-020 — SHALL:** Build-time network access be denied by default and limited to declared admitted sources when required.
- **REQ-SEC-SC-021 — SHALL:** Build secrets be short-lived, minimum-scope, non-exportable where supported, and excluded from build outputs, logs, caches, and provenance payloads.
- **REQ-SEC-SC-022 — SHALL NOT:** Production signing keys, production root credentials, or unrestricted production service credentials be exposed to general build workers.
- **REQ-SEC-SC-023 — SHALL:** Resource Governor constrain build CPU, memory, I/O, workers, processes, network-intensive tasks, queues, timeouts, and artifact storage.
- **REQ-SEC-SC-024 — SHALL:** Build procedures separate compilation or packaging from production signing and release authorization.
- **REQ-SEC-SC-025 — SHALL:** A reproducible build declare the source, dependencies, toolchains, parameters, environment identity, and expected output identities required for independent reproduction.
- **REQ-SEC-SC-026 — SHALL:** Reproducibility claims be supported by an independent rebuild or a declared deterministic-equivalence test.
- **REQ-SEC-SC-027 — SHALL:** A reproducibility mismatch block promotion until explained, bounded, and dispositioned.
- **REQ-SEC-SC-028 — SHALL:** Every promoted software artifact include an applicable SBOM covering shipped packages, libraries, runtimes, embedded tools, and container layers.
- **REQ-SEC-SC-029 — SHALL:** The SBOM identify exact component versions, supplier or origin where known, dependency relationships, and artifact identity.
- **REQ-SEC-SC-030 — SHALL:** Build provenance bind the artifact to source revision, dependency resolution, toolchain identity, builder identity, build environment, parameters, and build result.
- **REQ-SEC-SC-031 — SHALL:** Provenance and attestations be machine-readable, immutable after publication, and verifiable against the exact artifact identity.
- **REQ-SEC-SC-032 — SHALL:** Artifact digests identify content, while signatures authenticate the signing identity and signed statement; neither alone grants activation authority.
- **REQ-SEC-SC-033 — SHALL:** Signing keys be separated by purpose, environment, artifact class, release channel, and authority scope where applicable.
- **REQ-SEC-SC-034 — SHALL:** Signing operations require resolved identity, policy, artifact identity, evidence completeness, key scope, and current authorization.
- **REQ-SEC-SC-035 — SHALL NOT:** A developer key, test key, expired key, revoked key, or wrong-scope key authorize a production artifact.
- **REQ-SEC-SC-036 — SHALL:** Artifact admission verify schema, digest, signatures, trust chain, provenance, SBOM, vulnerability disposition, policy, profile compatibility, release-channel compatibility, and required evidence.
- **REQ-SEC-SC-037 — SHALL:** Failed artifact admission quarantine or reject the exact candidate without modifying active artifacts.
- **REQ-SEC-SC-038 — SHALL NOT:** A cache, mirror, registry, repository, transport bundle, or integration endpoint become authoritative merely because it stores an artifact.
- **REQ-SEC-SC-039 — SHALL:** Promotion preserve the exact admitted artifact identity across staging, signing, release publication, Release Set binding, transfer, and activation.
- **REQ-SEC-SC-040 — SHALL:** Every executable artifact belong to the applicable release channel and declare compatibility with the active versions of the other channels.
- **REQ-SEC-SC-041 — SHALL:** A Release Set bind exact compatible `system`, `services`, `governance`, and `knowledge` versions before cross-channel activation.
- **REQ-SEC-SC-042 — SHALL NOT:** An independent channel update proceed when compatibility with any active channel is unresolved.
- **REQ-SEC-SC-043 — SHALL:** Offline software transfer use a sealed verified offline bundle or equivalent approved transport whose manifest binds every contained artifact and evidence item.
- **REQ-SEC-SC-044 — SHALL:** Offline admission perform the same trust, integrity, provenance, SBOM, vulnerability, compatibility, evidence, and authority checks as connected admission.
- **REQ-SEC-SC-045 — SHALL NOT:** Network isolation or urgency justify bypassing supply-chain verification.
- **REQ-SEC-SC-046 — SHALL:** AI-generated source, tests, configuration, build definitions, scripts, and documentation remain candidate inputs subject to the same review, provenance, execution, and admission controls.
- **REQ-SEC-SC-047 — SHALL NOT:** An AI tool, external integration, editor extension, or generator approve, sign, publish, promote, or activate its own output.
- **REQ-SEC-SC-048 — SHALL:** A suspected source, dependency, toolchain, builder, registry, signing-key, or artifact compromise trigger containment, revocation, scope analysis, evidence preservation, quarantine, and controlled rebuild.
- **REQ-SEC-SC-049 — SHALL:** Revocation identify every affected source revision, dependency version, build, artifact, signature, Release Set, profile, node, and downstream derivative that can be determined.
- **REQ-SEC-SC-050 — SHALL:** Compromised or untrusted artifacts remain non-authoritative and be removed from future admission while preserving required forensic evidence.
- **REQ-SEC-SC-051 — SHALL:** Recovery rebuild from independently verified source, dependencies, toolchains, builder baselines, trust roots, and signing authorities.
- **REQ-SEC-SC-052 — SHALL:** Supply-chain failure degrade or block only affected builds, artifacts, releases, channels, or capabilities while preserving unrelated verified active state.
- **REQ-SEC-SC-053 — SHALL:** Critical admission, signing, revocation, Release Set, and activation transitions emit required machine-readable receipts.
- **REQ-SEC-SC-054 — SHALL:** Retention preserve source and dependency resolutions, toolchain identities, SBOMs, provenance, attestations, signatures, admission results, Release Sets, revocations, exceptions, and evidence required for recovery and conformance.
- **REQ-SEC-SC-055 — SHALL:** Profile-specific builder, sandbox, container, orchestration, signing, registry, transparency, mirror, or transport mechanisms remain scoped to the contracts that adopt them.
- **REQ-SEC-SC-056 — SHALL:** Software supply-chain conformance test source and dependency admission, clean builds, reproducibility, secret exclusion, SBOM and provenance completeness, signing scope, artifact admission, Release Set compatibility, offline transfer, revocation, recovery, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Admit source

1. resolve source owner and repository or bundle identity;
2. select an immutable revision;
3. verify required reviews and signatures;
4. enumerate generated and vendored source;
5. verify policy and exception state;
6. scan for exposed secrets and prohibited material;
7. record source-admission evidence;
8. admit or reject the revision.

### 6.2 Resolve dependencies and toolchains

1. load declared dependency and toolchain contracts;
2. resolve exact package, image, and tool versions;
3. resolve admitted sources and mirrors;
4. verify package and image integrity;
5. compare lock or resolution changes;
6. evaluate vulnerabilities, policy, and licenses where applicable;
7. resolve exceptions;
8. freeze the resolution record;
9. record evidence.

### 6.3 Prepare a clean build

1. select the active build-farm profile;
2. allocate a clean verified worker;
3. bind admitted source and immutable dependency inputs;
4. bind exact toolchain identities;
5. exclude ambient and production credentials;
6. apply network restrictions;
7. apply Resource Governor limits;
8. record the build environment identity;
9. begin build execution.

### 6.4 Build and verify

1. execute declared build steps;
2. capture bounded logs and test results;
3. verify that no undeclared input was accessed;
4. generate exact artifact identities;
5. perform reproducibility or deterministic-equivalence checks where required;
6. generate SBOM;
7. generate provenance and attestations;
8. scan candidate artifacts;
9. mark the result verified or rejected.

### 6.5 Sign

1. resolve signing authority and key scope;
2. verify artifact digest and class;
3. verify evidence completeness;
4. verify current policy and key status;
5. construct the exact signed statement;
6. execute signing in the approved boundary;
7. verify the produced signature;
8. emit signing evidence or receipt.

The signer does not modify artifact bytes after digest selection.

### 6.6 Admit an artifact

1. retrieve by exact content identity;
2. validate artifact schema and media type;
3. verify digest;
4. verify signatures and trust;
5. verify provenance and attestations;
6. verify SBOM and vulnerability disposition;
7. verify profile, component, interface, and release-channel compatibility;
8. verify required tests and exceptions;
9. admit, quarantine, or reject the exact candidate.

### 6.7 Publish and bind a Release Set

1. publish admitted artifacts to their canonical channels;
2. identify exact channel release versions;
3. evaluate cross-channel compatibility;
4. construct the Release Set;
5. sign and verify the Release Set according to its contract;
6. retain compatibility evidence;
7. publish the Release Set for deployment admission.

### 6.8 Create an offline bundle

1. select an exact Release Set;
2. include every required artifact and evidence item;
3. include channel trust material needed for local verification;
4. create a deterministic manifest of content identities;
5. verify completeness;
6. seal and sign the transport bundle;
7. retain assembly provenance and receipt;
8. transfer through the approved physical or logical path.

The bundle transports authority references. It does not gain activation authority.

### 6.9 Revoke compromised material

1. identify suspected compromised object and scope;
2. block new admission and promotion;
3. revoke applicable keys, signatures, artifacts, packages, or source revisions;
4. locate dependent builds, derivatives, Release Sets, bundles, and deployments;
5. quarantine affected candidates and stores;
6. preserve evidence;
7. select rollback or forward repair for active deployments;
8. rebuild from independently verified inputs;
9. publish corrected releases and revocation evidence.

### 6.10 Recover the supply chain

1. verify trust roots and signing authorities;
2. restore admitted source and dependency sources;
3. verify clean builder baselines;
4. invalidate compromised caches and mirrors;
5. rebuild affected artifacts;
6. compare reproducibility results;
7. regenerate SBOM and provenance;
8. re-run admission and compatibility;
9. issue new Release Sets;
10. recover deployments through their lifecycle contracts;
11. close the incident with retained evidence.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Source identity or review unresolved | Block source admission | Previously admitted revisions |
| Dependency source unavailable | Use verified admitted mirror or cache; otherwise block resolution | Existing locked environments |
| Package digest or signature mismatch | Reject and quarantine package | Other verified dependencies |
| Vulnerability disposition unresolved | Block promotion | Local analysis and unaffected artifacts |
| Toolchain identity unresolved | Block release build | Source review and known verified toolchains |
| Clean builder unavailable | Block release build | Existing active releases |
| Build accesses undeclared input | Reject build result | Source and prior verified artifacts |
| Reproducibility mismatch | Block promotion | Candidate diagnostics and prior artifact |
| SBOM incomplete | Block promotion requiring SBOM | Build result for remediation |
| Provenance incomplete or unverifiable | Block artifact admission | Prior admitted artifacts |
| Signing authority unavailable | Keep candidate unsigned or development-scoped | Candidate analysis |
| Signing key revoked or wrong scope | Reject signature and artifact authorization | Other valid signatures |
| Artifact registry unavailable | Use approved verified local store where permitted | Active artifacts |
| Registry content differs from expected digest | Reject retrieved content | Known exact artifact identity |
| Release Set compatibility unresolved | Block activation | Current compatible Release Set |
| Offline bundle seal invalid | Reject bundle import | Current local artifacts |
| External AI or integration unavailable | Disable dependent assistance | Deterministic local development and build |
| Supply-chain compromise suspected | Contain, revoke, quarantine, and investigate | Unrelated verified channels and artifacts |
| Receipt persistence unavailable | Keep receipt-before-commit transition uncommitted | Previous authoritative state |
| Recovery verification incomplete | Remain `restoring` or `blocked` | Last verified supply-chain state |

Safe degradation never accepts unknown bytes, weakens key scope, ignores revocation, substitutes mutable tags, or activates incompatible releases.

## 8. Cross-Component Interactions

### 8.1 Developer workspaces

Developer workspaces produce reviewed source changes and development candidates.

Mutable workstation state is not a release input unless converted into an admitted, reproducible, provenance-bearing artifact through the declared handoff.

### 8.2 Build Farm

Build Farm executes controlled clean builds and produces candidate artifacts, tests, SBOMs, provenance, and attestations.

It does not acquire production signing or activation authority.

### 8.3 Identity and Trust

Identity and Trust resolves developers, reviewers, builders, signers, release services, deployment authorities, keys, certificates, and trust roots.

A signature from an unresolved or revoked identity fails verification.

### 8.4 Governance Policy Runtime

Governance Policy Runtime evaluates exceptional dependency use, signing approval, privileged builder operations, vulnerability exceptions, release exceptions, and emergency revocation actions where required.

It does not perform builds or allocate resources.

### 8.5 Resource Governor

Resource Governor constrains build workers, scanners, artifact stores, queues, reproducibility jobs, and recovery builds.

Resource availability does not authorize a candidate.

### 8.6 Audit Broker

Audit Broker retains required admission, signing, Release Set, revocation, incident, and recovery receipts.

It does not own the artifact or release decision.

### 8.7 Artifact Verifier and stores

Artifact Verifier validates exact candidates.

Stores, registries, mirrors, caches, and offline bundles preserve and transport bytes. They do not establish authority by storage location.

### 8.8 Release and deployment authorities

Release authority publishes exact channel releases and Release Sets.

Deployment authority verifies target applicability and performs activation through lifecycle procedures.

### 8.9 External integrations

An integration providing source, packages, scans, signatures, transparency, or storage operates through an integration manifest.

Its failure, removal, or substitution cannot silently change authoritative inputs or trust policy.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- release input begins with admitted immutable source;
- dependencies and toolchains are explicit and versioned;
- clean controlled builders produce release candidates;
- production signing is separate from general build execution;
- SBOM and provenance accompany promoted software where required;
- digests identify content but do not grant authority;
- signatures authenticate signed statements but do not grant authority by themselves;
- artifact admission is distinct from storage and publication;
- Release Sets bind all four channels;
- offline admission performs equivalent verification;
- AI and generated content remain candidate input;
- compromise triggers revocation, quarantine, rebuild, and controlled deployment recovery;
- profile-specific supply-chain mechanisms remain profile-scoped.

Prohibited assumptions include:

- trusting a branch name as immutable source identity;
- using an untracked developer file in a release build;
- treating `latest` as a version;
- trusting a package because TLS download succeeded;
- trusting a package because it exists in a familiar registry;
- using mutable container tags for reproducible builds;
- allowing build scripts unrestricted Internet access;
- exposing signing keys to general build workers;
- treating a clean vulnerability scan as complete safety proof;
- treating an SBOM as provenance;
- treating provenance as release approval;
- treating a digest as a signature;
- treating a signature as compatibility evidence;
- treating registry presence as artifact admission;
- treating admission as activation;
- letting an AI-generated build definition approve itself;
- allowing an exception to follow a dependency upgrade automatically;
- accepting an offline bundle without local verification;
- applying one builder, registry, signing, or transparency implementation globally.

## 10. Validation Criteria

Software supply-chain conformance validates when:

1. source repositories and revisions resolve to immutable admitted identities;
2. source reviews and required signatures resolve;
3. generated and vendored source provenance resolves;
4. dependencies and toolchains are declared and locked;
5. package sources and mirrors are admitted;
6. package, image, tool, and artifact integrity checks pass;
7. vulnerability findings have exact dispositions;
8. exceptions have exact scope, owner, mitigation, and expiry;
9. release builds run in clean isolated workers;
10. ambient workstation state and production credentials are absent;
11. build network access matches declared requirements;
12. build secrets do not appear in outputs, caches, logs, or provenance;
13. exact toolchain identities are recorded;
14. required reproducibility checks pass;
15. SBOM completeness passes;
16. provenance binds source, dependencies, tools, builder, parameters, and artifact;
17. signing identities, keys, algorithms, scope, and revocation status pass;
18. development and test keys cannot authorize production artifacts;
19. artifact admission validates schema, integrity, trust, evidence, and compatibility;
20. stores and bundles do not become authority owners;
21. exact artifact identity survives promotion unchanged;
22. channel ownership remains correct;
23. Release Set compatibility covers all four channels;
24. offline transfer and admission pass equivalent checks;
25. AI-generated changes pass normal review and provenance;
26. revocation identifies reachable downstream impact;
27. compromised candidates remain quarantined;
28. rebuild and recovery use independently verified inputs;
29. critical transitions produce required receipts;
30. all decisions, requirements, locks, exceptions, tests, and evidence resolve;
31. no unresolved marker, placeholder, duplicate owner, or ordinary documentation hash appears;
32. supply-chain, release, profile, component-boundary, traceability, and Interfile Alignment Lock checks pass.

Applicable checks include:

`bash
python docs/tools/check_artifact_contracts.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_profile_composition.py
python docs/tools/check_release_sets.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 Python service build

An admitted source revision contains `pyproject.toml` and `uv.lock`.

A clean worker uses the declared Python and UV versions, performs `uv sync --frozen`, runs tests, builds the package, produces an SBOM and provenance, and submits the exact artifact for signing and admission.

### 11.2 Container base image

A service build references a base image by immutable digest.

The image source, digest, SBOM, vulnerabilities, and policy disposition are recorded. A mutable tag can be displayed for convenience but is not the authoritative input.

### 11.3 Reproducibility mismatch

Two clean builders use the same admitted inputs but produce different package bytes.

Promotion stops. The investigation identifies an embedded timestamp not covered by the declared normalization procedure. The build contract is corrected and both builds are repeated.

### 11.4 Signing separation

Build Farm produces a verified candidate and evidence bundle.

A separate signing authority verifies the artifact digest, evidence, release channel, key scope, and policy decision before signing. Build Farm never receives the production signing key.

### 11.5 Offline bundle

A sovereign node receives a sealed offline bundle containing an exact Release Set, artifacts, SBOMs, provenance, signatures, and trust material.

The node verifies all content locally before admission. Physical custody of the bundle does not grant activation authority.

### 11.6 Compromised dependency

A dependency version is found to have been compromised.

New admission is blocked, affected artifacts and Release Sets are identified, active deployments select rollback or forward repair, and corrected artifacts are rebuilt from verified source and toolchains.

### 11.7 AI-generated build script

An external AI surface proposes a build script.

The script is reviewed as source, executed first in an isolated untrusted environment, and admitted only after its dependencies, network behavior, outputs, and provenance pass normal controls.
