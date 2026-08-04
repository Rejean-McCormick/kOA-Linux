<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-007",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "governance_release_channel",
    "governance_policy_runtime_profiles"
  ],
  "canonical_refs": [
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/system.contract.json#/resource_governance/governance_policy_runtime",
    "contracts/system.contract.json#/global_boundaries/privilege",
    "contracts/release-channels.contract.json#/channels/governance",
    "contracts/artifact-classes.contract.json#/artifact_classes/governance_policy_bundle",
    "contracts/artifact-contracts/policy-bundle.schema.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/audit-broker.component.json",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-SYS-001",
    "DEC-PROFILE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-REL-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-GPB-001",
    "REQ-LIFE-GPB-002",
    "REQ-LIFE-GPB-003",
    "REQ-LIFE-GPB-004",
    "REQ-LIFE-GPB-005",
    "REQ-LIFE-GPB-006",
    "REQ-LIFE-GPB-007",
    "REQ-LIFE-GPB-008",
    "REQ-LIFE-GPB-009",
    "REQ-LIFE-GPB-010",
    "REQ-LIFE-GPB-011",
    "REQ-LIFE-GPB-012",
    "REQ-LIFE-GPB-013",
    "REQ-LIFE-GPB-014",
    "REQ-LIFE-GPB-015",
    "REQ-LIFE-GPB-016",
    "REQ-LIFE-GPB-017",
    "REQ-LIFE-GPB-018",
    "REQ-LIFE-GPB-019",
    "REQ-LIFE-GPB-020",
    "REQ-LIFE-GPB-021",
    "REQ-LIFE-GPB-022",
    "REQ-LIFE-GPB-023",
    "REQ-LIFE-GPB-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-GOV-001",
    "LOCK-DATA-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-SYS-020",
    "DOC-COMP-005",
    "DOC-COMP-011",
    "DOC-DEV-014",
    "DOC-LIFE-000",
    "DOC-LIFE-001",
    "DOC-LIFE-002",
    "DOC-LIFE-003",
    "DOC-LIFE-004"
  ],
  "tags": [
    "lifecycle",
    "governance",
    "policy-bundle",
    "governance-channel",
    "policy-runtime",
    "signing",
    "compatibility",
    "activation",
    "rollback",
    "offline-import",
    "receipts",
    "non-ai"
  ]
}
KOA:DOC-META:END -->

# Governance Policy Bundles

## 1. Purpose

This document defines the lifecycle of governance policy bundles used by deployments that instantiate Governance Policy Runtime.

A governance policy bundle is a versioned, verifiable artifact in the `governance` release channel. It packages deterministic policy modules and the metadata required to validate, stage, activate, audit, roll back, recover, deprecate, and reproduce their behavior.

The bundle carries policy implementation. It does not create its own authority. Owner decisions, profile membership, trust roots, artifact classes, release compatibility, component ownership, and exception authority remain with their canonical owners.

The active bundle format is owned by `contracts/artifact-contracts/policy-bundle.schema.json`.

## 2. Scope

This document applies to:

- deterministic governance policy source and compiled modules;
- policy-bundle manifests;
- build and compilation provenance;
- integrity and signing;
- profile and policy-runtime compatibility;
- governance release-channel publication;
- independent governance-channel updates;
- Release Set updates;
- staging and quarantine;
- target validation;
- atomic activation;
- rollback, restore, forward repair, and recovery;
- offline export and import;
- deprecation, revocation, expiry, supersession, retention, and deletion;
- activation, failure, recovery, and audit receipts;
- evidence supporting bundle, activation, and conformance claims.

It applies only to profiles that require or allow Governance Policy Runtime. It does not make the runtime a universal baseline component.

This document does not define policy semantics, owner decisions, trust-root management, source-component data, privileged execution implementation, Resource Governor policy, or publication authority.

## 3. Canonical References

| Canonical reference | Ownership |
| --- | --- |
| `contracts/system.contract.json#/release_and_artifact_identity` | Release channels, Release Sets, independent updates, non-partial activation, and recovery |
| `contracts/system.contract.json#/critical_transitions` | Policy, artifact, and release receipts |
| `contracts/system.contract.json#/resource_governance/governance_policy_runtime` | Governance Policy Runtime authority domains and profile-conditioned membership |
| `contracts/system.contract.json#/global_boundaries/privilege` | Policy decision, profile authorization, and narrow privilege requirements |
| `contracts/release-channels.contract.json#/channels/governance` | Governance release-channel identity and channel behavior |
| `contracts/artifact-classes.contract.json#/artifact_classes/governance_policy_bundle` | Bundle artifact class, integrity, signing, activation, recovery, retention, and evidence |
| `contracts/artifact-contracts/policy-bundle.schema.json` | Bundle structure and field constraints |
| `contracts/artifact-contracts/release-set.schema.json` | Compatible multi-channel release composition |
| `contracts/artifact-contracts/offline-bundle.schema.json` | Signed offline transfer, quarantine, and import |
| `contracts/components/governance-policy-runtime.component.json` | Runtime loading, evaluation, decision, failure, and recovery behavior |
| `contracts/components/identity-and-trust.component.json` | Signer identity, trust scope, verification, and revocation |
| `contracts/components/koa-node-agent.component.json` | Target-local activation, non-partial transition, rollback, and receipts |
| `contracts/components/audit-broker.component.json` | Selective activation and policy-decision audit |
| `generated/profile-catalog.json` | Profile applicability and overlays |
| `generated/requirements-index.json` | Normative statements projected in Section 5 |
| `generated/assertion-index.json` | Governance, data, lifecycle, profile, component, and AI invariants |
| `generated/traceability.json` | Links among decisions, bundles, profiles, components, tests, receipts, and evidence |
| `generated/test-catalog.json` | Registered policy-bundle tests |
| `generated/evidence-catalog.json` | Active evidence and validity |

## 4. Model and Responsibilities

### 4.1 Bundle identity

A policy bundle is one immutable release artifact with:

- one bundle identity;
- one version;
- one policy namespace;
- one governance-channel identity;
- one target-profile set;
- one supported runtime-version range;
- one complete included-module manifest;
- one provenance chain;
- one integrity and trust state;
- one activation and recovery contract.

A new canonical byte representation uses a new artifact identity.

### 4.2 Required bundle sections

| Section | Content |
| --- | --- |
| `identity` | Bundle identifier, semantic version, artifact class, governance release-channel identity, creation time, status, and language. |
| `scope` | Policy namespace, authority domains, target profiles, target runtime versions, component consumers, connectivity assumptions, and applicability constraints. |
| `contents` | Included deterministic policy modules, compiled artifacts, static data required by policy evaluation, and module manifests. |
| `compatibility` | Required system, service, knowledge, runtime, schema, profile, and Release Set versions; incompatible versions and conflicts. |
| `provenance` | Source revision, compiler, toolchain, configuration, producer identity, build worker, input artifacts, tests, and evidence. |
| `integrity and trust` | Digests, signatures, signing identity, trust scope, certificate or key references, revocation information, and validity interval. |
| `activation` | Preconditions, staging behavior, smoke tests, atomic switch mechanism, expected active state, and activation receipt policy. |
| `recovery` | Previous-state retention, rollback or restore artifact, forward-repair conditions, recovery tests, and recovery receipt policy. |
| `lifecycle` | Effective time, expiry, supersession, deprecation, revocation, archival, retention, export, and disposition rules. |

Raw secrets, private keys, arbitrary commands, unrestricted scripts, undeclared native code, and mutable provider dependencies remain outside the bundle.

### 4.3 Policy modules

Each policy module declares:

- module identifier and version;
- policy authority domain;
- accepted input contract;
- produced decision contract;
- deterministic evaluation behavior;
- precedence and conflict rules;
- dependencies;
- validity conditions;
- tests and evidence;
- deprecation and replacement relationships.

A module may implement authorization, disclosure, consent, privilege decisions, or governed exceptions only within the authority granted by active decisions, profiles, and contracts.

### 4.4 Build and compilation

Policy source is compiled through a registered deterministic toolchain.

The build records:

- source revision;
- compiler and toolchain identity;
- build configuration;
- dependency lock state;
- included schemas and static data;
- build worker identity;
- input artifact identities;
- tests and evidence;
- produced bundle identity.

A development build produces a candidate. Governance-channel publication and release approval remain separate.

### 4.5 Verification

| Check | Acceptance condition | Failure result |
| --- | --- | --- |
| Schema | Bundle and every included module match active registered schemas. | Reject or quarantine |
| Identity | Bundle, module, dependency, and release identities are unique and resolvable. | Reject |
| Integrity | Artifact digests match the canonical bytes. | Quarantine |
| Signature and trust | Required signatures validate under an authorized non-revoked trust scope. | Reject or quarantine |
| Validity | Effective time, expiry, revocation, and supersession conditions permit use. | Reject or retain as historical only |
| Profile applicability | The target primary profile and overlays permit the policy runtime and bundle. | Block activation |
| Runtime compatibility | The policy runtime supports the bundle and module contract versions. | Block activation |
| Dependency compatibility | All referenced policy, schema, data, system, services, and knowledge dependencies resolve. | Block activation |
| Conflict analysis | Precedence, conflicts, duplicate domains, and incompatible rules have deterministic registered resolution. | Block activation |
| Authority boundaries | Rules remain within declared policy domains and do not acquire component, profile, trust, release, or resource authority. | Block activation |
| Behavior tests | Allow, deny, consent, disclosure, privilege, exception, break-glass, offline, and failure behavior passes registered tests. | Block activation |
| Recovery | Previous valid state and declared rollback, restore, or repair path are verified. | Block activation |

Verification is performed before staging, again before activation when required, and after transfer to a target whose trust or profile context differs.

### 4.6 Staging and quarantine

A verified source may enter staging. An offline, externally transferred, incompletely trusted, or failed candidate enters quarantine.

Neither state affects active policy evaluation.

Quarantine permits bounded inspection, verification, and deletion. It does not permit policy execution against authoritative requests.

### 4.7 Activation

Activation changes the complete active policy set used by Governance Policy Runtime.

The transition:

1. verifies the candidate;
2. verifies target state and compatibility;
3. runs pre-activation tests;
4. preserves the previous valid set;
5. stages the complete new set;
6. switches atomically;
7. runs post-activation health and decision tests;
8. records the outcome and recovery reference.

The active state is never an unvalidated mixture of old and new modules.

### 4.8 Release channel and Release Sets

The governance channel may update independently when declared compatibility remains satisfied.

A Release Set may bind governance with system, services, and knowledge-channel releases. In that case, bundle activation follows the Release Set's complete compatibility and non-partial activation rules.

An independent governance update cannot silently require an unavailable system, service, knowledge artifact, profile capability, or runtime version.

### 4.9 Trust and authority

Identity and Trust verifies signatures and signer scope. It does not decide policy correctness.

Governance Policy Runtime evaluates admitted policy modules. It does not create owner decisions.

The kOA Node Agent or equivalent profile-authorized local lifecycle component performs target-local activation. It does not define policy semantics.

Audit Broker records bounded policy and activation evidence. Observation does not transfer policy authority.

Resource Governor limits compilation, verification, loading, tests, and activation work. It does not grant authorization.

### 4.10 AI boundary

ChatGPT may help a user draft candidate policy text, examples, or tests outside the authoritative lifecycle. Such material remains candidate input until deterministic compilation, registered validation, review, and acceptance.

Suno, Gamma, and Ariane voice have no policy-bundle lifecycle authority.

No native or external AI service compiles, merges, resolves conflicts, authorizes, activates, repairs, or validates a bundle as an authoritative operation.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-GPB-001,REQ-LIFE-GPB-002,REQ-LIFE-GPB-003,REQ-LIFE-GPB-004,REQ-LIFE-GPB-005,REQ-LIFE-GPB-006,REQ-LIFE-GPB-007,REQ-LIFE-GPB-008,REQ-LIFE-GPB-009,REQ-LIFE-GPB-010,REQ-LIFE-GPB-011,REQ-LIFE-GPB-012,REQ-LIFE-GPB-013,REQ-LIFE-GPB-014,REQ-LIFE-GPB-015,REQ-LIFE-GPB-016,REQ-LIFE-GPB-017,REQ-LIFE-GPB-018,REQ-LIFE-GPB-019,REQ-LIFE-GPB-020,REQ-LIFE-GPB-021,REQ-LIFE-GPB-022,REQ-LIFE-GPB-023,REQ-LIFE-GPB-024 -->
- **REQ-LIFE-GPB-001 — SHALL:** A governance policy bundle shall be a registered artifact in the `governance` release channel and shall conform to the active policy-bundle schema.
- **REQ-LIFE-GPB-002 — SHALL:** Each bundle shall identify its bundle identity, version, policy namespace, policy-runtime compatibility, target profiles, source and compiler provenance, included policy modules, dependencies, validity conditions, activation strategy, and recovery strategy.
- **REQ-LIFE-GPB-003 — SHALL:** Each included policy module shall have a stable identifier, version, declared authority domain, input contract, output contract, precedence or conflict behavior, and test references.
- **REQ-LIFE-GPB-004 — SHALL NOT:** A policy bundle shall not create, replace, or infer an owner decision, profile membership, trust root, component authority, release compatibility rule, or exception authority.
- **REQ-LIFE-GPB-005 — SHALL NOT:** A policy bundle shall not contain raw secrets, private keys, arbitrary executable commands, unrestricted scripts, undeclared native code, or mutable external-provider dependencies.
- **REQ-LIFE-GPB-006 — SHALL:** Policy compilation shall be deterministic and shall record the source revision, compiler identity, toolchain identity, configuration, and complete input artifact identities.
- **REQ-LIFE-GPB-007 — SHALL:** A bundle used beyond local development shall include or reference valid provenance, integrity, compatibility, test, and evidence records.
- **REQ-LIFE-GPB-008 — SHALL:** A bundle shall be signed when required by the artifact class, active profile, trust scope, release contract, or security policy.
- **REQ-LIFE-GPB-009 — SHALL:** Bundle verification shall validate schema, identity, manifest, integrity, signature, signer trust, revocation, validity interval, target profile, runtime compatibility, dependencies, conflicts, and Release Set compatibility when applicable.
- **REQ-LIFE-GPB-010 — SHALL NOT:** A valid signature alone shall not establish policy correctness, authorization, profile applicability, runtime compatibility, or release approval.
- **REQ-LIFE-GPB-011 — SHALL:** A candidate bundle shall be staged or quarantined separately from the active policy set and shall not affect decisions before successful activation.
- **REQ-LIFE-GPB-012 — SHALL:** Activation shall be atomic and shall switch from one complete validated policy set to another complete validated policy set.
- **REQ-LIFE-GPB-013 — SHALL NOT:** Activation failure, runtime crash, or host restart shall not leave a partially active governance policy set.
- **REQ-LIFE-GPB-014 — SHALL:** Before activation, the target shall run schema, compatibility, conflict, authorization-boundary, deterministic-decision, denial, exception, break-glass, offline, performance, rollback, and recovery tests applicable to the bundle.
- **REQ-LIFE-GPB-015 — SHALL:** Bundle activation shall require target-node or target-runtime final validation and shall produce a machine-readable activation receipt.
- **REQ-LIFE-GPB-016 — SHALL:** The activation receipt shall identify the previous and new bundle sets, target profile, runtime version, policy decision or release authorization, verification results, activation outcome, timing, actor or component identity, and rollback or recovery reference.
- **REQ-LIFE-GPB-017 — SHALL:** A failed activation shall preserve or restore the previous valid policy set and shall execute the declared rollback, restore, or forward-repair strategy.
- **REQ-LIFE-GPB-018 — SHALL:** An independent governance-channel update shall activate only when all declared compatibility constraints with the active system, services, knowledge artifacts, profiles, and policy runtime remain satisfied.
- **REQ-LIFE-GPB-019 — SHALL:** A governance policy bundle included in a Release Set shall activate consistently with the Release Set's compatibility and non-partial activation rules.
- **REQ-LIFE-GPB-020 — SHALL:** Offline transfer shall use a signed and integrity-protected offline bundle, quarantine on import, local trust and compatibility verification, explicit activation, and local receipts.
- **REQ-LIFE-GPB-021 — SHALL:** Loss of network, control plane, remote artifact source, or external service shall preserve the previously valid local policy set and shall not trigger silent fallback or automatic policy substitution.
- **REQ-LIFE-GPB-022 — SHALL NOT:** Native or external AI shall not compile, select, merge, resolve conflicts, authorize, activate, repair, or validate governance policy bundles as an authoritative operation.
- **REQ-LIFE-GPB-023 — SHALL:** Deprecation, revocation, expiry, supersession, retention, export, and deletion of a policy bundle shall preserve required receipts, provenance, historical decision reproducibility, and recovery obligations.
- **REQ-LIFE-GPB-024 — SHALL:** Every active governance policy bundle, activation, compatibility, rollback, recovery, and conformance claim shall be traceable to accepted decisions, active requirements, applicable locks, registered tests, and valid evidence.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Build a candidate bundle

1. Select the accepted owner decisions and active policy sources.
2. resolve module identifiers, authority domains, dependencies, and target profiles;
3. select the registered deterministic compiler and toolchain;
4. compile in an isolated environment;
5. construct the complete manifest;
6. run schema, unit, deterministic-decision, conflict, and compatibility tests;
7. record provenance and evidence;
8. compute integrity values;
9. sign when required;
10. register the candidate without activating it.

### 6.2 Publish to the governance channel

1. Verify candidate identity and artifact class.
2. verify build provenance, tests, evidence, integrity, and required signatures;
3. verify deprecation and compatibility declarations;
4. assign governance-channel release identity;
5. publish the immutable artifact and manifest;
6. preserve the candidate-to-release lineage;
7. record publication evidence.

Publication makes the artifact available. It does not activate it on a target.

### 6.3 Stage a bundle

1. Receive the selected artifact.
2. verify transport and artifact integrity;
3. verify signer identity and trust when required;
4. validate schema, profile applicability, runtime compatibility, and dependencies;
5. evaluate quarantine conditions;
6. place the bundle in staging or quarantine;
7. record staging or quarantine state;
8. produce the applicable receipt.

### 6.4 Activate an independent governance update

1. Resolve the active target profile and policy runtime.
2. resolve the current governance bundle set;
3. verify independent-update compatibility with active system, services, and knowledge artifacts;
4. verify policy authority boundaries and conflicts;
5. run applicable pre-activation tests;
6. verify the previous valid set and recovery path;
7. request target-local activation;
8. switch to the complete new set atomically;
9. run post-activation tests;
10. produce activation and audit receipts;
11. retain the previous set according to recovery and retention policy.

### 6.5 Activate through a Release Set

1. Resolve the complete Release Set.
2. verify required channel membership;
3. verify cross-channel compatibility;
4. stage every required artifact;
5. verify every target-local precondition;
6. activate through the Release Set's non-partial transition;
7. verify system, services, governance, and knowledge state;
8. produce release and artifact activation receipts;
9. recover the complete prior valid state when the transition fails.

### 6.6 Roll back or repair

1. Identify the failed activation and affected bundle set.
2. resolve the declared recovery strategy;
3. verify the previous or repair artifact;
4. authorize the recovery transition;
5. stop new governed mutations when required;
6. restore, roll back, or forward-repair the complete policy set;
7. run decision, denial, exception, and health tests;
8. produce recovery and audit receipts;
9. invalidate unsupported evidence and claims.

### 6.7 Import through an offline bundle

1. Receive the selected offline bundle.
2. verify offline-bundle structure, integrity, signatures, signer trust, and transfer provenance;
3. import into quarantine;
4. extract and verify the policy bundle independently;
5. validate local profile, runtime, dependencies, conflicts, and compatibility;
6. stage the candidate;
7. require explicit local activation;
8. produce import, staging, activation, and recovery receipts as applicable.

### 6.8 Deprecate, revoke, or supersede

1. Record the lifecycle action and authority.
2. identify affected profiles, runtimes, Release Sets, targets, tests, evidence, and historical decisions;
3. define replacement or continued-use behavior;
4. prevent unsupported new activation;
5. preserve historical artifacts needed to reproduce prior decisions;
6. migrate or activate the replacement through ordinary procedures;
7. retain receipts, provenance, and recovery material;
8. dispose only after retention and dependency checks pass.

## 7. Failure States and Safe Degradation

| Failure state | Required behavior | Preserved state | Blocked behavior or claim |
| --- | --- | --- | --- |
| Schema or manifest invalid | Reject the bundle before staging. | Current active policy set | Candidate use |
| Integrity mismatch | Quarantine the candidate and block dependent claims. | Current active policy set and historical evidence | Activation |
| Signature or trust failure | Reject or quarantine the candidate without changing active trust or policy. | Existing trusted policy set | Candidate authority |
| Bundle expired, revoked, or superseded | Prevent new activation and apply the registered active-state policy for already active bundles. | Historical receipts and reproducibility data | Unsupported continued claim |
| Runtime incompatibility | Block activation and preserve the current policy runtime and bundle. | Existing decisions | Schema guessing or automatic conversion |
| Policy conflict unresolved | Block activation. | Current deterministic decision behavior | Implicit precedence |
| Required test or evidence missing | Block the affected activation or conformance claim. | Candidate and logs as non-authoritative material | Release or activation approval |
| Staging storage pressure | Defer or reject the candidate and preserve recovery capacity. | Active bundle and recovery state | Additional staging |
| Activation process fails | Retain or restore the previous complete valid set and produce failure and recovery receipts. | Previous valid decision behavior | Partial active set |
| Governance Policy Runtime fails after switch | Revert or recover according to the declared strategy. | Previous valid set and recovery artifacts | Automatic unknown fallback |
| Control plane unavailable | Continue the previous valid local policy set and block unsupported new remote activations. | Node-local governance decisions | Unverified desired state |
| Network unavailable | Use already active local bundles and permit verified local offline import where the profile allows it. | Local policy behavior | Silent remote substitution |
| Audit Broker unavailable | Preserve local activation evidence and block a claim that requires unavailable audit registration. | Active policy and local receipts | Unsupported audit claim |
| Recovery artifact unavailable | Block activation before the switch. | Current active policy set | Unrecoverable transition |

A bundle failure never broadens policy, grants privilege, changes trust, creates a profile, or authorizes a partial policy set.

## 8. Cross-Component Interactions

| Producer or owner | Consumer | Interaction | Authority boundary |
| --- | --- | --- | --- |
| Policy source owner | Policy compiler | Accepted source, module identity, and authority domain | Compiler does not create owner decisions |
| Build farm | Governance release workflow | Candidate bundle, provenance, tests, evidence, and signatures | Candidate output is not release approval |
| Governance release channel | Target or control plane | Immutable bundle and manifest | Publication is not activation |
| Control plane | Target Node Agent | Coordinated desired bundle or Release Set | Target-local validation remains required |
| kOA Node Agent | Governance Policy Runtime | Stage and atomically activate the verified complete set | Node Agent does not define policy semantics |
| Governance Policy Runtime | Owning components | Deterministic policy decisions and receipts | Runtime does not acquire component data authority |
| Identity and Trust | Verifier and runtime | Signer identity, trust scope, and revocation | Signature validity is not policy correctness |
| Resource Governor | Compiler, verifier, runtime, and activation workers | CPU, memory, I/O, concurrency, queue, and process limits | Resource control is not policy authority |
| Audit Broker | Policy and release workflows | Selective policy-decision, activation, failure, and recovery records | Audit does not alter policy state |
| Offline-bundle importer | Local quarantine and staging | Signed controlled transfer | Import does not imply activation |
| Release Set | Target lifecycle | Cross-channel compatibility and coordinated activation | One channel cannot infer another channel's compatibility |
| Evidence registry | Release and conformance gates | Active valid bundle, test, activation, and recovery evidence | Evidence registration does not activate a bundle |

No interaction permits direct writes to another component's authoritative source tables.

## 9. Decision Closure and Prohibited Assumptions

### Accepted decisions

| Decision ID | Closed question |
| --- | --- |
| `DEC-SYS-001` | Governance artifacts operate inside the local-first, modular, explicit-authority system baseline. |
| `DEC-PROFILE-001` | Governance Policy Runtime and bundle applicability are profile-conditioned. |
| `DEC-DATA-001` | Policy runtime and lifecycle components cannot write another component's authoritative source tables directly. |
| `DEC-GOV-001` | Governance Policy Runtime owns policy decisions and remains separate from Resource Governor. |
| `DEC-REL-001` | Governance is one release channel and uses Release Sets, compatibility, non-partial activation, receipts, and recovery. |
| `DEC-AI-001` | Native and external AI have no authoritative policy-bundle lifecycle role. |

### Prohibited assumptions

- Every profile installs Governance Policy Runtime.
- A bundle is authoritative because it exists in a repository.
- A development build is a governance-channel release.
- A published bundle is active on every target.
- A valid signature proves correct policy behavior.
- A trusted signer can redefine an owner decision.
- A bundle can add its own trust root.
- Root or administrator identity may activate policy without profile and policy authorization.
- A control-plane request bypasses target validation.
- Independent governance updates may ignore other active channels.
- A Release Set may partially activate its governance modules.
- Unresolved policy conflicts may use document order or file order.
- A runtime may guess a missing schema or dependency.
- Offline import implies activation.
- Network loss permits remote fallback.
- Policy-runtime failure permits silent allow-by-default behavior.
- Break-glass rules may be introduced without stronger authority and receipts.
- External AI output is compiled policy authority.
- Historical bundles may be deleted when they are still required to reproduce decisions.
- Missing evidence may be replaced by operator confidence.

## 10. Validation Criteria

1. The metadata block parses as JSON and declares `DOC-LIFE-007`, status `active`, language `en`, lifecycle layer, and the two declared scopes.
2. All eleven required sections exist in numerical order.
3. Every decision ID is accepted in `generated/decision-index.json`.
4. Every requirement ID appears exactly once in `generated/requirements-index.json`.
5. Every lock ID resolves to an active lock.
6. `TEST-LIFE-GPB-001` validates bundle schema, required sections, identities, versions, and manifest completeness.
7. `TEST-LIFE-GPB-002` verifies stable module identities, authority domains, contracts, conflicts, dependencies, and test references.
8. `TEST-LIFE-GPB-003` rejects raw secrets, private keys, arbitrary executable commands, unrestricted scripts, undeclared native code, and mutable provider dependencies.
9. `TEST-LIFE-GPB-004` verifies deterministic compilation and complete source, compiler, toolchain, configuration, worker, and input provenance.
10. `TEST-LIFE-GPB-005` verifies integrity, signatures, trust scope, revocation, validity, and target identity.
11. `TEST-LIFE-GPB-006` verifies that signature validity does not bypass correctness, compatibility, profile, policy, or release gates.
12. `TEST-LIFE-GPB-007` verifies profile, runtime, dependency, conflict, system, services, knowledge, and Release Set compatibility.
13. `TEST-LIFE-GPB-008` verifies staging and quarantine isolation from active decisions.
14. `TEST-LIFE-GPB-009` verifies deterministic allow, deny, consent, disclosure, privilege, exception, and break-glass behavior.
15. `TEST-LIFE-GPB-010` verifies target-local final validation and complete activation receipts.
16. `TEST-LIFE-GPB-011` verifies atomic activation with no mixed or partial policy set.
17. `TEST-LIFE-GPB-012` verifies rollback, restore, forward repair, and preservation of the previous valid set.
18. `TEST-LIFE-GPB-013` verifies independent governance-channel updates under declared compatibility.
19. `TEST-LIFE-GPB-014` verifies coordinated Release Set activation and complete recovery on failure.
20. `TEST-LIFE-GPB-015` verifies signed offline transfer, quarantine, local verification, explicit activation, and receipts.
21. `TEST-LIFE-GPB-016` verifies local policy continuity without control plane, network, remote source, or external service and rejects silent fallback.
22. `TEST-LIFE-GPB-017` verifies absence of native or external AI compilation, selection, conflict resolution, authorization, activation, repair, and validation.
23. `TEST-LIFE-GPB-018` verifies expiry, revocation, deprecation, supersession, retention, historical reproducibility, and disposition.
24. `TEST-LIFE-GPB-019` verifies bounded compilation, verification, loading, staging, activation, rollback, and evidence resources.
25. `TEST-LIFE-GPB-020` verifies traceability to decisions, requirements, locks, profiles, components, artifacts, releases, tests, receipts, and evidence.
26. Active prose is English and contains no unresolved marker, placeholder, metadata hash, or source hash.
27. The generated requirement block matches the canonical requirement registry.

These criteria define validation requirements. They do not claim that a particular policy source, bundle, signer, target, runtime, Release Set, or activation already conforms.

## 11. Non-Normative Examples

> **Non-normative example:** A bundle changes disclosure rules for one sovereign profile. The build records source, compiler, worker, inputs, tests, and evidence. The target verifies profile and runtime compatibility, stages the bundle, runs decision tests, switches atomically, and produces an activation receipt.

> **Non-normative example:** A signature validates, but the bundle targets a newer runtime contract than the node supports. Activation is blocked and the current policy set remains active.

> **Non-normative example:** Two included modules define incompatible outcomes for the same authority domain without a registered conflict rule. The bundle is rejected rather than using file order.

> **Non-normative example:** A control plane distributes a new governance-channel artifact. The target Node Agent independently verifies expected state, profile, compatibility, integrity, signatures, recovery readiness, and authorization before activating it.

> **Non-normative example:** An offline bundle arrives on removable media. The policy bundle enters quarantine, is verified locally, and remains inactive until an authorized local activation request succeeds.

> **Non-normative example:** ChatGPT proposes a candidate consent rule. A policy owner reviews it, records the required owner decision, implements deterministic policy source, compiles it with the registered toolchain, runs registered tests, and admits the resulting bundle through the ordinary lifecycle. The generated suggestion has no direct authority.
