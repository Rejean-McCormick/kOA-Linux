<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-021",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global",
    "profile_conditioned_security"
  ],
  "canonical_refs": [
    "contracts/security-controls.contract.json",
    "schemas/security-controls.contract.schema.json",
    "contracts/artifact-contracts/security-evidence.schema.json",
    "07-security/00-threat-model.md",
    "07-security/01-security-baseline.md",
    "07-security/02-security-domains.md",
    "07-security/03-identity-trust-and-signatures.md",
    "07-security/04-trust-root-scoping.md",
    "07-security/05-privilege-boundaries.md",
    "07-security/06-privileged-broker.md",
    "07-security/07-secrets-and-keys.md",
    "07-security/08-network-boundaries.md",
    "07-security/09-storage-boundaries.md",
    "07-security/10-data-at-rest.md",
    "07-security/15-selective-audit.md",
    "07-security/18-offline-import-security.md",
    "07-security/19-software-supply-chain.md",
    "07-security/20-break-glass-security.md",
    "03-profiles/00-profile-model.md",
    "09-conformance/04-profile-test-matrices.md",
    "09-conformance/05-test-evidence.md"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-SEC-CTRL-001",
    "LOCK-SEC-CTRL-002",
    "LOCK-SEC-CTRL-003",
    "LOCK-SEC-CTRL-004",
    "LOCK-SEC-CTRL-005",
    "LOCK-SEC-CTRL-006",
    "LOCK-SEC-CTRL-007",
    "LOCK-SEC-CTRL-008"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003",
    "DOC-SEC-004",
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-007",
    "DOC-SEC-008",
    "DOC-SEC-009",
    "DOC-SEC-010",
    "DOC-SEC-015",
    "DOC-SEC-018",
    "DOC-SEC-019",
    "DOC-SEC-020",
    "DOC-PRO-000",
    "DOC-CONF-004",
    "DOC-CONF-005",
    "DOC-GOV-015"
  ],
  "tags": [
    "security",
    "controls",
    "architecture",
    "profile-applicability",
    "evidence",
    "recovery"
  ]
}
KOA:DOC-META:END -->

# Security Control Architecture

## 1. Purpose

This document adds the control-orchestration layer for the existing kOA security corpus. It does not replace the threat model, security baseline, identity model, privilege boundary, key model, network boundary, storage boundary, privacy rules, offline-import rules, software-supply-chain rules, audit model, or break-glass rules.

The thematic documents remain authoritative for the meaning and behavior of their security domains. `contracts/security-controls.contract.json` is the canonical owner of security-control identifiers, category membership, profile applicability, implementation bindings, validation bindings, failure behavior, and evidence classes.

A security claim is valid only when the applicable thematic rule, control record, implementation, validation result, and retained evidence agree.

## 2. Security Control Model

A kOA security control SHALL be represented by one active control record containing:

- one stable `control_id`;
- one category;
- one accountable owner;
- one canonical thematic document;
- one concise enforceable objective;
- one implementation binding;
- one validation binding;
- one declared failure behavior;
- one evidence class;
- one applicability state for every profile contract;
- an applicability condition when the control depends on ownership of hardware, boot, remote administration, removable media, or another conditional surface.

A control record does not replace the normative requirement expressed by its canonical thematic document. It binds that requirement to implementation and conformance.

## 3. Security Invariants

The following invariants apply across the complete system.

### 3.1 `SEC-INV-001` — Verified activation

No critical system, service, policy, release set, or governed artifact SHALL become active without verification of its identity, digest, compatibility, admission state, and applicable signature policy.

### 3.2 `SEC-INV-002` — Default deny

Filesystem, network, device, process, privilege, and external-integration access SHALL be denied unless explicitly declared by the owning contract and active profile.

### 3.3 `SEC-INV-003` — No implicit privilege

Locality, installation, application administration, user-interface visibility, navigation state, governance influence, or ownership of business data SHALL NOT imply machine privilege.

### 3.4 `SEC-INV-004` — One owner per authoritative state

No component or subsystem SHALL directly mutate another owner’s private authoritative state. Exchange SHALL use a declared interface, gateway, import, publication path, or receipt-bearing transition.

### 3.5 `SEC-INV-005` — Closed privileged operations

No arbitrary shell command, path, unit, device operation, mount request, or capability SHALL cross the privileged broker. Privileged operations SHALL be registered, typed, bounded, authorized, idempotent where applicable, and receipted.

### 3.6 `SEC-INV-006` — Traceable active artifacts

Every active governed artifact SHALL have an origin, version, digest, applicable signature policy, provenance, compatibility declaration, and applicable software bill of materials.

### 3.7 `SEC-INV-007` — Accountability without indiscriminate surveillance

Critical security actions SHALL be traceable. Event collection, retention, correlation, and disclosure SHALL remain purpose-limited, profile-bounded, and privacy-minimized.

### 3.8 `SEC-INV-008` — Proven recovery

Backup, rollback, last-known-good, disaster-recovery, and independent-restore claims SHALL require successful exercises and retained evidence.

## 4. Control Lifecycle

The lifecycle of a control is:

```text
security risk or invariant
        ↓
canonical thematic rule
        ↓
control identity and profile applicability
        ↓
implementation binding
        ↓
validation binding
        ↓
security evidence
        ↓
profile and release conformance decision
```

A control SHALL NOT move directly from prose to a conformance claim. A control without implementation, validation, or evidence binding remains architecturally declared but cannot satisfy a required profile claim.

### 4.1 Creation

A new control requires:

1. a security risk, invariant, or thematic requirement that is not already represented;
2. a unique identifier in `contracts/security-controls.contract.json`;
3. a canonical thematic document;
4. applicability for every active profile contract;
5. an owner, failure behavior, implementation binding, validation binding, and evidence class;
6. successful semantic validation.

### 4.2 Modification

A semantic control change SHALL identify its impact on:

- affected profiles;
- implementation generators and deployed configuration;
- tests and runtime probes;
- existing evidence validity;
- active exceptions;
- release compatibility and rollback;
- threat-model assumptions.

Changing only the matrix presentation without changing the contract has no normative effect.

### 4.3 Retirement

A control identifier SHALL NOT be reused. Retirement requires an accepted replacement or a recorded reason why the risk no longer applies. Existing evidence and historical conformance records SHALL retain the retired identifier.

## 5. Applicability States

The allowed states are:

- `required` — the profile cannot claim conformance without passing evidence for the control;
- `recommended` — the profile is expected to implement the control unless an accepted architecture decision documents why the risk is otherwise bounded;
- `optional` — the control may be implemented and, when implemented, SHALL satisfy its canonical rule and evidence requirements;
- `prohibited` — the profile SHALL NOT implement the behavior represented by the control;
- `not_applicable` — the profile does not own or expose the controlled surface.

`not_applicable` is not equivalent to `pass`. It requires a profile or deployment fact that proves the controlled surface is absent or owned by another platform boundary.

An overlay profile SHALL narrow or strengthen its base profile. It SHALL NOT silently weaken a required base-profile control.

## 6. Control Ownership

Control ownership means accountability for keeping the control definition, implementation binding, validation binding, failure behavior, and evidence requirements aligned. It does not transfer ownership of another component’s data or internal behavior.

Typical owners include:

- `security_architecture` for invariants, default-deny policy, and cross-profile composition;
- `host_platform` for boot, system image, Linux isolation, networking, storage, and recovery environment;
- `identity_and_trust` for identities, credentials, signatures, trust roots, and revocation;
- `koa_node_agent` for the privileged broker;
- `release_authority` for release admission, signing, promotion, anti-rollback metadata, and revocation;
- `audit_broker` for security-event structure, integrity, retention, and selective evidence;
- `data_owners` for data classification, encryption, retention, export, and deletion;
- `component_maintainers` for secure-development controls within their code boundary;
- `backup_restore_owner` and `incident_response_owner` for recovery and incident controls.

An owner MAY delegate implementation work. Accountability for the control remains singular.

## 7. Implementation Bindings

An implementation binding identifies the source or generated-output boundary expected to enforce a control. It is not a claim that every referenced file already exists.

Bindings SHALL follow the frozen code and filesystem architecture when that architecture is active. Generated configuration SHALL remain derived from canonical contracts and SHALL NOT become an independent security authority.

Examples include:

- host boot and image configuration;
- systemd and mandatory-access-control profiles;
- identity and trust services;
- privileged-broker operation registries;
- network policy renderers;
- release verification and signing pipelines;
- offline-import quarantine;
- audit and backup services.

A required control SHALL NOT be implemented only by a user-interface restriction. Hiding a command, route, button, module, or widget is not authorization or privilege enforcement.

## 8. Validation Bindings

A validation binding SHALL identify at least one of:

- deterministic contract validation;
- static configuration analysis;
- unit or property tests;
- integration tests;
- negative tests;
- fuzzing;
- runtime probes;
- boot or activation tests;
- restore or incident exercises;
- independent review where automation cannot prove the property.

A test SHALL verify the behavior at the authority boundary. An end-to-end interface test alone does not prove authorization, privilege isolation, signature verification, data ownership, or recovery correctness.

Validation SHALL test expected failure behavior. A control that passes only when all dependencies are healthy is incomplete if the declared security property matters during failure or offline operation.

## 9. Security Evidence

Security evidence SHALL conform to `contracts/artifact-contracts/security-evidence.schema.json` and identify:

- the control and profile;
- the evaluated subject;
- the implementation and version;
- the validation method and tests;
- start and completion times;
- result and observations;
- applicable exceptions;
- evidence and subject digests;
- disclosure and retention classes;
- signer information where required.

Evidence is not authority. A passing evidence object does not activate a release, grant authorization, or supersede an owner decision. Profile conformance evaluates the complete required-control set and the freshness, integrity, scope, and compatibility of its evidence.

Evidence SHALL be regenerated when a change can invalidate the tested property, including changes to:

- the implementation;
- the active profile;
- the kernel, container runtime, system manager, or security backend;
- the identity or trust configuration;
- the validation method;
- the relevant threat-model assumption;
- a dependency or release input;
- an exception or compensating control.

## 10. Failure Behavior

Every control declares a failure behavior. Failure behavior SHALL be enforced by the owning authority rather than inferred by the interface.

Allowed architectural patterns include:

- deny the operation;
- refuse service or artifact activation;
- block merge, build, release, or conformance claim;
- quarantine an import or restore candidate;
- restore the last-known-good state;
- enter a bounded recovery or incident mode;
- preserve local audit while degrading capability;
- deny unsafe disclosure.

A failure SHALL NOT trigger an undeclared substitute, silently weaken the profile, bypass an authority owner, or promote candidate data to authoritative state.

## 11. Exceptions and Compensating Controls

A security exception SHALL be explicit, bounded, reviewable, and temporary unless an accepted architecture decision establishes a permanent profile rule.

An exception SHALL record:

- the affected control and profile;
- the affected implementation and deployment scope;
- the risk accepted;
- the accountable approver;
- compensating controls;
- issue and expiry times;
- required review or remediation event;
- suspended conformance claims;
- evidence and incident references.

An expired or unresolved exception SHALL fail closed for the affected conformance claim.

## 12. Relationship to Existing Security Documents

The control contract points to existing thematic authority:

| Control family | Thematic authority |
| --- | --- |
| Threats and baseline | `00-threat-model.md`, `01-security-baseline.md` |
| Domains and isolation | `02-security-domains.md`, `05-privilege-boundaries.md` |
| Identity and trust | `03-identity-trust-and-signatures.md`, `04-trust-root-scoping.md` |
| Privileged operations | `06-privileged-broker.md` |
| Keys and secrets | `07-secrets-and-keys.md` |
| Network and storage | `08-network-boundaries.md`, `09-storage-boundaries.md`, `10-data-at-rest.md` |
| Privacy and evidence | `13-privacy-and-disclosure.md`, `15-selective-audit.md`, `16-public-evidence-and-private-proof.md` |
| Offline import | `18-offline-import-security.md` |
| Supply chain | `19-software-supply-chain.md`, lifecycle provenance documents |
| Emergency privilege | `20-break-glass-security.md`, operations break-glass procedures |
| Incident and recovery | operations incident, backup, restore, and disaster-recovery documents |

This document SHALL NOT be used to reinterpret a thematic rule. A conflict is resolved by the documentation authority and change protocol, not by selecting the less restrictive text.

## 13. Conformance

A profile security claim requires:

1. a resolved profile and overlay composition;
2. the complete required-control set from the canonical contract;
3. no prohibited control behavior;
4. valid evidence for every required control;
5. valid exceptions for any explicitly waived requirement;
6. successful security-architecture validation;
7. successful profile, release, and evidence validation;
8. retained recovery evidence where required.

Recommended controls that are not implemented SHALL have an accepted and bounded rationale before a production or sovereign conformance claim is made.

## 14. Validation Criteria

`tools/check_security_architecture.py` SHALL reject:

- duplicate or malformed control identifiers;
- unknown profiles, categories, or applicability states;
- a control missing any profile classification;
- a control listed under more than one state for a profile;
- a missing canonical document;
- a missing owner, implementation binding, validation binding, failure behavior, or evidence class;
- a matrix that omits or invents control identifiers;
- an unresolved evidence schema or example;
- a profile record whose contract reference is missing;
- fewer or different security invariants than the active contract declares.

## 15. Architecture Locks

- `LOCK-SEC-CTRL-001` — thematic security documents remain authoritative for security behavior; the control contract owns identifiers and applicability.
- `LOCK-SEC-CTRL-002` — every active control has one owner and one complete profile-applicability mapping.
- `LOCK-SEC-CTRL-003` — a required control without implementation, validation, failure behavior, and evidence class cannot satisfy conformance.
- `LOCK-SEC-CTRL-004` — user-interface visibility and navigation state never provide authorization or machine privilege.
- `LOCK-SEC-CTRL-005` — generated security configuration is derived and never becomes independent authority.
- `LOCK-SEC-CTRL-006` — exceptions are bounded, expiring, compensating, and conformance-aware.
- `LOCK-SEC-CTRL-007` — security evidence records validation results but does not activate, authorize, or supersede owner authority.
- `LOCK-SEC-CTRL-008` — no security, backup, rollback, or recovery claim is conforming without retained validation evidence.
