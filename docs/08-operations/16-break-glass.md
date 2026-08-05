<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-OPS-016",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "operations",
  "scope": [
    "break_glass_operation",
    "emergency_access",
    "emergency_override",
    "incident_response",
    "recovery"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json#/security_and_operations",
    "contracts/system.contract.json#/capability_degradation",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/component-catalog.json#/components/audit_broker",
    "generated/component-catalog.json#/components/koa_node_agent",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json#/artifact_classes/decision_receipt",
    "contracts/artifact-classes.contract.json#/artifact_classes/provenance_receipt",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/provenance-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-OPS-BG-001",
    "REQ-OPS-BG-002",
    "REQ-OPS-BG-003",
    "REQ-OPS-BG-004",
    "REQ-OPS-BG-005",
    "REQ-OPS-BG-006",
    "REQ-OPS-BG-007",
    "REQ-OPS-BG-008",
    "REQ-OPS-BG-009",
    "REQ-OPS-BG-010",
    "REQ-OPS-BG-011",
    "REQ-OPS-BG-012",
    "REQ-OPS-BG-013",
    "REQ-OPS-BG-014",
    "REQ-OPS-BG-015",
    "REQ-OPS-BG-016",
    "REQ-OPS-BG-017",
    "REQ-OPS-BG-018",
    "REQ-OPS-BG-019",
    "REQ-OPS-BG-020",
    "REQ-OPS-BG-021",
    "REQ-OPS-BG-022",
    "REQ-OPS-BG-023",
    "REQ-OPS-BG-024",
    "REQ-OPS-BG-025",
    "REQ-OPS-BG-026",
    "REQ-OPS-BG-027",
    "REQ-OPS-BG-028",
    "REQ-OPS-BG-029",
    "REQ-OPS-BG-030",
    "REQ-OPS-BG-031",
    "REQ-OPS-BG-032",
    "REQ-OPS-BG-033",
    "REQ-OPS-BG-034",
    "REQ-OPS-BG-035",
    "REQ-OPS-BG-036",
    "REQ-OPS-BG-037",
    "REQ-OPS-BG-038",
    "REQ-OPS-BG-039",
    "REQ-OPS-BG-040",
    "REQ-OPS-BG-041",
    "REQ-OPS-BG-042",
    "REQ-OPS-BG-043",
    "REQ-OPS-BG-044",
    "REQ-OPS-BG-045",
    "REQ-OPS-BG-046",
    "REQ-OPS-BG-047",
    "REQ-OPS-BG-048",
    "REQ-OPS-BG-049",
    "REQ-OPS-BG-050",
    "REQ-OPS-BG-051",
    "REQ-OPS-BG-052",
    "REQ-OPS-BG-053",
    "REQ-OPS-BG-054",
    "REQ-OPS-BG-055",
    "REQ-OPS-BG-056"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-DEV-013",
    "DOC-LIFE-006",
    "DOC-LIFE-016",
    "DOC-SEC-009",
    "DOC-SEC-019",
    "DOC-OPS-000",
    "DOC-OPS-001",
    "DOC-OPS-002",
    "DOC-OPS-003",
    "DOC-OPS-004",
    "DOC-OPS-005",
    "DOC-OPS-006",
    "DOC-OPS-007",
    "DOC-OPS-008",
    "DOC-OPS-009",
    "DOC-OPS-010",
    "DOC-OPS-011",
    "DOC-OPS-012",
    "DOC-OPS-013",
    "DOC-OPS-014",
    "DOC-OPS-015"
  ],
  "tags": [
    "operations",
    "break-glass",
    "emergency-access",
    "emergency-override",
    "least-privilege",
    "dual-control",
    "time-bounded",
    "receipts",
    "revocation",
    "incident-response",
    "restoration",
    "post-event-review"
  ]
}
KOA:DOC-META:END -->

# Break-Glass Operations

> **Document status:** Normative operations architecture.
> **Definition:** A break-glass operation is a narrowly controlled emergency operation requiring explicit authorization, evidence, and post-event review.
> **Authority rule:** Break-glass temporarily enables one already-defined capability; it does not create new architectural authority.

## 1. Purpose

This document defines how kOA requests, approves, grants, executes, observes, expires, revokes, restores, and reviews break-glass operations.

Break-glass exists for emergencies in which delay or failure of the normal path could cause material harm, such as:

- loss or corruption of authoritative data;
- prolonged loss of a required capability;
- active security compromise;
- unsafe resource exhaustion;
- inability to revoke exposed credentials;
- failure of normal recovery or policy infrastructure;
- an urgent sovereign-node condition while disconnected;
- an irreversible transition requiring immediate containment.

Break-glass is exceptional. It is not an alternate administrative workflow.

The procedure protects:

- explicit current authorization;
- least privilege;
- component and data ownership;
- profile boundaries;
- cryptographic and release integrity;
- bounded duration;
- independent oversight where required;
- complete attribution and receipts;
- safe termination and revocation;
- controlled rollback or forward repair;
- restoration of normal operations;
- mandatory post-event learning.

## 2. Scope

### 2.1 Included scope

This document applies to emergency operations involving:

- identity or credential revocation;
- service control;
- node control;
- resource-pressure intervention;
- emergency isolation;
- temporary read or maintenance access;
- emergency data-owner repair;
- queue or lease containment;
- recovery routing;
- artifact or Release Set recovery;
- governance recovery;
- offline sovereign-node intervention;
- incident containment;
- restoration after a failed transition.

### 2.2 Excluded uses

Break-glass is not used for:

- ordinary deployment;
- planned maintenance;
- routine support;
- convenience access;
- faster approval;
- bypassing a disputed policy;
- avoiding test or release requirements;
- permanent administration;
- exploratory data access;
- unrestricted diagnostics;
- performance tuning;
- compensating for missing operational documentation;
- normal user access recovery when the normal recovery path works.

### 2.3 Security and operations distinction

This document owns the operational lifecycle of a break-glass action:

`text
request
→ approve
→ grant
→ execute
→ observe
→ stop
→ revoke
→ restore
→ review
`

Security contracts own identity assurance, credential protection, cryptographic controls, privileged-path mechanisms, and security classifications.

Component, lifecycle, profile, data, and release contracts continue to own their respective boundaries.

### 2.4 Profile applicability

Break-glass is available only when the active profile explicitly supports it.

A profile can:

- prohibit break-glass;
- permit only read or isolation actions;
- require multiple approvers;
- require physical presence;
- require hardware-backed credentials;
- require live independent observation;
- support offline quorum;
- limit action classes and duration.

High-assurance profiles require governed, temporary, receipted break-glass behavior.

## 3. Canonical References

### 3.1 Canonical ownership

| Information | Canonical owner |
| --- | --- |
| Break-glass concept and supported operation classes | System security-and-operations registry |
| Actor, approver, executor, service, node, and credential identity | Identity and Trust |
| Emergency authorization, conditions, quorum, exceptions, and expiry | Governance Policy Runtime |
| CPU, memory, I/O, process, worker, queue, and timeout enforcement | Resource Governor |
| Component action semantics and authoritative data | Owning component contract |
| Profile-specific mechanism and permitted scope | Active profile contract |
| Critical receipts and evidence | Audit Broker and evidence registry |
| Service, artifact, migration, rollback, and forward-repair behavior | Lifecycle contracts |
| Exact active channel compatibility | Release Set |
| Requirements, locks, exceptions, tests, and evidence | Canonical registries |

### 3.2 Decision receipt

A break-glass authorization uses the canonical decision-receipt contract.

The receipt identifies at least:

- decision and correlation identities;
- requester and approver identities;
- exact action and target;
- scope and conditions;
- decision;
- reason codes;
- validity period;
- obligations;
- applicable policy identity.

The receipt does not contain credential values.

### 3.3 Execution and provenance evidence

The operation can produce provenance receipts and additional evidence for:

- grant issuance;
- command or operation invocation;
- material mutation;
- rollback or forward repair;
- credential revocation;
- restoration validation;
- post-event review.

Evidence references exact operation identities rather than duplicating authoritative component state.

## 4. Model and Responsibilities

### 4.1 Break-glass states

The lifecycle states are:

`text
requested
→ validating
→ approved
→ granted
→ active
→ stopping
→ revoked
→ restoring
→ closed
`

Alternative terminal or recovery states are:

`text
denied
expired
failed
rolled_back
forward_repair
`

`approved` means policy has allowed the request.

`granted` means the bounded capability or credential has been issued.

`active` means execution has started.

None of these states by itself proves that the emergency objective succeeded.

### 4.2 Responsibility allocation

| Actor or component | Responsibility |
| --- | --- |
| Requester | Declares emergency, harm, failed normal path, scope, duration, and restoration plan |
| Approver | Evaluates necessity, proportionality, scope, separation of duties, and conditions |
| Governance Policy Runtime | Produces the authoritative allow or deny decision |
| Identity and Trust | Resolves actors, sessions, devices, services, nodes, and trust material |
| Grant issuer or privileged broker | Issues and enforces the exact temporary capability |
| Executor | Performs only approved actions and stops at declared conditions |
| Independent observer | Monitors execution where profile or policy requires it |
| Owning component | Owns domain semantics, data mutations, validation, and recovery interfaces |
| Resource Governor | Enforces execution resource and timeout boundaries |
| Audit Broker | Persists required receipts and correlated evidence |
| kOA Node Agent | Coordinates node-local privileged operations where deployed |
| Incident commander | Coordinates the wider incident without replacing component or policy authority |
| Reviewer | Conducts post-event review and tracks corrective actions |

### 4.3 Impact classes

The applicable registry or policy classifies break-glass operations by impact.

Operational interpretation:

| Impact | Typical characteristics |
| --- | --- |
| Bounded diagnostic | Read-only, narrow data, no authoritative mutation |
| Containment | Isolation, revocation, suspension, routing restriction |
| Recovery mutation | Owner-approved state or configuration repair |
| High impact | Broad service effect, sensitive data, identity, policy, signing, Release Set, irreversible migration, or sovereign-node control |

Approval quorum, observation, credentials, and duration can increase with impact.

### 4.4 Request model

A complete request includes:

`text
request_id
incident_id
requester_identity
affected_capability
target_scope
requested_action
impact_class
expected_harm
normal_path_failure
minimum_required_privilege
requested_start
maximum_duration
stop_conditions
restoration_plan
evidence_plan
`

It also references:

`text
component_contract
profile
current_release_set
policy
resource_envelope
exception
repair_or_rollback_plan
`

where applicable.

### 4.5 Grant model

A grant binds:

- exact approved actor or service;
- exact target;
- exact operation verbs;
- exact data and tenant scope;
- exact network and host scope;
- start and expiry;
- maximum session duration;
- required observer;
- resource envelope;
- stop conditions;
- revocation identity;
- decision receipt;
- incident correlation.

A grant is denied by default outside those values.

### 4.6 Separation-of-duties model

Separation can involve:

- requester;
- policy approver;
- second approver;
- credential custodian;
- executor;
- independent observer;
- reviewer.

High-assurance high-impact operations require at least two distinct human approvers.

The exact quorum and role incompatibilities are owned by the active profile and policy.

Automation can enforce or execute a grant but cannot act as the required independent human approval quorum.

### 4.7 Enforcement model

The preferred execution model is capability-based:

`text
approved request
→ bounded temporary grant
→ narrow broker or owner interface
→ exact operation
→ verified result
→ automatic expiry or explicit revocation
`

A full administrative shell is used only when no narrower active contract can resolve the emergency and the profile explicitly permits that action class.

Even then, command and target constraints remain enforceable where technically possible.

### 4.8 Invariant boundary

Break-glass can temporarily override a governed operational restriction only when the policy explicitly allows that exact override.

It cannot override:

- unresolved identity;
- cryptographic invalidity;
- wrong trust-root scope;
- component data ownership;
- absence of an owner-approved mutation interface;
- incompatible active artifact state;
- profile exclusion;
- hard physical resource limits;
- safety properties declared non-overridable;
- receipt-before-commit requirements;
- cultural or sovereignty constraints not explicitly included in the decision.

### 4.9 Observation and evidence

Observation is selective and purpose-bound.

It can capture:

- operation identities;
- approved and executed verbs;
- target identities;
- timestamps;
- state transitions;
- exit status;
- affected object references;
- validation results;
- resource observations;
- receipt references.

It excludes secret values and unnecessary business payloads.

### 4.10 Termination and restoration model

Every grant ends through:

- successful objective completion;
- explicit revocation;
- automatic expiry;
- stop condition;
- target divergence;
- execution failure;
- approver or incident-command withdrawal.

Termination is followed by restoration.

Restoration removes temporary authority and proves that normal contracts again govern the affected capability.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN
source=generated/requirements-index.json#/requirements
ids=REQ-OPS-BG-001,REQ-OPS-BG-002,REQ-OPS-BG-003,REQ-OPS-BG-004,REQ-OPS-BG-005,REQ-OPS-BG-006,REQ-OPS-BG-007,REQ-OPS-BG-008,REQ-OPS-BG-009,REQ-OPS-BG-010,REQ-OPS-BG-011,REQ-OPS-BG-012,REQ-OPS-BG-013,REQ-OPS-BG-014,REQ-OPS-BG-015,REQ-OPS-BG-016,REQ-OPS-BG-017,REQ-OPS-BG-018,REQ-OPS-BG-019,REQ-OPS-BG-020,REQ-OPS-BG-021,REQ-OPS-BG-022,REQ-OPS-BG-023,REQ-OPS-BG-024,REQ-OPS-BG-025,REQ-OPS-BG-026,REQ-OPS-BG-027,REQ-OPS-BG-028,REQ-OPS-BG-029,REQ-OPS-BG-030,REQ-OPS-BG-031,REQ-OPS-BG-032,REQ-OPS-BG-033,REQ-OPS-BG-034,REQ-OPS-BG-035,REQ-OPS-BG-036,REQ-OPS-BG-037,REQ-OPS-BG-038,REQ-OPS-BG-039,REQ-OPS-BG-040,REQ-OPS-BG-041,REQ-OPS-BG-042,REQ-OPS-BG-043,REQ-OPS-BG-044,REQ-OPS-BG-045,REQ-OPS-BG-046,REQ-OPS-BG-047,REQ-OPS-BG-048,REQ-OPS-BG-049,REQ-OPS-BG-050,REQ-OPS-BG-051,REQ-OPS-BG-052,REQ-OPS-BG-053,REQ-OPS-BG-054,REQ-OPS-BG-055,REQ-OPS-BG-056
renderer=requirements-list-v1
-->
- **REQ-OPS-BG-001 — SHALL:** A break-glass operation be used only to prevent or limit imminent material harm when the normal authorized path is unavailable, too slow, or incapable of resolving the emergency.
- **REQ-OPS-BG-002 — SHALL NOT:** Convenience, deadline pressure, ordinary maintenance, incomplete planning, staffing shortage, policy disagreement, or performance optimization justify break-glass use.
- **REQ-OPS-BG-003 — SHALL:** The active profile and Governance Policy Runtime explicitly permit the requested break-glass capability before it can be invoked.
- **REQ-OPS-BG-004 — SHALL NOT:** Break-glass create a capability, privilege, integration, data-access path, or host mutation mechanism absent from active contracts.
- **REQ-OPS-BG-005 — SHALL:** Every break-glass request identify the emergency, affected capability, target scope, requested action, expected harm, normal-path failure, requester, approver requirements, maximum duration, and restoration plan.
- **REQ-OPS-BG-006 — SHALL:** Identity and Trust resolve every requester, approver, executor, target node, service, device, credential, and session involved in a break-glass operation.
- **REQ-OPS-BG-007 — SHALL NOT:** Shared, anonymous, generic, borrowed, or unresolved operator identities authorize break-glass.
- **REQ-OPS-BG-008 — SHALL:** Governance Policy Runtime issue an explicit allow decision for the exact break-glass action, scope, actor, target, purpose, conditions, and validity interval.
- **REQ-OPS-BG-009 — SHALL NOT:** A prior approval, standing administrator role, host root access, physical possession, queue priority, or incident severity substitute for the current break-glass decision.
- **REQ-OPS-BG-010 — SHALL:** High-assurance profiles require approval by at least two distinct currently authorized human actors for a high-impact break-glass operation.
- **REQ-OPS-BG-011 — SHALL:** The requester, required approvers, and executor remain separately attributable even when one actor may fill more than one role under an explicitly permitted lower-impact policy.
- **REQ-OPS-BG-012 — SHALL:** The approval policy prevent one actor from approving an action solely for that same actor when the applicable profile or impact class requires separation of duties.
- **REQ-OPS-BG-013 — SHALL:** A break-glass grant use the minimum capability, target scope, data scope, network scope, operation set, and duration sufficient for the declared emergency.
- **REQ-OPS-BG-014 — SHALL NOT:** A break-glass grant provide unrestricted shell, database, storage, network, identity, signing, policy, or cross-component authority when a narrower capability can resolve the emergency.
- **REQ-OPS-BG-015 — SHALL:** Every break-glass grant have an explicit start time, expiry time, maximum duration, revocation path, and renewal policy.
- **REQ-OPS-BG-016 — SHALL NOT:** A break-glass grant be permanent, silently renewable, or converted into a standing role.
- **REQ-OPS-BG-017 — SHALL:** Renewal require a new current-state evaluation, current identities, current justification, current scope, and new decision receipt.
- **REQ-OPS-BG-018 — SHALL:** Break-glass credentials, tokens, leases, certificates, or sessions be ephemeral, purpose-bound, non-transferable, and invalid after expiry or revocation.
- **REQ-OPS-BG-019 — SHALL:** The execution mechanism enforce the exact approved verbs, resources, targets, and conditions rather than relying only on operator instructions.
- **REQ-OPS-BG-020 — SHALL:** Privileged host actions use the active profile's approved narrow privileged path.
- **REQ-OPS-BG-021 — SHALL NOT:** Break-glass bypass cryptographic verification, artifact admission, signature validation, trust-root scope, Release Set compatibility, or required integrity checks.
- **REQ-OPS-BG-022 — SHALL NOT:** Break-glass transfer component ownership, permit direct cross-component authoritative writes, or make a cache, replica, export, backup, queue, or deployment tool authoritative.
- **REQ-OPS-BG-023 — SHALL:** A break-glass mutation of component-owned data use the owning component's approved maintenance, recovery, migration, or repair interface.
- **REQ-OPS-BG-024 — SHALL:** Break-glass preserve data minimization, tenant isolation, cultural rights, consent, disclosure, retention, and deletion obligations unless the exact obligation is itself subject to an explicitly authorized bounded emergency exception.
- **REQ-OPS-BG-025 — SHALL NOT:** An emergency exception silently override another legal, cultural, tenant, safety, or sovereignty constraint.
- **REQ-OPS-BG-026 — SHALL:** Resource Governor enforce CPU, memory, I/O, process, worker, queue, concurrency, timeout, and storage boundaries for break-glass execution.
- **REQ-OPS-BG-027 — SHALL NOT:** Governance Policy Runtime substitute for Resource Governor or Resource Governor substitute for Governance Policy Runtime.
- **REQ-OPS-BG-028 — SHALL:** The break-glass procedure define expected preconditions, permitted mutations, prohibited effects, verification steps, safe stop points, and restoration postconditions.
- **REQ-OPS-BG-029 — SHALL:** The executor verify current target identity, active profile, current Release Set, component state, data version, service version, resource state, and incident state immediately before mutation.
- **REQ-OPS-BG-030 — SHALL:** A mismatch between the approved target state and observed current state block execution and require a new decision.
- **REQ-OPS-BG-031 — SHALL:** Critical break-glass selection, approval, grant, execution start, material mutation, renewal, revocation, expiry, completion, and failed restoration emit required machine-readable receipts.
- **REQ-OPS-BG-032 — SHALL:** Receipt records identify the decision, actors, target, exact action, scope, conditions, timestamps, result, correlated incident, and evidence references without recording secret values.
- **REQ-OPS-BG-033 — SHALL:** If required receipt persistence fails under receipt-before-commit semantics, the corresponding critical mutation remain uncommitted.
- **REQ-OPS-BG-034 — SHALL NOT:** Logging, screen recording, command capture, or diagnostics indiscriminately retain secrets, personal data, tenant data, cultural material, or unrelated business payloads.
- **REQ-OPS-BG-035 — SHALL:** Break-glass execution be observable in real time to authorized operations or security roles when the active profile and incident conditions support that observation.
- **REQ-OPS-BG-036 — SHALL:** A monitoring failure block high-impact break-glass execution when the applicable profile requires live independent observation.
- **REQ-OPS-BG-037 — SHALL:** The executor stop when the approved objective is reached, the grant expires, a revocation occurs, a prohibited effect appears, the target state diverges, or safe execution can no longer be verified.
- **REQ-OPS-BG-038 — SHALL:** Emergency changes be idempotent, reversible, compensatable, or governed by a predeclared forward-repair path according to the owning lifecycle contract.
- **REQ-OPS-BG-039 — SHALL NOT:** An executor improvise destructive rollback, reverse an irreversible migration, truncate authoritative data, broaden authority, or bypass a failed safety check.
- **REQ-OPS-BG-040 — SHALL:** Break-glass failure degrade or block only affected capabilities while preserving unrelated verified capabilities.
- **REQ-OPS-BG-041 — SHALL:** A break-glass action that changes active artifacts, services, policies, data versions, routing, or Release Set state follow the applicable lifecycle activation, rollback, or forward-repair contract.
- **REQ-OPS-BG-042 — SHALL:** Completion revoke or expire every temporary credential, token, lease, route, privilege, session, and execution binding created for the operation.
- **REQ-OPS-BG-043 — SHALL:** Restoration remove temporary configuration, verify component and data ownership, reconcile queues and leases, validate services and artifacts, and return capabilities through `restoring`.
- **REQ-OPS-BG-044 — SHALL NOT:** Normal operation resume while temporary authority, unresolved mutation, stale route, orphaned process, unverified data state, or incomplete receipt remains.
- **REQ-OPS-BG-045 — SHALL:** The final outcome distinguish completed, partially completed, failed, revoked, expired, rolled back, and forward-repaired operations.
- **REQ-OPS-BG-046 — SHALL:** A post-event review occur after every exercised break-glass operation, including failed and test operations classified by policy as reviewable.
- **REQ-OPS-BG-047 — SHALL:** The post-event review evaluate necessity, decision quality, scope, separation of duties, execution, data effects, evidence, restoration, user impact, control failures, and recurrence prevention.
- **REQ-OPS-BG-048 — SHALL:** Temporary emergency changes either be removed or converted through the normal reviewed development, release, policy, and activation process.
- **REQ-OPS-BG-049 — SHALL NOT:** A successful emergency change become canonical configuration, code, policy, data migration, or operational practice solely because it worked.
- **REQ-OPS-BG-050 — SHALL:** Offline break-glass use locally admitted identities, policies, trust material, credentials, receipts, and repair artifacts and preserve equivalent scope, expiry, evidence, and restoration controls.
- **REQ-OPS-BG-051 — SHALL NOT:** Network unavailability justify anonymous access, missing approval, unbounded duration, absent receipts, integrity bypass, or delayed revocation beyond the declared offline procedure.
- **REQ-OPS-BG-052 — SHALL:** Where required online approvers are unavailable, an offline emergency quorum and credential path must have been explicitly provisioned and tested before the incident.
- **REQ-OPS-BG-053 — SHALL:** Break-glass secrets and sealed emergency materials be inventoried, protected, periodically tested without exposing values, rotated after use or suspected exposure, and recoverable under the active profile.
- **REQ-OPS-BG-054 — SHALL:** Profile-specific mechanisms such as hardware tokens, sealed credentials, physical custody, recovery consoles, privileged brokers, quorum rules, or live observation remain scoped to profiles that adopt them.
- **REQ-OPS-BG-055 — SHALL:** Retention preserve decisions, receipts, commands or operation records, evidence, restoration results, reviews, exceptions, and corrective actions for the applicable policy period while minimizing sensitive payload content.
- **REQ-OPS-BG-056 — SHALL:** Break-glass conformance test denied normal-path use, identity resolution, quorum, minimum scope, expiry, revocation, enforcement, receipts, safe stop, rollback or forward repair, offline use, restoration, review, and prohibited side effects.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Request

1. identify the incident and affected capability;
2. describe imminent material harm;
3. show why the normal path cannot resolve the emergency;
4. select the smallest defined action class;
5. identify exact targets and data scope;
6. specify requested duration and stop conditions;
7. attach rollback, repair, or restoration behavior;
8. submit the request through the declared emergency path.

### 6.2 Validate

The validation step:

1. resolves requester identity and session assurance;
2. resolves the active profile and break-glass support;
3. resolves the target component, node, service, data, and current Release Set;
4. verifies that the requested capability already exists in active contracts;
5. verifies the impact class;
6. verifies current incident state;
7. verifies resource and privileged-path availability;
8. verifies required receipts and observation;
9. rejects incomplete or overbroad requests.

### 6.3 Approve

1. Governance Policy Runtime evaluates current policy;
2. required approvers review necessity and proportionality;
3. approvers reduce scope or duration where possible;
4. separation-of-duties rules are checked;
5. conditions, obligations, stop rules, and validity are fixed;
6. an allow or deny decision receipt is persisted;
7. grant issuance proceeds only after an allow decision.

### 6.4 Issue the grant

1. bind the decision to exact actors, target, verbs, scope, and incident;
2. issue an ephemeral credential, token, lease, certificate, session, or broker capability;
3. bind start and expiry;
4. bind resource and execution limits;
5. bind observer requirements;
6. verify the grant against the approved request;
7. emit the grant receipt;
8. keep the grant inactive until execution preflight passes where the mechanism supports staged activation.

### 6.5 Execute preflight

Immediately before mutation:

1. reauthenticate the executor;
2. verify the grant is active and unrevoked;
3. verify target identity and state;
4. verify active profile and Release Set;
5. verify applicable component and data versions;
6. verify current incident and stop conditions;
7. verify resource limits;
8. verify observer and receipt persistence;
9. stop and request a new decision on any mismatch.

### 6.6 Execute

1. enter `active`;
2. invoke the narrow broker or component-owner interface;
3. perform only approved operations;
4. observe state and resource effects;
5. persist required material-operation receipts;
6. validate each critical mutation;
7. stop at the first objective-complete or mandatory-stop condition;
8. never expand scope during the active grant.

A new action or target requires a new request and decision.

### 6.7 Handle failure

On failure:

1. stop additional mutations;
2. preserve bounded evidence;
3. revoke or freeze the active grant where appropriate;
4. identify the last verified state;
5. classify whether rollback remains safe;
6. execute only the predeclared rollback, compensation, containment, or forward-repair path;
7. keep affected capabilities blocked, degraded, or restoring;
8. emit failure and recovery-selection receipts.

### 6.8 Stop and revoke

1. mark execution stopping;
2. prevent new operation starts;
3. allow only declared safe completion or cancellation;
4. revoke every temporary credential and lease;
5. close temporary routes, sessions, ports, processes, and bindings;
6. verify revocation at the enforcement point;
7. emit revocation or expiry receipts.

### 6.9 Restore

1. remove temporary configuration;
2. reconcile service, process, queue, lease, routing, and storage state;
3. verify component-owned data through owner interfaces;
4. verify artifacts, policies, services, and Release Set compatibility;
5. verify no temporary privilege remains;
6. verify required receipts;
7. enter `restoring`;
8. run representative capability tests;
9. return to normal or a declared continuing degraded state.

### 6.10 Close and review

1. record the final outcome;
2. preserve correlated evidence;
3. identify user, tenant, cultural, security, and operational impacts;
4. conduct the required post-event review;
5. identify control, documentation, tooling, policy, or architecture gaps;
6. assign corrective actions and owners;
7. process any durable change through normal development and release;
8. close the break-glass record only after restoration and review requirements are satisfied.

### 6.11 Offline break-glass

For a disconnected node:

1. resolve the locally provisioned emergency quorum;
2. authenticate with admitted local emergency credentials;
3. resolve the locally admitted policy and profile;
4. create and persist local decision and operation receipts;
5. issue the bounded local grant;
6. execute normal preflight, enforcement, stop, revocation, and restoration;
7. protect receipts against loss or alteration;
8. synchronize receipts and review records when an authorized connection becomes available.

Offline operation does not weaken scope or expiry.

## 7. Failure States and Safe Degradation

| Failure condition | Required response | Preserved behavior |
| --- | --- | --- |
| Normal path remains available | Deny break-glass | Normal authorized procedure |
| Request justification incomplete | Deny or return for normal-path remediation | Existing state |
| Requester identity unresolved | Deny | Existing authorities |
| Required approver unavailable | Deny unless a preprovisioned offline quorum applies | Current verified state |
| Separation of duties fails | Deny | Existing operation |
| Policy engine unavailable | Use only an explicitly provisioned offline policy path; otherwise deny | Current verified state |
| Grant issuance fails | Do not execute | Approved decision without capability |
| Target state differs from approval | Stop and request a new decision | Current observed state |
| Resource envelope cannot be enforced | Block execution | Existing bounded capabilities |
| Observer unavailable where mandatory | Block high-impact execution | Lower-impact unaffected work |
| Receipt persistence unavailable | Keep receipt-before-commit mutation uncommitted | Prior authoritative state |
| Grant expires during operation | Stop new operations and enter safe stop or recovery | Last verified state |
| Revocation propagation fails | Isolate target and affected credentials | Unrelated capabilities |
| Owner repair interface unavailable | Block authoritative mutation | Read-only or containment actions where approved |
| Rollback is unsafe | Use predeclared forward repair | Preserved post-boundary state |
| Restoration validation fails | Remain `restoring` or `blocked` | Last verified state |
| Offline receipt store unavailable | Deny material mutation | Non-mutating local diagnostics where policy allows |
| Emergency credentials suspected exposed | Revoke, rotate, and suspend their use | Alternate verified emergency path |
| Partial operation outcome uncertain | Reconcile current state before retry or repair | Current authoritative state |
| Post-event review overdue | Keep governance finding open and block renewal where policy requires | Restored runtime capability |

Safe degradation never converts an expired or failed grant into standing access.

## 8. Cross-Component Interactions

### 8.1 Governance Policy Runtime

Governance Policy Runtime is the authoritative decision point for governed break-glass actions.

It defines applicable quorum, impact class, conditions, duration, obligations, and exceptions.

It does not execute the action.

### 8.2 Identity and Trust

Identity and Trust authenticates all actors, services, nodes, devices, credentials, and sessions.

Emergency credentials remain subject to identity, expiry, revocation, and trust-root scope.

### 8.3 Resource Governor

Resource Governor constrains emergency processes, jobs, workers, queues, CPU, memory, I/O, timeouts, and storage.

Emergency authorization does not remove resource limits.

### 8.4 Audit Broker

Audit Broker receives required decision, grant, execution, mutation, revocation, restoration, and review receipts.

It does not receive unrestricted payloads or secrets.

### 8.5 Owning component

The owning component defines:

- valid emergency operations;
- data and business preconditions;
- mutation interfaces;
- validation;
- rollback;
- compensation;
- forward repair;
- final domain result.

Break-glass does not transfer those responsibilities.

### 8.6 kOA Node Agent

Where deployed, kOA Node Agent can enforce node-local grants, service control, isolation, temporary routing, process termination, artifact selection, and restoration.

Its actions remain bounded by the decision, profile, lifecycle, component, and resource contracts.

### 8.7 Release and lifecycle authorities

Changes to artifacts, policies, services, migrations, and Release Sets follow the normal lifecycle contracts even during an emergency.

Break-glass can authorize entry into the emergency procedure. It cannot redefine artifact compatibility or activation semantics.

### 8.8 Incident response

Incident response owns coordination, communication, containment strategy, and incident status.

Break-glass is one controlled action within the incident, not the incident authority itself.

### 8.9 Support and diagnostics

Support can gather bounded diagnostics before or during an emergency.

Diagnostic access does not automatically grant break-glass mutation authority.

## 9. Decision Closure and Prohibited Assumptions

The following decisions are closed:

- break-glass is exceptional and harm-driven;
- the capability must already exist in active contracts;
- Governance Policy Runtime issues the exact current authorization;
- every actor is individually attributable;
- high-assurance high-impact operations require at least two distinct human approvers;
- scope and duration are minimal and enforced;
- grants are temporary and non-transferable;
- integrity, ownership, profile, and release boundaries remain active;
- critical steps produce receipts;
- failure uses declared rollback or forward repair;
- every grant is revoked or expires;
- restoration passes through `restoring`;
- every exercised operation receives post-event review;
- durable changes return through normal development and release;
- offline use requires preprovisioned equivalent controls.

Prohibited assumptions include:

- treating root access as emergency authorization;
- treating physical access as identity;
- using a shared emergency account;
- approving an unrestricted shell when a narrow operation exists;
- leaving an emergency token active for future use;
- changing scope during execution without a new decision;
- bypassing signatures or artifact admission;
- writing directly into another component's database;
- treating a backup as permission for destructive action;
- logging secret values for audit completeness;
- continuing after grant expiry;
- assuming revocation succeeded without verification;
- declaring restoration because the process restarted;
- converting an emergency fix directly into canonical configuration;
- postponing review because the emergency was successful;
- allowing an external AI or integration to approve or execute break-glass authority;
- using Internet loss as justification for unreceipted access;
- applying hardware-token, physical-custody, or quorum mechanisms globally outside adopting profiles.

## 10. Validation Criteria

Break-glass conformance validates when:

1. normal-path availability is evaluated;
2. imminent material harm and emergency necessity are explicit;
3. the requested capability exists in active contracts;
4. the active profile permits the action class;
5. requester, approvers, executor, observer, target, and session identities resolve;
6. applicable separation-of-duties rules pass;
7. high-assurance high-impact tests require two distinct human approvers;
8. the decision binds exact action, target, scope, duration, and conditions;
9. the grant cannot exceed the decision;
10. temporary credentials expire and revoke correctly;
11. enforcement limits verbs, resources, targets, and data scope;
12. privileged actions use the approved narrow path;
13. cryptographic, artifact, profile, component, data, and Release Set boundaries remain enforced;
14. Resource Governor and Governance Policy Runtime remain separate;
15. preflight detects target-state drift;
16. required receipts persist at each critical state;
17. logs and evidence exclude secret values and unnecessary payloads;
18. mandatory observation failure blocks the applicable operation;
19. stop conditions and expiry halt new actions;
20. failure selects only declared rollback, compensation, containment, or forward repair;
21. unrelated capabilities survive affected-scope failure;
22. all temporary routes, privileges, processes, sessions, and credentials are removed;
23. restoration verifies data, services, artifacts, routing, leases, queues, resources, and receipts;
24. normal mutation resumes only after `restoring` passes;
25. the final outcome is explicit;
26. post-event review covers necessity, execution, impact, restoration, and corrective action;
27. durable emergency changes pass normal development and release;
28. offline tests preserve equivalent quorum, scope, expiry, evidence, and revocation;
29. emergency materials are inventoried, tested, rotated, and recoverable;
30. profile-specific mechanisms remain profile-scoped;
31. all decisions, requirements, locks, exceptions, tests, and evidence resolve;
32. no unresolved marker, placeholder, duplicate canonical owner, or ordinary documentation hash appears;
33. operations, security, component-boundary, lifecycle, traceability, and Interfile Alignment Lock checks pass.

Applicable checks include:

`bash
python docs/tools/check_component_boundaries.py
python docs/tools/check_profile_composition.py
python docs/tools/check_artifact_contracts.py
python docs/tools/check_release_sets.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

### 11.1 Emergency credential revocation

An active service credential is suspected compromised, and the normal identity administration path is unavailable.

Two authorized high-assurance approvers allow one exact revocation operation for one credential. A bounded broker revokes it, verification confirms rejection at the service boundary, temporary authority expires, and the incident proceeds through restoration and review.

### 11.2 Resource-pressure containment

A runaway optional workload threatens a required service.

Break-glass authorizes termination of one exact workload process when the normal scheduler-control path is unavailable. Resource Governor still enforces node boundaries, and no broader service-control privilege is issued.

### 11.3 Owner-approved data repair

A committed migration leaves one component's records in a state incompatible with rollback.

Break-glass authorizes execution of the predeclared forward-repair artifact through the component owner's repair interface. It does not grant direct database editing.

### 11.4 Denied convenience request

An operator requests an unrestricted administrative shell to avoid waiting for a routine deployment approval.

The request is denied because the normal path remains available and no imminent material harm exists.

### 11.5 Expired grant

A five-minute emergency isolation grant expires before the executor starts a second target.

The second action is blocked. A new current-state request and decision are required.

### 11.6 Offline sovereign-node operation

A disconnected sovereign node cannot reach online approvers during an active credential compromise.

A preprovisioned offline quorum uses locally admitted hardware-backed identities, issues a bounded local decision receipt, revokes the exact credential, records receipts locally, restores the node, and later synchronizes the evidence through an authorized path.

### 11.7 Emergency change converted normally

An emergency route restriction successfully contains an incident.

The temporary rule is removed after restoration. A durable equivalent is proposed, reviewed, tested, published, and activated through the normal governance and release process.
