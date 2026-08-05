<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-SYS-012",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "system_baseline",
  "scope": [
    "global"
  ],
  "canonical_refs": [
    "contracts/system.contract.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/artifact-contracts/koa-media-record.schema.json",
    "contracts/artifact-contracts/uckk-publication-package.schema.json",
    "contracts/artifact-contracts/uckk-publication-receipt.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/components/publication-gateway.component.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "generated/integration-catalog.json",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "04-components/uckk-import-bridge.md"
  ],
  "decision_ids": [
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-OFFLINE-001"
  ],
  "requirement_ids": [
    "REQ-MEDIATHEQUE-001",
    "REQ-MEDIATHEQUE-002",
    "REQ-MEDIATHEQUE-003",
    "REQ-UCKK-PUB-001",
    "REQ-UCKK-PUB-002",
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006"
  ],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-DATA-001",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-GOV-001",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-000",
    "DOC-SYS-004",
    "DOC-SYS-005",
    "DOC-SYS-007",
    "DOC-SYS-008",
    "DOC-SYS-015",
    "DOC-SYS-016",
    "DOC-COMP-UCKK-IMPORT-001"
  ],
  "tags": [
    "mediatheque",
    "media",
    "files",
    "offline",
    "uckk",
    "moodle",
    "external-integration",
    "publication-boundary",
    "import-from-uckk",
    "offline-learning"
  ]
}
KOA:DOC-META:END -->

# kOA and UCKK Mediatheque System Boundary

## 1. Purpose

This document defines the relationship between the **kOA Mediatheque**, the private local and offline media authority of kOA-Linux Operating System, and the **UCKK Mediatheque**, the online media and learning-content authority inside the external UCKK Moodle platform.

The two surfaces use the same shared Mediatheque frame or compatible frame versions. They remain separate systems with separate records, storage, identities, access control, lifecycle, and authority.

## 2. System Boundary

```text
kOA-Linux Operating System
└── kOA Mediatheque
    ├── private local records and versions
    ├── local instructions and organization-specific knowledge
    ├── downloaded courses and learning paths
    ├── rights, restrictions, provenance, and local lifecycle
    └── offline browsing, backup, restore, and deterministic processing

            publish_to_uckk ↓       ↑ import_from_uckk

Governed UCKK interchange boundary
├── outbound disclosure authorization and publication transport
├── inbound source, license, integrity, compatibility, and quarantine checks
├── directional queues and receipts
└── no implicit synchronization

External UCKK Moodle platform
└── UCKK Mediatheque
    ├── online courses and learning paths
    ├── activities and educational resources
    ├── UCKK users, roles, permissions, and destinations
    └── remote records, versions, publication, and lifecycle
```

## 3. Authorities

1. The kOA Mediatheque owns local records, local versions, managed local content, local rights state, local provenance, import and export history, and local backup and restore state.
2. Publication Gateway owns outbound disclosure authorization from kOA to UCKK.
3. UCKK-specific outbound transport owns package mapping, transmission, retry, remote-result normalization, and receipt preservation; it does not own disclosure authority.
4. The controlled inbound path owns retrieval, quarantine, source and license checks, integrity and compatibility validation, and delivery to the kOA Mediatheque acceptance workflow.
5. The external UCKK platform owns its courses, learning paths, activities, permissions, remote media records, UCKK Mediatheque state, and online lifecycle.

## 4. Shared Mediatheque Frame

The shared frame covers compatible concepts such as:

- stable object identity;
- version identity;
- content hashes and integrity;
- media type and renditions;
- metadata, dimensions, collections, tags, and relationships;
- language and accessibility information;
- rights, licenses, restrictions, consent, and cultural conditions;
- provenance and derivation;
- lifecycle state;
- package manifests and transfer receipts.

A shared frame is an interchange contract. It is not a shared database, shared identifier namespace, shared access-control system, shared lifecycle, or shared authority.

A mapping that cannot preserve a required right, restriction, provenance field, or lifecycle condition blocks the affected transfer or requires explicit review. It is never silently discarded.

## 5. Outbound: `publish_to_uckk`

1. A user or governed workflow selects exact local record versions.
2. The kOA Mediatheque produces a bounded candidate representation.
3. Publication Gateway evaluates identity, purpose, audience, rights, restrictions, consent, destination, and expiry.
4. An approved UCKK publication package is created.
5. UCKK-specific transport maps and sends only the approved representation.
6. UCKK accepts, rejects, or partially accepts the remote operation.
7. A validated receipt is attached to local export history.

The local source remains authoritative in kOA. The UCKK object is a separate remote object under UCKK authority.

## 6. Inbound: `import_from_uckk`

1. A user or governed workflow selects an UCKK course, learning path, instruction set, manual, or resource for local use.
2. The system resolves the source endpoint, remote object identity, version, license, and required resource graph.
3. A transfer package is downloaded or received through a supported offline bundle path.
4. The package enters quarantine.
5. Signatures, hashes, manifest completeness, licenses, restrictions, provenance, compatibility, and required resources are validated.
6. The user or authorized local workflow explicitly accepts or rejects the package.
7. The kOA Mediatheque creates a local record and version with preserved UCKK provenance.
8. The installed content becomes available within the local profile's offline consultation capability.

The imported local copy is governed by kOA authority. The UCKK source remains governed by UCKK. A later remote version is a new import candidate.

## 7. Offline Learning Use

The local system can hold private instructions or downloaded learning material without remaining connected to UCKK.

Valid use cases include:

- the complete kOA-Linux user and administrator manual;
- an organization's private administrative procedures;
- local safety and maintenance instructions;
- a school curriculum for an isolated environment;
- professional learning paths;
- practical “univers-cité” collections such as bread making, agriculture, construction, or equipment repair.

The local installation is not required to accept the public UCKK catalog. It may contain only private or explicitly selected content.

## 8. Offline and Reconnection Behavior

While disconnected:

- local cataloging, browsing, search, rights management, backup, restore, and deterministic processing continue;
- accepted UCKK-derived packages remain available locally;
- new UCKK discovery and live downloads are unavailable;
- outbound publication delivery is deferred;
- complete transferred packages may be validated offline when all required evidence is locally available;
- incomplete packages remain quarantined.

On reconnection, outbound and inbound queues are evaluated separately. Authorization, rights, versions, destinations, licenses, integrity, compatibility, and expiry are revalidated as applicable. No last-writer-wins or background synchronization rule is inferred.

## 9. Failure and Recovery

- Integrity failure quarantines the affected local or transferred version.
- Rights or authorization changes cancel pending outbound publication and require a new decision.
- License or compatibility failure rejects inbound acceptance.
- Destination unavailability does not degrade local Mediatheque authority.
- Ambiguous remote outcomes require reconciliation by idempotency key before retry.
- Restore activates only after database, content, manifest, permissions, queue, package, and receipt references reconcile.

## 10. Prohibited Architecture

The following models are prohibited:

- UCKK as a native kOA-Linux component or required local subsystem;
- the kOA Mediatheque as a module owned by UCKK;
- direct reads or writes to UCKK database tables;
- shared authoritative storage between the two Mediatheques;
- replacing local identities with UCKK identifiers;
- treating a downloaded package as accepted before validation;
- treating an outbound receipt as local rights or semantic authority;
- implicit background bidirectional synchronization;
- silent remote overwrite of a local copy;
- silent local overwrite of an UCKK source.

## 11. Conformance Direction

The current outbound publication contract remains one direction of the boundary. Full bidirectional conformance additionally requires dedicated inbound package, import-receipt, quarantine, acceptance, and conflict contracts. Until those artifacts exist and validate, an implementation may claim outbound UCKK publication conformance but not complete UCKK Mediatheque interchange conformance.
