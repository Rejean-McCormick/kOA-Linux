<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-UCKK-IMPORT-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component_integration",
  "scope": [
    "integration:uckk-import"
  ],
  "canonical_refs": [
    "contracts/integrations/uckk-import.integration.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "02-system/12-koa-mediatheque-system-boundary.md",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/large-payload-reference.schema.json"
  ],
  "decision_ids": [
    "DEC-UCKK-EXT-001",
    "DEC-MEDIATHEQUE-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-OFFLINE-001",
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001"
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
    "REQ-UCKK-IMPORT-012",
    "REQ-PATTERN-006",
    "REQ-PATTERN-007",
    "REQ-PATTERN-008",
    "REQ-PATTERN-009",
    "REQ-PATTERN-010",
    "REQ-PATTERN-011",
    "REQ-PATTERN-012",
    "REQ-PATTERN-013",
    "REQ-PATTERN-014",
    "REQ-PATTERN-015",
    "REQ-PATTERN-016",
    "REQ-PATTERN-017",
    "REQ-PATTERN-018",
    "REQ-PATTERN-019",
    "REQ-PATTERN-020",
    "REQ-PATTERN-021",
    "REQ-PATTERN-022",
    "REQ-PATTERN-023",
    "REQ-PATTERN-024",
    "REQ-PATTERN-025",
    "REQ-PATTERN-026",
    "REQ-PATTERN-027",
    "REQ-PATTERN-028",
    "REQ-PATTERN-029",
    "REQ-PATTERN-030"
  ],
  "lock_ids": [
    "LOCK-UCKK-EXT-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-OFFLINE-001",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-012",
    "DOC-COMP-MEDIATHEQUE-001",
    "DOC-SYS-034"
  ],
  "tags": [
    "uckk",
    "moodle",
    "import",
    "offline-learning",
    "quarantine",
    "mediatheque",
    "directional-interchange",
    "architecture-patterns"
  ]
}
KOA:DOC-META:END -->

# UCKK Import Bridge

## 1. Purpose

The UCKK Import Bridge implements `import_from_uckk`: the controlled inbound path from the online UCKK Mediatheque to the private local kOA Mediatheque.

It retrieves or receives a selected course, learning path, instruction collection, manual, or resource graph; places the package in quarantine; validates the source, license, integrity, provenance, completeness, and shared-frame compatibility; and presents the package for explicit local acceptance.

The bridge is not an authority over accepted local records. The kOA Mediatheque owns local acceptance and resulting local identities. Governance Policy Runtime evaluates policy when the active profile, rights, consent, or cultural conditions require it.

## 2. Directional Boundary

```text
online UCKK Mediatheque
        |
        | selected UCKK learning package
        v
UCKK Import Bridge
├── source and endpoint validation
├── authenticated retrieval or offline-bundle intake
├── quarantine
├── manifest, signature, and hash verification
├── license, restriction, and provenance checks
├── shared Mediatheque frame mapping validation
└── import receipt production
        |
        | explicit local acceptance candidate
        v
private offline kOA Mediatheque
```

The reverse direction is owned by the separate UCKK Publication Bridge and Publication Gateway workflow. The two queues, packages, receipts, retries, credentials, and authority decisions are not interchangeable.

## 3. Shared Frame

Every transferable resource declares the shared Mediatheque frame version and mapping version. The frame carries compatible identity references, version references, integrity, media description, rights, restrictions, provenance, lifecycle, and mapping evidence.

The frame does not create a shared database, identifier namespace, access-control system, lifecycle, or authority domain. Imported UCKK identifiers remain source references. Accepted content receives separate kOA record and version identities.

## 4. Required Workflow

1. A user or governed workflow explicitly selects an UCKK object and version scope.
2. The bridge resolves an allowlisted endpoint and declared source identity.
3. The complete package and required resource graph are retrieved online or received through a supported offline bundle.
4. The package enters quarantine before any local activation.
5. The system verifies package completeness, signatures or equivalent source evidence, hashes, license, restrictions, provenance, malware policy, offline-use permission, and frame compatibility.
6. Any lossy mapping, unresolved right, missing resource, or incompatible runtime requirement blocks acceptance or requires explicit review.
7. An authorized local actor accepts or rejects the validated candidate.
8. The kOA Mediatheque creates local identities and preserves UCKK source and version provenance.
9. The accepted learning material becomes available under the local profile's offline consultation capability.
10. An import receipt records every terminal result.

## 5. Offline Schools and Organizations

A complete validated package can be moved by removable media, local network, or intermittently connected hub. Once accepted, the course, instructions, media, and required offline runtime remain locally available without UCKK connectivity.

Local progress, annotations, organization-specific procedures, adaptations, and private derived material remain local unless separately selected and authorized for outbound publication.

## 6. Update Handling

A later remote version is a new update candidate. It does not overwrite the accepted local copy automatically.

The local workflow compares source version, rights, resource graph, local adaptations, and mapping version before accepting, deferring, or rejecting the update. Source withdrawal is recorded but does not silently delete a locally lawful accepted copy.

## 7. Prohibited Behavior

- importing an entire UCKK catalog without explicit selection;
- accepting content before quarantine and validation;
- direct access to UCKK database tables;
- dropping rights, restrictions, provenance, or unsupported frame fields silently;
- replacing local identities with UCKK identifiers;
- remote last-writer-wins overwrite;
- automatic upload of local progress or adaptations on reconnection;
- background bidirectional synchronization;
- treating UCKK metadata as local governance authority.

## 8. Safe Degradation

When UCKK is unavailable, accepted local content remains usable. New discovery, retrieval, and remote update checks are unavailable. Complete offline packages can still be validated when all required trust, license, integrity, and compatibility evidence is present locally. Incomplete or uncertain packages remain quarantined.

## 9. Validation Criteria

Conformance requires evidence for explicit selection, allowlisted source resolution, quarantine-before-acceptance, complete manifest validation, source and signature verification, license enforcement, rights and provenance preservation, frame-version mapping, separate local identity creation, offline bundle intake, update-candidate handling, and absence of implicit synchronization.

## Distributed import resilience

`import_from_uckk` is implemented as a distributed workflow. Retrieval, quarantine, verification, rights evaluation, local acceptance, and terminal receipt are distinct steps. Remote calls use the declared circuit policy. Large package members use verified references where supported. Failed work enters monitored quarantine, and local authority changes only at the explicit acceptance step.
