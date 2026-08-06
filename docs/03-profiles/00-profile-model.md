<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PRO-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profiles",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/profile_model",
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
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md",
    "03-profiles/14-koa-spaces-deployment.md"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-DEV-001",
    "DEC-DEV-002",
    "DEC-AI-001",
    "DEC-SENT-001"
  ],
  "requirement_ids": [
    "REQ-PRO-MODEL-001",
    "REQ-PRO-MODEL-002",
    "REQ-PRO-MODEL-003",
    "REQ-PRO-MODEL-004",
    "REQ-PRO-MODEL-005",
    "REQ-PRO-MODEL-006",
    "REQ-PRO-MODEL-007",
    "REQ-PRO-MODEL-008",
    "REQ-PRO-MODEL-009",
    "REQ-PRO-MODEL-010",
    "REQ-PRO-MODEL-011",
    "REQ-PRO-MODEL-012",
    "REQ-PRO-MODEL-013",
    "REQ-PRO-MODEL-014",
    "REQ-PRO-MODEL-015",
    "REQ-PRO-MODEL-016",
    "REQ-PRO-MODEL-017",
    "REQ-PRO-MODEL-018",
    "REQ-PRO-MODEL-019",
    "REQ-PRO-MODEL-020"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-GOV-001",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CON-006",
    "DOC-SYS-000",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-021",
    "DOC-SYS-022",
    "DOC-PROFILE-014"
  ],
  "tags": [
    "profiles",
    "profile-model",
    "overlays",
    "composition",
    "inheritance",
    "conformance",
    "scope",
    "security-controls",
    "security-applicability",
    "koa-spaces",
    "profile-membership"
  ]
}
KOA:DOC-META:END -->

# Profile Model

## 1. Purpose

This document defines the deployment-profile model of the kOA operating environment.

A profile is a machine-readable declaration of the capabilities, components, operating constraints, resource envelopes, security properties, lifecycle behavior, offline behavior, and conformance obligations that apply to one deployment form.

The profile model exists to prevent deployment-specific choices from being mistaken for global system requirements.

It establishes:

- the distinction between the global system baseline, primary profiles, and overlays;
- the canonical set of primary profiles and composable overlays;
- profile identity and lifecycle;
- profile composition and precedence;
- explicit inheritance;
- component and capability membership;
- profile-specific requirements and restrictions;
- resource, data, security, lifecycle, and offline constraints;
- profile conformance claims;
- validation and evidence expectations.

A profile is not a product edition, marketing label, hardware SKU, container technology, operating-system package list, or implementation recipe. It is a canonical scope of architectural applicability.

## 2. Scope

This document applies globally to:

- all profile contracts under `contracts/profiles/`;
- the profile index;
- all primary deployment profiles;
- all profile overlays;
- profile-specific requirements;
- component membership and optionality;
- capability membership;
- hardware and resource envelopes;
- storage and data-isolation choices;
- security and governance properties;
- release and artifact compatibility;
- offline and degradation behavior;
- development toolchains;
- conformance claims, tests, and evidence;
- profile-specific documentation and recipes.

It governs the relationship between:

1. the global system baseline;
2. one selected primary profile;
3. zero or more compatible overlays;
4. applicable component contracts;
5. applicable artifact and toolchain contracts;
6. applicable security, lifecycle, operations, and conformance rules.

This document does not define the complete content of each profile. Each profile contract owns its own capability membership, component membership, defaults, constraints, and claims.

Profile contracts do not own the cross-profile security-control matrix. `contracts/security-controls.contract.json` owns security-control identifiers, categories, profile applicability, implementation bindings, validation bindings, failure behavior, and evidence classes. A profile may supply facts used to resolve conditional applicability, but it SHALL NOT duplicate or override the canonical mapping.

This document does not make a deployment profile mandatory merely because it exists.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `generated/authority-manifest.json` | Activates profile registries, contracts, schemas, and documentation versions. |
| `generated/decision-index.json` | Owns accepted decisions that establish or modify profile behavior. |
| `contracts/system.contract.json#/profile_model` | Owns the global profile classes, composition model, and profile-model invariants. |
| `generated/profile-catalog.json` | Owns the active profile and overlay inventory, profile paths, identifiers, versions, classes, and lifecycle status. |
| `contracts/profiles/*.profile.json` | Own each profile's capabilities, components, requirements, defaults, restrictions, dependencies, resource envelopes, and conformance claims. |
| `generated/component-catalog.json` | Owns component identities, responsibilities, dependencies, and authoritative data ownership. |
| `generated/requirements-index.json` | Owns the normative requirements displayed in Section 5. |
| `generated/assertion-index.json` | Owns cross-file profile, component, data, AI, governance, and development invariants. |
| `generated/traceability.json` | Links profiles to decisions, requirements, components, tests, evidence, artifacts, and documents. |
| `generated/exception-index.json` | Owns approved profile-specific deviations and compensating controls. |
| `schemas/deployment-profile.schema.json` | Defines structural validity for profile contracts. |
| `schemas/profile-index.schema.json` | Defines structural validity for the profile index. |
| `contracts/security-controls.contract.json` | Owns security-control identifiers and applicability for every primary profile and overlay. |
| `schemas/security-controls.contract.schema.json` | Defines structural validity for the security-control contract. |
| `contracts/artifact-contracts/security-evidence.schema.json` | Defines evidence records for evaluated security controls. |

Profile Markdown explains the profile contracts. It does not maintain a second capability matrix or component list.

## 4. Model and Responsibilities

### 4.1 Profile layers

The effective deployment configuration is evaluated in this order:

`text
global system baseline
 ↓
one primary profile
 ↓
zero or more compatible overlays
 ↓
applicable component contracts
 ↓
applicable artifact, toolchain, security, lifecycle, operations, and conformance contracts
`

The global baseline defines behavior that applies to every profile.

A primary profile defines one complete deployment purpose and its mandatory baseline.

An overlay adds or narrows a bounded cross-cutting property. It does not replace the primary profile.

### 4.2 Primary profiles

The active primary profile classes are:

| Profile ID | Deployment purpose |
| --- | --- |
| `user_lightweight` | Resource-bounded local user operation with a minimal installed and always-running set. |
| `developer_linux_workstation` | Native Linux development with isolated parallel workspaces and reproducible toolchains. |
| `developer_windows_wsl` | Windows-hosted development through WSL2 and permitted development services without claiming sovereign Linux-node conformance. |
| `sovereign_linux_node` | Governed Linux production node with explicit release, identity, privilege, recovery, offline, and evidence properties. |
| `sovereign_hub` | Multi-node sovereign service hub with stronger coordination, storage, lifecycle, and operational responsibilities. |
| `build_farm` | Controlled build and publication environment for reproducible artifacts, tests, provenance, and evidence. |
| `control_plane` | Governed coordination and management environment for declared control-plane capabilities. |

Exactly one primary profile is selected for one profile instance.

A host may run multiple isolated profile instances only when each instance has a distinct identity, authority scope, state boundary, resource envelope, and conformance record.

### 4.3 Overlays

The active overlays are:

| Overlay ID | Cross-cutting effect |
| --- | --- |
| `high_assurance` | Adds stronger identity, trust, isolation, evidence, verification, and security requirements. |
| `sovereign_offline` | Adds stronger offline-continuity, offline-import, local-authority, synchronization, and recovery requirements. |
| `appliance_shell` | Adds a constrained user-shell and appliance interaction model where compatible with the selected primary profile. |

An overlay:

- declares compatible primary profiles;
- declares incompatible overlays;
- declares the properties it adds or narrows;
- declares its requirements and tests;
- does not silently remove a primary-profile obligation;
- does not become a standalone deployment profile.

### 4.4 Profile instance

A profile instance has:

- a unique instance identifier;
- one primary profile ID and version;
- zero or more overlay IDs and versions;
- one effective profile version;
- applicable hardware and resource facts;
- enabled and disabled capabilities;
- installed, required, optional, and prohibited components;
- applicable artifact and release channels;
- applicable toolchains;
- storage and data-isolation configuration;
- identity and trust configuration;
- offline and degradation configuration;
- validation results;
- conformance claims;
- evidence references;
- exception references.

The instance record does not modify canonical profile definitions.

### 4.5 Capability membership

Each capability is classified for a profile as one of:

| Membership | Meaning |
| --- | --- |
| `required` | The capability is part of the profile's mandatory baseline and must pass its conformance checks. |
| `optional` | The capability may be installed or activated without changing the mandatory baseline. |
| `conditional` | The capability applies only when its declared condition is true. |
| `prohibited` | The capability must not be enabled in a conforming instance. |
| `not_applicable` | The capability does not belong to the profile's scope. |

An optional capability does not become required through prevalence, packaging, or user-interface exposure.

A prohibited capability cannot be enabled through a recipe or local default.

### 4.6 Component membership

Each component is classified for a profile as:

- required;
- optional;
- conditional;
- prohibited;
- external integration only.

Component membership references the canonical component identifier.

A profile may consolidate or separate component processes and storage without changing logical responsibility or data ownership.

### 4.7 Defaults and restrictions

A profile contract may define:

- enabled-by-default capabilities;
- disabled-by-default optional capabilities;
- startup behavior;
- task activation;
- worker concurrency;
- loaded-language limits;
- resource budgets;
- storage placement;
- network exposure;
- offline requirements;
- external integration availability;
- artifact and release channels;
- backup, restore, and exit obligations.

A default is not a requirement unless a registered requirement states that the default must be preserved.

A restriction is enforced independently of implementation convenience.

### 4.8 Composition result

Profile composition produces one deterministic effective profile.

The effective profile contains:

- the union of applicable requirements;
- the union of mandatory validation checks;
- the intersection of allowed capabilities;
- the union of prohibited capabilities;
- the narrowest compatible resource and security constraints;
- explicit component membership;
- explicit artifact and release compatibility;
- resolved defaults;
- resolved exceptions;
- a composition report.

A value is not resolved by textual order, filename order, timestamp, or implementation prevalence.

### 4.9 Conflict handling

A composition conflict exists when two active inputs:

- require and prohibit the same capability;
- assign incompatible component membership;
- define incompatible data-isolation rules;
- define incompatible release channels;
- require mutually exclusive technologies;
- define incompatible hardware envelopes;
- define contradictory authority or failure behavior;
- create a profile dependency cycle.

A conflict is resolved only by an accepted decision and updated canonical contracts.

Without such a resolution, the composition result is `blocked`.

The validator does not apply a generic "stricter wins" rule unless the relevant property explicitly defines an ordering and both contracts authorize that ordering.

### 4.10 Inheritance

Profile inheritance is explicit, machine-readable, directional, and acyclic.

A profile inherits only the fields and claims listed by its inheritance contract.

Primary-profile inheritance is permitted only when:

- the parent relationship is declared;
- the inherited scope is enumerated;
- exclusions and overrides are explicit;
- the resulting profile remains a complete primary profile;
- conformance tests cover inherited and local requirements.

Overlays do not inherit implicitly from other overlays.

A new profile does not inherit from the most similar existing profile by convention.

### 4.11 Global and profile scopes

Global requirements apply to every profile unless an accepted global decision changes them.

A profile may:

- add requirements;
- narrow capabilities;
- require stronger isolation;
- require stronger evidence;
- require a smaller resource envelope;
- require additional lifecycle or recovery behavior.

A profile does not:

- weaken a global constitutional invariant;
- transfer component data ownership;
- authorize direct cross-component writes;
- introduce native AI into the global baseline;
- turn an optional external service into hidden core authority;
- redefine another profile.

### 4.12 Container and topology choices

Container technology is not a standalone deployment profile.

Container use is represented through:

- profile properties;
- component deployment constraints;
- toolchain contracts;
- artifact contracts;
- implementation recipes.

The use of Podman, Quadlet, Docker, systemd, WSL2, virtual machines, or native processes is profile-scoped.

A topology choice does not change logical component identity, authority, data ownership, or contract semantics.

### 4.13 Profile conformance

A profile conformance claim identifies:

- profile ID and version;
- overlay IDs and versions;
- effective profile identity;
- instance identity;
- tested platform and hardware;
- applicable requirements;
- applicable locks;
- applicable tests;
- effective security-control applicability;
- required security-control results and security-evidence records;
- machine-resolvable `not_applicable` justifications;
- active exceptions;
- result;
- issue date;
- validity conditions.

A complete profile claim is valid only when every mandatory requirement and test passes or is covered by an active approved exception.

It also requires current evidence for every security control whose effective applicability is `required`, negative or absence evidence for every `prohibited` control, and a machine-resolvable predicate for every `not_applicable` control. A semantic change to `contracts/security-controls.contract.json` invalidates the affected claim until re-evaluation.

A capability-specific claim may be issued for a bounded capability without claiming complete profile conformance.

A deployment does not inherit conformance from another deployment, image, or host.

### 4.14 Profile lifecycle

Profile lifecycle statuses are:

- `active`;
- `deprecated`;
- `superseded`;
- `retired`.

Only active profiles may support new complete conformance claims.

Deprecation preserves a declared compatibility period.

Supersession names a replacement and migration path.

Retirement preserves the profile identifier and historical evidence.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PRO-MODEL-001,REQ-PRO-MODEL-002,REQ-PRO-MODEL-003,REQ-PRO-MODEL-004,REQ-PRO-MODEL-005,REQ-PRO-MODEL-006,REQ-PRO-MODEL-007,REQ-PRO-MODEL-008,REQ-PRO-MODEL-009,REQ-PRO-MODEL-010,REQ-PRO-MODEL-011,REQ-PRO-MODEL-012,REQ-PRO-MODEL-013,REQ-PRO-MODEL-014,REQ-PRO-MODEL-015,REQ-PRO-MODEL-016,REQ-PRO-MODEL-017,REQ-PRO-MODEL-018,REQ-PRO-MODEL-019,REQ-PRO-MODEL-020 -->
- **REQ-PRO-MODEL-001 — SHALL:** Every active deployment profile and overlay shall have one unique identifier, one active index entry, and one active profile contract.
- **REQ-PRO-MODEL-002 — SHALL:** Every profile instance shall select exactly one primary profile.
- **REQ-PRO-MODEL-003 — MAY:** A profile instance may apply zero or more overlays that explicitly declare compatibility with the selected primary profile and with each other.
- **REQ-PRO-MODEL-004 — SHALL NOT:** An overlay shall not operate as a standalone primary profile.
- **REQ-PRO-MODEL-005 — SHALL:** Profile inheritance, overlay composition, exclusions, and overrides shall be explicit, machine-readable, directional, and acyclic.
- **REQ-PRO-MODEL-006 — SHALL NOT:** A profile-specific requirement shall not become global through repetition, implementation prevalence, packaging, or AI inference.
- **REQ-PRO-MODEL-007 — SHALL NOT:** A profile shall weaken a global constitutional, authority, component-ownership, data-ownership, or fail-closed invariant.
- **REQ-PRO-MODEL-008 — SHALL:** Each profile shall classify applicable capabilities and components as required, optional, conditional, prohibited, not applicable, or external integration only, as appropriate to the object type.
- **REQ-PRO-MODEL-009 — SHALL:** Every conditional capability or component shall declare a machine-evaluable activation condition.
- **REQ-PRO-MODEL-010 — SHALL:** Profile composition shall produce one deterministic effective profile and one composition report.
- **REQ-PRO-MODEL-011 — SHALL:** An unresolved composition conflict shall block activation and conformance claims.
- **REQ-PRO-MODEL-012 — SHALL NOT:** Filename order, declaration order, timestamp, implementation prevalence, or an undeclared "stricter wins" rule shall resolve a profile conflict.
- **REQ-PRO-MODEL-013 — SHALL:** A profile may change physical topology or isolation while preserving logical component identity, responsibility, authority, and data ownership.
- **REQ-PRO-MODEL-014 — SHALL NOT:** Container technology, service-management technology, operating-system packaging, or desktop-shell technology shall constitute an independent deployment profile.
- **REQ-PRO-MODEL-015 — SHALL:** Optional components and external integrations shall be removable without breaking the mandatory baseline of profiles that do not require them.
- **REQ-PRO-MODEL-016 — SHALL:** Every complete profile conformance claim shall identify the effective profile, instance, requirements, locks, tests, evidence, exceptions, and validity conditions.
- **REQ-PRO-MODEL-017 — SHALL NOT:** A deployment shall inherit conformance from another deployment, image, host, or profile instance without its own applicable validation and evidence.
- **REQ-PRO-MODEL-018 — SHALL:** A profile lifecycle change shall preserve identifiers, impact analysis, replacement or removal rationale, migration guidance, and historical evidence.
- **REQ-PRO-MODEL-019 — SHALL:** Profile-specific resource, offline, security, lifecycle, and degradation behavior shall be declared in canonical profile contracts rather than inferred from recipes.
- **REQ-PRO-MODEL-020 — SHALL:** Every effective profile shall remain traceable to accepted decisions, active requirements, active locks, applicable components, tests, evidence, and approved exceptions.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Creating a primary profile

A primary profile is created through this ordered procedure:

1. accept the owner decision defining its deployment purpose;
2. assign a permanent profile identifier;
3. declare the profile class as `primary`;
4. define its mandatory baseline;
5. classify capabilities and components;
6. define resource, data, security, lifecycle, offline, and degradation properties;
7. define artifact, release-channel, and toolchain applicability;
8. define dependencies and incompatibilities;
9. create the canonical profile contract;
10. add the profile to the index;
11. create requirements, locks, tests, and evidence expectations;
12. create explanatory documentation;
13. validate composition and conformance behavior;
14. activate the related objects together.

### 6.2 Creating an overlay

An overlay is created through this sequence:

1. accept the decision defining the cross-cutting property;
2. assign a permanent overlay identifier;
3. declare compatible primary profiles;
4. declare compatible and incompatible overlays;
5. define added or narrowed properties;
6. define prohibited effects;
7. define composition rules;
8. add requirements, tests, and evidence;
9. validate every supported composition;
10. activate the overlay and index entry together.

### 6.3 Composing an effective profile

The composition engine:

1. loads the active global baseline;
2. loads one active primary profile;
3. loads the selected active overlays;
4. validates declared compatibility;
5. resolves explicit inheritance;
6. gathers applicable capabilities and components;
7. applies explicit additions, restrictions, exclusions, and overrides;
8. resolves resource, data, security, lifecycle, offline, and degradation constraints;
9. applies active exceptions;
10. detects conflicts;
11. generates the effective profile;
12. generates the composition report;
13. computes applicable requirements, locks, tests, and evidence;
14. returns `pass` or `blocked`.

A blocked composition cannot be activated.

### 6.4 Creating a profile instance

A profile instance is created by:

1. selecting the primary profile and overlays;
2. assigning an instance identifier;
3. recording platform and hardware facts;
4. generating the effective profile;
5. validating artifact and release compatibility;
6. provisioning component identities and state boundaries;
7. applying resource and security constraints;
8. running profile validation;
9. recording evidence;
10. issuing the applicable claim.

### 6.5 Changing a profile

A semantic profile change:

1. references an accepted decision;
2. classifies the change;
3. updates the canonical profile contract;
4. updates the index when identity or lifecycle changes;
5. computes impact on compositions and instances;
6. updates requirements, locks, tests, evidence, artifacts, toolchains, and documentation;
7. validates all supported compositions;
8. updates conformance guidance;
9. activates the change last.

### 6.6 Applying an exception

A profile exception:

1. identifies the affected profile, overlay, instance, requirement, and property;
2. defines a bounded scope;
3. defines validity conditions;
4. defines compensating controls;
5. defines required evidence;
6. receives approval;
7. is registered;
8. is included in composition and claim results.

An exception does not modify the canonical profile contract.

### 6.7 Deprecating or retiring a profile

Deprecation or retirement requires:

- an accepted decision;
- affected-instance inventory;
- replacement or removal rationale;
- migration path;
- compatibility period where applicable;
- updated composition rules;
- updated artifact and release support;
- updated tests and claims;
- preserved historical identity and evidence.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior |
| --- | --- |
| Primary profile is missing or inactive | Profile composition is blocked. |
| More than one primary profile is selected | Profile composition is blocked. |
| Overlay is incompatible with the primary profile | The overlay is rejected and the requested composition is blocked. |
| Overlay conflict is not explicitly resolved | The effective profile is not produced. |
| Inheritance cycle exists | Activation and composition are blocked. |
| Conditional capability lacks an activation condition | The profile contract fails validation. |
| Required component is unavailable | The affected mandatory profile capability fails closed or the instance loses complete conformance. |
| Optional component is unavailable | Only explicitly dependent optional capabilities become unavailable. |
| Prohibited component is enabled | The instance fails profile conformance. |
| Hardware falls below the declared envelope | Activation is blocked or the instance enters the profile's declared degraded mode. |
| Resource constraint cannot be enforced | Work outside the last verified envelope is denied. |
| Required offline behavior is unavailable | The applicable offline claim fails and affected capabilities follow declared degradation. |
| Required security or trust property is unavailable | The affected action or instance fails closed. |
| Profile contract conflicts with a global invariant | The profile is invalid; the global invariant remains authoritative. |
| Profile exception expires or its condition fails | The exception no longer applies and affected claims are reevaluated. |
| Conformance evidence is missing | The corresponding claim is `blocked` or `fail`, never `pass`. |
| Effective profile cannot be reproduced | Activation and claims are blocked. |

A failed overlay does not silently disappear from a requested conformance claim. The request either uses a validated composition or remains blocked.

## 8. Cross-Component Interactions

### 8.1 Components registry

Profile contracts reference component identifiers from `generated/component-catalog.json`.

A profile controls component membership and deployment constraints. It does not redefine component responsibility or authoritative data ownership.

### 8.2 Resource Governor

Every profile declares a resource envelope and enforcement expectations.

The Resource Governor enforces the effective envelope. It does not decide profile identity, authorization, consent, or disclosure.

### 8.3 Governance Policy Runtime

Profiles that claim sovereign governance or high assurance declare whether the Governance Policy Runtime is required and which policy-controlled capabilities depend on it.

Its absence does not create permission.

### 8.4 Identity and Trust

Profiles declare required identity, credential, trust-root, and verification properties.

The high-assurance overlay may add stronger requirements without changing component ownership.

### 8.5 Data-owning components

Profiles may select shared or separate physical data services.

Logical component ownership, identities, write paths, export, backup, restore, and evidence remain explicit.

### 8.6 Development toolchains

Developer and build profiles reference canonical toolchain contracts.

Toolchain requirements do not apply to user profiles unless explicitly adopted.

The user-lightweight profile does not require GF Wordbench, compilers, development containers, or mutable development environments.

### 8.7 AI and external integrations

The global baseline contains no native AI authority.

Profiles may enable approved optional external integrations only through declared integration contracts.

An external integration does not become a profile solely because it is enabled.

### 8.8 SenTient

SenTient may be optional in developer and build profiles.

It remains prohibited from becoming authoritative, always-running, or required for the local system baseline.

### 8.9 Ariane

Profiles may require Ariane local navigation.

External voice remains a separate optional integration and does not determine profile validity unless a profile explicitly claims that optional capability.

### 8.10 Lifecycle and artifacts

Profiles declare compatible artifact classes, release channels, activation rules, rollback behavior, retention, and offline-bundle expectations.

A profile does not activate an incompatible artifact merely because the artifact is available.

### 8.11 Conformance system

The conformance system evaluates the effective profile, not only the primary profile source file.

It includes overlays, conditions, exceptions, platform facts, component membership, and evidence.

It also resolves the effective security-control set from `contracts/security-controls.contract.json`. Profile-local summaries are projections and cannot replace that contract.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-PROFILE-001` | Defines seven primary profiles and three composable overlays; container technology is not a profile. |
| `DEC-PROFILE-BASELINE-001` | Separates global baseline behavior from deployment-specific behavior. |
| `DEC-DATA-001` | Preserves logical data ownership across profile-dependent physical consolidation or separation. |
| `DEC-GOV-001` | Keeps Resource Governor and Governance Policy Runtime as separate authorities, with profile-specific policy-runtime applicability. |
| `DEC-DEV-001` | Establishes native Linux development and isolated toolchains as a first-class profile concern. |
| `DEC-DEV-002` | Requires parallel applications and branches to remain isolated. |
| `DEC-AI-001` | Keeps native AI outside the global baseline and treats approved AI surfaces as optional integrations. |
| `DEC-SENT-001` | Keeps SenTient optional, isolated, task-activated, and non-authoritative. |

### 9.2 Related ADRs

| ADR | Profile-model effect |
| --- | --- |
| `ADR-015` | Defines isolated development workspaces with UV. |
| `ADR-019` | Separates resource and policy authorities. |
| `ADR-024` | Defines logical ownership with profile-dependent physical isolation. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a deployment can select multiple primary profiles as one effective profile;
- an overlay is a primary profile;
- the most restrictive text automatically wins;
- declaration order establishes precedence;
- a profile inherits from a similarly named profile;
- Linux-specific requirements are global;
- a container runtime defines a profile;
- a desktop shell defines the entire system baseline;
- physical data consolidation merges logical ownership;
- an optional component becomes required because it is installed;
- an unavailable optional service invalidates unrelated core capabilities;
- a recipe creates a profile requirement;
- a profile can weaken a global invariant;
- one instance's evidence proves another instance;
- an artifact's profile label proves deployment conformance;
- a deprecated profile can support an indefinite new claim;
- an absent profile decision may be inferred from implementation.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `03-profiles/00-profile-model.md`;
3. all identifiers and canonical references resolve;
4. all listed decisions are accepted;
5. all requirements exist with identical text and strength;
6. all locks exist and pass;
7. the profile index contains seven active primary profiles and three active overlays;
8. every index entry references one valid profile contract;
9. profile and overlay identifiers are unique;
10. every profile contract validates against `deployment-profile.schema.json`;
11. every instance selects exactly one primary profile;
12. every overlay composition is explicitly compatible;
13. inheritance and composition graphs are acyclic;
14. conditional capabilities have machine-evaluable conditions;
15. every component reference resolves;
16. no profile redefines component responsibility or data ownership;
17. no profile weakens a global invariant;
18. no profile-specific rule appears as a global requirement;
19. effective profiles are deterministic and reproducible;
20. composition conflicts return `blocked`;
21. optional components are removable from profiles that do not require them;
22. profile-specific physical consolidation preserves logical isolation;
23. conformance claims include requirements, locks, tests, evidence, exceptions, and validity conditions;
24. each complete claim passes every mandatory check or identifies an active approved exception;
25. retired identifiers remain reserved;
26. active content is English;
27. no unresolved-authority marker or template token appears.

28. every effective profile resolves one applicability state for every active security control;
29. no profile contract or Markdown table duplicates or overrides the canonical security-control matrix;
30. every required, prohibited, and not-applicable security-control disposition has the validation or predicate required by the security-control contract.

The validator reports actionable failures, including:

`text
profile_missing_index_entry
profile_missing_contract
profile_identifier_collision
profile_primary_count_invalid
profile_overlay_incompatible
profile_overlay_conflict
profile_inheritance_cycle
profile_undeclared_override
profile_condition_missing
profile_component_reference_missing
profile_global_scope_violation
profile_data_ownership_violation
profile_effective_result_not_deterministic
profile_required_component_unavailable
profile_prohibited_component_enabled
profile_claim_missing_evidence
profile_claim_invalid_exception
`

## 11. Non-Normative Examples

### 11.1 Lightweight user instance

An instance selects `user_lightweight` with no overlay.

It runs the required local baseline within its resource envelope. SenTient, GF Wordbench, development containers, and local AI runtimes are absent. Optional external integrations may be enabled without changing the mandatory profile claim.

### 11.2 Sovereign node with offline overlay

An instance selects `sovereign_linux_node` plus `sovereign_offline`.

The effective profile includes the sovereign-node release, identity, privilege, recovery, and evidence requirements plus stronger offline import, local continuity, synchronization, and offline-bundle requirements.

### 11.3 Sovereign node with two overlays

An instance selects `sovereign_linux_node`, `high_assurance`, and `sovereign_offline`.

Composition succeeds only when both overlays declare compatibility with the primary profile and with each other. The conformance claim identifies all three contracts and their effective requirements.

### 11.4 Appliance shell

An instance selects `user_lightweight` plus `appliance_shell`.

The overlay constrains the interaction shell and permitted UI topology. It does not turn Wayland, an embedded browser engine, or the absence of GNOME into global system requirements.

### 11.5 Windows development

An instance selects `developer_windows_wsl`.

It may use Windows 11, WSL2, containers, isolated workspaces, and selected workbenches. It does not claim `sovereign_linux_node` conformance.

### 11.6 Build farm

An instance selects `build_farm`.

It applies reproducible toolchains, controlled dependency resolution, isolated build jobs, test execution, artifact publication, provenance, and evidence requirements. User-interface capabilities are not implied.

### 11.7 Shared database process

A `user_lightweight` instance uses one PostgreSQL process for several components.

Each component retains a separate schema or database, identity, migration path, authoritative write path, backup mapping, and restore mapping. The profile changes physical topology, not logical ownership.

### 11.8 Invalid composition

An overlay requires a capability that the selected primary profile prohibits, and no accepted decision defines a compatible override.

The composition result is `blocked`. The system does not select the later declaration or assume that the overlay wins.

## kOA Spaces Profile Membership

Each profile contract states whether kOA Spaces is optional, unavailable, inherited, or selected as a presentation surface. Membership never makes the subsystem part of the privileged core or a prerequisite for business authority. Security-control applicability remains owned by `contracts/security-controls.contract.json`; kOA Spaces membership only selects presentation behavior and its own operational obligations.
