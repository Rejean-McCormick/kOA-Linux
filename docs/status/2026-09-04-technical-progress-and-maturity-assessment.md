<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-STATUS-003",
  "document_class": "explanatory_markdown",
  "status": "active",
  "authority_participation": "non_authoritative",
  "language": "en",
  "layer": "governance",
  "scope": [
    "global"
  ],
  "canonical_refs": [],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [
    "DOC-STATUS-000",
    "DOC-STATUS-001",
    "DOC-STATUS-002"
  ],
  "tags": [
    "status",
    "technical-maturity",
    "release-readiness",
    "assessment",
    "system-closure",
    "component-build-closure",
    "qualification"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# Koali Technical Progress and Maturity Assessment

**Assessment date:** 2026-09-04  
**Current status:** Advanced Beta — System Closure & Qualification  
**Estimated engineering maturity:** ~85–87%  
**Estimated Release Candidate readiness:** ~60–65%

> This document is a technical progress checkpoint. It is not a Release Candidate declaration. Percentages are engineering estimates rather than mathematical completion metrics, and blocked qualification gates are not counted as passes.

## Executive summary

Koali has completed a significant component-build and development-environment closure cycle since the 2026-08-28 checkpoint.

The most important new result is that all eight first-party component build targets now produce their component bundles through the supported Koali Control Panel workflow. The build path is no longer dependent on ad hoc terminal preparation for Python, Rust, Cargo dependency caching, or the native compiler/linker toolchain.

The current build result is:

```text
audit-broker                    PASS
governance-policy-runtime       PASS
identity-and-trust              PASS
koa-mediatheque                 PASS
koa-node-agent                  PASS
kristal-runtime                 PASS
publication-gateway             PASS
resource-governor               PASS

component bundles               8 / 8
```

This closes a blocker that was explicitly present in the previous maturity assessment.

The remaining critical path is now above the component-build layer: authority-derived assembly inputs, subsystem source closure, package resolution, resolved deployment-plan materialization, B-0092/image projection, reproducible system-image production, QEMU qualification, recovery proof, and complete Release Set evidence.

The most accurate current classification remains:

**Advanced Beta — System Closure & Qualification**

The project has advanced materially in engineering closure, but it has not yet crossed the system-image and machine-qualification boundary required for pre-RC status.

## Progress since the previous checkpoint

### 1. Component build closure: 8/8

All eight declared component build targets have now been built successfully from the WSL Linux workspace through the Control Panel.

The seven Python-oriented components passed first:

- Audit Broker;
- Governance Policy Runtime;
- Identity and Trust;
- kOA Mediatheque;
- Kristal Runtime;
- Publication Gateway;
- Resource Governor.

The remaining Rust component, kOA Node Agent, initially exposed a sequence of environment prerequisites. Those prerequisites were fixed at the orchestration layer rather than handled as undocumented manual steps.

The final `koa-node-agent` build completed successfully with the same deterministic build workflow used by the component builder.

This is an important maturity change: component build closure is now demonstrated rather than inferred from source completeness.

### 2. Koali Control Panel build-environment closure

The Control Panel was advanced incrementally, with each validated step preserved rather than replaced by manual instructions.

The current validated reference is:

**Koali Control Panel 2.4.5**

The relevant progression was:

| Version | Closure achieved |
|---|---|
| 2.4.1 | Correct Ubuntu 24.04 OVMF/UEFI discovery |
| 2.4.2 | Correct internal kOA component-builder invocation |
| 2.4.3 | Repository-declared Rust toolchain provisioning |
| 2.4.4 | Cargo locked dependency cache preparation and offline verification |
| 2.4.5 | Native `cc` compiler/linker provisioning and compile/link probe |

The resulting development preparation path now covers:

```text
Windows authoritative source
        ↓
WSL workspace refresh
        ↓
Python / uv environment
        ↓
setuptools / wheel build prerequisites
        ↓
Rust toolchain from rust-toolchain.toml
        ↓
cargo / clippy / rustfmt
        ↓
Cargo.lock dependency cache
        ↓
offline Cargo verification
        ↓
native compiler/linker
        ↓
component builds
```

The current repository-declared Rust toolchain is provisioned exactly rather than guessed:

```text
rustc 1.85.1
cargo 1.85.1
clippy installed
rustfmt installed
```

The native build preflight also validates an actual temporary C compile/link operation rather than checking only for the presence of an executable.

### 3. Deterministic and offline-oriented build behavior

The component build path preserves the repository's fail-closed behavior.

For the Rust component:

- the build uses `Cargo.lock`;
- the actual component build remains `--locked`;
- the actual component build remains `--offline`;
- dependency download is performed only during environment preparation when the locked cache is incomplete;
- the cache is then explicitly rechecked in offline mode before the development environment is considered ready.

This preserves a useful boundary between environment preparation and deterministic component production.

### 4. Interface-first operational workflow established

A project operating rule has now been established and exercised:

> If a recurring manual prerequisite is required for the normal Koali workflow, it should be captured by the Control Panel once understood and validated.

This has already converted several transient troubleshooting steps into repeatable interface-driven behavior.

The Control Panel does not autonomously clean, reset, stash, commit, or otherwise decide repository Git state. Strict source cleanliness remains the responsibility of the reproducible component builder where that requirement is semantically appropriate.

This separation is now working in practice.

### 5. LevelUpDiag debugging model improved

LevelUpDiag-Koali 2.1.0 separates diagnostic execution from formal conformance.

The primary DEBUG campaign is designed so that independent diagnostic levels continue even when a local level is blocked or non-conformant. Repository formalities are no longer allowed to hide the actual system-under-test blockers.

The latest captured DEBUG campaign established that the remaining high-level blockers were concentrated in QEMU/runtime qualification rather than repository cleanliness.

The earlier N01 Cargo warning is now stale with respect to the current prepared WSL environment because Rust/Cargo has since been provisioned successfully. A new LevelUpDiag run is required before that warning can be considered formally cleared in diagnostic evidence.

### 6. QEMU infrastructure readiness

The QEMU infrastructure layer is prepared:

```text
qemu-system-x86_64     available
OVMF / UEFI            available
Ubuntu 24.04 path      correctly detected
network policy         off
```

The remaining QEMU blockers are not emulator installation problems.

They are system-product inputs that do not yet exist or are not yet materialized, including:

- a canonical built system image;
- release identity expectations;
- effective runtime/profile context;
- session/compositor/navigation expectations;
- confinement expectations;
- offline runtime expectations.

This is the intended fail-closed behavior.

## Current maturity by area

| Area | Estimated maturity |
|---|---:|
| Architecture and canonical contracts | 96–98% |
| Profile authority and composition | 90–95% |
| Internal component implementation | 93–96% |
| First-party component build closure | 100% for the 8 declared build targets |
| Interfaces and adapters | 84–88% |
| Component/repository-level validation | 94–96% |
| Development/build environment automation | 95%+ |
| Packaging and release engineering machinery | 83–87% |
| Linux host, boot and recovery machinery | 74–80% |
| Authority-derived deployment-plan materialization | 55–60% |
| End-to-end system integration | 58–63% |
| Security/offline machine qualification | 40–50% |
| Overall engineering maturity | ~85–87% |
| RC readiness | ~60–65% |

These estimates deliberately distinguish implementation closure from candidate qualification.

Closing all component builds is a substantial engineering milestone, but it does not substitute for producing and qualifying a complete bootable system image.

## Current pipeline state

The intended authority and build sequence remains:

```text
canonical profile + overlays
        ↓
deterministic effective profile
        ↓
component bundles
        ↓
8 / 8 COMPLETE
        ↓
subsystem source/bundle closure
        ↓
deterministic package resolution
        ↓
authority-derived resolved deployment plan
        ↓
B-0092 / image manifest projection
        ↓
reproducible inactive system-image candidate
        ↓
independent recovery material
        ↓
QEMU boot
        ↓
system / security / confinement qualification
        ↓
offline qualification
        ↓
recovery / rollback / last-known-good proof
        ↓
SBOM + provenance + compatibility + signatures
        ↓
complete compatible Release Set
        ↓
staging and activation
```

The component-bundle stage is now closed.

The next unresolved stage is assembly/input closure.

## Current blockers before pre-RC

Koali should not yet be classified as pre-RC.

The remaining critical sequence is now:

1. run the assembly preflight and expose the exact current blockers without bypassing them;
2. regenerate the effective profile if it is absent from the refreshed WSL workspace;
3. resolve the required subsystem source locks and subsystem bundle inputs without transferring subsystem authority;
4. complete deterministic package resolution and root filesystem materialization evidence;
5. materialize the authority-derived `resolved-plan.json`;
6. render B-0092 and the image manifest from closed inputs;
7. build a reproducible inactive system-image candidate;
8. produce and independently verify recovery material;
9. populate the QEMU runtime context from actual generated system/profile artifacts rather than invented values;
10. boot the candidate under the supported QEMU path;
11. pass machine-observed system, security, and confinement validation;
12. pass disconnected/offline machine validation;
13. prove failed activation, rollback, last-known-good, restore, and forward-repair behavior;
14. complete SBOM, provenance, compatibility, signatures, and required release evidence;
15. construct and verify a complete compatible Release Set;
16. stage and activate only after all mandatory gates pass.

## Immediate next engineering checkpoint

The next supported action is the Control Panel assembly preflight:

```text
Build
  → Assemble --check
```

The purpose of this step is to observe the exact assembly blockers after component closure without prematurely attempting to build the final system image.

`Build System Image` and `BUILD + BOOT` remain premature until the assembly and image inputs are closed.

## Release interpretation

Koali is now substantially closed at the architecture, contract, component implementation, component build, developer-environment, diagnostic, and emulator-infrastructure layers.

The project has moved past the question of whether its first-party components can be built reproducibly in the supported development environment.

The remaining question is whether those closed component and subsystem inputs can be assembled into one complete, authority-derived, reproducible, bootable, recoverable, offline-capable, and verifiably releasable system.

> **Koali: all first-party component build targets are now closed; the remaining work is system assembly, image production, machine qualification, recovery proof, and Release Set closure.**

## Recommended public status

**Advanced Beta — System Closure & Qualification**

Suggested short description:

> Koali is in advanced beta. Its contract-first architecture, profile model, first-party components, component build pipeline, development environment automation, diagnostics, and QEMU infrastructure are substantially closed. All eight declared component build targets now produce successfully through the supported interface-driven workflow. Current work is focused on authority-derived assembly, subsystem and package closure, reproducible system-image production, QEMU system/security/offline qualification, recovery proof, and complete Release Set evidence. Koali is not yet a Release Candidate.
