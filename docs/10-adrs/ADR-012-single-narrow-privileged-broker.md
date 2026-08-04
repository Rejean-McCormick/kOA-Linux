<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-012",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-012",
    "generated/decision-index.json#/decisions/DEC-SYS-001",
    "contracts/system.contract.json#/global_boundaries/privilege",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/resource_governance",
    "generated/component-catalog.json#/components/koa_node_agent",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/identity-and-trust.component.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/node-profile.schema.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-COMP-NODE-001",
    "REQ-COMP-NODE-002",
    "REQ-COMP-NODE-003",
    "REQ-COMP-NODE-004",
    "REQ-COMP-NODE-005",
    "REQ-COMP-NODE-006",
    "REQ-COMP-NODE-007",
    "REQ-COMP-NODE-008",
    "REQ-COMP-NODE-009",
    "REQ-COMP-NODE-010",
    "REQ-COMP-NODE-011",
    "REQ-COMP-NODE-012",
    "REQ-COMP-NODE-013",
    "REQ-COMP-NODE-014",
    "REQ-COMP-NODE-015",
    "REQ-COMP-NODE-016",
    "REQ-COMP-NODE-017",
    "REQ-COMP-NODE-018",
    "REQ-COMP-NODE-019",
    "REQ-COMP-NODE-020",
    "REQ-COMP-NODE-021",
    "REQ-COMP-NODE-022",
    "REQ-COMP-NODE-023",
    "REQ-COMP-NODE-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-014",
    "DOC-GOV-016",
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-COMP-005",
    "DOC-COMP-011",
    "DOC-LIFE-017",
    "DOC-SEC-010",
    "DOC-OPS-007",
    "DOC-CONF-012",
    "DOC-CONF-019"
  ],
  "tags": [
    "architecture-decision",
    "privileged-broker",
    "koa-node-agent",
    "single-authority-path",
    "closed-operations",
    "least-privilege",
    "node-local-validation",
    "idempotency",
    "receipts",
    "break-glass",
    "safe-degradation",
    "non-ai"
  ]
}
KOA:DOC-META:END -->

# ADR-012 — Single Narrow Privileged Broker

**ADR ID:** `ADR-012`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `system_architecture_authority`  
**Owner decision:** `DEC-SYS-001`  
**Change packet:** `CHG-2026-0012`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

kOA uses one logical node-local privileged broker for profile-authorized sensitive host mutations. The registered broker is the kOA Node Agent. It accepts only versioned closed high-level operation classes, performs final node-local validation, applies the minimum required privilege, serializes conflicting mutations, protects idempotency and replay state, preserves rollback or forward-repair behavior, and emits machine-readable receipts.

No component, control plane, administrator, container runtime, Kubernetes role, package manager, service manager, external AI service, script collection, or emergency procedure creates a parallel ordinary privilege path.

“Single” means one logical authority and mutation-coordination domain per node. High availability can use multiple processes or passive replicas only when they share one canonical operation registry, one authoritative idempotency and operation-state model, one receipt sequence, and one active mutation lease or equivalent serialization mechanism.

## 2. Scope

### 2.1 Included scope

- Sensitive host mutations required by active component, profile, artifact, release, security, recovery, and operations contracts.
- Node-local system, service, governance, and knowledge artifact staging and activation.
- Declared encrypted-volume lifecycle.
- Node-scoped key rotation without raw-key export.
- Allowlisted service-group restart.
- Verified offline-bundle import.
- Recovery-target entry.
- Rollback, revert, restore, reconstruction, and forward repair.
- Authorized bounded node-evidence export.
- Final node-local validation of local, administrator, control-plane, and offline requests.
- Idempotency, replay protection, timeouts, queues, resource bounds, receipts, health, readiness, backup, restore, and rebuild of broker-owned state.
- Break-glass operation classes when an active policy and profile permit them.

### 2.2 Excluded scope

- Ordinary application operations owned by application components.
- Governance policy decisions.
- Resource allocation policy.
- Identity and trust-root ownership.
- Artifact contents, release approval, or compatibility definition.
- Component source data, application databases, and publication authority.
- Generic shell, file-transfer, package-manager, service-manager, container, device, network, or private-key interfaces.
- General remote administration.
- User-interface implementation.
- A mandatory Linux daemon, systemd, polkit, SELinux, sudo, D-Bus, Unix-socket, Kubernetes, or container-runtime implementation.
- Native or external AI control.

### 2.3 Applicability

The architectural uniqueness rule is global. Deployment of the broker and its enabled operation classes remains profile-conditioned.

A profile can omit all privileged mutation capability. A profile that permits any covered sensitive host mutation routes it through the registered broker and cannot add another ordinary path.

A separate Publication Gateway, UCKK Dimension Gateway, Resource Governor, Governance Policy Runtime, Audit Broker, or Identity and Trust component is not a second privileged broker because those components retain separate authority and do not expose generic host mutation.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-SYS-001`
- `DEC-SYS-001`

### 3.2 Canonical architecture

- `contracts/system.contract.json#/global_boundaries/privilege`
- `contracts/system.contract.json#/critical_transitions`
- `contracts/system.contract.json#/degradation_baseline`
- `contracts/system.contract.json#/resource_governance`
- `generated/component-catalog.json#/components/koa_node_agent`
- `contracts/components/koa-node-agent.component.json`
- `generated/profile-catalog.json`
- `contracts/artifact-classes.contract.json`

### 3.3 Related decisions

- `DEC-SYS-001`
- `DEC-PROFILE-001`
- `DEC-DATA-001`
- `DEC-GOV-001`
- `DEC-REL-001`
- `DEC-CONTAINER-001`
- `DEC-K8S-001`
- `DEC-AI-001`

### 3.4 Related requirements

- `REQ-COMP-NODE-001`
- `REQ-COMP-NODE-002`
- `REQ-COMP-NODE-003`
- `REQ-COMP-NODE-004`
- `REQ-COMP-NODE-005`
- `REQ-COMP-NODE-006`
- `REQ-COMP-NODE-007`
- `REQ-COMP-NODE-008`
- `REQ-COMP-NODE-009`
- `REQ-COMP-NODE-010`
- `REQ-COMP-NODE-011`
- `REQ-COMP-NODE-012`
- `REQ-COMP-NODE-013`
- `REQ-COMP-NODE-014`
- `REQ-COMP-NODE-015`
- `REQ-COMP-NODE-016`
- `REQ-COMP-NODE-017`
- `REQ-COMP-NODE-018`
- `REQ-COMP-NODE-019`
- `REQ-COMP-NODE-020`
- `REQ-COMP-NODE-021`
- `REQ-COMP-NODE-022`
- `REQ-COMP-NODE-023`
- `REQ-COMP-NODE-024`

### 3.5 Related locks

- `LOCK-SYS-001`
- `LOCK-SYS-002`
- `LOCK-SYS-003`
- `LOCK-SYS-004`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-DATA-001`
- `LOCK-GOV-001`
- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`
- `LOCK-AI-001`
- `LOCK-AI-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

The system architecture assigns ordinary application operation authority to the owning component. Sensitive host mutations require applicable policy, a narrow privileged operation path, and profile authorization. Root or host-administrator identity is explicitly not the application governance interface.

The kOA Node Agent contract already defines the component class `node_local_lifecycle_and_privileged_operation_broker`, lists `ADR-012`, and rejects arbitrary shell, service-manager, file, package, container, device, and private-key interfaces.

The architecture also separates:

- Governance Policy Runtime from Resource Governor;
- control-plane desired state from target authority;
- release definition from activation execution;
- identity and trust from privileged execution;
- Audit Broker evidence handling from source authority;
- component data ownership from storage or host administration.

### 4.2 Problem statement

Host mutation requires elevated operating-system capability. If each component, deployment tool, administrator, orchestrator, recovery script, and control-plane service receives its own elevation path, kOA cannot demonstrate a single authorization boundary or prove which semantics were applied.

Multiple privilege paths create:

- inconsistent authorization;
- duplicate or conflicting mutations;
- unclear idempotency;
- nonuniform receipts;
- broader attack surface;
- incomplete rollback;
- hidden emergency bypasses;
- profile drift;
- direct component-data access;
- implementation lock-in;
- operator confusion;
- difficult incident reconstruction.

A generic privileged daemon reduces the number of processes but does not solve the problem when it accepts arbitrary commands, paths, files, packages, service names, devices, or container arguments.

### 4.3 Why a decision is required

This decision changes or constrains:

- component topology;
- host mutation authority;
- profile composition;
- policy and identity dependencies;
- control-plane containment;
- operation schemas;
- failure behavior;
- resource control;
- break-glass architecture;
- receipts and evidence;
- recovery;
- implementation recipes;
- conformance and release gates.

The decision therefore belongs in an ADR rather than an implementation guide.

### 4.4 Threats addressed

- Compromised component invoking arbitrary root behavior.
- Control plane bypassing target validation.
- Administrator identity being mistaken for application authorization.
- Command injection through operation parameters.
- Path traversal and arbitrary file replacement.
- Unbounded service-manager or package-manager access.
- Container-runtime escape becoming application authority.
- Replayed or changed requests under the same identity.
- Concurrent conflicting mutations.
- Partial activation or recovery.
- Missing receipts.
- Emergency procedures becoming permanent ordinary paths.
- AI-generated operations or recovery commands becoming authoritative.
- Hidden alternate privilege after broker failure.

### 4.5 Constraints

- The broker cannot become policy, release, trust-root, data, resource, or publication authority.
- Operation classes remain finite, registered, versioned, and testable.
- Every mutating request has a declared recovery strategy.
- Final validation occurs on the target node.
- Broker unavailability cannot open an alternate path.
- Profiles own operation availability and implementation requirements.
- Critical host mutations produce receipts.
- The design supports disconnected operation where the profile claims it.
- The design remains implementation-neutral.
- Break-glass remains separate and more restrictive than ordinary operation.

## 5. Decision Drivers

1. One auditable privilege boundary per node.
2. Least privilege at operation and parameter level.
3. Explicit separation between authorization and execution.
4. Target-local final validation.
5. Elimination of generic privileged command surfaces.
6. Idempotent, replay-safe, expected-state-bound mutation.
7. Atomic activation and complete recovery behavior.
8. Consistent receipts and incident reconstruction.
9. Safe operation without a control plane.
10. Profile-specific membership without implementation leakage.
11. Bounded resource use and mutation serialization.
12. Ability to strengthen controls under high-assurance overlays.
13. Absence of native or external AI authority.
14. Replaceable implementation beneath a stable component contract.

## 6. Considered Options

| Option | Architecture | Decision | Rationale |
| --- | --- | --- | --- |
| `A` | Single logical node-local broker with closed operation classes | `Selected` | Creates one auditable, testable, profile-aware path while preserving external authority separation. |
| `B` | Separate privileged helper for each component | `Rejected` | Multiplies root-capable surfaces, policy interpretations, receipts, recovery paths, and bypass risk. |
| `C` | Generic root daemon, remote shell, or administrative command runner | `Rejected` | Exposes an unbounded command surface that cannot preserve operation semantics or least privilege. |
| `D` | Control plane directly mutates managed hosts | `Rejected` | Treats coordination identity as target authority and removes node-local final validation. |
| `E` | Container-runtime or Kubernetes administration as the privilege interface | `Rejected` | Infrastructure administration does not encode application, policy, release, or data authority. |
| `F` | Ad hoc sudo, polkit, scripts, service units, and package hooks | `Rejected as architecture` | These mechanisms can implement bounded internals but cannot be the public authority or operation contract. |

### 6.1 Selected option details

The selected option places operation semantics in versioned contracts rather than command strings.

A request identifies an operation class and provides only fields permitted by that operation schema. The broker validates the complete request and invokes a bounded implementation that cannot widen the operation scope.

The broker can internally use operating-system facilities such as capabilities, systemd units, polkit, SELinux, AppArmor, namespaces, mount helpers, bootloader tools, cryptographic APIs, or container APIs. Those facilities remain implementation mechanisms and are not exposed as the kOA authority contract.

### 6.2 Why one logical broker is safer than many helpers

A per-component helper can appear narrow individually while the collection becomes broad. Separate helpers can disagree about:

- caller identity;
- policy expiry;
- profile scope;
- expected state;
- target naming;
- artifact verification;
- replay behavior;
- timeout;
- resource admission;
- receipt format;
- recovery;
- break-glass;
- offline behavior.

One logical broker centralizes these cross-cutting mutation controls without taking ownership of component semantics.

## 7. Decision

### 7.1 Selected architecture

`single_logical_node_local_narrow_privileged_broker`

### 7.2 Registered component

- Component ID: `koa_node_agent`
- Contract: `contracts/components/koa-node-agent.component.json`
- Component class: `node_local_lifecycle_and_privileged_operation_broker`
- ADR linkage: `ADR-012`

### 7.3 Meaning of “single”

A node authority domain has exactly one active logical broker identity.

The implementation can use:

- one process;
- a supervised process with restart;
- active-passive replicas;
- a small front end plus isolated operation-specific executors;
- an active lease over shared durable operation state.

It cannot use multiple independently authoritative brokers, independent operation registries, independent idempotency stores, or concurrent mutation authorities.

Only one broker instance or elected authority executes mutating operations at a time unless an operation contract proves safe independent parallelism. The default mutating concurrency is one.

### 7.4 Required request binding

Every operation request binds:

- operation ID and schema version;
- canonical request ID;
- correlation ID;
- authenticated caller identity;
- caller component or control-plane identity;
- active node identity;
- primary profile and overlays;
- authorization class;
- applicable policy decision when required;
- policy validity and expiry;
- target or artifact identities;
- expected current state;
- bounded parameters;
- deadline and timeout;
- idempotency behavior;
- resource requirements;
- receipt policy;
- failure and recovery behavior.

### 7.5 Required validation

Before invoking privilege, the broker validates:

- operation registration;
- request schema;
- caller identity and scope;
- node and profile context;
- policy decision and expiry when applicable;
- target allowlists;
- parameter and path allowlists;
- expected state;
- artifact identity, integrity, trust, compatibility, and provenance where applicable;
- replay and idempotency state;
- resource admission;
- staging and recovery capacity;
- conflicting active operations;
- timeout and cancellation state;
- receipt availability for critical transitions.

### 7.6 Closed operation registry

The active contract currently includes:

| Operation ID | Purpose | Mutates host | Authorization class | Receipt policy |
| --- | --- | ---: | --- | --- |
| `inspect_node_state` | Return bounded node identity, active profile, booted release, active Release Set, health, readiness, and recovery state. | `no` | `node_inspection` | `optional_unless_profile_or_security_policy_requires` |
| `stage_system_artifact` | Stage a validated system image or equivalent system-channel artifact without activating it. | `yes` | `system_artifact_staging` | `required` |
| `activate_system_artifact` | Activate a staged verified system artifact through an atomic boot slot, pointer, or equivalent profile-defined transition. | `yes` | `system_artifact_activation` | `required` |
| `activate_service_bundle` | Activate a compatible services-channel bundle using a complete profile-authorized transition. | `yes` | `service_bundle_activation` | `required` |
| `activate_governance_bundle` | Activate an accepted and compatible governance policy bundle without creating or changing policy authority. | `yes` | `governance_bundle_activation` | `required` |
| `manage_knowledge_artifact` | Install, activate, pin, unpin, quarantine, or revert a registered knowledge artifact when permitted by its class and profile. | `yes` | `knowledge_artifact_lifecycle` | `required_for_activation_quarantine_or_revert` |
| `import_offline_bundle` | Admit a verified offline bundle into quarantine or staging for controlled local validation and activation. | `yes` | `offline_bundle_import` | `required` |
| `manage_declared_encrypted_volume` | Create, unlock, mount, unmount, rotate, or retire a profile-declared encrypted volume through a closed operation schema. | `yes` | `encrypted_volume_lifecycle` | `required` |
| `restart_allowlisted_service_group` | Restart one profile-declared service group after validation of current state, dependency conditions, and authorization. | `yes` | `service_group_control` | `required_when_critical` |
| `rotate_node_scoped_key` | Perform a governed rotation of one node-scoped key without exporting raw private-key material. | `yes` | `node_key_rotation` | `required` |
| `export_node_evidence` | Export an authorized bounded node-evidence package through the applicable audit and disclosure path. | `no` | `node_evidence_export` | `required` |
| `enter_recovery_target` | Transition the node into a profile-defined recovery environment or mode. | `yes` | `node_recovery` | `required` |
| `execute_rollback_or_forward_repair` | Apply the declared recovery strategy for a failed activation or migration. | `yes` | `node_recovery` | `required` |

Adding or changing an operation class is a semantic contract change. It requires accepted authority, compatibility analysis, security review, operation-schema versioning, tests, evidence, and recovery behavior.

### 7.7 Prohibited interfaces

The broker does not expose:

- arbitrary shell commands;
- arbitrary command-line argument forwarding;
- arbitrary environment variables;
- arbitrary service-manager unit names;
- arbitrary file copy, path traversal, or filesystem mutation;
- generic package-manager operations;
- arbitrary container image, entrypoint, command, volume, device, or privilege arguments;
- unrestricted network reconfiguration;
- unrestricted device access;
- raw private-key export;
- direct application-database writes;
- arbitrary script upload and execution;
- remote desktop or generic root session;
- operation selection or parameterization by AI.

### 7.8 Authority separation

The broker executes only after external authorities provide their owned decisions:

- owning components define ordinary application semantics;
- Governance Policy Runtime supplies policy decisions where deployed and required;
- Identity and Trust supplies identities, trust, signatures, and revocation;
- artifact and release contracts define artifacts and compatibility;
- profiles define operation availability;
- Resource Governor supplies resource admission and limits;
- Audit Broker handles selective evidence;
- control plane supplies coordinated desired state but not unilateral authority.

The broker independently accepts or rejects the request against target-local state.

### 7.9 Idempotency and replay

Equivalent repeated requests using the same request ID return the recorded result.

Reuse of a request ID with a different canonical request body is rejected.

Expected-state binding prevents a valid old request from mutating a changed node. Expired, cancelled, superseded, or authorization-invalid queued requests do not execute after reconnection or restart.

### 7.10 Receipts

Privileged host mutation and other contract-declared critical transitions produce machine-readable receipts recording:

- request and operation identity;
- caller and broker identity;
- profile context;
- authorization and policy references;
- before and after state;
- artifact or target identities;
- validation results;
- start, completion, and duration;
- result and stable reason codes;
- idempotency result;
- correlation;
- recovery or rollback information;
- audit registration state.

Receipts contain no secrets, raw keys, or unnecessary component data.

### 7.11 Break-glass

Break-glass uses separate operation classes and a separate stronger policy.

It is:

- time-bound;
- actor-bound;
- node-bound;
- scope-bound;
- reason-bound;
- non-reusable;
- receipted;
- subject to post-event review.

Caller UID, root login, physical access, or possession of a generic administrator token is not sufficient break-glass authorization.

### 7.12 Broker failure rule

If the broker is unavailable, privileged host mutations are unavailable. Application components retain their own authority and continue according to their contracts.

No hidden sudo script, control-plane channel, Kubernetes job, package hook, service unit, recovery shell, or second daemon becomes the ordinary fallback.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- ADR owner: `generated/decision-index.json#/adrs/ADR-012`
- Architecture owner decision: `generated/decision-index.json#/decisions/DEC-SYS-001`
- Component owner: `contracts/components/koa-node-agent.component.json`
- Component registry identity: `generated/component-catalog.json#/components/koa_node_agent`

### 8.2 Broker-owned authoritative data

The broker owns only:

- node-agent request identities;
- canonical request bodies needed for replay protection;
- idempotency records;
- operation execution state;
- node-local staging state;
- node-local activation execution state;
- node-local recovery execution state;
- node operation receipts;
- broker health and readiness state;
- broker configuration required for rebuild.

### 8.3 Data the broker does not own

The broker does not own:

- application component records;
- user or tenant data;
- governance policies;
- resource policies;
- trust roots;
- release contents;
- artifact manifests;
- profile membership;
- audit disclosure policy;
- publication decisions;
- control-plane desired state as authority;
- component migration semantics.

### 8.4 Write boundaries

The broker writes only:

- its own operation, idempotency, staging, receipt, and recovery stores;
- profile-declared host targets through one closed operation implementation;
- artifact-class-defined activation pointers, slots, volumes, keys, or recovery state.

It does not write directly to another component's authoritative source tables.

### 8.5 Read boundaries

The broker reads only the minimum required:

- target state;
- profile context;
- identity and trust results;
- policy decisions;
- artifact manifests and verification results;
- resource admission;
- recovery metadata;
- bounded health and evidence state.

Observation does not transfer authority or ownership.

### 8.6 Trust boundaries

A trusted broker binary is not sufficient authorization.

A trusted caller is not sufficient authorization.

A valid policy decision is not sufficient without target-local state validation.

A valid artifact signature is not sufficient compatibility.

Root execution capability is not application governance authority.

### 8.7 Gateway relationships

The broker interacts with:

- Governance Policy Runtime for policy-conditioned authorization;
- Resource Governor for capacity and limits;
- Identity and Trust for identity, trust, signatures, and revocation;
- Audit Broker for selective evidence;
- Publication Gateway only for separately authorized publication;
- control plane for coordinated requests;
- owning components for operation intent and result consumption.

These interactions do not merge component authority.

## 9. Profile and Deployment Effects

| Profile or overlay | Membership | Decision effect | Authority boundary |
| --- | --- | --- | --- |
| `user_lightweight` | Profile-conditioned | The broker is present only when the profile declares sensitive host lifecycle operations that require it. | No sovereign, control-plane, release, or administrator authority is inferred. |
| `developer_linux_workstation` | Permitted | The broker can support closed local lifecycle and test operations without replacing ordinary developer tooling. | Development convenience cannot widen the production operation registry. |
| `developer_windows_wsl` | WSL-scoped and profile-conditioned | A Linux-side broker can operate only inside the declared WSL environment and cannot mutate the Windows host through an implicit path. | Windows administrator identity and WSL integration are not application authority. |
| `sovereign_linux_node` | Required when the profile enables privileged lifecycle | The broker owns the sole node-local path for system activation, protected storage, recovery, key rotation, and other registered host mutations. | Direct root, package-manager, service-manager, or orchestration bypass is excluded. |
| `sovereign_hub` | Profile-conditioned | The hub contract selects required operation classes and resource limits explicitly. | Similarity to a sovereign node does not create implicit membership. |
| `build_farm` | Profile-conditioned | A broker may manage the worker host through closed operations, but build and signing authority remain separate. | Build-worker identity cannot approve or activate releases. |
| `control_plane` | Required by the active profile contract | The local broker protects the control-plane node and also ensures that remote desired state is not unilateral authority. | Control-plane administration cannot bypass target-local validation. |
| `high_assurance` | Strengthening overlay | Can require stronger isolation, multi-party authorization, hardware-backed keys, stricter receipt handling, and enhanced review. | The overlay does not add a second privileged broker. |
| `sovereign_offline` | Strengthening overlay | Requires local trust verification, offline bundle admission, local recovery, and delayed receipt aggregation. | Disconnected operation cannot expand operation scope. |
| `appliance_shell` | No direct authority effect | The shell can call registered operations through normal authorization. | A restricted user interface is not itself the privileged boundary. |

### 9.1 Profile contract requirements

A profile that enables the broker defines:

- required or optional membership;
- enabled operation classes;
- implementation path;
- privilege mechanism;
- hardware and storage prerequisites;
- network and offline behavior;
- recovery target;
- resource envelope;
- receipt retention;
- break-glass availability;
- required tests and evidence.

The component contract cannot infer profile membership.

### 9.2 Deployment topology

The broker is node-local. A central service can coordinate requests but does not replace the target broker.

A cluster can have one broker authority per managed node. “Single” does not mean one global broker for every node.

Shared active-passive broker infrastructure on one node must preserve one logical identity and operation state. Split-brain mutation authority is prohibited.

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

The decision reduces privileged attack surface by replacing generic interfaces with closed operations.

Security controls include:

- component-scoped broker identity;
- profile-defined privileged execution identity;
- minimum required privilege;
- caller authentication;
- authorization binding;
- policy expiry;
- replay protection;
- expected-state checks;
- request idempotency;
- parameter, path, service-group, and device allowlists;
- operation timeouts;
- bounded resources;
- atomic transitions;
- recovery;
- receipts;
- no raw-key export.

Implementation hardening can include:

- dedicated operating-system identity;
- local Unix socket;
- authenticated IPC;
- systemd sandboxing;
- SELinux or AppArmor confinement;
- minimal Linux capabilities;
- `no_new_privileges`;
- protected system paths;
- private temporary storage;
- restricted address families;
- seccomp;
- mount namespaces;
- read-only executable content;
- measured or verified broker binary.

These are implementation controls, not substitutes for the operation contract.

### 10.2 Privacy and disclosure effects

The broker receives only data required to validate and execute the operation. It does not ingest general application content.

Receipts and health output minimize:

- user identities;
- tenant identifiers;
- paths;
- component data;
- environment details;
- secrets;
- keys;
- protected configuration.

Evidence export is a separate authorized operation and follows disclosure policy.

### 10.3 Rights, consent, and cultural authority

The broker cannot infer consent, disclosure rights, cultural authority, or publication permission from host access.

Operations affecting protected content require the owning component and applicable policy decision. The broker executes the bounded host effect only.

### 10.4 AI effects

The decision introduces no native AI.

ChatGPT, Suno, Gamma, Ariane voice, or any external AI can help a human understand a failure report or draft a candidate operation proposal. AI cannot:

- select the operation class;
- authorize the caller;
- create policy authority;
- choose target paths or devices;
- change parameters after authorization;
- acknowledge success;
- validate recovery;
- approve break-glass;
- become a receipt signer;
- substitute for deterministic checks.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline operation

Where the active profile permits it, the broker supports:

- local inspection;
- local recovery;
- continued previously valid local operation;
- verified offline-bundle import;
- local artifact verification;
- local receipts;
- later authorized evidence aggregation.

Offline operation cannot expand operation or policy scope. New remote desired state is unavailable without connectivity. Queued remote requests remain bounded, visible, expiring, idempotent, and subject to complete revalidation.

### 11.2 Resource behavior

Resource Governor bounds:

- concurrent requests;
- mutating-operation concurrency;
- verification workers;
- CPU and memory;
- I/O and network;
- staging and temporary storage;
- receipt queues;
- logs and diagnostics;
- recovery work.

The default maximum parallel mutating operations is one.

Under pressure, the broker:

1. rejects invalid or oversized new work;
2. reduces verification concurrency;
3. pauses new activations;
4. preserves an active atomic transition;
5. preserves receipts and idempotency state;
6. preserves recovery capacity;
7. prioritizes inspection and recovery;
8. enters inspection-only mode before integrity risk.

### 11.3 Health and readiness

Health reports:

- component state;
- enabled operation classes;
- active request;
- active operation;
- idempotency-store state;
- receipt-generation state;
- staging capacity;
- artifact-verification state;
- recovery-path state;
- resource pressure;
- last successful critical transition.

The broker is not ready for mutating operations when required identity, profile, policy, verification, receipt, or recovery dependencies are unavailable.

### 11.4 Operational failure matrix

| Failure state | Required response | Preserved state | Blocked behavior |
| --- | --- | --- | --- |
| Unregistered operation class | Reject the request before any host mutation. | Host and broker state | Best-effort command interpretation |
| Malformed or unsupported request version | Reject with a stable schema or version error. | Recorded prior results | Schema guessing or implicit conversion |
| Caller identity unavailable or invalid | Block the affected operation. | Current valid host state | Anonymous or UID-only authorization |
| Policy decision missing, expired, revoked, or scope-mismatched | Fail closed for policy-conditioned operations. | Inspection or independently authorized behavior when declared | Allow-by-default execution |
| Profile does not permit the operation | Reject without invoking the privileged implementation. | Active profile and host state | Inferring permission from installed software |
| Expected state mismatch | Return conflict and leave the host unchanged. | Current authoritative state | Executing against stale assumptions |
| Request ID reused with a different body | Reject the replay and preserve the original result. | Idempotency record | Changing parameters under an accepted identity |
| Artifact, signature, trust, or compatibility failure | Block staging or activation and preserve the previous valid state. | Current release and recovery path | Partial or substituted artifact |
| Receipt generation failure | Do not record the critical transition as successful; enter recovery or operator review. | Operation evidence and prior state | Unreceipted success claim |
| Resource pressure | Serialize or pause mutations and prioritize active-transition integrity, inspection, receipts, and recovery. | Recoverable node state | Unbounded concurrency or queue growth |
| Control plane unavailable | Preserve existing local authority and block or visibly defer unsupported new remote changes. | Previously valid local operation | Hidden remote fallback |
| Governance Policy Runtime unavailable | Fail closed for policy-conditioned operations. | Resource governance and profile-permitted inspection | Policy bypass |
| Broker unavailable | Make privileged host mutations unavailable and preserve application-component authority. | Application data and current host state | Alternate hidden privileged path |
| Activation or recovery failure | Preserve or restore the previous valid state through the declared strategy. | Receipts, recovery data, and unaffected capabilities | Partial authoritative state |
| Break-glass dependency unavailable | Keep ordinary operations unchanged and require the separate emergency procedure. | Normal broker authority | Reusing an ordinary operation as emergency access |

### 11.5 Startup and shutdown

Startup verifies:

- configuration;
- broker identity;
- profile context;
- operation registry;
- idempotency store;
- receipt generation;
- staging paths;
- recovery paths;
- resource envelope;
- absence of a conflicting active broker authority.

Shutdown stops new mutations, safely completes or aborts active transitions, persists idempotency and receipt state, and leaves the host in a complete valid state.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`conditionally_compatible`

The decision is globally compatible with kOA because it constrains the privilege architecture. Deployment remains profile-conditioned.

A second ordinary privileged broker, generic privileged command interface, or direct control-plane mutation path is incompatible.

### 12.2 Component compatibility

Broker versions are compatible only when they preserve:

- component identity;
- operation IDs and schema versions;
- request canonicalization;
- idempotency semantics;
- stable result and error codes;
- receipt schema;
- profile and policy binding;
- recovery behavior;
- broker-owned state migration;
- authority boundaries.

An operation semantic change requires a new schema or operation version and explicit migration.

### 12.3 Request compatibility

Requests include an operation and schema version. Unsupported versions fail explicitly.

The broker does not accept the nearest known version, remove unrecognized fields silently, or infer missing authority fields.

### 12.4 Receipt compatibility

Receipt evolution preserves:

- request identity;
- operation identity;
- caller;
- authorization;
- before and after state;
- target identity;
- result;
- timing;
- correlation;
- recovery relationship.

Historical receipt readers remain available for retained records.

### 12.5 Lifecycle states

The broker supports:

- uninitialized;
- starting;
- ready;
- degraded;
- inspection-only;
- activating;
- recovering;
- stopping;
- unavailable.

A broker version can be deprecated, superseded, revoked, or archived without reusing its identity.

### 12.6 Deprecation effects

Generic privileged interfaces and duplicate helper authorities are deprecated as architecture.

A migration can retain deprecated scripts only behind a registered closed operation implementation during a bounded transition. They are not directly callable by ordinary components or operators.

### 12.7 Release effects

Broker binaries and operation registries are release artifacts under the applicable channel and profile contracts.

Activation requires compatibility, recovery, target-local validation, and receipts. A valid broker artifact does not change the operation registry or profile permission by itself.

## 13. Migration Plan

### 13.1 Preconditions

- Accepted `DEC-SYS-001`.
- Active kOA Node Agent component contract.
- Registered profile contracts.
- Complete inventory of privileged host mutations.
- Identity, policy, resource, audit, and recovery dependencies.
- Operation-schema and receipt contracts.
- Broker state storage and backup plan.
- Tests for current and proposed privilege surfaces.
- Recovery and break-glass procedures.

### 13.2 Inventory deprecated privilege paths

Inventory:

- sudoers entries;
- polkit actions;
- root services;
- setuid or file-capability binaries;
- configuration-management agents;
- remote shells;
- SSH forced commands;
- systemd socket and D-Bus privileged services;
- package hooks;
- container sockets;
- Kubernetes node agents;
- device helpers;
- backup and restore scripts;
- update scripts;
- recovery media;
- administrator runbooks;
- component-specific root helpers.

Each path receives an owner, callers, inputs, outputs, target state, authority source, resource use, receipt behavior, recovery behavior, and disposition.

### 13.3 Classify each path

Disposition is one of:

- ordinary component operation with no host privilege;
- registered broker operation;
- implementation detail behind a registered operation;
- separate publication or data gateway;
- break-glass-only procedure;
- prohibited and removed;
- historical and archived.

No path remains unclassified.

### 13.4 Define operation classes

For every retained mutation:

1. define one semantic operation;
2. define request and result schemas;
3. bind the authorization class;
4. define profile membership;
5. define expected-state checks;
6. define target and parameter allowlists;
7. define timeout and cancellation;
8. define idempotency and replay behavior;
9. define resource admission;
10. define receipt fields;
11. define failure and recovery;
12. register tests and evidence.

### 13.5 Migrate callers

Callers stop invoking operating-system privilege directly.

They submit a versioned request using the broker interface and consume the structured result and receipt reference.

Control-plane callers retain desired-state coordination but accept target rejection.

### 13.6 Disable alternate paths

After equivalent broker operations pass validation:

- remove direct sudo permissions;
- disable generic root APIs;
- close container sockets to application components;
- remove arbitrary service-manager access;
- remove package-manager access;
- revoke obsolete helper identities;
- disable direct script execution;
- archive deprecated runbooks;
- verify filesystem, service, IPC, and network absence.

### 13.7 Migrate break-glass

Emergency procedures move to separate operation classes or an isolated recovery environment with stronger authorization, expiration, receipt, and review.

Emergency access is not included in ordinary client libraries.

### 13.8 Cutover

1. Stage the broker version and operation registry.
2. verify broker identity and state stores;
3. disable new requests through deprecated paths;
4. drain or cancel existing deprecated work;
5. activate the broker;
6. validate every enabled operation;
7. verify no alternate path remains;
8. preserve rollback to the previous broker version;
9. register migration evidence.

### 13.9 deprecated disposition

deprecated privilege documentation is retained as migration evidence. Active documentation points to this ADR and the Node Agent contract.

Operation-specific deprecated scripts can remain only as inaccessible implementation internals during a bounded compatibility period.

## 14. Rollback and Forward Repair

### 14.1 Rollback unit

The rollback unit includes:

- broker binary and runtime configuration;
- operation registry;
- request and result schemas;
- idempotency-store schema;
- receipt schema and queue state;
- staging and recovery configuration;
- active profile bindings;
- client compatibility declarations.

Rollback does not restore generic privileged interfaces.

### 14.2 Rollback triggers

- broker cannot start or authenticate;
- operation registry is invalid;
- idempotency store cannot be read safely;
- receipt generation is unavailable;
- required recovery path is invalid;
- target-local validation is incorrect;
- an operation exceeds its declared scope;
- duplicate active broker authority is detected;
- a mutating transition leaves an invalid state;
- profile or caller compatibility fails.

### 14.3 Rollback procedure

1. Stop new mutating requests.
2. preserve the active request and receipt state.
3. complete or recover the active atomic transition.
4. verify the previous broker artifact and state compatibility.
5. restore the previous broker version and operation registry.
6. reconcile idempotency records and queued requests.
7. revalidate profile, identity, policy, resource, staging, and recovery dependencies.
8. confirm one active logical broker.
9. run operation-surface and no-bypass tests.
10. record rollback evidence.

### 14.4 Forward repair

Forward repair uses a new validated broker artifact, operation-schema migration, or state repair procedure.

It preserves request identities and receipts and cannot reinterpret a failed request as successful.

A local shell patch is not durable forward repair. Any emergency change is captured in a reviewed artifact or configuration release before ordinary readiness returns.

### 14.5 Broker rebuild

A broker can be rebuilt from:

- verified system and release artifacts;
- active profile;
- protected configuration;
- idempotency records;
- receipts;
- staging manifests;
- active and previous release identity;
- recovery tokens;
- encrypted-volume lifecycle state.

Rebuild validation proves that no duplicate active authority or replay ambiguity exists.

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `generated/impact/IMPACT-2026-08-03-ADR-012.json`

### 15.2 Modified or constrained canonical references

- `generated/decision-index.json#/adrs/ADR-012`
- `generated/component-catalog.json#/components/koa_node_agent`
- `contracts/components/koa-node-agent.component.json`
- `contracts/system.contract.json#/global_boundaries/privilege`
- `generated/profile-catalog.json`
- `generated/test-catalog.json#/tests/TEST-ADR-012-001`
- `generated/traceability.json#/adrs/ADR-012`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-CONST-003` | `reviewed_no_change` | Already defines the narrow privileged operation path and authority separation. |
| `DOC-SYS-000` | `reviewed_no_change` | Already routes policy authorization to a privileged broker without transferring execution authority. |
| `DOC-COMP-011` | `updated` | Owns the concrete Node Agent component contract and closed operation model. |
| `DOC-SEC-010` | `updated` | Uses the broker for protected volume, key, mount, restore, and storage lifecycle mutations. |
| `DOC-OPS-007` | `updated` | Defines broker failure, policy failure, resource pressure, inspection-only state, and restoration. |
| `DOC-LIFE-017` | `updated` | Applies compatibility and deprecation to operation schemas and broker versions. |
| `DOC-CONF-012` | `reviewed_no_change` | Generated operation tables and profile projections remain canonical-source projections. |
| `DOC-CONF-019` | `updated` | Release gates validate the broker contract, operation surface, receipts, recovery, and profile evidence. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-SYS-001` | `unchanged` | Preserves explicit authority and local-first system behavior. |
| `LOCK-PROFILE-001` | `unchanged` | Keeps broker membership and implementation profile-scoped. |
| `LOCK-PROFILE-002` | `unchanged` | Requires explicit compatible overlays. |
| `LOCK-DATA-001` | `unchanged` | Prevents the broker from owning or writing component source data. |
| `LOCK-GOV-001` | `unchanged` | Keeps policy authority and resource authority separate from execution. |
| `LOCK-COMP-001` | `unchanged` | Requires exclusive component ownership and versioned contracts. |
| `LOCK-COMP-002` | `unchanged` | Forbids implicit cross-component authority. |
| `LOCK-LIFE-001` | `unchanged` | Requires lifecycle, receipts, and recovery for critical transitions. |
| `LOCK-LIFE-002` | `unchanged` | Forbids partial authoritative activation. |
| `LOCK-AI-002` | `unchanged` | Prevents AI output from controlling privileged operations. |
| `LOCK-IMPL-001` | `unchanged` | Keeps systemd, polkit, SELinux, capabilities, sockets, and similar mechanisms as implementation choices. |
| `LOCK-IMPL-002` | `unchanged` | Prevents one Linux privilege implementation from becoming universal. |

### 15.5 Affected requirements

| Requirement ID | Disposition | Validation effect |
| --- | --- | --- |
| `REQ-COMP-NODE-001` | `unchanged` | Defines the closed registered operation surface. |
| `REQ-COMP-NODE-002` | `unchanged` | Excludes arbitrary privileged interfaces. |
| `REQ-COMP-NODE-004` | `unchanged` | Binds requests to identity, profile, policy, target, expected state, and deadline. |
| `REQ-COMP-NODE-005` | `unchanged` | Requires target-local final validation. |
| `REQ-COMP-NODE-006` | `unchanged` | Rejects root, administrator, orchestration, and control-plane identity as sufficient authority. |
| `REQ-COMP-NODE-007` | `unchanged` | Requires idempotent repeated-request behavior. |
| `REQ-COMP-NODE-010` | `unchanged` | Requires atomic mutating transitions. |
| `REQ-COMP-NODE-013` | `unchanged` | Requires receipts for privileged host mutations and critical transitions. |
| `REQ-COMP-NODE-016` | `unchanged` | Requires the profile-authorized narrow privilege path and minimum privilege. |
| `REQ-COMP-NODE-017` | `unchanged` | Separates break-glass operations and strengthens their authorization and review. |
| `REQ-COMP-NODE-019` | `unchanged` | Defines safe resource-pressure behavior. |
| `REQ-COMP-NODE-022` | `unchanged` | Excludes native and external AI authority. |

### 15.6 Generated artifacts

Semantic changes require regeneration of:

- ADR index;
- component catalog;
- Node Agent operation table;
- profile membership and capability matrices;
- privilege-boundary diagrams;
- operation-schema catalog;
- security and threat-model projections;
- test catalog;
- receipt-class catalog;
- traceability graph;
- release-gate matrix;
- AI context packages for system, components, security, operations, and conformance.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-ADR-012-001` | Verify that exactly one logical privileged-broker component identity is active per node authority domain. | `pass` |
| `TEST-ADR-012-002` | Verify that every exposed operation is registered, versioned, schema-bound, and closed. | `pass` |
| `TEST-ADR-012-003` | Reject arbitrary shell, file, package, service-manager, container, device, and private-key interfaces. | `pass` |
| `TEST-ADR-012-004` | Verify authenticated caller, active profile, policy, target, expected state, deadline, correlation, and resource validation. | `pass` |
| `TEST-ADR-012-005` | Verify target-local final validation for local, administrator, and control-plane requests. | `pass` |
| `TEST-ADR-012-006` | Verify idempotent repeated requests and rejection of request-identity reuse with a changed body. | `pass` |
| `TEST-ADR-012-007` | Verify parameter, path, service-group, device, artifact, and action allowlists. | `pass` |
| `TEST-ADR-012-008` | Verify atomic activation and absence of partial authoritative host state. | `pass` |
| `TEST-ADR-012-009` | Verify complete machine-readable receipts for privileged host mutations and critical transitions. | `pass` |
| `TEST-ADR-012-010` | Verify that component data ownership, policy authority, resource authority, release authority, and trust-root authority remain external. | `pass` |
| `TEST-ADR-012-011` | Verify resource admission, serialization of mutations, bounded queues, timeouts, and inspection-only degradation. | `pass` |
| `TEST-ADR-012-012` | Verify safe control-plane loss, policy-runtime loss, broker failure, and offline behavior without silent fallback. | `pass` |
| `TEST-ADR-012-013` | Verify separate break-glass operation classes, stronger authorization, expiration, receipts, and post-event review. | `pass` |
| `TEST-ADR-012-014` | Verify backup, restore, rebuild, rollback, and forward-repair without partial authority. | `pass` |
| `TEST-ADR-012-015` | Verify profile membership, overlay strengthening, and absence of implicit global implementation requirements. | `pass` |
| `TEST-ADR-012-016` | Verify that high-availability deployment retains one logical operation authority and serialized mutating state. | `pass` |
| `TEST-ADR-012-017` | Verify absence of native or external AI operation selection, authorization, parameterization, validation, acknowledgement, or recovery authority. | `pass` |
| `TEST-ADR-012-018` | Verify complete decision, requirement, lock, component, profile, operation, receipt, test, and evidence traceability. | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-012-SURFACE` | Operation-surface inventory and arbitrary-interface absence report | `generated/evidence-catalog.json#/evidence/EVID-ADR-012-SURFACE` |
| `EVID-ADR-012-AUTH` | Identity, profile, policy, expected-state, replay, and authorization validation evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-012-AUTH` |
| `EVID-ADR-012-RECEIPT` | Critical-transition receipt completeness and disclosure-minimization evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-012-RECEIPT` |
| `EVID-ADR-012-RECOVERY` | Failure, rollback, restore, forward-repair, and broker-rebuild evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-012-RECOVERY` |
| `EVID-ADR-012-PROFILE` | Profile membership, overlay strengthening, and single-authority validation report | `generated/evidence-catalog.json#/evidence/EVID-ADR-012-PROFILE` |
| `EVID-ADR-012-OFFLINE` | Disconnected operation, offline import, local validation, and delayed evidence aggregation report | `generated/evidence-catalog.json#/evidence/EVID-ADR-012-OFFLINE` |

### 16.3 Required validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/check_privileged_surface.py
python docs/tools/check_operation_schemas.py
python docs/tools/check_receipt_contracts.py
python docs/tools/check_profile_membership.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific acceptance criteria

1. One logical broker identity is active per node authority domain.
2. The component contract lists `ADR-012`.
3. Every exposed operation is registered, closed, versioned, and profile-bound.
4. No generic privileged command, path, file, package, service, container, device, or key interface is available.
5. Every mutating request binds identity, authority, expected state, timeout, resources, receipt, and recovery.
6. Target-local validation applies to control-plane and administrator requests.
7. Equivalent replay returns the original result.
8. Changed replay is rejected.
9. Conflicting mutation is serialized or rejected.
10. Critical transitions have complete minimized receipts.
11. Break-glass is separate and stronger.
12. Broker failure does not expose an alternate path.
13. Offline behavior preserves local authority without scope expansion.
14. High availability preserves one logical authority and state model.
15. AI has no operation authority.
16. All affected objects have a final impact disposition.
17. All required tests pass.
18. Active evidence resolves and remains valid.

## 17. Consequences

### 17.1 Positive consequences

- One explicit privilege boundary.
- Reduced root-capable attack surface.
- Uniform identity and policy binding.
- Uniform expected-state validation.
- Deterministic operation semantics.
- Strong replay protection.
- Consistent receipts.
- Easier incident investigation.
- Easier profile conformance.
- Reliable control-plane containment.
- Safer offline operation.
- Stronger rollback and recovery.
- Replaceable implementation behind stable contracts.

### 17.2 Negative consequences and costs

- The broker becomes a critical operational dependency.
- Operation design and schema review add work.
- New privileged use cases cannot be solved by an immediate arbitrary command.
- Broker state requires backup and migration.
- High availability requires careful single-authority coordination.
- Debugging may be slower than direct root access.
- Existing scripts and tools require adaptation.
- Emergency procedures require separate governance.
- A broker defect can block multiple mutation classes.

### 17.3 Risk treatment

Critical-dependency risk is treated through:

- minimal code and operation surface;
- process supervision;
- active-passive design where needed;
- protected idempotency and receipt state;
- inspection-only mode;
- independent recovery target;
- versioned rollback;
- deterministic rebuild;
- bounded break-glass;
- extensive negative testing.

### 17.4 Operational obligations

- Maintain the operation registry.
- Review every new operation semantically.
- Protect broker identity and state.
- Monitor failed authorization, replay, scope, receipt, and recovery checks.
- Exercise broker rollback and rebuild.
- Verify no alternate privileged path after system changes.
- Rotate broker credentials and trust.
- Retain receipts according to policy.
- Test control-plane and policy-runtime outages.
- Audit break-glass usage.
- Keep resource limits and staging capacity current.

### 17.5 Documentation obligations

- Keep this ADR, system privilege boundary, Node Agent contract, profiles, security policies, operations runbooks, test catalog, evidence, traceability, and release gates aligned.
- Regenerate operation and profile projections after canonical changes.
- Preserve historical operation schemas and receipt readers.
- Record implementation mechanisms separately.
- Keep rejected alternatives and reconsideration triggers current.

### 17.6 Technical debt explicitly accepted

The first implementation may use one Linux-specific broker implementation and one IPC mechanism.

This is acceptable only while:

- the component contract remains implementation-neutral;
- operation semantics remain portable;
- implementation-specific privilege rules remain profile or recipe scoped;
- no client depends on shell commands or Linux-specific target names;
- state and receipts can be exported;
- a replacement migration is documented;
- unsupported platforms block rather than approximate.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Per-component privileged helpers | The aggregate surface becomes broad and cannot guarantee common replay, receipts, recovery, or policy binding. | A formally verified composition proves one logical authority, common state, and equivalent attack surface. |
| Generic root daemon | Arbitrary commands and parameters cannot provide closed operation semantics. | None for ordinary operation; a generic shell remains outside the architecture. |
| Direct control-plane mutation | Remote coordination is not sufficient target authority. | None while node-local authority remains a system principle. |
| Kubernetes or container administration | Infrastructure roles do not encode application or policy authority. | A profile can use these mechanisms only behind registered operations. |
| Sudo or polkit as the public API | Rule files grant low-level actions without the complete kOA request, receipt, expected-state, and recovery contract. | They can remain internal implementation mechanisms. |
| SSH forced commands | Command parsing and shell environment remain difficult to constrain and evidence completely. | A forced command can be an internal transport only if it accepts a closed signed request and invokes the broker. |
| Separate emergency root path | Emergency access tends to become an ordinary bypass. | Only a separately governed break-glass or recovery procedure is permitted. |
| AI-generated remediation execution | AI cannot provide deterministic authority, compatibility, or recovery validation. | None under the active AI boundary. |

Rejected alternatives cannot be introduced as undocumented exceptions or convenience paths.

## 19. Exceptions and Waivers

Not applicable.

A bounded exception must identify:

- exact node and profile scope;
- exact missing broker operation;
- affected requirement;
- business and safety reason;
- owner and approvers;
- start and expiry;
- compensating identity, policy, resource, receipt, and recovery controls;
- prohibited expansion;
- migration to a registered operation;
- tests and evidence;
- post-use review.

An exception cannot establish a permanent generic shell, parallel broker, direct cross-component data write, AI authority, or control-plane bypass. It does not change this ADR globally.

## 20. Implementation Guidance

This section is non-normative.

A practical Linux implementation can use:

- a small broker daemon;
- local authenticated Unix-domain socket;
- dedicated service identity;
- operation-specific helper executables;
- systemd service and socket activation;
- SELinux or AppArmor domain;
- minimal Linux capabilities;
- seccomp;
- mount and user namespaces;
- read-only executable paths;
- protected state directories;
- an append-only or integrity-protected receipt store;
- SQLite or another durable local idempotency store;
- file locks, database leases, or consensus-free single-node active leases;
- signed request envelopes for offline workflows.

The public interface should accept structured canonical requests rather than shell strings.

Each operation-specific executor should receive only the validated parameters required for that operation. It should not parse arbitrary extra flags or inherit an uncontrolled environment.

Paths should be symbolic target identities resolved through profile-owned configuration. A request should not supply a raw filesystem path unless the operation schema strictly permits and validates it.

Service control should use profile-declared groups rather than arbitrary unit names.

Container operations, when needed internally, should use fixed image identities, entrypoints, arguments, mounts, devices, capabilities, networks, and resource limits.

A passive replica should not execute mutations. Failover should acquire one active lease and reconcile request, idempotency, receipt, and operation state before reporting readiness.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-SYS-001`
- Decision status: `accepted`
- Decision owner: `system_architecture_authority`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-SYS-001`
- Related profile decision: `DEC-PROFILE-001`
- Related governance decision: `DEC-GOV-001`
- Related release decision: `DEC-REL-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `architecture-migration-author` | `submitted` | `2026-08-03` |
| Canonical owner | `system-architecture-authority` | `approved` | `2026-08-03` |
| Component owner | `koa-node-agent-owner` | `approved` | `2026-08-03` |
| Security reviewer | `security-authority` | `approved` | `2026-08-03` |
| Operations reviewer | `operations-authority` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `documentation-authority` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0012",
  "adr_ids": [
    "ADR-012"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-AI-001"
],
  "modified_canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-012",
    "generated/component-catalog.json#/components/koa_node_agent",
    "contracts/components/koa-node-agent.component.json",
    "contracts/system.contract.json#/global_boundaries/privilege"
  ],
  "requirement_ids": [
    "REQ-COMP-NODE-001",
    "REQ-COMP-NODE-002",
    "REQ-COMP-NODE-003",
    "REQ-COMP-NODE-004",
    "REQ-COMP-NODE-005",
    "REQ-COMP-NODE-006",
    "REQ-COMP-NODE-007",
    "REQ-COMP-NODE-008",
    "REQ-COMP-NODE-009",
    "REQ-COMP-NODE-010",
    "REQ-COMP-NODE-011",
    "REQ-COMP-NODE-012",
    "REQ-COMP-NODE-013",
    "REQ-COMP-NODE-014",
    "REQ-COMP-NODE-015",
    "REQ-COMP-NODE-016",
    "REQ-COMP-NODE-017",
    "REQ-COMP-NODE-018",
    "REQ-COMP-NODE-019",
    "REQ-COMP-NODE-020",
    "REQ-COMP-NODE-021",
    "REQ-COMP-NODE-022",
    "REQ-COMP-NODE-023",
    "REQ-COMP-NODE-024"
],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
],
  "exception_ids": [],
  "test_ids": [
    "TEST-ADR-012-001",
    "TEST-ADR-012-002",
    "TEST-ADR-012-003",
    "TEST-ADR-012-004",
    "TEST-ADR-012-005",
    "TEST-ADR-012-006",
    "TEST-ADR-012-007",
    "TEST-ADR-012-008",
    "TEST-ADR-012-009",
    "TEST-ADR-012-010",
    "TEST-ADR-012-011",
    "TEST-ADR-012-012",
    "TEST-ADR-012-013",
    "TEST-ADR-012-014",
    "TEST-ADR-012-015",
    "TEST-ADR-012-016",
    "TEST-ADR-012-017",
    "TEST-ADR-012-018"
],
  "evidence_ids": [
    "EVID-ADR-012-SURFACE",
    "EVID-ADR-012-AUTH",
    "EVID-ADR-012-RECEIPT",
    "EVID-ADR-012-RECOVERY",
    "EVID-ADR-012-PROFILE",
    "EVID-ADR-012-OFFLINE"
],
  "tests_run": [
    "metadata_parse",
    "adr_section_order",
    "decision_alignment",
    "single_logical_broker",
    "closed_operation_surface",
    "authority_separation",
    "node_local_final_validation",
    "idempotency_and_replay",
    "receipt_completeness",
    "failure_and_recovery",
    "profile_scope",
    "no_ai_authority",
    "no_unresolved_markers"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-ADR-012.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement references `ADR-012`;
4. the original identifier and path remain reserved;
5. historical operation schemas, broker versions, request identities, receipts, migration records, impact reports, tests, evidence, incidents, exceptions, and recovery procedures remain available;
6. active component, profile, security, operations, conformance, and release projections are regenerated;
7. AI context packages stop treating this ADR as current rationale;
8. retired operation IDs and receipt schemas remain preserved where required for audit, replay analysis, recovery, and historical reconstruction;
9. no supersession reuses an operation identity for different semantics.

This ADR remains in the repository after acceptance, deprecation, rejection, or supersession.
