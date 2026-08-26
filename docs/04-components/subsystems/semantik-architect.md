<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-SEMANTIK-ARCHITECT",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/semantik-architect.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystem",
    "semantik_architect",
    "integration-boundary"
  ]
}
KOA:DOC-META:END -->

# SemantiK Architect Subsystem Boundary

## Purpose

This page defines the **kOA-Linux host boundary** for SemantiK Architect. SemantiK Architect remains one independently owned planner-centered multilingual NLG ecosystem system.

## Official documentation

The official documentation mount is `subsystems/semantik-architect/` and remains authoritative for Architect internals.

## Host role

Within kOA-Linux, SemantiK Architect is an **integrated subsystem**. kOA-Linux can own/mediate:

- deployment-profile membership;
- process/service lifecycle;
- resource envelope;
- identity/trust boundary;
- network and storage exposure;
- artifact admission/verification;
- local activation state when a declared artifact contract requires it;
- health/readiness integration;
- backup coordination;
- safe degradation.

SemantiK Architect owns:

- request normalization;
- planner behavior;
- `PlannedSentence`;
- `ConstructionPlan`;
- lexical resolution;
- renderer selection and backend behavior;
- `SurfaceResult`;
- the public generation contract.

GF/PGF is a supported backend/tooling family inside Architect, not a separate ecosystem system and not the architecture center.

```text
ecosystem scope: SemantiK Architect = ecosystem system
host scope:      SemantiK Architect = integrated subsystem
```
