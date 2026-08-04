<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-008",
  "document_class": "architecture_decision_record",
  "status": "active",
  "adr_status": "accepted",
  "language": "en",
  "layer": "architecture_decisions",
  "scope": [
    "global"
  ],
  "decision_date": "2026-08-03",
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/release-channels.contract.json",
    "schemas/release-channels.contract.schema.json",
    "contracts/artifact-classes.contract.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/examples/release-set.example.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/integration-types.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/exception-index.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-LIFE-001",
    "DEC-LIFE-CHANNEL-001",
    "DEC-LIFE-ACT-001",
    "DEC-SYS-COMP-001",
    "DEC-SYS-OFFLINE-001",
    "DEC-SYS-AUDIT-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-CHANNEL-001",
    "REQ-LIFE-CHANNEL-002",
    "REQ-LIFE-CHANNEL-003",
    "REQ-LIFE-CHANNEL-004",
    "REQ-LIFE-CHANNEL-005",
    "REQ-LIFE-CHANNEL-006",
    "REQ-LIFE-CHANNEL-007",
    "REQ-LIFE-CHANNEL-008",
    "REQ-LIFE-CHANNEL-009",
    "REQ-LIFE-CHANNEL-010",
    "REQ-LIFE-CHANNEL-011",
    "REQ-LIFE-CHANNEL-012",
    "REQ-LIFE-CHANNEL-013",
    "REQ-LIFE-CHANNEL-014",
    "REQ-LIFE-CHANNEL-015",
    "REQ-LIFE-CHANNEL-016",
    "REQ-LIFE-CHANNEL-017",
    "REQ-LIFE-CHANNEL-018",
    "REQ-LIFE-CHANNEL-019",
    "REQ-LIFE-CHANNEL-020",
    "REQ-LIFE-CHANNEL-021",
    "REQ-LIFE-CHANNEL-022",
    "REQ-LIFE-CHANNEL-023",
    "REQ-LIFE-CHANNEL-024",
    "REQ-LIFE-CHANNEL-025",
    "REQ-LIFE-CHANNEL-026",
    "REQ-LIFE-CHANNEL-027",
    "REQ-LIFE-CHANNEL-028",
    "REQ-LIFE-CHANNEL-029",
    "REQ-LIFE-CHANNEL-030",
    "REQ-LIFE-CHANNEL-031",
    "REQ-LIFE-CHANNEL-032",
    "REQ-LIFE-CHANNEL-033",
    "REQ-LIFE-CHANNEL-034",
    "REQ-LIFE-CHANNEL-035",
    "REQ-LIFE-CHANNEL-036",
    "REQ-LIFE-CHANNEL-037",
    "REQ-LIFE-CHANNEL-038",
    "REQ-LIFE-CHANNEL-039",
    "REQ-LIFE-CHANNEL-040"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-GATE-001",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-GOV-001",
    "DOC-GOV-002",
    "DOC-GOV-003",
    "DOC-GOV-004",
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-007",
    "DOC-GOV-008",
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
    "DOC-SEC-005",
    "DOC-SEC-006",
    "DOC-SEC-016",
    "DOC-OPS-003",
    "DOC-OPS-013",
    "DOC-CONF-003",
    "DOC-CONF-013",
    "DOC-CONF-019"
  ],
  "supersedes": [],
  "superseded_by": [],
  "tags": [
    "adr",
    "release-channels",
    "release-set",
    "independent-versioning",
    "compatibility",
    "atomic-activation",
    "rollback",
    "forward-repair",
    "offline-release",
    "accepted-decision"
  ]
}
KOA:DOC-META:END -->

# ADR-008: Four Independent Release Channels

## 1. Status

**Accepted**

Decision date: **2026-08-03**

This ADR records the accepted architectural decision to divide kOA release artifacts into four independently versioned channels:

```text
system
services
governance
knowledge
```

The decision establishes independent versioning, not independent activation.

Every authoritative active state is one complete compatible Release Set containing exactly one version from each channel.

The machine-readable release-channels registry owns the active channel identities, artifact memberships, compatibility constraints, Release Set records, and lifecycle facts. This ADR records the rationale, consequences, and rejected alternatives behind that model.

## 2. Context

kOA contains several classes of change with different owners, risk profiles, rates of evolution, and recovery needs.

Examples include:

- foundational host, boot, recovery, and node execution artifacts;
- executable component services and service migrations;
- governance registries, policies, contracts, decisions, and schemas;
- knowledge, language, terminology, UCKK, and runtime-pack artifacts.

Treating all of these as one monolithic version creates avoidable coupling. A terminology correction or knowledge-pack update would require a system-image version change even when no system artifact changed. A service patch would force a governance version change even when governance authority was unchanged. Operationally unrelated changes would become indistinguishable inside one global version.

Treating each package as independently activatable creates the opposite failure. Nodes could assemble combinations that were never tested together. A new services package could require a newer governance contract. A governance change could reject an older artifact class. A knowledge pack could require a newer deterministic runtime. A system substrate could remove an interface required by an older service version.

The architecture therefore needs both:

1. independent version identities for independently owned classes of change;
2. one atomic compatibility and activation unit for the complete authoritative state.

The decision also needs to support:

- sovereign and offline nodes;
- complete rollback;
- forward repair;
- signed distribution;
- profile-specific compatibility;
- component data ownership;
- separate build, publication, approval, signing, and activation authority;
- historical interpretation of the exact active combination.

## 3. Decision

kOA uses four canonical release channels:

| Channel | Architectural responsibility |
| --- | --- |
| `system` | Host, node, boot, recovery, foundational runtime, and system-execution substrate |
| `services` | Executable component services, service packages, manifests, migrations, and service runtime assets |
| `governance` | Authority, policy, contracts, registries, schemas, decisions, lifecycle rules, and conformance artifacts |
| `knowledge` | Knowledge packages, terminology, language assets, UCKK artifacts, runtime packs, and distributable knowledge resources |

Each active artifact class belongs to exactly one channel.

Each channel has:

- one canonical owner;
- independent semantic versions;
- immutable published manifests;
- explicit artifact membership;
- compatibility metadata;
- tests and evidence;
- activation and recovery policy.

A channel can publish a new version while the other three channels retain their existing versions.

A changed channel does not activate by itself. The change creates a new candidate Release Set that selects:

```text
one system version
one services version
one governance version
one knowledge version
```

The selected combination passes all applicable directional compatibility constraints, profile checks, tests, evidence checks, signature verification, release gates, staging checks, and activation checks.

The Release Set is the canonical unit of:

- approval;
- signing;
- distribution;
- staging;
- activation;
- rollback;
- forward repair;
- revocation;
- profile and deployment claims.

Independent versioning is therefore combined with complete activation.

## 4. Channel Boundaries

### 4.1 System channel

The system channel carries artifacts that establish the protected execution substrate.

Typical members include:

- immutable operating-system and recovery artifacts;
- boot and recovery configuration;
- host and node foundations;
- foundational runtime dependencies;
- protected system configuration;
- node-level execution mechanisms;
- system compatibility metadata.

A system-channel artifact does not become owner of service data, governance policy, or knowledge semantics.

### 4.2 Services channel

The services channel carries executable component behavior.

Typical members include:

- component service packages;
- runtime images;
- service manifests;
- component-compatible configuration;
- service migrations;
- interface-compatible runtime assets.

Membership in the services channel does not transfer authority over another component's data or policy.

### 4.3 Governance channel

The governance channel carries versioned authority and enforcement artifacts.

Typical members include:

- authority records;
- canonical registries;
- schemas;
- accepted decisions;
- policies;
- component contracts;
- profile contracts;
- lifecycle contracts;
- compatibility contracts;
- conformance rules.

Governance artifacts participate directly in cross-channel compatibility because they can change which system, service, and knowledge artifacts are admitted or how those artifacts operate.

### 4.4 Knowledge channel

The knowledge channel carries versioned knowledge-bearing artifacts.

Typical members include:

- UCKK knowledge artifacts;
- knowledge packages;
- language packs;
- terminology assets;
- controlled content collections;
- runtime packs;
- distributable index inputs;
- other registered knowledge resources.

Regenerable caches remain outside release membership unless their artifact contracts classify them as distributable release artifacts.

### 4.5 Exclusive membership

Artifact membership is semantic and canonical.

A repository directory, package name, container image name, documentation heading, deployment unit, team ownership convention, or build job does not decide channel membership.

Moving an artifact class between channels changes:

- canonical ownership;
- versioning responsibility;
- compatibility relationships;
- Release Set assembly;
- signing scope;
- recovery behavior;
- traceability;
- conformance expectations.

Such a move requires an accepted owner decision and registry change.

## 5. Release Set and Compatibility Model

### 5.1 Release Set identity

A Release Set contains:

```text
release_set_id
semantic_version
lifecycle_status
created_at
system_channel_version
services_channel_version
governance_channel_version
knowledge_channel_version
compatibility_result
test_refs
evidence_refs
signature
```

The canonical schema represents the four channel selections as exactly four channel-version entries.

The Release Set lifecycle is:

```text
candidate
validated
active
superseded
revoked
archived
```

### 5.2 Compatibility

Compatibility is explicit and can be directional.

Examples include:

- a services version requires a minimum governance version;
- a knowledge runtime pack requires a minimum services runtime;
- a governance version prohibits a revoked system artifact;
- a system version supports only a bounded service interface range;
- a profile permits a Release Set only when all selected artifacts fit its resource and security envelope.

A compatibility record identifies:

- source channel and artifact class;
- source version selector;
- target channel and artifact class;
- target version selector;
- applicable profiles;
- enforcement points;
- tests;
- evidence;
- failure result.

Compatibility is evaluated at every declared enforcement point:

```text
publication
release_set_assembly
activation
rollback
forward_repair
```

Initial publication success does not eliminate later revalidation because trust, revocation, profile, evidence, or target state can change.

### 5.3 Independent update procedure

When one channel changes:

1. publish an immutable candidate version of that channel;
2. evaluate its channel-local checks;
3. resolve compatible versions of the other three channels;
4. assemble a new candidate Release Set;
5. run cross-channel and profile compatibility checks;
6. execute required release tests;
7. bind current evidence;
8. sign the complete Release Set;
9. pass release gates;
10. distribute and activate through the ordinary lifecycle.

The unchanged channels keep their versions.

The Release Set identity changes because the complete selected combination changed.

### 5.4 Signing

The Release Set signature binds:

- Release Set identity and version;
- all four channel identities and versions;
- channel manifests;
- applicable artifact-integrity references;
- compatibility result;
- tests;
- evidence;
- signing identity;
- signing time.

Signing authority remains separate from build, publication, approval, distribution, and activation authority.

### 5.5 Functional integrity

Release artifacts, signed manifests, Release Sets, offline bundles, archives, provenance records, source freezes, and cutover manifests use integrity metadata when their artifact contracts require it.

Ordinary Markdown documentation does not receive a general file-content-hash requirement.

## 6. Publication, Activation, and Recovery

### 6.1 Publication

Channel publication establishes an immutable channel version and manifest.

Publication does not make that version active on any node.

A published version can participate in zero, one, or multiple compatible Release Sets.

### 6.2 Distribution

Distribution transports a validated Release Set and its artifacts.

Distribution can be:

- connected;
- repository-based;
- federation-based;
- destination-bound export;
- signed offline bundle;
- controlled removable-media transfer.

Possession or download does not establish activation authority.

### 6.3 Staging

Staging verifies the candidate against the target:

- target profile;
- expected active Release Set;
- manifests;
- signatures;
- trust and revocation;
- functional integrity;
- resource admission;
- migration readiness;
- rollback or forward-repair material;
- recovery environment;
- receipt durability.

Staging is not activation.

### 6.4 Atomic activation

Activation changes one complete authoritative combination.

Dependent artifacts, services, policies, contracts, migrations, and knowledge objects are prepared and verified before the active authority reference changes.

The authority index or equivalent active pointer changes last.

Activation completion requires:

- the complete Release Set committed;
- actual post-activation state verified;
- critical receipts durable;
- post-activation checks started or completed according to policy.

A service restart, artifact copy, manifest verification, image pull, or partial channel switch does not constitute complete activation.

### 6.5 Rollback

Rollback selects a complete prior compatible Release Set.

It does not independently revert one channel into a combination that lacks compatibility evidence.

Rollback uses the same identity, authorization, expected-state, signature, compatibility, migration, audit, and recovery controls as activation.

### 6.6 Forward repair

When rollback is unsafe or impossible, forward repair produces a new immutable complete Release Set.

The repair preserves evidence linking:

- failed Release Set;
- failure;
- repair decision;
- changed channel versions;
- tests;
- evidence;
- activation result.

The failed Release Set is not edited in place.

### 6.7 Revocation

Revocation can prohibit:

- publication;
- assembly into new Release Sets;
- activation;
- continued operation;
- rollback;
- recovery use.

The revocation record identifies affected channel versions and Release Sets, trust state, reason, required replacement or recovery path, and operator action.

### 6.8 Offline operation

Offline distribution preserves:

- complete Release Set identity;
- all four channel manifests;
- signatures;
- artifact-integrity records;
- compatibility evidence;
- profile constraints;
- replay and downgrade protection;
- rollback or repair material.

A sovereign-offline node validates and activates locally using the same authority and compatibility model.

## 7. Consequences

### 7.1 Positive consequences

The decision provides:

- independent evolution of system, services, governance, and knowledge;
- smaller semantic version changes;
- clearer ownership;
- explicit artifact membership;
- profile-specific compatibility;
- complete activation identity;
- reproducible historical state;
- atomic rollback;
- signed offline distribution;
- reduced temptation to combine arbitrary latest versions;
- direct traceability from active deployment to four channel manifests;
- separation of build, approval, signing, distribution, and activation authority.

A knowledge update can occur without renumbering the system channel.

A service patch can occur without pretending governance changed.

A governance correction can be released without rebuilding unchanged system artifacts.

### 7.2 Costs and complexity

The decision introduces:

- a compatibility graph;
- Release Set assembly;
- four channel manifests;
- cross-channel tests;
- profile-specific compatibility checks;
- a complete signing operation;
- additional release and recovery evidence;
- Release Set identity changes for single-channel updates;
- more explicit rollback planning.

These costs are intentional. They expose compatibility and authority that a monolithic version or package-by-package deployment would otherwise hide.

### 7.3 Operational implications

Operators reason about one active Release Set, not four independent active channels.

Operational interfaces display:

- Release Set identity;
- all four channel versions;
- compatibility status;
- signature state;
- lifecycle state;
- rollback target;
- activation receipt.

Channel details remain available for diagnosis and release planning.

### 7.4 Development implications

Development workspaces can produce candidate artifacts and candidate channel versions according to profile authority.

They do not gain production publication, signing, or activation authority from successful builds.

Candidate artifacts preserve provenance so build-farm and release workflows can assemble and validate the production Release Set.

### 7.5 Conformance implications

Profile, deployment, operational, recovery, and release claims identify:

- the Release Set;
- all four channel versions;
- applicable profiles and overlays;
- tests;
- evidence;
- exceptions;
- validity.

A claim against an unregistered version mixture is invalid.

## 8. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Compatibility metadata becomes incomplete | Closed compatibility contracts, release gates, tests, evidence, and blocked indeterminate results |
| Teams treat channel independence as activation independence | Release Set-only approval, signing, distribution, activation, rollback, and conformance |
| Operators select newest versions automatically | Explicit compatibility selection and signed Release Set manifests |
| Governance changes unexpectedly affect runtime | Directional cross-channel constraints and profile tests |
| Knowledge artifacts drift from runtime support | Knowledge-to-services and knowledge-to-governance compatibility constraints |
| System rollback breaks newer data or governance | Complete prior Release Set selection plus migration and recovery checks |
| Four manifests create operational confusion | One top-level Release Set identity with four visible channel selections |
| Offline nodes receive incomplete updates | Signed complete offline bundles with target-profile and rollback material |
| A revoked artifact remains in a valid-looking set | Revocation revalidation at staging, activation, rollback, and recovery |
| Evidence is reused across a changed set | Release Set-bound tests and evidence with validated equivalence rules |
| A single-channel correction creates excessive rebuild work | Unchanged channels retain versions; only the Release Set assembly and affected checks change |
| A future fifth category appears | Require a new accepted owner decision and canonical registry change rather than informal channel creation |

## 9. Alternatives Considered

### 9.1 One monolithic release version

**Rejected.**

A single version simplifies naming but creates false coupling.

It obscures which authority changed, forces unrelated version changes, enlarges rebuild and review scope, and makes knowledge or governance updates appear equivalent to system substrate changes.

It remains possible to present a Release Set version as the top-level operational identity without collapsing channel ownership.

### 9.2 Independently activatable packages

**Rejected.**

Package-level activation permits combinations without complete compatibility evidence.

It weakens rollback, historical interpretation, signing, profile claims, offline distribution, and atomic authority.

### 9.3 Three channels

**Rejected.**

Combining governance with services would allow executable packaging concerns to obscure authority and contract changes.

Combining knowledge with services would force knowledge and language evolution into service release cadence and weaken deterministic knowledge/runtime compatibility.

Combining system with services would recreate monolithic infrastructure and application coupling.

### 9.4 Five or more channels

**Rejected for the active baseline.**

Additional channels increase compatibility, signing, recovery, and operational complexity.

A new channel can be considered only when an artifact family has a distinct authority, lifecycle, compatibility pattern, and operational need that cannot be represented correctly in the four existing channels.

### 9.5 Environment-specific channels

**Rejected.**

Development, production, sovereign, offline, high-assurance, and appliance concerns belong to profiles and overlays.

Creating environment channels would mix deployment policy with artifact ownership.

### 9.6 Provider-specific channels

**Rejected.**

Provider packaging belongs to integration or distribution contracts.

A provider does not become a canonical release authority.

### 9.7 Governance as unversioned configuration

**Rejected.**

Governance artifacts affect authority, admission, compatibility, and conformance.

They require immutable version identity, tests, evidence, release compatibility, rollback or repair, and historical interpretation.

### 9.8 Knowledge outside release governance

**Rejected.**

Knowledge artifacts can affect deterministic runtime behavior, terminology, language, indexing, and user-visible outcomes.

Distributable knowledge therefore requires version identity, compatibility, provenance, and recovery.

## 10. Conformance and Reconsideration

### 10.1 Conformance conditions

This decision is correctly implemented when:

1. exactly four active channel identities exist;
2. each active artifact class belongs to one channel;
3. each channel has one owner;
4. published channel versions are immutable;
5. a single-channel update can retain unchanged versions of the other channels;
6. every candidate and active Release Set contains exactly one version from each channel;
7. compatibility is explicit, directional where needed, and enforced at declared lifecycle points;
8. channel-local success cannot replace Release Set compatibility;
9. Release Set signatures bind all four versions and their manifests;
10. release tests and evidence bind to the complete selected combination;
11. activation changes the complete set atomically;
12. dependent state is prepared before authority changes;
13. the active authority pointer changes last;
14. rollback uses a complete prior compatible Release Set;
15. forward repair creates a new Release Set;
16. revocation affects applicable channel versions and Release Sets;
17. offline bundles contain the complete set and recovery material;
18. profile and operational claims identify the Release Set and four versions;
19. development profiles remain candidate-only unless separately authorized;
20. ordinary Markdown hashes remain outside release integrity requirements;
21. all decisions, channels, artifact classes, profiles, components, tests, evidence, receipts, and exceptions resolve;
22. no prohibited open-state marker enters active authority.

The principal validation entry point is:

```bash
uv run python docs/tools/validate_docs.py
```

Supporting checks include:

```text
docs/tools/check_release_sets.py
docs/tools/check_artifact_contracts.py
docs/tools/check_profile_inheritance.py
docs/tools/check_component_boundaries.py
docs/tools/check_interfile_locks.py
docs/tools/check_traceability.py
docs/tools/check_decision_closure.py
docs/tools/check_no_unresolved_state.py
```

### 10.2 Reconsideration triggers

This ADR can be reconsidered when:

- an artifact family cannot be assigned correctly to any existing channel;
- compatibility complexity becomes unmanageable despite closed contracts and tooling;
- an accepted system decision changes the unit of atomic authority;
- recovery evidence shows the Release Set is not a safe activation unit;
- a new distribution model requires a different signed compatibility boundary;
- governance or knowledge artifacts no longer affect executable or authoritative behavior;
- profile composition requires a release abstraction not representable by Release Sets.

Reconsideration requires a new accepted ADR and canonical registry changes.

Existing release history remains interpretable under this decision.

## 11. Non-Normative Examples

### 11.1 Services-only change

Services advances from 2.3.1 to 2.3.2.

System 1.4.0, governance 3.2.0, and knowledge 5.1.0 remain unchanged.

A new Release Set is assembled and signed with:

```text
system 1.4.0
services 2.3.2
governance 3.2.0
knowledge 5.1.0
```

### 11.2 Governance compatibility floor

Services 2.4.0 requires governance 3.3.0 or newer.

A Release Set containing services 2.4.0 and governance 3.2.0 fails compatibility even when both channel versions pass their individual tests.

### 11.3 Knowledge update

A terminology and language-pack correction advances knowledge from 5.1.0 to 5.1.1.

No system or services artifact changes, but a new Release Set identity records the new authoritative combination.

### 11.4 Revoked system artifact

A system artifact is revoked for a trust failure.

Every Release Set containing that system version becomes ineligible according to the revocation policy, including otherwise unchanged service, governance, and knowledge versions.

### 11.5 Rollback

A services migration causes a critical failure.

The node selects the prior complete compatible Release Set rather than changing only the services pointer.

### 11.6 Forward repair

A governance schema change cannot be reversed without unsafe data loss.

A corrected governance version and any required compatible services version are assembled into a new Release Set.

### 11.7 Offline update

A sovereign-offline node receives one signed bundle containing the Release Set manifest, all four channel manifests, required artifacts, compatibility evidence, anti-replay data, and rollback material.

### 11.8 Development candidate

A developer workspace builds a candidate services artifact.

The artifact has provenance and tests but does not become a published services channel version or active Release Set until the authorized release workflow accepts it.

### 11.9 Profile constraint

A Release Set passes global compatibility but exceeds the user-lightweight resource envelope.

It can remain valid for another profile while failing the user-lightweight profile gate.

### 11.10 Public release receipt

A public receipt identifies the Release Set and its four channel versions, approval state, activation state, and verification status.

Detailed protected gate evidence remains private.
