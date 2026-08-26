<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-ROOT-CODE-ALIGNMENT",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": ["global"],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/terminology.contract.json",
    "contracts/subsystems/konnaxion.subsystem.json",
    "contracts/subsystems/orgo.subsystem.json",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "contracts/components/kristal-runtime.component.json",
    "contracts/artifact-contracts/language-pack.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": ["DOC-SYS-000", "DOC-CONST-013", "DOC-SYS-013", "DOC-LIFE-009"],
  "tags": ["alignment", "implementation", "contracts", "subsystems", "language", "kristal"]
}
KOA:DOC-META:END -->

# kOA-Linux — Code and Contract Alignment Notes

## Purpose

This is one technical alignment note. It identifies implementation/contracts that should converge with the current kOA-Linux architecture. The supplied package is documentation/contracts rather than a complete kOA-Linux application source snapshot, so implementation-path observations are contract-driven unless the file exists in this corpus.

## 1. Treat integrated ecosystem systems as subsystems, not native components

Konnaxion, Orgo and SemantiK Architect have active subsystem contracts and official documentation mounts. Runtime/deployment code should resolve those subsystem identities rather than assuming they are native kOA-Linux component owners.

Host responsibilities include process lifecycle, resources, trust exposure, storage/network exposure, artifact admission, health, backup coordination and degradation. Internal domain/workflow/API semantics remain with the subsystem.

## 2. Keep subsystem references out of the native component catalog

The generated component catalog is built from `contracts/components/*.component.json` and represents native kOA-Linux component contracts. Konnaxion, Orgo, SemantiK Architect, Ariane and SenTient instead have `contracts/subsystems/*.subsystem.json` boundaries.

Implementation/configuration must not recreate synthetic references such as `generated/component-catalog.json#/components/konnaxion` or `.../semantik_architect_runtime` when no corresponding native component contract exists. Use the subsystem contract or a specifically defined host-local native component contract.

## 3. Keep SemantiK Architect planner-first and backend-flexible

The current Architect documentation defines the runtime around:

```text
normalization → planner → PlannedSentence → ConstructionPlan
→ lexical resolution → renderer backend → SurfaceResult
```

GF/PGF is one backend/tooling family. kOA-Linux code should not implement a separate GF-first architecture or make PGF mandatory for every Architect deployment.

The updated `language-pack.schema.json` permits a declared generic backend asset set while retaining explicit PGF assets for GF-backed packs. Implementers should align pack builders, validators and activation code with the declared backend rather than hard-coding `gf_wordbench` / `compiled_pgf_required` as universal truth.

## 4. Align language-pack discriminator and artifact class

The previous language-pack schema used `artifact_class = language_runtime_pack` while the artifact-class registry and example used `language_pack`. The updated contract uses `language_pack`.

Any pack builder, verifier, fixture, release validator, database enum or activation service still using `language_runtime_pack` as the kOA artifact-class discriminator should be updated or given an explicit compatibility mapping at the boundary.

## 5. Preserve Kristal system vs local Kristal Runtime distinction

`kristal_runtime` is a native kOA-Linux component. **Kristal is the broader epistemic ecosystem system.**

Code around Runtime Pack handling should keep these layers separate:

```text
Kristal Specification / implementation
    owns artifact semantics

kOA-Linux artifact boundary
    verifies/adopts a candidate locally

kristal_runtime
    owns local verification/compatibility/active-pack/rollback/runtime state
```

Do not put Orgo workflow, Konnaxion domain state, policy authorization, resource scheduling or host privilege inside `kristal_runtime`.

## 6. Preserve scoped Runtime Pack discriminators

Kristal uses its own manifest discriminator (`artifact_type = runtime_pack_manifest`) while kOA-Linux can classify the platform artifact as `artifact_class = runtime_pack`. Code should treat these as different scoped fields rather than forcing one global enum.

## 7. kOA Spaces `module` means interface contribution, not architecture ownership

Any implementation that reads `module_interface_manifest` or renders the module selector should treat `module` as a presentation contribution identity. It must not infer:

- native component ownership;
- business authorization;
- workflow ownership;
- host privilege;
- resource admission;
- release activation authority.

## 8. Mount official subsystem documentation without copying it

The validator currently reports absent reserved mounts for independently owned subsystems. The final development/release workspace should mount/link the official docs for Konnaxion, Orgo, SemantiK Architect, Ariane, SenTient and kOA Spaces at the reserved `docs/subsystems/*` paths.

Do not copy internal subsystem documentation into kOA-Linux and then evolve it independently.

## 9. Keep host authorization, resource admission and business authority separate

Implementation paths that activate artifacts or perform host-sensitive work should preserve the current separation:

```text
identity/trust result
≠ policy authorization
≠ resource grant
≠ privileged host operation
≠ component/domain mutation
```

A successful resource admission does not authorize activation. A policy decision does not perform the activation. A receipt does not replace the active-state record.

## 10. Keep offline behavior fail-closed

Offline/degraded code should continue from already admitted local state where the active profile permits it. It should not:

- bypass trust;
- invent a substitute subsystem;
- fetch network content as a hidden side effect;
- invoke external AI silently;
- activate an unverified candidate;
- transfer domain authority to a platform fallback.

## 11. Re-run the documentation/contracts validators with implementation changes

The documentation corpus already provides `docs/tools/validate_docs.py` and generated catalogs. Contract-affecting implementation changes should stay consistent with those machine-readable sources and their conformance checks.
