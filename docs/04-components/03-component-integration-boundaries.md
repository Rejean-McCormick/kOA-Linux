<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-003",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/component-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/system.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-INT-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-GATE-001",
    "DEC-AI-001",
    "DEC-SENT-001",
    "DEC-UCKK-001",
    "DEC-OFFLINE-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001"
  ],
  "requirement_ids": [
    "REQ-COMP-INT-001",
    "REQ-COMP-INT-002",
    "REQ-COMP-INT-003",
    "REQ-COMP-INT-004",
    "REQ-COMP-INT-005",
    "REQ-COMP-INT-006",
    "REQ-COMP-INT-007",
    "REQ-COMP-INT-008",
    "REQ-COMP-INT-009",
    "REQ-COMP-INT-010",
    "REQ-COMP-INT-011",
    "REQ-COMP-INT-012",
    "REQ-COMP-INT-013",
    "REQ-COMP-INT-014",
    "REQ-COMP-INT-015",
    "REQ-COMP-INT-016",
    "REQ-COMP-INT-017",
    "REQ-COMP-INT-018",
    "REQ-COMP-INT-019",
    "REQ-COMP-INT-020",
    "REQ-COMP-INT-021",
    "REQ-COMP-INT-022",
    "REQ-COMP-INT-023",
    "REQ-COMP-INT-024",
    "REQ-COMP-INT-025",
    "REQ-COMP-INT-026",
    "REQ-COMP-INT-027",
    "REQ-COMP-INT-028"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-SENT-001",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002",
    "LOCK-OFFLINE-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-INT-001",
    "LOCK-INT-002",
    "LOCK-INT-003",
    "LOCK-INT-004",
    "LOCK-INT-005"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-SYS-004",
    "DOC-COMP-000"
  ],
  "tags": [
    "component",
    "integration",
    "boundaries",
    "data-authority",
    "interfaces",
    "events",
    "gateways",
    "versioning"
  ]
}
KOA:DOC-META:END -->

# Component Integration Boundaries

## 1. Purpose

This document defines the global integration boundaries between kOA components. It establishes how components exchange commands, queries, events, artifacts, configuration, evidence, and governed requests without collapsing their independent responsibilities or data authority.

The integration model is designed to preserve:

- explicit component ownership;
- stable and versioned contracts;
- authenticated and scoped communication;
- bounded data movement;
- deterministic acceptance of received material;
- safe retries and replay;
- local and offline continuity;
- selective observability;
- independent component evolution;
- profile-specific deployment without profile-specific authority drift.

The objective is not to maximize connectivity. The objective is to permit only the connectivity required for a declared capability while keeping every component independently understandable, testable, replaceable, recoverable, and removable.

## 2. Scope

### 2.1 Global applicability

This document applies to every active kOA component and to every connection between:

- two components in one process;
- two components on one host;
- two components in separate containers;
- two components on separate hosts;
- a component and a gateway;
- a component and an external integration;
- a component and an artifact repository;
- a component and a message broker;
- a component and a local or remote profile service;
- a component and a migration or validation tool.

The same authority rules apply regardless of whether the transport is an in-process call, Unix socket, local HTTP interface, network API, event stream, queue, file exchange, artifact import, or administrative operation.

### 2.2 Permitted integration classes

The supported integration classes are:

| Integration class | Intended use |
| --- | --- |
| Versioned component API | Bounded commands, queries, and status operations. |
| Declared event contract | Asynchronous facts emitted by an owning component. |
| Governed gateway request | Publication, admission, or another cross-domain operation. |
| Verified artifact exchange | Immutable or versioned packages validated before use. |
| Runtime Pack or Exchange package | Controlled knowledge-runtime distribution. |
| PGF and language manifest | Deterministic language-runtime activation. |
| Atlas Pack | Structured Ariane navigation capability. |
| Validated configuration | Explicit component configuration owned by the deployment contract. |
| Evidence reference | Selective proof without direct access to another component’s internal evidence store. |
| Explicit migration contract | Versioned state transformation during a controlled migration. |

### 2.3 Prohibited integration classes

The following patterns are outside the integration model:

- direct writes to another component’s authoritative database;
- direct mutation of another component’s internal files;
- shared mutable application tables without an explicit single owner;
- unversioned shared state used as an implicit interface;
- network reachability treated as authorization;
- a valid signature treated as sufficient authority;
- direct publication that bypasses Publication Gateway;
- direct UCKK admission that bypasses UCKK Dimension Gateway;
- external-service output written directly into authoritative data;
- a message broker used as an undeclared universal database;
- a cache used as authoritative state;
- an implementation recipe used as a component contract;
- an internal library call used to bypass a documented boundary.

### 2.4 Profile and transport independence

A profile selects components, deployment mechanisms, and permitted integrations. It does not change the ownership of component data or decisions.

A transport can vary by profile when the contract semantics remain equivalent. For example, a local deployment can use a Unix socket while a hub deployment uses mutually authenticated network transport. The change in transport does not broaden the operation, audience, identity, or data authority.

### 2.5 Explicit non-goals

This document does not:

- define every component’s internal architecture;
- define the payload of every artifact;
- assign profile membership;
- assign release-channel membership;
- replace component contracts;
- replace integration manifests;
- make all components mutually reachable;
- require a central service bus;
- require Kubernetes;
- require containers;
- require Internet connectivity;
- create a global shared database;
- make an external AI surface part of the native component model.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `generated/component-catalog.json` | Owns component identities, responsibilities, authoritative data domains, and primary interfaces. |
| `contracts/integration-types.contract.json` | Owns registered integration identities, participants, declared data movement, direction, transport class, and lifecycle. |
| `contracts/system.contract.json` | Owns system-wide authority boundaries, component relationships, gateways, offline behavior, and safe degradation. |
| `generated/requirements-index.json` | Owns the normative requirement statements rendered in Section 5. |
| `generated/assertion-index.json` | Owns cross-file assertions preserving integration, data, gateway, AI, offline, and lifecycle alignment. |

Additional contract ownership is distributed as follows:

- `generated/component-catalog.json` owns component-contract discovery and path mapping;
- individual files under `contracts/components/` own component-specific behavior;
- individual files under `contracts/artifact-contracts/` own payload and artifact structure;
- `generated/profile-catalog.json` and profile contracts own deployment selection;
- `contracts/release-channels.contract.json` owns release-channel identities;
- `generated/evidence-catalog.json` owns evidence records;
- `generated/exception-index.json` owns approved bounded deviations.

## 4. Model and Responsibilities

### 4.1 Ownership model

Every authoritative datum has one logical owning component.

The owner is responsible for:

- validating mutations;
- assigning stable identity;
- maintaining lifecycle state;
- preserving invariants;
- authorizing read and write operations;
- producing outbound events or artifacts;
- accepting or rejecting inbound candidate material;
- exposing supported status and recovery operations.

Another component can hold:

- a reference;
- a bounded read model;
- a cache;
- an immutable artifact;
- a candidate import;
- a receipt;
- a replay checkpoint.

None of these automatically becomes a second authoritative copy.

### 4.2 Command, query, and event model

A command requests a state change from the owning component.

A query requests a bounded representation without transferring ownership.

An event records a fact that the emitting component has already accepted into its authoritative state.

A consumer does not reinterpret an event as permission to mutate the emitter. It updates only its own state through its own acceptance rules.

Commands and events remain distinct. Publishing an event is not equivalent to accepting a command, and receiving an event is not equivalent to acknowledging successful downstream processing.

### 4.3 Contract identity and versioning

Every integration identifies:

- participating components;
- direction;
- operation class;
- payload contract;
- contract version;
- authentication method;
- authorization scope;
- tenant or authority domain where applicable;
- idempotency behavior;
- retry behavior;
- ordering expectations;
- error model;
- retention;
- observability;
- offline behavior;
- lifecycle compatibility.

A breaking contract change uses a new compatible version boundary. Silent semantic reinterpretation under an unchanged version is prohibited.

### 4.4 Identity and scope propagation

Every cross-component request carries the context required by the receiving contract, including where applicable:

- caller component identity;
- end-user or service identity;
- tenant;
- authority domain;
- delegated role;
- requested action;
- object scope;
- purpose;
- audience;
- correlation identifier;
- idempotency identifier;
- policy decision reference;
- consent reference;
- trace context.

The receiver validates the context independently. A caller cannot assert that authorization has occurred without a verifiable decision or accepted delegation contract.

### 4.5 Data minimization

A producer sends the smallest representation sufficient for the declared operation.

The integration contract identifies fields that are:

- required;
- optional;
- prohibited;
- sensitive;
- restricted;
- tenant-scoped;
- ephemeral;
- safe for logs;
- safe for public evidence.

A consumer cannot require unrestricted database access merely because a bounded API is inconvenient.

### 4.6 Acceptance model

Received material is classified as one of:

- authoritative command input;
- verified immutable artifact;
- candidate import;
- informational event;
- cacheable read model;
- evidence reference;
- rejected input.

A candidate import becomes authoritative only after the receiving component validates and accepts it.

External AI output, SenTient output, migration output, generated context, and external integration output are candidate material unless another active contract explicitly defines a stronger verified artifact class.

### 4.7 Gateway model

Gateways mediate authority transitions.

Publication Gateway mediates governed release from one disclosure or authority domain to another.

UCKK Dimension Gateway mediates controlled admission of user-selected media into a UCKK dimension.

The gateways can exchange references or receipts, but their responsibilities, data, decisions, and execution paths remain separate.

### 4.8 Governance and resource separation

Governance Policy Runtime evaluates authorization, disclosure, consent, privilege, and governed exceptions.

Resource Governor controls CPU, memory, storage, process, queue, network, and activation budgets.

An integration can depend on both services, but one decision cannot substitute for the other.

### 4.9 Asynchronous delivery

Asynchronous integrations define:

- message identity;
- producer identity;
- schema version;
- aggregate or object identity;
- ordering key where needed;
- occurrence time;
- acceptance time;
- retry count;
- expiry;
- deduplication behavior;
- dead-letter or quarantine behavior;
- replay behavior.

A broker transports messages. It does not own the business fact and does not decide whether the consumer accepts it.

### 4.10 Configuration boundary

Configuration is accepted only through a declared configuration contract.

Deployment-specific values such as endpoint addresses, service identities, feature activation, resource budgets, and secret references belong to deployment or profile configuration.

A component contract cannot depend on an undeclared environment variable, hidden shared file, or operator convention for correctness.

### 4.11 Administrative boundary

Administrative interfaces are separate from application interfaces.

Administrative actions require:

- strong authentication;
- explicit authorization;
- narrow operation identifiers;
- bounded parameters;
- audit evidence;
- safe retry behavior;
- clear failure state.

Administrative access does not grant application data authority or cultural authority.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-COMP-INT-001,REQ-COMP-INT-002,REQ-COMP-INT-003,REQ-COMP-INT-004,REQ-COMP-INT-005,REQ-COMP-INT-006,REQ-COMP-INT-007,REQ-COMP-INT-008,REQ-COMP-INT-009,REQ-COMP-INT-010,REQ-COMP-INT-011,REQ-COMP-INT-012,REQ-COMP-INT-013,REQ-COMP-INT-014,REQ-COMP-INT-015,REQ-COMP-INT-016,REQ-COMP-INT-017,REQ-COMP-INT-018,REQ-COMP-INT-019,REQ-COMP-INT-020,REQ-COMP-INT-021,REQ-COMP-INT-022,REQ-COMP-INT-023,REQ-COMP-INT-024,REQ-COMP-INT-025,REQ-COMP-INT-026,REQ-COMP-INT-027,REQ-COMP-INT-028 -->
- **REQ-COMP-INT-001 — SHALL:** Every cross-component integration identify its participants, direction, operation class, payload contract, version, authority scope, transport class, lifecycle, and failure behavior.
- **REQ-COMP-INT-002 — SHALL:** Every authoritative datum have one logical owning component.
- **REQ-COMP-INT-003 — SHALL NOT:** A component write directly into another component’s authoritative database, files, object store, queue state, or internal mutable structures.
- **REQ-COMP-INT-004 — SHALL:** Cross-component mutation occur through a versioned command API, governed gateway, declared event-driven acceptance flow, verified artifact import, or explicit migration contract.
- **REQ-COMP-INT-005 — SHALL:** The receiving component independently validate identity, authorization, tenant or authority scope, payload, contract version, and acceptance conditions.
- **REQ-COMP-INT-006 — SHALL NOT:** Network location, process co-location, container membership, host administration, or a valid signature be treated as sufficient authorization.
- **REQ-COMP-INT-007 — SHALL:** Integrations transmit the minimum data required for the declared operation and preserve applicable confidentiality, consent, audience, provenance, and retention restrictions.
- **REQ-COMP-INT-008 — SHALL NOT:** Secrets, unrestricted credentials, or unnecessary protected content be embedded in events, logs, traces, configuration files, or receipts.
- **REQ-COMP-INT-009 — SHALL:** Commands, queries, events, artifacts, candidate imports, evidence references, and receipts remain distinguishable.
- **REQ-COMP-INT-010 — SHALL NOT:** Receipt of an event, artifact, generated output, SenTient result, or external-service result make that material authoritative without receiving-component acceptance.
- **REQ-COMP-INT-011 — SHALL:** Every mutation-capable request use a stable request identity or idempotency key and define duplicate handling.
- **REQ-COMP-INT-012 — SHALL:** Asynchronous consumers be replay-safe and define ordering, deduplication, expiry, retry, quarantine, and terminal-failure behavior.
- **REQ-COMP-INT-013 — SHALL NOT:** A retry broaden identity, scope, purpose, audience, payload, destination, or authority.
- **REQ-COMP-INT-014 — SHALL:** Breaking interface or payload changes use explicit version evolution and compatibility validation.
- **REQ-COMP-INT-015 — SHALL NOT:** An unchanged contract version silently change field meaning, authority semantics, acceptance behavior, or failure behavior.
- **REQ-COMP-INT-016 — SHALL:** Missing, ambiguous, expired, revoked, or incompatible authority fail closed for the affected operation.
- **REQ-COMP-INT-017 — SHALL:** Unrelated component capabilities continue when a bounded integration fails and continued operation is safe.
- **REQ-COMP-INT-018 — SHALL:** Queued operations be revalidated after reconnection or material authority change before transmission, acceptance, publication, or activation.
- **REQ-COMP-INT-019 — SHALL:** Publication Gateway mediate governed cross-domain publication.
- **REQ-COMP-INT-020 — SHALL:** UCKK Dimension Gateway mediate controlled admission into UCKK.
- **REQ-COMP-INT-021 — SHALL NOT:** Publication Gateway and UCKK Dimension Gateway share authority state, substitute for one another, or be bypassed through direct component integration.
- **REQ-COMP-INT-022 — SHALL:** Governance Policy Runtime and Resource Governor remain separate authorities even when one integration depends on both.
- **REQ-COMP-INT-023 — SHALL NOT:** External AI, external creative services, or SenTient write authoritative component data directly.
- **REQ-COMP-INT-024 — SHALL:** Administrative interfaces remain separate from application interfaces and use narrow authenticated, authorized, and audited operations.
- **REQ-COMP-INT-025 — SHALL:** Integration observability expose health, latency, queue, retry, rejection, compatibility, and correlation state without indiscriminate protected-data disclosure.
- **REQ-COMP-INT-026 — SHALL:** Release activation validate component-contract, integration-contract, payload-schema, profile, migration, and cross-channel compatibility.
- **REQ-COMP-INT-027 — SHALL NOT:** A profile, transport, recipe, generated context, deployment convenience, or shared implementation process silently transfer component authority.
- **REQ-COMP-INT-028 — SHALL:** Integration removal leave each participating component in a defined state and preserve unrelated local capabilities, authoritative data, evidence, and recovery paths.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Integration registration

A new integration is registered through this sequence:

1. Identify the capability that requires communication.
2. Identify the owning component for every authoritative datum.
3. Identify producer and consumer roles.
4. Select the permitted integration class.
5. Define the operation, direction, scope, and data minimization.
6. Define the payload or artifact contract.
7. Define identity, authorization, tenant, consent, and governance context.
8. Define idempotency, ordering, retries, expiry, and quarantine.
9. Define offline and reconnection behavior.
10. Define observability and evidence.
11. Define versioning and removal behavior.
12. Add the integration to `contracts/integration-types.contract.json`.
13. Add or update component contracts.
14. Add tests, locks, traceability, and evidence requirements.
15. Activate only after validation passes.

### 6.2 Synchronous request flow

The synchronous request flow is:

```text
constructed
  -> authenticated
  -> authorized
  -> contract_validated
  -> accepted | denied | blocked
  -> executed
  -> committed
  -> responded
```

The response distinguishes validation failure, authorization denial, blocked authority, conflict, resource exhaustion, dependency unavailability, and internal failure.

A timeout does not prove that execution failed. The caller uses the idempotency identifier or status interface before retrying.

### 6.3 Asynchronous event flow

The event flow is:

```text
fact_committed_by_owner
  -> event_created
  -> event_published
  -> event_delivered
  -> consumer_validated
  -> consumer_accepted | rejected | quarantined
  -> consumer_state_committed
  -> checkpoint_advanced
```

A consumer checkpoint advances only after its own state commit or another declared durable acceptance point.

### 6.4 Candidate import flow

Candidate material follows this sequence:

1. Receive the candidate through a declared boundary.
2. Record source and provenance.
3. Validate payload structure and size.
4. Verify applicable integrity evidence.
5. Scan or inspect according to the artifact policy.
6. Validate authority, audience, consent, and destination.
7. Resolve semantic or business acceptance rules.
8. Accept into component-owned authoritative state, retain as non-authoritative candidate, quarantine, or reject.
9. Produce an acceptance or rejection receipt.
10. Notify downstream integrations only after authoritative acceptance.

### 6.5 Offline queue flow

When a remote dependency is unavailable:

1. Determine whether queueing is permitted for the operation.
2. Persist the exact request and authority context.
3. Record contract versions and source identity.
4. Mark the request as pending and not authorized for automatic release.
5. Preserve local component operation.
6. On reconnection, refresh identity, trust, consent, policy, version, target, time, and conflict state.
7. Release only requests that still pass.
8. Retain, cancel, or replace invalid requests with a new explicit operation.

### 6.6 Contract upgrade flow

A contract upgrade proceeds through:

1. Publish the candidate contract.
2. Identify producers and consumers.
3. Determine backward and forward compatibility.
4. Provide adapters or parallel-version operation when required.
5. Validate migrations and replay behavior.
6. Test rollback or forward repair.
7. Update profile and Release Set compatibility.
8. Activate the candidate contract.
9. Observe errors and consumer acceptance.
10. Retire the old version only after all required consumers have migrated.

### 6.7 Integration removal flow

Removal proceeds through:

1. Stop new use of the integration.
2. Drain or explicitly cancel queued operations.
3. Resolve in-flight requests.
4. Export or preserve required receipts and evidence.
5. Remove credentials and trust scopes.
6. Remove endpoints, routes, subscriptions, and service identities.
7. Preserve component-owned authoritative data.
8. Remove caches and non-authoritative replicas according to policy.
9. Validate unrelated component capabilities.
10. Record completion and unresolved external dependencies.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Caller identity invalid | Reject before business execution. | Receiving component health and unrelated operations | Requested operation |
| Authorization missing | Deny or block according to authority state. | Safe reads and unrelated actions | Protected action |
| Contract version unsupported | Return explicit incompatibility. | Existing supported versions | Unsupported request |
| Payload invalid | Reject and record bounded diagnostics. | Service availability | Invalid mutation |
| Idempotency key reused with different payload | Reject as conflict. | Original request result | Ambiguous duplicate |
| Timeout after possible execution | Require status lookup or idempotent retry. | Existing committed state | Blind duplicate execution |
| Event delivered more than once | Deduplicate or replay safely. | Consumer correctness | Duplicate effect |
| Event arrives out of order | Buffer, reject, or reconcile by contract. | Previously accepted state | Invalid sequence |
| Queue full | Apply backpressure and reject new work visibly. | Committed state and critical traffic | Unbounded enqueue |
| Message expired | Quarantine or discard with evidence. | Current valid work | Stale execution |
| Consumer unavailable | Retain bounded durable work or report failure. | Producer authoritative state | Immediate downstream effect |
| Broker unavailable | Preserve producer state and local operation. | Component-local capability | Event transport |
| Governance runtime unavailable | Block governed operations. | Ungoverned local functions where safe | New governed decision |
| Resource Governor unavailable | Apply declared safe static limits or block heavy activation. | Essential bounded services | Uncontrolled heavy work |
| Publication Gateway unavailable | Keep publication unexecuted. | Source editing and storage | Cross-domain publication |
| UCKK Dimension Gateway unavailable | Preserve existing UCKK content. | Read, export, backup | New governed admission |
| External service unavailable | Disable that integration only. | Native local capability | External assistance |
| External result invalid | Quarantine or reject. | Original authoritative data | Authoritative import |
| Reconnection changes authority | Keep queued request blocked or cancelled. | Local state and evidence | Automatic release |
| Partial remote effect | Enter remediation and prevent silent retry. | Recorded state and recovery | False completion |
| Database of another component unavailable | Do not bypass through direct storage access. | Own component state | Cross-boundary shortcut |
| Observability sink unavailable | Continue bounded local capture where policy allows. | Component operation | Remote telemetry |
| Trust or time uncertain | Block affected time-sensitive or trust-sensitive operation. | Non-sensitive local work | Sensitive exchange |
| Integration removed | Use declared removal state. | Participating components and data | Removed capability |

Safe degradation preserves authority boundaries. It does not introduce shared databases, hidden fallback providers, unbounded retries, implicit publication, direct filesystem mutation, or automatic authority expansion.

## 8. Cross-Component Interactions

### 8.1 Konnaxion and Orgo

Konnaxion owns public-domain application and participation state. Orgo owns private cases, tasks, assignments, approvals, and workflow state.

Public representation of Orgo data is produced through an explicit bounded publication request. Konnaxion does not query or write Orgo’s private database directly.

### 8.2 Kristal and consuming applications

Kristal Runtime owns accepted knowledge artifacts, Runtime Packs, Exchange packages, validation state, and query contracts.

A consuming component references or queries Kristal through a declared interface. Application workflow state remains with the consuming component.

### 8.3 GF Wordbench and SemantiK Architect Runtime

GF Wordbench owns grammar source projects and language build inputs.

SemantiK Architect Runtime consumes verified PGF artifacts and language manifests for deterministic rendering. Runtime use does not grant the runtime authority to edit grammar sources.

### 8.4 Ariane and applications

Ariane produces bounded navigation or action requests through approved application interfaces.

The receiving application validates the request and commits its own data. Ariane does not gain direct database access and does not become the application’s authorization authority.

### 8.5 UCKK Platform and its gateways

UCKK Dimension Gateway validates controlled admission into UCKK.

UCKK Platform owns accepted media objects, versions, collections, provenance, access rules, and component-owned derivatives.

Publication Gateway separately mediates release to another domain or audience.

### 8.6 Identity, governance, audit, and resources

Identity and Trust resolves identity, delegation, trust, and revocation.

Governance Policy Runtime evaluates governed decisions.

Audit Broker brokers selective evidence and disclosure.

Resource Governor controls deterministic resource allocation and service activation.

A business component can depend on all four services while retaining ownership of its business data.

### 8.7 SenTient and Kristal

SenTient can consume bounded material and produce candidate resolution output with provenance.

Kristal Runtime accepts or rejects the candidate through a controlled import path. SenTient does not mutate accepted knowledge directly.

### 8.8 Node Agent and hosted components

kOA Node Agent performs allowlisted lifecycle and host operations.

Hosted components request narrow operations rather than obtaining general host privilege. The agent does not become the owner of component state or release authority.

### 8.9 External integrations

An external integration uses an approved integration manifest and bounded transfer.

The responsible component accepts returned material through its own contract. Removal of the integration leaves native local capabilities intact where those capabilities do not depend on the external surface.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the integration model.

The following assumptions are prohibited:

1. Components in the same process share authority.
2. Components on the same host can read one another’s storage.
3. A shared database engine implies shared tables or identities.
4. A shared message broker owns business events.
5. A network allow rule is authorization.
6. A valid signature is a complete trust decision.
7. An administrator can bypass application contracts.
8. A query result can be edited and written back without a command contract.
9. Event delivery proves consumer acceptance.
10. A timeout proves no effect occurred.
11. A retry can use a new or broader scope.
12. An event can replace a command for mutation.
13. A cache is authoritative because it is current.
14. A candidate import is authoritative because it passed syntax validation.
15. External AI output is authoritative.
16. SenTient output is accepted knowledge.
17. UCKK admission authorizes publication.
18. Publication authorizes UCKK admission.
19. Governance Policy Runtime controls resources.
20. Resource Governor decides consent or disclosure.
21. Offline queueing preserves authorization indefinitely.
22. Reconnection authorizes automatic transmission.
23. A profile can silently change data ownership.
24. A transport change can silently change operation semantics.
25. A shared implementation process can collapse gateway responsibilities.
26. A recipe or example is a versioned interface.
27. A migration can write arbitrary cross-component state.
28. Integration removal permits deletion of another component’s authoritative data.

A missing contract, unresolved authority, incompatible version, unverified identity, ambiguous scope, or failed acceptance condition leaves the affected operation blocked.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-COMP-003`.
2. Its path is `04-components/03-component-integration-boundaries.md`.
3. Its class is `normative_markdown`.
4. Its status is `active`.
5. Its language is `en`.
6. Its layer is `component`.
7. Its scope is `global`.
8. Its metadata matches `generated/document-index.json`.
9. Every canonical reference resolves.
10. Every listed decision resolves with accepted status.
11. Every listed requirement resolves and matches the generated block.
12. Every listed lock resolves and passes.
13. The eleven mandatory sections exist in the required order.
14. Normative keywords occur only in the generated requirements block.
15. Every active component has one component contract.
16. Every registered integration resolves to active participants.
17. Every authoritative data class has one logical owner.
18. Direct cross-component authoritative writes fail validation.
19. Every mutation path uses a permitted integration class.
20. Every mutation-capable request has stable identity and duplicate behavior.
21. Every asynchronous integration defines ordering, retry, expiry, deduplication, quarantine, and replay.
22. Every breaking change has explicit version evolution.
23. Identity, tenant, authority, purpose, and correlation context are validated where applicable.
24. Data minimization and confidentiality checks pass.
25. External and SenTient outputs remain non-authoritative until accepted.
26. Publication Gateway and UCKK Dimension Gateway separation tests pass.
27. Governance Policy Runtime and Resource Governor separation tests pass.
28. Offline queues do not release automatically after reconnection.
29. Integration removal preserves component-owned data and unrelated capabilities.
30. Release activation validates component, integration, artifact, profile, migration, and Release Set compatibility.
31. Observability excludes secrets and unnecessary protected content.
32. Traceability and active evidence are complete.
33. No unresolved marker, provisional value, parallel authority, or file-content hash requirement appears.
34. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Orgo publication to Konnaxion

Orgo creates a bounded publication request for an approved public summary. Publication Gateway evaluates identity, consent, policy, audience, and representation. Konnaxion receives only the approved representation and stores its own public-domain record.

### 11.2 Duplicate command

A caller retries a task-creation command after a timeout using the same idempotency key. Orgo returns the existing task result rather than creating a duplicate.

### 11.3 Event replay

A consumer rebuilds a local read model from recorded component events. Duplicate events are ignored by event identity, and the consumer commits its checkpoint only after its own state update succeeds.

### 11.4 External AI candidate

A component sends minimized text to an approved external surface. The returned result is stored as candidate material with provenance. The component validates and explicitly accepts selected content before updating authoritative state.

### 11.5 SenTient candidate resolution

SenTient proposes a bounded ambiguity resolution. Kristal Runtime receives the proposal through a controlled import interface and rejects it because required provenance is incomplete. Existing accepted knowledge remains unchanged.

### 11.6 Local transport variation

A lightweight endpoint uses a Unix socket for the same versioned interface that a sovereign hub exposes through mutually authenticated HTTPS. Identity, operation, payload, errors, and authority semantics remain equivalent.

### 11.7 Broker outage

Orgo commits a workflow state change while the broker is unavailable. It records the outbound event durably and publishes it later. The workflow commit does not depend on another component writing into Orgo’s database.

### 11.8 Reconnection revalidation

A publication request is queued while offline. Consent expires before connectivity returns. Revalidation denies the request, and no publication occurs.

### 11.9 Integration removal

An optional external translation integration is removed. Credentials, routes, and pending transfers are cleared. Local deterministic rendering and user-authored content remain available.

### 11.10 Partial delivery

A destination accepts one part of a multi-object transfer before failing. The integration records partial delivery, enters remediation, and does not report complete success or retry the entire request blindly.
