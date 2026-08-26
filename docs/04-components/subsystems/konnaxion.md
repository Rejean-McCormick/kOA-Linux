<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-KONNAXION",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/konnaxion.subsystem.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "subsystem",
    "konnaxion",
    "integration-boundary"
  ]
}
KOA:DOC-META:END -->

# Konnaxion Subsystem Boundary

## Purpose

This page defines the **kOA-Linux host boundary** for Konnaxion. Konnaxion remains an independently owned ecosystem system. This page does not reproduce or redefine its internal documentation.

## Official documentation

The official documentation mount is `subsystems/konnaxion/` and remains authoritative for Konnaxion internals.

## Host role

Within kOA-Linux, Konnaxion is an **integrated subsystem**. kOA-Linux can own/mediate deployment-profile membership, process lifecycle, resource envelope, trust boundary, network/storage exposure, artifact admission, health integration, backup coordination, safe degradation, and declared cross-system interactions.

Konnaxion itself owns its civic/public domain model, internal workflows/state machines, API semantics, validation logic, application behavior, and user interfaces.

```text
ecosystem scope: Konnaxion = ecosystem system
host scope:      Konnaxion = integrated subsystem
```

No direct cross-system authoritative writes are permitted.
