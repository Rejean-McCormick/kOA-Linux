<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-LIFE-005",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "lifecycle",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/release-channels.contract.json",
    "contracts/artifact-classes.contract.json"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-HW-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-IMG-001",
    "REQ-LIFE-IMG-002",
    "REQ-LIFE-IMG-003",
    "REQ-LIFE-IMG-004",
    "REQ-LIFE-IMG-005",
    "REQ-LIFE-IMG-006",
    "REQ-LIFE-IMG-007",
    "REQ-LIFE-IMG-008",
    "REQ-LIFE-IMG-009",
    "REQ-LIFE-IMG-010",
    "REQ-LIFE-IMG-011",
    "REQ-LIFE-IMG-012",
    "REQ-LIFE-IMG-013",
    "REQ-LIFE-IMG-014",
    "REQ-LIFE-IMG-015",
    "REQ-LIFE-IMG-016",
    "REQ-LIFE-IMG-017",
    "REQ-LIFE-IMG-018",
    "REQ-LIFE-IMG-019",
    "REQ-LIFE-IMG-020",
    "REQ-LIFE-IMG-021",
    "REQ-LIFE-IMG-022",
    "REQ-LIFE-IMG-023",
    "REQ-LIFE-IMG-024",
    "REQ-LIFE-IMG-025",
    "REQ-LIFE-IMG-026",
    "REQ-LIFE-IMG-027",
    "REQ-LIFE-IMG-028"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-000",
    "DOC-LIFE-000"
  ],
  "tags": [
    "lifecycle",
    "normative-markdown",
    "05",
    "system",
    "image",
    "updates"
  ]
}
KOA:DOC-META:END -->

# System Image Updates

## 1. Purpose

This document defines the lifecycle for updating the bootable system foundation of a kOA deployment through the `system` release channel.

A system image update can change the operating-system image, boot artifacts, recovery artifacts, host-platform packages, kernel, low-level runtime dependencies, or another artifact class assigned canonically to the system channel. Because these artifacts establish the environment in which all other channels execute, their activation requires a complete compatibility decision rather than a package-by-package assumption.

The lifecycle provides verifiable candidate identity and provenance, profile-aware compatibility, inactive staging, atomic boot-target selection, preservation of a last known good state, recovery after failed activation, offline import without weaker validation, and explicit coordination with services, governance, and knowledge releases.

This document defines global behavior. Each deployment profile owns the concrete image format, boot mechanism, storage layout, update transport, recovery interface, and host-specific implementation.

## 2. Scope

### 2.1 Included artifacts

This document applies to artifact classes assigned to the `system` channel, including:

- system images;
- boot artifacts;
- recovery artifacts;
- profile-declared host-platform bundles that participate in boot or recovery;
- system-channel metadata required to validate and activate those artifacts.

The canonical channel membership is owned by `contracts/release-channels.contract.json` and `contracts/artifact-classes.contract.json`.

### 2.2 Included profiles

The lifecycle applies to every profile that activates a system-channel release, including user endpoints, developer workstations, sovereign Linux nodes, sovereign hubs, build-farm nodes, control-plane nodes, and explicit profile-overlay compositions.

Implementation differs by profile. A sovereign Linux node can require an immutable signed image and measured activation, while a developer workstation can use a transactional image mechanism or another rollback-capable profile-approved method. A profile-specific mechanism does not become a global requirement.

### 2.3 Included operations

The lifecycle covers discovery, online download, offline import, verification, compatibility evaluation, staging, boot-target selection, activation, health observation, acceptance, rollback, forward repair, recovery-artifact replacement, candidate retirement, cleanup, and evidence production.

### 2.4 State boundaries

System update state remains separate from component-owned application data, services-channel packages, governance policy bundles, knowledge artifacts, user content, development workspaces, external integration output, caches, and reproducible derivatives.

A system update can include a declared migration for profile-owned host state. It does not gain authority to rewrite component-owned data directly.

### 2.5 Explicit non-goals

This document does not require one operating-system distribution, one image-building technology, A/B partitions, containers, Kubernetes, a permanent network connection, or one update interface. It does not treat successful download or successful boot as acceptance, permit partial authoritative activation, guarantee rollback after an irreversible migration, define application database migrations, or turn the recovery environment into a normal production runtime.

## 3. Canonical References

| Canonical reference | Responsibility in this document |
| --- | --- |
| `contracts/release-channels.contract.json` | Owns the `system` channel identity, membership, independence from the other channels, activation expectations, and complete Release Set rules. |
| `contracts/artifact-classes.contract.json` | Owns artifact-class definitions, required metadata, compatibility declarations, activation semantics, and rollback or forward-repair behavior. |

Supporting authority is owned by the decisions, authority, profile, requirements, locks, tests, evidence, exceptions, Release Set, system-image, boot-artifact, and recovery-artifact contracts.

This document explains lifecycle behavior. It does not become a second owner of channel membership, artifact structure, image format, bootloader configuration, or profile-specific storage layout.

## 4. Model and Responsibilities

### 4.1 Release identities

A deployment distinguishes the active and candidate system-channel releases, the active releases from the services, governance, and knowledge channels, and the signed Release Set that binds exactly one tested-compatible release from each canonical channel.

A candidate system release becomes eligible for activation only through a complete candidate Release Set. An independent system-channel update therefore produces a replacement Release Set after every declared cross-channel constraint and applicable test passes.

### 4.2 Update objects

| Object | Responsibility |
| --- | --- |
| System release manifest | Identifies the candidate release and constituent artifacts. |
| System image | Provides the bootable operating-system and host-platform foundation. |
| Boot artifact | Provides bootloader, kernel, initialization, or equivalent boot-stage material. |
| Recovery artifact | Provides an independently invokable supported recovery path. |
| Compatibility declaration | States supported profiles, hardware, boot mechanisms, channel releases, schemas, and migrations. |
| Release Set | Binds tested-compatible versions from all four channels. |
| Activation record | Records staging, boot selection, attempts, results, and recovery action. |
| Health verdict | Records whether the candidate met its declared post-boot criteria. |

### 4.3 Retained system states

A deployment preserves distinguishable states:

- `active`: the accepted system release;
- `candidate`: a verified and staged release not yet accepted;
- `previous_good`: the most recent accepted release retained for rollback;
- `recovery`: an independently invokable recovery environment;
- `failed_candidate`: a candidate that failed activation or health;
- `retired`: an inactive release no longer eligible for activation.

The physical layout can be dual-slot, snapshot-based, transactional, image-store-based, or another profile-approved design. The required outcome is inactive staging without partial mutation of the active system.

### 4.4 Responsibilities

The release producer creates artifacts, declares compatibility, supplies provenance and evidence, and defines rollback or forward repair. The release authority accepts the system release and replacement Release Set. The update agent verifies, stages, selects, records, and invokes recovery but does not grant release authority. The boot environment selects only an explicitly staged target. The health evaluator checks declared boot, storage, identity, services, governance, data-mount, network, and recovery criteria. The operator initiates and observes lifecycle actions within policy but cannot authorize an invalid candidate through administrative access alone.

### 4.5 Compatibility model

Compatibility can reference profile and overlay identity, processor architecture, hardware and firmware class, boot mechanism, storage layout, required drivers, recovery compatibility, supported services and governance releases, knowledge-runtime constraints, schemas, migrations, active exceptions, prohibited prior versions, and required update sequence.

An undeclared compatibility assumption does not become permission to activate.

### 4.6 Host-owned and component-owned state

The system image manages only profile-declared host state such as boot state, system configuration, host service definitions, trust references, update-agent state, and recovery configuration.

Component databases, repositories, queues, objects, user content, and business records remain outside direct system-image mutation. Any host-state migration uses an explicit migration contract and preserves a declared rollback or forward-repair path.

### 4.7 Transport and trust

Candidates can arrive from an approved online repository, sovereign hub, local artifact registry, removable media, verified offline bundle, or another registered system-channel integration.

Transport does not establish trust. Every source follows the same artifact identity, authority, provenance, compatibility, Release Set, staging, health, and recovery validation.

### 4.8 Activation and acceptance

Activation and acceptance are separate. A candidate can boot and remain under observation without becoming accepted. Acceptance occurs only after declared health criteria pass. The former active release becomes `previous_good` or is retained according to profile policy.

## 5. Applicable Normative Requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-LIFE-IMG-001,REQ-LIFE-IMG-002,REQ-LIFE-IMG-003,REQ-LIFE-IMG-004,REQ-LIFE-IMG-005,REQ-LIFE-IMG-006,REQ-LIFE-IMG-007,REQ-LIFE-IMG-008,REQ-LIFE-IMG-009,REQ-LIFE-IMG-010,REQ-LIFE-IMG-011,REQ-LIFE-IMG-012,REQ-LIFE-IMG-013,REQ-LIFE-IMG-014,REQ-LIFE-IMG-015,REQ-LIFE-IMG-016,REQ-LIFE-IMG-017,REQ-LIFE-IMG-018,REQ-LIFE-IMG-019,REQ-LIFE-IMG-020,REQ-LIFE-IMG-021,REQ-LIFE-IMG-022,REQ-LIFE-IMG-023,REQ-LIFE-IMG-024,REQ-LIFE-IMG-025,REQ-LIFE-IMG-026,REQ-LIFE-IMG-027,REQ-LIFE-IMG-028 -->
- **REQ-LIFE-IMG-001 — SHALL:** Every system image update identify the system-channel release, constituent artifacts, supported profiles, compatibility declarations, provenance, activation procedure, and rollback or forward-repair behavior.
- **REQ-LIFE-IMG-002 — SHALL:** A candidate system release participate in a complete signed Release Set containing exactly one tested-compatible release from each canonical release channel.
- **REQ-LIFE-IMG-003 — SHALL NOT:** Download, import, staging, successful boot, or operator possession alone authorize system image activation.
- **REQ-LIFE-IMG-004 — SHALL:** Candidate verification validate release authority, artifact identity, provenance, revocation state, profile compatibility, hardware compatibility, boot compatibility, and required evidence.
- **REQ-LIFE-IMG-005 — SHALL:** Candidate staging preserve the currently active system release as a complete bootable or otherwise recoverable state.
- **REQ-LIFE-IMG-006 — SHALL NOT:** Staging create a partially candidate active system or overwrite the only known-good recovery path.
- **REQ-LIFE-IMG-007 — SHALL:** Boot-target selection be explicit, durable, attributable, and reversible until the candidate is accepted or forward repair is declared.
- **REQ-LIFE-IMG-008 — SHALL:** Activation be atomic at the system-image boundary defined by the active profile.
- **REQ-LIFE-IMG-009 — SHALL:** Activation and acceptance remain separate lifecycle decisions.
- **REQ-LIFE-IMG-010 — SHALL:** A candidate pass profile-declared post-boot health criteria before acceptance.
- **REQ-LIFE-IMG-011 — SHALL:** A failed activation preserve or restore access to the previous good release or the independent recovery environment.
- **REQ-LIFE-IMG-012 — SHALL:** Every system artifact class define rollback or forward-repair behavior.
- **REQ-LIFE-IMG-013 — SHALL NOT:** Rollback reactivate a system release incompatible with an irreversible host-state migration.
- **REQ-LIFE-IMG-014 — SHALL:** Forward repair be used only when declared compatibility or migration evidence establishes that rollback is unsafe or impossible.
- **REQ-LIFE-IMG-015 — SHALL:** System image updates preserve component-owned authoritative data and interact with that data only through declared migration or compatibility contracts.
- **REQ-LIFE-IMG-016 — SHALL NOT:** A system image update write directly into component-owned application databases, repositories, queues, object stores, or business records.
- **REQ-LIFE-IMG-017 — SHALL:** Offline and removable-media updates use the same authority, identity, compatibility, Release Set, staging, health, and recovery validation as online updates.
- **REQ-LIFE-IMG-018 — SHALL NOT:** Restoration of connectivity automatically activate a downloaded, imported, staged, queued, or previously blocked system release.
- **REQ-LIFE-IMG-019 — SHALL:** The update mechanism record discovery, verification, staging, selection, boot attempt, health verdict, acceptance, rollback, repair, and retirement state.
- **REQ-LIFE-IMG-020 — SHALL:** Update evidence identify the active and candidate system releases, active Release Set, profile, result, and recovery target without exposing unnecessary secrets or protected user data.
- **REQ-LIFE-IMG-021 — SHALL:** Recovery artifacts remain independently invokable and compatible with the active profile and retained system states.
- **REQ-LIFE-IMG-022 — SHALL NOT:** Recovery artifacts be replaced or retired until their replacement passes recovery validation.
- **REQ-LIFE-IMG-023 — SHALL:** Resource pressure, power loss, process termination, or interrupted transfer leave the active system and update state in a defined recoverable condition.
- **REQ-LIFE-IMG-024 — SHALL:** Update cleanup preserve the active release, previous good release, required recovery artifacts, activation evidence, and state required for declared forward repair.
- **REQ-LIFE-IMG-025 — SHALL NOT:** A profile-specific image mechanism, container runtime, Kubernetes deployment, recipe, generated context, or implementation convenience become a global system-image requirement.
- **REQ-LIFE-IMG-026 — SHALL:** An independent system-channel update reevaluate every declared cross-channel compatibility constraint and issue a replacement Release Set before activation.
- **REQ-LIFE-IMG-027 — SHALL:** System image update conformance include interrupted-update, failed-boot, failed-health, rollback, recovery, offline-import, incompatible-Release-Set, and host-state-migration tests.
- **REQ-LIFE-IMG-028 — SHALL NOT:** An exception, emergency action, migration record, or administrative override silently bypass release authority, compatibility, evidence, or recovery requirements.
<!-- GENERATED:REQUIREMENTS:END -->

## 6. Procedures or State Transitions

### 6.1 Candidate discovery and verification

1. Resolve the active profile, overlays, system release, and Release Set.
2. Discover or import the candidate without executing candidate code.
3. Confirm that all candidate artifact classes belong to the system channel.
4. Validate the release manifest and every constituent artifact contract.
5. Validate artifact identity, provenance, release authority, and revocation state.
6. Validate profile, hardware, firmware, architecture, boot, storage, and recovery compatibility.
7. Validate services, governance, knowledge, schema, migration, and exception constraints.
8. Execute applicable compatibility tests.
9. Validate a complete replacement Release Set.
10. Record `verified`, `blocked`, or `denied` without changing the active target.

### 6.2 Inactive staging

1. Reserve a profile-approved inactive target.
2. Confirm that the active, previous-good, and recovery targets remain intact.
3. Transfer or materialize the candidate into inactive storage.
4. Apply only declared host-state preparation.
5. Create candidate boot configuration without accepting the candidate.
6. Run static and pre-boot validation.
7. Record target location and candidate identity.
8. Mark the candidate staged only after validation completes.

An interruption leaves the candidate incomplete and ineligible for boot selection.

### 6.3 Pre-activation checkpoint

1. Recheck trust, revocation, compatibility, Release Set, and evidence.
2. Confirm required backups or host-state checkpoints.
3. Confirm previous-good and recovery targets.
4. Confirm power, storage reserve, update-agent health, and maintenance policy.
5. Record health criteria, observation window, rollback target, and repair path.
6. Select the candidate as the next boot target.
7. Record selection durably.

### 6.4 Activation progression

```text
discovered
  -> verified
  -> staged
  -> selected
  -> booting
  -> observing
  -> accepted
```

Alternative states are:

```text
blocked
denied
failed_boot
failed_health
rollback_required
rolled_back
forward_repair_required
recovered
retired
```

During activation, the deployment confirms the expected system release and Release Set, validates storage and profile-owned host state, starts profile-required constitutional services, starts compatible component services, evaluates health, and preserves failure evidence. Acceptance occurs only after all required checks pass.

### 6.5 Rollback

1. Stop candidate progression safely where possible.
2. Confirm rollback compatibility with current host-owned state.
3. Select the previous-good system target.
4. Restore the corresponding or another declared compatible Release Set.
5. Boot the previous-good target.
6. Validate essential health and component-data accessibility.
7. Mark the candidate failed and inactive.
8. Preserve activation and failure evidence.
9. Prevent automatic candidate retry.

### 6.6 Forward repair

1. Record why rollback is unsafe or impossible.
2. Enter the narrowest safe recovery mode.
3. Preserve evidence and recovery access.
4. Select a declared repair artifact or replacement release.
5. Validate the repair against current host-owned state.
6. Validate a complete compatible Release Set.
7. Stage and activate the repair through the normal boundary where possible.
8. Verify restored health and record remaining limitations.

### 6.7 Offline update

1. Receive the bundle through an approved local or physical path.
2. Inspect its manifest before importing executable material.
3. Validate available authority, provenance, trust, and revocation information.
4. Block the candidate when required current authority cannot be established.
5. Import into quarantine or inactive storage.
6. Execute normal compatibility and Release Set validation.
7. Stage and activate through the standard lifecycle.
8. Record the offline source and validation basis.

### 6.8 Retention and cleanup

After acceptance, preserve the active release, the profile-required previous-good release, validated recovery artifacts, and required lifecycle evidence. Retire failed or superseded candidates, remove incomplete staging data, reclaim transfer caches, and verify that cleanup did not remove a required recovery path.

## 7. Failure States and Safe Degradation

| Failure condition | Required behavior | Preserved capability | Denied capability |
| --- | --- | --- | --- |
| Invalid candidate manifest | Reject before staging. | Active system | Candidate use |
| Invalid or revoked release authority | Block candidate. | Active system and recovery | Candidate activation |
| Invalid artifact identity or provenance | Quarantine or reject. | Active release | Staging and activation |
| Profile, hardware, or boot incompatibility | Block before boot selection. | Current boot path | Candidate boot |
| Incomplete Release Set | Block activation. | Current complete Release Set | Candidate activation |
| Failed cross-channel constraint | Retain active Release Set. | Existing deployment | Independent update |
| Interrupted transfer | Resume safely or discard incomplete data. | Active and recovery targets | Incomplete candidate use |
| Interrupted staging | Keep candidate inactive. | Active and recovery targets | Candidate selection |
| Insufficient storage reserve | Stop staging and expose cleanup. | Current system | New staging |
| Power loss before selection | Resume from recorded state. | Current boot target | Unverified transition |
| Candidate fails to boot | Select previous-good or recovery target. | Recovery and rollback | Acceptance |
| Candidate boots with wrong identity | Treat as activation failure. | Recovery path | Acceptance |
| Required storage unavailable | Enter recovery or rollback. | Recovery tools | Normal acceptance |
| Governance runtime incompatible | Fail health and recover. | Evidence and rollback | Governed operation |
| Required service incompatible | Fail candidate health. | Previous-good or safe mode | Acceptance |
| Health observation fails | Keep candidate unaccepted and recover. | Evidence and recovery target | Acceptance |
| Previous-good target unusable | Use recovery and forward repair. | Recovery environment | Normal rollback |
| Recovery artifact invalid | Block activation. | Current active system | Update activation |
| Rollback incompatible with migration | Enter forward repair. | Recovery and bounded safe mode | Unsafe rollback |
| Update agent failure | Keep active boot state unchanged where possible. | Current system and manual recovery | Automated progression |
| Time or trust uncertain | Block sensitive activation. | Active state | Candidate activation |
| Offline authority insufficient | Keep candidate quarantined or blocked. | Current offline operation | Activation |
| Candidate revoked after staging | Clear selection and quarantine or retire it. | Active system | Candidate boot |
| Cleanup failure | Preserve required targets and record incomplete cleanup. | Active, previous-good, recovery | Retirement completion |

Safe degradation preserves an accepted system and a recovery route. It does not boot an unverified candidate, omit channels, bypass compatibility, mutate component data directly, or report an unaccepted candidate as active.

## 8. Cross-Component Interactions

### 8.1 Release channels

The system channel versions independently, but activation uses a complete Release Set. A successful independent system update produces a new Release Set binding the candidate system release to compatible services, governance, and knowledge releases.

### 8.2 Profile contracts

Profiles select image format, boot mechanism, staging layout, retention count, transport, recovery method, health criteria, operator interaction, and host-state migration controls. They cannot redefine channel identity or weaken Release Set completeness.

### 8.3 Update agent and Node Agent

A profile can assign execution to kOA Node Agent or another dedicated update agent. The agent performs allowlisted lifecycle operations and records state. It does not become release authority or write component-owned application data directly.

### 8.4 Resource Governor

Resource Governor reserves bounded capacity for verification, staging, activation, and recovery. Resource availability can defer work but cannot authorize a candidate.

### 8.5 Governance Policy Runtime

Where profile policy requires a governed maintenance decision, Governance Policy Runtime evaluates the request. It does not perform boot selection or resource allocation. Its compatibility participates in Release Set and health validation.

### 8.6 Identity, Trust, Audit, and Evidence

Identity and Trust validates release and operator authority. Audit Broker or profile-approved evidence tooling records selective lifecycle evidence. Evidence identifies releases, profile, Release Set, result, and recovery target without collecting component database content or user content.

### 8.7 Component services and data

Services quiesce, migrate, restart, and report health through declared contracts. System rollback does not substitute for component-data backup or restore, and the image update does not silently reinterpret application schemas.

### 8.8 Recovery and external sources

Recovery artifacts provide independent inspection and repair. Online repositories, hubs, mirrors, and removable media transport candidates but do not gain activation authority.

## 9. Decision Closure and Prohibited Assumptions

The accepted decisions referenced in the metadata close the global model.

The following assumptions are prohibited:

1. Every profile uses the same image format.
2. Every profile requires an immutable image.
3. Every profile uses A/B partitions.
4. Containers constitute a system image.
5. Kubernetes is required for activation.
6. Successful download proves validity.
7. Valid artifact identity proves deployment authorization.
8. Successful boot proves acceptance.
9. The system channel can activate without a complete Release Set.
10. Other channel releases can be inferred compatible.
11. Staging can overwrite the only active system state.
12. Recovery media can be replaced before validation.
13. Rollback is always safe after migration.
14. Forward repair can be selected for convenience.
15. A system update owns component data.
16. Host administration is release authority.
17. Offline bundles need weaker validation.
18. Reconnection authorizes activation.
19. Failed candidates can retry without revalidation.
20. A package-manager transaction alone proves atomic image activation.
21. A snapshot alone proves recovery readiness.
22. The previous-good image can be deleted after first boot.
23. Process startup alone proves health.
24. A recipe replaces the profile contract.
25. A profile-specific mechanism becomes global.
26. An emergency silently omits evidence or recovery planning.
27. Operating-system rollback restores component data.
28. A recovery environment becomes an undeclared production profile.

When release authority, artifact identity, profile compatibility, Release Set compatibility, recovery readiness, migration safety, or health criteria are unresolved, the candidate remains inactive.

## 10. Validation Criteria

This document is conformant when:

1. It is registered as `DOC-LIFE-005` at `06-lifecycle/05-system-image-updates.md`.
2. Its class, status, language, layer, scope, canonical references, dependencies, and tags match the documentation registry.
3. Every listed decision, requirement, and lock resolves and is active where required.
4. The eleven mandatory sections exist in order.
5. Normative keywords occur only inside the generated requirement block.
6. System-image, boot-artifact, and recovery-artifact classes belong only to the system channel.
7. Every candidate references a complete signed Release Set with exactly one tested-compatible release from each channel.
8. Candidate verification covers authority, identity, provenance, revocation, profile, hardware, boot, recovery, and compatibility.
9. Staging leaves active and recovery targets intact.
10. Activation is atomic at the profile-defined image boundary.
11. Activation and acceptance remain distinct.
12. Failed boot and failed health reach rollback, recovery, or declared forward repair.
13. The previous-good target remains usable until retention policy permits retirement.
14. Recovery artifacts pass independent invocation and compatibility tests.
15. Offline import produces the same validation outcome as equivalent online delivery.
16. Interrupted transfer, staging, selection, and activation leave a defined recoverable state.
17. Component-owned data remains unchanged except through declared migration contracts.
18. Incompatible rollback enters forward repair.
19. Reconnection does not activate a queued or staged candidate automatically.
20. Evidence identifies candidate, active release, Release Set, profile, result, and recovery target.
21. Cleanup preserves required active, prior-good, recovery, and evidence objects.
22. Profile-specific mechanisms remain profile-scoped.
23. Traceability and active evidence are complete.
24. No unresolved marker, provisional value, parallel authority, or ordinary Markdown file-identity field appears.
25. Complete documentation validation returns `pass`.

## 11. Non-Normative Examples

### 11.1 Transactional user endpoint

A user endpoint downloads a candidate while running the current image. The candidate is verified and staged in an inactive deployment. The endpoint restarts into it and accepts it only after storage, local interfaces, profile-required services, governance-dependent functions, and recovery access pass.

### 11.2 Sovereign node offline update

A sovereign node receives a release through removable media. It validates the offline bundle, profile compatibility, release authority, recovery artifact, and complete Release Set without requiring an Internet connection.

### 11.3 Failed candidate boot

A candidate kernel cannot initialize required storage. The boot environment selects the previous-good target. The failed candidate remains inactive and its activation record is retained.

### 11.4 Failed post-boot health

A candidate boots, but Governance Policy Runtime is incompatible with the selected services release. Health validation fails and the deployment returns to the previous compatible Release Set.

### 11.5 Independent system update

The system channel releases a security update while other channel versions remain unchanged. Compatibility tests pass, and a new Release Set binds the candidate system release to the existing services, governance, and knowledge releases.

### 11.6 Interrupted staging

Power is lost while materializing the inactive candidate. The current boot target remains unchanged. On restart, the incomplete candidate is resumed or discarded according to profile policy and is not treated as staged prematurely.

### 11.7 Forward repair

A candidate performs a declared irreversible migration of profile-owned boot metadata. A later failure makes the previous image incompatible. The deployment enters recovery and applies a validated repair release rather than booting unsafe prior state.

### 11.8 Developer workstation

A developer workstation uses a transactional update mechanism rather than an appliance image. It still preserves inactive staging, previous-good state, Release Set compatibility, health validation, and rollback behavior.

### 11.9 Recovery-artifact replacement

A release includes a new recovery artifact. The old recovery environment remains until the replacement boots independently and can inspect and recover the active and previous-good targets.

### 11.10 Reconnection

A candidate was staged before connectivity loss. When connectivity returns, trust and Release Set state are revalidated and the required operator or maintenance-policy decision is obtained before boot selection.
