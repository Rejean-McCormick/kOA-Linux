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
    "REQ-UCKK-PUB-012"
  ],
  "lock_ids": [
    "LOCK-UCKK-EXT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-GATE-001",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-OFFLINE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-SYS-012",
    "DOC-COMP-MEDIATHEQUE-001"
  ],
  "tags": [
    "integration",
    "uckk",
    "moodle",
    "publication",
    "bridge",
    "external-platform",
    "idempotency",
    "offline-queue"
  ]
}
KOA:DOC-META:END -->

# UCKK Publication Bridge

## 1. Purpose

The UCKK publication bridge implements the `uckk-publication` external integration. It maps an explicitly authorized publication package to an external UCKK Moodle destination and returns a structured receipt.

The bridge is an adapter at the kOA-Linux boundary. It is not the UCKK platform, not the UCKK Mediatheque, and not an owner of local media records.

## 2. Separation of Responsibilities

| Owner | Responsibility |
| --- | --- |
| kOA Mediatheque | Local source records, versions, content bindings, rights, provenance, and export history |
| Publication Gateway | Publication request, disclosure and authorization decision, obligations, and cross-domain publication receipt chain |
| UCKK publication bridge | Moodle/UCKK capability discovery, mapping, packaging transport, idempotency, retry, and remote result normalization |
| External UCKK platform | Remote Moodle and UCKK records, users, permissions, courses, repositories, and destination lifecycle |

The bridge must not combine these authority domains.

## 3. Inputs and Outputs

Input:

```text
uckk-publication-package.schema.json
```

Output:

```text
uckk-publication-receipt.schema.json
```

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

## 8. Import Is Separate

This contract is outbound publication only. A future UCKK-to-kOA import requires a separate integration contract, quarantine, provenance, rights validation, and explicit acceptance into the kOA Mediatheque. It must not be implemented as background bidirectional synchronization.

## 9. Failure Codes

Recommended normalized codes include:

```text
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
```

## 10. Conformance

The bridge conforms only when it proves explicit authorization, least-privilege credentials, no direct database writes, bounded retry, per-item receipts, source-authority preservation, and local operation independent from UCKK.
