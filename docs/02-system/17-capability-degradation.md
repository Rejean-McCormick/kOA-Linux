<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-017",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "contracts/subsystems/koa-spaces.subsystem.json",
    "02-system/21-koa-spaces-experience-layer.md",
    "02-system/22-koa-spaces-interface-composition.md"
  ],
  "decision_ids": [
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-DATA-001",
    "DEC-GATE-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-SENT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [
    "REQ-DEG-001",
    "REQ-DEG-002",
    "REQ-DEG-003",
    "REQ-DEG-004",
    "REQ-DEG-005",
    "REQ-DEG-006",
    "REQ-DEG-007",
    "REQ-DEG-008",
    "REQ-DEG-009",
    "REQ-DEG-010",
    "REQ-DEG-011",
    "REQ-DEG-012",
    "REQ-DEG-013",
    "REQ-DEG-014",
    "REQ-DEG-015",
    "REQ-DEG-016",
    "REQ-DEG-017",
    "REQ-DEG-018",
    "REQ-DEG-019",
    "REQ-DEG-020",
    "REQ-DEG-021",
    "REQ-DEG-022",
    "REQ-DEG-023",
    "REQ-DEG-024",
    "REQ-DEG-025",
    "REQ-DEG-026",
    "REQ-DEG-027",
    "REQ-DEG-028",
    "REQ-DEG-029",
    "REQ-DEG-030",
    "REQ-DEG-031",
    "REQ-DEG-032",
    "REQ-DEG-033",
    "REQ-DEG-034",
    "REQ-DEG-035",
    "REQ-DEG-036"
  ],
  "lock_ids": [
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SENT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-SPACES-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-000",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-SYS-019",
    "DOC-SYS-020"
  ],
  "tags": [
    "system",
    "capability-degradation",
    "safe-degradation",
    "fail-closed",
    "offline-continuity",
    "recovery",
    "resource-governance",
    "component-separation",
    "artifact-activation",
    "observability",
    "koa-spaces",
    "experience-layer"
  ]
}
KOA:DOC-META:END -->

# Capability Degradation

## 1. Purpose

This document defines how kOA reduces, blocks, and restores capabilities when an authority, dependency, resource, integration, data path, artifact, or infrastructure function is unavailable or invalid.

The objective is to keep unaffected capabilities useful while preventing degraded operation from silently weakening authority, integrity, privacy, cultural rights, component ownership, release compatibility, or recovery guarantees.

Degradation is capability-scoped. A failure does not make the entire system either fully available or fully unavailable.

## 2. Scope

This document applies to:

- all global system capabilities;
- all deployment profiles and profile overlays;
- all component capabilities and component dependencies;
- all operating modes;
- all local, disconnected, and externally integrated operation;
- all resource, storage, queue, network, identity, policy, publication, ingestion, audit, backup, restore, and artifact-activation paths;
- all critical transitions and their receipts;
- all conformance claims concerning continuity, failure handling, recovery, or offline behavior.

This document does not define:

- provider-specific uptime targets;
- implementation-specific retry intervals;
- component-internal algorithms that do not affect an external capability contract;
- a universal requirement that every capability remain available;
- permission to bypass an unavailable authority.

Profile-specific degradation envelopes remain owned by profile contracts. Component-specific behavior remains owned by component contracts. This document defines the global model they must follow.

## 3. Canonical References

The canonical sources are:

`text
contracts/system.contract.json#/capability_degradation
generated/component-catalog.json
generated/profile-catalog.json
contracts/profiles/*.profile.json
contracts/artifact-classes.contract.json
contracts/release-channels.contract.json
contracts/integration-types.contract.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/exception-index.json
generated/test-catalog.json
generated/evidence-catalog.json
`

Ownership is divided as follows:

| Information | Canonical owner |
| --- | --- |
| Global degradation states, modes, cause classes, and transition rules | `system.registry.json#/capability_degradation` |
| Capability owner, dependencies, interfaces, data ownership, and component failure behavior | `components.registry.json` and component contracts |
| Required, optional, conditional, task-activated, and excluded capabilities | Profile contracts |
| Profile-specific offline and degradation envelopes | Profile contracts |
| Artifact activation, rejection, rollback, revocation, recreation, and repair behavior | `artifact-classes.registry.json` |
| Cross-channel compatibility and Release Set activation | `release-channels.registry.json` |
| External integration failure and removal behavior | `integrations.registry.json` |
| Normative statements | `requirements.registry.json` |
| Cross-file invariants | `locks.registry.json` |
| Test and evidence relationships | `traceability.registry.json` |
| Approved deviations | `exceptions.registry.json` |

The canonical terminology includes:

- **safe degradation** — reduction of an affected capability without silently violating authority, integrity, or unrelated core behavior;
- **fail-closed authority** — an operation requiring authority does not proceed when identity, policy, scope, compatibility, or ownership cannot be resolved;
- **offline continuity** — declared core capabilities remain available without Internet access within the applicable profile envelope.

## 4. Model and Responsibilities

### 4.1 Capability as the unit of degradation

A capability is the smallest externally meaningful behavior that can be independently evaluated, degraded, blocked, restored, tested, and evidenced.

Each capability record has:

| Field | Meaning |
| --- | --- |
| `capability_id` | Stable machine-readable identity |
| `owner_ref` | Owning component or canonical authority |
| `scope` | Global, profile, overlay, component, artifact, or toolchain applicability |
| `criticality` | Effect of loss within the applicable profile |
| `dependencies` | Authorities, components, data, resources, integrations, artifacts, and infrastructure required |
| `normal_behavior` | Behavior when all required dependencies are valid |
| `permitted_degradation_modes` | Allowed reduced behaviors |
| `blocked_conditions` | Conditions under which no operation is permitted |
| `preserved_state` | State that remains authoritative during failure |
| `prohibited_actions` | Actions that remain forbidden during degradation |
| `recovery_preconditions` | Checks required before normal mutation resumes |
| `receipt_policy` | Whether degradation and recovery transitions require receipts |
| `test_refs` | Tests that prove behavior and non-effects |
| `evidence_refs` | Evidence required for a conformance claim |

A process, service instance, container, host, or provider can support several capabilities. Failure of that implementation unit does not define the required outcome by itself; the capability contracts do.

### 4.2 Global state model

The global capability states are:

| State | Meaning | Mutation |
| --- | --- | --- |
| `normal` | All required dependencies and authorities for the capability are valid | Allowed within normal authority |
| `degraded` | A declared reduced mode preserves applicable authority and safety | Limited to the selected mode |
| `blocked` | No safe declared mode exists or a required authority cannot be resolved | Prohibited |
| `restoring` | Dependencies have returned, but validation and reconciliation are incomplete | Limited to restoration procedures |

The allowed degraded modes are:

| Mode | Meaning | Typical use |
| --- | --- | --- |
| `read_only` | Previously verified state can be inspected but not changed | Authority, storage, policy, or migration outage |
| `advisory` | Non-authoritative analysis or guidance can be produced without committing state | Optional analysis or planning capability |
| `queued` | Requests can be durably retained for later reevaluation | Publication, synchronization, background work |
| `locally_limited` | A bounded local subset continues without a missing external or high-cost dependency | Offline operation, resource pressure, optional integration outage |

A capability uses `degraded` only with one or more explicitly declared modes.

### 4.3 Cause classes

Cause classes identify why a capability changed state:

| Cause class | Examples |
| --- | --- |
| `authority_unresolved` | Missing decision, owner, policy, identity, scope, or exception |
| `contract_invalid` | Schema failure, incompatible version, unresolved reference |
| `dependency_unavailable` | Required component, service, data source, or gateway unavailable |
| `resource_exhausted` | CPU, memory, I/O, process, worker, or queue limit reached |
| `storage_unavailable` | Write path, capacity, durability, or database failure |
| `network_unavailable` | Internet, controlled network, or required peer unavailable |
| `integration_unavailable` | Approved optional provider or adapter unavailable |
| `verification_failed` | Signature, provenance, integrity, evidence, or admission failure |
| `artifact_activation_failed` | Staging, compatibility, activation, or rollback precondition failed |
| `receipt_persistence_failed` | Required critical-transition receipt cannot be committed |
| `recovery_incomplete` | Restore, reconciliation, or queued-work validation incomplete |
| `operator_suspension` | Explicit governed suspension for safety, maintenance, or incident response |

Cause classification describes the failure. It does not grant recovery authority.

### 4.4 Responsibilities

| Actor or component | Responsibility |
| --- | --- |
| Capability owner | Defines normal behavior, permitted degraded modes, blocked conditions, and recovery checks |
| Deployment profile | Declares capability membership, criticality, offline envelope, and profile-specific constraints |
| Resource Governor | Enforces resource limits, priorities, queues, and task suspension |
| Governance Policy Runtime | Evaluates governed authorization, disclosure, consent, privilege, and exceptions where required |
| Identity and Trust | Resolves identities and trust material required by a capability |
| Artifact verifier | Validates artifact integrity, provenance, compatibility, and admissibility |
| kOA Node Agent | Coordinates profile, release, activation, recovery, and node-level state where deployed |
| Audit Broker | Persists required evidence and receipts without becoming the authority for the underlying action |
| Component runtime | Enforces its own data ownership and declared degraded behavior |
| Operator | Performs governed intervention without bypassing capability authority |
| Conformance validator | Tests both allowed degraded behavior and prohibited side effects |

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-DEG-001,REQ-DEG-002,REQ-DEG-003,REQ-DEG-004,REQ-DEG-005,REQ-DEG-006,REQ-DEG-007,REQ-DEG-008,REQ-DEG-009,REQ-DEG-010,REQ-DEG-011,REQ-DEG-012,REQ-DEG-013,REQ-DEG-014,REQ-DEG-015,REQ-DEG-016,REQ-DEG-017,REQ-DEG-018,REQ-DEG-019,REQ-DEG-020,REQ-DEG-021,REQ-DEG-022,REQ-DEG-023,REQ-DEG-024,REQ-DEG-025,REQ-DEG-026,REQ-DEG-027,REQ-DEG-028,REQ-DEG-029,REQ-DEG-030,REQ-DEG-031,REQ-DEG-032,REQ-DEG-033,REQ-DEG-034,REQ-DEG-035,REQ-DEG-036
renderer=requirements-list-v1
-->
- **REQ-DEG-001 — SHALL:** Degradation be evaluated and reported per capability rather than per product, process, host, or deployment as a whole.
- **REQ-DEG-002 — SHALL:** Every capability have one owning component or canonical authority and one declared degradation policy.
- **REQ-DEG-003 — SHALL:** The capability state model use `normal`, `degraded`, `blocked`, and `restoring` as the global states.
- **REQ-DEG-004 — SHALL:** A degraded capability use only a declared `read_only`, `advisory`, `queued`, or `locally_limited` mode.
- **REQ-DEG-005 — SHALL NOT:** A degradation mode broaden authority, privilege, disclosure, mutation rights, data ownership, network reachability, or profile scope.
- **REQ-DEG-006 — SHALL:** A capability enter `blocked` when no declared degradation mode preserves authority, integrity, safety, and applicable rights.
- **REQ-DEG-007 — SHALL:** Failure of one capability preserve unrelated capabilities whose dependencies remain satisfied.
- **REQ-DEG-008 — SHALL:** Every degraded or blocked state expose the affected capability, cause class, active mode, preserved behavior, prohibited behavior, and recovery preconditions.
- **REQ-DEG-009 — SHALL:** A state transition classified as critical emit a machine-readable receipt or remain uncommitted when the required receipt cannot be persisted.
- **REQ-DEG-010 — SHALL:** Authority ambiguity, missing owner decisions, unresolved scope, incompatible contracts, or failed identity verification block the affected authoritative operation.
- **REQ-DEG-011 — SHALL NOT:** A presentation surface, cache, replica, external integration, AI surface, recipe, or fallback component acquire authority because the intended authority is unavailable.
- **REQ-DEG-012 — MAY:** Previously verified state remain readable during an authority outage when the applicable policy explicitly permits read-only access.
- **REQ-DEG-013 — SHALL:** Pending mutations remain uncommitted, rejected, or durably queued according to the capability contract.
- **REQ-DEG-014 — SHALL:** A durable queue preserve request identity, owner, ordering requirements, expiry, retry limits, and cancellation behavior.
- **REQ-DEG-015 — SHALL NOT:** A queue convert an unauthorized request into an authorized request when dependencies recover.
- **REQ-DEG-016 — SHALL:** Resource pressure be handled through deterministic limits, throttling, queuing, task suspension, or task rejection before unrelated core capabilities are exhausted.
- **REQ-DEG-017 — SHALL:** Resource Governor remain the authority for resource envelopes, priorities, concurrency, queues, scheduling, and process limits during degradation.
- **REQ-DEG-018 — SHALL:** Unavailability of Resource Governor block unconstrained or resource-intensive work whose safe envelope cannot otherwise be enforced.
- **REQ-DEG-019 — SHALL:** Unavailability of Governance Policy Runtime block governed authorization, disclosure, consent, exception, or privilege decisions for profiles and capabilities that require it.
- **REQ-DEG-020 — SHALL NOT:** Resource Governor substitute for Governance Policy Runtime or Governance Policy Runtime substitute for Resource Governor.
- **REQ-DEG-021 — SHALL:** Internet or optional external-integration failure disable only capabilities that explicitly depend on that integration.
- **REQ-DEG-022 — SHALL:** The declared offline core remain available within the active profile's offline capability envelope.
- **REQ-DEG-023 — SHALL:** External AI failure preserve deterministic local workflows and authoritative local state.
- **REQ-DEG-024 — SHALL:** Ariane voice unavailability remove voice interaction without changing non-vocal Ariane navigation authority.
- **REQ-DEG-025 — SHALL:** SenTient resource, engine, or model failure remain isolated from required baseline operation.
- **REQ-DEG-026 — SHALL:** kOA Mediatheque transformation or background-worker failure preserve accepted local source media and previously verified outputs.
- **REQ-DEG-027 — SHALL:** Publication Gateway failure queue or reject publication without changing source-domain authority or disclosing content.
- **REQ-DEG-028 — SHALL:** UCKK Publication Bridge failure reject or defer new media publication without affecting existing kOA Mediatheque content.
- **REQ-DEG-029 — SHALL:** Artifact verification, compatibility, signature, provenance, or activation failure leave the previous verified artifact authoritative.
- **REQ-DEG-030 — SHALL NOT:** A failed Release Set activation create a partially active combination of system, services, governance, and knowledge channel versions.
- **REQ-DEG-031 — SHALL:** Storage exhaustion or write-path failure prevent new authoritative writes before corrupting or silently truncating owned data.
- **REQ-DEG-032 — SHALL:** Backup, restore, export, import, and recovery failures preserve the last verified authoritative state and expose a repeatable recovery action.
- **REQ-DEG-033 — SHALL:** Restoration revalidate authority, profile scope, component ownership, compatibility, queued work, and applicable evidence before normal mutation resumes.
- **REQ-DEG-034 — SHALL:** A recovered dependency return a capability through `restoring`; it shall not move directly from `blocked` to unrestricted mutation.
- **REQ-DEG-035 — SHALL:** Deployment profiles declare which capabilities are required, optional, conditional, task-activated, or excluded and define their profile-specific degradation envelopes.
- **REQ-DEG-036 — SHALL:** Conformance tests verify both the intended degraded behavior and the absence of prohibited authority, mutation, disclosure, and cross-component side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Dependency evaluation

Before a capability starts or mutates state:

1. resolve the active authority release;
2. resolve the owning component or authority;
3. resolve the active deployment profile and overlays;
4. resolve required decisions, requirements, locks, and exceptions;
5. validate required identities, contracts, data sources, artifacts, resources, and integrations;
6. select `normal`, a declared `degraded` mode, or `blocked`;
7. expose the selected state and cause;
8. emit a receipt when the transition is classified as critical.

No implementation selects a less restrictive state than the capability contract permits.

### 6.2 Degradation transition

The normal transition is:

`text
normal
→ degraded
→ restoring
→ normal
`

When no safe reduced mode exists:

`text
normal | degraded
→ blocked
→ restoring
→ normal
`

A transition to `degraded` records:

- the cause class;
- selected mode;
- preserved behavior;
- prohibited actions;
- expected recovery preconditions;
- queue or retry behavior where applicable;
- receipt identity where required.

### 6.3 Queued operation

A capability may use `queued` only when:

1. the request is valid at submission time;
2. queue ownership and durability are declared;
3. the request records its authority context without freezing a future authorization result;
4. expiry, cancellation, ordering, retry, and capacity limits are explicit;
5. the operation is reevaluated against current authority before execution;
6. duplicate execution is prevented or made idempotent;
7. queue exhaustion has a declared rejection behavior.

A queued request is pending work, not an approved future mutation.

### 6.4 Resource-pressure transition

Resource pressure follows:

`text
resource threshold approached
→ lower priority or reduce concurrency
→ queue or suspend task-activated work
→ reject new heavy work
→ preserve required core capabilities
`

Resource Governor applies the active resource envelope. It does not modify authorization, disclosure, consent, or data ownership.

When the required envelope cannot be enforced, the affected unconstrained work is blocked.

### 6.5 Artifact activation failure

Artifact activation follows:

`text
validate
→ verify
→ stage
→ compatibility check
→ activate atomically
`

If any step fails:

1. the active pointer does not move, or it returns to the previous verified target;
2. no partial authoritative state remains;
3. the failed candidate is isolated;
4. the failure and recovery state are recorded;
5. retry requires the original preconditions to be reevaluated.

A Release Set activation applies this rule across all four release channels.

### 6.6 Recovery transition

Recovery follows:

1. identify the original cause;
2. restore or replace the failed dependency;
3. enter `restoring`;
4. revalidate authority and profile scope;
5. revalidate component ownership and contract compatibility;
6. verify authoritative state and recovery artifacts;
7. inspect queued work for expiry, cancellation, duplicates, and current authorization;
8. reconcile derived state without overwriting authoritative owners;
9. execute applicable recovery tests;
10. emit recovery evidence or receipts;
11. return the capability to `normal` or a declared `degraded` mode.

A dependency becoming reachable is not sufficient evidence of recovery.

## 7. Failure States and Safe Degradation

### 7.1 Global failure matrix

| Failure condition | Required capability state or mode | Preserved behavior | Prohibited behavior |
| --- | --- | --- | --- |
| Authority, owner, scope, identity, or policy unresolved | `blocked`, or `degraded/read_only` when explicitly allowed | Inspection of previously verified state | New authoritative mutation |
| Contract or reference invalid | `blocked` | Previous valid contract and active state | Use of the invalid object |
| Optional external integration unavailable | `degraded/locally_limited` or capability-specific `blocked` | Non-integrated core | Hidden substitute provider |
| Internet unavailable | Profile-declared offline modes | Declared offline core | External-only operations |
| Resource threshold exceeded | `degraded/queued` or `degraded/locally_limited` | Required core and low-cost work | Unbounded heavy work |
| Resource Governor unavailable | Heavy or unconstrained work `blocked` | Bounded low-risk operation allowed by contract | Execution without enforceable envelope |
| Governance Policy Runtime unavailable where required | Governed mutation `blocked`; possible `read_only` | Existing state and unprivileged access allowed by policy | New governed decision |
| Authoritative data owner unavailable | `read_only`, `queued`, or `blocked` as declared | Cached or replicated read-only projection with provenance | Writes through a non-owner |
| Storage capacity or durability failure | Write capability `blocked`; possible `read_only` | Last durable authoritative state | Silent truncation or partial commit |
| Required receipt cannot be persisted | Critical transition `blocked` or uncommitted | Previous authoritative state | Committed transition without required receipt |
| Verification or signature failure | Candidate `blocked` or rejected | Previous verified artifact or data | Admission or activation of failed candidate |
| Release incompatibility | Activation `blocked` | Current compatible Release Set | Partial cross-channel activation |
| Backup failure | Backup capability `blocked` or `queued` | Active authoritative state | False backup-success claim |
| Restore verification failure | Restore remains `restoring` or `blocked` | Last verified active state | Activation of unverified restored state |
| Queue capacity reached | New queue submission rejected or lower-priority work expired by policy | Existing accepted queue entries | Unbounded growth or silent loss |
| Operator suspension | Capability `blocked` or declared maintenance mode | Preserved state and diagnostics | Automatic unsuspension without authority |

### 7.2 Named capability behavior

| Capability or boundary | Failure | Required behavior |
| --- | --- | --- |
| External AI assistance | Provider, network, or adapter unavailable | Disable only the requested AI-assisted capability; retain deterministic local workflows |
| Ariane voice | Approved voice adapter unavailable | Voice unavailable; non-vocal Ariane navigation remains `normal` |
| SenTient task | Engine, model, index, or resource failure | Pause, terminate, or block the isolated task; baseline operation continues |
| kOA Mediatheque background transformation | Worker or resource failure | Queue, pause, or reject transformation; accepted local source media and verified outputs remain intact |
| kOA Mediatheque core | Required local dependency unavailable | Affected kOA Mediatheque capability degrades or blocks according to ownership and storage safety; unrelated components continue |
| UCKK Publication Bridge | UCKK transport unavailable | Queue or reject new UCKK publication; existing kOA Mediatheque content remains available |
| Publication Gateway | Publication boundary unavailable | Queue or reject publication; no disclosure occurs |
| Governance Policy Runtime | Required policy authority unavailable | Governed decisions block; Resource Governor does not substitute |
| Resource Governor | Enforcement unavailable | Heavy or unconstrained work blocks; Governance Policy Runtime does not substitute |
| Identity and Trust | Required identity or trust proof unresolved | Identity-dependent capability blocks |
| Audit Broker | Required receipt or evidence persistence unavailable | Critical transition remains uncommitted; noncritical operation follows its contract |
| kOA Node Agent | Node orchestration unavailable | Existing verified runtime state may continue when safe; new node-level activation or recovery blocks |
| Kristal Runtime | Projection or package unavailable | Dependent reading or projection capability blocks or uses a verified prior package; component-owned operational data remains unaffected |
| Language Runtime | Language pack unavailable or invalid | Affected language capability uses an explicitly available verified pack or blocks; no runtime compilation substitute |
| External publication destination | Destination unavailable | Publication remains queued or rejected according to contract; source authority remains local |

### 7.3 Safe-degradation properties

Every safe degraded state is:

- explicit;
- capability-scoped;
- profile-aware;
- authority-preserving;
- data-owner-preserving;
- bounded in time or condition;
- observable;
- reversible;
- testable;
- associated with a declared recovery path.

A degraded state that cannot satisfy all properties is treated as `blocked`.

## 8. Cross-Component Interactions

### 8.1 Dependency propagation

A component failure propagates only through declared capability dependencies.

A dependency graph can make several capabilities degrade, but the graph does not authorize a component to mutate another component's data or assume its responsibility.

### 8.2 Read-only projections

A component may display a previously verified projection during an owner outage when:

- the projection is explicitly classified as read-only;
- its source authority and freshness are visible;
- the projection cannot be written back as authoritative state;
- policy permits continued access;
- the component does not present stale data as current without qualification.

### 8.3 Resource and policy separation

Resource Governor can reduce concurrency, pause workers, reject jobs, and enforce limits.

Governance Policy Runtime can permit or deny governed operations.

A resource allowance does not authorize an operation. A policy allowance does not guarantee sufficient resources.

### 8.4 Publication and ingestion separation

Publication Gateway failure affects cross-domain publication.

UCKK Publication Bridge failure affects only outbound packaging, transport, and destination-receipt handling. UCKK Import Bridge failure affects new retrieval, quarantine intake, and remote update checks; already accepted local learning material remains available offline.

Neither failure transfers responsibility to the other gateway, and neither gateway can bypass the missing boundary.

### 8.5 Queue ownership

The capability owner or a declared queue component owns pending work.

A queue stores requests and delivery state. It does not own the authoritative domain object the request may later affect.

### 8.6 Artifact and runtime interaction

A runtime consumes only artifacts admitted for its class, version, profile, and compatibility constraints.

If a candidate artifact fails, the runtime continues with the previous verified artifact or blocks the affected capability. It does not merge partial candidate content with active state.

### 8.7 Evidence interaction

Audit Broker, evidence collectors, and conformance validators observe and record degradation.

They do not change the capability state unless they are separately authorized to request a transition through the owning component.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- degradation is capability-scoped rather than host-wide by default;
- the global states are `normal`, `degraded`, `blocked`, and `restoring`;
- the allowed degraded modes are `read_only`, `advisory`, `queued`, and `locally_limited`;
- fail-closed behavior applies to authority-dependent operations;
- safe degradation reduces capability and never expands authority;
- optional integrations do not become core dependencies;
- the active profile owns its capability and offline envelope;
- Resource Governor and Governance Policy Runtime remain separate authorities;
- Publication Gateway authorization and UCKK-specific bridge transport remain distinct sequential boundaries;
- Ariane voice loss does not disable non-vocal navigation;
- SenTient failure does not disable the baseline;
- kOA Mediatheque background-work failure preserves accepted local source media;
- failed artifact or Release Set activation preserves the previous verified state;
- recovery includes revalidation and reconciliation before unrestricted mutation resumes.

Prohibited assumptions include:

- marking an entire product unavailable because one capability failed;
- marking an entire product healthy because one process responds;
- retrying indefinitely without queue and resource limits;
- executing queued work without reevaluating current authority;
- treating cached data as authoritative because the owner is unavailable;
- using a replica, integration, or AI surface as a replacement data owner;
- treating network reconnection as proof of recovery;
- treating process restart as proof of data integrity;
- accepting partial Release Set activation;
- committing a critical transition without its required receipt;
- silently dropping pending work;
- silently changing a degraded mode;
- applying a sovereign or high-assurance failure rule globally without profile authority;
- inventing an undeclared fallback capability.

## 10. Validation Criteria

This document is conformant when:

1. metadata status is `active`;
2. all 36 requirement identifiers are unique and resolve;
3. all referenced decisions are accepted;
4. all referenced locks resolve and pass;
5. the system registry contains the four states and four degraded modes defined here;
6. every registered capability has one owner and one degradation policy;
7. every profile declares capability membership and its degradation envelope;
8. every component contract declares dependency, failure, preserved-state, and recovery behavior;
9. degraded operation never broadens authority, disclosure, privilege, mutation, data ownership, or scope;
10. unrelated capabilities remain available when their dependencies remain satisfied;
11. queued work has durability, identity, expiry, retry, cancellation, and reevaluation rules;
12. Resource Governor and Governance Policy Runtime remain distinct;
13. UCKK publication requires both gateway authorization and bridge transport;
14. external AI, Ariane voice, and SenTient failure behaviors match their canonical contracts;
15. artifact activation and Release Set failure preserve the previous verified state;
16. storage and receipt failures prevent unsafe commits;
17. recovery passes through `restoring`;
18. recovery tests verify authority, compatibility, state integrity, queues, and evidence;
19. conformance tests prove prohibited side effects do not occur;
20. no unresolved-authority marker, duplicate owner, placeholder, or silent fallback exists.

Applicable validation commands are:

`bash
python docs/tools/check_component_boundaries.py
python docs/tools/check_profile_composition.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 External AI outage

ChatGPT is unavailable.

The requested drafting capability becomes blocked or locally limited according to its integration contract. Local document access, deterministic workflows, non-vocal Ariane navigation, export, backup, and restore remain unaffected.

### 11.2 Resource pressure during kOA Mediatheque processing

A large kOA Mediatheque conversion reaches the active memory envelope.

Resource Governor lowers priority, reduces concurrency, and queues the conversion. Existing accepted local media and previously verified outputs remain readable. The system does not terminate unrelated required services to finish the conversion.

### 11.3 Policy authority outage

A governed publication request requires Governance Policy Runtime, but the runtime is unavailable.

The publication capability is blocked. The source component continues local use of its data. Publication Gateway does not infer approval, and Resource Governor does not substitute a policy decision.

### 11.4 Database write failure

A component's authoritative database loses its durable write path.

The component moves affected mutation capabilities to `blocked` and may expose verified data as read-only. Another component does not write into the failed owner's store.

### 11.5 Release incompatibility

A new services-channel version is not compatible with the active governance-channel version.

Activation stops. The previous compatible Release Set remains active. No service is selectively activated outside a declared compatible set.

### 11.6 Ariane voice failure

The approved Ariane voice adapter disconnects.

Voice interaction becomes unavailable. Ariane Runtime continues deterministic local navigation through non-vocal controls.

### 11.7 Recovery with queued work

Publication Gateway returns after an outage.

The capability enters `restoring`. Queued requests are checked for expiry, cancellation, current authorization, duplicate execution, and current destination policy. Only valid requests return to execution.

## Experience-Layer Degradation

A kOA Spaces failure is presentation-scoped. Invalid candidates are rejected while the previous validated Space remains active; missing optional contributions are hidden or marked unavailable; complete subsystem failure falls back to native interfaces or a declared administrative surface. Authority is never reassigned during degradation.
