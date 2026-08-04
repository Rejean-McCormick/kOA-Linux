<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-002",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
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
    "schemas/deployment-profile.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-PROFILE-002",
    "DEC-PROFILE-INHERIT-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AI-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-INHERIT-001",
    "REQ-PROFILE-INHERIT-002",
    "REQ-PROFILE-INHERIT-003",
    "REQ-PROFILE-INHERIT-004",
    "REQ-PROFILE-INHERIT-005",
    "REQ-PROFILE-INHERIT-006",
    "REQ-PROFILE-INHERIT-007",
    "REQ-PROFILE-INHERIT-008",
    "REQ-PROFILE-INHERIT-009",
    "REQ-PROFILE-INHERIT-010",
    "REQ-PROFILE-INHERIT-011",
    "REQ-PROFILE-INHERIT-012",
    "REQ-PROFILE-INHERIT-013",
    "REQ-PROFILE-INHERIT-014",
    "REQ-PROFILE-INHERIT-015",
    "REQ-PROFILE-INHERIT-016",
    "REQ-PROFILE-INHERIT-017",
    "REQ-PROFILE-INHERIT-018",
    "REQ-PROFILE-INHERIT-019",
    "REQ-PROFILE-INHERIT-020",
    "REQ-PROFILE-INHERIT-021",
    "REQ-PROFILE-INHERIT-022",
    "REQ-PROFILE-INHERIT-023",
    "REQ-PROFILE-INHERIT-024",
    "REQ-PROFILE-INHERIT-025",
    "REQ-PROFILE-INHERIT-026",
    "REQ-PROFILE-INHERIT-027",
    "REQ-PROFILE-INHERIT-028",
    "REQ-PROFILE-INHERIT-029",
    "REQ-PROFILE-INHERIT-030"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
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
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001"
  ],
  "tags": [
    "profiles",
    "profile-inheritance",
    "profile-composition",
    "primary-profiles",
    "profile-overlays",
    "scope-containment",
    "capability-closure",
    "compatibility",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Profile Inheritance

## 1. Purpose

This document defines how deployment profiles relate to the global kOA baseline and how profile overlays compose with primary profiles.

The profile system avoids implicit inheritance. Similar files, common components, shared host technologies, or historical ancestry do not transfer requirements from one profile to another. Shared behavior comes from canonical global registries and reusable contracts. Conditional behavior comes from one primary profile and explicitly compatible overlays.

The model exists to prevent:

- profile-specific rules from becoming global by repetition;
- one primary profile from silently inheriting another profile's assumptions;
- overlays from becoming independently deployable products;
- incompatible controls from being combined through guesswork;
- component ownership from changing through composition;
- conformance claims from including untested inherited behavior;
- implementation convenience from overriding system boundaries.

The canonical profile contracts and profile index own relationship facts. This document explains the inheritance and composition rules that those objects implement.

## 2. Scope

This document applies to:

- all primary deployment profiles;
- all profile overlays;
- the global baseline applied to every active profile;
- profile compatibility and incompatibility;
- profile and overlay composition;
- effective capability and component calculation;
- profile-specific resource, hardware, security, offline, lifecycle, integration, and implementation rules;
- profile exceptions and waivers;
- profile conformance claims;
- generated profile matrices and AI context packages;
- migration of undeclared appliance or deployment rules into explicit profile scope.

The current primary profiles are:

```text
user_lightweight
developer_linux_workstation
developer_windows_wsl
sovereign_linux_node
sovereign_hub
build_farm
control_plane
```

The current profile overlays are:

```text
high_assurance
sovereign_offline
appliance_shell
```

This document does not assign the compatibility of a specific overlay to a specific primary profile. Each canonical profile contract owns those facts.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Active profile inventory and profile kind | `generated/profile-catalog.json` |
| Primary-profile facts | `contracts/profiles/*.profile.json` |
| Overlay facts and compatibility | `contracts/profiles/*.profile.json` |
| Profile-contract structure | `schemas/deployment-profile.schema.json` |
| Profile-index structure | `schemas/profile-index.schema.json` |
| Global constitutional and system baseline | `contracts/system.contract.json` and active constitutional requirements |
| Component identities and ownership | `generated/component-catalog.json` |
| Global capability model | `contracts/system.contract.json#/capability_model` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Profile and composition invariants | `generated/assertion-index.json` |
| Profile, component, capability, test, and evidence links | `generated/traceability.json` |
| Profile conformance tests | `generated/test-catalog.json` |
| Profile conformance evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted profile decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

The profile index records discoverability and relationship references. It does not replace the complete contracts. Each profile contract remains the owner of its own behavior, compatibility, and claims.

## 4. Model and Responsibilities

### 4.1 Global baseline application

Every active profile operates inside the same constitutional and system authority.

The global baseline includes:

- explicit and fail-closed authority;
- safe degradation;
- component separation;
- data ownership;
- offline continuity;
- selective audit and recourse;
- portability, restore, and exit;
- cultural rights and consent;
- the native no-AI boundary;
- gateway and governance separation;
- release and artifact integrity rules.

This relationship is baseline application, not profile inheritance. A profile cannot select only the global rules it prefers.

### 4.2 Primary profiles

A primary profile represents one deployable system identity.

It defines:

- intended environment and operator context;
- included and excluded scope;
- required, optional, conditional, and excluded capabilities;
- required, task-activated, and prohibited components;
- hardware and resource envelope;
- security and privilege posture;
- offline envelope;
- network and integration exposure;
- artifact and release behavior;
- operational and recovery behavior;
- conformance claim.

Primary profiles are siblings. They do not form a parent-child chain.

For example, `developer_windows_wsl` and `developer_linux_workstation` can share UV toolchain rules through the canonical toolchain contract. Neither profile inherits the other profile's host, container, security, hardware, or conformance rules.

### 4.3 Profile overlays

A profile overlay modifies or strengthens a compatible primary profile.

An overlay can:

- add required controls;
- strengthen identity or trust requirements;
- narrow external connectivity;
- add offline-transfer requirements;
- increase evidence obligations;
- constrain optional capabilities;
- add an appliance presentation surface;
- strengthen artifact or activation requirements;
- introduce profile-specific operational procedures.

An overlay does not define an independently deployable system. Its effective meaning exists only after composition with a compatible primary profile.

### 4.4 Relationship vocabulary

The profile relationship model distinguishes:

| Relationship | Meaning |
| --- | --- |
| `applies_global_baseline` | The profile is governed by current global authority |
| `compatible_overlay` | The overlay can be composed with the primary profile |
| `incompatible_overlay` | Composition is explicitly prohibited |
| `requires_overlay` | The profile or overlay depends on another declared overlay |
| `conflicts_with_overlay` | The two overlays cannot coexist |
| `sibling_profile` | The profiles share no inheritance relationship |
| `supersedes_profile_version` | A newer version replaces an older version of the same profile identity |
| `migration_source` | Historical input with no current profile authority |

Naming similarity does not establish any relationship.

### 4.5 Effective-profile equation

The effective profile is calculated as:

```text
active global baseline
+ exactly one active primary profile
+ zero or more active compatible overlays
+ applicable active exceptions or waivers
= one validated effective profile contract
```

Exceptions remain separate records. They do not modify the source profile contracts or become reusable inherited behavior.

The effective contract records every contributing object and version.

### 4.6 Composition order

Composition uses this authority order:

1. global constitutional and system authority;
2. primary-profile contract;
3. compatible overlay contracts;
4. applicable bounded exceptions or waivers;
5. generated effective-profile projection.

The order does not mean that a lower item can override a higher authority. It defines the sequence in which constraints are evaluated.

Multiple overlays use the ordering declared by their composition records when order affects meaning. An absent order for order-sensitive overlays blocks composition.

### 4.7 Merge strategies

Every composable field has an owner-defined merge strategy.

Common strategies include:

| Strategy | Use |
| --- | --- |
| `exact_match` | All contributors need the same value |
| `set_union` | Add controls, requirements, components, tests, or evidence |
| `set_intersection` | Retain only jointly permitted values |
| `explicit_exclusion` | Remove an optional item through a declared exclusion |
| `minimum_floor` | Enforce the highest declared minimum |
| `maximum_ceiling` | Enforce the lowest declared maximum |
| `ordered_composition` | Apply declared transformations in a validated order |
| `replace_same_profile_version` | Replace an older version of the same profile identity |

The schema or owning registry defines which strategy applies to each field. A validator does not choose a strategy from the data values.

### 4.8 Non-composable fields

Fields that establish identity or exclusive authority are not merged across profiles.

These include:

- primary profile identity;
- profile kind;
- canonical owner;
- primary deployment purpose;
- component data ownership;
- component identity;
- release-channel identity;
- artifact-class identity;
- authority order;
- global AI boundary;
- gateway separation;
- resource-governance and policy-governance ownership.

A requested change to one of these fields requires the owning canonical object and accepted decision, not an overlay workaround.

### 4.9 Capability calculation

Effective capability membership is calculated from:

- global capabilities;
- primary-profile membership;
- overlay additions and constraints;
- dependency closure;
- component availability;
- integration availability;
- resource envelope;
- offline envelope;
- security and authority rules;
- active exceptions;
- current tests and evidence.

Capabilities remain identified by their canonical capability IDs. Composition does not create unnamed implied capabilities.

An overlay can constrain an optional capability. It cannot remove a global or primary required capability while preserving an unqualified claim.

### 4.10 Component calculation

The effective component set distinguishes:

```text
required
session_activated
task_activated
optional
prohibited
```

Every included component resolves to the component registry and component-contract index.

Composition preserves:

- one owner for each authoritative data domain;
- direct-write prohibition across component boundaries;
- Resource Governor and Governance Policy Runtime separation;
- Publication Gateway and UCKK Dimension Gateway separation;
- runtime and development-workbench separation.

Component overlap between profiles does not create inheritance.

### 4.11 Resource and hardware calculation

Hardware and resource fields remain profile-scoped.

Composition can raise minimums, lower maximums, reserve resources, reduce concurrency, or disable optional high-cost work when the applicable merge strategy allows it.

The effective contract records:

- resulting hardware envelope;
- resulting resource class limits;
- Resource Governor behavior;
- pressure response;
- profile-specific exclusions;
- validation evidence.

A development workstation's hardware values do not become requirements for a user profile or sovereign production node.

### 4.12 Security, offline, and integration calculation

An overlay can strengthen:

- authentication;
- trust;
- network isolation;
- encryption;
- evidence;
- offline transfer;
- approval;
- recovery;
- artifact activation.

It cannot weaken the global boundaries.

The effective profile preserves:

- no native AI;
- optional approved external surfaces only;
- Ariane local non-voice navigation;
- deterministic native UCKK;
- optional and non-authoritative SenTient in eligible profiles;
- explicit integration classification and removal;
- offline continuity of declared local capabilities.

### 4.13 Version evolution

A new version of a profile can supersede an older version of the same profile identity.

Version evolution records:

- compatibility class;
- accepted decision;
- changed fields;
- impacted overlays;
- migration procedure;
- tests and evidence;
- supersession and activation.

Version succession is not inheritance. Historical versions remain evidence and do not contribute behavior to the active effective profile.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-INHERIT-001,REQ-PROFILE-INHERIT-002,REQ-PROFILE-INHERIT-003,REQ-PROFILE-INHERIT-004,REQ-PROFILE-INHERIT-005,REQ-PROFILE-INHERIT-006,REQ-PROFILE-INHERIT-007,REQ-PROFILE-INHERIT-008,REQ-PROFILE-INHERIT-009,REQ-PROFILE-INHERIT-010,REQ-PROFILE-INHERIT-011,REQ-PROFILE-INHERIT-012,REQ-PROFILE-INHERIT-013,REQ-PROFILE-INHERIT-014,REQ-PROFILE-INHERIT-015,REQ-PROFILE-INHERIT-016,REQ-PROFILE-INHERIT-017,REQ-PROFILE-INHERIT-018,REQ-PROFILE-INHERIT-019,REQ-PROFILE-INHERIT-020,REQ-PROFILE-INHERIT-021,REQ-PROFILE-INHERIT-022,REQ-PROFILE-INHERIT-023,REQ-PROFILE-INHERIT-024,REQ-PROFILE-INHERIT-025,REQ-PROFILE-INHERIT-026,REQ-PROFILE-INHERIT-027,REQ-PROFILE-INHERIT-028,REQ-PROFILE-INHERIT-029,REQ-PROFILE-INHERIT-030 -->
- **REQ-PROFILE-INHERIT-001 — SHALL:** Every active profile contract declare whether it is a primary profile or a profile overlay.
- **REQ-PROFILE-INHERIT-002 — SHALL:** Every active profile inherit the global constitutional and system baseline through explicit conformance to the active authority release.
- **REQ-PROFILE-INHERIT-003 — SHALL NOT:** Application of the global baseline be represented as inheritance from another deployment profile.
- **REQ-PROFILE-INHERIT-004 — SHALL:** A primary profile define one independently deployable system identity, intended environment, capability envelope, component set, resource envelope, security posture, offline behavior, lifecycle behavior, and conformance claim.
- **REQ-PROFILE-INHERIT-005 — SHALL NOT:** A primary profile inherit another primary profile's requirements, capabilities, components, implementation choices, hardware values, or conformance claims.
- **REQ-PROFILE-INHERIT-006 — SHALL:** Shared behavior between primary profiles originate from global registries, reusable component contracts, toolchain contracts, artifact contracts, or shared registered requirements rather than sibling-profile inheritance.
- **REQ-PROFILE-INHERIT-007 — SHALL:** A profile overlay be non-deployable by itself and declare the primary profiles with which it is compatible.
- **REQ-PROFILE-INHERIT-008 — SHALL:** A profile overlay declare every capability, component, control, resource, security, lifecycle, interface, or presentation field that it modifies.
- **REQ-PROFILE-INHERIT-009 — SHALL NOT:** A profile overlay redefine the identity, canonical owner, or primary deployment purpose of the primary profile to which it is applied.
- **REQ-PROFILE-INHERIT-010 — SHALL NOT:** A profile overlay weaken a global invariant, remove a required primary-profile capability, bypass an authority boundary, or invalidate a non-waivable lock.
- **REQ-PROFILE-INHERIT-011 — SHALL:** A profile overlay limit or disable an optional capability only when the modification is explicit, compatible with the primary profile, and reflected in the effective capability claim.
- **REQ-PROFILE-INHERIT-012 — SHALL:** Composition of more than one overlay require pairwise compatibility, declared ordering where ordering affects meaning, and a conflict-free effective contract.
- **REQ-PROFILE-INHERIT-013 — SHALL NOT:** A generic rule such as newest wins, longest definition wins, strongest wording wins, or stricter wins resolve a profile-composition conflict.
- **REQ-PROFILE-INHERIT-014 — SHALL:** Every profile relationship be represented by resolvable canonical references in the profile contract and profile index.
- **REQ-PROFILE-INHERIT-015 — SHALL NOT:** A relationship be inferred from file location, naming similarity, component overlap, installed software, shared implementation, implementation ancestry, or common deployment.
- **REQ-PROFILE-INHERIT-016 — SHALL:** The profile relationship graph be acyclic and contain only active, schema-valid profile records.
- **REQ-PROFILE-INHERIT-017 — SHALL:** The effective profile equal the active global baseline plus one primary profile plus zero or more compatible overlays plus separately registered applicable exceptions.
- **REQ-PROFILE-INHERIT-018 — SHALL NOT:** An exception or waiver become an inherited profile rule or alter unrelated profile instances.
- **REQ-PROFILE-INHERIT-019 — SHALL:** Every composable field use a merge strategy defined by the profile schema, owning registry, or accepted owner decision.
- **REQ-PROFILE-INHERIT-020 — SHALL:** An undefined merge strategy or incompatible field value block composition and the resulting conformance claim.
- **REQ-PROFILE-INHERIT-021 — SHALL:** Effective capability membership include only capabilities explicitly required, optional, conditional, excluded, or modified by the global model, primary profile, and active compatible overlays.
- **REQ-PROFILE-INHERIT-022 — SHALL:** Every enabled effective capability have complete dependency closure across components, authorities, data, artifacts, resources, integrations, and environment conditions.
- **REQ-PROFILE-INHERIT-023 — SHALL NOT:** A profile or overlay acquire authority to write another component's canonical data through inheritance or composition.
- **REQ-PROFILE-INHERIT-024 — SHALL:** Profile composition preserve the separation of Resource Governor from Governance Policy Runtime and Publication Gateway from UCKK Dimension Gateway.
- **REQ-PROFILE-INHERIT-025 — SHALL:** Profile composition preserve the no-native-AI baseline and represent ChatGPT, Suno, Gamma, and the approved Ariane voice adapter only as optional external surfaces.
- **REQ-PROFILE-INHERIT-026 — SHALL:** Profile composition preserve Ariane local non-voice navigation independently of external AI and external voice.
- **REQ-PROFILE-INHERIT-027 — SHALL:** SenTient remain optional, isolated, non-authoritative, and limited to eligible development or build profiles after all profile composition.
- **REQ-PROFILE-INHERIT-028 — SHALL:** An effective profile conformance claim identify the primary profile, all applied overlays, active exceptions, effective contract version, applicable release set, tests, and evidence.
- **REQ-PROFILE-INHERIT-029 — SHALL NOT:** A profile claim include inherited or composed behavior when any relationship, dependency, conflict, test, evidence item, or authority reference is unresolved.
- **REQ-PROFILE-INHERIT-030 — SHALL:** Profile-inheritance conformance include graph validation, compatibility validation, deterministic merge validation, scope containment, capability closure, component-boundary validation, lock evaluation, exception evaluation, and current evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Composition and State Transitions

### 6.1 Registering a primary profile

Registration proceeds through:

1. assign a stable profile identity;
2. classify the record as a primary profile;
3. bind the global baseline;
4. define scope and exclusions;
5. define capabilities and components;
6. define hardware and resource envelopes;
7. define security, offline, integration, lifecycle, and operational behavior;
8. declare compatible and incompatible overlays;
9. link decisions, requirements, locks, tests, and evidence;
10. validate the contract and profile index;
11. activate the profile through the authority release.

The primary profile remains outside active claims until validation passes.

### 6.2 Registering an overlay

Overlay registration proceeds through:

1. assign a stable overlay identity;
2. classify the record as a profile overlay;
3. declare compatible primary profiles;
4. declare required and conflicting overlays;
5. enumerate every modified field;
6. bind one merge strategy to each modification;
7. demonstrate preservation of global and primary boundaries;
8. define added tests and evidence;
9. validate every supported composition;
10. activate the overlay through the authority release.

An overlay with no compatible primary profile remains non-deployable and cannot support an active effective-profile claim.

### 6.3 Calculating an effective profile

Effective-profile calculation proceeds through:

```text
select_primary
resolve_global_baseline
resolve_overlays
validate_relationship_graph
validate_compatibility
order_overlays
apply_merge_strategies
apply_bounded_exceptions
resolve_capability_dependencies
resolve_component_set
resolve_resources
resolve_security_and_offline_behavior
evaluate_locks
evaluate_tests_and_evidence
emit_effective_contract
emit_conformance_claim
```

Every input object and version appears in the generated effective contract.

### 6.4 Adding an overlay

Adding an overlay:

1. verifies primary-profile compatibility;
2. verifies pairwise compatibility with existing overlays;
3. verifies required overlay dependencies;
4. determines composition order;
5. recalculates all affected fields;
6. recalculates capabilities and components;
7. executes applicable tests;
8. creates new evidence;
9. issues a new effective-profile identity or version;
10. retires the prior effective projection after successful activation.

The active source profile contracts remain unchanged.

### 6.5 Removing an overlay

Removing an overlay:

1. identifies behavior introduced or constrained by the overlay;
2. checks dependent overlays;
3. verifies that no active claim requires the overlay;
4. recalculates the effective contract;
5. removes overlay-specific components, resources, controls, and evidence;
6. verifies safe data and artifact handling;
7. validates the resulting primary profile and remaining overlays;
8. activates the replacement effective contract.

Removal does not silently retain an overlay rule as local configuration.

### 6.6 Changing profile compatibility

A compatibility change is semantic.

It includes:

- an accepted decision;
- impact analysis;
- affected profiles and overlays;
- effective-profile regeneration;
- test and evidence updates;
- compatibility or migration handling;
- authority activation after all dependent objects pass.

Existing effective profiles continue under their active versions until the replacement is valid or their claims are explicitly withdrawn.

## 7. Failure Modes and Safe Degradation

| Failure | Required behavior |
| --- | --- |
| Profile reference missing | Block composition and claim generation. |
| Profile record inactive | Exclude it from new effective profiles. |
| Primary profile absent | Block deployment identity creation. |
| More than one primary profile selected | Block composition. |
| Overlay used without a primary profile | Block deployment and claim generation. |
| Overlay incompatible with primary | Block composition. |
| Overlay pair incompatible | Block composition. |
| Required overlay absent | Block the dependent overlay. |
| Relationship cycle detected | Block every affected effective profile. |
| Merge strategy missing | Block the affected field and composition. |
| Field values conflict | Preserve source records and block the effective contract. |
| Capability dependency unresolved | Exclude the claim and block dependent activation. |
| Required component unavailable | Mark affected capabilities blocked or unavailable according to the primary profile. |
| Resource envelope inconsistent | Block activation until a valid envelope is calculated. |
| Global lock violation | Block composition; no overlay or exception inference occurs. |
| Evidence expired | Block the affected conformance claim. |
| Exception expired | Recalculate without the exception and block incompatible claims. |
| Generated effective contract stale | Exclude it from authority and regenerate. |
| Profile index disagrees with contract | Block profile discovery and activation until canonical alignment is restored. |

A failed overlay does not corrupt its primary profile. The last valid effective profile can remain active according to release and rollback policy.

## 8. Authority, Security, and Scope Boundaries

Profile composition does not alter canonical ownership.

The effective profile remains inside:

- global authority order;
- component data ownership;
- component interface contracts;
- policy and privilege boundaries;
- release and artifact identities;
- integration classifications;
- audit and recourse controls;
- profile-specific scope.

Security controls are cumulative or explicitly constraining according to their merge strategies. Ambiguity blocks composition.

An overlay cannot:

- grant itself host privilege;
- write component data directly;
- expand a provider's authority;
- reclassify external AI as native;
- create a new release channel;
- change a component's owner;
- make a migration source current authority;
- turn a recipe into a global requirement.

Profile contracts contain no embedded credentials or unrestricted secrets. Effective contracts reference managed secret requirements and profile-specific provisioning rules.

Generated AI context identifies the selected primary profile and overlays. An AI agent does not infer profile relationships from a task description or host environment.

## 9. Exceptions and Compatibility

Exceptions and waivers are evaluated after profile and overlay composition.

An applicable record identifies:

- exact deployment or effective-profile target;
- affected requirements and locks;
- compensating controls;
- expiration;
- conformance effect;
- human risk owner and approval;
- tests and evidence.

An exception does not change compatibility for other profiles. It does not become part of an overlay. It does not survive outside its declared scope or duration.

Compatibility evaluation covers:

- profile and overlay versions;
- capability membership;
- component contracts;
- artifact classes;
- toolchain versions;
- resource envelopes;
- security controls;
- offline behavior;
- integrations;
- lifecycle rules;
- tests and evidence.

A composition is compatible only when all applicable relationships and field-level merge rules pass. Similarity, successful startup, or implementation experience is insufficient.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. every active profile has one unique identity and one profile kind;
2. every primary profile is independently deployable;
3. every overlay is non-deployable by itself;
4. the global baseline applies to every active profile;
5. no primary profile inherits another primary profile;
6. shared behavior originates from canonical common owners;
7. every profile relationship resolves through the profile index and contracts;
8. the relationship graph is acyclic;
9. every overlay lists compatible primaries;
10. every multi-overlay composition is pairwise compatible;
11. ordering is present for order-sensitive composition;
12. every modified field has an owner-defined merge strategy;
13. undefined or conflicting values block composition;
14. non-composable identity and ownership fields remain unchanged;
15. effective capabilities are explicit and dependency-complete;
16. effective components preserve canonical ownership and separation;
17. resource and hardware envelopes are profile-scoped and internally consistent;
18. security, offline, lifecycle, and integration rules preserve global locks;
19. no native AI enters an effective profile;
20. approved external AI surfaces remain optional and non-authoritative;
21. Ariane local navigation remains independent of external voice;
22. SenTient remains optional, isolated, non-authoritative, and eligible-profile-only;
23. exceptions remain bounded and separately visible;
24. effective-profile claims include all contributing versions, tests, and evidence;
25. stale generated effective contracts are rejected;
26. all decisions, requirements, locks, components, capabilities, tests, evidence, and exceptions resolve;
27. no unresolved marker or inferred relationship enters active authority.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_profile_inheritance.py
tools/check_interfile_locks.py
tools/check_component_boundaries.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
tools/generate_profile_matrix.py --check
```

## 11. Non-Normative Examples

### 11.1 Shared UV behavior without profile inheritance

`developer_linux_workstation` and `developer_windows_wsl` both use the canonical UV toolchain contract. They remain sibling primary profiles. The Windows profile does not inherit Linux host, container, privilege, or conformance rules.

### 11.2 High-assurance composition

A compatible production primary profile composes with `high_assurance`. The overlay adds stronger trust, evidence, approval, and activation controls. It does not change the primary profile identity or component ownership.

### 11.3 Sovereign-offline composition

A compatible sovereign primary profile composes with `sovereign_offline`. The effective profile adds validated offline bundles, restricted network behavior, local continuity evidence, and offline recovery requirements.

### 11.4 Appliance-shell composition

A compatible primary profile composes with `appliance_shell`. The overlay constrains presentation and operator interaction. It does not redefine the runtime components or create a new system authority.

### 11.5 Invalid developer composition

`developer_windows_wsl` lists `high_assurance`, `sovereign_offline`, and `appliance_shell` as incompatible overlays. Selecting one of those overlays blocks effective-profile generation rather than converting the development workstation into a sovereign production profile.

### 11.6 Optional SenTient

A developer primary profile enables SenTient as an isolated optional workbench. A shared component list in another profile does not inherit SenTient. A non-development profile needs its own explicit eligibility decision and contract before any such capability appears.

### 11.7 Resource merge

A primary profile permits two background media jobs. A compatible overlay sets a maximum ceiling of one. The effective profile records one. A second overlay requesting a conflicting minimum of three blocks composition unless an accepted decision defines a compatible field model.

### 11.8 Expired waiver

An effective profile temporarily uses a waiver for one test environment. At expiration, the waiver disappears from the calculation. The source profiles remain unchanged, and the affected conformance claim becomes blocked until the requirement passes or a valid new authority exists.
