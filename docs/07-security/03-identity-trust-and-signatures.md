<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-003",
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
    "contracts/system.contract.json#/identity_and_trust",
    "contracts/system.contract.json#/release_model",
    "generated/component-catalog.json#/components/identity_and_trust",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "contracts/artifact-classes.contract.json",
    "generated/artifact-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-DEV-001",
    "DEC-DEV-002"
  ],
  "requirement_ids": [
    "REQ-SEC-ID-001",
    "REQ-SEC-ID-002",
    "REQ-SEC-ID-003",
    "REQ-SEC-ID-004",
    "REQ-SEC-ID-005",
    "REQ-SEC-ID-006",
    "REQ-SEC-ID-007",
    "REQ-SEC-ID-008",
    "REQ-SEC-ID-009",
    "REQ-SEC-ID-010",
    "REQ-SEC-ID-011",
    "REQ-SEC-ID-012",
    "REQ-SEC-ID-013",
    "REQ-SEC-ID-014",
    "REQ-SEC-ID-015",
    "REQ-SEC-ID-016",
    "REQ-SEC-ID-017",
    "REQ-SEC-ID-018",
    "REQ-SEC-ID-019",
    "REQ-SEC-ID-020",
    "REQ-SEC-ID-021",
    "REQ-SEC-ID-022",
    "REQ-SEC-ID-023",
    "REQ-SEC-ID-024",
    "REQ-SEC-ID-025",
    "REQ-SEC-ID-026",
    "REQ-SEC-ID-027",
    "REQ-SEC-ID-028",
    "REQ-SEC-ID-029",
    "REQ-SEC-ID-030"
  ],
  "lock_ids": [
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-SEC-003",
    "LOCK-SEC-004",
    "LOCK-SEC-005",
    "LOCK-SEC-006",
    "LOCK-SEC-007",
    "LOCK-SEC-008",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CON-006",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-009",
    "DOC-SYS-014",
    "DOC-SYS-015",
    "DOC-SYS-017",
    "DOC-SYS-018",
    "DOC-SYS-019",
    "DOC-PRO-000",
    "DOC-LIFE-001",
    "DOC-LIFE-011"
  ],
  "tags": [
    "identity",
    "trust",
    "credentials",
    "signatures",
    "trust-roots",
    "revocation",
    "offline-trust",
    "key-lifecycle",
    "receipts",
    "verification"
  ]
}
KOA:DOC-META:END -->

# Identity, Trust, and Signatures

## 1. Purpose

This document defines the global security model for identity, trust, credentials, signatures, verification, revocation, and trust-state transitions in kOA.

The model ensures that a verified identity or signature has a precise and limited meaning.

It preserves the distinction between:

- identity and authorization;
- authentication and consent;
- credential possession and business authority;
- signature validity and artifact compatibility;
- signing and approval;
- approval and publication;
- publication and activation;
- trust evaluation and execution;
- public receipts and private proof;
- component identity and data ownership;
- recovery authority and ordinary operation.

Identity and Trust is the first-class component that verifies identity and trust claims and manages the trust material assigned to its contract.

It does not execute the consuming component's business operation, decide component data ownership, allocate resources, approve publication, or activate an artifact.

The consuming component remains responsible for the operation it performs. The Governance Policy Runtime remains responsible for applicable authorization, disclosure, consent, privilege, and governed-exception decisions.

This document does not select one universal certificate authority, credential format, signature algorithm, hardware module, key size, protocol, or trust-store implementation. Those implementation choices belong to active security contracts, profiles, artifact contracts, integration contracts, and compatibility records.

## 2. Scope

This document applies to identities and trust relationships used by:

- people;
- communities and collective authorities;
- operators and administrators;
- services;
- components;
- nodes and appliances;
- workspaces;
- development branches and worktrees;
- workers;
- jobs;
- process groups;
- integrations;
- publishers;
- release channels;
- artifact producers;
- signers;
- policy approvers;
- trust authorities;
- recovery and break-glass authorities.

It applies to:

- local authentication;
- mutual service authentication;
- component-to-component calls;
- signed commands;
- signed events and receipts;
- artifact signing;
- release signing;
- policy-bundle signing;
- offline bundles;
- trust updates;
- revocation;
- encryption-recipient identification;
- publication destinations;
- synchronization peers;
- backup and restore identities;
- build-farm workers;
- development workspace credentials;
- high-assurance and sovereign profiles;
- offline verification.

It covers the lifecycle of:

`text
identity record
credential request
credential issuance
credential activation
authentication
trust evaluation
signature generation
signature verification
rotation
suspension
revocation
expiry
replacement
recovery
destruction
evidence retention
`

It does not make an identity result sufficient for a policy-bound action.

It does not define ownership of the records operated on after verification.

It does not grant machine privilege.

## 3. Canonical References

| Canonical reference | Responsibility |
| --- | --- |
| `contracts/system.contract.json#/identity_and_trust` | Global identity, trust, credential, signature, and verification model. |
| `generated/component-catalog.json#/components/identity_and_trust` | Identity and Trust component identity, responsibility boundary, dependencies, and data ownership. |
| `contracts/components/identity-and-trust.component.json` | Identity, credential, trust, signature-verification, revocation, and trust-update interfaces. |
| `contracts/components/governance-policy-runtime.component.json` | Authorization, consent, disclosure, privilege, and governed-exception decisions. |
| `contracts/components/koa-node-agent.component.json` | Narrow node-local privileged execution for approved lifecycle and recovery operations. |
| `contracts/components/audit-broker.component.json` | Selective routing and preservation of declared identity and trust events. |
| `contracts/profiles/*.profile.json` | Profile-specific proofing, assurance, key custody, trust roots, offline behavior, time sources, recovery, and retention. |
| `contracts/artifact-classes.contract.json` | Artifact identity, signer scope, signatures, trust, revocation, downgrade, and activation requirements by artifact class. |
| `contracts/artifact-contracts/*.schema.json` | Signed object, receipt, trust-update, bundle, policy, provenance, and compatibility structures. |
| `contracts/integration-types.contract.json` | External identity providers, signing services, publication destinations, synchronization peers, and key-management integrations. |
| `generated/test-catalog.json` | Proofing, issuance, scope, signing, verification, replay, expiry, rotation, revocation, offline, recovery, and compromise tests. |
| `generated/evidence-catalog.json` | Identity, signature, trust, revocation, recovery, and conformance evidence. |
| `generated/requirements-index.json` | Normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Security, lifecycle, component, profile, data, and governance invariants. |
| `generated/traceability.json` | Links among decisions, identities, credentials, trust roots, requirements, tests, evidence, components, and profiles. |
| `generated/exception-index.json` | Approved bounded deviations and compensating controls. |

Exact key and algorithm requirements are owned by the applicable profile and security contract rather than by examples in this document.

## 4. Model and Responsibilities

### 4.1 Core terms

| Term | Meaning |
| --- | --- |
| Identity | A stable reference to a subject recognized within a declared scope. |
| Subject | The person, community, service, component, node, workspace, worker, job, integration, issuer, signer, publisher, or authority represented by an identity. |
| Credential | Evidence issued or accepted for proving an identity, attribute, key binding, role, scope, or assurance claim. |
| Authentication | Verification that a requester controls or presents the required credential material for the current relying context. |
| Trust | A bounded decision that an issuer, credential, key, signature, or claim is acceptable for a declared purpose and scope. |
| Trust root | A locally configured authority from which a specific trust evaluation begins. |
| Signature | A cryptographic statement binding a signer and protected context to an object representation. |
| Attestation | A signed claim about a system, build, process, measurement, or event. |
| Authorization | A decision that an identified actor can perform a requested action under the applicable policy. |
| Approval | A governed decision authorizing a lifecycle step such as signing, publication, activation, or exception use. |
| Receipt | An attributable record of a requested or completed transition and its result. |
| Revocation | A scoped declaration that a credential, key, signer, trust state, or authority is no longer acceptable from an effective point. |

A valid identity result can be an input to authorization.

It is not authorization by itself.

A valid signature proves only the class-specific statements bound by the signed representation and accepted trust scope.

### 4.2 Identity types

The identity model distinguishes at least:

| Identity type | Primary use |
| --- | --- |
| `human` | User, reviewer, operator, administrator, approver, or recovery actor. |
| `community_authority` | Collective or delegated cultural, civic, or governance authority. |
| `service` | One service instance or logical service identity. |
| `component` | One first-class component authority boundary. |
| `node` | One enrolled node, appliance, hub, or control-plane member. |
| `workspace` | One isolated development workspace. |
| `worker` | One build, processing, migration, backup, or task worker. |
| `job` | One admitted unit of bounded work. |
| `process_group` | One runtime group sharing an explicit isolation and resource context. |
| `integration` | One external service or adapter with a declared data-transfer and trust scope. |
| `issuer` | An authority permitted to issue a declared credential type. |
| `signer` | An authority permitted to sign a declared object class and scope. |
| `publisher` | An authority permitted to publish to a declared channel and destination. |
| `recovery_authority` | A separately controlled authority used for recovery or break-glass procedures. |

One physical machine, account, process, container, or operator can hold more than one identity only when the identities remain separately issued, scoped, used, logged, rotated, and revoked.

### 4.3 Identity record

An identity record normally contains:

- stable identity;
- identity type;
- display information;
- issuer or enrollment authority;
- relying scope;
- applicable profiles;
- owning component;
- subject attributes;
- credential bindings;
- assurance level;
- lifecycle status;
- activation time;
- expiry or review time;
- suspension and revocation state;
- delegation and recovery relationships;
- evidence references.

Identity records do not store unrestricted secret material.

Identity metadata does not become component business data merely because Identity and Trust verifies it.

### 4.4 Credential classes

Credential classes can include:

- user authentication credentials;
- service credentials;
- component credentials;
- node enrollment credentials;
- workspace credentials;
- worker and job credentials;
- mutual transport credentials;
- signing credentials;
- encryption-recipient credentials;
- publisher credentials;
- recovery credentials;
- short-lived delegated credentials;
- hardware-backed attestations;
- offline verification credentials.

Every credential class declares:

- issuer;
- subject types;
- key usage;
- relying purposes;
- scope;
- validity;
- proofing;
- activation;
- renewal;
- rotation;
- suspension;
- revocation;
- recovery;
- storage;
- exportability;
- evidence.

A credential accepted for transport authentication is not implicitly accepted for artifact signing.

A release signer is not implicitly a publisher.

A publisher is not implicitly an activation authority.

### 4.5 Trust-root hierarchy and scoping

Trust roots are scoped rather than universal.

Common trust domains include:

- human and community identity;
- node enrollment;
- service and component identity;
- development workspace identity;
- build worker and job identity;
- system-channel signing;
- services-channel signing;
- governance-channel signing;
- knowledge-channel signing;
- policy approval;
- offline bundle signing;
- trust and revocation updates;
- recovery;
- publication destinations;
- external integrations.

A trust path is evaluated against all applicable dimensions:

`text
issuer
credential or signer class
object type
artifact class
release channel
environment
profile
tenant or audience
target component
operation
validity
revocation
sequence or epoch
downgrade floor
required evidence
`

A root trusted for one domain does not acquire authority in another domain through technical reuse.

### 4.6 Root, intermediate, and leaf authorities

A profile can use root, intermediate, and leaf authorities.

The architecture expects:

- root authority to be highly protected and rarely used;
- online or delegated intermediates to be purpose- and environment-scoped;
- leaf credentials and signing identities to have the narrowest practical scope;
- recovery authority to remain separate from ordinary online authority;
- test and development trust to remain separate from production trust.

The exact hierarchy and custody mechanism are profile-specific.

A single-key design still has to express equivalent logical scopes and lifecycle controls if a profile permits it.

### 4.7 Key purposes

Keys are purpose-bound.

Examples include:

- authentication;
- transport protection;
- artifact signing;
- receipt signing;
- policy signing;
- trust-update signing;
- encryption;
- recovery;
- data-at-rest protection;
- attestation.

One key pair does not silently satisfy unrelated purposes.

A public verification key can be distributed more broadly than its corresponding private key while preserving scope metadata, revocation, and trust policy.

### 4.8 Key custody

Private-key custody can use:

- hardware-backed storage;
- operating-system protected storage;
- profile-approved secret stores;
- dedicated signing services;
- offline or disconnected custody;
- threshold or multi-party custody;
- short-lived process-bound material;
- other declared protected boundaries.

The custody boundary records:

- key identity;
- purpose;
- owner;
- profile;
- storage class;
- exportability;
- access roles;
- activation state;
- backup and recovery policy;
- rotation;
- destruction;
- evidence.

Build workers receive signatures and receipts from a signing boundary rather than release-signing private keys.

Ordinary application components receive only the credentials required by their contract.

### 4.9 Identity proofing and enrollment

Identity proofing establishes the subject and the authority permitted to enroll it.

Proofing can involve:

- existing trusted identity;
- in-person or community verification;
- node ownership;
- device attestation;
- component registry identity;
- workspace controller identity;
- build scheduler identity;
- organizational directory;
- delegated authority;
- recovery evidence.

Proofing strength is matched to the requested credential and action risk.

Enrollment records the relying purpose and requested scope rather than issuing a general credential.

### 4.10 Credential lifecycle

Credential lifecycle states can include:

`text
requested
proofed
approved
issued
staged
active
suspended
rotating
expired
revoked
destroyed
rejected
`

The credential contract owns the permitted transitions.

Suspension is reversible when the contract permits it.

Revocation is a trust-state transition with explicit effective scope and recovery behavior.

Expiry is not equivalent to revocation, but both make a credential unacceptable after their applicable boundary.

### 4.11 Authentication result

An authentication result records:

- subject identity;
- presented credential identity;
- issuer;
- relying service or component;
- relying operation;
- assurance;
- challenge or session context;
- issue time;
- expiry;
- revocation state;
- trust epoch;
- audience;
- result;
- reason;
- evidence.

A relying component validates that the result was issued for its operation and context.

A successful result from a different audience or operation is rejected.

### 4.12 Trust evaluation result

A trust result can be:

- trusted;
- trusted with freshness limitation;
- trusted with obligations;
- suspended;
- expired;
- revoked;
- wrong scope;
- incompatible;
- replayed;
- unknown;
- rejected.

The result identifies the scope and reason rather than returning an undifferentiated boolean.

`trusted with freshness limitation` does not remove profile-specific restrictions on high-impact operations.

### 4.13 Signed representation

A signed representation binds the signer to a deterministic or explicitly defined byte representation.

The contract defines:

- canonicalization;
- content type;
- object type;
- object identity;
- schema or contract version;
- protected headers or context;
- payload integrity;
- signature container;
- detached or embedded form;
- multiple-signature ordering;
- countersignature semantics;
- excluded mutable metadata.

Mutable publication, audience, activation, recognition, or workflow state is stored separately unless the signature contract intentionally signs that state as a new record.

### 4.14 Domain separation

Signature input includes a domain that prevents valid bytes from being reused as another command, receipt, artifact, policy, or trust update.

A conceptual signing context is:

`text
kOA domain
object type
contract version
purpose
scope
canonical object identity
payload integrity
anti-replay context
`

The exact encoding belongs to the signed-object contract.

### 4.15 Multiple signatures and quorum

Some objects can require:

- one signer;
- independent dual control;
- role-separated signatures;
- threshold signatures;
- quorum approval;
- creator and community approval;
- release and security approval;
- online signer plus offline countersignature.

The contract identifies whether order matters and whether signers can satisfy more than one required role.

A signature threshold does not replace governance requirements that exist outside the signed object.

### 4.16 Signature verification

Verification is class-aware.

Common checks include:

- bounded parsing;
- object schema;
- signed representation;
- object identity;
- signature integrity;
- signer identity;
- signer credential;
- trust chain;
- signer purpose and scope;
- key usage;
- algorithm policy;
- creation time;
- validity;
- audience or recipient;
- environment;
- profile;
- tenant;
- artifact class;
- release channel;
- target component;
- revocation;
- trust epoch;
- replay;
- downgrade;
- required co-signatures;
- evidence.

Signature validity remains separate from compatibility and authorization.

### 4.17 Artifact and release signatures

Software, policy, knowledge, bundle, migration, trust, and evidence artifacts use class-specific signer scopes.

The four release channels remain independent:

- `system`;
- `services`;
- `governance`;
- `knowledge`.

A signer authorized for one channel is not implicitly authorized for another.

A successful build does not compel signing.

A successful signature does not compel approval.

Approval does not compel publication.

Publication does not compel activation.

### 4.18 Signed commands and events

A signed command binds:

- command identity;
- issuer;
- actor;
- target;
- operation;
- parameters;
- expected state or version;
- purpose;
- audience;
- validity;
- replay context;
- correlation;
- payload integrity.

A signed event or receipt binds the event type and result that actually occurred.

A signature on a request does not prove that the requested transition completed.

### 4.19 Revocation

Revocation can apply to:

- a credential;
- a key;
- an issuer;
- a signer scope;
- a trust root;
- an intermediate authority;
- a node;
- a service identity;
- a publisher;
- an artifact signature;
- an integration;
- a recovery authority;
- a trust epoch.

Revocation records preserve:

- revoked identity;
- authority;
- reason;
- scope;
- effective time;
- effective sequence or epoch;
- replacement;
- affected classes or channels;
- emergency behavior;
- evidence.

Revocation state is itself protected against tampering, replay, and downgrade.

### 4.20 Offline trust

Offline nodes use locally available trusted state.

The applicable profile defines:

- trusted clock sources;
- clock confidence;
- maximum acceptable staleness by operation;
- local revocation material;
- trust epochs;
- cached identity-result reuse;
- emergency and recovery rules;
- synchronization and result export;
- high-impact operations blocked by stale state.

An offline node does not silently claim online freshness.

Local deterministic operation can continue where the relying contract permits it.

### 4.21 Trust updates

A trust update is a high-impact lifecycle artifact or transition.

It can add, remove, suspend, replace, or narrow:

- roots;
- intermediates;
- signer scopes;
- algorithms;
- key usage;
- revocation state;
- trust epochs;
- recipients;
- recovery authorities.

The update is verified under the current trusted state or a separately declared recovery path.

Activation preserves the previous known-good trust state or the recovery material required by the update contract.

### 4.22 Algorithm agility

Algorithm agility is controlled rather than automatic.

A security contract defines:

- accepted algorithms;
- parameters;
- object classes;
- key purposes;
- creation cutoff;
- verification horizon;
- migration;
- dual-signature intervals;
- downgrade floor;
- revocation;
- compatibility;
- evidence.

An implementation does not select a weaker or alternate algorithm because a preferred algorithm is unavailable.

### 4.23 Receipts and private proof

Identity and trust transitions produce receipts.

Public receipt content can include:

- receipt identity;
- transition type;
- subject or object reference;
- issuer or signer reference;
- bounded scope;
- result;
- reason codes;
- issue time;
- validity;
- correlation.

Private proof can include:

- proofing evidence;
- credential details;
- trust path;
- revocation evidence;
- device attestation;
- operator identity;
- approval evidence;
- diagnostic information;
- compromise evidence.

Private proof remains separately access-controlled and minimized.

### 4.24 Development identity isolation

Every development workspace has its own:

- workspace identity;
- service identities;
- database identities;
- secret namespace;
- trust context;
- test issuers or credentials where applicable;
- temporary credentials;
- local signing identities when permitted;
- revocation and cleanup records.

Parallel branches do not share mutable production-like credentials.

Read-only public trust material can be shared only through an explicit profile or workspace contract.

### 4.25 Recovery and break glass

Recovery identity remains outside ordinary authorization paths.

Recovery procedures identify:

- triggering condition;
- recovery authority;
- required approvals;
- time limit;
- target;
- minimum privilege;
- key or credential;
- network and physical conditions;
- affected trust scope;
- receipt;
- post-use revocation;
- review;
- evidence.

Recovery cannot become an undocumented permanent bypass.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-ID-001,REQ-SEC-ID-002,REQ-SEC-ID-003,REQ-SEC-ID-004,REQ-SEC-ID-005,REQ-SEC-ID-006,REQ-SEC-ID-007,REQ-SEC-ID-008,REQ-SEC-ID-009,REQ-SEC-ID-010,REQ-SEC-ID-011,REQ-SEC-ID-012,REQ-SEC-ID-013,REQ-SEC-ID-014,REQ-SEC-ID-015,REQ-SEC-ID-016,REQ-SEC-ID-017,REQ-SEC-ID-018,REQ-SEC-ID-019,REQ-SEC-ID-020,REQ-SEC-ID-021,REQ-SEC-ID-022,REQ-SEC-ID-023,REQ-SEC-ID-024,REQ-SEC-ID-025,REQ-SEC-ID-026,REQ-SEC-ID-027,REQ-SEC-ID-028,REQ-SEC-ID-029,REQ-SEC-ID-030 -->
- **REQ-SEC-ID-001 — SHALL:** Every security-relevant identity shall have one stable identifier, one declared identity type, one issuing authority, one scope, one lifecycle state, and one verification method.
- **REQ-SEC-ID-002 — SHALL:** Identity verification shall return a bounded result that identifies the subject, issuer, relying context, credential, trust scope, validity, revocation state, assurance, and evidence.
- **REQ-SEC-ID-003 — SHALL NOT:** Identity verification, authentication, credential possession, network reachability, or a valid signature shall be represented as business authorization, consent, disclosure approval, publication approval, release approval, or machine privilege.
- **REQ-SEC-ID-004 — SHALL:** The consuming component shall remain responsible for the operation it performs after receiving an identity or trust result.
- **REQ-SEC-ID-005 — SHALL:** Trust roots, intermediate authorities, issuing keys, signer identities, and verification keys shall be scoped by purpose, artifact class, release channel, environment, profile, tenant or audience, target component, operation, and validity as applicable.
- **REQ-SEC-ID-006 — SHALL NOT:** A cryptographically valid signature from a signer outside the required scope shall satisfy verification.
- **REQ-SEC-ID-007 — SHALL:** Every signed object shall bind its object type, canonical identity, version, purpose, issuer, audience or recipient scope, environment, creation time, validity rules, anti-replay context, and payload integrity as required by its artifact or interface contract.
- **REQ-SEC-ID-008 — SHALL:** Signature generation shall use a canonical representation or an explicitly declared signing representation that prevents ambiguity and cross-protocol substitution.
- **REQ-SEC-ID-009 — SHALL NOT:** Signing keys, private credential material, recovery secrets, bearer tokens, or equivalent secret material shall appear in source code, ordinary configuration, logs, receipts, build outputs, caches, unencrypted backups, or user-visible diagnostics.
- **REQ-SEC-ID-010 — SHALL:** Private signing and trust-root keys shall remain inside the profile-approved custody boundary and shall be accessed only through declared signing, issuance, rotation, revocation, or recovery interfaces.
- **REQ-SEC-ID-011 — SHALL NOT:** Build workers, application components, ordinary service processes, or user workspaces shall receive release-signing or trust-root private-key custody.
- **REQ-SEC-ID-012 — SHALL:** Credential issuance shall verify issuer authority, subject identity, requested scope, relying purpose, validity, key possession when applicable, and approval evidence before activation.
- **REQ-SEC-ID-013 — SHALL:** Credential rotation shall overlap old and new material only for a declared compatibility interval and shall preserve independent identifiers, activation times, revocation behavior, and evidence.
- **REQ-SEC-ID-014 — SHALL:** Revocation shall identify the revoked credential or trust state, issuer, scope, reason, effective sequence or epoch, effective time, replacement or recovery relationship, and evidence.
- **REQ-SEC-ID-015 — SHALL:** Trust and revocation updates shall be monotonic within their declared scope and shall include replay protection, downgrade protection, atomic activation, recovery behavior, and independent receipts.
- **REQ-SEC-ID-016 — SHALL NOT:** A trust update carried inside an unverified envelope shall bootstrap or validate the same envelope unless a separately trusted recovery contract explicitly authorizes that sequence.
- **REQ-SEC-ID-017 — SHALL:** Offline verification shall use the newest trusted local identity, trust, revocation, and time state available and shall expose freshness, staleness, and confidence in the verification result.
- **REQ-SEC-ID-018 — SHALL NOT:** Stale, missing, expired, revoked, suspended, unknown, or unverifiable trust state shall be silently treated as current or valid.
- **REQ-SEC-ID-019 — SHALL:** Cached identity and trust results shall be used only when their validity interval, revocation model, relying contract, profile policy, subject scope, and operation risk permit reuse.
- **REQ-SEC-ID-020 — SHALL:** Non-idempotent signed requests and high-impact trust transitions shall include nonce, sequence, transaction identity, challenge, or equivalent anti-replay controls appropriate to their contract.
- **REQ-SEC-ID-021 — SHALL:** Multi-party, quorum, dual-control, and countersignature requirements shall identify every required role, signer scope, signing order or independence rule, threshold, and failure result.
- **REQ-SEC-ID-022 — SHALL:** Signature verification shall remain separate from schema validation, artifact compatibility, governance approval, publication, staging, activation, and execution.
- **REQ-SEC-ID-023 — SHALL:** Every verification, issuance, rotation, suspension, revocation, signing, trust update, recovery, and key-destruction transition that affects authority shall produce an attributable receipt or evidence record.
- **REQ-SEC-ID-024 — SHALL:** Public receipts shall contain bounded identity and result information while private proof preserves sensitive identity, credential, authority, and diagnostic evidence under separate access controls.
- **REQ-SEC-ID-025 — SHALL:** Service, component, node, workspace, worker, job, integration, publisher, and operator identities shall remain distinct even when they execute in the same process, container, host, account, or physical device.
- **REQ-SEC-ID-026 — SHALL:** Development workspaces and parallel branches shall use separate mutable credentials, service identities, database identities, secret namespaces, and trust contexts except for explicitly approved read-only trust material.
- **REQ-SEC-ID-027 — SHALL:** Recovery and break-glass identities shall be separately scoped, time-bounded, strongly authenticated, independently approved where required, minimally privileged, fully receipted, and revoked or disabled after use.
- **REQ-SEC-ID-028 — SHALL:** Algorithm and key-format agility shall be implemented through versioned security contracts and compatibility rules without weakening existing trust scope, revocation, downgrade, or evidence requirements.
- **REQ-SEC-ID-029 — SHALL:** Suspected credential or signing-key compromise shall block affected issuance or signing, trigger incident handling, identify potentially affected objects and signatures, publish applicable revocation state, and preserve forensic evidence.
- **REQ-SEC-ID-030 — SHALL:** A complete identity, trust, and signature conformance claim shall include identity proofing, issuance, authentication, verification, scope, signing, replay, expiry, rotation, suspension, revocation, offline staleness, trust update, recovery, destruction, receipt, and negative-path tests with evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Enrolling an identity

Enrollment follows this order:

1. identify the requested subject and identity type;
2. identify the enrollment authority;
3. resolve the target profile and relying purpose;
4. verify proofing requirements;
5. verify subject control or delegation;
6. assign the stable identity;
7. create the identity record;
8. record assurance, scope, and review conditions;
9. produce enrollment evidence;
10. make the identity eligible for credential issuance.

Enrollment does not issue broader authority than the requested and approved scope.

### 6.2 Issuing a credential

Issuance:

1. receives the credential request;
2. validates subject identity and issuer authority;
3. validates requested purpose, audience, environment, profile, and validity;
4. verifies key possession or creates key material inside the approved custody boundary;
5. evaluates required approval;
6. assigns credential identity;
7. binds subject, issuer, scope, key usage, and validity;
8. signs or protects the credential;
9. records issuance evidence;
10. activates or stages the credential according to its contract.

A failed issuance leaves no active partial credential.

### 6.3 Authenticating a request

Authentication:

1. identifies the relying component and requested operation;
2. selects the accepted credential class;
3. receives the credential and proof;
4. validates bounded encoding and integrity;
5. verifies subject control;
6. verifies issuer and trust scope;
7. verifies audience, operation, environment, profile, and tenant;
8. verifies validity, suspension, revocation, epoch, and replay;
9. calculates assurance and freshness;
10. returns the bounded authentication result;
11. records evidence when required.

The relying component then performs its own authorization and state validation.

### 6.4 Signing an artifact or record

Signing:

1. receives an immutable candidate identity;
2. validates the object contract and signing representation;
3. validates producer, source, provenance, SBOM, tests, and evidence as applicable;
4. verifies signer scope and approval prerequisites;
5. verifies key state and custody;
6. constructs the protected signing context;
7. generates the signature inside the signing boundary;
8. verifies the produced signature;
9. returns the signature and signing receipt;
10. leaves approval, publication, and activation as separate transitions.

### 6.5 Verifying a signature

Verification:

1. identify the object type and contract;
2. parse the object and signature within declared limits;
3. reconstruct the protected signing representation;
4. verify object identity and payload integrity;
5. resolve signer identity and credential;
6. resolve the required trust domain;
7. verify signature integrity;
8. verify key purpose and signer scope;
9. verify audience, environment, profile, tenant, channel, class, and component;
10. verify validity, trusted time, revocation, epoch, replay, and downgrade;
11. verify required co-signatures;
12. return a bounded verification result;
13. continue with compatibility or policy evaluation only when applicable.

### 6.6 Rotating a credential or key

Rotation:

1. identify the current credential and replacement purpose;
2. create or enroll the replacement under the current policy;
3. verify compatibility and relying-party readiness;
4. activate the new credential;
5. retain the old credential for the declared overlap interval;
6. update trust distribution;
7. stop new use of the old credential;
8. revoke or expire the old credential;
9. verify all relying parties use the replacement;
10. destroy obsolete private material according to custody policy;
11. record rotation evidence.

### 6.7 Suspending and reinstating a credential

Suspension:

1. identify the credential and reason;
2. verify suspension authority;
3. publish or distribute suspension state;
4. block new trust results;
5. preserve evidence;
6. investigate or wait for the declared condition.

Reinstatement:

1. verifies that the suspension condition is resolved;
2. verifies credential validity and key custody;
3. verifies that revocation did not supersede suspension;
4. records approval;
5. activates the credential;
6. publishes the new state;
7. records evidence.

### 6.8 Revoking a credential or signer

Revocation:

1. identify the credential, key, signer, issuer, or scope;
2. verify revocation authority;
3. assign effective time and monotonic sequence or epoch;
4. identify affected objects, classes, channels, recipients, and relying parties;
5. create the protected revocation record;
6. distribute the revocation;
7. block new verification results;
8. evaluate active sessions or deployments;
9. initiate replacement, isolation, rollback, or recovery;
10. record incident and revocation evidence.

### 6.9 Applying a trust update

Trust update:

1. isolate the candidate update;
2. validate its contract and integrity;
3. verify current trusted signer authority;
4. verify sequence, epoch, scope, replay, validity, and downgrade;
5. verify required approvals or quorum;
6. test representative accepted and rejected paths;
7. stage the new trust state;
8. switch atomically or through an equivalent no-partial-state transition;
9. revalidate critical identities and signers;
10. commit the new epoch or invoke recovery;
11. retain the previous state or recovery material;
12. produce the update receipt.

### 6.10 Verifying while offline

Offline verification:

1. identify the required operation and risk class;
2. load the newest trusted local roots, intermediates, revocation state, trust epoch, and clock evidence;
3. calculate freshness and confidence;
4. verify identity, signature, scope, validity, replay, and downgrade;
5. compare staleness with the profile and relying contract;
6. return trusted, limited, blocked, or rejected status;
7. expose freshness in the result;
8. queue or export required receipts when connectivity is absent.

### 6.11 Recovering trust

Trust recovery:

1. enter the declared recovery state;
2. isolate ordinary signing and issuance;
3. verify recovery authority and approvals;
4. verify recovery media or material;
5. identify the last known-good trust state;
6. apply revocation or replacement;
7. re-enroll affected nodes, services, or signers as required;
8. verify representative trust paths;
9. exit recovery only after validation;
10. disable or revoke recovery credentials;
11. record complete recovery evidence.

### 6.12 Destroying key material

Destruction:

1. identify the key and all active bindings;
2. verify that replacement, revocation, retention, and recovery conditions are satisfied;
3. stop new use;
4. revoke or retire the binding;
5. destroy private material through the custody mechanism;
6. verify destruction when the mechanism supports it;
7. retain public verification and historical evidence for the required period;
8. record destruction evidence.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior |
| --- | --- |
| Identity service is unavailable | New identity-bound operations stop unless a still-valid cached result is explicitly permitted by profile and relying contract. |
| Credential is missing | The operation requiring that credential is blocked. |
| Credential is malformed | Parsing stops and no subject claim is trusted. |
| Credential is expired | New authentication and verification fail for that credential. |
| Credential is suspended | New trust results remain blocked until valid reinstatement. |
| Credential or key is revoked | New trust results fail and affected active use follows the revocation contract. |
| Trust root is unavailable | Operations requiring that root remain blocked; an unrelated trust domain can continue independently. |
| Trust path is incomplete | Verification returns a bounded failure rather than trying an undeclared issuer. |
| Signature is invalid | The signed object is rejected for the requested transition. |
| Signature is valid but scope is wrong | Verification fails for the requested purpose. |
| Signature algorithm is unsupported | Verification is blocked; a silent algorithm substitution is not selected. |
| Required co-signature is missing | The object remains incomplete for the governed transition. |
| Trusted time is uncertain | Freshness and confidence are exposed; risk-sensitive operations can remain blocked. |
| Revocation state is stale | The stale state is disclosed and profile-specific operation restrictions apply. |
| Replay is detected | The prior idempotent result is returned or the request is rejected; non-idempotent effects are not repeated. |
| Lower trust epoch or downgrade is detected | The update or object is rejected unless a declared recovery procedure permits it. |
| Signing service is unavailable | Unsigned candidates remain candidates; signing, publication, or activation is not inferred. |
| Private-key compromise is suspected | Affected signing and issuance stop, incident handling begins, and applicable revocation is prepared. |
| Key custody backend fails | New key use stops or remains within the last verified safe state according to profile policy. |
| Identity result is for another audience | The relying component rejects it. |
| Governance Policy Runtime is unavailable | Identity verification can continue, but policy-bound operations requiring a new decision remain blocked. |
| Audit or receipt storage is unavailable | Evidence-required trust transitions remain blocked or uncommitted. |
| Offline synchronization fails | Local trust state remains unchanged and results remain queued for later exchange. |
| Trust update activation fails | The previous known-good state remains active or the recovery procedure begins. |
| Recovery credential is lost | Ordinary operation does not inherit recovery authority; the higher-order recovery procedure is used. |
| Destruction cannot be verified | The key remains treated as potentially present and its credential remains revoked or blocked. |

Safe degradation does not convert identity into authorization or signature validity into compatibility.

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust owns identity verification, credential and trust evaluation, scoped trust roots, revocation state, and the interfaces assigned by its component contract.

It returns bounded results.

It does not execute the caller's business mutation.

### 8.2 Governance Policy Runtime

The Governance Policy Runtime consumes verified identity and trust context to evaluate authorization, disclosure, consent, privilege, and governed exceptions when required.

It does not issue arbitrary credentials or hold release-signing key custody merely because it evaluates approval.

### 8.3 Resource Governor

The Resource Governor can limit identity, signing, verification, rotation, or revocation workloads.

It does not change trust semantics or grant authority when capacity is available.

### 8.4 kOA Node Agent

The Node Agent can execute bounded node-local enrollment, credential installation, trust-store activation, key rotation, recovery, and destruction operations through its privilege contract.

It does not decide signer scope or policy approval.

### 8.5 Audit Broker

Identity and trust components emit declared events and receipts.

The Audit Broker preserves selective accountability without collecting unrestricted credential or private-key material.

### 8.6 Build farm and signing service

The build farm produces verified candidates and requests signatures.

The signing service validates signer scope and returns signatures and receipts.

Workers do not receive private signing keys.

### 8.7 Release channels

System, services, governance, and knowledge signers remain independently scoped.

A publication adapter has destination-scoped credentials and cannot sign a different channel merely because it can upload there.

### 8.8 Artifact lifecycle

Artifact verification consumes identity and trust results.

Compatibility, policy approval, staging, activation, rollback, and recovery remain separate lifecycle transitions.

### 8.9 Publication Gateway

The Publication Gateway verifies source, requester, audience, purpose, consent, policy, and destination identity for cross-domain publication.

A valid requester signature does not bypass disclosure controls.

### 8.10 Component owners

A component receives identity and trust results for its own commands and data.

Identity and Trust does not write the component's authoritative records.

### 8.11 Development workspaces

The workspace controller creates isolated workspace and service identities.

Production roots and credentials are not copied into ordinary development workspaces.

### 8.12 Offline importer

The offline importer verifies bundle and payload signer identities against locally trusted scoped state.

Trust updates use a separate high-impact transition and do not silently validate their own envelope.

### 8.13 External integrations

External identity providers, signing systems, key stores, directories, and publication services are classified integrations.

Their credentials, data transfers, availability, failure behavior, and trust scope are explicit.

## 9. Decision Closure and Prohibited Assumptions

### 9.1 Accepted decisions

| Decision | Effect |
| --- | --- |
| `DEC-COMP-001` | Keeps Identity and Trust as one first-class component with a bounded responsibility rather than a universal execution engine. |
| `DEC-DATA-001` | Keeps component data ownership separate from identity and trust verification. |
| `DEC-GOV-001` | Keeps resource enforcement separate from authorization, consent, disclosure, and privilege decisions. |
| `DEC-REL-001` | Keeps signers and release authority independent across the four release channels. |
| `DEC-PROFILE-BASELINE-001` | Keeps proofing, custody, offline, assurance, recovery, and trust-topology choices profile-scoped. |
| `DEC-DEV-001` | Requires isolated identity, secret, service, database, and resource contexts per development workspace. |
| `DEC-DEV-002` | Requires parallel branches and applications to avoid mutable identity and credential collisions. |

### 9.2 Related ADRs

| ADR | Relevance |
| --- | --- |
| `ADR-012` | Keeps privileged host execution inside one narrow broker boundary. |
| `ADR-015` | Requires isolated development workspaces and credentials. |
| `ADR-019` | Separates Resource Governor and Governance Policy Runtime authority. |

### 9.3 Prohibited assumptions

The following assumptions are prohibited:

- a username is a verified identity;
- possession of a credential proves authorization;
- network location proves identity;
- process UID proves component authority;
- a container identity is automatically a service identity;
- a valid TLS session proves permission for a business action;
- a valid signature proves artifact compatibility;
- a valid signature proves approval;
- a signature proves publication;
- publication proves activation;
- one trust root is valid for every purpose;
- one release-channel signer can sign every channel;
- one key can serve authentication, signing, encryption, and recovery without explicit authority;
- an online signer can act as a recovery root by convenience;
- a build worker can hold release-signing keys;
- a publisher can approve its own release by uploading it;
- stale revocation state is current;
- absence from a local revocation list proves global validity;
- a trust update can validate itself;
- an expired credential becomes valid when offline;
- an unsupported algorithm can be replaced silently;
- a replayed signed request can repeat a migration or trust update;
- a cached authentication result is valid for a different audience or operation;
- an Identity and Trust result changes component data ownership;
- a recovery credential is ordinary administrative access;
- private proof can be copied into public receipts;
- deleting a credential file proves key destruction;
- test and production trust domains can share mutable issuers;
- implementation prevalence creates canonical trust authority.

## 10. Validation Criteria

This document conforms when all of the following checks pass:

1. metadata status is `active`;
2. the registered path is `07-security/03-identity-trust-and-signatures.md`;
3. all canonical references resolve;
4. all listed decisions are accepted;
5. all requirements match the requirements registry;
6. all locks resolve and pass;
7. every identity identifier is unique within its authority domain;
8. every identity declares type, issuer, scope, lifecycle, and verification method;
9. every credential declares issuer, subject, purpose, key usage, validity, scope, rotation, revocation, recovery, and evidence;
10. every trust root has an explicit purpose and scope;
11. every signer scope is class-, channel-, environment-, profile-, audience-, and component-aware where applicable;
12. private keys remain inside approved custody;
13. workers and ordinary components lack release-signing key custody;
14. signing input uses the declared representation and domain separation;
15. signed-object identity and payload integrity match;
16. signature verification rejects wrong-purpose keys;
17. signature verification rejects wrong-audience and wrong-environment credentials;
18. signature verification rejects wrong artifact class or release channel;
19. multi-signature and quorum rules are complete;
20. schema, signature, compatibility, policy, publication, staging, and activation results remain separate;
21. credential issuance tests cover proofing and key possession;
22. authentication tests cover relying context and audience;
23. replay tests cover signed requests, receipts, trust updates, and migrations;
24. expiry and suspension tests block new trust results;
25. revocation tests cover credentials, issuers, signers, scopes, roots, nodes, and integrations;
26. rotation tests cover overlap, replacement, revocation, and relying-party transition;
27. offline tests cover trusted time, confidence, staleness, epochs, and high-impact blocking;
28. trust-update tests cover monotonic sequence, downgrade, atomic activation, rollback, and recovery;
29. key-compromise tests block signing and identify affected signatures;
30. recovery tests cover separate authority, approvals, time bounds, minimum privilege, post-use revocation, and evidence;
31. destruction tests preserve public verification evidence while removing private material;
32. workspace tests prove separate mutable identity and credential contexts;
33. component tests prove Identity and Trust does not execute business mutations;
34. governance tests prove identity does not substitute for policy;
35. resource tests prove capacity does not affect trust semantics;
36. receipts separate public content from private proof;
37. logs and diagnostics contain no secret material;
38. degraded identity or trust state is reported accurately;
39. complete requirement-to-test-to-evidence traceability exists;
40. active content is English;
41. placeholder and open-authority markers are absent.

The validator reports focused failures, including:

`text
identity_identifier_collision
identity_type_missing
identity_issuer_missing
identity_scope_missing
credential_purpose_missing
credential_key_usage_missing
credential_validity_invalid
credential_scope_invalid
trust_root_scope_missing
trust_path_incomplete
signer_scope_invalid
signature_representation_ambiguous
signature_domain_separation_missing
signature_integrity_failed
signature_wrong_audience
signature_wrong_environment
signature_wrong_profile
signature_wrong_channel
signature_wrong_artifact_class
signature_required_cosigner_missing
signature_replay_detected
credential_expired
credential_suspended
credential_revoked
revocation_state_stale
trust_epoch_downgrade
trust_update_self_bootstrap
trust_update_partial_activation
signing_key_custody_violation
private_material_in_receipt
workspace_identity_collision
identity_used_as_authorization
signature_used_as_approval
signature_used_as_activation
recovery_authority_not_isolated
key_destruction_unverified
`

## 11. Non-Normative Examples

### 11.1 Service authentication

Konnaxion calls Identity and Trust with its service identity and the relying context for a participant verification request.

Identity and Trust returns the subject, credential, issuer, assurance, audience, validity, revocation state, and result. Konnaxion then applies its own command and policy rules.

### 11.2 Wrong signer scope

A valid services-channel signer signs a governance policy bundle.

The signature cryptographically verifies, but the signer lacks governance-channel and policy-bundle scope. The bundle is rejected.

### 11.3 Build signing

A clean build worker produces a service artifact and provenance.

The worker submits the immutable artifact identity and evidence to the signing service. The signing service returns a services-channel signature and receipt. The worker never receives the signing private key.

### 11.4 Publication separation

A knowledge artifact has a valid signature and approved compatibility.

The Publication Gateway or release publisher still requires separate publication authorization. A successful upload creates a publication receipt but does not activate the artifact on any runtime.

### 11.5 Offline stale revocation

A sovereign node has trusted revocation state that is older than the high-impact threshold.

The node reports the staleness. Low-risk previously authorized local reads can continue when their contracts permit them. A trust-root update and system-image activation remain blocked.

### 11.6 Credential rotation

A service receives a replacement credential.

Both old and new credentials are accepted during a declared short overlap. The service migrates to the new credential, the old credential is revoked, and verification confirms that no active peer still depends on it.

### 11.7 Replayed signed migration

A signed migration command completed before a result was returned.

The retried command carries the same transaction identity and sequence. The component returns the recorded result and does not execute the migration again.

### 11.8 Quorum trust update

A trust-root change requires independent security and recovery-authority signatures.

Both signatures bind the same update identity and epoch. The node stages the update, switches trust state atomically, verifies representative paths, and retains recovery material.

### 11.9 Parallel workspaces

Two Konnaxion branches run simultaneously.

Each has a separate workspace identity, service credential, database identity, secret namespace, and test trust context. They can share a read-only public test root only when the workspace contract declares it.

### 11.10 Recovery credential

A node loses its ordinary trust state.

A separately stored recovery credential is activated through dual control for one recovery operation. The node restores a known-good trust state, records the receipt, and disables the recovery credential after validation.
