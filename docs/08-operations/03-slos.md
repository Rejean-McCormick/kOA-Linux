<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-003",
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
    "contracts/system.contract.json#/operations_model/service_level_objectives",
    "contracts/system.contract.json#/capability_model",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-OPS-SLO-001",
    "DEC-SYS-CAP-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-OPS-SLO-001",
    "REQ-OPS-SLO-002",
    "REQ-OPS-SLO-003",
    "REQ-OPS-SLO-004",
    "REQ-OPS-SLO-005",
    "REQ-OPS-SLO-006",
    "REQ-OPS-SLO-007",
    "REQ-OPS-SLO-008",
    "REQ-OPS-SLO-009",
    "REQ-OPS-SLO-010",
    "REQ-OPS-SLO-011",
    "REQ-OPS-SLO-012",
    "REQ-OPS-SLO-013",
    "REQ-OPS-SLO-014",
    "REQ-OPS-SLO-015",
    "REQ-OPS-SLO-016",
    "REQ-OPS-SLO-017",
    "REQ-OPS-SLO-018",
    "REQ-OPS-SLO-019",
    "REQ-OPS-SLO-020",
    "REQ-OPS-SLO-021",
    "REQ-OPS-SLO-022",
    "REQ-OPS-SLO-023",
    "REQ-OPS-SLO-024",
    "REQ-OPS-SLO-025",
    "REQ-OPS-SLO-026",
    "REQ-OPS-SLO-027",
    "REQ-OPS-SLO-028",
    "REQ-OPS-SLO-029",
    "REQ-OPS-SLO-030",
    "REQ-OPS-SLO-031",
    "REQ-OPS-SLO-032",
    "REQ-OPS-SLO-033",
    "REQ-OPS-SLO-034",
    "REQ-OPS-SLO-035",
    "REQ-OPS-SLO-036",
    "REQ-OPS-SLO-037",
    "REQ-OPS-SLO-038",
    "REQ-OPS-SLO-039",
    "REQ-OPS-SLO-040"
  ],
  "lock_ids": [
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002"
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
    "DOC-LIFE-003",
    "DOC-LIFE-013",
    "DOC-SEC-016",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002"
  ],
  "tags": [
    "operations",
    "service-level-objectives",
    "service-level-indicators",
    "error-budgets",
    "availability",
    "latency",
    "correctness",
    "durability",
    "freshness",
    "recovery",
    "offline-continuity",
    "measurement",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Service-Level Objectives

## 1. Purpose

This document defines the kOA model for service-level indicators, service-level objectives, and error budgets.

An SLO is a governed internal reliability target for one observable capability outcome under an explicit profile and operating state. It is not a generic uptime promise and does not create a contractual service-level agreement by itself.

The model ensures that reliability measurement:

- follows user-visible or authority-visible outcomes;
- preserves correctness and safety before speed;
- distinguishes connected, offline, degraded, recovery, and maintenance behavior;
- separates end-to-end results from dependency attribution;
- keeps measurement quality visible;
- prevents exclusions from hiding operational failure;
- converts error-budget consumption into controlled operational decisions;
- preserves historical interpretation across releases and measurement changes.

No global numeric target is established here. Numeric objectives remain owned by the applicable capability, component, profile, or service contract.

## 2. Scope

This document applies globally to:

- service-level indicators;
- service-level objectives;
- availability;
- success rate;
- correctness;
- latency;
- queue delay;
- throughput where it represents a governed outcome;
- durability;
- freshness;
- recovery time;
- recovery point;
- audit and receipt durability;
- offline continuity;
- deferred-operation reconciliation;
- dependency attribution;
- measurement pipelines;
- maintenance treatment;
- error budgets;
- burn alerts;
- breach records;
- SLO changes;
- profile and release conformance.

This document applies to local, federated, connected, disconnected, online-transfer, and offline-transfer operation according to the active profile.

This document does not establish commercial remedies, customer credits, contractual penalties, staffing schedules, or one common target for all profiles.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Global SLO model | `contracts/system.contract.json#/operations_model/service_level_objectives` |
| Capability identity and outcome | `contracts/system.contract.json#/capability_model` |
| Component ownership, interfaces, states, and failures | `generated/component-catalog.json` and `contracts/components/*.component.json` |
| Profile applicability and target values | `contracts/profiles/*.profile.json` |
| Release and artifact compatibility | `contracts/release-channels.contract.json` and `contracts/artifact-classes.contract.json` |
| External dependency classification | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Reliability and cross-file invariants | `generated/assertion-index.json` |
| SLO, component, profile, test, incident, and evidence links | `generated/traceability.json` |
| SLO and reliability tests | `generated/test-catalog.json` |
| Current measurement and breach evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted SLO decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

Dashboards and alerts are generated operational views. They do not own target values, indicator semantics, exclusions, or error-budget policy.

## 4. SLO Model and Ownership

### 4.1 Core terms

| Term | Meaning |
| --- | --- |
| Service-level indicator | A defined measurement of an observable capability outcome |
| Service-level objective | A target applied to an indicator over a defined window |
| Error budget | The permitted non-conforming portion implied by the target |
| Measurement window | The bounded period used to evaluate the objective |
| Eligible event | An event or interval included in the indicator population |
| Good event | An eligible event satisfying the declared outcome |
| Bad event | An eligible event failing the declared outcome |
| Invalid event | An observation that cannot be evaluated under the indicator contract |
| Exclusion | An approved bounded removal from one calculation |
| Burn rate | Error-budget consumption relative to elapsed window time |
| Breach | An SLO result outside its target |
| Measurement block | Insufficient trustworthy evidence for a conformance claim |

### 4.2 Service classes

Each SLO uses one service class:

| Service class | Typical role |
| --- | --- |
| `critical_authoritative` | Identity, policy, authority, activation, audit durability, protected state |
| `core_interactive` | User-facing local navigation and primary interactive workflows |
| `core_background` | Required background processing, receipts, reconciliation, resource governance |
| `bounded_batch` | Imports, exports, indexing, builds, migrations, scheduled processing |
| `optional_workbench` | Developer or analytical tools whose absence does not break the core |
| `external_dependency` | External providers, repositories, federation peers, or remote services |

The service class affects alerting, budget response, recovery priority, and acceptable degradation. It does not weaken correctness.

### 4.3 Operating states

SLO applicability is defined separately for:

```text
normal
degraded
offline
recovery
maintenance
```

A capability can have a different objective or no applicability in a given state. The profile declares the expected state behavior.

For example, a remote publication capability can be unavailable offline while the durability of its deferred local request remains continuously measured.

### 4.4 Ownership

Every SLO identifies:

- `slo_id`;
- owner;
- capability;
- accountable component or authority;
- profiles;
- service class;
- operating states;
- indicator;
- target;
- window;
- exclusions;
- error-budget policy;
- tests;
- evidence.

The SLO owner controls semantic changes. The component owner controls instrumented behavior. The profile owner controls deployment-specific applicability and values.

### 4.5 Outcome hierarchy

Measurement follows this hierarchy:

1. authoritative correctness and safety;
2. durable completion and evidence;
3. user- or workflow-visible success;
4. latency and freshness;
5. supporting component and infrastructure health.

A faster incorrect result remains a bad result.

### 4.6 SLO status

Operational reporting uses:

| Status | Meaning |
| --- | --- |
| `conformant` | Objective passes with trustworthy complete measurement |
| `at_risk` | Objective still passes but burn or forecast crosses an alert threshold |
| `breached` | Objective fails for the active window |
| `measurement_blocked` | Measurement evidence is insufficient or untrustworthy |
| `authorized_suspended` | A governed suspension is active and impact remains recorded |
| `not_applicable` | The SLO contract excludes the current profile or operating state |

A suspension is not a passing result.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-SLO-001,REQ-OPS-SLO-002,REQ-OPS-SLO-003,REQ-OPS-SLO-004,REQ-OPS-SLO-005,REQ-OPS-SLO-006,REQ-OPS-SLO-007,REQ-OPS-SLO-008,REQ-OPS-SLO-009,REQ-OPS-SLO-010,REQ-OPS-SLO-011,REQ-OPS-SLO-012,REQ-OPS-SLO-013,REQ-OPS-SLO-014,REQ-OPS-SLO-015,REQ-OPS-SLO-016,REQ-OPS-SLO-017,REQ-OPS-SLO-018,REQ-OPS-SLO-019,REQ-OPS-SLO-020,REQ-OPS-SLO-021,REQ-OPS-SLO-022,REQ-OPS-SLO-023,REQ-OPS-SLO-024,REQ-OPS-SLO-025,REQ-OPS-SLO-026,REQ-OPS-SLO-027,REQ-OPS-SLO-028,REQ-OPS-SLO-029,REQ-OPS-SLO-030,REQ-OPS-SLO-031,REQ-OPS-SLO-032,REQ-OPS-SLO-033,REQ-OPS-SLO-034,REQ-OPS-SLO-035,REQ-OPS-SLO-036,REQ-OPS-SLO-037,REQ-OPS-SLO-038,REQ-OPS-SLO-039,REQ-OPS-SLO-040 -->
- **REQ-OPS-SLO-001 — SHALL:** Every active service-level objective identify one owning capability, one accountable component or authority, applicable profiles, operating states, user or system outcome, indicator, target, measurement window, data source, exclusions, error-budget policy, tests, and evidence.
- **REQ-OPS-SLO-002 — SHALL NOT:** A process-uptime percentage, host-uptime percentage, container-running state, health endpoint, or infrastructure metric alone represent an end-to-end service-level objective.
- **REQ-OPS-SLO-003 — SHALL:** Service-level indicators measure observable outcomes at the authority boundary experienced by the intended user, component, node, operator, or governed workflow.
- **REQ-OPS-SLO-004 — SHALL:** Correctness, safety, authorization, integrity, durability, and audit obligations take precedence over latency or availability targets.
- **REQ-OPS-SLO-005 — SHALL NOT:** An SLO target authorize unsafe success, false completion, bypassed validation, missing evidence, partial authority, silent data loss, or weakened security.
- **REQ-OPS-SLO-006 — SHALL:** Every SLO distinguish the measured capability from supporting component, infrastructure, network, provider, and dependency indicators.
- **REQ-OPS-SLO-007 — SHALL:** Every SLO declare whether it applies to critical authoritative, core interactive, core background, bounded batch, optional workbench, or external dependency service class.
- **REQ-OPS-SLO-008 — SHALL:** Every SLO declare its applicable normal, degraded, offline, recovery, and maintenance behavior rather than combining unlike operating states into one undifferentiated target.
- **REQ-OPS-SLO-009 — SHALL NOT:** Connected-path failure be hidden by an offline-path result, and offline continuity failure be hidden by connected-path availability.
- **REQ-OPS-SLO-010 — SHALL:** Profiles own deployment-specific SLO applicability, target values, measurement constraints, recovery commitments, and declared exclusions.
- **REQ-OPS-SLO-011 — SHALL NOT:** A development-profile measurement establish production, sovereign, high-assurance, build-farm, control-plane, or user-lightweight SLO conformance.
- **REQ-OPS-SLO-012 — SHALL:** Every indicator define its event population, good-event rule, bad-event rule, invalid-event rule, time source, aggregation method, units, dimensions, sampling behavior, and low-volume behavior.
- **REQ-OPS-SLO-013 — SHALL:** Every latency indicator define its start event, completion event, timeout treatment, cancelled-request treatment, percentile or distribution method, and maximum observation horizon.
- **REQ-OPS-SLO-014 — SHALL:** Every availability indicator define what constitutes an eligible request or capability interval and distinguish rejected, blocked, deferred, unavailable, degraded, conflicted, expired, and recovery-required outcomes.
- **REQ-OPS-SLO-015 — SHALL:** Every correctness indicator verify authoritative outcome or invariant rather than infer correctness from transport success or response codes alone.
- **REQ-OPS-SLO-016 — SHALL:** Every durability indicator define the acknowledged durability boundary, verification method, loss event, corruption event, replay behavior, and recovery evidence.
- **REQ-OPS-SLO-017 — SHALL:** Every freshness indicator define source time, observation time, permitted delay, clock-quality requirements, and treatment of disconnected or deferred states.
- **REQ-OPS-SLO-018 — SHALL:** Every recovery indicator define the initiating failure, detection point, recovery start, restored capability state, data-consistency state, receipt state, and final verification.
- **REQ-OPS-SLO-019 — SHALL:** Every SLO use one explicitly versioned measurement window and preserve enough historical data to evaluate the complete active window.
- **REQ-OPS-SLO-020 — SHALL NOT:** Restart, deployment, profile change, release activation, counter reset, exporter replacement, or measurement implementation change erase or restart an active SLO window.
- **REQ-OPS-SLO-021 — SHALL:** Measurement coverage, integrity, clock quality, cardinality, missing-data rate, and pipeline health be evaluated separately from the service result.
- **REQ-OPS-SLO-022 — SHALL NOT:** Missing, delayed, corrupt, incompatible, or selectively unavailable telemetry be counted automatically as successful service.
- **REQ-OPS-SLO-023 — SHALL:** An SLO with insufficient trustworthy measurement enter a measurement-blocked state and suspend its conformance claim without erasing observed failures.
- **REQ-OPS-SLO-024 — SHALL:** Every exclusion be closed, versioned, attributable, time-bounded, purpose-specific, independently measurable, and approved by the SLO owner.
- **REQ-OPS-SLO-025 — SHALL NOT:** Operator error, deployment failure, dependency failure, capacity shortage, planned maintenance, incident severity, unavailable telemetry, or an inconvenient result be excluded automatically.
- **REQ-OPS-SLO-026 — SHALL:** Approved maintenance exclusions record affected users and capabilities, actual impact, start and finish, authority, tests, and evidence even when excluded from one target calculation.
- **REQ-OPS-SLO-027 — SHALL:** Every SLO define an error budget derived from the target and measurement window, together with burn calculation, alert thresholds, decision owners, and permitted operational responses.
- **REQ-OPS-SLO-028 — SHALL:** Fast and sustained error-budget burn be evaluated independently so short severe failures and long moderate degradation are both visible.
- **REQ-OPS-SLO-029 — SHALL:** Error-budget exhaustion trigger the registered change, release, incident, capacity, or remediation controls for the affected capability and profile.
- **REQ-OPS-SLO-030 — SHALL NOT:** Error-budget exhaustion disable safety controls, audit capture, backup, restore, rollback, recourse, security validation, or critical offline continuity.
- **REQ-OPS-SLO-031 — SHALL NOT:** An SLO target, window, indicator, event population, exclusion, or classification be changed retroactively to convert a recorded breach into conformance.
- **REQ-OPS-SLO-032 — SHALL:** Semantic SLO changes use accepted decisions, versioned contracts, impact analysis, migration of dashboards and alerts, test updates, and a stated effective time.
- **REQ-OPS-SLO-033 — SHALL:** Every dependency-sensitive SLO preserve the end-to-end user outcome while also attributing supporting failures to local components, external providers, networks, storage, identity, policy, resources, or other dependencies.
- **REQ-OPS-SLO-034 — SHALL NOT:** External provider availability or acknowledgement substitute for local acceptance, authoritative completion, or the end-to-end kOA outcome.
- **REQ-OPS-SLO-035 — SHALL:** Offline-capable SLOs measure locally promised capability continuity, deferred effect durability, queue bounds, reconciliation, and recovery independently from remote reachability.
- **REQ-OPS-SLO-036 — SHALL:** Resource pressure preserve the measurement, receipts, journals, critical SLOs, recovery indicators, and incident evidence required to determine actual service state.
- **REQ-OPS-SLO-037 — SHALL NOT:** Resource state decide authorization, consent, publication, disclosure, cultural rights, or whether a failed authoritative operation is counted as successful.
- **REQ-OPS-SLO-038 — SHALL:** Every SLO breach create or update an attributable operational record containing affected scope, start, detection, indicator values, budget state, cause classification, mitigation, user impact, recovery, and evidence.
- **REQ-OPS-SLO-039 — SHALL:** SLO reporting distinguish conformant, at-risk, breached, measurement-blocked, authorized-suspended, and not-applicable states with explicit reason codes.
- **REQ-OPS-SLO-040 — SHALL:** SLO conformance include canonical ownership, profile scope, service class, complete indicator semantics, trustworthy measurement, closed exclusions, error-budget governance, dependency attribution, offline treatment, incident linkage, historical preservation, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Indicator and Measurement Design

### 6.1 Indicator contract

Every SLI defines:

```text
sli_id
version
outcome_statement
eligible_population
good_event_rule
bad_event_rule
invalid_event_rule
start_event
completion_event
time_source
units
aggregation
dimensions
sampling
low_volume_behavior
data_sources
quality_checks
```

The outcome statement is understandable without reading the metric implementation.

### 6.2 Availability and success indicators

Availability and success indicators classify every eligible outcome.

Common result categories include:

```text
completed
rejected
blocked
deferred
unavailable
degraded
conflicted
expired
cancelled
recovery_required
```

The SLO contract determines which categories count as good, bad, or outside the eligible population.

A policy-correct rejection can be a correct service outcome for an authorization SLO while remaining an unsuccessful business operation. Separate indicators preserve that distinction.

### 6.3 Correctness indicators

Correctness indicators evaluate authoritative results such as:

- expected state reached;
- no partial authority;
- invariant preserved;
- destination reconciled;
- signature and integrity verified;
- duplicate effect prevented;
- receipt durable;
- rights or policy outcome enforced;
- rollback restored a complete compatible state.

Transport success is supporting evidence only.

### 6.4 Latency indicators

A latency indicator identifies:

- accepted start event;
- terminal completion event;
- deadline;
- timeout treatment;
- queue time;
- execution time;
- external wait time;
- reconciliation time;
- percentile or distribution method;
- maximum observation duration.

Cancelled or abandoned requests are classified explicitly rather than disappearing.

### 6.5 Durability indicators

Durability can measure:

- acknowledged write survival;
- receipt survival;
- journal survival;
- backup verification;
- deferred-queue survival;
- restart recovery;
- corruption detection;
- restore success.

The indicator states the durability boundary. Process memory does not qualify as durable state.

### 6.6 Freshness indicators

Freshness measures age relative to a source event or authoritative version.

It identifies:

- source timestamp;
- trusted clock;
- local observation timestamp;
- expected propagation path;
- permitted delay;
- disconnected behavior;
- deferred behavior;
- correction and supersession handling.

Clock quality is part of measurement quality.

### 6.7 Recovery indicators

Recovery measurement distinguishes:

- detection time;
- acknowledgement time;
- containment time;
- service restoration time;
- authoritative consistency restoration time;
- receipt and evidence restoration time;
- final recovery verification.

A service restart is not complete recovery when data, authority, receipts, or queues remain inconsistent.

### 6.8 Offline indicators

Offline indicators can measure:

- local core availability;
- restart while disconnected;
- local identity and policy availability;
- local receipt durability;
- deferred queue age and bounds;
- offline-transfer validation;
- reconnection reconciliation;
- duplicate prevention;
- time since last valid trust or policy update;
- recovery after reconnection.

Remote reachability remains a separate indicator.

### 6.9 Dimensions

Dimensions are bounded and meaningful.

Typical dimensions include:

```text
profile
capability
component
operation
result class
operating state
release set
dependency class
priority class
```

High-cardinality identities remain in protected traces or evidence rather than unrestricted metric labels.

### 6.10 Low-volume behavior

Low-volume SLOs use a declared method such as:

- event-count window;
- longer rolling window;
- exact-event evaluation;
- synthetic conformance transaction;
- state-based invariant;
- combined event and interval model.

A missing sample does not become a successful sample.

## 7. Windows, Exclusions, and Error Budgets

### 7.1 Measurement windows

A window declaration includes:

```text
window_type
window_length
effective_at
minimum_coverage
retention
late_event_policy
correction_policy
```

Supported window types can include rolling, calendar, event-count, and state-interval windows.

Changes take effect prospectively.

### 7.2 Measurement continuity

Window state survives:

- process restart;
- telemetry restart;
- component upgrade;
- Release Set activation;
- profile-compatible migration;
- dashboard replacement;
- metric backend migration.

Historical evaluation retains the indicator and target version used at event time.

### 7.3 Exclusions

An exclusion record identifies:

- exclusion identity;
- affected SLO;
- event or interval selection;
- reason;
- authority;
- start and finish;
- scope;
- evidence;
- impact outside the target calculation;
- expiry.

Exclusions remain visible in reports.

### 7.4 Maintenance

Maintenance has three separate records:

1. planned maintenance window;
2. actual capability impact;
3. SLO treatment.

A profile or SLO can include, exclude, or evaluate maintenance under a separate objective. Planning alone does not remove the impact.

### 7.5 Error-budget calculation

For an event-based objective:

```text
error budget = eligible events × permitted bad-event fraction
```

For an interval-based objective:

```text
error budget = eligible service time × permitted non-conforming fraction
```

The contract defines rounding, partial intervals, late events, and corrections.

### 7.6 Burn rate

Burn evaluation compares consumed budget with elapsed window time.

The policy includes:

- fast-burn threshold;
- sustained-burn threshold;
- alert recipients;
- incident linkage;
- release or change controls;
- capacity review;
- remediation requirements;
- exit criteria.

Threshold values remain profile- and SLO-owned.

### 7.7 Budget responses

Registered responses can include:

- increase observation;
- stop optional work;
- reduce change rate;
- block risky release activation;
- require rollback or forward repair;
- trigger incident response;
- prioritize capacity or defect remediation;
- require owner review;
- require evidence refresh.

A response cannot suppress the measurement that triggered it.

### 7.8 Budget exhaustion

Budget exhaustion records:

- affected SLO and profile;
- current window;
- consumed and remaining budget;
- primary bad-event classes;
- affected users or workflows;
- active Release Set;
- dependencies;
- incidents;
- mitigations;
- decision owner;
- recovery criteria.

The record remains linked after the window closes.

## 8. Dependencies, Offline Operation, and Failure Behavior

### 8.1 End-to-end and dependency SLOs

An end-to-end SLO measures the promised kOA outcome.

Supporting indicators attribute delay or failure to:

- local component;
- local infrastructure;
- Identity and Trust;
- Governance Policy Runtime;
- Resource Governor;
- Audit Broker;
- network;
- storage;
- external provider;
- federation peer;
- destination;
- artifact or release incompatibility.

Attribution does not remove the end-to-end failure.

### 8.2 External dependencies

An external dependency record identifies:

- integration;
- provider or peer;
- promised local behavior during absence;
- retry and timeout;
- data and cost boundary;
- provider indicator;
- local end-to-end indicator;
- deferred or unavailable behavior.

Provider acknowledgement does not establish local authoritative completion.

### 8.3 Resource pressure

Under pressure, operations preserve:

1. authoritative state;
2. journals and receipts;
3. critical measurement;
4. incident evidence;
5. last-known-good and recovery material;
6. core interactive measurement;
7. optional detailed telemetry.

Sampling reduction never changes the semantic event classification.

### 8.4 Measurement failures

| Failure | Operational treatment |
| --- | --- |
| Metric source unavailable | Mark affected measurement blocked and preserve raw local evidence where available. |
| Clock quality invalid | Reject time-derived conclusions until a governed correction is possible. |
| Event schema incompatible | Quarantine or translate through a versioned validated path. |
| Duplicate event | Deduplicate by canonical identity and preserve duplicate evidence. |
| Late event | Apply the declared late-event policy and retain historical correction. |
| Missing denominator | Block ratio conformance instead of reporting zero failures. |
| Cardinality overflow | Preserve bounded aggregate measurement and protected detailed evidence. |
| Storage pressure | Retain critical SLO state before optional telemetry. |
| Offline remote sink | Keep local durable measurement and defer export. |
| Dashboard unavailable | Preserve canonical measurement and evidence; dashboard loss does not erase state. |
| Indicator implementation change | Run compatibility or parallel measurement before cutover. |
| SLO contract invalid | Preserve the last validated interpretation and suspend the affected claim. |

### 8.5 Incident linkage

An SLO breach or severe burn links to incident response when the active policy threshold is met.

The incident record and SLO record remain separate:

- SLO record owns objective result;
- incident record owns coordinated response;
- evidence links them.

### 8.6 Safe degradation

A degraded capability reports:

- available operations;
- unavailable operations;
- reduced guarantees;
- user-visible impact;
- active SLO treatment;
- recovery criteria.

A degraded state cannot be presented as full conformance.

## 9. Governance, Reporting, and Change

### 9.1 SLO contract

A canonical SLO record includes:

```text
slo_id
version
owner_ref
capability_ref
component_or_authority_ref
profile_refs
service_class
operating_states
sli_ref
target
window
exclusions
error_budget_policy
reporting_policy
incident_policy_ref
test_refs
evidence_refs
effective_at
```

The target representation supports the indicator type without forcing every objective into a percentage.

### 9.2 Reports

SLO reports include:

- current status;
- indicator value;
- target;
- window progress;
- coverage and measurement quality;
- budget consumed and remaining;
- burn state;
- exclusions;
- maintenance;
- dependencies;
- incidents;
- Release Set;
- trend;
- reason codes;
- evidence currency.

Public reports use minimum disclosure. Restricted operational detail remains protected.

### 9.3 Semantic changes

Semantic changes include:

- event population;
- good or bad rule;
- target;
- window;
- service class;
- profile applicability;
- operating-state treatment;
- exclusion policy;
- error-budget response;
- measurement source that changes meaning.

They receive accepted decision and version treatment.

### 9.4 Measurement implementation changes

A compatible implementation change records:

- prior and new implementation;
- semantic-equivalence claim;
- parallel-run or replay result;
- coverage comparison;
- value comparison;
- cutover time;
- rollback plan;
- evidence.

Historical data remains interpretable.

### 9.5 Release gates

A release gate can use:

- current SLO status;
- recent burn;
- measurement quality;
- active incidents;
- rollback readiness;
- profile risk;
- change class.

Release gating does not mutate the SLO result.

### 9.6 Exceptions

A bounded exception can adjust:

- a target;
- a window;
- an exclusion;
- a measurement source;
- a burn threshold;
- a report audience;
- a profile-specific applicability rule;
- an evidence source.

The exception identifies scope, owner, effective period, impact, compensating controls, and exit criteria.

An exception cannot convert unsafe or incorrect outcomes into good events, erase historical breaches, count missing telemetry as success, or remove critical audit and recovery measurement.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. every SLO has a stable identity and version;
2. every SLO resolves to one capability owner and accountable component or authority;
3. profile applicability and numeric values are explicit;
4. one service class is selected;
5. operating-state treatment is complete;
6. the indicator contract defines event population and classification;
7. correctness and safety precede latency and availability;
8. latency start, completion, timeout, and percentile semantics are explicit;
9. durability and recovery boundaries are verifiable;
10. offline and connected measurements remain separate;
11. measurement windows survive restarts and releases;
12. coverage, integrity, clock, missing data, and pipeline health are measured;
13. untrustworthy measurement blocks the claim rather than passing it;
14. exclusions are closed, approved, time-bounded, and visible;
15. maintenance treatment is explicit;
16. error budget and burn policies are computable;
17. fast and sustained burn are evaluated;
18. exhaustion responses preserve safety, evidence, backup, recovery, and recourse;
19. historical breaches cannot be rewritten by retroactive semantic changes;
20. dependency attribution preserves end-to-end outcomes;
21. external acknowledgements remain separate from local completion;
22. resource pressure preserves critical measurement and evidence;
23. breach records link scope, time, cause, impact, mitigation, recovery, and evidence;
24. reporting uses the canonical status vocabulary;
25. semantic changes use decisions, versions, migration, tests, and effective time;
26. all capabilities, components, profiles, integrations, releases, tests, incidents, evidence, and exceptions resolve;
27. no prohibited open-state marker enters active operations authority.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_slo_contracts.py
tools/check_observability_coverage.py
tools/check_profile_inheritance.py
tools/check_component_boundaries.py
tools/check_interfile_locks.py
tools/check_release_sets.py
tools/check_traceability.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
```

A failed SLO check blocks the affected reliability claim, release gate, profile claim, or incident closure.

## 11. Non-Normative Examples

### 11.1 Interactive request

A core interactive capability measures completed authoritative requests within two seconds over a rolling window. Rejected unauthorized requests are tracked separately as correct policy enforcement rather than hidden as transport failure.

### 11.2 Receipt durability

A critical authoritative SLO measures whether every completed privileged transition has a locally durable receipt. Audit Broker forwarding delay uses a separate freshness objective.

### 11.3 Offline publication

Publication to a remote destination is unavailable offline. The offline SLO instead measures durable local queueing, bounded backlog, restart survival, and duplicate-safe reconciliation after reconnection.

### 11.4 Provider outage

An external provider is unavailable. The provider indicator attributes the dependency failure, while the end-to-end user operation remains deferred or unavailable according to its local contract.

### 11.5 Measurement outage

A metric exporter fails for twenty minutes. The SLO enters `measurement_blocked`; it does not report perfect availability for the missing interval.

### 11.6 Planned maintenance

A planned maintenance window is approved. Actual user impact and duration are still recorded. The SLO contract determines whether the interval is included, excluded, or evaluated under a maintenance objective.

### 11.7 Fast burn

A release causes a short severe failure. The fast-burn threshold triggers incident response and rollback even though the rolling-window objective has not yet breached.

### 11.8 Sustained degradation

A queue remains slower than target for several days. Sustained burn triggers capacity and defect remediation even without a single severe incident.

### 11.9 Target change

A target changes prospectively after an accepted decision and impact analysis. Historical windows keep the prior target and indicator version.

### 11.10 Low-volume recovery

A rare disaster-recovery workflow uses exact-event evaluation and verified recovery evidence rather than a percentage calculated from too few events.
