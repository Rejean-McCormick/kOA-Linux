<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-013",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global",
    "system_baseline",
    "deployment_profiles"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-PROFILE-001",
    "contracts/system.contract.json",
    "generated/profile-catalog.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-hub.profile.json",
    "contracts/profiles/build-farm.profile.json",
    "contracts/profiles/control-plane.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/profiles/appliance-shell.profile.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-SYS-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-LIFE-001",
    "DEC-HW-001",
    "DEC-DEV-001"
  ],
  "requirement_ids": [
    "REQ-PROF-MODEL-001",
    "REQ-PROF-MODEL-002",
    "REQ-PROF-MODEL-003",
    "REQ-PROF-MODEL-004",
    "REQ-PROF-MODEL-005",
    "REQ-PROF-MODEL-006",
    "REQ-PROF-MODEL-007",
    "REQ-PROF-MODEL-008",
    "REQ-PROF-MODEL-009",
    "REQ-PROF-MODEL-010",
    "REQ-PROF-MODEL-011",
    "REQ-PROF-MODEL-012",
    "REQ-PROF-MODEL-013",
    "REQ-PROF-MODEL-014",
    "REQ-PROF-MODEL-015",
    "REQ-PROF-MODEL-016",
    "REQ-PROF-MODEL-017",
    "REQ-PROF-MODEL-018",
    "REQ-PROF-MODEL-019",
    "REQ-PROF-MODEL-020",
    "REQ-PROF-MODEL-021",
    "REQ-PROF-MODEL-022",
    "REQ-PROF-MODEL-023",
    "REQ-PROF-MODEL-024",
    "REQ-PROF-MODEL-025",
    "REQ-PROF-MODEL-026"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-001",
    "LOCK-DOC-002",
    "LOCK-DOC-003",
    "LOCK-DOC-011",
    "LOCK-DOC-012",
    "LOCK-DOC-013",
    "LOCK-DOC-015",
    "LOCK-DOC-016",
    "LOCK-DOC-017",
    "LOCK-DOC-018",
    "LOCK-DOC-021",
    "LOCK-DOC-022",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AUTH-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-004",
    "DOC-SYS-001",
    "DOC-PROF-011",
    "DOC-SEC-000",
    "DOC-OPS-018",
    "DOC-CONF-009",
    "DOC-ADR-003"
  ],
  "tags": [
    "architecture-decision",
    "system-baseline",
    "deployment-profiles",
    "primary-profile",
    "profile-overlay",
    "scope-separation",
    "composition",
    "canonical-ownership",
    "implementation-separation",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# ADR-013 — System Baseline and Profile Separation

**ADR ID:** `ADR-013`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `owner:profile-architecture`  
**Owner decision:** `DEC-PROFILE-001`  
**Change packet:** `CHG-2026-0013`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

kOA separates the global system baseline from deployable profiles.

The global baseline defines universal system roles, first-class components, authority and data boundaries, operating modes, AI and integration boundaries, safe degradation, and artifact lifecycle invariants. It defines the capability and contract universe, not one universal installation.

Every deployable environment selects exactly one primary profile and can compose zero or more explicitly compatible overlays.

Primary profiles are:

```text
user_lightweight
developer_linux_workstation
developer_windows_wsl
sovereign_linux_node
sovereign_hub
build_farm
control_plane
```

Composable overlays are:

```text
high_assurance
sovereign_offline
appliance_shell
```

Container engines, virtual machines, desktop environments, service managers, package managers, and orchestrators are implementation technologies or profile properties rather than standalone deployment profiles.

## 2. Scope

### 2.1 Included scope

- ownership of the global system baseline;
- primary-profile and overlay identities;
- profile compatibility and composition;
- profile inheritance and exclusion;
- component membership ownership;
- profile-scoped hardware, topology, resources, networks, storage, backup, and recovery;
- implementation-technology separation;
- conformance and traceability for composed deployments;
- migration of deprecated global statements into profile-scoped requirements.

### 2.2 Excluded scope

- the detailed content of each primary profile;
- the detailed controls of each overlay;
- one operating-system distribution;
- one desktop environment;
- one container or virtual-machine runtime;
- one orchestrator;
- one filesystem, database, or network topology;
- one hardware model;
- one implementation recipe;
- one component's stores, APIs, or internal state model.

Those facts remain with their canonical owners.

### 2.3 Applicability

The decision applies to:

- every active system-baseline document;
- every primary profile;
- every overlay;
- every profile-composition claim;
- every component-membership projection;
- every implementation recipe that discusses deployment technology;
- every generated profile matrix, conformance matrix, authority manifest, and AI context.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-PROFILE-001`
- `DEC-PROFILE-001`

### 3.2 Canonical objects changed or constrained

- `contracts/system.contract.json`
- `generated/profile-catalog.json`
- `contracts/profiles/*.profile.json`
- `generated/component-catalog.json`
- `generated/requirements-index.json#/requirements/REQ-PROF-MODEL-001`
- `generated/requirements-index.json#/requirements/REQ-PROF-MODEL-026`
- `generated/assertion-index.json#/locks/LOCK-PROFILE-001`
- `generated/assertion-index.json#/locks/LOCK-PROFILE-002`

### 3.3 Related documents

- `DOC-SYS-001` — `02-system/01-system-context.md`
- `DOC-PROF-000` — `03-profiles/00-profile-model.md`
- `DOC-PROF-001` through `DOC-PROF-007` — primary-profile documents
- `DOC-PROF-011` through `DOC-PROF-013` — overlay documents
- `DOC-SEC-000` — `07-security/00-threat-model.md`
- `DOC-OPS-018` — `08-operations/18-sovereign-node-operations.md`
- `DOC-CONF-009` — `09-conformance/09-interfile-lock-validation.md`
- `DOC-ADR-003` — `10-adrs/ADR-003-appliance-shell-without-gnome.md`

### 3.4 Related requirements

- `REQ-PROF-MODEL-001` through `REQ-PROF-MODEL-026`

### 3.5 Related locks

- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`
- `LOCK-DOC-003`
- `LOCK-DOC-011`
- `LOCK-DOC-015`
- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-DATA-001`
- `LOCK-AI-001`
- `LOCK-SENT-001`
- `LOCK-LIFE-001` through `LOCK-LIFE-004`
- `LOCK-DEV-001` through `LOCK-DEV-005`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

The source corpus contains global product principles, physical architecture, node-profile descriptions, implementation choices, and recipes written at different times.

Several deprecated documents describe a sovereign appliance image and endpoint hardening as if those choices applied to every kOA deployment. Other sources describe developer workstations, Windows WSL, hubs, build farms, and control planes with materially different needs.

The frozen architecture resolves this by defining one global system model and a separate profile model.

### 4.2 Problem statement

Without a formal separation:

- endpoint hardening can become a universal development requirement;
- developer tooling can become an implied production dependency;
- a desktop choice can become a global system rule;
- a container or orchestrator can be misclassified as a deployment profile;
- a component can appear mandatory everywhere because it is first class globally;
- an overlay can be mistaken for a deployable environment;
- a profile can inherit undeclared requirements;
- the same fact can have competing owners;
- conformance claims can omit the exact profile composition they validate.

The architecture needs one accepted decision defining which facts are global, which are profile owned, and how compositions are resolved.

### 4.3 Why a decision is required

The boundary changes:

- architecture ownership;
- documentation layers;
- requirement scope;
- profile identity;
- component membership;
- implementation freedom;
- test applicability;
- evidence;
- migration and cutover behavior.

This is a major semantic decision.

It cannot be established through a directory layout or an implementation recipe.

### 4.4 Constraints

- Global constitutional and security invariants remain universal.
- Components remain first class even when a profile excludes them.
- Profiles select deployment membership without owning component internals.
- Overlays remain composable and non-deployable.
- Profile conflicts fail closed.
- Optional AI, SenTient, appliance-shell, high-assurance, offline, and orchestration behavior stays scoped.
- Endpoint profiles retain no universal Kubernetes requirement.
- Standard Linux profiles retain maintained desktop choices.
- Release channels remain independent in every profile.
- Recipes remain non-normative unless adopted.
- Active authority remains registry first.

## 5. Decision Drivers

1. Preserve one coherent global product and authority model.
2. Support materially different user, developer, node, hub, build, and control environments.
3. Prevent profile-specific hardening and implementation choices from becoming universal.
4. Prevent global invariants from being weakened by profiles.
5. Give component membership one canonical owner.
6. Make overlay composition deterministic and testable.
7. Preserve implementation freedom inside explicit profile contracts.
8. Support offline, high-assurance, appliance, development, and scaled deployments without parallel architectures.
9. Enable complete impact analysis and conformance.
10. Keep migration from undeclared appliance-centric documentation explicit.

## 6. Considered Options

### 6.1 Option A — Global Baseline Plus One Primary Profile and Compatible Overlays

**Description**

Define one global system baseline, seven primary profiles, and three composable overlays. Every deployment selects one primary profile. Compatible overlays strengthen or modify declared dimensions.

**Advantages**

- Separates universal architecture from deployable realization.
- Supports endpoints, developers, hubs, build farms, and control planes.
- Keeps overlays reusable across compatible primary profiles.
- Makes membership, resources, topology, and network exposure machine readable.
- Prevents implementation technologies from becoming architecture identities.
- Enables scoped conformance and evidence.

**Disadvantages and costs**

- More profile contracts and tests are required.
- Cross-profile changes require impact analysis.
- Effective composed requirements need generated projections.
- Operators and developers need to identify the exact active composition.
- Profile conflict handling becomes an explicit validation responsibility.

**Constraint fit**

This option matches `DEC-PROFILE-001`, `LOCK-PROFILE-001`, and `LOCK-PROFILE-002`.

It preserves component, data, release, AI, authority, and implementation boundaries.

### 6.2 Option B — One Universal Deployment Baseline

**Description**

Define one required deployment stack for every kOA environment.

**Advantages**

- Fewer profile documents.
- Fewer deployment variations.
- Simpler superficial installation narrative.

**Disadvantages and costs**

- Forces endpoint, developer, hub, build, and control-plane needs into one design.
- Makes heavy workbenches and infrastructure appear universal.
- Makes endpoint hardening constrain development unnecessarily.
- Encourages remote-control or cluster dependencies on sovereign endpoints.
- Makes profile-specific resource and hardware values misleading globally.

**Reason rejected**

The option cannot accurately represent the accepted deployment environments.

It conflicts with offline sovereignty, development isolation, high-assurance composition, and endpoint non-Kubernetes rules.

### 6.3 Option C — Independent Product Variants Without a Shared Baseline

**Description**

Treat each deployment profile as a separate architecture with its own components, authority, release rules, and security model.

**Advantages**

- Maximum local freedom for each variant.
- Minimal cross-profile coordination.

**Disadvantages and costs**

- Duplicates authority and component definitions.
- Creates competing canonical owners.
- Makes artifact and release compatibility difficult.
- Produces divergent AI, privacy, data, and recovery boundaries.
- Prevents reliable cross-profile portability and exit.
- Encourages parallel active documentation corpora.

**Reason rejected**

kOA requires one shared product, component, authority, artifact, and governance model.

Profiles realize that model; they do not fork it.

### 6.4 Option D — Technology-Named Profiles

**Description**

Define profiles such as Podman, Kubernetes, GNOME, Wayland, virtual machine, or container deployment.

**Advantages**

- Familiar implementation labels.
- Direct mapping from deployment technology to documentation.

**Disadvantages and costs**

- Confuses purpose and assurance with implementation technology.
- Creates profile explosion.
- Makes technology replacement a profile-identity migration.
- Prevents the same technology from serving several profiles differently.
- Promotes recipes and vendor choices into architecture.

**Reason rejected**

Technology remains a profile property, component requirement, toolchain contract, artifact contract, or recipe.

It does not define the deployment's purpose and authority identity.

## 7. Decision

### 7.1 Selected option

`Option A — Global Baseline Plus One Primary Profile and Compatible Overlays`

### 7.2 Normative effect

`DEC-PROFILE-001` authorizes the following canonical model:

- one global system baseline;
- seven primary deployment profiles;
- three composable overlays;
- exactly one primary profile per deployment;
- zero or more compatible overlays;
- deterministic fail-closed composition;
- profile ownership of deployment membership and envelope;
- component ownership of component internals;
- implementation technology outside profile identity;
- major change control for changes to the boundary.

### 7.3 Required behavior

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROF-MODEL-001,REQ-PROF-MODEL-002,REQ-PROF-MODEL-003,REQ-PROF-MODEL-004,REQ-PROF-MODEL-005,REQ-PROF-MODEL-006,REQ-PROF-MODEL-007,REQ-PROF-MODEL-008,REQ-PROF-MODEL-009,REQ-PROF-MODEL-010,REQ-PROF-MODEL-011,REQ-PROF-MODEL-012,REQ-PROF-MODEL-013,REQ-PROF-MODEL-014,REQ-PROF-MODEL-015,REQ-PROF-MODEL-016,REQ-PROF-MODEL-017,REQ-PROF-MODEL-018,REQ-PROF-MODEL-019,REQ-PROF-MODEL-020,REQ-PROF-MODEL-021,REQ-PROF-MODEL-022,REQ-PROF-MODEL-023,REQ-PROF-MODEL-024,REQ-PROF-MODEL-025,REQ-PROF-MODEL-026 -->
- **REQ-PROF-MODEL-001 — SHALL:** The global system baseline defines universal system roles, first-class component identities, authority and data boundaries, operating modes, global AI and integration boundaries, degradation principles, and artifact lifecycle invariants.
- **REQ-PROF-MODEL-002 — SHALL NOT:** The global system baseline selects one universal operating-system distribution, desktop environment, container engine, orchestrator, hardware envelope, process topology, network topology, storage layout, resource envelope, or component deployment set.
- **REQ-PROF-MODEL-003 — SHALL:** The only primary deployment profile identities are `user_lightweight`, `developer_linux_workstation`, `developer_windows_wsl`, `sovereign_linux_node`, `sovereign_hub`, `build_farm`, and `control_plane` until an accepted profile-model change introduces or retires an identity.
- **REQ-PROF-MODEL-004 — SHALL:** The only composable overlay identities are `high_assurance`, `sovereign_offline`, and `appliance_shell` until an accepted profile-model change introduces or retires an identity.
- **REQ-PROF-MODEL-005 — SHALL:** Every deployable environment selects exactly one active primary profile.
- **REQ-PROF-MODEL-006 — SHALL NOT:** A profile overlay is treated as an independently deployable environment identity.
- **REQ-PROF-MODEL-007 — SHALL:** A deployment composes zero or more overlays only when every selected overlay declares compatibility with the primary profile and with every other selected overlay.
- **REQ-PROF-MODEL-008 — SHALL:** Profile composition combines applicable obligations, intersects permissions, unions prohibitions, applies the most restrictive compatible data and network boundary, and blocks unresolved conflicts.
- **REQ-PROF-MODEL-009 — SHALL:** The primary profile owns deployable component membership, topology, activation mode, hardware placement, resource envelope, storage, network exposure, backup, recovery, and operator model unless it explicitly delegates a dimension to a compatible overlay.
- **REQ-PROF-MODEL-010 — SHALL:** An overlay modifies or strengthens only its declared dimensions and preserves all unaffected primary-profile decisions.
- **REQ-PROF-MODEL-011 — SHALL NOT:** An overlay silently re-enables a capability, component, network path, data class, external integration, or privilege explicitly excluded by the primary profile.
- **REQ-PROF-MODEL-012 — SHALL NOT:** A profile-specific or overlay-specific requirement is represented as a global baseline requirement without a separate accepted global owner decision.
- **REQ-PROF-MODEL-013 — SHALL NOT:** A primary profile or overlay weakens a global constitutional, authority, identity, component, data, privacy, AI, release, or recovery invariant.
- **REQ-PROF-MODEL-014 — SHALL:** Profile inheritance, defaults, optional capabilities, conditional capabilities, exclusions, conflicts, precedence, and compatibility are explicit in machine-readable profile contracts.
- **REQ-PROF-MODEL-015 — SHALL NOT:** A deployment inherits an undeclared profile requirement through prose repetition, filename, directory placement, package presence, host capability, implementation recipe, or component preference.
- **REQ-PROF-MODEL-016 — SHALL:** Component membership is owned by profile contracts, while component identity, responsibilities, stores, interfaces, relationships, and prohibited responsibilities remain owned by component contracts and the component registry.
- **REQ-PROF-MODEL-017 — SHALL NOT:** The component registry, component documentation, or component implementation silently defines global or profile-specific deployment membership.
- **REQ-PROF-MODEL-018 — SHALL NOT:** Container technology, virtual-machine technology, a desktop environment, a service manager, a package manager, or an orchestrator is represented as a standalone deployment profile.
- **REQ-PROF-MODEL-019 — SHALL:** Implementation technology is represented through profile properties, component requirements, toolchain contracts, artifact contracts, and non-normative recipes unless an active profile contract adopts a specific technology.
- **REQ-PROF-MODEL-020 — SHALL:** `contracts/system.contract.json` owns global baseline values, `generated/profile-catalog.json` owns profile and overlay identity and compatibility, and each `contracts/profiles/*.profile.json` file owns its deployable or composable profile contract.
- **REQ-PROF-MODEL-021 — SHALL NOT:** Markdown, examples, recipes, generated matrices, AI contexts, or implementation manifests replace the canonical registry ownership defined by this decision.
- **REQ-PROF-MODEL-022 — SHALL:** Every profile conformance claim identifies the exact primary profile, overlays, effective requirements, component membership, artifacts, Release Set, authority release, exceptions, tests, and evidence.
- **REQ-PROF-MODEL-023 — SHALL:** SenTient, external AI, development toolchains, appliance-shell behavior, high-assurance controls, offline strengthening, and orchestrator use remain scoped to the profiles or overlays that explicitly adopt them.
- **REQ-PROF-MODEL-024 — SHALL NOT:** Endpoint profiles require Kubernetes or another cluster orchestrator unless the exact primary profile explicitly declares, constrains, and validates that orchestrator.
- **REQ-PROF-MODEL-025 — SHALL:** Moving a fact between the global baseline and a profile, changing a primary profile or overlay identity, or changing composition semantics is a major architecture change requiring an accepted decision, ADR, impact report, migration plan, tests, evidence, and authority activation last.
- **REQ-PROF-MODEL-026 — SHALL:** Every active system-baseline and profile-separation claim has complete decision, requirement, lock, system, profile, component, artifact, test, evidence, exception, and authority traceability.
<!-- GENERATED:REQUIREMENTS:END -->

### 7.4 Ownership matrix

| Concept | Scope | Canonical owner | Meaning |
| --- | --- | --- | --- |
| System identity and mission | `Global` | System Registry and constitution | Shared system purpose and protected outcomes. |
| First-class component identities | `Global` | Components Registry | The component universe, responsibilities, ownership, and boundaries. |
| Authority, identity, data, privacy, AI, and release invariants | `Global` | Constitution, System Registry, decisions, locks | Rules that every profile preserves. |
| Operating modes and degradation principles | `Global` | System Registry | Connected, offline, degraded, maintenance, and recovery semantics. |
| Component membership and topology | `Profile` | Primary profile contract | Which components run, where, and under what activation mode. |
| Hardware, resources, storage, and networks | `Profile` | Primary profile and compatible overlays | Concrete deployable envelope and exposure. |
| Assurance strengthening | `Overlay` | High-assurance overlay | Hardware trust, protected custody, separation of duties, and evidence. |
| Offline strengthening | `Overlay` | Sovereign-offline overlay | Extended disconnected operation, local mirrors, and stale-trust behavior. |
| Constrained appliance presentation | `Overlay` | Appliance-shell overlay | Minimal Wayland product session without a global desktop rule. |
| Exact commands and technology realization | `Implementation` | Toolchain contracts and recipes | Non-normative details unless an active profile adopts them. |

### 7.5 Composition rules

| Dimension | Merge rule | Failure rule |
| --- | --- | --- |
| Required obligations | Merge rule | Failure rule | A conflict without declared resolution blocks the composition. |
| Permissions | Merge rule | Failure rule | An overlay cannot broaden primary-profile permission silently. |
| Prohibitions | Merge rule | Failure rule | The stricter prohibition remains effective. |
| Component membership | Merge rule | Failure rule | Excluded components remain excluded unless the primary profile explicitly delegates re-enablement. |
| Network exposure | Merge rule | Failure rule | A blocked path does not reopen because another layer is permissive. |
| Data classification and AI eligibility | Merge rule | Failure rule | No-AI, restricted, audience, consent, and export controls remain effective. |
| Resources | Merge rule | Failure rule | Unsatisfied capacity blocks the affected composition claim. |
| Artifacts and releases | Merge rule | Failure rule | Publication and staging do not imply activation. |
| Tests and evidence | Merge rule | Failure rule | A missing overlay test removes the overlay claim, not the underlying primary claim when safe. |

### 7.6 Prohibited behavior

The selected architecture excludes:

- treating the system baseline as one universal installed stack;
- treating every first-class component as installed in every profile;
- deploying an overlay without a primary profile;
- assigning two primary profiles to one environment;
- silently inheriting undeclared profile rules;
- promoting one profile's operating system, desktop, container, orchestrator, hardware, or topology globally;
- weakening global invariants through profile configuration;
- using component documentation to define profile membership;
- using recipes or generated matrices as canonical owners;
- treating package presence as profile activation;
- representing a control plane as a required dependency for local sovereign-node readiness;
- treating Kubernetes as an endpoint default;
- creating a parallel architecture for each profile.

### 7.7 Defaults

- Global facts remain global only when owned by a global canonical registry or accepted global decision.
- Deployment facts remain profile scoped unless promoted through a separate accepted global decision.
- A deployment has one primary profile.
- Overlays are inactive unless explicitly selected and compatible.
- Unknown composition conflicts block the affected claim.
- Exclusions are explicit.
- Component membership is profile owned.
- Component internals are component owned.
- Implementation technology remains replaceable unless a profile contract adopts it.
- The active conformance claim identifies the exact composition.

### 7.8 Failure and safe-degradation behavior

When profile resolution or composition fails:

- the affected deployment or overlay claim remains blocked;
- no permissive profile is inferred;
- no overlay operates alone;
- no excluded capability becomes active;
- the last validated complete profile composition can remain active when safe;
- unaffected profiles and unrelated claims remain valid;
- diagnostics identify the conflicting profiles, overlays, requirements, resources, artifacts, tests, and evidence;
- authority activation remains blocked until the conflict is resolved.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Global baseline owner

`contracts/system.contract.json` owns:

- global system identity;
- system roles and domains;
- operating modes;
- offline minimum principles;
- first-class component references;
- AI boundary;
- Ariane and UCKK global behavior;
- deterministic language and resource-governance boundaries;
- external integration classes;
- global artifact and degradation principles.

It does not own concrete profile membership or topology.

### 8.2 Profile index owner

`generated/profile-catalog.json` owns:

- primary-profile identities;
- overlay identities;
- lifecycle status;
- compatibility;
- conflicts;
- inheritance model;
- profile paths;
- composition semantics.

### 8.3 Individual profile owner

Each `contracts/profiles/*.profile.json` owns:

- profile type;
- intended deployment;
- required, optional, conditional, task-activated, and excluded components;
- hardware and placement;
- topology and activation mode;
- resources;
- storage and filesystem expectations;
- networks and egress;
- security and identity realization;
- offline envelope;
- release and artifact behavior;
- backup, recovery, operations, and exit;
- tests and evidence.

### 8.4 Component owner

`generated/component-catalog.json` and component contracts own:

- component identity;
- kind;
- responsibilities;
- prohibited responsibilities;
- authoritative data domains;
- stores;
- interfaces;
- events;
- state transitions;
- failures;
- resource semantics;
- observability;
- relationships;
- artifacts;
- conformance.

A component remains first class when a profile excludes it.

### 8.5 Data ownership

Profile composition never transfers authoritative data ownership.

One component remains the owner of each authoritative data domain.

A profile can decide whether and where the component is deployed, not which component owns the data.

### 8.6 Generated and explanatory projections

Profile documents, matrices, catalogs, installation guides, AI contexts, and recipes explain or project canonical facts.

They cannot define new profile identities, defaults, compatibility, component membership, or global invariants.

## 9. Profile and Deployment Effects

| Profile or overlay | Type | Purpose | Separation boundary |
| --- | --- | --- | --- |
| `user_lightweight` | `primary_profile` | Light local user deployment with explicit exclusions for heavy workbenches and infrastructure. | Owns its component, resource, desktop, storage, network, backup, and offline envelope. |
| `developer_linux_workstation` | `primary_profile` | Native Linux development with UV, mutable workspace isolation, local services, and developer tools. | Does not convert development tools or desktop choices into global requirements. |
| `developer_windows_wsl` | `primary_profile` | Windows-hosted WSL development with host and guest boundaries. | Cannot claim host controls that WSL cannot establish. |
| `sovereign_linux_node` | `primary_profile` | Locally controlled Linux node with offline minimum capability, backup, recovery, and independent operation. | Can compose compatible assurance, offline, or appliance overlays. |
| `sovereign_hub` | `primary_profile` | Multi-service sovereign hub with declared scale, storage, network, and federation behavior. | Hub topology does not become an endpoint requirement. |
| `build_farm` | `primary_profile` | Controlled build, validation, reproducibility, and publication-candidate environment. | Orchestration use is explicit and build authority remains separate from signing and activation. |
| `control_plane` | `primary_profile` | Fleet, authority-distribution, policy, release, or coordination control environment. | Does not become a required dependency for local sovereign-node readiness. |
| `high_assurance` | `profile_overlay` | Strengthens compatible primary profiles with hardware trust, protected custody, duty separation, and evidence. | Never operates without one compatible primary profile. |
| `sovereign_offline` | `profile_overlay` | Strengthens disconnected operation, local artifact availability, trust freshness handling, and recovery. | Does not create a separate primary deployment identity. |
| `appliance_shell` | `profile_overlay` | Adds a constrained appliance presentation to a compatible primary profile. | Does not create a global no-GNOME or no-desktop rule. |

### 9.1 Environment identity

A deployed environment identity includes:

- environment ID;
- exactly one primary profile ID and version;
- zero or more overlay IDs and versions;
- effective requirement set;
- effective component membership;
- active Release Set;
- active authority release;
- active exceptions;
- evidence state.

A hostname, operating system, package list, container runtime, or orchestrator does not replace that identity.

### 9.2 Component membership

A profile classifies a component as:

- required;
- optional;
- conditional;
- task activated;
- excluded.

The classification applies only to that profile or composed environment.

It does not alter the component's global identity.

### 9.3 Overlay removal

An overlay can be removed only when:

- the resulting primary profile remains valid;
- no active artifact, key, data, operation, or claim depends on the overlay;
- affected resources and networks remain valid;
- required migration or rollback completes;
- the resulting composition passes tests and evidence.

Removing an overlay does not retire its identity globally.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Global security invariants

Every profile preserves:

- explicit authority;
- identity-layer separation;
- component and data ownership;
- no direct cross-component authoritative writes;
- bounded privilege;
- classified evidence;
- safe degradation;
- artifact verification;
- rollback and recovery;
- rights, consent, audience, withdrawal, and recourse;
- AI non-authority.

A profile can strengthen these controls.

It cannot weaken them.

### 10.2 High-assurance scope

Hardware-backed trust, measured or verified boot, stronger key custody, duty separation, and attestation apply when `high_assurance` is composed.

They are not inferred globally from hardware capability.

### 10.3 Offline scope

Extended disconnected operation, local mirrors, offline trust bundles, and stricter freshness handling apply when the primary profile or `sovereign_offline` overlay declares them.

The global baseline retains local-first and safe-degradation principles without assigning one offline duration or storage topology to every environment.

### 10.4 AI and SenTient scope

The global baseline excludes a native AI dependency and defines the optional external-AI boundary.

Profiles decide whether an approved external integration is available.

SenTient remains available only in compatible developer and build profiles and never becomes a global component-membership requirement.

### 10.5 Privacy and rights scope

Global privacy, consent, cultural-rights, no-AI, attribution, audience, export, and withdrawal invariants apply everywhere.

Profiles own concrete storage, network, encryption, operator, backup, and offline realization.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

The system baseline defines capability-scoped degradation and minimum local principles.

Each profile defines:

- which capabilities remain local;
- which remote capabilities become unavailable;
- trust and revocation freshness behavior;
- local artifact availability;
- local storage and capacity;
- backup targets;
- synchronization queues;
- recovery path.

### 11.2 Resource behavior

The system baseline defines deterministic resource governance and protection priorities.

Profiles define:

- CPU and memory envelope;
- storage and I/O;
- queue and concurrency limits;
- task activation;
- reservations;
- optional heavy work;
- pressure behavior appropriate to the deployment.

### 11.3 Operations

Operational documents apply through the selected profile.

A sovereign-node procedure does not become a developer-workstation procedure by default.

A build-farm procedure does not become an endpoint requirement.

### 11.4 Backup and recovery

The global baseline requires credible backup, restore, and exit.

Profiles define:

- data classes and objectives;
- target placement;
- independent and offline copies;
- recovery environment;
- operator roles;
- restore cadence;
- high-assurance key handling;
- environment-specific evidence.

### 11.5 Desktop, containers, and orchestration

A primary profile can select:

- GNOME;
- KDE Plasma;
- an appliance shell;
- no graphical session;
- rootless containers;
- constrained containers;
- virtual machines;
- host services;
- an orchestrator.

The selected technology remains subordinate to the profile's purpose, authority, security, resource, backup, recovery, and exit contract.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`global_foundational`

Every active profile, overlay, component-membership claim, deployment document, recipe, and conformance claim is compatible only when it preserves this separation.

### 12.2 Affected release channels

- `system`
- `services`
- `governance`
- `knowledge`

The profile selects compatible artifacts across all applicable independent channels.

The profile model does not merge the channels.

### 12.3 Profile lifecycle

Profile lifecycle states include:

- proposed;
- active;
- deprecated;
- superseded;
- retired;
- archived.

An identity can be retired but not reused.

A replacement preserves predecessor and supersession relationships.

### 12.4 Composition lifecycle

A profile composition moves through:

```text
candidate
-> structurally valid
-> compatible
-> resource valid
-> artifact compatible
-> policy authorized
-> tested
-> evidenced
-> active
-> superseded or retired
```

A package installation or configuration file alone does not establish an active composition.

### 12.5 Artifact compatibility

Artifacts declare compatible profiles, overlays, runtime contracts, architectures, release channels, and authority floors.

A valid signature does not prove profile compatibility.

A profile-valid artifact remains inactive until the owning lifecycle completes.

## 13. Migration Plan

### 13.1 Preconditions

- `DEC-PROFILE-001` is accepted.
- `contracts/system.contract.json` exists as global owner.
- `generated/profile-catalog.json` exists as profile-identity and compatibility owner.
- primary-profile and overlay schemas validate.
- component membership is removed from component-registry ownership.
- profile and implementation locks are active.

### 13.2 Migration steps

1. Inventory every deprecated global, profile, topology, desktop, container, orchestration, hardware, and resource statement.
2. classify each fact as constitutional, system baseline, primary profile, overlay, component contract, artifact contract, toolchain contract, operations procedure, or recipe.
3. create the seven primary profile contracts.
4. create the three overlay contracts.
5. move profile membership and deployable envelopes into profile contracts.
6. keep component identity and internals in component contracts.
7. replace globalized endpoint and appliance requirements with profile-scoped requirements.
8. replace technology-named profile concepts with profile properties or recipes.
9. create requirement, lock, test, evidence, and traceability relationships.
10. regenerate profile, component, release, conformance, and AI-context projections.
11. validate every profile independently and every supported overlay composition.
12. activate the complete authority release last.

### 13.3 deprecated disposition

- `doc/01-architecture/03-node-profiles.md` — split into the profile model, primary-profile documents, and overlay documents.
- `doc/01-architecture/02-physical-architecture.md` — split into global physical principles, profile topology, and implementation recipes.
- `doc/00-foundation/00-charter.md` — retained for constitutional and system-baseline principles; appliance-specific realization is profile scoped.
- `doc/08-adrs/ADR-003-no-gnome-product-shell.md` — adapted into `ADR-003` and scoped to `appliance_shell`.
- `doc/08-adrs/ADR-005-rootless-podman-and-quadlet.md` — retained as source lineage for profile and recipe decisions rather than a deployment-profile identity.
- `doc/08-adrs/ADR-011-no-kubernetes-on-endpoints.md` — retained as the endpoint profile constraint while build and control profiles can declare orchestration.
- unvalidated container or desktop “profiles” — reclassified as properties, overlays, contracts, or recipes.

### 13.4 Redirects and compatibility period

Migration mapping records deprecated paths and stable concepts.

The active corpus exposes one profile model under `docs/03-profiles/`.

removed source files remain archive-only and cannot act as parallel authority after cutover.

## 14. Rollback and Forward Repair

### 14.1 Rollback trigger

Rollback is required when a candidate profile-model change causes:

- duplicate or missing primary-profile identity;
- an overlay that can operate independently;
- incompatible overlays accepted together;
- undeclared inheritance;
- profile-specific requirements promoted globally;
- global invariants weakened by a profile;
- component membership owned by the component registry;
- technology choices promoted to profile identities;
- missing profile tests or evidence;
- incomplete migration or impact closure.

### 14.2 Rollback unit

The rollback unit is the complete compatible authority state containing:

- system registry;
- profile index;
- all active profile contracts;
- component registry;
- decisions;
- requirements;
- locks;
- traceability;
- tests;
- evidence;
- generated matrices;
- authority manifest.

A mixture of old and new profile semantics is not a valid rollback state.

### 14.3 Rollback procedure

1. Stop activation of new profile compositions.
2. preserve the failed candidate and diagnostics.
3. restore the previous complete authority release.
4. regenerate profile and conformance projections from that release.
5. verify active environments still resolve to one valid primary profile and compatible overlays.
6. record rollback evidence.

### 14.4 Forward repair

Forward repair is used when profile identities, environment records, artifacts, or migrations have already moved to the new model and direct rollback would create invalid identity or compatibility state.

The repair remains governed by a replacement accepted decision and a complete impact report.

### 14.5 Last known valid state

- Authority manifest: `generated/authority-manifest.json#/active_authority_release`
- Profile model: `generated/profile-catalog.json`
- System baseline: `contracts/system.contract.json`
- Composed environment state: exact environment profile records and active Release Sets under the previous complete authority release

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `generated/impact/IMPACT-2026-08-03-DEC-PROFILE-001.json`

### 15.2 Modified canonical references

- `generated/decision-index.json#/decisions/DEC-PROFILE-001`
- `contracts/system.contract.json`
- `generated/profile-catalog.json`
- `contracts/profiles/*.profile.json`
- `generated/requirements-index.json#/requirements/REQ-PROF-MODEL-001`
- `generated/requirements-index.json#/requirements/REQ-PROF-MODEL-026`
- `generated/assertion-index.json#/locks/LOCK-PROFILE-001`
- `generated/assertion-index.json#/locks/LOCK-PROFILE-002`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-SYS-001` | `updated` | Clarifies that the global system context is deployment-independent and does not own profile membership or topology. |
| `DOC-PROF-000` | `introduced_or_updated` | Projects primary-profile and overlay identities, compatibility, and composition semantics. |
| `DOC-PROF-001` | `introduced_or_updated` | Projects the `user_lightweight` primary profile. |
| `DOC-PROF-002` | `introduced_or_updated` | Projects the `developer_linux_workstation` primary profile. |
| `DOC-PROF-003` | `introduced_or_updated` | Projects the `developer_windows_wsl` primary profile. |
| `DOC-PROF-004` | `introduced_or_updated` | Projects the `sovereign_linux_node` primary profile. |
| `DOC-PROF-005` | `introduced_or_updated` | Projects the `sovereign_hub` primary profile. |
| `DOC-PROF-006` | `introduced_or_updated` | Projects the `build_farm` primary profile. |
| `DOC-PROF-007` | `introduced_or_updated` | Projects the `control_plane` primary profile. |
| `DOC-PROF-011` | `reviewed_no_change` | Remains an overlay and preserves primary-profile ownership. |
| `DOC-PROF-012` | `introduced_or_updated` | Projects the `sovereign_offline` overlay. |
| `DOC-PROF-013` | `introduced_or_updated` | Projects the `appliance_shell` overlay. |
| `DOC-ADR-003` | `reviewed_no_change` | Its appliance decision remains overlay scoped. |
| `DOC-SEC-000` | `reviewed_no_change` | Profile-specific controls remain scoped and global threats remain universal. |
| `DOC-OPS-018` | `reviewed_no_change` | Sovereign-node operations retain primary-profile ownership and compatible overlays. |
| `DOC-CONF-009` | `reviewed_no_change` | Profile locks enforce scope, compatibility, inheritance, and impact closure. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-PROFILE-001` | `unchanged` | Prevents profile-specific facts from being promoted to global baseline. |
| `LOCK-PROFILE-002` | `unchanged` | Requires explicit primary-profile and overlay composition. |
| `LOCK-IMPL-001` | `unchanged` | Prevents implementation details from replacing contracts. |
| `LOCK-IMPL-002` | `unchanged` | Keeps container, desktop, orchestration, and service-manager choices profile scoped. |
| `LOCK-DOC-003` | `unchanged` | Prevents Markdown from redefining registry-owned values. |
| `LOCK-DOC-011` | `unchanged` | Requires accepted decisions for implementation-affecting ambiguity. |
| `LOCK-DOC-015` | `unchanged` | Protects profile and global scope in generated and explanatory projections. |
| `LOCK-COMP-001` | `unchanged` | Preserves component boundary and ownership independently of deployment membership. |
| `LOCK-COMP-002` | `unchanged` | Preserves component identities while profiles select membership. |
| `LOCK-DATA-001` | `unchanged` | Keeps authoritative data ownership outside profile composition. |
| `LOCK-AI-001` | `unchanged` | Prevents optional external AI from becoming a native global baseline dependency. |
| `LOCK-SENT-001` | `unchanged` | Keeps SenTient optional and limited to compatible profiles. |
| `LOCK-LIFE-001` | `unchanged` | Preserves independent release channels across every profile. |
| `LOCK-DEV-003` | `unchanged` | Keeps development isolation requirements inside developer profiles and toolchain contracts. |

### 15.5 Affected requirements

| Requirement ID | Disposition | Validation effect |
| --- | --- | --- |
| `REQ-PROF-MODEL-001` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-002` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-003` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-004` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-005` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-006` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-007` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-008` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-009` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-010` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-011` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-012` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-013` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-014` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-015` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-016` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-017` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-018` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-019` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-020` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-021` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-022` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-023` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-024` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-025` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |
| `REQ-PROF-MODEL-026` | `introduced` | Projects one accepted baseline/profile-separation invariant into the requirements registry. |

### 15.6 Generated artifacts

Regeneration includes:

- documentation registry metadata;
- profile index;
- profile-composition matrix;
- component-membership matrix;
- effective-requirement matrices;
- hardware, resource, network, offline, backup, and recovery matrices;
- conformance matrix;
- decision and ADR indexes;
- traceability graph;
- impact report;
- release compatibility matrix;
- authority manifest;
- active AI context packages.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-PROF-001` | Profile identities are unique | `pass` |
| `TEST-PROF-002` | Profile inheritance is explicit | `pass` |
| `TEST-PROF-003` | Overlay composition is valid | `pass` |
| `TEST-PROF-004` | Profile exclusions are explicit | `pass` |
| `TEST-PROF-005` | Profile resource envelopes are complete | `pass` |
| `TEST-PROF-006` | Profile offline envelopes are tested | `pass` |
| `TEST-PROF-007` | Profile security boundaries are complete | `pass` |
| `TEST-PROF-008` | Profile component membership resolves | `pass` |
| `TEST-PROF-009` | Profile claims have evidence | `pass` |
| `TEST-PROF-010` | User lightweight profile excludes heavy workbenches | `pass` |
| `TEST-PROF-011` | Developer Python workspaces use UV isolation | `pass` |
| `TEST-PROF-012` | Developer workspaces isolate mutable state | `pass` |
| `TEST-PROF-013` | Sovereign Linux choices remain profile scoped | `pass` |
| `TEST-PROF-014` | Endpoint profiles do not require Kubernetes | `pass` |
| `TEST-PROF-015` | Build and control profiles declare orchestrator use explicitly | `pass` |
| `TEST-COMP-REG-001` | Component identifiers are unique | `pass` |
| `TEST-COMP-REG-004` | Authoritative data domains are unique | `pass` |
| `TEST-COMP-REG-007` | Decision references resolve | `pass` |
| `TEST-COMP-REG-008` | Lock references resolve | `pass` |
| `TEST-COMP-REG-009` | Profile membership is not owned by the component registry | `pass` |
| `TEST-COMP-REG-010` | Direct cross-component writes are prohibited | `pass` |
| `TEST-COMP-REG-011` | Boundary separations remain explicit | `pass` |
| `TEST-SYS-001` | Core operation remains available offline | `pass` |
| `TEST-SYS-002` | No native AI dependency exists | `pass` |
| `TEST-SYS-004` | Authority fails closed | `pass` |
| `TEST-SYS-005` | Safe degradation is capability scoped | `pass` |
| `TEST-SYS-012` | External integrations are removable | `pass` |
| `TEST-SYS-013` | Component stores remain isolated | `pass` |
| `TEST-SYS-015` | Optional heavy work is task activated | `pass` |
| `TEST-CROSS-004` | Resource and governance authorities remain separate | `pass` |
| `TEST-CROSS-005` | Language build and runtime remain separate | `pass` |
| `TEST-CROSS-006` | SenTient remains isolated and non-authoritative | `pass` |
| `TEST-CROSS-007` | Node Agent rejects arbitrary privileged execution | `pass` |
| `TEST-CROSS-008` | Policy decision precedes governed privilege | `pass` |
| `TEST-CROSS-009` | Audit Broker does not become an authorization engine | `pass` |
| `TEST-CROSS-011` | Ariane voice remains externally optional | `pass` |
| `TEST-CROSS-012` | kOA Mediatheque ingestion and UCKK learning-package validation remain deterministic and independent of AI | `pass` |
| `TEST-CROSS-013` | External AI cannot directly mutate authority | `pass` |
| `TEST-CROSS-014` | Identity layers remain distinct | `pass` |
| `TEST-CROSS-015` | All cross-component mutations are contract-bound | `pass` |
| `TEST-LIFE-001` | Release channels activate independently | `pass` |
| `TEST-LIFE-002` | Release Set compatibility is validated | `pass` |
| `TEST-LIFE-003` | Artifact verification precedes activation | `pass` |
| `TEST-LIFE-004` | Activation is atomic for the artifact class | `pass` |
| `TEST-LIFE-005` | Rollback restores a valid predecessor | `pass` |
| `TEST-LIFE-012` | Policy bundles activate independently | `pass` |
| `TEST-LIFE-013` | Language artifacts activate independently | `pass` |
| `TEST-LIFE-014` | Kristal runtime packs activate independently | `pass` |
| `TEST-DOC-DEC-001` | Proposed decisions cannot support active requirements | `pass` |
| `TEST-DOC-DEC-002` | Missing decisions block active profiles | `pass` |
| `TEST-DOC-DEC-003` | Conflicting accepted decisions are detected | `pass` |
| `TEST-DOC-DEC-005` | Ambiguous decision scope is rejected | `pass` |
| `TEST-DOC-DEC-007` | Validation precedes authority activation | `pass` |
| `TEST-DOC-DEC-010` | Missing decisions produce blocked machine output | `pass` |
| `TEST-DOC-VAL-003` | Canonical references resolve | `pass` |
| `TEST-DOC-VAL-004` | Stable identifiers are unique | `pass` |
| `TEST-DOC-VAL-005` | Canonical ownership is exclusive | `pass` |
| `TEST-DOC-VAL-006` | Decision references are accepted | `pass` |
| `TEST-DOC-VAL-007` | Alignment lock references are active | `pass` |
| `TEST-DOC-VAL-008` | Required document sections exist | `pass` |
| `TEST-DOC-VAL-009` | Active documentation is English | `pass` |
| `TEST-DOC-VAL-010` | Unresolved authority markers are absent | `pass` |
| `TEST-DOC-VAL-012` | Generated content is reproducible | `pass` |
| `TEST-DOC-VAL-013` | Documentation dependency graph is acyclic | `pass` |
| `TEST-DOC-VAL-014` | Document class and path agree | `pass` |
| `TEST-DOC-VAL-016` | Traceability is complete | `pass` |
| `TEST-DOC-VAL-017` | Authority activation occurs last | `pass` |
| `TEST-DOC-VAL-018` | Validation uses a clean repository state | `pass` |
| `TEST-DOC-VAL-019` | Registry and schema versions are compatible | `pass` |
| `TEST-DOC-VAL-020` | Validation performs no semantic auto-fix | `pass` |
| `TEST-MIG-009` | Authority registry activation occurs last | `pass` |
| `TEST-MIG-012` | Rollback restores a complete authority state | `pass` |
| `TEST-MIG-013` | Failed cutover evidence is retained | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-013-DECISION` | Accepted profile-model decision | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-DECISION` |
| `EVID-ADR-013-SYSTEM` | Global baseline ownership and exclusion validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-SYSTEM` |
| `EVID-ADR-013-PROFILES` | Primary-profile identity and contract validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-PROFILES` |
| `EVID-ADR-013-OVERLAYS` | Overlay compatibility and composition validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-OVERLAYS` |
| `EVID-ADR-013-COMPONENTS` | Component membership and ownership separation | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-COMPONENTS` |
| `EVID-ADR-013-IMPL` | Implementation-technology and recipe separation | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-IMPL` |
| `EVID-ADR-013-MIGRATION` | deprecated classification and cutover coverage | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-MIGRATION` |
| `EVID-ADR-013-CONFORMANCE` | Complete profile and overlay conformance results | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-CONFORMANCE` |
| `EVID-ADR-013-DOCS` | Documentation, lock, traceability, and authority validation | `generated/evidence-catalog.json#/evidence/EVID-ADR-013-DOCS` |

### 16.3 Required validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

- validate that the global baseline contains universal system facts and excludes deployable profile details;
- validate the exact seven primary profile IDs;
- validate the exact three overlay IDs;
- validate exactly one primary profile per deployment;
- validate that overlays cannot operate independently;
- validate pairwise and whole-composition compatibility;
- validate deterministic merge and conflict behavior;
- validate explicit inheritance, defaults, exclusions, conflicts, and precedence;
- validate profile ownership of component membership;
- validate component ownership of internals and authoritative data;
- validate that container, desktop, service-manager, package-manager, and orchestrator choices are not standalone profiles;
- validate profile-specific scope in prose, generated matrices, recipes, and AI contexts;
- validate endpoint non-Kubernetes rules and explicit build or control-plane orchestration;
- validate that SenTient and external AI remain scoped and optional;
- validate every supported composition with exact artifacts, tests, evidence, and authority.

### 16.5 Acceptance criteria

1. `DEC-PROFILE-001` is accepted.
2. `contracts/system.contract.json` is the exclusive global-baseline owner.
3. `generated/profile-catalog.json` declares exactly seven primary profiles and three overlays.
4. Every deployable environment selects exactly one primary profile.
5. Every overlay declares compatible primary profiles, conflicts, and precedence.
6. Unsupported or conflicting compositions fail closed.
7. Profile-specific values are absent from the global baseline unless separately accepted globally.
8. Global invariants remain present in every profile.
9. Component membership is profile owned and component internals remain component owned.
10. Implementation technologies are properties, contracts, or recipes rather than profile identities.
11. Every affected object has a final impact disposition.
12. Every required test and evidence record resolves to the exact candidate authority state.
13. The authority registry activates the validated complete state last.

## 17. Consequences

### 17.1 Positive consequences

- The global architecture remains coherent across diverse deployments.
- Profiles can differ without creating separate products.
- Endpoint, developer, hub, build, and control needs no longer distort each other.
- Global invariants have a clear owner.
- Component membership has a clear owner.
- Overlays become reusable and testable.
- Desktop, container, orchestrator, hardware, and topology choices remain replaceable.
- Profile conformance is exact and machine readable.
- undeclared appliance-centric statements can be migrated safely.
- AI agents receive a clear scope boundary for authoring and reasoning.

### 17.2 Negative consequences and costs

- The corpus requires ten profile and overlay contracts.
- Each supported composition needs tests and evidence.
- Cross-profile changes can have large impact graphs.
- Effective profile requirements need generated matrices.
- Operators need to identify exact environment composition.
- Documentation authors need disciplined global-versus-profile classification.
- Migration from non-authoritative sources requires many explicit dispositions.

### 17.3 Operational obligations

- Record the active primary profile and overlays on every environment.
- Monitor profile compatibility and evidence.
- Prevent package or configuration drift from changing profile identity implicitly.
- Revalidate profile composition after artifact, resource, network, hardware, or component changes.
- Preserve prior complete profile and authority states for rollback.
- Keep profile-specific procedures attached to their profiles.
- Test removal of optional overlays and integrations.

### 17.4 Documentation obligations

- State document scope explicitly.
- Use canonical registry references.
- Keep profile-specific requirements out of global prose.
- Keep global invariants in every profile projection.
- Generate membership and effective-requirement matrices.
- Register all dependencies.
- Recompute impact after profile-model changes.
- Exclude proposals, archives, stale profiles, and invalid compositions from active AI context.
- Preserve retired identifiers and migration lineage.

### 17.5 Technical debt explicitly accepted

The architecture accepts profile-matrix and composition-tooling complexity in exchange for correct scope and deployable diversity.

The debt cannot be reduced by merging profiles into one universal stack or by allowing implicit inheritance.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| One universal deployment stack | Cannot represent endpoint, developer, hub, build, and control environments without overconstraint or unsafe omission. | A future accepted architecture proves one stack satisfies every purpose, resource, trust, offline, and exit requirement. |
| Independent architecture per product variant | Creates duplicate owners and incompatible authority, component, artifact, and recovery models. | None while kOA remains one interoperable ecosystem. |
| Technology-named profiles | Confuses implementation with deployment purpose and makes technology replacement an identity migration. | A technology becomes a genuine authority and deployment identity through a new accepted decision. |
| Multiple primary profiles on one environment | Creates ambiguous ownership, conflicting defaults, and unclear conformance. | A future composition model defines a new higher-level deployable identity and supersedes this ADR. |
| Overlay-only deployment | Lacks a complete component, resource, topology, backup, and recovery base. | An overlay is promoted to a primary profile through a new identity and full profile contract. |
| Prose-only profile descriptions | Cannot guarantee compatibility, inheritance, membership, tests, or evidence. | None for active authority. |

Rejected alternatives are not implemented as undocumented exceptions.

## 19. Exceptions and Waivers

Not applicable.

A deployment that cannot satisfy its selected profile remains non-conformant or selects another valid primary profile.

A semantic exception that changes profile identity, global scope, composition, ownership, or deployment membership requires a new accepted decision rather than a waiver.

## 20. Implementation Guidance

This section is non-normative.

A profile resolver can:

1. load one primary profile;
2. load selected overlays;
3. verify versions and compatibility;
4. union obligations;
5. intersect permissions;
6. union prohibitions;
7. apply restrictive data and network rules;
8. merge component membership with explicit overlay changes;
9. validate resources and topology;
10. resolve required artifacts and Release Set;
11. compute effective tests and evidence;
12. emit a deterministic effective-profile document.

An effective-profile document can contain:

```text
environment_id
primary_profile
overlays
effective_requirements
effective_components
effective_resources
effective_networks
effective_storage
effective_offline_envelope
effective_artifacts
effective_tests
effective_evidence
active_exceptions
authority_release
```

The effective document remains generated from canonical contracts.

It does not replace them.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-PROFILE-001`
- Decision status: `accepted`
- Decision owner: `owner:profile-architecture`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-PROFILE-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `actor:documentation-generation` | `submitted` | `2026-08-03` |
| Canonical owner | `owner:profile-architecture` | `approved` | `2026-08-03` |
| System architecture reviewer | `owner:system-architecture` | `approved` | `2026-08-03` |
| Component architecture reviewer | `owner:component-architecture` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `authority:documentation-release` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0013",
  "decision_ids": [
    "DEC-PROFILE-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-PROFILE-001",
    "contracts/system.contract.json",
    "generated/profile-catalog.json",
    "contracts/profiles/*.profile.json",
    "generated/requirements-index.json#/requirements/REQ-PROF-MODEL-001",
    "generated/requirements-index.json#/requirements/REQ-PROF-MODEL-026",
    "generated/assertion-index.json#/locks/LOCK-PROFILE-001",
    "generated/assertion-index.json#/locks/LOCK-PROFILE-002"
  ],
  "primary_profiles": [
    "user_lightweight",
    "developer_linux_workstation",
    "developer_windows_wsl",
    "sovereign_linux_node",
    "sovereign_hub",
    "build_farm",
    "control_plane"
],
  "profile_overlays": [
    "high_assurance",
    "sovereign_offline",
    "appliance_shell"
],
  "affected_document_ids": [
    "DOC-SYS-001",
    "DOC-PROF-000",
    "DOC-PROF-001",
    "DOC-PROF-002",
    "DOC-PROF-003",
    "DOC-PROF-004",
    "DOC-PROF-005",
    "DOC-PROF-006",
    "DOC-PROF-007",
    "DOC-PROF-011",
    "DOC-PROF-012",
    "DOC-PROF-013",
    "DOC-ADR-003",
    "DOC-SEC-000",
    "DOC-OPS-018",
    "DOC-CONF-009",
    "DOC-ADR-013"
],
  "requirement_ids": [
    "REQ-PROF-MODEL-001",
    "REQ-PROF-MODEL-002",
    "REQ-PROF-MODEL-003",
    "REQ-PROF-MODEL-004",
    "REQ-PROF-MODEL-005",
    "REQ-PROF-MODEL-006",
    "REQ-PROF-MODEL-007",
    "REQ-PROF-MODEL-008",
    "REQ-PROF-MODEL-009",
    "REQ-PROF-MODEL-010",
    "REQ-PROF-MODEL-011",
    "REQ-PROF-MODEL-012",
    "REQ-PROF-MODEL-013",
    "REQ-PROF-MODEL-014",
    "REQ-PROF-MODEL-015",
    "REQ-PROF-MODEL-016",
    "REQ-PROF-MODEL-017",
    "REQ-PROF-MODEL-018",
    "REQ-PROF-MODEL-019",
    "REQ-PROF-MODEL-020",
    "REQ-PROF-MODEL-021",
    "REQ-PROF-MODEL-022",
    "REQ-PROF-MODEL-023",
    "REQ-PROF-MODEL-024",
    "REQ-PROF-MODEL-025",
    "REQ-PROF-MODEL-026"
],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-011",
    "LOCK-DOC-015",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-SENT-001",
    "LOCK-LIFE-001",
    "LOCK-DEV-003"
],
  "exception_ids": [],
  "adr_ids": [
    "ADR-003",
    "ADR-013"
  ],
  "test_ids": [
    "TEST-PROF-001",
    "TEST-PROF-002",
    "TEST-PROF-003",
    "TEST-PROF-004",
    "TEST-PROF-005",
    "TEST-PROF-006",
    "TEST-PROF-007",
    "TEST-PROF-008",
    "TEST-PROF-009",
    "TEST-PROF-010",
    "TEST-PROF-011",
    "TEST-PROF-012",
    "TEST-PROF-013",
    "TEST-PROF-014",
    "TEST-PROF-015",
    "TEST-COMP-REG-001",
    "TEST-COMP-REG-004",
    "TEST-COMP-REG-007",
    "TEST-COMP-REG-008",
    "TEST-COMP-REG-009",
    "TEST-COMP-REG-010",
    "TEST-COMP-REG-011",
    "TEST-SYS-001",
    "TEST-SYS-002",
    "TEST-SYS-004",
    "TEST-SYS-005",
    "TEST-SYS-012",
    "TEST-SYS-013",
    "TEST-SYS-015",
    "TEST-CROSS-004",
    "TEST-CROSS-005",
    "TEST-CROSS-006",
    "TEST-CROSS-007",
    "TEST-CROSS-008",
    "TEST-CROSS-009",
    "TEST-CROSS-011",
    "TEST-CROSS-012",
    "TEST-CROSS-013",
    "TEST-CROSS-014",
    "TEST-CROSS-015",
    "TEST-LIFE-001",
    "TEST-LIFE-002",
    "TEST-LIFE-003",
    "TEST-LIFE-004",
    "TEST-LIFE-005",
    "TEST-LIFE-012",
    "TEST-LIFE-013",
    "TEST-LIFE-014",
    "TEST-DOC-DEC-001",
    "TEST-DOC-DEC-002",
    "TEST-DOC-DEC-003",
    "TEST-DOC-DEC-005",
    "TEST-DOC-DEC-007",
    "TEST-DOC-DEC-010",
    "TEST-DOC-VAL-003",
    "TEST-DOC-VAL-004",
    "TEST-DOC-VAL-005",
    "TEST-DOC-VAL-006",
    "TEST-DOC-VAL-007",
    "TEST-DOC-VAL-008",
    "TEST-DOC-VAL-009",
    "TEST-DOC-VAL-010",
    "TEST-DOC-VAL-012",
    "TEST-DOC-VAL-013",
    "TEST-DOC-VAL-014",
    "TEST-DOC-VAL-016",
    "TEST-DOC-VAL-017",
    "TEST-DOC-VAL-018",
    "TEST-DOC-VAL-019",
    "TEST-DOC-VAL-020",
    "TEST-MIG-009",
    "TEST-MIG-012",
    "TEST-MIG-013"
],
  "evidence_ids": [
    "EVID-ADR-013-DECISION",
    "EVID-ADR-013-SYSTEM",
    "EVID-ADR-013-PROFILES",
    "EVID-ADR-013-OVERLAYS",
    "EVID-ADR-013-COMPONENTS",
    "EVID-ADR-013-IMPL",
    "EVID-ADR-013-MIGRATION",
    "EVID-ADR-013-CONFORMANCE",
    "EVID-ADR-013-DOCS"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-DEC-PROFILE-001.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement ADR references `ADR-013` through `supersedes`;
4. `DEC-PROFILE-001` is superseded or replaced through its declared decision lifecycle;
5. every primary-profile and overlay identity remains reserved;
6. environment records, profile contracts, artifacts, releases, tests, evidence, impact reports, migration lineage, and authority manifests preserve the historical model;
7. generated profile, component, conformance, and AI-context projections are regenerated;
8. active authority changes only after complete validation.

This ADR remains in the corpus after acceptance, deprecation, rejection, retirement, or supersession.
