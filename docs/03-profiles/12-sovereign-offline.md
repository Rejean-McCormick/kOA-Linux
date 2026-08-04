<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "profile",
  "scope": [
    "profile_overlay"
  ],
  "profile_id": "sovereign_offline",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "schemas/deployment-profile.schema.json",
    "contracts/integration-types.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-SOFF-001",
    "DEC-PROFILE-INHERIT-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AI-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-INT-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-SOFF-001",
    "REQ-PROFILE-SOFF-002",
    "REQ-PROFILE-SOFF-003",
    "REQ-PROFILE-SOFF-004",
    "REQ-PROFILE-SOFF-005",
    "REQ-PROFILE-SOFF-006",
    "REQ-PROFILE-SOFF-007",
    "REQ-PROFILE-SOFF-008",
    "REQ-PROFILE-SOFF-009",
    "REQ-PROFILE-SOFF-010",
    "REQ-PROFILE-SOFF-011",
    "REQ-PROFILE-SOFF-012",
    "REQ-PROFILE-SOFF-013",
    "REQ-PROFILE-SOFF-014",
    "REQ-PROFILE-SOFF-015",
    "REQ-PROFILE-SOFF-016",
    "REQ-PROFILE-SOFF-017",
    "REQ-PROFILE-SOFF-018",
    "REQ-PROFILE-SOFF-019",
    "REQ-PROFILE-SOFF-020",
    "REQ-PROFILE-SOFF-021",
    "REQ-PROFILE-SOFF-022",
    "REQ-PROFILE-SOFF-023",
    "REQ-PROFILE-SOFF-024",
    "REQ-PROFILE-SOFF-025",
    "REQ-PROFILE-SOFF-026",
    "REQ-PROFILE-SOFF-027",
    "REQ-PROFILE-SOFF-028",
    "REQ-PROFILE-SOFF-029",
    "REQ-PROFILE-SOFF-030",
    "REQ-PROFILE-SOFF-031",
    "REQ-PROFILE-SOFF-032"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-SENT-001"
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
    "DOC-PROFILE-002"
  ],
  "tags": [
    "sovereign-offline",
    "profile-overlay",
    "offline-continuity",
    "disconnected-operation",
    "offline-transfer",
    "signed-bundles",
    "anti-rollback",
    "local-authority",
    "local-trust",
    "recovery",
    "release-sets",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Sovereign Offline

## 1. Purpose

This document defines the `sovereign_offline` profile overlay.

The overlay strengthens a compatible sovereign primary profile so that its declared local core can operate, recover, update, and produce conformance evidence without depending on Internet access, a remote control plane, an external identity provider, an external policy service, an external artifact service, or an external AI provider.

Sovereign offline operation is more than temporary network loss. It is an intentionally governed operating condition with:

- complete local authority for the declared capability envelope;
- local trust, identity, policy, audit, time, and recovery material;
- explicit network denial or restriction;
- signed and validated offline-transfer artifacts;
- replay, downgrade, and duplicate-activation protection;
- atomic local release activation;
- locally available rollback and restore paths;
- measured resource and storage resilience;
- tested operation over the declared disconnected interval.

The overlay does not make every external capability local. It makes every unavailable external dependency explicit and preserves the local capabilities that the effective profile claims.

## 2. Scope

This document applies to the `sovereign_offline` overlay and every effective profile that composes it with an explicitly compatible primary profile.

It governs:

- disconnected boot and steady-state operation;
- local identity, trust, authorization, and policy evaluation;
- local authoritative data;
- local audit and recourse intake;
- network interfaces, routes, peers, and services;
- offline import and export;
- release, policy, configuration, trust, and revocation updates;
- signed bundles and manifests;
- local activation, rollback, and forward repair;
- backup, restore, portability, exit, and replacement-node recovery;
- time and freshness handling;
- resource, storage, power, and queue pressure;
- Ariane, UCKK, external AI, and optional integrations;
- sovereign-offline conformance claims and evidence.

The overlay is not independently deployable. It does not define the primary profile's hardware identity, component inventory, business purpose, or complete capability set. Those facts remain owned by the compatible primary profile.

The overlay does not guarantee indefinite operation under unlimited hardware failure, depleted storage, absent power, expired trust, or unavailable repair artifacts. The effective profile declares the tested disconnected interval and resource assumptions.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Overlay identity, compatibility, and profile-specific facts | `contracts/profiles/sovereign-offline.profile.json` |
| Active profile inventory and relationships | `generated/profile-catalog.json` |
| Profile and overlay schema | `schemas/deployment-profile.schema.json` |
| Global offline-continuity model | `contracts/system.contract.json#/offline_continuity` |
| Global capability model | `contracts/system.contract.json#/capability_model` |
| Component identity and authoritative ownership | `generated/component-catalog.json` |
| Integration and offline-transfer boundaries | `contracts/integration-types.contract.json` |
| Release-channel compatibility and Release Sets | `contracts/release-channels.contract.json` |
| Transfer, release, evidence, and recovery artifact classes | `contracts/artifact-classes.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file sovereign-offline invariants | `generated/assertion-index.json` |
| Profile, capability, release, test, and evidence links | `generated/traceability.json` |
| Sovereign-offline conformance tests | `generated/test-catalog.json` |
| Sovereign-offline evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted architectural decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

This document explains the overlay. The profile contract owns compatibility, hardware and resource values, disconnected interval, network policy, permitted transfer classes, tests, and evidence.

## 4. Profile Model

### 4.1 Overlay identity

`sovereign_offline` is a profile overlay.

It:

- has no independent deployment identity;
- composes with one compatible primary profile;
- can compose with another compatible overlay only when every relationship is explicit;
- strengthens offline, network, trust, update, recovery, and evidence controls;
- does not replace the primary profile's component or capability ownership;
- produces one effective profile contract after validated composition.

A primary profile that does not list this overlay as compatible cannot claim sovereign-offline conformance.

### 4.2 Effective-profile composition

The effective profile is calculated as:

```text
active global baseline
+ one compatible sovereign primary profile
+ sovereign_offline
+ zero or more compatible overlays
+ applicable active exceptions
= one validated sovereign-offline effective profile
```

Composition preserves the authority order. The overlay cannot weaken the global baseline or the primary profile's required local capabilities.

An effective profile records every contributing object and version.

### 4.3 Operating states

The sovereign-offline operating model uses explicit states:

```text
connected_restricted
preparing_disconnection
disconnected
offline_transfer_import
offline_transfer_export
reconnection_assessment
recovery
```

`connected_restricted` permits only network paths declared by the effective profile.

`preparing_disconnection` verifies local authority, trust, time, release, recovery, storage, and evidence readiness.

`disconnected` contains no undeclared external dependency.

`offline_transfer_import` and `offline_transfer_export` are controlled boundary states, not general network availability.

`reconnection_assessment` evaluates newly available paths without enabling them automatically.

`recovery` restores a known compatible local authority state from locally controlled artifacts.

### 4.4 Capability envelope

The primary profile owns the capability inventory. This overlay strengthens the behavior of capabilities under complete external network denial.

The effective capability envelope distinguishes:

| Category | Meaning |
| --- | --- |
| `required_continuous` | Full local behavior remains available throughout the tested disconnected interval |
| `required_degraded` | A defined safe local subset remains available |
| `deferred_external` | A local request can be preserved for later governed transfer |
| `unavailable_external` | The external capability is disabled without false completion |
| `offline_transfer` | A signed and validated bundle replaces a live external path |
| `prohibited` | The capability conflicts with sovereign-offline authority or risk controls |

Every category is machine-readable in the effective profile.

### 4.5 Local authority services

The effective profile provides locally controlled material for:

- node and service identity;
- user authentication appropriate to the primary profile;
- authorization and policy evaluation;
- trust-root and signature verification;
- artifact and release compatibility;
- consent and cultural-rights decisions where applicable;
- audit capture;
- recourse intake;
- local configuration;
- resource governance;
- backup, restore, and recovery;
- time and freshness evaluation within the declared policy.

Local availability does not imply unlimited cached authority. Expiry, revocation, and freshness-sensitive actions retain their fail-closed conditions.

### 4.6 Network model

External connectivity defaults to absent or explicitly restricted.

The effective profile declares:

- physical and virtual interfaces;
- enabled and disabled states;
- local segments;
- permitted peers;
- inbound and outbound protocols;
- routes and gateways;
- name-resolution sources;
- proxy behavior;
- time sources;
- update paths;
- transfer devices;
- monitoring boundaries;
- administrative access paths.

An enabled interface does not imply Internet permission.

Local network capability can remain available for explicitly trusted local peers, devices, or operator stations. Every path remains purpose- and scope-bound.

### 4.7 Offline-transfer model

Offline transfer uses governed artifacts.

A transfer bundle can contain:

- release artifacts;
- policy bundles;
- trust and revocation updates;
- configuration;
- data imports;
- controlled exports;
- evidence;
- backup or restore material;
- portability packages;
- migration material.

A bundle does not inherit authority from its transport medium. The target validates the bundle and each contained artifact before acceptance.

### 4.8 Release and update model

The effective profile consumes compatible versions of the four release channels:

```text
system
services
governance
knowledge
```

A Release Set identifies one tested version per channel. Offline distribution preserves the Release Set identity, manifests, compatibility evidence, signatures, and rollback information.

Activation is atomic. The authority index activates after dependent objects pass validation.

Partial active authority is not a sovereign-offline update state.

### 4.9 Trust and time model

Disconnected authority depends on locally verifiable trust and bounded freshness.

The effective profile declares:

- trusted roots;
- signing identities;
- revocation material;
- validity intervals;
- trusted time sources;
- maximum tolerated clock uncertainty;
- offline freshness intervals;
- actions permitted under degraded time;
- actions blocked without current freshness;
- update and recovery procedures.

A local clock is not automatically trusted merely because the node is offline.

### 4.10 Audit, recourse, and evidence

Critical events remain locally durable.

The effective profile stores:

- authority decisions;
- privileged transitions;
- import and export receipts;
- release activation and rollback receipts;
- trust and time updates;
- audit access events;
- recourse cases and remedies;
- failure and recovery evidence.

Later export uses controlled transfer and duplicate-safe reconciliation.

No remote destination is required for local event durability.

### 4.11 Resource and longevity model

The profile contract defines the tested disconnected interval and resource assumptions.

The Resource Governor protects:

- interactive local core;
- identity and policy services;
- authoritative storage;
- audit durability;
- transfer validation;
- recovery artifacts;
- essential indexing and retrieval;
- reserve storage and memory.

Optional processing, background indexing, retained caches, and non-essential work yield before the local core.

The Governance Policy Runtime remains separate and does not become a resource scheduler.

### 4.12 Ariane, UCKK, external AI, and SenTient

Ariane local non-voice navigation remains available offline.

Native UCKK ingestion, validation, routing, local indexing, retrieval, and dimension transfer remain deterministic and local within the effective resource envelope.

ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain external surfaces. They are unavailable during complete disconnection unless a future accepted decision and registered controlled transfer mechanism explicitly supports a bounded operation. Their absence does not alter the native baseline.

The overlay does not add SenTient or any AI runtime. SenTient remains limited to eligible development or build profiles and remains optional, isolated, and non-authoritative.

### 4.13 Recovery and replacement

A conformant effective profile retains locally controlled recovery material sufficient to:

- restore authoritative data;
- restore active release and policy state;
- verify trust and artifacts;
- reconstruct configuration;
- recover audit and recourse state;
- resume pending offline operations safely;
- replace failed storage or a failed node;
- export data and evidence for exit.

Recovery does not depend on a central service being reachable.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-SOFF-001,REQ-PROFILE-SOFF-002,REQ-PROFILE-SOFF-003,REQ-PROFILE-SOFF-004,REQ-PROFILE-SOFF-005,REQ-PROFILE-SOFF-006,REQ-PROFILE-SOFF-007,REQ-PROFILE-SOFF-008,REQ-PROFILE-SOFF-009,REQ-PROFILE-SOFF-010,REQ-PROFILE-SOFF-011,REQ-PROFILE-SOFF-012,REQ-PROFILE-SOFF-013,REQ-PROFILE-SOFF-014,REQ-PROFILE-SOFF-015,REQ-PROFILE-SOFF-016,REQ-PROFILE-SOFF-017,REQ-PROFILE-SOFF-018,REQ-PROFILE-SOFF-019,REQ-PROFILE-SOFF-020,REQ-PROFILE-SOFF-021,REQ-PROFILE-SOFF-022,REQ-PROFILE-SOFF-023,REQ-PROFILE-SOFF-024,REQ-PROFILE-SOFF-025,REQ-PROFILE-SOFF-026,REQ-PROFILE-SOFF-027,REQ-PROFILE-SOFF-028,REQ-PROFILE-SOFF-029,REQ-PROFILE-SOFF-030,REQ-PROFILE-SOFF-031,REQ-PROFILE-SOFF-032 -->
- **REQ-PROFILE-SOFF-001 — SHALL:** The sovereign_offline profile be represented as a non-deployable overlay that composes only with primary profiles explicitly listed as compatible in the canonical profile contracts.
- **REQ-PROFILE-SOFF-002 — SHALL NOT:** The sovereign_offline overlay be activated, claimed, or distributed as an independent primary deployment profile.
- **REQ-PROFILE-SOFF-003 — SHALL:** The effective profile preserve complete local operation of every capability classified as required and continuous by the compatible primary profile and this overlay.
- **REQ-PROFILE-SOFF-004 — SHALL NOT:** Profile boot, local authentication, local authorization, policy evaluation, local navigation, local authoritative data access, audit capture, recovery, or shutdown depend on Internet access or a remote control plane.
- **REQ-PROFILE-SOFF-005 — SHALL:** The effective profile maintain local identity, trust, policy, authorization, audit, time, configuration, and recovery material sufficient for its declared disconnected operating interval.
- **REQ-PROFILE-SOFF-006 — SHALL:** Every capability in the effective profile declare continuous, degraded, deferred, unavailable, or offline-transfer behavior under complete external network denial.
- **REQ-PROFILE-SOFF-007 — SHALL NOT:** Loss of an external network, provider, federation peer, directory, package source, artifact service, or external AI surface cause unrelated local core capabilities to fail.
- **REQ-PROFILE-SOFF-008 — SHALL:** External network interfaces and routes default to disabled or explicitly restricted according to the effective profile's registered network policy.
- **REQ-PROFILE-SOFF-009 — SHALL NOT:** Automatic discovery, fallback routing, captive-portal behavior, implicit proxy use, or operating-system service defaults create undeclared external connectivity.
- **REQ-PROFILE-SOFF-010 — SHALL:** Every permitted local network segment, peer, protocol, direction, address source, trust boundary, and purpose be explicitly declared and validated.
- **REQ-PROFILE-SOFF-011 — SHALL:** All cross-boundary imports and exports use controlled offline-transfer artifacts or another explicitly registered integration path compatible with sovereign_offline.
- **REQ-PROFILE-SOFF-012 — SHALL:** Every offline-transfer bundle carry a manifest, stable identity, source, destination scope, artifact classes, versions, provenance, creation time, expiry where applicable, integrity records, and signature verification material.
- **REQ-PROFILE-SOFF-013 — SHALL:** Every inbound bundle be quarantined and validated for source identity, trust, signature, integrity, compatibility, policy, consent, cultural rights, duplicate status, and target ownership before authoritative acceptance or activation.
- **REQ-PROFILE-SOFF-014 — SHALL:** Every outbound bundle be minimized, destination-bound, purpose-bound, policy-authorized, provenance-preserving, and recorded with a transfer receipt.
- **REQ-PROFILE-SOFF-015 — SHALL NOT:** Physical possession of removable media, a transfer bundle, an archive, or a signed object by itself authorize import, disclosure, publication, activation, or execution.
- **REQ-PROFILE-SOFF-016 — SHALL:** Release and policy updates enter through signed, versioned, compatibility-tested artifacts and activate atomically through the applicable release and lifecycle controls.
- **REQ-PROFILE-SOFF-017 — SHALL:** The effective profile detect and block replay, downgrade, rollback below an allowed floor, duplicate activation, and activation of revoked or incompatible artifacts.
- **REQ-PROFILE-SOFF-018 — SHALL:** Rollback and forward-repair artifacts required for the active release remain locally retrievable and verifiable without an external service.
- **REQ-PROFILE-SOFF-019 — SHALL:** The effective profile maintain a bounded, auditable method for introducing trust-root, revocation, policy, and time-authority updates while disconnected.
- **REQ-PROFILE-SOFF-020 — SHALL:** Expiry-sensitive, authorization-sensitive, or replay-sensitive operations fail closed when trusted time or freshness cannot be established within the active offline policy.
- **REQ-PROFILE-SOFF-021 — SHALL:** Critical audit events and recourse intake remain locally durable during disconnected operation and preserve later export without duplicate effects.
- **REQ-PROFILE-SOFF-022 — SHALL NOT:** Absence of a central audit destination, remote approver, remote policy service, or external evidence store be represented as successful delivery or approval.
- **REQ-PROFILE-SOFF-023 — SHALL:** The Resource Governor protect the local core under storage, memory, CPU, power, thermal, and queue pressure using the effective profile's conservative resource envelope.
- **REQ-PROFILE-SOFF-024 — SHALL NOT:** The Resource Governor decide authorization, consent, disclosure, publication, privilege, or governance policy while enforcing offline resource limits.
- **REQ-PROFILE-SOFF-025 — SHALL:** The native capability baseline remain non-AI, and ChatGPT, Suno, Gamma, and the approved Ariane voice adapter remain unavailable while no explicitly authorized external transfer path exists.
- **REQ-PROFILE-SOFF-026 — SHALL:** Ariane local non-voice navigation remain continuously available without Internet access, external AI, or the approved external voice adapter.
- **REQ-PROFILE-SOFF-027 — SHALL:** Native UCKK ingestion, validation, routing, local indexing, retrieval, and UCKK dimension transfer remain deterministic and locally operable within the effective profile's declared resource envelope.
- **REQ-PROFILE-SOFF-028 — SHALL NOT:** The Publication Gateway and the UCKK Dimension Gateway be merged or substituted for one another in offline-transfer workflows.
- **REQ-PROFILE-SOFF-029 — SHALL NOT:** The sovereign_offline overlay add SenTient, a local AI runtime, an external AI dependency, or an undeclared developer workbench to an otherwise ineligible primary profile.
- **REQ-PROFILE-SOFF-030 — SHALL:** Backup, restore, disaster recovery, portability, exit, and replacement-node procedures remain executable from locally controlled artifacts and documented offline procedures.
- **REQ-PROFILE-SOFF-031 — SHALL:** An effective sovereign_offline conformance claim identify the primary profile, all overlays, active exceptions, release set, trust state, offline interval assumptions, network policy, transfer controls, tests, and current evidence.
- **REQ-PROFILE-SOFF-032 — SHALL:** Sovereign-offline conformance include tested cold boot without external networks, prolonged disconnection, local authority evaluation, local restart, power loss, storage pressure, trusted-time degradation, signed bundle import and export, replay and downgrade rejection, atomic update, rollback, restore, and optional-integration absence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures and State Transitions

### 6.1 Preparing for disconnection

Preparation proceeds through:

1. identify the effective profile and release set;
2. verify all required local components;
3. verify local identity, trust, policy, and authorization material;
4. verify trusted time and freshness assumptions;
5. verify required authoritative data;
6. verify storage, power, and resource reserves;
7. verify local audit and recourse durability;
8. verify backup, restore, rollback, and repair artifacts;
9. close or classify pending external operations;
10. disable undeclared external routes and services;
11. execute the disconnection-readiness tests;
12. record a readiness receipt.

A failed readiness check blocks an unqualified sovereign-offline claim.

### 6.2 Entering disconnected operation

The transition to `disconnected`:

1. records the network-policy state;
2. disables non-permitted interfaces, routes, proxies, and discovery;
3. verifies that no required capability depends on an external service;
4. recalculates every capability's availability state;
5. starts local-only monitoring and audit;
6. preserves pending external operations explicitly;
7. activates the conservative resource envelope;
8. records the effective trust, time, release, and recovery state.

Disconnected operation is a normal governed state, not break-glass authority.

### 6.3 Importing an offline bundle

Import proceeds through:

```text
media_received
device_or_medium_identified
bundle_quarantined
manifest_parsed
source_authenticated
signature_verified
integrity_verified
freshness_checked
replay_and_downgrade_checked
artifact_classes_validated
compatibility_validated
policy_and_rights_checked
target_owners_resolved
owner_acceptance_recorded
staged
activated_or_imported
receipt_recorded
```

Failure at any validation stage preserves the current active state.

### 6.4 Exporting an offline bundle

Export proceeds through:

1. identify the destination and purpose;
2. select data and artifacts through owning components;
3. evaluate policy, consent, cultural rights, and disclosure;
4. minimize the payload;
5. attach provenance and compatibility information;
6. create a destination-bound manifest;
7. sign and protect the bundle;
8. record the export receipt;
9. transfer through the registered medium or device;
10. preserve local completion state separately from destination acceptance.

Creation of an export bundle does not prove that the destination accepted it.

### 6.5 Applying a release or policy update

Update proceeds through:

1. import the signed Release Set or governed policy bundle;
2. verify trust, signature, integrity, freshness, compatibility, and anti-rollback rules;
3. stage all required channel and policy objects;
4. execute pre-activation tests;
5. verify rollback and forward-repair material;
6. activate dependent objects atomically;
7. activate the authority index last;
8. execute post-activation tests;
9. record activation evidence;
10. retain the prior valid state according to rollback policy.

An incomplete Release Set remains inactive.

### 6.6 Updating trust, revocation, or time material

A trust or freshness update:

1. identifies the currently active authority;
2. verifies the update's signer and authorization;
3. checks sequence, validity, replay, and rollback constraints;
4. stages the new material;
5. validates affected identities, artifacts, and policies;
6. activates the update atomically;
7. records the transition;
8. retains required recovery evidence.

A stale or unverifiable update is rejected.

### 6.7 Recovering after interruption

Recovery after power loss, process failure, or node restart:

1. verifies local storage and journal integrity;
2. restores committed authoritative state;
3. verifies the active authority and release set;
4. restores pending transfer and deferred-operation state;
5. evaluates time and freshness;
6. restores audit and recourse durability;
7. applies the conservative resource envelope;
8. recalculates capability availability;
9. quarantines ambiguous or corrupted records;
10. records recovery evidence.

The system does not replay an operation whose prior outcome is unknown until duplicate effects are excluded.

### 6.8 Reconnecting a sovereign-offline node

Reconnection begins in `reconnection_assessment`.

The system:

1. keeps external routes disabled by default;
2. identifies the proposed network and peers;
3. verifies identity, trust, policy, time, and compatibility;
4. compares local and remote release, revocation, and authority states;
5. classifies pending imports, exports, and deferred operations;
6. detects conflicts and prior remote effects;
7. enables only explicitly approved paths;
8. reconciles through owning components;
9. records every boundary transition.

Physical connectivity does not automatically exit sovereign-offline authority.

## 7. Failure Modes and Safe Degradation

| Failure | Required behavior |
| --- | --- |
| Internet or upstream network unavailable | Continue the declared local core without changing conformance state solely because the expected condition persists. |
| Local network interface fails | Preserve node-local capabilities and mark dependent local-peer capabilities unavailable or degraded. |
| Name resolution unavailable | Use only registered local resolution paths; do not fall back to public resolvers. |
| Trusted time uncertainty exceeds policy | Block expiry-sensitive and replay-sensitive actions while preserving safe local capabilities. |
| Trust or revocation material expires | Block affected verification or activation paths; preserve the last valid authoritative state. |
| Transfer signature invalid | Quarantine and reject the bundle. |
| Transfer manifest incomplete | Reject before artifact acceptance. |
| Replay or downgrade detected | Reject and record security evidence. |
| Release channels incompatible | Block activation and retain the current Release Set. |
| Partial update staged | Keep all staged objects inactive. |
| Rollback artifact unavailable | Block the update unless an accepted forward-repair policy explicitly satisfies the active lifecycle contract. |
| Removable medium fails | Preserve local authoritative state and record an incomplete transfer. |
| Audit export unavailable | Continue local durable audit capture. |
| Storage pressure | Protect authoritative state, audit, trust, and recovery reserves before caches and optional work. |
| Power loss | Recover committed state and explicit pending state from local durable records. |
| External AI unavailable | Preserve all native capability claims. |
| Ariane voice unavailable | Preserve local non-voice navigation. |
| External UCKK adapter unavailable | Preserve deterministic native UCKK behavior. |
| Corrupted recovery artifact | Quarantine it and retain the last verified recoverable state. |
| Profile or authority contract invalid | Block new activation and claims while preserving the last validated local state. |

Safe degradation never creates broader authority, silent data loss, undeclared connectivity, or false completion.

## 8. Security, Trust, and Data Boundaries

Sovereign-offline security begins with local control, but local possession is not sufficient authority.

The effective profile enforces:

- locally controlled identities and trust roots;
- explicit privileged-operation paths;
- managed secret references;
- protected signing and verification keys;
- purpose-bound network paths;
- media and device controls;
- transfer quarantine;
- signed manifests;
- artifact integrity and compatibility checks;
- replay and downgrade protection;
- component-owned authoritative data;
- no direct cross-component writes;
- public and restricted audit separation;
- consent and cultural-rights evaluation;
- local recourse;
- bounded retention;
- tested backup, restore, and exit.

Transfer devices and removable media remain outside local authority until validated. A trusted device can carry an untrusted bundle, and a trusted bundle can target an unauthorized operation.

External AI is not a local trust authority. External AI outputs do not enter the system during disconnection through undocumented copying or unregistered media.

The Publication Gateway governs applicable disclosure. The UCKK Dimension Gateway governs applicable user-selected UCKK dimension transfer. Their offline artifacts, receipts, policies, and ownership remain distinct.

## 9. Exceptions and Compatibility

An exception or waiver can apply only to a bounded effective deployment, release, component instance, artifact instance, or migration action.

It cannot:

- make the overlay independently deployable;
- add compatibility with an undeclared primary profile;
- require Internet access for the local core;
- create an undeclared external route;
- disable local audit or recourse durability;
- permit unsigned or unverifiable release activation;
- bypass replay, downgrade, or compatibility controls;
- make external AI native or authoritative;
- make Ariane navigation depend on external voice;
- merge Publication Gateway with UCKK Dimension Gateway;
- change component data ownership;
- authorize a sovereign-offline claim without required tests and evidence.

Compatibility covers:

- primary profile and overlay versions;
- hardware and resource envelopes;
- local component contracts;
- offline behavior;
- network policy;
- identity and trust material;
- time and freshness policy;
- transfer manifests;
- artifact classes and versions;
- release-channel versions;
- backup and restore formats;
- audit and evidence formats;
- tests and evidence.

An imported object with unknown compatibility remains quarantined. Agent inference does not establish compatibility.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. `sovereign_offline` is active and classified as a profile overlay;
2. the overlay is not independently deployable;
3. the selected primary profile explicitly declares compatibility;
4. every additional overlay is pairwise compatible;
5. the effective profile identifies every contributing object and version;
6. every required local capability operates under complete external network denial;
7. every other capability has explicit degraded, deferred, unavailable, offline-transfer, or prohibited behavior;
8. boot, identity, authorization, policy, audit, recovery, and shutdown have no remote dependency;
9. no undeclared route, proxy, resolver, discovery path, callback, or external service is active;
10. every permitted local network path is explicit and tested;
11. every inbound and outbound transfer uses a registered artifact and integration contract;
12. manifests, signatures, integrity, provenance, policy, target ownership, and compatibility validate;
13. replay, duplicate, revocation, and downgrade tests pass;
14. all four release channels form one compatible Release Set before activation;
15. activation is atomic and authority activates last;
16. rollback or validated forward repair remains locally available;
17. local trust, revocation, time, and freshness behavior passes the declared disconnected interval;
18. critical audit and recourse records survive restart and later export without duplication;
19. resource and storage pressure preserve the local core and recovery reserves;
20. backup, restore, portability, exit, and replacement-node procedures execute offline;
21. the native baseline remains non-AI;
22. external AI surfaces remain unavailable without an authorized boundary;
23. Ariane local non-voice navigation passes without network or voice;
24. native UCKK processing remains deterministic and local;
25. gateway and component ownership separations remain intact;
26. exceptions remain bounded and visible;
27. every requirement, lock, component, profile, release, artifact, test, and evidence reference resolves;
28. no unresolved marker or inferred compatibility enters the active claim.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_profile_inheritance.py
tools/check_offline_continuity.py
tools/check_interfile_locks.py
tools/check_component_boundaries.py
tools/check_ai_boundary.py
tools/check_release_sets.py
tools/check_artifact_contracts.py
tools/check_traceability.py
tools/check_no_unresolved_state.py
```

## 11. Non-Normative Examples

### 11.1 Sovereign node composition

A compatible sovereign node composes its primary profile with `sovereign_offline`. The effective profile retains local identity, policy, audit, Ariane navigation, UCKK processing, authoritative data, recovery, and signed offline updates.

### 11.2 Controlled release transfer

An operator receives a signed offline Release Set containing compatible system, services, governance, and knowledge versions. The node quarantines and verifies the bundle, stages all channels, executes local tests, and activates atomically.

### 11.3 Revocation update

A signed revocation bundle arrives through controlled media. The node verifies sequence and trust, stages the new material, evaluates affected identities and artifacts, activates the update, and records evidence. An older replayed bundle is rejected.

### 11.4 Local network without Internet

A sovereign hub uses an explicitly declared isolated local segment for trusted nodes and an operator station. No default route, public resolver, automatic proxy, or external callback exists. Local connectivity does not weaken the offline claim.

### 11.5 UCKK transfer

A user exports selected media through the UCKK Dimension Gateway into a destination-bound offline bundle. The Publication Gateway is not substituted, and no general disclosure authority is inferred.

### 11.6 Ariane during complete disconnection

The node has no external connectivity. Ariane continues local non-voice navigation. The external voice adapter is unavailable and does not affect local interaction.

### 11.7 Storage pressure

Local storage approaches its reserve threshold. The Resource Governor removes regenerable caches, pauses optional indexing, and rejects new heavy work before authoritative data, audit records, trust material, and recovery artifacts are endangered.

### 11.8 Failed update

A policy bundle is validly signed but incompatible with the active governance channel. The node keeps the current policy active, records the failure, and waits for a compatible bundle or validated repair.

### 11.9 Power-loss recovery

Power fails during a staged update. After restart, the node restores the previous active Release Set, verifies pending state, and keeps the incomplete staged objects inactive.

### 11.10 Reconnection assessment

A disconnected node is connected to a maintenance network. External routes remain disabled until peer identity, trust, policy, time, compatibility, and pending transfers are assessed. Cable insertion alone changes no authority.
