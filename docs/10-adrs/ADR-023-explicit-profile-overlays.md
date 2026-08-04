<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-023",
  "document_class": "adr",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-017",
    "LOCK-DOC-021",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-004"
  ],
  "tags": [
    "architecture-decision",
    "adr",
    "023",
    "explicit",
    "profile",
    "overlays"
  ]
}
KOA:DOC-META:END -->

# ADR-023 — Explicit Profile Overlays

**ADR ID:** `ADR-023`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `profile_architecture_owner`  
**Owner decision:** `DEC-PROFILE-001`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** None.  
**Superseded by:** None.

## 1. Decision Summary

kOA adopts explicit profile overlays as the only supported mechanism for adding cross-cutting deployment constraints to a base profile.

Every effective deployment profile consists of:

- exactly one active base profile;
- zero or more explicitly selected overlays;
- explicitly selected optional components and integrations;
- one declared platform and implementation;
- one declared topology;
- one compatible active Release Set.

The active base profiles are:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`.

The composable overlays are:

- `high_assurance`;
- `sovereign_offline`;
- `appliance_shell`.

An overlay is not a standalone deployment profile, an informal label, a recipe, a container choice, a desktop preference, a Kubernetes mode, a release channel, or a hidden inheritance layer. It is a versioned profile contract that adds or strengthens explicitly declared constraints.

Overlay composition is contract-based and fail-closed. A deployment can activate a composition only when:

- the base profile declares the overlay compatible;
- the overlay declares the base profile compatible;
- every selected overlay pair declares compatibility;
- every dependency and ordering relation resolves without cycles;
- all added requirements, components, resources, tests, and lifecycle obligations resolve;
- no overlay weakens a global or base-profile rule;
- no two selected overlays produce an unresolved semantic conflict;
- the generated effective-profile projection validates;
- the exact composition passes its conformance matrix.

No overlay is inherited implicitly from hardware, hostname, installation method, container runtime, desktop environment, network state, operator preference, or another deployment.

## 2. Scope

### 2.1 Included scope

This decision applies globally to:

- profile identity;
- profile inheritance;
- overlay identity;
- overlay compatibility;
- overlay dependencies;
- overlay ordering;
- effective-profile generation;
- component selection;
- integration selection;
- hardware and resource constraints;
- security and governance additions;
- offline additions;
- user-interface and appliance-shell additions;
- profile test matrices;
- release compatibility;
- activation;
- removal;
- migration;
- rollback;
- support and diagnostics;
- AI-generated profile context.

### 2.2 Base-profile scope

A base profile defines the primary deployment purpose and operating envelope.

It owns, directly or by referenced contracts:

- primary deployment role;
- required and optional components;
- supported operating systems;
- topology;
- hardware and resource envelope;
- data ownership;
- network model;
- offline baseline;
- lifecycle behavior;
- conformance prerequisites;
- compatible overlays.

A base profile remains identifiable after overlays are applied.

### 2.3 Overlay scope

An overlay defines cross-cutting additions for compatible base profiles.

An overlay can:

- strengthen security;
- add evidence requirements;
- add offline requirements;
- add interface restrictions;
- add recovery requirements;
- add components when the base profile explicitly permits that addition;
- disable optional capabilities;
- narrow allowed implementations;
- add tests;
- add protected reserves;
- add lifecycle and removal obligations.

An overlay cannot silently replace the base profile’s purpose, owner, component data boundaries, or canonical identity.

### 2.4 Current overlays

| Overlay ID | Primary addition |
| --- | --- |
| `high_assurance` | Stronger identity, separation of duties, evidence, isolation, recovery, review, and fail-closed behavior. |
| `sovereign_offline` | Sustained local operation, support, update, exchange, verification, and recovery without Internet or upstream-control-plane dependencies. |
| `appliance_shell` | Constrained appliance interface, minimal Wayland shell, bounded administration, local navigation, and restricted general-purpose desktop behavior. |

The table summarizes purpose. The overlay contracts own exact facts.

### 2.5 Explicit exclusions

The following are not overlays:

- rootless Podman;
- Docker;
- Quadlet;
- systemd;
- Kubernetes;
- GNOME;
- KDE Plasma;
- WSL;
- Linux;
- Windows;
- a GPU;
- a database product;
- a backup product;
- a release channel;
- a component;
- SenTient;
- external AI;
- a customer tier;
- a tenant;
- a recipe;
- a build mode.

These can be profile properties, implementation selections, components, integrations, or recipes, but they do not become overlays by convention.

### 2.6 Excluded authority

This decision does not independently define:

- the exact fields of every profile contract;
- every compatibility pair;
- every hardware minimum;
- every overlay test;
- component business behavior;
- component data ownership;
- release membership;
- implementation recipes;
- user consent;
- cultural authority;
- publication authority.

Those facts remain owned by the relevant canonical contracts.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json`
- `DEC-PROFILE-001` — primary deployment profiles and composable overlays.

### 3.2 ADR registry

- `generated/decision-index.json`
- `ADR-023`

The ADR registry owns identity, status, owner-decision relationship, supersession, and authority participation for this ADR.

### 3.3 Canonical profile references

The decision constrains:

- `generated/profile-catalog.json`;
- `contracts/profiles/user-lightweight.profile.json`;
- `contracts/profiles/developer-linux-workstation.profile.json`;
- `contracts/profiles/developer-windows-wsl.profile.json`;
- `contracts/profiles/sovereign-linux-node.profile.json`;
- `contracts/profiles/sovereign-hub.profile.json`;
- `contracts/profiles/build-farm.profile.json`;
- `contracts/profiles/control-plane.profile.json`;
- `contracts/profiles/high-assurance.profile.json`;
- `contracts/profiles/sovereign-offline.profile.json`;
- `contracts/profiles/appliance-shell.profile.json`.

### 3.4 Related canonical references

Overlay composition also consumes:

- `contracts/system.contract.json`;
- `generated/component-catalog.json`;
- `contracts/integration-types.contract.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/traceability.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- `generated/exception-index.json`;
- `contracts/release-channels.contract.json`;
- component contracts;
- toolchain contracts;
- artifact contracts;
- profile schemas.

### 3.5 Related documents

- `03-profiles/00-profile-model.md`;
- `03-profiles/01-profile-composition.md`;
- `03-profiles/02-profile-schema.md`;
- `03-profiles/03-profile-inheritance.md`;
- `03-profiles/11-high-assurance.md`;
- `03-profiles/12-sovereign-offline.md`;
- `03-profiles/13-appliance-shell.md`;
- `09-conformance/04-profile-test-matrices.md`;
- `10-adrs/ADR-003-appliance-shell-without-gnome.md`;
- applicable profile implementation and recipe documents.

### 3.6 Related locks

This decision is protected by:

- profile-scope locks;
- implementation-scope locks;
- documentation ownership and dependency locks;
- decision-closure locks;
- lifecycle activation locks.

No overlay-specific lock can override the global lock catalog without an accepted owner decision.

## 4. Context and Problem

### 4.1 Repeated cross-cutting needs

Several deployment concerns cut across more than one base profile:

- high-assurance operation;
- extended offline sovereignty;
- constrained appliance user experience.

Duplicating each concern inside every compatible base profile would create:

- repeated requirements;
- diverging terminology;
- incompatible test lists;
- inconsistent lifecycle behavior;
- hidden assumptions;
- difficult change impact;
- accidental omissions.

### 4.2 Inheritance risk

Traditional profile inheritance often creates hidden behavior:

- a child profile receives fields indirectly;
- parent changes affect children unexpectedly;
- multiple inheritance creates ambiguous precedence;
- implementation details become semantic authority;
- a deployment name implies constraints that are not visible;
- removal of one inherited layer is difficult to reason about.

kOA requires every active constraint to remain visible and attributable.

### 4.3 Informal-label risk

Terms such as “secure,” “offline,” “appliance,” “containerized,” or “production” can be used informally without a precise contract.

An informal label can cause operators or AI agents to infer:

- additional components;
- disabled capabilities;
- network restrictions;
- desktop rules;
- hardware requirements;
- trust assumptions;
- update behavior;
- evidence requirements.

These inferences can alter implementation without canonical authority.

### 4.4 Precedence risk

A raw configuration-merge model can permit later files to override earlier rules. This creates an unsafe assumption that ordering is authority.

For example:

- an overlay could re-enable a capability prohibited by the base;
- an appliance overlay could remove a recovery interface;
- an offline overlay could retain an undeclared online dependency;
- a high-assurance overlay could be weakened by a later implementation file;
- two overlays could assign incompatible values without validation.

The architecture requires semantic composition rather than last-write-wins merging.

### 4.5 Removal risk

A deployment may need to remove an overlay after:

- a mission change;
- a support transition;
- hardware replacement;
- an offline period;
- a security posture change;
- appliance conversion or decommissioning.

If overlay state is not separately owned and reversible, removal can damage base-profile data or leave hidden services, credentials, routes, queues, or policies.

### 4.6 Decision requirement

A major architecture decision is required because overlay behavior affects:

- profile contracts;
- schemas;
- component activation;
- security;
- resources;
- offline guarantees;
- user interface;
- test selection;
- release compatibility;
- migration;
- removal;
- AI context.

## 5. Decision Drivers

Decision drivers, in priority order, are:

1. Explicit effective composition.
2. No implicit inheritance.
3. No semantic last-write-wins behavior.
4. Preservation of global and base-profile guarantees.
5. Deterministic compatibility.
6. Reversible activation and removal.
7. Complete conformance coverage.
8. Canonical ownership of every added rule.
9. Profile-specific implementation independence.
10. Offline visibility of the composition.
11. Clear AI authoring boundaries.
12. Stable profile identity.
13. Predictable change impact.
14. Support for multiple compatible overlays.

## 6. Considered Options

### 6.1 Option A — Explicit contract-based overlays

**Description**

Use exactly one base profile and zero or more named, versioned, explicitly selected overlays. Each contract declares compatibility, dependencies, conflicts, additions, prohibitions, resource effects, lifecycle behavior, and tests. Generate an effective-profile projection and reject unresolved conflicts.

**Advantages**

- Composition is visible.
- Scope is machine-resolvable.
- Overlay removal is tractable.
- Tests can be derived.
- Multiple overlays can be supported safely.
- No ordering shortcut overrides authority.
- Base profile identity remains stable.
- AI context can show exact composition.
- Repeated cross-cutting concerns remain centralized.

**Disadvantages and costs**

- Requires compatibility declarations.
- Requires composition validation.
- Requires additional test matrices.
- Requires migration from implicit variants.
- Conflicts can block activation.
- Overlay contracts require lifecycle maintenance.

**Constraint fit**

This option satisfies all decision drivers.

### 6.2 Option B — Duplicate full profile variants

**Description**

Create separate complete profiles for combinations such as secure hub, offline hub, appliance node, secure offline node, and appliance offline node.

**Advantages**

- Each profile appears self-contained.
- No overlay resolver is required.
- Deployment selection is simple initially.

**Disadvantages and costs**

- Combination count grows quickly.
- Common facts diverge.
- Fixes must be repeated.
- Identity and compatibility become unclear.
- AI context receives many near-duplicate profiles.
- Conformance matrices become difficult to maintain.
- Migration between variants is treated as a full profile replacement.

**Reason rejected**

The approach duplicates authority and scales poorly.

### 6.3 Option C — Informal labels and recipes

**Description**

Keep base profiles only. Apply “high assurance,” “offline,” or “appliance” through deployment recipes and operator conventions.

**Advantages**

- Low schema complexity.
- Easy local customization.
- No compatibility registry.

**Disadvantages and costs**

- Labels are not authoritative.
- Recipes can become hidden requirements.
- Conformance cannot resolve applicability.
- AI agents can infer incompatible defaults.
- Removal and rollback are unclear.
- Different deployments use the same label differently.

**Reason rejected**

The option cannot support reliable architecture, conformance, or automation.

### 6.4 Option D — Multiple inheritance with override precedence

**Description**

Allow profiles to inherit from several parents. Resolve field conflicts through parent order or last-write-wins merging.

**Advantages**

- Familiar configuration pattern.
- Compact representation.
- Flexible composition.

**Disadvantages and costs**

- Order becomes hidden authority.
- Parent changes have indirect effects.
- Prohibitions can be overridden.
- Semantic conflicts can appear valid structurally.
- Removal and impact analysis become difficult.
- Test applicability becomes order-dependent.

**Reason rejected**

The option conflicts with fail-closed authority and explicit decision closure.

### 6.5 Option E — Dynamic runtime capability negotiation

**Description**

Let a deployment infer its profile and overlay behavior from available hardware, network state, installed services, or runtime probes.

**Advantages**

- Adaptive deployment.
- Reduced initial configuration.
- Potential automatic optimization.

**Disadvantages and costs**

- Capability becomes authority.
- Hardware or connectivity changes alter semantics silently.
- Installed optional services can appear required.
- Conformance identity becomes unstable.
- Offline state can change profile meaning.
- Recovery and support cannot rely on a stable contract.

**Reason rejected**

Runtime observation can inform operation but cannot select architectural authority.

## 7. Decision

### 7.1 Selected option

`explicit_contract_based_profile_overlays`

### 7.2 Effective composition

An effective profile is identified by:

- base profile ID and version;
- selected overlay IDs and versions;
- selected optional component IDs and versions;
- selected integration IDs and versions;
- platform;
- implementation;
- topology;
- active Release Set;
- configuration identity;
- generated effective-profile projection identity.

The effective projection is derived. The base and overlay contracts remain canonical.

### 7.3 Exactly one base profile

Every deployment has exactly one base profile.

A deployment cannot:

- combine two base profiles;
- treat an overlay as a base profile;
- operate without a base profile;
- infer the base profile from installed packages;
- switch base profile silently.

Changing the base profile is a profile migration, not an overlay update.

### 7.4 Explicit overlay selection

Every selected overlay appears in the deployment composition and activation evidence.

No overlay is selected implicitly by:

- a profile name suffix;
- a machine role;
- an environment variable without a contract;
- a container label;
- a desktop session;
- network disconnection;
- hardware capability;
- a recipe;
- an AI-generated plan;
- previous deployment history.

### 7.5 Compatibility

Compatibility is bidirectional and complete.

A composition requires:

- base-to-overlay compatibility;
- overlay-to-base compatibility;
- pairwise overlay compatibility;
- component compatibility;
- integration compatibility;
- platform compatibility;
- topology compatibility;
- Release Set compatibility.

An omitted compatibility relationship is treated as unavailable, not assumed compatible.

### 7.6 Composition semantics

Composition operates on typed semantic categories rather than arbitrary document merge order.

Categories include:

- requirements;
- prohibitions;
- required components;
- permitted optional components;
- disabled components;
- integrations;
- implementation constraints;
- hardware constraints;
- resource reserves;
- network zones;
- offline guarantees;
- user-interface constraints;
- lifecycle obligations;
- tests;
- evidence;
- support and recovery behavior.

Each category has an explicit composition rule.

### 7.7 Additive and strengthening behavior

An overlay can add or strengthen:

- requirements;
- prohibitions;
- validation;
- evidence;
- isolation;
- resource reserves;
- offline duration;
- recovery paths;
- review requirements;
- interface constraints;
- negative tests.

An overlay does not weaken a global or base-profile requirement.

When a permitted value set is narrowed by an overlay, the effective value is the intersection. An empty intersection blocks composition.

### 7.8 Conflicts

A semantic conflict occurs when selected contracts require incompatible outcomes.

Examples include:

- one contract requires a component that another prohibits;
- one requires an online dependency that `sovereign_offline` prohibits;
- one requires a general-purpose desktop that `appliance_shell` prohibits;
- resource minima exceed the active hardware envelope;
- required network routes violate a stronger security rule;
- two overlays define incompatible lifecycle behavior.

Conflicts are resolved only by:

- changing the selected composition;
- changing a canonical contract through an accepted decision;
- adding an explicitly authorized compatibility rule;
- using a valid bounded exception where the affected authority is waivable.

Ordering does not resolve semantic conflict.

### 7.9 Overlay dependency order

An overlay can declare `requires_overlay` or `applies_after` relationships when operational sequencing is necessary.

The relationships form an acyclic graph. The order controls generation and activation sequence only. It does not grant later overlays general override authority.

### 7.10 Effective-profile projection

The generated effective profile contains:

- all source contract references;
- resolved compatibility;
- resolved requirements and prohibitions;
- resolved components and integrations;
- resolved resources;
- resolved implementation constraints;
- resolved lifecycle;
- resolved tests;
- source attribution for every resolved value;
- conflicts and blocked reasons;
- generator identity and version.

The projection is read-only and cannot be edited as a source.

### 7.11 Activation

Activation requires:

- all contracts active;
- accepted owner decisions;
- exact compatible versions;
- complete effective projection;
- no unresolved conflict;
- complete impact analysis;
- applicable conformance tests passed;
- evidence current;
- Release Set compatible;
- migration and rollback ready.

### 7.12 Removal

Overlay removal is explicit.

Removal:

- stops new overlay-specific operations;
- preserves base-profile authoritative data;
- exports or migrates overlay-owned state where applicable;
- revokes overlay-specific credentials and routes;
- removes overlay-only services;
- drains or cancels overlay queues;
- removes temporary resource reservations;
- regenerates the effective profile;
- runs base-profile and removal tests;
- activates only after the remaining composition validates.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Profiles index ownership

`generated/profile-catalog.json` owns:

- discoverability;
- profile and overlay IDs;
- canonical contract paths;
- class as base profile or overlay;
- active status;
- version;
- high-level compatibility references.

It does not duplicate complete profile behavior.

### 8.2 Base-profile contract ownership

A base-profile contract owns:

- deployment purpose;
- primary component selection;
- supported platforms;
- topology;
- hardware envelope;
- resource envelope;
- baseline offline behavior;
- baseline security;
- lifecycle;
- compatible overlays;
- conformance prerequisites.

### 8.3 Overlay contract ownership

An overlay contract owns:

- overlay purpose;
- compatible base profiles;
- compatible and incompatible overlays;
- dependencies;
- added requirements;
- added prohibitions;
- component additions or exclusions;
- integration restrictions;
- resource additions;
- offline additions;
- interface additions;
- lifecycle additions;
- removal behavior;
- test additions;
- evidence additions.

### 8.4 Component ownership

Applying an overlay does not alter component data ownership.

An overlay can require a component, restrict a component, or disable an optional component. It cannot authorize one component to write another component’s authoritative data.

### 8.5 Implementation ownership

Implementation mechanisms remain owned by:

- profile properties;
- component contracts;
- toolchain contracts;
- implementation contracts;
- recipes.

An overlay can narrow permitted implementation choices but cannot make a recipe canonical.

### 8.6 Generated effective-profile ownership

The effective profile is generated from canonical sources.

It owns no independent fact and cannot:

- introduce a component;
- change compatibility;
- relax a requirement;
- create an exception;
- change a decision;
- select an implementation not permitted by sources.

### 8.7 Forbidden direct paths

The architecture prohibits:

- overlay facts stored only in deployment prose;
- a recipe selecting an undeclared overlay;
- an overlay writing another overlay’s contract;
- direct edits to generated effective profiles;
- hidden environment-based overlays;
- profile inference from installed packages;
- implicit overlay activation after reconnection;
- component data migration without the owning component;
- overlay-specific credentials shared across unrelated compositions.

## 9. Profile and Deployment Effects

### 9.1 Base-profile matrix

| Base profile | Overlay behavior |
| --- | --- |
| `user_lightweight` | Accepts only overlays declared compatible with bounded resources, local-first behavior, and no native AI dependency. |
| `developer_linux_workstation` | Retains workspace, UV, port, data, secret, service, and resource isolation under every compatible overlay. |
| `developer_windows_wsl` | Retains Windows/WSL boundary semantics and requires platform-specific overlay evidence. |
| `sovereign_linux_node` | Supports sovereign security, offline, shell, lifecycle, backup, and recovery compositions where declared compatible. |
| `sovereign_hub` | Supports multi-tenant, zone, governance, publication, federation, capacity, backup, and recovery additions where compatible. |
| `build_farm` | Accepts overlays only when worker isolation, reproducibility, candidate-artifact status, and cleanup remain intact. |
| `control_plane` | Accepts overlays without making the control plane a dependency for minimum local correctness. |

### 9.2 High-assurance overlay

`high_assurance` can add:

- stronger identity assurance;
- shorter session and credential duration;
- separation of duties;
- human review;
- stronger evidence;
- stricter network and administrative boundaries;
- protected recovery reserves;
- enhanced negative tests;
- constrained exceptions;
- stronger support-session controls.

It does not create a new base profile or authorize broad administrative access.

### 9.3 Sovereign-offline overlay

`sovereign_offline` can add:

- sustained Internet absence;
- public-DNS absence;
- upstream-control-plane absence;
- local identity and governance;
- offline update;
- removable-media exchange;
- offline support;
- local verification;
- queued-operation controls;
- reconnection revalidation;
- local backup, restore, and exit.

Temporary network disconnection does not activate this overlay. The overlay is selected and validated before its guarantees are claimed.

### 9.4 Appliance-shell overlay

`appliance_shell` can add:

- minimal Wayland compositor;
- embedded web interface where appropriate;
- restricted general-purpose desktop behavior;
- local Ariane navigation where selected;
- bounded administration;
- explicit recovery entry;
- appliance startup and shutdown;
- limited user-exposed services;
- accessibility requirements;
- shell-removal and recovery tests.

The absence of GNOME is an appliance-overlay requirement, not a global Linux requirement.

### 9.5 Multi-overlay example

A deployment can compose:

```text
sovereign_linux_node
+ high_assurance
+ sovereign_offline
```

only when:

- both overlays are compatible with the base;
- the overlays are compatible with each other;
- combined resource and recovery requirements fit;
- offline identity and strong-assurance mechanisms remain locally usable;
- the effective matrix passes.

### 9.6 Appliance and offline composition

An appliance deployment can compose `appliance_shell` with `sovereign_offline` only when:

- local navigation and recovery remain available;
- no hidden online shell dependency exists;
- offline update and support are compatible with the constrained interface;
- removable-media or local administrative paths remain bounded;
- accessibility and emergency recovery are preserved.

### 9.7 Development compositions

A developer profile can use a compatible overlay without changing:

- workspace identity;
- per-workspace `.venv`;
- isolated services;
- isolated ports;
- isolated mutable data;
- isolated secrets;
- resource budgets;
- platform-specific behavior.

An overlay can add stricter controls but cannot collapse workspace isolation.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

Explicit overlays improve security by making stronger controls visible and testable.

Security-relevant overlay effects include:

- identity strength;
- session rules;
- administrator separation;
- network restrictions;
- service exposure;
- evidence;
- recovery;
- exception constraints;
- negative tests;
- credential lifecycle.

No “secure mode” label substitutes for an active overlay contract.

### 10.2 Privacy and rights effects

An overlay can strengthen privacy, consent, cultural-rights, selective-audit, or disclosure controls.

It cannot:

- remove consent requirements;
- broaden publication authority;
- make protected data public;
- weaken cultural restrictions;
- change data ownership;
- permit cross-tenant access;
- hide evidence.

### 10.3 Appliance effects

A constrained shell cannot remove:

- user-visible status;
- consent controls;
- recourse;
- accessibility;
- backup and export;
- recovery access;
- support disclosure review.

A reduced interface remains an interface constraint, not a reduction in user rights.

### 10.4 AI effects

AI can:

- resolve the selected composition;
- compare compatibility;
- generate an effective-profile proposal;
- identify conflicts;
- generate test matrices;
- prepare impact reports;
- explain source attribution.

AI cannot:

- activate an overlay;
- infer an overlay from a label;
- approve compatibility;
- invent a merge precedence;
- weaken a conflict;
- approve an exception;
- choose a base profile silently;
- convert an implementation preference into an overlay.

Generated AI context names the exact base profile and overlays and remains non-authoritative.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline resolution

Profile and overlay contracts remain locally available.

The deployment can determine:

- active base profile;
- active overlays;
- effective constraints;
- compatibility;
- tests;
- blocked state;
- removal procedure;

without Internet access or a remote control plane.

### 11.2 Resource aggregation

The effective resource envelope accounts for:

- base-profile minimums;
- overlay reserves;
- selected components;
- selected integrations;
- maintenance;
- backup;
- restore;
- rollback;
- update;
- migration;
- evidence;
- support;
- failure allowance.

Resource values are combined according to their typed semantics. They are not all added mechanically.

### 11.3 Heavy services

An overlay does not make SenTient, local model runtimes, search engines, media processors, or other heavy services mandatory unless the base and overlay contracts explicitly require them.

Optional heavy services remain task-activated and capacity-controlled.

### 11.4 Operational identity

Observability exposes:

- base profile;
- overlay set;
- source contract versions;
- effective projection version;
- compatibility state;
- active Release Set;
- components;
- disabled capabilities;
- resource envelope;
- test state;
- exception state.

The overlay set is never hidden behind a generic “mode” value.

### 11.5 Support and diagnostics

Support cases identify the exact composition.

Diagnostic conclusions remain scoped to:

- base profile;
- overlays;
- platform;
- implementation;
- components;
- Release Set;
- configuration.

Evidence for one composition does not automatically prove another.

### 11.6 Capacity effects

Overlay activation can be blocked when:

- additional memory reserve is unavailable;
- storage recovery reserve is insufficient;
- offline update staging is absent;
- stronger evidence retention exceeds capacity;
- appliance recovery resources are missing;
- required human review capacity is unavailable;
- network isolation cannot be implemented.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`breaking`

This decision rejects implicit profile variants, unregistered modes, and raw merge precedence.

### 12.2 Compatibility graph

The profile compatibility graph contains:

- base-profile nodes;
- overlay nodes;
- base-to-overlay edges;
- overlay-to-base edges;
- overlay-to-overlay edges;
- dependency edges;
- conflict edges;
- platform constraints;
- component constraints;
- integration constraints;
- Release Set constraints.

Required dependency edges are acyclic.

### 12.3 Compatibility resolution

A composition is compatible only when every required edge resolves positively and no conflict edge applies.

“Not listed” means incompatible or unresolved, not permitted.

### 12.4 Overlay lifecycle

An overlay contract can be:

- proposed;
- active;
- deprecated;
- superseded;
- retired.

A selected overlay must be active. A deprecated overlay can remain active for a bounded migration period only when its contract and authority release permit it.

### 12.5 Composition lifecycle

An effective composition can be:

```text
declared
resolving
blocked
validated
staged
active
degraded
removing
superseded
retired
```

The exact machine states remain owned by the applicable profile artifact contract.

### 12.6 Release compatibility

Overlay contracts can affect all four release channels:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

A signed Release Set binds compatible profile, overlay, component, integration, policy, and artifact versions.

Updating one affected channel makes impacted composition evidence stale until revalidated.

### 12.7 Exceptions

An exception or waiver can apply only to a concrete composition and exact target.

It cannot:

- create compatibility absent from canonical contracts;
- change a prohibited composition into a globally supported composition;
- authorize implicit overlays;
- turn failed overlay tests into passes;
- remove non-waivable base guarantees.

## 13. Migration Plan

### 13.1 Migration inventory

Migration inventories:

- full profile variants;
- profile name suffixes;
- deployment modes;
- security modes;
- offline modes;
- appliance modes;
- recipes that imply profile behavior;
- environment variables that alter profile semantics;
- implementation-specific profile forks;
- duplicated requirements;
- duplicated tests;
- deployment-specific exceptions;
- profile detection scripts.

### 13.2 Classification

Each deprecated variant is classified as:

- base-profile fact;
- overlay fact;
- component selection;
- integration selection;
- implementation selection;
- recipe;
- configuration;
- exception;
- unsupported behavior;
- historical record.

### 13.3 Migration steps

1. Assign one base profile.
2. Identify intended overlay concerns.
3. Create or select explicit overlay contracts.
4. move duplicated cross-cutting facts to the overlay owner;
5. Keep base-specific facts in the base contract.
6. Register compatibility.
7. Register conflicts and dependencies.
8. Register selected components and integrations.
9. Define migration and removal behavior.
10. Generate the effective profile.
11. Generate the test matrix.
12. Run compatibility, resource, lifecycle, security, offline, and removal tests.
13. Record evidence.
14. Activate the exact composition.
15. Retire the deprecated variant identifier without reuse.

### 13.4 deprecated names

deprecated names can remain as non-canonical aliases during migration only when they resolve to one exact composition.

An alias records:

- deprecated name;
- base profile;
- overlay set;
- versions;
- migration deadline;
- replacement;
- owner.

An alias cannot select different compositions in different deployments.

### 13.5 Data and state migration

Overlay migration preserves component ownership.

Overlay-specific state is categorized as:

- canonical component data;
- profile configuration;
- security policy;
- credentials;
- generated projection;
- cache;
- queue;
- evidence;
- temporary staging.

Each category follows its owner’s migration and removal contract.

## 14. Rollback and Forward Repair

### 14.1 Rollback triggers

Rollback or deactivation is required when:

- compatibility resolution changes unexpectedly;
- an overlay weakens a base requirement;
- two overlays conflict;
- the dependency graph cycles;
- the effective projection omits source attribution;
- required components fail;
- resource reserves fail;
- offline guarantees fail;
- appliance recovery is unavailable;
- test applicability is incomplete;
- overlay removal damages base state;
- Release Set compatibility fails.

### 14.2 Rollback unit

The rollback unit includes:

- base-profile contract version;
- overlay contract versions;
- component and integration selections;
- effective projection;
- configuration;
- active Release Set;
- migration state;
- test and evidence set.

A rollback does not activate a mixed composition.

### 14.3 Rollback procedure

1. Stop new overlay-specific work.
2. Preserve authoritative component data.
3. Select the last validated composition.
4. Restore compatible contracts and Release Set.
5. Revoke candidate overlay credentials and routes.
6. remove candidate-only services;
7. Restore resource allocations.
8. Regenerate the effective profile.
9. Run conformance and recovery checks.
10. Record rollback evidence.

### 14.4 Forward repair

Forward repair is preferred when:

- a compatibility edge is missing but the architecture is valid;
- generated source attribution is incomplete;
- a test mapping is missing;
- a resource declaration is incorrect;
- an overlay removal step is incomplete;
- an accepted identifier must be preserved.

Repair changes canonical contracts through accepted authority and regenerates the projection.

### 14.5 Base-profile preservation

Overlay failure does not change the base-profile identity.

Where safe, the system degrades by disabling the overlay-specific capability and preserving the last validated base-compatible operation. It does not claim base-only conformance until removal and regression tests pass.

## 15. Interfile Alignment Impact

### 15.1 Primary impact report

- `generated/impact/IMPACT-2026-08-03-DEC-PROFILE-001-OVERLAYS.json`

### 15.2 Canonical contracts affected

The decision affects:

- `generated/decision-index.json`;
- `generated/decision-index.json`;
- `generated/profile-catalog.json`;
- all seven base-profile contracts;
- all three overlay contracts;
- `generated/component-catalog.json`;
- `contracts/integration-types.contract.json`;
- `generated/requirements-index.json`;
- `generated/assertion-index.json`;
- `generated/traceability.json`;
- `generated/test-catalog.json`;
- `generated/evidence-catalog.json`;
- `contracts/release-channels.contract.json`.

### 15.3 Documents affected

| Document | Effect |
| --- | --- |
| `03-profiles/00-profile-model.md` | Defines base and overlay classes. |
| `03-profiles/01-profile-composition.md` | Defines composition semantics. |
| `03-profiles/02-profile-schema.md` | Defines profile and overlay fields. |
| `03-profiles/03-profile-inheritance.md` | Restricts inheritance and precedence. |
| `03-profiles/11-high-assurance.md` | Explains the high-assurance overlay. |
| `03-profiles/12-sovereign-offline.md` | Explains the sovereign-offline overlay. |
| `03-profiles/13-appliance-shell.md` | Explains the appliance-shell overlay. |
| `09-conformance/04-profile-test-matrices.md` | Adds overlay test families to base matrices. |
| `ADR-003` | Preserves appliance-shell desktop scope. |
| `ADR-023` | Records this decision. |

### 15.4 Generated artifacts

The decision causes generation or regeneration of:

- profiles index projections;
- compatibility matrices;
- effective-profile projections;
- profile test matrices;
- component and integration selection matrices;
- resource summaries;
- lifecycle manifests;
- overlay removal plans;
- Release Set compatibility reports;
- impact reports;
- AI context packages.

### 15.5 Lock effects

Profile locks confirm that:

- exactly one base profile is selected;
- overlays are explicit;
- profile-specific rules remain scoped;
- implementation choices do not become global;
- effective projections remain generated;
- decisions and dependencies resolve;
- activation occurs after validation.

## 16. Validation and Evidence

### 16.1 Required validation families

Validation covers:

- profile index;
- profile schemas;
- unique IDs;
- base-versus-overlay class;
- exactly one base profile;
- explicit overlay list;
- bidirectional compatibility;
- pairwise overlay compatibility;
- dependency acyclicity;
- conflict detection;
- source attribution;
- component selection;
- integration selection;
- resource aggregation;
- security additions;
- offline additions;
- appliance interface;
- lifecycle;
- removal;
- profile test matrices;
- Release Set compatibility;
- AI context.

### 16.2 Required negative tests

Negative tests verify rejection of:

- zero base profiles;
- two base profiles;
- overlay used as base;
- implicit overlay;
- undeclared overlay;
- one-sided compatibility;
- incompatible overlay pair;
- cyclic dependencies;
- last-write-wins conflict resolution;
- overlay weakening a base requirement;
- appliance-shell rule applied globally;
- network disconnection activating `sovereign_offline`;
- installed security tooling activating `high_assurance`;
- container runtime treated as a profile;
- Kubernetes treated as an endpoint overlay;
- generated effective profile edited manually;
- unselected optional component left active;
- automatic overlay transfer to a new Release Set.

### 16.3 Activation evidence

Activation evidence includes:

- accepted `DEC-PROFILE-001`;
- accepted `ADR-023`;
- profile and overlay schema validation;
- compatibility report;
- dependency-graph report;
- conflict report;
- effective-profile projection;
- source-attribution report;
- component-boundary report;
- resource and capacity report;
- applicable profile test matrix;
- offline report where applicable;
- security report where applicable;
- appliance report where applicable;
- removal rehearsal;
- Release Set compatibility;
- impact report.

### 16.4 Decision-specific checks

Decision-specific checks confirm:

1. One and only one base profile exists.
2. Every overlay is explicit.
3. Every overlay is active and versioned.
4. Compatibility is bidirectional.
5. Every selected overlay pair is compatible.
6. Dependencies are acyclic.
7. Conflicts remain blocking.
8. No overlay weakens global or base authority.
9. Every resolved fact includes source attribution.
10. Generated projections are read-only.
11. Test matrices contain base, overlay, component, integration, platform, and negative tests.
12. Removal returns a validated remaining composition.
13. AI context names the exact composition and cannot select it.
14. The active Release Set contains compatible versions.

### 16.5 Acceptance criteria

This ADR is accepted and active when:

1. `DEC-PROFILE-001` is accepted.
2. `ADR-023` is registered.
3. The seven base profiles and three overlays are registered.
4. Profile classes are unambiguous.
5. Compatibility and dependency contracts validate.
6. Effective-profile generation is deterministic.
7. Conflict detection fails closed.
8. Profile test matrices include overlay additions.
9. Resource and lifecycle aggregation validates.
10. Removal tests pass.
11. AI context tests pass.
12. Complete documentation validation passes.
13. The compatible authority release activates last.

## 17. Consequences

### 17.1 Positive consequences

- Cross-cutting deployment concerns have one owner.
- Base profiles remain stable.
- Composition is visible.
- Multiple overlays can be tested together.
- Implementation preferences remain scoped.
- Appliance behavior does not become a global desktop rule.
- Offline state does not become implicit profile authority.
- Stronger security remains explicit.
- Removal and rollback become testable.
- AI context can represent exact composition.
- Change impact is computable.

### 17.2 Negative consequences and costs

- Compatibility matrices require maintenance.
- Overlay pairs need tests.
- Effective-profile generation adds tooling.
- Some combinations remain intentionally unavailable.
- Deployment declarations become more detailed.
- Removal requires explicit lifecycle work.
- Resource aggregation can block otherwise functional combinations.
- deprecated full-profile variants require migration.
- A contract change can invalidate several compositions.

### 17.3 Operational obligations

Operators maintain:

- exact composition identity;
- compatible versions;
- generated effective profile;
- composition evidence;
- resource capacity;
- overlay-specific credentials;
- overlay-specific routes;
- removal readiness;
- rollback target;
- profile-specific support data.

### 17.4 Documentation obligations

Documentation owners maintain:

- profiles index;
- profile and overlay contracts;
- compatibility edges;
- conflict rules;
- dependencies;
- requirements;
- locks;
- traceability;
- test matrices;
- evidence;
- explanatory profile documents;
- migration lineage;
- generated contexts.

### 17.5 Technical debt explicitly accepted

The architecture accepts:

- explicit compatibility declarations;
- a generator for effective profiles;
- duplicate execution of some base regression tests under each overlay composition;
- bounded profile alias support during migration.

These costs are preferred to implicit inheritance and duplicated full profiles.

## 18. Rejected Alternatives

| Alternative | Rejection reason | Reconsideration trigger |
| --- | --- | --- |
| Full profile per combination | Creates combinatorial duplication and drift. | None while several overlays remain composable. |
| Informal deployment modes | Cannot support canonical conformance. | None. |
| Recipe-owned overlays | Makes implementation guidance authoritative. | None. |
| Multiple inheritance | Creates hidden precedence and indirect effects. | None. |
| Last-write-wins merge | Allows silent weakening and order-based authority. | None. |
| Runtime profile inference | Makes hardware and connectivity select authority. | None. |
| Containers as a profile | Confuses implementation with deployment purpose. | None. |
| Kubernetes as a universal overlay | Introduces an undeclared endpoint dependency. | None. |
| Desktop environment as profile identity | Makes a shell choice own system behavior. | None. |
| AI-selected composition | Creates architecture without human and canonical authority. | None. |

## 19. Exceptions and Waivers

No active exception or waiver applies to this ADR.

A future deviation:

- uses `schemas/exception.schema.json`;
- identifies one exact base profile and overlay composition;
- identifies exact deployment, release, or claim targets;
- preserves one-base-profile identity;
- preserves explicit overlay selection;
- preserves component data ownership;
- preserves truthful test outcomes;
- remains human-approved and expiring;
- cannot create global compatibility absent from canonical contracts;
- cannot authorize a hidden overlay;
- cannot make a recipe or generated projection canonical;
- cannot turn a conflict into a pass;
- cannot extend automatically to another Release Set or target.

A material change to the overlay architecture requires a new accepted decision and superseding ADR.

## 20. Implementation Guidance

Implementation guidance is non-authoritative unless adopted by an active contract.

Recommended practices include:

1. Represent overlay selection as an ordered display list plus a semantic dependency graph.
2. Use stable overlay IDs and semantic versions.
3. Store compatibility in machine-readable contracts.
4. Require reciprocal compatibility declarations.
5. Use typed composition rules per field category.
6. Preserve source attribution for every effective value.
7. Reject empty permitted-value intersections.
8. Keep generated effective profiles immutable.
9. Show base and overlay identities in system status.
10. Store overlay-specific credentials separately.
11. Keep overlay-specific state removable.
12. Test base regression after overlay removal.
13. Include negative tests for absent optional components.
14. Keep resource reservations visible.
15. Use explicit aliases only during migration.
16. Generate AI contexts from the effective projection and canonical sources.
17. Never infer `sovereign_offline` from current connectivity.
18. Never infer `high_assurance` from installed tools.
19. Never infer `appliance_shell` from the absence of GNOME.
20. Keep recipes subordinate to the selected composition.

## 21. Decision Record

### 21.1 Decision authority

- Decision ID: `DEC-PROFILE-001`
- Decision status: `accepted`
- Decision owner: `profile_architecture_owner`
- Decision registry: `generated/decision-index.json`
- ADR registry: `generated/decision-index.json`
- ADR ID: `ADR-023`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `profile_architecture_owner` | `submitted` | `2026-08-03` |
| Canonical owner | `profile_architecture_owner` | `approved` | `2026-08-03` |
| Security reviewer | `security_architecture_review` | `approved` | `2026-08-03` |
| Operations reviewer | `operations_architecture_review` | `approved` | `2026-08-03` |
| Conformance reviewer | `conformance_architecture_review` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `documentation_authority_activator` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0023",
  "decision_ids": [
    "DEC-PROFILE-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json",
    "generated/decision-index.json",
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
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "affected_document_ids": [
    "ADR-003",
    "ADR-023",
    "DOC-PROFILE-000",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003",
    "DOC-PROFILE-011",
    "DOC-PROFILE-012",
    "DOC-PROFILE-013",
    "DOC-CONF-004"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002",
    "LOCK-DOC-003",
    "LOCK-DOC-004",
    "LOCK-DOC-006",
    "LOCK-DOC-007",
    "LOCK-DOC-010",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-017",
    "LOCK-DOC-021",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "adr_ids": [
    "ADR-023"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-DEC-PROFILE-001-OVERLAYS.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. `generated/decision-index.json` marks `ADR-023` as superseded.
2. The replacement ADR references `ADR-023` through `supersedes`.
3. `ADR-023` references the replacement through `superseded_by`.
4. The identifier and path remain reserved.
5. Historical authority releases preserve the active period.
6. Effective-profile projections retain source contract and generator references.
7. Prior conformance evidence remains valid only for its original composition and validity period.
8. New composition semantics do not rewrite historical deployment identity.
9. deprecated aliases retain migration lineage.
10. Generated profile, compatibility, test, impact, and AI-context indexes are regenerated.
11. Retired overlays remain historical records and cannot be reactivated through aliasing.
12. Active deployments migrate through an explicit compatible profile change.
13. Historical evidence of conflicts, removals, and rollbacks remains available.
14. No unrelated profile or overlay reuses the retired identifiers.

Accepted, rejected, deprecated, superseded, and archived ADRs remain historical records and are not deleted.
