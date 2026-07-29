# Founding Requirements Matrix

This matrix turns the architecture into verifiable requirements. “Evidence” identifies the minimum proof expected from an implementation.

| ID | Requirement | Level | Owner | Verification evidence |
|---|---|---|---|---|
| KOA-FND-001 | Use a maintained standard Linux kernel. | MUST | OS | kernel provenance, support policy, patch inventory |
| KOA-FND-002 | Build and activate an immutable signed OS image. | MUST | OS | image digest/signature, drift test, rollback test |
| KOA-FND-003 | Expose booted image and active Release Set identity. | MUST | Node | status API and boot evidence |
| KOA-FND-004 | Separate OS, service, policy, and Kristal release identities. | MUST | Release | four signed manifests and compatibility test |
| KOA-FND-005 | Bind tested combinations with a signed Release Set. | MUST | Release | schema-valid Release Set and signature |
| KOA-FND-006 | Present Konnaxion and Orgo as co-principal workspaces. | MUST | UX | navigation and failure-isolation test |
| KOA-FND-007 | Keep Konnaxion and Orgo in separate security domains. | MUST | Platform | process, storage, identity, and network isolation tests |
| KOA-FND-008 | Route cross-domain publication through a controlled gateway. | MUST | Publication | no direct DB access; redaction/disclosure tests |
| KOA-FND-009 | Keep Kristal content identity independent of tenant workflow state. | MUST | Kristal | canonicalization vectors and tenant comparison test |
| KOA-FND-010 | Verify Runtime Pack signature, inventory, compatibility, and channel before activation. | MUST | Kristal/Node | negative and positive conformance vectors |
| KOA-FND-011 | Activate Runtime Packs atomically and retain last-known-good. | MUST | Node | crash-injection and rollback test |
| KOA-FND-012 | Prevent unauthorized downgrade and substitution. | MUST | Node/Kristal | downgrade and same-release/different-artifact tests |
| KOA-FND-013 | Maintain declared minimum capability without Internet. | MUST | Profile owners | cable-pull test and offline acceptance suite |
| KOA-FND-014 | Deny authority when required verification is unavailable. | MUST | All | fail-closed reason-code tests |
| KOA-FND-015 | Preserve safe labeled context where policy permits. | MUST | UX/Kristal | capability-degradation matrix test |
| KOA-FND-016 | Use one narrow normal privileged broker. | MUST | Node | privilege map and arbitrary-command rejection |
| KOA-FND-017 | Require policy decision binding for sensitive node operations. | MUST | Policy/Node | replay, expiry, caller, and decision-binding tests |
| KOA-FND-018 | Emit decision and operation receipts. | MUST | Policy/Node/Audit | schema validation and correlation test |
| KOA-FND-019 | Evaluate required policies locally and deterministically. | MUST | Policy | offline deterministic vector suite |
| KOA-FND-020 | Activate Governance Policy Bundles atomically with rollback. | MUST | Policy/Node | bundle verification and rollback test |
| KOA-FND-021 | Prevent root access from becoming the ordinary governance API. | MUST | Platform | interface review and privileged-path audit |
| KOA-FND-022 | Use rootless containers for application services where feasible. | SHOULD | Platform | runtime identity and capability inspection |
| KOA-FND-023 | Apply default-deny network policy across domains. | MUST | Network | network reachability matrix |
| KOA-FND-024 | Bound retries, queues, timeouts, and resources. | MUST | Services | fault injection and retry-storm test |
| KOA-FND-025 | Preserve public audit and private evidence as separate classes. | MUST | Audit | disclosure and access-control tests |
| KOA-FND-026 | Audit access to restricted evidence. | MUST | Audit | read-access receipt test |
| KOA-FND-027 | Keep secrets out of images, logs, receipts, and ordinary exports. | MUST | Security | secret scan and export inspection |
| KOA-FND-028 | Scope trust roots by tenant, environment, channel, and artifact class. | MUST | Trust | cross-scope rejection tests |
| KOA-FND-029 | Support signed offline revocation and trust updates. | MUST | Trust/Node | disconnected revocation test |
| KOA-FND-030 | Treat AI output as untrusted candidate input. | MUST | AI/Applications | direct-authority negative tests |
| KOA-FND-031 | Enforce AI data capabilities at mount/network/API boundaries. | MUST | AI/Platform | restricted-data isolation test |
| KOA-FND-032 | Preserve baseline and advisory readings where weighted civic results exist. | MUST | Konnaxion | result and explanation API tests |
| KOA-FND-033 | Never map SmartVote/EkoH directly to Linux privilege. | MUST | Konnaxion/Node | authorization architecture test |
| KOA-FND-034 | Enforce cultural rights and consent at every access boundary. | MUST | Rights/Applications | read, export, AI, sync, and withdrawal tests |
| KOA-FND-035 | Build audience-scoped or encrypted artifacts for restricted content. | SHOULD | Kristal/Distribution | artifact inventory and audience test |
| KOA-FND-036 | Classify every external integration. | MUST | Integration owner | signed integration manifest |
| KOA-FND-037 | Remove an optional integration without core failure. | MUST | Integration owner | removal and degraded-operation test |
| KOA-FND-038 | Use Transactional Outbox when local commit emits external events. | MUST where applicable | Product owners | transaction/failure injection test |
| KOA-FND-039 | Make consumers idempotent and poison messages reviewable. | MUST | Messaging | duplicate and dead-letter tests |
| KOA-FND-040 | Declare irreversible migrations and provide forward repair. | MUST | Data owner | migration plan and interrupted-run test |
| KOA-FND-041 | Encrypt sensitive durable state at rest. | MUST | Platform/Data | storage inspection and key-loss behavior |
| KOA-FND-042 | Provide signed offline import with quarantine. | MUST | Node | malicious media and parser-limit suite |
| KOA-FND-043 | Provide encrypted backup and verified restore. | MUST | Operations | scheduled clean restore result |
| KOA-FND-044 | Export a documented Sovereignty Bundle. | MUST | Product/Operations | schema/inventory verification |
| KOA-FND-045 | Restore a Sovereignty Bundle without the original operator. | MUST | Operations | independent clean-node exit test |
| KOA-FND-046 | Provide a separate recoverable boot target. | MUST | OS/Node | recovery-entry and action tests |
| KOA-FND-047 | Govern and receipt break-glass actions. | MUST | Policy/Node/Audit | expiry and post-review tests |
| KOA-FND-048 | Preserve local critical audit capture during network loss. | MUST | Audit | network-loss and storage-pressure tests |
| KOA-FND-049 | Produce SBOM, provenance, and conformance evidence for releases. | SHOULD | Release | release evidence bundle |
| KOA-FND-050 | Record and expose implementation exceptions through ADRs. | MUST | Architecture | ADR review and exception inventory |
