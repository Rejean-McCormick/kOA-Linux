# Capability-Based Degradation

## 1. Principle

The system degrades capabilities, not truth labels. It distinguishes the ability to inspect, advise, publish, and execute.

## 2. Reference matrix

| State | Inspect context | Use as advisory | Publish as reference | Execute/activate |
|---|---:|---:|---:|---:|
| verified and active | yes | yes | policy-dependent | yes |
| provisional | labeled | limited | no by default | policy-dependent |
| contested | labeled | limited | no as single reference | no by default |
| expired/stale | labeled | limited | no | no |
| revoked | audit/quarantine only | no | no | no |
| corrupted | no | no | no | no |
| incompatible | manifest/diagnostic only | no | no | no |

## 3. Dependency failures

- network loss: local capability continues;
- central identity loss: cached local identity follows declared expiry policy;
- policy runtime loss: sensitive writes deny; safe reads may continue;
- audit forwarding loss: local capture continues;
- Konnaxion loss: Orgo and Kristal may continue;
- Orgo loss: Konnaxion and approved public knowledge may continue;
- AI loss: assistance stops; core correctness continues;
- build farm loss: active releases remain usable.

## 4. Visibility

Users and operators MUST see degraded state, affected capability, last successful synchronization, active release identities, and next safe action. Graceful degradation without visible logging is a failure.

## 5. Restoration

Recovery from degradation uses bounded retries with jitter, health revalidation, and replay-safe queues. A returning dependency MUST NOT immediately receive an uncontrolled backlog storm.
