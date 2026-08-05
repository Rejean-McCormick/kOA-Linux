<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-GOV-TPL-PROFILE-001",
  "document_class": "template",
  "status": "active",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "00-governance/02-documentation-contract.md",
    "00-governance/03-normative-language.md",
    "00-governance/08-generated-content-policy.md"
  ],
  "decision_ids": [
    "DEC-DOC-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-DOC-003",
    "LOCK-DOC-005",
    "LOCK-DOC-016"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-008"
  ],
  "tags": [
    "template",
    "profile",
    "ai-authoring"
  ]
}
KOA:DOC-META:END -->

<!--
KOA PROFILE DOCUMENT TEMPLATE

Template path:
docs/00-governance/templates/profile-document.template.md

Purpose:
Use this template for normative Markdown documents that explain one deployment
profile or one composable profile overlay.

Canonical ownership:
- The profile contract under contracts/profiles/ owns profile membership,
 inheritance, capabilities, components, hardware envelopes, implementation
 adoptions, security claims, offline behavior, and conformance claims.
- requirements.registry.json owns normative requirement statements.
- locks.registry.json owns cross-file invariants.
- decisions.registry.json owns accepted architectural decisions.
- This Markdown document explains those canonical objects.
- It does not independently define or override them.

Template status:
- This file is an authoring template, not active profile authority.
- Placeholder markers are permitted only inside governance templates.
- Every placeholder must be replaced before activation.
- Generated blocks must not be edited manually.
-->

<!-- KOA:TARGET-DOC-META:BEGIN
{
 "doc_id": "{{DOC-PROFILE-NNN}}",
 "document_class": "normative_markdown",
 "status": "{{draft|active|deprecated|archived}}",
 "language": "en",
 "layer": "profile",
 "scope": ["{{profile:PROFILE_ID|profile_overlay:PROFILE_ID}}"],
 "canonical_refs": [
 "contracts/profiles/{{PROFILE_ID}}.profile.json"
 ],
 "decision_ids": ["{{DEC-PROFILE-NNN}}"],
 "requirement_ids": ["{{REQ-PROFILE-NNN}}"],
 "lock_ids": ["{{LOCK-PROFILE-NNN}}"],
 "exception_ids": [],
 "depends_on": [
 "DOC-PROFILE-000",
 "DOC-PROFILE-001",
 "{{DOC-SYS-NNN}}"
 ],
 "tags": [
 "deployment-profile",
 "{{PROFILE_ID}}",
 "{{primary-profile|profile-overlay}}"
 ]
}
KOA:TARGET-DOC-META:END -->

# {{Profile Display Name}}

> **Document status:** Normative profile explanation.
> **Profile ID:** `{{PROFILE_ID}}`
> **Profile kind:** `{{primary_profile|profile_overlay}}`
> **Canonical profile contract:** `contracts/profiles/{{PROFILE_ID}}.profile.json`
> **Authority rule:** The canonical profile contract owns profile facts. This document explains how those facts apply.

## 1. Purpose

This document explains the `{{PROFILE_ID}}` profile.

The profile exists to support:

- {{primary deployment purpose}};
- {{primary user or operator context}};
- {{primary assurance, development, or operational objective}}.

This document explains where the profile applies, which capabilities and components it selects, which overlays it accepts, its hardware and resource envelope, its offline, security, lifecycle and operational claims, its implementation adoptions, and its conformance validation.

It does not redefine the global system baseline.

## 2. Scope

### 2.1 Included scope

This profile applies to:

- {{deployment environment}};
- {{host or execution context}};
- {{intended user, operator, or workload}};
- {{development, production, build, hub, control, or appliance purpose}}.

### 2.2 Excluded scope

This profile does not claim:

- {{excluded deployment purpose}};
- {{excluded assurance property}};
- {{excluded component or workload}};
- {{excluded host or operating environment}}.

### 2.3 Profile classification

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/classification
renderer=profile-classification-v1
-->
{{Generated profile classification.}}
<!-- GENERATED:END -->

### 2.4 Profile status

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/status
renderer=scalar-value-v1
-->
{{Generated profile status.}}
<!-- GENERATED:END -->

### 2.5 Applicable operating modes

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/operating_modes
renderer=canonical-list-v1
-->
{{Generated operating-mode list.}}
<!-- GENERATED:END -->

### 2.6 Profile inheritance

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/inherits
renderer=profile-inheritance-v1
-->
{{Generated inherited-profile and overlay relationships, or "No inherited profile."}}
<!-- GENERATED:END -->

Inheritance is explicit. A capability or requirement is not inherited unless represented in the canonical profile contract.

## 3. Canonical References

### 3.1 Primary profile authority

`text
contracts/profiles/{{PROFILE_ID}}.profile.json
`

### 3.2 Global authority

| Reference | Owned information |
| --- | --- |
| `generated/authority-manifest.json` | Active authority order and registry versions |
| `generated/decision-index.json` | Accepted profile and system decisions |
| `contracts/system.contract.json` | Global system baseline |
| `generated/component-catalog.json` | Component identities and ownership |
| `generated/requirements-index.json` | Normative requirements |
| `generated/assertion-index.json` | Alignment invariants |
| `generated/traceability.json` | Requirements, tests, and evidence |
| `generated/exception-index.json` | Approved profile exceptions |
| `contracts/terminology.contract.json` | Canonical terminology |

### 3.3 Related profile references

| Profile or overlay | Canonical reference | Relationship |
| --- | --- | --- |
| `{{PROFILE_ID}}` | `contracts/profiles/{{PROFILE_ID}}.profile.json` | Current profile |
| `{{RELATED_PROFILE_ID}}` | `contracts/profiles/{{RELATED_PROFILE_ID}}.profile.json` | {{inherited, compatible, excluded, or composable}} |

### 3.4 Related component contracts

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/component_contract_refs
renderer=canonical-reference-table-v1
-->
{{Generated component-contract references.}}
<!-- GENERATED:END -->

### 3.5 Related decisions

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/decision_ids
renderer=decision-reference-table-v1
-->
{{Generated decision references.}}
<!-- GENERATED:END -->

## 4. Model and Responsibilities

### 4.1 Profile intent

{{Explain the intended system realization represented by this profile.}}

The profile selects, constrains, or strengthens capabilities already represented by the global system and component contracts.

### 4.2 Profile type

`text
{{primary_profile|profile_overlay}}
`

A primary profile defines a deployable system identity.

A profile overlay modifies or strengthens compatible primary profiles without becoming independently deployable.

### 4.3 Supported users and operators

Intended users or operators:

- {{user or operator class}};
- {{user or operator class}}.

Not intended for:

- {{excluded user or operator class}}.

### 4.4 Capability envelope

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/capabilities
renderer=profile-capability-matrix-v1
-->
{{Generated required, optional, conditional, and excluded capabilities.}}
<!-- GENERATED:END -->

### 4.5 Component composition

#### Required components

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/components/required
renderer=component-list-v1
-->
{{Generated required-component list.}}
<!-- GENERATED:END -->

#### Optional components

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/components/optional
renderer=component-list-v1
-->
{{Generated optional-component list.}}
<!-- GENERATED:END -->

#### Task-activated components

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/components/task_activated
renderer=component-list-v1
-->
{{Generated task-activated-component list.}}
<!-- GENERATED:END -->

#### Excluded components

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/components/excluded
renderer=component-list-v1
-->
{{Generated excluded-component list.}}
<!-- GENERATED:END -->

### 4.6 Component activation model

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/component_activation
renderer=component-activation-table-v1
-->
{{Generated always-on, socket-activated, task-activated, manual, and prohibited activation modes.}}
<!-- GENERATED:END -->

### 4.7 Hardware envelope

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/hardware_envelope
renderer=hardware-envelope-v1
-->
{{Generated minimum, recommended, and maximum tested hardware values.}}
<!-- GENERATED:END -->

The hardware envelope is a profile claim, not a universal kOA requirement.

### 4.8 Resource envelope

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/resource_envelope
renderer=resource-envelope-v1
-->
{{Generated CPU, memory, storage, I/O, worker, queue, and concurrency limits.}}
<!-- GENERATED:END -->

### 4.9 Offline capability envelope

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/offline_envelope
renderer=offline-capability-matrix-v1
-->
{{Generated offline capability claims.}}
<!-- GENERATED:END -->

Each declared offline capability must be tested without Internet access.

### 4.10 AI and external-service envelope

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/ai_and_external_services
renderer=external-capability-matrix-v1
-->
{{Generated native, external, optional, unavailable, and prohibited AI or external-service capabilities.}}
<!-- GENERATED:END -->

External AI output remains candidate input until accepted through a component-owned workflow.

### 4.11 Data and storage model

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/data_and_storage
renderer=profile-data-storage-v1
-->
{{Generated database, schema, storage, encryption, persistence, and separation model.}}
<!-- GENERATED:END -->

Logical component data ownership remains mandatory even when physical infrastructure is shared.

### 4.12 Network model

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/network
renderer=profile-network-model-v1
-->
{{Generated network zones, default policy, ingress, egress, and inter-component communication rules.}}
<!-- GENERATED:END -->

### 4.13 Privilege model

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/privilege
renderer=profile-privilege-model-v1
-->
{{Generated user, service, container, broker, and host-privilege rules.}}
<!-- GENERATED:END -->

Root or host-administrator access is not an ordinary application governance interface.

### 4.14 Security and assurance claims

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/security_claims
renderer=security-claims-v1
-->
{{Generated security and assurance claims.}}
<!-- GENERATED:END -->

### 4.15 Lifecycle claims

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/lifecycle
renderer=profile-lifecycle-v1
-->
{{Generated installation, update, release, activation, rollback, recovery, and migration rules.}}
<!-- GENERATED:END -->

### 4.16 Backup, restore, and exit

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/backup_restore_exit
renderer=backup-restore-exit-v1
-->
{{Generated backup, restore, portability, and independent-exit claims.}}
<!-- GENERATED:END -->

### 4.17 Adopted implementation choices

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/implementation_adoptions
renderer=implementation-adoption-table-v1
-->
{{Generated implementation choices explicitly adopted by this profile.}}
<!-- GENERATED:END -->

An implementation choice is normative only for the scope and version explicitly adopted by this profile.

### 4.18 Compatible overlays

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/compatible_overlays
renderer=profile-overlay-matrix-v1
-->
{{Generated compatible, required, conditional, and incompatible overlays.}}
<!-- GENERATED:END -->

### 4.19 Incompatible profiles and overlays

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/incompatible_with
renderer=canonical-list-v1
-->
{{Generated incompatible profile list, or "None."}}
<!-- GENERATED:END -->

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids={{REQ-PROFILE-NNN,...}} -->
{{Generated profile requirements.}}
<!-- GENERATED:REQUIREMENTS:END -->

### 5.1 Requirement groups

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/requirement_groups
renderer=requirement-group-index-v1
-->
{{Generated global, inherited, profile-specific, overlay, and conditional requirement groups.}}
<!-- GENERATED:END -->

### 5.2 Requirement inheritance

Inherited requirements remain owned by `requirements.registry.json`.

The profile contract declares applicability. It does not copy or rewrite statements.

### 5.3 Conditional requirements

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/conditional_requirements
renderer=conditional-requirement-table-v1
-->
{{Generated condition-to-requirement mappings.}}
<!-- GENERATED:END -->

### 5.4 Approved exceptions

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/exception_ids
renderer=exception-reference-table-v1
-->
{{Generated approved exceptions, or "No active exceptions."}}
<!-- GENERATED:END -->

An exception does not change the original requirement.

## 6. Procedures or State Transitions

### 6.1 Profile selection

The selected profile identity must resolve to the active profile registry and authority manifest.

### 6.2 Profile composition

1. load the global baseline;
2. load the primary profile;
3. load explicitly selected compatible overlays;
4. resolve inherited requirements;
5. apply overlay strengthening or restriction;
6. reject incompatible combinations;
7. resolve approved exceptions;
8. compute the effective profile;
9. validate it;
10. generate a claim and evidence plan.

An overlay cannot silently remove a global invariant.

### 6.3 Provisioning

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/procedures/provisioning
renderer=ordered-procedure-v1
-->
{{Generated provisioning sequence.}}
<!-- GENERATED:END -->

### 6.4 Activation

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/procedures/activation
renderer=ordered-procedure-v1
-->
{{Generated activation sequence.}}
<!-- GENERATED:END -->

Activation must not create partial authoritative state.

### 6.5 Update

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/procedures/update
renderer=ordered-procedure-v1
-->
{{Generated update sequence.}}
<!-- GENERATED:END -->

### 6.6 Rollback or forward repair

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/procedures/recovery
renderer=profile-recovery-procedure-v1
-->
{{Generated rollback, restore, or forward-repair sequence.}}
<!-- GENERATED:END -->

### 6.7 Profile removal

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/procedures/removal
renderer=ordered-procedure-v1
-->
{{Generated deactivation, cleanup, export, and removal sequence.}}
<!-- GENERATED:END -->

Removal of an optional capability must not corrupt another component’s authoritative state.

### 6.8 Overlay addition

An overlay may be added only when the primary profile declares compatibility, preconditions pass, strengthened requirements are supported, required tests exist, exceptions do not conflict, and the effective profile remains valid.

### 6.9 Overlay removal

An overlay may be removed only when no retained artifact or claim depends on it and the resulting primary profile validates independently.

## 7. Failure States and Safe Degradation

Canonical failure codes include:

`text
invalid_profile_identity
incompatible_profile_composition
missing_inherited_profile
missing_owner_decision
`

No similar profile or fallback is inferred automatically.

Hardware below minimum prevents full conformance.

Resource pressure degrades optional or heavy capabilities before core authority or data integrity.

Loss of an optional external service affects only its declared capability and does not activate a substitute.

Verification failure causes fail-closed authority for the affected operation. Previously valid read-only or advisory state may remain only when explicitly permitted.

## 8. Cross-Component Interactions

### 8.1 Effective component graph

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/effective_component_graph
renderer=component-interaction-matrix-v1
-->
{{Generated component interaction graph.}}
<!-- GENERATED:END -->

### 8.2 Data ownership

A profile may change physical placement, activation, process isolation, database topology, or resources. It does not transfer logical data ownership without an accepted architecture decision.

### 8.3 Shared infrastructure

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/shared_infrastructure
renderer=shared-infrastructure-table-v1
-->
{{Generated shared database, network, storage, cache, broker, and host-service topology.}}
<!-- GENERATED:END -->

Shared infrastructure does not permit undeclared cross-component writes.

### 8.4 Gateways and cross-domain flows

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/gateways
renderer=gateway-flow-table-v1
-->
{{Generated gateway and cross-domain flow mappings.}}
<!-- GENERATED:END -->

### 8.5 Messaging and asynchronous work

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/messaging
renderer=messaging-topology-v1
-->
{{Generated queue, outbox, retry, idempotency, and poison-message rules.}}
<!-- GENERATED:END -->

### 8.6 Resource governance

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/resource_governance
renderer=resource-governance-matrix-v1
-->
{{Generated Resource Governor interactions.}}
<!-- GENERATED:END -->

Resource Governor remains distinct from Governance Policy Runtime.

### 8.7 Privileged host operations

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/privileged_operations
renderer=privileged-operation-flow-v1
-->
{{Generated privileged-operation path, or "No governed host mutation capability."}}
<!-- GENERATED:END -->

### 8.8 External integrations

<!-- GENERATED:BEGIN
source=contracts/profiles/{{PROFILE_ID}}.profile.json#/external_integrations
renderer=integration-classification-table-v1
-->
{{Generated permitted, optional, required, and prohibited integrations.}}
<!-- GENERATED:END -->

Every optional integration must be removable without breaking the profile’s declared core capability envelope.

## 9. Decision Closure and Prohibited Assumptions

Every referenced decision must be accepted before profile activation.

An AI agent or maintainer must not assume that a profile rule is global, an overlay is independently deployable, undeclared overlays are compatible, optional means installed or active, excluded means temporarily inactive, recipes are adopted by location, current code defines profile authority, hardware recommendations equal minimums, shared infrastructure transfers ownership, installed services are always active, Internet or external AI is available, undeclared fallbacks exist, similar profiles may substitute, development proves sovereign conformance, sovereign profiles constrain all developers, or profiles may weaken global invariants.

Missing profile authority returns:

`json
{
 "validation_status": "blocked",
 "reason": "missing_profile_authority",
 "profile_id": "{{PROFILE_ID}}",
 "affected_objects": [],
 "prohibited_inference": true
}
`

## 10. Validation Criteria

A profile validates only when its ID is unique, schema passes, index entry exists, status is active, all decisions are accepted, inheritance resolves without cycles, overlays are explicit, components and contracts resolve, requirements have validation, locks pass, exceptions are active and scoped, references resolve, hardware/resource/offline envelopes are complete, external dependency failure is defined, implementation adoptions resolve, and generated blocks match.

A deployment may claim conformance only when the effective profile and overlays are identified, authority manifest is recorded, mandatory requirements and tests pass, evidence exists, exceptions are valid, no excluded or undeclared capability is active, hardware minimums are met, and offline claims are tested.

Required checks:

`bash
python docs/tools/check_profile_inheritance.py
python docs/tools/check_component_boundaries.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_traceability.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/validate_docs.py
`

Conformance output includes profile ID and version, overlays, authority version, requirements evaluated and passed, failures, tests, evidence, exceptions, undeclared and excluded capabilities, and validation status.

## 11. Non-Normative Examples

A native Linux development workstation may use `developer_linux_workstation` with isolated workspaces, UV-managed Python environments, rootless services, and workspace-scoped mutable state.

A sovereign deployment may compose `sovereign_linux_node + high_assurance + sovereign_offline` only when all contracts declare compatibility.

A sovereign Linux profile may adopt rootless Podman, Quadlet, and systemd, while a Windows/WSL profile permits Docker. Neither becomes global.

A lightweight profile may share one PostgreSQL process while preserving separate schemas, identities, and prohibited cross-component writes.

SenTient may be optional and task-activated without becoming baseline, default, authoritative, or available in another profile.

Running under WSL does not prove sovereign Linux conformance.

## Final Rule

> A profile selects, constrains, or strengthens the global kOA system for a declared deployment purpose. Its JSON contract owns the facts. Requirements constrain the facts. This document explains the facts. Recipes implement selected choices. No profile-specific rule becomes global implicitly.
