# Suno external-service boundary

This directory declares the kOA boundary for the approved Suno external media-generation surface. It does not contain a provider SDK, credentials, endpoint implementation, background worker, or media-generation logic.

## Authority

Suno is optional and non-authoritative. One explicit user action may request one declared audio or music-generation operation. The provider result returns as a candidate media artifact and remains outside authoritative kOA state until the owning kOA Mediatheque workflow validates integrity, media type, size, rights, policy, provenance, and user acceptance.

Generation does not imply import, acceptance, publication, privilege, policy, release activation, consent, or rights resolution. Publication is a separate operation through Publication Gateway and its policy and receipt contracts.

## Files

- `integration.toml` declares identity, classification, capability scope, trigger, authority, transfer, output, networking, and removal behavior.
- `policy.toml` declares allowed and forbidden triggers, data classes, candidate admission, authority prohibitions, resilience, evidence, and failure outcomes.
- `health.toml` declares optional-capability health and readiness without exposing secrets or payloads.
- `tests/test_boundary.py` verifies the closed boundary and contract identifiers.
- `tests/test_failure.py` verifies safe failure, offline behavior, removal, and absence of substitution.

## Operation sequence

1. Resolve an active profile that permits `suno`.
2. Require an explicit visible user action for a declared capability.
3. Display provider, purpose, selected data, destination, retention context, limitations, and cancellation behavior.
4. Transfer only the admitted minimum representation.
5. Receive the provider result into a candidate or quarantine namespace.
6. Record provider and operation identity and create provenance evidence.
7. Validate the candidate through the owning component.
8. Require user approval before local admission.
9. Use a separate Publication Gateway request for any publication.

## Safe degradation

Network loss, provider refusal, quota exhaustion, incompatibility, invalid output, or removal disables only the requested external-media capability. Deterministic local kOA Mediatheque ingestion, integrity verification, metadata capture, rendering, storage, export, backup, and restore remain available. No provider, local model, or native AI capability is substituted silently.

## Secrets and networking

No secret is stored in this directory. Health output may report whether a credential reference is configured, but never its value. Tests parse local files only and make no network calls.
