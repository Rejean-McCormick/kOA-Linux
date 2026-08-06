# kOA shared implementation interfaces

This directory contains implementation-level transport envelopes and binding entry points. It does not redefine domain contracts, component ownership, capability membership, authorization, policy, consent, state machines, artifact identity, or release authority owned under `docs/contracts/`.

## Transport files

| File | Purpose |
| --- | --- |
| `transport/http-over-unix.toml` | Common local HTTP-over-Unix transport properties and security semantics. Concrete endpoint paths, limits, and timeouts remain profile-, workspace-, or interface-scoped. |
| `transport/event-envelope.schema.json` | Versioned envelope for a domain event that describes an already committed fact. |
| `transport/error-envelope.schema.json` | Versioned, minimized machine-readable failure envelope. |
| `transport/idempotency.schema.json` | Stable operation identity, canonical request fingerprint, and owner-enforced duplicate behavior. |
| `transport/version-negotiation.schema.json` | Explicit interface version offer, selection, or rejection without automatic schema guessing. |

## Shared invariants

1. Every cross-component message identifies its interface version, sender, intended receiver, operation or event identity, correlation context, and payload representation.
2. A transport carries data and delivery metadata only. Reachability, a successful HTTP exchange, or possession of a Unix socket path does not establish identity, authorization, ownership, policy approval, or authoritative commit.
3. The receiving component independently validates identity, capability, target scope, authority, policy, consent, compatibility, payload, idempotency, deadlines, and resource conditions before changing owned state.
4. Domain events describe facts committed by their publishing owner. A consumer may update only its own state or request a separately authorized command.
5. Retries preserve request, correlation, and idempotency identities. An unknown outcome requires status resolution rather than blind replay.
6. Interface incompatibility blocks the affected transition and preserves the existing valid state. Automatic schema guessing is prohibited.
7. Error and event metadata minimize governed payload data. Secrets, credentials, private keys, unrestricted content, and unnecessary personal data are not transport metadata.
8. Correlation connects evidence across components but never merges their authority or data ownership.

## JSON Schema conventions

The schemas use JSON Schema Draft 2020-12, stable `$id` values under `https://schemas.koa.local/interfaces/transport/`, closed objects, semantic versions, RFC 3339 timestamps, explicit correlation, and explicit authority-denial fields. Payload bodies remain governed by the schema named in `payload_representation.schema_ref`; these envelopes do not duplicate domain payload fields.

Schema version `1.0.0` is the version of the common envelope itself. `interface_version`, `event_version`, and payload `schema_version` are independently versioned and must not be inferred from one another.

## Minimal event example

```json
{
  "schema_version": "1.0.0",
  "envelope_type": "domain_event",
  "message_id": "msg_01J00000000000000000000001",
  "event_id": "evt_01J00000000000000000000001",
  "event_type": "media_record_committed",
  "event_version": "1.0.0",
  "interface": {
    "interface_id": "koa-mediatheque.events",
    "interface_version": "1.0.0",
    "contract_ref": "docs/contracts/components/koa-mediatheque.component.json"
  },
  "publisher": {"component_id": "koa-mediatheque"},
  "intended_receivers": [{"kind": "subscription", "identifier": "media-record-consumers"}],
  "correlation": {"correlation_id": "corr_01J00000000000000000000001"},
  "occurred_at": "2026-08-06T12:00:00Z",
  "committed_at": "2026-08-06T12:00:00Z",
  "payload_representation": {
    "media_type": "application/json",
    "schema_ref": "docs/contracts/artifact-contracts/koa-media-record.schema.json",
    "schema_version": "1.0.0",
    "encoding": "identity"
  },
  "payload": {"record_id": "media_01J00000000000000000000001"},
  "ordering": {"scope": "koa-mediatheque.media-record", "sequence": 1},
  "replay": {"mode": "original", "duplicate_handling": "ignore_if_applied"},
  "disclosure": {"class": "operator_restricted", "payload_minimized": true},
  "authority": {
    "effect": "committed_fact_evidence",
    "publisher_owns_fact": true,
    "grants_mutation_authority": false,
    "transfers_ownership": false
  }
}
```

## Consumer responsibilities

Generated Python and Rust bindings may expose these structures, but generated code remains a projection of the schemas. Component contracts remain the owners of domain fields, accepted operations, errors, idempotency semantics, compatibility commitments, and recovery behavior.
