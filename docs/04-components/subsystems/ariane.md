<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-ARIANE",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/ariane.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystem",
    "ariane",
    "integration-boundary"
  ]
}
KOA:DOC-META:END -->

# Ariane Subsystem Boundary

## Purpose

This page defines the kOA integration boundary for Ariane. It does not reproduce the subsystem's internal documentation.

## Official Documentation Location

The official documentation is expected at `subsystems/ariane/`.

This path is reserved for a directory junction or symbolic link. It can remain absent until the subsystem documentation is available. Windows `.lnk` shortcut files are not used.

## Role in kOA

Deterministic local navigation and interaction orchestration.

## Boundary

The subsystem owns its internal domain model, workflow, state, complete API, product behavior, and user interface. kOA owns deployment, resources, trust, lifecycle, health, storage exposure, backup coordination, and declared cross-subsystem interactions.

Direct writes to another subsystem's authoritative state are prohibited. Missing capability follows the declared capability state; no undeclared substitute is activated.

## Validation

The alignment check validates the reserved mount location and rejects duplicated internal catalogs. Use `--require-mounted` only when all subsystem documentation links have been installed.
