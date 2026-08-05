<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SEC-004",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "security",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/profiles/developer-linux-workstation.profile.json",
    "contracts/profiles/developer-windows-wsl.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/resource-governor.component.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-DEV-001",
    "DEC-REL-001",
    "DEC-DATA-001",
    "DEC-GATE-001"
  ],
  "requirement_ids": [
    "REQ-SEC-TRUST-001",
    "REQ-SEC-TRUST-002",
    "REQ-SEC-TRUST-003",
    "REQ-SEC-TRUST-004",
    "REQ-SEC-TRUST-005",
    "REQ-SEC-TRUST-006",
    "REQ-SEC-TRUST-007",
    "REQ-SEC-TRUST-008",
    "REQ-SEC-TRUST-009",
    "REQ-SEC-TRUST-010",
    "REQ-SEC-TRUST-011",
    "REQ-SEC-TRUST-012",
    "REQ-SEC-TRUST-013",
    "REQ-SEC-TRUST-014",
    "REQ-SEC-TRUST-015",
    "REQ-SEC-TRUST-016",
    "REQ-SEC-TRUST-017",
    "REQ-SEC-TRUST-018",
    "REQ-SEC-TRUST-019",
    "REQ-SEC-TRUST-020",
    "REQ-SEC-TRUST-021",
    "REQ-SEC-TRUST-022",
    "REQ-SEC-TRUST-023",
    "REQ-SEC-TRUST-024",
    "REQ-SEC-TRUST-025",
    "REQ-SEC-TRUST-026",
    "REQ-SEC-TRUST-027",
    "REQ-SEC-TRUST-028",
    "REQ-SEC-TRUST-029",
    "REQ-SEC-TRUST-030"
  ],
  "lock_ids": [
    "LOCK-DOC-002",
    "LOCK-DATA-001",
    "LOCK-GATE-001",
    "LOCK-PROFILE-001",
    "LOCK-DEV-003",
    "LOCK-DEV-004",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-IMPL-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-CONST-007",
    "DOC-CONST-008",
    "DOC-SYS-002",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-006",
    "DOC-SYS-007",
    "DOC-SYS-014",
    "DOC-SYS-017",
    "DOC-SYS-019",
    "DOC-SYS-020",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-COMP-000",
    "DOC-DEV-009",
    "DOC-LIFE-002",
    "DOC-LIFE-012",
    "DOC-SEC-000",
    "DOC-SEC-001",
    "DOC-SEC-002",
    "DOC-SEC-003"
  ],
  "tags": [
    "security",
    "trust-roots",
    "trust-domains",
    "signatures",
    "identity",
    "release-trust",
    "revocation",
    "rotation",
    "offline-verification",
    "profile-scoping"
  ]
}
KOA:DOC-META:END -->

# Trust Root Scoping

## 1. Purpose

This document defines how trust roots are scoped throughout the kOA operating environment.

A trust root is an explicitly registered anchor used to validate a bounded class of identity, credential, signature, artifact, policy, publication, evidence, transport, or integration claims. Possession of a valid chain to a root is not a general authorization. Trust remains limited to the purpose, subjects, operations, targets, profiles, environments, channels, artifact classes, audiences, and time intervals declared by the root's active contract.

The model prevents development trust, public web trust, release trust, governance trust, publication trust, user identity, service identity, and evidence trust from collapsing into one undifferentiated authority.

## 2. Scope

This document applies to:

- root certificates, raw public-key anchors, pinned keys, trust manifests, and equivalent registered anchors;
- intermediate authorities, delegated signers, leaf credentials, certificate chains, and trust paths;
- user and service identity verification;
- local transport and mutual-authentication trust;
- system, services, governance, and knowledge release-channel artifacts;
- artifact signatures, Release Sets, offline bundles, provenance, and verification receipts;
- governance-policy bundles and governed decisions;
- Publication Gateway approvals and publication receipts;
- evidence, selective audit, and decision receipts;
- development workspaces and generated local certificate authorities;
- sovereign, high-assurance, offline, endpoint, hub, build-farm, and control-plane deployments;
- root provisioning, activation, delegation, rotation, overlap, revocation, compromise response, replacement, retirement, backup, recovery, and validation;
- cross-signing, bridge trust, external integrations, and imported trust material.

This document does not:

- prescribe one public-key infrastructure, cryptographic algorithm, hardware module, operating-system trust store, certificate format, key-management product, or online validation protocol globally;
- define component data ownership, application authorization, resource admission, host privilege, release-channel membership, or publication acceptance;
- make every profile use the same trust roots or assurance controls;
- permit private keys or secret material in documentation;
- replace artifact, profile, component, identity, governance, publication, or evidence contracts.

## 3. Canonical References

| Canonical reference | Ownership role |
| --- | --- |
| `contracts/components/identity-and-trust.component.json` | Owns identity, credential, signature, chain, root, validity, and revocation verification interfaces. |
| `contracts/profiles/*.profile.json` | Owns profile-specific trust controls, assurance levels, hardware custody, offline behavior, and evidence requirements. |
| `contracts/release-channels.contract.json` | Owns release-channel identities and membership; a trust root cannot redefine them. |
| `contracts/artifact-classes.contract.json` and artifact contracts | Own artifact-class identities, signature claims, integrity scopes, and class-specific verification rules. |
| `contracts/components/governance-policy-runtime.component.json` | Owns policy authorization and governed exceptions; signature trust does not replace policy evaluation. |
| `contracts/components/publication-gateway.component.json` | Owns cross-domain publication control; a valid signer cannot bypass the gateway. |
| `contracts/components/resource-governor.component.json` | Owns resource admission for verification and signing work. |
| `contracts/artifact-contracts/decision-receipt.schema.json` | Defines machine-readable decision and trust-related receipt evidence. |
| `contracts/artifact-contracts/offline-bundle.schema.json` | Owns offline-bundle structure and declared trust material relationships. |
| `contracts/artifact-contracts/release-set.schema.json` | Owns Release Set structure and compatibility evidence. |
| `generated/requirements-index.json` | Owns the normative statements displayed in Section 5. |
| `generated/assertion-index.json` | Owns canonical ownership, component separation, profile scope, development isolation, and lifecycle alignment assertions. |
| `generated/traceability.json` | Owns decision, requirement, lock, profile, component, test, and evidence relationships. |
| `generated/test-catalog.json` and `generated/evidence-catalog.json` | Own trust-root conformance test and evidence identities. |

This Markdown document explains trust-root scoping. Exact root identities, public material, scopes, lifecycle states, and trust-store versions remain machine-readable canonical data.

## 4. Model and Responsibilities

### 4.1 Trust-root identity

Every root has one stable identity independent from:

- its file name;
- its certificate-store alias;
- its host path;
- its hardware slot;
- its cloud-provider identifier;
- its current public-key encoding;
- its physical custodian;
- the machine where verification occurs.

A rotated successor receives a new root identity and links to its predecessor. A retired or revoked identifier remains reserved.

### 4.2 Scope dimensions

A root scope can constrain:

- trust purpose;
- subject type and subject namespace;
- credential or signature type;
- permitted operations;
- components and integrations;
- artifact classes;
- release channels;
- profiles and overlays;
- environment or deployment class;
- tenant, node, workspace, or trust domain;
- destination or audience;
- validity interval;
- algorithm or assurance policy;
- issuance and delegation depth;
- required verification and evidence.

A verifier evaluates all applicable dimensions. Omitted dimensions do not silently become global authority.

### 4.3 Explanatory trust domains

The following categories explain common trust boundaries. They are not a competing canonical enum.

| Trust domain | Typical claims | Boundary |
| --- | --- | --- |
| Development-local | Local service identities, local transport, disposable tests | One workspace or explicit shared development domain |
| User identity | Human account and session identity | Declared user and tenant scopes |
| Service identity | Component and service instance identity | Declared component, service, environment, and operation scopes |
| Artifact and release | Artifact provenance and release signatures | Declared artifact classes, channels, profiles, producers, and transitions |
| Governance | Policy-bundle and governed-decision authenticity | Governance Policy Runtime scope |
| Publication | Approval and cross-domain publication evidence | Publication Gateway scope |
| Evidence | Receipts and audit evidence | Declared evidence authority and disclosure scope |
| External integration | External provider or partner claims | One registered integration and transfer boundary |
| Bootstrap and recovery | Initial trust-store or recovery-state authenticity | Declared bootstrap or recovery procedure |

A root can cover more than one category only when the overlap is explicit, justified, testable, and compatible with the effective profile.

### 4.4 Trust path

A trust path contains:

1. one active root;
2. zero or more intermediates or delegated authorities;
3. one subject credential or signer;
4. declared constraints at every level;
5. the target verification context;
6. current validity and revocation information;
7. a final trust outcome.

Every child authority remains within the intersection of all parent constraints. A cryptographically valid path with a scope mismatch is not an authorized path.

### 4.5 Trust store

A trust store is a versioned set of root identities and public verification material for one declared trust context.

It records:

- trust-store identity and version;
- owning authority;
- applicable profiles and environments;
- included root identities;
- permitted purposes and exclusions;
- activation and recovery behavior;
- provenance;
- validation and evidence;
- predecessor and successor relationships.

A trust store can reference roots without owning their underlying authority or private key custody.

### 4.6 Private-key custody

Private root capability remains outside ordinary verifier distribution.

The active profile and trust contract define:

- custodian roles;
- issuance access;
- signing access;
- recovery access;
- backup and restore;
- hardware or offline custody when required;
- threshold or multi-party approval;
- audit and evidence;
- compromise and destruction procedures.

Public trust material and private authority material remain distinguishable.

### 4.7 Release and artifact trust

Release trust is evaluated in addition to artifact identity, class, channel, integrity, provenance, compatibility, profile applicability, policy, and lifecycle state.

A trusted signature answers whether the signer is authorized for a bounded signing purpose. It does not prove that:

- the artifact belongs to the claimed class;
- the artifact belongs to the claimed release channel;
- the artifact is compatible with the target;
- a required Release Set is valid;
- the artifact is authorized for activation;
- migration and recovery conditions are satisfied.

### 4.8 Development trust

Each development workspace can generate or consume workspace-scoped local trust.

Development roots and certificates support local testing and transport without making production, sovereign, release, publication, governance, or conformance claims.

A shared local development root exists only through an explicit development trust-domain contract identifying all consumers, privileges, rotation, revocation, and cleanup.

### 4.9 Profile overlays

A primary profile establishes its baseline trust needs. An overlay can add assurance controls such as:

- hardware-backed custody;
- threshold signing;
- offline root storage;
- independent approval roots;
- reduced validity periods;
- stricter algorithms;
- additional revocation evidence;
- signed offline transfer;
- enhanced receipt and audit requirements.

Composition cannot broaden trust silently or weaken a global prohibition.

### 4.10 Authority separation

Trust verification does not replace:

- component-owned state validation;
- Governance Policy Runtime authorization;
- Resource Governor admission;
- privileged-broker execution;
- release-channel membership;
- artifact compatibility;
- Publication Gateway acceptance;
- evidence-custody decisions.

The service verifying a chain can report trust without acquiring the right to perform the requested operation.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SEC-TRUST-001,REQ-SEC-TRUST-002,REQ-SEC-TRUST-003,REQ-SEC-TRUST-004,REQ-SEC-TRUST-005,REQ-SEC-TRUST-006,REQ-SEC-TRUST-007,REQ-SEC-TRUST-008,REQ-SEC-TRUST-009,REQ-SEC-TRUST-010,REQ-SEC-TRUST-011,REQ-SEC-TRUST-012,REQ-SEC-TRUST-013,REQ-SEC-TRUST-014,REQ-SEC-TRUST-015,REQ-SEC-TRUST-016,REQ-SEC-TRUST-017,REQ-SEC-TRUST-018,REQ-SEC-TRUST-019,REQ-SEC-TRUST-020,REQ-SEC-TRUST-021,REQ-SEC-TRUST-022,REQ-SEC-TRUST-023,REQ-SEC-TRUST-024,REQ-SEC-TRUST-025,REQ-SEC-TRUST-026,REQ-SEC-TRUST-027,REQ-SEC-TRUST-028,REQ-SEC-TRUST-029,REQ-SEC-TRUST-030 -->
- **REQ-SEC-TRUST-001 — SHALL:** Every active trust root has a stable root identifier, accountable owner, trust purpose, authorized scopes, validity interval, key or anchor type, lifecycle status, revocation behavior, and canonical contract reference.
- **REQ-SEC-TRUST-002 — SHALL:** Every trust decision records the exact root set, chain, subject, credential or signature, operation, target, effective profile, time, validation policy, revocation context, and final outcome.
- **REQ-SEC-TRUST-003 — SHALL NOT:** Cryptographic validity grants authority outside the signer's or root's declared purpose, subject, operation, component, artifact class, release channel, profile, environment, tenant, audience, or time scope.
- **REQ-SEC-TRUST-004 — SHALL:** Trust scope is explicit and machine-readable for every applicable dimension rather than inferred from root possession, chain construction, storage location, network reachability, or operator familiarity.
- **REQ-SEC-TRUST-005 — SHALL NOT:** Trust propagates transitively between development, production, sovereign, release, governance, publication, evidence, user-identity, service-identity, or external-integration domains unless an active cross-trust contract declares the exact relationship.
- **REQ-SEC-TRUST-006 — SHALL NOT:** An intermediate authority, delegated credential, leaf certificate, signer, or verifier broadens the constraints of its parent root or delegating authority.
- **REQ-SEC-TRUST-007 — SHALL NOT:** A development root, generated workspace certificate authority, test signer, fixture key, or local service identity establishes production, sovereign, release, governance, publication, or user trust.
- **REQ-SEC-TRUST-008 — SHALL NOT:** Production, sovereign, release-signing, governance, publication, or user-identity private keys are copied into, reused by, or made available to development workspaces or tests.
- **REQ-SEC-TRUST-009 — SHALL:** Artifact-signing trust maps explicitly to the permitted artifact classes, release channels, producer identities, target profiles, verification policies, and validity periods.
- **REQ-SEC-TRUST-010 — SHALL:** Artifact verification evaluates signatures and credentials against the trust context recorded for the exact artifact, target, profile, release channel, and requested lifecycle transition.
- **REQ-SEC-TRUST-011 — SHALL NOT:** An artifact, offline bundle, Release Set, mirror, repository, transport, or peer silently adds a new root to the target trust store merely because the artifact or bundle contains that root.
- **REQ-SEC-TRUST-012 — SHALL:** Profile-specific requirements for hardware-backed keys, measured boot, threshold approval, offline custody, algorithm restrictions, independent roots, or enhanced evidence remain scoped to the profiles and overlays that declare them.
- **REQ-SEC-TRUST-013 — SHALL:** Trust requirements contributed by profile overlays compose through explicit compatibility, precedence, and conflict rules without weakening a primary profile or a global prohibition.
- **REQ-SEC-TRUST-014 — SHALL:** A generated development trust root and its issued certificates remain scoped to one workspace or one explicitly declared shared development trust domain and are removed or revoked during cleanup.
- **REQ-SEC-TRUST-015 — SHALL NOT:** A root private key, recovery secret, signing key, or equivalent root-capability material is distributed as an ordinary certificate, trust-store entry, artifact payload, log field, receipt field, example, or documentation value.
- **REQ-SEC-TRUST-016 — SHALL:** Root-key custody, signer access, issuance authority, verifier access, recovery access, and revocation authority follow least privilege and separation of duties appropriate to the effective profile.
- **REQ-SEC-TRUST-017 — SHALL:** Where threshold, multi-party, hardware-backed, or offline approval is required, the active profile or trust contract defines the threshold, roles, custody, recovery, evidence, and failure behavior.
- **REQ-SEC-TRUST-018 — SHALL:** Trust-root rotation defines predecessor and successor identifiers, overlap duration, accepted chains, target rollout order, cached-result invalidation, rollback or forward-repair behavior, and completion evidence.
- **REQ-SEC-TRUST-019 — SHALL:** Revocation of a root or delegated authority blocks new trust decisions within the revoked scope and triggers the declared replacement, containment, revalidation, recovery, or removal procedure.
- **REQ-SEC-TRUST-020 — SHALL:** Root compromise invalidates affected cached verification results and causes review of artifacts, credentials, sessions, receipts, active states, and dependent trust relationships within the compromise scope.
- **REQ-SEC-TRUST-021 — SHALL:** A trust-store update is validated and activated atomically within its owning authority boundary.
- **REQ-SEC-TRUST-022 — SHALL:** A failed trust-store update preserves or restores the last valid trust set or enters a declared forward-repair state without leaving a partially authoritative root set.
- **REQ-SEC-TRUST-023 — SHALL NOT:** Failure to resolve the required root, chain, validity, scope, revocation state, profile, policy, or verifier causes silent fallback to another root, weaker trust domain, public web trust, development trust, or operator-local trust.
- **REQ-SEC-TRUST-024 — SHALL:** Cross-signing and bridge trust declare both authorities, direction, permitted subjects and operations, profile and environment scope, maximum validity, revocation behavior, audit evidence, and termination procedure.
- **REQ-SEC-TRUST-025 — SHALL NOT:** Operating-system, browser, public web, enterprise, cloud, container-registry, or external-provider trust stores automatically become kOA internal component, release, governance, publication, or evidence trust.
- **REQ-SEC-TRUST-026 — SHALL NOT:** A root authorized for user identity, service identity, transport security, artifact signing, governance policy, publication approval, evidence signing, or external integration is treated as authorized for another purpose without an explicit active scope.
- **REQ-SEC-TRUST-027 — SHALL:** Trust decisions and lifecycle transitions emit machine-readable receipts that identify roots and scopes without exposing private keys, recovery material, secret values, or unnecessarily sensitive identity and provenance data.
- **REQ-SEC-TRUST-028 — SHALL NOT:** A trust root or successful trust verification acquires component data ownership, governance-policy authority, resource authority, host privilege, release-channel membership authority, publication authority, or mutation authority by implication.
- **REQ-SEC-TRUST-029 — SHALL:** Validation detects unknown roots, duplicate active root identities, overlapping contradictory scopes, excessive delegation, invalid chains, expired or revoked authorities, unscoped cross-signing, stale trust stores, unsafe fallback, and incomplete rotation or cleanup.
- **REQ-SEC-TRUST-030 — SHALL:** Every active trust-root requirement is traceable to accepted decisions, applicable locks, validation tests, and required evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Registering and activating a root

Root introduction:

1. identifies the bounded trust purpose;
2. identifies adjacent trust domains and prohibited uses;
3. assigns a stable root identifier and accountable owner;
4. records public material and integrity through the canonical trust contract;
5. declares profiles, environments, subjects, operations, channels, artifact classes, validity, delegation, and evidence;
6. defines private-key custody and recovery;
7. defines revocation and compromise response;
8. validates collision-free identity and non-overlapping authority;
9. stages the trust-store update;
10. activates the complete valid trust set atomically;
11. emits an activation receipt.

The root remains inactive when any required scope or authority is unresolved.

### 6.2 Verifying a trust path

A verifier:

1. resolves the requested operation and target;
2. resolves the active profile and trust context;
3. resolves the expected root set from trusted canonical configuration;
4. validates chain structure and cryptographic proofs;
5. intersects root, intermediate, delegated, and leaf constraints;
6. validates subject, purpose, operation, target, profile, environment, channel, artifact class, audience, and time;
7. checks validity and required revocation sources;
8. obtains policy authorization where applicable;
9. records each check and the final outcome;
10. emits a scoped receipt.

The credential does not select its own root set without external canonical confirmation.

### 6.3 Rotating a root

Root rotation:

1. creates a successor with a new root identity;
2. records the predecessor relationship;
3. defines the overlap and accepted-chain period;
4. updates issuers and signers in a controlled order;
5. distributes successor public material through an authorized path;
6. activates trust stores atomically;
7. reissues or replaces dependent credentials where required;
8. verifies targets using the successor path;
9. ends predecessor issuance;
10. revokes or retires the predecessor according to policy;
11. invalidates affected cached results;
12. records completion evidence.

### 6.4 Revoking or containing a compromised root

Compromise response:

1. identifies the affected root, delegated authorities, scope, and time window;
2. blocks new trust decisions within that scope;
3. distributes authenticated revocation or replacement information;
4. identifies artifacts, credentials, sessions, trust stores, receipts, and active states requiring review;
5. preserves unaffected trust domains;
6. replaces the root and dependent credentials;
7. revalidates or withdraws affected claims;
8. applies rollback or forward repair where active state depends on invalid trust;
9. records containment, recovery, and residual-risk evidence.

### 6.5 Importing trust for offline operation

Offline trust import:

1. begins from a previously trusted local bootstrap context;
2. verifies the bundle and trust-update manifest;
3. confirms that every proposed root or revocation belongs to an authorized trust-update contract;
4. validates scope, profile, target, integrity, provenance, signatures, compatibility, and validity;
5. keeps proposed trust material quarantined;
6. stages the complete trust-store replacement;
7. activates atomically;
8. preserves the previous valid set for declared recovery;
9. emits local verification and activation receipts.

A root embedded in an ordinary payload is not a trust-store update.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved authority | Blocked or degraded behavior | Evidence |
| --- | --- | --- | --- | --- |
| Required root identity is unresolved | Return a blocked trust outcome | Last valid root set | Dependent trust decision | Root-resolution failure |
| Chain is cryptographically invalid | Reject the claim | Existing trusted identities and artifacts | Requested operation | Chain-validation result |
| Chain is valid but scope mismatches | Reject authorization for that purpose | Validity of unrelated permitted scopes | Out-of-scope operation | Scope-mismatch receipt |
| Validity interval is expired or not yet active | Reject the claim | Other current credentials | Credential-dependent operation | Time-validation result |
| Required revocation source is unavailable | Keep the trust decision blocked | Last valid unrelated trust | Revocation-dependent operation | Revocation-source state |
| Root or delegation is revoked | Reject new trust and begin replacement policy | Historical identity and evidence | New use within revoked scope | Revocation receipt |
| Trust-store update is invalid | Keep the candidate inactive | Last valid trust store | New root or revocation activation | Trust-store validation failure |
| Trust-store activation partially fails | Restore the previous complete set or enter forward repair | Last coherent trust state | Candidate trust set | Activation and recovery receipt |
| Development root appears in production context | Reject the path and report domain misuse | Production trust context | Development credential use | Trust-domain incident |
| Public web root appears as internal authority | Reject internal authority inference | Explicit internal roots | Internal component or release claim | External-root mismatch |
| Root compromise is suspected | Contain affected scope and invalidate reusable results | Unaffected trust domains | Affected verification and activation | Incident and review evidence |
| Cross-signing contract expires | Stop accepting the bridge after its declared end | Independent native roots | Bridged trust path | Bridge-expiration evidence |
| Offline trust bundle is incomplete | Quarantine the complete update | Existing local trust store | Offline trust update | Bundle-completeness report |
| Evidence path is unavailable | Apply the declared synchronous-fail or bounded-queue rule | Source trust decision where permitted | Transition requiring mandatory evidence | Evidence-path state |
| Recovery material is unavailable | Follow the declared break-glass or forward-repair procedure without inventing a substitute root | Existing valid trust where possible | Recovery-dependent transition | Recovery failure |

## 8. Cross-Component Interactions

### 8.1 Identity and Trust

Identity and Trust performs chain, credential, signature, root, validity, and revocation verification through its active contract.

It reports scoped outcomes. It does not perform the component mutation, policy decision, resource admission, privileged operation, release activation, or publication transition.

### 8.2 Governance Policy Runtime

The Governance Policy Runtime decides whether a trusted subject is authorized for a governed action.

A valid credential can identify the subject and prove a bounded signature. It cannot bypass consent, disclosure, exception, privilege, or authorization policy.

### 8.3 Release and artifact owners

Artifact owners declare required signatures and trust contexts.

Release-channel authorities confirm channel membership. Activating components validate target compatibility and perform activation. Trust verification is one prerequisite among these independent checks.

### 8.4 Publication Gateway

Publication approvals, requests, and receipts can be signed within an explicit publication trust scope.

A publication signer does not gain authority over UCKK Import Bridge retrieval, local import acceptance, source-component data, destination-component state, or general release signing.

### 8.5 Resource Governor and privileged operations

The Resource Governor admits resource-consuming cryptographic and lifecycle work.

A privileged broker can access protected key devices only through a narrow authorized operation. Resource availability and host access do not broaden signing or trust authority.

### 8.6 Evidence authority

The evidence authority preserves trust receipts and authorized views.

Public evidence can expose root identifiers, statuses, algorithms, and verification outcomes where policy permits. Private proof can retain restricted chain, identity, provenance, and incident details without publishing secret material.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Effect |
| --- | --- |
| `DEC-PROFILE-001` | Keeps assurance, offline, hardware, and deployment-specific trust controls within explicit profile and overlay scope. |
| `DEC-DEV-001` | Establishes isolated workspace secrets, local identities, and generated local certificate material for development. |
| `DEC-REL-001` | Establishes independent release channels, Release Sets, and owner-controlled artifact verification and activation. |
| `DEC-DATA-001` | Preserves component data authority independently from trust verification and shared infrastructure. |
| `DEC-GATE-001` | Preserves separate Publication Gateway, UCKK publication transport, UCKK import, and local acceptance boundaries. |

### Prohibited assumptions

- one root can authorize every identity, artifact, policy, publication, and evidence purpose;
- a valid signature proves compatibility or activation authorization;
- a root is global because it appears in a default operating-system or browser store;
- a certificate can define its own trusted root set;
- an offline bundle can bootstrap arbitrary new trust from its own contents;
- a development certificate can support a production or conformance claim;
- a production signer can be copied into a test environment;
- a newer root automatically supersedes an older root;
- rotation is complete when the successor public key is distributed;
- revocation affects every trust domain rather than the declared scope;
- a verifier owns the operation it verifies;
- key custody grants component data ownership;
- hardware-backed storage grants policy authorization;
- cross-signing creates permanent bidirectional trust;
- an unavailable revocation source can be ignored;
- operator familiarity with a key replaces canonical scope;
- a recipe determines the global trust technology;
- high-assurance controls apply to every profile;
- public evidence can expose private keys or recovery material.

## 10. Validation Criteria

This document is conformant when:

1. `DOC-SEC-004` is active at `07-security/04-trust-root-scoping.md`.
2. Every canonical reference resolves.
3. Every listed decision exists with status `accepted`.
4. Every requirement in Section 5 exists with identical strength, statement, scope, owner, source decision, and validation mapping.
5. Every listed lock exists and is active.
6. Every active root has one unique identifier and one accountable owner.
7. Every active root declares purpose, scope dimensions, validity, lifecycle, revocation, custody, and canonical contract.
8. Root, intermediate, delegated, and leaf constraints form a non-broadening intersection.
9. Development, production, release, governance, publication, evidence, user, service, and external-integration trust domains do not overlap implicitly.
10. Artifact-signing scopes resolve artifact classes, release channels, profiles, producers, and transitions.
11. Trust-store updates activate atomically and preserve the last valid set.
12. Rotation declares successor, overlap, rollout, invalidation, recovery, and completion evidence.
13. Revocation and compromise tests block new affected trust and identify dependent objects for review.
14. Cached trust and artifact-verification results invalidate when roots, scopes, policies, revocation state, profiles, targets, or verifier semantics change.
15. Offline trust updates begin from an independently trusted bootstrap context.
16. Ordinary artifacts and bundles cannot silently add roots.
17. Development roots and private production keys remain isolated.
18. Profile-specific hardware, threshold, offline, and algorithm requirements remain profile-scoped.
19. Cross-signing has explicit direction, scope, validity, revocation, and termination.
20. Public, operating-system, browser, enterprise, cloud, and provider trust stores do not create implicit internal authority.
21. Trust receipts expose no private keys, recovery material, or secret values.
22. Trust verification does not acquire data, policy, resource, privilege, channel, publication, or mutation authority.
23. Unknown, invalid, expired, revoked, ambiguous, or unavailable required trust fails closed.
24. Every critical trust transition maps to tests and evidence.
25. Active prose is English and contains no unresolved-authority marker.
26. No normative keyword appears outside the generated requirement block.
27. The documentation dependency graph remains acyclic.

The validation entry point is:

`bash
python docs/tools/validate_docs.py
`

## 11. Non-Normative Examples

> **Non-normative example:** This example illustrates purpose scoping.

A root authorized to sign knowledge-channel Runtime Packs can validate a Runtime Pack signature. The same root does not automatically authorize a governance policy bundle or a service binary.

> **Non-normative example:** This example illustrates development isolation.

A workspace can generate a local root for mutual authentication among its containers. Another workspace and a sovereign node do not trust that root unless an explicit development trust-domain contract says otherwise.

> **Non-normative example:** This example illustrates rotation.

A release root can overlap with its successor for a bounded period. Targets receive and validate the successor before predecessor issuance ends, then the predecessor is retired or revoked according to the recorded policy.

> **Non-normative example:** This example illustrates offline bootstrap.

A sovereign-offline node can import a signed trust-store update from removable media. The node validates the update using a pre-existing local bootstrap root rather than trusting a new root solely because it is inside the bundle.

> **Non-normative example:** This example illustrates authority separation.

Identity and Trust can verify that a publication approval receipt was signed by an authorized publication role. Publication Gateway still decides whether the complete publication request satisfies disclosure and destination contracts.
