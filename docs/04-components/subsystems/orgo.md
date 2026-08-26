<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-ORGO",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/orgo.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystem",
    "orgo",
    "integration-boundary"
  ]
}
KOA:DOC-META:END -->

# Orgo Subsystem Boundary

## Purpose

This page defines the **kOA-Linux host boundary** for Orgo. Orgo remains an independently owned ecosystem system. This page does not reproduce or redefine its Task/Case/workflow documentation.

## Official documentation

The official documentation mount is `subsystems/orgo/` and remains authoritative for Orgo internals.

## Host role

Within kOA-Linux, Orgo is an **integrated subsystem**. kOA-Linux can own/mediate deployment-profile membership, process lifecycle, resource envelope, trust boundary, network/storage exposure, artifact admission, health integration, backup coordination, safe degradation, and declared cross-system interactions.

Orgo itself owns Organizations, Cases, Tasks, workflow rules/state, routing/labels, domain extensions, its APIs, and operational audit semantics.

```text
ecosystem scope: Orgo = ecosystem system
host scope:      Orgo = integrated subsystem
```

A kOA-Linux platform event or receipt does not become Orgo workflow state unless Orgo accepts it through its own contract.
