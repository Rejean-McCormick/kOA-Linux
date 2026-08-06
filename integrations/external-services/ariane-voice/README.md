# Ariane Voice external-service boundary

Ariane Voice is the approved, optional external voice-input surface for the Ariane subsystem. It accepts one explicitly initiated, bounded voice operation and may return a candidate transcript and candidate navigation intent. It is never an Ariane command executor and never acquires authority over local state.

## Authority chain

```text
explicit user voice-mode activation
→ active-profile permission
→ governed transfer decision
→ exact transfer preview and confirmation
→ scoped audio transfer to the managed provider endpoint
→ candidate transcript or candidate navigation intent
→ local Ariane schema and deterministic command validation
→ local ambiguity and safety handling
→ local confirmation when required
→ Ariane-owned guidance or execution
```

The external service cannot click, type, select hidden targets, bypass an Atlas, authorize an action, confirm a sensitive action, publish content, change policy, grant privilege, or write Ariane or application state.

## Activation and data transfer

The integration is disabled by default. Repository presence, credentials, endpoint reachability, or a profile allowlist does not activate it. Every operation requires explicit user action, a bounded request, a transfer preview, an applicable policy decision, and confirmation for the exact prepared audio transfer.

Only current-session audio frames and the minimum operation metadata may leave kOA. Repository data, component stores, unrelated tenant or profile state, secrets, unrestricted logs, screenshots, clipboard contents, and hidden application context are excluded. Provider terms, retention, training or reuse behavior, data location, account separation, and endpoint policy must be resolved before enablement.

## Candidate handling

Returned material remains untrusted and non-authoritative. Ariane owns candidate validation, deterministic goal resolution, ambiguity rejection, confirmation, authorization, execution, verification, and resulting state. Unknown, incomplete, stale, unsupported, ambiguous, or unsafe candidates are rejected or require explicit local confirmation before any side effect.

## Failure and removal

Provider unavailability, timeout, invalid output, transfer rejection, policy denial, cancellation, or local validation failure affects only external voice. Keyboard, pointer, touch, menu, shortcut, accessibility, structured local commands, guidance, and deterministic navigation continue.

Failures produce minimized, correlated evidence without raw audio, transcripts, candidate parameters, credentials, or unrelated context. There is no background queue, unbounded retry, silent provider substitution, local-model fallback, or authoritative mutation on failure.

Removing the integration revokes its credential reference, closes its egress path, stops its adapter, preserves required evidence for already accepted results, and verifies that local Ariane navigation remains operational.

## Files

- `integration.toml` — identity, capability, dependencies, data flow, transport, resilience, removal.
- `policy.toml` — transfer, authority, privacy, provider-term, credential, candidate, and evidence rules.
- `health.toml` — liveness/readiness separation, provider degradation, reason codes, failure evidence.
- `tests/test_boundary.py` — closed authority and data-boundary conformance.
- `tests/test_failure.py` — failure, offline, retry, fallback, and evidence conformance.

No provider endpoint or credential is stored in this directory. Runtime configuration must supply managed references after all prerequisite contracts and Ariane adapter boundaries are present and validated.
