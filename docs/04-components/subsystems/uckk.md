<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-UCKK",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/uckk.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystem",
    "uckk",
    "integration-boundary"
  ]
}
KOA:DOC-META:END -->

# UCKK Subsystem Boundary

## Purpose

This page defines the kOA integration boundary for UCKK. It does not reproduce the subsystem's internal documentation.

## Official Documentation Location

The official documentation is expected at `subsystems/uckk/`.

This path is reserved for a directory junction or symbolic link. It can remain absent until the subsystem documentation is available. Windows `.lnk` shortcut files are not used.

## Role in kOA

Native media, file classification, managed storage, processing, provenance, rights, lifecycle, export, backup, and restore subsystem.

## Boundary

The subsystem owns its internal domain model, workflow, state, complete API, product behavior, and user interface. kOA owns deployment, resources, trust, lifecycle, health, storage exposure, backup coordination, and declared cross-subsystem interactions.

Direct writes to another subsystem's authoritative state are prohibited. Missing capability follows the declared capability state; no undeclared substitute is activated.

## Native Mediatheque

The UCKK Mediatheque is native to UCKK. UCKK owns its complete object, version, classification, rights, provenance, rendition, and lifecycle model. kOA documents only the operating boundary.

The official Mediatheque documentation is expected at `subsystems/uckk/mediatheque/`.

## Validation

The alignment check validates the reserved mount location and rejects duplicated internal catalogs. Use `--require-mounted` only when all subsystem documentation links have been installed.
