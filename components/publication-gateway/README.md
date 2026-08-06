# Publication Gateway

Publication Gateway is the kOA component that mediates governed publication across authority or disclosure domains. It validates one bounded publication request, preserves the source component's authority, resolves the required identity and governance evidence, delivers only an approved representation through a declared publisher, and records truthful terminal evidence.

It does **not** own source content, source semantic truth, identity records, governance policy, cultural authority, consent grants, destination authoritative state, UCKK destination state, or release-channel identity. It never writes directly to another component's store and publication does not transfer authority.

## This completion bundle

This package-level bundle establishes:

- immutable component metadata and packaging configuration;
- strict, non-secret runtime configuration;
- startup without implicit adapters;
- distinct process health and publication readiness;
- explicit dependency and adapter observations;
- truthful gateway-owned transition receipts;
- a bounded command-line interface for configuration and health inspection.

The domain model, use cases, ports, adapters, public API, migrations, packaging payload, and tests are owned by their existing bundles and are not modified here.

## Configuration

Configuration is loaded from environment variables with the `KOA_PUBLICATION_GATEWAY_` prefix. No private key, password, token, credential, source payload, destination payload, policy decision, or consent record is accepted.

| Variable | Default | Meaning |
| --- | --- | --- |
| `COMPONENT_ID` | `publication_gateway` | Fixed component identity. |
| `CONTRACT_VERSION` | `1.0.0` | Supported component-contract version. |
| `INTERFACE_VERSION` | `1.0.0` | Supported public-interface version. |
| `SERVICE_IDENTITY` | `publication_gateway` | Component-scoped service identity reference. |
| `INSTANCE_ID` | `publication_gateway.local` | Stable local instance identity. |
| `UNIX_SOCKET_PATH` | `/run/koa/sockets/publication-gateway.sock` | Local service socket. |
| `STATE_DIRECTORY` | `/var/lib/koa/publication-gateway` | Gateway-owned durable state. |
| `RUNTIME_DIRECTORY` | `/run/koa/publication` | Ephemeral runtime state. |
| `RECEIPT_DIRECTORY` | `/var/lib/koa/receipts/publication-gateway` | Durable receipt path. |
| `STAGING_DIRECTORY` | `/var/lib/koa/publication-gateway/staging` | Inactive bounded representations. |
| `CACHE_DIRECTORY` | `/var/cache/koa/publication-gateway` | Non-authoritative cache. |
| `MAX_QUEUE_DEPTH` | `1024` | Hard bound for queued publication requests. |
| `MAX_CONCURRENT_PUBLICATIONS` | `8` | Hard execution concurrency bound. |
| `MAX_REQUEST_BYTES` | `8388608` | Maximum accepted request size. |
| `MAX_RETRY_ATTEMPTS` | `3` | Maximum controlled retry attempts. |
| `AUDIT_REQUIRED` | `true` | Whether terminal publication work requires the Audit Broker path. |

Paths must be absolute and normalized. Bounds must be positive, concurrency cannot exceed queue capacity, and no configuration key containing secret material is accepted.

## Startup and readiness

`bootstrap()` never chooses an adapter. Callers provide dependency observations and explicit bindings for the publisher, receipt store, audit sink, rights provider, and policy runtime. Missing bindings do not create a substitute; the process can start for diagnostics while publication readiness remains blocked.

Health and readiness remain distinct:

- **health** reports whether the local process and owned paths are usable;
- **readiness** reports whether new publication work can safely cross the gateway;
- status and queue inspection may remain available while publication is blocked;
- a publication cannot become ready without an explicit publisher and durable receipt path;
- a terminal success cannot be reported before accepted destination acknowledgement and durable local receipt evidence.

## CLI

```text
python -m koa_publication_gateway check-config
python -m koa_publication_gateway health
python -m koa_publication_gateway health --assume-local-paths-ready
```

The development probe flag supplies bounded observations only. It does not discover, configure, authorize, or bind an adapter and therefore does not make publication ready.

## Receipt boundary

`receipts.py` creates evidence only for transitions owned by Publication Gateway. A committed publication receipt requires:

1. an allow decision;
2. completed delivery execution;
3. an accepted destination acknowledgement reference;
4. a destination object reference;
5. a ready local receipt path;
6. execution and decision evidence references.

Preparation, queueing, transport attempts, unknown acknowledgement, partial delivery, and receipt-persistence failure cannot produce a committed-success outcome.
