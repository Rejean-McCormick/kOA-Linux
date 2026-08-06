# kOA Node Agent

The kOA Node Agent is the node-local owner of privileged-operation execution state, staging state, activation and recovery execution state, idempotency records, and node-operation receipts. It is a narrow broker, not a general administration service.

This bundle establishes only the component metadata, Rust crate, strict configuration, process entry point, bootstrap, health/readiness evaluation, and receipt primitives. Domain requests, validation, ports, adapters, broker operations, host backends, sockets, packaging, and integration/security tests belong to later bundles.

## Authority boundary

The Node Agent may reject a request after final node-local validation. It may not invent or replace:

- caller or signer identity;
- governance authorization;
- profile membership or implementation selection;
- artifact class, manifest, release compatibility, or recovery strategy;
- Resource Governor admission;
- Audit Broker disclosure policy;
- application-component authoritative state.

A control-plane request is never sufficient authority. Root identity is an execution property, not application governance authority.

## Closed public surface

The registered command interfaces are:

- `execute_node_operation`;
- `cancel_node_operation`;
- `acknowledge_recovery_result`.

The registered queries are:

- `get_node_agent_capabilities`;
- `get_node_operation_status`;
- `get_node_agent_health`.

Bundle B-0039 does not execute these commands. It exposes only local process commands for `describe`, `check-config`, `health`, and `readiness`. There is no shell, generic service-manager, generic file-transfer, package-manager, container, device, or private-key interface.

## Configuration

Configuration is read from an optional absolute TOML path with one `[koa_node_agent]` table and from the closed `KOA_NODE_AGENT_*` environment namespace. Unknown keys and unknown prefixed environment variables are rejected. Secret-like configuration names are prohibited.

The default configuration is intentionally fail-closed:

- no operation class is profile-enabled;
- external authority and verification dependencies are unavailable;
- receipt and idempotency stores are unavailable;
- staging capacity and resource pressure are unknown;
- recovery is unavailable.

Example for local validation only:

```toml
[koa_node_agent]
profile_context_ref = "contracts/profiles/sovereign-linux-node.profile.json"
enabled_operation_classes = ["inspect_node_state"]
identity_verification_mode = "available"
profile_validation_mode = "available"
policy_runtime_mode = "unavailable"
artifact_verification_mode = "unavailable"
resource_envelope_mode = "available"
control_plane_mode = "unavailable"
receipt_store_mode = "durable"
idempotency_store_mode = "durable"
staging_capacity_state = "available"
recovery_path_state = "verified"
resource_pressure_state = "normal"
```

Enabling a class in configuration does not authorize an operation. It only records profile-resolved availability. Runtime request validation remains responsible for identity, policy, expected state, artifacts, compatibility, resource admission, replay protection, timeout, and recovery readiness.

## Health and readiness

Health output is bounded and contains no secrets, private keys, application data, or authority-bearing payloads. It reports the contract-owned fields:

- component state;
- enabled and blocked operation classes;
- active request and operation in the authenticated operational view;
- staging capacity;
- receipt and idempotency store state;
- artifact verification and recovery state;
- resource pressure;
- last successful critical transition time.

Loss of the control plane preserves existing node-local authority. Loss of identity, profile validation, policy, receipt durability, idempotency durability, artifact verification, resource admission, or recovery readiness blocks the affected operation. There is no silent alternate privileged path.

## Receipts

`NodeOperationReceipt` requires the fields declared in the component contract. Successful critical transitions require a durable receipt path. Receipt identifiers are deterministic correlation fingerprints, not signatures or trust proofs; integrity and signing remain conditioned by the applicable artifact and profile contracts and by the public interface bindings.

Public receipt views omit policy-decision and recovery-token references. Operational views remain secret-free.

## Build and local checks

```text
cargo fmt --check --manifest-path components/koa-node-agent/Cargo.toml
cargo check --manifest-path components/koa-node-agent/Cargo.toml
cargo test --manifest-path components/koa-node-agent/Cargo.toml
```

The crate declares B-0018 through the public `interfaces/rust` Cargo package and contains no private component dependency. These foundational files do not call cross-component APIs; later request and transport bundles consume the generated public bindings.
