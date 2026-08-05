<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-005",
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
    "contracts/system.contract.json#/security_model",
    "generated/component-catalog.json",
    "generated/component-catalog.json#/components/identity_and_trust",
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "generated/component-catalog.json#/components/resource_governor",
    "generated/component-catalog.json#/components/audit_broker",
    "generated/component-catalog.json#/components/koa_node_agent",
    "contracts/components/koa-node-agent.component.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-SEC-PRIV-001",
    "DEC-COMP-NODE-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-RESOURCE-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001",
    "DEC-LIFE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-PRIV-001",
    "REQ-SEC-PRIV-002",
    "REQ-SEC-PRIV-003",
    "REQ-SEC-PRIV-004",
    "REQ-SEC-PRIV-005",
    "REQ-SEC-PRIV-006",
    "REQ-SEC-PRIV-007",
    "REQ-SEC-PRIV-008",
    "REQ-SEC-PRIV-009",
    "REQ-SEC-PRIV-010",
    "REQ-SEC-PRIV-011",
    "REQ-SEC-PRIV-012",
    "REQ-SEC-PRIV-013",
    "REQ-SEC-PRIV-014",
    "REQ-SEC-PRIV-015",
    "REQ-SEC-PRIV-016",
    "REQ-SEC-PRIV-017",
    "REQ-SEC-PRIV-018",
    "REQ-SEC-PRIV-019",
    "REQ-SEC-PRIV-020",
    "REQ-SEC-PRIV-021",
    "REQ-SEC-PRIV-022",
    "REQ-SEC-PRIV-023",
    "REQ-SEC-PRIV-024",
    "REQ-SEC-PRIV-025",
    "REQ-SEC-PRIV-026",
    "REQ-SEC-PRIV-027",
    "REQ-SEC-PRIV-028",
    "REQ-SEC-PRIV-029",
    "REQ-SEC-PRIV-030",
    "REQ-SEC-PRIV-031",
    "REQ-SEC-PRIV-032",
    "REQ-SEC-PRIV-033",
    "REQ-SEC-PRIV-034",
    "REQ-SEC-PRIV-035",
    "REQ-SEC-PRIV-036",
    "REQ-SEC-PRIV-037",
    "REQ-SEC-PRIV-038",
    "REQ-SEC-PRIV-039",
    "REQ-SEC-PRIV-040"
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
    "DOC-SEC-004"
  ],
  "tags": [
    "privilege-boundaries",
    "least-privilege",
    "privileged-broker",
    "host-mutation",
    "authorization",
    "service-identity",
    "capabilities",
    "containers",
    "break-glass",
    "audit",
    "offline-security",
    "conformance"
  ]
}
KOA:DOC-META:END -->

# Privilege Boundaries

## 1. Purpose

This document defines the privilege boundaries of kOA.

Privilege is the ability to produce an effect that ordinary component execution cannot produce safely by itself. Examples include changing boot state, installing or activating protected artifacts, controlling host services, modifying firewall or route policy, operating encrypted volumes, accessing protected devices, rotating node-scoped keys, entering recovery, or writing protected host configuration.

The security model separates five questions:

1. who or what is making the request;
2. whether the requested effect is authorized;
3. whether resources are available;
4. which narrow executor performs the effect;
5. where the result and evidence become authoritative.

These questions have different owners. A single root process, administrator account, privileged container, automation agent, or external control service does not combine them.

The model establishes least privilege by operation, target, scope, time, profile, expected state, and evidence. It does not rely on informal trust in an operator or broad administrator access.

## 2. Scope

This document applies globally to:

- operating-system privilege;
- root and administrator identities;
- Linux capabilities and equivalent platform privileges;
- service-manager control;
- boot and recovery control;
- host and network configuration;
- encrypted storage and device access;
- node-scoped key operations;
- protected artifact staging and activation;
- local privileged APIs and sockets;
- container privilege;
- developer workstation privilege;
- offline privileged operations;
- emergency and break-glass operations;
- privileged-operation receipts and evidence;
- component, profile, test, and conformance claims.

It applies to every primary profile and compatible overlay.

This document does not define the complete operation list of kOA Node Agent, the complete break-glass procedure, trust-root custody, secret storage internals, or platform-specific hardening values. Those facts remain owned by the corresponding component contract, security document, profile contract, and implementation evidence.

## 3. Canonical References

Canonical ownership is distributed as follows:

| Subject | Canonical owner |
| --- | --- |
| Global security and privilege model | `contracts/system.contract.json#/security_model` |
| Component identity and responsibility | `generated/component-catalog.json` |
| kOA Node Agent operation and privilege contract | `contracts/components/koa-node-agent.component.json` |
| User, service, node, artifact, signer, and key identity | Identity and Trust component contract |
| Privilege authorization and obligations | Governance Policy Runtime component contract |
| Resource admission and pressure enforcement | Resource Governor component contract |
| Privileged audit storage and evidence access | Audit Broker component contract |
| Profile-specific privilege and hardening | `contracts/profiles/*.profile.json` |
| Artifact identity, trust, compatibility, and lifecycle | `contracts/artifact-classes.contract.json` |
| External and offline integration boundaries | `contracts/integration-types.contract.json` |
| Requirement statements and strength | `generated/requirements-index.json` |
| Cross-file privilege invariants | `generated/assertion-index.json` |
| Privilege, component, profile, test, and evidence links | `generated/traceability.json` |
| Privilege and security tests | `generated/test-catalog.json` |
| Current privilege evidence | `generated/evidence-catalog.json` |
| Approved bounded deviations | `generated/exception-index.json` |
| Accepted privilege decisions | `generated/decision-index.json` |
| Active versions and authority order | `generated/authority-manifest.json` |

The operating system enforces part of the boundary. It does not own the kOA authorization decision.

## 4. Privilege Model and Responsibilities

### 4.1 Privilege effect classes

The model classifies privileged effects independently of implementation technology.

| Effect class | Examples |
| --- | --- |
| `protected_read` | Read restricted host, device, trust, or lifecycle state |
| `host_configuration` | Apply registered host configuration |
| `service_lifecycle` | Start, stop, restart, or reload an allowlisted service group |
| `release_lifecycle` | Stage, activate, roll back, or repair a Release Set |
| `artifact_lifecycle` | Stage, activate, pin, quarantine, or retire protected artifacts |
| `storage_lifecycle` | Create, unlock, lock, resize, verify, or retire declared encrypted volumes |
| `network_enforcement` | Apply registered interface, route, firewall, resolver, or proxy policy |
| `trust_lifecycle` | Execute approved node-scoped key or trust material transitions |
| `device_operation` | Access an allowlisted device or controlled transfer medium |
| `recovery` | Enter, operate, or exit a verified recovery environment |
| `boot_control` | Select or verify a registered boot slot or boot entry |
| `security_evidence` | Read or export protected node evidence through governed selection |

Each effect class remains closed. A class does not imply arbitrary command execution.

### 4.2 Authority separation

The privilege workflow has separate authorities:

| Responsibility | Owner |
| --- | --- |
| Caller and service identity | Identity and Trust |
| Target artifact and signer identity | Identity and Trust |
| Authorization, target scope, expiry, and obligations | Governance Policy Runtime or another registered authority |
| Resource admission | Resource Governor |
| Local host execution | kOA Node Agent or another explicitly registered narrow broker |
| Component business-state transition | Owning component |
| Release compatibility | Release-channel authority |
| Artifact semantic validation | Artifact owner or consuming component |
| Audit storage and evidence access | Audit Broker |
| User-visible workflow state | Owning application component |

The executor can reject an invalid request. It cannot invent a missing decision.

### 4.3 Ordinary privileged broker

kOA Node Agent is the sole ordinary host-privileged broker where its active contract applies.

Its ordinary interface uses:

- local transport;
- authenticated peer and service identity;
- a closed operation name;
- a closed parameter schema;
- a current authorization decision;
- a target profile and scope;
- expected state;
- an idempotency identity;
- a deadline;
- required artifacts and integrity records;
- durable operation state;
- a result and receipt.

The broker is authoritative for execution state and result. It is not authoritative for identity, policy, release compatibility, component business data, publication rights, consent, cultural rights, or resource policy.

### 4.4 Application components

Application components operate as dedicated unprivileged service identities.

They interact with protected host state through:

- registered component APIs;
- kOA Node Agent operations;
- registered artifacts;
- gateways;
- controlled import or export;
- profile-approved device adapters.

An application process does not receive broad privilege merely because it coordinates a workflow whose final step is privileged.

### 4.5 Root and administrator identities

Root or administrator identity is an operating-system execution property.

It is not:

- a user authorization decision;
- a publication decision;
- a consent decision;
- a release compatibility decision;
- a cultural-rights decision;
- a reason to bypass expected-state checks;
- a reason to ignore expiry or revocation;
- evidence that the operation was requested by the correct authority.

A privileged executor running as root remains constrained by its operation contract and system hardening.

### 4.6 Least privilege by operation

Least privilege is expressed as a tuple:

`text
service identity
operation identity
target identity
profile
authority scope
parameter schema
expected state
time window
required artifacts
operating-system permissions
audit class
`

Changing any tuple element creates a distinct authorization and validation context.

### 4.7 Operating-system enforcement

The implementation uses applicable mechanisms such as:

- dedicated service users and groups;
- file ownership and mode;
- Unix-domain socket permissions;
- Linux capability bounding;
- no-new-privileges enforcement;
- system-call filters;
- address-family restrictions;
- protected system and home paths;
- private temporary storage;
- bounded writable paths;
- device allowlists;
- cgroup resource controls;
- namespace isolation;
- mandatory access control where provided;
- service-manager sandboxing.

Profile contracts own platform-specific values. The logical boundary remains consistent across platforms.

### 4.8 Privileged service hardening

A privileged service's evidence identifies:

- execution identity;
- effective capabilities or privileges;
- ambient capabilities;
- permitted system calls;
- address families;
- writable paths;
- readable protected paths;
- device access;
- network listener state;
- service-manager hardening;
- resource limits;
- active profile and contract version.

Unused privilege is removed rather than left dormant.

### 4.9 Container boundary

Containers are not a privilege authority.

An ordinary containerized component uses:

- rootless execution;
- no privileged flag;
- no container-daemon socket;
- no unrestricted host filesystem;
- no host PID namespace;
- no host user namespace;
- no unrestricted host network;
- no unregistered devices;
- an explicit capability set;
- read-only runtime image where practical;
- workspace- or profile-scoped writable storage.

A container that needs a privileged host effect requests a registered broker operation.

### 4.10 Developer boundary

A developer can have administrator access to a workstation while kOA components remain unprivileged.

Developer access is outside the runtime authority path. Actions performed manually with host privilege:

- do not become component conformance evidence automatically;
- do not establish a supported operation;
- do not transfer to production profiles;
- do not justify a broader broker interface;
- do not change canonical ownership.

Debugging helpers remain profile-scoped and excluded from production claims.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-PRIV-001,REQ-SEC-PRIV-002,REQ-SEC-PRIV-003,REQ-SEC-PRIV-004,REQ-SEC-PRIV-005,REQ-SEC-PRIV-006,REQ-SEC-PRIV-007,REQ-SEC-PRIV-008,REQ-SEC-PRIV-009,REQ-SEC-PRIV-010,REQ-SEC-PRIV-011,REQ-SEC-PRIV-012,REQ-SEC-PRIV-013,REQ-SEC-PRIV-014,REQ-SEC-PRIV-015,REQ-SEC-PRIV-016,REQ-SEC-PRIV-017,REQ-SEC-PRIV-018,REQ-SEC-PRIV-019,REQ-SEC-PRIV-020,REQ-SEC-PRIV-021,REQ-SEC-PRIV-022,REQ-SEC-PRIV-023,REQ-SEC-PRIV-024,REQ-SEC-PRIV-025,REQ-SEC-PRIV-026,REQ-SEC-PRIV-027,REQ-SEC-PRIV-028,REQ-SEC-PRIV-029,REQ-SEC-PRIV-030,REQ-SEC-PRIV-031,REQ-SEC-PRIV-032,REQ-SEC-PRIV-033,REQ-SEC-PRIV-034,REQ-SEC-PRIV-035,REQ-SEC-PRIV-036,REQ-SEC-PRIV-037,REQ-SEC-PRIV-038,REQ-SEC-PRIV-039,REQ-SEC-PRIV-040 -->
- **REQ-SEC-PRIV-001 — SHALL:** Every privileged effect have one explicit operation identity, authority owner, execution boundary, target scope, parameter contract, preconditions, result contract, and audit class.
- **REQ-SEC-PRIV-002 — SHALL:** Ordinary application components execute without general host-administrator, root, kernel, hypervisor, container-daemon, boot-loader, device-management, or unrestricted storage privilege.
- **REQ-SEC-PRIV-003 — SHALL NOT:** Installation, process ownership, Unix user identity, root identity, container membership, local socket access, network reachability, or successful authentication by itself authorize a privileged effect.
- **REQ-SEC-PRIV-004 — SHALL:** Identity and Trust verify user, service, node, artifact, signer, key, and device identities used by privileged workflows.
- **REQ-SEC-PRIV-005 — SHALL:** Governance Policy Runtime or another explicitly registered authority decide whether a privileged operation is permitted, for which target, under which profile, until which expiry, and with which obligations.
- **REQ-SEC-PRIV-006 — SHALL:** kOA Node Agent be the sole ordinary narrow broker for registered host-privileged node operations where its component contract applies.
- **REQ-SEC-PRIV-007 — SHALL NOT:** kOA Node Agent expose arbitrary shell execution, arbitrary system-service control, arbitrary package-manager access, arbitrary container execution, arbitrary filesystem mutation, unrestricted device access, or raw private-key export.
- **REQ-SEC-PRIV-008 — SHALL:** Every brokered privileged operation use a closed request schema and reject unknown operations, unknown parameters, incompatible contract versions, missing expected state, and reuse of an idempotency identity with a different canonical body.
- **REQ-SEC-PRIV-009 — SHALL:** Every privileged request bind the authenticated caller, authorization decision, target profile, target resource, expected state, correlation identity, request time, and deadline.
- **REQ-SEC-PRIV-010 — SHALL:** Every time-sensitive privileged decision be revalidated before the first privileged mutation and before the authoritative commit.
- **REQ-SEC-PRIV-011 — SHALL:** Resource-affecting privileged operations obtain Resource Governor admission without transferring authorization or governance policy authority to the Resource Governor.
- **REQ-SEC-PRIV-012 — SHALL NOT:** Resource pressure, resource ownership, process priority, cgroup membership, or hardware availability determine authorization, consent, disclosure, publication, cultural rights, or governance policy.
- **REQ-SEC-PRIV-013 — SHALL:** Privileged service identities use the minimum operating-system capabilities, filesystem paths, devices, address families, system calls, namespaces, and service-manager controls required by their closed operation set.
- **REQ-SEC-PRIV-014 — SHALL:** Privileged services use dedicated service identities, restrictive file permissions, private temporary storage, protected system paths, bounded writable paths, bounded resources, and no-new-privileges enforcement where supported.
- **REQ-SEC-PRIV-015 — SHALL NOT:** Set-user-ID executables, set-group-ID executables, ambient capabilities, unrestricted sudo rules, passwordless general administrator shells, or privileged helper binaries become the ordinary component integration path.
- **REQ-SEC-PRIV-016 — SHALL:** Every privileged local interface use a local transport or another explicitly registered boundary with peer identity verification, service identity verification, authorization binding, rate and queue bounds, timeout behavior, and fail-closed compatibility handling.
- **REQ-SEC-PRIV-017 — SHALL NOT:** An ordinary privileged management interface listen on a public or undeclared network boundary.
- **REQ-SEC-PRIV-018 — SHALL:** Privileged storage access be limited to registered paths, volumes, device classes, data classes, and lifecycle operations owned by the active component and profile contracts.
- **REQ-SEC-PRIV-019 — SHALL NOT:** A privileged broker write directly to another component's authoritative business store or reinterpret another component's migration, policy, publication, consent, or data-ownership decision.
- **REQ-SEC-PRIV-020 — SHALL:** Every privileged artifact operation verify artifact identity, class, signature or trust where required, functional integrity, compatibility, revocation state, expected active state, and recovery material before activation.
- **REQ-SEC-PRIV-021 — SHALL:** Every privileged activation or configuration change use atomic commit or a validated equivalent, preserve the prior valid state, and provide rollback, forward repair, or recovery.
- **REQ-SEC-PRIV-022 — SHALL NOT:** A partial privileged effect be reported as complete, and an unknown effect after interruption be retried blindly.
- **REQ-SEC-PRIV-023 — SHALL:** Every privileged operation bind one idempotency identity to one canonical request body and return the recorded or equivalent result for an authorized replay.
- **REQ-SEC-PRIV-024 — SHALL:** Conflicting privileged operations be serialized for their target scope, including activation, rollback, key rotation, trust-root change, network-policy change, storage transition, and recovery transition.
- **REQ-SEC-PRIV-025 — SHALL:** Every privileged operation produce a durable critical-transition receipt with caller, authority, target, operation, request, before state, after state, artifacts, result, reason codes, timing, and recovery references.
- **REQ-SEC-PRIV-026 — SHALL NOT:** Privileged requests, logs, metrics, traces, receipts, or evidence contain secret values, raw private keys, unrestricted sensitive payloads, or credentials copied from a source component.
- **REQ-SEC-PRIV-027 — SHALL:** Audit Broker receive privileged-operation receipts through durable idempotent delivery, while temporary Audit Broker unavailability preserves local receipt durability.
- **REQ-SEC-PRIV-028 — SHALL:** Access to restricted privileged evidence be separately authorized and audited.
- **REQ-SEC-PRIV-029 — SHALL:** Break-glass operations use a separate operation namespace, stronger authentication, explicit human authority, bounded target and duration, reason codes, compensating controls, and enhanced audit.
- **REQ-SEC-PRIV-030 — SHALL NOT:** A component, agent, model, automation, operator UID, or service account infer break-glass authority from urgency, failure severity, local ownership, or lack of connectivity.
- **REQ-SEC-PRIV-031 — SHALL:** Containerized components remain unprivileged by default and use rootless execution, bounded mounts, bounded devices, isolated networks, and explicit capability sets according to the active profile.
- **REQ-SEC-PRIV-032 — SHALL NOT:** Privileged containers, host PID or user namespaces, unrestricted host networking, container-daemon sockets, arbitrary host mounts, or device pass-through become the ordinary runtime baseline.
- **REQ-SEC-PRIV-033 — SHALL:** Developer profiles preserve the same component and authority boundaries even when the developer has host-administrator access outside kOA.
- **REQ-SEC-PRIV-034 — SHALL NOT:** Developer convenience, debugging, local success, workstation ownership, WSL administration, or container-backend administration establish production or runtime privilege authority.
- **REQ-SEC-PRIV-035 — SHALL:** Privileged local core operations remain executable offline when the active profile provides local identity, authorization, trust, artifact, audit, and recovery material.
- **REQ-SEC-PRIV-036 — SHALL:** Offline privileged import, activation, key, trust, network, and recovery workflows apply the same identity, authorization, integrity, compatibility, replay, atomicity, receipt, and recovery controls as connected workflows.
- **REQ-SEC-PRIV-037 — SHALL:** External integrations and external AI surfaces have no direct privileged host interface and produce only registered candidate, request, artifact, or decision inputs for local validation.
- **REQ-SEC-PRIV-038 — SHALL NOT:** External AI output, external provider acknowledgement, federation input, removable-media possession, or signed transport alone authorize a privileged local effect.
- **REQ-SEC-PRIV-039 — SHALL:** Profile and component conformance claims identify every privileged operation class, broker, service identity, authorization authority, operating-system capability, writable path, device, network boundary, test, and current evidence.
- **REQ-SEC-PRIV-040 — SHALL:** Privilege-boundary conformance include least-privilege execution, closed broker operations, identity and policy separation, resource separation, component data ownership, interface locality, hardening, atomicity, idempotency, audit durability, break-glass separation, container restrictions, offline execution, reference resolution, and absence of prohibited open-state markers.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Privileged Operation Procedure

### 6.1 Request creation

A privileged request includes:

`text
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
`

Only operation-specific fields permitted by the active contract can appear.

Secret values remain outside the request. Managed references identify required credentials or keys.

### 6.2 Admission sequence

Admission proceeds through:

`text
request_received
transport_peer_verified
service_identity_verified
request_schema_verified
operation_allowlist_verified
target_scope_verified
policy_decision_verified
decision_expiry_verified
decision_obligations_loaded
expected_state_verified
artifact_and_trust_verified
resource_admission_verified
request_accepted
`

A failed stage blocks the privileged effect.

### 6.3 Pre-mutation verification

Immediately before mutation, the executor rechecks:

- authorization validity;
- target identity;
- expected state;
- artifact trust and revocation;
- resource admission;
- deadline;
- conflicting operations;
- recovery readiness;
- receipt storage.

This protects against state change between admission and execution.

### 6.4 Execution

Execution uses a fixed adapter for the selected operation.

The adapter receives only validated bounded parameters. It does not interpret user-provided shell fragments, service names, filesystem paths, package names, container arguments, devices, or network rules outside the registered contract.

Every material step records before and after state in the privileged-operation journal.

### 6.5 Commit and verification

For authoritative effects, commit uses an atomic mechanism or validated equivalent.

Examples include:

`text
atomic pointer
transactional journal
boot slot
atomic configuration swap
verified service-group transition
hardware-backed key generation switch
validated equivalent
`

After commit, the executor verifies actual state rather than assuming adapter success.

### 6.6 Result and receipt

The result distinguishes:

`text
completed
blocked
rejected
cancelled
failed
conflicted
expired
rolled_back
recovery_required
`

Completion requires:

- committed effect;
- verified after state;
- durable receipt.

The receipt is delivered to Audit Broker idempotently and retained locally when delivery is unavailable.

### 6.7 Idempotency and replay

One idempotency identity binds one canonical request body.

Equivalent replay returns the recorded or equivalent result after rechecking any authority that remains time-sensitive for the requested action.

A different body using the same identity is rejected and recorded as a security event.

An unknown prior external or host effect enters reconciliation before retry.

### 6.8 Concurrency

The executor serializes operations that can conflict through:

- the same host state;
- the same service group;
- the same release scope;
- the same key;
- the same network policy;
- the same encrypted volume;
- the same recovery target;
- the same device.

Non-conflicting operations remain bounded by the active resource envelope.

### 6.9 Cancellation

Cancellation can stop an accepted operation before an irreversible commit boundary.

After the boundary, the workflow uses rollback, compensation, forward repair, or recovery according to the operation contract.

Cancellation never deletes required receipts or evidence.

## 7. Failure Modes and Safe Degradation

| Failure | Required behavior |
| --- | --- |
| Caller identity unavailable | Reject before privileged mutation. |
| Service identity invalid | Reject and record the attempted boundary crossing. |
| Policy decision missing or expired | Block the operation. |
| Target outside scope | Reject without probing or mutating the target. |
| Unknown operation | Reject. |
| Unknown parameter | Reject. |
| Expected state mismatch | Enter conflict without mutation. |
| Artifact trust or integrity failure | Quarantine or reject the artifact. |
| Resource admission denied | Defer or reject while preserving active state. |
| Privileged adapter incompatible | Block the operation. |
| Operation deadline exceeded before commit | Fail without authoritative effect. |
| Operation outcome unknown after mutation | Enter `recovery_required` and block blind replay. |
| Receipt storage unavailable | Block new authoritative privileged effects that require durable evidence. |
| Audit Broker unavailable | Preserve local receipt durability and retry. |
| Storage pressure | Preserve journals, receipts, active state, and recovery artifacts before optional work. |
| Network unavailable | Continue locally authorized operations supported by the profile. |
| Remote authorization unavailable | Use only valid locally held authority; otherwise defer or block. |
| Revocation received | Block, isolate, roll back, repair, or recover according to the registered rule. |
| Broker contract invalid | Preserve the last validated state and reject new privileged mutations. |
| Break-glass authority incomplete | Reject the emergency operation. |

Safe degradation does not broaden the operation set, target scope, privileges, network exposure, or data access.

## 8. Security and Trust Boundaries

### 8.1 Local interface boundary

The ordinary privileged broker interface is local.

A Unix-domain socket is the default where supported. The implementation verifies:

- peer process credentials;
- service identity;
- socket ownership and permissions;
- active contract version;
- operation rate and queue limits;
- request size;
- request deadline;
- audit correlation.

A remote administration service can request a local operation only through an explicitly registered integration and local authorization path. It does not expose the broker socket directly.

### 8.2 Capability boundary

Operating-system capabilities are assigned to the broker service, not to arbitrary calling components.

Capability evidence maps every capability to active operations. A capability with no active operation justification is removed.

Ambient capabilities remain empty in the ordinary service model.

### 8.3 Filesystem boundary

The broker can read or write only:

- its own operation ledger;
- activation journals;
- protected artifact staging locations;
- registered configuration targets;
- registered volume or device control paths;
- registered recovery state;
- paths explicitly owned by active operation contracts.

Arbitrary paths and path traversal are rejected.

Component data migrations execute through the owning component or a registered migration adapter. The broker does not become the database owner.

### 8.4 Service-manager boundary

Service lifecycle operations identify an allowlisted service group and dependency plan.

The broker does not expose generic unit names, arbitrary environment changes, arbitrary command overrides, or arbitrary service-manager properties.

The result verifies the intended service and health state.

### 8.5 Network boundary

Network operations use signed or policy-authorized network configurations compatible with the active profile.

The broker can apply an approved configuration. It does not decide disclosure, remote trust, integration eligibility, or publication authority.

Connectivity guards and rollback paths protect against accidental administrative lockout.

### 8.6 Key and trust boundary

Identity and Trust owns key lifecycle policy, signing identities, trust roots, revocation, and verification.

The broker can execute the host-privileged portion of an approved node-scoped key transition. It cannot export raw private keys or invent a key-rotation plan.

### 8.7 Device boundary

Devices and removable media use explicit device classes and operation contracts.

Possession or attachment of a device does not authorize reading, importing, executing, unlocking, or exporting.

Offline bundles remain quarantined until identity, trust, integrity, replay, compatibility, policy, rights, and ownership checks pass.

### 8.8 Audit boundary

Privileged receipts use `security_and_node_audit` unless a stricter audit class applies.

Public transparency receipts, when produced, omit protected implementation details and remain distinct from restricted evidence.

Access to transaction journals, host state, key references, network details, and security evidence is itself audited.

### 8.9 External and AI boundary

External providers and external AI surfaces have no privileged host channel.

Returned material can be:

- a candidate artifact;
- a candidate configuration;
- a non-authoritative recommendation;
- a controlled import;
- an approval input from a registered human workflow.

Local authorities validate it before any privileged request is accepted.

## 9. Break-Glass, Profiles, and Exceptions

### 9.1 Break-glass separation

Break-glass operations use a separate namespace and policy.

They include:

- explicit human requester;
- explicit approving authority;
- stronger authentication;
- exact target;
- exact permitted operation;
- bounded duration;
- reason codes;
- compensating controls;
- enhanced evidence;
- post-event review;
- revocation or closure.

Ordinary operation names are not silently reinterpreted as emergency operations.

### 9.2 Profile scoping

Profiles own:

- available privileged operations;
- required broker activation mode;
- operating-system capability set;
- writable paths;
- device classes;
- network exposure;
- hardening settings;
- offline authority;
- evidence requirements;
- break-glass eligibility.

A development profile can expose diagnostic operations that production profiles exclude. Those operations remain profile-scoped.

### 9.3 Offline profiles

A sovereign-offline profile retains enough local identity, authorization, trust, time, artifact, audit, and recovery material for its declared privileged core.

Expired or unverifiable local authority fails closed.

Offline state does not create emergency authority.

### 9.4 Exceptions

A bounded exception can adjust:

- a platform-specific hardening mechanism;
- one capability mapping;
- one path implementation;
- one device adapter;
- a test environment;
- a compatibility interval;
- a profile-specific diagnostic operation.

An exception cannot:

- create arbitrary shell access;
- make root identity sufficient authorization;
- bypass Identity and Trust;
- bypass Governance Policy Runtime;
- allow direct cross-component database writes;
- remove closed parameter schemas;
- remove idempotency or receipts;
- permit secret leakage;
- merge ordinary and break-glass operations;
- authorize privileged containers as the default;
- create a public broker listener;
- support an unqualified conformance claim outside its scope.

## 10. Validation Criteria

This document is conformant when validation confirms:

1. every privileged effect maps to a stable operation identity;
2. every operation identifies its authority owner, executor, target, parameters, result, and audit class;
3. ordinary components have no general host privilege;
4. root or administrator identity does not bypass authorization;
5. Identity and Trust verifies all applicable identities;
6. Governance Policy Runtime or another registered authority owns authorization;
7. kOA Node Agent remains the sole ordinary narrow broker where applicable;
8. arbitrary shell, service, package, container, filesystem, device, and key-export interfaces are absent;
9. request schemas and parameters are closed;
10. expected-state, expiry, profile, scope, and idempotency checks pass;
11. resource admission remains separate from policy authority;
12. operating-system privileges are minimal and operation-mapped;
13. service hardening is present and profile-compatible;
14. local interface peer and service identity verification pass;
15. public or undeclared privileged listeners are absent;
16. filesystem, service-manager, network, storage, device, and key boundaries are explicit;
17. no direct cross-component authoritative-store writes exist;
18. artifact trust, integrity, compatibility, and revocation checks pass;
19. authoritative effects are atomic or have a validated equivalent;
20. last-known-good, rollback, forward repair, or recovery exists;
21. interrupted unknown effects enter recovery before retry;
22. conflicting operations serialize;
23. receipts are durable and delivered idempotently;
24. secrets and unrestricted payloads remain absent from operational evidence;
25. restricted evidence access is authorized and audited;
26. break-glass is separate, human-authorized, bounded, and reviewed;
27. ordinary containers remain unprivileged and isolated;
28. developer administrator access does not alter runtime authority;
29. offline privilege uses equivalent controls;
30. external integrations and AI have no direct privileged effect;
31. all decisions, profiles, components, operations, artifacts, tests, evidence, and exceptions resolve;
32. no prohibited open-state marker enters active security authority.

The principal validation entry point is:

`bash
python docs/tools/validate_docs.py
`

Supporting checks include:

`text
tools/check_component_boundaries.py
tools/check_privilege_boundaries.py
tools/check_interfile_locks.py
tools/check_profile_inheritance.py
tools/check_artifact_contracts.py
tools/check_ai_boundary.py
tools/check_traceability.py
tools/check_decision_closure.py
tools/check_no_unresolved_state.py
`

A failed privilege-boundary check blocks the affected operation, component, profile, release activation, or conformance claim.

## 11. Non-Normative Examples

### 11.1 Service restart

An application requests restart of an allowlisted service group. Identity and Trust verifies the caller, Governance Policy Runtime verifies authorization, Resource Governor admits the operation, and kOA Node Agent executes the fixed restart plan.

### 11.2 Rejected generic command

A caller submits `run_command` with a shell string. The broker rejects the unknown operation because no generic command interface exists.

### 11.3 Root caller

A local root process connects to the broker socket without a valid service identity and policy decision. The request is rejected.

### 11.4 Release activation

A validated Release Set is staged. kOA Node Agent verifies expected state, trust, integrity, compatibility, recovery readiness, and authorization before atomically changing the active state.

### 11.5 Database migration

A component release requires a data migration. The owning component executes or governs the semantic migration. The privileged broker performs only registered host or service steps.

### 11.6 Network change

An authorized network-policy bundle includes a rollback path and connectivity guard. The broker applies it atomically and verifies the expected interface, route, and firewall state.

### 11.7 Key rotation

Identity and Trust creates an approved node-scoped rotation plan. The broker invokes the hardware or host adapter, records the resulting generation, and never exports the private key.

### 11.8 Developer workstation

A developer uses host administrator access to inspect a failed container backend. The application containers remain unprivileged, and the manual action does not become a supported production operation.

### 11.9 Offline bundle

A sovereign-offline node receives a signed release bundle on removable media. Possession of the media grants no authority. The bundle is quarantined and validated before a local activation request can be authorized.

### 11.10 Break-glass recovery

A verified recovery case uses a separate emergency operation, stronger authentication, two human authorities, a short validity period, exact target scope, local receipts, and post-event review.
