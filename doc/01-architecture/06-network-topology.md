# Network Topology

## 1. Network zones

```text
User Session Zone
        |
Application Gateway
   |             |
Public Zone    Private Zone
Konnaxion      Orgo
   |             |
Publication Gateway
        |
Kristal Distribution / Federation Zone
        |
External Networks
```

## 2. Default-deny principle

Inbound and outbound communication MUST be denied unless declared by service profile. Internal location does not imply trust. Every cross-domain request requires authenticated identity, tenant context, action scope, and correlation data.

## 3. Public zone

Konnaxion-facing services MAY expose controlled HTTP endpoints. Public services MUST NOT share an addressable database or unrestricted filesystem with Orgo.

## 4. Private zone

Orgo SHOULD have no public inbound endpoint by default. Remote access requires tenant policy, strong authentication, rate limits, and audit. Hermetic mode MUST remain supported where declared.

## 5. Node-local APIs

Privileged and policy APIs SHOULD use Unix domain sockets with peer credential verification. TCP loopback is permitted only when mutual authentication and equivalent confinement are demonstrated.

## 6. Federation

Federation peers are explicitly configured. Trust is scoped by tenant, environment, channel, authority, and artifact type. A valid signature from another trust domain MUST NOT be accepted automatically.

## 7. Offline and intermittent links

Synchronization MUST be resumable, idempotent, bandwidth-aware, and manifest-first. Transfer priority SHOULD be:

1. revocations and trust-root updates;
2. security and governance policies;
3. critical Orgo operational state;
4. Kristal manifests and indexes;
5. essential content;
6. large media;
7. optional caches.

## 8. Resilience controls

Remote calls MUST use timeout budgets, exponential backoff with jitter, circuit breakers, rate limits, and bulkheads where failure could cascade. Reconnection MUST NOT create a retry storm.

## 9. Name and time dependencies

Local correctness MUST NOT depend on public DNS or online time sources during offline operation. The node SHOULD cache necessary name data and record clock uncertainty. Expiry decisions affected by uncertain time MUST fail safely and visibly.
