<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-020",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/operating_modes",
    "contracts/system.contract.json#/component_boundaries",
    "contracts/system.contract.json#/data_authority_and_ownership",
    "contracts/system.contract.json#/receipts_and_critical_transitions",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-DATA-001",
    "DEC-PROFILE-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-BG-001",
    "REQ-SEC-BG-002",
    "REQ-SEC-BG-003",
    "REQ-SEC-BG-004",
    "REQ-SEC-BG-005",
    "REQ-SEC-BG-006",
    "REQ-SEC-BG-007",
    "REQ-SEC-BG-008",
    "REQ-SEC-BG-009",
    "REQ-SEC-BG-010",
    "REQ-SEC-BG-011",
    "REQ-SEC-BG-012",
    "REQ-SEC-BG-013",
    "REQ-SEC-BG-014",
    "REQ-SEC-BG-015",
    "REQ-SEC-BG-016",
    "REQ-SEC-BG-017",
    "REQ-SEC-BG-018",
    "REQ-SEC-BG-019",
    "REQ-SEC-BG-020",
    "REQ-SEC-BG-021",
    "REQ-SEC-BG-022",
    "REQ-SEC-BG-023",
    "REQ-SEC-BG-024",
    "REQ-SEC-BG-025",
    "REQ-SEC-BG-026",
    "REQ-SEC-BG-027",
    "REQ-SEC-BG-028",
    "REQ-SEC-BG-029",
    "REQ-SEC-BG-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DOC-011",
    "LOCK-DOC-013",
    "LOCK-DOC-019",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-020",
    "DOC-COMP-IDT-001",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-013",
    "DOC-SEC-015",
    "DOC-SEC-016"
  ],
  "tags": [
    "security",
    "break-glass",
    "emergency-authority",
    "privileged-operations",
    "recovery",
    "identity",
    "policy",
    "least-privilege",
    "time-bound",
    "receipts",
    "selective-audit",
    "offline",
    "closure",
    "recourse"
  ]
}
KOA:DOC-META:END -->

# Break-Glass Security

## 1. Purpose

This document defines the kOA break-glass security model.

Break-glass is a controlled emergency authority mechanism for exceptional situations in which ordinary operational paths cannot protect safety, availability, integrity, recovery, or another explicitly protected interest within the required time.

Break-glass is not a permanent administrator role.

It is a temporary state transition:

```text
bounded emergency condition
    → explicit request
    → identity and policy decision
    → narrowly scoped grant
    → visible controlled execution
    → automatic expiry or revocation
    → verified closure
    → mandatory evidence and review
```

The model ensures that emergency access remains:

- profile-enabled rather than globally assumed;
- purpose-bound;
- identity-bound;
- target-bound;
- time-bound;
- capability-bound;
- visible;
- revocable;
- receipted;
- reviewable;
- recoverable;
- compatible with offline operation where explicitly supported.

The model also preserves a central boundary:

```text
machine privilege is an execution mechanism
not the source of governance authority
```

Root or administrator access never becomes the ordinary governance API.

## 2. Scope

This document applies globally to the security model for any capability named or treated as break-glass.

The capability itself is active only where an applicable profile, component contract, and policy enable it.

Potential break-glass targets include:

- sovereign nodes;
- sovereign hubs;
- control-plane services;
- high-assurance overlays;
- recovery environments;
- identity and trust recovery;
- governance policy recovery;
- artifact activation recovery;
- backup and restore;
- critical service isolation;
- credential or trust-root revocation;
- data-protection actions;
- node-level privileged mutation;
- publication stop or containment;
- incident containment;
- emergency shutdown;
- forward repair.

The document applies to:

- request and approval;
- operator identity;
- separation of duties;
- grant creation;
- credential activation;
- privileged broker use;
- node-agent operations;
- recovery commands;
- component-owned emergency actions;
- data access;
- network access;
- status visibility;
- local receipt capture;
- expiry and revocation;
- closure;
- post-event review;
- correction and recourse.

It does not create a universal break-glass capability for every user, component, profile, or deployment.

It does not define one mandatory hardware token, number of approvers, session-recording product, privileged-access system, operating-system mechanism, or recovery shell. Those controls remain profile-specific or implementation-specific.

## 3. Canonical References

The canonical sources for this document are:

```text
generated/authority-manifest.json
generated/decision-index.json
contracts/system.contract.json#/operating_modes
contracts/system.contract.json#/component_boundaries
contracts/system.contract.json#/data_authority_and_ownership
contracts/system.contract.json#/receipts_and_critical_transitions
generated/component-catalog.json
generated/profile-catalog.json
contracts/components/identity-and-trust.component.json
contracts/components/governance-policy-runtime.component.json
contracts/components/audit-broker.component.json
contracts/components/koa-node-agent.component.json
contracts/artifact-contracts/decision-receipt.schema.json
contracts/artifact-contracts/policy-bundle.schema.json
generated/requirements-index.json
generated/assertion-index.json
generated/traceability.json
generated/test-catalog.json
generated/evidence-catalog.json
generated/exception-index.json
```

Their ownership roles are:

| Canonical source | Ownership |
| --- | --- |
| Profile contracts | Whether break-glass exists and the required assurance, approval, hardware, isolation, retention, and recovery controls |
| Governance Policy Runtime contract | Authorization, denial, indeterminate result, scope, expiry, revocation, and governed exceptions |
| Identity and Trust contract | Requester, approver, operator, observer, recovery identity, credential, trust, and revocation evidence |
| Component contracts | Emergency operations, target invariants, business authority, data ownership, failure behavior, and recovery |
| Node Agent contract | Bounded node and lifecycle operations where the component is the declared executor |
| Privileged broker design | Narrow execution of approved host mutations |
| Audit Broker contract | Receipt storage, verification, indexing, reconciliation, and selective disclosure |
| Decision-receipt contract | Machine-readable request, decision, execution, commit, rollback, and closure evidence |
| Policy-bundle contract | Versioned break-glass authorization and obligation rules |
| `requirements.registry.json` | Normative break-glass requirements |
| `locks.registry.json` | Profile, data, governance, lifecycle, ownership, and decision-closure invariants |
| `traceability.registry.json` | Requirement, profile, policy, component, test, and evidence relationships |
| `test-catalog.registry.json` | Activation, expiry, revocation, action, failure, closure, and offline tests |
| `evidence.registry.json` | Conformance and operational break-glass evidence |
| `exceptions.registry.json` | Bounded deviations that cannot create permanent or implicit emergency authority |

This document explains the model. It does not own the enabled profile list, exact approval count, privileged command catalog, or active policy values.

## 4. Model and Responsibilities

### 4.1 Eligibility

Break-glass eligibility requires all of the following:

```text
enabled profile capability
enabled target component or node capability
active break-glass policy
eligible requester identity
eligible approver or local authority path
eligible operator identity
verified receipt path
declared closure and recovery path
```

A missing element leaves the capability unavailable.

### 4.2 Valid emergency classes

A policy can define bounded emergency classes such as:

- imminent loss of service required for safety or sovereignty;
- active compromise containment;
- identity or trust recovery;
- revocation of a compromised credential or root;
- failure of an ordinary privileged workflow;
- failed activation requiring rollback or forward repair;
- unavailable ordinary recovery path;
- protection of data from imminent loss or unauthorized disclosure;
- isolation of a destructive or runaway service;
- recovery from a failed policy activation.

The active policy owns exact classes and evidence.

Break-glass is not justified by impatience, ordinary ticket delay, convenience, or desire to bypass a denied action.

### 4.3 Roles

The break-glass model distinguishes these roles:

| Role | Responsibility |
| --- | --- |
| Requester | Declares the emergency, purpose, target, scope, and expected closure |
| Approver | Evaluates emergency authority under the active policy |
| Operator | Performs only approved actions |
| Observer | Receives required visibility or monitors the active session |
| Target owner | Enforces component or node invariants |
| Closure authority | Verifies that temporary authority and effects are closed |
| Reviewer | Performs post-event review |
| Audit Broker | Stores and serves receipts without becoming the decision owner |

One identity can hold more than one role only when the active profile and policy explicitly permit it.

### 4.4 Request model

A break-glass request includes:

```text
request_id
requester_identity_ref
proposed_operator_identity_ref
emergency_class
reason
target_domain
target_component_or_node
tenant
environment
profile
requested_capabilities
requested_operations
requested_data_views
requested_network_destinations
requested_privilege
start_condition
requested_expiry
authority_refs
evidence_refs
expected_closure_condition
correlation_id
```

The request is not an active grant.

### 4.5 Decision model

The policy decision is one of:

```text
authorized
denied
indeterminate
```

An authorized decision contains:

- grant identity;
- operator identity;
- target;
- approved capabilities;
- approved operations;
- approved data views;
- privilege ceiling;
- network scope;
- validity;
- revocation conditions;
- approval identities;
- separation-of-duty result;
- required obligations;
- receipt classes;
- closure requirements.

An indeterminate result fails closed for activation.

### 4.6 Grant model

The grant is a temporary capability object.

It does not create a permanent role or group membership.

Grant scope can include:

| Scope dimension | Example |
| --- | --- |
| Target | One node, component, database, tenant, service, or recovery environment |
| Operations | Named privileged broker commands or component emergency operations |
| Data | Specific view classes rather than unrestricted source-table access |
| Privilege | Exact privilege ceiling |
| Network | Named destinations or no external network |
| Time | Not-before, maximum duration, hard expiry |
| Concurrency | One operator session or declared bound |
| Environment | Production, recovery, or another exact class |
| Profile | Exact primary profile and overlays |
| Evidence | Receipt, observer, recording, or review obligations |

### 4.7 Credential model

A break-glass grant can activate a temporary:

- capability token;
- short-lived certificate;
- broker session;
- node-agent authorization;
- recovery credential;
- database role;
- network rule;
- decryption capability;
- component emergency session.

Temporary credentials reference the grant and expire no later than the grant.

Long-lived shared emergency passwords are not the default architecture.

### 4.8 Lifecycle states

The lifecycle states are:

```text
requested
pending_approval
authorized
active
suspended
expired
revoked
closure_pending
closed
denied
failed
recovery_required
```

State changes are explicit and receipted where required.

### 4.9 Activation

Activation binds:

- the approved grant;
- the authenticated operator;
- target state;
- temporary credentials;
- policy version;
- profile;
- visibility indicators;
- receipt correlation;
- automatic expiry.

A partially activated grant is not active.

### 4.10 Action execution

Each action under an active grant follows:

```text
operator identity
    → active grant
    → target and operation match
    → expiry and revocation check
    → component or node owner validation
    → privileged execution if required
    → target effect validation
    → receipt
```

The executor remains the component or broker that owns the operation.

### 4.11 Privileged broker

A privileged broker exposes a narrow command catalog for host mutations.

Examples can include:

- isolate a service;
- stop or restart an approved unit;
- activate a recovery target;
- apply a bounded network containment rule;
- mount a verified recovery volume;
- rotate an approved credential;
- trigger a declared rollback;
- collect a restricted diagnostic package.

The broker does not expose general root authority when a bounded command exists.

### 4.12 Component emergency operations

A component can expose its own break-glass operations, such as:

- revoke a credential;
- disable an integration;
- stop a publication;
- freeze writes;
- activate read-only mode;
- rebuild a derived index;
- enter recovery;
- restore from a verified checkpoint.

The component owns validation and mutation of its authoritative state.

### 4.13 Visibility

Active break-glass state is visibly indicated through the applicable interface.

Visibility can include:

- local banner;
- operator console status;
- Ariane status;
- node status;
- observer notification;
- active grant identifier;
- target and expiry;
- reason class;
- closure status.

Visibility does not expose protected reason details to unauthorized viewers.

### 4.14 Receipt model

Receipt classes can include:

```text
request receipt
decision receipt
activation receipt
action-attempt receipt
action-effect receipt
denial receipt
suspension receipt
expiry receipt
revocation receipt
rollback or repair receipt
closure receipt
restricted-evidence-access receipt
post-review receipt
```

The receipt model distinguishes the decision from execution and the requested effect from authoritative commit.

### 4.15 Offline model

A sovereign-offline profile can support local break-glass when:

- signed local policy enables it;
- identities and credentials are locally verifiable;
- revocation state is within its freshness bound;
- reliable time or the approved alternative time model is available;
- local receipt storage is durable;
- target operations are locally executable;
- reconciliation is defined.

Network loss alone never activates break-glass.

### 4.16 Closure model

Closure verifies:

- no active sessions remain;
- temporary credentials are revoked or expired;
- temporary roles and network rules are removed;
- resource reservations are released;
- target state is known;
- rollback or repair is complete;
- pending receipts are durable;
- affected owners are notified;
- review is scheduled or complete;
- the grant is closed.

Closure is a state transition rather than an informal operator declaration.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-BG-001,REQ-SEC-BG-002,REQ-SEC-BG-003,REQ-SEC-BG-004,REQ-SEC-BG-005,REQ-SEC-BG-006,REQ-SEC-BG-007,REQ-SEC-BG-008,REQ-SEC-BG-009,REQ-SEC-BG-010,REQ-SEC-BG-011,REQ-SEC-BG-012,REQ-SEC-BG-013,REQ-SEC-BG-014,REQ-SEC-BG-015,REQ-SEC-BG-016,REQ-SEC-BG-017,REQ-SEC-BG-018,REQ-SEC-BG-019,REQ-SEC-BG-020,REQ-SEC-BG-021,REQ-SEC-BG-022,REQ-SEC-BG-023,REQ-SEC-BG-024,REQ-SEC-BG-025,REQ-SEC-BG-026,REQ-SEC-BG-027,REQ-SEC-BG-028,REQ-SEC-BG-029,REQ-SEC-BG-030 -->
- **REQ-SEC-BG-001 — SHALL:** Break-glass capability exist only where an active profile, component contract, and governance policy explicitly enable it for named emergency or recovery purposes.
- **REQ-SEC-BG-002 — SHALL NOT:** Break-glass be used for convenience, ordinary administration, planned maintenance, performance optimization, routine support, policy avoidance, or missing product functionality.
- **REQ-SEC-BG-003 — SHALL:** Every break-glass request identify the requester, proposed operator, target domain, target component or node, emergency condition, requested actions, data classes, affected subjects, capability scope, start condition, expiry, authority references, and expected closure condition.
- **REQ-SEC-BG-004 — SHALL:** The requester and operator use stable identities, fresh authentication, and the assurance level required by the active profile and policy.
- **REQ-SEC-BG-005 — SHALL:** Break-glass authorization be an explicit Governance Policy Runtime or profile-approved local policy decision with authorized, denied, or indeterminate result and stable reason code.
- **REQ-SEC-BG-006 — SHALL NOT:** Operating-system root, administrator membership, physical console access, possession of recovery media, network isolation, resource availability, or service ownership create break-glass authority.
- **REQ-SEC-BG-007 — SHALL:** Separation-of-duty requirements for request, approval, execution, observation, and closure be enforced exactly as declared by the active profile and policy.
- **REQ-SEC-BG-008 — SHALL:** Any profile-permitted single-operator emergency path be explicit, more narrowly scoped, shorter-lived, visibly marked, and subject to mandatory post-event review.
- **REQ-SEC-BG-009 — SHALL:** A break-glass grant identify its exact permitted commands or operation classes, target resources, tenant and environment, data views, privilege level, network destinations, concurrency, start time, expiry, revocation conditions, and receipt obligations.
- **REQ-SEC-BG-010 — SHALL NOT:** A break-glass grant provide unrestricted cross-tenant, cross-component, cross-environment, cross-profile, database-source-table, shell, network, publication, or external-integration access by default.
- **REQ-SEC-BG-011 — SHALL:** Privileged break-glass actions execute through the narrowest declared owner interface, privileged broker, node-agent operation, recovery command, or component contract capable of performing the approved action.
- **REQ-SEC-BG-012 — SHALL NOT:** Root access become the ordinary governance API or bypass the owning component's authoritative state transition when an approved bounded interface exists.
- **REQ-SEC-BG-013 — SHALL:** The break-glass lifecycle distinguish requested, pending_approval, authorized, active, suspended, expired, revoked, closure_pending, closed, denied, failed, and recovery_required states.
- **REQ-SEC-BG-014 — SHALL:** Activation be atomic with respect to the grant, credentials, policy state, visibility state, target capability, and initial receipt.
- **REQ-SEC-BG-015 — SHALL:** Break-glass state be visibly indicated to the active operator and relevant accountable observers for the full active interval.
- **REQ-SEC-BG-016 — SHALL:** Every protected action performed under break-glass revalidate grant state, identity, target, scope, expiry, revocation, operation class, and required component authority immediately before execution.
- **REQ-SEC-BG-017 — SHALL NOT:** A valid break-glass grant authorize an action outside its declared scope or convert external AI output, user preference, vote, recommendation, queue priority, or resource admission into machine privilege.
- **REQ-SEC-BG-018 — SHALL:** Break-glass credentials, tokens, sessions, capabilities, and temporary network or storage access expire or revoke automatically at the earliest applicable bound.
- **REQ-SEC-BG-019 — SHALL:** Every activation, denial, action attempt, successful action, failed action, scope change, suspension, expiry, revocation, credential event, rollback, recovery, and closure produce or reference a machine-readable receipt where required by the active policy.
- **REQ-SEC-BG-020 — SHALL:** Break-glass receipts distinguish request, decision, execution, target effect, authoritative commit, rollback or repair, expiry or revocation, and closure truthfully.
- **REQ-SEC-BG-021 — SHALL:** Receipts, logs, diagnostics, status views, and review packages use selective disclosure and exclude passwords, private keys, secret tokens, recovery secrets, unrestricted personal data, protected cultural content, and unnecessary payloads.
- **REQ-SEC-BG-022 — SHALL:** Critical break-glass evidence remain durably capturable locally during network failure and reconcile with the Audit Broker after connectivity returns.
- **REQ-SEC-BG-023 — SHALL:** Offline break-glass decisions use the last valid signed local identity, trust, policy, profile, revocation, and time state within declared freshness bounds.
- **REQ-SEC-BG-024 — SHALL NOT:** Loss of connectivity, unavailable remote approver, stale policy, failed time source, missing receipt path, or indeterminate identity silently broaden break-glass authority.
- **REQ-SEC-BG-025 — SHALL:** Closure revoke temporary authority, terminate sessions, remove temporary credentials and access paths, release reservations, validate target state, preserve evidence, and record the final outcome.
- **REQ-SEC-BG-026 — SHALL:** Post-event review evaluate necessity, scope, actions, data accessed, target effects, policy decisions, failures, credentials, receipts, follow-up repair, and prevention of recurrence.
- **REQ-SEC-BG-027 — SHALL:** Break-glass recovery and rollback preserve component data ownership, tenant boundaries, trust scope, authoritative-state truth, and the distinction between executable rollback and data restoration.
- **REQ-SEC-BG-028 — SHALL:** A break-glass failure degrade only the affected emergency capability, fail closed for missing authority, preserve independently valid ordinary capabilities, and expose stable machine-readable status.
- **REQ-SEC-BG-029 — SHALL:** Users, subjects, communities, operators, and authorized representatives receive notice, explanation, correction, challenge, and recourse paths when break-glass activity materially affects their data, rights, service, or authority and the active policy permits disclosure.
- **REQ-SEC-BG-030 — SHALL:** Profile-specific approval count, hardware token, console, recovery target, privileged broker, session-recording, network isolation, retention, and response-time controls remain explicit and cannot become global break-glass requirements through repetition.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Request

A request follows this sequence:

1. authenticate the requester;
2. select an active emergency class;
3. identify the target and owner;
4. declare requested operations, data, privilege, network, and duration;
5. declare expected closure;
6. attach available evidence;
7. validate profile eligibility;
8. create the request receipt;
9. enter `pending_approval`.

An invalid or ineligible request enters `denied`.

### 6.2 Approval

Approval:

1. authenticates the approver or resolves the approved local authority path;
2. loads the active policy and profile;
3. evaluates emergency class and evidence;
4. evaluates separation of duties;
5. minimizes capability, target, data, privilege, network, and duration;
6. defines obligations and closure;
7. returns authorized, denied, or indeterminate;
8. creates the decision receipt.

A denial or indeterminate decision does not activate temporary credentials.

### 6.3 Grant activation

Activation:

1. reauthenticates the operator;
2. verifies operator eligibility;
3. verifies the approved grant and current policy;
4. verifies target identity and state;
5. creates temporary credentials and access paths;
6. enables visibility and observer obligations;
7. starts expiry enforcement;
8. creates the activation receipt;
9. enters `active` atomically.

A failure revokes partial credentials and enters `failed` or `recovery_required`.

### 6.4 Action execution

For every action:

1. resolve the active grant;
2. verify identity, target, operation, data view, privilege, network, time, and revocation;
3. evaluate any action-specific component authority;
4. invoke the narrow owner interface or broker command;
5. capture the execution result;
6. verify the authoritative target effect;
7. emit action and effect receipts;
8. update visible status.

A command execution success without target-effect verification remains incomplete.

### 6.5 Scope change

A scope change:

1. creates a new request linked to the active grant;
2. reevaluates policy and separation of duties;
3. records denial or authorization;
4. activates the amended grant atomically;
5. revokes replaced capabilities;
6. preserves the original receipts.

Scope does not expand through operator choice.

### 6.6 Suspension

Suspension:

1. blocks new actions;
2. preserves active evidence;
3. leaves target state unchanged unless containment requires a declared action;
4. evaluates whether to resume, revoke, expire, or recover;
5. records the suspension result.

### 6.7 Expiry

Expiry:

1. stops new actions at the hard expiry;
2. invalidates temporary credentials and sessions;
3. removes temporary access paths;
4. marks pending operations cancelled or failed as appropriate;
5. verifies target state;
6. enters `closure_pending`;
7. records expiry.

Expiry does not wait for operator logout.

### 6.8 Revocation

Revocation:

1. validates the revoking authority;
2. blocks new actions immediately;
3. terminates or isolates active sessions;
4. invalidates credentials;
5. removes temporary network, storage, and privilege paths;
6. validates target state;
7. enters `closure_pending` or `recovery_required`;
8. records revocation.

### 6.9 Rollback or forward repair

When an action causes an invalid state:

1. isolate the affected target;
2. preserve evidence;
3. select the owner-approved rollback or repair path;
4. verify artifact, checkpoint, trust, and compatibility;
5. apply the bounded transition;
6. validate authoritative state;
7. record rollback or repair;
8. continue closure.

Data restoration follows the owning data contract.

### 6.10 Closure

Closure:

1. verify grant expiry or revocation;
2. verify session termination;
3. verify credential removal;
4. verify temporary access-path removal;
5. verify target state and outstanding work;
6. reconcile receipts;
7. record affected data and actions;
8. create the closure receipt;
9. enter `closed`.

### 6.11 Post-event review

Review:

1. validates the emergency justification;
2. compares requested, approved, and executed scope;
3. examines all actions and target effects;
4. examines data and evidence access;
5. examines failures, retries, rollback, and repair;
6. examines credentials and residual access;
7. identifies policy, component, operational, or product changes;
8. assigns follow-up owners;
9. records the review outcome;
10. closes remaining remediation.

### 6.12 Offline reconciliation

After connectivity returns:

1. preserve local receipt ordering;
2. verify local receipt integrity;
3. submit receipts to the Audit Broker;
4. reconcile policy, identity, revocation, and time state;
5. identify any conflict;
6. enter review or recovery for inconsistent state;
7. preserve local evidence;
8. record reconciliation.

## 7. Failure States and Safe Degradation

| Failure code | Condition | Protected result | Safe degraded result |
| --- | --- | --- | --- |
| `break_glass_not_enabled` | Active profile or target does not enable the capability | Request is denied | Ordinary support or recovery path |
| `break_glass_emergency_class_invalid` | Request does not match an active emergency class | Request is denied | Planned operational workflow |
| `break_glass_request_incomplete` | Target, scope, duration, authority, or closure is missing | Request is denied | Repair the request |
| `break_glass_requester_identity_failed` | Requester identity is not established | Request is denied | Existing ordinary capabilities continue |
| `break_glass_operator_identity_failed` | Operator identity or assurance is invalid | Activation is denied | Select an eligible operator |
| `break_glass_approver_unavailable` | Required approval path is unavailable | Activation is denied unless an explicit local policy path applies | Preserve current state |
| `break_glass_policy_indeterminate` | Policy cannot return an authoritative decision | Activation is denied | Recovery without protected mutation where possible |
| `break_glass_separation_of_duty_failed` | Required roles are not independently satisfied | Activation is denied | Use the required role set |
| `break_glass_scope_too_broad` | Requested grant exceeds policy bounds | Broad grant is denied | Authorize a narrower grant |
| `break_glass_target_mismatch` | Action target differs from the grant | Action is denied | Use the approved target |
| `break_glass_operation_not_authorized` | Operation class is outside the grant | Action is denied | Request an amended grant |
| `break_glass_data_view_not_authorized` | Requested data exceeds the approved view | Access is denied | Use the minimized view |
| `break_glass_privilege_ceiling_exceeded` | Required privilege exceeds the grant | Action is denied | Use a bounded command or new decision |
| `break_glass_direct_source_write_attempt` | Operator attempts direct mutation of another component's source store | Write is denied | Use the owner component interface |
| `break_glass_broker_command_unavailable` | Approved bounded command cannot execute | Action fails safely | Use recovery or approved repair |
| `break_glass_activation_partial` | Credentials or visibility activate without complete grant commit | Partial access is revoked | Retry from inactive state |
| `break_glass_expired` | Grant or credential reaches hard expiry | New actions stop | Closure begins automatically |
| `break_glass_revoked` | Grant is revoked | Sessions and access are terminated | Closure or recovery |
| `break_glass_time_state_invalid` | Reliable time or approved alternative is unavailable | Time-bound activation is denied | Preserve existing protected state |
| `break_glass_receipt_path_unavailable` | Required durable local or central receipt path is unavailable | Critical activation or action is blocked | Non-mutating diagnosis where permitted |
| `break_glass_target_effect_unknown` | Execution returns but authoritative target effect is unknown | Success is not reported | Reconcile or recover |
| `break_glass_closure_partial` | Temporary credentials, sessions, or access paths remain | Grant remains closure-pending | Complete cleanup under recovery |
| `break_glass_offline_reconciliation_failed` | Local and connected authority state conflict | Grant remains closed and target enters review | Preserve evidence and repair |
| `break_glass_status_ambiguous` | Active, expired, revoked, or closed state cannot be reported truthfully | New actions are blocked | Restore authoritative status state |

Failure remains scoped to the affected emergency capability. Ordinary independently authorized functions continue. A failed break-glass activation never creates a fallback root shell automatically.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust establishes requester, approver, operator, observer, reviewer, and recovery identities.

It issues or validates temporary credentials and revocation state without deciding the target action.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates whether the emergency grant is authorized, denied, or indeterminate.

It owns grant scope and obligations where the profile deploys it. It does not execute host commands or mutate component data.

### 8.3 Privileged broker

The privileged broker executes only named host operations under an active grant.

It validates correlation and grant state for each command and returns the actual execution result.

### 8.4 Node Agent

The Node Agent can coordinate declared node lifecycle, isolation, recovery, rollback, or service operations.

It does not treat node administration identity as component business authority.

### 8.5 Owning components

Each target component validates its emergency operation and owns its data mutation.

Break-glass does not transfer its authoritative source-table ownership to the operator or broker.

### 8.6 Resource Governor

Resource Governor can reserve bounded capacity for emergency action, evidence capture, rollback, or recovery.

Resource admission does not authorize the action.

### 8.7 Audit Broker

Audit Broker stores and verifies break-glass receipts and produces selective evidence views.

It does not approve the grant or become the source of the target state.

### 8.8 Ariane and operator interfaces

Ariane or another approved operator interface can display active state, target, expiry, reason class, and closure status.

Interface availability does not create authority.

### 8.9 Backup and recovery

Backup and recovery services provide verified checkpoints and restoration procedures.

The active grant identifies exactly which recovery actions are authorized. Restore activation follows the owning lifecycle and data contracts.

### 8.10 External integrations and AI

External integrations can be disabled or isolated through approved emergency actions.

External AI output, voice intent, vote, recommendation, or enrichment does not authorize break-glass activation or machine privilege.

## 9. Decision Closure and Prohibited Assumptions

This document closes the break-glass interpretation as follows:

- break-glass is conditional, not a global baseline entitlement;
- emergency authority is policy-derived;
- root is not the governance API;
- profiles own exact assurance and approval controls;
- grants are temporary capability objects rather than permanent roles;
- scope includes target, action, data, privilege, network, time, and evidence;
- activation is atomic;
- every action revalidates the grant;
- the target owner retains authoritative-state control;
- visibility persists throughout the active interval;
- expiry and revocation terminate access automatically;
- receipts distinguish request, decision, execution, effect, commit, and closure;
- offline use requires signed local authority and durable evidence;
- closure removes temporary authority;
- post-event review is mandatory;
- recourse applies where material effects and policy permit it.

The following assumptions are prohibited:

- an emergency declaration creates authority;
- root or administrator membership is a break-glass grant;
- physical console access is approval;
- network failure permits wider access;
- unavailable approvers permit self-authorization automatically;
- available resources authorize privileged work;
- an approved grant permits any command;
- a database administrator owns component records;
- a vote or recommendation can trigger machine privilege;
- external AI can approve or execute emergency authority;
- a successful command proves the target effect;
- session logout is sufficient closure;
- expiry can be extended silently;
- receipts can be omitted during offline operation;
- a recovery shell can become an unrestricted ordinary interface;
- profile-specific two-person control is universal;
- post-event review can rewrite historical receipts.

A new global emergency class, permanent emergency role, implicit activation path, authority-merging rule, or unrestricted privileged interface requires an accepted owner decision and complete impact validation.

## 10. Validation Criteria

This document is conformant when all of the following checks pass:

1. the metadata block is first, valid, and declares status `active`;
2. the document contains the required 11 normative sections;
3. all 30 requirement identifiers are unique and registered;
4. every declared decision is accepted;
5. every declared lock exists and is active;
6. every enabled profile declares break-glass capability, eligible targets, assurance, roles, approval path, maximum duration, receipt path, and closure behavior;
7. disabled profiles reject activation;
8. request tests cover identity, emergency class, target, scope, data, privilege, network, duration, authority, evidence, and closure;
9. policy tests cover authorized, denied, and indeterminate outcomes;
10. tests prove that root, console, network failure, resources, and service ownership do not create authority;
11. separation-of-duty tests follow the active profile rather than a global assumption;
12. grant tests validate operation, target, tenant, environment, data view, privilege, network, time, revocation, and evidence bounds;
13. activation tests prove atomic grant, credential, visibility, expiry, and receipt state;
14. action tests revalidate grant state before every protected operation;
15. broker tests reject undeclared commands and general root fallback;
16. component tests reject direct source-table mutation;
17. tests prove that votes, preferences, recommendations, external AI, and resource decisions cannot create machine privilege;
18. visibility tests cover the full active interval;
19. expiry tests terminate sessions and credentials automatically;
20. revocation tests terminate new and active use according to policy;
21. receipt tests cover request, decision, activation, action, effect, denial, failure, expiry, revocation, rollback, recovery, and closure;
22. selective-disclosure tests exclude secrets and unnecessary protected data;
23. offline tests cover local policy, identity, trust, revocation, time, durable receipts, no authority expansion, and reconciliation;
24. target-effect tests reject false success;
25. closure tests remove sessions, credentials, roles, network paths, storage paths, and resource reservations;
26. rollback and repair tests preserve data ownership and authoritative-state truth;
27. review tests compare requested, approved, and executed scope;
28. recourse tests cover notice, explanation, correction, challenge, and accountable owner where applicable;
29. profile tests keep approval count, hardware token, console, recovery target, broker, session recording, network isolation, retention, and timing controls profile-scoped;
30. no unresolved-authority marker, duplicate identifier, or unregistered normative statement exists;
31. active prose is English;
32. ordinary Markdown validation does not depend on file-content hashes.

Expected validator failure codes include:

```text
break_glass_not_enabled
break_glass_emergency_class_invalid
break_glass_request_incomplete
break_glass_requester_identity_failed
break_glass_operator_identity_failed
break_glass_approver_unavailable
break_glass_policy_indeterminate
break_glass_separation_of_duty_failed
break_glass_scope_too_broad
break_glass_target_mismatch
break_glass_operation_not_authorized
break_glass_data_view_not_authorized
break_glass_privilege_ceiling_exceeded
break_glass_direct_source_write_attempt
break_glass_broker_command_unavailable
break_glass_activation_partial
break_glass_expired
break_glass_revoked
break_glass_time_state_invalid
break_glass_receipt_path_unavailable
break_glass_target_effect_unknown
break_glass_closure_partial
break_glass_offline_reconciliation_failed
break_glass_status_ambiguous
```

## 11. Non-Normative Examples

### 11.1 Compromised service credential

A sovereign operator requests authority to revoke one compromised service credential. The grant targets Identity and Trust, permits one revocation operation, expires in fifteen minutes, and requires activation, action, effect, and closure receipts. It does not grant database or shell access.

### 11.2 Failed system activation

A node cannot complete a system activation and the ordinary rollback interface is unavailable. A verified recovery operator receives a grant for the node agent's named recovery command. The command activates a retained recovery target and records the actual boot result.

### 11.3 Offline sovereign node

A sovereign-offline node loses network connectivity during an incident. Signed local policy permits one locally approved containment operation with a short duration and durable local receipts. The outage does not grant general administrator access. Receipts reconcile after connectivity returns.

### 11.4 Denied convenience request

An operator requests break-glass to bypass a slow planned maintenance approval. The emergency class does not apply. The request is denied and the ordinary maintenance workflow remains the correct path.

### 11.5 Partial closure

An emergency session expires, but one temporary network rule remains. The grant enters `closure_pending`, not `closed`. Recovery removes the rule, validates the target, and creates the final closure receipt.
