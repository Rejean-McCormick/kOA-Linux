<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-006",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "component",
    "global"
  ],
  "component_id": "koa_node_agent",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/security_model",
    "contracts/system.contract.json#/lifecycle_model",
    "generated/component-catalog.json#/components/koa_node_agent",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/component-catalog.json#/components/audit_broker",
    "contracts/components/koa-node-agent.component.json",
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
    "DEC-SEC-BROKER-001",
    "DEC-SEC-PRIV-001",
    "DEC-COMP-NODE-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-LIFE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-SEC-BROKER-001",
    "REQ-SEC-BROKER-002",
    "REQ-SEC-BROKER-003",
    "REQ-SEC-BROKER-004",
    "REQ-SEC-BROKER-005",
    "REQ-SEC-BROKER-006",
    "REQ-SEC-BROKER-007",
    "REQ-SEC-BROKER-008",
    "REQ-SEC-BROKER-009",
    "REQ-SEC-BROKER-010",
    "REQ-SEC-BROKER-011",
    "REQ-SEC-BROKER-012",
    "REQ-SEC-BROKER-013",
    "REQ-SEC-BROKER-014",
    "REQ-SEC-BROKER-015",
    "REQ-SEC-BROKER-016",
    "REQ-SEC-BROKER-017",
    "REQ-SEC-BROKER-018",
    "REQ-SEC-BROKER-019",
    "REQ-SEC-BROKER-020",
    "REQ-SEC-BROKER-021",
    "REQ-SEC-BROKER-022",
    "REQ-SEC-BROKER-023",
    "REQ-SEC-BROKER-024",
    "REQ-SEC-BROKER-025",
    "REQ-SEC-BROKER-026",
    "REQ-SEC-BROKER-027",
    "REQ-SEC-BROKER-028",
    "REQ-SEC-BROKER-029",
    "REQ-SEC-BROKER-030",
    "REQ-SEC-BROKER-031",
    "REQ-SEC-BROKER-032",
    "REQ-SEC-BROKER-033",
    "REQ-SEC-BROKER-034",
    "REQ-SEC-BROKER-035",
    "REQ-SEC-BROKER-036",
    "REQ-SEC-BROKER-037",
    "REQ-SEC-BROKER-038",
    "REQ-SEC-BROKER-039",
    "REQ-SEC-BROKER-040"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-GATE-001"
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
    "DOC-DEV-000",
    "DOC-LIFE-003",
    "DOC-LIFE-013",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005"
  ],
  "tags": [
    "privileged-broker",
    "koa-node-agent",
    "closed-operations",
    "local-interface",
    "admission",
    "idempotency",
    "atomicity",
    "journaling",
    "receipts",
    "recovery",
    "break-glass",
    "offline-security",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Privileged Broker

## 1. Purpose

This document defines the security and operational model of the kOA privileged broker.

The privileged broker is the narrow execution boundary between unprivileged components and protected host effects. Its canonical implementation identity is kOA Node Agent where the active component contract assigns that role.

The broker exists to replace broad administrator interfaces with a closed operation model. A caller does not request a shell, a package command, a service-manager command, a path mutation, or a device action. It requests one registered semantic operation with bounded parameters, an explicit target, a valid authority decision, expected state, an idempotency identity, a deadline, and a declared recovery path.

The broker executes. It does not decide identity, policy, resource policy, release compatibility, component data semantics, publication authority, consent, cultural rights, or external-provider trust.

## 2. Scope

This document applies globally to:

- kOA Node Agent as the ordinary privileged broker;
- local broker transports;
- privileged operation registration;
- request admission;
- identity and authorization binding;
- expected-state verification;
- resource admission;
- fixed privileged adapters;
- transaction journals;
- idempotency and replay;
- atomic commit;
- rollback, compensation, forward repair, and recovery;
- operation receipts;
- service hardening;
- break-glass separation;
- offline broker operation;
- profile-specific privilege;
- privileged-broker testing and evidence.

The broker can execute registered operations for:

- protected state inspection;
- Release Set staging, activation, rollback, and repair;
- protected artifact lifecycle;
- service-group lifecycle;
- encrypted volume lifecycle;
- network-policy activation;
- host configuration;
- node-scoped key transitions;
- boot and recovery transitions;
- controlled import and evidence export.

The exact active operation inventory remains canonical in the kOA Node Agent component contract.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Broker component identity | `generated/component-catalog.json#/components/koa_node_agent` |
| Active broker operation contract | `contracts/components/koa-node-agent.component.json` |
| Global privilege model | `07-security/05-privilege-boundaries.md` |
| User, service, node, artifact, signer, key, device, and trust identity | Identity and Trust component contract |
| Privilege authorization and obligations | Governance Policy Runtime component contract |
| Resource admission and pressure enforcement | Resource Governor component contract |
| Receipt storage and protected evidence | Audit Broker component contract |
| Release compatibility and Release Sets | `contracts/release-channels.contract.json` |
| Artifact identity, integrity, and lifecycle | `contracts/artifact-classes.contract.json` |
| Profile-specific privilege and offline behavior | `contracts/profiles/*.profile.json` |
| External and offline boundaries | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file privilege and lifecycle invariants | `generated/assertion-index.json` |
| Operation, profile, test, receipt, and evidence links | `generated/traceability.json` |
| Broker and security tests | `generated/test-catalog.json` |
| Current broker evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted broker decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

This document explains the broker contract. It does not replace the machine-readable operation inventory.

## 4. Broker Model and Responsibilities

### 4.1 Broker identity

The ordinary broker component identity is:

```text
koa_node_agent
```

Its component class is `privileged_broker`. Its authority class is `authoritative_executor`.

The broker is authoritative for:

- privileged request identity;
- request-body and idempotency binding;
- operation state;
- transaction journals;
- observed before and after state;
- operation result;
- broker-local quarantine state;
- local operation receipt before Audit Broker acceptance;
- crash-recovery classification.

### 4.2 Responsibilities owned elsewhere

| Responsibility | Owner |
| --- | --- |
| User and service identity | Identity and Trust |
| Artifact, signer, key, and trust identity | Identity and Trust |
| Operation authorization and obligations | Governance Policy Runtime or another registered authority |
| Resource admission | Resource Governor |
| Critical audit record storage | Audit Broker |
| Release compatibility | Release-channel authority |
| Component business-state transition | Owning component |
| Publication authority | Publication Gateway and applicable policy authority |
| UCKK dimension admission | UCKK Platform and UCKK Dimension Gateway |
| Profile eligibility | Active profile contract |

The broker validates references to these authorities but does not replace them.

### 4.3 Closed operation model

Every operation declares:

```text
operation_id
operation_class
purpose
authority_effect
privilege_effect
request_contract_ref
result_contract_ref
receipt_contract_ref
allowed_parameters
required_artifacts
preconditions
timeout_seconds
offline_behavior
replay_behavior
rollback_or_recovery_behavior
```

An operation is unavailable when its active contract is missing, invalid, incompatible, revoked, or outside the profile.

### 4.4 Prohibited interfaces

The broker has no ordinary interface for:

- arbitrary commands;
- arbitrary shell fragments;
- arbitrary scripts;
- arbitrary package names;
- arbitrary service units;
- arbitrary container images or arguments;
- arbitrary filesystem paths;
- arbitrary device nodes;
- arbitrary network rules;
- arbitrary kernel settings;
- arbitrary boot entries;
- arbitrary key material;
- raw private-key export.

A new semantic effect requires a new registered operation.

### 4.5 Fixed adapters

Each operation maps to one fixed adapter implementation or one explicitly versioned compatible adapter family.

An adapter declares:

- adapter identity and version;
- operation identities implemented;
- target platform and profile;
- exact privilege needs;
- input schema;
- output schema;
- expected-state model;
- commit boundary;
- rollback or recovery behavior;
- tests and evidence.

Adapter selection is deterministic from the active profile and contract.

### 4.6 Local interface

The default ordinary interface is a local Unix-domain socket or validated platform equivalent.

The interface authenticates:

- transport peer;
- service identity;
- requesting subject or delegated authority;
- active contract version.

The interface exposes no public network listener.

### 4.7 Service hardening

The broker service runs with:

- a dedicated service identity;
- a closed capability bounding set;
- empty ambient capabilities;
- no-new-privileges enforcement;
- private temporary storage;
- protected system and home paths;
- bounded readable and writable paths;
- system-call filtering;
- address-family restrictions;
- device allowlists;
- cgroup or equivalent resource controls;
- profile-specific mandatory access control where available.

Hardening evidence maps each granted privilege to an active operation.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-BROKER-001,REQ-SEC-BROKER-002,REQ-SEC-BROKER-003,REQ-SEC-BROKER-004,REQ-SEC-BROKER-005,REQ-SEC-BROKER-006,REQ-SEC-BROKER-007,REQ-SEC-BROKER-008,REQ-SEC-BROKER-009,REQ-SEC-BROKER-010,REQ-SEC-BROKER-011,REQ-SEC-BROKER-012,REQ-SEC-BROKER-013,REQ-SEC-BROKER-014,REQ-SEC-BROKER-015,REQ-SEC-BROKER-016,REQ-SEC-BROKER-017,REQ-SEC-BROKER-018,REQ-SEC-BROKER-019,REQ-SEC-BROKER-020,REQ-SEC-BROKER-021,REQ-SEC-BROKER-022,REQ-SEC-BROKER-023,REQ-SEC-BROKER-024,REQ-SEC-BROKER-025,REQ-SEC-BROKER-026,REQ-SEC-BROKER-027,REQ-SEC-BROKER-028,REQ-SEC-BROKER-029,REQ-SEC-BROKER-030,REQ-SEC-BROKER-031,REQ-SEC-BROKER-032,REQ-SEC-BROKER-033,REQ-SEC-BROKER-034,REQ-SEC-BROKER-035,REQ-SEC-BROKER-036,REQ-SEC-BROKER-037,REQ-SEC-BROKER-038,REQ-SEC-BROKER-039,REQ-SEC-BROKER-040 -->
- **REQ-SEC-BROKER-001 — SHALL:** kOA Node Agent operate as the sole ordinary narrow privileged broker for registered host-level node operations where its active component contract applies.
- **REQ-SEC-BROKER-002 — SHALL NOT:** The broker expose a generic shell, command runner, package-manager interface, arbitrary service controller, arbitrary container runner, arbitrary filesystem writer, unrestricted device interface, or raw private-key export.
- **REQ-SEC-BROKER-003 — SHALL:** Every active broker operation have a stable operation identifier, operation class, purpose, authority effect, privilege effect, request contract, result contract, receipt contract, timeout, replay behavior, and offline behavior.
- **REQ-SEC-BROKER-004 — SHALL:** Every broker request use a closed schema and reject unknown fields, unknown operations, unknown parameters, incompatible contract versions, and values outside the selected operation's allowlist.
- **REQ-SEC-BROKER-005 — SHALL:** Every request identify the caller, service identity, profile, authority scope, target, policy decision, expected state, parameters, correlation identity, request time, deadline, and idempotency identity.
- **REQ-SEC-BROKER-006 — SHALL:** One idempotency identity bind to one canonical request body and return the recorded or equivalent result for an authorized replay.
- **REQ-SEC-BROKER-007 — SHALL NOT:** Reuse of an idempotency identity with a different canonical request body be accepted.
- **REQ-SEC-BROKER-008 — SHALL:** The broker verify local transport peer credentials, service identity, caller identity, policy decision, target scope, profile, expiry, obligations, expected state, artifact trust, resource admission, and recovery readiness before privileged mutation.
- **REQ-SEC-BROKER-009 — SHALL:** Time-sensitive identity, authorization, trust, revocation, expected-state, and resource inputs be revalidated immediately before the authoritative commit.
- **REQ-SEC-BROKER-010 — SHALL NOT:** Root identity, administrator identity, socket access, local process ownership, successful authentication, or possession of an artifact substitute for authorization.
- **REQ-SEC-BROKER-011 — SHALL:** The broker use local transport by default and expose no public or undeclared network listener.
- **REQ-SEC-BROKER-012 — SHALL:** Every ordinary broker endpoint enforce peer identity, service identity, request-size limits, queue bounds, rate limits, deadlines, compatibility checks, and fail-closed behavior.
- **REQ-SEC-BROKER-013 — SHALL:** The broker execute each privileged effect through one fixed registered adapter with bounded inputs and a declared target domain.
- **REQ-SEC-BROKER-014 — SHALL NOT:** An adapter interpret user-supplied shell fragments, arbitrary paths, arbitrary service names, arbitrary package names, arbitrary image arguments, arbitrary devices, or undeclared network rules.
- **REQ-SEC-BROKER-015 — SHALL:** The broker maintain a durable privileged-operation ledger binding request identity, canonical body, state, result, receipt, and replay status.
- **REQ-SEC-BROKER-016 — SHALL:** The broker maintain durable transaction journals for activation, rollback, configuration, storage, network, key, boot, and recovery operations whose effects can outlive the process.
- **REQ-SEC-BROKER-017 — SHALL:** Every material privileged step record before state, intended effect, commit boundary, observed after state, and compensating or recovery action.
- **REQ-SEC-BROKER-018 — SHALL:** Authoritative privileged effects use atomic commit or a validated equivalent that leaves either the previous valid state or the complete new valid state after interruption.
- **REQ-SEC-BROKER-019 — SHALL NOT:** A partial effect, adapter return code, service restart, file copy, package installation, image pull, or provider acknowledgement be reported as completed authority.
- **REQ-SEC-BROKER-020 — SHALL:** Completion require the privileged effect to be committed, actual after state to be verified, and the operation receipt to be durable.
- **REQ-SEC-BROKER-021 — SHALL:** Every operation define pre-commit cancellation and post-commit rollback, compensation, forward-repair, or recovery behavior.
- **REQ-SEC-BROKER-022 — SHALL:** An operation whose prior effect is unknown enter recovery-required state and block blind replay until actual state is reconciled.
- **REQ-SEC-BROKER-023 — SHALL:** Conflicting operations serialize within their target scope, including release activation, rollback, key rotation, network-policy activation, storage transitions, boot changes, and recovery transitions.
- **REQ-SEC-BROKER-024 — SHALL:** Non-conflicting operations remain bounded by per-class concurrency, queue, timeout, and resource limits.
- **REQ-SEC-BROKER-025 — SHALL:** Resource Governor admit resource-affecting operations and protect journals, receipts, active artifacts, last-known-good state, recovery material, and critical services under pressure.
- **REQ-SEC-BROKER-026 — SHALL NOT:** The broker or Resource Governor infer authorization, consent, disclosure, publication, cultural rights, release compatibility, or governance policy from resource state.
- **REQ-SEC-BROKER-027 — SHALL:** Identity and Trust remain authoritative for caller, service, node, artifact, signer, key, device, trust, and revocation state.
- **REQ-SEC-BROKER-028 — SHALL:** Governance Policy Runtime or another registered authority remain authoritative for operation permission, scope, expiry, obligations, and break-glass authorization.
- **REQ-SEC-BROKER-029 — SHALL NOT:** The broker write directly to another component's authoritative business store or reinterpret another component's data, migration, consent, policy, publication, or lifecycle decision.
- **REQ-SEC-BROKER-030 — SHALL:** Every operation produce a durable critical-transition receipt containing operation, request, caller, authority, profile, target, before state, after state, artifacts, result, reason codes, timing, correlation, and recovery references.
- **REQ-SEC-BROKER-031 — SHALL:** Audit Broker receive operation receipts through durable idempotent delivery while local receipt storage remains authoritative until delivery is accepted.
- **REQ-SEC-BROKER-032 — SHALL NOT:** Requests, journals, logs, metrics, traces, receipts, or evidence contain secret values, raw private keys, unrestricted sensitive payloads, or another component's copied credentials.
- **REQ-SEC-BROKER-033 — SHALL:** The broker service identity use only the operating-system capabilities, system calls, address families, devices, readable paths, writable paths, and service-manager controls required by the active operation set.
- **REQ-SEC-BROKER-034 — SHALL:** The broker use dedicated service identity, private temporary storage, protected system and home paths, no-new-privileges enforcement, bounded writable paths, capability bounding, system-call filtering, and resource controls where supported.
- **REQ-SEC-BROKER-035 — SHALL:** Break-glass operations use a separate operation namespace, stronger authentication, explicit human authority, bounded scope and duration, enhanced evidence, and post-event review.
- **REQ-SEC-BROKER-036 — SHALL NOT:** Urgency, outage severity, disconnected state, local ownership, automation, AI output, or operator status imply break-glass authority.
- **REQ-SEC-BROKER-037 — SHALL:** The broker remain locally operable offline when the active profile provides valid local identity, authorization, trust, artifact, audit, resource, and recovery inputs.
- **REQ-SEC-BROKER-038 — SHALL:** Offline import, activation, key, trust, network, storage, boot, and recovery operations apply the same identity, authorization, integrity, compatibility, replay, atomicity, receipt, and recovery controls as connected operations.
- **REQ-SEC-BROKER-039 — SHALL:** External integrations and external AI surfaces produce only registered candidate, artifact, request, or decision inputs and have no direct broker or host-privilege channel.
- **REQ-SEC-BROKER-040 — SHALL:** Privileged-broker conformance include operation closure, interface locality, identity and policy separation, adapter bounds, journaling, expected-state checks, idempotency, atomicity, recovery, receipt durability, hardening, break-glass separation, offline execution, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Request Admission and Execution

### 6.1 Request envelope

A broker request includes:

```text
operation
request_id
idempotency_id
caller_identity_ref
service_identity_ref
profile_ref
authority_scope_ref
target_ref
policy_decision_ref
expected_state
parameters
artifact_refs
resource_admission_ref
correlation_id
requested_at
deadline_at
```

Operation-specific schemas can require additional canonical references. Unknown fields are rejected.

### 6.2 Admission states

Admission proceeds through:

```text
received
transport_peer_verified
service_identity_verified
caller_identity_verified
schema_verified
operation_verified
profile_verified
scope_verified
authorization_verified
expected_state_verified
artifact_and_trust_verified
resource_admitted
accepted
```

A failed stage produces an explicit blocked or rejected result before privileged mutation.

### 6.3 Authorization verification

Authorization verification confirms:

- decision type;
- operation identity;
- target identity;
- profile;
- authority scope;
- requesting identity;
- delegated identity where applicable;
- issue and expiry time;
- revocation state;
- obligations;
- break-glass status.

The broker enforces obligations that apply to execution, receipt creation, target handling, or recovery.

### 6.4 Expected-state verification

Expected state protects against stale or conflicting requests.

Applicable values include:

- active Release Set;
- active artifact;
- configuration version;
- service health state;
- volume state;
- key generation;
- network-policy identity;
- boot or recovery state.

The broker checks expected state before mutation and before authoritative commit.

### 6.5 Artifact verification

Artifact-backed operations verify:

- artifact identity;
- artifact class;
- manifest;
- signature and signer trust where applicable;
- functional integrity;
- compatibility;
- revocation;
- target profile;
- rollback or repair material.

Artifact presence is not activation authority.

### 6.6 Resource admission

The Resource Governor evaluates:

- CPU;
- memory;
- storage;
- I/O;
- network;
- device;
- concurrency;
- recovery reserve.

A denied admission blocks or defers the operation. It does not alter the authorization decision.

### 6.7 Adapter invocation

The broker converts the accepted semantic request into the adapter's closed internal input.

Only the selected operation's bounded values reach the adapter. Free-form user input does not become a command, path, unit, package, image, device, or network rule.

### 6.8 Commit and verification

The adapter reports its execution steps. The broker verifies actual state independently where practical.

Commit uses a registered mechanism such as:

```text
atomic pointer
transactional journal
boot slot
atomic configuration swap
verified service-group transition
hardware-backed generation switch
validated equivalent
```

### 6.9 Completion

Completion occurs after:

1. the privileged effect commits;
2. actual state matches the intended result;
3. the operation journal reaches a terminal state;
4. the receipt is durable;
5. dependent local reconciliation completes.

A successful adapter return alone is not completion.

## 7. Journaling, Idempotency, and Recovery

### 7.1 Operation ledger

The operation ledger records:

- request identity;
- canonical request body;
- idempotency identity;
- authenticated caller and service;
- authorization decision;
- profile and target;
- operation state;
- attempts;
- result;
- receipt reference;
- terminal state.

The ledger is durable and protected from ordinary component writes.

### 7.2 Transaction journal

A transaction journal records:

- planned steps;
- before state;
- commit boundaries;
- completed steps;
- observed after state;
- compensating actions;
- last-known-good state;
- recovery environment;
- receipt state.

The journal is created before the first privileged mutation.

### 7.3 Idempotent replay

Equivalent replay:

1. resolves the existing ledger entry;
2. verifies the canonical body match;
3. verifies the caller remains entitled to receive the result;
4. revalidates any authority needed for a new effect;
5. returns the recorded or equivalent result without duplicate effect.

A body mismatch is a security event.

### 7.4 Crash classification

After restart, incomplete operations are classified as:

```text
not_started
pre_commit
commit_unknown
committed_verification_pending
receipt_pending
recovery_required
```

The broker compares journal state with actual host state.

### 7.5 Unknown effects

When commit outcome is unknown, the broker:

- blocks replay;
- isolates the affected target;
- inspects actual state;
- compares before, intended, and observed state;
- selects completion, rollback, compensation, forward repair, or recovery;
- records the reconciliation result.

### 7.6 Rollback and forward repair

Rollback uses a registered previous valid state.

Forward repair produces a new immutable artifact, configuration, or Release Set where the failed state cannot be reversed safely.

The broker executes the plan. The owning authority selects and authorizes it.

### 7.7 Cancellation

Cancellation before commit stops processing and records the terminal result.

Cancellation after an irreversible boundary invokes the declared compensation or recovery plan.

Required evidence remains durable.

### 7.8 Quarantine

Rejected artifacts, incompatible requests, malformed bundles, and suspicious replay attempts can enter broker-local quarantine.

Quarantine stores references, reason codes, observed metadata, and evidence. It does not duplicate unrestricted payloads unless the active evidence policy authorizes protected retention.

## 8. Receipts, Security, and Offline Behavior

### 8.1 Operation receipt

Every critical operation receipt identifies:

```text
receipt_id
operation
request_id
result_id
caller_identity_ref
service_identity_ref
policy_decision_ref
profile_ref
target_ref
before_state_ref
after_state_ref
artifact_refs
result_status
reason_codes
duration
correlation_id
occurred_at
recovery_ref
```

The receipt excludes secret values and unrestricted payloads.

### 8.2 Audit delivery

The broker stores the receipt locally before reporting final success.

Delivery to Audit Broker is:

- durable;
- idempotent;
- ordered where contractually required;
- duplicate-safe;
- restart-safe.

Audit Broker unavailability does not erase the receipt.

### 8.3 Restricted evidence

Transaction journals and protected host observations are restricted evidence.

Access requires separate authorization and produces its own audit record.

Public transparency receipts contain only the minimum safe proof.

### 8.4 Secret handling

The broker accepts managed references to keys or credentials.

It does not accept secret values in ordinary request parameters.

Adapters receive secrets only through the registered local secret mechanism and return no secret values in results or receipts.

### 8.5 Offline operation

The broker can operate offline when local authority inputs remain valid.

Supported offline operation can include:

- local Release Set activation;
- rollback;
- locally authorized configuration;
- service lifecycle;
- encrypted-volume lifecycle;
- node-scoped key transition;
- network-policy activation;
- recovery;
- signed offline bundle import;
- protected evidence export.

Unavailable remote services produce deferred or blocked states without weakening local controls.

### 8.6 Offline bundles

Offline bundles are quarantined before privileged handling.

Validation includes:

- manifest;
- source and signer identity;
- trust and revocation;
- signature;
- functional integrity;
- replay and downgrade;
- compatibility;
- target profile;
- authorization;
- rollback or repair material.

Possession of the medium does not authorize execution.

### 8.7 External systems and AI

External providers, federation peers, devices, controlled imports, and AI surfaces have no direct host-privilege interface.

Their outputs enter as candidate artifacts, requests, or evidence references.

Local identity, policy, compatibility, integrity, and broker validation remain mandatory.

## 9. Break-Glass, Profiles, and Failure Modes

### 9.1 Break-glass namespace

Break-glass operations are separate from ordinary operations.

A break-glass request includes:

- emergency operation identity;
- requesting human;
- approving human authority;
- stronger authentication;
- target;
- exact effect;
- short validity interval;
- reason codes;
- compensating controls;
- enhanced receipt;
- post-event review.

Ordinary operation names are not reinterpreted as emergency operations.

### 9.2 Profile scoping

Profiles own:

- enabled operation classes;
- adapter selection;
- broker activation mode;
- capability set;
- readable and writable paths;
- device access;
- network boundary;
- queue and resource limits;
- offline authority;
- recovery material;
- evidence requirements.

Profile composition can restrict an operation. It cannot add undeclared arbitrary behavior.

### 9.3 Failure model

| Failure | Broker behavior |
| --- | --- |
| Local peer invalid | Reject before parsing privileged parameters. |
| Service or caller identity invalid | Reject and record the boundary attempt. |
| Contract incompatible | Reject. |
| Unknown operation or parameter | Reject. |
| Authorization absent, expired, or revoked | Block. |
| Expected state mismatch | Enter conflict. |
| Artifact trust or integrity failure | Quarantine or reject. |
| Resource admission denied | Defer or reject. |
| Journal storage unavailable | Block new authoritative operations. |
| Adapter unavailable or incompatible | Block. |
| Failure before commit | Preserve prior valid state. |
| Commit outcome unknown | Enter recovery-required state. |
| Post-commit verification fails | Invoke rollback, repair, or recovery. |
| Receipt storage unavailable | Block final completion. |
| Audit Broker unavailable | Retain locally and retry. |
| Network unavailable | Continue profile-supported local behavior. |
| Contract authority invalid | Preserve last validated state and block mutation. |
| Break-glass approval incomplete | Reject. |

### 9.4 Resource pressure

Under pressure, the broker prioritizes:

1. journal integrity;
2. receipt durability;
3. active state;
4. last-known-good and rollback artifacts;
5. recovery environment;
6. reconciliation;
7. rollback;
8. new ordinary operations;
9. optional evidence export.

The broker does not evict another component's authoritative data.

### 9.5 Deactivation

Broker deactivation requires:

- no accepted nonterminal operation;
- durable journals and receipts;
- preserved recovery path;
- replacement broker or recovery environment where the profile requires privileged continuity;
- explicit lifecycle authorization.

An ordinary profile cannot silently remove the broker while retaining claims that depend on it.

## 10. Exceptions and Validation

### 10.1 Exceptions

A bounded exception can adjust:

- a platform-specific local transport;
- one adapter implementation;
- one capability mapping;
- one path or device representation;
- a queue or timeout value;
- a test environment;
- a compatibility interval;
- profile-specific diagnostic behavior.

An exception cannot:

- add arbitrary command execution;
- add a public broker listener;
- make root identity sufficient authority;
- bypass identity, policy, expected-state, trust, integrity, idempotency, or receipts;
- permit direct cross-component database writes;
- remove journaling for durable effects;
- permit blind replay;
- merge ordinary and break-glass operations;
- permit secret leakage;
- make external AI authoritative;
- remove rollback, repair, or recovery.

### 10.2 Validation criteria

This document is conformant when validation confirms:

1. the active broker identity is `koa_node_agent`;
2. the active component contract resolves;
3. one ordinary broker owns host-privileged execution;
4. every active operation has a complete closed contract;
5. generic shell, package, service, container, filesystem, device, and key-export interfaces are absent;
6. the ordinary interface is local and authenticated;
7. unknown fields and incompatible versions fail closed;
8. request identities bind to canonical bodies;
9. caller, service, policy, profile, target, expected state, deadline, and correlation are present;
10. identity and authorization remain separate;
11. resource admission remains separate from policy;
12. fixed adapters receive bounded inputs only;
13. every adapter privilege maps to an active operation;
14. journals begin before mutation;
15. before, intended, and observed states are recorded;
16. authoritative effects are atomic or have a validated equivalent;
17. completion requires verified after state and durable receipt;
18. duplicate replay is safe;
19. body mismatch is rejected;
20. conflicting operations serialize;
21. unknown effects enter recovery;
22. rollback, compensation, forward repair, or recovery exists;
23. receipts are durable and delivered idempotently;
24. restricted evidence access is separately authorized and audited;
25. secret values and unrestricted payloads are absent;
26. service hardening matches the active profile;
27. break-glass remains separate and human-authorized;
28. offline operation uses equivalent controls;
29. external integrations and AI have no direct privilege path;
30. every decision, profile, operation, adapter, artifact, test, evidence, receipt, and exception reference resolves;
31. no prohibited open-state marker enters active security authority.

The principal validation entry point is:

```bash
python docs/tools/validate_docs.py
```

Supporting checks include:

```text
tools/check_privilege_boundaries.py
tools/check_component_boundaries.py
tools/check_interfile_locks.py
tools/check_profile_inheritance.py
tools/check_artifact_contracts.py
tools/check_release_sets.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_no_unresolved_state.py
```

A failed broker check blocks the affected operation, broker contract, profile claim, release activation, or recovery completion.

## 11. Non-Normative Examples

### 11.1 Closed restart operation

A caller requests `restart_service_group` with an allowlisted group, expected health state, authorization decision, and idempotency identity. The broker invokes the fixed service adapter and verifies the resulting health state.

### 11.2 Rejected arbitrary shell

A caller submits `run_command` with `systemctl restart ...`. The broker rejects the unknown operation before any privileged adapter invocation.

### 11.3 Equivalent replay

A client retries the same activation request after a connection loss. The broker finds the same canonical body and returns the recorded result without activating twice.

### 11.4 Body mismatch

A caller reuses an idempotency identity but changes the target Release Set. The broker rejects the request and creates a security receipt.

### 11.5 Unknown commit outcome

Power fails during network-policy activation. On restart, the broker checks actual firewall, route, interface, and connectivity-guard state before deciding completion, rollback, or recovery.

### 11.6 Audit outage

Audit Broker is temporarily unavailable. The broker keeps the receipt durable locally, reports the delivery state accurately, and retries idempotently.

### 11.7 Key rotation

Identity and Trust authorizes a node-scoped key rotation. The broker invokes the fixed hardware or host adapter and records the new generation without exposing private key material.

### 11.8 Offline release activation

A sovereign-offline node imports a signed Release Set bundle. The broker verifies all local authority and recovery inputs before atomically activating the complete Release Set.

### 11.9 Developer profile

A developer has administrator access to the host. Application components still use the broker contract, and the developer's manual privilege does not become a production operation.

### 11.10 Break-glass recovery

A verified emergency operation uses a separate namespace, stronger authentication, exact scope, two human authorities, a short validity interval, enhanced evidence, and post-event review.
