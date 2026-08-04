<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-001",
  "document_class": "architecture_decision_record",
  "status": "active",
  "language": "en",
  "layer": "adrs",
  "adr_id": "ADR-001",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-KERNEL-001",
  "created_at": "2026-08-03",
  "accepted_at": "2026-08-03",
  "effective_at": "2026-08-03",
  "supersedes": [],
  "superseded_by": null,
  "scope": [
    "profile:developer_linux_workstation",
    "profile:sovereign_linux_node",
    "profile:sovereign_hub",
    "profile:build_farm",
    "profile:control_plane",
    "linux_system_channel"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json#/decisions/DEC-KERNEL-001",
    "generated/decision-index.json#/adrs/ADR-001",
    "contracts/terminology.contract.json",
    "contracts/system.contract.json",
    "generated/component-catalog.json",
    "generated/profile-catalog.json",
    "contracts/release-channels.contract.json#/channels/system",
    "contracts/artifact-classes.contract.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-KERNEL-001",
    "DEC-PROFILE-001",
    "DEC-REL-001"
  ],
  "requirement_ids": [
    "REQ-CONF-SLN-011",
    "REQ-CONF-SLN-012",
    "REQ-CONF-SLN-013",
    "REQ-CONF-SLN-014",
    "REQ-CONF-SLN-015",
    "REQ-SEC-SC-004",
    "REQ-SEC-SC-005",
    "REQ-SEC-SC-012",
    "REQ-SEC-SC-016",
    "REQ-SEC-SC-017",
    "REQ-SEC-SC-025",
    "REQ-SEC-SC-028",
    "REQ-SEC-SC-030",
    "REQ-SEC-SC-036",
    "REQ-SEC-SC-039",
    "REQ-SEC-SC-040",
    "REQ-SEC-SC-041",
    "REQ-SEC-SC-048",
    "REQ-SEC-SC-051",
    "REQ-SEC-SC-054",
    "REQ-SEC-SC-055"
  ],
  "lock_ids": [
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-SEC-010"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CONST-002",
    "DOC-CONST-013",
    "DOC-SEC-019",
    "DOC-CONF-016"
  ],
  "tags": [
    "adr",
    "linux",
    "kernel",
    "maintenance",
    "upstream",
    "distribution",
    "system-channel",
    "security-updates",
    "hardware-support",
    "supply-chain"
  ]
}
KOA:DOC-META:END -->

# ADR-001 — Use a Standard Maintained Linux Kernel

| Field | Value |
| --- | --- |
| ADR | `ADR-001` |
| Owner decision | `DEC-KERNEL-001` |
| Status | Accepted |
| Decision class | Major |
| Accepted | 2026-08-03 |
| Effective | 2026-08-03 |
| Supersedes | None |
| Superseded by | None |

## 1. Context

kOA Linux deployments require a kernel that can provide:

- timely security maintenance;
- broad and predictable hardware support;
- stable userspace and driver interfaces;
- process, memory, I/O, namespace, networking, and storage isolation primitives;
- resource-control support required by Resource Governor;
- reliable recovery and system-update behavior;
- compatibility with standard operating-system, container, service, and observability tooling;
- verifiable source, build, artifact, and release provenance.

Maintaining a permanent kOA-specific kernel fork would create a continuous obligation to:

- monitor upstream security disclosures;
- backport security and correctness fixes;
- maintain hardware drivers;
- preserve compatibility with supported userspace;
- reproduce and attest kernel builds;
- qualify every kernel change across applicable profiles;
- support rollback and recovery;
- retain specialized kernel engineering capacity for the lifetime of every deployment.

Those obligations do not provide primary kOA product differentiation. kOA differentiation belongs mainly in component boundaries, governance, policy, services, artifacts, profiles, conformance, and user experience.

At the same time, “standard kernel” cannot mean selecting any convenient kernel package. The selected kernel must remain inside a recognized active maintenance chain and must satisfy the exact profile, hardware, security, lifecycle, and evidence requirements of its deployment.

## 2. Decision

kOA Linux profiles shall use a standard maintained Linux kernel supplied through a recognized upstream, distribution, or hardware-vendor maintenance chain.

The selected maintenance chain shall provide:

- a named and accountable maintainer;
- a published support and end-of-support model;
- an active security-vulnerability intake and correction process;
- traceable source and patch provenance;
- identifiable release artifacts;
- a supported update path;
- sufficient hardware and userspace compatibility for the target profile.

The active deployment profile shall select the permitted kernel source, version family, configuration requirements, module policy, support horizon, update mechanism, recovery behavior, and required evidence.

kOA shall not maintain a permanent product kernel fork as the default or baseline.

Product-specific kernel patches shall remain:

- minimal;
- explicitly documented;
- reproducibly buildable;
- security reviewed;
- covered by profile and conformance tests;
- associated with a maintenance owner;
- associated with an upstream, distribution, or removal plan;
- absent when the same requirement can be met by a maintained standard kernel, userspace service, policy, profile, or hardware choice.

A custom kernel or durable kernel fork is permitted only after a separate accepted ADR demonstrates that a required invariant cannot be met through a recognized maintenance chain.

## 3. Decision Scope

### 3.1 Included profiles

This decision applies to every active profile whose system contract selects Linux, including as applicable:

- `developer_linux_workstation`;
- `sovereign_linux_node`;
- `sovereign_hub`;
- `build_farm`;
- `control_plane`.

A profile remains responsible for declaring whether Linux is required and which kernel maintenance chain it accepts.

This ADR does not make Linux mandatory for profiles that do not otherwise select Linux.

### 3.2 Included kernel material

The decision applies to:

- kernel image;
- kernel configuration;
- in-tree drivers;
- loadable kernel modules;
- initramfs content that is part of kernel activation;
- kernel firmware dependencies where governed by the system contract;
- kernel command-line policy;
- kernel patch delta;
- kernel build toolchain and provenance;
- kernel update and recovery artifacts.

### 3.3 Excluded decisions

This ADR does not decide:

- one universal Linux distribution;
- one exact kernel version;
- one universal LTS branch;
- one filesystem;
- one bootloader;
- one service manager;
- one container runtime;
- whether the operating-system image is immutable;
- whether Secure Boot, TPM, measured boot, module signing, or hardware-backed keys are required;
- whether a real-time or hardened kernel is required for a particular profile.

Those choices remain profile-, system-, security-, hardware-, or overlay-specific.

## 4. Definitions and Interpretation

### 4.1 Standard maintained Linux kernel

A **standard maintained Linux kernel** is a kernel whose primary maintenance responsibility remains with an upstream Linux maintenance branch, a recognized Linux distribution, or an accountable hardware or platform vendor.

It can include:

- distribution backports;
- vendor-supported hardware enablement;
- profile-specific configuration;
- an explicitly controlled small patch delta;
- approved out-of-tree modules.

It is not standard maintained merely because it is based on Linux source.

### 4.2 Recognized maintenance chain

A maintenance chain is recognized when the active profile and supply-chain authorities can verify:

- source origin;
- release identity;
- maintainer identity;
- support lifecycle;
- security-update process;
- update artifacts;
- vulnerability and revocation handling;
- provenance and integrity material;
- target hardware and userspace support.

Popularity, package availability, or a public source repository alone is insufficient.

### 4.3 Custom kernel

A **custom kernel** is a kernel for which kOA or its deployment owner assumes primary responsibility for a material, durable divergence from the selected maintenance chain.

The following do not automatically create a custom kernel:

- selecting supported configuration options;
- disabling unnecessary drivers;
- applying a distribution-supported configuration;
- rebuilding exact maintained sources reproducibly;
- carrying a small temporary patch under this ADR’s controls.

A durable fork, a large private patch set, an unsupported branch, or an unmaintained vendor kernel is custom.

### 4.4 Maintained status

Maintained status is evaluated at the time of:

- profile admission;
- system release publication;
- Release Set construction;
- node activation;
- periodic conformance review;
- relevant security incident;
- upstream or distribution support change.

A kernel that was maintained when first deployed does not remain conformant after its accepted support window ends.

## 5. Rationale

### 5.1 Security response

A recognized maintenance chain distributes security analysis and patching across a larger maintained ecosystem.

This reduces the probability that kOA deployments remain exposed because a private fork failed to receive or correctly backport a fix.

### 5.2 Hardware and driver support

Standard maintained kernels provide the broadest practical hardware, firmware, driver, and diagnostic compatibility.

This supports profile portability and avoids tying kOA to a narrow appliance bill of materials unless a profile intentionally does so.

### 5.3 Userspace compatibility

Mainstream kernels receive continuous validation against distributions, libraries, service managers, container runtimes, observability tools, storage systems, and recovery tooling.

kOA can therefore concentrate conformance effort on its own contracts and required kernel capabilities rather than maintaining a separate operating-system ecosystem.

### 5.4 Supply-chain accountability

A standard maintenance chain provides externally identifiable source, release, and vulnerability history.

That history supports:

- admitted source;
- exact build inputs;
- SBOM and provenance;
- signature and trust validation where required;
- vulnerability disposition;
- artifact revocation;
- controlled rebuild;
- forensic comparison.

### 5.5 Lifecycle sustainability

Kernel maintenance is a long-lived obligation rather than a one-time engineering task.

Using a maintained chain keeps the operating burden proportionate to the value the kernel supplies to kOA.

### 5.6 Architectural focus

The decision keeps product differentiation outside the kernel unless the kernel is the only place where a required invariant can be enforced.

This favors:

- profiles over hard-coded product assumptions;
- userspace components over private kernel services;
- explicit policy over invisible kernel behavior;
- standard interfaces over product-only interfaces;
- portable conformance evidence over one-off hardware qualification.

## 6. Required Decision Rules

### 6.1 Kernel selection

A profile-selected kernel shall:

1. be within an active accepted support window;
2. support the profile’s target architecture and hardware class;
3. provide the isolation and resource primitives required by active contracts;
4. support the profile’s storage, network, recovery, and service model;
5. have an admitted source and artifact path;
6. have a declared vulnerability and update process;
7. have testable rollback, recovery, or forward-repair behavior;
8. be compatible with the profile’s userspace and system artifacts.

### 6.2 Version selection

The profile shall select a kernel version family based on:

- support horizon;
- security-maintenance quality;
- target hardware support;
- required kernel interfaces;
- userspace compatibility;
- update and rollback behavior;
- conformance evidence.

The newest kernel is not automatically preferred.

An older kernel is not acceptable merely because it remains installed or operational.

### 6.3 Configuration

Kernel configuration shall be version controlled and attributable to the selecting profile or system artifact.

Configuration changes shall be treated as system-channel changes when they can affect:

- privilege;
- isolation;
- resource enforcement;
- networking;
- storage;
- cryptography;
- module loading;
- observability;
- recovery;
- hardware support.

Configuration shall not silently weaken a profile requirement.

### 6.4 Patch delta

Every product-specific patch shall identify:

- source maintenance chain and base release;
- patch purpose;
- affected invariant or requirement;
- security impact;
- maintenance owner;
- test coverage;
- expected lifetime;
- upstream, distribution, replacement, or removal path;
- affected profiles and architectures.

A patch shall be removed when the maintenance chain supplies an accepted equivalent.

### 6.5 Out-of-tree modules

An out-of-tree module shall:

- have an explicit owner;
- identify source and build provenance;
- identify compatible kernel versions;
- be rebuilt and retested for applicable kernel updates;
- follow the active profile’s loading and signing rules;
- have vulnerability, revocation, rollback, and removal behavior;
- not force use of an unsupported kernel after its maintenance window ends.

### 6.6 Custom-kernel escalation

A proposal for a custom kernel shall require a separate major ADR.

That ADR shall include:

- the invariant that cannot be met otherwise;
- alternatives attempted;
- threat model;
- exact fork scope;
- primary maintenance owner;
- staffing and support horizon;
- upstream security-intake process;
- patch and backport service expectations;
- build reproducibility;
- SBOM and provenance;
- signing and key scope;
- target hardware matrix;
- profile and release impact;
- update, rollback, and forward-repair behavior;
- exit or upstreaming strategy;
- complete conformance plan.

An ordinary exception or waiver cannot create a permanent custom-kernel baseline.

## 7. Consequences

### 7.1 Positive consequences

- Security corrections can follow established maintenance processes.
- Hardware support remains broad and replaceable.
- Kernel engineering becomes a bounded integration responsibility.
- Supply-chain evidence can reference recognized source and release histories.
- Profile portability improves.
- Standard diagnostic and recovery tooling remains usable.
- Container, service, storage, and networking technology can use maintained kernel interfaces.
- kOA avoids hidden product authority inside a private kernel fork.
- Kernel support status can be evaluated consistently during conformance.

### 7.2 Costs and constraints

- kOA can be constrained by upstream or distribution release schedules.
- New hardware or kernel capabilities can require waiting for a maintained release.
- Distribution backports can differ from upstream version numbering.
- Profile qualification must cover kernel updates.
- A small product patch can require repeated rebasing until accepted or removed.
- Kernel end-of-support can force a system-channel migration even when higher layers are unchanged.
- Multiple Linux profiles can select different maintained families, increasing the test matrix.

### 7.3 Operational consequences

Operations shall track:

- current kernel identity;
- source maintenance chain;
- support window;
- vulnerability status;
- active patch and module delta;
- target profile compatibility;
- update availability;
- recovery readiness;
- conformance evidence.

A kernel support deadline is a lifecycle constraint, not merely an informational warning.

## 8. Alternatives Considered

### 8.1 Permanent kOA-maintained kernel fork

**Rejected as the baseline.**

It creates a permanent security, hardware, compatibility, testing, and staffing burden disproportionate to kOA differentiation.

It remains possible only through the custom-kernel escalation defined in this ADR.

### 8.2 Always use the latest upstream mainline kernel

**Rejected.**

Mainline freshness does not guarantee an appropriate support horizon, distribution integration, hardware qualification, or recovery path.

Profiles select an accepted maintained family rather than following a moving branch.

### 8.3 Pin one universal kernel version for every Linux profile

**Rejected.**

Developer workstations, sovereign nodes, hubs, build farms, and control planes can have different hardware and support requirements.

The decision standardizes maintenance properties, not one version number.

### 8.4 Use an end-of-support kernel while functionality remains adequate

**Rejected.**

Functional operation does not replace active security maintenance.

A bounded emergency exception can support migration operations, but it cannot make the unsupported kernel conformant.

### 8.5 Use a specialized hardened or real-time kernel everywhere

**Rejected as a global rule.**

A profile can select a maintained specialized kernel when its requirements justify it.

Specialization is not automatically appropriate for every profile.

### 8.6 Depend on containers to isolate kernel risk

**Rejected.**

Containers share the host kernel.

Container isolation does not remove kernel maintenance, vulnerability, driver, resource-control, or host-boundary obligations.

### 8.7 Carry private out-of-tree drivers indefinitely

**Rejected.**

A driver can be accepted under bounded ownership and maintenance controls, but it cannot justify indefinite use of an unsupported kernel or an unowned private patch stack.

## 9. Security, Supply-Chain, and Lifecycle Implications

### 9.1 Release channel

The kernel belongs to the `system` release channel.

A kernel change shall not be published as a `services`, `governance`, or `knowledge` release.

Its compatibility with the other channels shall be represented through the applicable Release Set.

### 9.2 Build and provenance

A published kernel artifact shall follow the software supply-chain controls applicable to its artifact class, including as required:

- admitted source;
- exact patch delta;
- exact configuration;
- exact toolchain;
- clean build;
- SBOM;
- provenance;
- vulnerability disposition;
- signatures and trust evidence;
- artifact admission.

A locally rebuilt kernel is not production-authoritative merely because its source revision matches.

### 9.3 Activation

Kernel activation shall follow the system lifecycle selected by the active profile.

That lifecycle can use:

- package-based replacement;
- image-based activation;
- A/B system state;
- boot-entry selection;
- another declared system mechanism.

Activation shall verify the booted kernel identity rather than only the staged artifact.

### 9.4 Rollback and recovery

The prior kernel can be retained as a recovery target when:

- the profile declares that behavior;
- userspace and system state remain compatible;
- the prior kernel remains trusted for the recovery purpose;
- the rollback path is tested.

When rollback is unsafe or incompatible, recovery shall use the declared forward-repair or system-recovery path.

### 9.5 Vulnerability response

A material kernel or module vulnerability shall trigger:

1. affected-version identification;
2. exposure and exploitability analysis;
3. maintainer and patch status review;
4. mitigation or isolation where required;
5. corrected artifact admission;
6. profile and Release Set compatibility validation;
7. controlled activation;
8. revocation or retirement of affected artifacts;
9. retained incident and conformance evidence.

Break-glass cannot make an invalid kernel signature, untrusted artifact, or incompatible Release Set acceptable.

## 10. Conformance and Evidence

Conformance shall verify the exact claimed node, profile, architecture, kernel artifact, configuration, modules, userspace, and Release Set.

Required evidence includes, where applicable:

| Evidence area | Required conclusion |
| --- | --- |
| Kernel identity | The running kernel matches an admitted system artifact |
| Maintenance chain | Source, maintainer, support lifecycle, and update path resolve |
| Support status | The selected release remains inside its accepted maintenance window |
| Source and patch provenance | Base source and every product delta are attributable |
| Configuration | The active configuration matches the profile-owned configuration |
| Module inventory | Loaded and available modules match declared policy |
| Hardware | Required devices and target architecture are supported |
| Isolation | Required process, namespace, networking, storage, and privilege boundaries work |
| Resource governance | Required CPU, memory, I/O, process, and worker controls work |
| Security | Applicable vulnerability, hardening, loading, and trust rules pass |
| Supply chain | SBOM, provenance, signatures, and artifact admission pass where required |
| Lifecycle | Update, boot verification, rollback, recovery, and forward repair pass |
| Release compatibility | The exact system release belongs to a compatible Release Set |
| Patch exit | Every private patch has an active owner and removal or upstream plan |

The following fail the affected conformance claim:

- unsupported kernel release;
- unresolved maintenance chain;
- undeclared kernel or configuration artifact;
- unverified patch delta;
- unowned out-of-tree module;
- booted identity differing from the admitted artifact;
- missing required resource or isolation capability;
- incompatible userspace or Release Set;
- required recovery path not passing;
- permanent custom fork without a separate accepted ADR.

Conformance evidence shall follow `docs/09-conformance/05-test-evidence.md`.

## 11. Decision Closure, Review, and Supersession

### 11.1 Closed decisions

This ADR closes the following questions:

- kOA does not use a permanent private kernel fork as its Linux baseline.
- Linux profiles select kernels from recognized active maintenance chains.
- Exact kernel family and implementation remain profile-specific.
- Kernel configuration and small temporary deltas are permitted only under explicit controls.
- Unsupported kernels are nonconformant even when still functional.
- Kernel artifacts belong to the system release channel.
- A durable custom kernel requires a separate major ADR.
- Product differentiation remains primarily above the kernel.

### 11.2 Prohibited assumptions

This ADR shall not be interpreted to mean:

- every profile must use Linux;
- every Linux profile must use one distribution or version;
- every selected kernel must be an upstream LTS release rather than a maintained distribution or vendor release;
- a distribution package is trusted without artifact admission;
- an immutable signed image is globally required;
- Secure Boot, TPM, measured boot, or module signing is globally required;
- rootless containers compensate for an unsupported kernel;
- a supported kernel automatically satisfies every profile requirement;
- a temporary patch can remain indefinitely without review;
- an exception can establish a permanent custom-kernel architecture.

### 11.3 Review triggers

This ADR shall be reviewed when:

- Linux upstream maintenance practices materially change;
- a selected maintenance chain can no longer satisfy required security response;
- a required invariant appears to require durable kernel divergence;
- target hardware cannot be supported by an accepted maintained chain;
- kernel architecture changes invalidate the maintenance model;
- a profile proposes a specialized kernel as a baseline;
- evidence shows that the standard-kernel decision creates unacceptable sovereign, safety, or lifecycle risk.

### 11.4 Supersession condition

Supersession requires a new accepted ADR that:

- identifies this ADR;
- explains the changed constraints;
- defines the replacement maintenance and authority model;
- addresses supply chain, security response, hardware, lifecycle, recovery, staffing, and conformance;
- updates the owner decision and affected profile contracts.

Until superseded, this ADR remains the controlling rationale for `DEC-KERNEL-001`.
