<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "deployment_profiles",
  "scope": [
    "user_lightweight",
    "developer_linux_workstation",
    "developer_windows_wsl",
    "sovereign_linux_node",
    "sovereign_hub",
    "build_farm",
    "control_plane",
    "high_assurance",
    "sovereign_offline",
    "appliance_shell"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
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
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/artifact-contracts/node-profile.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-PROFILE-002",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-COMP-001",
    "REQ-PROFILE-COMP-002",
    "REQ-PROFILE-COMP-003",
    "REQ-PROFILE-COMP-004",
    "REQ-PROFILE-COMP-005",
    "REQ-PROFILE-COMP-006",
    "REQ-PROFILE-COMP-007",
    "REQ-PROFILE-COMP-008",
    "REQ-PROFILE-COMP-009",
    "REQ-PROFILE-COMP-010",
    "REQ-PROFILE-COMP-011",
    "REQ-PROFILE-COMP-012",
    "REQ-PROFILE-COMP-013",
    "REQ-PROFILE-COMP-014",
    "REQ-PROFILE-COMP-015",
    "REQ-PROFILE-COMP-016",
    "REQ-PROFILE-COMP-017",
    "REQ-PROFILE-COMP-018",
    "REQ-PROFILE-COMP-019",
    "REQ-PROFILE-COMP-020",
    "REQ-PROFILE-COMP-021",
    "REQ-PROFILE-COMP-022",
    "REQ-PROFILE-COMP-023",
    "REQ-PROFILE-COMP-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DOC-002",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-SYS-000",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018"
  ],
  "tags": [
    "profiles",
    "profile-composition",
    "overlays",
    "deterministic-merge",
    "scope-containment",
    "conformance",
    "explicit-inheritance"
  ]
}
KOA:DOC-META:END -->

# Profile Composition and Overlays

## 1. Purpose

This document defines how kOA deployment profiles and overlays compose into one effective deployment configuration.

The profile model separates complete deployment forms from conditional overlays:

- a primary profile defines the complete base deployment form;
- an overlay adds or constrains a declared set of conditions;
- the global constitutional and system baseline remains applicable to every composition;
- profile composition never creates implicit inheritance or duplicate authority.

The result of composition is deterministic, machine-validatable, and traceable to active profile contracts.

## 2. Scope

This document applies to the seven active primary profiles:

- `user_lightweight`;
- `developer_linux_workstation`;
- `developer_windows_wsl`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`.

It also applies to the three active overlays:

- `high_assurance`;
- `sovereign_offline`;
- `appliance_shell`.

It governs:

- selection of a primary profile;
- selection and compatibility of overlays;
- deterministic merge behavior;
- profile and overlay scope;
- effective component membership;
- effective capabilities;
- resource and hardware constraints;
- physical isolation;
- offline behavior;
- assurance and evidence requirements;
- profile exceptions;
- effective-profile activation and rollback;
- profile conformance claims.

This document does not define the detailed behavior of any individual profile. Each profile contract remains the exclusive owner of its own capabilities, component membership, resource envelope, prerequisites, compatibility declarations, and conformance rules.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/profile-catalog.json` | Owns profile identity, classification, catalog membership, contract paths, versions, and lifecycle status. |
| `contracts/profiles/*.profile.json` | Owns detailed behavior, membership, compatibility, merge operations, prerequisites, and conformance for each profile. |
| `contracts/system.contract.json` | Owns global system behavior that profiles cannot silently redefine. |
| `generated/component-catalog.json` | Owns global component identities and logical responsibility boundaries. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns profile, component, data, governance, AI, and lifecycle alignment assertions. |
| `generated/exception-index.json` | Owns approved scoped deviations and their compensating controls. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, and evidence relationships. |
| `contracts/artifact-contracts/node-profile.schema.json` | Defines the machine-readable effective-profile declaration used for deployment and conformance evidence. |

Profile behavior is owned by the individual profile contracts. This document explains composition semantics without duplicating their profile-specific values.

## 4. Model and Responsibilities

### 4.1 Primary profiles

A primary profile is a complete deployment form. It establishes the base:

- deployment purpose;
- component membership;
- capability membership;
- operating modes;
- resource and hardware envelope;
- storage and network assumptions;
- offline capability;
- security and assurance baseline;
- lifecycle behavior;
- conformance evidence.

Exactly one primary profile participates in an effective deployment configuration.

A primary profile is not an ancestor from which unrelated profiles inherit implicitly. Shared global behavior comes from the constitutional and system baseline, not from copying one primary profile into another.

### 4.2 Overlays

An overlay is not a standalone deployment form. It modifies a compatible primary profile through declared operations.

The active overlays have these roles:

| Overlay | Composition role |
| --- | --- |
| `high_assurance` | Adds stronger verification, separation, evidence, recovery, and governed-control conditions. |
| `sovereign_offline` | Adds disconnected-operation, local-authority, offline-import, offline-update, and continuity conditions. |
| `appliance_shell` | Constrains the user interface and host interaction surface for appliance-style operation. |

The exact compatible bases, prerequisites, exclusions, component changes, capability changes, and conformance checks remain owned by each overlay contract.

### 4.3 Effective profile

An effective profile is the validated result of:

```text
global constitutional and system baseline
+ one active primary profile
+ zero or more compatible active overlays
+ zero or more active scoped exceptions
= one effective deployment configuration
```

The effective profile records:

- primary profile identity and version;
- overlay identities and versions;
- applicable system and constitutional versions;
- applied exception identities;
- effective capabilities;
- effective component membership;
- effective constraints;
- unresolved conflicts, which must be empty;
- validation outcome;
- generated evidence identity.

The effective profile is a derived configuration. It does not replace the source contracts.

### 4.4 Composition operators

Every composable field declares a merge operator.

| Operator | Deterministic result |
| --- | --- |
| `exact` | One value is accepted; unequal active assignments conflict unless an explicit replacement rule exists. |
| `set_union` | Unique permitted values are combined. |
| `set_intersection` | Only values permitted by every applicable contract remain. |
| `minimum_floor` | The greatest applicable minimum is selected. |
| `maximum_ceiling` | The smallest applicable maximum is selected. |
| `range_intersection` | The common numeric or version range is selected; an empty range conflicts. |
| `require_union` | All required items are combined. |
| `prohibit_union` | All prohibited items are combined. |
| `capability_state` | Required, optional, unavailable, and prohibited states are resolved by the declared capability-state rules; contradictory states conflict. |
| `component_state` | Required, optional, excluded, and prohibited component states are resolved by the declared component-state rules; contradictory states conflict. |
| `ordered_pipeline` | Steps compose only in the canonical order declared by the contracts. |
| `replace_declared_target` | A value is replaced only when the base marks the field overlayable and the overlay identifies the exact replacement target. |

A field without a declared operator is not overlayable.

### 4.5 Conflict behavior

Composition is blocked when:

- more than one primary profile is selected;
- an overlay has no primary base;
- an overlay does not list the selected primary profile as compatible;
- selected overlays are mutually incompatible;
- a prerequisite is missing;
- two exact assignments disagree without an explicit replacement rule;
- a range intersection is empty;
- a capability is both required and prohibited;
- a component is both required and prohibited;
- an overlay weakens a global prohibition;
- an exception is missing, inactive, expired, or outside its scope;
- required tests or evidence are absent.

No file order, overlay listing order, implementation default, or operator preference repairs an undeclared conflict.

### 4.6 Scope containment

A composed rule retains the narrowest applicable scope.

Examples:

- an appliance-shell user-interface constraint remains scoped to deployments that activate `appliance_shell`;
- a high-assurance evidence requirement remains scoped to deployments that activate `high_assurance`;
- a sovereign-offline network rule remains scoped to deployments that activate `sovereign_offline`;
- a development-workspace rule remains scoped to the applicable developer primary profiles;
- a global component or data-ownership rule remains global across all compositions.

### 4.7 Composition authority

Responsibilities remain separated:

| Object | Responsibility |
| --- | --- |
| Profile index | Identity, classification, membership, paths, active versions |
| Primary profile contract | Complete base deployment behavior |
| Overlay contract | Compatibility, constraints, additions, exclusions, merge operations |
| System registry | Global behavior and boundaries |
| Component registry | Global component identity and logical ownership |
| Requirements registry | Normative statements |
| Locks registry | Cross-file invariants |
| Exceptions registry | Authorized scoped deviations |
| Effective-profile declaration | Derived result and activation evidence |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-COMP-001,REQ-PROFILE-COMP-002,REQ-PROFILE-COMP-003,REQ-PROFILE-COMP-004,REQ-PROFILE-COMP-005,REQ-PROFILE-COMP-006,REQ-PROFILE-COMP-007,REQ-PROFILE-COMP-008,REQ-PROFILE-COMP-009,REQ-PROFILE-COMP-010,REQ-PROFILE-COMP-011,REQ-PROFILE-COMP-012,REQ-PROFILE-COMP-013,REQ-PROFILE-COMP-014,REQ-PROFILE-COMP-015,REQ-PROFILE-COMP-016,REQ-PROFILE-COMP-017,REQ-PROFILE-COMP-018,REQ-PROFILE-COMP-019,REQ-PROFILE-COMP-020,REQ-PROFILE-COMP-021,REQ-PROFILE-COMP-022,REQ-PROFILE-COMP-023,REQ-PROFILE-COMP-024 -->
- **REQ-PROFILE-COMP-001 — SHALL:** Every effective deployment configuration selects exactly one active primary profile.
- **REQ-PROFILE-COMP-002 — SHALL:** An effective deployment configuration may select zero or more active overlays.
- **REQ-PROFILE-COMP-003 — SHALL NOT:** An overlay is activated without an active primary profile.
- **REQ-PROFILE-COMP-004 — SHALL:** Each overlay contract declares its compatible primary profiles, incompatible profiles, incompatible overlays, prerequisites, added requirements, constrained values, and validation rules.
- **REQ-PROFILE-COMP-005 — SHALL NOT:** Compatibility, inheritance, or overlay applicability is inferred from profile names, implementation similarity, historical deployment, or documentation proximity.
- **REQ-PROFILE-COMP-006 — SHALL:** The effective profile is derived from the global system baseline, one primary profile, the selected compatible overlays, and active scoped exceptions.
- **REQ-PROFILE-COMP-007 — SHALL NOT:** A primary profile or overlay weakens a global constitutional or system-baseline prohibition.
- **REQ-PROFILE-COMP-008 — SHALL:** An overlay modifies only fields explicitly declared overlayable by the applicable schema and contracts.
- **REQ-PROFILE-COMP-009 — SHALL:** Every overlay operation uses a declared deterministic merge operator.
- **REQ-PROFILE-COMP-010 — SHALL:** Conflicting exact assignments, empty range intersections, incompatible capability states, incompatible component states, or incompatible authority claims block composition.
- **REQ-PROFILE-COMP-011 — SHALL NOT:** Overlay order is used as an undocumented conflict-resolution mechanism.
- **REQ-PROFILE-COMP-012 — SHALL:** When overlay operations are order-sensitive, the active contracts declare one canonical order and the validator verifies that order.
- **REQ-PROFILE-COMP-013 — SHALL:** Profile-specific requirements remain scoped to the primary profile or overlay that owns them.
- **REQ-PROFILE-COMP-014 — SHALL NOT:** A profile or overlay requirement becomes global through repetition, common deployment, inheritance, or implementation convenience.
- **REQ-PROFILE-COMP-015 — SHALL:** Logical component and data ownership remains stable across profile composition unless an accepted owner decision explicitly changes global ownership.
- **REQ-PROFILE-COMP-016 — SHALL:** Profile composition may strengthen physical isolation, assurance, offline operation, interface restrictions, recovery controls, and evidence requirements without silently changing global logical ownership.
- **REQ-PROFILE-COMP-017 — SHALL:** Every effective profile declaration records the primary profile, selected overlays, contract versions, applied exceptions, composition result, and validation outcome.
- **REQ-PROFILE-COMP-018 — SHALL:** A component is active in an effective profile only when the composed component membership permits it and all component prerequisites resolve.
- **REQ-PROFILE-COMP-019 — SHALL:** A capability is claimed only when the composed capability state, dependencies, resources, security controls, offline behavior, and evidence requirements are satisfied.
- **REQ-PROFILE-COMP-020 — SHALL NOT:** An exception silently repairs an incompatible composition or expands its own declared scope.
- **REQ-PROFILE-COMP-021 — SHALL:** A semantic change to profile classification, compatibility, merge behavior, ownership, or conformance produces an accepted decision, impact analysis, updated tests, and updated evidence before activation.
- **REQ-PROFILE-COMP-022 — SHALL:** Composition failure preserves the last valid effective profile and blocks activation of the invalid composition.
- **REQ-PROFILE-COMP-023 — SHALL:** Generated profile catalogs, effective-profile views, and AI context packages remain projections of active profile contracts.
- **REQ-PROFILE-COMP-024 — SHALL:** Every active composition rule is traceable to accepted decisions, applicable locks, validation tests, and evidence requirements.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating an effective profile

The composition process:

1. resolves the active authority release;
2. selects exactly one active primary profile;
3. resolves the selected overlay contracts;
4. verifies primary-to-overlay compatibility;
5. verifies pairwise overlay compatibility;
6. resolves all prerequisites and exclusions;
7. loads applicable global constitutional and system constraints;
8. applies each declared merge operator;
9. applies active scoped exceptions;
10. resolves effective components, capabilities, resources, security controls, lifecycle rules, and evidence requirements;
11. validates the complete composition;
12. emits an effective-profile declaration;
13. activates the result only after validation passes.

### 6.2 Adding an overlay

Adding an overlay:

1. identifies the active effective profile;
2. resolves the overlay contract and version;
3. verifies compatible primary profiles;
4. verifies compatibility with existing overlays;
5. calculates direct and transitive impacts;
6. recomputes every affected composed field;
7. runs profile, component, security, lifecycle, offline, and conformance tests;
8. emits replacement evidence;
9. activates the new effective profile atomically.

The previous effective profile remains the rollback target until the new composition is accepted.

### 6.3 Removing an overlay

Removing an overlay:

1. verifies that no active dependency requires it;
2. removes only rules owned by that overlay;
3. recomputes values inherited from the primary profile and remaining overlays;
4. verifies that capabilities and components still satisfy their prerequisites;
5. reruns affected conformance tests;
6. activates the recomposed profile atomically.

Removing an overlay does not remove global rules or unrelated primary-profile behavior.

### 6.4 Changing composition semantics

A change to classification, compatibility, merge operators, conflict behavior, or overlay authority:

1. records an accepted owner decision;
2. produces a transitive impact report;
3. updates the relevant profile contracts and schema;
4. updates requirements and locks;
5. updates effective-profile generation;
6. updates tests and evidence;
7. validates all affected primary and overlay combinations;
8. activates the replacement semantics last.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved state | Blocked state | Evidence |
| --- | --- | --- | --- | --- |
| No primary profile selected | Reject composition | Last valid effective profile | New activation | Composition failure |
| Multiple primary profiles selected | Reject composition | Last valid effective profile | New activation | Primary-profile conflict |
| Overlay incompatible with primary | Reject overlay addition | Current valid composition | Incompatible composition | Compatibility failure |
| Overlays incompatible with each other | Reject combined composition | Last valid overlay set | Conflicting overlay set | Pairwise conflict record |
| Merge operator absent | Mark field non-composable | Source profile contracts | Derived value | Schema or contract failure |
| Exact values conflict | Block composition | Last valid value | Undeclared replacement | Merge-conflict evidence |
| Effective range is empty | Block composition | Last valid envelope | Impossible envelope | Range-conflict evidence |
| Required component is prohibited | Block composition | Last valid component set | Contradictory membership | Component conflict |
| Required capability is unavailable | Block capability claim or composition as declared | Unaffected capabilities | Unsupported claim | Capability-resolution failure |
| Required exception is inactive | Reject deviation | Canonical unmodified rule | Exception-dependent composition | Exception validation failure |
| Effective-profile generator is stale | Reject generated result | Source contracts | Activation of stale projection | Generation validation failure |
| New composition fails validation | Retain previous active composition | Last valid deployment state | New profile activation | Validation report |

## 8. Cross-Component Interactions

Profile composition affects component deployment without changing global component identity or logical ownership.

For each effective profile, component resolution determines:

- required components;
- optional components;
- excluded components;
- prohibited components;
- startup and recovery prerequisites;
- resource envelopes;
- network and storage isolation;
- required integrations;
- offline availability;
- evidence and conformance obligations.

A component contract remains bounded by:

- global constitutional rules;
- system-baseline rules;
- the effective primary profile;
- selected overlays;
- active security and lifecycle rules;
- active scoped exceptions.

A profile can require stronger physical separation or additional gateways. It cannot authorize direct writes across component-owned data, merge Resource Governor and Governance Policy Runtime authority, convert external AI into native authority, or transfer canonical ownership by deployment convention.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-PROFILE-001` | Establishes seven primary profiles and three composable overlays. |
| `DEC-PROFILE-002` | Establishes explicit deterministic profile composition and overlay rules. |
| `DEC-DATA-001` | Keeps logical data ownership stable across profile-dependent physical deployment. |
| `DEC-GOV-001` | Keeps Resource Governor and Governance Policy Runtime as separate authorities across profile composition. |
| `DEC-AI-001` | Keeps the external AI boundary global and unavailable for profile-level silent weakening. |

### Prohibited assumptions

- an overlay can run without a primary profile;
- two primary profiles can be merged into one deployment;
- an overlay is compatible because its name or purpose appears related;
- all overlays are compatible with all primary profiles;
- overlay order can silently choose a winner;
- a later file overrides an earlier file;
- a stricter-looking statement automatically wins;
- a profile-specific rule becomes global through repetition;
- a primary profile inherits another primary profile;
- an overlay can change component or data ownership implicitly;
- a compatible composition is automatically conformant;
- an implementation recipe defines compatibility;
- a deployed combination is authoritative because it appears to work;
- an exception can expand beyond its approved scope;
- a generated effective profile is independent authority;
- missing compatibility data can be inferred.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-PROFILE-001` is active at `03-profiles/01-profile-composition-and-overlays.md`.
2. The profile index contains exactly seven active primary profiles and three active overlays.
3. Every profile identity and contract reference resolves.
4. Every listed decision exists with status `accepted`.
5. Every requirement in Section 5 exists with identical strength, statement, scope, owner, decision source, and validation mapping.
6. Every listed lock exists and is active.
7. Every effective profile selects exactly one primary profile.
8. Every overlay declares compatible bases, conflicts, prerequisites, operations, and validation.
9. Every composable field declares a supported merge operator.
10. No composition depends on file order or undeclared overlay order.
11. Every selected overlay is compatible with the primary profile and every other selected overlay.
12. Global prohibitions remain effective in every composition.
13. Profile-specific requirements retain their profile or overlay scope.
14. Logical component and data ownership remains stable.
15. Effective component and capability claims satisfy prerequisites and evidence.
16. Empty range intersections and contradictory component or capability states fail validation.
17. Invalid composition preserves the last valid effective profile.
18. Every effective-profile declaration records source versions, overlays, exceptions, result, and validation outcome.
19. Generated effective-profile views remain reproducible projections.
20. Active prose is English and contains no unresolved-authority marker.
21. No normative keyword appears outside the generated requirement block.
22. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates composition mechanics. It does not declare compatibility that is absent from the profile contracts.

A deployment can select `sovereign_linux_node` as its primary profile and add an overlay only when that overlay contract explicitly lists `sovereign_linux_node` as compatible. The effective result includes the primary rules plus the overlay's declared constraints.

> **Non-normative example:** This example illustrates deterministic ranges. It does not define a profile value.

A primary profile can declare a memory minimum and an overlay can declare a higher minimum. The `minimum_floor` operator selects the higher applicable minimum. If one contract sets a maximum below that result, the range is empty and composition fails.

> **Non-normative example:** This example illustrates scope containment. It does not make an overlay global.

An appliance-shell constraint affects only deployments that activate `appliance_shell`. Standard user and developer profiles do not inherit the restricted shell merely because the overlay exists in the catalog.

> **Non-normative example:** This example illustrates authority separation.

A high-assurance composition can require stronger evidence and physical isolation. It does not transfer application data ownership to the Governance Policy Runtime or resource authority to the policy runtime.

> **Non-normative example:** This example illustrates projection behavior.

An effective-profile JSON file can list the resolved components, capabilities, limits, and evidence requirements. The file is generated from active contracts and does not replace them.
