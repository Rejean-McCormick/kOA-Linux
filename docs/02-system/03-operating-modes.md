<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/operating_modes",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-SYS-003",
    "DEC-SYS-004",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-ARI-001",
    "DEC-UCKK-001",
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-SYS-MODE-001",
    "REQ-SYS-MODE-002",
    "REQ-SYS-MODE-003",
    "REQ-SYS-MODE-004",
    "REQ-SYS-MODE-005",
    "REQ-SYS-MODE-006",
    "REQ-SYS-MODE-007",
    "REQ-SYS-MODE-008",
    "REQ-SYS-MODE-009",
    "REQ-SYS-MODE-010",
    "REQ-SYS-MODE-011",
    "REQ-SYS-MODE-012",
    "REQ-SYS-MODE-013",
    "REQ-SYS-MODE-014",
    "REQ-SYS-MODE-015",
    "REQ-SYS-MODE-016",
    "REQ-SYS-MODE-017",
    "REQ-SYS-MODE-018",
    "REQ-SYS-MODE-019",
    "REQ-SYS-MODE-020"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-GOV-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-002",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-017"
  ],
  "tags": [
    "system",
    "operating-modes",
    "user-mode",
    "developer-mode",
    "service-mode",
    "maintenance",
    "recovery",
    "offline",
    "degradation",
    "resource-governance"
  ]
}
KOA:DOC-META:END -->

# Operating Modes

## 1. Purpose

This document defines the operating-mode model for the kOA operating environment.

The model describes how capabilities are exposed and constrained during interactive use, development, unattended service execution, maintenance, recovery, offline operation, degraded operation, and controlled emergency access.

An operating mode is not a deployment profile.

A deployment profile defines which components, capabilities, assurance properties, resource envelopes, and implementation choices are available for a deployment. An operating mode defines how an allowed capability is being used at a particular time and within a particular scope.

The mode model prevents several forms of architectural drift:

- treating developer convenience as a production entitlement;
- treating an offline condition as unrestricted local authority;
- treating maintenance or recovery as a universal privilege bypass;
- treating one failed external integration as a whole-system failure;
- treating resource availability as authorization;
- treating an optional workbench as part of the default user baseline;
- treating a host-wide label as sufficient when different workspaces or components are operating independently.

## 2. Scope

This document applies globally to:

- interactive sessions;
- development workspaces;
- unattended component services;
- background workers and scheduled jobs;
- maintenance activities;
- backup, restore, rollback, and recovery activities;
- connected and disconnected operation;
- nominal and degraded capability states;
- ordinary and break-glass authority contexts;
- local and external integrations;
- all deployment profiles and overlays.

The mode model applies at the smallest meaningful execution scope, which can be:

```text
session
workspace
component instance
worker
job
service group
node
deployment
recovery environment
```

A host can therefore contain several simultaneous mode instances. For example, one user session can remain in interactive user mode while an isolated development workspace runs in development workspace mode and background components run in unattended service mode.

This document does not define the full membership of a deployment profile, the internal state machine of a component, the structure of a release artifact, or the detailed offline behavior of each capability. Those facts belong to their respective canonical owners.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/operating_modes
generated/profile-catalog.json
generated/component-catalog.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/exception-index.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| `authority.registry.json` | Active authority and registry versions |
| `decisions.registry.json` | Accepted decisions governing the mode model |
| `system.registry.json#/operating_modes` | Mode identities, state dimensions, transition rules, and global behavior |
| `profiles/index.json` and profile contracts | Modes and overlays permitted by each deployment profile |
| `components.registry.json` | Components eligible to instantiate service, maintenance, or recovery behavior |
| `requirements.registry.json` | Normative mode requirements |
| `locks.registry.json` | Cross-file invariants for profiles, development, AI, resources, and lifecycle |
| `traceability.registry.json` | Links to profiles, components, tests, evidence, and documents |
| `exceptions.registry.json` | Bounded deviations that cannot create missing authority |

This document explains the mode model. It does not independently own canonical mode identifiers or profile membership.

## 4. Model and Responsibilities

### 4.1 Orthogonal model

A mode instance is described by four independent dimensions:

```text
primary mode
connectivity state
capability health
authority context
```

The dimensions are evaluated for a declared execution scope rather than assumed globally.

### 4.2 Primary modes

The global primary modes are:

| Mode | Purpose | Typical scope | Core restriction |
| --- | --- | --- | --- |
| `interactive_user` | Consume installed and activated capabilities | Session or user-facing application set | No implicit build, release, production, or host-mutation authority |
| `development_workspace` | Build, test, debug, and inspect software in isolation | Workspace, branch, worktree, or component sandbox | No implicit production or publication authority |
| `unattended_service` | Run declared component services and workers | Component instance, service group, worker, or job | Bounded identity, interfaces, resources, retries, and owned data |
| `maintenance` | Perform planned inspection, upgrade, repair, or administrative work | Component, service group, node, or deployment | Explicit target and permitted action set |
| `recovery` | Restore a valid state after failure or corruption | Recovery environment, component, node, or deployment | Only recovery-related capabilities remain enabled |

These modes describe behavior, not assurance level. A `sovereign_linux_node` and a `developer_windows_wsl` deployment can both instantiate `development_workspace` or `unattended_service` only where their profile contracts permit those modes.

### 4.3 Connectivity states

| State | Meaning |
| --- | --- |
| `connected` | Required network dependencies are available and permitted |
| `offline` | The scope operates without required external network access |
| `restricted_connectivity` | Only a declared subset of endpoints, networks, or transfer paths is available |

Connectivity does not determine authority. An operation performed locally or offline still requires applicable authority.

### 4.4 Capability-health states

| State | Meaning |
| --- | --- |
| `nominal` | The declared capability set is available within its profile envelope |
| `degraded` | One or more capabilities are reduced, delayed, read-only, advisory, queued, or unavailable |
| `suspended` | The affected capability is intentionally stopped pending repair, authority, or operator action |

Degradation is capability-scoped. One unavailable capability does not automatically place the entire system in a global degraded state.

### 4.5 Authority contexts

| Context | Meaning |
| --- | --- |
| `ordinary` | Normal explicit authority applies |
| `break_glass` | A predefined, temporary emergency grant applies |
| `authority_blocked` | Required authority cannot be established and the protected effect is denied |

Break-glass is a distinct authority context, not a primary mode and not a profile.

### 4.6 Interactive user mode

Interactive user mode is the default human-facing runtime mode for ordinary use.

It is oriented toward:

- local applications and browser-based interfaces;
- compiled and activated runtime artifacts;
- Ariane local navigation;
- Orgo, Konnaxion, Kristal, SemantiK runtime, and UCKK capabilities permitted by the active profile;
- user-triggered external integrations;
- bounded background work.

The mode excludes build compilers, unrestricted development consoles, permanent heavy workbenches, broad administrative control, and automatic external AI dependence from the default baseline.

GF Wordbench, compiler toolchains, development containers, and similar authoring facilities belong to development-capable profiles and workspaces. The user language runtime consumes compiled artifacts.

SenTient is not part of the default interactive user baseline. Where installed, it runs as an optional isolated workbench under separately declared resources and authority.

### 4.7 Development workspace mode

Development workspace mode is scoped to a registered workspace.

Each workspace has independent:

- source identity;
- branch or worktree identity;
- UV-managed dependency environment;
- service namespace;
- network namespace or collision-resistant network naming;
- ports and sockets;
- databases and volumes;
- secrets and local certificates;
- process names and logs;
- resource budget;
- cleanup lifecycle.

Multiple workspaces can run concurrently without collisions. A development workspace does not become a production control plane merely because it can build or test production artifacts.

### 4.8 Unattended service mode

Unattended service mode covers long-running services, socket-activated processes, scheduled workers, queued jobs, and event-driven tasks.

Each service instance declares:

- component identity;
- service identity;
- execution identity;
- owned data and permitted interfaces;
- accepted input classes;
- produced artifacts or events;
- resource budget;
- retry and timeout limits;
- health and readiness signals;
- startup and shutdown behavior;
- failure and degradation behavior.

Optional integrations and heavy workers can be stopped without disabling the native baseline when their capability is not required.

### 4.9 Maintenance mode

Maintenance mode supports planned changes and diagnostics.

Examples include:

- schema migration;
- service upgrade;
- artifact verification;
- index rebuild;
- storage inspection;
- certificate replacement;
- controlled host mutation;
- backup validation;
- configuration repair.

Maintenance mode does not grant authority by itself. Privileged work still uses the applicable policy decision and privileged broker where required by the profile.

### 4.10 Recovery mode

Recovery mode supports:

- diagnosis;
- rollback;
- restoration;
- forward repair;
- backup recovery;
- trusted artifact reactivation;
- evidence collection;
- controlled data export for recovery.

Ordinary workloads remain disabled when they can interfere with recovery integrity. The recovery environment does not silently become a general administrative environment.

### 4.11 Resource governance

The Resource Governor applies budgets independently from authorization.

Mode-specific resource behavior includes:

- prioritizing interactive responsiveness in user mode;
- isolating workspace budgets in development mode;
- limiting retries and concurrency in service mode;
- reserving capacity for maintenance and recovery;
- serializing or deferring heavy UCKK media jobs on constrained hardware;
- stopping optional heavy services when the active profile excludes them.

The Governance Policy Runtime, when deployed, evaluates governance authorization. It remains separate from the Resource Governor.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-MODE-001,REQ-SYS-MODE-002,REQ-SYS-MODE-003,REQ-SYS-MODE-004,REQ-SYS-MODE-005,REQ-SYS-MODE-006,REQ-SYS-MODE-007,REQ-SYS-MODE-008,REQ-SYS-MODE-009,REQ-SYS-MODE-010,REQ-SYS-MODE-011,REQ-SYS-MODE-012,REQ-SYS-MODE-013,REQ-SYS-MODE-014,REQ-SYS-MODE-015,REQ-SYS-MODE-016,REQ-SYS-MODE-017,REQ-SYS-MODE-018,REQ-SYS-MODE-019,REQ-SYS-MODE-020 -->
- **REQ-SYS-MODE-001 — SHALL:** Every authority-bearing operation resolve an active operating-mode context for the actor, capability, target, and execution scope.
- **REQ-SYS-MODE-002 — SHALL:** Each deployment profile declare the primary operating modes and state overlays it permits.
- **REQ-SYS-MODE-003 — SHALL NOT:** A mode transition broaden authority, data ownership, trust, disclosure, privilege, or profile scope by itself.
- **REQ-SYS-MODE-004 — SHALL:** Interactive user mode consume installed and activated runtime artifacts without requiring build toolchains, compilers, development containers, or unrestricted administrative interfaces.
- **REQ-SYS-MODE-005 — SHALL:** Development workspace mode isolate mutable dependencies, service state, ports, data, secrets, processes, and resource budgets by workspace.
- **REQ-SYS-MODE-006 — SHALL NOT:** Development workspace mode confer production, publication, release, policy, or host-mutation authority unless separately and explicitly granted.
- **REQ-SYS-MODE-007 — SHALL:** Unattended service mode run only declared component capabilities under bounded identities, resources, interfaces, and retry policies.
- **REQ-SYS-MODE-008 — SHALL:** Maintenance mode identify its initiator, target scope, permitted actions, start condition, completion condition, and rollback or repair behavior.
- **REQ-SYS-MODE-009 — SHALL:** Recovery mode restrict activity to diagnosis, restoration, rollback, forward repair, evidence collection, and explicitly authorized data export.
- **REQ-SYS-MODE-010 — SHALL NOT:** Offline, degraded, maintenance, recovery, or break-glass state be treated as a general authorization bypass.
- **REQ-SYS-MODE-011 — SHALL:** Offline operation remain inside the capability envelope declared by the active profile and applicable offline-authority contracts.
- **REQ-SYS-MODE-012 — SHALL:** Degradation be contained to affected capabilities while independently valid local, read-only, advisory, or queued capabilities remain available.
- **REQ-SYS-MODE-013 — SHALL:** Break-glass authority be explicit, narrowly scoped, time-bounded, human-invoked, recorded, and reviewed.
- **REQ-SYS-MODE-014 — SHALL:** Operating-mode transitions preserve the last valid authoritative state when activation or transition cannot complete atomically.
- **REQ-SYS-MODE-015 — SHALL:** The current mode and applicable connectivity, health, and authority overlays be exposed through machine-readable state and truthful user-facing status.
- **REQ-SYS-MODE-016 — SHALL:** External AI surfaces remain optional candidate-input adapters whose absence cannot disable the native system baseline.
- **REQ-SYS-MODE-017 — SHALL:** Ariane local navigation remain available without external AI when its local runtime and authority remain valid.
- **REQ-SYS-MODE-018 — SHALL:** SenTient remain optional, isolated, non-authoritative, and absent from the default interactive user baseline.
- **REQ-SYS-MODE-019 — SHALL:** Resource-intensive jobs be admitted, scheduled, limited, paused, or rejected by the Resource Governor according to the active profile and mode budget.
- **REQ-SYS-MODE-020 — SHALL:** Concurrent mode instances remain isolated and independently authorized when multiple users, workspaces, components, or services operate on the same host.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Mode-instance activation

A mode instance is activated through this sequence:

1. identify the requested primary mode and execution scope;
2. resolve the active deployment profile and overlays;
3. verify that the profile permits the requested mode;
4. resolve the component, workspace, service, or recovery contract;
5. establish ordinary or break-glass authority;
6. allocate the declared resource budget;
7. resolve connectivity and capability-health states;
8. start only the permitted capabilities;
9. expose machine-readable and user-facing mode status;
10. emit a receipt when activation is a critical transition.

A failed activation leaves the prior valid mode state intact or enters a declared safe state.

### 6.2 Interactive user to development workspace

Development work begins by creating or activating a registered workspace rather than converting the entire host into an unrestricted developer state.

The transition:

1. creates or resolves the workspace identity;
2. validates the permitted development profile;
3. activates the workspace-specific UV environment;
4. allocates ports, services, data, secrets, and resources;
5. starts only the requested toolchains and services;
6. keeps user applications and unrelated workspaces isolated;
7. records teardown and cleanup ownership.

Closing the workspace does not terminate unrelated user or service mode instances.

### 6.3 Connected to offline

A scope enters offline state by:

1. identifying lost or intentionally disabled dependencies;
2. resolving the active offline capability envelope;
3. validating cached or local authority;
4. disabling external-only capabilities;
5. retaining independently valid local capabilities;
6. queuing only work whose later execution requires fresh reevaluation;
7. exposing the offline state and capability differences;
8. reconciling queued work after connectivity returns.

The system does not fabricate successful external completion while offline.

### 6.4 Nominal to degraded

A capability enters degraded state when a dependency, resource, authority, or component is unavailable but a reduced behavior remains valid.

The transition:

1. identifies the affected capability;
2. prevents the unavailable or unauthorized effect;
3. selects the declared degraded behavior;
4. verifies that the reduced behavior does not broaden authority;
5. updates status and health signals;
6. continues unrelated capabilities;
7. retries or repairs according to bounded policy.

### 6.5 Maintenance entry and exit

Maintenance starts with a declared maintenance plan containing:

- initiator;
- target;
- permitted actions;
- expected service impact;
- backup or checkpoint requirement;
- completion test;
- rollback or forward-repair path.

The mode ends only after validation confirms the target state, affected services return to an allowed mode, and the maintenance outcome is recorded.

### 6.6 Recovery entry and exit

Recovery begins after a failed activation, corruption, unrecoverable service state, failed migration, lost dependency, or operator-declared recovery event.

The recovery sequence:

1. isolates the affected scope;
2. preserves evidence and current state where safe;
3. selects rollback, restore, or forward repair;
4. verifies recovery inputs and authority;
5. performs the bounded recovery action;
6. validates data and service integrity;
7. reactivates the last valid or newly repaired state;
8. closes the recovery event and records evidence.

### 6.7 Break-glass activation

Break-glass authority is activated only through its canonical contract.

Its activation includes:

1. identified human invocation;
2. predefined emergency condition;
3. constrained target and action;
4. short validity;
5. independent recording;
6. automatic expiration;
7. mandatory review.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Mode effect | Safe behavior |
| --- | --- | --- | --- |
| `mode_not_permitted_by_profile` | The active profile excludes the requested mode | Activation is denied | Continue the prior allowed mode |
| `mode_scope_undefined` | No session, workspace, component, service, node, or recovery scope is declared | Activation is denied | Request a concrete scope |
| `mode_authority_unavailable` | Required authority cannot be established | Protected effects are denied | Read-only or advisory behavior where separately valid |
| `workspace_isolation_conflict` | Ports, data, secrets, names, or resources collide | Workspace activation is denied | Allocate new isolated values |
| `offline_envelope_missing` | No offline contract covers the capability | External-dependent effect is unavailable | Local capabilities continue |
| `external_integration_unavailable` | An optional integration fails | Only the adapter-dependent capability degrades | Native baseline continues |
| `ai_surface_unavailable` | Approved external AI surface is unavailable | AI-assisted capability is unavailable | Deterministic native and local functions continue |
| `ariane_voice_unavailable` | External voice path is unavailable | Voice commands are unavailable | Ariane local non-voice navigation continues |
| `sentient_unavailable` | Optional SenTient workbench is absent or stopped | SenTient functions are unavailable | Default user baseline continues |
| `resource_budget_exceeded` | Work exceeds mode or profile limits | Job is queued, limited, paused, or rejected | Interactive and critical work retains priority |
| `maintenance_validation_failed` | Maintenance completion checks fail | Prior state remains or recovery begins | Rollback or forward repair |
| `recovery_input_invalid` | Backup or recovery artifact cannot be trusted | Recovery activation is denied | Preserve evidence and last valid state |
| `mode_transition_partial` | Transition cannot commit completely | Partial state does not become authoritative | Rollback or declared forward repair |
| `break_glass_contract_invalid` | Emergency authority is missing or invalid | Emergency action is denied | Escalation without unauthorized effect |

A degraded mode is not defined by reduced quality alone. It is a declared state with bounded behavior, observable status, validation, and a recovery path.

## 8. Cross-Component Interactions

### 8.1 Ariane

Ariane presents mode and capability status to the user.

Local navigation remains independent from external AI. External voice is an optional adapter. Failure of the voice path affects voice-dependent interaction only.

### 8.2 UCKK

Native UCKK ingestion, routing, verification, queuing, and lifecycle behavior remain deterministic and non-AI.

Suno and Gamma are user-triggered external adapters. Their absence does not prevent native UCKK operation. Resource-intensive media work follows Resource Governor admission and scheduling.

### 8.3 SenTient

SenTient is an optional isolated workbench. It is not authoritative, is not started by default in the lightweight user baseline, and does not become a permanent dependency of ordinary user or service modes.

### 8.4 Language runtime and GF Wordbench

The user-facing language runtime consumes compiled PGF and related activated artifacts. GF Wordbench and compiler activity run in development-capable workspaces rather than ordinary interactive user mode.

### 8.5 Resource Governor and Governance Policy Runtime

The Resource Governor controls resource allocation, scheduling, limits, and pressure response.

The Governance Policy Runtime controls governance authorization, disclosure, and privilege where deployed. Neither component silently assumes the other's authority.

### 8.6 Component services

Each component defines its own service-mode instances and internal states. The system mode model constrains how those states interact with profiles, authority, resources, connectivity, and lifecycle.

### 8.7 Publication and UCKK Dimension gateways

The Publication Gateway controls governed disclosure across domains. The UCKK Dimension Gateway controls user-selected ingestion into UCKK. Their mode state and authority remain separate.

### 8.8 Lifecycle services

Lifecycle services coordinate maintenance, recovery, artifact activation, rollback, and forward repair. A mode transition that changes authoritative activation state uses the applicable lifecycle contract and receipt.

## 9. Decision Closure and Prohibited Assumptions

This document closes the operating-mode model as follows:

- profiles and modes are distinct;
- modes are scoped and can coexist;
- offline and degraded states are overlays rather than universal profiles;
- break-glass is an authority context rather than a general mode;
- maintenance and recovery do not imply unrestricted privilege;
- interactive user mode does not include development toolchains by default;
- development workspace mode does not imply production authority;
- unattended services operate under bounded component identities and resources;
- external AI remains optional and non-native;
- Ariane local navigation remains available without external AI;
- SenTient remains optional, isolated, and outside the default user baseline;
- resource control remains separate from policy authorization.

The following assumptions are prohibited:

- the whole host has one indivisible operating mode;
- selecting a mode creates authority;
- offline operation means unrestricted local access;
- degraded operation permits bypassing policy;
- maintenance grants universal administrator authority;
- recovery grants unrestricted data access;
- developer mode is production mode with extra tools;
- a user profile must include compilers and build services;
- an optional external integration is part of the native baseline;
- external AI failure disables deterministic native capabilities;
- SenTient must remain permanently active;
- resource availability establishes authorization;
- a profile-specific Linux implementation becomes a global mode requirement;
- multiple workspaces can share mutable installed dependencies or state.

Any new primary mode or global state dimension requires an accepted owner decision, canonical system-registry update, profile-impact analysis, requirement and lock updates, and validation before activation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. `contracts/system.contract.json#/operating_modes` defines the five primary modes and three state dimensions described here;
4. every profile declares its permitted primary modes and overlays;
5. every active mode instance has an explicit scope;
6. all 20 requirements are unique, active, globally scoped, and traceable to accepted decisions;
7. every declared lock exists and is active;
8. interactive user profile tests prove that build toolchains and SenTient are absent from the default baseline;
9. development tests prove isolated UV environments, services, ports, data, secrets, and resources;
10. service tests prove bounded identities, retries, timeouts, interfaces, and resources;
11. offline tests prove that external-only capabilities fail truthfully while allowed local capabilities continue;
12. degraded-mode tests prove capability containment;
13. Ariane tests prove local navigation without external AI;
14. UCKK tests prove deterministic native behavior without Suno or Gamma;
15. maintenance tests prove declared scope, completion checks, and rollback or repair;
16. recovery tests prove isolation, verified inputs, integrity checks, and valid reactivation;
17. break-glass tests prove human invocation, narrow scope, expiration, recording, and review;
18. transition tests prove atomic activation or preservation of the prior valid state;
19. user-facing and machine-readable status expose the current mode and overlays consistently;
20. ordinary Markdown validation does not depend on file-content hashes;
21. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
22. active prose is English.

Expected validator failure codes include:

```text
mode_not_permitted_by_profile
mode_scope_undefined
mode_authority_unavailable
workspace_isolation_conflict
offline_envelope_missing
capability_degradation_not_contained
mode_status_mismatch
mode_transition_partial
break_glass_control_incomplete
user_baseline_contains_development_toolchain
user_baseline_contains_sentient
external_ai_baseline_dependency
resource_policy_authority_confusion
```

## 11. Non-Normative Examples

### 11.1 Lightweight user session

A user starts kOA on a constrained computer. The session runs in `interactive_user` mode with `connected`, `nominal`, and `ordinary` overlays. SenTient, GF Wordbench, compilers, development containers, and external AI services are not started. A heavy UCKK preview job is queued behind interactive work by the Resource Governor.

### 11.2 Parallel development workspace

The same host keeps the user session active while a developer opens a registered worktree. The worktree runs in `development_workspace` mode with its own `.venv`, ports, database, volumes, secrets, logs, and resource budget. Closing the workspace leaves the user session and unrelated services running.

### 11.3 Disconnected operation

Connectivity is lost. Local Ariane navigation, compiled language artifacts, local documents, and deterministic UCKK functions remain available within the profile's offline envelope. Suno, Gamma, external voice, and other external-only capabilities report unavailability rather than fabricated completion.

### 11.4 Optional SenTient analysis

A user explicitly starts the SenTient workbench on a capable profile. SenTient runs in an isolated mode instance with a separate resource budget and cannot mutate authoritative component state directly. Stopping it has no effect on the native user baseline.

### 11.5 Failed maintenance activation

A service upgrade enters maintenance mode but fails its completion checks. The new artifact does not become active. The lifecycle service restores the prior valid version or enters recovery mode under the declared repair plan.
