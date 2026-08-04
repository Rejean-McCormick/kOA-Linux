<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-CONST-007",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "constitution",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "contracts/integration-types.contract.json"
  ],
  "decision_ids": [
    "DEC-CONST-COMP-001",
    "DEC-SYS-DATA-001",
    "DEC-SYS-GOV-001",
    "DEC-SYS-GATE-001",
    "DEC-SYS-SENT-001",
    "DEC-SYS-KRISTAL-001"
  ],
  "requirement_ids": [
    "REQ-CONST-COMP-001",
    "REQ-CONST-COMP-002",
    "REQ-CONST-COMP-003",
    "REQ-CONST-COMP-004",
    "REQ-CONST-COMP-005",
    "REQ-CONST-COMP-006",
    "REQ-CONST-COMP-007",
    "REQ-CONST-COMP-008",
    "REQ-CONST-COMP-009",
    "REQ-CONST-COMP-010",
    "REQ-CONST-COMP-011",
    "REQ-CONST-COMP-012",
    "REQ-CONST-COMP-013",
    "REQ-CONST-COMP-014",
    "REQ-CONST-COMP-015",
    "REQ-CONST-COMP-016"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-SENT-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-000",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005"
  ],
  "tags": [
    "constitution",
    "component-separation",
    "canonical-ownership",
    "data-authority",
    "cross-component-contracts",
    "safe-degradation"
  ]
}
KOA:DOC-META:END -->

# Component Separation

## 1. Purpose

This document defines component separation as a global constitutional property of the kOA operating environment.

It explains how active components preserve distinct responsibility, data ownership, authority, lifecycle, and failure boundaries while participating in one system. It also establishes the conditions under which components exchange data, requests, artifacts, events, evidence, and policy decisions.

The deterministic outcome is a system in which component composition does not create implicit shared authority, hidden coupling, or cross-component state mutation.

## 2. Scope

This document applies globally to:

- every component registered in `generated/component-catalog.json`;
- every component contract under `contracts/components/`;
- every deployment profile and profile overlay;
- every cross-component API, event, queue, artifact exchange, gateway, broker, and shared infrastructure dependency;
- every component-owned data set, state machine, receipt, and externally observable capability;
- development, runtime, lifecycle, security, operations, and conformance behavior where component boundaries are involved.

This document defines logical separation. Physical isolation is governed by active profile, security, and deployment contracts.

This document does not:

- define the internal implementation of a component;
- require one process, container, virtual machine, database server, or physical host per component;
- prohibit shared infrastructure when logical ownership and access controls remain explicit;
- define profile membership or deployment topology;
- define the detailed payload of a component interface;
- authorize direct access to another component's private implementation.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `generated/decision-index.json#/decisions` | Owns accepted decisions that establish or change component boundaries. |
| `contracts/system.contract.json#/component_model` | Owns the global component model and system-level dependency rules. |
| `generated/component-catalog.json#/components` | Owns component identities, responsibilities, classifications, dependencies, and authoritative data ownership. |
| `generated/component-catalog.json#/components` | Indexes the active observable contracts for individual components. |
| `contracts/integration-types.contract.json#/integrations` | Owns classified external and cross-domain integration identities. |
| `generated/requirements-index.json#/requirements` | Owns the normative requirement statements displayed in Section 5. |
| `generated/assertion-index.json#/locks` | Owns component, data, governance-authority, gateway, and SenTient alignment locks. |
| `generated/traceability.json#/links` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/profile-catalog.json#/profiles` | Owns profile membership and profile-dependent deployment conditions. |

## 4. Model and Responsibilities

### 4.1 Component boundary

A component boundary contains:

- one stable component identity;
- a declared system responsibility;
- authoritative data and state ownership;
- observable interfaces and accepted input classes;
- produced events, artifacts, and receipts;
- dependency direction;
- failure ownership;
- lifecycle and compatibility obligations;
- applicable profiles, requirements, locks, and evidence.

The component registry owns component identity and high-level responsibility. The individual component contract owns observable interface behavior. Internal implementation remains private unless another active contract explicitly exposes it.

### 4.2 Logical ownership and physical deployment

Logical ownership does not depend on physical deployment.

Several components can use:

- one database server;
- one message transport;
- one host;
- one container runtime;
- one language runtime;
- one object store;
- one observability stack.

Such sharing does not merge their authoritative data sets or responsibility boundaries. Access remains mediated by identities, schemas, contracts, permissions, and ownership rules.

A profile can increase physical separation. It cannot silently change global logical ownership.

### 4.3 Authoritative data

The owning component controls:

- the canonical schema of its authoritative state;
- accepted mutations;
- invariants and state transitions;
- compatibility rules;
- export and disclosure behavior;
- recovery and migration behavior;
- evidence required for critical transitions.

Other components interact through published interfaces, authorized artifact exchange, or controlled gateways. Read replicas, caches, search indexes, analytical copies, and generated projections remain derived data unless an accepted decision explicitly transfers ownership.

### 4.4 Authority-bearing services

Infrastructure services remain inside their declared authority:

| Service or component | Authority retained | Authority excluded |
| --- | --- | --- |
| Resource Governor | Resource measurement, quotas, priorities, scheduling, and deterministic degradation | Disclosure policy, identity policy, business authorization, and component data ownership |
| Governance Policy Runtime | Authorization, disclosure, privilege, and policy evaluation | Resource scheduling, component implementation, and direct host mutation |
| Publication Gateway | Controlled cross-domain disclosure and publication | UCKK media ingestion and ownership of source-domain data |
| UCKK Dimension Gateway | User-authorized ingestion into a UCKK dimension | External publication and ownership of upstream source data |
| Audit Broker | Receipt intake, integrity-preserving evidence handling, and authorized audit views | Mutation of source component state |
| Identity and Trust | Identity, credential, trust, and signature verification | Ownership of application business state |
| Kristal Runtime | Epistemic artifact identity and runtime consumption | Universal workflow, universal operational storage, and component business authority |
| SenTient | Optional isolated analysis over authorized exports | Native system authority and direct mutation of authoritative component stores |

### 4.5 Dependency direction

A dependency declaration identifies which component requires a capability from another component. It does not transfer responsibility for either component.

Circular runtime dependencies are rejected unless an accepted decision and active contracts define:

- the cycle;
- startup and recovery order;
- failure containment;
- replay behavior;
- deadlock prevention;
- evidence and conformance tests.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-CONST-COMP-001,REQ-CONST-COMP-002,REQ-CONST-COMP-003,REQ-CONST-COMP-004,REQ-CONST-COMP-005,REQ-CONST-COMP-006,REQ-CONST-COMP-007,REQ-CONST-COMP-008,REQ-CONST-COMP-009,REQ-CONST-COMP-010,REQ-CONST-COMP-011,REQ-CONST-COMP-012,REQ-CONST-COMP-013,REQ-CONST-COMP-014,REQ-CONST-COMP-015,REQ-CONST-COMP-016 -->
- **REQ-CONST-COMP-001 — SHALL:** Every active component has one stable identity, one declared responsibility boundary, and one accountable owner.
- **REQ-CONST-COMP-002 — SHALL:** Every authoritative data set, state machine, and externally observable component capability has exactly one canonical owning component or canonical owning registry.
- **REQ-CONST-COMP-003 — SHALL NOT:** A component writes directly to another component's authoritative storage, internal tables, private queues, or private state.
- **REQ-CONST-COMP-004 — SHALL:** Every cross-component interaction uses an explicit active contract that identifies the producer, consumer, direction, authority boundary, permitted operations, failure ownership, and validation evidence.
- **REQ-CONST-COMP-005 — SHALL NOT:** A consuming component broadens, delegates, or reinterprets authority received through an interface beyond the authority granted by the owning component and applicable policy.
- **REQ-CONST-COMP-006 — SHALL:** A component validates the identity, contract version, scope, and authorization of every authority-bearing cross-component request before changing authoritative state.
- **REQ-CONST-COMP-007 — SHALL:** The Resource Governor and the Governance Policy Runtime remain separate authorities: the former controls deterministic resource allocation and scheduling, while the latter evaluates authorization, disclosure, and privilege policy.
- **REQ-CONST-COMP-008 — SHALL:** The Publication Gateway and the UCKK Dimension Gateway remain separate contracts: the former controls cross-domain publication, while the latter ingests user-selected media into the user's UCKK dimension.
- **REQ-CONST-COMP-009 — SHALL NOT:** Kristal becomes a universal operational database, workflow engine, or substitute for component-owned authoritative state.
- **REQ-CONST-COMP-010 — SHALL:** SenTient remains an optional isolated workbench that consumes authorized exports and does not become native system authority or a direct writer to component-owned authoritative state.
- **REQ-CONST-COMP-011 — SHALL NOT:** Failure, unavailability, or removal of an optional component transfers its authority to another component by implication.
- **REQ-CONST-COMP-012 — SHALL:** Profile-specific component membership, deployment topology, and physical isolation remain conditional on active profile contracts and do not alter global logical ownership.
- **REQ-CONST-COMP-013 — SHALL NOT:** Shared infrastructure, shared storage technology, shared transport, shared runtime, or co-location creates shared ownership of component state.
- **REQ-CONST-COMP-014 — SHALL:** A component change that alters responsibility, owned data, interface authority, or dependency direction updates the component registry, affected contracts, requirements, locks, traceability links, tests, and evidence before activation.
- **REQ-CONST-COMP-015 — SHALL:** Every critical cross-component transition produces machine-readable evidence sufficient to identify the initiating authority, contract, subject, outcome, and owning component.
- **REQ-CONST-COMP-016 — SHALL:** When a dependency fails or becomes unauthorized, degradation remains bounded to the affected capability and preserves the authority of unaffected components.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Establishing or changing a component boundary

A boundary-affecting change follows this order:

1. identify the responsibility, data, interface, or dependency being changed;
2. resolve the owning component and scope;
3. record an accepted decision when ownership or authority changes;
4. update `components.registry.json`;
5. update the affected component contracts;
6. update integration records when an external or cross-domain boundary changes;
7. update requirements and alignment locks;
8. update traceability links, tests, and expected evidence;
9. update explanatory documents and generated AI contexts;
10. run validation and activate the complete change atomically.

A partial update does not activate.

### 6.2 Processing an authority-bearing request

The receiving component:

1. authenticates the caller or verifies the artifact origin;
2. resolves the active contract and version;
3. verifies the requested operation and subject scope;
4. obtains applicable policy authorization;
5. validates input schema and replay constraints;
6. applies the mutation only through the owning component's state transition;
7. records the required receipt or evidence;
8. returns an outcome that does not expose private internal state.

### 6.3 Derived data lifecycle

A component that creates a cache, index, projection, or analytical copy:

1. records the authoritative source and contract;
2. limits the copy to authorized fields and purposes;
3. marks the copy as derived;
4. prevents the derived copy from becoming a mutation path;
5. detects source invalidation or version incompatibility;
6. rebuilds or removes the derived copy when it is no longer valid.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Authority retained | Authority denied | Evidence |
| --- | --- | --- | --- | --- |
| Component contract is absent, inactive, or incompatible | Block the interaction before state mutation | Each component retains its existing local authority | Cross-component operation | Contract-resolution failure |
| Caller identity or authorization cannot be verified | Reject the authority-bearing request | Read access already authorized independently, when applicable | Requested mutation or disclosure | Authentication or policy decision record |
| Dependency is unavailable | Degrade only the dependent capability | Unaffected local component functions | Capability requiring the dependency | Health state and dependency failure event |
| Derived cache or index is stale | Ignore, invalidate, or rebuild the derived copy | Authoritative source component | Mutation through the derived copy | Invalidation or rebuild evidence |
| Cross-component request is duplicated | Apply declared idempotency or replay rejection | Owning component state machine | Duplicate transition | Idempotency or replay receipt |
| Resource limit is reached | Resource Governor applies the active resource policy | Component authority over valid local state | Work exceeding the resource grant | Resource-governor decision |
| Governance policy service is unavailable for a policy-gated action | Fail closed for the gated action | Operations not requiring that policy decision | Policy-gated mutation, disclosure, or privilege | Policy-resolution failure |
| Optional SenTient workbench is unavailable | Keep the analysis capability unavailable without replacing it implicitly | Source components and ordinary system operation | SenTient analysis | Workbench health state |
| Publication Gateway is unavailable | Keep external publication unavailable | Source-domain data and internal operations | Cross-domain publication | Gateway health and failed publication record |
| UCKK Dimension Gateway is unavailable | Keep UCKK ingestion unavailable | Source media and existing UCKK state | New ingestion through the gateway | Gateway health and failed-ingestion record |

## 8. Cross-Component Interactions

Every interaction record identifies:

- producer and consumer;
- active contract;
- request, event, or artifact direction;
- owning component for each authoritative state involved;
- authentication and trust mechanism;
- authorization point;
- idempotency or replay behavior;
- timeout and retry ownership;
- failure owner;
- audit or receipt behavior;
- prohibited direct-access path.

The following interaction classes are distinguished:

| Interaction class | Permitted effect | Boundary rule |
| --- | --- | --- |
| Query | Returns an authorized view | Consumer does not acquire ownership of source state |
| Command | Requests an owning component transition | Owning component validates and executes the transition |
| Event | Reports an occurred fact | Consumer treats it according to the event contract and replay rules |
| Artifact transfer | Moves an immutable or versioned artifact | Activation remains controlled by the receiving artifact contract |
| Gateway transfer | Crosses a declared trust or disclosure boundary | Gateway policy and receipt requirements apply |
| Policy decision | Returns an authorization result | Decision does not execute the requested mutation |
| Resource decision | Returns or applies a resource grant | Grant does not authorize business action or disclosure |
| Evidence submission | Sends a receipt or proof to an audit boundary | Audit system does not mutate source state |

Direct database writes, private queue injection, private file mutation, and undocumented internal API calls across component boundaries are prohibited interaction paths.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect on this document |
| --- | --- |
| `DEC-CONST-COMP-001` | Establishes component separation as a global constitutional property. |
| `DEC-SYS-DATA-001` | Establishes logical data ownership independently of profile-dependent physical isolation. |
| `DEC-SYS-GOV-001` | Separates Resource Governor authority from Governance Policy Runtime authority. |
| `DEC-SYS-GATE-001` | Separates Publication Gateway from UCKK Dimension Gateway. |
| `DEC-SYS-SENT-001` | Classifies SenTient as an optional isolated workbench without native authority. |
| `DEC-SYS-KRISTAL-001` | Preserves Kristal as a transversal epistemic foundation without universal operational ownership. |

### Prohibited assumptions

- co-location implies shared authority;
- use of one database technology permits cross-component table writes;
- an event consumer owns the event producer's source state;
- a cache, index, replica, or analytical copy becomes authoritative through operational convenience;
- a policy decision executes a privileged or business mutation;
- a resource decision authorizes disclosure or business behavior;
- an optional component's failure transfers its responsibility to another component;
- a profile deployment choice becomes a global component boundary;
- a gateway can absorb another gateway's responsibility because both transfer data;
- internal implementation details are stable public interfaces;
- a component can redefine another component's responsibility in its own documentation;
- a shared library is automatically an independent component.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. `DOC-CONST-007` is active and registered at `01-constitution/07-component-separation.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical text, strength, scope, owner, decision source, and validation mapping.
5. `LOCK-COMP-001`, `LOCK-COMP-002`, `LOCK-DATA-001`, `LOCK-GOV-001`, `LOCK-GATE-001`, and `LOCK-SENT-001` are active.
6. Every active component has one unique identity and one declared responsibility owner.
7. Every authoritative data declaration resolves to one owning component or registry.
8. No active component contract authorizes direct writes to another component's private authoritative storage.
9. Resource Governor and Governance Policy Runtime responsibilities do not overlap.
10. Publication Gateway and UCKK Dimension Gateway responsibilities do not overlap.
11. SenTient is optional, isolated, and absent from native authority paths.
12. Kristal is not designated as a universal operational database or workflow engine.
13. Every cross-component mutation path references an active observable contract.
14. Every critical cross-component transition maps to at least one test and one evidence requirement.
15. Profile-specific physical-isolation rules do not alter global logical ownership.
16. Active prose is English and contains no unresolved-authority marker.
17. No normative keyword appears outside the generated requirement block.
18. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

Konnaxion and Orgo can use schemas on one PostgreSQL server in a lightweight profile. Separate database roles, schemas, migration ownership, and service interfaces preserve logical ownership. Orgo does not update Konnaxion tables directly.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

The Governance Policy Runtime can return an authorization decision to a narrow privileged broker. The policy runtime does not perform the host mutation, and the broker does not invent policy.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

The UCKK Dimension Gateway can accept user-selected media and create an ingestion request for UCKK. Publishing that media outside the user's domain requires a separate Publication Gateway interaction.

> **Non-normative example:** This example illustrates one valid implementation or scenario. It does not redefine the canonical contract.

SenTient can analyze an authorized export in an isolated workspace. Its index and annotations remain derived workbench data until an explicit owning-component import contract accepts a result.
