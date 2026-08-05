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
    "contracts/components/publication-gateway.component.json",
    "generated/profile-catalog.json",
    "generated/component-catalog.json",
    "generated/integration-catalog.json",
    "10-adrs/ADR-030-koa-mediatheque-as-an-internal-component.md",
    "10-adrs/ADR-031-uckk-as-an-external-moodle-publication-target.md"
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
    "REQ-UCKK-PUB-002"
  ],
  "lock_ids": [
    "LOCK-MEDIATHEQUE-001",
    "LOCK-MEDIATHEQUE-002",
    "LOCK-UCKK-EXT-001",
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
    "DOC-SYS-016"
  ],
  "tags": [
    "mediatheque",
    "media",
    "files",
    "offline",
    "uckk",
    "moodle",
    "external-integration",
    "publication-boundary"
  ]
}
KOA:DOC-META:END -->

# kOA Mediatheque System Boundary

## 1. Purpose

This document defines the system boundary for the **kOA Mediatheque**, the native local media and file-management capability of kOA-Linux Operating System.

The kOA Mediatheque owns its local catalog, media records, file versions, managed-content bindings, classification, rights, restrictions, provenance, renditions, lifecycle state, import and export history, and backup and restore state.

UCKK is a separate external Moodle platform. UCKK may expose its own Mediatheque using a compatible conceptual frame, but that compatibility does not create shared storage, shared identity, shared lifecycle, or shared authority.

## 2. System Boundary

```text
kOA-Linux Operating System
  └── kOA Mediatheque
        ├── local authoritative records
        ├── local managed content
        ├── rights and provenance
        ├── offline browsing and processing
        └── governed export candidates
              ↓
        Publication Gateway decision
              ↓
        UCKK publication bridge
              ↓
External UCKK Moodle platform
  └── UCKK Mediatheque and Moodle-owned records
```

The boundary has four independent authorities:

1. the kOA Mediatheque owns local source records and managed versions;
2. Governance Policy Runtime and Publication Gateway own authorization and disclosure decisions;
3. the UCKK publication integration owns target mapping, transport, retry, and remote-result handling;
4. the external UCKK platform owns the destination records it creates or updates.

## 3. Invariants

- **REQ-MEDIATHEQUE-001 — MUST:** The kOA Mediatheque MUST remain usable without UCKK and without Internet access for locally available records and content.
- **REQ-MEDIATHEQUE-002 — MUST:** Local media identity, version identity, rights, restrictions, provenance, and lifecycle MUST remain authoritative in the kOA Mediatheque.
- **REQ-MEDIATHEQUE-003 — MUST NOT:** A remote UCKK identifier MUST NOT replace a local kOA record or version identifier.
- **REQ-UCKK-PUB-001 — MUST:** Publication to UCKK MUST require explicit selection and an allow decision from the Publication Gateway.
- **REQ-UCKK-PUB-002 — MUST NOT:** kOA-Linux MUST NOT write directly into UCKK database tables or treat UCKK as an internal subsystem.
- A shared Mediatheque frame describes compatible exchange concepts; it does not assign ownership.
- Local backup and restore cover kOA Mediatheque data, local queues, packages, manifests, and receipts. They do not claim to back up the external UCKK authority domain.

## 4. Native Local Capability

The local baseline is:

- SQLite for structured component-owned state;
- managed local content storage;
- deterministic content hashing;
- explicit record and version identities;
- bounded local media workers;
- local search and browsing;
- local import, export, backup, and restore;
- no required external AI or cloud service.

The active profile may replace physical mechanisms while preserving the same ownership and behavior.

## 5. Shared Frame and Compatibility

The kOA and UCKK Mediatheques may share concepts such as media identity, version, hash, collection, dimension, rights, restrictions, provenance, publication eligibility, manifest, and receipt.

Compatibility is expressed through versioned schemas and mapping contracts. Unsupported fields, rights, or restrictions block publication or require review; they are not silently discarded.

## 6. Publication to UCKK

Publication is a controlled external operation:

1. a user or governed workflow selects exact local record versions;
2. the kOA Mediatheque produces a bounded candidate representation;
3. Publication Gateway resolves identity, purpose, rights, restrictions, consent, audience, destination, and expiry;
4. an approved `uckk-publication-package` is created;
5. the bridge maps the package to the declared UCKK Moodle destination;
6. transmission is authenticated, bounded, and idempotent;
7. the returned `uckk-publication-receipt` is validated and attached to local export history.

A successful publication means that an external representation was accepted. It does not transfer local source authority.

## 7. Offline Behavior

Local cataloging, classification, rights management, browsing, and bounded media work continue when required local services and content are available.

UCKK publication is unavailable while disconnected. An already authorized package may be queued if its authorization, source version, rights, destination, and expiry remain locally verifiable. The interface must show `queued`, not `published`, until a remote receipt is validated.

## 8. Failure and Recovery

- Integrity failure quarantines the affected version.
- Rights or authorization changes cancel pending publication and require a new decision.
- Destination unavailability does not degrade local Mediatheque authority.
- Ambiguous remote outcomes require reconciliation by idempotency key before retry.
- Restore activates only after database, content, manifest, permissions, and queue references reconcile.

## 9. Prohibited Architecture

The following models are prohibited:

- UCKK as a native kOA-Linux subsystem;
- the kOA Mediatheque as a module owned by UCKK;
- a required `docs/subsystems/uckk` mount;
- direct UCKK database access;
- implicit background bidirectional synchronization;
- treating an external publication receipt as local semantic or rights authority.
