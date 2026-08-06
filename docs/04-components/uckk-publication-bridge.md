<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-COMP-UCKK-PUB-001",
  "document_class": "normative_markdown",
  "status": "active",
  "language": "en",
  "layer": "component_integration",
  "scope": [
    "integration:uckk-publication"
  ],
  "canonical_refs": [
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/artifact-contracts/uckk-publication-package.schema.json",
    "contracts/artifact-contracts/uckk-publication-receipt.schema.json",
    "02-system/12-koa-mediatheque-system-boundary.md",
    "contracts/integrations/uckk-import.integration.json",
    "contracts/artifact-contracts/shared-mediatheque-frame.schema.json",
    "contracts/artifact-contracts/uckk-learning-package.schema.json",
    "contracts/artifact-contracts/uckk-import-receipt.schema.json",
    "04-components/uckk-import-bridge.md",
    "contracts/architecture-patterns.contract.json",
    "contracts/artifact-contracts/integration-resilience-policy.schema.json",
    "contracts/artifact-contracts/dead-letter-record.schema.json",
    "contracts/artifact-contracts/distributed-workflow.schema.json",
    "contracts/artifact-contracts/large-payload-reference.schema.json"
  ],
  "decision_ids": [
    "DEC-MEDIATHEQUE-001",
    "DEC-UCKK-EXT-001",
    "DEC-DATA-001",
    "DEC-COMP-001",
    "DEC-GOV-001",
    "DEC-OFFLINE-001",
    "DEC-RES-001",
    "DEC-MSG-001",
    "DEC-WF-001",
    "DEC-PAYLOAD-001"
  ],
  "requirement_ids": [
    "REQ-UCKK-PUB-001",
    "REQ-UCKK-PUB-002",
    "REQ-UCKK-PUB-003",
    "REQ-UCKK-PUB-004",
    "REQ-UCKK-PUB-005",
    "REQ-UCKK-PUB-006",
    "REQ-UCKK-PUB-007",
    "REQ-UCKK-PUB-008",
    "REQ-UCKK-PUB-009",
    "REQ-UCKK-PUB-010",
    "REQ-UCKK-PUB-011",
    "REQ-UCKK-PUB-012",
    "REQ-UCKK-IMPORT-001",
    "REQ-UCKK-IMPORT-002",
    "REQ-UCKK-IMPORT-003",
    "REQ-UCKK-IMPORT-004",
    "REQ-UCKK-IMPORT-005",
    "REQ-UCKK-IMPORT-006",
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
    "LOCK-MEDIATHEQUE-001",
    "LOCK-GATE-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-OFFLINE-001",
    "LOCK-UCKK-EXT-002",
    "LOCK-RES-001",
    "LOCK-MSG-001",
    "LOCK-WF-001",
    "LOCK-PAYLOAD-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-012",
    "DOC-COMP-MEDIATHEQUE-001",
    "DOC-COMP-UCKK-IMPORT-001",
    "DOC-SYS-034"
  ],
  "tags": [
    "integration",
    "uckk",
    "moodle",
    "publication",
    "bridge",
    "external-platform",
    "idempotency",
    "offline-queue",
    "import-from-uckk",
    "offline-learning",
    "architecture-patterns"
  ]
}
KOA:DOC-META:END -->

# UCKK Publication Bridge

## 1. Purpose

The UCKK Publication Bridge implements the outbound `publish_to_uckk` direction of the governed Mediatheque interchange boundary.

It maps an explicitly authorized kOA publication package to the online UCKK Moodle platform and returns a structured receipt. It is not the UCKK platform, not either Mediatheque, not an authorization authority, and not an inbound import mechanism.

The opposite `import_from_uckk` direction requires a separate controlled import contract. Keeping the directions separate prevents a publication adapter from becoming an implicit synchronization service.

## 2. Separation of Responsibilities

| Owner | Responsibility |
| --- | --- |
| kOA Mediatheque | Local source records, versions, content bindings, rights, provenance, export history, and accepted local copies of imported content |
| Publication Gateway | Outbound disclosure request, authorization decision, obligations, and cross-domain receipt chain |
| UCKK Publication Bridge | Outbound UCKK capability discovery, mapping, package transport, idempotency, retry, and remote result normalization |
| Controlled UCKK import path | Inbound retrieval, source and license verification, integrity and compatibility validation, quarantine, and delivery to local acceptance |
| External UCKK platform | Online Moodle courses, learning paths, activities, permissions, UCKK Mediatheque records, and remote lifecycle |

The shared Mediatheque frame supports mapping but does not combine these authority domains.

## 3. Inputs and Outputs

Input:

`text
uckk-publication-package.schema.json
`

Output:

`text
uckk-publication-receipt.schema.json
`

The package binds exact local versions, rights assertions, destination mapping, authorization, manifest, and idempotency key. The receipt records per-item remote outcomes and references.

## 4. Publication Sequence

1. Validate package schema and manifest.
2. Confirm that the authorization is still valid.
3. Resolve the allowlisted UCKK endpoint and Moodle API version.
4. Resolve credentials from the dedicated secret store.
5. Check destination capabilities and mapping compatibility.
6. Reconcile the idempotency key with any prior attempt.
7. Transfer only the selected authorized content and metadata.
8. Normalize per-item results.
9. Verify the remote response when signatures or digests are supported.
10. Produce a local receipt and evidence references.

## 5. Offline and Retry Behavior

The bridge can retain an authorized package in a protected queue while offline. The queue exposes:

- package identity;
- destination;
- creation and expiry;
- attempt count;
- next attempt time;
- cancellation reason;
- last known outcome.

A retry reuses the idempotency key. A new package is required when the source version, rights, authorization, destination mapping, or package contents change.

An ambiguous timeout does not immediately retry as a new publication. The bridge first reconciles the idempotency key with UCKK to avoid duplicate remote objects.

## 6. Security

- Endpoints must be allowlisted.
- Transport security and authenticated API access are required.
- Credentials are least-privilege and never embedded in packages or media records.
- Logs exclude content and restricted metadata.
- Rate limits, payload limits, and retry limits are mandatory.
- Direct database access is prohibited.
- External AI is not required.

## 7. Rights and Withdrawal

The bridge transmits only the representation approved by Publication Gateway. It does not independently interpret consent or rights.

When a local right, consent, or authorization is withdrawn:

- pending work is cancelled;
- future retries stop;
- a supported withdrawal notice may be sent;
- the result is recorded;
- history is not falsified;
- deletion from the external platform is not claimed unless UCKK explicitly confirms it.

## 8. Inbound Import Is a Separate Direction

This contract is the outbound `publish_to_uckk` direction only. The active sibling contract `contracts/integrations/uckk-import.integration.json` owns `import_from_uckk`.

UCKK-to-kOA acquisition is governed by the separate active UCKK Import integration, which requires:

- explicit source and object selection;
- course or learning-path dependency manifests;
- license, rights, restriction, and provenance validation;
- signature and content-integrity verification;
- quarantine and malware controls;
- compatibility and required-resource validation;
- explicit acceptance into the kOA Mediatheque;
- an import receipt and conflict policy.

Outbound and inbound operations may share the Mediatheque frame and common transport utilities. They do not share authorization, queue state, retry decisions, receipts, or authority by implication. They must not be implemented as background bidirectional synchronization.

## 9. Failure Codes

Recommended normalized codes include:

`text
AUTHENTICATION_FAILED
AUTHORIZATION_EXPIRED
SOURCE_VERSION_CHANGED
RIGHTS_CHANGED
DESTINATION_UNAVAILABLE
DESTINATION_UNSUPPORTED
MAPPING_INCOMPATIBLE
CONTENT_REJECTED
RATE_LIMITED
PARTIAL_PUBLICATION
REMOTE_RESULT_AMBIGUOUS
RECEIPT_INVALID
CANCELLED
`

## 10. Conformance

The bridge conforms only when it proves explicit Publication Gateway authorization, least-privilege credentials, no direct database writes, bounded retry, idempotent reconciliation, per-item receipts, source-authority preservation, and local operation independent from UCKK.

Passing outbound conformance does not establish inbound import or complete two-direction Mediatheque interchange conformance.

## Distributed publication resilience

`publish_to_uckk` is implemented as a distributed workflow. Authorization, package construction, remote transfer, remote acceptance, and terminal receipt are distinct steps. Remote calls use the declared circuit policy. Large media uses verified references or bounded package members. Exhausted asynchronous failures enter monitored quarantine. Remote acceptance is never inferred from local send success.
