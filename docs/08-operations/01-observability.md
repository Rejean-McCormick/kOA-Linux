<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-OPS-OBS-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AUD-001",
    "DEC-PROFILE-001"
  ],
  "requirement_ids": [
    "REQ-OPS-OBS-001",
    "REQ-OPS-OBS-002",
    "REQ-OPS-OBS-003",
    "REQ-OPS-OBS-004",
    "REQ-OPS-OBS-005",
    "REQ-OPS-OBS-006",
    "REQ-OPS-OBS-007",
    "REQ-OPS-OBS-008",
    "REQ-OPS-OBS-009",
    "REQ-OPS-OBS-010",
    "REQ-OPS-OBS-011",
    "REQ-OPS-OBS-012",
    "REQ-OPS-OBS-013",
    "REQ-OPS-OBS-014",
    "REQ-OPS-OBS-015",
    "REQ-OPS-OBS-016",
    "REQ-OPS-OBS-017",
    "REQ-OPS-OBS-018",
    "REQ-OPS-OBS-019",
    "REQ-OPS-OBS-020",
    "REQ-OPS-OBS-021",
    "REQ-OPS-OBS-022",
    "REQ-OPS-OBS-023",
    "REQ-OPS-OBS-024",
    "REQ-OPS-OBS-025",
    "REQ-OPS-OBS-026",
    "REQ-OPS-OBS-027",
    "REQ-OPS-OBS-028",
    "REQ-OPS-OBS-029",
    "REQ-OPS-OBS-030"
  ],
  "lock_ids": [
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-DOC-002"
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
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-COMP-000",
    "DOC-LIFE-002",
    "DOC-LIFE-012",
    "DOC-SEC-004",
    "DOC-SEC-015",
    "DOC-OPS-000"
  ],
  "tags": [
    "operations",
    "observability",
    "health",
    "readiness",
    "metrics",
    "events",
    "traces",
    "receipts",
    "bounded-telemetry",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# Observability

## 1. Purpose

This document defines the operational observability model for the kOA operating environment.

Observability makes system state understandable without creating a second source of authority. Components expose bounded signals about health, readiness, load, failures, dependencies, degradation, transitions, and resource use. Shared operational services can collect, aggregate, retain, correlate, alert on, and display those signals while preserving component ownership, tenant isolation, disclosure controls, and resource limits.

The model distinguishes immediate operations, diagnosis, capacity planning, selective audit, and conformance evidence. These uses can consume related signals, but their authority, retention, audience, and evidence requirements remain separate.

## 2. Scope

This document applies to:

- component health and readiness;
- capability and dependency state;
- operational metrics;
- structured events;
- diagnostic logs;
- distributed traces and correlation context;
- decision, resource, verification, publication, activation, and recovery receipts used operationally;
- alert evaluation, routing, deduplication, suppression, escalation, and recovery;
- dashboards and authorized operational views;
- telemetry collection, buffering, transport, aggregation, storage, query, export, retention, and disposition;
- profiling, diagnostic bundles, crash information, and bounded support data;
- tenant, node, workspace, component, profile, release, and control-plane observability;
- online, offline, disconnected, degraded, and recovery operation;
- observability resource use, failure behavior, security, privacy, selective audit, and conformance evidence.

This document does not:

- make dashboards or telemetry stores authoritative component state;
- replace component contracts or profile contracts;
- define policy authorization, resource admission, artifact verification, release activation, or audit disclosure;
- prescribe one telemetry protocol, collector, metrics database, log system, tracing backend, dashboard, alert manager, or monitoring vendor;
- require every profile to emit or retain identical signal detail;
- permit unbounded telemetry or universal unrestricted log access;
- authorize remediation merely because an alert fired.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/component-catalog.json` and component contracts | Own signal meaning, source identity, health, readiness, state, dependency, and failure semantics. |
| `contracts/profiles/*.profile.json` | Own profile-specific signal detail, collection topology, retention, offline behavior, access, and resource constraints. |
| `contracts/components/resource-governor.component.json` | Owns telemetry resource admission, limits, queues, throttling, and scheduling where applicable. |
| `contracts/components/governance-policy-runtime.component.json` | Owns policy-gated access, export, retention override, diagnostic capture, and remediation authorization. |
| `contracts/components/identity-and-trust.component.json` | Owns requester, service, collector, exporter, and destination identity and trust verification. |
| `contracts/components/audit-broker.component.json` | Owns declared evidence custody, restricted access records, and authorized audit views. |
| `contracts/artifact-contracts/decision-receipt.schema.json` | Defines machine-readable access, remediation, transition, and operational decision receipts. |
| `contracts/artifact-contracts/resource-envelope.schema.json` | Defines resource-envelope artifacts consumed by operational capacity and admission views. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns observability authority, bounded telemetry, health/readiness, data, policy/resource, profile, and documentation assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, component, profile, test, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own observability validation-test and evidence identities. |

This Markdown document explains operational behavior. Exact signal identifiers, fields, state values, units, limits, routes, retention, and profile membership remain in canonical contracts.

## 4. Model and Responsibilities

### 4.1 Signal classes

| Signal class | Purpose | Typical authority |
| --- | --- | --- |
| Health | Reports internal validity and ability to continue declared operation | Source component contract |
| Readiness | Reports ability to accept a declared class of new work | Source component plus current dependency and admission context |
| State | Reports lifecycle, capability, dependency, or degradation state | Source component contract |
| Metric | Reports bounded numeric observations or aggregates | Source component signal contract |
| Structured event | Reports an occurrence or transition with declared fields | Source component event contract |
| Diagnostic log | Supports bounded human or automated diagnosis | Source component diagnostic contract |
| Trace | Correlates declared work across boundaries | Participating component contracts |
| Receipt | Records an authority decision or critical transition | Issuing authority and receipt contract |
| Capacity record | Supports planning and resource-envelope analysis | Resource and operations contracts |
| Audit evidence | Supports accountability and recourse | Audit Broker and evidence contracts |

One occurrence can create more than one object. The objects retain separate classifications and owners.

### 4.2 Health

Health reports whether a component is internally coherent enough to continue its declared operation.

Health can account for:

- internal invariant validity;
- required local state;
- worker or process state;
- storage integrity;
- critical dependency state;
- active artifact validity;
- trust and policy prerequisites when part of ordinary operation;
- recovery or degradation state.

A healthy component can be not ready for new work because a queue is full, a maintenance window is active, or a required resource grant is unavailable.

### 4.3 Readiness

Readiness is work-class specific.

A component can separately report readiness for:

- queries;
- commands;
- artifact admission;
- background jobs;
- privileged operations;
- publication;
- migration;
- recovery;
- administrative access.

Readiness does not establish that a specific requester is authorized or that a specific artifact is compatible. Those checks occur in their owning authorities.

### 4.4 State and degradation

Operational state includes the scope of an affected capability.

A useful degradation signal identifies:

- component and instance;
- affected capability;
- affected tenant, profile, node, workspace, or operation class where relevant;
- cause class;
- start time;
- current behavior;
- preserved behavior;
- blocked behavior;
- recovery condition;
- related receipts or incidents.

A generic `degraded` label without scope is insufficient for operational diagnosis.

### 4.5 Metrics

Metric contracts define:

- metric identity;
- meaning;
- type;
- unit;
- dimensions;
- aggregation;
- collection interval;
- reset behavior;
- precision;
- expected range;
- cardinality budget;
- retention;
- classification;
- profile applicability.

Metric labels use bounded enumerations or controlled identifiers. Arbitrary content, paths, user text, request payloads, and raw artifact identities remain outside ordinary metric dimensions.

### 4.6 Events and logs

Structured events are preferred for stable operational automation and correlation.

Diagnostic logs can carry human-readable context, but their fields remain classified and bounded. Log text does not become a canonical state model or machine authority.

Event and log contracts define:

- source;
- event or message class;
- severity;
- occurrence time;
- correlation and causation;
- subject scope;
- payload fields;
- classification;
- retention;
- sampling;
- redaction;
- routing.

### 4.7 Traces

Trace context crosses only declared integration boundaries.

A trace can correlate:

- client request to component query;
- component command to receiving component;
- artifact verification to activation;
- resource admission to job execution;
- publication request to gateway decision;
- recovery request to resulting state.

Trace context is not an authentication token or authority grant. Receiving components independently validate identity, authorization, contracts, and input.

### 4.8 Receipts and audit evidence

Operational views can reference decision and transition receipts.

Receipts support questions such as:

- why an operation was blocked;
- which policy decision applied;
- which resource grant admitted a job;
- which artifact verification covered activation;
- whether recovery completed;
- who accessed restricted diagnostics.

Selective-audit custody and disclosure remain distinct from ordinary operational telemetry. A dashboard can show a receipt outcome without receiving the complete private proof payload.

### 4.9 Access and views

Operational views are purpose-limited projections.

An authorized view can constrain:

- components;
- tenants;
- nodes;
- workspaces;
- profiles;
- signal classes;
- fields;
- time range;
- aggregation;
- destination;
- validity;
- export rights.

Administrative infrastructure access does not imply unrestricted observability access.

### 4.10 Resource and failure model

Telemetry competes for CPU, memory, I/O, network, storage, and operator attention.

The effective profile and Resource Governor bound:

- signal production;
- sample frequency;
- event volume;
- log rate;
- trace sampling;
- buffer size;
- retry count;
- export concurrency;
- query duration;
- storage growth;
- diagnostic package size;
- alert evaluation cost.

The observability system degrades deliberately rather than exhausting the observed system.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-OPS-OBS-001,REQ-OPS-OBS-002,REQ-OPS-OBS-003,REQ-OPS-OBS-004,REQ-OPS-OBS-005,REQ-OPS-OBS-006,REQ-OPS-OBS-007,REQ-OPS-OBS-008,REQ-OPS-OBS-009,REQ-OPS-OBS-010,REQ-OPS-OBS-011,REQ-OPS-OBS-012,REQ-OPS-OBS-013,REQ-OPS-OBS-014,REQ-OPS-OBS-015,REQ-OPS-OBS-016,REQ-OPS-OBS-017,REQ-OPS-OBS-018,REQ-OPS-OBS-019,REQ-OPS-OBS-020,REQ-OPS-OBS-021,REQ-OPS-OBS-022,REQ-OPS-OBS-023,REQ-OPS-OBS-024,REQ-OPS-OBS-025,REQ-OPS-OBS-026,REQ-OPS-OBS-027,REQ-OPS-OBS-028,REQ-OPS-OBS-029,REQ-OPS-OBS-030 -->
- **REQ-OPS-OBS-001 — SHALL:** Every observable signal has a stable signal identity or signal-type identity, source component, source instance, signal class, occurrence time, capture time, classification, retention class, and canonical owner.
- **REQ-OPS-OBS-002 — SHALL:** The observability model distinguishes health state, readiness state, operational metrics, structured events, diagnostic logs, traces, decision receipts, audit evidence, and capacity records.
- **REQ-OPS-OBS-003 — SHALL NOT:** A health, readiness, metric, event, log, trace, or dashboard state becomes component authority, policy authorization, resource admission, data ownership, release approval, or publication approval by implication.
- **REQ-OPS-OBS-004 — SHALL:** Each component owns the meaning and production contract of its signals while shared collectors and views own only declared transport, storage, indexing, aggregation, and presentation behavior.
- **REQ-OPS-OBS-005 — SHALL NOT:** An observability collector, dashboard, alerting system, trace backend, log store, or metrics store writes directly to component-owned authoritative state.
- **REQ-OPS-OBS-006 — SHALL:** Health indicates whether a component or dependency is operating within its declared internal validity conditions.
- **REQ-OPS-OBS-007 — SHALL:** Readiness indicates whether a component is prepared to accept a declared class of new work in the current profile, dependency, policy, trust, and resource context.
- **REQ-OPS-OBS-008 — SHALL NOT:** Health and readiness are treated as equivalent or used as substitutes for authorization, compatibility, integrity, trust, or evidence validation.
- **REQ-OPS-OBS-009 — SHALL:** A component can expose distinct readiness states for distinct interfaces, capabilities, tenants, profiles, or work classes when their admission conditions differ.
- **REQ-OPS-OBS-010 — SHALL:** Operational state and degradation signals identify the affected capability, scope, cause class, start time, current behavior, preserved capability, blocked capability, and recovery condition.
- **REQ-OPS-OBS-011 — SHALL:** Metrics use declared units, dimensions, aggregation semantics, collection intervals, reset behavior, precision, cardinality limits, and retention policies.
- **REQ-OPS-OBS-012 — SHALL NOT:** Unbounded tenant, user, request, artifact, path, content, or free-text values are used as metric dimensions.
- **REQ-OPS-OBS-013 — SHALL:** Structured operational events identify event class, source, subject scope, correlation, causation, severity, classification, occurrence time, and declared payload fields.
- **REQ-OPS-OBS-014 — SHALL:** Distributed traces use explicit propagation boundaries and record only the context required to correlate declared cross-component interactions.
- **REQ-OPS-OBS-015 — SHALL NOT:** Trace propagation silently transfers credentials, secret values, unrestricted personal data, private evidence payloads, cultural-rights content, or component-private business data.
- **REQ-OPS-OBS-016 — SHALL:** Logs, traces, metrics, events, profiles, dumps, and diagnostics apply field classification, minimization, redaction, sampling, and access controls before ordinary storage or export.
- **REQ-OPS-OBS-017 — SHALL NOT:** Secret values, private keys, recovery material, bearer credentials, raw authentication tokens, or credential-bearing configuration appear in ordinary observability output.
- **REQ-OPS-OBS-018 — SHALL:** Observability access is scoped by requester identity, role, purpose, component, tenant, profile, signal class, field set, time range, destination, and validity period.
- **REQ-OPS-OBS-019 — SHALL:** Access to restricted observability data and every export, diagnostic package, sampling override, retention override, or high-cardinality query produces a machine-readable receipt.
- **REQ-OPS-OBS-020 — SHALL:** Audit evidence and operational observability remain distinct even when one structured event or receipt contributes to both systems.
- **REQ-OPS-OBS-021 — SHALL:** Alert rules identify the source signals, evaluation window, thresholds or state conditions, suppression behavior, routing scope, deduplication key, escalation path, and recovery condition.
- **REQ-OPS-OBS-022 — SHALL NOT:** An alert alone performs privileged remediation, policy override, release activation, data mutation, destructive cleanup, or cross-component command execution.
- **REQ-OPS-OBS-023 — SHALL:** Automatic remediation triggered from observability follows an independently authorized command or workflow contract and records the triggering signals, authorization, performed action, result, and recovery state.
- **REQ-OPS-OBS-024 — SHALL:** Telemetry production, collection, buffering, retries, storage, querying, aggregation, export, profiling, and diagnostic capture remain bounded by active contracts and effective profile resource envelopes.
- **REQ-OPS-OBS-025 — SHALL:** When an observability path is unavailable, the source applies its declared drop, bounded-buffer, local-retention, backpressure, fail-closed, or degraded-observability behavior according to signal criticality.
- **REQ-OPS-OBS-026 — SHALL NOT:** Loss of optional metrics, traces, dashboards, or central collection disables a core component capability unless the active component or profile contract explicitly makes that signal path an authority prerequisite.
- **REQ-OPS-OBS-027 — SHALL:** Offline and disconnected profiles define local signal collection, bounded retention, clock-quality handling, custody, later synchronization, conflict handling, and proof of data gaps.
- **REQ-OPS-OBS-028 — SHALL:** Observability schema, signal, dashboard, alert, retention, sampling, and routing changes are versioned, reviewed for cardinality and disclosure impact, tested, and activated through their canonical owners.
- **REQ-OPS-OBS-029 — SHALL:** Validation detects missing signal ownership, invalid health or readiness semantics, unbounded cardinality, secret leakage, cross-tenant leakage, stale alerts, unbounded retention, broken correlation, unauthorized exports, and observability-induced component failure.
- **REQ-OPS-OBS-030 — SHALL:** Every active observability requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering a signal

Signal introduction:

1. identifies the owning component and decision;
2. defines signal identity, class, meaning, fields, unit, and dimensions;
3. defines classification, retention, sampling, routing, and profile applicability;
4. defines resource and cardinality budgets;
5. defines failure and degraded-observability behavior;
6. defines tests, alerts, dashboards, and evidence relationships;
7. validates disclosure and cross-tenant boundaries;
8. activates the canonical signal contract;
9. deploys collectors and views as derived consumers.

### 6.2 Evaluating health and readiness

Evaluation:

1. resolves the component and interface contract;
2. reads declared internal, dependency, trust, policy, resource, artifact, and lifecycle prerequisites;
3. evaluates health separately from work-class readiness;
4. records affected scope and reason codes;
5. exposes the current state through a bounded interface;
6. emits a transition event when the state changes;
7. triggers only independently authorized follow-up work.

### 6.3 Collecting and transporting signals

Collection:

1. authenticates the source and collector where required;
2. validates the signal envelope;
3. applies source-side classification, minimization, redaction, and sampling;
4. applies rate, size, and buffer limits;
5. transports through a declared route;
6. records gaps, drops, delays, and clock quality;
7. stores only declared fields and retention classes;
8. preserves correlation and source identity.

### 6.4 Creating alerts

Alert creation:

1. identifies the operational question;
2. selects canonical source signals;
3. defines evaluation window and state or threshold logic;
4. estimates cardinality, cost, and expected event rate;
5. defines deduplication, suppression, maintenance, and recovery behavior;
6. defines routing, ownership, escalation, and response expectations;
7. validates access and disclosure;
8. tests normal, degraded, failure, and recovery cases;
9. activates the versioned rule.

### 6.5 Performing automated remediation

Remediation:

1. receives an alert or state-transition trigger;
2. resolves the remediation command or workflow contract;
3. verifies identity and authorization;
4. obtains resource admission;
5. validates current state to avoid stale action;
6. performs the bounded operation through the owning component;
7. records trigger, authorization, action, result, and recovery state;
8. prevents repeated action beyond declared retry and deduplication bounds.

### 6.6 Handling disconnected operation

Offline handling:

1. applies the profile's local signal set and retention budget;
2. records clock quality and local sequence information;
3. preserves mandatory local receipts and evidence;
4. applies bounded buffering or declared dropping by signal criticality;
5. continues core capabilities that do not require central observability;
6. authenticates the synchronization destination on reconnection;
7. reconciles gaps, duplicates, time uncertainty, and custody;
8. records synchronization outcomes.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Signal contract is unresolved | Reject or isolate the signal | Source component authority | Signal ingestion and automation | Contract-resolution result |
| Health evaluation fails | Report unknown or failed health with scope | Existing authoritative state | Health-dependent routing | Health-evaluation record |
| Readiness dependency is unavailable | Report not ready for affected work class | Existing in-flight work where safe | New affected work | Readiness transition |
| Collector is unavailable | Use bounded local buffering or declared dropping | Source component operation | Central visibility | Collector-health state |
| Buffer reaches its limit | Apply priority, backpressure, or declared dropping | Higher-criticality signals | Lower-priority telemetry | Drop and gap counters |
| Metrics backend is unavailable | Preserve source operation and local health where possible | Core component capability | Historical metrics and dashboards | Backend-health state |
| Log or trace backend is unavailable | Apply bounded local retention or sampling reduction | Core component capability | Central diagnostics | Telemetry-path state |
| Secret or restricted field is detected | Redact, quarantine, or reject the signal | Non-sensitive telemetry | Affected signal delivery | Disclosure incident |
| Cardinality budget is exceeded | Reject or aggregate new series | Existing bounded metric set | High-cardinality detail | Cardinality-limit event |
| Query resource limit is reached | Cancel or truncate according to contract | Stored signals | Expensive query | Query-limit receipt |
| Alert evaluator is unavailable | Mark affected rules unknown and use declared fallback routing | Source signals | Automated alerting | Alert-system state |
| Alert route is unavailable | Queue within bounds or escalate through declared alternate route | Alert identity and source state | Recipient delivery | Routing outcome |
| Policy authority is unavailable | Keep restricted export or remediation blocked | Existing valid views and ordinary signals | New gated action | Policy-path state |
| Clock quality is insufficient | Record uncertainty and avoid false ordering claims | Signal payload and local sequence | Precise cross-source timing | Clock-quality record |
| Trace context is invalid | Start a new bounded trace or omit correlation | Request processing | End-to-end trace continuity | Propagation failure |
| Observability load harms the source | Reduce sampling, rate, or diagnostics within profile rules | Source workload | Telemetry detail | Self-protection event |

## 8. Cross-Component Interactions

### 8.1 Source components

Each component emits only signals defined by its active contract.

The component remains the owner of signal meaning and business state. A collector cannot infer a new component state model from arbitrary log text.

### 8.2 Resource Governor

Resource Governor can provide:

- telemetry production budgets;
- collector budgets;
- query admission;
- storage and export limits;
- profiling and diagnostic capture admission;
- backpressure and throttling decisions.

A resource grant controls consumption. It does not authorize disclosure or remediation.

### 8.3 Governance Policy Runtime

Governance Policy Runtime can authorize:

- restricted views;
- exports;
- diagnostic bundles;
- retention overrides;
- temporary sampling increases;
- gated remediation;
- cross-tenant or sensitive operational access.

The policy decision does not generate the signal or perform the remediation command.

### 8.4 Audit Broker

Audit Broker preserves declared receipts and restricted evidence.

Operational systems can consume authorized outcomes and links. They do not receive private proof merely because an event is operationally relevant.

### 8.5 Identity and Trust

Identity and Trust verifies sources, collectors, viewers, exporters, destinations, and remediation actors.

Trust verification remains scoped to the requested signal or operation and does not create component or policy authority.

### 8.6 Control plane and local nodes

A control plane can aggregate authorized node summaries, fleet health, capacity, release, and incident state.

Local nodes preserve their own component authority and declared offline behavior. Loss of central aggregation does not transfer node authority to stale control-plane state.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-OPS-OBS-001` | Establishes bounded, classified operational signals with explicit ownership and separation from authority and audit custody. |
| `DEC-DATA-001` | Preserves component data ownership and prohibits direct writes from observability systems. |
| `DEC-GOV-001` | Preserves the distinction between resource admission, policy authorization, and operational observation. |
| `DEC-AUD-001` | Separates ordinary observability from selective audit, restricted evidence, and public proof. |
| `DEC-PROFILE-001` | Keeps signal detail, topology, retention, offline behavior, and implementation mechanisms profile-scoped. |

### Prohibited assumptions

- a green dashboard proves authorization, compatibility, or trust;
- a healthy component is ready for every class of work;
- a ready component is authorized to accept a specific request;
- logs are a canonical component state model;
- a metrics store owns the measured business data;
- trace context can carry credentials or authority;
- every event belongs in a public or globally visible stream;
- every signal needs indefinite retention;
- more telemetry always improves reliability;
- arbitrary labels are acceptable metric dimensions;
- central observability is required for all local operation;
- an alert can directly mutate component state;
- a collector administrator owns component data;
- one profile's detailed telemetry applies globally;
- an offline node can discard mandatory receipts;
- a missing signal implies a successful state;
- an unavailable policy authority permits restricted export;
- dashboards and audit evidence are interchangeable;
- operator access to the host grants unrestricted tenant observability.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-OPS-001` is active at `08-operations/01-observability.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. Every active signal resolves one canonical owner and one signal contract.
7. Health and readiness remain distinct and work-class readiness is expressible.
8. Signal state never substitutes for authorization, trust, compatibility, integrity, or resource admission.
9. Metric units, dimensions, aggregation, intervals, reset behavior, cardinality, and retention are declared.
10. Metric dimensions exclude unbounded content and free text.
11. Events and traces preserve source, scope, correlation, classification, and declared fields.
12. Trace propagation carries no credentials or unrestricted sensitive payload.
13. Logs, metrics, events, traces, dumps, and diagnostics apply minimization and redaction.
14. Ordinary observability output contains no secret or private-key material.
15. Tenant, component, profile, node, and workspace views enforce scope boundaries.
16. Restricted access and export map to decision receipts.
17. Audit evidence and operational telemetry remain distinguishable.
18. Alerts define source, evaluation, suppression, routing, deduplication, escalation, and recovery.
19. Automatic remediation resolves an independent authorization and component command.
20. Telemetry production, storage, queries, exports, and diagnostics are bounded.
21. Optional observability failure does not disable unrelated core capability.
22. Offline profiles define local collection, retention, timing, gaps, and reconciliation.
23. Observability changes receive cardinality, performance, disclosure, and compatibility review.
24. Observability systems contain no direct write path to component-owned authoritative data.
25. Critical operational paths map to tests and evidence.
26. Active prose is English and contains no unresolved-authority marker.
27. No normative keyword appears outside the generated requirement block.
28. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates health and readiness separation.

A service can be healthy because its internal state is valid while reporting not ready for new jobs because its resource queue has reached the profile-defined admission limit.

> **Non-normative example:** This example illustrates bounded metrics.

A request counter can use component, operation class, outcome class, and profile as controlled dimensions. It does not use the full URL, user name, document title, or raw artifact identifier as labels.

> **Non-normative example:** This example illustrates selective trace context.

Orgo can call Publication Gateway with a correlation identifier and operation class. The trace does not carry Orgo database credentials or the private publication candidate payload.

> **Non-normative example:** This example illustrates optional central collection.

A sovereign-offline node can continue local operation while central metrics collection is unavailable. It preserves mandatory local receipts and bounded operational signals for later reconciliation.

> **Non-normative example:** This example illustrates authorized remediation.

A disk-capacity alert can trigger a governed cleanup workflow. The workflow independently verifies authorization and executes through the owning component rather than allowing the alert rule to delete data directly.
