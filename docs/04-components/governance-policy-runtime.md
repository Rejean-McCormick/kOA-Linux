<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-GOV-POL-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component",
  "scope": [
    "component:governance_policy_runtime"
  ],
  "canonical_refs": [
    "generated/component-catalog.json#/components/governance_policy_runtime",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/system.contract.json#/global_capabilities",
    "contracts/system.contract.json#/global_boundaries",
    "contracts/system.contract.json#/degradation_baseline",
    "contracts/system.contract.json#/critical_transitions",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "generated/exception-index.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-SYS-GOV-001",
    "REQ-SYS-GOV-002",
    "REQ-SYS-GOV-003",
    "REQ-SYS-GOV-004",
    "REQ-SYS-GOV-005",
    "REQ-SYS-GOV-006",
    "REQ-SYS-GOV-007",
    "REQ-SYS-GOV-008",
    "REQ-SYS-GOV-009",
    "REQ-SYS-GOV-010",
    "REQ-SYS-GOV-011",
    "REQ-SYS-GOV-012",
    "REQ-SYS-GOV-013",
    "REQ-SYS-GOV-014",
    "REQ-SYS-GOV-015",
    "REQ-SYS-GOV-016",
    "REQ-SYS-GOV-017",
    "REQ-SYS-GOV-018",
    "REQ-SYS-GOV-019",
    "REQ-SYS-GOV-020",
    "REQ-SYS-GOV-021",
    "REQ-SYS-GOV-022",
    "REQ-SYS-GOV-023",
    "REQ-SYS-GOV-024",
    "REQ-SYS-GOV-025",
    "REQ-SYS-GOV-026",
    "REQ-SYS-GOV-027",
    "REQ-SYS-GOV-028",
    "REQ-SYS-GOV-029",
    "REQ-SYS-GOV-030",
    "REQ-SYS-GOV-031",
    "REQ-SYS-GOV-032"
  ],
  "lock_ids": [
    "LOCK-GOV-001",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-AI-002",
    "LOCK-PROFILE-001",
    "LOCK-LIFE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-COMP-000",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-015",
    "DOC-PROFILE-007",
    "DOC-PROFILE-012"
  ],
  "tags": [
    "component",
    "governance-policy-runtime",
    "policy-authority",
    "authorization",
    "disclosure",
    "consent",
    "privilege",
    "exceptions",
    "policy-bundles",
    "decision-receipts",
    "profile-conditioned"
  ]
}
KOA:DOC-META:END -->

# Governance Policy Runtime

> **Component ID:** `governance_policy_runtime`  
> **Contract:** `contracts/components/governance-policy-runtime.component.json`  
> **Contract version:** `1.0.0`  
> **Authority role:** `policy_authority`

## 1. Purpose

Governance Policy Runtime is the kOA component responsible for evaluating governed decisions against the exact active compatible policy set and verified bounded context.

It exists so that authorization, disclosure, consent, privilege, and registered-exception decisions have one explicit policy authority without turning that authority into a universal executor or universal data owner.

Its authoritative results are:

- policy-evaluation results;
- policy obligations;
- policy diagnostics;
- policy decision receipts;
- policy-set activation state.

The component is not responsible for executing the governed operation.

The calling authoritative component, gateway, or privileged execution component applies the result, satisfies applicable obligations, performs or rejects the operation, and owns the resulting state transition.

This division preserves accountability:

```text
verified request and bounded context
                ↓
Governance Policy Runtime
                ↓
decision + obligations + receipt
                ↓
authoritative caller or execution boundary
                ↓
execution result + execution evidence
```

A decision receipt proves that policy evaluation occurred. It does not, by itself, prove that the governed operation was executed correctly.

## 2. Scope

### 2.1 Included responsibilities

The component covers:

- evaluation of registered governance decisions;
- resolution of the active compatible policy set;
- resolution of applicable registered exceptions;
- creation of bounded obligations and diagnostics;
- production and retention of policy decision receipts;
- staging and validation of policy bundles;
- atomic activation and compatible rollback of policy sets;
- health, readiness, degradation, compatibility, and recovery reporting.

The five decision classes are:

- `authorization`;
- `disclosure`;
- `consent`;
- `privilege`;
- `exception`.

### 2.2 Excluded responsibilities

The component does not own:

- product or workflow state;
- publication transport;
- privileged host execution;
- operating-system credentials;
- identity issuance;
- CPU, memory, I/O, queue, concurrency, or scheduling control;
- consent-record creation;
- exception-record creation;
- application audit state;
- requirements or locks;
- external AI inference;
- policy invention when authority is missing.

These responsibilities remain with their registered owners.

### 2.3 Applicable profiles

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/profile_applicability
renderer=component-profile-applicability-v1
-->
| Context | Applicability | Interpretation |
| --- | --- | --- |
| Global baseline | Optional | Registration does not create a universal runtime dependency. |
| Primary profiles requiring the component | `sovereign_linux_node`, `sovereign_hub` | The profile contract owns the exact activation and assurance behavior. |
| Overlays requiring the component | `high_assurance`, `sovereign_offline` | The overlay strengthens local or assurance behavior. |
| Profiles not requiring it by default | `user_lightweight`, `developer_linux_workstation`, `developer_windows_wsl`, `build_farm` | Another active profile claim can still select it explicitly. |
<!-- GENERATED:END -->

The component is profile-conditioned.

Its registration in the component catalog does not make it mandatory for every deployment.

A profile that claims sovereign governance, high-assurance governance, or offline governed operation selects the local policy runtime and its required policy, trust, receipt, recovery, and evidence behavior.

### 2.4 Activation

The contract permits these activation patterns:

- `always_available`;
- `socket_activated`;
- `task_activated`;
- `embedded_behind_registered_interface`.

The active profile owns the selected pattern.

A process that is running but cannot resolve a compatible active policy set, required trust sources, the active authority version, or its receipt path is not ready.

### 2.5 Offline behavior

Offline governed operation uses:

- locally available active policy bundles;
- locally resolvable identity and trust assertions;
- locally available required exception data;
- local decision evaluation;
- local decision receipts or profile-approved evidence buffering;
- local rollback or forward-repair material.

External policy services and external AI services are not required.

## 3. Canonical References

### 3.1 Primary references

```text
generated/component-catalog.json#/components/governance_policy_runtime
contracts/components/governance-policy-runtime.component.json
```

The component registry owns identity and primary responsibility.

The component contract owns observable interfaces, inputs, outputs, state, data domains, failures, events, compatibility, and validation.

### 3.2 Related system authority

```text
contracts/system.contract.json#/global_capabilities
contracts/system.contract.json#/global_boundaries
contracts/system.contract.json#/data_authority
contracts/system.contract.json#/cross_component_communication
contracts/system.contract.json#/degradation_baseline
contracts/system.contract.json#/critical_transitions
```

### 3.3 Related component contracts

```text
contracts/components/identity-and-trust.component.json
contracts/components/audit-broker.component.json
contracts/components/publication-gateway.component.json
contracts/components/koa-node-agent.component.json
contracts/components/resource-governor.component.json
```

### 3.4 Related profile authority

```text
generated/profile-catalog.json
contracts/profiles/sovereign-linux-node.profile.json
contracts/profiles/sovereign-hub.profile.json
contracts/profiles/high-assurance.profile.json
contracts/profiles/sovereign-offline.profile.json
```

### 3.5 Related lifecycle and evidence authority

```text
contracts/release-channels.contract.json
contracts/artifact-classes.contract.json
contracts/artifact-contracts/policy-bundle.schema.json
contracts/artifact-contracts/decision-receipt.schema.json
contracts/artifact-contracts/release-set.schema.json
generated/exception-index.json
generated/test-catalog.json
generated/evidence-catalog.json
```

## 4. Model and Responsibilities

### 4.1 Component identity

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/classification
renderer=component-identity-v1
-->
| Field | Value |
| --- | --- |
| Component ID | `governance_policy_runtime` |
| Contract ID | `component-contract:governance_policy_runtime` |
| Component class | `governance_service` |
| Logical plane | `governance_identity_and_accountability` |
| Authority role | `policy_authority` |
| Native | `true` |
| Profile-conditioned | `true` |
| External service | `false` |
| AI component | `false` |
<!-- GENERATED:END -->

### 4.2 Authority boundary

The component can:

- evaluate registered governance decisions;
- resolve active policy rules;
- resolve registered exception applicability;
- produce obligations and diagnostics;
- produce policy decision receipts;
- stage, validate, activate, and roll back policy sets;
- report health and compatibility.

The component cannot:

- mutate another component's authoritative state;
- execute publication;
- execute privileged host operations;
- issue operating-system privilege;
- allocate resources;
- create consent or exception authority;
- rewrite requirements or locks;
- use external AI as policy authority;
- infer missing authority;
- activate partial policy state.

A positive policy result is bounded to the declared requester, action, target, scope, policy-set version, authority version, context, and validity conditions.

It does not grant a standing credential or transfer ownership.

### 4.3 Decision classes

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/decision_semantics
renderer=policy-decision-class-table-v1
-->
| Decision class | Required context | Boundary |
| --- | --- | --- |
| `authorization` | `verified_requester`, `registered_action`, `target`, `scope`, `component_authority`, `profile_applicability` | `does_not_imply`: `disclosure_permission`, `consent`, `privilege`, `data_ownership` |
| `disclosure` | `source_owner`, `data_or_representation`, `destination`, `audience`, `purpose`, `applicable_consent`, `retention_or_use_constraints` | `execution_component`: `publication_gateway`; `does_not_imply`: `transport_completed`, `destination_owns_source_domain` |
| `consent` | `subject`, `purpose`, `data_scope`, `recipient_or_use_domain`, `duration_or_closure_condition`, `revocation_state`, `evidence_obligations` | `consent_may_be_inferred_from_silence`: `false` |
| `privilege` | `verified_requester`, `target_node_or_resource`, `exact_privileged_operation`, `profile`, `assurance_context`, `duration`, `evidence_requirements` | `execution_component`: `koa_node_agent_or_registered_privileged_broker`; `decision_is_credential`: `false` |
| `exception` | `exception_id`, `affected_requirement_or_lock`, `subject`, `scope`, `activation_condition`, `expiration_or_closure_condition`, `compensating_controls`, `evidence_obligations` | `registered_exception_required`: `true`; `underlying_requirement_mutated`: `false`; `underlying_lock_mutated`: `false` |
<!-- GENERATED:END -->

A decision class does not imply another class.

For example:

- authorization does not imply disclosure permission;
- disclosure permission does not prove transport completion;
- consent does not imply privilege;
- privilege approval is not a credential;
- an applicable exception does not alter the underlying requirement or lock.

### 4.4 Request model

A policy-evaluation request identifies:

- `request_id`;
- `correlation_id`;
- `decision_class`;
- requester;
- action;
- target;
- governed scope;
- policy-set reference;
- authority version;
- bounded evaluation context.

Optional references include applicable exceptions and prior decision receipts.

The context uses the minimum information required for the declared decision.

Undeclared or excessive context is rejected rather than silently retained.

Verified identity and trust assertions come from registered trust sources.

### 4.5 Result model

A policy-evaluation result is one of:

| Result | Meaning |
| --- | --- |
| `allow` | The declared request is permitted within its exact scope when all returned obligations and caller checks are satisfied. |
| `deny` | Active policy resolves the request and does not permit the operation. |
| `blocked` | The component cannot produce an authoritative allow or deny result because required authority, trust, compatibility, context, or evidence is unavailable or invalid. |

The caller verifies correlation, authority version, scope, and validity before enforcement.

A caller unable to satisfy a required obligation treats the operation as blocked.

### 4.6 Obligations

The contract supports obligation categories including:

- data minimization;
- destination restriction;
- secondary approval;
- duration limits;
- a registered privileged path;
- selected audit evidence;
- subject notification;
- compensating controls;
- follow-up review;
- retention limits;
- receipt linkage;
- reevaluation before execution.

An obligation narrows or conditions the declared action.

It does not broaden the original request.

### 4.7 Provided interfaces

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/provided_interfaces
renderer=component-interface-table-v1
-->
| Interface | Name | Kind | Availability | Purpose | Critical |
| --- | --- | --- | --- | --- | --- |
| `IFACE-GOV-POL-001` | `evaluate_decision` | `request_response` | `required_when_component_active` | Evaluate one governed request using the active policy set. | Yes |
| `IFACE-GOV-POL-002` | `get_policy_set_status` | `query` | `required_when_component_active` | Return active, staged, previous-valid, and compatibility state. | No |
| `IFACE-GOV-POL-003` | `stage_policy_bundle` | `command` | `maintenance_or_release_workflow` | Stage and validate a candidate policy bundle without activation. | Yes |
| `IFACE-GOV-POL-004` | `activate_policy_set` | `command` | `maintenance_or_release_workflow` | Atomically activate a validated compatible complete policy set. | Yes |
| `IFACE-GOV-POL-005` | `rollback_policy_set` | `command` | `recovery_workflow` | Restore the previous valid compatible policy set when safe. | Yes |
| `IFACE-GOV-POL-006` | `get_decision_receipt` | `query` | `required_when_receipts_retained_locally` | Retrieve a retained decision receipt by receipt or correlation identity. | No |
| `IFACE-GOV-POL-007` | `health_and_readiness` | `query` | `always_when_process_running` | Report process health, active authority, compatibility, and readiness. | Yes |
<!-- GENERATED:END -->

The primary decision interface is `IFACE-GOV-POL-001`.

Policy lifecycle interfaces stage, activate, and restore complete policy sets without creating mixed or partial authority.

### 4.8 Consumed interfaces and dependencies

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/consumed_interfaces
renderer=component-dependency-table-v1
-->
| Dependency | Component | Class | Purpose | Failure result |
| --- | --- | --- | --- | --- |
| `DEP-GOV-POL-001` | `identity_and_trust` | `required_runtime` | Verify actor, component, signer, and trust assertions. | `trust_dependent_evaluation_blocked` |
| `DEP-GOV-POL-002` | `audit_broker` | `profile_conditioned_runtime` | Submit selected decision evidence and activation evidence. | `profile_receipt_policy_applied` |
| `DEP-GOV-POL-003` | `koa_node_agent` | `activation_time` | Coordinate profile-authorized policy-bundle staging and activation. | `policy_activation_blocked` |
| `DEP-GOV-POL-004` | `publication_gateway` | `optional_runtime_consumer` | Correlate disclosure decisions with publication execution. | `publication_capability_unavailable` |
| `DEP-GOV-POL-005` | `resource_governor` | `independent_peer` | Observe independent readiness where a profile coordinates policy and resource-sensitive work; no decision authority is exchanged. | `resource_sensitive_work_follows_resource_governor_contract` |
<!-- GENERATED:END -->

Dependency use does not transfer authority.

Identity and Trust provides verified assertions.

Audit Broker accepts selected evidence.

kOA Node Agent coordinates node-local lifecycle work.

Publication Gateway executes publication.

Resource Governor remains an independent peer and does not exchange policy authority.

### 4.9 Owned data

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/owned_data
renderer=component-data-table-v1
-->
| Data domain | Name | Authority | Content summary |
| --- | --- | --- | --- |
| `DATA-GOV-POL-001` | `policy_set_state` | `authoritative` | `installed_policy_bundle_refs`, `staged_policy_set_refs`, `validated_policy_set_refs`, `active_policy_set_ref`, `previous_valid_policy_set_ref`, `compatibility_state`, `activation_state` |
| `DATA-GOV-POL-002` | `decision_receipts` | `authoritative_for_policy_evaluation_event` | `decision_request_reference`, `semantic_result`, `obligations`, `diagnostics`, `policy_set_ref`, `authority_version`, `verified_context_refs`, `evaluation_time`, `evaluator_identity` |
| `DATA-GOV-POL-003` | `evaluation_operational_state` | `authoritative_for_component_operation` | `request_processing_state`, `idempotency_state`, `receipt_generation_state`, `health_state`, `readiness_state` |
| `DATA-GOV-POL-004` | `verified_canonical_input_cache` | `derived` | `policy_input_references`, `profile_references`, `exception_references`, `authority_references` |
<!-- GENERATED:END -->

The component does not own foreign application data.

Its verified canonical-input cache is derived, freshness-bounded, and unusable after its authority or compatibility expires.

### 4.10 Foreign-data policy

The component has no authority to write:

- foreign authoritative state;
- foreign source tables;
- consent records owned elsewhere;
- exception records;
- identity records;
- Resource Governor schedules.

Read access is limited to the minimum contract-defined context needed for evaluation.

### 4.11 Policy-set state

The policy-set states are:

```text
absent
staged
validating
validated
active
superseded
activation_failed
rollback_required
forward_repair_required
```

The allowed transitions are canonical in the component contract.

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/state_model/allowed_transitions
renderer=state-transition-table-v1
-->
| Transition | From | To | Trigger |
| --- | --- | --- | --- |
| `TRANSITION-GOV-POL-001` | `absent` | `staged` | `stage_verified_policy_bundle` |
| `TRANSITION-GOV-POL-002` | `staged` | `validating` | `begin_policy_validation` |
| `TRANSITION-GOV-POL-003` | `validating` | `validated` | `all_required_validation_passes` |
| `TRANSITION-GOV-POL-004` | `validated` | `active` | `atomic_activation_authorized` |
| `TRANSITION-GOV-POL-005` | `active` | `superseded` | `compatible_replacement_activated` |
| `TRANSITION-GOV-POL-006` | `validating` | `activation_failed` | `validation_or_compatibility_failure` |
| `TRANSITION-GOV-POL-007` | `validated` | `activation_failed` | `atomic_activation_failure` |
| `TRANSITION-GOV-POL-008` | `activation_failed` | `active` | `previous_valid_policy_set_restored` |
| `TRANSITION-GOV-POL-009` | `activation_failed` | `forward_repair_required` | `rollback_incompatible` |
<!-- GENERATED:END -->

Mixed policy-set versions and partial policy authority are prohibited by the contract.

### 4.12 Policy-bundle lifecycle

A policy bundle belongs to the governance release channel.

Before activation, it is checked for:

- identity;
- signature and provenance;
- policy syntax and semantics;
- evaluator compatibility;
- profile compatibility;
- component compatibility;
- exception compatibility;
- artifact-contract compatibility;
- Release Set compatibility;
- required tests and evidence;
- rollback or forward-repair behavior.

The previous valid policy set remains active until complete replacement activation succeeds.

### 4.13 Decision receipts

A decision receipt records the policy evaluation event.

It includes:

- receipt, request, and correlation identities;
- requester, action, target, and scope;
- decision class and result;
- obligations;
- policy-set reference;
- authority version;
- verified context references;
- applicable exceptions;
- evaluation time;
- evaluator identity and version.

The receipt excludes unrestricted business-state payloads by default.

Execution evidence remains separate and linkable.

### 4.14 Published events

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/published_events
renderer=component-event-table-v1
-->
| Event | Name | Meaning |
| --- | --- | --- |
| `EVENT-GOV-POL-001` | `policy_decision_completed` | A policy request produced allow or deny. |
| `EVENT-GOV-POL-002` | `policy_decision_blocked` | A policy request could not produce authoritative allow or deny. |
| `EVENT-GOV-POL-003` | `policy_bundle_staged` | A candidate bundle entered staged non-active state. |
| `EVENT-GOV-POL-004` | `policy_bundle_stage_failed` | A candidate bundle could not enter valid staged state. |
| `EVENT-GOV-POL-005` | `policy_set_activated` | A complete validated policy set became active atomically. |
| `EVENT-GOV-POL-006` | `policy_set_activation_failed` | Candidate activation failed and did not create partial authority. |
| `EVENT-GOV-POL-007` | `policy_set_rolled_back` | The previous compatible policy set was restored. |
| `EVENT-GOV-POL-008` | `policy_set_forward_repair_required` | Rollback was unsafe or incompatible and forward repair is required. |
| `EVENT-GOV-POL-009` | `governance_policy_runtime_degraded` | One or more policy capabilities are unavailable or blocked. |
| `EVENT-GOV-POL-010` | `governance_policy_runtime_recovered` | Required authority and compatibility checks passed after degradation. |
<!-- GENERATED:END -->

A policy-decision event describes evaluation.

It is not authoritative evidence that the governed action completed.

### 4.15 Security and privacy

The component uses:

- authenticated callers;
- verified assertions;
- least privilege;
- bounded context;
- integrity-protected policy bundles;
- integrity-protected receipts;
- registered local or profile-conditioned endpoints.

It does not accept raw root credentials or foreign database credentials.

External AI is absent from policy evaluation.

General logs exclude sensitive decision context unless explicitly authorized by a separate evidence or diagnostic contract.

### 4.16 Reproducibility

The same active policy set and the same recorded semantic inputs produce the same semantic result, except for declared trusted dynamic inputs.

Trusted dynamic inputs include:

- trusted time;
- active authority version;
- active profile state;
- consent validity;
- exception validity;
- artifact or release state.

Their references and relevant values are recorded for review.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-GOV-001,REQ-SYS-GOV-002,REQ-SYS-GOV-003,REQ-SYS-GOV-004,REQ-SYS-GOV-005,REQ-SYS-GOV-006,REQ-SYS-GOV-007,REQ-SYS-GOV-008,REQ-SYS-GOV-009,REQ-SYS-GOV-010,REQ-SYS-GOV-011,REQ-SYS-GOV-012,REQ-SYS-GOV-013,REQ-SYS-GOV-014,REQ-SYS-GOV-015,REQ-SYS-GOV-016,REQ-SYS-GOV-017,REQ-SYS-GOV-018,REQ-SYS-GOV-019,REQ-SYS-GOV-020,REQ-SYS-GOV-021,REQ-SYS-GOV-022,REQ-SYS-GOV-023,REQ-SYS-GOV-024,REQ-SYS-GOV-025,REQ-SYS-GOV-026,REQ-SYS-GOV-027,REQ-SYS-GOV-028,REQ-SYS-GOV-029,REQ-SYS-GOV-030,REQ-SYS-GOV-031,REQ-SYS-GOV-032 -->
- **REQ-SYS-GOV-001 — SHALL:** Governance Policy Runtime remain a separate component authority from Resource Governor.
- **REQ-SYS-GOV-002 — SHALL:** Governance Policy Runtime evaluate only governance decisions declared by active policy, profile, component, gateway, security, lifecycle, or exception contracts.
- **REQ-SYS-GOV-003 — SHALL:** Governance Policy Runtime support governed decisions for authorization, disclosure, consent, privilege, and registered exceptions.
- **REQ-SYS-GOV-004 — SHALL NOT:** Governance Policy Runtime allocate CPU, memory, I/O, concurrency, queues, job schedules, or process limits.
- **REQ-SYS-GOV-005 — SHALL NOT:** Resource Governor authorize disclosure, consent, privilege, policy exceptions, or component-owned state transitions.
- **REQ-SYS-GOV-006 — SHALL:** The active deployment profile declare whether Governance Policy Runtime is required, optional, unavailable, or prohibited for that profile.
- **REQ-SYS-GOV-007 — SHALL NOT:** Governance Policy Runtime become a mandatory dependency of profiles that make no sovereign-governance or high-assurance claim.
- **REQ-SYS-GOV-008 — SHALL:** Every policy evaluation identify the requesting actor or component, requested action, target, governing scope, active policy set, and evaluation context.
- **REQ-SYS-GOV-009 — SHALL:** Every policy result identify the decision, applicable obligations, policy-set version, evaluation time, and correlation identifier.
- **REQ-SYS-GOV-010 — SHALL:** An indeterminate, unverifiable, missing, stale, incompatible, or unauthorized policy state block the affected governed transition.
- **REQ-SYS-GOV-011 — SHALL:** The calling authoritative component or gateway enforce the returned decision and remain responsible for its own state transition.
- **REQ-SYS-GOV-012 — SHALL NOT:** Governance Policy Runtime write directly to another component's authoritative source state.
- **REQ-SYS-GOV-013 — SHALL NOT:** A policy decision implicitly transfer data ownership, component authority, publication authority, or privilege ownership.
- **REQ-SYS-GOV-014 — SHALL:** Policy inputs use the minimum context required for the declared decision and remain bounded by active disclosure and privacy rules.
- **REQ-SYS-GOV-015 — SHALL:** Policy evaluation use authenticated identities and verified assertions from registered trust sources.
- **REQ-SYS-GOV-016 — SHALL:** Policy bundles be versioned, validated, attributable, compatible with their target profiles and components, and activated atomically.
- **REQ-SYS-GOV-017 — SHALL:** A policy-bundle activation preserve the previous valid policy set until the complete replacement passes validation and activation.
- **REQ-SYS-GOV-018 — SHALL:** Governance Policy Runtime operate from locally available active policy bundles for profiles that claim offline governed operation.
- **REQ-SYS-GOV-019 — SHALL NOT:** External AI output, generated prose, a prompt, a recipe, or an informal instruction act as policy authority.
- **REQ-SYS-GOV-020 — SHALL:** External AI output affecting a governed decision remain candidate input until validated and explicitly adopted through an authoritative workflow.
- **REQ-SYS-GOV-021 — SHALL:** A governed exception reference an active registered exception, exact scope, activation condition, expiration or closure condition, compensating controls, and evidence obligations.
- **REQ-SYS-GOV-022 — SHALL NOT:** An exception silently rewrite, weaken, broaden, suspend, or replace the underlying requirement or lock.
- **REQ-SYS-GOV-023 — SHALL:** Privilege decisions identify the requested privileged operation and remain separate from execution by the applicable privileged component or broker.
- **REQ-SYS-GOV-024 — SHALL:** Disclosure and publication decisions remain separate from transport and execution by Publication Gateway.
- **REQ-SYS-GOV-025 — SHALL:** Consent decisions identify the subject, purpose, data scope, recipient or use domain, duration or closure condition, and evidence obligations.
- **REQ-SYS-GOV-026 — SHALL:** Critical governed decisions produce machine-readable decision receipts or evidence records.
- **REQ-SYS-GOV-027 — SHALL:** Audit records contain the minimum evidence required to establish accountability without turning Audit Broker into a universal operational data store.
- **REQ-SYS-GOV-028 — SHALL:** Policy evaluation be reproducible for the recorded policy set and recorded decision inputs, except for explicitly declared trusted dynamic inputs.
- **REQ-SYS-GOV-029 — SHALL:** Policy-set compatibility be validated against affected components, profiles, gateways, artifacts, exceptions, tests, and evidence before activation.
- **REQ-SYS-GOV-030 — SHALL:** Governance Policy Runtime degradation preserve unaffected non-governed capabilities while blocking transitions that require unavailable policy authority.
- **REQ-SYS-GOV-031 — SHALL:** A semantic change to policy authority, evaluation meaning, decision input, obligation, exception handling, profile applicability, or failure behavior use an accepted decision and complete impact analysis.
- **REQ-SYS-GOV-032 — SHALL:** Governance Policy Runtime conformance be traceable from accepted decisions through requirements, locks, component and profile contracts, tests, evidence, and active authority.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Evaluate a governed request

1. The caller creates a unique request and correlation identity.
2. The caller identifies the decision class, action, target, and scope.
3. Identity and Trust verifies required identities and assertions.
4. The caller supplies the minimum contract-defined context.
5. The component resolves the requested active compatible policy set.
6. The component resolves applicable canonical requirements, locks, profile rules, consent, and registered exceptions.
7. The component evaluates the request.
8. The component creates a bounded result, obligations, diagnostics, and receipt.
9. The caller verifies correlation, authority version, validity, and scope.
10. The caller satisfies required obligations.
11. The caller executes or rejects its own operation.
12. Decision and execution evidence are linked where required.

### 6.2 Stage a policy bundle

1. Receive a registered policy-bundle artifact reference.
2. Verify artifact identity, signature, and provenance.
3. Resolve target profiles, components, exceptions, and evaluator version.
4. Verify policy syntax and semantic closure.
5. Verify compatibility with the active authority and proposed Release Set.
6. Resolve migration, rollback, or forward-repair behavior.
7. Generate the required test and evidence plan.
8. Place the candidate in staged non-active state.
9. Retain the current active policy set unchanged.
10. Report a stable stage result.

### 6.3 Activate a policy set

1. Resolve a validated staged policy set.
2. Verify that all required validation completed successfully.
3. Verify receipt and evidence readiness.
4. Verify that the previous valid policy set remains recoverable.
5. Obtain the required activation authority.
6. Activate the complete policy set atomically.
7. expose the new set only after active-state verification.
8. retain the predecessor according to lifecycle policy.
9. produce activation evidence.

### 6.4 Roll back or repair

1. Identify the failed or incompatible candidate.
2. Preserve diagnostics and activation evidence.
3. Check whether the previous policy set remains compatible with current state.
4. Restore the previous set when safe.
5. Use the declared forward-repair plan when rollback is incompatible.
6. validate the recovered policy authority.
7. reenable affected decision classes only after readiness passes.
8. produce recovery evidence.

### 6.5 Evaluate a registered exception

1. Resolve the exception identifier.
2. verify active status and exact affected requirement or lock.
3. verify subject, scope, activation condition, and closure condition.
4. verify compensating controls and evidence requirements.
5. evaluate the base rule with the bounded exception.
6. record the exception reference in the result and receipt.
7. leave the underlying requirement and lock unchanged.

### 6.6 Evaluate privilege

1. Resolve the exact privileged operation and target.
2. verify requester, profile, assurance context, and duration.
3. evaluate policy and applicable exceptions.
4. return a result and obligations.
5. send an allowed request to the registered privileged component.
6. correlate execution evidence with the decision receipt.
7. close temporary authority according to the execution contract.

### 6.7 Evaluate disclosure

1. Resolve source owner, representation, destination, audience, purpose, and consent.
2. evaluate the active disclosure policy.
3. return minimization, destination, retention, evidence, or review obligations.
4. Publication Gateway verifies and applies the result.
5. Publication Gateway performs or rejects transport.
6. decision and publication receipts are linked.
7. source ownership remains unchanged.

## 7. Failure States and Safe Degradation

<!-- GENERATED:BEGIN
source=contracts/components/governance-policy-runtime.component.json#/failure_contract
renderer=component-failure-table-v1
-->
| Failure code | Condition | Result | Preserved state | Retry |
| --- | --- | --- | --- | --- |
| `GOV_POLICY_MISSING` | No active applicable policy set resolves. | `blocked` | `previous_valid_policy_set_when_explicitly_permitted_and_verifiable` | `after_policy_authority_restored` |
| `GOV_POLICY_STALE` | Policy freshness or authority-version validity fails. | `blocked` | `unaffected_non_governed_capabilities` | `after_compatible_policy_refresh` |
| `GOV_POLICY_INCOMPATIBLE` | Policy set is incompatible with profile, component, release, or evaluator. | `blocked` | `current_compatible_active_policy_set` | `after_compatibility_restored` |
| `GOV_IDENTITY_UNVERIFIED` | Required identity or trust assertion cannot be verified. | `blocked` | `unaffected_verified_activity` | `after_trust_verification` |
| `GOV_CONTEXT_INVALID` | Required context is missing, malformed, excessive, or unauthorized. | `blocked` | `authoritative_component_state` | `with_valid_bounded_context` |
| `GOV_EXCEPTION_INVALID` | Exception is missing, inactive, expired, closed, or out of scope. | `evaluate_without_exception_or_block_under_base_rule` | `underlying_requirement_and_lock` | `only_with_active_applicable_exception` |
| `GOV_OBLIGATION_UNSATISFIED` | Caller cannot satisfy a required obligation. | `blocked` | `pre_transition_state` | `after_obligation_can_be_satisfied` |
| `GOV_RECEIPT_FAILURE` | A required decision receipt cannot be durably created. | `blocked_for_receipt_required_transition` | `pre_transition_state` | `after_receipt_storage_recovers` |
| `GOV_AUDIT_UNAVAILABLE` | Required audit evidence intake is unavailable. | `profile_evidence_policy_applied` | `locally_retained_evidence_when_permitted` | `after_audit_or_buffer_recovery` |
| `GOV_ACTIVATION_FAILED` | Policy-set activation fails. | `candidate_inactive` | `previous_valid_policy_set` | `after_validation_or_repair` |
| `GOV_EXTERNAL_AI_UNAVAILABLE` | An optional external AI surface is unavailable. | `no_effect_on_native_policy_evaluation` | `all_native_policy_capabilities` | `not_required_for_core_recovery` |
<!-- GENERATED:END -->

### 7.1 Degradation principles

Degradation is capability-scoped.

The component does not create partial authority or silently substitute another source.

When policy evaluation is unavailable:

- new policy-dependent transitions are blocked;
- unaffected non-governed capabilities remain available;
- health and diagnostics remain available;
- the previous valid authoritative state is preserved.

When one decision class is unavailable, another class remains available only when its independent authority and dependencies can be verified.

When required receipt or audit storage is unavailable, receipt-required critical transitions remain blocked.

Loss of remote connectivity does not affect local policy evaluation for profiles that claim offline governed operation.

### 7.2 Recovery readiness

Recovery requires:

- an active compatible policy set;
- a valid authority version;
- required trust sources;
- required exception data;
- a compatible evaluator;
- a ready receipt path;
- successful health and readiness checks.

Process responsiveness alone is insufficient.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust verifies actor, component, signer, and trust assertions.

Governance Policy Runtime consumes bounded verified assertions.

It does not issue or mutate the underlying identity records.

A verified identity can still receive `deny` or `blocked`.

### 8.2 Authoritative application components

The application component owns:

- its operation;
- its application validation;
- its state;
- enforcement of the policy result;
- execution outcome;
- component-specific recovery.

The policy runtime owns the evaluation and decision receipt only.

### 8.3 Resource Governor

Resource Governor controls resources.

Governance Policy Runtime controls governance decisions.

A workload can require both controls:

```text
policy evaluation
        ↓
component acceptance
        ↓
resource admission and scheduling
        ↓
component execution
```

Policy approval does not guarantee resource availability.

Resource availability does not grant permission.

### 8.4 Publication Gateway

Governance Policy Runtime evaluates disclosure.

Publication Gateway:

- verifies the result and obligations;
- prepares the allowed representation;
- performs transport;
- records the publication result.

Neither component absorbs the other's authority.

### 8.5 kOA Node Agent

The policy runtime evaluates a privilege request.

kOA Node Agent coordinates the exact profile-authorized node operation.

The registered privileged boundary executes the operation.

A decision result is not a root credential or general shell.

### 8.6 Audit Broker

The policy runtime submits selected decision evidence.

The executing component submits selected execution evidence.

Audit Broker retains or routes evidence according to its contract without becoming a universal operational store.

### 8.7 Exception registry

The exception registry owns exception identity, scope, controls, lifecycle, and evidence requirements.

The policy runtime evaluates applicability.

It cannot create or modify an exception during decision evaluation.

### 8.8 Policy-bundle artifacts

Policy-bundle artifacts carry executable policy authority.

Markdown explains policy behavior but is not an executable policy set.

Candidate bundles remain inactive until validation and atomic activation complete.

### 8.9 External AI

External AI output is candidate material only.

A policy owner can review and adopt validated content through the governed change process.

Only activated canonical policy authority affects runtime evaluation.

The component does not call an external AI system to invent a rule or resolve missing authority.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision or ADR | Closed choice |
| --- | --- |
| `DEC-GOV-001` / `ADR-009` | Governance Policy Runtime and Resource Governor remain separate authorities |
| `ADR-010` | Audit remains selective |
| `ADR-012` | Privileged execution remains behind a narrow registered boundary |
| `DEC-AI-001` | External AI remains optional and non-authoritative |
| `DEC-PROFILE-001` | Applicability is profile-conditioned and machine-readable |
| `DEC-DATA-001` | Data ownership remains with registered component owners |
| `DEC-GATE-001` | Publication execution remains separate from policy evaluation |

### 9.2 Protected locks

| Lock | Protected boundary |
| --- | --- |
| `LOCK-GOV-001` | Resource and governance policy authorities remain separate |
| `LOCK-DATA-001` | Policy evaluation cannot justify direct foreign-state mutation |
| `LOCK-GATE-001` | Disclosure evaluation and publication execution remain separate |
| `LOCK-AI-002` | External AI cannot directly change authoritative policy or state |
| `LOCK-PROFILE-001` | Profile-specific applicability does not become global |
| `LOCK-LIFE-001` | Policy artifacts do not activate partially |

### 9.3 Prohibited assumptions

The following assumptions are invalid:

- every profile requires the component;
- a running process is ready;
- a verified identity is automatically allowed;
- authorization implies disclosure, consent, or privilege;
- a policy result executes the operation;
- an allow result is a credential;
- policy evaluation transfers data ownership;
- the component can write into an application database;
- the component can publish data;
- the component can schedule CPU or workers;
- Resource Governor can make governance decisions;
- an exception changes its underlying rule;
- an expired exception remains applicable;
- missing policy has an obvious default;
- stale policy can remain active after compatibility expires;
- partial policy activation is acceptable;
- a decision receipt proves successful execution;
- Audit Broker owns the application event described by evidence;
- administrator access creates policy authority;
- a prompt or external AI answer creates policy;
- implementation behavior overrides active policy contracts;
- failure permits an informal bypass.

Missing, stale, incompatible, unverifiable, or indeterminate authority blocks the affected governed transition.

## 10. Validation Criteria

This document and component contract are aligned when:

1. the document is registered as `DOC-COMP-GOV-POL-001`;
2. the path is `04-components/governance-policy-runtime.md`;
3. the scope resolves to `component:governance_policy_runtime`;
4. the active component record resolves;
5. the active component contract validates;
6. component class and authority role match the contract;
7. all seven provided interfaces match the contract;
8. all five dependencies resolve;
9. all four owned data domains match the contract;
10. all commands reference existing interfaces and events;
11. all events use unique stable identifiers;
12. every state transition uses a declared state;
13. every failure code is unique and has a result and recovery condition;
14. no direct foreign authoritative-state write is permitted;
15. Resource Governor remains an independent peer;
16. Publication Gateway remains the publication executor;
17. kOA Node Agent or another registered broker remains the privileged executor;
18. Identity and Trust remains the identity assertion owner;
19. Audit Broker receives only selected evidence;
20. profile applicability resolves without implicit inheritance;
21. offline-governance claims pass without remote policy or external AI services;
22. policy-bundle identity, signature, provenance, compatibility, and activation pass;
23. activation preserves the previous valid policy set;
24. partial policy authority is impossible;
25. decision and execution evidence remain distinct;
26. registered exceptions preserve the underlying requirement and lock;
27. all 32 linked requirements resolve;
28. all 20 linked tests execute;
29. all 20 linked evidence definitions resolve to valid evidence;
30. no unresolved authority or compatibility state exists;
31. generated catalogs and AI context match the contract;
32. complete documentation validation passes.

Expected test coverage includes:

```text
TEST-SYS-GOV-001  Resource and policy authority separation
TEST-SYS-GOV-002  Profile-conditioned component applicability
TEST-SYS-GOV-003  Policy request completeness
TEST-SYS-GOV-004  Policy result and obligation completeness
TEST-SYS-GOV-005  Fail-closed indeterminate evaluation
TEST-SYS-GOV-006  Calling-component enforcement boundary
TEST-SYS-GOV-007  Foreign authoritative-state write rejection
TEST-SYS-GOV-008  Identity assertion verification
TEST-SYS-GOV-009  Policy-bundle compatibility
TEST-SYS-GOV-010  Atomic policy activation and predecessor retention
TEST-SYS-GOV-011  Offline governed operation
TEST-SYS-GOV-012  External AI non-authority
TEST-SYS-GOV-013  Registered exception applicability
TEST-SYS-GOV-014  Underlying requirement preservation
TEST-SYS-GOV-015  Privilege evaluation and execution separation
TEST-SYS-GOV-016  Disclosure evaluation and publication separation
TEST-SYS-GOV-017  Consent-context completeness
TEST-SYS-GOV-018  Decision receipt generation
TEST-SYS-GOV-019  Decision and execution evidence distinction
TEST-SYS-GOV-020  Capability-scoped policy-runtime degradation
```

The test catalog and evidence registry own executable controls and evidence definitions.

This document does not claim that those tests have already executed.

## 11. Non-Normative Examples

> **Non-normative example:** These examples illustrate valid interactions. They do not redefine the component contract.

### 11.1 Authorization

Orgo asks whether an identified actor can perform a declared workflow action.

The policy runtime evaluates the exact actor, action, target, profile, scope, and active policy set.

It returns `allow` with an audit obligation.

Orgo records the required evidence and performs the operation in Orgo-owned state.

### 11.2 Disclosure

Konnaxion requests publication to a declared audience.

The policy runtime evaluates disclosure and consent and returns field-minimization and receipt obligations.

Publication Gateway prepares and transports the minimized representation.

The policy runtime never opens the external connection.

### 11.3 Privilege

An operator requests activation of a signed release on a sovereign node.

The policy runtime evaluates the exact operation and returns a bounded allow result.

kOA Node Agent coordinates the registered privileged operation.

Decision and execution evidence share the correlation identity.

### 11.4 Exception

A registered exception permits one compatibility adapter for one profile until a declared release condition.

The policy runtime verifies scope, condition, compensating controls, and evidence requirements.

The underlying requirement remains active and unchanged.

### 11.5 Offline evaluation

A `sovereign_offline` deployment has local policy bundles, trust material, exception data, and receipt storage.

Internet connectivity is absent.

The runtime evaluates locally and retains receipts for controlled later export.

### 11.6 Resource pressure

A governed UCKK export is permitted by policy.

Resource Governor delays the job because the active resource envelope is full.

The policy result remains valid only within its declared validity conditions, but it does not override the resource queue.

### 11.7 External AI candidate

An approved external AI surface proposes explanatory policy prose.

A policy owner reviews and converts accepted content into canonical requirements and a policy bundle through the normal change process.

The external text never becomes executable policy directly.

### 11.8 Invalid merged service

One implementation proposes a service that evaluates policy, grants root credentials, publishes data, schedules CPU, and writes into product databases.

The implementation is invalid because it merges governance policy, privilege execution, publication, resource, and data authority.
