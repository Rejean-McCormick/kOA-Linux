<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-019",
  "document_class": "adr",
  "version": "1.0.0",
  "status": "active",
  "language": "en",
  "layer": "architecture_decision",
  "owner": "governance-architecture",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/decisions/DEC-GOV-001",
    "contracts/system.contract.json#/resource_governance",
    "contracts/system.contract.json#/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "contracts/components/resource-governor.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-GOV-001"
  ],
  "requirement_ids": [
    "REQ-COMP-RG-001",
    "REQ-COMP-RG-002",
    "REQ-COMP-RG-003",
    "REQ-COMP-RG-004",
    "REQ-COMP-RG-005",
    "REQ-COMP-RG-012",
    "REQ-COMP-RG-013",
    "REQ-COMP-RG-014",
    "REQ-COMP-RG-015",
    "REQ-COMP-RG-016",
    "REQ-COMP-RG-017",
    "REQ-COMP-RG-018",
    "REQ-COMP-RG-019",
    "REQ-COMP-RG-021",
    "REQ-COMP-RG-022",
    "REQ-COMP-RG-023",
    "REQ-COMP-RG-024"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "adr_ids": [
    "ADR-019"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-020",
    "DOC-COMP-RG-001",
    "DOC-PROFILE-001",
    "DOC-SEC-002",
    "DOC-SEC-013",
    "DOC-SEC-020",
    "DOC-LIFE-000",
    "DOC-CONF-000"
  ],
  "tags": [
    "adr",
    "resource-governor",
    "governance-policy-runtime",
    "authority-separation",
    "resource-admission",
    "authorization",
    "policy",
    "scheduling",
    "limits",
    "receipts",
    "fail-closed",
    "profiles"
  ],
  "effective_at": "2026-08-03T19:39:00-04:00"
}
KOA:DOC-META:END -->

# ADR-019: Resource Governor and Policy Runtime Separation

## Status

**Accepted**

- **ADR ID:** `ADR-019`
- **Owner decision:** `DEC-GOV-001`
- **Effective date:** 2026-08-03
- **Decision owner:** Governance Architecture
- **Change class:** Major when authority ownership, decision composition, profile applicability, or receipt semantics change

## Context

kOA needs to answer two different questions before many workloads execute:

```text
Is the requested action authorized?

Can the resulting workload run now,
under which resource limits,
priority, queue, and pressure behavior?
```

These questions use different inputs, produce different outcomes, fail for different reasons, and belong to different authorities.

Authorization can depend on:

- subject identity;
- tenant;
- target resource;
- component-owned business rules;
- disclosure and consent;
- privilege;
- cultural-rights policy;
- governed exceptions;
- environment and profile;
- validity and revocation.

Resource admission can depend on:

- CPU;
- memory;
- I/O;
- process count;
- concurrency;
- queue capacity;
- scheduling class;
- execution time;
- retry limits;
- temporary storage;
- workload class;
- current pressure;
- reserved recovery capacity.

Merging these concerns would create ambiguous authority. A scheduler could accidentally grant business permission because capacity exists. A governance engine could accidentally promise execution because an action is permitted. A component could report false success because one decision passed while the other failed.

The architecture therefore requires two independent authorities with explicit composition at the execution boundary.

## Decision

Resource Governor and Governance Policy Runtime remain separate authorities.

Resource Governor manages:

- resource admission;
- CPU and memory limits;
- I/O bounds;
- process limits;
- concurrency;
- queues;
- job scheduling;
- execution time;
- retry and worker bounds;
- reservations;
- pressure response;
- throttling, pausing, rejection, and release.

Governance Policy Runtime manages:

- governed authorization;
- disclosure;
- consent;
- privilege decisions;
- cultural-rights policy where applicable;
- governed exceptions;
- policy obligations;
- policy validity and revocation.

The owning component remains responsible for:

- workload purpose;
- business operation;
- data ownership;
- input and output;
- component invariants;
- authoritative state transition;
- business result.

Identity and Trust remains responsible for subject, service, node, signer, credential, and trust evidence.

Lifecycle services remain responsible for artifact verification, activation, rollback, forward repair, and recovery.

Resource Governor belongs to the global baseline.

Governance Policy Runtime is required only by profiles that claim sovereign governance or high assurance.

## Decision Rule

When both decisions apply, protected execution requires:

```text
valid component or governance authority
AND
valid Resource Governor admission
AND
current target and input state
```

The two decisions remain independently identifiable.

A positive governance decision does not reserve resources.

A positive resource-admission decision does not create missing authorization.

A denial, rejection, expiry, revocation, or indeterminate result from either applicable authority prevents execution or continuation according to the owning contract.

The decisions can be evaluated sequentially or in parallel when the active contract permits it. Execution begins only after all required results are positive, current, scope-matched, and correlated.

## Authority Matrix

| Concern | Canonical owner | Example result |
| --- | --- | --- |
| Subject and service identity | Identity and Trust | established, not established, indeterminate |
| Business operation | Owning component | authorized, denied, indeterminate |
| Governed disclosure or privilege | Governance Policy Runtime | authorized, denied, indeterminate |
| Resource admission | Resource Governor | admitted, queued, rejected, expired |
| Resource pressure | Resource Governor | continue, throttle, pause, cancel |
| Authoritative data commit | Owning component | committed, not committed, rolled back |
| Artifact activation | Lifecycle owner | active, failed, rolled back, repaired |
| Receipt storage and disclosure | Audit Broker | stored, verified, selectively disclosed |

No row inherits authority from another row automatically.

## Resource Governor Boundary

Resource Governor receives a workload declaration containing:

```text
workload_id
component_id
tenant and execution scope
active profile and overlays
operating mode
workload class
resource class
requested limits
priority
timeout
retry limit
cancellation behavior
authority_context_ref where required
correlation_id
```

It produces a resource decision containing:

```text
resource_decision_id
result
effective limits
reservation or queue identity
scheduling class
queue position where applicable
pressure behavior
valid_from
expires_at
reason_code
correlation_id
receipt_ref where required
```

Resource Governor does not:

- decide whether a user can read or change business data;
- evaluate consent or cultural-rights permission;
- approve publication or disclosure;
- grant machine privilege;
- become the owner of a workload result;
- write to another component's authoritative source tables;
- reinterpret an external AI result as authority;
- activate an artifact merely because capacity exists.

It can reject an otherwise authorized workload when capacity is unavailable or the requested envelope is invalid.

## Governance Policy Runtime Boundary

Governance Policy Runtime receives a governed decision request containing:

```text
policy_request_id
subject and service identity references
tenant and environment
owning component
action
target resource
data and disclosure classes
purpose
consent and rights context
privilege context
active policy bundle
profile and overlays
correlation_id
```

It produces a policy decision containing:

```text
policy_decision_id
authorized, denied, or indeterminate result
reason_code
obligations
scope
valid_from
expires_at
revocation context
correlation_id
decision_receipt_ref
```

Governance Policy Runtime does not:

- allocate CPU or memory;
- schedule workers;
- reserve queue capacity;
- choose pressure behavior;
- own component business data;
- commit another component's state;
- guarantee that an authorized workload will run;
- replace the owning component's business invariants;
- infer availability from policy authorization.

It can authorize an action that Resource Governor later queues or rejects.

## Owning-Component Boundary

The owning component composes required decisions before its protected transition.

It validates:

1. the actor and service identity;
2. the policy or component authority decision;
3. the Resource Governor decision;
4. scope, tenant, target, operation, profile, and correlation;
5. expiry and revocation;
6. current target state;
7. component invariants;
8. commit conditions.

The component performs its own state transition through its declared interface.

Neither Resource Governor nor Governance Policy Runtime receives direct write authority over the component's authoritative source records.

For workloads that have no governed authorization requirement, the component's own authority decision can satisfy the action-authority side. Resource admission remains separate where the workload is resource-governed.

## Decision Composition

A composed execution context references, rather than merges, decision identities:

```text
execution_context_id
component_authority_ref
governance_policy_decision_ref where applicable
resource_decision_ref
identity_evidence_ref
profile_ref
target_ref
operation
validity intersection
correlation_id
```

Its validity ends at the earliest expiry, revocation, scope change, target-state invalidation, resource cancellation, or component cancellation.

Decision composition does not produce a new super-authority. It records that the owning component verified the required independent inputs.

## Ordering and Race Control

The active operation contract can select an evaluation order.

### Authority-first

Used when resource reservation would be wasteful or disclose information before authorization.

```text
authority decision
    → resource admission
    → component execution
```

### Admission-first with no protected execution

Used when a small temporary reservation is needed before an expensive policy or component evaluation.

```text
tentative bounded reservation
    → authority decision
    → final admission
    → component execution
```

A tentative reservation cannot perform the protected action.

### Parallel evaluation

Used when both decisions are independent and latency matters.

```text
authority evaluation
resource evaluation
    → scope and validity join
    → component execution
```

Before execution, the component revalidates both results. Long-running work follows the declared revalidation and cancellation policy.

## State Models

Resource workload states are:

```text
requested
admitted
queued
running
throttled
paused
succeeded
failed
cancelled
rejected
expired
```

Governance decision states are:

```text
requested
authorized
denied
indeterminate
expired
revoked
superseded
```

Component execution and commit states remain separate:

```text
not_started
running
succeeded
failed
cancelled

not_applicable
not_committed
committed
rolled_back
forward_repaired
```

A queued workload is not an authorized business result.

An authorized policy decision is not a running workload.

A succeeded process is not necessarily an authoritative commit.

## Resource Envelopes and Policy Bundles

Resource envelopes and policy bundles are different artifact classes.

A resource envelope declares:

- hard limits;
- soft targets;
- reservations;
- burst allowances;
- queue and concurrency bounds;
- pressure responses;
- profile applicability.

A policy bundle declares:

- governed action rules;
- disclosure and consent rules;
- privilege rules;
- cultural-rights rules;
- exceptions;
- obligations;
- validity and revocation behavior.

Their activation, rollback, forward repair, and receipts remain independently attributable.

A Release Set can bind compatible versions of both through their canonical release-channel selections without merging their authority.

## Profile Applicability

Resource Governor is part of the global baseline because finite resource control applies to user, development, service, maintenance, recovery, build, and sovereign workloads.

Exact resource capacities, enforcement mechanisms, hardware assumptions, and orchestration choices remain profile-specific.

Governance Policy Runtime is required for profiles that claim sovereign governance or high assurance.

Other profiles can use component-owned authorization without deploying the full Governance Policy Runtime unless their active profile contract requires it.

A profile-specific governance or resource choice does not become global through repetition.

## Offline and Degraded Operation

Resource Governor continues to enforce the last valid local resource envelopes during offline or restricted-connectivity operation.

Governance Policy Runtime, where required, evaluates the last valid signed local policy state within its freshness, identity, trust, revocation, and time bounds.

Loss of connectivity does not merge authorities or broaden either decision.

When Governance Policy Runtime is unavailable in a profile that requires it:

- governed actions fail closed;
- independently authorized non-governed local capabilities can continue;
- Resource Governor continues resource enforcement;
- status reports governance unavailability separately from capacity.

When Resource Governor cannot make a safe admission decision:

- new governed workloads are rejected or held according to the active contract;
- authorization decisions remain historically true but do not imply execution;
- existing workloads follow declared pressure and recovery behavior;
- critical recovery capacity remains protected where declared.

## Receipts and Evidence

The architecture records independent evidence for:

- policy request and decision;
- resource request and decision;
- queueing and scheduling;
- admission expiry or revocation;
- workload start and termination;
- component execution;
- target effect;
- authoritative commit;
- rollback or forward repair;
- envelope activation;
- policy-bundle activation;
- emergency reservation;
- forced termination.

Receipts share correlation context but retain their producer and authority.

Audit Broker can store, index, verify, and selectively disclose the receipts. It does not become the underlying policy, resource, or component authority.

Ordinary views exclude secret values, credentials, private keys, protected payloads, and unnecessary policy inputs.

## Consequences

### Positive consequences

- authorization and capacity remain understandable and independently testable;
- resource pressure cannot grant permission;
- policy approval cannot promise execution;
- component data ownership remains intact;
- profiles can deploy governance selectively;
- Resource Governor can remain lightweight and globally available;
- offline operation preserves local resource enforcement;
- receipts report exact decision and commit truth;
- policy and resource artifacts can evolve independently;
- failures remain capability-scoped;
- conformance can identify which authority failed or blocked.

### Costs and tradeoffs

- protected execution can require several correlated decisions;
- callers and components must propagate decision references and validity;
- race and expiry handling need explicit revalidation;
- two components, contracts, artifact classes, and health models must be operated;
- tests must cover partial success and disagreement;
- observability must distinguish policy, resource, execution, and commit states;
- policy-authorized workloads can still be delayed or rejected;
- capacity can be reserved briefly before final authority in selected flows;
- profile composition must declare whether Governance Policy Runtime is present.

### Risks and controls

| Risk | Required control |
| --- | --- |
| Resource admission is treated as authorization | Contract tests and `LOCK-GOV-001` |
| Policy authorization is treated as capacity guarantee | Separate result types and workload-state checks |
| One service writes another's data | Owning-component execution and `LOCK-DATA-001` |
| Decision expiry creates a race | Validity intersection and pre-execution revalidation |
| Tentative reservation performs protected work | No protected execution before authority and final admission |
| Correlation is mistaken for ownership | Preserve producer and authority on every receipt |
| Governance becomes mandatory everywhere | Profile applicability tests |
| Resource implementation choices become global | Profile-scoped envelopes and `LOCK-PROFILE-001` |
| Audit Broker becomes the source of truth | Preserve underlying owner receipts |
| External scheduler or AI gains authority | Registered integration boundary and owner validation |

## Alternatives Considered

### One combined governance and resource engine

Rejected because it would merge permission with capacity, make failure semantics ambiguous, complicate profile applicability, and risk authority expansion from scheduling state.

### Governance Policy Runtime owns resource scheduling

Rejected because policy authorization does not own current CPU, memory, I/O, queue, concurrency, or pressure state.

### Resource Governor owns authorization

Rejected because resource admission lacks subject, consent, disclosure, privilege, cultural-rights, and business-rule authority.

### Every component implements all resource governance locally

Rejected because global fairness, reservations, pressure response, protected interactive capacity, recovery capacity, and cross-workload attribution require a system resource authority.

Components still declare workload intent and handle component-specific cancellation and results.

### Orchestrator or container runtime is the authority

Rejected because a runtime can enforce limits but does not own kOA governance semantics, tenant authorization, component business rules, or release identity.

### External AI or external scheduling service decides both

Rejected because the native baseline has no external authority dependency, external AI output remains candidate input, and offline operation must retain local deterministic control.

### Treat authorization as a scheduling priority

Rejected because priority affects resource order, not whether an action is permitted.

## Migration Guidance

Implementations that combine policy and resource decisions migrate in this order:

1. inventory existing decision inputs, outputs, state, storage, APIs, and receipts;
2. classify each rule as identity, component authority, governance policy, resource admission, execution, or commit;
3. assign governance rules to Governance Policy Runtime or the owning component;
4. assign limits, queues, scheduling, concurrency, and pressure behavior to Resource Governor;
5. create separate decision identities and schemas;
6. update components to reference both decisions where applicable;
7. remove direct data writes from either authority into component-owned stores;
8. separate policy bundles from resource envelopes;
9. create independent health, failure, rollback, repair, and receipt paths;
10. update profile applicability;
11. test policy-authorized/resource-rejected and policy-denied/resource-available cases;
12. preserve historical combined records as migration evidence;
13. cut over atomically with rollback or forward repair.

Migration does not reinterpret previous capacity decisions as authorization or previous authorization as admission.

## Validation

Conformance evidence for this ADR includes:

1. `DEC-GOV-001` and `LOCK-GOV-001` are active;
2. Resource Governor controls resource dimensions and not governed authorization;
3. Governance Policy Runtime controls governed policy decisions and not resource scheduling;
4. the owning component retains business data and commit authority;
5. Identity and Trust remains separate from both decision authorities;
6. resource and policy requests use separate stable identities;
7. resource and policy results use separate result types;
8. execution contexts reference both decisions without creating a super-authority;
9. positive resource admission cannot bypass denied or missing authority;
10. positive policy authorization cannot bypass rejected or missing resource admission;
11. expiry, revocation, target mismatch, and correlation mismatch block execution;
12. tentative reservations cannot execute protected actions;
13. Resource Governor remains in the global baseline;
14. Governance Policy Runtime is required only for sovereign-governance or high-assurance profile claims;
15. profile-specific capacities and implementations remain profile-scoped;
16. offline tests preserve separate local policy and resource decisions;
17. failure tests cover every partial-success combination;
18. receipts distinguish policy, resource, execution, effect, commit, rollback, repair, and recovery;
19. neither authority writes directly to another component's authoritative source tables;
20. resource envelopes and policy bundles activate and roll back independently;
21. Audit Broker stores evidence without replacing underlying authority;
22. deterministic inputs produce deterministic mandatory decisions where their contracts require determinism.

Expected validation failure codes include:

```text
governance_resource_authority_merged
resource_admission_used_as_authorization
policy_authorization_used_as_capacity
resource_decision_identity_missing
policy_decision_identity_missing
decision_scope_mismatch
decision_correlation_mismatch
decision_validity_intersection_empty
resource_admission_missing
governance_authority_missing
governance_policy_indeterminate
resource_capacity_rejected
tentative_reservation_executed
component_commit_authority_bypassed
cross_component_source_write_attempt
resource_envelope_policy_bundle_confused
profile_governance_requirement_mismatch
offline_authority_expanded
receipt_authority_ambiguous
audit_broker_authority_promoted
```

## Supersession

This ADR remains active until an accepted successor changes `DEC-GOV-001` or the ownership of resource admission and governed policy decisions.

A successor must:

- preserve explicit authority ownership;
- identify affected profiles, components, artifact classes, interfaces, tests, and evidence;
- provide migration, rollback, or forward repair;
- define decision-composition and expiry semantics;
- prevent resource state from becoming implicit authorization;
- prevent policy authorization from becoming an execution guarantee;
- preserve component data ownership and receipt truth;
- update `LOCK-GOV-001` through the lock-mutation protocol;
- record supersession in the ADR registry.

Historical copies remain retained and the identifier `ADR-019` remains permanently reserved.
