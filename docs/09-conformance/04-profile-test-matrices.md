<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-004",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "07-security/21-security-control-architecture.md",
    "07-security/22-security-control-profile-matrix.md",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-DOC-001",
    "DEC-REL-001",
    "DEC-HW-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-CONF-PROF-001",
    "REQ-CONF-PROF-002",
    "REQ-CONF-PROF-003",
    "REQ-CONF-PROF-004",
    "REQ-CONF-PROF-005",
    "REQ-CONF-PROF-006",
    "REQ-CONF-PROF-007",
    "REQ-CONF-PROF-008",
    "REQ-CONF-PROF-009",
    "REQ-CONF-PROF-010",
    "REQ-CONF-PROF-011",
    "REQ-CONF-PROF-012",
    "REQ-CONF-PROF-013",
    "REQ-CONF-PROF-014",
    "REQ-CONF-PROF-015",
    "REQ-CONF-PROF-016",
    "REQ-CONF-PROF-017",
    "REQ-CONF-PROF-018",
    "REQ-CONF-PROF-019",
    "REQ-CONF-PROF-020",
    "REQ-CONF-PROF-021",
    "REQ-CONF-PROF-022",
    "REQ-CONF-PROF-023",
    "REQ-CONF-PROF-024",
    "REQ-CONF-PROF-025",
    "REQ-CONF-PROF-026",
    "REQ-CONF-PROF-027",
    "REQ-CONF-PROF-028",
    "REQ-CONF-PROF-029",
    "REQ-CONF-PROF-030",
    "REQ-CONF-PROF-031",
    "REQ-CONF-PROF-032",
    "REQ-CONF-PROF-033"
  ],
  "lock_ids": [
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-005",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-013",
    "DOC-CONF-000",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "conformance",
    "normative-markdown",
    "04",
    "profile",
    "test",
    "matrices",
    "security-controls",
    "security-evidence",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Profile Test Matrices

## 1. Purpose

This document defines how kOA conformance tests are selected, combined, executed, and evaluated for deployment profiles and profile overlays.

A profile conformance claim applies to one exact composition:

- one base profile;
- zero or more explicitly permitted overlays;
- one component selection;
- one topology;
- one platform and implementation;
- one active Release Set;
- one configuration set;
- one evidence scope;
- one test-catalog version.

The profile test matrices prevent a deployment from claiming broad conformance after running only generic tests or tests for a different composition. They also prevent optional capabilities from being treated as silently active, absent capabilities from being counted as passed, and implementation-specific tests from becoming global requirements.

The matrices provide:

- common test families that apply to every profile;
- base-profile test families;
- overlay additions;
- component-selection additions;
- platform and implementation additions;
- lifecycle, security, offline, data, and recovery coverage;
- explicit applicability states;
- explicit result states;
- evidence and traceability requirements;
- rules for blocked, failed, excluded, and not-applicable tests;
- a repeatable method for calculating a profile conformance outcome.

This document does not duplicate the complete test catalog. It defines how the catalog is projected into a profile-specific execution matrix.

## 2. Scope

### 2.1 Base profiles

The base-profile matrix covers:

| Profile ID | Contract path | Primary purpose |
| --- | --- | --- |
| `user_lightweight` | `contracts/profiles/user-lightweight.profile.json` | Local-first user endpoint with bounded resources and no native AI dependency. |
| `developer_linux_workstation` | `contracts/profiles/developer-linux-workstation.profile.json` | Native Linux development workstation with isolated workspaces and UV-based Python development. |
| `developer_windows_wsl` | `contracts/profiles/developer-windows-wsl.profile.json` | Windows and WSL development workstation with equivalent workspace and toolchain isolation. |
| `sovereign_linux_node` | `contracts/profiles/sovereign-linux-node.profile.json` | Sovereign local Linux node with local lifecycle, security, backup, and recovery. |
| `sovereign_hub` | `contracts/profiles/sovereign-hub.profile.json` | Multi-tenant hub with separated zones, governance, publication, federation, and recovery. |
| `build_farm` | `contracts/profiles/build-farm.profile.json` | Controlled parallel build, test, packaging, validation, and candidate-artifact production. |
| `control_plane` | `contracts/profiles/control-plane.profile.json` | Coordination, registry, policy-distribution, and fleet-management services that remain non-essential to local correctness. |

### 2.2 Overlays

The overlay matrix covers:

| Overlay ID | Contract path | Added test concern |
| --- | --- | --- |
| `high_assurance` | `contracts/profiles/high-assurance.profile.json` | Stronger identity, separation, evidence, recovery, and failure controls. |
| `sovereign_offline` | `contracts/profiles/sovereign-offline.profile.json` | Sustained operation, update, support, exchange, and recovery without online dependencies. |
| `appliance_shell` | `contracts/profiles/appliance-shell.profile.json` | Constrained appliance user experience, bounded administration, local navigation, and recovery access. |

An overlay is not a standalone profile. Its tests are added to an explicitly compatible base profile.

### 2.3 Component and capability selection

The matrix includes tests introduced by:

- required components;
- selected optional components;
- activated integrations;
- selected external adapters;
- enabled federation;
- selected storage or database implementations;
- selected container or native-process implementations;
- selected operating-system mechanisms;
- activated release channels;
- selected development workbenches;
- enabled heavy services;
- tenant and authority-domain configuration.

Installation alone does not make an optional component active. Active selection is resolved from the profile contract and deployment composition.

### 2.4 Test dimensions

Profile testing covers:

- contract and schema validity;
- traceability;
- component presence and absence;
- data ownership;
- integration boundaries;
- profile inheritance and overlay composition;
- hardware and resource behavior;
- offline continuity;
- identity, trust, governance, and audit;
- security and network boundaries;
- kOA Mediatheque ownership and optional UCKK publication-boundary separation;
- backup, restore, exit, update, rollback, and migration;
- workspace and toolchain isolation;
- tenant isolation;
- federation;
- build reproducibility;
- capacity and load behavior;
- support and diagnostics;
- removal and cleanup;
- evidence validity.

### 2.5 Excluded uses

This document does not:

- define test implementation code;
- own test identifiers;
- own requirement or lock status;
- own evidence records;
- declare a deployment conformant by itself;
- permit one profile’s evidence to prove another profile;
- turn a successful example into conformance evidence;
- make optional capabilities required globally;
- make containers or Kubernetes endpoint requirements;
- make external AI a baseline dependency;
- replace component, profile, or overlay contracts.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/requirements-index.json` | Owns the normative requirements that tests verify. |
| `generated/assertion-index.json` | Owns cross-document and cross-contract alignment assertions. |
| `generated/traceability.json` | Owns requirement-to-test, lock-to-test, decision-to-test, artifact-to-test, and evidence traceability. |
| `generated/test-catalog.json` | Owns test identities, descriptions, procedures, applicability predicates, expected outcomes, and evidence types. |
| `generated/evidence-catalog.json` | Owns evidence identities, subjects, producers, scope, results, validity, and lifecycle. |
| `contracts/security-controls.contract.json` | Owns security-control identities, categories, profile applicability, implementation bindings, validation bindings, failure behavior, and evidence classes. |
| `contracts/artifact-contracts/security-evidence.schema.json` | Owns the structure of control-specific security evidence. |
| `07-security/21-security-control-architecture.md` | Defines control composition, lifecycle, exception, and conformance rules. |
| `07-security/22-security-control-profile-matrix.md` | Renders the canonical control applicability matrix for human review. |

Profile contracts under `contracts/profiles/` own:

- base-profile identity;
- inheritance;
- compatible overlays;
- component requirements and selections;
- hardware envelope;
- implementation constraints;
- offline behavior;
- conformance claim prerequisites;
- profile-specific test references.

Component contracts own component-specific test obligations.

The active Release Set owns the tested combination of `system`, `services`, `governance`, and `knowledge` release-channel versions.

This document owns only the matrix-construction and outcome rules.

## 4. Model and Responsibilities

### 4.1 Matrix identity

A profile test matrix instance identifies:

- matrix identity;
- base profile ID and version;
- overlay IDs and versions;
- profile-contract references;
- selected components and versions;
- selected integrations and versions;
- platform and implementation;
- topology;
- tenant and authority-domain scope;
- active Release Set;
- test-catalog version;
- traceability-registry version;
- evidence-registry version;
- security-control contract version;
- effective security-control applicability set;
- generation time;
- generator identity and version;
- matrix state;
- claim target.

A matrix becomes stale after any input that affects applicability changes.

### 4.2 Applicability states

Every catalog test receives one matrix applicability state:

| State | Meaning |
| --- | --- |
| `required` | The test applies and a passing result with valid evidence is necessary. |
| `conditional_required` | The test applies when its explicit predicate is true. The generated matrix resolves the predicate before execution. |
| `not_applicable` | The active composition lacks the tested capability and the catalog permits exclusion. |
| `prohibited` | The test verifies that an excluded capability or behavior remains absent. |
| `blocked` | Applicability cannot be resolved because required contracts, versions, configuration, or authority are unavailable. |

`not_applicable` is not a successful test result. `prohibited` tests are active negative tests and require execution.

Security-control applicability is first resolved from `contracts/security-controls.contract.json`. A control state of `required` activates its declared validation binding; `prohibited` activates a negative test or verified-absence check; `not_applicable` requires a recorded machine-resolvable predicate; `recommended` activates either implementation validation or a bounded accepted rationale. Test applicability cannot silently weaken the control state.

### 4.3 Result states

An applicable test receives one result:

| Result | Meaning |
| --- | --- |
| `pass` | The observed outcome matches the catalog expectation and valid evidence exists. |
| `fail` | The observed outcome contradicts the expectation. |
| `blocked` | Execution or evaluation cannot complete because a required dependency, authority, environment, or evidence source is unavailable. |
| `not_run` | The test was selected but execution has not occurred. |
| `invalid` | The result or evidence does not match the matrix scope or test contract. |
| `cancelled` | Execution stopped before a valid terminal result. |

A not-applicable test has applicability `not_applicable` and no pass result.

### 4.4 Common test families

Every base profile includes these common families:

| Family ID | Family | Coverage |
| --- | --- | --- |
| `PF-COMMON-CONTRACT` | Contract validity | Profile schema, IDs, references, inheritance, overlays, status, and version. |
| `PF-COMMON-TRACE` | Traceability | Decisions, requirements, locks, tests, and evidence resolve without gaps. |
| `PF-COMMON-RELEASE` | Release compatibility | Active Release Set is complete, signed, compatible, and profile-supported. |
| `PF-COMMON-COMPONENT` | Component boundaries | Required components exist; non-responsibilities and data ownership are preserved. |
| `PF-COMMON-SECURITY` | Security baseline and control orchestration | Identity, least privilege, network boundaries, secret handling, safe denial, control applicability, validation bindings, and security evidence. |
| `PF-COMMON-GOVERNANCE` | Governance boundary | Governance Policy Runtime remains distinct from Resource Governor and application authority. |
| `PF-COMMON-GATEWAY` | Gateway separation | Publication Gateway authorizes disclosure; the UCKK Publication Bridge performs target-specific packaging and transport; neither owns kOA Mediatheque source records. |
| `PF-COMMON-OFFLINE` | Local continuity | Minimum local operation continues without Internet or upstream control plane. |
| `PF-COMMON-LIFECYCLE` | Lifecycle | Update, rollback, backup, restore, migration, removal, and exit behavior. |
| `PF-COMMON-EVIDENCE` | Evidence validity | Evidence scope, producer, result, release, profile, and freshness are valid. |
| `PF-COMMON-NEGATIVE` | Prohibited behavior | Native AI assumptions, direct cross-component writes, silent fallbacks, and hidden authority fail. |

### 4.5 Base-profile family matrix

Legend:

- `R`: required family;
- `C`: conditionally required according to active capability;
- `P`: prohibited-behavior family;
- `N`: not applicable in the base composition;
- `A`: added through another matrix dimension.

| Test family | User lightweight | Developer Linux | Developer Windows/WSL | Sovereign Linux node | Sovereign hub | Build farm | Control plane |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Common contract and traceability | R | R | R | R | R | R | R |
| Complete Release Set compatibility | R | R | R | R | R | R | R |
| Component data ownership | R | R | R | R | R | R | R |
| Native-AI absence and external-AI boundary | R | R | R | R | R | R | R |
| Minimum local operation offline | R | R | R | R | R | C | R |
| Local user interaction continuity | R | C | C | R | C | N | C |
| Workspace identity and mutable-state isolation | N | R | R | C | C | R | C |
| UV and per-workspace Python environment | N | R | R | C | C | R | C |
| Windows-to-WSL boundary | N | N | R | N | N | N | N |
| Native Linux host lifecycle | C | R | C | R | R | R | R |
| Lightweight resource degradation | R | C | C | C | C | N | C |
| Heavy-service task activation | C | R | R | C | R | C | C |
| Multi-tenant isolation | N | N | N | C | R | C | C |
| Public/private/governance zone separation | C | C | C | C | R | C | R |
| Federation trust and reconciliation | C | C | C | C | R | C | R |
| Publication execution and receipts | C | C | C | C | R | C | C |
| kOA Mediatheque / UCKK publication separation | C | C | C | C | R | C | C |
| Backup and isolated restore | R | C | C | R | R | C | R |
| Credible exit and removal | R | R | R | R | R | R | R |
| Capacity and saturation evidence | C | R | R | R | R | R | R |
| Reproducible build and candidate artifacts | N | R | R | C | C | R | C |
| Build-worker isolation and clean-room behavior | N | C | C | N | C | R | C |
| Fleet coordination non-dependency | N | N | N | C | C | C | R |
| Registry and policy distribution | C | C | C | C | C | C | R |
| Appliance user-interface boundary | C | N | N | C | C | N | N |
| Kubernetes endpoint baseline prohibition | P | P | P | P | P | C | C |
| Direct authoritative storage access prohibition | P | P | P | P | P | P | P |
| Automatic reconnection release prohibition | P | P | P | P | P | P | P |
| Unselected optional component absence | P | P | P | P | P | P | P |

The table selects families, not individual test cases. The test catalog resolves each family into exact tests.

### 4.6 User lightweight matrix

The user-lightweight profile emphasizes:

- local startup and user-visible health;
- operation without external AI;
- Ariane local navigation independent from external voice;
- deterministic local kOA Mediatheque behavior;
- bounded resources and safe optional-service absence;
- local identity and governance;
- offline continuity;
- local data ownership;
- backup, restore, update, rollback, and exit;
- no direct cross-component writes;
- no hidden dependency on a control plane.

Tests for SenTient, external voice, remote publication, federation, or heavy services become conditional only when those capabilities are explicitly selected.

### 4.7 Developer Linux matrix

The developer Linux profile includes profile-declared tests such as:

- `TEST-PROFILE-DEV-LINUX-001`;
- `TEST-DEV-WS-001`;
- `TEST-DEV-UV-001`;
- `TEST-DEV-UV-002`;
- `TEST-DEV-SVC-001`;
- `TEST-DEV-PORT-001`;
- `TEST-DEV-DATA-001`;
- `TEST-DEV-SECRET-001`;
- `TEST-DEV-PARALLEL-001`;
- `TEST-DEV-RESOURCE-001`;
- `TEST-DEV-OFFLINE-001`;
- `TEST-DEV-AI-001`;
- `TEST-DEV-PUBLISH-001`.

The catalog owns the procedures and outcomes for these identities.

The matrix covers per-workspace `.venv`, isolated ports, services, data, secrets, databases, resource budgets, parallel worktrees, rootless-container behavior where selected, native-process equivalence, deterministic kOA Mediatheque processing, separately optional UCKK publication and UCKK import when selected, quarantine-before-acceptance, offline learning-package use, optional SenTient isolation, and candidate-artifact publication.

### 4.8 Developer Windows and WSL matrix

The Windows and WSL profile adds:

- Windows host and WSL distribution identity;
- Linux-native mutable toolchain state;
- path normalization across Windows and WSL;
- case-folding and mount-alias collision detection;
- port exposure and loopback behavior;
- resource limits across host and WSL;
- restart and recovery of WSL services;
- editor integration without identity ownership;
- equivalent workspace, UV, service, data, secret, offline, AI-boundary, and publication outcomes.

Tests that validate only native Linux host mechanisms do not transfer automatically. Equivalent behavior requires platform-scoped evidence.

### 4.9 Sovereign Linux node matrix

The sovereign Linux node matrix emphasizes:

- local autonomy;
- boot, service, storage, and recovery state;
- system-image updates;
- previous-good and recovery targets;
- backup and isolated restore;
- data migrations;
- local identity, governance, audit, and administration;
- network boundaries;
- bounded local Mediatheque operation, optional queued UCKK publication, controlled UCKK learning-package import, quarantine, separate local identity creation, and offline use where selected;
- offline operation;
- hardware and storage health;
- node removal and data export.

Cluster and multi-tenant tests remain conditional unless the profile composition activates them.

### 4.10 Sovereign hub matrix

The sovereign hub profile includes profile-declared tests such as:

- `TEST-PROFILE-HUB-001`;
- `TEST-HUB-TOPOLOGY-001`;
- `TEST-HUB-NETWORK-001`;
- `TEST-HUB-TENANT-001`;
- `TEST-HUB-DATA-001`;
- `TEST-HUB-GOV-001`;
- `TEST-HUB-PUBLICATION-001`;
- `TEST-HUB-OFFLINE-001`;
- `TEST-HUB-FEDERATION-001`;
- `TEST-HUB-RESOURCE-001`;
- `TEST-HUB-BACKUP-001`;
- `TEST-HUB-RESTORE-001`;
- `TEST-HUB-EXIT-001`;
- `TEST-HUB-RELEASE-001`;
- `TEST-HUB-SECURITY-001`;
- `TEST-HUB-CAPACITY-001`.

The matrix covers required components, logical zones, default-deny networking, tenant isolation, directional UCKK publication and import, import quarantine and local acceptance, federation trust, offline continuity, queue revalidation, resource reserves, backup, restore, exit, release rollback, load, capacity, governance/resource separation, and optional-service isolation.

### 4.11 Build farm matrix

The build-farm matrix emphasizes:

- clean worker initialization;
- workspace and dependency isolation;
- pinned toolchains;
- deterministic and reproducible builds where the artifact contract requires it;
- source and dependency provenance;
- candidate-artifact identity;
- test execution and evidence;
- parallel-worker containment;
- resource and queue limits;
- secret minimization;
- no production credentials;
- no direct publication into authoritative release channels;
- signed handoff to the release process;
- worker cleanup;
- offline or mirrored dependency behavior according to the profile.

A build result is candidate material until the applicable release and artifact contracts accept it.

### 4.12 Control-plane matrix

The control-plane matrix emphasizes:

- coordination without becoming required for minimum local operation;
- registry and policy distribution;
- node and profile inventory;
- signed artifact and Release Set distribution;
- bounded fleet operations;
- administrative separation;
- tenant and authority scope;
- offline node continuity;
- stale-state and reconnection handling;
- audit and evidence;
- credential and route revocation;
- control-plane loss;
- node removal;
- no direct ownership of component application data;
- no silent activation of remote changes.

The control plane can coordinate. It cannot substitute for local identity, governance, lifecycle, or recovery authority where those functions are required locally.

### 4.13 Overlay addition matrix

| Overlay family | High assurance | Sovereign offline | Appliance shell |
| --- | --- | --- | --- |
| Overlay contract and compatibility | R | R | R |
| Base-profile regression | R | R | R |
| Stronger identity and session controls | R | C | C |
| Separation of duties and human review | R | C | C |
| Selective evidence and restricted disclosure | R | R | C |
| Failure containment and recovery evidence | R | R | R |
| Sustained Internet absence | C | R | C |
| Public DNS and upstream-control-plane absence | C | R | C |
| Offline update and removable-media exchange | C | R | C |
| External integration absence | C | R | C |
| Constrained local user interface | C | C | R |
| Bounded administration and recovery entry | R | R | R |
| Hidden general-purpose desktop absence | C | C | R |
| Local Ariane navigation where selected | C | C | R |
| Overlay removal and base-profile restoration | R | R | R |

An overlay can turn a base conditional family into a required family. It cannot convert a base prohibition into permission unless a canonical profile decision explicitly changes the architecture.

### 4.14 Component-selection additions

For every selected component, the matrix adds:

- component contract validation;
- responsibility and non-responsibility tests;
- authoritative-data ownership tests;
- interface and event tests;
- dependency failure tests;
- offline behavior tests;
- resource tests;
- security tests;
- lifecycle tests;
- removal tests;
- evidence tests.

For every unselected optional component, the matrix adds absence tests when the profile contract requires proof that no service, data, route, credential, queue, or dependency remains active.

### 4.15 Evidence binding

Each result binds to:

- matrix identity;
- test identity and version;
- subject profile composition;
- execution environment;
- active Release Set;
- component and integration versions;
- data and workload shape;
- start and completion time;
- producer identity;
- observed result;
- evidence references;
- validity interval;
- exceptions;
- limitations.

Evidence from another matrix composition is reusable only when the test catalog and evidence contract explicitly permit reuse and the scopes match.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-PROF-001,REQ-CONF-PROF-002,REQ-CONF-PROF-003,REQ-CONF-PROF-004,REQ-CONF-PROF-005,REQ-CONF-PROF-006,REQ-CONF-PROF-007,REQ-CONF-PROF-008,REQ-CONF-PROF-009,REQ-CONF-PROF-010,REQ-CONF-PROF-011,REQ-CONF-PROF-012,REQ-CONF-PROF-013,REQ-CONF-PROF-014,REQ-CONF-PROF-015,REQ-CONF-PROF-016,REQ-CONF-PROF-017,REQ-CONF-PROF-018,REQ-CONF-PROF-019,REQ-CONF-PROF-020,REQ-CONF-PROF-021,REQ-CONF-PROF-022,REQ-CONF-PROF-023,REQ-CONF-PROF-024,REQ-CONF-PROF-025,REQ-CONF-PROF-026,REQ-CONF-PROF-027,REQ-CONF-PROF-028,REQ-CONF-PROF-029,REQ-CONF-PROF-030,REQ-CONF-PROF-031,REQ-CONF-PROF-032,REQ-CONF-PROF-033 -->
- **REQ-CONF-PROF-001 — SHALL:** Every profile conformance claim bind to one exact base profile, overlay set, component selection, integration set, topology, platform, configuration, active Release Set, test-catalog version, and evidence scope.
- **REQ-CONF-PROF-002 — SHALL:** The profile matrix derive test applicability from canonical profile, overlay, component, integration, requirement, lock, traceability, and test-catalog records.
- **REQ-CONF-PROF-003 — SHALL NOT:** A manually curated checklist, example, dashboard, prior result, or undocumented convention replace the generated profile matrix.
- **REQ-CONF-PROF-004 — SHALL:** Every catalog test receive exactly one applicability state for the matrix composition.
- **REQ-CONF-PROF-005 — SHALL NOT:** A `not_applicable`, `blocked`, `not_run`, `cancelled`, or `invalid` test be counted as `pass`.
- **REQ-CONF-PROF-006 — SHALL:** A `not_applicable` decision identify the absent capability and the canonical predicate that permits exclusion.
- **REQ-CONF-PROF-007 — SHALL:** A prohibited capability be validated through active negative tests rather than omitted as not applicable.
- **REQ-CONF-PROF-008 — SHALL:** Every required and resolved conditional test produce a valid terminal result and scoped evidence.
- **REQ-CONF-PROF-009 — SHALL:** Missing, stale, incompatible, unresolvable, or invalid evidence produce a blocked conformance outcome for the affected claim.
- **REQ-CONF-PROF-010 — SHALL:** Any failed required or prohibited-behavior test produce a non-conformant profile outcome.
- **REQ-CONF-PROF-011 — SHALL:** Overlay tests be added to the compatible base-profile matrix without replacing base tests.
- **REQ-CONF-PROF-012 — SHALL NOT:** An overlay weaken a base-profile requirement, lock, prohibition, component boundary, data-ownership rule, or offline guarantee without an explicit canonical authority change.
- **REQ-CONF-PROF-013 — SHALL:** Selection of an optional component or integration activate its component, boundary, security, resource, offline, lifecycle, removal, and evidence tests.
- **REQ-CONF-PROF-014 — SHALL:** Exclusion of an optional component activate required absence tests for its service, route, credential, data, queue, and dependency state.
- **REQ-CONF-PROF-015 — SHALL:** Platform-specific implementations produce evidence for their actual mechanisms and equivalent required outcomes.
- **REQ-CONF-PROF-016 — SHALL NOT:** Native Linux evidence automatically prove Windows and WSL behavior, or Windows and WSL evidence automatically prove native Linux behavior.
- **REQ-CONF-PROF-017 — SHALL:** Every profile validate minimum local operation without Internet and without an upstream control plane according to its profile contract.
- **REQ-CONF-PROF-018 — SHALL NOT:** External AI, SenTient, containers, Kubernetes, federation, a GPU, or remote services become implicit prerequisites when the active profile does not require them.
- **REQ-CONF-PROF-019 — SHALL:** Profile tests verify component data ownership and reject direct cross-component authoritative writes.
- **REQ-CONF-PROF-020 — SHALL:** Profile tests verify that kOA Mediatheque remains the local media authority, Publication Gateway authorizes outbound disclosure, UCKK Publication Bridge performs only target-specific packaging and transport, and UCKK Import Bridge cannot create local authoritative state before quarantine validation and explicit acceptance.
- **REQ-CONF-PROF-021 — SHALL:** Lifecycle coverage include applicable update, rollback, backup, restore, migration, removal, exit, and recovery tests.
- **REQ-CONF-PROF-022 — SHALL:** Resource and capacity tests cover declared limits, protected reserves, queues, heavy-work admission, saturation, containment, and cleanup.
- **REQ-CONF-PROF-023 — SHALL:** Security tests cover identity, trust, authorization, network boundaries, secrets, privileged operations, selective evidence, and safe denial.
- **REQ-CONF-PROF-024 — SHALL:** Offline and reconnection tests verify that queued work remains unexecuted until complete revalidation.
- **REQ-CONF-PROF-025 — SHALL:** Evidence bind to the matrix, test, profile composition, platform, topology, Release Set, component versions, workload, producer, time, and result.
- **REQ-CONF-PROF-026 — SHALL NOT:** Evidence be reused across profiles, overlays, platforms, topologies, releases, workloads, or time periods unless the evidence contract and test catalog permit the exact reuse.
- **REQ-CONF-PROF-027 — SHALL:** A material change to profile, overlay, component, integration, topology, platform, configuration, Release Set, test catalog, traceability, or evidence validity make the affected matrix stale.
- **REQ-CONF-PROF-028 — SHALL:** Exceptions remain test-visible, scoped, approved, unexpired, and unable to convert a failed test into a pass.
- **REQ-CONF-PROF-029 — SHALL:** The final conformance record list all required, conditional, prohibited, not-applicable, blocked, failed, invalid, cancelled, and not-run counts with their identities.
- **REQ-CONF-PROF-030 — SHALL NOT:** A profile, recipe, test runner, orchestration platform, generated context, or implementation convenience silently alter matrix applicability or result semantics.
- **REQ-CONF-PROF-031 — SHALL:** Applicable profile matrices test UCKK import source validation, complete-package quarantine, integrity, license, rights, provenance, shared-frame compatibility, separate local identities, and import receipts.
- **REQ-CONF-PROF-032 — SHALL:** Applicable offline profile matrices prove that accepted UCKK learning packages remain usable without network access and that incomplete packages remain quarantined.
- **REQ-CONF-PROF-033 — SHALL NOT:** Profile tests accept automatic upload, download, overwrite, deletion, progress transfer, or bidirectional synchronization on reconnection.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Matrix generation

Matrix generation proceeds through:

1. Resolve the base profile contract.
2. Resolve profile inheritance.
3. Resolve the explicit overlay set.
4. Validate overlay compatibility and order.
5. Resolve required and selected optional components.
6. Resolve active integrations and external adapters.
7. Resolve platform, implementation, and topology.
8. Resolve tenants, authority domains, workspaces, and zones where applicable.
9. Resolve the active Release Set.
10. Load requirements, locks, traceability, test catalog, and evidence rules.
11. Load `contracts/security-controls.contract.json` and resolve every control for the effective profile composition.
12. Add each required control's declared validation binding.
13. Add negative tests or verified-absence checks for prohibited controls.
14. Record machine-resolvable reasons for not-applicable controls.
15. Resolve recommended controls to implementation validation or an accepted bounded rationale.
16. Evaluate every remaining test applicability predicate.
17. Detect unresolved predicates or control bindings.
18. Emit the immutable execution matrix.
19. Validate matrix completeness.

### 6.2 Matrix lifecycle

The matrix lifecycle is:

`text
generated
 -> validated
 -> ready
 -> executing
 -> evaluating
 -> conformant | non_conformant | blocked
 -> superseded
`

Supporting states include:

`text
stale
cancelled
invalid
`

A stale or superseded matrix cannot support a new conformance claim.

### 6.3 Test preparation

Before execution:

1. Resolve the test identity and version.
2. Resolve expected result and negative conditions.
3. Resolve the subject scope.
4. Resolve required fixtures and workload.
5. Resolve destructive-test isolation.
6. Resolve evidence producer.
7. Resolve platform mechanism.
8. Resolve required authority and approvals.
9. Confirm recovery readiness.
10. Confirm active matrix state.
11. Mark the test ready.

### 6.4 Test execution

Execution proceeds through:

1. Record start time and environment.
2. Confirm profile and Release Set identity.
3. Apply the declared fixture.
4. Execute the catalog procedure.
5. Capture bounded observations.
6. Restore or clean test state.
7. Record terminal result.
8. Produce evidence.
9. Validate evidence structure.
10. Link evidence to the matrix and traceability registry.

A destructive test runs only in its declared isolated environment or approved maintenance context.

### 6.5 Conditional applicability resolution

A conditional test is resolved through:

1. Read the catalog predicate.
2. Read the relevant profile, overlay, component, integration, security-control, or configuration value.
3. Record the value and source.
4. Set applicability to required when true.
5. Set applicability to not applicable only when false and catalog exclusion is permitted.
6. Set applicability to blocked when the value cannot be resolved.
7. Preserve the resolution evidence.

### 6.6 Negative-test execution

A prohibited-behavior test:

1. Identifies the forbidden capability or path.
2. Attempts the bounded prohibited action or inspects verified absence.
3. Confirms denial, absence, quarantine, or containment.
4. Confirms unrelated capabilities continue.
5. records security and audit evidence;
6. Produces pass only when the prohibited behavior remains unavailable.

Examples include direct database writes, unselected service startup, automatic queue release, native-AI dependency, hidden external fallback, and gateway bypass.

A security control with applicability `prohibited` remains active in the matrix even when the prohibited implementation is absent. Its evidence confirms absence, denial, quarantine, or containment for the evaluated subject.

### 6.7 Result evaluation

Evaluation proceeds through:

1. Validate every result against its catalog contract.
2. Validate evidence scope and freshness.
3. Count results by applicability and terminal state.
4. detect failed required tests;
5. Detect failed prohibited-behavior tests.
6. Detect blocked or missing evidence.
7. Detect stale matrix inputs.
8. Detect invalid exceptions.
9. Calculate the claim outcome.
10. Produce the conformance record.

Outcome logic is:

- `non_conformant` when any required or prohibited-behavior test fails;
- `blocked` when no failure exists but a required test, predicate, dependency, or evidence remains blocked, invalid, not run, cancelled, or stale;
- `conformant` only when every required and prohibited-behavior test passes with valid evidence and all not-applicable decisions are valid.

### 6.8 Change impact

When an input changes:

1. Identify the changed profile, overlay, component, integration, platform, topology, configuration, release, catalog, traceability, or evidence record.
2. Traverse traceability to affected tests.
3. Mark affected matrix entries stale.
4. Preserve unaffected evidence only when reuse rules permit it.
5. regenerate the matrix;
6. Execute affected tests.
7. Re-evaluate the claim.

### 6.9 Exception handling

A test-related exception proceeds through:

1. Identify the affected requirement, lock, test, and profile scope.
2. Validate human approval and expiry.
3. preserve the original expected result;
4. Record compensating controls.
5. Execute the test normally.
6. Record pass, fail, or blocked without rewriting it.
7. Evaluate whether the exception permits activation despite the known deviation.
8. Keep the conformance claim distinct from exception-authorized operation.
9. Expire and retest at the declared time.

### 6.10 Evidence retirement

Evidence retirement proceeds through:

1. Detect expiry, supersession, environment change, or invalidation.
2. Identify matrices and claims that reference the evidence.
3. Mark affected claims stale or blocked.
4. Preserve historical records.
5. produce replacement evidence;
6. Re-evaluate current claims.
7. Retire only after references and retention requirements are satisfied.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Base profile unresolved | Block matrix generation. | Existing historical claims | New profile claim |
| Overlay incompatible | Reject the composition. | Valid base profile | Invalid overlay claim |
| Component selection ambiguous | Block affected applicability. | Resolved components | Complete claim |
| Test catalog unavailable | Use no inferred procedures and block generation. | Historical records | New execution matrix |
| Traceability gap | Block affected claim. | Resolved test paths | Completeness claim |
| Applicability predicate unresolved | Mark the test blocked. | Other resolved tests | Conformant outcome |
| Required test not run | Keep claim blocked. | Existing valid results | Conformant outcome |
| Negative test omitted | Keep claim blocked. | Other test results | Prohibition claim |
| Test fails | Mark profile non-conformant. | Evidence and unrelated tests | Conformant claim |
| Evidence missing | Mark affected result blocked or invalid. | Observations without claim | Evidence-backed pass |
| Evidence stale | Mark affected matrix stale. | Historical evidence | Current claim |
| Wrong platform evidence | Reject reuse. | Source-platform claim | Target-platform claim |
| Release Set changed | Mark affected tests stale. | Previous release history | New release claim |
| Test environment contaminated | Invalidate the result and clean the environment. | Other isolated tests | Contaminated result |
| Cleanup fails | Preserve evidence and block affected scope. | Unrelated environment | Completion claim |
| Destructive test escapes scope | Stop execution and initiate incident handling. | Protected unaffected systems | Continued test run |
| Exception expired | Remove operational authorization and retest. | Historical exception record | Continued exception use |
| Evidence producer untrusted | Reject the evidence. | Raw observations where safe | Valid pass |
| Matrix generator incompatible | Preserve last valid matrix and block new claim. | Historical claim | Candidate matrix |
| One profile fails | Isolate the outcome. | Other profile claims | Failed profile only |

Safe degradation preserves historical evidence and valid claims while refusing broader conformance. It does not infer applicability, convert blocked results into passes, reuse mismatched evidence, or omit negative tests.

## 8. Cross-Component Interactions

### 8.1 Profile contracts

Profile contracts declare:

- profile identity;
- inheritance;
- overlay compatibility;
- component selection;
- operating modes;
- hardware and resource envelope;
- offline behavior;
- security and lifecycle expectations;
- conformance prerequisites;
- profile-specific test IDs.

The matrix reads these declarations and does not rewrite them.

Profile contracts provide composition facts. `contracts/security-controls.contract.json` separately owns cross-profile security-control applicability, and the matrix combines both without copying either authority.

### 8.2 Component contracts

Component contracts add tests for:

- responsibilities;
- non-responsibilities;
- data ownership;
- interfaces;
- dependencies;
- state transitions;
- failure behavior;
- offline behavior;
- security;
- resources;
- profile bindings;
- lifecycle;
- removal.

A selected component activates its applicable tests in every profile composition.

### 8.3 Requirements and locks

Requirements define normative behavior. Locks define cross-record alignment.

The traceability registry maps them to tests. A matrix does not invent coverage merely because a test name appears relevant.

### 8.4 Test catalog

The test catalog owns:

- test ID;
- version;
- purpose;
- procedure;
- applicability predicate;
- fixtures;
- expected result;
- negative expectation;
- evidence type;
- cleanup;
- timeout;
- destructive scope;
- reuse rules.

The matrix owns the resolved selection and execution status for one composition.

For security controls, the declared validation binding is authoritative for coverage. A test catalog entry counts toward a `control_id` only when that binding resolves explicitly.

### 8.5 Evidence registry

The evidence registry validates the producer, subject, result, scope, versions, time, and lifecycle of evidence.

A test runner can create evidence. It cannot declare the evidence valid outside the evidence contract.

### 8.6 Release lifecycle

System, services, governance, and knowledge releases remain independent channels. The active signed Release Set binds tested-compatible versions.

A profile conformance claim applies to that exact Release Set. Updating one channel invalidates only the affected test scope when traceability proves isolation; otherwise the full compatibility set is retested.

### 8.7 Resource Governor

Resource Governor provides bounded test resources, queues, concurrency, and isolation.

It does not change applicability or expected results because a test is expensive.

### 8.8 Governance Policy Runtime

Governance Policy Runtime can authorize protected test operations and fixtures.

It does not convert a failing behavior into conformance or hide a test result.

### 8.9 Build farm

The build farm can execute tests and produce candidate artifacts and evidence.

Build-farm execution does not by itself prove endpoint, hub, Windows/WSL, offline, hardware, network, or recovery behavior unless the test contract uses a representative environment and permits that evidence scope.

### 8.10 Control plane

The control plane can coordinate matrix distribution, execution scheduling, and result collection.

Local nodes retain the ability to verify profile identity, test scope, evidence, and operation without treating the control plane as the final authority for local conformance.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the profile-matrix model.

The following assumptions are prohibited:

1. Every profile runs the same test list.
2. A successful generic test proves profile-specific behavior.
3. An optional component can be ignored without absence testing.
4. A not-applicable test is a pass.
5. A blocked test is a pass.
6. A skipped negative test proves the prohibited behavior is absent.
7. One platform’s evidence proves another platform.
8. One topology’s evidence proves another topology.
9. One Release Set’s evidence proves another Release Set.
10. One tenant’s isolation test proves every tenant configuration.
11. A development workstation test proves a sovereign-hub claim.
12. A build-farm result proves endpoint runtime behavior.
13. Container tests prove native-process behavior automatically.
14. Native-process tests prove container isolation automatically.
15. Kubernetes is required for every profile.
16. External AI availability is required for conformance.
17. SenTient installation means SenTient activation.
18. Internet connectivity is required for minimum local conformance.
19. An overlay can replace base-profile tests.
20. An overlay can silently weaken a prohibition.
21. Passing schema validation proves runtime conformance.
22. Passing runtime tests proves traceability completeness.
23. A test name proves requirement coverage without a traceability record.
24. Evidence remains valid indefinitely.
25. A dashboard count is the canonical result.
26. An exception changes the observed result.
27. An approved exception creates a conformant claim automatically.
28. A matrix remains current after profile or release changes.
29. Historical evidence can be relabeled for a new composition.
30. A recipe or test-runner default owns applicability.

When profile composition, test applicability, evidence scope, platform equivalence, release compatibility, or exception status is uncertain, the claim remains blocked.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-CONF-004`.
2. Its path is `09-conformance/04-profile-test-matrices.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `conformance`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every base profile resolves to one active profile contract.
16. Every overlay resolves to one active overlay contract.
17. Every matrix resolves the exact base profile and overlay composition.
18. Required, conditional, not-applicable, prohibited, and blocked applicability states are mutually exclusive.
19. Pass, fail, blocked, not-run, invalid, and cancelled results are mutually exclusive.
20. Not-applicable entries include valid predicates and canonical sources.
21. Prohibited capabilities have active negative tests.
22. Selected optional components add their full applicable test families.
23. Unselected optional components add required absence tests where declared.
24. Linux and Windows/WSL evidence remains platform-scoped.
25. Profile-specific test IDs resolve through profile contracts and the test catalog.
26. Every required and prohibited-behavior result has valid evidence.
27. Evidence resolves to the exact matrix, profile, Release Set, platform, topology, workload, and time scope.
28. Failed required tests produce non-conformant outcomes.
29. Missing, stale, invalid, cancelled, blocked, or not-run required tests prevent conformant outcomes.
30. Overlay matrices preserve all base-profile tests.
31. Material input changes mark affected matrix entries stale.
32. Exceptions remain separate from observed results and conformance outcomes.
33. Final records list counts and identities for every applicability and result state.
34. Traceability from decisions, requirements, locks, tests, evidence, profiles, components, and Release Sets is complete.
35. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
36. Complete documentation validation returns `pass`.

Additional security-control validation confirms:

1. every active control resolves to exactly one applicability state for the effective profile;
2. every required control resolves to at least one applicable validation binding;
3. every prohibited control resolves to a negative test or verified-absence method;
4. every not-applicable control records a machine-resolvable predicate and source fact;
5. every recommended control records implementation validation or an accepted bounded rationale;
6. every security result references evidence valid against `contracts/artifact-contracts/security-evidence.schema.json`;
7. `docs/tools/check_security_architecture.py` passes.

## 11. Non-Normative Examples

### 11.1 Lightweight profile without SenTient

A user-lightweight deployment does not select SenTient. SenTient functional tests are not applicable, while absence, no-route, no-service, no-data, and no-native-AI-dependency tests remain active.

### 11.2 Lightweight profile with SenTient selected

The same base profile explicitly selects SenTient under a compatible composition. SenTient isolation, task activation, resources, data boundaries, failure, offline behavior, removal, and non-authoritative-output tests become required.

### 11.3 Developer Linux and Windows/WSL

Both developer profiles run workspace, UV, port, service, data, secret, resource, offline, and publication-boundary families. Windows/WSL additionally runs path translation, mount alias, case folding, WSL resource, host-port exposure, and restart recovery tests.

### 11.4 Sovereign hub with offline overlay

A sovereign hub with `sovereign_offline` runs all hub tests plus sustained Internet absence, public-DNS absence, removable-media update, offline support exchange, local trust, queue non-release, and reconnection revalidation tests.

### 11.5 High-assurance overlay

A sovereign Linux node with `high_assurance` retains every node test. It adds stronger session, separation-of-duty, evidence, recovery, and protected-operation tests. It does not remove ordinary node lifecycle or offline tests.

### 11.6 Build result reuse

A build farm produces evidence that a package built reproducibly. The evidence can support the artifact build claim. It does not prove that the package boots, restores, operates offline, or preserves user interaction on a lightweight endpoint.

### 11.7 Not-applicable result

A profile has no federation capability. Federation functional tests are marked not applicable with the profile capability predicate. A separate negative test verifies that no federation route, credential, queue, or peer service is active.

### 11.8 Blocked evidence

A required restore test completes, but its evidence references the previous Release Set. The result cannot support the current matrix and the profile claim remains blocked.

### 11.9 Exception

A temporary hardware exception authorizes reduced redundancy. The redundancy test still records its observed failure. The exception permits bounded operation but does not turn the profile result into a pass.

### 11.10 Control-plane outage

A node matrix includes a test that disconnects the control plane. The node continues its declared local capabilities, retains local identity and governance behavior, queues eligible remote work, and requires revalidation before reconnection release.

## kOA Spaces Test Projection

When a profile selects kOA Spaces, its effective test matrix includes subsystem presence, artifact-schema validation, route collision checks, capability visibility, authorization non-bypass, offline behavior, accessibility, resource bounds, health, activation, rollback, backup scope, and fallback availability. Omitted kOA Spaces does not fail a profile that classifies it as optional.
