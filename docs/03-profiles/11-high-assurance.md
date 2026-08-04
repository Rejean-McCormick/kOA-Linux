<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-PROF-011",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "deployment_profiles",
  "scope": [
    "profile_overlay:high_assurance"
  ],
  "canonical_refs": [
    "contracts/profiles/high-assurance.profile.json",
    "generated/profile-catalog.json",
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-ASSURANCE-001",
    "DEC-HW-001",
    "DEC-AUTH-001",
    "DEC-IDENT-001",
    "DEC-GOV-001",
    "DEC-PRIV-001",
    "DEC-LIFE-001",
    "DEC-AI-001",
    "DEC-DATA-001"
  ],
  "requirement_ids": [
    "REQ-PROF-HA-001",
    "REQ-PROF-HA-002",
    "REQ-PROF-HA-003",
    "REQ-PROF-HA-004",
    "REQ-PROF-HA-005",
    "REQ-PROF-HA-006",
    "REQ-PROF-HA-007",
    "REQ-PROF-HA-008",
    "REQ-PROF-HA-009",
    "REQ-PROF-HA-010",
    "REQ-PROF-HA-011",
    "REQ-PROF-HA-012",
    "REQ-PROF-HA-013",
    "REQ-PROF-HA-014",
    "REQ-PROF-HA-015",
    "REQ-PROF-HA-016",
    "REQ-PROF-HA-017",
    "REQ-PROF-HA-018",
    "REQ-PROF-HA-019",
    "REQ-PROF-HA-020",
    "REQ-PROF-HA-021",
    "REQ-PROF-HA-022",
    "REQ-PROF-HA-023",
    "REQ-PROF-HA-024",
    "REQ-PROF-HA-025",
    "REQ-PROF-HA-026",
    "REQ-PROF-HA-027",
    "REQ-PROF-HA-028",
    "REQ-PROF-HA-029",
    "REQ-PROF-HA-030",
    "REQ-PROF-HA-031",
    "REQ-PROF-HA-032",
    "REQ-PROF-HA-033",
    "REQ-PROF-HA-034",
    "REQ-PROF-HA-035",
    "REQ-PROF-HA-036",
    "REQ-PROF-HA-037",
    "REQ-PROF-HA-038",
    "REQ-PROF-HA-039",
    "REQ-PROF-HA-040"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-AUTH-001",
    "LOCK-AUTH-002",
    "LOCK-AUTH-003",
    "LOCK-AUTH-004",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-PRIV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-015",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011",
    "DOC-SYS-001",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-SYS-020"
  ],
  "tags": [
    "profile-overlay",
    "high-assurance",
    "measured-boot",
    "hardware-trust",
    "key-custody",
    "separation-of-duties",
    "privilege",
    "audit",
    "recovery",
    "release-security",
    "offline"
  ]
}
KOA:DOC-META:END -->

# High-Assurance Overlay

## 1. Purpose

This document explains the `high_assurance` deployment overlay.

The overlay strengthens a compatible primary deployment profile with additional controls for:

- verified boot and measured system identity;
- hardware-backed node and workload identity;
- protected key custody;
- separation of duties;
- narrowly bounded privilege;
- mandatory access control;
- default-deny networking;
- tamper-evident audit;
- artifact and release verification;
- recovery under independent control;
- current conformance evidence.

The overlay changes the assurance posture of a deployment. It does not change the global product model, replace the primary deployment profile, or make its controls universal requirements for every kOA installation.

The machine-readable owner of overlay compatibility, composition, controls, requirements, tests, and evidence expectations is:

```text
contracts/profiles/high-assurance.profile.json
```

## 2. Scope

The overlay applies to a composed deployment consisting of:

```text
one compatible primary profile
+
high_assurance
+
zero or more compatible overlays
```

Compatible primary profiles are:

`user_lightweight`, `developer_linux_workstation`, `sovereign_linux_node`, `sovereign_hub`, `build_farm`, `control_plane`

The overlay is not compatible with `developer_windows_wsl`. WSL alone cannot establish the host measured-boot chain, hardware-rooted node identity, host privilege boundary, and recovery evidence required by the overlay.

Compatible overlays are:

`sovereign_offline`, `appliance_shell`

The overlay can apply to:

- endpoints;
- sovereign Linux nodes;
- hubs;
- build farms;
- control planes;
- Linux developer workstations;
- lightweight user deployments that meet the required hardware and control conditions.

The overlay does not define:

- a new primary profile;
- a universal Linux requirement;
- a mandatory desktop environment;
- a mandatory container engine;
- a mandatory cluster orchestrator;
- unrestricted remote administration;
- one hardware vendor;
- one hardware security module product;
- one mandatory-access-control implementation;
- one signature algorithm;
- exact port, path, unit, package, or container names.

Those choices remain owned by compatible profile contracts, component contracts, artifact contracts, toolchain contracts, security documents, and implementation recipes.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/profiles/high-assurance.profile.json` | Overlay identity, compatibility, merge semantics, required control components, assurance controls, requirements, tests, and evidence expectations. |
| `generated/profile-catalog.json` | Primary profile and overlay inventory. |
| `contracts/profiles/*.profile.json` | Primary component membership, topology, activation mode, hardware placement, resource limits, and network exposure. |
| `contracts/system.contract.json` | Global system, authority, offline, AI, degradation, and trust model. |
| `generated/component-catalog.json` | Component identities, responsibilities, ownership domains, and global boundaries. |
| `contracts/components/*.component.json` | Detailed component interfaces, stores, state transitions, failures, and security controls. |
| `contracts/release-channels.contract.json` | System, services, governance, and knowledge release-channel identities. |
| `contracts/artifact-classes.contract.json` | Artifact identity, verification, activation, rollback, revocation, and evidence rules. |
| `contracts/integration-types.contract.json` | External integration and external AI boundaries. |
| `generated/requirements-index.json` | Requirement statements displayed in section 5. |
| `generated/assertion-index.json` | Profile, authority, component, lifecycle, data, AI, and privilege invariants. |
| `generated/traceability.json` | Decision, requirement, lock, profile, component, test, evidence, exception, and claim relationships. |
| `generated/exception-index.json` | Approved deviations, duration, scope, compensating controls, and evidence. |
| `generated/test-catalog.json` | Profile, security, lifecycle, operations, system, and exit test definitions. |
| `generated/evidence-catalog.json` | Executed evidence for the active composed deployment. |

The overlay does not duplicate values owned by these sources.

## 4. Model and Responsibilities

### 4.1 Overlay model

`high_assurance` is a composable overlay rather than a standalone deployment profile.

The primary profile continues to own:

- normal component membership;
- activation modes;
- physical topology;
- hardware placement;
- base resource envelopes;
- ordinary network exposure;
- user and operator experience;
- profile-specific capability claims.

The overlay adds or narrows:

- assurance controls;
- required control components;
- hardware trust;
- identity protection;
- access and privilege rules;
- signing and key custody;
- network restrictions;
- audit and evidence;
- recovery;
- release and artifact verification;
- external integration and AI policy;
- conformance claim conditions.

### 4.2 Composition semantics

The canonical merge behavior is:

| Dimension | Merge rule |
| --- | --- |
| Permissions | Intersection |
| Obligations | Union |
| Resource minimums | Highest applicable minimum |
| Resource maximums | Lowest applicable maximum |
| Network exposure | Most restrictive rule |
| Audit and evidence | Most complete applicable requirement |
| Retention | Most restrictive compatible rule |
| Conflict | Blocked |

The overlay cannot weaken a global invariant.

The overlay cannot expand a capability excluded by the primary profile.

The overlay can add required control components when the composed deployment needs them.

An unresolved composition conflict does not produce an active deployment claim.

### 4.3 Assurance claim

The overlay creates the claim:

```text
CLAIM-PROFILE-HIGH-ASSURANCE
```

The claim applies to the composed deployment, not to the overlay file alone.

It indicates enhanced resistance to:

- privileged abuse;
- key compromise;
- artifact substitution;
- recovery capture;
- unauthorized disclosure;
- audit tampering;
- silent authority drift.

The claim depends on current authority, current evidence, the active profile composition, active releases, active artifacts, current trust state, and current control state.

A partial implementation does not create a partial high-assurance claim.

### 4.4 Required control components

| Component | Activation | Purpose |
| --- | --- | --- |
| `identity_and_trust` | required | Provide hardware-bound node and workload identity, scoped trust roots, delegation, revocation, and strong authentication context. |
| `governance_policy_runtime` | required | Evaluate authorization, disclosure, consent, privilege, activation, emergency, and exception policy deterministically. |
| `audit_broker` | required | Preserve classified, tamper-evident, attributable, and reviewable evidence for critical transitions. |
| `koa_node_agent` | required | Enforce the closed catalog of schema-bound privileged operations and reject arbitrary host control. |
| `resource_governor` | required | Protect identity, policy, audit, recovery, verification, and integrity-critical operations during resource pressure. |

`publication_gateway` becomes required when the composed profile permits private-to-public or cross-domain disclosure.

All other component inclusion and exclusion choices remain owned by the primary profile.

### 4.5 Hardware assurance

The overlay uses a hardware root of trust or an independently validated equivalent.

Accepted realizations include:

- TPM 2.0 with measured boot and protected keys;
- a platform security processor providing equivalent guarantees;
- a dedicated hardware security module for infrastructure roles combined with a separately verified boot chain.

The assurance model covers:

- secure boot or equivalent verified boot;
- measured firmware, boot policy, bootloader, kernel, initial system, and active system release;
- hardware-bound node identity;
- protected workload identity;
- rollback-resistant or monotonic state;
- trusted time for expiry, revocation, certificate, and evidence evaluation;
- controlled physical access for signing, recovery, and removable media.

A software-only emulation does not satisfy the hardware-root claim.

### 4.6 Host and runtime protection

The composed deployment uses:

- maintained firmware and kernel;
- verified system releases;
- an immutable or policy-controlled base;
- configuration-drift detection;
- enforcing mandatory access control;
- dedicated service identities;
- minimized Linux capabilities;
- `no_new_privileges` or an equivalent control;
- seccomp or an equivalent syscall boundary;
- explicit writable storage;
- rootless execution where compatible.

Unauthorized drift suspends the high-assurance claim until remediation and evidence complete.

Kubernetes is not an endpoint requirement. An orchestrator appears only when the primary profile explicitly adopts one.

### 4.7 Identity and access

Privileged human access uses phishing-resistant multi-factor authentication.

The overlay distinguishes:

- human identity;
- tenant and organization identity;
- role and delegation;
- node identity;
- workload and service identity;
- publisher identity;
- signer identity;
- artifact identity;
- release authority;
- activation authority.

Shared privileged accounts are excluded.

Delegation remains explicit, scoped, expiring, revocable, and non-transitive by default.

Critical trust-root, signing, recovery, break-glass, and high-impact governance actions use independent approval.

### 4.8 Key and secret custody

Key classes remain separate.

Protected classes include:

- system release signing;
- services release signing;
- governance policy signing;
- knowledge artifact signing;
- authority recognition;
- audit anchoring;
- node identity;
- recovery.

Release and authority private keys remain outside application nodes and ordinary build workers.

Accepted custody patterns include:

- hardware security modules;
- hardware tokens with independent approval;
- threshold or split-custody signing.

Service secrets use scoped delivery, explicit rotation, log exclusion, receipt exclusion, and ordinary-export exclusion.

Key recovery remains separate from data recovery.

### 4.9 Network posture

The overlay applies a default-deny posture.

When present, these zones remain distinct:

- public;
- private service;
- administrative;
- recovery;
- artifact or update;
- external-integration egress.

Sensitive remote interfaces use service-to-service authentication and mutual authentication when applicable.

Administrative services are not exposed directly to public networks.

External integration egress uses destination allowlists and separate policy for external AI transfer.

Loss of remote connectivity does not expand local authority.

### 4.10 Governance and privilege

Governance Policy Runtime evaluates governed decisions.

kOA Node Agent performs bounded privileged operations.

Normal privileged flow is:

```text
schema-bound request
-> authenticated subject and target
-> active governance decision
-> independent approval when required
-> operation and replay binding
-> allowlisted execution
-> before-and-after verification
-> protected receipt
-> review when required
```

Arbitrary shell, package-manager, file-copy, container, service-control, and key-export surfaces remain outside normal kOA privilege.

Break-glass authority uses:

- separate operation identities;
- stronger authentication;
- dual control;
- bounded capability and target;
- policy-bounded duration;
- automatic expiry;
- tamper-evident evidence;
- mandatory review.

### 4.11 Audit and evidence

Critical evidence classes include:

- identity and trust changes;
- governance decisions;
- privileged operations;
- release publication and signing;
- artifact verification and activation;
- trust-root changes;
- break-glass and recovery;
- publication and withdrawal;
- exceptions;
- conformance claims.

Evidence remains classified and minimized.

Public accountability evidence and restricted evidence remain separate.

Access to protected evidence creates its own audit record.

The deployment maintains an independent audit copy or equivalent tamper-evident anchor.

### 4.12 Artifact and release security

The four release channels remain independent:

- system;
- services;
- governance;
- knowledge.

The overlay adds:

- required provenance;
- publisher and signer identity;
- software bills of materials;
- build and signing separation;
- independent verification;
- reproducible-build evidence for build outputs;
- anti-downgrade and anti-substitution controls;
- verification before activation;
- atomic activation;
- last-known-good retention;
- rollback or forward repair;
- revocation handling.

Ordinary Markdown documentation does not receive an automatic hash requirement.

### 4.13 External integrations and AI

External integrations are disabled until explicitly enabled.

Approved external AI surfaces remain:

- ChatGPT;
- Suno;
- Gamma;
- Ariane external voice.

Their use depends on:

- explicit user initiation;
- destination allowlisting;
- data minimization;
- compatible policy for sensitive data;
- provenance on reimport;
- local review and admission.

Restricted and no-AI data remain outside these surfaces unless an explicit compatible policy permits the exact transfer.

External output remains a non-authoritative candidate.

### 4.14 Recovery and resilience

Recovery uses a separate reduced environment.

Recovery controls include:

- stronger authentication than ordinary administration;
- separate recovery credentials;
- dual control or split custody;
- explicit destructive-data handling;
- trust-root replacement evidence;
- independent approval;
- protected receipts;
- tested backup restoration;
- authority revalidation before reactivation.

The deployment retains locally available identity, policy, audit, artifact, and recovery functions needed for claimed offline operation.

### 4.15 Component-specific constraints

#### `identity_and_trust`

- Node and workload identities use hardware-bound or equivalently protected keys.
- Trust roots are scoped by tenant, environment, channel, artifact class, and authority domain.
- Revocation state and trust-root changes produce protected evidence.
- Authentication remains distinct from authorization.

#### `governance_policy_runtime`

- Unknown required facts fail closed.
- Critical decisions apply separation-of-duties and dual-control rules.
- Policy bundles activate independently and atomically.
- Emergency authority is explicit, bounded, expiring, and reviewable.

#### `audit_broker`

- Critical evidence uses protected append-only or tamper-evident storage.
- Audit classes remain separated by access, retention, encryption, disclosure, and deletion policy.
- Access to protected evidence is itself audited.
- Audit unavailability does not broaden authority.

#### `koa_node_agent`

- Arbitrary shell, package-manager, file-copy, container, service-control, and key-export operations are rejected.
- Every privileged operation is bound to an active policy decision and replay-protection value.
- Before-and-after state is verified.
- Break-glass operations use separate operation identities and stronger authorization.

#### `resource_governor`

- Identity, policy, audit, recovery, verification, and active-user control retain protected resource reservations.
- Optional heavy work is throttled or stopped before assurance-critical services.
- Resource control remains deterministic and non-AI.

#### `sentient`

- SenTient remains optional, isolated, task-activated, and non-authoritative.
- Restricted data is unavailable unless an explicit policy, classification, and workspace contract permits it.
- Candidate outputs require independent owning-component review.
- SenTient has no direct access to production authoritative stores or privileged host interfaces.

#### `ariane_runtime`

- External voice remains optional and non-authoritative.
- Sensitive actions require action-specific confirmation.
- Automation stops on stale observation, ambiguity, missing authority, or failed verification.
- Diagnostic capture is bounded and classified.

#### `uckk_platform`

- Restricted and no-AI content cannot be exported to external AI surfaces.
- Original media and provenance are preserved.
- Audience and rights restrictions apply to previews, search, exports, caches, and derivatives.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-PROF-HA-001,REQ-PROF-HA-002,REQ-PROF-HA-003,REQ-PROF-HA-004,REQ-PROF-HA-005,REQ-PROF-HA-006,REQ-PROF-HA-007,REQ-PROF-HA-008,REQ-PROF-HA-009,REQ-PROF-HA-010,REQ-PROF-HA-011,REQ-PROF-HA-012,REQ-PROF-HA-013,REQ-PROF-HA-014,REQ-PROF-HA-015,REQ-PROF-HA-016,REQ-PROF-HA-017,REQ-PROF-HA-018,REQ-PROF-HA-019,REQ-PROF-HA-020,REQ-PROF-HA-021,REQ-PROF-HA-022,REQ-PROF-HA-023,REQ-PROF-HA-024,REQ-PROF-HA-025,REQ-PROF-HA-026,REQ-PROF-HA-027,REQ-PROF-HA-028,REQ-PROF-HA-029,REQ-PROF-HA-030,REQ-PROF-HA-031,REQ-PROF-HA-032,REQ-PROF-HA-033,REQ-PROF-HA-034,REQ-PROF-HA-035,REQ-PROF-HA-036,REQ-PROF-HA-037,REQ-PROF-HA-038,REQ-PROF-HA-039,REQ-PROF-HA-040 -->
- **REQ-PROF-HA-001 — SHALL:** The overlay is composed with exactly one compatible primary profile.
- **REQ-PROF-HA-002 — SHALL:** The composed deployment establishes a verified boot chain and measured active system identity.
- **REQ-PROF-HA-003 — SHALL:** Node and workload identities use hardware-bound or equivalently protected keys.
- **REQ-PROF-HA-004 — SHALL:** Privileged human access uses phishing-resistant multi-factor authentication.
- **REQ-PROF-HA-005 — SHALL:** Trust-root, release-signing, destructive-recovery, and break-glass operations use independent approval.
- **REQ-PROF-HA-006 — SHALL:** Release and authority private keys remain outside application nodes and ordinary build workers.
- **REQ-PROF-HA-007 — SHALL:** Governance Policy Runtime, Audit Broker, kOA Node Agent, Identity and Trust, and Resource Governor are active.
- **REQ-PROF-HA-008 — SHALL:** Arbitrary privileged host operations are unavailable through normal kOA interfaces.
- **REQ-PROF-HA-009 — SHALL:** Every governed privileged operation is bound to a current policy decision and replay-protection value.
- **REQ-PROF-HA-010 — SHALL:** The host uses enforcing mandatory access control and least-privilege service isolation.
- **REQ-PROF-HA-011 — SHALL:** Durable sensitive state is encrypted and tenant and component data boundaries remain explicit.
- **REQ-PROF-HA-012 — SHALL:** Administrative and service networks follow default-deny and explicit allowlisting.
- **REQ-PROF-HA-013 — SHALL:** Remote administration uses a declared high-assurance policy, strong authentication, bounded scope, and evidence.
- **REQ-PROF-HA-014 — SHALL:** Removable media and offline bundles use quarantine, bounded parsing, verification, authorization, and controlled staging.
- **REQ-PROF-HA-015 — SHALL:** Release artifacts provide required provenance, signing, dependency, and software-bill-of-material evidence.
- **REQ-PROF-HA-016 — SHALL:** Artifact verification precedes atomic activation and preserves a last-known-good compatible state.
- **REQ-PROF-HA-017 — SHALL:** Downgrade, substitution, revoked-artifact, and incorrectly scoped activation attempts are rejected.
- **REQ-PROF-HA-018 — SHALL:** Critical security, authority, release, publication, recovery, and exception transitions produce protected evidence.
- **REQ-PROF-HA-019 — SHALL:** Protected evidence uses tamper-evident anchoring and access to protected evidence is audited.
- **REQ-PROF-HA-020 — SHALL:** Audit collection remains classified, minimized, and separated from unrestricted disclosure.
- **REQ-PROF-HA-021 — SHALL:** Break-glass authority is capability-scoped, time-bounded, attributable, expiring, and reviewed.
- **REQ-PROF-HA-022 — SHALL:** Recovery occurs in a separate reduced environment using stronger authentication and dual control.
- **REQ-PROF-HA-023 — SHALL:** Trust-root replacement requires independent approval, continuity evidence, and post-event audit.
- **REQ-PROF-HA-024 — SHALL:** Encrypted backups include an independent protected copy and pass controlled restore tests.
- **REQ-PROF-HA-025 — SHALL:** External integrations and AI surfaces are disabled by default and cannot directly mutate authority.
- **REQ-PROF-HA-026 — SHALL:** Restricted and no-AI data cannot be transferred to external AI surfaces without explicit compatible policy.
- **REQ-PROF-HA-027 — SHALL:** SenTient remains isolated, task-activated, non-authoritative, and disconnected from production authoritative stores.
- **REQ-PROF-HA-028 — SHALL:** Resource pressure preserves identity, policy, audit, verification, recovery, and interactive control before optional work.
- **REQ-PROF-HA-029 — SHALL:** Active release, artifact, component, trust, revocation, and drift identities remain inspectable.
- **REQ-PROF-HA-030 — SHALL:** Security and authority failures degrade only affected capabilities and never broaden authority.
- **REQ-PROF-HA-031 — SHALL:** Profile composition conflicts block activation rather than selecting a silent precedence.
- **REQ-PROF-HA-032 — SHALL:** The overlay does not generalize Linux-specific implementation choices into global system requirements.
- **REQ-PROF-HA-033 — SHALL:** The overlay does not require Kubernetes for endpoint profiles.
- **REQ-PROF-HA-034 — SHALL:** Public, private, administrative, recovery, artifact, and integration boundaries remain separated when present.
- **REQ-PROF-HA-035 — SHALL:** Service, node, workload, publisher, signer, artifact, tenant, and authority identities remain distinct.
- **REQ-PROF-HA-036 — SHALL:** Exceptions are registered, expiring, evidence-backed, and unable to waive constitutional controls.
- **REQ-PROF-HA-037 — SHALL:** The composed profile retains offline operation for every capability claimed as locally available.
- **REQ-PROF-HA-038 — SHALL:** Conformance evidence is current for the active authority release, target environment, profile composition, and artifact set.
- **REQ-PROF-HA-039 — SHALL:** A failed required control, test, or evidence check suspends the high-assurance claim.
- **REQ-PROF-HA-040 — SHALL:** The high-assurance claim has complete decision, requirement, lock, test, evidence, exception, component, profile, and release traceability.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Overlay composition

1. Select one primary profile.
2. Verify that the primary profile appears in the overlay's compatible list.
3. Resolve any additional overlays.
4. Apply the declared overlay order.
5. Merge permissions, obligations, resources, network exposure, audit, and retention.
6. Resolve required control components.
7. evaluate component and profile conflicts.
8. evaluate hardware and control prerequisites.
9. create the candidate composed profile.
10. run conformance validation.
11. register evidence.
12. activate the high-assurance claim only after a passing result.

### 6.2 Node enrollment

1. Verify firmware and boot-policy state.
2. verify secure boot or equivalent.
3. collect measured-boot evidence.
4. create or activate the hardware-bound node identity.
5. register the target environment and primary profile.
6. install active trust roots and revocation state.
7. verify mandatory access control.
8. activate required control components.
9. verify release and artifact identities.
10. run enrollment tests.
11. register evidence.
12. admit the node into the high-assurance deployment.

### 6.3 Privileged operation

1. Create a schema-bound request.
2. authenticate the human, workload, node, and target.
3. resolve current authority and trust state.
4. evaluate policy.
5. complete independent approval where required.
6. bind the decision to operation, target, scope, expiry, and replay protection.
7. execute through kOA Node Agent.
8. verify before-and-after state.
9. secure local evidence.
10. submit the result for review when required.

### 6.4 Release activation

1. receive the release candidate.
2. verify artifact identity, publisher, signer, provenance, dependencies, and software bill of materials.
3. evaluate profile and Release Set compatibility.
4. run required tests.
5. resolve activation authority.
6. preserve the last-known-good state.
7. activate atomically.
8. verify resulting identity and health.
9. secure activation evidence.
10. update the high-assurance claim state.

### 6.5 Break-glass activation

1. declare the emergency condition.
2. identify the bounded emergency capability and target.
3. authenticate independent actors.
4. obtain dual approval.
5. activate an expiring emergency grant.
6. execute only the emergency operation.
7. record tamper-evident evidence.
8. expire the grant automatically.
9. conduct post-event review.
10. remediate any temporary deviation.

### 6.6 Recovery

1. enter the reduced recovery environment.
2. authenticate recovery custodians.
3. verify recovery media and artifacts.
4. verify the active or intended Release Set.
5. identify the last known trustworthy state.
6. restore data and artifacts through controlled procedures.
7. revalidate trust, revocation, identities, and authority.
8. run restore and conformance tests.
9. register recovery evidence.
10. reactivate ordinary operation.

### 6.7 Trust-root replacement

1. identify the compromised, expired, or replaced trust root.
2. freeze affected signing or activation paths.
3. authenticate independent approvers.
4. establish continuity or replacement evidence.
5. activate the replacement root.
6. revoke or retire the predecessor.
7. update affected identities, channels, and artifact validation.
8. verify active releases and artifacts.
9. record protected evidence.
10. conduct post-event audit.

### 6.8 Claim suspension and restoration

The high-assurance claim enters a suspended or blocked state when:

- required evidence expires;
- hardware or boot identity becomes unverifiable;
- mandatory access control is disabled;
- required control components are inactive;
- unauthorized drift appears;
- key custody is compromised;
- a required test fails;
- an unresolved composition conflict appears.

Restoration requires remediation, retesting, current evidence, and renewed traceability.

## 7. Failure and Degradation

### 7.1 Missing hardware assurance

When the required hardware root, measured boot, or attestation evidence is unavailable:

- the high-assurance claim remains blocked;
- the primary profile can remain active under its own claim when safe;
- protected activation and administration can become restricted;
- the deployment does not substitute self-attestation for missing evidence.

### 7.2 Control-component failure

A failure of Identity and Trust, Governance Policy Runtime, Audit Broker, kOA Node Agent, or Resource Governor affects only capabilities that depend on that control.

Examples:

- new governed actions block when policy is unavailable;
- privileged host mutation blocks when the Node Agent is unavailable;
- critical transitions wait for durable local evidence when audit storage is unavailable;
- optional work stops before protected control services under resource pressure.

The failure does not broaden authority.

### 7.3 Key compromise

A suspected key compromise triggers:

- affected key and identity suspension;
- artifact or release activation freeze;
- revocation evaluation;
- independent incident review;
- replacement or recovery procedure;
- revalidation of affected releases and artifacts;
- evidence preservation.

A restored key does not regain authority automatically.

### 7.4 Audit-anchor failure

When the independent audit anchor is unavailable:

- local protected evidence remains durable;
- forwarding uses bounded queues;
- critical transitions complete only when their local evidence requirement is satisfied;
- the high-assurance claim can become restricted or suspended according to evidence freshness policy.

### 7.5 Network loss

Offline operation preserves local identity, policy, audit, recovery, release, and runtime functions within their valid envelope.

External integrations and remote administration become unavailable.

Remote loss does not permit wider local authority or weaker authentication.

### 7.6 Resource pressure

Resource Governor preserves:

- identity;
- policy;
- audit;
- privileged-operation control;
- artifact verification;
- recovery;
- interactive user control.

Optional heavy work, SenTient, derivatives, indexing, and nonessential background processing stop or throttle first.

### 7.7 Recovery failure

When rollback, clean restore, or forward repair fails:

- affected capabilities remain blocked;
- the primary profile and unaffected components can remain available when safe;
- evidence and recoverable state remain preserved;
- the deployment does not claim high assurance until recovery succeeds and current evidence exists.

### 7.8 External integration failure

An optional integration failure removes only the integration capability.

Core operation, local evidence, authority, and recovery remain available.

No queued external AI result gains authority merely because it returns later.

### 7.9 Composition conflict

A conflict between the primary profile and overlay produces a blocked composition.

The validator does not choose whichever rule appears newer, stricter, more common, or easier to implement.

## 8. Cross-Component Interactions

| Source | Target | High-assurance interaction |
| --- | --- | --- |
| Identity and Trust | All consuming components | Provides hardware-bound identity, trust-root, delegation, and revocation context. |
| Governance Policy Runtime | Owning components | Provides explicit decisions and obligations for governed actions. |
| Governance Policy Runtime | kOA Node Agent | Binds privilege decisions to exact operations and replay controls. |
| kOA Node Agent | Host operating system | Executes only allowlisted schema-bound protected operations. |
| Components | Audit Broker | Emit classified security, authority, release, publication, and recovery evidence. |
| Resource Governor | Required control components | Preserves protected resource capacity and bounded queues. |
| Release authority | Artifact lifecycle | Publishes approved channel releases without becoming target activation authority. |
| Runtime owner | Artifact lifecycle | Verifies and activates only compatible artifacts for its own runtime state. |
| Publication Gateway | Konnaxion | Delivers only approved and policy-conformant public outputs. |
| External integrations | Owning component | Provide candidate input through explicit admission boundaries. |
| SenTient | Review workflow | Produces isolated candidates without direct production writes. |
| Recovery environment | Active deployment | Restores only verified state under stronger authentication and independent approval. |

Direct cross-component writes remain prohibited.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Closed decisions

| Decision | Closed overlay rule |
| --- | --- |
| `DEC-PROFILE-001` | `high_assurance` is a composable overlay and not a primary profile. |
| `DEC-ASSURANCE-001` | The high-assurance claim depends on complete current controls and evidence. |
| `DEC-HW-001` | Hardware-rooted trust and measured boot support the claim. |
| `DEC-AUTH-001` | Every protected capability uses explicit bounded authority. |
| `DEC-IDENT-001` | Identity, authentication, authorization, signing, and activation authority remain separate. |
| `DEC-GOV-001` | Governance Policy Runtime and Resource Governor remain separate authorities. |
| `DEC-PRIV-001` | Privileged operations use the narrow kOA Node Agent. |
| `DEC-LIFE-001` | Release channels remain independently identified and activated. |
| `DEC-AI-001` | External AI remains optional, explicit, and non-authoritative. |
| `DEC-DATA-001` | Authoritative stores retain one owner and reject direct cross-component writes. |

### 9.2 Prohibited assumptions

Authors, implementers, validators, and AI agents do not assume that:

- the overlay can operate without a primary profile;
- high assurance is a synonym for sovereign Linux;
- WSL proves host high assurance;
- root access proves governance authority;
- secure boot alone proves the full claim;
- a TPM alone proves application integrity;
- a valid signature grants activation authority;
- more logging automatically creates better assurance;
- protected audit evidence can be public by default;
- a shared administrator account is acceptable;
- self-approval satisfies separation of duties;
- break-glass access can persist indefinitely;
- remote administration can remain permanently open;
- Kubernetes is required for endpoints;
- one hardware vendor is mandatory;
- ordinary Markdown needs content hashes;
- external AI can receive restricted data by default;
- SenTient becomes authoritative because it runs inside the deployment;
- recovery credentials can be identical to ordinary administration credentials;
- restoring a key automatically restores authority;
- an exception can waive a constitutional control;
- a passing configuration review replaces executed evidence;
- expired evidence still supports the active claim;
- a stricter overlay rule can silently conflict with the primary profile.

A new implementation-affecting assurance choice requires an accepted owner decision before dependent authority becomes active.

## 10. Validation Criteria

The high-assurance claim is conformant only when all applicable tests and evidence pass.

| Validation group | Required tests |
| --- | --- |
| Profile composition | `TEST-PROF-001`, `TEST-PROF-002`, `TEST-PROF-003`, `TEST-PROF-004`, `TEST-PROF-005`, `TEST-PROF-006`, `TEST-PROF-007`, `TEST-PROF-008`, `TEST-PROF-009`, `TEST-PROF-013`, `TEST-PROF-014` |
| Security and trust | `TEST-SEC-001`, `TEST-SEC-002`, `TEST-SEC-003`, `TEST-SEC-004`, `TEST-SEC-005`, `TEST-SEC-006`, `TEST-SEC-007`, `TEST-SEC-008`, `TEST-SEC-009`, `TEST-SEC-010`, `TEST-SEC-011`, `TEST-SEC-012`, `TEST-SEC-013`, `TEST-SEC-014`, `TEST-SEC-015` |
| Lifecycle and artifacts | `TEST-LIFE-001`, `TEST-LIFE-002`, `TEST-LIFE-003`, `TEST-LIFE-004`, `TEST-LIFE-005`, `TEST-LIFE-006`, `TEST-LIFE-007`, `TEST-LIFE-008`, `TEST-LIFE-009`, `TEST-LIFE-010`, `TEST-LIFE-011`, `TEST-LIFE-015` |
| Operations and recovery | `TEST-OPS-001`, `TEST-OPS-002`, `TEST-OPS-003`, `TEST-OPS-004`, `TEST-OPS-005`, `TEST-OPS-006`, `TEST-OPS-007`, `TEST-OPS-008`, `TEST-OPS-009`, `TEST-OPS-010` |
| System and boundaries | `TEST-SYS-001`, `TEST-SYS-004`, `TEST-SYS-005`, `TEST-SYS-011`, `TEST-SYS-012`, `TEST-SYS-013`, `TEST-CROSS-007`, `TEST-CROSS-008`, `TEST-CROSS-009`, `TEST-CROSS-013`, `TEST-CROSS-014`, `TEST-CROSS-015` |
| Portability and exit | `TEST-EXIT-001`, `TEST-EXIT-002`, `TEST-EXIT-003`, `TEST-EXIT-004`, `TEST-EXIT-005`, `TEST-EXIT-006`, `TEST-EXIT-007`, `TEST-EXIT-008` |

Required evidence types include:

- profile-composition validation;
- measured-boot evidence;
- attestation results;
- hardware-bound identity evidence;
- mandatory-access-control validation;
- privileged-operation negative tests;
- policy test-vector results;
- separation-of-duties evidence;
- key-custody evidence;
- artifact provenance and signing evidence;
- software bills of materials;
- Release Set compatibility results;
- activation and rollback results;
- revocation tests;
- tamper-evident audit validation;
- protected-evidence access tests;
- network-boundary validation;
- offline-operation results;
- backup and restore results;
- break-glass expiry results;
- recovery exercises;
- external-integration removal results;
- resource-pressure results;
- clean export and restore results.

Additional validation confirms:

1. the overlay is composed with exactly one compatible primary profile;
2. every required component exists and is active;
3. every component-specific constraint references a registered component;
4. every decision, requirement, lock, exception, and test reference resolves;
5. hardware, identity, key custody, network, privilege, audit, release, and recovery controls are complete;
6. external AI boundaries are explicit;
7. offline claims are tested;
8. resource reservations protect control components;
9. active evidence matches the current authority release, environment, profile composition, and artifact set;
10. no unresolved authority marker exists;
11. all active prose is in English.

A failed test produces `fail`.

Missing, stale, or unavailable required evidence produces `blocked`.

The high-assurance claim activates only after `pass`.

## 11. Non-Normative Examples

### 11.1 Sovereign Linux node with high assurance

A sovereign Linux node composes:

```text
sovereign_linux_node
+
high_assurance
```

The primary profile provides signed system activation, offline bundles, recovery, storage, and node topology.

The overlay adds measured boot, hardware-bound identity, independent signing custody, dual-control recovery, tamper-evident audit, and stricter artifact verification.

### 11.2 Lightweight user deployment

A lightweight user deployment can compose `high_assurance` when its hardware and control environment meet the overlay requirements.

The primary profile can still exclude SenTient, GF Wordbench, development containers, and heavy background services.

The overlay does not add those components. It adds the required control components and assurance behavior.

### 11.3 Developer Linux workstation

A Linux developer workstation can use the overlay for protected release or governance work.

Development workspaces remain isolated. Build workers do not receive release-signing keys. Production activation authority remains separate from development access.

### 11.4 Failed measured boot

A node boots but cannot verify the measured system identity.

The primary profile can enter a restricted recovery or diagnostic state. The high-assurance claim remains blocked. Privileged activation and trust-sensitive operations remain unavailable until the boot identity is verified or recovery completes.

### 11.5 Break-glass recovery

Two authorized custodians approve an expiring recovery operation.

The request is bound to one target and one capability. kOA Node Agent executes the allowlisted operation. Evidence records the actors, policy, target, timing, before-and-after state, and automatic expiry.

The emergency grant does not become a reusable administrator role.

### 11.6 External AI request

A user asks to export selected non-restricted material to Gamma.

The integration remains disabled until explicitly enabled. Policy evaluates the data classification and destination. The export contains only the selected material. The returned presentation is a non-authoritative candidate requiring local review and admission.

### 11.7 Release signing

A build farm produces a reproducible services artifact and software bill of materials.

A separate signing authority verifies provenance and test evidence. A protected signing key signs the release manifest after independent approval. The target environment separately evaluates compatibility and activation authority.

Build success does not equal signing or activation authority.

### 11.8 Claim suspension

A required audit anchor becomes unavailable beyond the permitted evidence window.

Local operation can continue according to the primary profile and degradation rules. The high-assurance claim becomes suspended or blocked until the anchor is restored, evidence is reconciled, and required tests pass.
