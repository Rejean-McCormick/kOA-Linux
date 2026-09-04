<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-STATUS-002",
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
    "DOC-STATUS-001"
  ],
  "tags": [
    "status",
    "technical-maturity",
    "release-readiness",
    "assessment",
    "system-closure",
    "system-qualification"
  ],
  "edit_policy": "manual"
}
KOA:DOC-META:END -->

# Koali Technical Maturity Assessment

**Assessment date:** 2026-08-28  
**Current status:** Advanced Beta — System Closure & Qualification  
**Estimated engineering maturity:** ~82–84%  
**Estimated Release Candidate readiness:** ~60–65%

> This assessment is a technical maturity checkpoint. It is not a Release Candidate declaration. Percentages are engineering estimates, not mathematical completion metrics, and blocked qualification gates are not counted as passes.

## Executive summary

Koali has completed a substantial integration-hardening cycle since the 2026-08-27 checkpoint. The strongest progress is in contract closure, profile composition, deterministic validation, repository tooling, fail-closed image/release boundaries, and observability of the remaining build pipeline.

The remaining critical path is narrower and better defined, but it is still release-critical: Koali does not yet have a fully authority-derived resolved deployment plan, a complete B-0092/image input closure, a qualified bootable system image, machine-observed security/offline evidence, or a complete compatible Release Set proven through activation and recovery.

The most accurate current classification is:

**Advanced Beta — System Closure & Qualification**

This is a maturity increase in implementation closure and diagnostic precision, not evidence that the product has entered pre-RC. RC readiness therefore remains deliberately conservative.

## Evidence since the previous checkpoint

### Validated repository gates on the working checkout

The latest user-run validation cycle established:

- `docs/tools/validate_docs.py`: pass, including 10/10 profile authority documents;
- official contracts gate: pass with 19 contract tests;
- profile and overlay resolution: 39 passed;
- touched profile tests: 8 passed;
- touched reproducibility tests: 6 passed;
- repository tooling suite: 94 passed and 4 skipped on Windows.

The tooling skips are Windows symlink-capability cases. They do not establish system qualification, but they are not product-logic regressions.

### Patch-level validation completed during this cycle

Additional controlled validation of the profile/image and diagnostic updates established:

- targeted profile/schema/assembly/reproducibility validation: 92 passed;
- focused tooling validation around CLI/image surfaces: 36 passed;
- official contracts gate remained green with 19 passed;
- generated-content, profile inheritance, AI boundary, interfile locks, traceability, decision closure, unresolved-state, security architecture, and UCKK boundary checks passed;
- after extending the public pipeline diagnostic surface, the complete tooling suite passed with 101 tests in the reconstructed validation checkout.

These checks validate the implementation changes and fail-closed behavior. They do not replace QEMU, activation, recovery, or Release Set qualification on a real candidate image.

## Architecture and implementation closure achieved

### Profile authority and composition

The profile migration and compatibility work is now substantially closed for the exercised contracts:

- all 10 profile authority documents load under the current profile schema;
- exactly one primary profile remains required;
- overlay compatibility is reciprocal and fail-closed;
- undeclared or one-sided compatibility does not become compatibility by inference;
- `appliance_shell` again carries its declared Linux graphical-seat and base-capability prerequisites;
- effective-profile output remains a deterministic derived projection rather than independent authority;
- generated profile projections are regenerated from canonical sources rather than hand-edited.

### Image and release fail-closed boundaries

The image pipeline now carries the declared disk-backend protocol and inactive-staging constraints, while preserving:

```text
status = blocked_missing_assembly_and_component_bundles
activation_ready = false
```

The rootfs reproducibility tests now conform to the strict package-resolution contract rather than weakening the builder. The bundle and release candidate command surfaces also fail closed when the repository lacks the complete authority or envelope required to construct a real offline bundle or Release Set.

No change in this cycle grants activation authority early.

### Pipeline observability

The public `koa diagnose` surface was extended with a read-only pipeline mode. It observes the profile-to-release path without creating plans, bundles, images, compatibility, evidence, signatures, or release authority.

Controlled validation of:

```text
koa diagnose --pipeline --profile sovereign-linux-node --json
```

reported the current pipeline as `blocked` with 18 explicit blocker records. The blockers are concentrated in the expected unresolved stages: component bundle closure, subsystem source/bundle closure, package resolution, the authority-derived resolved plan, B-0092/image readiness, and release evidence/Release Set eligibility.

This is an improvement in observability, not a bypass. Missing authority remains missing authority.

## Latest LevelUpDiag-Koali checkpoint

The latest captured LevelUpDiag campaign reported:

| Level | Result | Interpretation |
|---|---|---|
| N00 Control Panel | PASS | LevelUpDiag self-check passed |
| N01 Environment | WARN | Optional `cargo` executable was unavailable |
| N02 Repository | WARN | The worktree contained tracked or untracked development changes |
| N03 Documentation | PASS | Public documentation validation passed |
| N04 Contracts | PASS | Public contract validation passed |
| N05 Components | PASS | Public component validation passed |
| N06 Integrations | SKIP | Optional integration command was not configured |
| N07 Profiles | SKIP | `commands.profiles` was still empty in this captured campaign |
| N08 Security | BLOCKED | Static security checks passed, but QEMU confinement qualification lacks the required candidate image and expectations |
| N09 Offline | BLOCKED | Offline QEMU qualification lacks the required candidate image and declared offline expectations |
| N10 System | BLOCKED | System QEMU qualification lacks the required candidate image and declared boot/session expectations |
| N11 Delivery | PASS | LevelUpDiag was absent from the delivery target |

The N08, N09, and N10 outcomes are correct fail-closed results. They must not be reported as passes.

After this captured campaign, a LevelUpDiag local configuration was prepared to route N07 to the public read-only pipeline diagnostic. That configuration change is not counted here as executed N07 evidence because the supplied campaign predates it.

## Current pipeline state

The intended order remains:

```text
canonical profile + overlays
  ↓
deterministic effective profile
  ↓
component/subsystem/package build and verification inputs
  ↓
authority-derived resolved deployment plan
  ↓
B-0092 / image manifest projection
  ↓
inactive candidate system image + independent recovery material
  ↓
SBOM + provenance + compatibility + required evidence
  ↓
signature
  ↓
staging + QEMU/system/security/offline tests
  ↓
complete compatible Release Set
  ↓
activation
```

The current implementation is intentionally blocked in the middle of this chain. The remaining work is not to relax a gate; it is to supply and verify the authority that the existing gates correctly require.

## Maturity by area

| Area | Estimated maturity |
|---|---:|
| Architecture and canonical contracts | 96–98% |
| Profile authority and composition | 90–95% |
| Internal components | 88–92% |
| Interfaces and adapters | 82–87% |
| Component/repository-level validation | 92–95% |
| Packaging and release engineering machinery | 80–85% |
| Linux host, boot and recovery machinery | 72–78% |
| Authority-derived deployment-plan materialization | 55–60% |
| End-to-end system integration | 55–60% |
| Security/offline machine qualification | 40–50% |
| Overall engineering maturity | ~82–84% |
| RC readiness | ~60–65% |

The estimates deliberately separate code/contract maturity from candidate qualification. A well-implemented blocked gate increases confidence in architecture but does not itself increase release evidence.

## Strongest areas

### Contract-first boundaries

Koali now has strong evidence that the exercised contracts, generated projections, profile compatibility rules, security ownership rules, and repository tooling agree on the same fail-closed model.

### Determinism and non-inference

The system increasingly distinguishes canonical authority from derived projections. Effective profiles, plans, manifests, and diagnostics are not permitted to invent missing runtime commands, package identities, membership, compatibility, signatures, or evidence.

### Diagnostic precision

The remaining release path is now observable through stable public validation surfaces and LevelUpDiag orchestration. This makes the next engineering work more targeted while preserving kOA-Linux as the authority owner.

## Main blockers before pre-RC

Koali should not yet be classified as pre-RC. The remaining closure sequence is:

1. close required component bundle inputs from their owning contracts/builds;
2. resolve required subsystem source locks and bundle inputs without transferring subsystem authority;
3. complete deterministic package-resolution and rootfs materialization evidence;
4. materialize the authority-derived `resolved-plan.json`;
5. render B-0092 and the image manifest from that closed plan;
6. build a reproducible inactive system-image candidate;
7. produce and independently verify recovery material;
8. boot the candidate under the supported QEMU qualification path;
9. pass machine-observed system, security, and confinement validation;
10. pass disconnected/offline machine validation;
11. prove failed activation, rollback, last-known-good, restore, and forward repair;
12. complete SBOM, provenance, compatibility, signature, and required evidence;
13. construct and verify a complete compatible Release Set;
14. stage and activate only after all mandatory gates pass.

## Release interpretation

Koali is substantially implemented at the architecture, contract, component, tooling, and validation-framework layers. The project has moved from broad integration cleanup toward a specific system-closure problem.

The remaining milestone is not another documentation or test-count milestone. It is the production and proof of one complete, reproducible, bootable, recoverable, compatible Release Set under the existing authority model.

> **Koali: the repository-level architecture is largely closed; the complete bootable and recoverable release still has to be materialized and proven.**

## Recommended public status

**Advanced Beta — System Closure & Qualification**

Suggested short description:

> Koali is in advanced beta with its contract, profile, component, tooling, and validation foundations substantially closed. Current work is concentrated on authority-derived deployment-plan materialization, reproducible system-image production, QEMU system/security/offline qualification, recovery proof, and complete Release Set closure. It is not yet a Release Candidate.
