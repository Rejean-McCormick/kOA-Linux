# ChatGPT external-service boundary

This directory declares the kOA boundary for the approved `chatgpt` external AI surface. It does not contain a provider SDK, a hidden system backend, a model selection, an endpoint, a credential, or an implementation of ChatGPT.

## Authority

The canonical owner is `docs/contracts/integrations/chatgpt.integration.json`. The integration is:

- active but optional;
- invoked only by explicit user action;
- non-authoritative;
- limited to candidate drafting, summarization, translation, extraction, reconciliation, analysis, and development assistance;
- removable without failure of core local capabilities;
- prohibited from undeclared provider, local-model, or native-AI substitution.

Provider output is untrusted candidate material. It becomes local state only after deterministic validation, required review, explicit acceptance, and admission by the owning component. Generation never implies publication, privilege, policy, rights, identity, release, workflow, or recovery authority.

## Files

- `integration.toml` declares identity, capability scope, data and network boundaries, provider-assurance gates, adoption, prohibited effects, and removal behavior.
- `policy.toml` declares activation, transfer, authority, tool, evidence, degradation, publication, and removal rules.
- `health.toml` declares health, readiness, timeout, retry, circuit-breaker, offline, disabled, and removed behavior.
- `tests/test_boundary.py` proves the declared boundary and its alignment with the canonical contract.
- `tests/test_failure.py` proves failure receipts, closed degradation, no authoritative mutation, and no fallback.

## Operation sequence

1. Resolve the active profile and confirm that ChatGPT is permitted.
2. Require one explicit user action for one declared capability and purpose.
3. Present the provider, destination, exact selected data, fields, attachments, transformations, classification, retention context, intended output use, and material risks.
4. Obtain operation-scoped confirmation and a policy decision.
5. Transfer only the admitted, minimized representation through controlled egress configuration.
6. Receive the response as a separately identified candidate.
7. Validate schema, scope, provenance, policy, rights, and compatibility locally.
8. Let the user or accountable owner accept, edit, reject, or quarantine the candidate.
9. Record only the minimum evidence required for review and recourse.
10. Use the owning component's normal deterministic workflow for any authoritative change.

Cancellation or failure before acceptance produces no authoritative mutation.

## Data and secret boundary

No implicit repository, component-store, tenant, profile, host, or secret access is permitted. `secret` and `no-AI` data are never eligible. Other non-public classes require an exact compatible authority and minimization decision. Hidden application context, unrelated history, unrelated tenant data, private keys, unrestricted credentials, recovery material, privileged tokens, and hidden authority prompts are prohibited.

No endpoint or credential is stored here. Runtime endpoint selection and secret references must come from controlled configuration. Current provider terms, retention, secondary reuse or training, data-location, and deletion controls must be resolved for the actual account and operation. If required assurance cannot be resolved, the operation remains blocked.

## Health and failure

Health and readiness apply only to the optional ChatGPT assistance capability. They do not determine authorization and do not affect unrelated local workflows.

Provider unavailability, quota exhaustion, refusal, timeout, network loss, invalid output, drift, policy denial, failed validation, cancellation, or failed acceptance ends in an explicit non-success state with a correlated failure receipt. No other provider, local model, native model, queued background operation, or authoritative success is substituted.

Conformance tests are hermetic: they parse local declarations and contracts and make no network request, provider call, credential lookup, or model invocation.

## Publication and removal

Publication remains a separate operation owned by Publication Gateway and requires its own request, policy decision, review, and receipt. Disabling or removing this integration stops new operations, clears temporary provider-session state, removes endpoint and credential configuration, preserves authoritative local data, and retains provenance obligations for previously accepted outputs.
