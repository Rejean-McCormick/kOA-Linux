<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-013",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/language_runtime",
    "contracts/subsystems/semantik-architect.subsystem.json",
    "contracts/artifact-classes.contract.json#/artifact_classes/language_pack",
    "contracts/release-channels.contract.json#/channels/knowledge",
    "generated/profile-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/evidence-catalog.json"
  ],
  "decision_ids": [
    "DEC-COMP-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-AI-001",
    "DEC-REL-001",
    "DEC-HW-001"
  ],
  "requirement_ids": [
    "REQ-SYS-LANG-001",
    "REQ-SYS-LANG-002",
    "REQ-SYS-LANG-003",
    "REQ-SYS-LANG-004",
    "REQ-SYS-LANG-005",
    "REQ-SYS-LANG-006",
    "REQ-SYS-LANG-007",
    "REQ-SYS-LANG-008",
    "REQ-SYS-LANG-009",
    "REQ-SYS-LANG-010",
    "REQ-SYS-LANG-011",
    "REQ-SYS-LANG-012",
    "REQ-SYS-LANG-013",
    "REQ-SYS-LANG-014",
    "REQ-SYS-LANG-015",
    "REQ-SYS-LANG-016",
    "REQ-SYS-LANG-017",
    "REQ-SYS-LANG-018",
    "REQ-SYS-LANG-019",
    "REQ-SYS-LANG-020"
  ],
  "lock_ids": [
    "LOCK-COMP-002",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-DATA-001",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-DEV-001",
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-CON-006",
    "DOC-SYS-000",
    "DOC-SYS-002",
    "DOC-SYS-003",
    "DOC-SYS-004",
    "DOC-SYS-006",
    "DOC-SYS-008",
    "DOC-SYS-009"
  ],
  "tags": [
    "language-runtime",
    "semantik-architect",
    "gf-wordbench",
    "pgf",
    "deterministic-rendering",
    "offline",
    "language-pack"
  ]
}
KOA:DOC-META:END -->

# SemantiK Architect System Boundary

## 1. Purpose

This document defines the **kOA-Linux platform boundary** for SemantiK Architect. It does not redefine SemantiK Architect's internal NLG architecture.

SemantiK Architect is an independently owned planner-centered multilingual NLG ecosystem system. Its current architecture centers on:

```text
request / semantic input
→ normalization
→ planner
→ PlannedSentence
→ ConstructionPlan
→ lexical resolution
→ renderer backend
→ SurfaceResult
→ public response mapping
```

GF/PGF is one renderer/tooling family among supported backend classes. kOA-Linux therefore treats GF-backed runtime assets as one supported packaging/deployment profile rather than the universal definition of Architect.

## 2. Ownership

### SemantiK Architect owns

- public generation semantics and API contract;
- request/frame normalization;
- planner and sentence intent;
- `PlannedSentence`;
- `ConstructionPlan`;
- lexicon and lexical resolution;
- renderer selection;
- renderer/backend semantics, including GF/PGF, family renderers, and safe-mode behavior;
- `SurfaceResult`;
- language/construction capability and quality semantics;
- its internal build/test/tooling architecture.

### kOA-Linux owns or mediates

- deployment-profile membership;
- local process/service lifecycle;
- resource admission and limits;
- identity/trust boundary;
- network/storage exposure;
- admission and verification of declared runtime artifacts;
- local activation/rollback where a language/runtime artifact contract assigns those transitions to the host;
- health/readiness integration;
- backup/restore coordination;
- offline availability and safe degradation at the platform boundary.

The host does not rewrite Planner, ConstructionPlan, renderer, lexicon, or API semantics.

## 3. Public/runtime boundary

The current Architect public generation surface is centered on:

```text
POST /api/v1/generate/{lang_code}
```

kOA-Linux can expose, proxy, supervise, health-check, resource-bound, or isolate that service according to the active profile. It does not invent an alternate generation API.

## 4. Runtime assets

A kOA language-pack boundary can package runtime assets needed by an Architect deployment. The package declares the backend/resource assets it actually contains.

Supported package shapes can include, according to the Architect version/profile:

- GF/PGF assets;
- family-renderer resources;
- safe-mode resources;
- lexicon/runtime data;
- companion manifests/configuration;
- validation/compatibility evidence.

A GF-backed pack remains valid when declared, but `compiled PGF` is not a universal requirement for every SemantiK Architect runtime package.

## 5. Platform lifecycle

When kOA-Linux owns a local artifact transition for an Architect runtime asset, the lifecycle remains separated:

```text
receive
→ quarantine
→ verify integrity/provenance
→ evaluate compatibility
→ admit/stage
→ activate atomically when applicable
→ health/readiness check
→ rollback or forward repair
```

Publication or transfer never implies activation. A failed candidate does not overwrite the last valid local state.

## 6. Offline behavior

Offline operation can continue with already admitted local Architect runtime assets and local dependencies permitted by the active profile. kOA-Linux does not invoke an undeclared compiler, external AI service, network lookup, or backend substitution merely because connectivity is unavailable.

## 7. Data authority

The calling application retains ownership of the structured/domain facts it submits. Architect owns linguistic planning/realization state for the request. kOA-Linux owns only the platform state declared by its host contracts.

```text
application facts
≠ Architect planning state
≠ rendered text
≠ kOA-Linux process/artifact activation state
```

## 8. Applicable normative requirements

<!-- GENERATED:REQUIREMENTS:BEGIN ids=REQ-SYS-LANG-001,REQ-SYS-LANG-002,REQ-SYS-LANG-003,REQ-SYS-LANG-004,REQ-SYS-LANG-005,REQ-SYS-LANG-006,REQ-SYS-LANG-007,REQ-SYS-LANG-008,REQ-SYS-LANG-009,REQ-SYS-LANG-010,REQ-SYS-LANG-011,REQ-SYS-LANG-012,REQ-SYS-LANG-013,REQ-SYS-LANG-014,REQ-SYS-LANG-015,REQ-SYS-LANG-016,REQ-SYS-LANG-017,REQ-SYS-LANG-018,REQ-SYS-LANG-019,REQ-SYS-LANG-020 -->
- **REQ-SYS-LANG-001 — SHALL:** kOA-Linux shall represent SemantiK Architect as an independently owned integrated subsystem rather than a native owner of Architect internal semantics.
- **REQ-SYS-LANG-002 — SHALL NOT:** kOA-Linux shall not redefine the SemantiK Architect planner, PlannedSentence, ConstructionPlan, lexicon, renderer selection, SurfaceResult, or public generation contract.
- **REQ-SYS-LANG-003 — SHALL:** The local SemantiK Architect deployment boundary shall use the official subsystem contract and documentation as the owner of internal behavior.
- **REQ-SYS-LANG-004 — SHALL:** Runtime artifact admission shall identify the Architect/runtime version and the declared backend or resource assets required by the candidate.
- **REQ-SYS-LANG-005 — SHALL NOT:** A language-pack contract shall not require GF or PGF for every SemantiK Architect deployment unless the selected backend profile explicitly requires it.
- **REQ-SYS-LANG-006 — SHALL:** A GF-backed language pack shall declare GF/PGF assets, provenance, compatibility, and validation evidence explicitly.
- **REQ-SYS-LANG-007 — SHALL:** Non-GF backend assets shall declare an equivalent backend identity, integrity record, compatibility scope, and validation evidence.
- **REQ-SYS-LANG-008 — SHALL:** Artifact verification and artifact activation shall remain separate transitions.
- **REQ-SYS-LANG-009 — SHALL:** Activation, when owned by the host boundary, shall be atomic and preserve the last valid compatible state or an explicit forward-repair path.
- **REQ-SYS-LANG-010 — SHALL NOT:** A transferred, quarantined, rejected, incompatible, partially staged, or partially activated candidate shall serve as active runtime authority.
- **REQ-SYS-LANG-011 — SHALL:** The caller shall retain authority over structured/domain facts submitted for generation.
- **REQ-SYS-LANG-012 — SHALL NOT:** Rendered text shall not become the authoritative source of the caller's domain facts merely because kOA-Linux hosts the generator.
- **REQ-SYS-LANG-013 — SHALL:** kOA-Linux resource policies may bound workers, memory, CPU, queues, caches, and loaded runtime assets without changing Architect linguistic semantics.
- **REQ-SYS-LANG-014 — SHALL:** Offline operation shall use already admitted local assets and declared local dependencies.
- **REQ-SYS-LANG-015 — SHALL NOT:** Offline or degraded operation shall not silently invoke external AI, network content retrieval, compilers, or undeclared renderer substitution.
- **REQ-SYS-LANG-016 — SHALL:** Health/readiness integration shall distinguish process availability from language/construction/backend capability.
- **REQ-SYS-LANG-017 — SHALL:** Local caches and projections shall remain derived and invalidatable.
- **REQ-SYS-LANG-018 — SHALL:** Runtime results shall preserve the Architect response/diagnostic information required by the active Architect contract.
- **REQ-SYS-LANG-019 — SHALL:** Artifact activation, rollback, rejection, and recovery shall produce the receipts/evidence required by the active kOA-Linux lifecycle contract.
- **REQ-SYS-LANG-020 — SHALL NOT:** A profile or implementation recipe shall turn a host-local SemantiK Architect runtime label or GF tooling label into a separate ecosystem-system authority.
<!-- GENERATED:REQUIREMENTS:END -->

## 9. Validation criteria

The boundary is aligned when the subsystem contract remains authoritative for Architect internals, the language-pack schema permits backend diversity, GF-backed packs remain explicit profiles rather than universal architecture, platform activation is fail-closed/atomic when applicable, and kOA-Linux does not acquire the caller's domain authority.

## 10. Non-normative examples

> A French deployment can use a GF/PGF backend and package a PGF asset. Another language/construction can use a family renderer with different runtime assets. Both remain SemantiK Architect deployments if they satisfy the Architect contract.

> kOA-Linux can restart or resource-limit the Architect process. It cannot change `ConstructionPlan` semantics by platform policy.
