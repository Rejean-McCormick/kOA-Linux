<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-REC-UCKK-IMPORT-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "recipes",
  "scope": [
    "profile:user_lightweight",
    "integration:uckk-import"
  ],
  "canonical_refs": [
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "04-components/uckk-import-bridge.md",
    "11-recipes/user-lightweight/koa-mediatheque-local.md"
  ],
  "decision_ids": [
    "DEC-UCKK-EXT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-OFFLINE-001"
  ],
  "requirement_ids": [
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006",
    "REQ-UCKK-IMPORT-007",
    "REQ-UCKK-IMPORT-008",
    "REQ-UCKK-IMPORT-009",
    "REQ-UCKK-IMPORT-010",
    "REQ-UCKK-IMPORT-011",
    "REQ-UCKK-IMPORT-012"
  ],
  "lock_ids": [
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-COMP-UCKK-IMPORT-001"
  ],
  "tags": [
    "recipe",
    "uckk",
    "offline",
    "learning-package",
    "school",
    "isolated-environment"
  ]
}
KOA:DOC-META:END -->

# Import an UCKK Learning Package for Offline Use

## Purpose

This recipe shows one non-normative deployment pattern for bringing a selected UCKK course, learning path, manual, or instruction collection into a private local kOA installation.

## Preconditions

- the `uckk-import` integration is enabled explicitly;
- the source endpoint or offline package source is approved;
- a complete `uckk-learning-package` is available;
- quarantine storage has sufficient capacity;
- the shared Mediatheque frame and mapping versions are supported;
- the local actor has import-acceptance authority;
- license and offline-use conditions can be evaluated locally.

## Procedure

1. Select the exact UCKK course, path, manual, or resource collection and source version.
2. Retrieve the package through the UCKK Import Bridge or copy a complete offline bundle to the intake directory.
3. Move the package into quarantine without exposing it to the ordinary local catalog.
4. Validate the manifest, signatures, hashes, resource graph, license, restrictions, provenance, malware policy, and shared-frame mapping.
5. Present any lossy mappings, expiring rights, restricted resources, or missing runtime requirements for explicit review.
6. Accept or reject the package.
7. On acceptance, create separate kOA record and version identities while preserving UCKK source references.
8. Register the course or manual with the local offline consultation surface.
9. Store the import receipt with the local record and audit evidence references.
10. Keep future remote versions as update candidates until a new local decision is made.

## Isolated School Example

An intermittently connected hub downloads a curriculum package, verifies it, and transfers it to an isolated school on approved removable media. The school imports the package, teaches from it for months without Internet access, stores progress locally, and later chooses whether to import a newer version. No progress or locally adapted lesson is uploaded merely because a connection becomes available.

## Failure Handling

- incomplete packages remain quarantined;
- a hash or signature failure rejects the package;
- unknown or incompatible licenses block acceptance;
- unsupported mandatory activities block offline activation;
- storage exhaustion stops before partial local activation;
- a remote update never overwrites local adaptations automatically.
