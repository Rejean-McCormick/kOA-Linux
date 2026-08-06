<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CON-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/safe_degradation",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json",
    "contracts/integration-types.contract.json",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/cqrs-projection.schema.json",
    "contracts/artifact-contracts/cache-policy.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-BASELINE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-GOV-001",
    "DEC-UCKK-EXT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-ARI-001",
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-CQRS-001",
    "DEC-CACHE-001"
  ],
  "requirement_ids": [
    "REQ-CON-SAFE-001",
    "REQ-CON-SAFE-002",
    "REQ-CON-SAFE-003",
    "REQ-CON-SAFE-004",
    "REQ-CON-SAFE-005",
    "REQ-CON-SAFE-006",
    "REQ-CON-SAFE-007",
    "REQ-CON-SAFE-008",
    "REQ-CON-SAFE-009",
    "REQ-CON-SAFE-010",
    "REQ-CON-SAFE-011",
    "REQ-CON-SAFE-012",
    "REQ-CON-SAFE-013",
    "REQ-CON-SAFE-014",
    "REQ-CON-SAFE-015",
    "REQ-PATTERN-004",
    "REQ-PATTERN-005",
    "REQ-PATTERN-006",
    "REQ-PATTERN-007",
    "REQ-PATTERN-008",
    "REQ-PATTERN-009",
    "REQ-PATTERN-010",
    "REQ-PATTERN-011",
    "REQ-PATTERN-012",
    "REQ-PATTERN-013",
    "REQ-PATTERN-014",
    "REQ-PATTERN-015",
    "REQ-PATTERN-016",
    "REQ-PATTERN-017",
    "REQ-PATTERN-018",
    "REQ-PATTERN-019",
    "REQ-PATTERN-020",
    "REQ-PATTERN-021",
    "REQ-PATTERN-022",
    "REQ-PATTERN-023",
    "REQ-PATTERN-024",
    "REQ-PATTERN-038",
    "REQ-PATTERN-039",
    "REQ-PATTERN-040",
    "REQ-PATTERN-041",
    "REQ-PATTERN-042"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SENT-001",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-CQRS-001",
    "LOCK-CACHE-001"
  ],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "safe-degradation",
    "fail-closed",
    "capability-isolation",
    "read-only",
    "advisory-only",
    "recovery",
    "offline-continuity",
    "architecture-patterns"
  ]
}
KOA:DOC-META:END -->

# Safe Degradation

## 1. Purpose

This document defines the constitutional principle of safe degradation for the kOA-Linux Operating System.

Safe degradation allows an affected capability to retain a precisely bounded, lower-authority form of operation when its full operating conditions are unavailable. It prevents a localized failure from becoming either a system-wide outage or an unauthorized expansion of behavior.

The principle exists to make the following outcomes deterministic:

- authority is never broadened by failure;
- unavailable dependencies disable only the capabilities that actually depend on them;
- previously verified information may remain usable only within explicitly permitted limits;
- mutating operations stop when their required authority, integrity, policy, identity, or contract cannot be verified;
- unaffected capabilities may continue when their dependencies and authority remain valid;
- external and optional services may disappear without silently replacing the local baseline;
- recovery does not restore authority until verification succeeds.

Safe degradation is not best-effort behavior, an undocumented fallback, or permission to continue operating with uncertain authority. It is a controlled reduction of capability.

## 2. Scope

This document applies globally to:

- all runtime components;
- all deployment profiles and profile overlays;
- all local and remote capabilities;
- all data reads and writes;
- all policy-controlled actions;
- all privileged actions;
- all artifact activation and rollback operations;
- all external integrations;
- all optional workbenches;
- all generated, advisory, or non-authoritative outputs;
- all offline operating modes;
- all recovery and forward-repair procedures.

It applies whenever a required dependency, authority source, contract, identity, policy decision, integrity check, storage service, network service, resource allocation, external integration, or artifact becomes unavailable or invalid.

This document does not define component-specific degradation thresholds, resource values, timeouts, retry schedules, storage layouts, or user-interface wording. Those facts belong to their canonical system, profile, component, lifecycle, security, operations, integration, or artifact contracts.

A profile may narrow the degradable surface. A profile may not authorize broader degraded behavior than the global baseline.

An exception may permit a specifically bounded deviation only through `generated/exception-index.json`. Failure itself does not create an exception.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `generated/authority-manifest.json` | Identifies the active documentation and contract authority. |
| `generated/decision-index.json` | Owns accepted decisions that authorize the degradation model and its scoped variants. |
| `contracts/system.contract.json#/safe_degradation` | Owns the machine-readable global degradation states, transition rules, and capability classifications. |
| `generated/component-catalog.json` | Owns component identities, responsibilities, dependencies, and authoritative data domains. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns cross-file invariants for authority, AI, Ariane, profiles, components, data, and SenTient. |
| `generated/traceability.json` | Links requirements to decisions, components, profiles, tests, evidence, and documents. |
| `generated/evidence-catalog.json` | Owns evidence records for degradation entry, continued operation, recovery, and reactivation. |
| `generated/exception-index.json` | Owns approved deviations and compensating controls. |
| `contracts/integration-types.contract.json` | Owns integration classification, dependency direction, data transfer, and failure boundaries. |

This document explains the constitutional meaning of safe degradation. It does not become a second owner of machine-readable component states, profile matrices, dependency graphs, or integration inventories.

## 4. Model and Responsibilities

### 4.1 Core principle

Safe degradation is a reduction in available capability without a reduction in required authority.

A failure may remove functions, narrow permitted actions, delay work, expose only verified historical information, or require manual recovery. It does not authorize new data access, new privilege, new network transfer, new cross-component writes, new AI behavior, or a less restrictive policy.

### 4.2 Unit of degradation

The unit of degradation is a declared capability, not automatically the entire system or component.

Each capability has:

- an owning component;
- a declared authority source;
- required dependencies;
- authoritative data inputs;
- permitted output classes;
- applicable profiles;
- an allowed degradation behavior;
- recovery conditions;
- observable evidence.

A component with multiple capabilities may retain one capability while another becomes unavailable, provided their dependencies and authority are separable.

### 4.3 Operational conditions

The machine-readable state model is owned by `contracts/system.contract.json#/safe_degradation`. The following explanations apply to its operational conditions:

| Operational condition | Meaning |
| --- | --- |
| Full operation | All required authority, contracts, dependencies, integrity checks, and resource conditions are valid. |
| Constrained operation | The capability remains authoritative but operates within a smaller declared envelope, such as reduced concurrency or delayed background work. |
| Read-only degradation | Verified information remains readable, but operations that create, mutate, activate, publish, authorize, or delete authoritative state are denied. |
| Advisory-only degradation | The capability may produce clearly marked suggestions or diagnostics that carry no authority and cannot mutate canonical state. |
| Unavailable capability | The capability provides no output because a safe lower-authority mode does not exist. |
| Blocked activation | A candidate artifact, policy, release, document, or configuration cannot become active because its required validation or authority is incomplete. |
| Recovery in progress | The capability is being repaired or restored, but full authority remains withheld until verification completes. |

A capability may expose a cached or last-known-valid view only when the underlying record was previously verified, its provenance remains available, the view is clearly identified as non-current when freshness matters, and no policy prohibits continued disclosure.

### 4.4 Authority retained and denied

Every degradation rule identifies both retained and denied authority.

Retained authority may include:

- reading previously verified local state;
- displaying locally available navigation;
- exporting user-owned data when the export path and policy remain valid;
- queuing work without executing an authoritative transition;
- producing diagnostics;
- performing non-authoritative previews;
- continuing an isolated capability whose dependencies remain valid.

Denied authority may include:

- creating or changing authoritative records;
- activating artifacts or policies;
- publishing across a boundary;
- escalating privilege;
- inferring consent;
- substituting an unapproved identity or trust source;
- sending data to an unavailable or unapproved integration;
- treating advisory output as a decision;
- bypassing required receipts, validation, or policy.

### 4.5 Capability isolation

A failure is contained to the smallest declared capability boundary.

Continuation of unaffected capabilities requires:

- no hidden dependency on the failed capability;
- no shared authoritative transaction left incomplete;
- valid identity and policy for continued operations;
- valid storage and integrity for retained state;
- no violation of profile, security, lifecycle, or data-ownership boundaries.

A component does not write directly to another component's authoritative store in order to bypass an unavailable interface.

### 4.6 Optional and external capabilities

An optional capability is removable without breaking the required local baseline for its applicable profile.

Loss of an external integration affects only capabilities whose contracts explicitly depend on that integration.

The system does not silently substitute:

- another external provider;
- an embedded AI model;
- an autonomous agent;
- an unapproved network service;
- an alternate publication path;
- a less restrictive policy;
- a shared mutable data store.

Ariane local navigation remains available without the optional external voice path. Voice-dependent actions become unavailable when the approved voice path is unavailable.

SenTient remains isolated, optional, task-activated, and non-authoritative. Its absence does not reduce the authority or availability of the local kOA baseline.

### 4.7 Resource degradation

The Resource Governor may reduce concurrency, delay background jobs, suspend optional workers, or deny new work according to the active profile and resource contract.

The Resource Governor does not decide authorization, disclosure, consent, privilege, or exception policy. The Governance Policy Runtime does not allocate CPU, memory, storage bandwidth, or worker concurrency.

Resource pressure does not justify bypassing data ownership, policy, integrity, or audit controls.

### 4.8 Partial state

A partial transaction, partially activated artifact, incomplete migration, or incompletely published record is not authoritative.

Where atomic rollback is supported, the system returns to the last verified state. Where rollback would violate compatibility or data integrity, the system blocks rollback and uses a declared forward-repair procedure.

### 4.9 Evidence and observability

Every entry into or exit from a degraded condition produces observable evidence appropriate to the capability.

Evidence identifies:

- the affected capability;
- the detected condition;
- the failed or invalid dependency;
- retained authority;
- denied authority;
- selected degraded behavior;
- affected profile and component;
- start time;
- recovery criteria;
- recovery result;
- any receipt or incident reference.

User-facing status does not claim normal operation while the capability is degraded.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CON-SAFE-001,REQ-CON-SAFE-002,REQ-CON-SAFE-003,REQ-CON-SAFE-004,REQ-CON-SAFE-005,REQ-CON-SAFE-006,REQ-CON-SAFE-007,REQ-CON-SAFE-008,REQ-CON-SAFE-009,REQ-CON-SAFE-010,REQ-CON-SAFE-011,REQ-CON-SAFE-012,REQ-CON-SAFE-013,REQ-CON-SAFE-014,REQ-CON-SAFE-015 -->
- **REQ-CON-SAFE-001 — SHALL NOT:** A failure, timeout, unavailable dependency, invalid contract, or unverifiable authority source shall not broaden authority, privilege, disclosure, data access, network access, or permitted mutation.
- **REQ-CON-SAFE-002 — SHALL:** Degradation shall be applied to the smallest declared capability boundary whose dependencies or authority are invalid.
- **REQ-CON-SAFE-003 — SHALL:** A mutating operation shall fail closed when its required identity, policy, authority, integrity, contract, or receipt mechanism cannot be verified.
- **REQ-CON-SAFE-004 — SHALL:** Read-only degradation shall expose only previously verified data whose continued visibility is permitted by the applicable policy and profile.
- **REQ-CON-SAFE-005 — SHALL:** Advisory-only output shall be identified as non-authoritative and shall not directly create, mutate, activate, publish, authorize, or delete canonical state.
- **REQ-CON-SAFE-006 — SHALL:** Loss of an optional or external dependency shall disable only the capabilities that explicitly depend on it.
- **REQ-CON-SAFE-007 — SHALL NOT:** The system shall not silently substitute an unapproved provider, AI model, agent, identity source, policy source, publication path, or data store during degradation.
- **REQ-CON-SAFE-008 — SHALL:** Unaffected capabilities may continue only when their authority, dependencies, integrity, data ownership, and profile scope remain valid.
- **REQ-CON-SAFE-009 — SHALL NOT:** Degradation shall not authorize direct writes to another component's authoritative data source.
- **REQ-CON-SAFE-010 — SHALL:** Every degraded condition shall declare retained authority, denied authority, recovery criteria, and observable evidence.
- **REQ-CON-SAFE-011 — SHALL:** Partial activation, partial publication, partial migration, and partial authoritative transactions shall remain non-authoritative.
- **REQ-CON-SAFE-012 — SHALL:** Recovery shall preserve degraded restrictions until all required verification and revalidation checks pass.
- **REQ-CON-SAFE-013 — SHALL:** Rollback shall return to a compatible last-known-valid state; when safe rollback is impossible, the affected capability shall remain blocked until forward repair succeeds.
- **REQ-CON-SAFE-014 — SHALL:** Profile-specific degradation rules shall be explicitly declared and shall not broaden the global degradation baseline.
- **REQ-CON-SAFE-015 — SHALL NOT:** Documentation, interfaces, logs, receipts, or status endpoints shall not represent a degraded capability as fully operational.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Entering a degraded condition

The owning component performs the following ordered procedure:

1. detect a failed, unavailable, incompatible, or unverifiable condition;
2. identify the affected capability and its dependency boundary;
3. stop new authoritative mutations for that capability;
4. determine whether an incomplete operation exists;
5. complete an already-committed atomic operation, roll it back, or mark it non-authoritative according to its contract;
6. verify the integrity, provenance, policy, and permitted visibility of any retained state;
7. select the narrowest allowed degraded behavior;
8. deny all behavior not explicitly retained;
9. emit degradation evidence and update observable status;
10. notify dependent components through declared contracts;
11. continue unaffected capabilities only after dependency isolation is confirmed.

A timeout alone does not authorize a fallback. The fallback behavior must already exist in the owning contract.

### 6.2 Read-only entry

Read-only degradation is permitted only when:

- the data was previously verified;
- no incomplete mutation can be mistaken for committed state;
- disclosure remains authorized;
- provenance remains available;
- the component can enforce the write prohibition;
- freshness limitations are visible where they affect interpretation.

If any condition fails, the capability becomes unavailable rather than read-only.

### 6.3 Advisory-only entry

Advisory-only degradation is permitted only when:

- the output is not an owner decision;
- the output is visibly identified as advisory;
- the output cannot directly mutate canonical state;
- a separate authorized actor or component must review and apply any resulting action;
- data transfer remains within the applicable policy and integration contract.

### 6.4 Optional dependency loss

When an optional dependency disappears:

1. the dependent feature becomes unavailable or enters its declared lower-authority mode;
2. the local baseline remains active when its own dependencies remain valid;
3. no alternative provider is selected automatically;
4. queued work remains bounded and does not claim completion;
5. recovery occurs only after the dependency is reverified.

### 6.5 Recovery and reactivation

Recovery follows this sequence:

1. repair or restore the failed dependency;
2. verify identity, integrity, compatibility, authority, and policy;
3. reconcile queued, incomplete, or historical state;
4. run applicable component, profile, lifecycle, security, and conformance checks;
5. confirm that no partial state is being promoted;
6. produce recovery evidence;
7. reactivate the capability;
8. clear degraded status only after reactivation succeeds.

A recovered process is not automatically a recovered capability.

### 6.6 Rollback and forward repair

Rollback is selected when the previous state remains compatible with current authoritative data and contracts.

Forward repair is selected when:

- data migrations are irreversible;
- the prior contract cannot interpret current state;
- rollback would violate a security or policy invariant;
- rollback would reintroduce an invalid artifact;
- the last-known-valid state is no longer complete.

During forward repair, the affected capability remains blocked, read-only, or advisory-only according to its contract.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| Required authority or policy cannot be verified | Fail closed for the affected action | Previously valid state may remain readable when disclosure is still permitted | New authorization, mutation, privilege, activation, or publication | Verification failure record and affected capability ID |
| Identity or trust source is invalid | Reject operations requiring that identity | Public or already authorized local information only, if its policy permits | Authentication-dependent and identity-bound actions | Trust-verification result |
| Component dependency is unavailable | Apply the declared capability-specific mode | Unaffected independent capabilities | Hidden fallback and undeclared dependency bypass | Dependency-health event |
| Authoritative store is unavailable | Stop authoritative writes; allow verified read-only state only when supported | Last-known-valid readable state | Creates, updates, deletes, migrations, and commits | Storage-health and read-only entry evidence |
| Integrity verification fails | Treat affected data or artifact as invalid | Unaffected verified objects | Activation, execution, publication, or import of the invalid object | Integrity-failure receipt |
| Governance Policy Runtime is unavailable | Block policy-dependent sensitive actions | Operations that do not require that policy authority | Disclosure, consent, privilege, and exception decisions requiring policy | Policy-runtime health evidence |
| Resource Governor restricts capacity | Reduce concurrency, queue work, or suspend optional workers | Authorized work within the active envelope | Work above the active resource envelope | Resource-allocation event |
| External AI surface is unavailable | Disable only the dependent external capability | Local deterministic baseline | Silent local AI or alternate provider substitution | Integration-status event |
| Ariane external voice path is unavailable | Keep local non-voice navigation; disable voice-dependent actions | Local navigation and deterministic controls | Voice recognition and voice-dependent action initiation | Ariane capability-status event |
| SenTient is absent or stopped | Continue baseline without SenTient | Local authoritative components | SenTient research functions | Workbench availability event |
| Publication path is unavailable | Retain local authoritative state and queue only when the contract permits | Local state and bounded pending intent | Claim of publication or cross-domain disclosure | Publication failure receipt |
| Artifact activation is incomplete | Reject the candidate activation and return to a valid state or block for repair | Last-known-valid active artifact | Partial candidate authority | Activation and rollback receipt |
| Recovery validation fails | Remain in the current degraded mode | Previously retained authority | Full reactivation | Failed recovery-validation report |
| Evidence subsystem is unavailable for a transition that requires evidence | Block the transition | Existing valid state | Evidence-required transition | Evidence-service failure record |

Safe degradation does not require every capability to have a lower-authority mode. When no safe mode exists, unavailability is the correct behavior.

## 8. Cross-Component Interactions

### 8.1 Owning component

The owning component detects and contains failure inside its declared responsibility boundary. It does not transfer ownership merely because another component remains available.

### 8.2 Identity and Trust

Identity and Trust supplies verified identity and trust results. Consumers fail closed for identity-bound actions when those results are unavailable or invalid.

Cached identity material may be used only when its validity period, revocation model, profile policy, and relying contract explicitly permit it.

### 8.3 Governance Policy Runtime

The Governance Policy Runtime decides authorization, disclosure, consent, privilege, and governed exceptions for capabilities within its scope.

Its absence does not grant permission. Components may continue only operations that do not require a new policy decision or whose previously issued authorization remains valid under its canonical rules.

### 8.4 Resource Governor

The Resource Governor enforces deterministic resource envelopes. It may reduce workload concurrency or suspend optional work without changing the authorization semantics of that work.

### 8.5 Audit Broker and evidence producers

Components produce declared events or receipts. The Audit Broker and evidence system preserve selective accountability without requiring indiscriminate disclosure.

When evidence is required for authority, inability to produce or persist the evidence blocks the transition.

### 8.6 Data-owning components

A component may retain read access to its own previously verified state. Other components continue to use declared interfaces and do not bypass them through direct database access.

### 8.7 External integrations

Each integration contract defines:

- dependent capabilities;
- transferred data;
- authority boundary;
- retry and queue behavior;
- user-visible failure;
- recovery verification.

An integration failure cannot change the integration classification or widen data transfer.

### 8.8 Ariane

Ariane separates deterministic local navigation from optional external voice processing. Loss of voice processing preserves non-voice navigation and disables only voice-dependent actions.

### 8.9 kOA and UCKK Mediatheques

Loss of UCKK connectivity does not degrade the authority or availability of locally installed kOA Mediatheque content.

While disconnected:

- local records, local versions, rights state, provenance, search, browsing, backup, restore, and deterministic derivatives continue within the active profile envelope;
- previously imported and verified UCKK courses, learning paths, instructions, and resources remain available offline;
- new UCKK discovery, download, publication delivery, withdrawal delivery, and remote-result confirmation become deferred or unavailable;
- a queued outbound publication remains `pending`, never `published`;
- a partially downloaded inbound package remains quarantined and unavailable until integrity and acceptance checks pass.

Resource pressure may reduce local derivative concurrency or suspend previews, but it does not change ownership, rights, publication authority, or import acceptance rules.

### 8.10 SenTient

SenTient outputs remain isolated and non-authoritative. A SenTient result requires an explicit authorized transition before it can affect an authoritative component.

Stopping SenTient requires no substitution and does not impair the local baseline.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision ID | Effect on this document |
| --- | --- |
| `DEC-PROFILE-BASELINE-001` | Separates global baseline behavior from deployment-profile and overlay behavior. |
| `DEC-AI-001` | Establishes the strict external AI boundary and prohibits silent native AI substitution. |
| `DEC-SENT-001` | Classifies SenTient as isolated, optional, task-activated, and non-authoritative. |
| `DEC-GOV-001` | Separates deterministic resource control from governance authorization and disclosure decisions. |
| `DEC-ARI-001` | Preserves Ariane local navigation while making the approved external voice path optional and degradable. |

### 9.2 Related accepted ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-019` | Resource and policy authority remain separate during failure. |
| `ADR-021` | Ariane retains local navigation without external voice. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a failure creates permission;
- continued process execution means continued authority;
- cached data is safe merely because it is available;
- read-only behavior is always safe;
- a retry is equivalent to recovery;
- an optional integration may be replaced automatically;
- an external AI provider may be replaced by local AI without a decision;
- a component may write another component's store to restore service;
- resource pressure allows policy or integrity checks to be skipped;
- a degraded result may be presented as complete or current;
- a partial transaction may be treated as committed;
- a profile-specific fallback applies globally;
- the absence of a lower-authority mode is a design defect;
- rollback is always safer than forward repair;
- historical implementation behavior creates current authority.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the document is registered at `01-constitution/06-safe-degradation.md`;
3. all metadata identifiers are unique and resolve;
4. every listed decision has status `accepted`;
5. every requirement exists in `generated/requirements-index.json` with identical text and strength;
6. every lock exists in `generated/assertion-index.json`;
7. every canonical reference resolves;
8. `contracts/system.contract.json#/safe_degradation` defines machine-readable capability conditions and transitions consistent with this document;
9. component degradation rules identify retained and denied authority;
10. profile rules do not broaden the global baseline;
11. external integrations declare dependency and failure boundaries;
12. optional capabilities can be removed without breaking the required baseline of applicable profiles;
13. read-only and advisory-only modes cannot perform authoritative mutations;
14. recovery tests prove that full authority is restored only after revalidation;
15. tests cover dependency loss, policy loss, identity failure, integrity failure, storage failure, resource pressure, optional integration loss, rollback, and forward repair;
16. evidence records identify the affected capability and selected behavior;
17. no active file uses an undefined degradation state;
18. no active document describes an undeclared fallback;
19. no unresolved-authority marker or template token appears;
20. active content is written in English.

The validator reports actionable failures, including:

`text
safe_degradation_missing_capability_owner
safe_degradation_missing_dependency
safe_degradation_undeclared_mode
safe_degradation_authority_expansion
safe_degradation_write_not_blocked
safe_degradation_unapproved_substitution
safe_degradation_missing_evidence
safe_degradation_profile_scope_violation
safe_degradation_partial_state_authoritative
safe_degradation_recovery_not_revalidated
`

## 11. Non-Normative Examples

### 11.1 Ariane voice unavailable

The external voice path is unavailable. Ariane continues to provide local visual and keyboard navigation. Voice-dependent actions are disabled. No local speech model or alternate provider is activated automatically.

### 11.2 Local Mediatheque worker under resource pressure

The Resource Governor pauses preview generation and allows one low-priority media job at a time. Verified local source media and previously accepted offline learning packages remain available. Missing previews are shown as pending rather than corrupt. The resource decision does not change media ownership, UCKK import acceptance, or publication policy.

### 11.3 Governance policy unavailable

A user can continue reading locally available information that was already authorized and remains permitted for disclosure. A new cross-domain publication request is blocked because it requires a fresh policy decision.

### 11.4 Component database unavailable

The component displays a previously verified local snapshot as read-only and identifies its last successful update. It rejects create, update, delete, migration, and activation operations until storage integrity and recovery checks succeed.

### 11.5 SenTient stopped

The research workbench is absent from the user-lightweight profile and stopped in a developer profile. Konnaxion, Orgo, Ariane, Kristal, the kOA Mediatheque, installed offline learning content, and the language runtime continue according to their own contracts. No replacement AI service starts.

### 11.6 Failed artifact activation

A service artifact fails compatibility validation during activation. The candidate never becomes authoritative. The system retains the compatible previous artifact when rollback remains safe; otherwise, the service remains blocked while forward repair is performed.

### 11.7 Evidence service unavailable

A transition requiring a durable receipt is not executed. Existing state remains active. The interface reports that the requested action is blocked because evidence cannot be recorded.

## Architecture-pattern degradation

Remote and asynchronous failures are contained through the architecture-pattern policy. Open circuits fail fast without disabling independent local capabilities. Quarantined work remains visible. Distributed workflows expose pending or repair-required state. Stale projections and caches are bounded and labeled. No degraded mechanism may manufacture authoritative success.
