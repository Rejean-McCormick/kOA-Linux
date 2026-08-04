<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONF-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "conformance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/capability_model",
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
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-CONF-PROFILE-001",
    "DEC-PROFILE-001",
    "DEC-PROFILE-002",
    "DEC-PROFILE-INHERIT-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AI-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONF-CLAIM-001",
    "REQ-CONF-CLAIM-002",
    "REQ-CONF-CLAIM-003",
    "REQ-CONF-CLAIM-004",
    "REQ-CONF-CLAIM-005",
    "REQ-CONF-CLAIM-006",
    "REQ-CONF-CLAIM-007",
    "REQ-CONF-CLAIM-008",
    "REQ-CONF-CLAIM-009",
    "REQ-CONF-CLAIM-010",
    "REQ-CONF-CLAIM-011",
    "REQ-CONF-CLAIM-012",
    "REQ-CONF-CLAIM-013",
    "REQ-CONF-CLAIM-014",
    "REQ-CONF-CLAIM-015",
    "REQ-CONF-CLAIM-016",
    "REQ-CONF-CLAIM-017",
    "REQ-CONF-CLAIM-018",
    "REQ-CONF-CLAIM-019",
    "REQ-CONF-CLAIM-020",
    "REQ-CONF-CLAIM-021",
    "REQ-CONF-CLAIM-022",
    "REQ-CONF-CLAIM-023",
    "REQ-CONF-CLAIM-024",
    "REQ-CONF-CLAIM-025",
    "REQ-CONF-CLAIM-026",
    "REQ-CONF-CLAIM-027",
    "REQ-CONF-CLAIM-028",
    "REQ-CONF-CLAIM-029",
    "REQ-CONF-CLAIM-030",
    "REQ-CONF-CLAIM-031",
    "REQ-CONF-CLAIM-032",
    "REQ-CONF-CLAIM-033",
    "REQ-CONF-CLAIM-034",
    "REQ-CONF-CLAIM-035",
    "REQ-CONF-CLAIM-036",
    "REQ-CONF-CLAIM-037",
    "REQ-CONF-CLAIM-038",
    "REQ-CONF-CLAIM-039",
    "REQ-CONF-CLAIM-040"
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
    "LOCK-LIFE-004",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004"
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
    "DOC-SYS-010",
    "DOC-SYS-011",
    "DOC-SYS-012",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-COMP-000",
    "DOC-COMP-001",
    "DOC-DEV-000",
    "DOC-LIFE-003",
    "DOC-LIFE-013",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-016",
    "DOC-OPS-003",
    "DOC-OPS-013",
    "DOC-CONF-000",
    "DOC-CONF-001",
    "DOC-CONF-002"
  ],
  "tags": [
    "conformance",
    "profile-claims",
    "claim-scope",
    "effective-profile",
    "primary-profile",
    "overlays",
    "release-set",
    "evidence",
    "exceptions",
    "non-claims",
    "validity",
    "revocation"
  ]
}
KOA:DOC-META:END -->

# Profile Claims

## 1. Purpose

This document defines how kOA profile conformance claims are created, evaluated, bounded, maintained, invalidated, and retired.

A profile contract describes required and permitted behavior. A profile claim states that a specific subject, under a specific effective profile composition and Release Set, satisfies a specific bounded set of those obligations at a stated time with attributable evidence.

Conformance is never inferred from appearance or implementation technology. Installing Linux, using Windows WSL, running containers, selecting a profile-named directory, starting services, or passing a partial test does not create a claim.

The model prevents:

- profile names from becoming unverified labels;
- overlay behavior from being inferred;
- development evidence from becoming production evidence;
- one profile's behavior from being claimed by another;
- partial capability evidence from becoming whole-profile conformance;
- stale evidence from supporting current claims;
- exceptions from becoming silent requirement deletion;
- Release Set mixtures from becoming accepted deployments;
- historical failed or revoked claims from being rewritten.

## 2. Scope

This document applies globally to:

- profile-definition claims;
- implementation claims;
- deployment claims;
- operational claims;
- release-compatibility claims;
- bounded-capability claims;
- recovery claims;
- primary profiles;
- profile overlays;
- effective-profile composition;
- requirement applicability;
- test matrices;
- evidence;
- approved exceptions;
- claim issue, renewal, suspension, expiration, revocation, and supersession;
- development, user-lightweight, sovereign, build-farm, and control-plane claims;
- connected, degraded, offline, recovery, and maintenance operating states.

This document does not define the requirements of each profile. The canonical profile contracts own those facts.

It does not create a commercial certification, warranty, service-level agreement, regulatory attestation, or third-party accreditation unless another explicit contract establishes that meaning.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Active profile identities, classes, and relationships | `generated/profile-catalog.json` |
| Primary-profile and overlay facts | `contracts/profiles/*.profile.json` |
| Profile contract structure | `schemas/deployment-profile.schema.json` |
| Profile index structure | `schemas/profile-index.schema.json` |
| Global capability identity | `contracts/system.contract.json#/capability_model` |
| Component identity and behavior | `generated/component-catalog.json` and `contracts/components/*.component.json` |
| Release Set and four-channel compatibility | `contracts/release-channels.contract.json` |
| Artifact identity and lifecycle | `contracts/artifact-classes.contract.json` |
| External integration state | `contracts/integration-types.contract.json` |
| Requirement statements and applicability | `generated/requirements-index.json` |
| Interfile invariants | `generated/assertion-index.json` |
| Requirement, test, evidence, profile, release, and exception links | `generated/traceability.json` |
| Registered tests | `generated/test-catalog.json` |
| Accepted evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

A generated profile matrix, dashboard, report, certificate, badge, or user interface is a projection. It does not own the claim result.

## 4. Claim Model and Effective Profile

### 4.1 Claim artifact

A profile claim contains:

```text
claim_id
claim_version
claim_class
claimant_ref
subject_ref
effective_profile_ref
scope
evaluated_at
valid_from
valid_until
result
requirement_results
test_refs
evidence_refs
exception_refs
non_claims
invalidation_triggers
lifecycle
receipt_refs
```

The claim is immutable after issue except through linked lifecycle records. Renewal creates a new claim version or new claim identity according to the claim contract.

### 4.2 Effective profile composition

The effective profile is:

```text
global baseline
+ exactly one primary profile
+ zero or more explicitly compatible overlays
+ zero or more bounded approved exceptions
```

Global baseline application is not profile inheritance.

Primary profiles are siblings. One primary profile does not derive requirements from another primary profile.

Overlays are non-deployable modifiers. An overlay claim always identifies its primary profile.

### 4.3 Primary profiles

The current primary profile identities are:

```text
user_lightweight
developer_linux_workstation
developer_windows_wsl
sovereign_linux_node
sovereign_hub
build_farm
control_plane
```

A whole-profile claim identifies exactly one of these identities.

### 4.4 Profile overlays

The current overlay identities are:

```text
high_assurance
sovereign_offline
appliance_shell
```

Compatibility is determined by the canonical profile contracts. Similar hardware or observed behavior does not establish compatibility.

### 4.5 Claim classes

| Claim class | Meaning |
| --- | --- |
| `profile_definition` | The profile contract and index are internally valid and closed |
| `implementation` | An implementation satisfies the profile's implementation obligations |
| `deployment` | One deployed subject satisfies installation and active-state obligations |
| `operational` | One deployed subject satisfies current operational obligations |
| `release_compatibility` | A Release Set is valid for the effective profile |
| `bounded_capability` | Named capabilities satisfy a stated subset without whole-profile implication |
| `recovery` | A recovered or replacement subject satisfies the declared recovery endpoint |

Claim class controls required evidence.

### 4.6 Claim scope

Scope includes:

- subject identity;
- authority domain;
- physical or virtual deployment where relevant;
- primary profile;
- overlays;
- Release Set;
- capabilities;
- components;
- interfaces;
- data classes;
- integrations;
- operating states;
- evaluation interval;
- exclusions;
- non-claims.

A claim does not extend beyond these values.

### 4.7 Claim lifecycle

Claim lifecycle states are:

```text
candidate
evaluated
issued
suspended
expired
revoked
superseded
rejected
archived
```

The conformance result remains separate from lifecycle state.

### 4.8 Claim results

Claim results are:

| Result | Meaning |
| --- | --- |
| `conformant` | Every applicable requirement passes |
| `conformant_with_approved_exceptions` | Every non-waived requirement passes and every waiver is current and bounded |
| `nonconformant` | One or more applicable requirements fail |
| `blocked` | Evaluation cannot complete because a required dependency or authority is unavailable |
| `measurement_blocked` | Evidence quality is insufficient for the affected measured obligations |
| `suspended` | Reliance is temporarily prohibited pending reevaluation or remediation |
| `expired` | The validity interval ended |
| `revoked` | Authority withdrew reliance because of trust, safety, false claim, or material invalidation |
| `superseded` | A later claim replaced this claim |

A lifecycle state can require the matching result vocabulary, but the issued artifact preserves both.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONF-CLAIM-001,REQ-CONF-CLAIM-002,REQ-CONF-CLAIM-003,REQ-CONF-CLAIM-004,REQ-CONF-CLAIM-005,REQ-CONF-CLAIM-006,REQ-CONF-CLAIM-007,REQ-CONF-CLAIM-008,REQ-CONF-CLAIM-009,REQ-CONF-CLAIM-010,REQ-CONF-CLAIM-011,REQ-CONF-CLAIM-012,REQ-CONF-CLAIM-013,REQ-CONF-CLAIM-014,REQ-CONF-CLAIM-015,REQ-CONF-CLAIM-016,REQ-CONF-CLAIM-017,REQ-CONF-CLAIM-018,REQ-CONF-CLAIM-019,REQ-CONF-CLAIM-020,REQ-CONF-CLAIM-021,REQ-CONF-CLAIM-022,REQ-CONF-CLAIM-023,REQ-CONF-CLAIM-024,REQ-CONF-CLAIM-025,REQ-CONF-CLAIM-026,REQ-CONF-CLAIM-027,REQ-CONF-CLAIM-028,REQ-CONF-CLAIM-029,REQ-CONF-CLAIM-030,REQ-CONF-CLAIM-031,REQ-CONF-CLAIM-032,REQ-CONF-CLAIM-033,REQ-CONF-CLAIM-034,REQ-CONF-CLAIM-035,REQ-CONF-CLAIM-036,REQ-CONF-CLAIM-037,REQ-CONF-CLAIM-038,REQ-CONF-CLAIM-039,REQ-CONF-CLAIM-040 -->
- **REQ-CONF-CLAIM-001 — SHALL:** Every profile conformance claim be represented by one stable claim identity, one claimant, one governed subject, one effective profile composition, one claim class, one bounded scope, one evaluation time, one result, one validity interval, and one evidence set.
- **REQ-CONF-CLAIM-002 — SHALL NOT:** A profile name, installation choice, host type, operating-system label, repository branch, deployment directory, container stack, or successful startup by itself constitute a conformance claim.
- **REQ-CONF-CLAIM-003 — SHALL:** Every effective profile composition contain the global baseline, exactly one primary profile, zero or more explicitly compatible overlays, and zero or more applicable approved exceptions.
- **REQ-CONF-CLAIM-004 — SHALL NOT:** A primary profile inherit from another primary profile or acquire another profile's requirements through naming, directory placement, implementation similarity, shared components, or historical ancestry.
- **REQ-CONF-CLAIM-005 — SHALL:** Every claimed overlay be listed explicitly, compatible with the selected primary profile, active at evaluation time, and supported by overlay-specific tests and evidence.
- **REQ-CONF-CLAIM-006 — SHALL NOT:** An overlay be claimed independently as a deployable profile or be inferred from observed behavior without an effective-profile record.
- **REQ-CONF-CLAIM-007 — SHALL:** Every claim identify the exact active profile contract versions, profile-index version, authority-registry version, decision set, requirement set, lock set, component-contract set, and Release Set evaluated.
- **REQ-CONF-CLAIM-008 — SHALL:** Every deployment or operational claim identify one complete active Release Set containing exactly one system, services, governance, and knowledge channel version.
- **REQ-CONF-CLAIM-009 — SHALL NOT:** A claim use an unregistered mixture of channel versions, candidate artifacts, mutable tags, local substitutions, or partially activated release state.
- **REQ-CONF-CLAIM-010 — SHALL:** Every claim declare one claim class identified as profile_definition, implementation, deployment, operational, release_compatibility, bounded_capability, or recovery.
- **REQ-CONF-CLAIM-011 — SHALL:** Every claim scope identify the subject, environment, location or authority domain where applicable, capabilities, components, interfaces, data classes, operating states, time interval, and exclusions.
- **REQ-CONF-CLAIM-012 — SHALL NOT:** A bounded capability claim be presented as whole-profile conformance or be used to imply conformance of untested components, profiles, operating states, integrations, or lifecycle behavior.
- **REQ-CONF-CLAIM-013 — SHALL:** Every claim state explicit non-claims for profile classes, overlays, capabilities, environments, authority domains, release authority, security levels, and operating states not covered.
- **REQ-CONF-CLAIM-014 — SHALL:** Every claim evaluate all requirements applicable through the global baseline, primary profile, overlays, components, capabilities, Release Set, integrations, operating states, and approved exceptions.
- **REQ-CONF-CLAIM-015 — SHALL NOT:** A requirement be omitted because its implementation is unavailable, its evidence is inconvenient, its dependency is external, or its result would cause the claim to fail.
- **REQ-CONF-CLAIM-016 — SHALL:** Every evaluated requirement have one disposition identified as pass, fail, not_applicable, blocked, waived_by_approved_exception, or measurement_blocked.
- **REQ-CONF-CLAIM-017 — SHALL:** Every not_applicable disposition cite a canonical applicability rule and the exact claim scope that excludes the requirement.
- **REQ-CONF-CLAIM-018 — SHALL:** Every waived disposition cite one active approved exception whose scope, owner, expiry, compensating controls, tests, and evidence cover the requirement and claimed subject.
- **REQ-CONF-CLAIM-019 — SHALL NOT:** An expired, revoked, superseded, out-of-scope, unapproved, or evidence-incomplete exception support a conformance result.
- **REQ-CONF-CLAIM-020 — SHALL:** A claim result use conformant, conformant_with_approved_exceptions, nonconformant, blocked, measurement_blocked, suspended, expired, revoked, or superseded.
- **REQ-CONF-CLAIM-021 — SHALL:** A conformant result require every applicable requirement to pass and every required test and evidence item to be current, valid, attributable, and complete.
- **REQ-CONF-CLAIM-022 — SHALL:** A conformant_with_approved_exceptions result require all non-waived applicable requirements to pass and every waived requirement to have a current approved exception.
- **REQ-CONF-CLAIM-023 — SHALL NOT:** A failed, blocked, measurement-blocked, missing, stale, incompatible, or untested applicable requirement be counted as passing.
- **REQ-CONF-CLAIM-024 — SHALL:** Every evidence item identify the claim, subject, profile composition, Release Set, source or implementation version, test, requirement, environment, producer, time, result, and integrity or authenticity controls required by its artifact contract.
- **REQ-CONF-CLAIM-025 — SHALL:** Every claim preserve traceability from profile and global requirements through components, tests, evidence, exceptions, incidents, recovery records, and the final result.
- **REQ-CONF-CLAIM-026 — SHALL NOT:** Evidence produced for another profile, overlay composition, Release Set, component version, source revision, environment class, or operating state be reused without an explicit validated equivalence relation.
- **REQ-CONF-CLAIM-027 — SHALL:** Every operational claim include current evidence for active state, service-level objectives, incidents, privileged boundaries, audit durability, backups, disaster recovery, release activation, and applicable offline behavior.
- **REQ-CONF-CLAIM-028 — SHALL:** Every sovereign-offline claim include disconnected cold start, local authority, offline transfer, prolonged disconnection, deferred-operation durability, anti-replay, anti-downgrade, local recovery, and reconnection evidence.
- **REQ-CONF-CLAIM-029 — SHALL NOT:** Connected operation evidence substitute for an offline claim, and offline continuity evidence substitute for connected integration or publication behavior.
- **REQ-CONF-CLAIM-030 — SHALL:** Every development profile claim remain explicitly limited to development authority, candidate artifacts, local tests, and the profile's declared non-production operating model.
- **REQ-CONF-CLAIM-031 — SHALL NOT:** Developer Linux, Windows WSL, workstation ownership, container-backend administration, local administrator access, or successful candidate builds establish production, sovereign, high-assurance, release-signing, publication, or control-plane conformance.
- **REQ-CONF-CLAIM-032 — SHALL:** Every user-lightweight, sovereign-node, sovereign-hub, build-farm, and control-plane claim use the tests, evidence, hardware envelope, security boundary, lifecycle authority, and operational obligations owned by that exact primary profile.
- **REQ-CONF-CLAIM-033 — SHALL:** Every high-assurance claim demonstrate the effective primary profile together with the high_assurance overlay rather than replacing the primary profile identity.
- **REQ-CONF-CLAIM-034 — SHALL:** Every claim involving external integrations or external AI state which integrations were enabled, disabled, unavailable, exercised, or outside scope and preserve the local non-AI authoritative baseline.
- **REQ-CONF-CLAIM-035 — SHALL NOT:** External AI output, provider acknowledgement, external service availability, federation acceptance, or remote control-plane state establish local profile conformance without local validation and acceptance.
- **REQ-CONF-CLAIM-036 — SHALL:** Every claim define invalidation triggers including profile-contract change, Release Set change, component-contract change, requirement change, lock change, exception change, trust or revocation change, material configuration drift, evidence expiry, incident impact, and recovery-state change.
- **REQ-CONF-CLAIM-037 — SHALL:** A triggered invalidation move the claim to suspended, expired, revoked, superseded, blocked, or a newly evaluated result before further reliance.
- **REQ-CONF-CLAIM-038 — SHALL NOT:** A claim be edited in place to conceal historical scope, result, exceptions, evidence gaps, incidents, invalidation, supersession, or revocation.
- **REQ-CONF-CLAIM-039 — SHALL:** Every claim issue, renewal, suspension, revocation, supersession, and expiration create a durable receipt identifying authority, subject, prior state, new state, reason codes, time, evidence, and related claim.
- **REQ-CONF-CLAIM-040 — SHALL:** Profile-claim conformance include effective composition, exact versions, Release Set closure, requirement completeness, evidence attribution, exception validity, explicit non-claims, development limitations, offline separation, invalidation, historical preservation, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Claim Evaluation Procedure

### 6.1 Evaluation inputs

Evaluation resolves:

- active authority registry;
- profile index;
- primary profile;
- overlays;
- exceptions;
- global requirements;
- profile requirements;
- component contracts;
- capability model;
- integrations;
- artifact classes;
- active Release Set;
- active configuration;
- tests;
- evidence;
- incidents;
- recovery state;
- claim scope.

A missing authoritative input blocks issue.

### 6.2 Effective-requirement calculation

The evaluator constructs the requirement set in this order:

1. global baseline requirements;
2. primary-profile requirements;
3. compatible overlay requirements;
4. component requirements for required and active components;
5. capability requirements;
6. Release Set and artifact requirements;
7. integration requirements;
8. operating-state requirements;
9. approved exception effects.

An exception changes disposition only inside its approved scope. It does not remove the requirement from traceability.

### 6.3 Requirement dispositions

Each applicable requirement receives:

```text
pass
fail
not_applicable
blocked
waived_by_approved_exception
measurement_blocked
```

The result records:

- requirement identity;
- applicability source;
- evaluator;
- tests;
- evidence;
- exception where applicable;
- reason codes;
- evaluated time.

### 6.4 Applicability

`not_applicable` requires a canonical rule such as:

- the capability is not part of the profile;
- the integration is explicitly disabled and optional;
- the operating state is outside the claim;
- the artifact class is not selected;
- the overlay is absent;
- the component is prohibited for the profile.

Implementation absence alone does not establish non-applicability.

### 6.5 Test matrix

The test matrix maps:

```text
profile composition
claim class
requirement
test
environment
operating state
expected result
evidence class
validity
```

Whole-profile claims cover every applicable matrix row.

A failed required test produces a failed requirement unless the canonical requirement defines another bounded disposition.

### 6.6 Evidence evaluation

Evidence is accepted only when it is:

- attributable to the subject;
- produced under the claimed profile composition;
- tied to the evaluated Release Set;
- produced by a registered test or authoritative operation;
- current for its validity policy;
- complete for the requirement;
- authentic or integrity-protected where required;
- free from incompatible open-state conditions;
- traceable to the source or implementation version.

Evidence reuse requires validated equivalence.

### 6.7 Exception evaluation

An exception is usable only when:

- status is active;
- scope includes the subject and requirement;
- profile and overlay composition match;
- effective period covers evaluation and claim validity;
- owner and authority resolve;
- compensating controls are active;
- required tests pass;
- required evidence is current;
- exit and revocation conditions are observable.

The claim exposes every relied-upon exception.

### 6.8 Result calculation

The result is deterministic:

| Condition | Result |
| --- | --- |
| All applicable requirements pass | `conformant` |
| All non-waived requirements pass and every waiver is valid | `conformant_with_approved_exceptions` |
| Any applicable requirement fails | `nonconformant` |
| A non-measurement prerequisite blocks completion | `blocked` |
| Required measurement evidence is insufficient | `measurement_blocked` |

Lifecycle events can later move reliance to suspended, expired, revoked, or superseded.

### 6.9 Issue

Issue requires:

- completed evaluation;
- authorized issuer;
- exact scope;
- validity interval;
- explicit non-claims;
- complete Release Set identity;
- result;
- requirement summary;
- evidence summary;
- exception summary;
- invalidation triggers;
- durable issue receipt.

A user-facing summary cannot omit exceptions or non-claims.

## 7. Profile-Specific Claim Boundaries

### 7.1 Development profiles

The development primary profiles are:

```text
developer_linux_workstation
developer_windows_wsl
```

Their claims can cover:

- source and workspace isolation;
- UV and dependency locking;
- development component boundaries;
- candidate artifacts;
- local tests;
- local evidence;
- optional isolated workbenches;
- approved external development surfaces;
- qualified development offline behavior.

Their claims do not imply:

- production release authority;
- production signing;
- sovereign Linux operation;
- high-assurance operation;
- public publication authority;
- control-plane authority;
- production SLO compliance;
- production disaster-recovery compliance.

Windows 11, WSL2, container-backend administration, or developer administrator access remain convenience properties, not broader conformance authority.

### 7.2 User-lightweight profile

A `user_lightweight` claim evaluates its exact:

- hardware envelope;
- activated services;
- resource limits;
- local interaction path;
- optional integration behavior;
- offline behavior;
- upgrade and recovery obligations.

It does not inherit sovereign-node or developer-profile implementation rules.

### 7.3 Sovereign profiles

A `sovereign_linux_node` or `sovereign_hub` claim evaluates:

- local authority;
- identity and trust;
- protected storage;
- privileged broker;
- audit and recourse;
- complete Release Sets;
- backup and recovery;
- component ownership;
- network and integration controls;
- profile-specific hardware and operations.

A hub claim does not automatically apply to every connected node.

### 7.4 Sovereign-offline overlay

A sovereign-offline claim additionally evaluates:

- disconnected cold start;
- prolonged disconnection;
- local time and trust behavior;
- offline identity and policy;
- local audit durability;
- signed transfer bundles;
- quarantine;
- replay and downgrade rejection;
- local Release Set activation;
- local rollback and recovery;
- deferred operation durability;
- duplicate-safe reconnection.

The claim remains the primary sovereign profile plus `sovereign_offline`.

### 7.5 High-assurance overlay

A high-assurance claim identifies:

```text
primary profile + high_assurance
```

The overlay strengthens applicable security, trust, evidence, review, isolation, and lifecycle obligations. It does not replace the primary profile.

### 7.6 Appliance-shell overlay

An appliance-shell claim evaluates its exact user-session, graphical-shell, local navigation, application-launch, update, recovery, and administration restrictions together with its compatible primary profile.

It does not make the shell the system authority.

### 7.7 Build-farm profile

A `build_farm` claim evaluates:

- reproducible workers;
- source and dependency identity;
- artifact provenance;
- isolation;
- signing boundary;
- candidate and production build authority;
- caches;
- SBOM and evidence;
- resource and queue controls;
- release handoff.

It does not imply deployment or operational conformance of produced artifacts.

### 7.8 Control-plane profile

A `control_plane` claim evaluates:

- control authority;
- tenant and scope separation;
- policy and identity dependencies;
- orchestration behavior;
- release and artifact coordination;
- evidence;
- recovery;
- external boundaries.

It does not grant endpoint components general host privilege.

### 7.9 External integrations and AI

A claim identifies enabled and disabled integrations.

External AI remains optional and non-authoritative. The approved external surfaces are:

```text
chatgpt
suno
gamma
approved_ariane_voice_adapter
```

Profile conformance depends on the local non-AI baseline, controlled export and reimport, provenance, and local acceptance. Provider success is not profile success.

## 8. Validity, Invalidation, and Historical Integrity

### 8.1 Validity interval

A claim identifies:

- evaluation time;
- issue time;
- valid-from time;
- valid-until time;
- evidence freshness policy;
- renewal policy.

A claim cannot outlive required evidence, exceptions, trust, profile contract, or Release Set validity.

### 8.2 Invalidation triggers

Triggers include:

- authority-registry change;
- profile-index change;
- primary-profile change;
- overlay compatibility change;
- requirement or lock change;
- component-contract change;
- Release Set activation;
- artifact revocation;
- trust or signer revocation;
- material configuration drift;
- hardware-envelope change;
- integration change;
- evidence expiry;
- failed required test;
- SLO breach with claim impact;
- security incident;
- disaster recovery;
- exception expiry or revocation;
- detected false statement.

The claim contract identifies which triggers require immediate revocation and which require suspension and reevaluation.

### 8.3 Drift

Drift evaluation compares actual state with the claim's bound state:

- subject identity;
- profile composition;
- Release Set;
- configuration;
- component inventory;
- integration state;
- security boundaries;
- resource envelope;
- operating state;
- evidence validity.

Material drift suspends reliance.

### 8.4 Renewal

Renewal repeats the applicable evaluation using current authority and evidence.

Renewal does not simply extend a timestamp.

A renewed claim links to the prior claim and preserves changes in scope, result, evidence, exceptions, and non-claims.

### 8.5 Suspension

Suspension records:

- trigger;
- affected scope;
- decision authority;
- effective time;
- permitted operation during suspension;
- remediation;
- reevaluation requirements;
- receipt.

Suspension is not conformance.

### 8.6 Revocation

Revocation applies to false, unsafe, compromised, materially invalid, or prohibited claims.

The revocation record identifies:

- claim;
- authority;
- reason;
- affected reliance;
- effective time;
- required notices;
- remediation or replacement path;
- evidence.

### 8.7 Supersession

Supersession links the prior claim to the replacement claim.

The prior artifact remains available for historical interpretation and cannot be presented as current.

### 8.8 Public and restricted evidence

A public claim summary can disclose:

- claim identity;
- subject class;
- effective profile;
- claim class;
- result;
- validity;
- Release Set;
- exception presence;
- verification state;
- recourse reference.

Detailed tests, configuration, identities, incidents, security evidence, and protected exceptions remain in governed evidence classes.

## 9. Failure Modes and Safe Claiming

| Failure | Required treatment |
| --- | --- |
| Profile contract missing or invalid | Block evaluation. |
| Effective composition ambiguous | Block evaluation. |
| More than one primary profile selected | Reject composition. |
| Overlay compatibility absent | Reject the overlay claim. |
| Release Set incomplete or incompatible | Fail or block the affected deployment claim. |
| Requirement applicability unknown | Block issue until canonical applicability resolves. |
| Required test absent | Fail or block according to the requirement contract. |
| Evidence stale or incompatible | Fail, block, or mark measurement blocked. |
| Exception expired or out of scope | Treat the requirement as unwaived. |
| Configuration drift detected | Suspend reliance and reevaluate. |
| Security incident affects claim basis | Suspend or revoke according to impact. |
| Evidence store unavailable | Preserve current status and block new issue or renewal requiring that evidence. |
| External provider unavailable | Apply the profile's local behavior; do not invent conformance. |
| Offline evidence unavailable | Fail or block the offline claim. |
| Claim receipt storage unavailable | Block final issue, renewal, revocation, or supersession. |
| False or misleading summary detected | Correct, revoke, or supersede and preserve the original record. |
| Evaluation tool incompatible | Preserve the last valid claim state and block new evaluation. |

A failure cannot expand the claim scope.

## 10. Exceptions and Validation

### 10.1 Exceptions

A bounded exception can adjust:

- one requirement disposition;
- one evidence source;
- one test environment;
- one validity interval;
- one profile-specific implementation;
- one compatibility interval;
- one temporary operational restriction.

An exception cannot:

- add a second primary profile;
- make an overlay independently deployable;
- create implicit inheritance;
- activate an incomplete Release Set;
- convert failed or missing evidence into pass;
- claim production from a development profile;
- remove explicit non-claims;
- hide reliance on the exception;
- remove invalidation triggers;
- rewrite claim history;
- support reliance after expiry or revocation.

### 10.2 Validation criteria

This document is conformant when validation confirms:

1. every claim has stable identity, claimant, subject, class, scope, result, and validity;
2. effective composition contains the baseline, exactly one primary profile, explicit compatible overlays, and bounded exceptions;
3. primary profiles remain siblings;
4. overlays are never independent claims;
5. exact profile, authority, decision, requirement, lock, component, and Release Set versions resolve;
6. deployment and operational claims identify complete four-channel Release Sets;
7. claim class and scope are explicit;
8. non-claims are complete and visible;
9. the applicable requirement set is complete;
10. every requirement has one canonical disposition;
11. not-applicable results cite applicability authority;
12. waivers cite current approved exceptions;
13. result calculation is deterministic;
14. every passing result has current attributable tests and evidence;
15. evidence reuse has validated equivalence;
16. operational claims include SLO, incident, security, audit, backup, recovery, activation, and offline evidence where applicable;
17. sovereign-offline claims have disconnected and reconnection evidence;
18. connected and offline evidence remain separate;
19. development claims exclude production and sovereign authority;
20. high-assurance and other overlays preserve primary-profile identity;
21. external integrations and AI remain locally validated and non-authoritative;
22. invalidation triggers are complete;
23. drift, incidents, evidence expiry, trust change, and Release Set change cause appropriate lifecycle action;
24. issue, renewal, suspension, revocation, supersession, and expiration have durable receipts;
25. public summaries preserve minimum disclosure while exposing result, scope, validity, exceptions, and recourse;
26. historical claims remain immutable and interpretable;
27. all profiles, overlays, requirements, components, Release Sets, integrations, tests, evidence, incidents, exceptions, and receipts resolve;
28. no prohibited open-state marker enters active conformance authority.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_profile_claims.py
tools/check_profile_inheritance.py
tools/check_release_sets.py
tools/check_component_boundaries.py
tools/check_interfile_locks.py
tools/check_traceability.py
tools/check_artifact_contracts.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
```

A failed profile-claim check blocks issue, renewal, continued reliance, public verification, or the affected conformance assertion.

## 11. Non-Normative Examples

### 11.1 Development claim

A Windows WSL workspace claims `implementation` conformance to `developer_windows_wsl` for source isolation, UV, local tests, candidate artifacts, and optional external AI boundaries. Its non-claims exclude production release, sovereign operation, and high assurance.

### 11.2 Sovereign-offline deployment

A node claims `deployment` conformance to `sovereign_linux_node + sovereign_offline`. The claim identifies its complete Release Set and evidence for disconnected cold start, signed offline update, rollback, audit durability, and reconnection.

### 11.3 Bounded capability claim

A recovery environment proves only backup restoration and complete Release Set activation. The claim class is `bounded_capability`; it does not assert whole-profile operational conformance.

### 11.4 High-assurance overlay

A sovereign hub claims `sovereign_hub + high_assurance`. The claim evaluates both the primary profile and the overlay requirements and does not rename the effective profile to only `high_assurance`.

### 11.5 Exception

One storage control uses an approved temporary exception with compensating monitoring and a current test. The result is `conformant_with_approved_exceptions`, and the exception is visible in the claim.

### 11.6 Stale evidence

A required disaster-recovery exercise expires. The operational claim becomes suspended until a new exercise passes and a renewed claim is issued.

### 11.7 Release activation

A new Release Set becomes active. The prior deployment claim is suspended or superseded because its bound channel versions no longer describe the node.

### 11.8 Integration disabled

An optional external integration is disabled by profile configuration. Its availability test is not applicable under the canonical rule, while local core behavior remains fully evaluated.

### 11.9 Security incident

A trust compromise affects the claim basis. The claim is revoked, the subject is isolated, and a replacement claim requires new identity, trust, recovery, and operational evidence.

### 11.10 Public summary

A public verification record shows the claim identity, effective profile, result, validity, Release Set, exception presence, and recourse path. Restricted configuration and security evidence remain private.
