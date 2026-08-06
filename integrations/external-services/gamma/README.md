# Gamma external-service boundary

This directory declares the kOA boundary for the approved optional Gamma presentation-generation surface. It does not contain a Gamma SDK, provider implementation, credential, endpoint, or authoritative application logic.

## Authority

Gamma is registered as `external_media_service`, optional, and non-authoritative. Its sole declared capability is `presentation.generate_candidate`. A response is candidate material until an owning component performs controlled import, validation, provenance capture, review, and explicit acceptance.

The integration cannot:

- read a repository, component store, tenant, profile, host, or secret implicitly;
- write authoritative component state;
- grant privilege or decide policy;
- activate a release;
- publish content;
- infer publication consent from generation or candidate acceptance.

## Operation sequence

1. An explicit user action selects one bounded presentation-generation capability.
2. The UI discloses the provider, purpose, selected objects and fields, destination, retention context, expected output use, and disclosure risk.
3. Governance Policy Runtime resolves profile, data, consent, terms, credentials, endpoint, and network admission.
4. Only the admitted representation is exported.
5. Gamma returns an untrusted candidate presentation artifact.
6. The owning component validates and either rejects, quarantines, or explicitly accepts the candidate.
7. Publication, when requested later, uses Publication Gateway as a separate workflow.

Gamma must never be invoked by ingestion, indexing, classification, tagging, routing, synchronization, scheduled work, or background enrichment.

## Provider terms and configuration

The supplied corpus does not establish provider-specific service terms, retention, training or reuse, data location, subprocessors, account configuration, credentials, or endpoint values. Those values must resolve from current controlled runtime authority before enablement and before transfer. An unresolved value blocks the operation.

`integration.toml` contains the integration identity, capability, network boundary, finite limits, failure behavior, evidence requirements, lifecycle, and dependency references. `policy.toml` contains transfer, terms, credential, candidate-adoption, publication, observability, and removal controls. `health.toml` defines passive local health/readiness semantics and does not perform a provider network probe.

## Failure and removal

Failure affects only the requested Gamma capability. No alternate provider or local model is selected. No authoritative mutation occurs. A timeout is an unknown result requiring explicit reconciliation before a new user attempt.

Removal revokes credentials, closes network paths, stops the adapter, preserves required evidence and accepted-output provenance, reconciles pending candidates, and leaves unrelated local capabilities operational.

## Validation

The tests parse all TOML files, compare the declaration to `docs/contracts/integrations/gamma.integration.json`, verify the authority and transfer boundaries, reject hidden endpoints or secrets, and exercise failure/offline invariants without performing network calls.
