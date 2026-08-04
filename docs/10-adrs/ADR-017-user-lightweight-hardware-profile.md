<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ADR-017",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "architecture_decision",
  "scope": [
    "user_lightweight"
  ],
  "canonical_refs": [
    "generated/decision-index.json",
    "generated/profile-catalog.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/components/resource-governor.component.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-HW-001",
    "DEC-PROFILE-001",
    "DEC-GOV-001",
    "DEC-CONTAINER-001",
    "DEC-K8S-001",
    "DEC-SHELL-001"
  ],
  "requirement_ids": [
    "REQ-CONF-USER-001",
    "REQ-CONF-USER-002",
    "REQ-CONF-USER-003",
    "REQ-CONF-USER-004",
    "REQ-CONF-USER-005",
    "REQ-CONF-USER-006",
    "REQ-CONF-USER-007",
    "REQ-CONF-USER-008",
    "REQ-CONF-USER-009",
    "REQ-CONF-USER-010",
    "REQ-CONF-USER-011",
    "REQ-CONF-USER-012",
    "REQ-CONF-USER-013",
    "REQ-CONF-USER-027",
    "REQ-CONF-USER-029",
    "REQ-CONF-USER-030"
  ],
  "lock_ids": [
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-GOV-001",
    "LOCK-IMPL-001",
    "LOCK-DOC-002"
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
    "DOC-CONST-002",
    "DOC-CONST-003",
    "DOC-CONST-004",
    "DOC-CONST-005",
    "DOC-SYS-014",
    "DOC-PROFILE-001",
    "DOC-PROFILE-004",
    "DOC-OPS-001",
    "DOC-CONF-002",
    "DOC-CONF-007",
    "DOC-CONF-018"
  ],
  "tags": [
    "architecture-decision",
    "user-lightweight",
    "hardware-envelope",
    "resource-governor",
    "zram",
    "heavy-job",
    "integrated-gpu",
    "minimum-vs-recommended",
    "endpoint-profile",
    "bounded-operation"
  ]
}
KOA:DOC-META:END -->

# ADR-017 — User Lightweight Hardware Profile

**ADR ID:** `ADR-017`  
**Status:** `accepted`  
**Decision class:** `major`  
**Decision owner:** `profile-architecture`  
**Owner decision:** `DEC-HW-001`  
**Canonicalized:** `2026-08-03`  
**Decision source:** Frozen cross-domain owner decision  
**Original acceptance date:** Not recorded in the retained source  
**Supersedes:** Not applicable  
**Superseded by:** Not applicable

## 1. Decision Summary

The `user_lightweight` primary profile uses a bounded endpoint hardware envelope intended for reliable local operation without requiring workstation, build-farm, hub, or control-plane capacity.

| Dimension | Minimum or required value | Recommended value |
| --- | --- | --- |
| Processor | 4 modern CPU cores | 6 modern CPU cores |
| Memory | 16 GiB RAM | 32 GiB RAM |
| Storage | 512 GB SSD | 1 TB SSD |
| Graphics | Integrated GPU is sufficient | No discrete GPU recommendation is introduced |
| Swap behavior | zram is required | Profile-owned tuning can vary |
| Concurrent heavy jobs | Maximum 1 | No higher recommended concurrency is introduced |

The active profile contract remains the canonical owner of these values. This ADR records the accepted rationale, boundaries, consequences, migration, and validation obligations.

## 2. Scope

### 2.1 Included scope

This decision applies to:

- the base `user_lightweight` primary profile;
- CPU, memory, storage, graphics, zram, and heavy-job admission;
- Resource Governor behavior required to preserve the envelope;
- health, readiness, degradation, diagnostics, backup, restore, and recovery under resource pressure;
- profile tests, evidence, installation planning, and support claims.

### 2.2 Excluded scope

This decision does not define:

- developer, sovereign, hub, build-farm, or control-plane hardware;
- requirements added by overlays;
- a CPU, GPU, storage, or machine vendor;
- one zram recipe, compression algorithm, filesystem, service manager, or container runtime;
- application-specific optional hardware;
- a Kubernetes, container, or discrete-GPU requirement.

### 2.3 Claim boundary

A hardware result applies only to the exact tested installation, profile version, authority set, component set, artifact set, and overlay composition.

Meeting the envelope does not alone establish complete profile conformance.

## 3. Canonical References

### 3.1 Owner decision and profile

- `generated/decision-index.json#DEC-HW-001`
- `generated/profile-catalog.json`
- `contracts/profiles/user-lightweight.profile.json`

### 3.2 Supporting decisions

- `DEC-PROFILE-001`
- `DEC-GOV-001`
- `DEC-CONTAINER-001`
- `DEC-K8S-001`
- `DEC-SHELL-001`

### 3.3 Related documents

- `DOC-SYS-014` — Resource Governor
- `DOC-PROFILE-001` — Profile Composition and Overlays
- `DOC-PROFILE-004` — User Lightweight
- `DOC-OPS-001` — Observability
- `DOC-CONF-018` — User Lightweight Conformance

### 3.4 Requirements and locks

The requirement and lock identifiers in the generated metadata define the traceability set. Their statements and executable validations remain registry-owned.

## 4. Context and Problem

### 4.1 Current state

kOA needs a credible local user profile that supports deterministic local behavior, component separation, navigation, bounded media work, backup, restore, artifact verification, and safe degradation.

A hardware-undefined profile would permit incompatible implementations to claim the same identity. Services could assume workstation capacity, background jobs could exhaust memory, and recommendations could be confused with minimum requirements.

### 4.2 Problem statement

The architecture needs a minimum low enough for a broadly attainable endpoint and high enough for reliable local operation.

The decision also needs explicit memory-pressure resilience and heavy-work admission. Raw capacity without resource governance does not prevent overload.

### 4.3 Decision necessity

The envelope affects profile identity, resource admission, service activation, degraded behavior, procurement, support, conformance, and evidence. Recipes and installers cannot independently own these values.

### 4.4 Source limitation

The retained source records the selected envelope but not the original option discussion or acceptance date. The alternative analysis below documents current architectural rationale without claiming an undocumented historical debate.

## 5. Decision Drivers

1. Reliable local operation on attainable modern hardware.
2. Clear separation from developer and server profiles.
3. Bounded operation during memory and workload pressure.
4. No mandatory discrete GPU.
5. No Kubernetes or container dependency.
6. Separate minimum and recommended values.
7. Measurable conformance evidence.
8. Profile-owned, change-controlled values.
9. Visible safe degradation.
10. Implementation choice behind stable observable behavior.

## 6. Considered Options

### 6.1 Option A — Balanced endpoint envelope

Use the retained values with zram and one-heavy-job admission.

**Benefits**

- measurable minimums;
- broad modern endpoint applicability;
- a meaningful lightweight profile;
- memory-pressure resilience;
- bounded heavy work;
- no discrete-GPU dependency;
- clear procurement and support targets.

**Costs**

- smaller deprecated machines do not receive full conformance;
- zram and Resource Governor validation are required;
- heavy work can queue;
- storage growth requires active limits.

**Result:** Selected.

### 6.2 Option B — Hardware-agnostic profile

Allow every implementation to decide what is sufficient.

**Benefits**

- maximum implementation freedom;
- installation attempts on smaller machines.

**Costs**

- incomparable claims;
- no support baseline;
- hidden service requirements;
- architecture authority moves to recipes and installers.

**Result:** Rejected because the profile would not be testable.

### 6.3 Option C — Lower minimum without required pressure controls

Use less capacity and make zram or heavy-job limits optional.

**Benefits**

- lower acquisition cost;
- broader installation reach.

**Costs**

- unstable memory and input-output behavior;
- hidden feature removal;
- inconsistent recovery;
- unreliable support expectations.

**Result:** Rejected because lightweight does not mean unbounded or unreliable.

### 6.4 Option D — Workstation-class baseline

Use developer-workstation capacity as the user minimum.

**Benefits**

- more headroom;
- greater parallelism.

**Costs**

- eliminates the lightweight profile purpose;
- increases cost and energy use;
- confuses endpoint and developer claims.

**Result:** Rejected because higher-capacity profiles already exist.

## 7. Decision

### 7.1 Selected option

`balanced_user_endpoint_envelope`

### 7.2 Minimum versus recommended

Minimum values determine the base hardware result.

Recommended values guide procurement and expected headroom but:

- remain separately reported;
- do not become mandatory failures;
- do not make a minimum-compliant host nonconformant;
- can change independently only when compatibility rules permit.

### 7.3 CPU

The profile requires four modern CPU cores and recommends six. The contract and tests define architecture compatibility and sustained operation without making a vendor list canonical.

### 7.4 Memory and zram

The profile requires 16 GiB physical memory and recommends 32 GiB.

zram is required as observable compressed-memory swap behavior. Sizing and tuning remain implementation choices within profile and operational constraints.

### 7.5 Storage

The profile requires 512 GB SSD-class storage and recommends 1 TB.

Evidence records usable capacity, health, free-space reserve, and profile-owned recovery relationships without mandating a filesystem or vendor.

### 7.6 Graphics

Integrated graphics are sufficient. The base profile has no discrete-GPU or GPU-compute requirement.

### 7.7 Heavy jobs

At most one heavy job is admitted concurrently. Applicable component and resource contracts classify heavy work.

Excess work is rejected, queued, paused, or deferred through bounded Resource Governor behavior.

### 7.8 Safe degradation

Under pressure:

- authoritative state remains protected;
- lower-priority work can be delayed;
- queues and retries remain bounded;
- health and work-class readiness remain distinct;
- degraded state is visible;
- no silent substitute or authority escalation occurs.

## 8. Canonical Ownership and Boundaries

### 8.1 Profile owner

`contracts/profiles/user-lightweight.profile.json` owns:

- minimum and recommended values;
- zram behavior;
- heavy-job maximum;
- profile resource budgets;
- hardware conformance assertions.

### 8.2 Resource authority

Resource Governor owns admission and enforcement of CPU, memory, input-output, queue, retry, process, and concurrency behavior. It consumes profile bounds without redefining them.

### 8.3 Component ownership

Each component owns its resource declarations, heavy-work classification, queue behavior, degradation, health, readiness, and cleanup.

A component cannot broaden the profile envelope.

### 8.4 Recipe boundary

Installation, zram, cgroup, service-activation, and scheduling recipes are non-authoritative unless explicitly adopted by the profile contract.

### 8.5 Forbidden ownership

Installers, dashboards, benchmarks, support documents, package scripts, and hardware-detection tools do not own profile values.

## 9. Profile and Deployment Effects

### 9.1 Base profile

The decision applies only to `user_lightweight` and does not establish a global endpoint minimum.

### 9.2 Overlays

| Overlay | Composition effect |
| --- | --- |
| `high_assurance` | Can add explicit compatible assurance, custody, encryption, or evidence requirements. |
| `sovereign_offline` | Can add explicit compatible offline storage, recovery, transfer, or retention requirements. |
| `appliance_shell` | Can change interface and service activation through explicit composition. |

Overlay outcomes remain distinct from the base result.

### 9.3 Containers

Containers are optional. Runtime use does not change the envelope or become an application dependency unless the profile explicitly adopts it.

### 9.4 Kubernetes

Kubernetes is not required for baseline installation, operation, validation, recovery, or administration.

### 9.5 Desktop

A maintained general-purpose desktop is permitted. Appliance-shell restrictions apply only after explicit overlay composition.

## 10. Security, Privacy, and Rights Effects

### 10.1 Security

Resource pressure does not justify disabling trust checks, exposing secrets, bypassing authorization, weakening component data boundaries, or activating unverified artifacts.

### 10.2 Privacy

Telemetry, diagnostics, swap behavior, temporary files, and pressure evidence remain classified, minimized, access-controlled, and free of secret values.

### 10.3 Rights and consent

The hardware profile introduces no consent, cultural-rights, disclosure, or publication authority. Resource pressure cannot remove applicable checks.

### 10.4 External services

External processing is not an automatic substitute for insufficient local hardware. Optional external operations remain user initiated and contract controlled.

## 11. Offline, Resource, and Operational Effects

### 11.1 Offline operation

The hardware result requires no network connectivity. Optional external capabilities can be unavailable while unrelated local core behavior continues.

### 11.2 Operational signals

Evidence and observability cover:

- CPU saturation;
- physical and available memory;
- zram state and pressure;
- storage capacity and health;
- input-output pressure;
- heavy-job admission and queues;
- process and retry bounds;
- health, readiness, and degradation.

### 11.3 Storage growth

Logs, caches, previews, temporary data, artifacts, backups, and receipts remain bounded. The storage minimum does not authorize unlimited retention.

### 11.4 Backup and restore

Backup and restore account for temporary space, input-output bounds, one-heavy-job admission, component ownership, restoration readiness, and recovery evidence.

### 11.5 Incidents

Resource exhaustion, zram failure, storage pressure, thermal throttling, and repeated admission failure are observable conditions handled through component and incident contracts.

## 12. Compatibility and Lifecycle

### 12.1 Compatibility class

`profile_specific_major_decision`

Compatible implementations meet both the profile values and observable bounded behavior.

### 12.2 Major-change triggers

A change is major when it alters a minimum, zram requirement, heavy-job maximum, graphics baseline, profile ownership, or compatibility semantics.

A recommendation-only correction can be minor when mandatory compatibility is unchanged.

### 12.3 Claim and artifact effects

Profile claims and resource-envelope evidence identify the exact profile version. Artifacts can declare compatibility requirements but cannot redefine the envelope.

### 12.4 Revalidation triggers

Revalidation follows hardware replacement, material memory or storage change, zram change, Resource Governor change, heavy-work classification change, profile version change, overlay change, or resource-relevant component and artifact change.

### 12.5 Identifier preservation

`ADR-017` and `DEC-HW-001` remain reserved. Semantic replacement uses new accepted authority and explicit supersession relationships.

## 13. Migration Plan

### 13.1 Preconditions

- `DEC-HW-001` is accepted;
- `user_lightweight` is active in the profile index;
- the profile contract can own values;
- Resource Governor can enforce relevant behavior;
- tests and evidence can be registered.

### 13.2 Steps

1. Register this ADR and decision relationship.
2. Materialize or update the profile contract.
3. Place all active values in profile-owned canonical fields.
4. Replace manually maintained tables with generated projections or references.
5. Align conformance, operations, installers, recipes, and support material.
6. Register tests and evidence.
7. Regenerate catalogs, matrices, impact reports, and AI contexts.
8. Validate the complete repository.
9. Activate the exact validated authority set last.

### 13.3 Source disposition

The `DEC-HW-001` hardware-envelope record in the frozen architecture is retained. This ADR expands only its `user_lightweight` portion without altering values.

### 13.4 Existing installations

An installation below the minimum can remain an unsupported or partial deployment, but it does not receive a complete base-profile claim.

## 14. Rollback and Forward Repair

### 14.1 Rollback triggers

Rollback or containment applies when a change:

- raises a hidden minimum;
- removes zram;
- admits multiple heavy jobs;
- requires a discrete GPU;
- makes containers or Kubernetes mandatory;
- turns recommendations into mandatory failures;
- breaks bounded degradation.

### 14.2 Rollback unit

The rollback unit includes profile contract, Resource Governor settings, service activation, heavy-work classifications, tests, evidence expectations, projections, and relevant recipes.

### 14.3 Rollback behavior

Restore the last valid profile and enforcement set, then revalidate health, readiness, queues, memory pressure, storage, and heavy-job admission.

### 14.4 Forward repair

Forward repair introduces a versioned compatible profile or component change when reverting would invalidate newer operational state. The claim remains blocked until evidence passes.

### 14.5 Last valid state

The last valid state is the most recent active profile contract and Resource Governor configuration supported by a complete passing evidence set for the tested installation.

## 15. Interfile Alignment Impact

### 15.1 Canonical objects

Affected or constrained objects include:

- ADR and decision registries;
- `user-lightweight.profile.json`;
- Resource Governor contract;
- requirements and locks;
- traceability, tests, and evidence.

### 15.2 Documents

| Document | Disposition |
| --- | --- |
| `DOC-PROFILE-001` | `reviewed_no_change` |
| `DOC-PROFILE-004` | `updated_or_generated_from_profile_contract` |
| `DOC-SYS-014` | `reviewed_for_resource_enforcement` |
| `DOC-OPS-001` | `reviewed_for_resource_signals` |
| `DOC-CONF-018` | `reviewed_no_change` |
| `DOC-ADR-017` | `created` |

### 15.3 Generated projections

Regenerate ADR, decision, profile, requirement, lock, test, evidence, traceability, hardware-envelope, impact, and `user_lightweight` AI-context projections.

### 15.4 Drift checks

Validation detects stale values, minimum/recommended inversion, missing units, wrong profile scope, hidden implementation minimums, inconsistent zram behavior, and inconsistent heavy-job maximums.

## 16. Validation and Evidence

### 16.1 Required tests

| Test ID | Purpose |
| --- | --- |
| `TEST-CONF-USER-HW-001` | Profile identity, version, and contract resolution |
| `TEST-CONF-USER-HW-002` | CPU, memory, and storage minimum/recommended semantics |
| `TEST-CONF-USER-HW-003` | Integrated-GPU sufficiency and no discrete-GPU requirement |
| `TEST-CONF-USER-HW-004` | zram presence and memory-pressure behavior |
| `TEST-CONF-USER-HW-005` | Maximum one-heavy-job admission |
| `TEST-CONF-USER-HW-006` | Optional containers and no Kubernetes dependency |
| `TEST-CONF-USER-HW-007` | Bounded degradation, health, readiness, and recovery |
| `TEST-CONF-USER-HW-008` | Traceability, generated alignment, and evidence completeness |

Every test requires a passing result.

### 16.2 Required evidence

| Evidence ID | Subject |
| --- | --- |
| `EVID-CONF-USER-HW-001` | Profile and authority versions |
| `EVID-CONF-USER-HW-002` | CPU, memory, and storage inventory |
| `EVID-CONF-USER-HW-003` | Graphics capability |
| `EVID-CONF-USER-HW-004` | zram and memory-pressure behavior |
| `EVID-CONF-USER-HW-005` | Heavy-job admission |
| `EVID-CONF-USER-HW-006` | Runtime topology |
| `EVID-CONF-USER-HW-007` | Degradation and recovery |
| `EVID-CONF-USER-HW-008` | Traceability and generated alignment |

### 16.3 Validation commands

```bash
python docs/tools/generate_docs.py --check
python docs/tools/check_canonical_ownership.py
python docs/tools/check_interfile_locks.py
python docs/tools/check_generated_content.py
python docs/tools/check_document_graph.py
python docs/tools/check_traceability.py
python docs/tools/compute_impact.py --check-clean
python docs/tools/build_ai_context.py --check
python docs/tools/check_clean_repository.py
python docs/tools/validate_docs.py
```

### 16.4 Decision-specific checks

The checks confirm profile identity, canonical ownership, minimum/recommended separation, hardware minimums, zram, one-heavy-job admission, integrated graphics, optional containers, no Kubernetes requirement, bounded pressure behavior, and generated-value alignment.

### 16.5 Acceptance criteria

1. The decision and ADR resolve as accepted.
2. `user_lightweight` resolves as one active primary profile.
3. The active profile contract contains the accepted envelope.
4. All eight tests pass.
5. All eight evidence items apply to the exact tested installation and profile version.
6. Generated projections match the profile contract.
7. No mandatory gap is hidden by recommendation status or aggregate scoring.
8. The authority index references the exact validated versions.

## 17. Consequences

### 17.1 Positive

- clear procurement and support baseline;
- comparable conformance;
- reliable local operation without workstation hardware;
- predictable memory-pressure behavior;
- bounded heavy work;
- no discrete-GPU, container, or Kubernetes dependency;
- clear minimum/recommended separation.

### 17.2 Negative

- machines below 16 GiB do not receive complete conformance;
- zram setup and testing are required;
- heavy work can wait;
- background throughput is constrained;
- envelope changes require compatibility review and renewed evidence.

### 17.3 Operational obligations

Operators monitor CPU, memory, zram, storage, input-output, queues, and heavy work, retaining capacity for update, backup, restore, and recovery.

### 17.4 Documentation obligations

Profile contracts, conformance documents, projections, Resource Governor behavior, tests, evidence, recipes, and AI contexts remain aligned.

### 17.5 Accepted trade-off

The profile favors predictable bounded operation over maximum installation reach on smaller unsupported hardware.

## 18. Rejected Alternatives

| Alternative | Reason |
| --- | --- |
| Hardware-agnostic profile | Cannot produce comparable claims or predictable operation |
| Lower minimum without zram | Increases instability and hidden capability removal |
| Workstation minimum | Eliminates the lightweight profile distinction |
| Discrete-GPU requirement | Unnecessary for the accepted core profile |
| Unlimited heavy-job concurrency | Violates bounded-resource behavior |
| Kubernetes-dependent endpoint | Violates endpoint portability and profile scope |

A rejected alternative needs a new accepted decision and superseding ADR before implementation.

## 19. Exceptions and Waivers

No exception is embedded in this ADR.

A temporary deviation identifies the exact hardware field, tested installation, profile version, validity period, compensating controls, affected capabilities, tests, evidence, review, and expiry.

An exception does not change the base profile or create a general conformance claim.

## 20. Implementation Guidance

This section is non-normative.

Useful patterns include:

- maintained operating-system zram management;
- cgroup or equivalent resource controls;
- one heavy-job resource class;
- bounded worker pools and queues;
- storage free-space reserves;
- lower-priority background indexing;
- pressure-aware health and readiness;
- profile-selected service activation;
- hardware inventory in the claim evidence package.

Benchmarks inform tuning but do not replace canonical values or conformance tests.

## 21. Decision Record

### 21.1 Authority record

- Decision: `DEC-HW-001`
- Decision status: `accepted`
- Decision owner: `profile-architecture`
- ADR: `ADR-017`
- ADR status: `accepted`

### 21.2 Review record

| Role | Identifier | Result | Date |
| --- | --- | --- | --- |
| Frozen architecture source | `DEC-HW-001` | `accepted` | Original date not recorded |
| Profile index | `user_lightweight` | `active_primary` | `2026-08-03` |
| Conformance alignment | `DOC-CONF-018` | `aligned` | `2026-08-03` |
| Local structural validation | `automated` | `pass` | `2026-08-03` |
| Authority activation | `authority-registry` | `not_claimed_by_single_artifact` | `2026-08-03` |

### 21.3 Machine-readable change summary

```json
{
  "change_class": "canonicalized_frozen_decision",
  "decision_ids": ["DEC-HW-001", "DEC-PROFILE-001", "DEC-GOV-001", "DEC-CONTAINER-001", "DEC-K8S-001", "DEC-SHELL-001"],
  "adr_ids": ["ADR-017"],
  "profile_ids": ["user_lightweight"],
  "modified_canonical_refs": [
    "generated/decision-index.json",
    "generated/decision-index.json",
    "contracts/profiles/user-lightweight.profile.json",
    "contracts/components/resource-governor.component.json",
    "generated/traceability.json"
  ],
  "requirement_ids": ["REQ-CONF-USER-001", "REQ-CONF-USER-002", "REQ-CONF-USER-003", "REQ-CONF-USER-004", "REQ-CONF-USER-005", "REQ-CONF-USER-006", "REQ-CONF-USER-007", "REQ-CONF-USER-008", "REQ-CONF-USER-009", "REQ-CONF-USER-010", "REQ-CONF-USER-011", "REQ-CONF-USER-012", "REQ-CONF-USER-013", "REQ-CONF-USER-027", "REQ-CONF-USER-029", "REQ-CONF-USER-030"],
  "lock_ids": ["LOCK-PROFILE-001", "LOCK-PROFILE-002", "LOCK-GOV-001", "LOCK-IMPL-001", "LOCK-DOC-002"],
  "test_ids": ["TEST-CONF-USER-HW-001", "TEST-CONF-USER-HW-002", "TEST-CONF-USER-HW-003", "TEST-CONF-USER-HW-004", "TEST-CONF-USER-HW-005", "TEST-CONF-USER-HW-006", "TEST-CONF-USER-HW-007", "TEST-CONF-USER-HW-008"],
  "evidence_ids": ["EVID-CONF-USER-HW-001", "EVID-CONF-USER-HW-002", "EVID-CONF-USER-HW-003", "EVID-CONF-USER-HW-004", "EVID-CONF-USER-HW-005", "EVID-CONF-USER-HW-006", "EVID-CONF-USER-HW-007", "EVID-CONF-USER-HW-008"],
  "local_validation_status": "pass",
  "authority_activation_claimed": false
}
```

## 22. Supersession and Historical Integrity

When superseded:

1. this ADR changes to `superseded`;
2. the replacement references `ADR-017`;
3. the replacement decision links to `DEC-HW-001`;
4. historical envelopes and evidence remain visible;
5. claims retain the profile version they tested;
6. projections and AI contexts are regenerated;
7. active claims revalidate;
8. retired identifiers remain reserved.

Historical evidence remains valid for its exact profile version and installation, not automatically for a replacement envelope.
