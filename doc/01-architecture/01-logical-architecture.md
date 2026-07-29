# Logical Architecture

## 1. Planes

```text
Experience Plane
├── koa-session-shell
├── Konnaxion workspace
└── Orgo workspace

Application Plane
├── Konnaxion Core
├── Orgo Core
├── Kristal Runtime Plane
└── Specialized adapters

Governance Plane
├── koa-policy-runtime
├── policy registry
├── decision receipts
├── recourse workflows
└── disclosure, rights, and AI policies

Node Plane
├── koa-node-agent
├── trust store
├── release manager
├── audit broker
├── export and recovery
└── local synchronization transport

Linux Mechanism Plane
├── systemd
├── SELinux or equivalent LSM
├── namespaces, cgroups, and seccomp
├── Podman and Quadlet
├── storage encryption and integrity
└── Wayland, graphics, audio, and input
```

## 2. Dependency rule

Dependencies point toward more stable contracts:

```text
UI → domain API → domain ports → adapters
                         ↓
                 policy decision API
                         ↓
                  node operation API
```

Konnaxion and Orgo MUST NOT:

- execute arbitrary root commands;
- modify the immutable system image;
- read signing private keys;
- activate a Runtime Pack by directly moving files;
- read or write the other domain's internal database;
- convert an advisory result into a privileged operation without workflow and policy evaluation.

## 3. Contract types

### 3.1 Synchronous contracts

Use only when an immediate response is required:

- local authentication;
- policy decision;
- Kristal query;
- node status;
- interactive user action.

Synchronous chains MUST have explicit timeout budgets, cancellation, bounded retries, and degraded behavior.

### 3.2 Asynchronous contracts

Prefer for:

- synchronization;
- builds;
- publication;
- distribution;
- telemetry;
- notifications;
- SenTient and Architect work;
- large export/import operations.

Messages MUST carry stable event identifiers and correlation identifiers. Consumers MUST be idempotent. Poison messages MUST enter a reviewable dead-letter flow.

### 3.3 Artifact contracts

Use for immutable, signed, or content-addressed objects:

- OS image;
- service bundle;
- policy bundle;
- Kristal artifacts;
- offline bundle;
- Sovereignty Bundle.

## 4. Consistency model

Internal product transactions use ACID where possible. When a transaction must emit an external event, the product MUST use a Transactional Outbox or an equivalent atomic handoff.

Long-running distributed workflows are durable state machines. A compensation may be declared only when it restores a valid business state. An incorrect publication, recognition, or signature normally requires revocation or a superseding release, not deletion of history.

## 5. Modularity

Konnaxion and Orgo SHOULD be modular monoliths or coherent service groups, not artificial microservice constellations. Internal modules MUST expose public interfaces and MUST NOT reach into each other's private persistence structures.

Independently deployable services are justified when one or more of the following apply:

- different technology stack;
- independent trust domain;
- materially different scaling profile;
- optional availability;
- heavy resource isolation;
- separate release authority.

Expected independent services include SenTient, Architect Build, Kristal Compiler, signing/authority services, distribution registries, and central observability.

## 6. Policy and enforcement sequence

```text
Request
  ↓
Authentication and context resolution
  ↓
koa-policy-runtime
  ↓ allow / deny / require-review + receipt
Workflow approval when required
  ↓
koa-node-agent allowlisted operation
  ↓
Linux mechanism
  ↓
operation receipt and audit event
```

The policy runtime never performs unrestricted node mutation. The node agent never invents policy.
