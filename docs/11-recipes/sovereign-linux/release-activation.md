<!-- KOA:DOC-META:BEGIN GENERATED
{
  "doc_id": "DOC-REC-SOV-001",
  "document_class": "recipe",
  "status": "active",
  "language": "en",
  "layer": "implementation_recipe",
  "scope": [
    "profile:sovereign_linux_node",
    "profile_overlay:sovereign_offline",
    "profile_overlay:high_assurance"
  ],
  "canonical_refs": [
    "generated/authority-manifest.json",
    "generated/decision-index.json",
    "contracts/system.contract.json#/release_model",
    "contracts/system.contract.json#/health_and_readiness",
    "contracts/system.contract.json#/safe_degradation",
    "contracts/system.contract.json#/offline_behavior",
    "contracts/profiles/sovereign-linux-node.profile.json",
    "contracts/profiles/sovereign-offline.profile.json",
    "contracts/profiles/high-assurance.profile.json",
    "generated/component-catalog.json#/components/koa_node_agent",
    "contracts/components/koa-node-agent.component.json",
    "contracts/components/identity-and-trust.component.json",
    "contracts/components/governance-policy-runtime.component.json",
    "contracts/components/audit-broker.component.json",
    "contracts/artifact-classes.contract.json",
    "contracts/release-channels.contract.json",
    "contracts/artifact-contracts/release-set.schema.json",
    "contracts/artifact-contracts/offline-bundle.schema.json",
    "contracts/artifact-contracts/decision-receipt.schema.json",
    "contracts/artifact-contracts/resource-envelope.schema.json",
    "generated/test-catalog.json",
    "generated/evidence-catalog.json",
    "generated/requirements-index.json",
    "generated/assertion-index.json",
    "generated/traceability.json",
    "generated/exception-index.json",
    "06-lifecycle/01-artifact-classes.md",
    "06-lifecycle/11-offline-bundles.md",
    "07-security/03-identity-trust-and-signatures.md",
    "08-operations/02-health-and-readiness.md",
    "08-operations/11-offline-operations.md"
  ],
  "decision_ids": [
    "DEC-REL-001",
    "DEC-PROFILE-001",
    "DEC-PROFILE-BASELINE-001",
    "DEC-COMP-001",
    "DEC-DATA-001",
    "DEC-GOV-001",
    "DEC-AI-001",
    "DEC-ARI-001",
    "DEC-UCKK-001"
  ],
  "requirement_ids": [
    "REQ-LIFE-CLASS-001",
    "REQ-LIFE-CLASS-002",
    "REQ-LIFE-CLASS-003",
    "REQ-LIFE-CLASS-004",
    "REQ-LIFE-CLASS-005",
    "REQ-LIFE-CLASS-006",
    "REQ-LIFE-CLASS-007",
    "REQ-LIFE-CLASS-008",
    "REQ-LIFE-CLASS-009",
    "REQ-LIFE-CLASS-010",
    "REQ-LIFE-CLASS-011",
    "REQ-LIFE-CLASS-012",
    "REQ-LIFE-CLASS-013",
    "REQ-LIFE-CLASS-014",
    "REQ-LIFE-CLASS-015",
    "REQ-LIFE-CLASS-016",
    "REQ-LIFE-CLASS-017",
    "REQ-LIFE-CLASS-018",
    "REQ-LIFE-CLASS-019",
    "REQ-LIFE-CLASS-020",
    "REQ-LIFE-CLASS-021",
    "REQ-LIFE-CLASS-022",
    "REQ-LIFE-CLASS-023",
    "REQ-LIFE-CLASS-024",
    "REQ-LIFE-CLASS-025",
    "REQ-LIFE-CLASS-026",
    "REQ-LIFE-OFF-001",
    "REQ-LIFE-OFF-002",
    "REQ-LIFE-OFF-003",
    "REQ-LIFE-OFF-004",
    "REQ-LIFE-OFF-005",
    "REQ-LIFE-OFF-006",
    "REQ-LIFE-OFF-007",
    "REQ-LIFE-OFF-008",
    "REQ-LIFE-OFF-009",
    "REQ-LIFE-OFF-010",
    "REQ-LIFE-OFF-011",
    "REQ-LIFE-OFF-012",
    "REQ-LIFE-OFF-013",
    "REQ-LIFE-OFF-014",
    "REQ-LIFE-OFF-015",
    "REQ-LIFE-OFF-016",
    "REQ-LIFE-OFF-017",
    "REQ-LIFE-OFF-018",
    "REQ-LIFE-OFF-019",
    "REQ-LIFE-OFF-020",
    "REQ-LIFE-OFF-021",
    "REQ-LIFE-OFF-022",
    "REQ-LIFE-OFF-023",
    "REQ-LIFE-OFF-024",
    "REQ-LIFE-OFF-025",
    "REQ-LIFE-OFF-026",
    "REQ-LIFE-OFF-027",
    "REQ-LIFE-OFF-028",
    "REQ-OPS-HEALTH-020",
    "REQ-OPS-HEALTH-021",
    "REQ-OPS-HEALTH-022",
    "REQ-OPS-HEALTH-027",
    "REQ-OPS-HEALTH-028",
    "REQ-OPS-HEALTH-030",
    "REQ-OPS-OFF-018",
    "REQ-OPS-OFF-019",
    "REQ-OPS-OFF-020",
    "REQ-OPS-OFF-021",
    "REQ-OPS-OFF-028",
    "REQ-OPS-OFF-029",
    "REQ-OPS-OFF-030",
    "REQ-OPS-OFF-032"
  ],
  "lock_ids": [
    "LOCK-LIFE-001",
    "LOCK-LIFE-002",
    "LOCK-LIFE-003",
    "LOCK-LIFE-004",
    "LOCK-PROFILE-001",
    "LOCK-PROFILE-002",
    "LOCK-COMP-001",
    "LOCK-COMP-002",
    "LOCK-DATA-001",
    "LOCK-GOV-001",
    "LOCK-OPS-001",
    "LOCK-OPS-002",
    "LOCK-OPS-003",
    "LOCK-OPS-004",
    "LOCK-SEC-001",
    "LOCK-SEC-002",
    "LOCK-SEC-003",
    "LOCK-AI-001",
    "LOCK-AI-002",
    "LOCK-ARI-001",
    "LOCK-ARI-002",
    "LOCK-UCKK-001",
    "LOCK-UCKK-002"
  ],
  "exception_ids": [],
  "depends_on": [
    "DOC-LIFE-001",
    "DOC-LIFE-011",
    "DOC-SEC-003",
    "DOC-OPS-002",
    "DOC-OPS-011"
  ],
  "tags": [
    "recipe",
    "sovereign-linux",
    "release-activation",
    "release-set",
    "four-release-channels",
    "staging",
    "atomic-activation",
    "known-good",
    "rollback",
    "forward-repair",
    "offline-bundle",
    "health-acceptance",
    "recovery",
    "non-normative"
  ]
}
KOA:DOC-META:END -->

# Sovereign Linux Release Activation

> **Recipe status:** Active, non-normative implementation guidance.  
> **Authority rule:** This recipe does not define release identities, signers, compatibility, activation order, migrations, policy outcomes, health contracts, or rollback floors. It executes values already accepted by the active Release Set, artifact-class contracts, profile contracts, component contracts, and authority release.

## Recipe Identity

| Field | Value |
| --- | --- |
| Recipe ID | `RECIPE-SOV-001` |
| Title | Sovereign Linux Release Activation |
| Status | `active` |
| Version | `1.0.0` |
| Owner | `operations-architecture` |
| Last reviewed | `2026-08-03` |
| Primary profile | `sovereign_linux_node` |
| Optional overlays | `sovereign_offline`, `high_assurance` |
| Execution authority | kOA Node Agent through its registered narrow privilege boundary |
| Supported source paths | Verified local registry, verified transfer, or validated offline bundle |
| Supersedes | None |
| Replaced by | None |

## 1. Purpose

This recipe activates a verified kOA Release Set on a sovereign Linux node while preserving:

- independent `system`, `services`, `governance`, and `knowledge` release channels;
- exact artifact identities and signatures;
- target-profile compatibility;
- trusted-time and revocation state;
- one durable activation transaction;
- explicit staging before activation;
- channel-owner adapters;
- migration checkpoints;
- active and previous known-good state;
- capability-specific acceptance;
- reboot-aware continuation;
- rollback where reversal is safe;
- forward repair where reversal is unsafe;
- bounded receipts and protected evidence;
- offline execution when all prerequisites are locally available.

A Release Set is a signed compatibility statement for a tested combination. It does not merge the authority, signer, lifecycle, or rollback semantics of its channels.

The recipe uses this operational sequence:

```text
receive
  → quarantine
  → verify envelope
  → verify each artifact
  → resolve Release Set
  → calculate compatibility
  → stage every channel independently
  → establish backup and known-good state
  → validate activation plan
  → activate through channel adapters
  → cross reboot boundary when declared
  → accept capabilities
  → commit active Release Set identity
  → retain evidence and recovery material
```

A staged artifact is not active.

A running process is not accepted.

A successful reboot is not sufficient acceptance.

A queued or requested activation is not a completed activation.

## 2. Non-Normative Status

This recipe is one supported implementation procedure.

It does not replace:

- `contracts/artifact-classes.contract.json`;
- `contracts/release-channels.contract.json`;
- `contracts/artifact-contracts/release-set.schema.json`;
- `contracts/artifact-contracts/offline-bundle.schema.json`;
- the selected sovereign Linux profile;
- component-specific activation contracts;
- identity, trust, signing, policy, cultural-rights, health, backup, restore, or recovery contracts.

When a command or example conflicts with active canonical authority, execution stops and the canonical source is followed through an updated recipe or accepted profile-specific procedure.

The recipe does not:

- rebuild an artifact;
- retag an image as a new identity;
- update a Release Set;
- add a missing signer;
- invent activation order;
- downgrade below a trust, revocation, policy, schema, or security floor;
- activate one channel by silently embedding another;
- treat removable media as trusted;
- change data ownership;
- bypass the kOA Node Agent;
- directly edit component databases;
- consider a process alive as evidence of full readiness;
- erase failed activation evidence.

## 3. Scope

### 3.1 Included

The recipe covers:

- planned release activation;
- emergency activation under an already accepted emergency policy;
- online-local and offline sources;
- Release Set and channel artifact verification;
- quarantine and staging;
- compatibility and target-profile checks;
- migration preparation;
- backup and checkpoint preparation;
- activation-plan generation and validation;
- channel adapter execution;
- reboot continuation;
- health and representative acceptance;
- activation receipts;
- rollback and forward repair;
- cleanup and retained known-good material.

### 3.2 Excluded

The recipe does not cover:

- building or signing releases;
- changing trust roots;
- initial sovereign-node installation;
- factory reset;
- tenant export or credible exit;
- authoring governance policy;
- artifact publication;
- emergency-policy approval;
- arbitrary break-glass shell access;
- unsupported downgrade;
- changing the selected system-image mechanism;
- replacing the node agent's privilege model;
- defining database migration content;
- repairing component data through direct storage writes.

### 3.3 Channel coverage

The four channels are:

| Channel | Representative artifacts | Activation owner |
| --- | --- | --- |
| `system` | Signed immutable OS image, node services, recovery environment, host configuration owned by the system artifact class | kOA Node Agent through the profile-selected system activator |
| `services` | Signed service artifacts and service bundle, unit or container declarations, migrations, resource and health contracts | Service artifact owner through the profile-selected service activator |
| `governance` | Governance Policy Bundle, consent and disclosure policy modules, reason and obligation catalogs | Governance Policy Runtime lifecycle adapter |
| `knowledge` | Kristal, Runtime Pack, PGF, language, Ariane, approved knowledge, and other knowledge-channel artifacts | Applicable runtime or artifact owner through knowledge activation adapters |

The exact artifact set belongs to the Release Set and artifact-class registries.

### 3.4 Activation scope

A transaction can activate:

- a complete Release Set containing all four channels; or
- an explicitly compatible channel subset when the Release Set, profile, and artifact contracts permit independent activation.

The activation plan records which scope is used.

## 4. Canonical References

### 4.1 Decisions

- `DEC-REL-001`
- `DEC-PROFILE-001`
- `DEC-PROFILE-BASELINE-001`
- `DEC-COMP-001`
- `DEC-DATA-001`
- `DEC-GOV-001`
- `DEC-AI-001`
- `DEC-ARI-001`
- `DEC-UCKK-001`

### 4.2 Lifecycle and operations

- `06-lifecycle/01-artifact-classes.md`
- `06-lifecycle/11-offline-bundles.md`
- `08-operations/02-health-and-readiness.md`
- `08-operations/11-offline-operations.md`

### 4.3 Security

- `07-security/03-identity-trust-and-signatures.md`
- active trust, revocation, signing, and recipient contracts;
- active policy and cultural-rights contracts for protected artifact content.

### 4.4 Schemas and registries

- `contracts/artifact-contracts/release-set.schema.json`
- `contracts/artifact-contracts/offline-bundle.schema.json`
- `contracts/artifact-contracts/decision-receipt.schema.json`
- `contracts/artifact-classes.contract.json`
- `contracts/release-channels.contract.json`
- `contracts/profiles/sovereign-linux-node.profile.json`
- `generated/test-catalog.json`
- `generated/evidence-catalog.json`

### 4.5 Requirements and locks

The generated metadata lists the applicable lifecycle, health, offline, profile, component, data, governance, security, AI, Ariane, and UCKK requirement and lock identities.

The requirements registry owns the exact statements.

## 5. Preconditions

### 5.1 Authority prerequisites

Before activation:

- the Release Set is published or otherwise valid for the source route;
- every selected artifact is verified and approved for the target node;
- all required owner decisions are accepted;
- the target profile and overlays are active;
- required exceptions are valid and listed;
- required migrations and rollback or forward-repair paths are accepted;
- the activation order is derived from the accepted compatibility and migration graph;
- the kOA Node Agent and channel adapters match the active component and profile contracts.

### 5.2 Node prerequisites

The node has:

- stable power for the activation window;
- local console or profile-approved recovery access;
- a verified recovery environment;
- active and previous known-good identities;
- sufficient storage for quarantine, staging, backup, transaction evidence, and rollback material;
- trusted local time with acceptable confidence;
- current enough trust and revocation state for the operation;
- healthy local identity and policy evaluation;
- healthy receipt and private-evidence storage;
- no competing activation transaction;
- no active recovery, restore, or migration that conflicts with the release.

### 5.3 Data prerequisites

Before any migration:

- source component ownership resolves;
- current schema and migration state are known;
- a profile-appropriate checkpoint or backup is verified;
- migration interruption and resume behavior is known;
- rollback compatibility with old and new code is proven where rollback is claimed;
- irreversible steps identify a forward-repair artifact or procedure;
- queue, outbox, replay, and receipt state are included when required.

### 5.4 Operator prerequisites

The operator has:

- an authenticated identity;
- the role required to request activation;
- a valid maintenance or emergency authorization receipt;
- access to bounded release status and recovery procedures;
- no direct root shell requirement for ordinary activation.

The operator invokes the Node Agent or an approved management surface. The Node Agent performs privileged host transitions through its narrow contract.

## 6. Inputs and Outputs

### 6.1 Inputs

| Input | Canonical owner | Sensitive |
| --- | --- | ---: |
| Release Set identity, version, digest, signatures, compatibility | Release Set artifact | No |
| Channel artifact identities and digests | Artifact manifests | No |
| Target profile and overlays | Profile contracts | No |
| Trust roots and revocation state | Identity and Trust | Yes, protected |
| Activation and maintenance authorization | Governance workflow and receipt | Protected |
| Migration plans and checkpoints | Artifact and component lifecycle contracts | Protected where data details exist |
| Health and representative tests | Component and test contracts | No or protected by test data |
| Offline bundle carrier and envelope | Offline-bundle contract | No |
| Previous known-good identities | Node lifecycle state | Protected operational data |
| Resource envelope | Profile and Resource Governor | No |

### 6.2 Outputs

| Output | Destination | Authority |
| --- | --- | --- |
| Quarantine record | Node import boundary | Non-authoritative |
| Verification report | Transaction evidence | Evidence only |
| Staged artifact records | Channel-owned staging areas | Inactive |
| Activation plan | Transaction directory | Derived operational control |
| Activation state | Transaction directory | Operational state |
| Channel activation receipts | Receipt store | Attributable evidence |
| Accepted active identities | Channel lifecycle owners | Active authority |
| Active Release Set binding | Node lifecycle state | Compatibility record |
| Rollback or forward-repair result | Transaction and recovery records | Operational state |
| Health and conformance evidence | Evidence registry destination | Evidence |
| Retained previous known-good state | Channel and node recovery storage | Recovery authority |

### 6.3 Durable transaction state

The transaction directory contains:

```text
activation-plan.json
activation-plan.sha256
activation-order.txt
transaction-state.json
logs/
evidence/
channel-specific adapter state
```

The directory contains references and bounded evidence. It does not store private keys or unrestricted component data.

## 7. Safety and Security Boundaries

### 7.1 Privilege boundary

The Node Agent owns the host-facing activation transition.

An operator or orchestration surface submits a validated request.

Channel adapters expose only declared operations:

```text
prepare
activate
accept
rollback
status
```

An adapter does not expose an arbitrary shell command.

### 7.2 Signature and trust boundary

Verification distinguishes:

- transport or offline-bundle envelope signature;
- Release Set signature;
- channel artifact signature;
- signer role and scope;
- recipient and target scope;
- trust epoch;
- revocation;
- expiry and trusted time;
- downgrade floor;
- artifact digest.

A valid envelope does not validate its payloads.

A valid Release Set does not validate every artifact automatically.

A valid artifact does not make it compatible with the node.

### 7.3 Data boundary

Channel adapters use component or lifecycle contracts.

They do not:

- write another component's authoritative database;
- reinterpret another component's migration;
- merge backup ownership;
- use direct SQL as a release-control interface;
- transfer policy authority to Resource Governor;
- transfer source-data ownership to Publication Gateway or an importer.

### 7.4 Secret boundary

Activation state contains references to credentials and keys, never their values.

Private keys remain in their custody boundary.

The transaction directory uses restrictive permissions.

Logs redact bearer credentials, private keys, secret environment values, protected subject content, and private consent or trust evidence.

### 7.5 Offline media boundary

Removable media is treated as an untrusted carrier.

The bundle enters quarantine before parsing and verification.

Mount options, parser limits, path normalization, compression limits, file-count limits, extraction limits, and cleanup follow the offline-bundle contract.

## 8. Resource Envelope

Release activation receives a declared resource envelope.

The envelope accounts for:

- quarantine bytes;
- extracted payload bytes;
- staged artifact bytes;
- duplicate active and previous-known-good images;
- database checkpoint or backup bytes;
- transaction and evidence bytes;
- migration CPU, memory, and I/O;
- service overlap during blue/green or canary operation;
- reboot and recovery time;
- queue growth during maintenance.

Resource pressure behavior:

1. stop optional indexing, enrichment, media, and advisory work;
2. preserve authoritative component data;
3. preserve receipts, replay, and recovery material;
4. stop new import and staging before critical free-space thresholds;
5. retain the current active state;
6. report constrained or unavailable activation readiness.

Capacity does not substitute for trust, policy, compatibility, or migration safety.

## 9. Activation Plan Model

### 9.1 Purpose

The activation plan is a derived operational control.

It binds one transaction to:

- one target profile;
- one Release Set identity;
- one source route;
- one selected channel scope;
- one step per channel;
- exact artifact identities and digests;
- dependency order;
- acceptance checks;
- reboot boundaries;
- rollback floors;
- migration identities;
- forward-repair identities for irreversible steps.

It does not replace the Release Set or artifact manifests.

### 9.2 Dependency graph

The plan uses an acyclic dependency graph.

The order is not inferred from channel names.

Examples of valid reasons for an edge include:

- a service requires a newer policy contract;
- a Runtime Pack requires a service query contract;
- a system image must precede a service artifact;
- a migration requires both old and new service compatibility;
- a reboot must occur before a post-boot acceptance step.

The illustrative plan below is not a canonical default order.

### 9.3 Illustrative plan

```json
{
  "schema_version": "1.0.0",
  "transaction_id": "release-20260803-001",
  "target_profile": "sovereign_linux_node",
  "activation_scope": "release_set",
  "release_set": {
    "id": "koa-release-set:2026.08.03.1",
    "version": "2026.08.03.1",
    "digest": "sha256:1111111111111111111111111111111111111111111111111111111111111111"
  },
  "source": {
    "kind": "offline_bundle",
    "reference": "offline-bundle:2026.08.03.1",
    "carrier_id": "carrier:verified-transfer-01"
  },
  "maintenance_window": {
    "starts_at": "2026-08-04T01:00:00Z",
    "ends_at": "2026-08-04T03:00:00Z"
  },
  "operator_receipt_ref": "receipt:maintenance-approval-20260803-01",
  "steps": [
    {
      "step_id": "activate-governance",
      "channel": "governance",
      "artifact": {
        "id": "governance-policy-bundle:2026.08.03.1",
        "version": "2026.08.03.1",
        "digest": "sha256:2222222222222222222222222222222222222222222222222222222222222222"
      },
      "depends_on": [],
      "acceptance_checks": [
        "contract",
        "identity_trust",
        "policy",
        "representative_behavior",
        "receipts"
      ],
      "requires_reboot": false,
      "reversible": true,
      "rollback_floor": "governance-policy-bundle:2026.07.20.2",
      "migration_ids": []
    },
    {
      "step_id": "activate-knowledge",
      "channel": "knowledge",
      "artifact": {
        "id": "knowledge-release:2026.08.03.1",
        "version": "2026.08.03.1",
        "digest": "sha256:3333333333333333333333333333333333333333333333333333333333333333"
      },
      "depends_on": [
        "activate-governance"
      ],
      "acceptance_checks": [
        "contract",
        "data",
        "local_read",
        "representative_behavior"
      ],
      "requires_reboot": false,
      "reversible": true,
      "rollback_floor": "knowledge-release:2026.07.28.1",
      "migration_ids": []
    },
    {
      "step_id": "activate-services",
      "channel": "services",
      "artifact": {
        "id": "service-bundle:2026.08.03.1",
        "version": "2026.08.03.1",
        "digest": "sha256:4444444444444444444444444444444444444444444444444444444444444444"
      },
      "depends_on": [
        "activate-governance",
        "activate-knowledge"
      ],
      "acceptance_checks": [
        "startup",
        "contract",
        "dependencies",
        "data",
        "policy",
        "local_read",
        "write",
        "representative_behavior",
        "receipts"
      ],
      "requires_reboot": false,
      "reversible": true,
      "rollback_floor": "service-bundle:2026.07.28.3",
      "migration_ids": [
        "migration:services-20260803-01"
      ]
    },
    {
      "step_id": "activate-system",
      "channel": "system",
      "artifact": {
        "id": "system-image:2026.08.03.1",
        "version": "2026.08.03.1",
        "digest": "sha256:5555555555555555555555555555555555555555555555555555555555555555"
      },
      "depends_on": [
        "activate-services"
      ],
      "acceptance_checks": [
        "boot",
        "startup",
        "contract",
        "dependencies",
        "data",
        "identity_trust",
        "policy",
        "local_read",
        "write",
        "execution",
        "recovery",
        "representative_behavior",
        "receipts"
      ],
      "requires_reboot": true,
      "reversible": true,
      "rollback_floor": "system-image:2026.07.15.2",
      "migration_ids": []
    }
  ],
  "notes": "Illustrative order only; the accepted Release Set and migration graph own the real order."
}
```

### 9.4 Reference plan validator

The following validator is a reference implementation for development, test, recovery rehearsal, or a profile-selected equivalent. Production installation belongs to a signed system or service artifact.

```python
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

CHANNELS = {"system", "services", "governance", "knowledge"}
SOURCE_KINDS = {"offline_bundle", "local_registry", "verified_transfer"}
ACCEPTANCE_CHECKS = {
    "startup",
    "boot",
    "contract",
    "dependencies",
    "data",
    "identity_trust",
    "policy",
    "local_read",
    "write",
    "execution",
    "background_work",
    "recovery",
    "representative_behavior",
    "receipts",
}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
TRANSACTION_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{2,95}$")


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read activation plan {path}: {exc}")
    if not isinstance(value, dict):
        fail("activation plan root must be an object")
    return value


def require_exact_keys(
    value: dict[str, Any],
    required: set[str],
    optional: set[str],
    context: str,
) -> None:
    missing = required - set(value)
    extra = set(value) - required - optional
    if missing:
        fail(f"{context} is missing keys: {sorted(missing)}")
    if extra:
        fail(f"{context} has unsupported keys: {sorted(extra)}")


def text(value: Any, context: str, pattern: re.Pattern[str] | None = None) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{context} must be a non-empty string")
    if pattern is not None and not pattern.fullmatch(value):
        fail(f"{context} has an invalid value: {value}")
    return value


def boolean(value: Any, context: str) -> bool:
    if not isinstance(value, bool):
        fail(f"{context} must be a boolean")
    return value


def validate_artifact(value: Any, context: str) -> dict[str, str]:
    if not isinstance(value, dict):
        fail(f"{context} must be an object")
    require_exact_keys(
        value,
        {"id", "version", "digest"},
        {"channel_manifest_ref"},
        context,
    )
    artifact_id = text(value["id"], f"{context}.id", ID_PATTERN)
    version = text(value["version"], f"{context}.version", ID_PATTERN)
    digest = text(value["digest"], f"{context}.digest", DIGEST_PATTERN)
    result = {
        "id": artifact_id,
        "version": version,
        "digest": digest,
    }
    if "channel_manifest_ref" in value:
        result["channel_manifest_ref"] = text(
            value["channel_manifest_ref"],
            f"{context}.channel_manifest_ref",
        )
    return result


def topological_order(steps: list[dict[str, Any]]) -> list[str]:
    step_ids = {step["step_id"] for step in steps}
    dependencies = {
        step["step_id"]: set(step["depends_on"])
        for step in steps
    }

    for step_id, values in dependencies.items():
        unknown = values - step_ids
        if unknown:
            fail(
                f"step {step_id} depends on unknown steps: "
                f"{sorted(unknown)}"
            )
        if step_id in values:
            fail(f"step {step_id} depends on itself")

    ready = sorted(
        step_id
        for step_id, values in dependencies.items()
        if not values
    )
    order: list[str] = []

    while ready:
        current = ready.pop(0)
        order.append(current)

        for step_id in sorted(dependencies):
            if current in dependencies[step_id]:
                dependencies[step_id].remove(current)
                if (
                    not dependencies[step_id]
                    and step_id not in order
                    and step_id not in ready
                ):
                    ready.append(step_id)
                    ready.sort()

    if len(order) != len(steps):
        remaining = sorted(set(step_ids) - set(order))
        fail(f"activation dependency cycle detected: {remaining}")

    return order


def validate(plan: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    require_exact_keys(
        plan,
        {
            "schema_version",
            "transaction_id",
            "target_profile",
            "activation_scope",
            "release_set",
            "source",
            "steps",
        },
        {
            "maintenance_window",
            "operator_receipt_ref",
            "notes",
        },
        "activation plan",
    )

    if plan["schema_version"] != "1.0.0":
        fail("schema_version must be 1.0.0")

    transaction_id = text(
        plan["transaction_id"],
        "transaction_id",
        TRANSACTION_PATTERN,
    )

    if plan["target_profile"] != "sovereign_linux_node":
        fail("target_profile must be sovereign_linux_node")

    if plan["activation_scope"] not in {
        "release_set",
        "channel_subset",
    }:
        fail(
            "activation_scope must be release_set or channel_subset"
        )

    release_set = plan["release_set"]
    if not isinstance(release_set, dict):
        fail("release_set must be an object")
    require_exact_keys(
        release_set,
        {"id", "version", "digest"},
        set(),
        "release_set",
    )
    release_set_id = text(
        release_set["id"],
        "release_set.id",
        ID_PATTERN,
    )
    release_set_version = text(
        release_set["version"],
        "release_set.version",
        ID_PATTERN,
    )
    release_set_digest = text(
        release_set["digest"],
        "release_set.digest",
        DIGEST_PATTERN,
    )

    source = plan["source"]
    if not isinstance(source, dict):
        fail("source must be an object")
    require_exact_keys(
        source,
        {"kind", "reference"},
        {"carrier_id"},
        "source",
    )
    if source["kind"] not in SOURCE_KINDS:
        fail(f"unsupported source kind: {source['kind']}")
    text(source["reference"], "source.reference")
    if "carrier_id" in source:
        text(source["carrier_id"], "source.carrier_id", ID_PATTERN)

    steps = plan["steps"]
    if not isinstance(steps, list) or not steps:
        fail("steps must be a non-empty array")

    validated_steps: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_channels: set[str] = set()

    for index, step in enumerate(steps):
        context = f"steps[{index}]"
        if not isinstance(step, dict):
            fail(f"{context} must be an object")
        require_exact_keys(
            step,
            {
                "step_id",
                "channel",
                "artifact",
                "depends_on",
                "acceptance_checks",
                "requires_reboot",
                "reversible",
            },
            {
                "forward_repair_id",
                "migration_ids",
                "rollback_floor",
            },
            context,
        )

        step_id = text(
            step["step_id"],
            f"{context}.step_id",
            ID_PATTERN,
        )
        if step_id in seen_ids:
            fail(f"duplicate step_id: {step_id}")
        seen_ids.add(step_id)

        channel = step["channel"]
        if channel not in CHANNELS:
            fail(f"{context}.channel is unsupported: {channel}")
        if channel in seen_channels:
            fail(f"channel appears more than once: {channel}")
        seen_channels.add(channel)

        artifact = validate_artifact(
            step["artifact"],
            f"{context}.artifact",
        )

        depends_on = step["depends_on"]
        if (
            not isinstance(depends_on, list)
            or not all(isinstance(item, str) for item in depends_on)
            or len(depends_on) != len(set(depends_on))
        ):
            fail(
                f"{context}.depends_on must be a unique string array"
            )

        checks = step["acceptance_checks"]
        if (
            not isinstance(checks, list)
            or not checks
            or not all(isinstance(item, str) for item in checks)
            or len(checks) != len(set(checks))
        ):
            fail(
                f"{context}.acceptance_checks must be a "
                "non-empty unique string array"
            )
        unsupported_checks = set(checks) - ACCEPTANCE_CHECKS
        if unsupported_checks:
            fail(
                f"{context}.acceptance_checks contains unsupported "
                f"values: {sorted(unsupported_checks)}"
            )

        requires_reboot = boolean(
            step["requires_reboot"],
            f"{context}.requires_reboot",
        )
        reversible = boolean(
            step["reversible"],
            f"{context}.reversible",
        )

        if requires_reboot and channel != "system":
            fail(
                f"{context}.requires_reboot is permitted only "
                "for the system channel"
            )

        if not reversible and not step.get("forward_repair_id"):
            fail(
                f"{context} is irreversible and requires "
                "forward_repair_id"
            )

        if "forward_repair_id" in step:
            text(
                step["forward_repair_id"],
                f"{context}.forward_repair_id",
                ID_PATTERN,
            )

        migration_ids = step.get("migration_ids", [])
        if (
            not isinstance(migration_ids, list)
            or not all(isinstance(item, str) for item in migration_ids)
            or len(migration_ids) != len(set(migration_ids))
        ):
            fail(
                f"{context}.migration_ids must be a unique "
                "string array"
            )

        if "rollback_floor" in step:
            text(
                step["rollback_floor"],
                f"{context}.rollback_floor",
                ID_PATTERN,
            )

        validated_step = {
            "step_id": step_id,
            "channel": channel,
            "artifact": artifact,
            "depends_on": list(depends_on),
            "acceptance_checks": list(checks),
            "requires_reboot": requires_reboot,
            "reversible": reversible,
            "migration_ids": list(migration_ids),
        }

        if "forward_repair_id" in step:
            validated_step["forward_repair_id"] = step[
                "forward_repair_id"
            ]

        if "rollback_floor" in step:
            validated_step["rollback_floor"] = step[
                "rollback_floor"
            ]

        validated_steps.append(validated_step)

    if (
        plan["activation_scope"] == "release_set"
        and seen_channels != CHANNELS
    ):
        fail(
            "release_set activation must include exactly the "
            "system, services, governance, and knowledge channels"
        )

    order = topological_order(validated_steps)

    canonical = {
        "schema_version": "1.0.0",
        "transaction_id": transaction_id,
        "target_profile": "sovereign_linux_node",
        "activation_scope": plan["activation_scope"],
        "release_set": {
            "id": release_set_id,
            "version": release_set_version,
            "digest": release_set_digest,
        },
        "source": source,
        "steps": validated_steps,
    }

    for optional_key in (
        "maintenance_window",
        "operator_receipt_ref",
        "notes",
    ):
        if optional_key in plan:
            canonical[optional_key] = plan[optional_key]

    return canonical, order


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument(
        "--emit-order",
        action="store_true",
        help="Print one validated step identifier per line",
    )
    parser.add_argument(
        "--emit-canonical",
        action="store_true",
        help="Print normalized validated JSON",
    )
    args = parser.parse_args()

    canonical, order = validate(load(args.plan))

    if args.emit_order:
        print("\n".join(order))
        return

    if args.emit_canonical:
        print(
            json.dumps(
                canonical,
                indent=2,
                sort_keys=True,
            )
        )
        return

    digest = hashlib.sha256(
        json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()

    print(
        json.dumps(
            {
                "result": "pass",
                "transaction_id": canonical["transaction_id"],
                "target_profile": canonical["target_profile"],
                "activation_scope": canonical["activation_scope"],
                "release_set_id": canonical["release_set"]["id"],
                "release_set_version": canonical[
                    "release_set"
                ]["version"],
                "channels": [
                    step["channel"]
                    for step in canonical["steps"]
                ],
                "activation_order": order,
                "canonical_plan_digest": f"sha256:{digest}",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

```

It validates structure, channel uniqueness, full Release Set coverage, artifact digests, reboot constraints, irreversible-step repair identity, acceptance classes, dependency references, and acyclic order.

## 10. Channel Adapter Contract

### 10.1 Invocation

The reference orchestrator invokes:

```text
koa-release-adapter-system
koa-release-adapter-services
koa-release-adapter-governance
koa-release-adapter-knowledge
```

Each adapter receives:

```text
OPERATION PLAN_PATH STEP_ID TRANSACTION_DIRECTORY
```

### 10.2 Prepare

`prepare` verifies that the artifact is already quarantined, independently verified, compatible, and stageable.

It can:

- stage an immutable system deployment without changing the current boot;
- pull or load verified service images by digest into local storage;
- stage a governance policy bundle without selecting it as active;
- stage knowledge artifacts in inactive slots;
- verify migration prerequisites;
- reserve bounded resources;
- record channel-specific evidence.

It does not change active identity.

### 10.3 Activate

`activate` performs the channel-owned switch or requests the next boot identity.

It uses the exact artifact identity from the plan.

For a rebooting system step, activation requests the new boot and returns control so that the orchestrator can record a reboot boundary.

### 10.4 Accept

`accept` runs the channel-specific acceptance contract.

It verifies:

- active artifact identity;
- contract and schema compatibility;
- dependencies;
- data and migration state;
- identity, trust, and policy readiness;
- capability health;
- representative behavior;
- receipts and evidence;
- recovery state.

For a system image, acceptance occurs after boot.

### 10.5 Rollback

`rollback` returns to the recorded previous known-good state only when reversal is valid.

It accounts for:

- schema migrations;
- emitted events;
- policy decisions already receipted;
- data written by new services;
- revocation and security floors;
- artifacts consumed by other channels;
- reboot requirements.

An adapter returns failure when forward repair is required instead.

### 10.6 Status

`status` returns bounded machine-readable state without secret material.

It distinguishes:

```text
absent
verified
staged
activation_requested
active_unaccepted
accepted
rollback_requested
rolled_back
forward_repair_required
failed
```

## 11. Reference Activation Orchestrator

The following orchestrator demonstrates durable transaction state, one global activation lock, validated topological order, adapter dispatch, reboot pause and resume, reverse-order rollback, and forward-repair detection.

Production installation and privilege belong to the active Node Agent and profile artifacts.

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

note() {
  printf '%s\n' "$*"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 ||
    die "required command not found: $1"
}

adapter_for() {
  local channel=$1
  printf 'koa-release-adapter-%s' "$channel"
}

state_update() {
  local state_file=$1
  local status=$2
  local step_id=${3:-}
  local detail=${4:-}

  python3 - \
    "$state_file" \
    "$status" \
    "$step_id" \
    "$detail" <<'PY'
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

state_file = Path(sys.argv[1])
status = sys.argv[2]
step_id = sys.argv[3]
detail = sys.argv[4]

if state_file.exists():
    state = json.loads(state_file.read_text(encoding="utf-8"))
else:
    state = {
        "schema_version": "1.0.0",
        "events": [],
        "completed_steps": [],
        "activated_steps": [],
        "rolled_back_steps": [],
    }

event = {
    "observed_at": datetime.now(timezone.utc)
    .isoformat()
    .replace("+00:00", "Z"),
    "status": status,
}
if step_id:
    event["step_id"] = step_id
if detail:
    event["detail"] = detail

state["status"] = status
state["events"].append(event)

if status == "step_activated" and step_id:
    if step_id not in state["activated_steps"]:
        state["activated_steps"].append(step_id)

if status == "step_accepted" and step_id:
    if step_id not in state["completed_steps"]:
        state["completed_steps"].append(step_id)
    if step_id not in state["activated_steps"]:
        state["activated_steps"].append(step_id)

if status == "step_rolled_back" and step_id:
    if step_id not in state["rolled_back_steps"]:
        state["rolled_back_steps"].append(step_id)

if status == "reboot_pending" and step_id:
    state["pending_reboot_step"] = step_id
elif status == "reboot_accepted":
    state.pop("pending_reboot_step", None)

temporary = state_file.with_suffix(".tmp")
temporary.write_text(
    json.dumps(state, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
os.chmod(temporary, 0o600)
temporary.replace(state_file)
PY
}

state_value() {
  local state_file=$1
  local key=$2

  python3 - "$state_file" "$key" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
key = sys.argv[2]

if not path.exists():
    print("")
    raise SystemExit(0)

value = json.loads(path.read_text(encoding="utf-8")).get(key, "")
if isinstance(value, list):
    if value:
        sys.stdout.write(
            "\n".join(str(item) for item in value) + "\n"
        )
elif value is not None:
    sys.stdout.write(str(value) + "\n")
PY
}

plan_value() {
  local plan_file=$1
  local step_id=$2
  local key=$3

  python3 - "$plan_file" "$step_id" "$key" <<'PY'
import json
import sys
from pathlib import Path

plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
step_id = sys.argv[2]
key = sys.argv[3]

step = next(
    item for item in plan["steps"]
    if item["step_id"] == step_id
)
value = step[key]

if isinstance(value, bool):
    print("true" if value else "false")
elif isinstance(value, list):
    print("\n".join(str(item) for item in value))
elif value is None:
    print("")
else:
    print(value)
PY
}

contains_line() {
  local needle=$1
  shift
  printf '%s\n' "$@" | grep -Fxq "$needle"
}

rollback_steps() {
  local plan_file=$1
  local transaction_dir=$2
  local state_file=$3
  shift 3
  local activated=("$@")
  local index step_id channel reversible adapter

  for ((index=${#activated[@]} - 1; index >= 0; index -= 1)); do
    step_id=${activated[$index]}
    channel=$(plan_value "$plan_file" "$step_id" channel)
    reversible=$(plan_value "$plan_file" "$step_id" reversible)
    adapter=$(adapter_for "$channel")

    if test "$reversible" != "true"; then
      state_update \
        "$state_file" \
        "forward_repair_required" \
        "$step_id" \
        "activated step is not reversible"
      return 1
    fi

    if ! "$adapter" rollback "$plan_file" "$step_id" "$transaction_dir"; then
      state_update \
        "$state_file" \
        "forward_repair_required" \
        "$step_id" \
        "rollback adapter failed"
      return 1
    fi

    state_update "$state_file" "step_rolled_back" "$step_id"
  done

  state_update "$state_file" "rolled_back"
}

main() {
  require_command python3
  require_command sha256sum
  require_command flock

  local mode=start
  if test "${1:-}" = "--resume"; then
    mode=resume
    shift
  fi

  local plan_input=${1:-}
  local state_root=${2:-}

  test -n "$plan_input" && test -n "$state_root" ||
    die "usage: koa-release-activate [--resume] PLAN STATE_ROOT"

  plan_input=$(realpath "$plan_input")
  state_root=$(realpath -m "$state_root")

  test -f "$plan_input" ||
    die "activation plan not found: $plan_input"

  local checker=${KOA_RELEASE_PLAN_CHECK:-koa-release-plan-check}
  require_command "$checker"

  "$checker" "$plan_input" >/dev/null

  local transaction_id
  transaction_id=$(
    python3 - "$plan_input" <<'PY'
import json
import sys
from pathlib import Path
print(
    json.loads(
        Path(sys.argv[1]).read_text(encoding="utf-8")
    )["transaction_id"]
)
PY
  )

  local transaction_dir="$state_root/$transaction_id"
  local state_file="$transaction_dir/transaction-state.json"
  local plan_file="$transaction_dir/activation-plan.json"
  local order_file="$transaction_dir/activation-order.txt"
  local lock_file="$state_root/.activation.lock"

  mkdir -p "$state_root"
  chmod 700 "$state_root"

  exec 9>"$lock_file"
  flock -n 9 ||
    die "another release activation transaction is running"

  if test "$mode" = "start"; then
    test ! -e "$transaction_dir" ||
      die "transaction directory already exists: $transaction_dir"

    mkdir -p "$transaction_dir/logs" "$transaction_dir/evidence"
    chmod 700 "$transaction_dir"

    "$checker" "$plan_input" --emit-canonical >"$plan_file"
    "$checker" "$plan_file" --emit-order >"$order_file"

    chmod 600 "$plan_file" "$order_file"

    sha256sum "$plan_file" >"$transaction_dir/activation-plan.sha256"
    chmod 600 "$transaction_dir/activation-plan.sha256"

    state_update "$state_file" "validated"
  else
    test -d "$transaction_dir" ||
      die "transaction directory not found: $transaction_dir"
    test -f "$plan_file" && test -f "$state_file" ||
      die "transaction state is incomplete"
    (
      cd "$transaction_dir"
      sha256sum --check activation-plan.sha256
    ) >/dev/null
  fi

  mapfile -t order <"$order_file"
  mapfile -t completed < <(
    state_value "$state_file" completed_steps
  )
  mapfile -t activated < <(
    state_value "$state_file" activated_steps
  )

  local pending_reboot
  pending_reboot=$(
    state_value "$state_file" pending_reboot_step
  )

  if test "$mode" = "resume"; then
    test -n "$pending_reboot" ||
      die "transaction has no pending reboot step"

    local pending_channel pending_adapter
    pending_channel=$(
      plan_value "$plan_file" "$pending_reboot" channel
    )
    pending_adapter=$(adapter_for "$pending_channel")
    require_command "$pending_adapter"

    state_update \
      "$state_file" \
      "reboot_acceptance_started" \
      "$pending_reboot"

    if ! "$pending_adapter" \
      accept \
      "$plan_file" \
      "$pending_reboot" \
      "$transaction_dir"; then
      state_update \
        "$state_file" \
        "acceptance_failed" \
        "$pending_reboot" \
        "post-reboot acceptance failed"

      if ! rollback_steps \
        "$plan_file" \
        "$transaction_dir" \
        "$state_file" \
        "${activated[@]}"; then
        die "post-reboot acceptance failed; forward repair is required"
      fi

      die "post-reboot acceptance failed; activated steps were rolled back"
    fi

    state_update \
      "$state_file" \
      "reboot_accepted" \
      "$pending_reboot"
    state_update \
      "$state_file" \
      "step_accepted" \
      "$pending_reboot"

    completed+=("$pending_reboot")
    if ! contains_line "$pending_reboot" "${activated[@]}"; then
      activated+=("$pending_reboot")
    fi
  fi

  local step_id channel adapter requires_reboot

  for step_id in "${order[@]}"; do
    if contains_line "$step_id" "${completed[@]}"; then
      continue
    fi

    channel=$(plan_value "$plan_file" "$step_id" channel)
    adapter=$(adapter_for "$channel")
    requires_reboot=$(
      plan_value "$plan_file" "$step_id" requires_reboot
    )

    require_command "$adapter"

    state_update "$state_file" "step_prepare_started" "$step_id"
    if ! "$adapter" prepare "$plan_file" "$step_id" "$transaction_dir"; then
      state_update \
        "$state_file" \
        "prepare_failed" \
        "$step_id"
      rollback_steps \
        "$plan_file" \
        "$transaction_dir" \
        "$state_file" \
        "${activated[@]}" || true
      die "prepare failed for step $step_id"
    fi
    state_update "$state_file" "step_prepared" "$step_id"

    state_update "$state_file" "step_activation_started" "$step_id"
    if ! "$adapter" activate "$plan_file" "$step_id" "$transaction_dir"; then
      state_update \
        "$state_file" \
        "activation_failed" \
        "$step_id"
      rollback_steps \
        "$plan_file" \
        "$transaction_dir" \
        "$state_file" \
        "${activated[@]}" || true
      die "activation failed for step $step_id"
    fi

    if ! contains_line "$step_id" "${activated[@]}"; then
      activated+=("$step_id")
    fi

    state_update "$state_file" "step_activated" "$step_id"

    if test "$requires_reboot" = "true"; then
      state_update "$state_file" "reboot_pending" "$step_id"
      note "release activation paused for reboot"
      note "transaction: $transaction_id"
      note "after the node boots into the requested system state, run:"
      note "  koa-release-activate --resume '$plan_input' '$state_root'"
      exit 75
    fi

    state_update "$state_file" "step_acceptance_started" "$step_id"
    if ! "$adapter" accept "$plan_file" "$step_id" "$transaction_dir"; then
      state_update \
        "$state_file" \
        "acceptance_failed" \
        "$step_id"
      if ! rollback_steps \
        "$plan_file" \
        "$transaction_dir" \
        "$state_file" \
        "${activated[@]}"; then
        die "acceptance failed for $step_id; forward repair is required"
      fi
      die "acceptance failed for $step_id; activated steps were rolled back"
    fi

    state_update "$state_file" "step_accepted" "$step_id"
    completed+=("$step_id")
  done

  state_update "$state_file" "accepted"
  note "release activation accepted"
  note "transaction: $transaction_id"
  note "state: $state_file"
}

main "$@"

```

The orchestrator intentionally knows nothing about system-image, service, governance, or knowledge internals. Those semantics remain in the adapters.

## 12. Procedure

### Step 1 — Open the maintenance transaction

**Objective**

Create one attributable activation request without changing active state.

**Actions**

1. authenticate the operator;
2. verify maintenance or emergency authority;
3. record target node identity and profile;
4. record Release Set identity;
5. reserve the maintenance window;
6. record current active and previous known-good identities;
7. obtain the request receipt;
8. verify that no activation, restore, trust recovery, or incompatible migration is running.

**Expected result**

The request is authorized and the node remains on its current active state.

### Step 2 — Establish local recovery

**Objective**

Ensure recovery remains available if activation fails.

**Actions**

- verify recovery environment bootability;
- verify local console or profile-approved remote recovery;
- verify previous system deployment;
- verify previous service, policy, and knowledge identities;
- verify trust and time recovery;
- verify transaction and evidence storage;
- verify rollback or forward-repair artifacts.

**Expected result**

Recovery readiness passes for the selected profile.

### Step 3 — Receive the release

**Objective**

Place the candidate source in a non-authoritative import boundary.

**Online-local route**

Use the profile-approved local registry or verified transfer endpoint.

**Offline route**

Copy the signed offline bundle from the untrusted carrier into quarantine.

**Expected result**

The carrier or transfer is recorded. No payload is active or staged.

### Step 4 — Verify the envelope

**Objective**

Validate transport identity before extraction.

**Checks**

- envelope schema;
- sender and recipient;
- signature;
- trust scope;
- revocation;
- time and expiry;
- sequence and replay;
- size and file-count limits;
- encryption recipient;
- path and compression limits.

**Expected result**

The envelope becomes eligible for bounded extraction.

### Step 5 — Verify every payload independently

**Objective**

Establish artifact identity without transferring authority from the envelope.

**Checks**

- artifact-class schema;
- manifest;
- digest;
- signature and signer role;
- release channel;
- target profile;
- revocation and downgrade floor;
- dependencies;
- required artifact contracts;
- protected-content and cultural-rights handling where applicable.

**Expected result**

Each payload receives its own verified or rejected result.

### Step 6 — Validate the Release Set

**Objective**

Confirm that the selected identities form a tested compatible combination.

**Checks**

- Release Set schema;
- Release Set signature;
- target profile;
- exact artifact identities and digests;
- contract and schema ranges;
- hardware and storage prerequisites;
- migrations;
- rollback constraints;
- conformance profiles;
- signer authority;
- no implicit channel activation.

**Expected result**

The Release Set is valid for planning. Current active state remains unchanged.

### Step 7 — Verify node readiness

**Objective**

Confirm that the node can stage and activate safely.

**Checks**

- trusted time;
- trust and revocation freshness;
- local Identity and Trust;
- Governance Policy Runtime;
- Node Agent;
- Audit Broker and evidence storage;
- Resource Governor and activation envelope;
- storage capacity;
- current component health;
- queue and outbox state;
- no conflicting recovery state;
- local backup destination;
- external dependencies required by the plan.

**Expected result**

Activation readiness is either ready, constrained with accepted limits, or blocked with reason codes.

### Step 8 — Stage all selected channels

**Objective**

Prepare each artifact without changing active identity.

**Actions**

For each planned channel, call its adapter `prepare` operation.

**Expected result**

Every selected artifact is staged independently. Staging state identifies the exact artifact and source Release Set.

**Failure behavior**

One staging failure rejects or pauses the candidate transaction. Already staged artifacts remain inactive and can be cleaned independently.

### Step 9 — Validate migrations

**Objective**

Prove that data and event transitions are safe for the selected order.

**Checks**

- current schema;
- target schema;
- expand and contract compatibility where used;
- old and new code coexistence;
- migration checkpoints;
- interruption and resume;
- event and outbox compatibility;
- replay behavior;
- rollback compatibility;
- forward-repair artifact;
- storage requirement;
- representative test data;
- component ownership.

**Expected result**

Every migration has a disposition and evidence.

### Step 10 — Create backup and checkpoint

**Objective**

Preserve recoverable state before the first active transition.

**Actions**

- create profile-required component backups or snapshots;
- verify encryption and recipient;
- verify integrity;
- capture queue, outbox, replay, policy, trust, artifact, and schema state where required;
- restore-test the applicable backup class or verify a current restore test;
- record backup and checkpoint receipts.

**Expected result**

The transaction references a verified recovery point.

### Step 11 — Generate the activation plan

**Objective**

Convert accepted Release Set, artifact, migration, profile, and health facts into one transaction plan.

**Actions**

- select complete Release Set or compatible channel subset;
- assign one step per selected channel;
- add exact artifact identities;
- add dependency edges;
- add acceptance checks;
- add reboot boundary;
- add rollback floors;
- add migration identities;
- add forward-repair identity for irreversible steps;
- record maintenance and operator receipts.

**Expected result**

The plan contains no arbitrary commands or embedded secrets.

### Step 12 — Validate the plan

**Reference command**

```bash
koa-release-plan-check activation-plan.json
koa-release-plan-check activation-plan.json --emit-order
```

**Expected result**

The validator reports a passing plan and deterministic topological order.

**Failure behavior**

Correct the canonical source, migration graph, or generated plan. Do not hand-edit an artifact identity, digest, signer, or rollback floor to force validation.

### Step 13 — Begin activation

**Reference command**

```bash
koa-release-activate   activation-plan.json   /var/lib/koa/release-transactions
```

The actual transaction root belongs to the selected profile and Node Agent contract. The path above is an implementation example.

**Expected result**

The orchestrator creates a durable transaction, prepares and activates steps in validated order, and accepts non-reboot steps.

### Step 14 — Cross a reboot boundary

When a system step requests reboot, the reference orchestrator exits with code `75`.

Before reboot:

- verify the transaction reports `reboot_pending`;
- verify the expected next boot identity;
- verify the previous known-good boot remains selectable;
- flush receipts and transaction state;
- stop new work;
- drain or checkpoint queues according to contract.

After boot:

- enter local recovery if the expected system identity does not start;
- otherwise resume:

```bash
koa-release-activate   --resume   activation-plan.json   /var/lib/koa/release-transactions
```

The Node Agent resolves the transaction from its protected state. An implementation does not rely only on an operator's shell history.

### Step 15 — Run acceptance

Acceptance uses capability-specific checks.

Common checks include:

- active identity matches the planned digest;
- system startup and boot success;
- storage unlock and integrity;
- schema and migration state;
- Identity and Trust readiness;
- Governance Policy Runtime readiness;
- Resource Governor enforcement;
- Audit Broker and receipts;
- local read readiness;
- authoritative write readiness;
- background work;
- publication capability where selected;
- Kristal and language runtime identity;
- Ariane local navigation;
- deterministic UCKK capability;
- offline behavior;
- representative commands, queries, events, and recovery checks.

External AI and external voice remain separate optional integration states.

### Step 16 — Commit active Release Set binding

After every selected channel is accepted:

- record the active channel identities;
- record the Release Set identity and version;
- record the compatibility result;
- record policy and trust epochs;
- record migration completion;
- record acceptance evidence;
- retain previous known-good identities;
- publish bounded local health;
- close the maintenance transaction.

The Release Set binding records compatibility. It does not make the Release Set the owner of channel artifacts.

### Step 17 — Observe the stability interval

The profile defines the stability interval.

During it, monitor:

- repeated service failure;
- storage errors;
- policy decision errors;
- queue growth;
- migration anomalies;
- resource pressure;
- boot or watchdog failures;
- receipt failures;
- integrity drift;
- synchronization behavior;
- protected-content or disclosure incidents.

A stability interval is not a substitute for acceptance. It catches delayed failure after acceptance.

### Step 18 — Clean staging and quarantine

Cleanup occurs only after acceptance or an explicit failure disposition.

Cleanup:

- retains required active and previous-known-good artifacts;
- retains required rollback and recovery material;
- retains receipts and evidence;
- removes rejected or expired quarantine payloads;
- removes superseded staging data when no rollback or investigation needs it;
- preserves component and artifact ownership;
- records deletion evidence where required.

Broad filesystem, container, image, or volume pruning is not used.

## 13. Idempotency

```text
Idempotent: transaction-scoped and conditional
```

The same validated transaction can be resumed when:

- transaction identity is unchanged;
- plan digest matches;
- active and staged identities match recorded state;
- completed adapter operations return their existing result;
- request identities and receipts remain stable;
- no superseding revocation, policy, profile, Release Set, or migration state invalidates the transaction.

A new Release Set, changed artifact digest, changed activation order, changed rollback floor, changed migration graph, or changed target profile creates a new transaction.

Adapters handle repeated calls safely:

| Operation | Idempotency expectation |
| --- | --- |
| `prepare` | Returns the existing staged identity or stages once. |
| `activate` | Returns the existing requested or active identity without repeating irreversible effects. |
| `accept` | Re-runs bounded checks without changing product truth. |
| `rollback` | Returns the existing rollback result or performs one valid reversal. |
| `status` | Read-only. |

The orchestrator does not repeat a completed migration merely because a process restarted.

## 14. Validation

### 14.1 Static validation

Run before staging:

- Release Set schema validation;
- artifact schema validation;
- signature and digest checks;
- profile and overlay checks;
- dependency and compatibility graph;
- migration graph;
- plan validation;
- resource-envelope validation;
- decision closure;
- lock validation;
- exception validation.

### 14.2 Dynamic validation

Run during staging and acceptance:

- active identity;
- health dimensions;
- representative contract tests;
- migration checkpoints;
- queue and outbox tests;
- rollback or forward-repair rehearsal evidence;
- offline behavior;
- recovery access;
- protected-data handling;
- receipt storage.

### 14.3 Negative tests

The release path rejects:

- invalid signature;
- revoked signer;
- wrong recipient;
- wrong profile;
- wrong channel;
- digest substitution;
- downgrade below floor;
- missing channel artifact;
- duplicate channel step;
- cyclic activation plan;
- insufficient storage;
- missing backup;
- missing migration;
- missing forward repair for irreversible work;
- process alive but capability not ready;
- receipt storage failure;
- reboot into wrong identity;
- cross-component direct write;
- external AI dependency in the native critical path;
- untrusted removable media;
- manual active-state editing.

### 14.4 Success criteria

The recipe succeeds when:

- all selected artifacts are independently verified;
- the Release Set is valid for the target;
- all selected channels are staged independently;
- the plan is valid and acyclic;
- backup and recovery readiness pass;
- every activation step reaches accepted;
- active identities exactly match the plan;
- migrations and data ownership pass;
- capability health passes;
- receipts and evidence exist;
- previous known-good state remains available as required;
- no unauthorized downgrade or direct write occurred;
- offline capability remains valid for the selected profile;
- the transaction closes as accepted.

## 15. Failure Handling

| Failure | Safe response |
| --- | --- |
| Envelope verification fails | Keep the candidate quarantined or reject it; do not extract unrestricted payloads. |
| One payload fails | Reject that payload independently; do not infer that other payloads are invalid or valid. |
| Release Set signature fails | Reject the compatibility statement and stop planning. |
| Artifact is valid but incompatible | Keep it inactive and report the exact compatibility reason. |
| Target profile mismatch | Stop before staging. |
| Trust or revocation state is stale | Apply the profile's stricter offline behavior; high-impact activation can remain blocked. |
| Trusted time is uncertain | Block time-sensitive activation or use the declared high-assurance recovery procedure. |
| Storage is insufficient | Stop before staging or backup; preserve active and recovery state. |
| Backup verification fails | Stop before the first active transition. |
| Migration prepare fails | Preserve current active state and migration evidence. |
| Prepare adapter fails | Keep all artifacts inactive; clean only the failed channel's bounded staging. |
| Activate adapter fails | Roll back already activated reversible steps in reverse order. |
| Acceptance fails before reboot | Roll back reversible steps or enter forward repair. |
| Expected boot fails | Use automatic or operator-approved previous known-good boot according to profile. |
| Post-boot acceptance fails | Roll back the system deployment if permitted or enter recovery and forward repair. |
| Governance activation fails | Preserve the previous policy identity and prior decision receipts. |
| Service rollback is data-incompatible | Stop pretending reversal is complete and use forward repair. |
| Knowledge activation fails | Restore the previous accepted artifact slot without rewriting source data. |
| Receipt storage fails | Keep acceptance incomplete for receipt-required transitions. |
| Resource pressure occurs | Pause optional work and activation; preserve authoritative data and recovery material. |
| Offline source becomes unavailable | Continue only with fully verified local inputs; do not substitute an undeclared source. |
| Operator session ends | Durable transaction state remains; resume through the Node Agent after re-authentication. |
| Global activation lock is held | Do not start a second transaction. |
| Unknown adapter state appears | Stop and enter bounded diagnosis; do not reset state manually. |
| Rollback adapter fails | Mark forward repair required and preserve evidence. |
| Security or disclosure incident occurs | Stop activation, isolate affected payloads, preserve evidence, and enter incident response. |

## 16. Rollback and Forward Repair

### 16.1 Rollback trigger

Rollback can follow:

- failed acceptance;
- repeated runtime error beyond a declared threshold;
- verified revocation;
- failed migration checkpoint;
- operator action with required authority;
- incident response;
- wrong active identity;
- recovery test failure.

### 16.2 Rollback authorization

Rollback is governed.

A downgrade below a security, trust, revocation, policy, schema, or compatibility floor uses a separately accepted emergency procedure and visible risk receipt.

### 16.3 Reverse order

For a reversible transaction, rollback runs accepted or active steps in reverse dependency order.

Each adapter verifies that its prior identity remains compatible with current data and dependent channels.

### 16.4 Forward repair

Forward repair is used when:

- a schema is no longer backward-compatible;
- new events cannot be retracted safely;
- policy decisions have already been receipted under the new policy;
- a security floor prohibits downgrade;
- a trust or revocation update cannot be reversed;
- another channel consumed irreversible output;
- rollback itself failed.

The transaction records the required forward-repair identity and remains in a restricted state until repair acceptance passes.

### 16.5 Data restore

Restore is separate from ordinary rollback.

It uses:

- verified backup identity;
- isolated restore validation;
- tenant and component ownership;
- encryption;
- schema compatibility;
- migration;
- queue and replay reconciliation;
- representative tests;
- activation acceptance.

Blind file replacement is not used.

## 17. Recovery

Recovery access provides:

- current and previous boot identity;
- Release Set and channel identity inspection;
- transaction-state inspection;
- system rollback;
- service, policy, and knowledge rollback through their owners;
- storage and filesystem diagnostics;
- trusted-time and trust repair;
- backup restore;
- offline bundle import;
- audit and evidence export;
- forward-repair activation.

Recovery does not silently erase tenant data, replace trust roots, select a different Release Set, or broaden authority.

A recovery action emits its own receipt and remains separate from the original activation receipt.

## 18. Offline Behavior

```text
offline_after_verified_local_inputs
```

The entire recipe can run offline when the node has:

- trusted local identity and policy evaluation;
- sufficiently fresh trust and revocation state;
- trusted local time;
- verified Release Set;
- every required artifact;
- every required migration;
- required backup destination;
- local channel adapters;
- local test vectors;
- recovery material;
- sufficient resources.

Offline activation preserves all four channel identities and signer scopes.

Reconnection is not required for acceptance unless an explicit selected capability requires a current remote dependency.

After reconnection, the node verifies peers, time, trust, revocation, policy, destinations, and queued evidence before remote synchronization or publication.

## 19. Observability and Evidence

### 19.1 Health

Expose:

- transaction state;
- selected Release Set;
- selected channel identities;
- quarantine and staging state;
- activation cursor;
- reboot-pending state;
- channel acceptance;
- policy and trust freshness;
- migration state;
- resource pressure;
- rollback availability;
- recovery state;
- denied operations.

Public status remains minimal.

Detailed diagnostics require appropriate authorization.

### 19.2 Logs

Logs include:

- transaction identity;
- step identity;
- channel;
- artifact identity;
- operation;
- result;
- reason code;
- correlation;
- observed time;
- evidence reference.

Logs exclude secret values and protected payloads.

### 19.3 Receipts

Receipts are required for:

- activation authorization;
- envelope and artifact verification where declared;
- staging where declared;
- active identity transition;
- migration completion;
- rollback or forward repair;
- acceptance;
- active Release Set binding;
- recovery.

Frequent health probes do not become activation receipts.

### 19.4 Evidence

Evidence can include:

- signature and trust reports;
- Release Set validation;
- artifact verification;
- target-profile compatibility;
- resource-capacity report;
- backup and restore evidence;
- migration dry-run and checkpoints;
- activation-plan validation;
- adapter logs;
- active-identity verification;
- health and representative tests;
- reboot evidence;
- rollback or repair result;
- final conformance result.

Private trust, identity, consent, cultural-rights, and incident evidence remains protected.

## 20. Cleanup and Retention

Retain according to artifact, profile, evidence, and recovery contracts:

- active artifacts;
- previous known-good artifacts;
- recovery environment;
- active Release Set;
- prior Release Set needed for rollback or history;
- signatures and manifests;
- transaction state;
- activation and recovery receipts;
- required migration evidence;
- required backup;
- revocation and downgrade evidence.

Remove only after disposition:

- rejected quarantine payloads;
- expired transport copies;
- superseded staging duplicates;
- temporary extraction directories;
- non-required transient logs;
- old backups outside retention;
- failed candidate service images outside incident retention.

Do not use broad image, volume, cache, package, or filesystem pruning.

Cleanup remains owner- and class-specific.

## 21. Troubleshooting

### Release Set validates, but one channel artifact does not

Treat the artifact result as authoritative for that payload. The Release Set cannot repair a wrong digest or invalid signature. Reject the transaction or obtain the exact verified artifact.

### Plan validator reports a missing channel

A `release_set` scope requires all four channels. Use `channel_subset` only when the accepted Release Set and compatibility rules permit the subset.

### Plan validator reports a dependency cycle

The migration or compatibility graph is inconsistent. Do not reorder steps manually. Return to the owners of the affected artifacts and migrations.

### Staging succeeds, but activation readiness is blocked

Review health reason codes for trust, policy, data, storage, backup, migration, receipts, or resource state. Staging does not compel activation.

### System activation exits with code 75

The reference orchestrator recorded a reboot boundary. Verify `reboot_pending`, flush state, reboot through the Node Agent, verify the expected boot identity, and resume the same transaction.

### Node boots the previous system image

Inspect boot selection and transaction state. Do not mark the system step accepted. Determine whether the new deployment failed, was not selected, or was rejected by the boot mechanism.

### Service processes run, but acceptance fails

Use capability readiness and representative contract tests. A process or container can be alive while schema, policy, dependencies, writes, receipts, or data behavior is invalid.

### Rollback is refused

The adapter determined that current data, events, policy, trust, or security floors are incompatible with reversal. Enter the declared forward-repair path.

### Governance policy changed outcomes unexpectedly

Keep the candidate unaccepted or restore the previous known-good bundle if safe. Preserve simulation, regression, decision, and receipt evidence. Existing receipts keep their original policy identity.

### Knowledge artifacts load, but local queries fail

Verify artifact contract, query contract, Runtime Pack or language-pack identity, source lineage, resource limits, and runtime compatibility. Restore the prior accepted artifact slot if safe.

### Offline activation cannot verify current revocation

Apply the profile's offline freshness policy. Do not infer that the signer remains valid. High-impact activation can remain blocked until an approved trust update is imported.

### Transaction directory exists after failure

Do not delete it manually. Read `transaction-state.json`, obtain adapter status, preserve evidence, and choose rollback, forward repair, or recovery.

## 22. AI Execution Protocol

An AI agent assisting this recipe:

1. loads the active sovereign Linux profile, overlays, Release Set, artifact classes, release channels, Node Agent contract, health contract, and recovery context;
2. treats the recipe as non-authoritative implementation guidance;
3. verifies exact artifact identities and digests from canonical inputs;
4. never invents activation order, migration, rollback floor, signer, or target profile;
5. never exposes private keys, credentials, trust evidence, protected subject content, or private consent evidence;
6. creates a candidate activation plan only from accepted inputs;
7. runs plan validation before requesting activation;
8. stops on missing, stale, conflicting, revoked, or inapplicable authority;
9. does not invoke arbitrary shell or direct database writes;
10. uses channel adapters through the Node Agent;
11. records reboot boundaries and resumes the same transaction;
12. distinguishes requested, staged, active-unaccepted, accepted, rolled-back, and forward-repair states;
13. reports process liveness separately from capability acceptance;
14. keeps external AI and external voice outside the native critical path;
15. preserves receipts and evidence;
16. presents destructive cleanup or restore actions only through their exact owner procedures.

Suggested execution summary:

```json
{
  "recipe_id": "RECIPE-SOV-001",
  "recipe_version": "1.0.0",
  "target_profile": "sovereign_linux_node",
  "transaction_id": "recorded-at-runtime",
  "release_set_id": "recorded-at-runtime",
  "activation_scope": "recorded-at-runtime",
  "selected_channels": [],
  "staged_channels": [],
  "accepted_channels": [],
  "rollback_channels": [],
  "forward_repair_required": false,
  "reboot_boundary_crossed": false,
  "tests_run": [],
  "receipts": [],
  "result": "pass"
}
```

Runtime values replace the explanatory strings before the summary is retained as evidence.

## 23. Maintenance Checklist

Before activation:

- [ ] The target profile and overlays are active.
- [ ] The operator request and maintenance window are authorized.
- [ ] The Release Set is exact and signed.
- [ ] Every channel artifact is independently verified.
- [ ] Trust, revocation, and time freshness pass.
- [ ] Target hardware and resources pass.
- [ ] Recovery environment is available.
- [ ] Active and previous known-good identities are recorded.
- [ ] Backup and restore evidence pass.
- [ ] Migrations and forward repair are complete.
- [ ] The activation plan is generated from canonical inputs.
- [ ] The plan validator passes.
- [ ] No competing activation, restore, or trust recovery is running.
- [ ] Receipt and private-evidence storage is ready.

During activation:

- [ ] Every adapter prepares its own artifact class.
- [ ] Active identity changes only through the adapter.
- [ ] Reboot boundaries are durably recorded.
- [ ] Capability-specific acceptance runs.
- [ ] Process liveness is not treated as full readiness.
- [ ] Failures preserve the current or previous known-good state.
- [ ] Irreversible failure enters forward repair.
- [ ] Logs contain no secret or protected payload.

After activation:

- [ ] Every selected channel is accepted.
- [ ] Active identities match the plan.
- [ ] The active Release Set binding is recorded.
- [ ] Migration completion is receipted.
- [ ] Health and representative tests pass.
- [ ] Offline capability remains valid.
- [ ] Previous known-good and recovery state remain available.
- [ ] Stability-interval monitoring is active.
- [ ] Quarantine and staging cleanup uses class-specific retention.
- [ ] Evidence is complete.
- [ ] The transaction closes as accepted, rolled back, or forward-repair required.

Review this recipe when any referenced profile, artifact class, release channel, trust rule, health model, Node Agent contract, migration policy, offline-bundle contract, rollback rule, or linked lock changes.
