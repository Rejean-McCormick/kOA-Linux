<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-014",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/operations",
    "generated/component-catalog.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-SEC-001",
    "DEC-PRIV-001",
    "DEC-OFFLINE-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-PORT-001",
    "DEC-PROFILE-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001",
    "DEC-IMAGE-001",
    "DEC-OS-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-OPS-MAINT-001",
    "REQ-OPS-MAINT-002",
    "REQ-OPS-MAINT-003",
    "REQ-OPS-MAINT-004",
    "REQ-OPS-MAINT-005",
    "REQ-OPS-MAINT-006",
    "REQ-OPS-MAINT-007",
    "REQ-OPS-MAINT-008",
    "REQ-OPS-MAINT-009",
    "REQ-OPS-MAINT-010",
    "REQ-OPS-MAINT-011",
    "REQ-OPS-MAINT-012",
    "REQ-OPS-MAINT-013",
    "REQ-OPS-MAINT-014",
    "REQ-OPS-MAINT-015",
    "REQ-OPS-MAINT-016",
    "REQ-OPS-MAINT-017",
    "REQ-OPS-MAINT-018",
    "REQ-OPS-MAINT-019",
    "REQ-OPS-MAINT-020",
    "REQ-OPS-MAINT-021",
    "REQ-OPS-MAINT-022",
    "REQ-OPS-MAINT-023",
    "REQ-OPS-MAINT-024",
    "REQ-OPS-MAINT-025",
    "REQ-OPS-MAINT-026",
    "REQ-OPS-MAINT-027",
    "REQ-OPS-MAINT-028",
    "REQ-OPS-MAINT-029",
    "REQ-OPS-MAINT-030",
    "REQ-OPS-MAINT-031",
    "REQ-OPS-MAINT-032"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-PRIV-001",
    "LOCK-OFFLINE-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-003",
    "DOC-OPS-004",
    "DOC-LIFE-004",
    "DOC-LIFE-005",
    "DOC-LIFE-006",
    "DOC-LIFE-011",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-017",
    "DOC-LIFE-018",
    "DOC-LIFE-019",
    "DOC-SEC-001",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-018",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "operations",
    "maintenance",
    "maintenance-window",
    "change-control",
    "preflight",
    "backups",
    "updates",
    "migrations",
    "cleanup",
    "capacity",
    "security",
    "offline",
    "rollback",
    "recovery",
    "receipts"
  ]
}
KOA:DOC-META:END -->

# Maintenance

## 1. Purpose

This document defines the global kOA operational maintenance model.

Maintenance is a controlled change or inspection performed to preserve or restore:

- availability;
- integrity;
- security;
- performance;
- capacity;
- lifecycle support;
- backup and recovery readiness;
- component conformance;
- Release Set conformance;
- physical and environmental health.

Maintenance includes routine inspection and cleanup, but it can also change active software, schemas, credentials, trust, storage, resources, or authority. For that reason, maintenance is treated as a lifecycle-controlled operational procedure rather than unrestricted administration.

The maintenance model ensures that:

- the exact target and purpose are known;
- authority is bounded;
- users and operators understand impact;
- a valid return path exists;
- component ownership is preserved;
- only registered artifacts become active;
- resource and recovery reserves are protected;
- emergency access remains temporary;
- completion is based on validation;
- partial changes and failures remain visible;
- receipts and recourse survive the event.

Maintenance is not a mechanism for bypassing release, security, governance, component, data, or profile contracts.

## 2. Scope

This document applies globally to planned, corrective, emergency, security-critical, lifecycle, data, capacity, integrity, credential, physical, and decommissioning maintenance.

It covers:

- health inspection;
- service restart and repair;
- system-image updates;
- service updates;
- governance policy updates;
- knowledge artifact updates;
- Release Set activation;
- schema and data migrations;
- index and projection rebuilds;
- backup and restore validation;
- storage cleanup;
- cache and derivative cleanup;
- capacity expansion;
- resource-envelope changes;
- credential and certificate rotation;
- trust and revocation updates;
- integration credential changes;
- offline bundle import and activation;
- recovery-media validation;
- physical host maintenance;
- operating-system and firmware maintenance when profile contracts permit;
- decommissioning and protected exit.

It applies to user, developer, sovereign, hub, build, and control profiles according to their operational role.

It does not define one ticketing system, communication tool, automation framework, configuration manager, backup product, service manager, package system, or remote-access implementation.

Recipes and implementation tools remain non-normative unless adopted by the active profile and maintenance contract.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json#/operations` | Global operational and maintenance model |
| `generated/profile-catalog.json` | Profile-specific maintenance, availability, offline, privilege, and recovery requirements |
| `generated/component-catalog.json` | Component identities, ownership, profile membership, and lifecycle role |
| `generated/component-catalog.json` | Component health, mutation, migration, backup, restore, and failure contracts |
| `contracts/components/identity-and-trust.component.json` | Operator, service, node, credential, trust, and revocation identity |
| `contracts/components/governance-policy-runtime.component.json` | Governed maintenance, emergency, destructive, exception, and review decisions |
| `contracts/components/resource-governor.component.json` | Capacity admission for maintenance tasks |
| `contracts/components/koa-node-agent.component.json` | Target identity, host health, lifecycle state, and recovery readiness |
| `contracts/components/audit-broker.component.json` | Critical maintenance evidence routing |
| `contracts/artifact-classes.contract.json` | Artifact validation, staging, activation, rollback, and retention |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge release identity |
| `contracts/integration-types.contract.json` | External maintenance dependencies and credential scope |
| `generated/requirements-index.json` | Normative maintenance requirements |
| `generated/assertion-index.json` | Lifecycle, release, security, privilege, offline, profile, component, and data assertions |
| `generated/traceability.json` | Maintenance relationships to targets, releases, artifacts, tests, and evidence |
| `generated/exception-index.json` | Bounded maintenance exceptions and compensating controls |
| `generated/test-catalog.json` | Preflight, maintenance, rollback, recovery, cleanup, and completion tests |
| `generated/evidence-catalog.json` | Maintenance and transition evidence |

The adjacent operations documents include:

```text
08-operations/00-operating-model.md
08-operations/01-observability.md
08-operations/02-health-and-readiness.md
08-operations/03-slos.md
08-operations/04-resource-envelopes.md
08-operations/05-capacity-management.md
08-operations/06-job-scheduling.md
08-operations/07-capability-degradation.md
08-operations/08-backup.md
08-operations/09-restore.md
08-operations/10-portability-and-exit.md
08-operations/11-offline-operations.md
08-operations/12-incident-response.md
08-operations/13-disaster-recovery.md
08-operations/15-support-and-diagnostics.md
08-operations/16-break-glass.md
08-operations/17-user-lightweight-operations.md
08-operations/18-sovereign-node-operations.md
08-operations/19-build-farm-operations.md
```

The authoritative lifecycle detail is defined in:

```text
06-lifecycle/04-release-sets.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/14-recovery.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
```

## 4. Maintenance Model and Responsibilities

### 4.1 Maintenance classes

| Class | Purpose | Typical examples |
| --- | --- | --- |
| `planned` | Scheduled preservation or improvement | Updates, certificate rotation, backup validation |
| `corrective` | Repair an observed defect | Service repair, index rebuild, storage remediation |
| `emergency` | Contain or restore an urgent unsafe condition | Security containment, failed release recovery |
| `security_critical` | Remove or reduce security exposure | Revocation, trust update, credential rotation |
| `lifecycle` | Change active artifacts or Release Set | System, service, governance, knowledge activation |
| `data` | Change schema, repair state, restore, or migrate | Component-owned migration or restore |
| `capacity` | Change resource or storage envelope | Resource-envelope update, storage expansion |
| `integrity` | Verify or rebuild reproducible structures | Index verification, projection rebuild |
| `credential` | Change identity or secret authority | Certificate, key, token, recovery-factor rotation |
| `physical` | Maintain hardware or environment | Disk replacement, cooling, power, firmware |
| `decommissioning` | End supported operation | Protected export, revocation, shutdown, disposal |

One maintenance event can have several classes.

### 4.2 Maintenance states

| State | Meaning |
| --- | --- |
| `proposed` | Purpose and candidate scope are recorded |
| `reviewing` | Authority, risk, impact, and procedure are under review |
| `approved` | Required authority and approvals are complete |
| `scheduled` | Target window and communications are set |
| `preflight` | Target readiness is being evaluated |
| `ready` | Required preconditions and return path are valid |
| `in_progress` | Authorized work is executing |
| `paused` | Work is safely stopped pending a condition or decision |
| `validating` | Post-change and completion checks are running |
| `completed` | Success criteria passed and closure is complete |
| `completed_restricted` | Valid restricted operation remains with explicit follow-up |
| `rolled_back` | Declared prior valid state is active |
| `forward_repair` | A new corrective state is being produced |
| `recovery` | Recovery procedure controls the target |
| `failed` | The selected procedure failed and a safe state is declared |
| `cancelled` | Work ended before authorized mutation |
| `closed` | Review, cleanup, evidence, and follow-up are recorded |

### 4.3 Maintenance record

A maintenance record identifies:

- maintenance ID;
- owner;
- target;
- profile and overlays;
- active Release Set;
- classes;
- purpose;
- affected components and capabilities;
- user impact;
- authority and approvals;
- procedure version;
- artifact and migration inventory;
- start and end window;
- preconditions;
- return path;
- success and failure criteria;
- communication plan;
- evidence plan;
- exceptions;
- final result.

The record never contains secret values.

### 4.4 Roles

| Role | Responsibility |
| --- | --- |
| Maintenance owner | End-to-end accountability and closure |
| Change approver | Scope, impact, timing, and procedure approval |
| Governance reviewer | Governed, destructive, emergency, or exception decisions |
| Component owner | Component-specific mutation, health, backup, restore, and validation |
| Lifecycle owner | Artifact staging, activation, rollback, recovery, and Release Set identity |
| Security owner | Credential, trust, revocation, vulnerability, and incident controls |
| Resource Governor | Maintenance resource admission and pressure response |
| Operator | Execute approved steps and record observations |
| Evidence owner | Preserve and route critical receipts |
| User or service representative | Receive impact, status, recourse, and completion information |

One person can hold several roles only when separation-of-duties rules permit it.

### 4.5 Maintenance authority

Maintenance authority is bounded by:

- target;
- operations;
- time;
- purpose;
- environment;
- profile;
- actor;
- required approvals;
- credential scope;
- emergency conditions.

Authority to perform one host operation does not grant access to component data or unrelated secrets.

### 4.6 Return path

A return path is the validated way to leave a failed or unsafe maintenance state.

It can be:

- current-set repair;
- Release Set rollback;
- system-image recovery;
- component-owned restore;
- forward repair;
- restricted operation;
- protected export and decommissioning.

The return path identifies required artifacts, data compatibility, credentials, authority, evidence, and tests.

### 4.7 Maintenance window

A maintenance window identifies the time during which approved work can begin or continue.

The window can include:

- preparation period;
- user-impact period;
- validation period;
- rollback or recovery reserve;
- closure period.

Window expiry stops new unauthorized steps. It does not force an unsafe interruption.

### 4.8 Change freeze

A freeze blocks selected non-emergency changes.

The freeze identifies:

- scope;
- start and end;
- prohibited classes;
- permitted exceptions;
- approval authority;
- existing in-progress work;
- exit criteria.

Emergency maintenance remains explicit and reviewed.

### 4.9 Maintenance artifacts

Maintenance can use:

- signed Release Sets;
- system images;
- service artifacts;
- policy bundles;
- knowledge artifacts;
- migration packages;
- trust and revocation updates;
- resource envelopes;
- test packs;
- operator instructions;
- recovery runtime packs.

The procedure refers to immutable registered identities rather than “latest.”

### 4.10 Maintenance evidence

Evidence distinguishes:

- authorization;
- preflight;
- backup readiness;
- step execution;
- component results;
- migration results;
- activation;
- rollback;
- recovery;
- cleanup;
- user impact;
- final validation.

Evidence is attributable and selectively disclosable.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-MAINT-001,REQ-OPS-MAINT-002,REQ-OPS-MAINT-003,REQ-OPS-MAINT-004,REQ-OPS-MAINT-005,REQ-OPS-MAINT-006,REQ-OPS-MAINT-007,REQ-OPS-MAINT-008,REQ-OPS-MAINT-009,REQ-OPS-MAINT-010,REQ-OPS-MAINT-011,REQ-OPS-MAINT-012,REQ-OPS-MAINT-013,REQ-OPS-MAINT-014,REQ-OPS-MAINT-015,REQ-OPS-MAINT-016,REQ-OPS-MAINT-017,REQ-OPS-MAINT-018,REQ-OPS-MAINT-019,REQ-OPS-MAINT-020,REQ-OPS-MAINT-021,REQ-OPS-MAINT-022,REQ-OPS-MAINT-023,REQ-OPS-MAINT-024,REQ-OPS-MAINT-025,REQ-OPS-MAINT-026,REQ-OPS-MAINT-027,REQ-OPS-MAINT-028,REQ-OPS-MAINT-029,REQ-OPS-MAINT-030,REQ-OPS-MAINT-031,REQ-OPS-MAINT-032 -->
- **REQ-OPS-MAINT-001 — SHALL:** Every maintenance action have a stable maintenance identifier, target, maintenance class, purpose, owner, scope, authority, planned start, validity window, affected capabilities, procedure, preconditions, success criteria, failure criteria, rollback or recovery path, and evidence plan.
- **REQ-OPS-MAINT-002 — SHALL:** Maintenance be classified as planned, corrective, emergency, security-critical, lifecycle, data, capacity, integrity, credential, physical, or decommissioning work, with the strictest applicable controls applied when classes overlap.
- **REQ-OPS-MAINT-003 — SHALL NOT:** A maintenance window, operator role, physical access, remote session, privileged broker capability, or emergency declaration grant unrestricted administrative authority beyond the declared target, operations, duration, and purpose.
- **REQ-OPS-MAINT-004 — SHALL:** Maintenance authority validate the actor, target identity, active profile composition, active Release Set, applicable policy, current exceptions, and required separation of duties before mutation begins.
- **REQ-OPS-MAINT-005 — SHALL:** Planned maintenance notify affected users, operators, integrations, and dependent teams according to the target's communication contract and identify expected capability impact, start, end, recourse, and status source.
- **REQ-OPS-MAINT-006 — SHALL:** Every maintenance preflight verify target health, current authority state, active Release Set, component inventory, data ownership, storage and resource reserves, backup and recovery readiness, required artifacts, migration state, credential state, evidence path, and operator access.
- **REQ-OPS-MAINT-007 — SHALL NOT:** Maintenance begin when a required preflight is failed, blocked, stale, unresolved, or applicable to a different target, unless an authorized emergency procedure records the exact exception and compensating controls.
- **REQ-OPS-MAINT-008 — SHALL:** Maintenance preserve or create a validated return path before destructive, schema-changing, authority-changing, trust-changing, or availability-affecting work.
- **REQ-OPS-MAINT-009 — SHALL NOT:** The presence of a backup, snapshot, prior image, previous Release Set, down migration, copied volume, retained package, or recovery medium be treated as proof that rollback or recovery is safe.
- **REQ-OPS-MAINT-010 — SHALL:** Maintenance execute component mutations, schema changes, data repair, retention work, backup, restore, and export through each owning component's declared interface and lifecycle contract.
- **REQ-OPS-MAINT-011 — SHALL NOT:** A maintenance coordinator, operator script, privileged broker, database administrator, backup tool, or lifecycle service directly write across participant component authoritative stores.
- **REQ-OPS-MAINT-012 — SHALL:** System, services, governance, and knowledge updates use signed validated artifacts and activate only through a compatible complete Release Set.
- **REQ-OPS-MAINT-013 — SHALL NOT:** Manual package replacement, copied binaries, editable installations, ad hoc container images, direct filesystem edits, locally rebuilt artifacts, or unregistered scripts become active product state.
- **REQ-OPS-MAINT-014 — SHALL:** Data migrations use component-owned ordered procedures with preflight, backup requirements, compatibility windows, interruption handling, validation, rollback or forward repair, and completion evidence.
- **REQ-OPS-MAINT-015 — SHALL:** Maintenance that rotates keys, credentials, certificates, trust roots, integration tokens, or recovery factors preserve purpose separation, environment separation, revocation propagation, offline verification, rollback constraints, and post-change validation.
- **REQ-OPS-MAINT-016 — SHALL NOT:** Rollback, restore, offline import, recovery, or maintenance convenience reactivate revoked, expired, compromised, withdrawn, or superseded authority.
- **REQ-OPS-MAINT-017 — SHALL:** Resource-intensive maintenance request capacity through Resource Governor and protect interactive, critical-service, receipt, evidence, active-authority, and recovery reserves before background or bulk work.
- **REQ-OPS-MAINT-018 — SHALL NOT:** A Governance Policy Runtime approval create resource capacity, and a Resource Governor admission create business, security, lifecycle, data, publication, or maintenance authority.
- **REQ-OPS-MAINT-019 — SHALL:** Maintenance entering a reduced-service, read-only, offline, recovery, or restricted state expose that state explicitly, identify retained and unavailable capabilities, and prevent unsupported writes.
- **REQ-OPS-MAINT-020 — SHALL:** Offline maintenance use locally verified authority, artifacts, trust, revocation, policies, procedures, tests, evidence buffering, rollback, and recovery material without weaker validation.
- **REQ-OPS-MAINT-021 — SHALL NOT:** Unavailable remote services authorize silent provider substitution, external AI analysis of governed maintenance data, skipped checks, broader privilege, implicit validity extension, or direct execution of unverified material.
- **REQ-OPS-MAINT-022 — SHALL:** Maintenance scripts and tools be versioned, attributable, bounded to declared operations, non-interactive where feasible, idempotent or explicitly non-repeatable, and tested against safe representative targets.
- **REQ-OPS-MAINT-023 — SHALL:** Every maintenance step define expected state, safe retry or resumption, timeout, terminal failure, operator decision point, and cleanup behavior.
- **REQ-OPS-MAINT-024 — SHALL NOT:** A step be marked complete from process exit, command return, file presence, service restart, reboot, migration invocation, or operator observation alone when contract validation is required.
- **REQ-OPS-MAINT-025 — SHALL:** Maintenance completion validate target identity, active Release Set, component health, schema state, data consistency, policy and identity availability, resource envelope, offline envelope, critical workflows, backup readiness, recovery readiness, observability, and evidence.
- **REQ-OPS-MAINT-026 — SHALL:** A failed maintenance action retain or restore a declared valid authority state, identify every partial physical change, block unsupported mixed operation, and expose the next valid rollback, recovery, forward-repair, or restricted-state action.
- **REQ-OPS-MAINT-027 — SHALL:** Temporary maintenance access, elevated credentials, mounts, decrypted material, staging paths, override rules, firewall changes, worker capacity, and diagnostic settings be removed or returned to the declared operational posture during closure.
- **REQ-OPS-MAINT-028 — SHALL:** Maintenance logs, diagnostics, receipts, and evidence preserve stable identities, commands or procedure steps, results, reason codes, and timing while omitting secret material and minimizing governed payloads.
- **REQ-OPS-MAINT-029 — SHALL:** Critical maintenance entry, authority, backup, destructive action, migration, trust change, activation, rollback, recovery, forward repair, emergency override, cleanup, and completion transitions produce machine-readable receipts or evidence records.
- **REQ-OPS-MAINT-030 — SHALL:** Maintenance closure record actual impact, achieved result, deviations, failed or skipped checks, data-loss and downtime measures, unresolved restrictions, user-visible status, recourse, follow-up work, and next validation date.
- **REQ-OPS-MAINT-031 — SHALL:** Maintenance procedures, return paths, recovery media, backups, scripts, credentials, resource assumptions, offline dependencies, tests, and operator instructions be reviewed and exercised at the profile-declared cadence and after semantic changes.
- **REQ-OPS-MAINT-032 — SHALL:** Maintenance conformance pass only when authority, communication, preflight, ownership, artifacts, migrations, credentials, resources, offline behavior, interruption, completion, rollback or recovery, cleanup, receipts, and post-maintenance review tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Planned Maintenance Procedure

### 6.1 Propose

The maintenance owner records:

1. target and purpose;
2. maintenance classes;
3. expected benefit;
4. affected capabilities;
5. risk and impact;
6. exact artifacts or procedures;
7. required access;
8. user impact;
9. return path;
10. proposed window;
11. validation;
12. evidence.

The proposal identifies assumptions requiring validation.

### 6.2 Review impact

Review covers:

- profile and overlays;
- active Release Set;
- component ownership;
- interfaces and events;
- schemas and migrations;
- credentials and trust;
- storage and capacity;
- offline operation;
- recovery;
- integrations;
- users and dependent teams;
- support and deprecation;
- compliance and evidence.

A semantic change uses an accepted architecture or owner decision where required.

### 6.3 Approve and schedule

Approvers validate the procedure, risk, timing, return path, and separation of duties.

Scheduling reserves:

- operator availability;
- component-owner availability;
- recovery capability;
- capacity;
- communication;
- evidence path;
- expected validation time.

The event receives a stable maintenance ID.

### 6.4 Communicate

Communication identifies:

- target service or capability;
- reason;
- expected impact;
- start and end;
- read-only or unavailable periods;
- user action;
- status source;
- recourse;
- completion notice.

Security-sensitive detail is minimized.

### 6.5 Freeze conflicting work

The maintenance owner identifies incompatible concurrent work.

Examples include:

- another Release Set activation;
- overlapping migration;
- trust-root change;
- component restore;
- storage replacement;
- destructive cleanup;
- recovery test using the same target.

Conflicting work is completed, paused, or cancelled through its own contract.

### 6.6 Run preflight

Preflight validates:

- target and profile identity;
- current active-set identity;
- component health;
- storage health and reserve;
- Resource Governor capacity;
- backups and restore tests;
- last-known-good artifacts;
- migration source state;
- credentials and trust;
- offline dependencies;
- evidence path;
- maintenance credentials;
- communication readiness;
- current incidents and freezes.

Preflight results are fresh for the actual target and window.

### 6.7 Enter maintenance mode

The target enters the declared operational state:

- normal with background work paused;
- reduced service;
- read-only;
- offline;
- recovery;
- restricted.

The state is visible to components, operators, users, and monitoring as applicable.

New work that conflicts with maintenance is rejected or deferred.

### 6.8 Preserve state

Before destructive or authority-changing work, the procedure preserves:

- current Release Set;
- component versions;
- schema versions;
- relevant configuration;
- trust and credential state;
- backup state;
- current health;
- incident evidence;
- queue and job state;
- user-visible operation state.

Preservation follows classification and retention rules.

### 6.9 Execute bounded steps

Each step has:

- identifier;
- expected starting state;
- owner;
- command or operation;
- target;
- timeout;
- resource request;
- safe retry;
- success check;
- failure check;
- cleanup;
- next valid state.

Operators do not substitute an undocumented command merely because the documented step failed.

### 6.10 Validate during execution

Long or phased work validates checkpoints.

Examples include:

- inactive system slot written;
- service artifact staged;
- policy bundle loaded inactive;
- migration phase complete;
- trust update staged;
- backup completed;
- storage replacement healthy;
- projection rebuild complete.

Checkpoint success does not equal final maintenance completion.

### 6.11 Activate or switch authority

When the maintenance changes active authority, lifecycle contracts perform the atomic switch.

This can be:

- Release Set;
- system image;
- service release;
- governance bundle;
- knowledge artifact;
- resource envelope;
- credential or trust set;
- restored component state.

The active identity is recorded.

### 6.12 Validate completion

Completion validation covers:

- target and active identity;
- component health;
- data and schema;
- critical workflows;
- policy and identity;
- rights and revocation;
- resource envelope;
- offline behavior;
- integration behavior;
- backup and recovery;
- observability;
- receipts;
- user impact.

A failed completion check invokes the declared return path.

### 6.13 Exit maintenance mode

The target exits reduced or restricted state only after required health checks pass.

Deferred work resumes according to Resource Governor and component contracts.

User-visible status is updated.

### 6.14 Clean up and close

Closure removes temporary access and state, records actual impact and deviations, preserves evidence, creates follow-up work, communicates completion, and sets the next validation or maintenance date.

## 7. Corrective and Emergency Maintenance

### 7.1 Corrective maintenance

Corrective work begins from a known defect or degraded state.

It still requires:

- target identity;
- authority;
- containment;
- procedure;
- return path;
- evidence;
- completion validation.

The schedule can be accelerated, but ownership and lifecycle boundaries remain.

### 7.2 Emergency entry

Emergency maintenance is justified only when delay would materially increase harm, data loss, compromise, or unavailability.

The emergency record includes:

- condition;
- target;
- immediate risk;
- initiating actor;
- emergency authority;
- operations allowed;
- duration;
- required evidence;
- review deadline.

Emergency authority is not a general shell role.

### 7.3 Containment before repair

Containment can:

- stop writes;
- isolate a component;
- suspend credentials;
- stop activation;
- disable an integration;
- enter offline or recovery mode;
- preserve storage;
- preserve evidence;
- reserve recovery capacity.

Containment remains reversible or documented.

### 7.4 Emergency artifacts

Emergency maintenance uses prevalidated local artifacts or a verified emergency/offline bundle where possible.

Unverified material remains quarantined.

An urgent need does not make an unsigned script a product artifact.

### 7.5 Emergency credential use

Break-glass credentials are target-bound, time-bound, purpose-bound, approved as required, and fully evidenced.

After use:

- access is revoked;
- affected credentials rotate;
- temporary trust is removed;
- sessions are invalidated;
- review occurs.

### 7.6 Failure handling

If the selected repair fails, the target enters:

- rollback;
- recovery;
- forward repair;
- restricted operation;
- protected exit.

Unsupported mixed state is blocked.

### 7.7 Safe degradation table

| Failure or condition | Required response | Retained state | Prohibited response | Evidence |
| --- | --- | --- | --- | --- |
| Maintenance target mismatch | Stop before mutation | Current valid target state | Applying the procedure to a similar target | Identity result |
| Required authority fails | Keep target unchanged or contained | Existing authority | Using operator possession as approval | Authority result |
| Communication cannot complete | Delay planned impact or apply declared exception | Current service | Silent planned outage | Communication result |
| Preflight is stale or blocked | Re-run or stop | Current active state | Proceeding from old evidence | Preflight result |
| Backup is invalid | Stop destructive work or select another return path | Current data | Treating backup presence as recovery | Backup result |
| Resource reserve is insufficient | Defer or narrow maintenance | Current service and recovery reserve | Consuming critical reserve | Capacity result |
| Artifact verification fails | Reject candidate | Current active artifacts | Manual replacement | Artifact result |
| Migration partially completes | Run owner-declared repair, restore, or compatible hold | Committed valid component state | Claiming completion | Migration evidence |
| Credential rotation partially completes | Retain explicit transition or restrict affected capability | Valid old or new credentials within overlap | Silent indefinite overlap | Rotation result |
| Trust update fails | Retain prior valid trust set | Current verified authority | Partial verifier activation | Trust result |
| Service health gate fails | Roll back, repair, or recover | Last valid Release Set | Ignoring one failed critical component | Health result |
| Evidence path fails | Block critical transition | Current valid state | Unevidenced completion | Evidence result |
| Maintenance window expires | Stop new steps and choose safe pause or authorized extension | Current safe checkpoint | Unsafe interruption or silent continuation | Window result |
| Temporary access cleanup fails | Keep target restricted | Recovered service where safe | Normal-operation claim | Cleanup result |
| User-impact exceeds declaration | Update status, assess harm, and invoke recourse | Current validated state | Hiding actual impact | Impact evidence |
| Emergency repair cannot restore normal service | Enter restricted recovery or protected exit | Recoverable data and evidence | False success declaration | Recovery result |

### 7.8 Forward repair

Forward repair is used when rollback would:

- lose accepted data;
- restore revoked authority;
- reintroduce a known defect;
- violate schema compatibility;
- invalidate a newer artifact dependency;
- break restored data.

Forward repair is a separately identifiable lifecycle result.

### 7.9 Restricted completion

Maintenance can end in `completed_restricted` only when:

- the restricted state is valid;
- retained capabilities are explicit;
- unsupported writes are blocked;
- user and operator status is updated;
- follow-up has an owner and deadline;
- recovery or exit remains available.

## 8. Maintenance Domains

### 8.1 System and firmware

System maintenance validates:

- profile support;
- hardware compatibility;
- signed image or firmware authority;
- recovery environment;
- power stability;
- inactive target slot where applicable;
- boot health;
- component and Release Set compatibility.

Sovereign production nodes use immutable signed system images for ordinary system updates.

### 8.2 Services

Service maintenance uses registered artifacts and services-channel releases.

The procedure preserves component identities, interfaces, event compatibility, queues, data ownership, and health gates.

Restarting a process does not redefine the service release.

### 8.3 Governance and knowledge

Governance and knowledge maintenance validates runtime compatibility, policy or artifact authority, offline availability, rollback, and complete Release Set compatibility.

Policy or knowledge activation remains atomic at its authority boundary.

### 8.4 Databases and migrations

Each component owns its migrations.

Maintenance coordinates order and compatibility without cross-owner writes.

Empty-target, prior-version, interruption, retry, restore, rollback, and forward-repair tests are used as applicable.

### 8.5 Backups and restore tests

Backup maintenance verifies:

- owner;
- source Release Set;
- schema;
- completeness;
- retention;
- encryption;
- access;
- independent restore;
- migration target;
- evidence.

A backup job success is not a restore test.

### 8.6 Storage cleanup

Cleanup follows owner retention and artifact-retention contracts.

Preferred removal order protects:

- authoritative data;
- originals;
- active Release Set metadata;
- manifests;
- receipts;
- evidence;
- recovery material.

Reproducible caches and derivatives can be rebuilt, but only owners authorize deletion.

### 8.7 Resource envelopes

Resource maintenance stages and atomically activates a validated envelope.

Manual cgroup, container, or process limit changes remain incident containment until reconciled with a canonical envelope.

### 8.8 Credentials and trust

Credential maintenance follows generation, delivery, overlap, rotation, revocation, offline propagation, recovery, and destruction rules.

Rollback candidates are checked against current revocation state.

### 8.9 Integrations

Integration maintenance uses provider-, tenant-, destination-, environment-, and capability-scoped credentials.

Disabling an integration affects only dependent capability.

No integration is a hidden requirement for local maintenance unless the profile explicitly declares it.

### 8.10 Physical maintenance

Physical work validates:

- target hardware identity;
- power and environmental controls;
- storage redundancy or backup;
- encryption and key access;
- replacement compatibility;
- firmware authority;
- boot and recovery path;
- post-replacement health.

Removed media follows secure disposition.

## 9. Cross-System Interactions

### 9.1 Identity and Trust

Identity and Trust authenticates maintenance actors, targets, services, recovery identities, credentials, signers, and revocation state.

It does not authorize component data mutation by itself.

### 9.2 Governance Policy Runtime

Governance Policy Runtime evaluates maintenance requests involving:

- destructive operations;
- emergency access;
- exceptions;
- trust changes;
- sensitive exports;
- publication;
- data retention;
- rights and consent.

Technical preflight and lifecycle validation remain separate.

### 9.3 Resource Governor

Resource Governor admits and limits maintenance tasks.

It protects active and recovery reserves.

It does not approve the maintenance purpose or mutate component data.

### 9.4 Component owners

Each component owns its health, mutation, migration, backup, restore, retention, cleanup, and validation semantics.

The maintenance owner coordinates these contracts.

### 9.5 kOA Node Agent and privileged broker

Node Agent reports target identity, profile, Release Set, host health, storage, resources, and recovery readiness.

The privileged broker exposes only narrow approved host operations.

### 9.6 Audit Broker

Audit Broker receives critical maintenance receipts and supports selective disclosure.

Evidence buffering remains available offline according to profile.

### 9.7 Release Sets and artifacts

Maintenance activating software or policy uses complete compatible Release Sets.

Artifact staging does not change active authority.

### 9.8 Offline bundles

Offline maintenance imports verified bundles through quarantine and local validation.

Import, staging, activation, rollback, and recovery remain separate.

### 9.9 Publication and external effects

Maintenance verifies that publication, withdrawal, revocation, rights, consent, and external references remain consistent after restore or migration.

Maintenance never silently republishes restored content.

### 9.10 AI and external tools

AI tools can assist with candidate analysis or documentation using redacted non-secret inputs.

They do not receive maintenance authority, credentials, governed payloads, direct production access, lifecycle activation, or autonomous repair authority.

## 10. Decision Closure and Validation Criteria

This document is supported by the accepted decisions declared in its metadata.

A semantic maintenance change requires:

1. an accepted owner decision;
2. impact analysis across profiles, components, Release Sets, artifacts, schemas, credentials, trust, resources, offline operation, recovery, users, tests, evidence, and operations;
3. canonical contract and procedure updates;
4. complete validation before operational activation.

The following assumptions are prohibited:

- maintenance mode grants unrestricted administration;
- a maintenance ticket is technical authority;
- physical access grants data ownership;
- a root shell replaces component contracts;
- a successful command means a successful maintenance step;
- a reboot means maintenance completion;
- a service restart proves release compatibility;
- a backup proves rollback or recovery;
- a snapshot proves restore;
- a down migration proves reversal safety;
- a previous artifact is necessarily last-known-good;
- a copied package can replace a registered artifact;
- a manually edited configuration becomes canonical;
- an operator script can write several component stores directly;
- a maintenance window permits skipping preflight;
- urgency permits unsigned or unverified artifacts;
- emergency credentials can remain active after the event;
- an unavailable evidence path can be repaired after completion;
- offline operation permits weaker trust checks;
- an external provider can substitute silently;
- an AI tool can diagnose and execute production repair autonomously;
- storage pressure authorizes arbitrary data deletion;
- partial success can be reported as full success;
- cleanup is complete when the operator disconnects;
- a restricted state can be presented as normal service;
- a manual resource limit change is an active resource envelope;
- source-code defaults override the active procedure.

No active exception currently weakens a requirement in this document.

This document is conformant when:

1. it is registered as `DOC-OPS-014`, active, English, and globally scoped;
2. every canonical reference resolves or is present in the planned canonical inventory;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists when the canonical lock registry is active and applicable assertions pass;
6. every maintenance event has a stable identity, owner, target, class, scope, authority, procedure, return path, and evidence plan;
7. maintenance classes and states are explicit;
8. authority is target-, operation-, purpose-, and time-bounded;
9. planned impact and recourse are communicated;
10. preflight covers target, authority, Release Set, components, data, resources, backups, recovery, credentials, and evidence;
11. blocked or stale preflight cannot silently pass;
12. destructive work has a validated return path;
13. component mutations preserve ownership;
14. active artifacts come only from validated compatible Release Sets;
15. migrations preserve owner, compatibility, interruption, and repair contracts;
16. credential and trust work preserves purpose, environment, revocation, and offline rules;
17. resource-intensive work protects active and recovery reserves;
18. Resource Governor and Governance Policy Runtime authority remain separate;
19. reduced, restricted, offline, and recovery states are explicit;
20. offline maintenance preserves full local validation;
21. tools and scripts are versioned, attributable, bounded, and tested;
22. every step has safe retry, terminal failure, validation, and cleanup;
23. command success is never the sole completion criterion;
24. completion validates Release Set, components, data, policy, identity, resources, offline behavior, workflows, backup, recovery, observability, and evidence;
25. failure preserves or restores a declared valid state;
26. temporary access, staging, decrypted material, mounts, overrides, and diagnostics are removed;
27. logs and evidence omit secrets and minimize governed payloads;
28. critical transitions produce machine-readable receipts;
29. closure records actual impact, deviations, unresolved restrictions, recourse, and follow-up;
30. procedures and return paths pass their declared review and exercise cadence;
31. no unresolved marker, undeclared authority, cross-owner write, unregistered artifact, or false completion claim exists;
32. the active text contains the complete required section structure.

Applicable failure codes include:

```text
maintenance_identity_missing
maintenance_target_mismatch
maintenance_class_missing
maintenance_authority_invalid
maintenance_scope_exceeded
maintenance_communication_missing
maintenance_preflight_failed
maintenance_preflight_stale
maintenance_return_path_unproven
maintenance_backup_invalid
maintenance_component_owner_bypass
maintenance_unregistered_artifact
maintenance_release_set_incompatible
maintenance_migration_failed
maintenance_revoked_authority_reactivated
maintenance_resource_reserve_violated
maintenance_policy_resource_authority_collision
maintenance_offline_validation_weakened
maintenance_tool_unattributed
maintenance_step_state_invalid
maintenance_false_completion
maintenance_partial_active_state
maintenance_evidence_path_unavailable
maintenance_cleanup_incomplete
maintenance_restricted_state_unreported
maintenance_receipt_missing
maintenance_review_overdue
```

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Planned services maintenance

A sovereign node receives a scheduled services update.

Operators notify affected users, validate the complete Release Set, confirm backups and recovery, stage artifacts, run component-owned migrations, atomically activate the set, validate critical workflows, remove temporary access, and issue completion receipts.

### Example 2 — Certificate rotation

A service certificate approaches expiry.

Maintenance issues a new certificate, validates identity and audience, runs a bounded overlap, updates dependent services and offline trust state, revokes the old certificate, verifies propagation, removes temporary material, and records rotation evidence.

### Example 3 — Storage cleanup

Free storage falls toward the protected floor.

The maintenance owner pauses new large imports and derivatives. Component owners prune reproducible caches under their retention contracts. Authoritative originals, Release Set manifests, receipts, evidence, and recovery material remain protected.

### Example 4 — Failed migration

A component-owned migration fails during post-change validation.

The maintenance event does not report completion. The component retains staged evidence, invokes its repair or restore path, and the lifecycle owner preserves the previous active authority until a valid compatible state is available.

### Example 5 — Offline maintenance

An offline sovereign deployment imports a verified maintenance bundle.

The target quarantines and validates the bundle, checks all four release channels, runs local tests, stages the candidate, and activates it through a separate lifecycle action. No remote provider or AI service is required.

### Example 6 — Emergency security maintenance

A signing credential is suspected compromised.

Emergency authority suspends the credential, blocks affected activation, preserves evidence, publishes revocation through online and offline paths, rotates dependent credentials, validates retained rollback candidates, and completes post-event review.

### Example 7 — Physical disk replacement

A node reports failing storage.

Operators validate backup and restore readiness, enter restricted maintenance, replace the identified device, restore component-owned state, validate the complete Release Set and recovery path, securely dispose of removed media, and return to normal operation only after health gates pass.

### Example 8 — Restricted completion

A maintenance event restores local operation but an optional remote integration remains unavailable.

The target records `completed_restricted`, exposes the unavailable integration, retains all core local capabilities, assigns follow-up ownership, and does not present the integration as healthy.
