# Node Profiles

## 1. Profile model

A node profile is a signed declaration of roles, services, minimum resources, trust assumptions, network exposure, and offline guarantees. A node MUST NOT silently enable a role not declared by its profile.

## 2. `koa-endpoint`

Purpose: user-facing local workstation or terminal.

Required capabilities:

- `koa-session-shell`;
- Konnaxion and Orgo workspaces appropriate to the tenant;
- Kristal verification, local pack store, constrained query runtime, and reader-policy evaluation;
- local identity and policy evaluation;
- local queues and resumable synchronization;
- safe import of signed offline bundles;
- last-known-good rollback and user-visible status;
- recovery environment.

Constraints:

- no mandatory cloud connection;
- no full Kristal compiler requirement;
- no mandatory SenTient, Architect Build, Solr, Elasticsearch, or large model runtime;
- low idle resource use;
- support for constrained and refurbished hardware profiles where validated.

## 3. `koa-sovereign-hub`

Purpose: local institutional or community infrastructure.

Typical capabilities:

- Konnaxion API and local web delivery;
- Orgo Core and workflow services;
- PostgreSQL and message broker;
- tenant identity and trust services;
- Kristal repository and distribution cache;
- publication gateway;
- local container registry;
- local backup and restore;
- LAN operation without Internet;
- controlled external federation.

The hub MUST preserve operation when upstream services are unavailable. Public and private interfaces MUST use separate network and disclosure policies.

## 4. `koa-build-farm`

Purpose: heavy deterministic and assisted build workloads.

Typical capabilities:

- Kristal Compiler;
- optional Claim-IR extraction;
- SenTient resolution;
- Architect Build;
- validation engines;
- large indexes and content-addressed caches;
- reproducibility workers;
- artifact assembly.

Private release signing SHOULD occur in a separate security domain. Build workers MUST NOT be trusted solely because they produced an artifact; outputs require independent verification.

## 5. `koa-control-plane`

Purpose: release, policy, registry, and fleet governance.

Typical capabilities:

- Release Set publication;
- service and artifact registries;
- policy registry;
- trust-root and revocation distribution;
- fleet inventory and health summaries;
- approval workflows;
- central audit aggregation where authorized.

The control plane MUST NOT be required for an endpoint's minimum offline capability.

## 6. Optional specialized profiles

Deployments MAY define:

- kiosk or classroom profile;
- mobile field node;
- air-gapped Orgo node;
- cultural archive node;
- public library node;
- disaster-response hub;
- high-assurance review station.

Every specialized profile MUST inherit the founding invariants and specify its deviations, limits, and test suite.

## 7. Role composition

Profiles MAY be combined on one physical machine only when the resulting trust and resource boundaries remain acceptable. Build/signing, public/private, and multi-tenant combinations require explicit threat-model review.
