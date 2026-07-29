# Component — `koa-node-agent`

## 1. Purpose

`koa-node-agent` is the sole narrow privileged broker for normal kOA node management. It exposes fixed high-level operations rather than a command execution interface.

## 2. Allowed operation classes

A baseline agent MAY implement:

- inspect node identity and booted release;
- stage and activate a verified OS image;
- activate or roll back a declared service bundle;
- activate or roll back a Governance Policy Bundle;
- install, activate, pin, unpin, or quarantine a Kristal Runtime Pack;
- manage declared encrypted volumes;
- import a verified offline bundle;
- export approved node evidence;
- enter recovery target;
- restart an allowlisted service group;
- rotate a node-scoped key through a governed workflow.

Every operation MUST have a closed schema, preconditions, authorization class, idempotency behavior, timeout, result schema, and stable error codes.

## 3. Prohibited interface

The agent MUST NOT expose:

- arbitrary shell execution;
- arbitrary systemd unit control;
- arbitrary file copy or path traversal;
- arbitrary container image or argument execution;
- generic package-manager access;
- unrestricted device access;
- raw private-key export.

## 4. Request contract

A request contains at least:

```json
{
  "operation": "activate_runtime_pack",
  "request_id": "uuid",
  "tenant_id": "tenant:example",
  "policy_decision_id": "decision:...",
  "artifact_id": "sha256:...",
  "expected_active_id": "sha256:...",
  "parameters": {},
  "correlation_id": "corr:..."
}
```

The agent verifies caller identity, decision binding, decision expiry, artifact identity, current state, operation allowlist, and replay/idempotency state.

## 5. Atomicity

Activation MUST use an atomic pointer, boot slot, transaction, or equivalent mechanism. A crash MUST leave either the previous valid state or the complete new state active—never a partially activated state.

## 6. Idempotency

Repeated requests with the same request identity and equivalent body MUST return the recorded result. Reuse with a different body MUST fail.

## 7. Audit

The agent emits an operation receipt containing:

- request and policy decision identities;
- authenticated caller;
- before and after state;
- artifact hashes;
- result and reason codes;
- duration;
- recovery or rollback token when applicable.

## 8. Hardening

The service SHOULD use systemd sandboxing, a dedicated SELinux domain, minimal Linux capabilities, `NoNewPrivileges`, protected system paths, private temporary storage, restricted address families, bounded resources, and a local Unix socket.

## 9. Emergency path

Break-glass actions use separate operation names and stronger policy. The agent MUST NOT infer emergency authorization from caller UID alone.
