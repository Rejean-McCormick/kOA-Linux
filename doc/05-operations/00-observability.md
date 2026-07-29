# Observability

## 1. Goals

Observability supports reliability, accountability, security, and reconstruction without exposing unnecessary sensitive content.

## 2. Signals

### Metrics

- availability and latency by capability;
- queue depth and retry rate;
- policy decision outcomes and evaluation time;
- activation and rollback success;
- synchronization age and conflict count;
- storage/cache pressure;
- verification failures;
- resource saturation;
- export/restore test results.

### Logs

Structured logs include timestamp, node, tenant where permitted, service, stage, outcome, error code, dependency, attempt, duration, and correlation ID. Raw claims, testimony, tokens, or secrets are excluded by default.

### Traces

Distributed tracing MAY be used across online services. Trace context MUST NOT create cross-tenant correlation leakage. Offline flows preserve correlation identifiers for later reconstruction.

### Receipts

Receipts are durable evidence for policy, privilege, release, publication, and governance transitions. They are not interchangeable with debugging logs.

## 3. Health model

Health distinguishes:

- process alive;
- dependency reachable;
- contract ready;
- capable of local read;
- capable of write;
- capable of authoritative publication/execution;
- degraded but safe.

## 4. Alerting

Alerts are tied to user or governance impact, not only infrastructure thresholds. Critical alerts include trust failure, repeated activation failure, audit gap, cross-tenant denial anomaly, revocation staleness, and recovery failure.

## 5. Offline operation

Nodes retain bounded local metrics, logs, and receipts. Forwarding resumes with backoff and idempotency. Storage exhaustion policies prioritize security and decision evidence over verbose diagnostics.
