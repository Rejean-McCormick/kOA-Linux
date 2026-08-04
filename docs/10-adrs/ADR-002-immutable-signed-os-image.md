<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-002",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "sovereign_linux_node"
  ],
  "canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-002",
    "generated/decision-index.json#/decisions/DEC-PROFILE-001",
    "contracts/profiles/sovereign-linux-node.profile.json#/operating_system/immutable_signed_image",
    "contracts/system.contract.json#/release_and_artifact_identity",
    "contracts/system.contract.json#/critical_transitions",
    "contracts/artifact-classes.contract.json#/artifact_classes/system_image",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/profiles/build-farm.profile.json",
    "generated/profile-catalog.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/traceability.json"
  ],
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-HW-001",
    "DEC-DATA-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-AI-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-CAD-008",
    "REQ-LIFE-CAD-010",
    "REQ-LIFE-CAD-011",
    "REQ-LIFE-CAD-014",
    "REQ-LIFE-CAD-023",
    "REQ-LIFE-CAD-024",
    "REQ-SEC-DAR-005",
    "REQ-SEC-DAR-014",
    "REQ-SEC-DAR-015",
    "REQ-SEC-DAR-016",
    "REQ-SEC-DAR-017",
    "REQ-SEC-DAR-018",
    "REQ-SEC-DAR-021",
    "REQ-SEC-DAR-024",
    "REQ-OPS-DEG-008",
    "REQ-OPS-DEG-009",
    "REQ-OPS-DEG-010",
    "REQ-OPS-DEG-016",
    "REQ-OPS-DEG-017",
    "REQ-OPS-DEG-018",
    "REQ-OPS-DEG-020",
    "REQ-OPS-DEG-021",
    "REQ-OPS-DEG-022",
    "REQ-OPS-DEG-024"
  ],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-GOV-005",
    "DOC-GOV-006",
    "DOC-GOV-009",
    "DOC-GOV-010",
    "DOC-GOV-011",
    "DOC-GOV-012",
    "DOC-GOV-013",
    "DOC-GOV-014",
    "DOC-GOV-016",
    "DOC-CONST-003",
    "DOC-SYS-000",
    "DOC-SYS-018",
    "DOC-PROFILE-001",
    "DOC-PROFILE-003",
    "DOC-PROFILE-007",
    "DOC-DEV-014",
    "DOC-LIFE-017",
    "DOC-SEC-010",
    "DOC-OPS-007",
    "DOC-OPS-018",
    "DOC-CONF-012",
    "DOC-CONF-016",
    "DOC-CONF-019"
  ],
  "tags": [
    "architecture-decision",
    "sovereign-linux-node",
    "immutable-os",
    "signed-system-image",
    "atomic-activation",
    "rollback",
    "system-release-channel",
    "supply-chain",
    "offline-update",
    "profile-scoped"
  ]
}
KOA:DOC-META:END -->

# ADR-002 — Immutable Signed OS Image

**ADR ID:** `ADR-002`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `profile_authority`  
**Owner decision:** `DEC-PROFILE-001`  
**Change packet:** `CHG-2026-0002`  
**Created:** `2026-08-03`  
**Accepted:** `2026-08-03`  
**Effective:** `2026-08-03`  
**Supersedes:** Not applicable.  
**Superseded by:** Not applicable.

## 1. Decision Summary

The `sovereign_linux_node` profile uses a complete immutable, integrity-protected, signed operating-system image delivered through the `system` release channel. The target stages the complete image outside the active deployment, verifies identity, provenance, signatures, trust, profile compatibility, resource capacity, boot compatibility, and recovery readiness, then changes the boot target atomically. In-place package mutation of the active system root is excluded. Mutable component data, databases, secrets, queues, logs, caches, configuration state, and recovery records remain outside the image under their owning contracts.

## 2. Scope

### 2.1 Included scope

- Profile scope: `sovereign_linux_node`.
- System-channel operating-system image construction, signing, distribution, staging, activation, boot verification, commitment, rollback, recovery, deprecation, and retirement.
- Kernel, initramfs, base userspace, profile-approved host agents, boot metadata, and system-level dependencies included by the system-image manifest.
- Target-local activation through the kOA Node Agent or equivalent closed profile-authorized lifecycle component.
- Online and signed offline transfer.
- Build-farm provenance and release-signing separation.
- Compatibility with services, governance, and knowledge channels.
- High-assurance and sovereign-offline overlays only when they explicitly compose with the primary profile.

### 2.2 Excluded scope

- `user_lightweight`, developer Linux, developer WSL, build-farm, control-plane, and sovereign-hub requirements unless their own profile contracts adopt this mechanism explicitly.
- Mutable application data, component databases, user content, secrets, credentials, logs, queues, indexes, caches, backup repositories, and runtime state.
- Services, governance policy bundles, and knowledge artifacts that have independent release-channel identities.
- Firmware and device updates except where a separate signed artifact contract binds them to a compatible Release Set.
- A particular distribution, image builder, bootloader, filesystem, bootc, OSTree, rpm-ostree, container runtime, or orchestration platform.
- Appliance-shell user-interface choices.
- Native or external AI capability.

### 2.3 Activation boundary

This ADR becomes applicable when a node-profile artifact selects `sovereign_linux_node` and resolves `contracts/profiles/sovereign-linux-node.profile.json#/operating_system/immutable_signed_image` as required. The profile contract, system-image artifact class, Release Set, trust policy, target Node Agent, and active evidence define the exact activation boundary. Physical similarity to a sovereign node does not activate the decision.

## 3. Canonical References

### 3.1 Owner decision

- `generated/decision-index.json#/decisions/DEC-PROFILE-001`
- `DEC-PROFILE-001`

### 3.2 Canonical objects changed or constrained

- `contracts/profiles/sovereign-linux-node.profile.json#/operating_system/immutable_signed_image`
- `contracts/artifact-classes.contract.json#/artifact_classes/system_image`
- `contracts/artifact-contracts/system-image.schema.json`
- `contracts/system.contract.json#/release_and_artifact_identity`
- `contracts/system.contract.json#/critical_transitions`
- `contracts/components/koa-node-agent.component.json#/operation_model`
- `contracts/release-channels.contract.json#/channels/system`

### 3.3 Related documents

- `DOC-PROFILE-007` — `03-profiles/07-sovereign-linux-node.md`
- `DOC-DEV-014` — `05-development/14-build-test-and-validation.md`
- `DOC-LIFE-017` — `06-lifecycle/17-contract-evolution-and-removal.md`
- `DOC-SEC-010` — `07-security/10-data-at-rest.md`
- `DOC-OPS-007` — `08-operations/07-capability-degradation.md`
- `DOC-OPS-018` — `08-operations/18-sovereign-node-operations.md`
- `DOC-CONF-016` — `09-conformance/16-sovereign-linux-conformance.md`
- `DOC-CONF-019` — `09-conformance/19-release-gates.md`

### 3.4 Related requirements

- `REQ-LIFE-CAD-008`
- `REQ-LIFE-CAD-010`
- `REQ-LIFE-CAD-011`
- `REQ-LIFE-CAD-014`
- `REQ-LIFE-CAD-023`
- `REQ-LIFE-CAD-024`
- `REQ-SEC-DAR-005`
- `REQ-SEC-DAR-014`
- `REQ-SEC-DAR-015`
- `REQ-SEC-DAR-016`
- `REQ-SEC-DAR-017`
- `REQ-SEC-DAR-018`
- `REQ-SEC-DAR-021`
- `REQ-SEC-DAR-024`
- `REQ-OPS-DEG-008`
- `REQ-OPS-DEG-009`
- `REQ-OPS-DEG-010`
- `REQ-OPS-DEG-016`
- `REQ-OPS-DEG-017`
- `REQ-OPS-DEG-018`
- `REQ-OPS-DEG-020`
- `REQ-OPS-DEG-021`
- `REQ-OPS-DEG-022`
- `REQ-OPS-DEG-024`

### 3.5 Related locks

- `LOCK-SYS-001`
- `LOCK-SYS-002`
- `LOCK-SYS-003`
- `LOCK-SYS-004`
- `LOCK-PROFILE-001`
- `LOCK-PROFILE-002`
- `LOCK-DATA-001`
- `LOCK-COMP-001`
- `LOCK-COMP-002`
- `LOCK-LIFE-001`
- `LOCK-LIFE-002`
- `LOCK-LIFE-003`
- `LOCK-LIFE-004`
- `LOCK-AI-001`
- `LOCK-AI-002`
- `LOCK-IMPL-001`
- `LOCK-IMPL-002`

### 3.6 Related exceptions

Not applicable.

## 4. Context and Problem

### 4.1 Current state

The reconciled architecture separates profile-specific deployment rules from the global baseline. The implementation-specific foundation accepted an immutable operating-system image because package-by-package mutation created drift and weakened rollback. Migration analysis retained that rule for `sovereign_linux_node`, not for developer or lightweight endpoints.

The active release model separates `system`, `services`, `governance`, and `knowledge` channels. It allows independent compatible updates, uses Release Sets for bound combinations, prohibits partial authoritative activation, and requires recovery behavior by artifact class.

The active privilege model also rejects root or host-administrator identity as an application governance interface. Sensitive host changes use a narrow profile-authorized path and produce machine-readable receipts.

### 4.2 Problem statement

A long-lived sovereign production node must remain explainable, recoverable, and consistent across disconnected or intermittently connected operation. In-place package mutation creates combinations that were not built, tested, signed, or reviewed as one unit. It can leave half-applied package transactions, configuration drift, unmanaged local fixes, incompatible boot artifacts, and uncertain rollback.

A simple read-only root does not solve this problem when the underlying installation can still drift between builds or when the boot target is not a complete signed artifact.

### 4.3 Why a decision is required

This is not a local packaging preference. It changes:

- system artifact identity;
- host mutation behavior;
- trust and signing;
- release-channel semantics;
- target activation;
- rollback and recovery;
- profile conformance;
- offline transfer;
- storage layout;
- build infrastructure;
- evidence and incident handling.

The profile decision must therefore close the architecture while leaving the concrete implementation replaceable.

### 4.4 Constraints

- The rule remains profile-scoped.
- The complete system state has one immutable artifact identity.
- Services, governance, and knowledge retain independent artifact identities.
- Component-owned mutable data stays outside the image.
- Activation cannot create mixed or partial authoritative system state.
- Target-local validation remains required.
- Offline import uses signed, integrity-protected, quarantined artifacts.
- The previous complete valid deployment and a recovery path remain available.
- Signing authority remains separate from build-worker trust.
- Boot and readiness failures preserve or restore the last valid deployment.
- Resource pressure cannot consume rollback or recovery capacity.
- Root access cannot legitimize an unmanaged mutation.
- AI cannot become build, signing, activation, compatibility, or recovery authority.

## 5. Decision Drivers

1. Recoverable complete-system updates with a precise rollback unit.
2. Verifiable supply-chain identity from source and toolchain to the booted deployment.
3. Elimination of unmanaged package drift on sovereign production nodes.
4. Safe disconnected operation and signed offline updates.
5. Separation of immutable system content from mutable component-owned data.
6. Compatibility with independent services, governance, and knowledge release channels.
7. Target-local final validation and fail-closed activation.
8. Implementation portability across maintained immutable-image mechanisms.
9. Bounded operational complexity and diagnosable failure states.
10. Preservation of profile scope without imposing appliance requirements on development or lightweight endpoints.

## 6. Considered Options

### 6.1 Option A — Complete immutable signed system image with atomic boot-target activation

**Description**

Build the complete system root and boot artifacts as one versioned system-channel image. Produce provenance and an SBOM, sign the canonical artifact, stage it outside the active deployment, validate it locally, switch the boot target atomically, reboot, run post-boot validation, and commit the deployment only after required health and readiness checks pass. Retain the previous valid deployment and an independent recovery environment.

A maintained bootc, OSTree, rpm-ostree, image-based A/B, read-only content-addressed root, or equivalent mechanism can implement this option when it satisfies the contract.

**Advantages**

- One exact system artifact identity.
- Complete rollback unit.
- No package-by-package active-root drift.
- Strong provenance and signature verification.
- Predictable offline transfer.
- Clear staging and activation boundary.
- Compatibility with Release Sets and target-local validation.
- Easier fleet comparison because nodes report exact deployed image identities.

**Disadvantages and costs**

- Requires clean image-build workers and release-signing infrastructure.
- Requires storage for staged, previous, and recovery deployments.
- Requires strict separation of mutable data and machine-specific state.
- Emergency host fixes become new image builds or bounded recovery operations.
- Driver and hardware compatibility require disciplined image testing.
- Large image transfer can cost bandwidth and time.

**Constraint fit**

This option satisfies the release, profile, data-ownership, privilege, integrity, offline, and recovery constraints without fixing one implementation technology.

### 6.2 Option B — Mutable package-managed production root with configuration management

**Description**

Install a conventional mutable distribution and apply package updates, configuration-management runs, and emergency fixes in place.

**Advantages**

- Familiar administrator workflow.
- Small package deltas.
- Broad distribution tooling.
- Rapid individual-package changes.

**Disadvantages and costs**

- The deployed state can differ from the tested state.
- Package order, local configuration, repositories, scripts, and interrupted transactions create drift.
- Rollback is package-specific and often incomplete.
- Offline reconstruction is harder.
- A root shell can silently bypass the intended release artifact.
- Fleet equality becomes an inference rather than an exact artifact identity.

**Reason rejected**

It does not provide the required complete signed activation and rollback unit for sovereign production nodes.

### 6.3 Option C — Read-only root assembled or modified locally

**Description**

Use a read-only or protected root at runtime but assemble, customize, or mutate the underlying installation locally outside a signed complete-image release process.

**Advantages**

- Reduces accidental writes during normal operation.
- Can reuse ordinary package-management tooling.
- May require less image infrastructure initially.

**Disadvantages and costs**

- Read-only behavior does not prove provenance.
- Locally assembled roots can differ between nodes.
- Signature and compatibility boundaries remain unclear.
- Recovery can restore a locally drifted state.
- Hidden overlay layers can create partial mutable behavior.

**Reason rejected**

Immutability without complete artifact identity, signing, provenance, and atomic activation does not meet the decision drivers.

### 6.4 Option D — Signed package repository with transactional package updates

**Description**

Trust a signed repository and apply transactional package changes to the production root.

**Advantages**

- Better integrity than unsigned packages.
- Smaller updates than complete images.
- Possible package-level rollback.

**Disadvantages and costs**

- Repository signatures validate packages, not the complete deployed combination.
- Local configuration and package script effects remain mutable.
- Kernel, initramfs, bootloader, and userspace can diverge.
- The rollback unit remains fragmented.
- Offline and recovery evidence require reconstructing the transaction history.

**Reason rejected**

Signed inputs do not establish one complete signed deployed system artifact.

## 7. Decision

### 7.1 Selected option

`complete_immutable_signed_system_image`

### 7.2 Normative effect

The sovereign Linux profile constrains the `system` release channel to complete immutable signed system images. The system-image contract owns image identity, contents, compatibility, provenance, integrity, signing, staging, activation, boot validation, commitment, rollback, recovery, retention, and deprecation.

The ADR does not move active values out of registries. It records why the profile and artifact contracts contain these rules.

### 7.3 Required behavior

- The image has a unique immutable artifact identity and version.
- The manifest identifies architecture, profile scope, boot artifacts, kernel, base userspace, included host components, toolchains, source revisions, dependencies, SBOM, provenance, compatibility, recovery, and retention.
- Clean registered workers build release candidates.
- Release signing uses an authorized signer scope distinct from mere build-worker identity.
- Target staging occurs outside the active deployment.
- Identity, integrity, signatures, trust, revocation, compatibility, resource capacity, and recovery are checked before activation.
- The boot target changes as one complete transition.
- The target reports and verifies the expected image identity after boot.
- Required health, readiness, storage, policy, network, and recovery checks complete before commitment.
- The previous valid deployment remains available until commitment and retention conditions permit retirement.
- Mutable data and machine-specific state remain outside the immutable root.
- Independent release channels remain independently versioned unless a Release Set binds them.
- Online and offline activation produce required receipts and evidence.

### 7.4 Prohibited behavior

- In-place package installation, removal, or upgrade on the active production root.
- Unmanaged host changes that survive as hidden authoritative system state.
- Activating an unsigned, untrusted, revoked, incompatible, corrupt, incomplete, or unrecognized image.
- Treating a valid signature as sufficient compatibility or release approval.
- Treating build-worker output as approved because the worker produced it.
- Writing component data, secrets, databases, logs, queues, mutable indexes, or backup state into the immutable image.
- Rebuilding the image locally on a production node as an unregistered emergency fix.
- Mixing files from two system-image versions in one active root.
- Deleting the last valid rollback deployment before the new deployment is committed and recoverable.
- Using control-plane desired state to bypass target-local validation.
- Guessing schemas, converting unrecognized images, or silently substituting another image or provider.
- Allowing AI output to control build, signing, compatibility, activation, rollback, or recovery.

### 7.5 Defaults

- The default scope is `sovereign_linux_node` only.
- The default activation model is stage, verify, atomic boot-target switch, reboot, post-boot validate, then commit.
- The default failure result before commitment is rollback to the previous complete valid deployment.
- The default storage model retains the active deployment, one previous valid deployment, and an independent recovery environment.
- The default active-root mutation policy is deny.
- The default offline behavior is signed bundle import into quarantine followed by local validation and explicit activation.
- The default implementation mechanism is not fixed.

### 7.6 Failure and safe-degradation behavior

A failed build, signature, trust, compatibility, staging, capacity, activation, boot, or readiness check cannot modify the committed deployment.

A failed pre-boot activation preserves the current boot target. A failed post-switch boot or readiness check returns to the previous complete valid deployment when rollback is safe. When mutable data migration makes rollback unsafe, the node enters recovery or inspection-only state and uses a declared forward-repair image or verified restore path.

The node does not report system-update readiness while recovery capacity, required trust, storage integrity, or target-local validation is unavailable.

## 8. Canonical Ownership and Data Boundaries

### 8.1 Canonical owner

- Owner profile contract: `contracts/profiles/sovereign-linux-node.profile.json`
- Owned JSON Pointer: `#/operating_system/immutable_signed_image`
- Artifact-class owner: `contracts/artifact-classes.contract.json#/artifact_classes/system_image`
- Active decision authority: `generated/decision-index.json#/decisions/DEC-PROFILE-001`

### 8.2 Produced authoritative data

- System-image manifest and artifact identity.
- Image provenance and SBOM.
- Image integrity and signing records.
- System release identity.
- Staging state.
- Target activation, boot, commitment, rollback, and recovery receipts.
- Current and previous deployed image identities.
- Image lifecycle, compatibility, deprecation, and retention records.

### 8.3 Consumed authoritative data

- Profile and overlay composition.
- Hardware and resource envelope.
- Trust roots, signer scope, revocation, and node identity.
- Release-channel and Release Set identities.
- Services, governance, and knowledge compatibility declarations.
- Node-local expected state.
- Storage, encryption, recovery, and backup state.
- Registered tests and active evidence.

### 8.4 Forbidden direct access

- The image builder cannot write release approval or target activation state.
- The signer cannot change image contents after canonicalization.
- The control plane cannot write the target boot state directly.
- The Node Agent cannot redefine image semantics or profile membership.
- The system image cannot own or directly mutate another component's authoritative source data.
- Root access cannot turn a local mutation into a registered system release.
- Services, governance, and knowledge workflows cannot mutate system-image bytes in place.
- A recovery environment cannot silently become the committed deployment.

### 8.5 Gateways and contracts

- System release channel.
- System-image artifact contract.
- Release Set contract.
- Offline-bundle contract.
- Identity and Trust verification contract.
- kOA Node Agent closed operation contract.
- Audit Broker selective receipt contract.
- Build-farm provenance contract.
- Profile and hardware-envelope contracts.
- Backup, restore, retention, portability, and recovery contracts.

## 9. Profile and Deployment Effects

| Profile or overlay | Effect | Required | Permitted | Prohibited | Conformance impact |
| --- | --- | ---: | ---: | ---: | --- |
| `user_lightweight` | No semantic effect. The profile can use a maintained mutable or immutable operating system according to its own contract. | false | true | false | No immutable-image conformance claim is inferred. |
| `developer_linux_workstation` | No semantic effect. Development hosts may remain package-managed and mutable. | false | true | false | The developer profile does not inherit the sovereign requirement. |
| `developer_windows_wsl` | No semantic effect. WSL remains a development environment rather than a sovereign production node. | false | false | true | An immutable signed host image is not a WSL profile requirement. |
| `sovereign_linux_node` | The active system root is delivered as a complete immutable signed system image with atomic activation and verified recovery. | true | true | false | Conformance requires image, signing, activation, rollback, offline, and evidence tests. |
| `sovereign_hub` | No implicit effect. A hub may adopt the mechanism only through its own explicit compatible profile rule. | false | true | false | No requirement is inherited from hardware similarity. |
| `build_farm` | Produces candidate system images and provenance when assigned, but does not activate or self-approve them. | false | true | false | Clean-worker and provenance evidence are required for release-authoritative output. |
| `control_plane` | Coordinates desired system releases when enabled but cannot bypass target-local validation. | false | true | false | The target Node Agent retains final activation authority. |
| `high_assurance` | May strengthen signing, boot verification, quorum, key custody, and evidence requirements when composed compatibly. | false | true | false | Overlay requirements remain explicit and machine-readable. |
| `sovereign_offline` | Strengthens offline transfer, local trust verification, retained recovery images, and disconnected activation. | false | true | false | Offline import does not imply activation. |
| `appliance_shell` | No direct effect on the system-image decision. | false | true | false | User-interface implementation remains a separate profile concern. |

## 10. Security, Privacy, Rights, and AI Effects

### 10.1 Security effects

The decision strengthens system supply-chain and host-state integrity through:

- clean build provenance;
- complete image digests;
- SBOM linkage;
- image signing;
- signer-scope validation;
- revocation checks;
- boot-time integrity verification under the active profile;
- target-local activation;
- closed privileged operations;
- non-partial transitions;
- retained rollback;
- minimized receipts;
- explicit mutable-data separation.

The signer is authorized for the exact artifact class and release scope. A signature does not grant profile applicability, compatibility, target activation, or application authority.

Keys and trust remain owned by Identity and Trust. Raw private keys are not embedded in images, build logs, receipts, or evidence. Node-specific credentials are provisioned outside the image.

### 10.2 Privacy and disclosure effects

The image contains no user or tenant data by default. Build and activation records minimize node identity and operational detail while retaining enough information for provenance, incident response, and rollback.

Crash data, diagnostics, and receipts exclude secrets and unnecessary protected content. Export of image, provenance, or fleet state follows disclosure and publication contracts.

### 10.3 Cultural rights and consent effects

The system image contains no authoritative cultural content or user consent state. Knowledge and UCKK artifacts retain their own release, rights, provenance, disclosure, and retention contracts.

A system update cannot silently replace or reclassify component-owned cultural material.

### 10.4 AI-boundary effects

The decision introduces no native AI.

External AI may help a human inspect a build report or draft candidate remediation. It does not select image contents, approve provenance, sign artifacts, determine compatibility, authorize activation, interpret boot health, choose rollback, or approve recovery. Any candidate recommendation enters the ordinary reviewed deterministic lifecycle.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline behavior

A sovereign node continues the currently committed image without a network or control plane.

An offline update arrives through a signed and integrity-protected offline bundle. The node imports it into quarantine, verifies the bundle and image independently, checks local trust, revocation state, profile compatibility, storage capacity, recovery readiness, and Release Set constraints, then requires explicit local activation.

A disconnected node records local receipts and preserves them for later authorized aggregation.

### 11.2 Resource envelope

The node reserves storage and I/O capacity for:

- the current deployment;
- the staged candidate;
- at least one previous complete valid deployment;
- the recovery environment;
- mutable state and logs;
- rollback or forward-repair work.

System-image staging, verification, decompression, boot preparation, and cleanup use Resource Governor limits. Resource pressure defers the update before it consumes rollback, recovery, or authoritative data capacity.

### 11.3 Observability

The node exposes bounded states for:

- current image identity;
- candidate image identity;
- staging progress;
- signature and trust result;
- compatibility result;
- recovery readiness;
- next boot target;
- last boot result;
- post-boot validation;
- commit state;
- rollback availability;
- blocked reason;
- required operator action.

It does not expose raw secrets, private keys, protected configuration, or unnecessary fleet identifiers.

### 11.4 Backup, restore, and exit

The immutable image itself is reconstructable from the registered system artifact. Mutable data is backed up under component-owned contracts.

The recovery plan includes:

- a retained previous image;
- an independent recovery environment;
- verified mutable-data backups;
- system manifest and provenance;
- exported profile and Release Set identities;
- documented portability to an equivalent maintained immutable-image mechanism.

The decision does not create dependence on one vendor or repository format.

### 11.5 Incident and recovery behavior

A compromised or revoked image is blocked or quarantined. New activation stops, dependent evidence is invalidated, affected nodes are identified, and a trusted replacement or previous valid image is selected.

A boot loop invokes the recovery environment and preserves failure evidence. A failed state migration uses forward repair or verified restore rather than unsafe image rollback. Emergency access remains time-bound, actor-bound, scope-bound, receipted, and reviewed.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`conditionally_compatible`

The decision is compatible with the global architecture only under the sovereign Linux profile and explicitly compatible overlays. It is breaking for an existing sovereign deployment that relies on unmanaged in-place package mutation.

### 12.2 Affected release channels

- `system`
- `services`
- `governance`
- `knowledge`

The direct artifact is in `system`. The other channels are affected through compatibility and Release Set relationships, not by inclusion in the image.

### 12.3 Artifact and schema effects

- Introduces or constrains the `system_image` artifact class.
- Requires `contracts/artifact-contracts/system-image.schema.json`.
- Requires system-release manifests with image identity, compatibility, signing, provenance, activation, and recovery.
- Requires target activation and recovery receipts.
- Requires offline-bundle support for disconnected transfer.
- Requires Release Set compatibility when channel versions are bound.
- Requires node-profile declaration of the active and previous system-image identities.
- Requires evidence for build, signing, activation, boot, rollback, and recovery.

### 12.4 Deprecation effects

Mutable sovereign production roots are deprecated as a deployment model. Existing mutable sovereign nodes require a recorded migration to the image-based profile before they can claim conformance.

Individual image versions can be deprecated or revoked without deprecating the artifact class.

### 12.5 Identifier preservation

Every released image identity remains reserved permanently. A superseding image references its predecessor and compatibility relationship. Deprecated, revoked, failed, and rolled-back image identities remain available for audit, incident analysis, migration, and historical reconstruction.

An image identity is never reused for different bytes.

## 13. Migration Plan

### 13.1 Preconditions

- Accepted `DEC-PROFILE-001`.
- Active sovereign Linux profile contract.
- Registered system-image artifact class and schema.
- Clean build-farm workflow.
- Authorized image-signing identity and trust roots.
- Target Node Agent operation classes.
- Separated mutable data and secrets.
- Verified backup and recovery target.
- Sufficient storage for active, staged, previous, and recovery deployments.
- Compatibility declarations for all active release channels.
- Passing migration rehearsal.

### 13.2 Migration steps

1. Inventory current packages, boot artifacts, configuration, services, mutable data, secrets, databases, logs, caches, and local deviations.
2. Move component-owned and machine-specific mutable state to declared external volumes and stores.
3. Define the canonical system-image manifest and build inputs.
4. Build the first candidate on a clean registered worker.
5. Produce provenance, SBOM, integrity, compatibility, and recovery metadata.
6. Sign the release candidate through the authorized signing path.
7. Install and validate the independent recovery environment.
8. Stage the image on a representative node without changing the current boot target.
9. Test boot, readiness, data mounts, network, identity, policy, services, rollback, restore, and offline behavior.
10. Create the first compatible Release Set when required.
11. Activate on a bounded pilot node and retain the previous mutable system only as a non-authoritative recovery source during the migration window.
12. Migrate remaining sovereign nodes after evidence passes.
13. Block mutable-root conformance claims after the declared cutoff.
14. Archive deprecated implementation guidance while retaining ADR lineage.

### 13.3 deprecated disposition

- deprecated ADR `ADR-002-immutable-os-image.md` is retained and adapted into this ADR.
- The non-authoritative statement is classified `retained_profile` for `sovereign_linux_node`.
- deprecated references to a universal immutable OS requirement are rejected.
- deprecated bootc or OSTree wording is retained as non-exclusive implementation guidance.
- The deprecated path remains recorded in migration lineage and is not an active canonical path.
- deprecated mutable-node recipes remain migration-only until dispositioned.

### 13.4 Redirects and compatibility period

- deprecated ADR alias: `doc/08-adrs/ADR-002-immutable-os-image.md` → `docs/10-adrs/ADR-002-immutable-signed-os-image.md`.
- The redirect remains for the full migration and archive-retention period.
- Mutable sovereign nodes remain nonconforming after the profile's migration cutoff.
- No identifier reuse is permitted.

## 14. Rollback and Forward Repair

### 14.1 Rollback trigger

Rollback begins when any pre-commit condition fails, including:

- boot failure;
- boot identity mismatch;
- signature or trust failure discovered after staging;
- required service or Node Agent failure;
- profile or Release Set incompatibility;
- missing protected data mount;
- data-integrity failure;
- policy or identity failure;
- unavailable recovery path;
- resource exhaustion that threatens completion;
- required receipt or evidence failure.

### 14.2 Rollback unit

The rollback unit is the complete committed system deployment:

- system-image identity;
- boot target;
- kernel and initramfs;
- system root;
- image-level configuration;
- compatible Release Set references;
- activation metadata;
- mutable-data schema state when the migration contract declares it rollback-compatible.

### 14.3 Rollback procedure

1. Stop new host and application mutations that depend on the failed deployment.
2. Preserve failure and boot evidence.
3. Select and verify the previous complete valid deployment.
4. Restore the previous boot target atomically.
5. Reboot or switch through the approved recovery mechanism.
6. Verify expected image identity, mutable-data compatibility, health, readiness, policy, network, and recovery.
7. Commit the restored deployment state.
8. produce rollback and audit receipts.
9. quarantine the failed candidate and invalidate dependent claims.

### 14.4 Forward repair

Forward repair is used when mutable data, trust state, or an irreversible migration makes image rollback unsafe. The repair is a new signed system image or a verified data restore and image combination with an explicit compatibility contract.

A local mutable patch is not forward repair. It can only be a bounded recovery action whose durable result is captured in a new image and release.

### 14.5 Last known valid state

- Authority manifest: `generated/authority-manifest.json#/active`
- Release Set: `contracts/releases/current-release-set.json`
- System deployment: `contracts/releases/system/current.json`
- Recovery deployment: `contracts/recovery.registry.json#/targets/sovereign-linux-node`
- Mutable data snapshot: component-owned verified backup references

## 15. Interfile Alignment Impact

### 15.1 Impact report

- `generated/impact/IMPACT-2026-08-03-DEC-PROFILE-001.json`

### 15.2 Modified canonical references

- `generated/decision-index.json#/adrs/ADR-002`
- `contracts/profiles/sovereign-linux-node.profile.json#/operating_system/immutable_signed_image`
- `contracts/artifact-classes.contract.json#/artifact_classes/system_image`
- `contracts/artifact-contracts/system-image.schema.json`
- `generated/test-catalog.json#/tests/TEST-ADR-002-001`
- `generated/traceability.json#/adrs/ADR-002`

### 15.3 Affected documents

| Document ID | Disposition | Reason |
| --- | --- | --- |
| `DOC-PROFILE-007` | `updated` | Owns the sovereign Linux immutable signed image requirement. |
| `DOC-SYS-018` | `reviewed_no_change` | Hardware envelope remains separate from operating-system delivery semantics. |
| `DOC-DEV-014` | `updated` | Build validation covers clean system-image assembly and provenance. |
| `DOC-LIFE-017` | `updated` | Compatibility and deprecation include system-image versions and boot compatibility. |
| `DOC-SEC-010` | `updated` | Image integrity, signing, keys, mutable-data separation, and recovery are aligned. |
| `DOC-OPS-007` | `updated` | Activation, boot, and recovery failure use explicit capability degradation. |
| `DOC-OPS-018` | `updated` | Sovereign node runbooks implement staging, activation, boot verification, and rollback. |
| `DOC-CONF-016` | `updated` | Sovereign conformance validates every decision effect. |
| `DOC-CONF-019` | `updated` | Release gates require signed image, compatibility, recovery, and evidence. |
| `DOC-CONF-012` | `reviewed_no_change` | Generated profile and release projections remain source-derived. |

### 15.4 Affected locks

| Lock ID | Disposition | Validation effect |
| --- | --- | --- |
| `LOCK-PROFILE-001` | `unchanged` | Prevents the sovereign image rule from becoming a global baseline. |
| `LOCK-PROFILE-002` | `unchanged` | Requires explicit overlay and profile composition. |
| `LOCK-DATA-001` | `unchanged` | Keeps mutable component data ownership separate from the system image. |
| `LOCK-LIFE-001` | `unchanged` | Requires artifact lifecycle, activation, and recovery. |
| `LOCK-LIFE-002` | `unchanged` | Prevents partial authoritative activation. |
| `LOCK-LIFE-003` | `unchanged` | Requires compatible Release Sets where channels are bound. |
| `LOCK-LIFE-004` | `unchanged` | Preserves rollback or forward-repair behavior. |
| `LOCK-AI-001` | `unchanged` | Keeps native AI out of the system baseline and image lifecycle. |
| `LOCK-AI-002` | `unchanged` | Prevents AI output from controlling authoritative image state. |
| `LOCK-IMPL-001` | `unchanged` | Keeps bootc, OSTree, and equivalent mechanisms as implementation choices unless adopted. |
| `LOCK-IMPL-002` | `unchanged` | Prevents one Linux implementation stack from becoming universal. |

### 15.5 Affected requirements

| Requirement ID | Disposition | Validation effect |
| --- | --- | --- |
| `REQ-LIFE-CAD-008` | `unchanged` | New incompatible system-image semantics require a new artifact identity and migration. |
| `REQ-LIFE-CAD-010` | `unchanged` | Independent system updates require cross-channel compatibility. |
| `REQ-LIFE-CAD-011` | `unchanged` | Release Sets prevent partial multi-channel activation. |
| `REQ-LIFE-CAD-023` | `unchanged` | Incompatibility preserves the previous valid deployment. |
| `REQ-SEC-DAR-005` | `unchanged` | Required sovereign storage encryption remains validated independently. |
| `REQ-SEC-DAR-014` | `unchanged` | System images require integrity, authenticity, and provenance. |
| `REQ-SEC-DAR-016` | `unchanged` | Sensitive host activation uses the narrow privileged path and receipts. |
| `REQ-SEC-DAR-017` | `unchanged` | Algorithm or key migration avoids partial protected state. |
| `REQ-OPS-DEG-008` | `unchanged` | Image incompatibility blocks activation and forbids guessing. |
| `REQ-OPS-DEG-020` | `unchanged` | Restoration requires full revalidation. |
| `REQ-OPS-DEG-022` | `unchanged` | Activation and recovery produce machine-readable records. |

### 15.6 Generated artifacts

The following derived outputs require regeneration after any semantic change to this ADR's canonical sources:

- ADR index and lifecycle catalog;
- profile catalog;
- sovereign Linux capability matrix;
- system artifact-class catalog;
- release-channel and Release Set compatibility matrices;
- image-build and activation test catalog;
- traceability graph;
- conformance matrix;
- impact report;
- AI context packages for sovereign Linux, system releases, security, operations, and conformance.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose | Required result |
| --- | --- | --- |
| `TEST-ADR-002-001` | Verify that the immutable signed image requirement appears only in the sovereign Linux profile and explicitly compatible overlays. | `pass` |
| `TEST-ADR-002-002` | Verify that the active root cannot be changed through in-place package mutation or unmanaged host writes. | `pass` |
| `TEST-ADR-002-003` | Verify complete system-image manifest, architecture, profile, boot-artifact, dependency, provenance, SBOM, integrity, and recovery metadata. | `pass` |
| `TEST-ADR-002-004` | Verify clean build-worker provenance and absence of undeclared build inputs. | `pass` |
| `TEST-ADR-002-005` | Verify required image signatures, signer scope, trust roots, revocation, and boot-time integrity validation. | `pass` |
| `TEST-ADR-002-006` | Verify strict separation of immutable system content from mutable component data, secrets, databases, logs, queues, caches, and recovery state. | `pass` |
| `TEST-ADR-002-007` | Verify inactive staging and absence of effect before target-local activation. | `pass` |
| `TEST-ADR-002-008` | Verify atomic boot-target switching without mixed or partial authoritative system state. | `pass` |
| `TEST-ADR-002-009` | Verify post-boot health, readiness, expected-version, policy, storage, network, and recovery checks before deployment commitment. | `pass` |
| `TEST-ADR-002-010` | Verify automatic or operator-directed rollback to the previous complete valid deployment after boot or readiness failure. | `pass` |
| `TEST-ADR-002-011` | Verify forward repair through a new signed image when stateful rollback is unsafe. | `pass` |
| `TEST-ADR-002-012` | Verify signed offline transfer, quarantine, local trust and compatibility validation, explicit activation, and local receipts. | `pass` |
| `TEST-ADR-002-013` | Verify independent services, governance, and knowledge channel updates and Release Set compatibility. | `pass` |
| `TEST-ADR-002-014` | Verify resource bounds, reserved staging capacity, retained previous deployment, recovery environment, and update-pressure behavior. | `pass` |
| `TEST-ADR-002-015` | Verify minimized machine-readable build, signing, staging, activation, boot, failure, rollback, and recovery receipts. | `pass` |
| `TEST-ADR-002-016` | Verify that local administrator, root, container runtime, control plane, build worker, and image signer do not gain application or release authority implicitly. | `pass` |
| `TEST-ADR-002-017` | Verify absence of native or external AI authority in image construction, signing, compatibility, activation, rollback, and recovery. | `pass` |
| `TEST-ADR-002-018` | Verify complete traceability and historical retention for the selected image and all rejected alternatives. | `pass` |

### 16.2 Required evidence

| Evidence ID | Evidence type | Location |
| --- | --- | --- |
| `EVID-ADR-002-BUILD` | Clean system-image build provenance and reproducibility report | `generated/evidence-catalog.json#/evidence/EVID-ADR-002-BUILD` |
| `EVID-ADR-002-SIGN` | Image-signing, trust-scope, revocation, and boot-verification evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-002-SIGN` |
| `EVID-ADR-002-ACTIVATE` | Target-local staging, activation, boot, readiness, and commit receipts | `generated/evidence-catalog.json#/evidence/EVID-ADR-002-ACTIVATE` |
| `EVID-ADR-002-RECOVERY` | Rollback, recovery-environment, restore, and forward-repair evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-002-RECOVERY` |
| `EVID-ADR-002-OFFLINE` | Disconnected transfer, quarantine, local verification, and activation evidence | `generated/evidence-catalog.json#/evidence/EVID-ADR-002-OFFLINE` |
| `EVID-ADR-002-PROFILE` | Profile-scope and non-inheritance validation report | `generated/evidence-catalog.json#/evidence/EVID-ADR-002-PROFILE` |

### 16.3 Required validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_normative_language.py
python docs/tools/check_language.py
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/check_decision_closure.py
python docs/tools/check_no_unresolved_state.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific validation

- Validate the sovereign profile's exact immutable-image declaration.
- Validate system-image schema and positive and negative examples.
- Validate clean build provenance and reproducibility requirements.
- Validate signing, trust, revocation, and signer scope.
- Validate boot-time expected image identity.
- Validate data and secret separation.
- Validate atomic staging, activation, commitment, and rollback.
- Validate failed boot and failed readiness recovery.
- Validate incompatible Release Set rejection.
- Validate online and offline distribution.
- Validate resource-pressure behavior.
- Validate non-inheritance by user and developer profiles.
- Validate absence of AI authority.
- Validate historical deprecated ADR disposition.

### 16.5 Acceptance criteria

1. The immutable image requirement resolves only for `sovereign_linux_node` and explicitly compatible overlays.
2. The selected system image has one canonical identity, complete manifest, provenance, SBOM, integrity, signature, trust scope, compatibility, and recovery contract.
3. A clean target stages the image without changing the active deployment.
4. Target-local validation blocks invalid, unsigned, revoked, incompatible, incomplete, or unrecoverable images.
5. Boot-target activation produces no mixed or partial system state.
6. A failed boot or readiness check restores the previous complete valid deployment.
7. Mutable component data remains usable and owned after update and rollback.
8. Offline transfer and activation complete without network or control-plane authority.
9. Services, governance, and knowledge retain independent release identities.
10. All affected objects have a final impact disposition.
11. All required checks complete successfully.
12. `authority.registry.json` references the exact validated versions and integrity values.

## 17. Consequences

### 17.1 Positive consequences

- Exact system identity for every conforming node.
- Reduced configuration and package drift.
- Atomic activation and a clear rollback unit.
- Stronger supply-chain provenance and signing.
- Predictable offline distribution.
- Easier fleet comparison and incident scoping.
- Cleaner separation between system content and component data.
- Reduced need for permanent privileged package-management access.
- Implementation portability through contract-level requirements.

### 17.2 Negative consequences and costs

- Image-build and signing infrastructure is mandatory.
- Updates can be larger than package deltas.
- Additional local storage is required.
- Hardware support must be validated before release.
- Mutable-state separation requires design and migration work.
- Emergency changes require recovery procedures and new image releases.
- Stateful data migrations can complicate rollback.
- Operators need image-specific diagnostics and recovery training.

### 17.3 Operational obligations

- Maintain clean image-build workers.
- Protect signing identities and trust roots.
- Test representative hardware.
- Reserve rollback and recovery capacity.
- Exercise failed-boot and failed-readiness recovery.
- Maintain offline update media and import procedures.
- Monitor image age, revocation, compatibility, and storage pressure.
- Retain sufficient provenance and receipts for incident reconstruction.
- Remove retired images only after dependency and retention checks.

### 17.4 Documentation obligations

- Regenerate every projection after canonical changes.
- Preserve this ADR and its predecessor lineage.
- Record implementation choices separately from the decision.
- Update rejected alternatives when an objective reconsideration trigger occurs.

### 17.5 Technical debt explicitly accepted

The first implementation may support one maintained immutable-image mechanism and one primary architecture. This is acceptable only while:

- the profile contract remains implementation-neutral;
- portability and export metadata are preserved;
- the selected mechanism remains maintained;
- a replacement migration is documented;
- additional architectures are blocked rather than guessed;
- the limitation is visible in compatibility and conformance evidence.

## 18. Rejected Alternatives

| Alternative | Reason rejected | Reconsideration trigger |
| --- | --- | --- |
| Mutable package-managed root | Cannot prove or restore one complete tested deployed system state. | A maintained mechanism demonstrates equivalent complete-state identity, atomic activation, and rollback with lower operational risk. |
| Read-only root assembled locally | Runtime immutability does not establish build provenance or release identity. | Local assembly becomes a registered deterministic signed artifact build with exact reproducibility and target-independent identity. |
| Signed packages with transactional updates | Package signatures do not sign the complete deployed combination or local configuration. | Transactional package technology produces one complete canonical signed deployment identity and equivalent rollback semantics. |
| Configuration-management convergence | Convergence does not prove the intermediate or final node matches a tested artifact exactly. | A formally verified convergence system supplies deterministic complete-state identity, offline reproducibility, atomic transition, and rollback. |
| Containerize all host functions | Containers do not replace kernel, boot, base userspace, storage, networking, identity, or privileged host lifecycle. | None; containers can remain an implementation detail inside the signed system image. |
| Rebuild locally on each node | Node-local build inputs, state, and authority are difficult to verify and compare. | A profile explicitly assigns clean reproducible build-worker authority to the node and separates signing and activation domains. |

Rejected alternatives cannot be implemented as undocumented exceptions.

## 19. Exceptions and Waivers

Not applicable.

A deployment that cannot use the immutable signed image cannot claim `sovereign_linux_node` conformance unless an accepted bounded exception references the exact requirement, node scope, owner, expiration, compensating controls, migration plan, tests, and evidence. Such an exception does not change this ADR or make mutable roots generally permitted.

## 20. Implementation Guidance

This section is non-normative.

A conforming implementation can use bootc, OSTree, rpm-ostree, an A/B partition design, a content-addressed read-only root, or another maintained mechanism. The implementation should provide:

- canonical image construction from locked inputs;
- separate boot and mutable-data storage;
- bootloader integration;
- image signature and digest verification;
- inactive deployment staging;
- deterministic boot-target selection;
- boot-success and health markers;
- previous deployment retention;
- recovery-media or recovery-partition support;
- local and offline artifact stores;
- bounded cleanup;
- Node Agent closed operations;
- explicit diagnostics.

Machine-specific enrollment, keys, network identity, and secrets should be provisioned after image construction and stored outside the image. Configuration that must vary by node should use a declared bounded mutable layer whose ownership and backup behavior are explicit.

A recovery shell can inspect, unlock, mount, collect evidence, choose a verified boot target, and restore data through closed procedures. It should not encourage permanent ad hoc mutation of the system root.

## 21. Decision Record

### 21.1 Decision authority record

- Decision ID: `DEC-PROFILE-001`
- Decision status: `accepted`
- Decision owner: `profile_authority`
- Decision registry reference: `generated/decision-index.json#/decisions/DEC-PROFILE-001`
- Related release decision: `DEC-REL-001`
- Related hardware decision: `DEC-HW-001`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Author | `migration-author` | `submitted` | `2026-08-03` |
| Canonical owner | `profile-authority` | `approved` | `2026-08-03` |
| Architecture reviewer | `architecture-governance` | `approved` | `2026-08-03` |
| Security reviewer | `security-authority` | `approved` | `2026-08-03` |
| Validation pipeline | `automated` | `pass` | `2026-08-03` |
| Authority activator | `documentation-authority` | `activated` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_id": "CHG-2026-0002",
  "decision_ids": [
    "DEC-PROFILE-001",
    "DEC-REL-001",
    "DEC-HW-001"
  ],
  "modified_canonical_refs": [
    "generated/decision-index.json#/adrs/ADR-002",
    "contracts/profiles/sovereign-linux-node.profile.json#/operating_system/immutable_signed_image",
    "contracts/artifact-classes.contract.json#/artifact_classes/system_image",
    "contracts/artifact-contracts/system-image.schema.json"
  ],
  "affected_document_ids": [
    "DOC-PROFILE-007",
    "DOC-DEV-014",
    "DOC-LIFE-017",
    "DOC-SEC-010",
    "DOC-OPS-007",
    "DOC-OPS-018",
    "DOC-CONF-016",
    "DOC-CONF-019"
  ],
  "requirement_ids": [
    "REQ-LIFE-CAD-008",
    "REQ-LIFE-CAD-010",
    "REQ-LIFE-CAD-011",
    "REQ-LIFE-CAD-014",
    "REQ-LIFE-CAD-023",
    "REQ-LIFE-CAD-024",
    "REQ-SEC-DAR-005",
    "REQ-SEC-DAR-014",
    "REQ-SEC-DAR-015",
    "REQ-SEC-DAR-016",
    "REQ-SEC-DAR-017",
    "REQ-SEC-DAR-018",
    "REQ-SEC-DAR-021",
    "REQ-SEC-DAR-024",
    "REQ-OPS-DEG-008",
    "REQ-OPS-DEG-009",
    "REQ-OPS-DEG-010",
    "REQ-OPS-DEG-016",
    "REQ-OPS-DEG-017",
    "REQ-OPS-DEG-018",
    "REQ-OPS-DEG-020",
    "REQ-OPS-DEG-021",
    "REQ-OPS-DEG-022",
    "REQ-OPS-DEG-024"
],
  "lock_ids": [
    "LOCK-SYS-001",
    "LOCK-SYS-002",
    "LOCK-SYS-003",
    "LOCK-SYS-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-IMPL-001",
    "LOCK-IMPL-002"
],
  "exception_ids": [],
  "adr_ids": [
    "ADR-002"
  ],
  "test_ids": [
    "TEST-ADR-002-001",
    "TEST-ADR-002-002",
    "TEST-ADR-002-003",
    "TEST-ADR-002-004",
    "TEST-ADR-002-005",
    "TEST-ADR-002-006",
    "TEST-ADR-002-007",
    "TEST-ADR-002-008",
    "TEST-ADR-002-009",
    "TEST-ADR-002-010",
    "TEST-ADR-002-011",
    "TEST-ADR-002-012",
    "TEST-ADR-002-013",
    "TEST-ADR-002-014",
    "TEST-ADR-002-015",
    "TEST-ADR-002-016",
    "TEST-ADR-002-017",
    "TEST-ADR-002-018"
],
  "evidence_ids": [
    "EVID-ADR-002-BUILD",
    "EVID-ADR-002-SIGN",
    "EVID-ADR-002-ACTIVATE",
    "EVID-ADR-002-RECOVERY",
    "EVID-ADR-002-OFFLINE",
    "EVID-ADR-002-PROFILE"
],
  "tests_run": [
    "metadata_parse",
    "adr_section_order",
    "profile_scope_alignment",
    "decision_alignment",
    "release_model_alignment",
    "node_agent_operation_alignment",
    "no_unresolved_markers"
  ],
  "impact_report": "generated/impact/IMPACT-2026-08-03-DEC-PROFILE-001.json",
  "validation_status": "pass"
}
```

## 22. Supersession and Historical Integrity

When this ADR is superseded:

1. its status changes to `superseded`;
2. `superseded_by` references the replacement ADR;
3. the replacement ADR references `ADR-002` through `supersedes`;
4. the original identifier and path remain reserved;
5. historical decisions, migration records, impact reports, validation evidence, image manifests, receipts, and authority manifests remain available;
6. active profile and release projections are regenerated;
7. AI context packages stop treating this ADR as current rationale;
8. retired implementation identifiers remain preserved where required for recovery and historical reconstruction.

This ADR remains in the repository after acceptance, rejection, deprecation, or supersession.
