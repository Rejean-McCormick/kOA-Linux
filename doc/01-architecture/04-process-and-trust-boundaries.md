# Process and Trust Boundaries

## 1. Security domains

At minimum, the host defines separate domains for:

- graphical session shell;
- Konnaxion services;
- Orgo services;
- Kristal Runtime;
- governance policy runtime;
- audit broker;
- publication gateway;
- node agent;
- optional AI/specialized engines;
- update and recovery.

Each domain SHOULD have a dedicated Unix identity, container namespace, storage path, SELinux label or equivalent, resource limits, and network policy.

## 2. Privilege hierarchy

```text
Unprivileged UI
    ↓ local authenticated API
Domain service
    ↓ policy request
koa-policy-runtime
    ↓ signed/receipted decision
koa-node-agent
    ↓ fixed operation
Linux mechanism
```

No service may pass arbitrary shell fragments, filesystem paths, unit names, device names, or container arguments to the privileged broker unless the operation contract validates them against a closed schema and allowlist.

## 3. Konnaxion / Orgo boundary

Konnaxion MUST NOT read Orgo private data directly. Orgo MUST NOT publish into Konnaxion by direct database write. Exchange occurs through:

- authenticated domain API;
- asynchronous event contract;
- `koa-publication-gateway`;
- signed/exported artifact;
- approved synchronization contract.

## 4. Kristal boundary

Kristal content identity excludes tenant workflow state. Konnaxion and Orgo may reference Kristal identifiers, but MUST keep assignments, approvals, ACLs, distribution status, and operational audit outside the hashed epistemic payload.

## 5. AI boundary

AI processes run in a separate capability domain. They receive only data classes explicitly authorized by policy. Restricted cultural, personal, or operational data MUST NOT be mounted or transmitted merely because an application promises not to use it.

## 6. Signing boundary

Release signing keys MUST NOT be available to ordinary build workers, Konnaxion, Orgo, or the session shell. Signing requests MUST identify artifact hashes and policy context. High-assurance signing SHOULD require independent review or threshold approval.

## 7. Recovery boundary

Recovery uses a separate target and reduced service set. Recovery credentials and trust transitions MUST be logged and SHOULD require dual control for high-assurance deployments.

## 8. Resource boundaries

CPU, memory, process count, storage, I/O, and network egress MUST be bounded per service. Heavy optional engines MUST NOT be able to starve policy evaluation, local identity, active Kristal access, Orgo critical workflows, or recovery.
