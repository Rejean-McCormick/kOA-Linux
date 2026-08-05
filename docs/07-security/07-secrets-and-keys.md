<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-007",
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
    "contracts/system.contract.json#/security",
    "generated/component-catalog.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SEC-001",
    "DEC-PRIV-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-PROFILE-001",
    "DEC-LIFE-001",
    "DEC-REL-001",
    "DEC-OFFLINE-001",
    "DEC-RECEIPT-001",
    "DEC-AUDIT-001",
    "DEC-PORT-001",
    "DEC-INTEGRATION-001",
    "DEC-AI-001",
    "DEC-IMAGE-001",
    "DEC-OS-001",
    "DEC-DEV-001",
    "DEC-DEV-002"
  ],
  "requirement_ids": [
    "REQ-SEC-SECRET-001",
    "REQ-SEC-SECRET-002",
    "REQ-SEC-SECRET-003",
    "REQ-SEC-SECRET-004",
    "REQ-SEC-SECRET-005",
    "REQ-SEC-SECRET-006",
    "REQ-SEC-SECRET-007",
    "REQ-SEC-SECRET-008",
    "REQ-SEC-SECRET-009",
    "REQ-SEC-SECRET-010",
    "REQ-SEC-SECRET-011",
    "REQ-SEC-SECRET-012",
    "REQ-SEC-SECRET-013",
    "REQ-SEC-SECRET-014",
    "REQ-SEC-SECRET-015",
    "REQ-SEC-SECRET-016",
    "REQ-SEC-SECRET-017",
    "REQ-SEC-SECRET-018",
    "REQ-SEC-SECRET-019",
    "REQ-SEC-SECRET-020",
    "REQ-SEC-SECRET-021",
    "REQ-SEC-SECRET-022",
    "REQ-SEC-SECRET-023",
    "REQ-SEC-SECRET-024",
    "REQ-SEC-SECRET-025",
    "REQ-SEC-SECRET-026",
    "REQ-SEC-SECRET-027",
    "REQ-SEC-SECRET-028",
    "REQ-SEC-SECRET-029",
    "REQ-SEC-SECRET-030",
    "REQ-SEC-SECRET-031",
    "REQ-SEC-SECRET-032"
  ],
  "lock_ids": [
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-PRIV-001",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-REL-001",
    "LOCK-REL-002",
    "LOCK-OFFLINE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-PORT-001",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
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
    "DOC-DEV-001",
    "DOC-DEV-003",
    "DOC-DEV-009",
    "DOC-LIFE-004",
    "DOC-LIFE-011",
    "DOC-LIFE-012",
    "DOC-LIFE-013",
    "DOC-LIFE-014",
    "DOC-SYS-001",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-009",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-COMP-001",
    "DOC-COMP-002",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-009",
    "DOC-CONST-010",
    "DOC-CONST-011"
  ],
  "tags": [
    "security",
    "secrets",
    "keys",
    "credentials",
    "certificates",
    "tokens",
    "trust-roots",
    "service-identities",
    "rotation",
    "revocation",
    "recovery",
    "offline",
    "break-glass",
    "supply-chain"
  ]
}
KOA:DOC-META:END -->

# Secrets and Keys

## 1. Purpose

This document defines the global kOA model for secrets, keys, credentials, certificates, trust roots, tokens, recovery factors, and related cryptographic authority.

The model protects:

- user authenticators;
- service identities;
- private signing keys;
- transport credentials;
- data-encryption keys;
- key-wrapping keys;
- release and artifact publication keys;
- certificate authorities and trust roots;
- integration credentials;
- recovery credentials and factors;
- emergency credentials;
- session and delegation tokens.

The model is built around explicit ownership, purpose separation, least capability, bounded validity, revocation, offline verification, recovery, evidence, and complete removal.

A secret is not merely a string. It is an authority-bearing object with a lifecycle, scope, owner, dependent capabilities, and failure consequences.

Cryptographic algorithms, key sizes, protected-store implementations, and hardware boundaries remain owned by active profile, security, artifact, and component contracts. This document defines the semantic controls that every implementation preserves.

## 2. Scope

This document applies globally to:

- user, service, node, build, recovery, and integration identities;
- passwords and password verifiers;
- private and symmetric keys;
- public keys and trust metadata;
- certificates and certificate chains;
- trust roots;
- revocation state;
- bearer, session, refresh, enrollment, delegation, and recovery tokens;
- API and integration credentials;
- artifact and Release Set signing authority;
- encryption and key-wrapping authority;
- backup and restore of protected key material;
- offline trust and revocation material;
- break-glass access;
- secret injection and runtime use;
- secret detection and incident response.

It applies across:

- development;
- test;
- staging;
- user endpoints;
- sovereign nodes;
- sovereign hubs;
- build workers;
- control infrastructure;
- offline and recovery environments.

Public keys, public certificates, and public trust statements are not secret material. They remain governed because they can define authority, identity, scope, validity, and revocation.

This document does not prescribe one secret-store product, hardware module, operating-system keyring, certificate protocol, password algorithm, transport protocol, or key-management service.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/components/identity-and-trust.component.json` | Identity, credential, certificate, trust-root, enrollment, delegation, and revocation authority |
| `contracts/components/governance-policy-runtime.component.json` | Authorization, emergency, exception, consent, disclosure, and recovery-policy decisions |
| `contracts/components/koa-node-agent.component.json` | Node identity reporting and declared privileged lifecycle operations |
| `contracts/components/audit-broker.component.json` | Critical-transition evidence routing and selective disclosure |
| `generated/component-catalog.json` | Component identity, ownership, and profile membership |
| `generated/profile-catalog.json` | Profile-specific trust, isolation, protected storage, offline, and recovery requirements |
| `contracts/artifact-classes.contract.json` | Signing, verification, publication, activation, rollback, and retention of artifacts |
| `contracts/release-channels.contract.json` | Release identity, signing authority, withdrawal, and compatibility |
| `contracts/integration-types.contract.json` | External credential scope, removability, and failure behavior |
| `contracts/system.contract.json#/security` | Global security and trust model |
| `generated/requirements-index.json` | Normative secrets-and-keys requirements |
| `generated/assertion-index.json` | Security, privilege, component, profile, lifecycle, release, and offline assertions |
| `generated/traceability.json` | Relationships among owners, keys, credentials, profiles, tests, and evidence |
| `generated/exception-index.json` | Bounded secret and key exceptions with compensating controls |
| `generated/test-catalog.json` | Exposure, isolation, rotation, revocation, recovery, and emergency tests |
| `generated/evidence-catalog.json` | Key and credential lifecycle evidence |

Related security documents are:

`text
07-security/00-threat-model.md
07-security/01-security-baseline.md
07-security/02-security-domains.md
07-security/03-identity-trust-and-signatures.md
07-security/04-trust-root-scoping.md
07-security/05-privilege-boundaries.md
07-security/06-privileged-broker.md
07-security/08-network-boundaries.md
07-security/09-storage-boundaries.md
07-security/10-data-at-rest.md
07-security/11-ai-boundaries.md
07-security/12-external-integration-classification.md
07-security/18-offline-import-security.md
07-security/19-software-supply-chain.md
07-security/20-break-glass-security.md
`

Development-specific secret handling is further described by:

`text
05-development/09-secrets-and-local-identities.md
`

## 4. Model and Responsibilities

### 4.1 Secret and key classes

| Class | Examples | Primary authority concern |
| --- | --- | --- |
| User authenticator | Password verifier, device credential, recovery factor | User identity and account recovery |
| Service identity | Service private key, service certificate, workload token | Component-to-component authentication |
| Node identity | Node enrollment key, node certificate | Node trust and profile membership |
| Session and delegation | Session token, delegated capability | Bounded acting authority |
| Transport protection | Endpoint certificate, channel credential | Authenticated confidential communication |
| Data encryption | Component data-encryption key | Confidentiality of owned state |
| Key wrapping | Protected wrapping or envelope key | Protection and rotation of data keys |
| Artifact signing | System, service, governance, or knowledge signing key | Artifact producer and release authority |
| Release authority | Release Set and channel publication key | Activation eligibility |
| Integration credential | Provider token, client credential | Scoped external capability |
| Recovery material | Recovery key, escrow share, offline factor | Controlled recovery |
| Emergency credential | Break-glass identity or factor | Time-bounded exceptional access |
| Trust root | Root certificate or public trust anchor | Verification authority |
| Revocation material | Revocation list, status artifact, withdrawn-key statement | Removal of authority |

### 4.2 Ownership

Identity and Trust owns identity and trust truth.

A component can own the operational use and rotation schedule of a component-scoped secret while Identity and Trust or another declared key authority owns issuance, identity binding, and revocation.

Release-channel owners own their signing-authority procedures.

A Build Farm can request or use bounded signing operations but does not automatically own release authority.

The privileged broker can use a secret handle for one declared host operation without disclosing the underlying key to the caller.

### 4.3 Purpose separation

Distinct purposes use distinct key or credential identities.

Purpose separation prevents one compromise from becoming universal authority.

The model separates at least:

- authentication from signing;
- transport from data encryption;
- data encryption from key wrapping;
- artifact signing from Release Set publication;
- component service identity from node administration;
- integration credentials from local service credentials;
- ordinary recovery from emergency access;
- development from production;
- online from offline recovery authority.

### 4.4 Environment separation

Each environment has distinct:

- identities;
- trust scope;
- service credentials;
- signing authority;
- integration accounts;
- recovery factors;
- revocation state;
- evidence.

A development credential cannot authenticate as a production component.

A production trust root cannot be copied into a developer workspace merely to simplify testing.

Test certificates and keys are visibly test-only and cannot validate production artifacts or targets.

### 4.5 Secret lifecycle

The lifecycle states are:

| State | Meaning |
| --- | --- |
| `planned` | Purpose and owner are approved but no material exists |
| `generated` | Material exists under controlled generation |
| `provisioned` | Material is delivered to its protected target |
| `active` | Material can exercise its declared authority |
| `rotating` | Old and new material coexist under a bounded transition |
| `suspended` | Use is temporarily blocked pending review |
| `revoked` | Authority is permanently removed |
| `expired` | Validity interval ended |
| `recovery_only` | Material is retained solely for declared recovery |
| `destroyed` | Supported use and supported recovery are removed |

A state change is explicit and attributable.

### 4.6 Handles and non-exportable use

Where supported, components receive a handle to a protected key rather than raw key material.

The protected service performs a declared operation such as:

- sign;
- decrypt;
- unwrap;
- derive a bounded session credential;
- attest identity.

A handle includes scope and does not become a general-purpose cryptographic interface.

### 4.7 Trust roots and certificates

Trust roots define who can establish identity or signing authority.

Trust-root scope identifies:

- environment;
- profile;
- organization or tenant;
- artifact class;
- release channel;
- component class;
- validity;
- revocation authority.

Adding a trust root is an authority change.

Removing or revoking a root propagates to active and recovery verification paths.

### 4.8 Passwords and user-entered secrets

User-entered secrets are verified without retaining recoverable plaintext.

Account recovery uses a declared recovery path rather than revealing the prior password.

Operational staff cannot retrieve user passwords.

Password resets invalidate affected sessions and record the transition.

### 4.9 Integration credentials

Each external integration has a distinct credential and declared:

- provider;
- account or tenant;
- destination;
- allowed capability;
- data class;
- environment;
- validity;
- rotation;
- revocation;
- local failure behavior.

Removing an integration credential disables only that integration.

### 4.10 Secret inventory

The canonical inventory records metadata, not secret values.

Inventory fields include:

- secret or key identifier;
- class;
- owner;
- purpose;
- environment;
- target;
- scope;
- status;
- issued time;
- validity;
- rotation schedule;
- revocation authority;
- recovery classification;
- dependent capabilities;
- evidence references.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-SECRET-001,REQ-SEC-SECRET-002,REQ-SEC-SECRET-003,REQ-SEC-SECRET-004,REQ-SEC-SECRET-005,REQ-SEC-SECRET-006,REQ-SEC-SECRET-007,REQ-SEC-SECRET-008,REQ-SEC-SECRET-009,REQ-SEC-SECRET-010,REQ-SEC-SECRET-011,REQ-SEC-SECRET-012,REQ-SEC-SECRET-013,REQ-SEC-SECRET-014,REQ-SEC-SECRET-015,REQ-SEC-SECRET-016,REQ-SEC-SECRET-017,REQ-SEC-SECRET-018,REQ-SEC-SECRET-019,REQ-SEC-SECRET-020,REQ-SEC-SECRET-021,REQ-SEC-SECRET-022,REQ-SEC-SECRET-023,REQ-SEC-SECRET-024,REQ-SEC-SECRET-025,REQ-SEC-SECRET-026,REQ-SEC-SECRET-027,REQ-SEC-SECRET-028,REQ-SEC-SECRET-029,REQ-SEC-SECRET-030,REQ-SEC-SECRET-031,REQ-SEC-SECRET-032 -->
- **REQ-SEC-SECRET-001 — SHALL:** Every secret, private key, credential, token, certificate, trust root, recovery factor, and signing authority have a declared owner, purpose, scope, classification, lifecycle state, permitted users, and revocation path.
- **REQ-SEC-SECRET-002 — SHALL:** Identity and Trust own cryptographic identity, credential, certificate, trust-root, delegation, enrollment, and revocation truth unless an active contract assigns a narrowly scoped signing or recovery authority to another declared owner.
- **REQ-SEC-SECRET-003 — SHALL:** Each component use a distinct service identity and only the secrets needed for its declared capabilities, target scope, environment, profile, and validity interval.
- **REQ-SEC-SECRET-004 — SHALL NOT:** Development, test, staging, user, sovereign, recovery, build, and production environments share mutable credentials, private keys, trust roots, recovery factors, or unrestricted integration tokens.
- **REQ-SEC-SECRET-005 — SHALL NOT:** Private keys, recovery secrets, passwords, bearer tokens, client secrets, session material, or unrestricted credentials appear in source control, active documentation, generated examples, ordinary artifacts, container images, system images, logs, traces, metrics, command history, issue text, or AI prompts.
- **REQ-SEC-SECRET-006 — SHALL:** Secret material at rest use a profile-approved protected store and encryption or protected hardware boundary appropriate to its classification and threat model.
- **REQ-SEC-SECRET-007 — SHALL:** Secret material in transit use authenticated, confidential, recipient-scoped delivery and verify both source authority and intended recipient before release.
- **REQ-SEC-SECRET-008 — SHALL:** Secret material be injected at runtime through a profile-approved mechanism and be absent from immutable application artifacts except for public trust material explicitly classified for distribution.
- **REQ-SEC-SECRET-009 — SHALL NOT:** Ordinary components receive a general secret-store credential, host root credential, shared administrator password, shared signing key, or a capability to enumerate secrets outside their declared scope.
- **REQ-SEC-SECRET-010 — SHALL:** Signing, authentication, transport, data-encryption, key-wrapping, recovery, artifact-publication, and integration credentials remain purpose-separated unless an accepted decision explicitly defines a narrower safe combination.
- **REQ-SEC-SECRET-011 — SHALL:** Secret and key generation use the active profile's approved cryptographic suite, entropy source, key size, identity binding, and generation authority, and record attributable generation evidence when required.
- **REQ-SEC-SECRET-012 — SHALL:** Passwords and equivalent user-entered secrets be represented by non-reversible verification material using the active security contract and never stored as recoverable plaintext.
- **REQ-SEC-SECRET-013 — SHALL:** Long-lived credentials be replaced by scoped short-lived credentials, delegated tokens, or handles where the component and profile contracts support them.
- **REQ-SEC-SECRET-014 — SHALL:** Every secret class define rotation triggers, maximum validity, overlap behavior, dependent-component update behavior, rollback constraints, and completion evidence.
- **REQ-SEC-SECRET-015 — SHALL:** Revocation propagate to every applicable verifier, offline trust store, active session, integration, artifact verifier, publication path, recovery environment, and retained rollback candidate.
- **REQ-SEC-SECRET-016 — SHALL NOT:** Rollback, restore, offline import, recovery, clock degradation, network loss, stale cache, or retained artifact presence reactivate a revoked, expired, withdrawn, superseded, or compromised credential or trust root.
- **REQ-SEC-SECRET-017 — SHALL:** A suspected or confirmed secret compromise trigger capability-scoped containment, credential suspension or revocation, dependent-session invalidation, impact analysis, rotation or replacement, evidence preservation, and post-event review.
- **REQ-SEC-SECRET-018 — SHALL:** When required trust, revocation, or secret state is unavailable, affected governed capabilities fail closed while explicitly safe inspection, export, recovery, and unaffected local capabilities remain available according to contract.
- **REQ-SEC-SECRET-019 — SHALL:** Offline profiles retain the local trust, revocation, certificate, credential, policy, time-confidence, and evidence inputs needed for their declared offline envelope.
- **REQ-SEC-SECRET-020 — SHALL NOT:** Offline operation select an undeclared credential provider, skip revocation checks, extend validity implicitly, broaden scope, or treat unavailable online verification as approval.
- **REQ-SEC-SECRET-021 — SHALL:** Backup and recovery material for keys and secrets be separately protected, encrypted, access-controlled, inventoried, tested, and unavailable to ordinary application identities.
- **REQ-SEC-SECRET-022 — SHALL:** Secret and key restoration validate target identity, owner, scope, version, revocation state, profile, Release Set compatibility, recovery authority, and required separation of duties before activation.
- **REQ-SEC-SECRET-023 — SHALL NOT:** Ordinary portability exports, component data exports, backups intended for user transfer, diagnostics packages, or credible-exit packages include private signing keys, private trust anchors, unrestricted credentials, or recovery secrets.
- **REQ-SEC-SECRET-024 — SHALL:** Break-glass and emergency credentials be separately owned, time-bounded, target-bounded, purpose-bounded, independently approved where required, automatically expired or revoked, and followed by credential rotation and review.
- **REQ-SEC-SECRET-025 — SHALL:** The privileged broker expose only declared operations and secret handles required for those operations and never provide ordinary callers with unrestricted secret or key access.
- **REQ-SEC-SECRET-026 — SHALL:** Logs, receipts, evidence, errors, support bundles, process listings, environment inspection, and observability outputs redact or omit secret material while retaining stable identifiers, reason codes, and lifecycle evidence.
- **REQ-SEC-SECRET-027 — SHALL NOT:** Native AI, external AI, voice services, creative services, notebooks, agents, workbenches, or automated support tools receive secret material or gain credential, signing, rotation, revocation, or recovery authority.
- **REQ-SEC-SECRET-028 — SHALL:** External integrations use distinct removable credentials with minimum capability, destination, tenant, audience, environment, and validity scope, and their removal disable only the dependent integration.
- **REQ-SEC-SECRET-029 — SHALL:** Source, build, artifact, image, configuration, log, fixture, example, migration, documentation, and deployment validation include automated secret detection and targeted negative tests.
- **REQ-SEC-SECRET-030 — SHALL:** Secret destruction remove active and staged copies, revoke derived access, invalidate dependent sessions, update inventory, preserve required evidence, and verify that no supported recovery path unintentionally restores the destroyed authority.
- **REQ-SEC-SECRET-031 — SHALL:** Critical generation, enrollment, issuance, delegation, rotation, revocation, recovery, emergency use, signing, trust-root change, and destruction transitions produce machine-readable receipts or evidence records.
- **REQ-SEC-SECRET-032 — SHALL:** Secrets-and-keys conformance pass only when ownership, separation, generation, storage, delivery, use, rotation, revocation, offline, recovery, emergency, integration, AI-boundary, destruction, receipt, and negative-exposure tests all pass.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Secret and Key Lifecycle Procedure

### 6.1 Define the authority object

Before material is generated, the owner records:

1. identifier;
2. secret or key class;
3. purpose;
4. owner;
5. environment;
6. profile;
7. subject and audience;
8. permitted operations;
9. classification;
10. validity interval;
11. rotation trigger;
12. revocation authority;
13. backup and recovery eligibility;
14. destruction behavior;
15. required evidence.

A request without a declared purpose or owner is rejected.

### 6.2 Generate

Generation occurs through a profile-approved cryptographic environment.

The generation process verifies:

- authorized generator;
- target identity;
- purpose;
- cryptographic suite;
- entropy source;
- protected-store destination;
- exportability policy;
- recovery policy;
- evidence path.

Private material is not printed or copied through general-purpose logs.

### 6.3 Provision

Provisioning delivers material only to the intended target.

The target verifies:

- source authority;
- target identity;
- recipient scope;
- environment;
- profile;
- expected secret identifier;
- validity;
- revocation state;
- protected destination.

Provisioning leaves no uncontrolled temporary copy.

### 6.4 Activate

Activation verifies dependent configuration and trust.

For service identity, the component confirms that it can authenticate only for the declared audience and operations.

For a signing key, the publication path confirms the signer's artifact class and release scope.

For a trust root, every affected verifier receives the update through a declared lifecycle transition.

### 6.5 Use

Secret use is mediated by the owning component or protected key service.

The caller provides:

- caller identity;
- requested operation;
- target or audience;
- correlation;
- authority or policy context when applicable.

The service checks scope before use.

Secret values do not appear in routine process arguments, crash output, telemetry, or support packages.

### 6.6 Rotate

Rotation creates new material and transitions dependents through a bounded overlap.

The rotation plan identifies:

- old and new identifiers;
- issuance;
- overlap interval;
- dependent components;
- offline targets;
- session handling;
- rollback limits;
- revocation timing;
- completion test;
- cleanup.

A rotation is incomplete while any required target still depends on undeclared old material.

### 6.7 Suspend and revoke

Suspension blocks use temporarily.

Revocation permanently removes authority.

The process:

1. records the initiating condition;
2. identifies affected identities, artifacts, sessions, integrations, and recovery paths;
3. publishes revocation through declared channels;
4. blocks new use;
5. invalidates dependent sessions;
6. selects replacement or restricted operation;
7. verifies propagation;
8. records evidence;
9. reviews impact.

### 6.8 Back up recovery-eligible material

Only declared recovery-eligible material enters protected backup.

The backup is:

- separately encrypted;
- separately inventoried;
- access-controlled;
- profile-scoped;
- tested on a clean recovery target;
- unavailable to ordinary component identities;
- retained for a declared interval.

Recovery copies are not ordinary portability exports.

### 6.9 Restore

Restore occurs in a controlled recovery environment.

The procedure validates:

- target identity;
- recovery authority;
- source ownership;
- source Release Set;
- secret status;
- revocation state;
- scope;
- profile compatibility;
- required approvals;
- evidence.

Restored material is staged before activation.

### 6.10 Destroy

Destruction covers:

- active protected-store entry;
- staged copies;
- temporary files;
- memory-backed staging where controllable;
- backups after retention ends;
- recovery copies;
- derived session authority;
- cached credentials;
- deployment copies.

The inventory enters `destroyed` only after verification.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Retained capability | Prohibited behavior | Evidence |
| --- | --- | --- | --- | --- |
| Owner or purpose is missing | Reject generation or use | Existing valid credentials | Creating an unowned secret | Inventory result |
| Secret appears in source or artifact | Block publication, rotate affected material, and investigate | Unaffected source and artifacts | Treating removal from the latest commit as complete containment | Exposure incident |
| Protected store is unavailable | Fail closed for affected secret use | Explicitly safe local and recovery functions | Loading a plaintext fallback file | Store-health result |
| Provisioning target identity fails | Reject delivery | Source protected material | Sending to a guessed recipient | Provisioning result |
| Credential is expired | Reject use and enter renewal or restricted path | Unaffected credentials | Extending validity locally | Expiry result |
| Revocation state is unavailable | Apply profile-declared closed or restricted behavior | Inspection, export, and recovery when permitted | Assuming non-revocation | Revocation-status result |
| Compromise is suspected | Suspend affected authority and contain dependents | Unaffected capabilities | Continuing normal use pending convenience | Incident record |
| Rotation partially completes | Keep transition visible and restrict unsupported targets | Targets on valid old or new state within declared overlap | Declaring completion | Rotation evidence |
| Old material remains after overlap | Revoke, isolate, and remediate | New valid authority | Extending overlap silently | Overlap failure |
| Offline target misses revocation update | Restrict affected verification or use retained safe authority | Unaffected offline capabilities | Accepting stale authority as current | Offline revocation state |
| Restore source contains revoked material | Keep restored material inactive | Other valid recovery material | Reactivating the revoked authority | Restore result |
| Recovery factors are unavailable | Enter declared restricted recovery or protected exit | Inspection and controlled export | Bypassing identity recovery | Recovery result |
| Integration credential fails | Disable only that integration | Local core operation | Reusing another integration's credential | Integration status |
| Privileged broker cannot use its handle | Stop the affected privileged operation | Nonprivileged operation | Exposing raw host credentials | Broker result |
| Evidence path is unavailable | Block critical key transition | Noncritical inspection | Unevidenced issuance, revocation, or recovery | Evidence state |
| Clock confidence is low | Apply profile-declared bounded review or restricted behavior | Existing validated local authority where allowed | Implicitly extending certificate or token validity | Clock result |
| Trust-root update is incompatible | Reject activation and retain prior valid trust set | Current valid trust | Partial verifier activation | Trust activation result |
| Destruction cannot be verified | Keep status non-destroyed and restrict use | Investigation | Claiming complete destruction | Destruction evidence |

Safe degradation never converts a missing secret into a shared credential, a revoked key into valid authority, an offline condition into approval, or an emergency identity into permanent access.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust owns:

- identity binding;
- enrollment;
- service and node credentials;
- certificate status;
- trust roots;
- delegation;
- session invalidation;
- revocation;
- recovery of identity authority.

Components retain only the references and handles required for their work.

### 8.2 Governance Policy Runtime

Governance Policy Runtime evaluates:

- credential issuance policy;
- delegation;
- emergency access;
- destructive rotation;
- trust-root change;
- sensitive export;
- recovery;
- exception use.

A policy decision does not reveal secret material or perform cryptographic operations.

### 8.3 Resource Governor

Resource Governor admits expensive generation, rotation, backup, restore, scanning, and verification jobs.

Resource capacity does not grant secret authority.

### 8.4 kOA Node Agent and privileged broker

Node Agent can report node identity and trust status.

The privileged broker performs narrowly declared host operations through protected handles.

Ordinary application components do not receive host administration keys.

### 8.5 Audit Broker

Audit Broker records critical lifecycle receipts and evidence.

Evidence uses identifiers and outcomes rather than raw secret values.

Selective disclosure exposes only what the verifier needs.

### 8.6 Component services

Each service:

- authenticates with its own identity;
- receives only scoped credentials;
- validates peer identity;
- reports credential-expiry and revocation state;
- supports rotation;
- removes temporary secret material;
- does not read another component's secret namespace.

### 8.7 Build Farm and release publication

Build workers use isolated build identities.

Artifact signing and release publication use distinct bounded authorities.

A build worker can submit material for signing without receiving the publication private key.

Release signing evidence remains attributable to the signing authority.

### 8.8 External integrations

Integration adapters receive provider-specific credentials through declared runtime injection.

The credentials are not copied into component data exports, user-visible configuration, AI prompts, or general logs.

### 8.9 Offline bundles

Offline bundles can carry public trust material, revocation updates, encrypted recipient-scoped secret material, and recovery instructions.

They do not embed unrestricted private signing keys.

Import remains separate from activation.

### 8.10 Recovery

Recovery environments receive only the recovery authority and material required for the selected path.

Temporary authority is removed after recovery.

Rollback candidates are checked against current revocation state.

### 8.11 AI systems and workbenches

AI and development workbenches can operate on redacted configuration templates and secret identifiers.

They do not receive real secret values or perform autonomous key lifecycle transitions.

## 9. Decision Closure and Prohibited Assumptions

This document is supported by the accepted decisions declared in its metadata.

A semantic change to secret or key authority requires:

1. an accepted owner decision;
2. impact analysis across Identity and Trust, profiles, components, artifacts, Release Sets, integrations, offline operation, recovery, privilege, tests, evidence, and operations;
3. canonical contract updates;
4. complete validation before activation.

The following assumptions are prohibited:

- a secret is safe because it is inside a private repository;
- a secret is safe because a repository commit was later deleted;
- environment variables are automatically confidential;
- a container image is an acceptable secret store;
- a system image can include production private keys;
- one service account can represent several components;
- root can access every component secret as an ordinary operating model;
- a database administrator owns every stored key;
- a hardware-backed key requires no rotation or revocation;
- a valid certificate proves current authorization;
- a valid signature proves the signer is still trusted;
- an expired credential can remain active while offline;
- a stale revocation cache implies non-revocation;
- rollback can restore revoked keys;
- restore can reactivate expired credentials;
- a backup proves secret recovery;
- a portability export should include signing keys for completeness;
- an integration token can be reused for another provider or environment;
- a development credential can be used temporarily in production;
- a Build Farm needs direct possession of release-publication keys;
- a privileged broker is a general password or key retrieval service;
- break-glass authority can remain active until the next maintenance window;
- log redaction after ingestion removes all prior exposure;
- an AI service can receive secrets because the user initiated the request;
- a secret scanner proves that no secret exists;
- public-key material is irrelevant to authority;
- source-code behavior can override the active credential contract;
- a recipe-selected key store becomes a global requirement.

No active exception currently weakens a requirement in this document.

## 10. Validation Criteria

This document is conformant when:

1. it is registered as `DOC-SEC-007`, active, English, and globally scoped;
2. every canonical reference resolves;
3. every declared decision is accepted;
4. every requirement is unique, active, and testable;
5. every lock exists and applicable assertions pass;
6. every secret and key class has an owner, purpose, scope, classification, lifecycle, and revocation path;
7. Identity and Trust ownership is consistent with component contracts;
8. every component and environment uses distinct identities and credentials;
9. private material is absent from source, documentation, examples, artifacts, images, logs, traces, and AI inputs;
10. protected storage and recipient-scoped delivery pass profile tests;
11. runtime injection leaves no uncontrolled temporary copy;
12. purpose separation is enforced for authentication, transport, encryption, wrapping, signing, publication, integration, and recovery;
13. generation and password-verifier tests use active security contracts;
14. rotation tests cover overlap, dependent updates, completion, and cleanup;
15. revocation reaches online, offline, recovery, rollback, integration, and session-verification paths;
16. rollback and restore cannot reactivate revoked or expired authority;
17. compromise tests contain affected capabilities and preserve evidence;
18. missing trust or revocation state produces closed or restricted behavior;
19. offline operation retains required local trust inputs without weaker validation;
20. recovery material is independently protected and tested;
21. ordinary exports exclude private signing and recovery authority;
22. break-glass use is bounded, reviewed, rotated, and evidenced;
23. privileged broker operations expose handles and declared operations only;
24. observability and support-package tests exclude secret values;
25. AI and workbench tests prove absence of credential authority and secret access;
26. external integration credentials are distinct, scoped, removable, and capability-limited;
27. automated detection runs across source, builds, artifacts, images, examples, migrations, logs, and deployment configuration;
28. destruction tests cover active, staged, temporary, backup, session, and recovery copies;
29. critical lifecycle transitions produce required receipts;
30. evidence is attributable, retained, minimized, and selectively disclosable;
31. no unresolved marker, undeclared owner, shared environment credential, or unrestricted secret path exists;
32. the active text contains the complete required section structure.

Applicable failure codes include:

`text
secret_owner_missing
secret_purpose_missing
shared_environment_credential
shared_component_identity
private_material_in_source
private_material_in_documentation
private_material_in_artifact
private_material_in_image
private_material_in_log
private_material_in_ai_input
secret_store_unprotected
secret_delivery_recipient_invalid
secret_runtime_injection_leak
credential_scope_excessive
key_purpose_collision
password_plaintext_retained
rotation_incomplete
revocation_not_propagated
revoked_key_reactivated
offline_revocation_state_stale
recovery_material_unprotected
secret_restore_validation_failed
private_key_in_portability_export
break_glass_expiry_failed
privileged_broker_secret_exposure
integration_credential_reuse
secret_destruction_unverified
secret_lifecycle_receipt_missing
`

A required validator that cannot run produces `blocked`, not `pass`.

## 11. Non-Normative Examples

### Example 1 — Service identity

Orgo and Konnaxion run on the same host.

Each service has a separate identity and certificate. Orgo cannot authenticate as Konnaxion, access Konnaxion credentials, or use Konnaxion's publication integration.

### Example 2 — Runtime injection

A service container starts without embedded credentials.

The profile-approved secret mechanism provides a short-lived scoped credential at runtime. The credential is not stored in the image, command line, source tree, or general environment dump.

### Example 3 — Artifact signing

Build Farm produces a services artifact.

The worker submits the validated artifact to a bounded signing operation. The signing authority verifies artifact class, producer evidence, and release scope, signs it, and returns a receipt. The worker never receives the signing private key.

### Example 4 — Rotation

A service certificate approaches expiry.

Identity and Trust issues a replacement, the service and peers accept both identities during a bounded overlap, the new identity becomes primary, the old certificate is revoked, sessions are refreshed, and completion evidence confirms that no required peer still depends on the old certificate.

### Example 5 — Offline revocation

A sovereign-offline node imports a verified revocation update.

The node removes trust in a withdrawn artifact-signing key before evaluating a retained rollback bundle. The old bundle remains stored for evidence but cannot activate.

### Example 6 — Integration token

A user enables an external creative service.

The adapter receives a provider-specific token scoped to the development or user environment and declared capability. Removing the integration revokes that token without affecting the local kOA Mediatheque, accepted offline learning material, Orgo, Ariane, or Kristal operation.

### Example 7 — Break-glass access

A node loses ordinary identity service during recovery.

Two authorized recovery roles activate a time-bounded emergency credential for one node and one recovery operation. Every use is recorded. After recovery, the credential is revoked, affected secrets are rotated, temporary authority is removed, and the event is reviewed.

### Example 8 — Credible exit

A user exports component-owned data for independent restoration.

The export includes stable identities, public verification material, rights, schemas, and restore instructions. It excludes release-signing keys, private trust anchors, service credentials, recovery factors, and integration tokens.
