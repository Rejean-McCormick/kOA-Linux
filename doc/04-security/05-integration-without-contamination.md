# Integration Without Contamination

## 1. Classification

Every external capability is classified as:

- **native** — implemented and governed within the core;
- **annexed** — isolated local component with a declared capability manifest;
- **connected** — external API/system behind an anti-corruption layer;
- **mimicked** — useful interaction pattern reimplemented natively;
- **forbidden** — incompatible with safety, governance, rights, or trust requirements.

## 2. Annex requirements

An annexed component MUST have:

- dedicated identity and storage;
- default-deny network;
- no direct database access to core domains;
- no signing keys;
- declared data classes;
- declared offline and failure behavior;
- explicit update owner;
- bounded resources;
- removable operation without core collapse;
- audit and health integration.

## 3. Connected systems

Connections use an Anti-Corruption Layer that maps external identifiers, states, and errors into kOA contracts. External semantics MUST NOT leak directly into core domain models without review.

## 4. Mimic decision

Mimic rather than annex when the external platform is opaque, structurally dominant, incompatible with offline or tenant boundaries, or would create a second source of governance truth.

## 5. Failure isolation

An optional integration failure MUST degrade its own capability, not prevent local identity, policy evaluation, critical Orgo work, active Kristal consultation, or recovery.

## 6. Manifest

Each integration has a signed manifest declaring mode, owner, version, network, filesystems, data classes, capabilities, dependencies, trust, health, and removal procedure.

## 7. Exit

Core data and governance state MUST remain exportable without the integrated tool. No integration may become an undocumented mandatory intermediary.
