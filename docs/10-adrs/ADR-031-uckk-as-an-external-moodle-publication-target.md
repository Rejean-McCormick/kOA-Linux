<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "ADR-031",
  "document_class": "adr",
  "status": "accepted",
  "language": "en",
  "layer": "decisions",
  "scope": [
    "global",
    "integration:uckk-publication"
  ],
  "canonical_refs": [
    "contracts/integrations/uckk-publication.integration.json",
    "contracts/components/publication-gateway.component.json",
    "contracts/components/koa-mediatheque.component.json",
    "contracts/artifact-contracts/uckk-publication-package.schema.json",
    "contracts/artifact-contracts/uckk-publication-receipt.schema.json",
    "04-components/uckk-publication-bridge.md",
    "10-adrs/ADR-020-publication-gateway-and-uckk-dimension-gateway-separation.md",
    "10-adrs/ADR-022-deterministic-native-uckk-pipeline.md",
    "10-adrs/ADR-029-native-uckk-mediatheque.md"
  ],
  "decision_ids": [
    "DEC-UCKK-EXT-001"
  ],
  "requirement_ids": [],
  "lock_ids": [
    "LOCK-UCKK-EXT-001",
    "LOCK-MEDIATHEQUE-001",
    "LOCK-GATE-001"
  ],
  "exception_ids": [],
  "depends_on": [
    "ADR-030"
  ],
  "tags": [
    "adr",
    "uckk",
    "moodle",
    "external-integration",
    "publication",
    "bridge"
  ],
  "adr_id": "ADR-031",
  "adr_status": "accepted",
  "decision_class": "major",
  "owner_decision_id": "DEC-UCKK-EXT-001",
  "created_at": "2026-08-04",
  "accepted_at": "2026-08-04",
  "effective_at": "2026-08-04",
  "supersedes": [
    "ADR-020",
    "ADR-022",
    "ADR-029"
  ],
  "superseded_by": null
}
KOA:DOC-META:END -->

# ADR-031: UCKK as an External Moodle Publication Target

## Status

Accepted.

## Context

UCKK is a Moodle platform outside kOA-Linux Operating System. It has its own Mediatheque and remote authority domain. kOA-Linux needs a safe way to publish selected local material to UCKK without embedding UCKK, merging both Mediatheques, or granting the external platform authority over local records.

## Decision

UCKK is classified as an **optional external Moodle publication target**.

Publication uses two separated responsibilities:

1. the generic Publication Gateway resolves identity, rights, consent, disclosure, audience, purpose, destination, obligations, and authorization;
2. the UCKK publication bridge maps the authorized package to the declared Moodle/UCKK API, transmits it, handles bounded retry, and returns a structured receipt.

The initial integration is outbound publication only. A future controlled import must use a separate contract and workflow. Background bidirectional synchronization is not part of this decision.

## Invariants

- UCKK is not an internal subsystem and does not require a local subsystem-documentation mount.
- UCKK is not required for local Mediatheque or offline operation.
- kOA-Linux does not write directly into UCKK database tables.
- Each publication binds exact local record versions, rights, authorization, destination, mapping version, manifest, and idempotency key.
- A remote identifier remains a destination reference.
- A successful receipt proves a publication result, not transfer of local source authority.
- Missing, unsupported, or lossy mappings block or require review.

## Consequences

- `uckk-publication.integration.json` becomes the canonical external boundary.
- The old `uckk_dimension_gateway` and `uckk_platform` internal-component model is retired.
- Profiles may enable or disable the bridge independently from the local Mediatheque.
- Offline nodes can queue authorized packages but cannot claim remote publication before receipt validation.
- Remote withdrawal or deletion is recorded only when the external platform acknowledges it.

## Superseded Decisions

This ADR supersedes the UCKK-internal architectural effects of ADR-020, ADR-022, and ADR-029. Those files remain historical records with superseded status.

## Rejected Alternatives

### Embed UCKK or Moodle in the kOA-Linux baseline

Rejected because UCKK is an external platform and its lifecycle and authority are separate.

### Direct database synchronization

Rejected because it bypasses platform contracts, authorization, audit, compatibility, and failure isolation.

### Automatic bidirectional synchronization

Rejected because identity, rights, conflict resolution, deletion, and authority-transfer semantics are not implicit.

### Let the bridge decide publication policy

Rejected because target transport and cross-domain authorization are separate responsibilities.
