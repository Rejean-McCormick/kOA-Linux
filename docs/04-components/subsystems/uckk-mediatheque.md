<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SUB-UCKK-MEDIATHEQUE",
  "document_class": "explanatory_markdown",
  "status": "active",
  "language": "en",
  "layer": "subsystem_boundaries",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/subsystems/uckk.subsystem.json",
    "contracts/artifact-contracts/uckk-media-reference.schema.json"
  ],
  "decision_ids": [],
  "requirement_ids": [],
  "lock_ids": [],
  "exception_ids": [],
  "depends_on": [],
  "tags": [
    "uckk",
    "mediatheque"
  ]
}
KOA:DOC-META:END -->

# UCKK Mediatheque Boundary

The Mediatheque is the native UCKK file classification and management surface. UCKK owns media objects, file versions, dimensions, collections, tags, relationships, rights, restrictions, provenance, renditions, lifecycle, duplicate handling, import, export, audit, backup, and restore.

kOA owns only deployment, resource, trust, storage exposure, gateway, publication, health, backup coordination, and degradation boundaries. SQLite and managed local storage form the native local baseline. XLSX and approved AI surfaces are interfaces, not authority.

The full Mediatheque documentation is expected at `subsystems/uckk/mediatheque/`.
