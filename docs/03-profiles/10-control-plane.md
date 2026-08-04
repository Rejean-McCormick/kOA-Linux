<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROFILE-010",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "deployment_profiles",
  "scope": [
    "control_plane"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/control-plane.profile.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "contracts/release-channels.contract.json",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/artifact-contracts/node-profile.schema.json",
    "contracts/artifact-contracts/release-set.schema.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-PROFILE-002",
    "DEC-K8S-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-PROFILE-CP-001",
    "REQ-PROFILE-CP-002",
    "REQ-PROFILE-CP-003",
    "REQ-PROFILE-CP-004",
    "REQ-PROFILE-CP-005",
    "REQ-PROFILE-CP-006",
    "REQ-PROFILE-CP-007",
    "REQ-PROFILE-CP-008",
    "REQ-PROFILE-CP-009",
    "REQ-PROFILE-CP-010",
    "REQ-PROFILE-CP-011",
    "REQ-PROFILE-CP-012",
    "REQ-PROFILE-CP-013",
    "REQ-PROFILE-CP-014",
    "REQ-PROFILE-CP-015",
    "REQ-PROFILE-CP-016",
    "REQ-PROFILE-CP-017",
    "REQ-PROFILE-CP-018",
    "REQ-PROFILE-CP-019",
    "REQ-PROFILE-CP-020",
    "REQ-PROFILE-CP-021",
    "REQ-PROFILE-CP-022"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-AI-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-003",
    "LOCK-IMPL-001"
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
    "DOC-SYS-000",
    "DOC-SYS-001",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-002",
    "DOC-PROFILE-003"
  ],
  "tags": [
    "profiles",
    "control-plane",
    "coordination",
    "orchestration",
    "release-coordination",
    "kubernetes-optional",
    "authority-separation",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Control Plane Profile

## 1. Purpose

This document explains the active `control_plane` deployment profile.

The profile provides a governed coordination environment for declared deployment, lifecycle, scheduling, health, and evidence workflows. It operates through explicit contracts and preserves the independent authority of the components, profiles, release channels, policy services, resource services, and data owners that it coordinates.

The profile supports both Kubernetes and non-Kubernetes realizations. The orchestration mechanism is a profile implementation choice, not a global kOA requirement.

## 2. Scope

This document applies only to deployments whose selected primary profile is:

```text
control_plane
```

It covers:

- profile purpose and authority boundaries;
- coordination and orchestration behavior;
- effective component membership;
- orchestration-mechanism selection;
- release and activation coordination;
- resource and policy authority separation;
- bounded reconciliation and scheduling;
- health, readiness, evidence, and recovery behavior;
- overlay composition;
- profile conformance.

This document does not:

- make the control plane mandatory for endpoints;
- define a universal cluster topology;
- require Kubernetes;
- define Kubernetes objects or command syntax;
- make a non-Kubernetes implementation nonconformant;
- transfer component data ownership to the control plane;
- make health observations or generated views authoritative;
- authorize direct writes to managed component storage;
- add native AI to the system baseline.

Detailed profile values, component membership, supported overlays, resource envelopes, orchestration selection, and conformance evidence remain owned by `contracts/profiles/control-plane.profile.json`.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `generated/profile-catalog.json#/profiles` | Owns the `control_plane` identity, primary-profile classification, contract path, version, and lifecycle status. |
| `contracts/profiles/control-plane.profile.json` | Owns detailed capabilities, component membership, orchestration selection, resources, compatibility, overlays, failure behavior, and conformance. |
| `contracts/system.contract.json` | Owns global system behavior and boundaries that the profile cannot weaken. |
| `generated/component-catalog.json` | Owns component identities and logical responsibility boundaries. |
| `contracts/release-channels.contract.json` | Owns the four release-channel identities and channel membership. |
| `contracts/components/resource-governor.component.json` | Owns observable resource-admission and scheduling behavior. |
| `contracts/components/governance-policy-runtime.component.json` | Owns observable authorization and governed-policy behavior. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns profile, component, data, governance, AI, lifecycle, and implementation alignment locks. |
| `generated/traceability.json` | Owns decision, requirement, lock, test, and evidence relationships. |
| `generated/exception-index.json` | Owns approved scoped deviations and compensating controls. |
| `contracts/artifact-contracts/node-profile.schema.json` | Defines the effective-profile declaration used for activation and conformance. |
| `contracts/artifact-contracts/release-set.schema.json` | Defines compatible coordinated release identities. |

## 4. Model and Responsibilities

### 4.1 Profile role

The control plane coordinates declared system operations without absorbing the authority of the managed system.

Its coordination model includes:

- resolving active profile and component contracts;
- accepting authenticated requests for declared operations;
- obtaining required policy and resource decisions;
- coordinating eligible work through owning components;
- observing progress and health through published interfaces;
- recording receipts and evidence;
- maintaining bounded reconciliation of declared and observed coordination state.

The individual component remains responsible for validating and applying its own authoritative state transitions.

### 4.2 Authority retained outside the control plane

| Authority | Canonical owner |
| --- | --- |
| Component identity and responsibility | Components registry and component contract |
| Component business state | Owning component |
| Data schema and accepted mutation | Owning component |
| Resource admission and scheduling | Resource Governor |
| Authorization, disclosure, consent, and privilege | Governance Policy Runtime when applicable |
| Release-channel identity | Release channels registry |
| Artifact verification and activation | Applicable lifecycle and artifact contracts |
| Profile behavior | Control-plane profile contract |
| Exceptions | Exceptions registry |
| Conformance tests and evidence | Test and evidence registries |

The control plane can coordinate these authorities but cannot silently replace them.

### 4.3 Orchestration implementations

The profile permits two implementation classes:

| Implementation class | Profile treatment |
| --- | --- |
| Kubernetes-based | Permitted when selected by the active control-plane contract and validated against all applicable kOA boundaries |
| Non-Kubernetes | Permitted when the implementation provides equivalent contract fulfillment, bounded operation, authority separation, evidence, and recovery |

Implementation recipes are stored separately:

```text
11-recipes/control-plane/kubernetes-deployment.md
11-recipes/control-plane/non-kubernetes-deployment.md
```

Those recipes illustrate deployment methods. They do not independently define the profile contract.

### 4.4 Declared and observed state

The control plane distinguishes:

- declared coordination intent;
- accepted authorization state;
- resource admission state;
- component-reported execution state;
- observed health and readiness;
- release and artifact identity;
- evidence and receipt state.

Observed state does not become authoritative business state. A health signal reports condition; it does not authorize mutation. A reconciliation result reports coordination progress; it does not override the owning component's transition result.

### 4.5 Release coordination

Control-plane release coordination uses the four canonical channels:

```text
system
services
governance
knowledge
```

A Release Set identifies tested compatible versions across those channels.

The control plane can coordinate staged verification, distribution, activation requests, observation, and recovery. The applicable artifact or component contract still owns verification, activation, rollback, and forward repair for its authority boundary.

### 4.6 Overlay composition

The `control_plane` profile participates in overlay composition only when each selected overlay contract explicitly lists it as compatible.

Composition follows:

```text
global constitutional and system baseline
+ control_plane primary profile
+ compatible overlays
+ active scoped exceptions
= effective control-plane configuration
```

The profile contract owns compatible overlays and merge behavior. No overlay compatibility is inferred from names or implementation similarity.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROFILE-CP-001,REQ-PROFILE-CP-002,REQ-PROFILE-CP-003,REQ-PROFILE-CP-004,REQ-PROFILE-CP-005,REQ-PROFILE-CP-006,REQ-PROFILE-CP-007,REQ-PROFILE-CP-008,REQ-PROFILE-CP-009,REQ-PROFILE-CP-010,REQ-PROFILE-CP-011,REQ-PROFILE-CP-012,REQ-PROFILE-CP-013,REQ-PROFILE-CP-014,REQ-PROFILE-CP-015,REQ-PROFILE-CP-016,REQ-PROFILE-CP-017,REQ-PROFILE-CP-018,REQ-PROFILE-CP-019,REQ-PROFILE-CP-020,REQ-PROFILE-CP-021,REQ-PROFILE-CP-022 -->
- **REQ-PROFILE-CP-001 — SHALL:** The control_plane profile is an active primary deployment profile with its complete behavior owned by contracts/profiles/control-plane.profile.json.
- **REQ-PROFILE-CP-002 — SHALL:** The control_plane profile coordinates declared deployment, lifecycle, scheduling, health, and evidence workflows only through active component, integration, profile, and artifact contracts.
- **REQ-PROFILE-CP-003 — SHALL NOT:** The control_plane profile becomes a required dependency of user, developer, or sovereign endpoint baselines.
- **REQ-PROFILE-CP-004 — SHALL:** Kubernetes is permitted in the control_plane profile when the active profile contract selects it.
- **REQ-PROFILE-CP-005 — SHALL NOT:** Kubernetes is treated as the only conformant control-plane implementation.
- **REQ-PROFILE-CP-006 — SHALL:** A non-Kubernetes deployment remains conformant when it satisfies the same active profile, component, security, lifecycle, resource, and evidence contracts.
- **REQ-PROFILE-CP-007 — SHALL:** The selected orchestration mechanism is declared in the effective profile and validated against the control-plane contract.
- **REQ-PROFILE-CP-008 — SHALL NOT:** The control plane writes directly to another component's authoritative storage, private queues, private files, or internal state.
- **REQ-PROFILE-CP-009 — SHALL:** Every control-plane request that can change deployment or lifecycle state identifies the initiating authority, target, active contract, requested operation, authorization result, and outcome.
- **REQ-PROFILE-CP-010 — SHALL:** The control plane preserves the canonical ownership and mutation authority of every managed component.
- **REQ-PROFILE-CP-011 — SHALL:** Resource admission, scheduling, concurrency, queues, and degradation remain under Resource Governor authority.
- **REQ-PROFILE-CP-012 — SHALL:** Authorization, disclosure, consent, privilege, and governed exceptions remain under Governance Policy Runtime authority when those controls apply.
- **REQ-PROFILE-CP-013 — SHALL NOT:** A resource decision substitutes for policy authorization, and a policy decision substitutes for resource admission.
- **REQ-PROFILE-CP-014 — SHALL:** Control-plane release coordination uses active release identities and compatibility constraints across the system, services, governance, and knowledge channels.
- **REQ-PROFILE-CP-015 — SHALL:** A coordinated activation preserves atomicity at each governed artifact boundary and retains the required rollback or forward-repair path.
- **REQ-PROFILE-CP-016 — SHALL:** Control-plane queues, retries, timeouts, reconciliation loops, worker counts, and concurrent operations have explicit finite bounds.
- **REQ-PROFILE-CP-017 — SHALL:** Loss of control-plane connectivity does not silently transfer authority to an unmanaged path or invalidate already active local authority.
- **REQ-PROFILE-CP-018 — SHALL:** When required authority, compatibility, identity, policy, resource, or evidence cannot be resolved, the affected control-plane operation is blocked.
- **REQ-PROFILE-CP-019 — SHALL:** Critical control-plane transitions produce machine-readable receipts and evidence sufficient to reconstruct the requested action, decision chain, target, result, and recovery state.
- **REQ-PROFILE-CP-020 — SHALL NOT:** The control_plane profile introduces native AI, autonomous agents, or AI-based authority into coordination, scheduling, reconciliation, or deployment decisions.
- **REQ-PROFILE-CP-021 — SHALL:** Selected overlays modify the control_plane profile only through explicit compatibility and deterministic composition rules.
- **REQ-PROFILE-CP-022 — SHALL:** Every control-plane conformance claim is traceable to the active profile contract, accepted decisions, requirements, locks, tests, evidence, and effective-profile declaration.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Activating the profile

Activation follows this sequence:

1. resolve the active authority release;
2. resolve the active `control_plane` profile contract;
3. resolve selected overlays and scoped exceptions;
4. generate and validate the effective-profile declaration;
5. resolve component, integration, release, policy, resource, and evidence dependencies;
6. select the declared orchestration implementation;
7. validate implementation conformance;
8. establish bounded queues and reconciliation controls;
9. verify recovery and evidence paths;
10. activate the complete profile atomically.

The previous valid profile state remains the recovery target until activation succeeds.

### 6.2 Processing a coordinated operation

A coordinated operation proceeds through:

1. request identity and target resolution;
2. active contract and profile resolution;
3. authentication and applicable policy evaluation;
4. resource admission;
5. target-component acceptance;
6. bounded execution and observation;
7. owning-component completion, failure, rollback, or repair;
8. receipt and evidence recording;
9. final coordination outcome.

A control-plane acceptance is not equivalent to target-component completion.

### 6.3 Reconciliation

A reconciliation loop:

1. reads declared coordination intent;
2. reads published observed state;
3. resolves active contracts and versions;
4. calculates a permitted next action;
5. verifies policy and resource prerequisites;
6. invokes the owning component through its active contract;
7. records the result;
8. stops, retries within bounds, or escalates according to the contract.

Reconciliation never bypasses the owning component's mutation path.

### 6.4 Changing orchestration implementation

Changing between Kubernetes and non-Kubernetes implementation:

1. keeps the `control_plane` profile identity unchanged;
2. records the implementation selection in the effective profile;
3. verifies equivalent contract coverage;
4. migrates control-plane-owned coordination state through an active migration contract;
5. preserves component and data ownership;
6. validates failure recovery, evidence, and rollback;
7. activates the new implementation atomically.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved authority | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Control plane unavailable | Managed components retain their valid local authority and declared offline behavior | Existing component authority | New centrally coordinated operations | Control-plane health record |
| Orchestration scheduler unavailable | Stop unsafe admission and retain bounded queued state | Active component state | New scheduled work | Scheduler failure evidence |
| Policy result unavailable | Keep governed operation blocked | Non-gated local operations | Policy-gated operation | Policy-resolution failure |
| Resource decision unavailable | Keep new work blocked when safe admission cannot be established | Existing bounded work | New unresolved work | Resource-resolution failure |
| Target component unavailable | Retain declared intent and bounded retry or failure state | Other components | Target operation | Component availability record |
| Contract or version incompatible | Reject before invocation | Current active state | Incompatible operation | Compatibility failure |
| Release Set incompatible | Reject coordinated activation | Last valid release state | New release activation | Release compatibility report |
| Evidence path unavailable | Follow the transition contract's synchronous-fail or bounded-queue rule | Source authority | Transition requiring unavailable mandatory evidence | Evidence-path status |
| Reconciliation limit reached | Stop automatic retries and surface intervention state | Last valid component state | Further automatic mutation | Retry-exhaustion record |
| Network partition | Preserve local authority; prevent ambiguous split authority | Valid local component state | Operations requiring unavailable remote authority | Partition state |
| New profile activation fails | Retain the last valid effective profile | Previous control-plane state | New profile composition | Activation report |
| Control-plane state corrupted | Restore verified control-plane-owned coordination state without rewriting managed component state | Managed component authority | Unverified coordination | Restore evidence |

## 8. Cross-Component Interactions

### 8.1 Managed components

The control plane interacts with managed components through active observable contracts.

Each interaction identifies:

- source and target identity;
- operation;
- authority boundary;
- profile and contract version;
- authentication and policy result;
- resource decision;
- idempotency or replay behavior;
- timeout and retry ownership;
- component result;
- required receipt and evidence.

### 8.2 Resource Governor

The Resource Governor evaluates resource budgets, queue capacity, concurrency, priority, and scheduling.

The control plane can submit eligible work and observe resource state. It cannot invent a resource grant or reinterpret a denial as authorization.

### 8.3 Governance Policy Runtime

The Governance Policy Runtime evaluates authorization, disclosure, consent, privilege, and governed exceptions where the effective profile requires those controls.

The control plane can request and consume a policy result. It cannot execute a prohibited operation because resources are available.

### 8.4 Identity, trust, audit, and lifecycle services

Identity and Trust verifies identities, credentials, signatures, and trust state.

Audit and evidence services preserve receipts and authorized evidence views without mutating the source transition.

Lifecycle services and owning components verify and activate artifacts according to their contracts.

The control plane coordinates these interactions while preserving each service's authority boundary.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-PROFILE-001` | Establishes `control_plane` as one of the seven primary deployment profiles. |
| `DEC-PROFILE-002` | Establishes explicit deterministic profile and overlay composition. |
| `DEC-K8S-001` | Permits Kubernetes for the control plane without requiring it on endpoint baselines. |
| `DEC-DATA-001` | Preserves logical data ownership across deployment profiles. |
| `DEC-GOV-001` | Separates Resource Governor from Governance Policy Runtime authority. |
| `DEC-AI-001` | Prohibits native AI authority in the global baseline. |
| `DEC-REL-001` | Establishes four release channels and compatible Release Sets. |

### Prohibited assumptions

- every kOA deployment requires a control plane;
- every control plane requires Kubernetes;
- Kubernetes use changes canonical component ownership;
- a non-Kubernetes implementation is nonconformant by definition;
- control-plane observation is authoritative application state;
- reconciliation permits direct database writes;
- scheduling priority grants authorization;
- policy approval guarantees resource admission;
- one successful deployment recipe defines the canonical profile;
- a network partition transfers authority silently;
- a retry loop can remain unbounded;
- a control-plane receipt replaces the target component's result;
- coordination of a release makes the control plane the artifact owner;
- a selected overlay is compatible without an explicit declaration;
- external AI can be introduced as a coordination shortcut;
- missing profile details can be inferred from generic platform conventions.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-PROFILE-010` is active at `03-profiles/10-control-plane.md`.
2. `control_plane` is active and classified as a primary profile in the profile index.
3. The control-plane profile contract validates against the deployment-profile schema.
4. Every canonical reference resolves.
5. Every listed decision exists with status `accepted`.
6. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
7. Every listed lock exists and is active.
8. Endpoint profiles do not depend on the control plane unless their own active contracts declare an optional integration.
9. Kubernetes is permitted but not represented as the sole conformant implementation.
10. The selected orchestration implementation is recorded in the effective profile.
11. Both implementation classes preserve component and data authority boundaries.
12. No control-plane contract permits direct writes to another component's authoritative state.
13. Resource Governor and Governance Policy Runtime responsibilities remain distinct.
14. Queues, retries, reconciliation loops, timeouts, workers, and concurrent operations are bounded.
15. Release coordination uses active channel identities and compatibility constraints.
16. Activation, rollback, and forward-repair behavior resolves for every coordinated artifact class.
17. Network-partition and control-plane-loss tests preserve valid local authority.
18. Every critical coordination transition maps to tests and evidence.
19. Selected overlays are explicitly compatible and deterministically composed.
20. No native AI or autonomous authority is introduced.
21. Active prose is English and contains no unresolved-authority marker.
22. No normative keyword appears outside the generated requirement block.
23. The documentation dependency graph remains acyclic.

The validation entry point is:

```bash
python docs/tools/validate_docs.py
```

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates one conformant implementation class. It does not make Kubernetes mandatory.

A control-plane deployment can use Kubernetes for scheduling and service placement while kOA component contracts continue to own state transitions, resource policy remains under the Resource Governor, and authorization remains under the Governance Policy Runtime.

> **Non-normative example:** This example illustrates another conformant implementation class.

A control-plane deployment can use independently managed services and a bounded local scheduler without Kubernetes. It remains conformant when the same profile, authority, lifecycle, evidence, and recovery contracts are satisfied.

> **Non-normative example:** This example illustrates loss of central coordination.

During a network partition, an endpoint can retain already valid local authority and declared offline behavior. The control plane does not silently become authoritative for unavailable local state, and the endpoint does not invent remote authorization.

> **Non-normative example:** This example illustrates release coordination.

The control plane can coordinate a Release Set across system, services, governance, and knowledge channels. Each artifact owner still verifies and activates its own artifact boundary, and a failed channel remains subject to its declared rollback or forward-repair behavior.
