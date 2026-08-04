<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-007",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "profile:sovereign_linux_node"
  ],
  "canonical_refs": [
    "contracts/profiles/sovereign-linux-node.profile.json",
    "generated/profile-catalog.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/profiles/appliance-shell.profile.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/decision-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/artifact-contracts/node-profile.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/sovereignty-bundle.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-SHELL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-SLN-001",
    "REQ-PROFILE-SLN-002",
    "REQ-PROFILE-SLN-003",
    "REQ-PROFILE-SLN-004",
    "REQ-PROFILE-SLN-005",
    "REQ-PROFILE-SLN-006",
    "REQ-PROFILE-SLN-007",
    "REQ-PROFILE-SLN-008",
    "REQ-PROFILE-SLN-009",
    "REQ-PROFILE-SLN-010",
    "REQ-PROFILE-SLN-011",
    "REQ-PROFILE-SLN-012",
    "REQ-PROFILE-SLN-013",
    "REQ-PROFILE-SLN-014",
    "REQ-PROFILE-SLN-015",
    "REQ-PROFILE-SLN-016",
    "REQ-PROFILE-SLN-017",
    "REQ-PROFILE-SLN-018",
    "REQ-PROFILE-SLN-019",
    "REQ-PROFILE-SLN-020",
    "REQ-PROFILE-SLN-021",
    "REQ-PROFILE-SLN-022",
    "REQ-PROFILE-SLN-023",
    "REQ-PROFILE-SLN-024",
    "REQ-PROFILE-SLN-025",
    "REQ-PROFILE-SLN-026",
    "REQ-PROFILE-SLN-027",
    "REQ-PROFILE-SLN-028",
    "REQ-PROFILE-SLN-029",
    "REQ-PROFILE-SLN-030",
    "REQ-PROFILE-SLN-031",
    "REQ-PROFILE-SLN-032",
    "REQ-PROFILE-SLN-033",
    "REQ-PROFILE-SLN-034"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-SYS-020"
  ],
  "tags": [
    "deployment-profile",
    "sovereign-linux-node",
    "primary-profile",
    "linux",
    "signed-system-image",
    "verified-boot-identity",
    "privileged-broker",
    "local-governance",
    "recovery",
    "release-set"
  ]
}
KOA:DOC-META:END -->

# Sovereign Linux Node

> **Document status:** Normative profile explanation  
> **Profile ID:** `sovereign_linux_node`  
> **Profile kind:** `primary_profile`  
> **Canonical profile contract:** `contracts/profiles/sovereign-linux-node.profile.json`  
> **Authority rule:** The profile contract owns profile facts. This document explains how those facts apply.

## 1. Purpose

This document explains the `sovereign_linux_node` primary deployment profile.

The profile defines a hardened, locally governable Linux node that can operate core kOA capabilities with explicit authority, bounded privilege, deterministic resource control, recoverable releases, local trust, local policy evaluation, and verifiable evidence.

The profile is intended for production deployments where operators require:

- locally controlled system and service operation;
- signed and attributable releases;
- a maintained Linux base;
- explicit component and data boundaries;
- a narrow path for privileged node mutation;
- local policy and identity services;
- verified backup and recovery;
- predictable failure and degradation behavior;
- optional composition with stronger assurance or offline overlays.

The profile does not redefine the global kOA system.

It selects and strengthens system behavior for one production Linux deployment form.

## 2. Scope

### 2.1 Included scope

The profile applies to:

- a production Linux node;
- a locally administered endpoint or service node;
- deployments that require a signed system image and recoverable activation;
- deployments that host one or more kOA runtime components;
- deployments that enforce local component, identity, policy, resource, storage, and audit boundaries;
- deployments that can compose approved overlays for higher assurance, offline sovereignty, or an appliance shell.

The node can serve:

- one user;
- one tenant;
- one organization;
- one bounded community deployment;
- a declared local workload set.

The exact role, selected components, tenant model, exposure, and overlays remain canonical in the profile contract and effective node-profile artifact.

### 2.2 Excluded scope

This profile does not define:

- a developer workstation;
- a Windows or WSL host;
- a build farm;
- a fleet control plane;
- a sovereign hub;
- a generic Kubernetes cluster;
- a mandatory appliance shell;
- a mandatory air-gapped deployment;
- a global requirement for systemd, Podman, Quadlet, Wayland, or any specific desktop environment;
- a general-purpose privileged administration environment;
- a native AI runtime;
- unrestricted cloud dependence.

`sovereign_hub` is a separate primary profile.

`high_assurance`, `sovereign_offline`, and `appliance_shell` are composable overlays rather than alternate names for this profile.

### 2.3 Profile classification

| Field | Value |
| --- | --- |
| Profile ID | `sovereign_linux_node` |
| Kind | Primary deployment profile |
| Operating-system family | Linux |
| Primary intent | Hardened local production node |
| Authority model | Explicit and locally resolvable |
| Privilege model | Narrow governed broker |
| Resource model | Locally enforced by Resource Governor |
| Release model | Signed independent channels bound by a Release Set |
| Recovery model | Previous known-good state plus dedicated recovery environment |
| External AI | Optional, external, non-authoritative, and unnecessary for core operation |
| Kubernetes | Not required by this profile |

### 2.4 Profile status

The profile status is `active`.

Activation of an individual node still depends on:

- an active profile contract;
- a compatible effective component set;
- a valid Release Set;
- successful profile validation;
- valid evidence;
- resolution of all selected overlays and exceptions.

### 2.5 Applicable operating modes

The profile supports:

- user-mode production operation;
- operator maintenance and recovery operation;
- profile-authorized administrative operation;
- controlled task activation for heavy or optional services.

Developer workbench activity is not an implicit property of this profile.

A development profile can target or produce artifacts for a sovereign Linux node without becoming the node's active deployment profile.

### 2.6 Profile composition

The profile can compose with:

| Overlay | Relationship | Primary effect |
| --- | --- | --- |
| `high_assurance` | Compatible when declared by both contracts | Stronger boot, trust, review, identity, evidence, and isolation controls |
| `sovereign_offline` | Compatible when declared by both contracts | Complete local authority and operation without Internet dependencies |
| `appliance_shell` | Compatible when declared by both contracts | Restricted shell and minimal Wayland-oriented user experience |

Composition is explicit.

An overlay can strengthen or restrict behavior within its declared scope.

An overlay cannot merge component authorities, weaken global invariants, or silently redefine this primary profile.

## 3. Canonical References

### 3.1 Primary profile authority

```text
contracts/profiles/sovereign-linux-node.profile.json
```

### 3.2 Global and profile authority

| Reference | Owned information |
| --- | --- |
| `generated/authority-manifest.json` | Active authority order and registry versions |
| `generated/decision-index.json` | Accepted system and profile decisions |
| `contracts/system.contract.json` | Global system baseline |
| `generated/component-catalog.json` | Component identities, responsibilities, dependencies, and data ownership |
| `generated/component-catalog.json` | Active component-contract inventory |
| `generated/profile-catalog.json` | Profile and overlay inventory |
| `contracts/profiles/sovereign-linux-node.profile.json` | Profile membership, claims, hardware, activation, implementation adoptions, and conformance |
| `contracts/profiles/high-assurance.profile.json` | Optional assurance strengthening |
| `contracts/profiles/sovereign-offline.profile.json` | Optional offline-sovereignty strengthening |
| `contracts/profiles/appliance-shell.profile.json` | Optional restricted shell |
| `contracts/release-channels.contract.json` | Release-channel identities and compatibility |
| `contracts/artifact-classes.contract.json` | Artifact lifecycle and activation |
| `generated/requirements-index.json` | Normative requirement statements |
| `generated/assertion-index.json` | Protected cross-file invariants |
| `generated/decision-index.json` | Accepted ADR identity and lifecycle |
| `generated/traceability.json` | Links to tests and evidence |
| `generated/test-catalog.json` | Conformance-test definitions |
| `generated/evidence-catalog.json` | Evidence definitions and validity |
| `generated/exception-index.json` | Active bounded deviations |

### 3.3 Accepted architectural records

The profile applies these accepted architectural records:

| Record | Effect |
| --- | --- |
| `ADR-001` | Uses a standard maintained Linux kernel |
| `ADR-002` | Uses an immutable signed operating-system image with atomic activation |
| `ADR-008` | Separates system, services, governance, and knowledge release channels |
| `ADR-009` | Uses Governance Policy Runtime where the profile requires governed policy evaluation |
| `ADR-010` | Uses selective audit rather than indiscriminate operational replication |
| `ADR-012` | Routes normal privileged node mutation through one narrow broker |
| `DEC-PROFILE-001` | Defines primary profiles and composable overlays |
| `DEC-DATA-001` | Preserves logical data ownership and prohibits foreign source writes |
| `DEC-GOV-001` | Separates Resource Governor from Governance Policy Runtime |
| `DEC-CONTAINER-001` | Keeps sovereign Linux container behavior profile-scoped |
| `DEC-HW-001` | Defines the sovereign-node hardware envelope |
| `DEC-REL-001` | Defines four independent release channels and Release Sets |

### 3.4 Related artifact contracts

| Artifact contract | Profile use |
| --- | --- |
| `node-profile.schema.json` | Effective node-role and profile declaration |
| `release-set.schema.json` | Compatible release-channel binding |
| `policy-bundle.schema.json` | Governance policy delivery |
| `offline-bundle.schema.json` | Controlled offline import when selected |
| `sovereignty-bundle.schema.json` | Portable export and clean-node restoration |
| `decision-receipt.schema.json` | Policy and governed-transition receipts |
| `provenance-receipt.schema.json` | Artifact and release provenance |
| `resource-envelope.schema.json` | Hardware and workload limits |

## 4. Model and Responsibilities

### 4.1 Profile intent

The profile realizes a sovereign production Linux node without turning one implementation into the global kOA baseline.

Its defining properties are:

- maintained Linux foundation;
- image-based signed operating-system delivery;
- verifiable booted-image and release identity;
- explicit component authority;
- local identity and policy capability;
- deterministic local resource control;
- narrow privileged execution;
- independent signed release channels;
- local recovery;
- testable offline envelope;
- selective evidence and audit;
- credible export and restoration.

Sovereignty in this profile means control and verifiability of the node's active authority.

It does not mean that every optional service is installed, every deployment is air-gapped, or every Linux-specific choice applies to other profiles.

### 4.2 Operating-system foundation

The operating-system base uses a standard Linux kernel from a recognized upstream or distribution maintenance chain.

Product differentiation remains primarily in:

- services;
- policy;
- component contracts;
- runtime and knowledge artifacts;
- user experience;
- release composition.

Kernel modifications remain exceptional and reviewable.

The operating-system base is image-built and signed.

Production activation replaces the base atomically rather than relying on undocumented mutable system state.

Mutable data belongs in declared state locations outside the immutable system base.

### 4.3 Boot and release identity

The node can identify:

- the booted operating-system image;
- the active system release;
- active service artifacts;
- active governance policy;
- active knowledge and runtime artifacts;
- the Release Set that binds their tested compatibility.

The profile itself requires verifiable identity.

Secure Boot, measured boot, TPM-backed evidence, dual control, or another hardware root of trust belong to the `high_assurance` overlay when stronger hardware-bound assurance is claimed.

Absence of that overlay does not remove the requirement to identify and verify active artifacts through the base profile's trust model.

### 4.4 Boot progression

The logical boot progression is:

```text
firmware and boot trust
        ↓
signed boot components and maintained kernel
        ↓
signed operating-system image
        ↓
storage unlock and integrity verification
        ↓
identity, trust, policy, audit, resource, and node services
        ↓
selected application and runtime components
        ↓
local user or operator experience
```

The exact service-manager targets and unit names belong to implementation recipes or profile-adopted configuration.

A failed optional application does not remove recovery access.

A failed trust, policy, storage, or release-verification foundation blocks the affected sensitive activation and exposes an actionable diagnostic state.

### 4.5 Component composition

The effective component set is declared by the profile contract and node-profile artifact.

Cross-cutting required responsibilities include:

- Identity and Trust;
- Governance Policy Runtime;
- Audit Broker;
- Resource Governor;
- kOA Node Agent;
- backup, restore, health, and evidence capabilities.

Application and runtime components can include:

- Konnaxion;
- Orgo;
- Kristal Runtime;
- SemantiK Architect Runtime;
- UCKK Platform;
- UCKK Dimension Gateway;
- Ariane Runtime;
- Publication Gateway.

Selection depends on the node role and effective profile.

Registration does not imply installation.

Installation does not imply continuous activation.

Optional workbenches such as SenTient and GF Wordbench are not part of the profile's required production runtime.

### 4.6 Privilege architecture

Ordinary product services run without unrestricted root privilege.

Privileged node mutation uses a narrow registered broker, normally `koa_node_agent` and its associated privileged execution boundary.

The broker accepts allowlisted operations with:

- fixed request contracts;
- verified caller identity;
- applicable policy decision;
- target and scope;
- idempotency behavior;
- bounded execution;
- result code;
- correlation identity;
- receipt or evidence.

The broker is not a general remote shell.

Ordinary user operation does not provide direct shell or root access.

Break-glass behavior, where adopted, remains separately governed and evidenced.

### 4.7 Policy and resource separation

Governance Policy Runtime evaluates:

- authorization;
- disclosure;
- consent;
- privilege;
- registered exceptions.

Resource Governor controls:

- CPU;
- memory;
- I/O;
- concurrency;
- queues;
- scheduling;
- process limits.

A sensitive workload can require both services.

The policy runtime decides whether the governed operation is permitted.

The owning component accepts the operation.

Resource Governor determines whether and when the workload runs within the active envelope.

Neither authority substitutes for the other.

### 4.8 Data and storage model

Every authoritative data domain has one owning component.

The profile strengthens physical and logical separation through:

- distinct service identities;
- distinct storage identities;
- distinct database identities;
- explicit namespaces;
- least-privilege access;
- component-owned backup and recovery mappings;
- contract-controlled transfers.

Separate database instances are preferred for authoritative domains.

A validated deployment can use another logically isolated arrangement only when the profile contract, component contracts, threat model, tests, and evidence support it.

No component repairs or coordinates another component by writing directly into its source tables.

### 4.9 Hardware envelope

| Resource | Minimum | Recommended or required companion |
| --- | ---: | --- |
| CPU | 8 modern cores | Additional capacity according to workload |
| Memory | 32 GiB | 64 GiB for sustained media, indexing, hub-like, or multi-tenant workloads |
| Primary storage | 1 TB encrypted SSD | Additional capacity according to retained data and recovery objectives |
| Recovery target | Required | Independently bootable or otherwise isolated according to contract |
| Verified backup target | Required | Integrity-tested and compatible with restore procedures |
| GPU | Not required by the base profile | Profile or component contract can add a workload-specific requirement |
| Network | Deployment-specific | Local operation and failure behavior remain declared |

The hardware envelope is a profile claim.

It is not a global kOA minimum.

A deployment below the minimum cannot claim full conformance to this profile.

### 4.10 Resource envelope

The node-profile artifact and resource-envelope artifact declare:

- total CPU and memory;
- reserved system capacity;
- component budgets;
- workload classes;
- queue limits;
- worker concurrency;
- I/O priorities;
- storage thresholds;
- pressure thresholds;
- degradation order;
- maximum simultaneous heavy jobs;
- recovery reserve.

Resource Governor enforces the active envelope.

Optional and heavy work degrades before core identity, policy, recovery, and authoritative-state integrity.

Unbounded new work remains blocked when resource governance cannot be verified.

### 4.11 Offline envelope

The profile declares a tested offline capability envelope.

The base profile preserves, at minimum:

- local identity verification;
- local policy evaluation;
- access to active verified runtime and knowledge artifacts;
- local authoritative work selected by the node role;
- local status and diagnostics;
- local backup and recovery;
- release and artifact inspection;
- safe handling of deferred synchronization or publication.

The base profile does not require a permanent cloud connection.

The `sovereign_offline` overlay adds the stronger condition that conformant operation prohibits Internet dependency and uses controlled signed offline transfer boundaries.

### 4.12 AI and external services

The global native baseline contains no required generative AI, classifier, summarizer, embedding model, autonomous routing model, or autonomous agent.

External AI surfaces remain:

- optional;
- explicit;
- capability-scoped;
- removable;
- non-authoritative;
- unable to write directly into authoritative state.

The profile's core remains functional without:

- ChatGPT;
- Suno;
- Gamma;
- external Ariane voice;
- SenTient;
- another external model or agent.

The `sovereign_offline` overlay disables external AI calls during conformant operation.

### 4.13 Release channels

The profile uses four independently versioned channels:

| Channel | Content |
| --- | --- |
| `system` | Operating-system image, kernel, host runtime, recovery base, and node services |
| `services` | Product services, gateways, runtime services, and profile-selected service artifacts |
| `governance` | Policy bundles, governance rules, revocations, and related governed artifacts |
| `knowledge` | Kristal, PGF, language runtime, Atlas, and approved knowledge artifacts |

Each channel retains independent identity and signature.

A Release Set binds the compatible versions that were tested for the active node profile.

Independent updates remain possible only when declared compatibility constraints continue to pass.

### 4.14 Activation and known-good state

The node stages candidate artifacts without replacing active authority.

Activation verifies:

- profile applicability;
- artifact identity;
- signatures;
- provenance;
- schema and contract compatibility;
- migration requirements;
- release-channel compatibility;
- tests;
- evidence;
- recovery readiness.

Activation completes as one coherent authority transition.

The previous known-good state remains available according to policy.

A migration that prevents safe rollback uses a declared forward-repair path.

### 4.15 Backup, restore, and exit

Backup preserves:

- component ownership;
- encryption;
- integrity;
- artifact and release identity;
- schema state;
- trust dependencies;
- restoration order;
- evidence.

Restore uses compatibility checks rather than blind file replacement.

A Sovereignty Bundle or other registered export format supports credible exit and restoration on a clean compatible node.

Exit capability is tested.

Documentation alone is not sufficient evidence of portability.

### 4.16 Desktop and service implementation choices

The profile can adopt Linux-specific implementation choices.

Current preferred choices include:

- rootless Podman for OCI workloads;
- Quadlet for profile-adopted container service declarations;
- systemd or an equivalent maintained Linux service manager;
- a maintained desktop environment when a general desktop is selected;
- a minimal Wayland-oriented shell only when the `appliance_shell` overlay is active.

These choices remain profile-scoped.

An application contract does not depend on runtime-specific behavior unless the profile explicitly adopts that dependency.

Kubernetes is not required by this profile.

### 4.17 Overlay relationships

#### High assurance

`high_assurance` can strengthen:

- boot identity;
- measured evidence;
- hardware-backed keys;
- dual control;
- review requirements;
- storage separation;
- trust-root operations;
- evidence retention.

#### Sovereign offline

`sovereign_offline` can strengthen:

- local authority;
- external-network denial;
- signed removable-media import;
- local policy and trust;
- local audit retention;
- offline update and evidence export;
- absence of external AI and cloud dependencies.

#### Appliance shell

`appliance_shell` can strengthen:

- restricted session behavior;
- minimal user interface;
- reduced general-purpose desktop access;
- embedded web application presentation.

Each overlay remains a separate canonical contract.

### 4.18 Operations model

The node maintains local operational capability for:

- health and readiness;
- resource observation;
- backup status;
- restore readiness;
- release status;
- policy status;
- trust status;
- audit and evidence status;
- local incident diagnostics;
- maintenance staging;
- recovery entry.

Readiness distinguishes process existence from ability to satisfy the component's critical contract.

Critical failures produce stable diagnostics and evidence.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-SLN-001,REQ-PROFILE-SLN-002,REQ-PROFILE-SLN-003,REQ-PROFILE-SLN-004,REQ-PROFILE-SLN-005,REQ-PROFILE-SLN-006,REQ-PROFILE-SLN-007,REQ-PROFILE-SLN-008,REQ-PROFILE-SLN-009,REQ-PROFILE-SLN-010,REQ-PROFILE-SLN-011,REQ-PROFILE-SLN-012,REQ-PROFILE-SLN-013,REQ-PROFILE-SLN-014,REQ-PROFILE-SLN-015,REQ-PROFILE-SLN-016,REQ-PROFILE-SLN-017,REQ-PROFILE-SLN-018,REQ-PROFILE-SLN-019,REQ-PROFILE-SLN-020,REQ-PROFILE-SLN-021,REQ-PROFILE-SLN-022,REQ-PROFILE-SLN-023,REQ-PROFILE-SLN-024,REQ-PROFILE-SLN-025,REQ-PROFILE-SLN-026,REQ-PROFILE-SLN-027,REQ-PROFILE-SLN-028,REQ-PROFILE-SLN-029,REQ-PROFILE-SLN-030,REQ-PROFILE-SLN-031,REQ-PROFILE-SLN-032,REQ-PROFILE-SLN-033,REQ-PROFILE-SLN-034 -->
- **REQ-PROFILE-SLN-001 — SHALL:** The `sovereign_linux_node` profile use a standard Linux kernel from a recognized maintenance chain.
- **REQ-PROFILE-SLN-002 — SHALL:** Product-specific kernel modifications remain minimal, published, reviewable, and upstreamable or removable.
- **REQ-PROFILE-SLN-003 — SHALL:** The operating-system base be image-built, signed, and activated atomically.
- **REQ-PROFILE-SLN-004 — SHALL NOT:** A conformant production node depend on undocumented in-place mutation of `/usr` or equivalent immutable system content.
- **REQ-PROFILE-SLN-005 — SHALL:** The node establish the identity of the booted operating-system image and active Release Set.
- **REQ-PROFILE-SLN-006 — SHALL:** The profile retain a recovery environment, active state, previous known-good state, required manifests, signatures, and recovery metadata.
- **REQ-PROFILE-SLN-007 — SHALL:** The node provide at least eight modern CPU cores, 32 GiB of memory, one terabyte of encrypted SSD storage, a recovery target, and a verified backup target.
- **REQ-PROFILE-SLN-008 — SHOULD:** A conformant node provide at least 64 GiB of memory when its declared workload envelope includes sustained media, indexing, hub, or multi-tenant workloads.
- **REQ-PROFILE-SLN-009 — SHALL:** The profile declare and enforce a machine-readable hardware and resource envelope.
- **REQ-PROFILE-SLN-010 — SHALL:** Resource Governor enforce local CPU, memory, I/O, queue, concurrency, and process limits.
- **REQ-PROFILE-SLN-011 — SHALL:** Governance Policy Runtime evaluate authorization, disclosure, consent, privilege, and registered-exception decisions required by the profile.
- **REQ-PROFILE-SLN-012 — SHALL NOT:** Resource Governor and Governance Policy Runtime merge their authority or substitute for one another.
- **REQ-PROFILE-SLN-013 — SHALL:** Normal product services operate without unrestricted root privilege.
- **REQ-PROFILE-SLN-014 — SHALL:** Privileged node mutations pass through `koa_node_agent` or an equivalent registered narrow broker with allowlisted operations, policy binding, idempotency, and receipts.
- **REQ-PROFILE-SLN-015 — SHALL:** A sensitive privileged operation receive an applicable policy decision before execution.
- **REQ-PROFILE-SLN-016 — SHALL:** The policy decision and privileged execution result remain correlated and auditable.
- **REQ-PROFILE-SLN-017 — SHALL:** The profile preserve separate component identities, storage boundaries, trust boundaries, and authoritative data ownership.
- **REQ-PROFILE-SLN-018 — SHALL NOT:** A component write directly to another component's authoritative source tables or equivalent mutable source state.
- **REQ-PROFILE-SLN-019 — SHALL:** Cross-domain access use an active component contract, gateway, signed artifact, or other registered transfer mechanism.
- **REQ-PROFILE-SLN-020 — SHALL:** Separate storage identities be used for component-owned authoritative data.
- **REQ-PROFILE-SLN-021 — SHOULD:** Separate database instances be used for authoritative component domains unless the profile contract records a validated logically isolated alternative.
- **REQ-PROFILE-SLN-022 — SHALL:** The node maintain local identity verification, local policy evaluation, local selective audit, local recovery, and access to active verified runtime and knowledge artifacts.
- **REQ-PROFILE-SLN-023 — SHALL NOT:** The profile require a permanent cloud connection or an external AI service for its declared core capability envelope.
- **REQ-PROFILE-SLN-024 — SHALL:** External AI outputs remain non-authoritative candidate inputs until validated and explicitly adopted by an authoritative component workflow.
- **REQ-PROFILE-SLN-025 — SHALL:** The profile define explicit behavior for loss of Internet, external integrations, policy evaluation, trust verification, audit evidence storage, and resource governance.
- **REQ-PROFILE-SLN-026 — SHALL:** Capability degradation preserve unaffected local capabilities while blocking operations whose authority, integrity, or required control cannot be verified.
- **REQ-PROFILE-SLN-027 — SHALL:** System, service, governance, and knowledge release channels retain independent identities and signatures.
- **REQ-PROFILE-SLN-028 — SHALL:** A signed Release Set identify tested compatible versions across all release channels required by the active node profile.
- **REQ-PROFILE-SLN-029 — SHALL NOT:** A release channel silently embed and activate another channel's authority.
- **REQ-PROFILE-SLN-030 — SHALL:** Operating-system images, service artifacts, policy bundles, runtime packs, and other authoritative artifacts activate without partial authoritative state.
- **REQ-PROFILE-SLN-031 — SHALL:** Every supported update and migration define rollback or forward-repair behavior and retain the previous known-good state according to policy.
- **REQ-PROFILE-SLN-032 — SHALL:** Backup and restore verify component ownership, encryption, integrity, schema, artifact, release, and trust compatibility before authoritative activation.
- **REQ-PROFILE-SLN-033 — SHALL:** The profile accept only explicitly compatible overlays and reject ambiguous or incompatible profile composition.
- **REQ-PROFILE-SLN-034 — SHALL:** A conformance claim identify the exact profile version, overlays, authority version, Release Set, hardware envelope, requirements, tests, evidence, exceptions, and validation result.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Profile selection

1. Resolve `sovereign_linux_node` in the active profile index.
2. Resolve the active profile-contract version.
3. Resolve the node's declared role and selected components.
4. Resolve explicitly selected overlays.
5. Reject undeclared, incompatible, or ambiguous composition.
6. Resolve active exceptions.
7. Compute the effective requirements, locks, components, artifacts, tests, and evidence plan.
8. Validate the effective profile before provisioning or activation.

### 6.2 Provisioning

1. Verify target hardware against the minimum envelope.
2. Establish node identity and local trust material.
3. Provision encrypted primary storage and separate component identities.
4. Provision the recovery target and verified backup target.
5. Install the signed operating-system image without activating incomplete authority.
6. Provision Resource Governor, Identity and Trust, Governance Policy Runtime, Audit Broker, and kOA Node Agent.
7. Stage profile-selected service and knowledge artifacts.
8. Install applicable policy bundles.
9. Resolve the compatible Release Set.
10. Configure the narrow privileged path.
11. Configure local health, backup, restore, audit, and evidence services.
12. Run preactivation tests.
13. Activate the coherent node release.
14. Record provisioning and activation evidence.

### 6.3 Normal boot

1. Verify boot components according to the active trust model.
2. identify the operating-system image.
3. unlock and verify storage.
4. start local identity, trust, policy, audit, resource, and node-control services.
5. verify the active Release Set.
6. start selected authoritative components.
7. start optional or user-facing components according to activation policy.
8. evaluate readiness.
9. expose normal operation only for capabilities whose authority and dependencies are valid.
10. preserve recovery entry when optional services fail.

### 6.4 Privileged operation

1. Identify the exact operation, target, actor, and correlation identity.
2. verify caller identity and active profile.
3. obtain the applicable policy decision.
4. verify operation allowlisting and request contract.
5. check idempotency and current node state.
6. execute through the narrow privileged boundary.
7. verify the result.
8. emit correlated decision and execution evidence.
9. expire temporary authority or access.
10. preserve the previous valid state on failure.

### 6.5 Update and activation

1. Receive or discover candidate artifacts through a registered channel.
2. verify artifact identity, signatures, and provenance.
3. resolve channel and Release Set compatibility.
4. inspect migration, rollback, and forward-repair requirements.
5. create or verify a current backup.
6. stage the complete candidate set.
7. run profile, component, migration, and recovery tests.
8. preserve the active known-good state.
9. authorize activation.
10. activate atomically.
11. run bounded boot and readiness acceptance.
12. retain the new state only after acceptance.
13. produce activation evidence.

### 6.6 Failed update

1. Detect failed activation, readiness, trust, policy, storage, migration, or component acceptance.
2. prevent incomplete authority from becoming active.
3. preserve diagnostics and failed evidence.
4. determine whether rollback is compatible.
5. restore the previous known-good state when safe.
6. use forward repair when irreversible migration makes rollback unsafe.
7. revalidate the recovered authority state.
8. produce failure and recovery evidence.
9. keep affected capability blocked until authority is valid.

### 6.7 Backup

1. Resolve component ownership and backup scope.
2. quiesce or coordinate mutation according to component contracts.
3. create encrypted backup artifacts.
4. record schema, artifact, release, trust, and profile identity.
5. verify integrity.
6. store on the verified backup target.
7. test restoration according to policy.
8. record evidence and retention state.

### 6.8 Restore

1. Select the backup, target node, profile, and target release.
2. verify backup integrity and provenance.
3. verify component, tenant, schema, artifact, encryption, trust, and release compatibility.
4. determine restore order.
5. preserve the current recoverable state.
6. restore into correct component authority boundaries.
7. perform declared migration or forward repair.
8. validate data invariants and cross-component references.
9. activate only the complete compatible authority state.
10. record restore evidence.

### 6.9 Recovery entry

Recovery can be entered through:

- automatic fallback after repeated boot or readiness failure;
- signed local operator request;
- physical recovery action;
- verified recovery media;
- another method explicitly adopted by the active profile and assurance overlay.

Recovery can provide:

- booted-image and Release Set inspection;
- previous-image rollback;
- policy and runtime-artifact rollback;
- storage diagnostics;
- trust repair;
- encrypted backup restore;
- Sovereignty Bundle import;
- selected audit export;
- explicit factory reset with declared data handling.

Recovery never silently erases authoritative data or replaces trust roots.

### 6.10 Profile removal or repurposing

1. identify retained data, artifacts, trust, and evidence.
2. produce required exports.
3. close or transfer active responsibilities through accepted contracts.
4. revoke node and service identities according to policy.
5. remove or archive sensitive key material.
6. verify backups and restoration path.
7. deactivate the profile.
8. wipe or repurpose storage according to registered data-handling policy.
9. record final disposition and evidence.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Booted image identity cannot be verified | Enter diagnostic or recovery state | Recovery and evidence access according to policy | Sensitive normal activation |
| Release Set is missing or incompatible | Keep previous valid release | Previous compatible operation | Candidate activation |
| Required policy bundle is unavailable | Fail closed for governed transitions | Unaffected non-governed capability | New governed action |
| Identity or trust verification fails | Reject trust-dependent operations | Verified local state | Unverified activation or privilege |
| Resource Governor is unavailable | Block unbounded resource-sensitive work | Safe lightweight and recovery capabilities | New heavy work |
| Governance Policy Runtime is unavailable | Block policy-dependent operations | Unaffected local capability | Authorization, disclosure, consent, privilege, or exception-dependent action |
| Audit evidence storage is unavailable | Follow declared buffering or block receipt-required transitions | Unaffected non-critical operation | Unreceipted critical transition |
| Backup target is unavailable | Report non-readiness and block operations that require current recovery assurance | Existing local operation where policy permits | Update or migration requiring backup |
| Recovery target is unavailable | Mark profile nonconformant and block risky activation | Current stable state | Activation lacking required recovery |
| Storage integrity fails | Isolate affected component state and enter recovery | Unaffected components where boundaries hold | Mutation of affected authoritative state |
| One application component fails | Degrade that capability | Identity, policy, recovery, and unrelated components | Failed component capability |
| External AI or integration fails | Disable only the external capability | Native local operation | External operation |
| Privileged broker fails | Reject privileged mutation | Non-privileged operation | Host mutation |
| Direct foreign data write is attempted | Reject and report a lock violation | Existing valid component state | Prohibited mutation |
| Update readiness fails | Restore or retain previous known-good state | Previous release | Candidate release |
| Rollback is unsafe after migration | Keep affected transition blocked and apply declared forward repair | Recoverable unaffected state | Blind downgrade |
| Hardware drops below required capacity | Apply degradation and mark conformance impact | Recovery and bounded core operation | Full profile claim where minimum cannot be met |
| Complete validation cannot execute | Mark activation blocked | Previous active authority | New conformance or release claim |

Failure does not create a fallback owner, substitute policy, substitute release, substitute external service, or broader privilege.

## 8. Cross-Component Interactions

### 8.1 Effective component graph

The effective graph is produced from:

- the global system registry;
- the sovereign Linux node profile contract;
- selected overlays;
- selected component contracts;
- active integration contracts;
- active Release Set;
- active exceptions.

The graph includes only declared components and interactions.

### 8.2 Data ownership

The profile changes deployment topology and assurance.

It does not transfer logical ownership.

Each component remains the only authoritative writer for its declared data domains.

Cross-component coordination uses versioned APIs, commands, events, signed artifacts, user-authorized transfer, or governed gateways.

### 8.3 Identity and policy

Identity and Trust supplies verified identity and trust assertions.

Governance Policy Runtime evaluates governed decisions.

The calling component remains responsible for enforcing the decision and for its own authoritative state transition.

### 8.4 Resource governance

Components declare workload class and resource needs.

Resource Governor applies the active resource envelope.

Policy approval does not guarantee immediate resource admission.

Resource availability does not create authorization.

### 8.5 Privileged host operations

```text
caller
  -> identity verification
  -> policy decision
  -> allowlisted node-agent request
  -> narrow privileged execution
  -> execution result
  -> correlated receipts
```

The path does not expose general root access to product services.

### 8.6 Publication

A source component initiates a publication request.

Governance Policy Runtime evaluates disclosure where required.

Publication Gateway prepares and transports the permitted representation.

The source component remains authoritative for source data.

UCKK Dimension Gateway does not substitute for Publication Gateway.

### 8.7 UCKK admission

A user or authorized component requests admission of selected media.

UCKK Dimension Gateway verifies the transfer boundary.

UCKK Platform accepts and owns the resulting UCKK state according to its contract.

Publication and UCKK admission remain distinct operations.

### 8.8 Audit and evidence

Components emit selected accountable events and evidence references.

Audit Broker stores or routes the required evidence.

Audit Broker does not become a universal operational database.

Decision evidence and execution evidence remain distinct and linkable.

### 8.9 Backup and restore

Backup tooling operates on component-owned data under registered procedures.

It does not acquire application authority.

Restore places data back into the correct component boundary and compatible release state.

### 8.10 External integrations

Every external integration is:

- registered;
- classified;
- explicitly activated;
- bounded by transferred data;
- subject to failure behavior;
- removable without unrelated core failure.

External outputs remain non-authoritative until adopted by an owning component.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision or ADR | Closed choice |
| --- | --- |
| `ADR-001` | Standard maintained Linux kernel |
| `ADR-002` | Signed image-built operating-system base and atomic activation |
| `ADR-008` / `DEC-REL-001` | Four independent release channels bound by Release Sets |
| `ADR-009` / `DEC-GOV-001` | Governance Policy Runtime remains separate from Resource Governor |
| `ADR-010` | Selective audit rather than indiscriminate data exposure |
| `ADR-012` | One narrow privileged node broker |
| `DEC-PROFILE-001` | Sovereign Linux node is a primary profile with explicit overlays |
| `DEC-DATA-001` | Logical data ownership and prohibited foreign writes |
| `DEC-CONTAINER-001` | Rootless Podman and Quadlet are sovereign-profile choices, not global rules |
| `DEC-K8S-001` | Kubernetes is not required by an endpoint profile |
| `DEC-HW-001` | Sovereign-node hardware envelope |
| `DEC-AI-001` | No native AI dependency in the global core |

### 9.2 Protected locks

| Lock ID | Protected relationship |
| --- | --- |
| `LOCK-PROFILE-001` | Profile-specific Linux behavior does not become global |
| `LOCK-PROFILE-002` | Overlay composition is explicit |
| `LOCK-DATA-001` | No direct foreign authoritative-source write |
| `LOCK-GOV-001` | Resource and policy authorities remain separate |
| `LOCK-AI-001` | Native baseline has no required AI model or autonomous agent |
| `LOCK-AI-002` | External AI cannot directly mutate authoritative state |
| `LOCK-LIFE-001` | Published artifacts do not activate partially |
| `LOCK-LIFE-002` | Artifact classes define rollback or forward repair |
| `LOCK-LIFE-003` | Release Sets bind compatible versions |
| `LOCK-LIFE-004` | Independent channel updates preserve compatibility |
| `LOCK-IMPL-001` | Recipes do not redefine the profile |
| `LOCK-IMPL-002` | systemd, Quadlet, Wayland, and no-GNOME remain profile-scoped |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- every Linux host is a sovereign Linux node;
- running under Linux proves profile conformance;
- a developer workstation is equivalent to a production node;
- the profile requires every registered component;
- every installed service is always active;
- the profile is automatically air-gapped;
- `sovereign_offline` is implicit;
- `high_assurance` is implicit;
- `appliance_shell` is implicit;
- Secure Boot or TPM evidence can be claimed without the applicable overlay and tests;
- systemd, Podman, Quadlet, Wayland, or no-GNOME are global kOA requirements;
- Kubernetes is required;
- a shared service process merges component authority;
- root access creates product authority;
- `koa_node_agent` is a general remote shell;
- a policy decision directly executes the operation;
- Resource Governor can grant privilege;
- Governance Policy Runtime can allocate CPU or schedule workers;
- a backup operator owns application data;
- a copied database is a valid restore without compatibility checks;
- a published artifact is active merely because it is available;
- one channel can silently activate another channel;
- external AI is required for local operation;
- external AI output is authoritative;
- failure permits a direct database repair across component boundaries;
- a recipe defines a profile fact;
- current implementation behavior overrides the profile contract;
- a hardware recommendation is interchangeable with the minimum;
- an undeclared similar profile can substitute;
- partial evidence supports full conformance.

Missing profile authority, missing release compatibility, unresolved overlay composition, unverifiable identity, or undefined failure behavior blocks the affected claim or activation.

## 10. Validation Criteria

The profile explanation is conformant when:

1. the document is registered as `DOC-PROFILE-007`;
2. the path is `03-profiles/07-sovereign-linux-node.md`;
3. the document class is `normative_markdown`;
4. the active language is English;
5. the scope resolves to `profile:sovereign_linux_node`;
6. the canonical profile contract resolves and validates;
7. the profile index contains one active entry;
8. every selected overlay is explicitly compatible;
9. inheritance and composition contain no cycle or ambiguity;
10. every component identity and component contract resolves;
11. every data domain has one authoritative owner;
12. no foreign authoritative-source write is permitted;
13. the maintained-kernel rule is represented in profile authority;
14. the signed image and atomic activation rules are represented;
15. the booted image and active Release Set are identifiable;
16. the recovery environment and previous known-good state exist;
17. minimum hardware is verified;
18. the resource envelope is complete and enforced;
19. the privileged broker exposes only allowlisted operations;
20. policy decisions precede applicable privileged operations;
21. decision and execution receipts correlate;
22. local identity, policy, audit, backup, and recovery capabilities pass;
23. offline tests exercise the declared offline envelope;
24. external AI failure does not break core operation;
25. independent release-channel identities resolve;
26. Release Set compatibility passes;
27. candidate activation cannot create partial authority;
28. rollback or forward repair is tested;
29. backup restoration is tested on compatible authority;
30. portability and clean-node restoration are evidenced;
31. profile-specific implementation choices remain profile-scoped;
32. requirements and locks resolve;
33. tests execute;
34. evidence is valid for the exact profile and release versions;
35. exceptions are active and scoped;
36. no unresolved architectural state exists;
37. generated profile catalogs and AI context match canonical authority;
38. complete documentation validation passes.

Expected test coverage includes:

```text
TEST-PROFILE-SLN-001  Maintained Linux kernel
TEST-PROFILE-SLN-002  Signed immutable operating-system image
TEST-PROFILE-SLN-003  Booted image and Release Set identity
TEST-PROFILE-SLN-004  Minimum hardware envelope
TEST-PROFILE-SLN-005  Recovery and verified backup targets
TEST-PROFILE-SLN-006  Resource Governor enforcement
TEST-PROFILE-SLN-007  Governance and resource authority separation
TEST-PROFILE-SLN-008  Narrow privileged broker
TEST-PROFILE-SLN-009  Policy-before-privilege correlation
TEST-PROFILE-SLN-010  Component and data boundary isolation
TEST-PROFILE-SLN-011  Local identity, policy, audit, and recovery
TEST-PROFILE-SLN-012  External AI independence
TEST-PROFILE-SLN-013  Offline capability envelope
TEST-PROFILE-SLN-014  Four release-channel identity
TEST-PROFILE-SLN-015  Release Set compatibility
TEST-PROFILE-SLN-016  Atomic activation and known-good rollback
TEST-PROFILE-SLN-017  Backup and restore compatibility
TEST-PROFILE-SLN-018  Sovereignty Bundle export and clean-node restore
TEST-PROFILE-SLN-019  Overlay compatibility
TEST-PROFILE-SLN-020  Profile-scoped implementation choices
```

The test catalog and evidence registry own executable test and evidence definitions.

This document does not claim that the tests have already run.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate possible conformant deployments. They do not redefine the profile contract.

### 11.1 Standard sovereign node

A production node uses:

- a maintained distribution kernel;
- a signed image-built operating-system base;
- encrypted local storage;
- separate service identities;
- Resource Governor;
- Governance Policy Runtime;
- Audit Broker;
- kOA Node Agent;
- one compatible Release Set;
- a recovery image;
- a verified backup target.

The node uses a maintained desktop environment.

It does not use the appliance-shell overlay.

### 11.2 High-assurance sovereign node

The node composes:

```text
sovereign_linux_node + high_assurance
```

The overlay adds hardware-backed trust, stronger boot evidence, stricter review, and stronger key handling.

Those controls are not implied for every base-profile deployment.

### 11.3 Offline sovereign node

The node composes:

```text
sovereign_linux_node + sovereign_offline
```

It operates without Internet routes, uses local policy and trust, imports signed offline bundles through quarantine, retains local audit evidence, and disables external AI operations.

### 11.4 Appliance node

The node composes:

```text
sovereign_linux_node + appliance_shell
```

It uses a minimal Wayland-oriented shell and restricts general-purpose desktop behavior.

The no-GNOME choice remains part of the overlay rather than the base profile.

### 11.5 Rootless service deployment

A service is packaged as an OCI image.

The profile uses rootless Podman and Quadlet to run it under a dedicated identity.

The component contract remains independent of Podman-specific behavior.

A different conformant implementation can use another maintained mechanism when the profile contract permits it.

### 11.6 Privileged update

A signed system image is staged.

Governance Policy Runtime authorizes activation.

kOA Node Agent sends one allowlisted activation operation to the privileged boundary.

The node activates the complete compatible Release Set, verifies readiness, and records decision and execution receipts.

### 11.7 Component database isolation

Konnaxion and Orgo run on the same physical node.

Each has a separate service identity and authoritative database boundary.

Orgo requests Konnaxion changes through the Konnaxion component contract.

It never updates Konnaxion source tables directly.

### 11.8 Failed application service

An optional application service fails during boot.

Identity, policy, audit, resource control, node diagnostics, and recovery remain available.

The failed capability is marked unavailable.

The node does not treat the failure as permission to bypass contracts or activate a substitute.

### 11.9 Invalid deployment

A deployment uses a mutable untracked `/usr`, runs product services as unrestricted root, lacks a recovery target, shares one database identity across components, and activates independently downloaded artifacts without a Release Set.

The deployment is not conformant to `sovereign_linux_node`.
