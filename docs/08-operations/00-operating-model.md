<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-000",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global",
    "profile_conditioned_operations"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
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
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-HW-001",
    "DEC-REL-001",
    "DEC-DOC-CHANGE-001"
  ],
  "requirement_ids": [
    "REQ-OPS-MODEL-001",
    "REQ-OPS-MODEL-002",
    "REQ-OPS-MODEL-003",
    "REQ-OPS-MODEL-004",
    "REQ-OPS-MODEL-005",
    "REQ-OPS-MODEL-006",
    "REQ-OPS-MODEL-007",
    "REQ-OPS-MODEL-008",
    "REQ-OPS-MODEL-009",
    "REQ-OPS-MODEL-010",
    "REQ-OPS-MODEL-011",
    "REQ-OPS-MODEL-012",
    "REQ-OPS-MODEL-013",
    "REQ-OPS-MODEL-014",
    "REQ-OPS-MODEL-015",
    "REQ-OPS-MODEL-016",
    "REQ-OPS-MODEL-017",
    "REQ-OPS-MODEL-018",
    "REQ-OPS-MODEL-019",
    "REQ-OPS-MODEL-020",
    "REQ-OPS-MODEL-021",
    "REQ-OPS-MODEL-022",
    "REQ-OPS-MODEL-023",
    "REQ-OPS-MODEL-024",
    "REQ-OPS-MODEL-025",
    "REQ-OPS-MODEL-026",
    "REQ-OPS-MODEL-027",
    "REQ-OPS-MODEL-028",
    "REQ-OPS-MODEL-029",
    "REQ-OPS-MODEL-030",
    "REQ-OPS-MODEL-031",
    "REQ-OPS-MODEL-032",
    "REQ-OPS-MODEL-033",
    "REQ-OPS-MODEL-034",
    "REQ-OPS-MODEL-035",
    "REQ-OPS-MODEL-036",
    "REQ-OPS-MODEL-037",
    "REQ-OPS-MODEL-038",
    "REQ-OPS-MODEL-039",
    "REQ-OPS-MODEL-040",
    "REQ-OPS-MODEL-041",
    "REQ-OPS-MODEL-042",
    "REQ-OPS-MODEL-043",
    "REQ-OPS-MODEL-044",
    "REQ-OPS-MODEL-045",
    "REQ-OPS-MODEL-046",
    "REQ-OPS-MODEL-047",
    "REQ-OPS-MODEL-048"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-DEV-001",
    "LOCK-DEV-002",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-DEV-005",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-DOC-015",
    "LOCK-DOC-020",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-008",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-DEV-016",
    "DOC-LIFE-013",
    "DOC-LIFE-015",
    "DOC-LIFE-016",
    "DOC-LIFE-019",
    "DOC-SEC-001",
    "DOC-SEC-012"
  ],
  "tags": [
    "operations",
    "operating-model",
    "service-ownership",
    "health",
    "readiness",
    "slo",
    "capacity",
    "maintenance",
    "incident-response",
    "backup",
    "restore",
    "release-operations",
    "offline-operations",
    "runbooks",
    "evidence"
  ]
}
KOA:DOC-META:END -->

# Operating Model

## 1. Purpose

This document defines how kOA is operated after deployment without weakening its component, profile, security, data, and lifecycle boundaries.

The operating model coordinates:

- routine service operation;
- health and readiness;
- capability-level objectives;
- capacity and resource control;
- maintenance;
- release and configuration changes;
- backup, restore, and credible exit;
- incidents and vulnerabilities;
- external integrations;
- offline operation;
- operational handoffs;
- automation and evidence;
- decommissioning.

The common operational control loop is:

```text
observe authoritative and derived state
        ↓
decide through the owning authority
        ↓
act through a registered interface or lifecycle transition
        ↓
verify actual resulting state
        ↓
retain the required evidence
```

A runbook describes how to carry out this loop.

It does not create permission.

An operator can coordinate several owners without becoming the owner of their component data, policy, identity, release state, resource decisions, or privileged interfaces.

### 1.1 Operating objectives

The operating objectives are:

1. keep declared capabilities available within their profile-specific objectives;
2. preserve authoritative state and ownership;
3. expose degraded and blocked states accurately;
4. maintain known-good recovery;
5. prevent local operational convenience from becoming architecture;
6. keep optional external dependencies removable;
7. produce evidence proportionate to the transition;
8. support independent restore and credible exit.

### 1.2 Operating principles

The operating model follows these principles:

- capability before process uptime;
- readiness before traffic;
- owner before action;
- policy before privilege;
- resource admission before heavy execution;
- verification after mutation;
- evidence after critical transition;
- known-good state before risk-bearing change;
- capability-scoped degradation;
- no silent substitution;
- profiles strengthen behavior without changing ownership;
- current contracts override recipes and historical practice.

## 2. Scope

### 2.1 Included environments

This document applies to:

- user endpoints;
- developer workstations;
- sovereign Linux nodes;
- sovereign hubs;
- build farms;
- control planes;
- high-assurance overlays;
- sovereign-offline overlays;
- appliance-shell overlays;
- recovery environments;
- staging environments;
- production environments;
- isolated test environments when they make operational or conformance claims.

### 2.2 Included activities

The operating model covers:

- startup and shutdown;
- dependency ordering;
- service readiness;
- routine checks;
- alerting;
- capacity planning;
- workload shedding;
- configuration and release changes;
- migrations;
- key and credential operations;
- backup and restore;
- offline import and export;
- incident response;
- integration enablement and outage handling;
- conformance checks;
- handoff;
- retirement and decommissioning.

### 2.3 Excluded detail

This document does not define:

- exact staffing schedules;
- one universal support model;
- exact SLO target values;
- exact alert thresholds;
- exact monitoring product;
- exact service-manager commands;
- exact backup schedule;
- exact incident-severity enum;
- exact maintenance cadence;
- exact escalation contacts;
- vendor-specific deployment steps.

Those details belong to active profile contracts, component contracts, operations registries, runbooks, schedules, evidence definitions, and local operating agreements.

### 2.4 Profiles are not operating modes

Profiles define deployment and assurance contracts.

They are not transient operating states.

A deployment can be in normal, degraded, maintenance, recovery, or stopped operational condition while retaining the same effective profile.

Changing profile composition is a governed configuration and lifecycle change rather than an informal mode switch.

### 2.5 Conceptual operational conditions

The following conditions are explanatory:

| Condition | Meaning |
| --- | --- |
| Normal | Required profile capabilities are ready and within objectives |
| Degraded | One or more capabilities are unavailable or reduced, with impact and safe behavior visible |
| Maintenance | A bounded authorized maintenance procedure is active |
| Blocked | A required authority, dependency, compatibility, or evidence condition prevents an operation |
| Recovery | The environment is restoring known-good authority and state |
| Quarantined | A component, artifact, integration, or data transfer is isolated from normal operation |
| Stopped | The selected service or environment is intentionally inactive |

Canonical component and lifecycle states remain in their machine-readable contracts.

## 3. Canonical References

### 3.1 Active authority

```text
generated/authority-manifest.json
generated/decision-index.json
generated/requirements-index.json
generated/assertion-index.json
generated/decision-index.json
```

### 3.2 System and components

```text
contracts/system.contract.json
generated/component-catalog.json
generated/component-catalog.json
contracts/components/*.component.json
```

Component contracts own interfaces, readiness, data, state, failure, recovery, and compatibility.

### 3.3 Profiles

```text
generated/profile-catalog.json
contracts/profiles/*.profile.json
```

Profiles own topology, selection, resources, locality, assurance, offline behavior, and implementation choices.

### 3.4 Lifecycle

```text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/artifact-contracts/release-set.schema.json
contracts/artifact-contracts/*.schema.json
```

Lifecycle contracts own artifact identity, publication, staging, activation, rollback, forward repair, retention, and retirement.

### 3.5 Integrations and evidence

```text
contracts/integration-types.contract.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
```

### 3.6 Related documents

```text
05-development/16-development-to-release-transition.md
06-lifecycle/13-activation-and-verification.md
06-lifecycle/15-data-schema-evolution.md
06-lifecycle/16-forward-repair.md
06-lifecycle/19-artifact-retention.md
07-security/01-security-baseline.md
07-security/12-external-integration-classification.md
```

## 4. Model and Responsibilities

### 4.1 Responsibility model

Operational roles coordinate existing owners.

| Responsibility | Primary authority |
| --- | --- |
| Component behavior and owned data | Component owner and component contract |
| Profile composition and operating envelope | Profile owner and profile contract |
| Resource admission and scheduling | Resource Governor or profile-defined equivalent |
| Governance decisions | Governance Policy Runtime where selected |
| Identity and trust | Identity and Trust |
| Privileged node operations | kOA Node Agent and registered privileged boundary |
| Artifact and release lifecycle | Artifact and release owners |
| External publication | Publication Gateway |
| UCKK dimension admission | UCKK Dimension Gateway and UCKK Platform |
| Security controls and incident containment | Security owner with affected owners |
| Backup and restore of component state | Owning component and profile recovery contract |
| Evidence handling | Audit Broker and evidence owner |
| Operational coordination | Designated operator or incident coordinator |

An operational coordinator can request and sequence work.

The coordinator does not absorb the primary authority of the owners involved.

### 4.2 Operational roles

A deployment can assign roles such as:

- service operator;
- component owner;
- profile owner;
- release operator;
- security operator;
- data or domain owner;
- integration owner;
- backup and recovery operator;
- incident coordinator;
- evidence reviewer;
- support operator.

Role assignments identify:

- scope;
- environment;
- tenant or security domain;
- permitted interfaces;
- approval conditions;
- time bounds;
- evidence;
- delegation;
- review;
- revocation.

A role name alone does not create access.

### 4.3 Inventory and declared state

Operations maintain an inventory sufficient to reconstruct the active environment.

The inventory includes:

- node or environment identity;
- effective primary profile and overlays;
- active Release Set;
- active channel artifact versions;
- component and contract versions;
- policy-set version;
- trust and revocation state;
- installed and active knowledge and language artifacts;
- owned storage domains;
- database and schema state;
- integrations and adapters;
- secret and key classes without secret values;
- backup and recovery relationships;
- known degradation;
- active exceptions;
- current incidents and changes.

The inventory is derived from canonical authority and actual runtime state.

It is not a replacement authority registry.

### 4.4 Health and readiness

Health and readiness answer different questions.

| Signal | Question |
| --- | --- |
| Process health | Is the process responsive? |
| Dependency health | Are declared dependencies reachable or locally available? |
| Contract readiness | Can the component satisfy its critical contract? |
| Read capability | Can it safely read required owned state? |
| Write capability | Can it safely perform owned mutations? |
| Governed capability | Can required identity, policy, consent, or privilege decisions resolve? |
| Publication or execution capability | Can the controlled gateway or executor complete its operation? |
| Recovery readiness | Are known-good state, backups, keys, artifacts, and procedures available? |
| Degraded safety | Can the component remain available without fabricating authority? |

Detailed health information is restricted according to sensitivity.

Public status exposes only minimized capability information.

### 4.5 Capability-level objectives

Objectives are defined by capability and profile.

Examples include:

- local session start;
- local navigation;
- critical Orgo workflows;
- Konnaxion read or update capability;
- active Kristal query;
- policy evaluation;
- UCKK local operation;
- publication;
- release activation;
- rollback;
- backup completion;
- restore success;
- offline continuity;
- integration availability.

A safe policy denial caused by an invalid request is not automatically an availability failure.

An unexplained denial, unstable reason code, or inability to inspect the blocked condition can be an operational failure.

### 4.6 Operating cadence

A deployment defines cadences appropriate to its profile.

Typical operating cadences include:

- continuous health and readiness;
- event-driven alerts;
- shift or daily review;
- scheduled capacity review;
- backup and replication review;
- periodic restore tests;
- periodic conformance and security tests;
- vulnerability review;
- credential and key review;
- release and retention review;
- credible-exit exercises.

Cadence does not replace event-triggered response.

A severe trust, security, data, release, or recovery condition is handled when detected.

### 4.7 Routine operating review

A routine review considers:

- current capability status;
- active and recent alerts;
- degraded services;
- queue age and retry state;
- resource saturation;
- storage and backup status;
- trust and revocation freshness;
- policy readiness;
- active releases and pending changes;
- migrations;
- integration availability;
- evidence delivery;
- active exceptions;
- unresolved incidents;
- upcoming maintenance;
- operator handoff.

The review records only information necessary for coordination and accountability.

### 4.8 Observability model

Operations use four signal families:

#### Metrics

Metrics cover capability availability, latency, queue depth, retries, resource use, storage pressure, verification failures, activation outcomes, backup and restore results, and integration state.

#### Logs

Structured logs contain time, component, environment, stage, outcome, stable error code, dependency, attempt, duration, and correlation identity where permitted.

#### Traces

Traces can link registered online service calls.

Trace propagation preserves tenant and security-domain separation.

#### Receipts

Receipts are durable evidence for policy, privilege, publication, release, migration, recovery, integration, and other critical transitions.

Receipts are not debugging logs.

### 4.9 Alerting

Alerts are tied to impact.

High-priority conditions can include:

- trust or revocation failure;
- policy authority unavailable;
- repeated activation or rollback failure;
- backup or restore failure;
- audit or receipt gap;
- cross-tenant or cross-domain anomaly;
- suspected key compromise;
- unauthorized integration traffic;
- data-integrity failure;
- migration inconsistency;
- resource exhaustion affecting critical capability;
- offline recovery incompleteness.

Alert closure requires verification rather than disappearance of one metric.

### 4.10 Resource and capacity operations

Resource planning uses profile envelopes and workload classes.

Operations consider:

- CPU;
- memory;
- I/O;
- storage;
- queue depth;
- concurrency;
- process and worker count;
- network;
- backup windows;
- restore capacity;
- release staging space;
- retained known-good artifacts.

Resource Governor remains separate from Governance Policy Runtime.

An operation can be authorized and still deferred for resource reasons.

### 4.11 Workload priority

A profile defines priority among capabilities.

A typical protected order is:

1. identity and trust;
2. governance policy;
3. critical component transactions;
4. local navigation and accessibility;
5. recovery and known-good state;
6. required evidence durability;
7. routine user workloads;
8. synchronization and background work;
9. optional integrations;
10. optional workbenches and heavy enrichment.

The exact order belongs to the active profile and resource policy.

### 4.12 Maintenance

Maintenance is a bounded operational procedure.

It identifies:

- scope;
- owner;
- affected capabilities;
- target profile and release;
- start and exit conditions;
- expected degradation;
- user or operator notice;
- backup and recovery readiness;
- policy and privilege;
- test plan;
- rollback or repair;
- evidence.

Maintenance does not authorize mixed or partial authority.

### 4.13 Change and release operations

Operational changes follow the development-to-release and lifecycle process.

Changes are classified before execution.

Examples include:

- configuration;
- component artifact;
- policy bundle;
- language or knowledge artifact;
- system image;
- integration manifest;
- credential or trust configuration;
- schema or data migration;
- resource envelope;
- profile composition.

A current implementation file or manual command is not a release authority.

### 4.14 Staging and activation

Staging prepares complete inactive state.

Operations verify:

- artifact identity;
- provenance;
- signatures and trust;
- revocation;
- profile and component compatibility;
- Release Set;
- migration;
- resource capacity;
- known-good predecessor;
- evidence path.

Activation changes the active pointer last.

Post-activation acceptance determines whether the new release remains active.

### 4.15 Configuration drift

Declared configuration and actual state are compared.

Drift can include:

- changed service definitions;
- changed network rules;
- changed package or image identity;
- changed secrets reference;
- changed profile selection;
- changed resource limits;
- changed database or schema state;
- changed trust or policy;
- changed integration endpoint.

Unexpected drift is classified and reconciled.

It is not normalized into authority merely because it has existed for some time.

### 4.16 Backup

Backup scope follows component ownership and profile recovery objectives.

A backup can include:

- component-owned authoritative state;
- identity and delegation state;
- policy bundles;
- trust and revocation state;
- active and previous Release Sets;
- required artifacts;
- rights and consent records;
- selected evidence;
- encryption and key references;
- restore metadata;
- migration state.

Derived caches can be rebuilt rather than backed up when their contracts permit it.

### 4.17 Restore and credible exit

Restore occurs on a clean compatible environment.

A credible-exit exercise proves that a declared tenant or environment can be:

1. exported;
2. transferred under custody;
3. verified independently;
4. restored on a clean compatible environment;
5. migrated or repaired;
6. reindexed where needed;
7. returned to authorized workflows;
8. operated without the former operator.

Private signing keys are transferred only under an explicit protected handover contract.

Otherwise, replacement trust is enrolled.

### 4.18 Incident response

Incident classes can include:

- host or service compromise;
- key or credential compromise;
- malicious or defective release;
- erroneous policy;
- data disclosure;
- cultural-rights violation;
- identity fraud;
- denial of service;
- integration misuse;
- lost or stolen node;
- backup or recovery failure;
- artifact or provenance failure.

Incident response coordinates affected owners while preserving their authority boundaries.

### 4.19 Containment

Containment can:

- isolate a service;
- isolate a tenant or security domain;
- disable an integration;
- revoke a credential or key;
- freeze a release channel;
- quarantine an artifact;
- switch to known-good state;
- enter offline or hermetic behavior;
- restrict publication;
- shed optional workloads.

Containment avoids unnecessary evidence destruction and unrelated capability loss.

### 4.20 Incident communication

Operational communication records:

- confirmed facts;
- suspected scope;
- affected capabilities;
- known unaffected capabilities;
- containment;
- user action;
- temporary safeguards;
- next review;
- unresolved questions.

Updates do not claim unsupported certainty.

Public, tenant, operator, regulator, and restricted-evidence audiences receive different permitted representations.

### 4.21 Recovery acceptance

Recovery is complete only after:

- clean or verified runtime state;
- trust and revocation checks;
- policy readiness;
- active artifact verification;
- data-integrity and migration checks;
- credential rotation where required;
- component readiness;
- profile conformance;
- critical user or operator journeys;
- recovery evidence.

Restored services do not rejoin normal traffic solely because processes start.

### 4.22 Vulnerability operations

A vulnerability record identifies:

- affected component or artifact;
- dependency;
- versions;
- profiles;
- exploitability;
- active deployments;
- retained deployments;
- mitigation;
- owner;
- update, rollback, revocation, or repair;
- evidence;
- closure.

Emergency remediation still preserves change identity, validation, and recovery.

### 4.23 Integration operations

Integration operation includes:

- registry and manifest validation;
- profile applicability;
- credential health;
- endpoint policy;
- provider terms;
- data-transfer controls;
- timeout and rate behavior;
- receipts;
- degraded state;
- removal.

External AI remains optional and user-triggered.

Suno and Gamma remain explicit external UCKK-related adapters.

Ariane external voice remains separate from local navigation.

SenTient remains a local isolated workbench rather than an external integration.

### 4.24 Offline operations

Offline operation has local closure for the profile's declared capabilities.

Operations verify:

- local identity and trust;
- local revocation state;
- local policy;
- local artifacts and Release Sets;
- local evidence;
- known-good predecessor;
- backups and recovery;
- operator documentation;
- clock and expiry behavior;
- removable-media procedures.

Internet-dependent capability is visibly unavailable.

It is not silently queued or redirected unless its contract explicitly defines safe bounded behavior.

### 4.25 Operational handoff

A handoff is a bounded transfer of coordination responsibility.

It identifies:

- active incidents;
- active maintenance;
- active changes and release candidates;
- degraded capabilities;
- unresolved alerts;
- capacity risks;
- backup and restore status;
- key and credential operations;
- active exceptions;
- pending approvals;
- next safe actions;
- escalation conditions.

Handoffs use references and summaries rather than copying unrestricted evidence.

### 4.26 Runbooks

A runbook identifies:

- purpose;
- owner;
- profiles;
- affected components;
- prerequisites;
- required authority;
- safe observations;
- actions;
- verification;
- evidence;
- rollback or repair;
- stop conditions;
- escalation;
- last validation.

A runbook is reviewed after relevant contract, profile, component, release, or security changes.

### 4.27 Automation

Automation can perform repetitive operational work.

Risk-bearing automation includes explicit:

- identity;
- profile;
- input schema;
- scope;
- preconditions;
- idempotency;
- retry behavior;
- timeout;
- cancellation;
- dry-run or preview where practical;
- verification;
- evidence;
- rollback or repair;
- terminal states.

Automation does not infer permission from missing data or a successful previous run.

### 4.28 Conformance and synthetic checks

Operational checks test declared capabilities without corrupting authoritative state.

Examples include:

- active policy vectors;
- language and knowledge pack loading;
- local navigation;
- publication redaction;
- queue durability;
- backup readability;
- restore prerequisites;
- known-good release availability;
- offline trust freshness;
- integration disablement;
- cross-tenant denial;
- evidence access controls.

Synthetic state is isolated and clearly identified.

### 4.29 Exception operations

Active operational exceptions are reviewed for:

- owner;
- scope;
- affected requirement or lock;
- profiles;
- expiry;
- closure condition;
- compensating controls;
- tests;
- evidence.

An exception does not become normal operating procedure.

### 4.30 Decommissioning

Decommissioning closes the full dependency set.

It can include:

- traffic;
- service identity;
- credentials and keys;
- integrations;
- schedules;
- privileged operations;
- network rules;
- storage;
- backups;
- retained artifacts;
- audit and evidence;
- monitoring;
- alerts;
- runbooks;
- profile and inventory entries.

Data and artifacts follow their owners' retention and deletion contracts.

An identifier remains reserved where lifecycle authority requires it.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-MODEL-001,REQ-OPS-MODEL-002,REQ-OPS-MODEL-003,REQ-OPS-MODEL-004,REQ-OPS-MODEL-005,REQ-OPS-MODEL-006,REQ-OPS-MODEL-007,REQ-OPS-MODEL-008,REQ-OPS-MODEL-009,REQ-OPS-MODEL-010,REQ-OPS-MODEL-011,REQ-OPS-MODEL-012,REQ-OPS-MODEL-013,REQ-OPS-MODEL-014,REQ-OPS-MODEL-015,REQ-OPS-MODEL-016,REQ-OPS-MODEL-017,REQ-OPS-MODEL-018,REQ-OPS-MODEL-019,REQ-OPS-MODEL-020,REQ-OPS-MODEL-021,REQ-OPS-MODEL-022,REQ-OPS-MODEL-023,REQ-OPS-MODEL-024,REQ-OPS-MODEL-025,REQ-OPS-MODEL-026,REQ-OPS-MODEL-027,REQ-OPS-MODEL-028,REQ-OPS-MODEL-029,REQ-OPS-MODEL-030,REQ-OPS-MODEL-031,REQ-OPS-MODEL-032,REQ-OPS-MODEL-033,REQ-OPS-MODEL-034,REQ-OPS-MODEL-035,REQ-OPS-MODEL-036,REQ-OPS-MODEL-037,REQ-OPS-MODEL-038,REQ-OPS-MODEL-039,REQ-OPS-MODEL-040,REQ-OPS-MODEL-041,REQ-OPS-MODEL-042,REQ-OPS-MODEL-043,REQ-OPS-MODEL-044,REQ-OPS-MODEL-045,REQ-OPS-MODEL-046,REQ-OPS-MODEL-047,REQ-OPS-MODEL-048 -->
- **REQ-OPS-MODEL-001 — SHALL:** Every operating responsibility resolve to an active component owner, profile owner, lifecycle owner, security owner, data owner, or explicitly delegated operational role.
- **REQ-OPS-MODEL-002 — SHALL:** Every operational action identify the effective profile, active Release Set, affected component contracts, target environment, actor, purpose, and correlation identity.
- **REQ-OPS-MODEL-003 — SHALL NOT:** An operator, administrator, runbook, automation, support tool, or monitoring system create authority absent from active contracts and policy.
- **REQ-OPS-MODEL-004 — SHALL NOT:** Routine operations write directly to another component's authoritative source tables or equivalent mutable source state.
- **REQ-OPS-MODEL-005 — SHALL:** Operational state changes use registered component interfaces, lifecycle transitions, governed gateways, or closed privileged operations.
- **REQ-OPS-MODEL-006 — SHALL:** Every operational procedure use the control loop observe, decide, act, verify, and evidence.
- **REQ-OPS-MODEL-007 — SHALL:** Every active service expose health and readiness information appropriate to its component contract and profile.
- **REQ-OPS-MODEL-008 — SHALL NOT:** Process liveness, container status, service-manager status, or network reachability be treated as proof of contract readiness.
- **REQ-OPS-MODEL-009 — SHALL:** Service-level objectives and alerts be defined by user-visible or governance-relevant capability and effective profile rather than service uptime alone.
- **REQ-OPS-MODEL-010 — SHALL:** Operational inventories identify active profiles, Release Sets, component and artifact versions, trust and policy versions, storage domains, integrations, and recovery dependencies.
- **REQ-OPS-MODEL-011 — SHALL:** Routine operating checks verify identity, trust, policy, readiness, capacity, storage, queues, backups, evidence paths, release state, and known degradation.
- **REQ-OPS-MODEL-012 — SHALL:** Maintenance windows declare affected capabilities, owners, approvals, user impact, entry conditions, rollback or forward-repair behavior, evidence, and exit criteria.
- **REQ-OPS-MODEL-013 — SHALL NOT:** A maintenance window suspend component ownership, tenant isolation, security policy, evidence requirements, or release compatibility.
- **REQ-OPS-MODEL-014 — SHALL:** Resource capacity and workload priority be enforced through Resource Governor or the active profile's equivalent resource authority.
- **REQ-OPS-MODEL-015 — SHALL NOT:** Resource pressure be resolved by bypassing governance policy, granting undeclared privilege, merging data domains, or disabling required recovery capability.
- **REQ-OPS-MODEL-016 — SHALL:** Resource exhaustion shed optional and lower-priority work before identity, policy, critical workflows, local navigation, recovery, and evidence durability.
- **REQ-OPS-MODEL-017 — SHALL:** Operational logs, metrics, traces, and receipts use stable correlation identities and exclude secrets and unrestricted protected payloads by default.
- **REQ-OPS-MODEL-018 — SHALL:** Debugging logs, operational telemetry, audit evidence, and durable decision or transition receipts remain distinct evidence classes.
- **REQ-OPS-MODEL-019 — SHALL:** Alerts identify the affected capability, scope, active release, first observed time, current state, user or governance impact, and next safe action.
- **REQ-OPS-MODEL-020 — SHALL NOT:** A degraded state, unresolved alert, stale dependency, or failed control be hidden by reporting only aggregate healthy status.
- **REQ-OPS-MODEL-021 — SHALL:** Operational changes be classified and follow the accepted change, impact, validation, release, migration, and activation process applicable to their semantics.
- **REQ-OPS-MODEL-022 — SHALL NOT:** Configuration drift, emergency edits, mutable tags, local patches, or undocumented host changes become durable production state.
- **REQ-OPS-MODEL-023 — SHALL:** Published artifacts and configurations remain inactive until complete compatible staging and atomic activation succeed.
- **REQ-OPS-MODEL-024 — SHALL NOT:** Operations expose partial system, service, governance, knowledge, schema, policy, or documentation authority as an active release.
- **REQ-OPS-MODEL-025 — SHALL:** Every risk-bearing change preserve a verified previous known-good state or a tested forward-repair path when rollback is unsafe.
- **REQ-OPS-MODEL-026 — SHALL:** Persistent-state migrations execute through the owning component's migration contract with declared backup, ordering, interruption, verification, rollback boundary, and forward repair.
- **REQ-OPS-MODEL-027 — SHALL:** Backups preserve declared component ownership, tenant or domain scope, artifact and Release Set identity, encryption, trust, policy, migration, retention, and restore metadata.
- **REQ-OPS-MODEL-028 — SHALL:** Restore capability be demonstrated on a clean compatible environment at the frequency required by the effective profile and data class.
- **REQ-OPS-MODEL-029 — SHALL NOT:** The existence of backup bytes, snapshots, mirrors, or archives be treated as proof of successful restore.
- **REQ-OPS-MODEL-030 — SHALL:** Recovery verify identity, integrity, trust, profile, Release Set, component compatibility, data ownership, migration state, key availability, readiness, and evidence before normal traffic resumes.
- **REQ-OPS-MODEL-031 — SHALL:** Incident response follow detect, classify, contain, preserve evidence, decide, revoke or repair, communicate, recover, review, and corrective-action closure.
- **REQ-OPS-MODEL-032 — SHALL:** Incident containment preserve evidence and unrelated capabilities while limiting affected identities, components, artifacts, integrations, channels, tenants, or security domains.
- **REQ-OPS-MODEL-033 — SHALL:** Emergency and break-glass actions be explicit, time-bounded, capability-bounded, strongly authenticated, evidenced, reviewed, and closed.
- **REQ-OPS-MODEL-034 — SHALL:** Incident communications distinguish confirmed facts, suspected scope, affected capabilities, safeguards, required user action, and unresolved questions.
- **REQ-OPS-MODEL-035 — SHALL NOT:** Operations claim certainty, full containment, complete deletion, complete recovery, or absence of impact beyond available evidence.
- **REQ-OPS-MODEL-036 — SHALL:** Vulnerabilities, key compromises, defective releases, policy failures, privacy incidents, cultural-rights violations, capacity failures, and recovery failures have explicit owners and terminal dispositions.
- **REQ-OPS-MODEL-037 — SHALL:** Optional integrations and external AI surfaces be operated as removable capability-scoped dependencies with explicit credentials, network policy, provider terms, receipts, and degraded behavior.
- **REQ-OPS-MODEL-038 — SHALL NOT:** Failure of ChatGPT, Suno, Gamma, Ariane external voice, SenTient, or another optional surface activate a silent provider, local AI, weaker policy, or direct authoritative fallback.
- **REQ-OPS-MODEL-039 — SHALL:** Offline-capable profiles retain local trust, revocation, policy, artifacts, Release Sets, receipts, recovery material, operator documentation, and required previous known-good state.
- **REQ-OPS-MODEL-040 — SHALL:** Offline and removable-media imports use custody records, quarantine, bounded parsing, verification, compatibility checks, inactive staging, explicit activation, and receipts.
- **REQ-OPS-MODEL-041 — SHALL:** Operational handoffs record active incidents, changes, degradations, exceptions, capacity risks, backup or restore status, pending approvals, and next safe actions.
- **REQ-OPS-MODEL-042 — SHALL:** Operational automation be idempotent where repeatable, bounded, cancellable where applicable, profile-aware, dry-run capable for risk-bearing actions where practical, and verifiable after execution.
- **REQ-OPS-MODEL-043 — SHALL NOT:** Automation interpret ambiguous state as permission to delete, migrate, publish, activate, revoke, rotate, restore, or grant privilege.
- **REQ-OPS-MODEL-044 — SHALL:** Periodic conformance and synthetic checks bind the exact profile, Release Set, component versions, test vector, environment, result, evidence, and active exceptions.
- **REQ-OPS-MODEL-045 — SHALL NOT:** A skipped, unavailable, blocked, incomplete, stale, or manually asserted operational check be represented as passing.
- **REQ-OPS-MODEL-046 — SHALL:** Decommissioning close traffic, credentials, integrations, schedules, privileged paths, storage, backups, retention, monitoring, alerts, documentation, and evidence without affecting unrelated owners.
- **REQ-OPS-MODEL-047 — SHALL:** Credible-exit and sovereignty restore exercises prove that declared tenants or environments can be exported, restored, verified, and operated without dependence on the former operator.
- **REQ-OPS-MODEL-048 — SHALL:** A semantic change to operational authority, roles, health, SLOs, capacity, maintenance, change control, backup, recovery, incident response, automation, offline operation, or decommissioning use an accepted owner decision and complete impact analysis.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Begin an operating shift or review period

1. Resolve the environment and effective profile.
2. verify operator identity and role scope.
3. read the previous handoff.
4. resolve active incidents, changes, maintenance, exceptions, and degradations.
5. verify active Release Set and recent activation state.
6. review health, readiness, alerts, capacity, storage, queues, backups, and evidence paths.
7. verify trust, revocation, policy, and integration status.
8. identify required actions and owners.
9. record the new handoff or operating review.
10. escalate any unresolved authority or critical recovery gap.

### 6.2 Start a node or service set

1. Identify node, profile, and selected Release Set.
2. verify booted or installed artifact identity.
3. verify storage and key availability.
4. start dependencies in declared order.
5. evaluate process health.
6. evaluate contract readiness.
7. verify identity, policy, resource, storage, and evidence dependencies.
8. expose interfaces only after readiness passes.
9. record degraded capabilities explicitly.
10. produce startup evidence where required.

### 6.3 Perform routine maintenance

1. Open the maintenance record.
2. identify scope, owners, approvals, release, and expected impact.
3. verify backup and known-good state.
4. enter the declared maintenance condition.
5. stop or quiesce affected work safely.
6. perform actions through registered interfaces.
7. verify each resulting state.
8. run maintenance acceptance checks.
9. restore normal capability or execute rollback or repair.
10. close the maintenance record with evidence.

### 6.4 Apply an operational change

1. Classify the change.
2. resolve the accepted decision and impact report where required.
3. produce a release candidate or governed configuration candidate.
4. validate component, profile, security, migration, and recovery effects.
5. publish the immutable artifact or configuration.
6. assemble or update the compatible Release Set.
7. stage complete inactive state.
8. obtain activation authority.
9. activate atomically.
10. run post-activation acceptance.
11. retain or restore known-good state.
12. record final disposition.

### 6.5 Respond to resource pressure

1. Identify affected capability and resource.
2. resolve the active profile resource policy.
3. stop new optional or low-priority work.
4. bound retries and queue admission.
5. protect identity, policy, recovery, critical workflows, and evidence.
6. scale or redistribute only through profile-permitted mechanisms.
7. verify that no ownership or security boundary was weakened.
8. report user-visible degradation.
9. recover gradually with bounded replay.
10. record the event and corrective capacity action.

### 6.6 Verify backup and restore

1. Select data classes, components, profile, and Release Set.
2. verify backup identity, encryption, integrity, and ownership.
3. provision a clean compatible restore environment.
4. restore trust, policy, artifacts, and component-owned state in declared order.
5. execute migrations or repair.
6. rebuild derived indexes and caches.
7. verify data authority and tenant or domain separation.
8. run readiness and critical workflow checks.
9. record RPO and RTO results where defined.
10. retain restore evidence and corrective actions.

### 6.7 Handle an incident

1. Detect and record the condition.
2. classify severity, scope, owners, and affected capabilities.
3. preserve evidence.
4. contain identities, services, integrations, artifacts, channels, or domains.
5. resolve emergency policy and privilege.
6. revoke, roll back, repair, or isolate.
7. communicate confirmed facts and uncertainty.
8. restore through verified known-good state.
9. run acceptance checks.
10. close temporary authority.
11. perform post-incident review.
12. track corrective decisions, artifacts, tests, and evidence to completion.

### 6.8 Handle an optional integration outage

1. Mark the integration capability unavailable.
2. stop new requests.
3. identify pending and indeterminate operations.
4. reconcile provider-side actions where required.
5. preserve native and local capabilities.
6. report explicit user-visible status.
7. avoid silent alternate provider or local AI fallback.
8. recover credential, endpoint, or provider state.
9. rerun integration readiness checks.
10. require a new explicit request when the manifest specifies it.
11. record degradation and recovery evidence.

### 6.9 Import an offline release

1. Receive media under custody.
2. quarantine the media and bundle.
3. inventory contents under parser and resource limits.
4. verify identity, integrity, provenance, signatures, trust, and revocation.
5. verify downgrade and compatibility state.
6. verify target profile and local resource envelope.
7. stage the complete Release Set.
8. verify backup and rollback or repair readiness.
9. obtain activation authority.
10. activate atomically.
11. run local post-activation acceptance.
12. retain local receipts and recovery material.

### 6.10 Decommission a component or environment

1. Resolve owners and retained dependencies.
2. stop new work.
3. drain, cancel, or reconcile pending operations.
4. remove traffic and schedules.
5. revoke identities, credentials, keys, and integration access as applicable.
6. export or retain data and artifacts through their owner contracts.
7. close privileged and network paths.
8. remove services and profile selection.
9. update monitoring, alerts, runbooks, and inventories.
10. verify unrelated capabilities.
11. retain required historical evidence.
12. close the decommissioning record.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior | Blocked behavior |
| --- | --- | --- | --- |
| Effective profile cannot be resolved | Keep affected operations blocked | Existing known-good state | New profile-dependent action |
| Active Release Set identity is unknown | Freeze risk-bearing changes | Current service state where safe | Activation, migration, restore claim |
| Process is healthy but contract readiness fails | Keep service out of traffic | Diagnostics and unaffected services | Dependent capability |
| Policy runtime is unavailable where required | Block governed transitions | Unaffected non-governed capability | New governed action |
| Resource Governor is unavailable | Defer new resource-sensitive work | Existing state and lightweight capability | New heavy work |
| Privileged broker is unavailable | Block host mutation | Unprivileged workflows | Privileged operation |
| Evidence path is unavailable | Apply evidence policy and preserve local evidence where permitted | Existing state | Receipt-critical transition |
| Backup completes but restore validation fails | Mark recovery readiness failed | Current active state and backup evidence | Backup-success claim |
| Previous known-good release is incomplete | Block risk-bearing activation | Current active release | Change requiring rollback protection |
| Migration preflight fails | Preserve source state | Current compatible release | Migration and activation |
| Post-activation readiness fails | Roll back or forward repair | Recoverable state | Release acceptance |
| Capacity threshold is exceeded | Shed optional work and bound queues | Critical and reserved capabilities | New low-priority work |
| External integration fails | Disable affected integration | Native local capability | Provider operation |
| Network connectivity is lost | Enter profile-defined offline behavior | Local capabilities | Internet-dependent capability |
| Trust or revocation state is stale | Mark affected authority degraded or blocked | Unaffected trust domains | New trust-dependent transitions |
| Incident scope is unknown | Contain conservatively and preserve evidence | Unaffected capabilities | Unsupported full-recovery claim |
| Handoff is incomplete | Escalate and preserve current controls | Existing state | Unreviewed high-risk action |
| Automation encounters ambiguous state | Stop and require owner decision | Current authoritative state | Delete, migrate, activate, revoke, or restore |
| Decommission inventory is incomplete | Keep decommissioning open | Existing isolation and retained state | Final closure or deletion |
| Complete operational validation cannot execute | Keep prior valid state | Known-good operation | New conformance claim |

Degradation remains visible and capability-scoped.

Failure does not authorize silent substitution, partial authority, foreign data access, missing evidence, or indefinite unbounded retry.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Operations consume verified identities, trust assertions, signer state, and revocation state.

Operators do not edit canonical identity or trust records outside the registered lifecycle.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates governed operational decisions.

It does not execute the action, schedule resources, or mutate component state.

Operations verify that the caller enforces the result and satisfies obligations.

### 8.3 Resource Governor

Resource Governor controls resource admission and workload priority.

Operations can change resource policy only through the profile and resource lifecycle.

An operational priority request does not become a governance decision.

### 8.4 kOA Node Agent

kOA Node Agent coordinates node-local lifecycle and closed privileged operations.

Operations use its registered interfaces and verify before-and-after state.

An arbitrary administrative shell is not the normal operating interface.

### 8.5 Audit Broker

Audit Broker handles selected operational and security evidence.

Operations separate routine logs from durable evidence and avoid unrestricted data replication.

### 8.6 Publication Gateway

Publication Gateway owns external publication execution.

An operator cannot publish directly from a source component or bypass disclosure controls during an incident or maintenance window.

### 8.7 UCKK Dimension Gateway

UCKK Dimension Gateway controls explicit admission into UCKK dimensions.

Operations do not substitute Publication Gateway, Suno, Gamma, or direct UCKK storage access for that admission contract.

### 8.8 Component owners

Component owners define:

- readiness;
- safe shutdown;
- migration;
- backup and restore;
- degradation;
- data ownership;
- validation;
- recovery.

Operations coordinate those contracts rather than creating one universal service procedure.

### 8.9 Profile owners

Profile owners define:

- topology;
- selected components;
- resource envelope;
- locality;
- security strengthening;
- offline behavior;
- implementation mechanisms;
- conformance.

An operating practice on one profile does not become a global requirement.

### 8.10 Release and artifact owners

Release and artifact owners control publication, compatibility, staging, activation, rollback, forward repair, retention, and retirement.

Operations execute the lifecycle while preserving exact artifact identity.

### 8.11 External integrations

Integration owners manage manifests, credentials, endpoints, provider terms, degraded behavior, and removal.

Operations preserve native core independence and candidate-adoption boundaries.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed choice |
| --- | --- |
| `DEC-PROFILE-001` | Operating topology, resources, implementation, and strengthening remain profile-specific |
| `DEC-DATA-001` | Operations preserve exclusive component data ownership |
| `DEC-GOV-001` | Resource Governor and Governance Policy Runtime remain separate authorities |
| `DEC-GATE-001` | Publication Gateway and UCKK Dimension Gateway remain separate |
| `DEC-AI-001` | External AI remains optional, explicit, removable, and non-authoritative |
| `DEC-SENT-001` | SenTient remains an optional isolated developer and build workbench |
| `DEC-CONTAINER-001` | Container runtime choices remain profile-scoped |
| `DEC-K8S-001` | Kubernetes is not required for endpoint operation |
| `DEC-HW-001` | Sovereign-node minimum resources and recovery targets are profile-owned |
| `DEC-REL-001` | Four release channels retain independent identity and Release Set compatibility |
| `DEC-DOC-CHANGE-001` | Semantic operational changes use accepted decisions and transitive impact analysis |

### 9.2 Protected locks

| Lock group | Protected operating boundary |
| --- | --- |
| `LOCK-AI-001`, `LOCK-AI-002` | No native AI dependency or direct AI mutation of authoritative state |
| `LOCK-SENT-001` | SenTient failure or prevalence does not change core operation |
| `LOCK-DATA-001` | Operators and tools cannot write foreign authoritative state |
| `LOCK-GOV-001` | Policy and resource operations remain separate |
| `LOCK-GATE-001` | Publication and UCKK admission operations remain separate |
| `LOCK-PROFILE-001` | Profile-specific operating choices do not become global |
| `LOCK-DEV-001` to `LOCK-DEV-005` | Operational development and test workspaces remain isolated |
| `LOCK-LIFE-001` to `LOCK-LIFE-004` | Activation, recovery, Release Sets, and channel compatibility remain controlled |
| `LOCK-DOC-015`, `LOCK-DOC-020` | Major changes receive impact analysis and clean-state validation |
| `LOCK-IMPL-001`, `LOCK-IMPL-002` | Runbooks and profile-specific implementation details do not redefine architecture |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- an operator owns every component;
- root access creates product or policy authority;
- a runbook grants permission;
- monitoring state is authoritative product state;
- a running process is ready;
- a green dashboard proves recovery readiness;
- one SLO target applies to every profile;
- a maintenance window permits security bypass;
- resource pressure permits data-domain merging;
- a successful backup proves restore;
- one restore test proves every data class and profile;
- a snapshot contains complete Release Set and trust state automatically;
- a current process image identifies the active release sufficiently;
- configuration drift becomes valid after repeated use;
- an emergency edit can remain undocumented;
- publication implies activation;
- a partially staged release can be exposed during maintenance;
- rollback is always safe;
- forward repair can be designed after failure;
- a cleared alert proves incident closure;
- restarting a compromised service proves recovery;
- an incident coordinator can override all owners;
- break-glass authority is permanent;
- unavailable external AI can be replaced silently;
- offline operation can depend on remote policy or artifact repositories;
- audit forwarding loss permits dropping required evidence;
- logs can replace receipts;
- a manual statement can replace test evidence;
- skipped synthetic checks can be treated as passing;
- one operational inventory can overwrite canonical registries;
- decommissioning ends when a process is stopped;
- deleting a service deletes its retention and evidence obligations;
- Kubernetes is required for operations because one profile uses it;
- Quadlet or systemd choices apply to every profile;
- current practice overrides active contracts;
- an expired exception remains an operating standard.

Missing owner, profile, Release Set, readiness, policy, trust, migration, recovery, exception, or evidence authority blocks the affected action.

## 10. Validation Criteria

This document is conformant when:

1. the document is registered as `DOC-OPS-000`;
2. the path is `08-operations/00-operating-model.md`;
3. the active language is English;
4. all operating responsibilities resolve to active owners or delegations;
5. operational actions identify profile, Release Set, environment, actor, purpose, and correlation;
6. operators and automation cannot create authority;
7. direct foreign authoritative writes are rejected;
8. state changes use registered interfaces or lifecycle transitions;
9. the observe-decide-act-verify-evidence loop is represented in procedures;
10. every active service distinguishes health and readiness;
11. capability objectives are profile-specific;
12. the runtime inventory reconciles with canonical authority;
13. routine reviews include readiness, capacity, storage, backup, evidence, release, trust, policy, integration, and degradation;
14. maintenance procedures define scope, impact, authority, recovery, and exit;
15. maintenance cannot weaken ownership or security;
16. Resource Governor or profile-equivalent controls capacity;
17. optional work sheds before protected capability;
18. logs, telemetry, audit, and receipts remain distinct and minimized;
19. alerts identify capability impact and next safe action;
20. degraded state is visible;
21. changes follow classification and lifecycle;
22. drift and emergency edits cannot become durable authority;
23. staging remains inactive;
24. activation is atomic;
25. previous known-good or tested forward repair exists;
26. migrations use owning component contracts;
27. backups preserve ownership, encryption, Release Set, trust, and restore metadata;
28. restore tests run on clean compatible environments;
29. backup existence is not reported as restore success;
30. recovery verifies complete authority before traffic;
31. incident response follows the declared lifecycle;
32. containment preserves evidence and unrelated capability;
33. break-glass authority is bounded and closed;
34. incident communication separates facts and uncertainty;
35. unsupported certainty claims are absent;
36. vulnerabilities and incidents have owners and terminal disposition;
37. optional integrations remain removable;
38. no silent provider or local AI fallback occurs;
39. offline profiles retain local authority and recovery closure;
40. offline imports use quarantine and verification;
41. operational handoffs contain required active-state information;
42. automation is bounded, idempotent where applicable, and ambiguity-safe;
43. ambiguous automation cannot execute destructive or authoritative transitions;
44. conformance checks bind exact environment and evidence;
45. skipped or incomplete checks are not reported as passing;
46. decommissioning closes all dependencies and retention obligations;
47. credible-exit exercises demonstrate operator independence;
48. semantic operational changes include accepted decisions and impact analysis;
49. all 48 linked requirements resolve;
50. all required operational tests execute;
51. all required evidence validates;
52. no unresolved operating authority remains;
53. generated operating catalogs and AI context match canonical authority;
54. complete documentation validation passes.

Expected test coverage includes:

```text
TEST-OPS-MODEL-001  Operating role and delegation resolution
TEST-OPS-MODEL-002  Effective profile and Release Set identification
TEST-OPS-MODEL-003  No operator-created authority
TEST-OPS-MODEL-004  Direct foreign-write rejection
TEST-OPS-MODEL-005  Registered operational interface use
TEST-OPS-MODEL-006  Health and readiness distinction
TEST-OPS-MODEL-007  Capability-level profile objectives
TEST-OPS-MODEL-008  Runtime inventory reconciliation
TEST-OPS-MODEL-009  Routine operating review completeness
TEST-OPS-MODEL-010  Maintenance entry and exit controls
TEST-OPS-MODEL-011  Resource pressure workload shedding
TEST-OPS-MODEL-012  Observability and receipt separation
TEST-OPS-MODEL-013  Visible capability degradation
TEST-OPS-MODEL-014  Drift detection and reconciliation
TEST-OPS-MODEL-015  Inactive staging and atomic activation
TEST-OPS-MODEL-016  Known-good rollback readiness
TEST-OPS-MODEL-017  Component-owned migration
TEST-OPS-MODEL-018  Backup identity and ownership closure
TEST-OPS-MODEL-019  Clean restore exercise
TEST-OPS-MODEL-020  Incident containment and evidence preservation
TEST-OPS-MODEL-021  Break-glass expiry and closure
TEST-OPS-MODEL-022  Incident communication evidence accuracy
TEST-OPS-MODEL-023  Optional integration removal
TEST-OPS-MODEL-024  No silent external or local AI fallback
TEST-OPS-MODEL-025  Offline local authority closure
TEST-OPS-MODEL-026  Quarantined offline import
TEST-OPS-MODEL-027  Handoff completeness
TEST-OPS-MODEL-028  Idempotent bounded automation
TEST-OPS-MODEL-029  No false pass for incomplete checks
TEST-OPS-MODEL-030  Complete decommissioning
TEST-OPS-MODEL-031  Credible-exit restore
```

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid operating behavior. They do not replace component, profile, lifecycle, security, or runbook contracts.

### 11.1 Normal sovereign-node startup

A sovereign Linux node verifies its booted image and active Release Set.

Identity, local policy, Audit Broker, Resource Governor, kOA Node Agent, component storage, and recovery state become ready.

Application interfaces enter traffic only after their component-specific readiness checks pass.

### 11.2 Process healthy but service blocked

An Orgo process responds to a health check.

Its migration state is incompatible with the active component contract.

The service remains out of traffic and reports contract readiness blocked.

Operations do not report the capability healthy.

### 11.3 Resource pressure

A heavy optional workbench reaches its memory limit.

Resource Governor stops new workbench tasks and preserves local navigation, identity, policy, critical Orgo work, and recovery capacity.

The workbench becomes visibly degraded without changing policy or data authority.

### 11.4 Failed release activation

A new services-channel artifact is staged as part of a Release Set.

Post-activation readiness fails.

Operations restore the previous compatible Release Set or execute the declared forward repair.

No mixed release remains active.

### 11.5 Backup restore exercise

A clean recovery environment receives a verified backup and retained Release Set.

The exercise restores keys, policy, component-owned data, migrations, and required artifacts.

Derived indexes are rebuilt.

Critical workflows resume, and evidence records actual RPO and RTO results.

### 11.6 Optional ChatGPT outage

ChatGPT becomes unavailable.

The integration reports unavailable status and reconciles any pending request.

Konnaxion, Orgo, local Ariane navigation, native UCKK, and the local language runtime continue.

No alternate provider or local model starts automatically.

### 11.7 Offline import

A sovereign-offline operator receives a signed release bundle.

The bundle enters quarantine, passes inventory and trust checks, is staged, and activates atomically.

The active local known-good Release Set remains available until acceptance succeeds.

### 11.8 Incident containment

A service credential is suspected compromised.

Operations revoke the credential, isolate the service, preserve evidence, rotate the identity, verify affected data and artifacts, and restore through a known-good service release.

Unrelated security domains remain available.

### 11.9 Handoff

An outgoing operator records one active degradation, one pending maintenance approval, a backup warning, and an integration outage.

The incoming operator verifies each referenced state and assumes coordination.

No new component authority transfers through the handoff note.

### 11.10 Invalid decommissioning

A service process is stopped, but its credentials, network route, scheduled job, database, backup, integration callback, alerts, and retention obligations remain.

The service is not decommissioned, and closure remains blocked.
