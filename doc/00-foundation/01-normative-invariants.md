# Normative Invariants

The following invariants define the minimum acceptable form of kOA Linux. A conforming implementation MUST satisfy every invariant that applies to its declared node profile.

## I-01 — Maintained standard kernel

kOA Linux MUST use a standard Linux kernel from a recognized maintenance chain. Product-specific kernel patches MUST be minimal, published, reviewable, and upstreamable or removable.

## I-02 — Immutable operating-system base

The operating-system base MUST be image-built, signed, and replaced atomically. Production nodes MUST NOT depend on undocumented in-place mutation of `/usr` or equivalent system content.

## I-03 — Verified boot and release identity

A node MUST be able to establish the identity of the booted OS image and the active release set. Deployments requiring high assurance SHOULD bind this identity to Secure Boot, measured boot, TPM-backed evidence, or an equivalent hardware root of trust.

## I-04 — Four independent release channels

OS images, service bundles, governance policy bundles, and Kristal artifact channels MUST have independent identities and signatures. A signed Release Set MUST declare tested compatible combinations.

## I-05 — Konnaxion and Orgo are co-principal

Konnaxion and Orgo MUST be represented as principal peer workspaces. Neither may be implemented as an ungoverned administrative submodule of the other.

## I-06 — Kristal is transversal

Kristal MUST remain a shared epistemic foundation, not an operational database, workflow engine, voting system, or UI framework.

## I-07 — One narrow privileged broker

Normal product services MUST NOT run with unrestricted root privilege. Privileged node mutations MUST pass through `koa-node-agent` or an equivalent narrow broker with an allowlisted operation contract.

## I-08 — Policy before privilege

A sensitive operation MUST receive an explicit policy decision before the privileged broker executes it. The decision and operation MUST be correlated and auditable.

## I-09 — Offline minimum capability

Each node profile MUST declare its offline capability envelope. The endpoint profile MUST retain access to active verified knowledge, local identity, local work, policy evaluation, and recovery without a permanent cloud dependency.

## I-10 — Fail closed for authority

Verification failure, ambiguity, expired trust, or incompatible contracts MUST NOT silently produce an authoritative result. The system MUST withhold activation or execution and expose a stable reason code.

## I-11 — Safe degradation by capability

Fail-closed behavior MUST NOT be interpreted as indiscriminate shutdown. The system MUST distinguish consultation, advisory use, publication, and execution. Context MAY remain visible with explicit status while unsafe activation remains blocked.

## I-12 — Atomic activation and known-good rollback

OS images, service bundles, policy bundles, and Runtime Packs MUST support atomic activation or an equivalent no-partial-state guarantee. A last-known-good state MUST be retained according to policy.

## I-13 — Tenant and security-domain separation

Konnaxion, Orgo, Kristal caches, and tenant data MUST be separated by explicit identities, storage boundaries, trust roots, and disclosure policies. Cross-domain sharing MUST use a declared gateway or contract.

## I-14 — Auditable without becoming a panopticon

The system MUST preserve public accountability and confidential evidence as separate disclosure classes. Auditability MUST NOT require indiscriminate exposure of personal or sensitive data.

## I-15 — Content-addressed immutable knowledge identity

Kristal content identity MUST be derived from declared canonical content, not tenant workflow state, UI metadata, or operator-specific storage paths.

## I-16 — AI is bounded and replaceable

AI MAY propose, extract, classify, summarize, translate, or assist. It MUST NOT become the sole correctness path for core civic transformations or directly grant system privilege.

## I-17 — Open interfaces and credible exit

A tenant MUST be exportable into a documented Sovereignty Bundle and restorable on a clean compatible node. Exit tests MUST be performed, not merely documented.

## I-18 — Deterministic receipts

Policy decisions, activations, publications, releases, and critical transitions MUST emit stable machine-readable receipts with input identities, policy identity, outcome, reason codes, and correlation identifiers.

## I-19 — Integration without contamination

External tools MUST be classified as native, annexed, connected, mimicked, or forbidden. Annexed and connected tools MUST be capability-limited and prevented from silently mutating trusted core state.

## I-20 — Reproducibility is a release property

A release MUST record the source, dependencies, build policy, toolchain identity, configuration, and artifact hashes needed to reproduce or independently verify its outputs.
